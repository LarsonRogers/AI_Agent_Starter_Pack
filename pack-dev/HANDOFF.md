# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.3 · **Audience mode:** Developer
**Last completed:** Provider-agnostic model tiering + per-project tier map. model-tiering.md split provider (which models exist) from harness (the switch); concrete map lives in AGENTS.md Part 2 → Model Tiers (bounded), established at stack selection (product-definition 3c / inherited 4c) with a safe single-tier default. Independent review APPROVED (0 blockers, 3 cosmetic minors, 2 fixed). v12.2→v12.3.
**Confirmed next task:** Effectiveness trials (user-led, in progress — empty-folder runs reported going well). Remaining probes externally blocked; see below.
**Branch:** `revised` (20 commits ahead of main)

**Open watch items (OPEN — none silently closed):**
- PROBE 2 — `opencode.json` edit-ask + `.env` read-deny: live-fire in an OpenCode session (unverifiable from Claude Code).
- PROBE 3 — semgrep CI step: on first real push, plant a string-built query in a scratch branch; the security job must fail. (Local Windows semgrep = silent no-op; CI is the only trustworthy SAST surface.)
- SETUP.md Step 0: distribution-point placeholder awaiting the user's download link.
- Model-tiering live dogfood: no live cheap-vs-capable sub-agent run yet. Trial — route a bounded check (e.g. header-presence scan) to a Light-tier sub-agent, confirm the tier is logged + a Capable-tier review still catches a planted defect. NOW ALSO: exercise a non-Anthropic tier map (e.g. an OpenCode `openai/…` or local `ollama/…` Light model) end-to-end to confirm the agnostic path works in practice, not just on paper.
- Trial-phase suggestions (not commitments): non-dev empty-folder first-session run; inherited-codebase run; legacy CAPTAINS_LOG migration run.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `revised`); its own logs live
    in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the last
    entries of pack-dev/DECISION_LOG.md as needed. Build phase + wave 2 are
    complete (v12.3); model tiering is now provider-agnostic with a per-project
    tier map. Current work is effectiveness trials — remaining probes (2, 3)
    are externally blocked, and tiering wants a live dogfood (including a
    non-Anthropic map). Report results before any further pack edits.
