# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.7 · **Audience mode:** Developer
**Last completed:** Corrected the per-harness model-tiering mechanism (v12.6→v12.7). Verified against official docs that there are TWO mechanisms: per-DEFINITION model (pin a model in a named subagent — works in Claude Code, OpenCode, Codex) and per-CALL dynamic selection at spawn time (Claude Code ONLY). OpenCode/Codex have no per-call selector — to tier you predefine a tier-specific subagent and invoke it by name. Rewrote model-tiering.md "harness mechanism" + AGENTS.md Part 2 "How to switch" cells; fixed stale Codex caveat; added OpenCode #22130 (prefer .opencode/agent/*.md over opencode.json) + #6651 notes. Plus (user follow-up) a "never leave Model Tiers blank" rule: on new project / inherited onboarding / just-after-upgrade, prompt to fill (detect provider, propose Light+Capable, ask once; single model → single-tier auto; decline → single-tier explicit), wired into upgrade.md (Step 3 note + Step 7 close gate). Independent reviewer re-fetched all three docs and APPROVED (0 blockers).

**Confirmed next task:** ask the user — no build task queued.

**Branch:** `main` (consolidated; `revised` retired). This v12.7 work is committed locally on `main`; pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- KEY VALIDATION (blocked on rig access): run the full pack on a real quantized 12B (RTX 3070 8GB / 64GB RAM) at 8-16k under LEAN — confirm (a) pointer-indirection holds on a 12B (Haiku passed as proxy), (b) the LEAN floor fits, (c) safety triggers still fire.
- Model-tiering live dogfood — now specifically: exercise a PREDEFINED light-tier subagent in OpenCode and/or Codex (not a per-call override, which they don't support) to confirm the corrected mechanism works end-to-end. Include a non-Anthropic tier map.
- upgrade.md is prose-verified only — no end-to-end migration dry-run against a real older-version deployed project yet (esp. the pre-v12.0 CAPTAINS_LOG/ARCHITECTURE/PROTOCOLS delta path, and the new NOT-SET setup-block fill at close).
- PROBE 2 — opencode.json edit-ask live-fire (needs OpenCode session).
- PROBE 3 — semgrep CI on first real push (needs GitHub Actions run).
- SETUP.md Step 0 — distribution link (user fills).

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`; `revised` retired); its
    own logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then
    the last entries of pack-dev/DECISION_LOG.md as needed. v12.7: per-harness
    model tiering corrected (per-definition portable across all three; per-call
    is Claude-Code-only — OpenCode/Codex tier by predefining a tier subagent)
    and Model Tiers is now prompt-filled, never left blank, on project start or
    pack upgrade. No build task queued — ask the user what's next. Likely: the
    real-12B LEAN validation or a live tiering dogfood with a predefined
    light-tier OpenCode/Codex subagent. This v12.7 commit is local on main;
    pushing needs user confirmation.
