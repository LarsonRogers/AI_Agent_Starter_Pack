#!/usr/bin/env python3
"""Cross-platform local-tier discovery and status canary."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import socket
import subprocess
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Mapping

from local_tier_common import ConfigError, endpoint_healthy, load_config, request_json, validate_loopback_url


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROBES = "ollama:11434 llama-server:8080 lm-studio:1234 vllm:8000"


def endpoint_recorded(project_dir: Path) -> bool:
    agents = project_dir / "AGENTS.md"
    if not agents.is_file():
        return False
    return any(
        "local endpoint" in line.lower()
        and re.search(r"http://(?:127\.0\.0\.1|\[::1\])(?::\d+)?(?:/|\s|$)", line)
        for line in agents.read_text(encoding="utf-8").splitlines()
    )


def _models(url: str, name: str) -> str:
    try:
        if name == "ollama":
            payload = request_json(url, "/api/tags", "", 3)
            return ", ".join(model.get("name", "") for model in payload.get("models", []) if model.get("name"))
        payload = request_json(url, "/v1/models", "", 3)
        return ", ".join(model.get("id", "") for model in payload.get("data", []) if model.get("id"))
    except (OSError, ValueError):
        return ""


def discover(project_dir: Path, environ: Mapping[str, str]) -> int:
    if endpoint_recorded(project_dir):
        return 0
    spec = environ.get("CANARY_PROBE_SPEC", DEFAULT_PROBES)
    for item in spec.split():
        name, separator, port = item.partition(":")
        if not separator or not port.isdigit():
            continue
        url = f"http://127.0.0.1:{port}"
        if endpoint_healthy(url, "", 3):
            models = _models(url, name)
            suffix = f", models: {models}" if models else ""
            print(
                f"local tier candidate: {name} at {url}{suffix} — recommend recording it "
                "as the Light tier after user approval; do not write Part 2 silently."
            )
            return 0
    print(
        "ask-once: no local endpoint found — offer a local/cheaper Light tier or record "
        "single-tier after the user's answer."
    )
    return 0


def _temperature() -> int | None:
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
            text=True,
            capture_output=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode:
        return None
    first = result.stdout.splitlines()[0].strip() if result.stdout.splitlines() else ""
    return int(first) if first.isdigit() else None


def status(project_dir: Path, environ: Mapping[str, str]) -> int:
    try:
        config, config_path = load_config(environ=environ)
    except ConfigError:
        return 0
    if not config_path.is_file() and "LOCAL_TIER_URL" not in environ:
        return 0
    try:
        url = validate_loopback_url(config.get("LOCAL_TIER_URL", ""))
    except ConfigError as error:
        print(f"local tier: invalid config ({error})")
        return 0
    model = config.get("LOCAL_TIER_MODEL", "unknown")
    api_key = config.get("LOCAL_TIER_API_KEY", "")
    try:
        configured_minimum = int(config.get("CANARY_MIN_TOKS", "5"))
        maximum_temperature = int(config.get("CANARY_MAX_TEMP", "85"))
        if configured_minimum < 0 or maximum_temperature <= 0:
            raise ValueError
    except ValueError:
        print("local tier: invalid numeric canary configuration")
        return 0
    if not endpoint_healthy(url, api_key, 4):
        print(f"local tier: down ({url})")
        return 0

    warmup = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 1,
    }
    with contextlib.suppress(OSError, ValueError):
        request_json(url, "/v1/chat/completions", api_key, 30, warmup)
    probe = {
        "model": model,
        "messages": [{"role": "user", "content": "Count 1 to 24 as digits separated by spaces."}],
        "max_tokens": 64,
    }
    started = time.monotonic()
    try:
        response = request_json(url, "/v1/chat/completions", api_key, 30, probe)
    except (OSError, ValueError):
        print(f"local tier: up, {model}, completion FAILED")
        return 0
    duration = max(time.monotonic() - started, 0.001)
    tokens = int(response.get("usage", {}).get("completion_tokens", 0))
    temperature = _temperature()
    temperature_text = "n/a" if temperature is None else f"{temperature}C"
    if tokens < 16:
        line = f"local tier: up, {model}, tok/s n/a ({tokens}-token sample), {temperature_text}"
    else:
        tokens_per_second = int(tokens / duration)
        minimum = configured_minimum
        agents = project_dir / "AGENTS.md"
        if agents.is_file():
            model_line = next(
                (line for line in agents.read_text(encoding="utf-8").splitlines() if model in line), ""
            )
            recorded = re.search(r"(\d+)\s+tok/s", model_line)
            if recorded:
                minimum = int(recorded.group(1)) // 2
        line = f"local tier: up, {model}, ~{tokens_per_second} tok/s, {temperature_text}"
        if tokens_per_second < minimum:
            line += f" [WARN: below {minimum} tok/s floor]"
    if temperature is not None and temperature > maximum_temperature:
        line += f" [WARN: over {maximum_temperature}C]"
    print(line)
    return 0


class _DiscoveryHandler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        payload = {"models": [{"name": "mock"}]} if self.path == "/api/tags" else {"status": "ok"}
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="canary-self-test-") as temporary:
        project = Path(temporary)
        (project / "AGENTS.md").write_text("- Local endpoint (if Light is local): [URL]\n", encoding="utf-8")
        server = ThreadingHTTPServer(("127.0.0.1", 0), _DiscoveryHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        port = server.server_address[1]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            discover(project, {"CANARY_PROBE_SPEC": f"ollama:{port}"})
        server.shutdown()
        server.server_close()
        hit = "candidate: ollama" in output.getvalue() and "approval" in output.getvalue()
        print("self-test PASS: dynamic-port discovery" if hit else "self-test FAIL: discovery")

        (project / "AGENTS.md").write_text(
            "- Local endpoint (if Light is local): http://127.0.0.1:9999\n", encoding="utf-8"
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            discover(project, {"CANARY_PROBE_SPEC": f"ollama:{port}"})
        silent = not output.getvalue()
        print("self-test PASS: recorded endpoint is silent" if silent else "self-test FAIL: recorded endpoint")

        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            unused = probe.getsockname()[1]
        (project / "AGENTS.md").write_text("- Local endpoint: [URL]\n", encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            discover(project, {"CANARY_PROBE_SPEC": f"ollama:{unused}"})
        miss = output.getvalue().startswith("ask-once:")
        print("self-test PASS: no endpoint asks once" if miss else "self-test FAIL: zero-hit behavior")
        return 0 if hit and silent and miss else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ROOT))
    if args.self_test:
        return self_test()
    if args.discover:
        return discover(project_dir, os.environ)
    return status(project_dir, os.environ)


if __name__ == "__main__":
    raise SystemExit(main())
