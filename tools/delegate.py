#!/usr/bin/env python3
"""Dispatch one briefing to a loopback Light-tier endpoint."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import socket
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Mapping

from local_tier_common import ConfigError, endpoint_healthy, load_config, request_json, validate_loopback_url


ROOT = Path(__file__).resolve().parent.parent

# Task classes map to micro slices built by tools/build.py. "general" keeps the
# universal micro loop for tasks that fit no slice.
TASK_CLASSES = ("bugfix", "investigation", "landing", "general")

# Fail-closed output verification (evals 2026-07-06/10: the light tier fabricated an
# [OBSERVED] test pass a single-shot completion cannot have performed, and returned
# ceremony without the deliverable). A rejected result exits 5 and is recorded
# "rejected" — it must never enter the task record as a usable answer.
#
# Run-claim patterns: first-person execution claims and past-tense pass reports.
# A line is exempt when it is instructing the delegator how to verify (Verify by /
# expect / [UNVERIFIED]) — quoting a command is honest; claiming it ran is not.
RUN_CLAIM_PATTERNS = (
    re.compile(r"(?i)\b(?:i|we)\s+(?:ran|executed|tested|verified|confirmed)\b"),
    re.compile(r"(?i)\btest(?:s)?\s+(?:passed|pass|succeeded|now\s+pass(?:es)?)\b"),
    re.compile(r"(?i)\bnow\s+(?:produces|prints|outputs|passes|works)\b"),
    re.compile(r"(?i)\brunning\s+\S+\s+(?:produces|prints|outputs|shows|confirms)\b"),
    re.compile(r"(?i)\[(?:VERIFIED|OBSERVED)\]\s*(?:via|by)?\s*(?:run|running|test|execution)\b"),
)
# Exemptions: instructing the delegator (Verify by / expect / [UNVERIFIED]) and naming a
# claim in order to reject it (evals 2026-07-09: refutation-quotes are not endorsements).
RUN_CLAIM_EXEMPT = re.compile(
    r"(?i)\[UNVERIFIED\]|verify\s+by|should\s+(?:print|show|output|produce)"
    r"|cannot\s+be\s+verified|unverifiable|claim(?:s|ed)?\b")

CLAIM_TAG = re.compile(r"\[(?:OBSERVED|INFERRED|ASSUMED)[^\]]*\]")

# Per-class deliverable requirements: headings from the slice's output skeleton.
REQUIRED_MARKERS = {
    "bugfix": ("FIX REPORT", "Hypothesis:", "Patch:", "Verify by:"),
    "investigation": ("INVESTIGATION REPORT", "Findings:", "Unknowns:"),
    "landing": ("LANDING AUDIT", "Drive-by hunks:", "Unverifiable claims:", "Verdict:"),
    "general": (),
}


def verify_output(content: str, task_class: str) -> list[str]:
    """Return violations that make a single-shot light-tier result unusable."""
    violations = []
    for line in content.splitlines():
        if RUN_CLAIM_EXEMPT.search(line):
            continue
        for pattern in RUN_CLAIM_PATTERNS:
            if pattern.search(line):
                violations.append(f"run-claim a single-shot completion cannot back: {line.strip()!r}")
                break
    for marker in REQUIRED_MARKERS[task_class]:
        if marker not in content:
            violations.append(f"missing required deliverable marker: {marker!r}")
    if task_class == "bugfix" and "```" not in content:
        violations.append("missing patch: no fenced code block in a bugfix result")
    if not CLAIM_TAG.search(content):
        violations.append("no claim tags ([OBSERVED]/[INFERRED]/[ASSUMED]) — untagged results go back")
    return violations


class DirectoryLock:
    def __init__(self, path: Path, stale_seconds: int):
        self.path = path
        self.stale_seconds = stale_seconds
        self.acquired = False

    def acquire(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.path.mkdir()
            self.acquired = True
            return True
        except FileExistsError:
            age = time.time() - self.path.stat().st_mtime
            if age <= self.stale_seconds:
                return False
            try:
                self.path.rmdir()
                self.path.mkdir()
            except OSError:
                return False
            print(f"stale lock reclaimed ({self.stale_seconds}s timeout)")
            self.acquired = True
            return True

    def release(self) -> None:
        if self.acquired:
            with contextlib.suppress(OSError):
                self.path.rmdir()
            self.acquired = False

    def __enter__(self):
        if not self.acquire():
            raise FileExistsError(self.path)
        return self

    def __exit__(self, *_):
        self.release()


def record_metric(path: Path, task_id: str, model: str, status: str, usage: dict, duration_ms: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "task_id": task_id,
        "model": model,
        "tokens_in": int(usage.get("prompt_tokens", 0)),
        "tokens_out": int(usage.get("completion_tokens", 0)),
        "duration_ms": duration_ms,
        "status": status,
    }
    with path.open("a", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(record, separators=(",", ":")) + "\n")


def dispatch(args, root: Path = ROOT, environ: Mapping[str, str] | None = None) -> int:
    environment = os.environ if environ is None else environ
    briefing = Path(args.briefing)
    task_class = getattr(args, "task_class", "general")
    if task_class == "general":
        micro = root / "adapters" / "system-prompt" / "fablized-micro.md"
    else:
        micro = root / "adapters" / "system-prompt" / f"fablized-micro-{task_class}.md"
    if not briefing.is_file():
        print(f"delegate.py: briefing file not found: {briefing}", file=sys.stderr)
        return 2
    if not micro.is_file():
        print(f"delegate.py: micro prompt missing: {micro} (run tools/build.py)", file=sys.stderr)
        return 2

    try:
        config, config_path = load_config(environ=environment)
        url = validate_loopback_url(config.get("LOCAL_TIER_URL", ""))
        timeout = int(config.get("LOCAL_TIER_TIMEOUT", "300"))
        stale = int(config.get("LOCAL_TIER_LOCK_STALE", "900"))
        if timeout <= 0 or stale <= timeout:
            raise ConfigError("LOCAL_TIER_TIMEOUT must be positive and LOCK_STALE must exceed it")
    except (ConfigError, ValueError) as error:
        print(f"delegate.py: invalid local-tier config: {error}", file=sys.stderr)
        return 2

    model = config.get("LOCAL_TIER_MODEL", "unknown")
    api_key = config.get("LOCAL_TIER_API_KEY", "")
    metrics = Path(environment.get("LOCAL_TIER_METRICS", str(root / "var" / "metrics" / "local-tier.jsonl")))
    lock_path = Path(environment.get("LOCAL_TIER_LOCKDIR", str(root / "var" / "lock" / "local-tier.lock")))
    print(f"health: checking {url}")
    if not endpoint_healthy(url, api_key):
        print(f"[OBSERVED] local tier unreachable: health check failed for {url}.")
        print("Queue this task or escalate per the briefing's Budget & escalation line.")
        return 3

    lock = DirectoryLock(lock_path, stale)
    if not lock.acquire():
        print(f"delegate.py: lock held ({lock_path}) — one task at a time")
        return 4
    try:
        if task_class == "general":
            # Slices carry their own return skeleton; only the universal loop needs one.
            suffix = ("\n\nReturn a concise landing report: outcome; verified observations; "
                      "assumed/unverified; noticed but not done; remaining risk.")
        else:
            suffix = "\n\nReturn exactly the skeleton your instructions define."
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": micro.read_text(encoding="utf-8")},
                {"role": "user", "content": briefing.read_text(encoding="utf-8") + suffix},
            ],
            "temperature": 0.2,
        }
        started = time.monotonic()
        response = None
        for attempt in range(2):
            try:
                response = request_json(url, "/v1/chat/completions", api_key, timeout, payload)
                break
            except OSError:
                if attempt or not endpoint_healthy(url, api_key):
                    break
        duration_ms = int((time.monotonic() - started) * 1000)
        if response is None:
            record_metric(metrics, args.task_id, model, "failed", {}, duration_ms)
            print(f"[OBSERVED] local tier request to {url} failed after one health-gated retry.")
            return 3
        content = response["choices"][0]["message"]["content"]
        usage = response.get("usage", {})
        violations = verify_output(content, task_class)
        if violations:
            record_metric(metrics, args.task_id, model, "rejected", usage, duration_ms)
            print(f"[OBSERVED] light-tier result REJECTED ({len(violations)} violation(s)):")
            for violation in violations:
                print(f"  - {violation}")
            print("\n--- rejected output (do not use as a result) ---")
            print(content)
            print("Re-brief with the missing evidence, or escalate to the capable tier.")
            return 5
        print(content)
        print(
            f"\n---\ntokens_in={usage.get('prompt_tokens', 0)} "
            f"tokens_out={usage.get('completion_tokens', 0)}",
            file=sys.stderr,
        )
        record_metric(metrics, args.task_id, model, "ok", usage, duration_ms)
        return 0
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"delegate.py: invalid endpoint response: {error}", file=sys.stderr)
        return 3
    finally:
        lock.release()


class _MockHandler(BaseHTTPRequestHandler):
    content = "Outcome: OK\nVerified: mock [OBSERVED]"

    def log_message(self, *_):
        pass

    def _send(self, value):
        body = json.dumps(value).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send({"status": "ok"})

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self._send(
            {
                "choices": [{"message": {"content": type(self).content}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 4},
            }
        )


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="delegate-self-test-") as temporary:
        root = Path(temporary)
        micro = root / "adapters" / "system-prompt" / "fablized-micro.md"
        micro.parent.mkdir(parents=True)
        micro.write_text("micro", encoding="utf-8")
        briefing = root / "briefing.md"
        briefing.write_text("## Goal\nSay OK.\n", encoding="utf-8")
        server = ThreadingHTTPServer(("127.0.0.1", 0), _MockHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        port = server.server_address[1]
        args = argparse.Namespace(briefing=str(briefing), task_id="self-test", task_class="general")
        environment = {
            "LOCAL_TIER_URL": f"http://127.0.0.1:{port}",
            "LOCAL_TIER_MODEL": "mock",
            "LOCAL_TIER_API_KEY": "synthetic",
            "LOCAL_TIER_TIMEOUT": "5",
            "LOCAL_TIER_LOCK_STALE": "10",
            "LOCAL_TIER_METRICS": str(root / "metrics.jsonl"),
            "LOCAL_TIER_LOCKDIR": str(root / "lock"),
            "FABLIZED_LOCAL_TIER_ENV": str(root / "missing.env"),
        }
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            status = dispatch(args, root, environment)
        passed = status == 0 and "Verified" in captured.getvalue() and (root / "metrics.jsonl").is_file()
        print("self-test PASS: secure loopback dispatch" if passed else "self-test FAIL: dispatch")

        # Fabricated run-claim must be rejected fail-closed (exit 5, status "rejected").
        _MockHandler.content = ("FIX REPORT\nTest passed: running python test.py now produces "
                                "the expected output [OBSERVED]")
        rejected_out = io.StringIO()
        with contextlib.redirect_stdout(rejected_out):
            rejected_status = dispatch(args, root, environment)
        _MockHandler.content = "Outcome: OK\nVerified: mock [OBSERVED]"
        server.shutdown()
        server.server_close()
        metrics_tail = (root / "metrics.jsonl").read_text(encoding="utf-8").strip().splitlines()[-1]
        rejected_passed = (rejected_status == 5
                           and "REJECTED" in rejected_out.getvalue()
                           and json.loads(metrics_tail)["status"] == "rejected")
        print("self-test PASS: fabricated run-claim rejected" if rejected_passed
              else "self-test FAIL: fabricated run-claim accepted")

        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            down_port = probe.getsockname()[1]
        environment["LOCAL_TIER_URL"] = f"http://127.0.0.1:{down_port}"
        with contextlib.redirect_stdout(io.StringIO()):
            down_status = dispatch(args, root, environment)
        down_passed = down_status == 3
        print("self-test PASS: unreachable endpoint fails closed" if down_passed else "self-test FAIL: down endpoint")

        environment["LOCAL_TIER_URL"] = "https://example.com"
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            remote_status = dispatch(args, root, environment)
        remote_passed = remote_status == 2
        print("self-test PASS: remote endpoint rejected" if remote_passed else "self-test FAIL: remote accepted")
        return 0 if passed and rejected_passed and down_passed and remote_passed else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--briefing")
    parser.add_argument("--task-id", default=f"task-{os.getpid()}")
    parser.add_argument("--task-class", choices=TASK_CLASSES, default="general",
                        help="selects the micro slice; the result is verified against its skeleton")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.briefing:
        parser.error("--briefing is required")
    return dispatch(args)


if __name__ == "__main__":
    raise SystemExit(main())
