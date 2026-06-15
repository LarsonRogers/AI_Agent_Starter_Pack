# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.11 · **Audience mode:** Developer
**Last completed:** Baked the **canonical pack source URL** into the pack (v12.10→v12.11) so update-check works out of the box. `AGENTS.md` Part 2 → Related Docs → "Pack source" now holds `https://raw.githubusercontent.com/LarsonRogers/AI_Agent_Starter_Pack/main/AGENTS.md` and is **the single source of truth** — the notify-hook now greps the URL from AGENTS.md instead of a hardcoded copy, so both the on-demand check and the hook read that one field (zero config). `update-check.md` + `SETUP.md` Step 0 updated (distribution link filled to the GitHub repo; "works out of the box"; fork → change that one row). Independent review APPROVE, 0 blockers.

**Confirmed next task:** ask the user — no build task queued.

**Branch:** `main` — 1 commit ahead of origin (v12.11), local. Pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- **Notify-hook live-fire** (partially de-risked): URL-extraction from AGENTS.md, upstream reachability (WebFetch), and the version-compare are all verified; only the hook's own `curl` to the baked-in URL is unexercised — outbound network from the hook was blocked in this sandbox. Confirm on a real Claude Code launch that it fetches and notifies when behind.
- **Tiering live dogfood:** in a live OpenCode/Codex session, confirm the agent-driven activation (prompt → agent writes `.opencode/agent/light-checker.md` with a real model → restart → delegation fires). Include a non-Anthropic model.
- KEY VALIDATION (blocked on rig): full pack on a real quantized 12B at 8-16k under LEAN — pointer-indirection holds, LEAN floor fits, safety triggers fire.
- upgrade.md prose-verified only — no end-to-end migration dry-run against a real older-version project (pre-v12.0 deltas, NOT-SET setup-block fill, in-section-field flagging).
- PROBE 2 (opencode.json edit-ask live-fire), PROBE 3 (semgrep CI on first push).
- (Resolved this session: SETUP Step 0 distribution link filled; Pack source set.)

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`; `revised` retired); its
    own logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then
    the last entries of pack-dev/DECISION_LOG.md as needed. v12.11: the canonical
    pack source URL is baked into AGENTS.md Part 2 → "Pack source" (single source
    of truth; the notify-hook greps it from there), so update-check works with
    zero setup. No build task queued — ask the user. Most actionable open item: a
    live notify-hook fire and a live tiering dogfood. main is 1 commit ahead of
    origin (local); pushing needs user confirmation.
