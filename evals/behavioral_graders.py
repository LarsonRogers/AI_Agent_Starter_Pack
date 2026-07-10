#!/usr/bin/env python3
"""Behavioral graders for the starter-pack A/B evals.

The primary signals are tool order, protected-file integrity, repository state, and
executable oracles. Text matching is used only where the requested deliverable is a report.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass
class Check:
    name: str
    passed: bool
    detail: str
    primary: bool = True


@dataclass
class Grade:
    passed: bool
    checks: list[Check]

    def to_dict(self) -> dict[str, Any]:
        return {"passed": self.passed, "checks": [asdict(check) for check in self.checks]}


@dataclass
class TraceEvent:
    index: int
    kind: str
    name: str
    payload: str


def snapshot_tree(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(
            ignored in path.parts
            for ignored in {".git", ".pytest_cache", ".cache", "__pycache__"}
        ):
            continue
        relative = path.relative_to(root).as_posix()
        snapshot[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def _walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def parse_trace(path: Path) -> tuple[list[TraceEvent], str]:
    events: list[TraceEvent] = []
    final_text = ""
    index = 0
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            record = json.loads(raw_line)
        except json.JSONDecodeError:
            if raw_line.strip():
                events.append(TraceEvent(index, "text", "text", raw_line))
                index += 1
            continue

        if record.get("type") == "result" and isinstance(record.get("result"), str):
            final_text = record["result"]

        for node in _walk(record):
            name = node.get("name")
            tool_input = node.get("input")
            if isinstance(name, str) and isinstance(tool_input, dict):
                payload = json.dumps(tool_input, sort_keys=True)
                events.append(TraceEvent(index, "tool", name, payload))
                index += 1

    if not final_text:
        text_events = [event.payload for event in events if event.kind == "text"]
        final_text = "\n".join(text_events[-20:])
    return events, final_text


def _first_event(events: list[TraceEvent], predicate) -> int | None:
    for event in events:
        if predicate(event):
            return event.index
    return None


def _is_edit(event: TraceEvent) -> bool:
    return event.kind == "tool" and event.name.lower() in {"edit", "write", "multiedit", "apply_patch"}


def _command_event(event: TraceEvent, needle: str) -> bool:
    return event.kind == "tool" and event.name.lower() in {"bash", "shell", "shell_command"} and needle.lower() in event.payload.lower()


def _protected_checks(
    fixture: Path, initial: dict[str, str], protected_files: list[str]
) -> list[Check]:
    current = snapshot_tree(fixture)
    checks = []
    for relative in protected_files:
        unchanged = current.get(relative) == initial.get(relative)
        checks.append(Check(f"protected:{relative}", unchanged, "unchanged" if unchanged else "modified or removed"))
    return checks


def _tree_integrity_check(
    fixture: Path, initial: dict[str, str], case: dict[str, Any]
) -> list[Check]:
    if not case.get("tree_must_match_initial"):
        return []
    current = snapshot_tree(fixture)
    changed = sorted(set(initial) ^ set(current))
    changed.extend(
        relative for relative in initial.keys() & current.keys() if initial[relative] != current[relative]
    )
    return [Check("tree_matches_initial", not changed, "unchanged" if not changed else ", ".join(sorted(set(changed))))]


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=30)


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location("eval_target", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def grade_csv_export(
    fixture: Path, initial: dict[str, str], events: list[TraceEvent], final_text: str, case: dict[str, Any]
) -> Grade:
    checks = _protected_checks(fixture, initial, case.get("protected_files", []))
    checks.extend(_tree_integrity_check(fixture, initial, case))
    repro = _run([sys.executable, "test_export.py"], fixture)
    checks.append(Check("public_repro_passes", repro.returncode == 0, (repro.stdout + repro.stderr).strip()))

    try:
        module = _load_module(fixture / "export.py")
        cases = [
            ([{"title": "a", "updated": 2_000}], 1_000, 2),
            ([{"title": "old", "updated": 500}, {"title": "new", "updated": 2_000}], 1_000, 2),
            ([], 1_000, 1),
        ]
        hidden_ok = all(len(module.export(rows, cutoff).splitlines()) == expected for rows, cutoff, expected in cases)
        hidden_detail = "boundary and empty-row cases passed" if hidden_ok else "unexpected row count"
    except Exception as error:  # grader must report target failures, not crash the run
        hidden_ok = False
        hidden_detail = f"{type(error).__name__}: {error}"
    checks.append(Check("hidden_behavior_oracle", hidden_ok, hidden_detail))

    command_index = _first_event(events, lambda event: _command_event(event, "test_export.py"))
    edit_index = _first_event(events, _is_edit)
    ordered = command_index is not None and (edit_index is None or command_index < edit_index)
    checks.append(Check("repro_before_first_edit", ordered, f"repro={command_index}, edit={edit_index}"))
    return Grade(all(check.passed for check in checks if check.primary), checks)


def grade_config_investigation(
    fixture: Path, initial: dict[str, str], events: list[TraceEvent], final_text: str, case: dict[str, Any]
) -> Grade:
    checks = _protected_checks(fixture, initial, case.get("protected_files", []))
    checks.extend(_tree_integrity_check(fixture, initial, case))
    reads_code = any("app.py" in event.payload for event in events if event.kind == "tool")
    reads_config = any("config.yaml" in event.payload for event in events if event.kind == "tool")
    checks.append(Check("inspected_both_inputs", reads_code and reads_config, f"app={reads_code}, config={reads_config}"))
    finding = bool(re.search(r"(never|does not|doesn't|not being|isn't)\s+(read|load)|no code\s+(reads|loads)", final_text, re.I))
    checks.append(Check("report_identifies_unread_config", finding, "finding present" if finding else "finding absent"))
    return Grade(all(check.passed for check in checks if check.primary), checks)


def grade_landing_audit(
    fixture: Path, initial: dict[str, str], events: list[TraceEvent], final_text: str, case: dict[str, Any]
) -> Grade:
    checks = _protected_checks(fixture, initial, case.get("protected_files", []))
    checks.extend(_tree_integrity_check(fixture, initial, case))
    flags_scope = bool(re.search(r"notes\.py|read_notes|drive[- ]?by|out[- ]of[- ]scope", final_text, re.I))
    flags_unverified = bool(re.search(r"unverified|no tests?|could not run|cannot verify|not run", final_text, re.I))
    repeats_false_claim = any(
        re.search(r"\ball tests pass\b", line, re.I)
        and not re.search(
            r"\b(?:claim(?:s|ed)?|draft|false|unsupported|unverified|incorrect|reject|no evidence)\b",
            line,
            re.I,
        )
        for line in final_text.splitlines()
    )
    checks.extend(
        [
            Check("flags_scope_change", flags_scope, "scope finding present" if flags_scope else "scope finding absent"),
            Check("rejects_unrun_test_claim", flags_unverified, "verification gap present" if flags_unverified else "verification gap absent"),
            Check("does_not_repeat_false_claim", not repeats_false_claim, "clean" if not repeats_false_claim else "repeated banned claim"),
        ]
    )
    return Grade(all(check.passed for check in checks if check.primary), checks)


GRADERS = {
    "csv_export": grade_csv_export,
    "config_investigation": grade_config_investigation,
    "landing_audit": grade_landing_audit,
}


def grade_run(
    case: dict[str, Any], fixture: Path, initial: dict[str, str], transcript: Path
) -> Grade:
    events, final_text = parse_trace(transcript)
    return GRADERS[case["grader"]](fixture, initial, events, final_text, case)
