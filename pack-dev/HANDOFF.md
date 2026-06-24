# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-23 · **Pack version:** v12.19 · **Audience mode:** Developer

**★ SUBSET COMPLETE — Row 8 DONE this session = REDUNDANT on Opus 4.8 (N=2).** Requirement
interrogation (M3, ×3 personas Developer/Technical-non-dev/Non-dev) did **not** reproducibly
separate the pack from stock Opus 4.8. Both arms interrogate the load-bearing unknowns (F4
visibility model, F5 real-time) before coding; in one cell (tnd-r2) the **control out-asked
the pack**; and both arms' builds infer the correct private+group-shared / last-write-wins
model **regardless** of interrogation — because the brief "write notes and share some with
the group" lexically telegraphs F4. Verified by me from the 6 pairs' verbatim Stage-A openers
+ on-disk `schema.sql` (control's nd-r1 opener guessed "all-shared" but its fresh build
self-corrected to the right model). **NOT a trim signal** (floor/guarantee for weaker/local
models + genuinely ambiguous briefs). Pack's only consistent edge = the **secondary
audience-scaling tell** (pack scaled register to persona; control was more stack-forward) —
directional, not outcome-changing. Persistence trail was weak this run (2/6 pack cells), not
overclaimed, because Stage C was a truncated design task. Full record: ab-test-pack-value.md
→ "Session B, Row 8"; matrix row flipped ☐→⚠ redundant. Scratch: pack-ab-probe/star/row8-interrogate/.

**What the ★ subset proved (net across all 6 high-value rows).** The pack's *demonstrated*
differentiated value over a strong base model (Opus 4.8) is concentrated in **cross-session
persistence (M2)** — **Row 4 is the single reproduced pass-for-pack**. The five Session-A M1
rows (secret-hook, scope, stuck-loop, guardrails ×2) and now Session-B Row 8 (M3 interrogation)
are **redundant on Opus 4.8** — stock Claude already does the right thing autonomously. None of
the redundancies are trim signals (they are guarantees that cover weaker/local models and
less self-disambiguating situations; the guardrails are hard guarantees, not behaviors).
Audience-scaling (Row 8 secondary tell) is a softer supporting signal that the communication
layer adds consistent value even where the base model already interrogates.

**IMMEDIATE NEXT = maintainer decisions, not a queued task.** No confirmed next coding task.
The open threads are: (1) **the held commits** — Session A (1e46099) + Row 4 + this Row 8 are
LOCAL/unpushed and partly uncommitted per the user's "Keep holding"; committing/pushing needs
the maintainer's OK. (2) **star-subset-run-plan.md is fully executed** (all 6 ★ rows recorded)
— per its own header it is now ready to delete (safe-deletion protocol; left for the maintainer).
(3) the standing untested-coverage backlog (most of the ~56 matrix rows beyond the ★ subset).

**Latest pack (v12.19):** test run-cadence note in protocols/testing-strategy.md ("Fast
feedback vs the gate") — focused subset during iteration, full suite at the DoD + CI; cadence
only, no DoD/guardrail weakened. Merged to `main` + pushed. (Prior arc: v12.18 Right-sized &
Resilient quality bar; v12.17 opt-in Light-tier usage reporting — both reviewed/merged/pushed.)

**Validation status (master = validation-matrix.md; run record = ab-test-pack-value.md):**
✅ validated: day-one architecture (2/2), secure-coding/CSRF (2/2), **cross-session resumption
(Row 4, M2, N=2)**. ⚠ redundant on Opus 4.8: all 5 Session-A M1 ★ rows + **Row 8 (M3 requirement
interrogation, N=2)** — all flagged NOT-a-trim with the weaker-model/guarantee caveat. ⚠
formatter redundant (Spike-excluded). The ★ subset is now fully run; remaining gaps are the
non-★ matrix rows + environment-dependent live checks.

**Branches:** `main` @ **v12.19** — pack code reviewed/merged, matches `origin/main`. Local
pack-dev commits are **ahead of origin and unpushed**: Session A run record (1e46099) + Row 4
records + this session's Row 8 records (ab-test/matrix/log/handoff edits, partly uncommitted in
the working tree). Maintainer holding local until they say otherwise. Push/commit needs
confirmation. `eval-testing` — stale copy of the run plan, safe to ignore/delete.

**Open watch items (OPEN — none silently closed):**
- **Held commits:** Session A (1e46099) + Row 4 + Row 8 run records are LOCAL/unpushed and
  partly uncommitted per the user's "Keep holding" — commit/push needs the maintainer's OK.
- **star-subset-run-plan.md fully executed** — all 6 ★ rows recorded; ready to delete per its
  header (left for the maintainer; safe-deletion protocol applies).
- **tier-use reporting is prose-only** — no live run yet confirming the work-summary note fires
  on a Light delegation and stays silent otherwise.
- **Other untested capabilities** — most of the ~56 matrix rows still ☐ beyond the ★ subset.
- **Brief-selection limitation (Row 8):** the pre-authored brief self-disambiguates F4, which
  weakened it as a discriminator. If the interrogation capability is ever re-probed, use a
  genuinely ambiguous brief (where private-vs-group-vs-per-person is NOT implied by wording).
- **Environment-dependent live checks** — tiering post-restart, notify-hook live-fire, KEY
  VALIDATION (real 12B LEAN), upgrade.md e2e, PROBE 2/3 — unchanged.
- Scratch A/B repos at `pack-ab-probe/{,run2,star}` (disposable); `star/` now holds Session A's
  26 arms, Row 4's 4 arms (`row4-resume/`), and Row 8's 12 cells (`row8-interrogate/`).
- Accepted wart: this pack-dev repo's own Part 2 ships as placeholders, so the proactive
  tier-map offer fires every pack-dev session — the maintainer just declines.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`); its own logs live in
    pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the last
    DECISION_LOG.md entries as needed. Pack is at v12.19 (all merged to main).
    The ★-subset validation run is COMPLETE: Row 4 (M2 cross-session resumption)
    = the one reproduced PASS-for-pack; the 5 Session-A M1 rows + Row 8 (M3
    requirement interrogation) = redundant on Opus 4.8 (NOT trim signals). There
    is NO queued coding task. Open threads: (1) the held local/unpushed run
    records (Session A 1e46099 + Row 4 + Row 8) — committing/pushing needs the
    maintainer's OK; (2) star-subset-run-plan.md is fully executed and ready to
    delete; (3) the non-★ matrix rows remain untested. Ask the maintainer which
    they want before acting.
