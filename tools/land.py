#!/usr/bin/env python3
"""Cross-platform deterministic landing gate."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


SCAFFOLD_RE = re.compile(
    r"console\.log\(|\bdebugger\b|\bdbg!\(|TODO[ _-]?remove|DO NOT COMMIT|"
    r"print\([\"'](?:DEBUG|debug|here|HERE|xxx)"
)
BANNED_RE = re.compile(
    r"should work|probably fixed|everything is (?:now )?fixed|this resolves the issue|"
    r"simply run",
    re.I,
)


def command(command_line: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command_line,
        cwd=cwd,
        shell=True,
        text=True,
        capture_output=True,
        timeout=900,
    )


def git_root(cwd: Path) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True, capture_output=True
    )
    return Path(result.stdout.strip()) if result.returncode == 0 else None


def validation_commands(agents: Path) -> list[tuple[str, str]]:
    if not agents.is_file():
        return []
    line = next(
        (line for line in agents.read_text(encoding="utf-8").splitlines() if line.startswith("- Lint:")),
        "",
    )
    commands = []
    for part in line.removeprefix("- ").split("·"):
        label, separator, value = part.partition(":")
        value = value.strip()
        if separator and value and "[" not in value and label.strip() != "Build":
            commands.append((label.strip(), value))
    return commands


def run_gate(
    cwd: Path, report: Path | None, done_check: str, run_configured: bool = False
) -> tuple[bool, list[str]]:
    root = git_root(cwd)
    if root is None:
        return False, ["not a git repository — the gate needs a diff to audit"]
    violations: list[str] = []
    configured = validation_commands(root / "AGENTS.md")
    if configured and not run_configured:
        violations.append(
            "configured validation commands were not executed — inspect them, then rerun "
            "with --run-configured"
        )
    elif run_configured:
        for label, configured_command in configured:
            result = command(configured_command, root)
            if result.returncode:
                violations.append(f"validation command failed — {label}: {configured_command}")

    if not done_check:
        violations.append("no done-check declared — pass --done-check or LAND_DONE_CHECK")
    else:
        result = command(done_check, root)
        if result.returncode:
            violations.append(f"done-check failed: {done_check}")

    diff = subprocess.run(
        [
            "git",
            "diff",
            "HEAD",
            "--",
            ".",
            ":(exclude)tools/land.py",
            ":(exclude)tools/land.sh",
            ":(exclude).githooks",
            ":(exclude).claude/hooks",
        ],
        cwd=root,
        text=True,
        capture_output=True,
    ).stdout
    scaffolding = [line for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++") and "land-ok" not in line and SCAFFOLD_RE.search(line)]
    if scaffolding:
        violations.append(f"debug scaffolding in working diff ({len(scaffolding)} line(s))")

    if report is not None:
        report_path = report if report.is_absolute() else root / report
        if not report_path.is_file():
            violations.append(f"report file not found: {report}")
        else:
            report_text = report_path.read_text(encoding="utf-8", errors="replace")
            if BANNED_RE.search(report_text):
                violations.append(f"banned landing phrase in report '{report}'")
            for line in report_text.splitlines():
                if re.search(r"\ball tests pass\b", line, re.I) and not re.search(
                    r"`[^`]+`|\b(?:ran|via|command)\b", line, re.I
                ):
                    violations.append(
                        f"unqualified 'all tests pass' claim in report '{report}' — name the command"
                    )
                    break
    return not violations, violations


def _init_repo(path: Path) -> None:
    for args in (
        ["git", "init", "-q"],
        ["git", "config", "user.email", "selftest@example.invalid"],
        ["git", "config", "user.name", "Self Test"],
    ):
        subprocess.run(args, cwd=path, check=True, capture_output=True)


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="land-self-test-") as temporary:
        root = Path(temporary)
        clean = root / "clean"
        clean.mkdir()
        _init_repo(clean)
        (clean / "app.txt").write_text("ok\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=clean, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "init"], cwd=clean, check=True, capture_output=True)
        report = clean / "report.md"
        report.write_text("Verified: observed the behavior.\n", encoding="utf-8")
        passing_check = f'"{sys.executable}" -c "pass"'
        clean_ok, _ = run_gate(clean, report, passing_check)
        print("self-test PASS: clean fixture passes" if clean_ok else "self-test FAIL: clean fixture")

        dirty = root / "dirty"
        dirty.mkdir()
        _init_repo(dirty)
        (dirty / "app.js").write_text("ok\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=dirty, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "init"], cwd=dirty, check=True, capture_output=True)
        (dirty / "app.js").write_text('ok\nconsole.log("debug");\n', encoding="utf-8")
        dirty_report = dirty / "report.md"
        dirty_report.write_text("Everything is fixed and it should work.\n", encoding="utf-8")
        dirty_ok, violations = run_gate(dirty, dirty_report, passing_check)
        caught = not dirty_ok and any("scaffolding" in item for item in violations) and any("banned" in item for item in violations)
        print("self-test PASS: planted violations caught" if caught else "self-test FAIL: planted fixture")
        return 0 if clean_ok and caught else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--done-check", default=os.environ.get("LAND_DONE_CHECK", ""))
    parser.add_argument(
        "--run-configured",
        action="store_true",
        default=os.environ.get("LAND_RUN_CONFIGURED") == "1",
        help="execute validation commands read from trusted AGENTS.md Part 2",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    passed, violations = run_gate(Path.cwd(), args.report, args.done_check, args.run_configured)
    for violation in violations:
        print(f"LAND GATE FAILED: {violation}")
    if not passed:
        return 1
    if args.report is None:
        print("land.py: no --report given — banned-phrase scan SKIPPED (not passed)")
    print("LAND GATE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
