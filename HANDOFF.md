# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     not copied into deployed projects. Overwritten after every committed task. -->

**As of:** 2026-06-11 · **Pack version:** v11.51 (headers bump to v12.0 in commit 8) · **Audience mode:** Developer
**Last completed:** Commit 6 — breadcrumb mechanism (DECISION_LOG.md + HANDOFF.md, CHANGELOG retired)
**Confirmed next task:** Commit 7 — lore strip, placeholder classification, non-dev setup gaps (Node/npm + OpenCode install, pack-acquisition placeholder, git init assignment), known-limitations.md move out of protocols/
**Branch:** `revised` (8 commits ahead of main)

**Open watch items:**
- `.claude/settings.json` ask-rule prompt: verify in a FRESH Claude Code session (attempt a protocols/ edit → expect prompt). Rules load at session start; could not fire mid-session.
- `opencode.json` edit-ask prompt: verify live in an OpenCode session (cannot fire from Claude Code; schema-shape validated only). Note open OpenCode issue re: permission enforcement — treat as defense-in-depth.
- known-limitations.md: pack-dev meta currently indexed as a triggerable protocol (counted in the 24) — move out of protocols/ in commit 7/8, drop index row, keep ls-vs-index check honest.
- Pack-dev artifacts (this file, DECISION_LOG.md, known-limitations.md): exclude from deployed-project distribution in commit 7/8.
- Commit 8 queue: `* text=auto` .gitattributes; sensitive-data scope line (catches known formats, not arbitrary confidential content; bash-read bypass note already recorded); session-type-D + testing-trigger wording; read-order vs auto-load reality; v12.0 bump everywhere.

**Resume prompt (paste into any agent):**

    Read AGENTS.md, then HANDOFF.md, then the last entries of DECISION_LOG.md
    as needed. This is the pack-development repo itself (branch `revised`).
    Continue the approved 8-commit refactor at the task named above. One
    commit per step; demonstrate any gate failing before trusting it; pause
    for user approval between commits.
