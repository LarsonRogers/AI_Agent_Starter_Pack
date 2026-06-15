# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.9 · **Audience mode:** Developer
**Last completed:** Shipped ready-to-use **Light-tier subagent templates** for all three harnesses (v12.8→v12.9), closing the "policy exists but tiering isn't actually usable" gap a live OpenCode session surfaced. New inert (`.example`) templates: `.claude/agents/light-checker.md.example` (model: haiku, works on rename), `.opencode/agent/light-checker.md.example` and `.codex/agents/light-checker.toml.example` (fill-the-model). Each is read-only / non-judgement scoped. `model-tiering.md` gained a "Predefined Light-tier subagents" section + the 4 activation steps (choose model → drop `.example` + set model → restart OpenCode/Codex → confirm @mention/description-match invocation; fail-safe = can't invoke → run Capable). Independent review APPROVE, 0 blockers (1 minor fixed).

**Confirmed next task:** ask the user — no build task queued. The OpenCode tiering chain is complete pack-side; what remains is user-side activation (pick model, drop `.example`, restart) and live validation.

**Branch:** `main`. v12.9 committed locally; pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- **Tiering live dogfood (now concrete):** activate `.opencode/agent/light-checker.md` (and/or Codex) with a REAL provider/model-id, restart, and confirm the primary actually delegates a bounded scan to it. Templates + steps now exist; only a live OpenCode/Codex session with a chosen model can close it. Include a non-Anthropic model.
- KEY VALIDATION (blocked on rig access): full pack on a real quantized 12B at 8-16k under LEAN — pointer-indirection holds, LEAN floor fits, safety triggers fire.
- update-check notify-hook unexercised live — verify SessionStart stdout injection + real fetch against a configured PACK_SOURCE_URL on an actual Claude Code launch.
- upgrade.md prose-verified only — no end-to-end migration dry-run against a real older-version project (incl. pre-v12.0 deltas, NOT-SET setup-block fill, in-section-field flagging).
- PROBE 2 (opencode.json edit-ask live-fire), PROBE 3 (semgrep CI on first push).
- SETUP Step 0 distribution URL — maintainer fills the actual link (mechanism exists).

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`; `revised` retired); its
    own logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then
    the last entries of pack-dev/DECISION_LOG.md as needed. v12.9: the pack now
    SHIPS Light-tier subagent templates (.claude/agents, .opencode/agent,
    .codex/agents — all *.example, inert until renamed) plus activation steps in
    model-tiering.md, so OpenCode/Codex tiering is usable (predefine + restart),
    not just described. No build task queued — ask the user. Most actionable open
    item: a live tiering dogfood (activate light-checker with a real model,
    restart OpenCode, confirm delegation). This v12.9 commit is local on main;
    pushing needs user confirmation.
