# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-11 · **Pack version:** v11.51 (headers bump to v12.0 in commit 8) · **Audience mode:** Developer
**Last completed:** Commit 7 — pack-dev boundary, lore strip, placeholder classification, non-dev setup gaps
**Confirmed next task:** Commit 8 — consistency pass: session-type-D wording, testing-strategy trigger wording, read-order vs auto-load reality, `* text=auto` .gitattributes, sensitive-data scope line (known formats only; privileged content stays out of the repo), prune/verify known-limitations entries, v12.0 version bump + full self-checks
**Branch:** `revised` (11 commits ahead of main)

**Open watch items:**
- `.claude/settings.json` ask-rule prompt: verify in a FRESH Claude Code session (attempt a protocols/ edit → expect prompt). Rules load at session start; could not fire mid-session.
- `opencode.json` edit-ask prompt: verify live in an OpenCode session (cannot fire from Claude Code; schema-shape validated only; open OpenCode issue re: permission enforcement — defense-in-depth).
- SETUP.md Step 0 distribution-point placeholder: user fills in the download link.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `revised`); its own logs live
    in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the last
    entries of pack-dev/DECISION_LOG.md as needed. Continue the approved
    refactor at the task named above. One commit per step; demonstrate any
    gate failing before trusting it; pause for user approval between commits.
