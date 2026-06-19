# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-18 · **Pack version:** v12.19 · **Audience mode:** Developer

**Latest pack (v12.19):** **test run-cadence note** in protocols/testing-strategy.md ("Fast feedback vs the gate"). Clarifies what to run when: during iteration, the focused subset (affected file / single test / changed-only mode — `jest --changed` etc.) for speed; at the DoD + CI, the **full suite** must pass (catches regressions elsewhere; a passing subset never satisfies the DoD). Scales run *cadence* only, not coverage/authoring; reaffirms the full-suite gate, no DoD/guardrail weakened. Review skipped by user (small additive note); merged to `main` + pushed.

**Prior shipped pack (v12.18):** explicit **Right-sized & Resilient** quality bar. New section in protocols/code-quality.md stipulating produced code is as **lightweight and robust as the project's stakes warrant** — *fit, not maximal* — Lightweight (fewest adequate dependencies, no speculative abstraction/YAGNI, remove dead weight, appropriate efficiency not premature optimization) + Robust (validate at boundaries, handle real failure modes, fail loudly, degrade gracefully). Both scale with Project Stakes; both subordinate to the existing rules + safety floor; doesn't change scope control. Folded one clause into the AGENTS.md "Code quality" Standing Rule (no new always-on bullet). Independent fresh-context review APPROVE, 0 blockers (2 by-design minors). Merged to `main` + pushed.

**Prior shipped pack (v12.17):** opt-in **Light-tier usage reporting**. When enabled, the agent appends a one-line note to its post-prompt work summary whenever ≥1 sub-task ran on the cheaper Light model that turn (silence = none), so the user sees how often it happens. Preference = new AGENTS.md Part 2 → Model Tiers → `Tier-use reporting` field (`on`/`off`/`n/a — single-tier`), default OFF, asked ONCE at tier setup and only when a Light tier exists. Behavior single-sourced in protocols/model-tiering.md ("Surfacing Light-tier use to the user (opt-in)" + activation step 2b); surfacing only — routing/guardrails/log behavior unchanged. Human docs updated same-commit. Independent fresh-context review APPROVE, 0 blockers (2 cosmetic/by-design minors). Merged to `main` + pushed.

**Validation status:** ✅ validated: day-one architecture (2/2), secure-coding/CSRF (2/2). ⚠ **redundant on Opus 4.8 (Session A, 2026-06-18, N=2):** all 5 cheap M1 ★ rows — pre-commit secret hook, scope control, stuck-loop, guardrail refusals (secrets + destructive). Stock Opus 4.8 did the right thing autonomously on every one (control even built a secret hook unprompted; both refused the secret-commit + the table-drop; both stayed in scope; neither hallucinated the fake API). Verified by me directly (git/grep/sqlite/mechanical-commit), no contamination. **NOT a trim signal for the hard guardrails** (redundancy on a strong safety-trained model ≠ weaker-model behavior; the rules are guarantees). The one pack-vs-control difference seen = the persistence trail (pack arms wrote DECISION_LOG/HANDOFF; no control did) — that's M2, not these rows. ⚠ formatter = the other redundancy (Spike-excluded). Full record: ab-test-pack-value.md → "Session A".

**Prior arc v12.6→v12.16:** upgrade/migration · model-tiering (templates + agent-driven activation + proactive offer + access-method caveat) · update-check + notify-hook · requirement pressure-test (v12.14) · Project Stakes (v12.15) · secure-coding re-weight (v12.16). Standing harness pack-dev/validation-matrix.md (run-record ab-test-pack-value.md).

**Confirmed next task — ★-subset Session B** (the heavy, pack-only rows; Session A done): **cross-session resumption (M2, N≥2)** and **requirement interrogation (M3, ×3 personas, N≥2)**. This is where the pack should actually separate — Session A showed the M1/guardrail behaviors are inherent to a strong base model, so M2 (persistence) + M3 (interaction) are the real test. Execution design AND the pre-authored M3 per-persona answer ledgers (Developer / Technical non-dev / Non-dev for the "notes app with collaboration" brief) are both in `pack-dev/star-subset-run-plan.md` (Rows 4 + 8) — **no prep left; Session B can start immediately**. Est. ~0.9–1.7M tokens — spanned to a fresh session per the token-refresh decision (2026-06-17). The Session-A workflow harness pattern (pre-staged seeds + parallel pack-vs-control arms + verify tells yourself) is reusable; Session A scratch repos at `pack-ab-probe/star/`.

**Branches:** `main` @ **v12.19** — pack code (v12.17–v12.19) is reviewed/merged and matches `origin/main`, BUT main is **1 commit ahead of origin (local, unpushed): the Session A run record** (`1e46099`) — maintainer chose to leave it local until after Session B. Push needs confirmation. `eval-testing` — older copy of the run plan (pushed); now superseded by main's copy, safe to ignore/delete.

**Open watch items (OPEN — none silently closed):**
- **NEW — tier-use reporting is prose-only:** no live run yet confirming the work-summary note fires on a Light delegation and stays silent otherwise.
- **★ Session B is the priority** — cross-session resumption (M2) + requirement interrogation (M3). M3 answer-ledgers are now PRE-AUTHORED in star-subset-run-plan.md (no prep left); M2 still needs a session-1 build substrate (design in the plan, Row 4).
- **Other untested capabilities** — most of the ~56 still ☐ beyond the ★ subset.
- **Requirement Pressure-Test** — still no isolated live trial (Session B Row 8 IS that trial). **Project Stakes** — prose-verified only.
- **Tiering post-restart**, **notify-hook live-fire**, **KEY VALIDATION** (real 12B LEAN), **upgrade.md** e2e, **PROBE 2/3** — environment-dependent live checks, unchanged.
- Scratch A/B repos at `pack-ab-probe/{,run2,star}` (disposable); `star/` holds Session A's 26 arms + the reusable seed/pack templates.
- Accepted wart: this pack-dev repo's own Part 2 ships as placeholders, so the proactive tier-map offer fires every pack-dev session — the maintainer just declines.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`); its own logs live in
    pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the last
    DECISION_LOG.md entries as needed. Pack is at v12.19 (all merged to main).
    NEXT TASK = ★-subset Session B: cross-session resumption (M2) + requirement
    interrogation (M3, ×3 personas), N≥2 — the full design AND the pre-authored M3
    answer ledgers are in pack-dev/star-subset-run-plan.md (read it; no prep left).
    Session A (the 5 M1 rows) is DONE — all redundant on Opus 4.8, recorded in
    ab-test-pack-value.md → "Session A". NOTE: main has 1 LOCAL unpushed commit
    (the Session A record, 1e46099) the maintainer is holding until after Session B;
    pushing/merging needs user confirmation.
