#!/usr/bin/env python3
"""Validate repository metadata without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"VALIDATION FAILED: {message}", file=sys.stderr)


def main() -> int:
    failures: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if plugin.get("version") != version:
        fail(f"plugin version {plugin.get('version')} != VERSION {version}", failures)
    if version not in (ROOT / "README.md").read_text(encoding="utf-8"):
        fail("README does not contain VERSION", failures)
    if not (ROOT / "LICENSE").is_file():
        fail("LICENSE is missing", failures)

    for path in ROOT.rglob("*.json"):
        if ".git" not in path.parts:
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as error:
                fail(f"invalid JSON {path.relative_to(ROOT)}: {error}", failures)
    for path in ROOT.rglob("*.toml"):
        if ".git" not in path.parts:
            try:
                tomllib.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as error:
                fail(f"invalid TOML {path.relative_to(ROOT)}: {error}", failures)

    profiles = json.loads(
        (ROOT / "adapters" / "system-prompt" / "profiles.json").read_text(encoding="utf-8")
    )["profiles"]
    for name, profile in profiles.items():
        prompt = ROOT / "adapters" / "system-prompt" / profile["file"]
        actual_words = len(prompt.read_text(encoding="utf-8").split())
        if actual_words != profile["words"] or actual_words > profile["budget"]:
            fail(
                f"profile manifest mismatch for {name}: words={actual_words}, "
                f"manifest={profile['words']}, budget={profile['budget']}",
                failures,
            )

    for workflow_path in (
        ROOT / ".github" / "workflows" / "agent-ci.yml",
        ROOT / "templates" / "agent-ci.yml",
    ):
        workflow = workflow_path.read_text(encoding="utf-8")
        for line in workflow.splitlines():
            match = re.search(r"\buses:\s*[^@\s]+@([^\s#]+)", line)
            if match and not re.fullmatch(r"[0-9a-f]{40}", match.group(1)):
                fail(
                    f"action is not commit-pinned in {workflow_path.relative_to(ROOT)}: "
                    f"{line.strip()}",
                    failures,
                )

    for path in list(ROOT.rglob("*.sh")) + [ROOT / ".githooks" / "pre-commit"]:
        if path.is_file() and b"\r\n" in path.read_bytes():
            fail(f"shell file has CRLF endings: {path.relative_to(ROOT)}", failures)

    if failures:
        return 1
    print(f"repository validation passed ({version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
