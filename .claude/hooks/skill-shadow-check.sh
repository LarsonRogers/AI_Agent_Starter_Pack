#!/usr/bin/env bash
# .claude/hooks/skill-shadow-check.sh — SessionStart shadow check (v13).
# NOTIFY-ONLY: warns when a kit skill name collides with another skill the
# harness may load first (built-in commands, user-level skills, other installed
# plugins) — a collision can silently shadow the kit's version. Exits 0 on
# every path. Detection is best-effort: built-ins are not enumerable from disk,
# so a known-name list is checked alongside the on-disk locations.

set -u

project_dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
kit_skills_dir="$project_dir/.claude/skills"
[ -d "$kit_skills_dir" ] || exit 0

# Known built-in / commonly-shipped Claude Code skill and command names.
# Best-effort list — extend when a new collision is reported.
BUILTINS="security-review review code-review init verify run simplify loop schedule
deep-research dataviz grill-me"

collisions=""
for d in "$kit_skills_dir"/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  src=""
  for b in $BUILTINS; do
    [ "$name" = "$b" ] && src="built-in"
  done
  [ -z "$src" ] && [ -d "$HOME/.claude/skills/$name" ] && src="user-level ~/.claude/skills"
  if [ -z "$src" ] && [ -d "$HOME/.claude/plugins" ]; then
    hit="$(find "$HOME/.claude/plugins" -maxdepth 4 -type d -name "$name" -path "*skills*" 2>/dev/null | head -1)"
    [ -n "$hit" ] && src="another installed plugin"
  fi
  [ -n "$src" ] && collisions="$collisions $name($src)"
done

if [ -n "$collisions" ]; then
  echo "skill shadow warning:$collisions — a same-named skill may load instead of the kit's; consider renaming the kit skill in core/ and rebuilding (see README)."
fi
exit 0
