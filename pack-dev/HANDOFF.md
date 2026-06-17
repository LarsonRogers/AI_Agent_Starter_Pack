# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-17 · **Pack version:** v12.16 · **Audience mode:** Developer

**Latest (pack-dev, no version change):** Built `pack-dev/validation-matrix.md` — the standing, harness-agnostic harness for proving each pack capability is *necessary* (adds value over the same model without the pack) vs redundant. Every Protocol Index capability has a row or is explicitly accounted-for; three test modes (M1 autonomous code-output / M2 cross-session fresh-agent resume / M3 interactive simulated-user ×3 knowledge levels); a ★ high-value subset any agent can run fast; runnable against Codex/OpenCode. Independent (adversarial) review APPROVE, 0 blockers, 8 minors fixed (control-conditioning so redundant outcomes can't read as wins; answer-key simulator; decorrelated judges; N≥2 for all behavioral tells; product-definition row; mechanical-C tagging; harness-agnostic scoping). `ab-test-pack-value.md` is now the *run-record*; `pack-dev/README.md` indexes both.

**Validation status:** ~2 of ~56 capabilities validated (✅ day-one architecture 2/2; ✅ secure-coding/CSRF 2/2). ⚠ formatter = the one redundancy found (already Spike-excluded). Everything else ☐ untested. A/B runs 1+2 (N=2) recorded in ab-test-pack-value.md; both load-bearing tells reproduced (no-pack flat+ships-CSRF / pack layered+closes-CSRF), and the v12.15 stakes dial fired correctly live (Standard at MVP → ratchet to Production on auth).

**Latest shipped pack (v12.16):** secure-coding re-weighted toward the high-miss items (born from probe-2). Prior arc v12.6→v12.16: upgrade/migration · model-tiering (corrected + templates + agent-driven activation + proactive offer + baked-in source) · update-check + notify-hook · requirement pressure-test (v12.14) · Project Stakes (v12.15). Human docs: README "Learn it", WALKTHROUGH.md, GUIDE.md.

**Confirmed next task:** run the ★ subset's 6 untested high-value rows from validation-matrix.md (cross-session resumption, secret-hook, scope-control, stuck-loop, guardrail refusals, requirement interrogation) at **full rigor**. Maintainer decided 2026-06-17 to **span the run across ≥2 sessions so token availability refreshes mid-way** — est. ~1.5–2.5M tokens / ~60–90 subagents total. The complete execution design (seed specs, per-row pass-criteria, agent counts, with-pack/control setup, suggested token-balanced session split) is pre-authored in **`pack-dev/star-subset-run-plan.md`** — read that first next session; nothing spawned yet, no scratch dirs created.

**Branch:** `main` — 1 commit ahead of origin (the validation-matrix, local). Pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- **Untested capabilities** — ~54 of 56 still ☐ in validation-matrix.md; the ★ subset is the priority. M3 (interactive) needs a built simulated-user; M2 needs a fresh-agent resume harness.
- **Project Stakes** + **Requirement Pressure-Test** — prose-verified only; no live trial yet (both are matrix rows now).
- **Tiering post-restart**, **notify-hook live-fire**, **KEY VALIDATION** (real 12B LEAN), **upgrade.md** e2e, **PROBE 2/3** — environment-dependent live checks, unchanged.
- Scratch A/B repos at `pack-ab-probe/{,run2}` (disposable).
- Accepted wart: this pack-dev repo's own Part 2 ships as placeholders, so the proactive tier-map offer fires every pack-dev session — the maintainer just declines.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`; `revised` retired); its own
    logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the last
    DECISION_LOG.md entries as needed. Pack is at v12.16. The standing capability-
    validation harness is pack-dev/validation-matrix.md (~2 of 56 validated; ★
    subset is the next priority). No build task queued — ask the user. main is 1
    commit ahead of origin (local); pushing needs user confirmation.
