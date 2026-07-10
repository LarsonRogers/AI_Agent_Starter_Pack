#!/usr/bin/env bash
# .claude/hooks/post-edit-validate.sh — PostToolUse (Edit|Write) hook (v13).
# NOTIFY-ONLY: runs the project's configured lint/format commands after an edit
# and prints a one-line warning if one fails. Exits 0 on every path — it never
# blocks an edit; the blocking gates are tools/land.py and .githooks/pre-commit.

set -u

project_dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

# Fire evidence (Fix 9): one line per invocation, before any exit path, so
# PostToolUse live-fire is a grep of var/log/hooks.log instead of transcript
# archaeology. var/ is gitignored.
mkdir -p "$project_dir/var/log" 2>/dev/null
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) post-edit-validate invoked" >> "$project_dir/var/log/hooks.log" 2>/dev/null

agents="$project_dir/AGENTS.md"
[ -f "$agents" ] || exit 0

line="$(grep -m1 -E '^- Lint:' "$agents" 2>/dev/null || true)"
[ -n "$line" ] || exit 0

if [ "${FABLIZED_RUN_CONFIGURED_HOOKS:-0}" != "1" ]; then
  echo "post-edit: configured lint/format commands not auto-run; inspect them and opt in with FABLIZED_RUN_CONFIGURED_HOOKS=1." >&2
  exit 0
fi

# sed, not tr: the '·' separator is multibyte UTF-8.
printf '%s\n' "${line#- }" | sed 's/·/\n/g' | while IFS= read -r part; do
  label="$(printf '%s' "${part%%:*}" | sed 's/^ *//;s/ *$//')"
  cmd="$(printf '%s' "${part#*:}" | sed 's/^ *//;s/ *$//')"
  case "$cmd" in ''|*'['*']'*) continue ;; esac    # placeholder or empty
  case "$label" in
    Lint|Format)
      if ! (cd "$project_dir" && sh -c "$cmd" >/dev/null 2>&1); then
        echo "post-edit: $label failed ($cmd) — fix before landing; tools/land.py will gate on it." >&2
      fi
      ;;
  esac
done

exit 0
