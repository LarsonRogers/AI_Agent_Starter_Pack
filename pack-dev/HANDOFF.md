# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.4 · **Audience mode:** Developer
**Last completed:** Pass 1 of lightweight-for-local work — lossless always-on slim. Moved First Session/Resumption checklists → protocols/session-start.md and Pre-Edit + checkpoint → protocols/task-workflow.md; compressed Standing Rules + Protocol Index. Guardrails + full DoD kept verbatim always-on. Floor ~9226t→~8254t (~11%). Independent review APPROVED (0 blockers, lossless verified). Protocols 27→29. v12.3→v12.4.
**Confirmed next task:** Pass 2 — the user-selectable FULL/LEAN profile (see watch items). Plus ongoing effectiveness trials.
**Branch:** `revised` (pushed to origin/revised; ahead of main)

**Open watch items (OPEN — none silently closed):**
- PASS 2 (next, confirmed direction): add `pack profile` (FULL / LEAN) + `context budget` to AGENTS.md Part 2 → Model Tiers; session-start router reads the profile; checkpoint cadence (context-window.md) scales to the context window; add a LEAN Part 2 variant (architecture/patterns → pointers) for the biggest local-specific floor cut. Decided model: lean single AGENTS.md (no second entrypoint, no RAG). FULL = resident discipline + aggressive checkpointing (needs ~32k); LEAN = slim + reduced ambition (runs ~8-16k).
- Indirection risk: weak/local models must reliably follow "load protocol X" pointers now that checklists are externalized — validate in the local dogfood; if a 12B skips pointers, reconsider what stays resident.
- PROBE 2 — opencode.json edit-ask live-fire (needs OpenCode session).
- PROBE 3 — semgrep CI on first real push (needs GitHub Actions run).
- SETUP.md Step 0 — distribution link (user fills).
- Model-tiering live dogfood, including a non-Anthropic tier map (OpenCode `openai/…` or local `ollama/…`) end-to-end.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `revised`, pushed to origin);
    its own logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md,
    then the last entries of pack-dev/DECISION_LOG.md as needed. v12.4: model
    tiering is provider-agnostic, and Pass 1 of the lightweight-for-local work
    (lossless always-on slim) is done. Next is Pass 2 — the user-selectable
    FULL/LEAN profile. Report before further pack edits.
