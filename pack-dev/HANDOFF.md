# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.5 · **Audience mode:** Developer
**Last completed:** Pass 2 — user-selectable FULL/LEAN pack profile (context-window.md owns it; Part 2 → Model Tiers carries Pack profile + Context budget; LEAN collapses Part 2 architecture/patterns to log pointers, checkpoints at 2-3, loads only strictly-needed protocols — never relaxes a gate). Independent review APPROVED (0 blockers, 2 minors fixed). Lightweight-for-local work COMPLETE (Pass 1 lossless slim + Pass 2 profile). v12.4→v12.5.
**Confirmed next task:** Build `protocols/upgrade.md` — a pack-upgrade/migration protocol (TOP PRIORITY, user-confirmed). The pack currently DETECTS a version mismatch (edge-cases.md → Pack Version Mismatch Handler, halts) but has no procedure to MIGRATE an existing project to a newer pack version. The protocol must encode the splice-and-preserve upgrade:
  - Pack-owned files REPLACED wholesale: entire protocols/ (add new, delete removed), CLAUDE.md, TASK_TEMPLATE.md.
  - AGENTS.md: replace Part 1, PRESERVE the project's Part 2 verbatim; add Part 2 sections new to the target version (e.g. Model Tiers / Pack profile) as NOT-SET placeholders — never invent values.
  - NEVER touch: DECISION_LOG.md, HANDOFF.md, BACKLOG.md, RUNBOOK.md, source code.
  - Enforcement configs (.claude/settings.json, .codex/config.toml, opencode.json): diff and confirm per-change — may be user-customized.
  - Branch first (pack-upgrade/vX.Y), run self-checks (version grep all match, ls-vs-index both directions), show full diff before commit.
  - Handle version-to-version structural deltas: pre-v12.0 projects had ARCHITECTURE.md + PROTOCOLS.md (deleted) and CAPTAINS_LOG.md/CHANGELOG.md (replaced by DECISION_LOG.md + HANDOFF.md — migration path already in log-format.md). The protocol detects source version from the AGENTS.md header (or CAPTAINS_LOG for very old) and maps the deltas.
  - Wire-in: new Protocol Index row (29→30, ls-vs-index), a standing-rule line, and a pointer from the edge-cases version-mismatch handler ("to migrate rather than just halt, see protocols/upgrade.md"). Independent review before close.
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
    (Pass 1 lossless slim + Pass 2 FULL/LEAN profile). CONFIRMED NEXT TASK:
    build protocols/upgrade.md (pack-upgrade/migration protocol) — see the
    full spec in "Confirmed next task" above. Reformulate it into a task brief
    and confirm with the user before editing. (Also still open: the real-12B
    LEAN validation, which needs the user's local rig.)
