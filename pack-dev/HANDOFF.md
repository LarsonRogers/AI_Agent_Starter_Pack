# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.5 · **Audience mode:** Developer
**Last completed:** Pass 2 — user-selectable FULL/LEAN pack profile (context-window.md owns it; Part 2 → Model Tiers carries Pack profile + Context budget; LEAN collapses Part 2 architecture/patterns to log pointers, checkpoints at 2-3, loads only strictly-needed protocols — never relaxes a gate). Independent review APPROVED (0 blockers, 2 minors fixed). Lightweight-for-local work COMPLETE (Pass 1 lossless slim + Pass 2 profile). v12.4→v12.5.
**Confirmed next task:** None committed — checkpoint reached (see below). Effectiveness trials continue.
**Branch:** `revised` (pushed to origin/revised; ahead of main)

**⚠️ CONTEXT CHECKPOINT:** This session completed ~5 logical tasks (model-tiering policy → provider-agnostic+tier-map → Pass 1 slim → Pass 2 profile). Per protocols/context-window.md, a fresh session is recommended before the next task to keep context sharp. This handoff is the resume point.

**Open watch items (OPEN — none silently closed):**
- KEY VALIDATION (blocked on rig access): run the full pack on a real quantized 12B (RTX 3070 8GB / 64GB RAM) at 8-16k under LEAN. Confirm (a) pointer-indirection holds on a 12B — Haiku passed as a proxy this session but is stronger than a 12B; (b) the LEAN floor actually fits the window; (c) safety triggers (secure-coding, safe-deletion, review) still fire. This is the make-or-break test for the whole lightweight-for-local effort.
- Model-tiering live dogfood, including a non-Anthropic tier map (OpenCode `openai/…` or local `ollama/…`) end-to-end.
- PROBE 2 — opencode.json edit-ask live-fire (needs OpenCode session).
- PROBE 3 — semgrep CI on first real push (needs GitHub Actions run).
- SETUP.md Step 0 — distribution link (user fills).

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `revised`, pushed to origin);
    its own logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md,
    then the last entries of pack-dev/DECISION_LOG.md as needed. v12.5: model
    tiering is provider-agnostic, and the lightweight-for-local work is done
    (Pass 1 lossless slim + Pass 2 FULL/LEAN profile). The big open item is the
    real-12B LEAN validation (needs the user's local rig). Report before any
    further pack edits.
