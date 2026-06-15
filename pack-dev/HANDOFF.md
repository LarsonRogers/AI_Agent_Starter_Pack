# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.8 · **Audience mode:** Developer
**Last completed:** Added a pack **update-check** (detect layer) — v12.7→v12.8. New `protocols/update-check.md` is a read-only, portable check (local vs upstream version; offline/no-source/no-fetch → skip silently; behind → hand to `upgrade.md`; never auto-applies). New opt-in, notify-only Claude-Code `SessionStart` script `.claude/hooks/check-pack-update.sh` (off by default; prints one line only when upstream is newer; never writes/downloads/applies; size-bounded fail-silent fetch). Wired: AGENTS.md standing rule + Index row (30→31) + Part 2 "Pack source" row; upgrade.md detect/apply note + in-section-field caveat; SETUP Step 0 reframed (closes the old distribution-link intent). Independent review APPROVE, 0 blockers (4 minors fixed).

**Confirmed next task:** ask the user — no build task queued.

**Branch:** `main` (consolidated; `revised` retired). v12.8 committed locally; pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- KEY VALIDATION (blocked on rig access): full pack on a real quantized 12B (RTX 3070 8GB / 64GB RAM) at 8-16k under LEAN — confirm pointer-indirection holds, LEAN floor fits, safety triggers fire.
- Model-tiering live dogfood — exercise a PREDEFINED light-tier subagent in OpenCode and/or Codex (not a per-call override, which they don't support), incl. a non-Anthropic tier map.
- update-check notify-hook is unexercised live — verify SessionStart stdout injection + a real fetch against a configured PACK_SOURCE_URL on an actual Claude Code launch once a distribution URL exists.
- upgrade.md is prose-verified only — no end-to-end migration dry-run against a real older-version project (incl. pre-v12.0 deltas, the NOT-SET setup-block fill, and the new in-section-field flagging).
- PROBE 2 (opencode.json edit-ask live-fire), PROBE 3 (semgrep CI on first push) — need OpenCode session / GitHub Actions run.
- SETUP Step 0 distribution URL — maintainer still fills the actual link (the mechanism to use it now exists).

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`; `revised` retired); its
    own logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then
    the last entries of pack-dev/DECISION_LOG.md as needed. v12.8: a detect-only
    pack update-check exists (protocols/update-check.md) with an opt-in,
    notify-only Claude-Code SessionStart hook (.claude/hooks/check-pack-update.sh,
    off by default); applying updates is still upgrade.md. No build task queued —
    ask the user what's next. Likely: real-12B LEAN validation, a live tiering
    dogfood, or live-firing the notify-hook once a distribution URL is set. This
    v12.8 commit is local on main; pushing needs user confirmation.
