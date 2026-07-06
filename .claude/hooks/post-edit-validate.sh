#!/usr/bin/env bash
# .claude/hooks/post-edit-validate.sh — PostToolUse (Edit|Write) hook (v13).
# NOTIFY-ONLY: runs the project's configured lint/format commands after an edit
# and prints a one-line warning if one fails. Exits 0 on every path — it never
# blocks an edit; the blocking gates are tools/land.sh and .githooks/pre-commit.

set -u

project_dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
agents="$project_dir/AGENTS.md"
[ -f "$agents" ] || exit 0

line="$(grep -m1 -E '^- Lint:' "$agents" 2>/dev/null || true)"
[ -n "$line" ] || exit 0

# sed, not tr: the '·' separator is multibyte UTF-8.
printf '%s\n' "${line#- }" | sed 's/·/\n/g' | while IFS= read -r part; do
  label="$(printf '%s' "${part%%:*}" | sed 's/^ *//;s/ *$//')"
  cmd="$(printf '%s' "${part#*:}" | sed 's/^ *//;s/ *$//')"
  case "$cmd" in ''|*'['*']'*) continue ;; esac    # placeholder or empty
  case "$label" in
    Lint|Format)
      if ! (cd "$project_dir" && sh -c "$cmd" >/dev/null 2>&1); then
        echo "post-edit: $label failed ($cmd) — fix before landing; tools/land.sh will gate on it." >&2
      fi
      ;;
  esac
done

exit 0
