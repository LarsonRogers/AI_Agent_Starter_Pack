#!/usr/bin/env python3
"""Fixture-scoped tool-loop adapter for local-tier eval runs.

Drives an OpenAI-compatible /v1/chat/completions endpoint that returns native
structured tool calls (llama.cpp with a tool-capable template). Emits the JSONL
trace `behavioral_graders.parse_trace` expects: one `tool_use` line per call and
a final `{"type": "result", ...}` line. Endpoint, key, and timeout come from the
same config as tools/delegate.py (`~/.config/fablized/local-tier.env` or
LOCAL_TIER_* environment variables); the loopback-only rule is enforced there.

Confinement: file tools resolve inside the working directory only; shell
commands are argv-executed (no shell) with an allowlisted first token and no
absolute or parent-escaping path arguments.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from local_tier_common import (
    ConfigError, endpoint_healthy, load_config, request_json, validate_loopback_url,
)

MAX_STEPS = 24
MAX_TOKENS = 8192
TEMPERATURE = 0.2
SHELL_TIMEOUT = 120
RESULT_CAP = 4000
SHELL_ALLOW = {
    "python", "python3", "git", "ls", "cat", "head", "tail",
    "grep", "wc", "diff", "pwd", "find",
}
ABSOLUTE_ARG = re.compile(r"^(/|\\|[A-Za-z]:)")

TOOLS = [
    {"type": "function", "function": {
        "name": "shell",
        "description": "Run one verification command (python/git/ls/cat/grep/...) in the "
                       "working directory. No pipes, no redirection, relative paths only.",
        "parameters": {"type": "object", "properties": {
            "command": {"type": "string", "description": "e.g. 'python test_export.py'"},
        }, "required": ["command"]},
    }},
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read a text file (relative path).",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"},
        }, "required": ["path"]},
    }},
    {"type": "function", "function": {
        "name": "write_file",
        "description": "Write full file contents (relative path).",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"},
        }, "required": ["path", "content"]},
    }},
    {"type": "function", "function": {
        "name": "replace_text",
        "description": "Replace one exact text span in a file (relative path).",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"},
            "old_text": {"type": "string"},
            "new_text": {"type": "string"},
        }, "required": ["path", "old_text", "new_text"]},
    }},
    {"type": "function", "function": {
        "name": "list_dir",
        "description": "List a directory (relative path, default '.').",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"},
        }},
    }},
]

HARNESS_NOTE = (
    "You are a coding agent working inside a repository checkout. Use the provided "
    "tools to inspect, run, and edit files. When the task is complete, reply with "
    "your final report as plain text (no tool call)."
)


def emit(record: dict) -> None:
    print(json.dumps(record, ensure_ascii=False), flush=True)


def confine(root: Path, relative: str) -> Path:
    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"path escapes working directory: {relative}")
    return target


def run_shell(root: Path, command: str) -> str:
    try:
        argv = shlex.split(command)
    except ValueError as error:
        return f"error: unparseable command: {error}"
    if not argv:
        return "error: empty command"
    if argv[0] not in SHELL_ALLOW:
        return f"error: command not allowed: {argv[0]} (allowed: {', '.join(sorted(SHELL_ALLOW))})"
    for token in argv[1:]:
        if ".." in token or ABSOLUTE_ARG.match(token):
            return f"error: path argument not allowed: {token}"
    try:
        result = subprocess.run(
            argv, cwd=root, text=True, capture_output=True, timeout=SHELL_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        return f"error: command timed out after {SHELL_TIMEOUT}s"
    except FileNotFoundError:
        return f"error: not found: {argv[0]}"
    output = (result.stdout + result.stderr).strip()
    return f"exit={result.returncode}\n{output}"


def execute(root: Path, name: str, arguments: dict) -> str:
    try:
        if name == "shell":
            return run_shell(root, arguments["command"])
        if name == "read_file":
            return confine(root, arguments["path"]).read_text(encoding="utf-8")
        if name == "write_file":
            target = confine(root, arguments["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(arguments["content"], encoding="utf-8", newline="\n")
            return f"wrote {arguments['path']}"
        if name == "replace_text":
            target = confine(root, arguments["path"])
            text = target.read_text(encoding="utf-8")
            old = arguments["old_text"]
            if text.count(old) != 1:
                return f"error: old_text must occur exactly once (found {text.count(old)})"
            target.write_text(text.replace(old, arguments["new_text"]), encoding="utf-8", newline="\n")
            return f"replaced in {arguments['path']}"
        if name == "list_dir":
            target = confine(root, arguments.get("path", "."))
            return "\n".join(sorted(p.name + ("/" if p.is_dir() else "") for p in target.iterdir()))
        return f"error: unknown tool {name}"
    except (OSError, ValueError, KeyError, UnicodeDecodeError) as error:
        return f"error: {type(error).__name__}: {error}"


def final_result_event(message: dict, finish_reason) -> dict:
    """Result event for a final (no-tool-call) turn. An empty deliverable is a known
    failure mode on thinking models: keep enough of the raw message to attribute it
    (finish reason, content shape, reasoning tail)."""
    content = message.get("content") or ""
    reasoning = message.get("reasoning_content") or ""
    event = {
        "type": "result",
        "result": content,
        "finish_reason": finish_reason,
        "reasoning_chars": len(reasoning),
    }
    if not content:
        event["content_type"] = type(message.get("content")).__name__
        event["reasoning_tail"] = reasoning[-2000:]
    return event


def main() -> int:
    # Windows defaults stdout to cp1252; model text (arrows, dashes) must not crash the trace.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--system-prompt-file", required=True)
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    root = Path.cwd().resolve()
    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    system_extra = Path(args.system_prompt_file).read_text(encoding="utf-8").strip()
    system = HARNESS_NOTE + ("\n\n" + system_extra if system_extra else "")

    try:
        config, _ = load_config()
        url = validate_loopback_url(config.get("LOCAL_TIER_URL", ""))
        api_key = config.get("LOCAL_TIER_API_KEY", "")
        timeout = int(config.get("LOCAL_TIER_TIMEOUT", "300"))
    except (ConfigError, ValueError) as error:
        emit({"type": "runner_error", "error": f"local-tier config: {error}"})
        return 2

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    for step in range(MAX_STEPS):
        payload = {
            "model": args.model,
            "messages": messages,
            "tools": TOOLS,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
        }
        # One health-gated retry, as in tools/delegate.py: a live server that dropped
        # one connection gets a second request; a dead one fails closed.
        response = None
        for attempt in range(2):
            try:
                response = request_json(url, "/v1/chat/completions", api_key, timeout, payload)
                break
            except OSError as error:
                last_error = error
                if attempt or not endpoint_healthy(url, api_key):
                    break
        try:
            if response is None:
                raise last_error
            message = response["choices"][0]["message"]
        except (OSError, KeyError, IndexError, TypeError, ValueError) as error:
            emit({"type": "runner_error", "error": f"endpoint: {type(error).__name__}: {error}"})
            return 3
        emit({"type": "turn", "step": step, "usage": response.get("usage", {})})

        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            emit(final_result_event(message, response["choices"][0].get("finish_reason")))
            return 0

        # Replay without reasoning_content: thinking stays out of the next turn's context.
        messages.append({
            "role": "assistant",
            "content": message.get("content") or "",
            "tool_calls": tool_calls,
        })
        for call in tool_calls:
            function = call.get("function", {})
            name = function.get("name", "")
            raw = function.get("arguments", "{}")
            try:
                arguments = raw if isinstance(raw, dict) else json.loads(raw)
            except json.JSONDecodeError:
                arguments = {}
            emit({"type": "tool_use", "name": name, "input": arguments})
            output = execute(root, name, arguments)[:RESULT_CAP]
            emit({"type": "tool_result", "tool": name, "output": output})
            messages.append({
                "role": "tool",
                "tool_call_id": call.get("id", f"call-{step}"),
                "content": output,
            })

    emit({"type": "runner_error", "error": f"step limit reached ({MAX_STEPS})"})
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
