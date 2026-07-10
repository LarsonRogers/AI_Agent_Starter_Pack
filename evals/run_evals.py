#!/usr/bin/env python3
"""Run automated kit-vs-baseline behavior evaluations with Claude Code."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from behavioral_graders import grade_run, snapshot_tree


ROOT = Path(__file__).resolve().parent.parent
EVAL_ROOT = ROOT / "evals"
PROMPTS = {
    "full": ROOT / "adapters/system-prompt/fablized-full.md",
    "compact": ROOT / "adapters/system-prompt/fablized-compact.md",
    "micro": ROOT / "adapters/system-prompt/fablized-micro.md",
}
PROFILE_MANIFEST = json.loads(
    (ROOT / "adapters" / "system-prompt" / "profiles.json").read_text(encoding="utf-8")
)["profiles"]
PROFILE_BUDGETS = {name: profile["budget"] for name, profile in PROFILE_MANIFEST.items()}


def artifact_component(value: str) -> str:
    """Return a portable, non-empty directory component for an external identifier."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._") or "model"


def run(command: list[str], cwd: Path, *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)


def prepare_fixture(case: dict[str, Any], destination: Path) -> dict[str, str]:
    shutil.copytree(
        EVAL_ROOT / case["fixture"],
        destination,
        ignore=shutil.ignore_patterns(".cache", ".pytest_cache", "__pycache__", "*.pyc"),
    )
    for action in case.get("setup", []):
        if action == "git_init":
            commands = [
                ["git", "init", "-q"],
                ["git", "config", "user.email", "eval@example.invalid"],
                ["git", "config", "user.name", "Eval Runner"],
                ["git", "add", "-A"],
                ["git", "commit", "-qm", "base"],
            ]
            for command in commands:
                result = run(command, destination)
                if result.returncode:
                    raise RuntimeError(f"setup failed: {' '.join(command)}\n{result.stderr}")
        elif action.startswith("apply:"):
            patch = action.split(":", 1)[1]
            result = run(["git", "apply", patch], destination)
            if result.returncode:
                raise RuntimeError(f"git apply failed: {result.stderr}")
        elif action.startswith("remove:"):
            (destination / action.split(":", 1)[1]).unlink()
        else:
            raise ValueError(f"unknown setup action: {action}")
    return snapshot_tree(destination)


def invoke_claude(
    claude: str,
    case: dict[str, Any],
    fixture: Path,
    model: str,
    arm: str,
    profile: str,
    transcript: Path,
    timeout: int,
) -> int:
    command = [
        claude,
        "-p",
        case["prompt"],
        "--model",
        model,
        "--dangerously-skip-permissions",
        "--output-format",
        "stream-json",
        "--verbose",
    ]
    if arm == "kit":
        command.extend(["--append-system-prompt-file", str(PROMPTS[profile])])
    with transcript.open("w", encoding="utf-8", newline="\n") as output:
        try:
            process = subprocess.run(
                command,
                cwd=fixture,
                text=True,
                stdout=output,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
            return process.returncode
        except subprocess.TimeoutExpired:
            output.write(json.dumps({"type": "runner_error", "error": "agent timeout"}) + "\n")
            return 124
        except FileNotFoundError as error:
            output.write(json.dumps({"type": "runner_error", "error": str(error)}) + "\n")
            return 127


def invoke_command(
    template: list[str],
    case: dict[str, Any],
    fixture: Path,
    model: str,
    arm: str,
    profile: str,
    transcript: Path,
    timeout: int,
) -> int:
    prompt_file = transcript.parent / "prompt.txt"
    prompt_file.write_text(case["prompt"] + "\n", encoding="utf-8")
    empty_prompt = transcript.parent / "baseline-system-prompt.txt"
    empty_prompt.write_text("", encoding="utf-8")
    system_prompt = PROMPTS[profile] if arm == "kit" else empty_prompt
    values = {
        "prompt_file": str(prompt_file),
        "system_prompt_file": str(system_prompt),
        "transcript": str(transcript),
        "model": model,
        "arm": arm,
        "fixture": str(fixture),
    }
    command = [argument.format(**values) for argument in template]
    environment = os.environ.copy()
    environment.update({f"FABLIZED_EVAL_{key.upper()}": value for key, value in values.items()})
    with transcript.open("w", encoding="utf-8", newline="\n") as output:
        try:
            process = subprocess.run(
                command,
                cwd=fixture,
                env=environment,
                text=True,
                stdout=output,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
            return process.returncode
        except subprocess.TimeoutExpired:
            output.write(json.dumps({"type": "runner_error", "error": "agent timeout"}) + "\n")
            return 124
        except FileNotFoundError as error:
            output.write(json.dumps({"type": "runner_error", "error": str(error)}) + "\n")
            return 127


def select_cases(all_cases: list[dict[str, Any]], requested: list[str]) -> list[dict[str, Any]]:
    if not requested:
        return all_cases
    selected = [case for case in all_cases if case["id"] in requested]
    missing = sorted(set(requested) - {case["id"] for case in selected})
    if missing:
        raise SystemExit(f"unknown case(s): {', '.join(missing)}")
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--profile", choices=sorted(PROMPTS), default="full")
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--arm", choices=["kit", "baseline", "both"], default="both")
    parser.add_argument("--claude", default="claude")
    parser.add_argument(
        "--command-json",
        help=(
            "Provider-neutral argv JSON array. Placeholders: {prompt_file}, "
            "{system_prompt_file}, {model}, {arm}, {fixture}, {transcript}."
        ),
    )
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--artifacts", type=Path, default=EVAL_ROOT / "artifacts")
    args = parser.parse_args()
    command_template = None
    if args.command_json:
        try:
            command_template = json.loads(args.command_json)
        except json.JSONDecodeError as error:
            parser.error(f"invalid --command-json: {error}")
        if not isinstance(command_template, list) or not command_template or not all(
            isinstance(item, str) for item in command_template
        ):
            parser.error("--command-json must be a non-empty JSON array of strings")

    spec = json.loads((EVAL_ROOT / "evals.json").read_text(encoding="utf-8"))
    cases = select_cases(spec["cases"], args.case)
    arms = ["kit", "baseline"] if args.arm == "both" else [args.arm]
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_root = args.artifacts / stamp / artifact_component(args.model)
    run_root.mkdir(parents=True, exist_ok=True)
    prompt_words = len(PROMPTS[args.profile].read_text(encoding="utf-8").split())
    summary: dict[str, Any] = {
        "model": args.model,
        "profile": args.profile,
        "prompt_words": prompt_words,
        "profile_budget_words": PROFILE_BUDGETS[args.profile],
        "cases": {},
    }

    with tempfile.TemporaryDirectory(prefix="fablized-evals-") as temporary:
        temp_root = Path(temporary)
        for case in cases:
            summary["cases"][case["id"]] = {}
            for arm in arms:
                fixture = temp_root / f"{case['id']}-{arm}"
                initial = prepare_fixture(case, fixture)
                artifact_dir = run_root / case["id"] / arm
                artifact_dir.mkdir(parents=True, exist_ok=True)
                transcript = artifact_dir / "stream.jsonl"
                if command_template:
                    exit_code = invoke_command(
                        command_template,
                        case,
                        fixture,
                        args.model,
                        arm,
                        args.profile,
                        transcript,
                        args.timeout,
                    )
                else:
                    exit_code = invoke_claude(
                        args.claude,
                        case,
                        fixture,
                        args.model,
                        arm,
                        args.profile,
                        transcript,
                        args.timeout,
                    )
                grade = grade_run(case, fixture, initial, transcript)
                result = {"agent_exit": exit_code, "grade": grade.to_dict()}
                final_snapshot = snapshot_tree(fixture)
                diff = run(["git", "diff", "--binary", "HEAD", "--", "."], fixture)
                (artifact_dir / "initial-tree.json").write_text(
                    json.dumps(initial, indent=2) + "\n", encoding="utf-8"
                )
                (artifact_dir / "final-tree.json").write_text(
                    json.dumps(final_snapshot, indent=2) + "\n", encoding="utf-8"
                )
                (artifact_dir / "final-diff.patch").write_text(diff.stdout, encoding="utf-8")
                (artifact_dir / "result.json").write_text(
                    json.dumps(result, indent=2) + "\n", encoding="utf-8"
                )
                summary["cases"][case["id"]][arm] = result

    kit_results = {
        case_id: result["kit"]["agent_exit"] == 0 and result["kit"]["grade"]["passed"]
        for case_id, result in summary["cases"].items()
        if "kit" in result
    }
    baseline_results = {
        case_id: result["baseline"]["agent_exit"] == 0
        and result["baseline"]["grade"]["passed"]
        for case_id, result in summary["cases"].items()
        if "baseline" in result
    }
    regressions = [
        case_id for case_id in kit_results.keys() & baseline_results
        if baseline_results[case_id] and not kit_results[case_id]
    ]
    lift = [
        case_id for case_id in kit_results.keys() & baseline_results
        if kit_results[case_id] and not baseline_results[case_id]
    ]
    budget_ok = prompt_words <= PROFILE_BUDGETS[args.profile]
    if baseline_results:
        accepted = budget_ok and not regressions and bool(lift)
    else:
        accepted = budget_ok and bool(kit_results) and all(kit_results.values())
    summary["acceptance"] = {
        "accepted": accepted,
        "lift_cases": sorted(lift),
        "regressions": sorted(regressions),
        "context_budget_passed": budget_ok,
    }
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
