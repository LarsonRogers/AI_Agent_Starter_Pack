# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.10 · **Audience mode:** Developer
**Last completed:** Made Light-tier activation **agent-driven** (v12.9→v12.10). The agent now: prompts the user for the Light model → **writes the live sub-agent config file itself** from the shipped template (user never hand-edits `.md`/`.toml`) → states whether a harness restart is needed (OpenCode/Codex restart; Claude Code = new session). Reworked `model-tiering.md` into a 5-step agent-driven flow (PROMPT/RECORD/ACTIVATE/INDICATE RESTART/CONFIRM), fail-safe unchanged. Independent review APPROVE, 0 blockers (1 minor fixed: Claude same-session wording).

**Confirmed next task:** ask the user — no build task queued. The model-tiering UX is now complete pack-side (policy → never-blank prompt → shipped templates → agent-driven activation + restart signal). What remains is live validation.

**Branch:** `main` — **2 commits ahead of origin** (v12.9 templates `1704966` + v12.10 agent-driven `2f8aff9`), both local. Pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- **Tiering live dogfood (most actionable):** in a live OpenCode/Codex session, confirm the agent-driven flow actually works end-to-end — agent prompts, writes `.opencode/agent/light-checker.md` with a real model, says "restart OpenCode," and after restart the primary delegates a bounded scan to it. Include a non-Anthropic model.
- KEY VALIDATION (blocked on rig): full pack on a real quantized 12B at 8-16k under LEAN — pointer-indirection holds, LEAN floor fits, safety triggers fire.
- update-check notify-hook unexercised live — verify SessionStart stdout injection + real fetch against a configured PACK_SOURCE_URL on an actual Claude Code launch.
- upgrade.md prose-verified only — no end-to-end migration dry-run against a real older-version project (pre-v12.0 deltas, NOT-SET setup-block fill, in-section-field flagging).
- PROBE 2 (opencode.json edit-ask live-fire), PROBE 3 (semgrep CI on first push).
- SETUP Step 0 distribution URL — maintainer fills the actual link (mechanism exists).

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`; `revised` retired); its
    own logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then
    the last entries of pack-dev/DECISION_LOG.md as needed. v12.10: model-tiering
    setup is agent-driven — the agent prompts for the Light model, writes the
    live sub-agent file from the shipped template (user never hand-edits config),
    and signals restart (OpenCode/Codex) or new session (Claude). No build task
    queued — ask the user. Most actionable open item: a live tiering dogfood in
    OpenCode/Codex. main is 2 commits ahead of origin (local); pushing needs
    user confirmation.
