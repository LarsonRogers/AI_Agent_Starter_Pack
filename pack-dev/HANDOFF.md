# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.2 · **Audience mode:** Developer
**Last completed:** Model-tiering policy for sub-agents (new protocols/model-tiering.md; standing rule + Protocol Index row; review.md reviewer pinned to Capable tier; all headers v12.1→v12.2). Independent review APPROVED (0 blockers, 4 minors all fixed). Protocols 26→27, ls-vs-index 27=27.
**Confirmed next task:** Effectiveness trials (user-led, in progress — user reports empty-folder runs going well). Remaining probes are externally blocked; see below.
**Branch:** `revised` (19 commits ahead of main)

**Open watch items (OPEN — none silently closed):**
- PROBE 2 — `opencode.json` edit-ask + `.env` read-deny: must be live-fired in an OpenCode session (unverifiable from Claude Code).
- PROBE 3 — semgrep CI step: on first real push, plant a string-built query in a scratch branch; the security job must fail. (Local Windows semgrep = silent no-op; CI is the only trustworthy SAST surface.)
- SETUP.md Step 0: distribution-point placeholder awaiting the user's download link.
- NEW — model-tiering is prose-verified only: no live cheap-vs-capable sub-agent run has been dogfooded in a deployed project. Trial-phase candidate: have a deployed project route a bounded check (e.g. header-presence scan) to a Light-tier sub-agent and confirm the tier is logged + a Capable-tier review still catches a planted defect.
- Trial-phase suggestions (not commitments): non-dev empty-folder first-session run; inherited-codebase run; legacy CAPTAINS_LOG migration run.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `revised`); its own logs live
    in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the last
    entries of pack-dev/DECISION_LOG.md as needed. Build phase + wave 2 are
    complete (v12.2); current work is effectiveness trials — the remaining
    probes (2, 3) are externally blocked, and model-tiering wants a live
    dogfood run. Report results before any further pack edits.
