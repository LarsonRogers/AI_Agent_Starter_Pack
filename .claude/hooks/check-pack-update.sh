#!/usr/bin/env bash
# Starter Pack v12.10 — .claude/hooks/check-pack-update.sh
#
# OPTIONAL, OPT-IN, NOTIFY-ONLY pack update check for the Claude Code
# SessionStart hook. Prints ONE line to stdout only when a newer pack version
# exists upstream; that line is injected as session context so Claude can relay
# it. This script NEVER downloads, overwrites, applies, or commits anything, and
# it exits 0 on every failure path so it can never block or error a session.
#
# To enable: set PACK_SOURCE_URL below to the raw URL of the upstream AGENTS.md,
# then register this script as a SessionStart "startup" hook in
# .claude/settings.json (see protocols/update-check.md). Off until you do both.
#
# Applying an update is a separate, user-confirmed step — see
# protocols/upgrade.md. This hook only tells you one is available.

set -u

# --- configure this -----------------------------------------------------------
# Raw URL of the upstream pack's AGENTS.md (e.g. a raw.githubusercontent.com path).
# Leave as-is to keep the hook a silent no-op.
PACK_SOURCE_URL=""
# ------------------------------------------------------------------------------

# No source configured → silent no-op (offline / local-only setups stay quiet).
[ -z "$PACK_SOURCE_URL" ] && exit 0

project_dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
local_agents="$project_dir/AGENTS.md"
[ -f "$local_agents" ] || exit 0

extract_ver() { grep -oE 'Starter Pack v[0-9]+\.[0-9]+' "$1" 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+'; }

local_ver="$(extract_ver "$local_agents")"
[ -n "$local_ver" ] || exit 0

# Fetch upstream AGENTS.md to a temp file (curl, then wget), short timeouts.
tmp="$(mktemp 2>/dev/null)" || exit 0
trap 'rm -f "$tmp"' EXIT
if command -v curl >/dev/null 2>&1; then
  curl -fsSL --max-time 5 --max-filesize 1000000 "$PACK_SOURCE_URL" -o "$tmp" 2>/dev/null || exit 0
elif command -v wget >/dev/null 2>&1; then
  wget -q -T 5 -O "$tmp" "$PACK_SOURCE_URL" 2>/dev/null || exit 0
else
  exit 0
fi

upstream_ver="$(extract_ver "$tmp")"
[ -n "$upstream_ver" ] || exit 0

# Compare vMAJOR.MINOR numerically; notify only when upstream is strictly newer.
# Both `2>/dev/null` guards below are load-bearing: they suppress any stderr from
# the integer tests so a malformed version never leaks a line into session
# context. Do not remove either when editing this condition.
l_major="${local_ver%%.*}";    l_minor="${local_ver##*.}"
u_major="${upstream_ver%%.*}"; u_minor="${upstream_ver##*.}"
if [ "$u_major" -gt "$l_major" ] 2>/dev/null || { [ "$u_major" -eq "$l_major" ] && [ "$u_minor" -gt "$l_minor" ]; } 2>/dev/null; then
  echo "Pack update available: v$local_ver → v$upstream_ver. Ask me to run the update-check (protocols/update-check.md) to review and upgrade."
fi
exit 0
