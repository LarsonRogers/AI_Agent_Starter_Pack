#!/usr/bin/env python3
"""Cross-platform staged-change guard used by .githooks/pre-commit."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


SECRET_RE = re.compile(
    rb"AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}|"
    rb"sk_(?:live|test)_[A-Za-z0-9]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
)
GENERATED_PATTERNS = (
    re.compile(r"^CLAUDE\.md$"),
    re.compile(r"^docs/fablized/"),
    re.compile(r"^adapters/"),
    re.compile(r"^\.claude/skills/[^/]+/SKILL\.md$"),
)


def git(args: list[str], cwd: Path, *, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=text)


def staged_files(cwd: Path) -> list[str]:
    result = git(["diff", "--cached", "--name-only", "--diff-filter=ACM", "-z"], cwd)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors="replace"))
    return [item.decode("utf-8", errors="surrogateescape") for item in result.stdout.split(b"\0") if item]


def main(cwd: Path | None = None) -> int:
    root = cwd or Path.cwd()
    try:
        staged = staged_files(root)
    except RuntimeError as error:
        print(f"PRE-COMMIT GATE FAILED: {error}", file=sys.stderr)
        return 1
    if not staged:
        return 0
    violations: list[str] = []

    diff = git(["diff", "--cached", "--unified=0", "--no-color", "--", "."], root).stdout
    additions = b"\n".join(
        line for line in diff.splitlines() if line.startswith(b"+") and not line.startswith(b"+++")
    )
    secret_matches = SECRET_RE.findall(additions)
    if secret_matches:
        violations.append(
            f"{len(secret_matches)} credential-format match(es) in staged additions; values redacted. "
            "Rotate if real and inspect locally."
        )

    if os.environ.get("SKIP_SIZE_GUARD") != "1":
        for relative in staged:
            result = git(["cat-file", "-s", f":0:{relative}"], root, text=True)
            try:
                size = int(result.stdout.strip()) if result.returncode == 0 else 0
            except ValueError:
                size = 0
            if size > 1_048_576:
                violations.append(
                    f"staged file over 1MB: {relative} ({size} bytes); set SKIP_SIZE_GUARD=1 "
                    "only after explicit review"
                )

    if os.environ.get("SKIP_GENERATED_GUARD") != "1":
        generated_touched = any(
            relative != "AGENTS.md" and any(pattern.search(relative) for pattern in GENERATED_PATTERNS)
            for relative in staged
        )
        core_touched = any(relative.startswith("core/") or relative == "tools/build.py" for relative in staged)
        if generated_touched or core_touched:
            build = root / "tools" / "build.py"
            if not build.is_file():
                violations.append("cannot verify generated outputs because tools/build.py is missing")
            else:
                unstaged = git(
                    [
                        "diff",
                        "--name-only",
                        "--",
                        "core",
                        "tools/build.py",
                        "CLAUDE.md",
                        "docs/fablized",
                        "adapters",
                        ".claude/skills",
                    ],
                    root,
                    text=True,
                ).stdout.splitlines()
                if unstaged:
                    violations.append(
                        "unstaged core/generated changes prevent staged-snapshot verification: "
                        + ", ".join(unstaged)
                    )
                result = subprocess.run(
                    [sys.executable, str(build), "--check"], cwd=root, capture_output=True, text=True
                )
                if not unstaged and result.returncode:
                    violations.append(
                        "generated outputs differ from core/ — run 'python tools/build.py', inspect, "
                        "and stage the complete result"
                    )

    for violation in violations:
        print(f"PRE-COMMIT GATE FAILED: {violation}", file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
