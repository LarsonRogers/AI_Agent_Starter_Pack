# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-15 · **Pack version:** v12.6 · **Audience mode:** Developer
**Last completed:** Built `protocols/upgrade.md` — the pack upgrade/migration procedure (procedure, not script). File-ownership table (pack-owned/replace-wholesale vs project-owned/never-touch) + 7 ordered steps: detect source+target version, branch `pack-upgrade/vX.Y`, splice AGENTS.md (preserve project Part 2 verbatim, add new sections as NOT-SET placeholders), diff-and-confirm enforcement/CI configs, apply pre-v12.0 structural deltas, self-checks, review+diff+handoff. Wired into AGENTS.md (standing rule + Index row, 29→30) and edge-cases.md (migrate-rather-than-halt pointer). Independent review APPROVED (0 blockers, 5 of 7 minors fixed). Headers v12.5→v12.6.

**Confirmed next task:** ask the user — the upgrade protocol closes the version-mismatch gap that was the last flagged build item. No build task is queued. Likely candidates from the watch list (user picks): the real quantized-12B LEAN validation (needs the user's rig), or a live dogfood of upgrade.md against an older-version deployed project if one is available.

**Branch:** `revised` (this commit is local; origin/revised is behind until pushed — push needs user confirmation)

**Open watch items (OPEN — none silently closed):**
- KEY VALIDATION (blocked on rig access): run the full pack on a real quantized 12B (RTX 3070 8GB / 64GB RAM) at 8-16k under LEAN. Confirm (a) pointer-indirection holds on a 12B (Haiku passed as a proxy, stronger than a 12B); (b) the LEAN floor fits the window; (c) safety triggers (secure-coding, safe-deletion, review) still fire. Make-or-break for the lightweight-for-local effort.
- upgrade.md is prose-verified only — no end-to-end migration dry-run against a real older-version deployed project yet, especially the pre-v12.0 CAPTAINS_LOG/ARCHITECTURE/PROTOCOLS delta path. Dogfood when such a project is available.
- Model-tiering live dogfood, including a non-Anthropic tier map (OpenCode `openai/…` or local `ollama/…`) end-to-end.
- PROBE 2 — opencode.json edit-ask live-fire (needs OpenCode session).
- PROBE 3 — semgrep CI on first real push (needs GitHub Actions run).
- SETUP.md Step 0 — distribution link (user fills).

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `revised`); its own logs live in
    pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the last entries
    of pack-dev/DECISION_LOG.md as needed. v12.6: protocols/upgrade.md now
    encodes pack upgrade/migration (was the last flagged build gap). No build
    task is queued — ask the user what's next; likely the real-12B LEAN
    validation (needs their rig) or a live dogfood of upgrade.md against an
    older-version project. This commit is local; pushing needs user confirmation.
