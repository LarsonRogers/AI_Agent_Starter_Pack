#!/usr/bin/env bash
# tools/land.sh — harness-independent landing gate (v13, Amendment 01).
#
# A GATE, not a notifier: exits nonzero on violation and names the violated rule.
# Runs identically under Claude Code, OpenCode, Codex, or a bare loop — for weak
# models, deterministic gates do the self-policing prose can't.
#
# Usage:
#   tools/land.sh [--report FILE] [--done-check "CMD"] [--self-test]
#
#   --report FILE      landing report to scan for banned phrases (optional; skipped
#                      with a note if absent — the report scan cannot pass silently)
#   --done-check CMD   the done-check declared in preflight; also read from the
#                      LAND_DONE_CHECK env var. Missing entirely = a violation.
#   --self-test        build a clean fixture (must pass) and a planted fixture
#                      (must fail, naming each rule), then report.
#
# Checks, in order:
#   1. Part 2 validation commands (parsed from AGENTS.md Quick constraints; each
#      configured command must exit 0). Placeholders ([cmd]) are skipped.
#   2. The declared done-check runs and passes, from the current tree.
#   3. Working diff (vs HEAD) contains no debug scaffolding. Suppress a deliberate
#      line by putting "land-ok" in a comment on that line.
#   4. The report file contains no banned landing phrases.

set -u

FAIL=0
violate() { printf 'LAND GATE FAILED: %s\n' "$1"; FAIL=1; }
note() { printf 'land.sh: %s\n' "$1"; }

REPORT=""
DONE_CHECK="${LAND_DONE_CHECK:-}"
SELF_TEST=0
while [ $# -gt 0 ]; do
  case "$1" in
    --report)     REPORT="${2:-}"; shift 2 ;;
    --done-check) DONE_CHECK="${2:-}"; shift 2 ;;
    --self-test)  SELF_TEST=1; shift ;;
    *) note "unknown argument: $1"; exit 2 ;;
  esac
done

# Patterns are word-boundary-anchored and marker-based on purpose: a bare "print("
# pattern would flag every Python project. Deliberate lines carry "land-ok".
SCAFFOLD_RE='console\.log\(|\bdebugger\b|\bdbg!\(|TODO[ _-]?remove|DO NOT COMMIT|print\(["'"'"'](DEBUG|debug|here|HERE|xxx)'
BANNED_RE='should work|probably fixed|everything is (now )?fixed|this resolves the issue|all tests pass|simply run'

run_gate() {
  root="$(git rev-parse --show-toplevel 2>/dev/null)" || {
    violate "not a git repository — the gate needs a diff to audit"; return
  }
  cd "$root" || { violate "cannot cd to repo root"; return; }

  # 1. Part 2 validation commands ------------------------------------------------
  if [ -f AGENTS.md ]; then
    line="$(grep -m1 -E '^- Lint:' AGENTS.md 2>/dev/null || true)"
    if [ -n "$line" ]; then
      # sed, not tr: '·' is multibyte UTF-8 and tr splits bytewise.
      printf '%s\n' "${line#- }" | sed 's/·/\n/g' | while IFS= read -r part; do
        cmd="${part#*:}"
        label="$(printf '%s' "${part%%:*}" | sed 's/^ *//;s/ *$//')"
        cmd="$(printf '%s' "$cmd" | sed 's/^ *//;s/ *$//')"
        case "$cmd" in ''|*'['*']'*) continue ;; esac   # placeholder or empty
        case "$label" in Build) continue ;; esac        # build is not a landing gate
        if ! sh -c "$cmd" >/dev/null 2>&1; then
          printf 'LAND GATE FAILED: validation command failed — %s: %s\n' "$label" "$cmd"
          touch "${TMPDIR:-/tmp}/land_subfail.$$"
        fi
      done
      [ -f "${TMPDIR:-/tmp}/land_subfail.$$" ] && { rm -f "${TMPDIR:-/tmp}/land_subfail.$$"; FAIL=1; }
    else
      note "no Quick-constraints validation line in AGENTS.md — nothing to run"
    fi
  else
    note "no AGENTS.md — validation commands skipped"
  fi

  # 2. Done-check -----------------------------------------------------------------
  if [ -z "$DONE_CHECK" ]; then
    violate "no done-check declared (pass --done-check or set LAND_DONE_CHECK) — a task without a runnable done-check cannot land"
  elif ! sh -c "$DONE_CHECK"; then
    violate "done-check failed: $DONE_CHECK"
  fi

  # 3. Debug scaffolding in the working diff --------------------------------------
  hits="$(git diff HEAD -- . ':(exclude)tools/land.sh' ':(exclude).githooks' ':(exclude).claude/hooks' 2>/dev/null \
          | grep -E '^\+' | grep -Ev '^\+\+\+' | grep -E "$SCAFFOLD_RE" | grep -v 'land-ok' || true)"
  if [ -n "$hits" ]; then
    violate "debug scaffolding in the working diff (suppress a deliberate line with 'land-ok'):"
    printf '%s\n' "$hits" | head -10
  fi

  # 4. Banned landing phrases in the report ----------------------------------------
  if [ -n "$REPORT" ]; then
    if [ -f "$REPORT" ]; then
      phrases="$(grep -inE "$BANNED_RE" "$REPORT" || true)"
      if [ -n "$phrases" ]; then
        violate "banned landing phrase in report '$REPORT' (claims need observations, not vibes):"
        printf '%s\n' "$phrases" | head -10
      fi
    else
      violate "report file not found: $REPORT"
    fi
  else
    note "no --report given — banned-phrase scan SKIPPED (not passed)"
  fi
}

self_test() {
  self="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  tmp="$(mktemp -d)" || { echo "self-test: mktemp failed"; exit 2; }
  trap 'rm -rf "$tmp"' EXIT
  status=0

  # --- clean fixture: must PASS ---------------------------------------------------
  mkdir -p "$tmp/clean" && cd "$tmp/clean" || exit 2
  git init -q && git config user.email t@t && git config user.name t
  echo "ok" > app.txt && git add -A && git commit -qm init
  printf 'Verified: ran the check, watched it exercise the change [OBSERVED].\n' > report.md
  if bash "$self" --report report.md --done-check "true" >/dev/null 2>&1; then
    echo "self-test PASS: clean fixture passes the gate"
  else
    echo "self-test FAIL: clean fixture was rejected"; status=1
  fi

  # --- planted fixture: must FAIL, naming both rules -------------------------------
  mkdir -p "$tmp/dirty" && cd "$tmp/dirty" || exit 2
  git init -q && git config user.email t@t && git config user.name t
  echo "ok" > app.js && git add -A && git commit -qm init
  printf 'console.log("leftover debug");\n' >> app.js          # planted scaffolding
  printf 'Everything is fixed and it should work now.\n' > report.md   # planted phrase
  out="$(bash "$self" --report report.md --done-check "true" 2>&1)" && {
    echo "self-test FAIL: planted fixture passed the gate"; status=1; }
  case "$out" in
    *"debug scaffolding"*) echo "self-test PASS: planted debug print caught, rule named" ;;
    *) echo "self-test FAIL: scaffolding rule not named"; status=1 ;;
  esac
  case "$out" in
    *"banned landing phrase"*) echo "self-test PASS: banned phrase caught, rule named" ;;
    *) echo "self-test FAIL: banned-phrase rule not named"; status=1 ;;
  esac
  exit "$status"
}

if [ "$SELF_TEST" -eq 1 ]; then
  self_test
fi

run_gate
if [ "$FAIL" -ne 0 ]; then
  exit 1
fi
echo "LAND GATE PASSED"
exit 0
