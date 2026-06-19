# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-18 · **Pack version:** v12.19 · **Audience mode:** Developer

**Latest pack (v12.19):** **test run-cadence note** in protocols/testing-strategy.md ("Fast feedback vs the gate"). Clarifies what to run when: during iteration, the focused subset (affected file / single test / changed-only mode — `jest --changed` etc.) for speed; at the DoD + CI, the **full suite** must pass (catches regressions elsewhere; a passing subset never satisfies the DoD). Scales run *cadence* only, not coverage/authoring; reaffirms the full-suite gate, no DoD/guardrail weakened. Review skipped by user (small additive note); merged to `main` + pushed.

**Prior shipped pack (v12.18):** explicit **Right-sized & Resilient** quality bar. New section in protocols/code-quality.md stipulating produced code is as **lightweight and robust as the project's stakes warrant** — *fit, not maximal* — Lightweight (fewest adequate dependencies, no speculative abstraction/YAGNI, remove dead weight, appropriate efficiency not premature optimization) + Robust (validate at boundaries, handle real failure modes, fail loudly, degrade gracefully). Both scale with Project Stakes; both subordinate to the existing rules + safety floor; doesn't change scope control. Folded one clause into the AGENTS.md "Code quality" Standing Rule (no new always-on bullet). Independent fresh-context review APPROVE, 0 blockers (2 by-design minors). Merged to `main` + pushed.

**Prior shipped pack (v12.17):** opt-in **Light-tier usage reporting**. When enabled, the agent appends a one-line note to its post-prompt work summary whenever ≥1 sub-task ran on the cheaper Light model that turn (silence = none), so the user sees how often it happens. Preference = new AGENTS.md Part 2 → Model Tiers → `Tier-use reporting` field (`on`/`off`/`n/a — single-tier`), default OFF, asked ONCE at tier setup and only when a Light tier exists. Behavior single-sourced in protocols/model-tiering.md ("Surfacing Light-tier use to the user (opt-in)" + activation step 2b); surfacing only — routing/guardrails/log behavior unchanged. Human docs updated same-commit. Independent fresh-context review APPROVE, 0 blockers (2 cosmetic/by-design minors). Merged to `main` + pushed.

**Validation status:** ~2 of ~56 capabilities validated (✅ day-one architecture 2/2; ✅ secure-coding/CSRF 2/2). ⚠ formatter = the one redundancy found (already Spike-excluded). Everything else ☐ untested. A/B runs 1+2 (N=2) in ab-test-pack-value.md; both load-bearing tells reproduced (no-pack flat+ships-CSRF / pack layered+closes-CSRF); v12.15 stakes dial fired correctly live.

**Prior arc v12.6→v12.16:** upgrade/migration · model-tiering (templates + agent-driven activation + proactive offer + access-method caveat) · update-check + notify-hook · requirement pressure-test (v12.14) · Project Stakes (v12.15) · secure-coding re-weight (v12.16). Standing harness pack-dev/validation-matrix.md (run-record ab-test-pack-value.md).

**Confirmed next task:** run the ★ subset's 6 untested high-value rows from validation-matrix.md (cross-session resumption, secret-hook, scope-control, stuck-loop, guardrail refusals, requirement interrogation) at **full rigor**, deliberately **spanned across ≥2 sessions so tokens refresh** (maintainer decision 2026-06-17). Full execution design pre-authored in `pack-dev/star-subset-run-plan.md` (read first; nothing spawned yet). Still owed before the M3 row: pre-author the per-persona answer ledgers.

**Branches:** `main` — now at **v12.19**, carrying v12.17 Light-tier usage reporting + v12.18 Right-sized & Resilient (both reviewed APPROVE) + v12.19 test run-cadence note (review skipped by user), all merged + pushed to `origin/main`. `eval-testing` — the ★-subset run plan (pushed, separate concern).

**Open watch items (OPEN — none silently closed):**
- **NEW — tier-use reporting is prose-only:** no live run yet confirming the work-summary note fires on a Light delegation and stays silent otherwise.
- **Untested capabilities** — ~54 of 56 still ☐; the ★ subset is the priority. M3 needs the answer-ledgers; M2 needs the fresh-agent resume substrate (both detailed in star-subset-run-plan.md).
- **Project Stakes** + **Requirement Pressure-Test** — prose-verified only; no live trial yet.
- **Tiering post-restart**, **notify-hook live-fire**, **KEY VALIDATION** (real 12B LEAN), **upgrade.md** e2e, **PROBE 2/3** — environment-dependent live checks, unchanged.
- Scratch A/B repos at `pack-ab-probe/{,run2}` (disposable); ★-subset scratch root will be `pack-ab-probe/star/` (not yet created).
- Accepted wart: this pack-dev repo's own Part 2 ships as placeholders, so the proactive tier-map offer fires every pack-dev session — the maintainer just declines.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`); its own logs live in
    pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the last
    DECISION_LOG.md entries as needed. Pack is at v12.18 — both v12.17 (Light-tier
    usage reporting) and v12.18 (Right-sized & Resilient quality bar) are reviewed,
    merged to main, and pushed to origin.
    The standing capability-validation harness is pack-dev/validation-matrix.md
    (~2 of 56 validated); the next queued work is the ★-subset run, design in
    pack-dev/star-subset-run-plan.md, spanned across ≥2 sessions. Pushing/merging
    needs user confirmation.
