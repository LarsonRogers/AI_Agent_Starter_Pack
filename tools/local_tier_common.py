#!/usr/bin/env python3
"""Shared, cross-platform local-tier configuration and HTTP helpers."""

from __future__ import annotations

import ast
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Mapping


CONFIG_KEYS = {
    "LOCAL_TIER_URL",
    "LOCAL_TIER_MODEL",
    "LOCAL_TIER_API_KEY",
    "LOCAL_TIER_TIMEOUT",
    "LOCAL_TIER_LOCK_STALE",
    "CANARY_MIN_TOKS",
    "CANARY_MAX_TEMP",
}
KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


class ConfigError(ValueError):
    pass


def _parse_value(raw: str, line_number: int) -> str:
    value = raw.strip()
    if not value:
        return ""
    if value[0] in {'"', "'"}:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as error:
            raise ConfigError(f"line {line_number}: invalid quoted value") from error
        if not isinstance(parsed, str):
            raise ConfigError(f"line {line_number}: value must be text")
        return parsed
    return value


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, separator, raw_value = line.partition("=")
        key = key.strip()
        if not separator or not KEY_RE.fullmatch(key):
            raise ConfigError(f"line {line_number}: expected KEY=VALUE")
        if key not in CONFIG_KEYS:
            raise ConfigError(f"line {line_number}: unsupported key {key}")
        values[key] = _parse_value(raw_value, line_number)
    return values


def load_config(
    path: Path | None = None, environ: Mapping[str, str] | None = None
) -> tuple[dict[str, str], Path]:
    environment = os.environ if environ is None else environ
    config_path = path or Path(
        environment.get(
            "FABLIZED_LOCAL_TIER_ENV",
            str(Path.home() / ".config" / "fablized" / "local-tier.env"),
        )
    )
    values = parse_env_file(config_path) if config_path.is_file() else {}
    for key in CONFIG_KEYS:
        if key in environment:
            values[key] = environment[key]
    return values, config_path


def validate_loopback_url(raw_url: str) -> str:
    parsed = urllib.parse.urlsplit(raw_url)
    if parsed.scheme != "http":
        raise ConfigError("LOCAL_TIER_URL must use http on loopback")
    if parsed.hostname not in {"127.0.0.1", "::1"}:
        raise ConfigError("LOCAL_TIER_URL must use explicit loopback 127.0.0.1 or ::1")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ConfigError("LOCAL_TIER_URL may not contain credentials, query, or fragment")
    if parsed.path not in {"", "/"}:
        raise ConfigError("LOCAL_TIER_URL must be a base URL without a path")
    try:
        parsed.port
    except ValueError as error:
        raise ConfigError("LOCAL_TIER_URL contains an invalid port") from error
    return raw_url.rstrip("/")


def request_json(
    base_url: str,
    path: str,
    api_key: str,
    timeout: float,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(base_url + path, data=body, headers=headers)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=timeout) as response:
        content = response.read()
    return json.loads(content or b"{}")


def endpoint_healthy(base_url: str, api_key: str, timeout: float = 5) -> bool:
    for path in ("/health", "/v1/models", "/api/tags"):
        try:
            request_json(base_url, path, api_key, timeout)
            return True
        except (OSError, ValueError, urllib.error.HTTPError, urllib.error.URLError):
            continue
    return False
