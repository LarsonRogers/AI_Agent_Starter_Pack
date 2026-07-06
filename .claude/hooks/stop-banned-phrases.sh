#!/usr/bin/env bash
# .claude/hooks/stop-banned-phrases.sh — Stop hook (v13). NOTIFY-ONLY.
# Scans the tail of the session transcript for banned landing phrases and prints
# a one-line warning. Never blocks: exits 0 on every path (Stop hooks cannot
# retroactively block anyway; this script also never tries).

set -u

# transcript_path arrives in the stdin JSON; extract without jq (may be absent).
input="$(cat 2>/dev/null || true)"
transcript="$(printf '%s' "$input" | sed -n 's/.*"transcript_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
[ -n "$transcript" ] && [ -f "$transcript" ] || exit 0

# Tail only: this fires every turn; scanning the whole transcript re-flags history.
found="$(tail -c 16384 "$transcript" 2>/dev/null \
  | grep -oiE 'should work|probably fixed|everything is (now )?fixed|this resolves the issue' \
  | sort -u | head -3 | paste -sd ', ' - 2>/dev/null || true)"

if [ -n "$found" ]; then
  echo "landing-phrase warning: \"$found\" — claims need observations (charter law 2); run the landing protocol before calling this done." >&2
fi
exit 0
