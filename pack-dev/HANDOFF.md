# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-16 · **Pack version:** v12.15 · **Audience mode:** Developer

**Latest (v12.15):** Added a **Project Stakes** dial (`protocols/project-stakes.md`) — Spike / Standard / Production, proposed at setup — that scales process ceremony (enforcement-tooling bundle, doc set, test depth, demo formality) but **never the safety floor** (secrets+secret-hook, secure-coding self-check, review-when-triggered, the day-one architecture sketch). Default = Standard (≈ current behavior); Spike auto-escalates up on real-data/auth/deploy. Born from the A/B probe (the pack applied full production ceremony to a toy, ~2× tokens). 7 consumers wired, protocols 32→33. Independent review APPROVE, 0 blockers (3 minors fixed). The *safe* minimization (gates ceremony, removes nothing); content-level trims await the 2nd A/B pair.

**Recent arc (v12.6→v12.15):** upgrade.md (migration) · model-tiering corrected + shipped templates + agent-driven activation + proactive offer + baked-in update source · update-check + notify-hook · Requirement Pressure-Test (v12.14) · Project Stakes (v12.15). Full detail in DECISION_LOG.md.

**Confirmed next task:** ask the user — no build task queued. Candidate: the **2nd A/B pair** (run the relational + login feature, 2× per arm) to fight N=1 and inform the deferred content-level trims (security checklist / meta-doc weight).

**Branch:** `main` — v12.15 committed locally, **2 commits ahead of origin** (v12.14 + v12.15). Pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- **2nd A/B pair** — run pack-dev/ab-test-pack-value.md pushed to the relational/login feature (where the architecture + security gap should bite hardest), 2× per arm. Probe-1 scratch repos at `I:/mega/megasync/projects/pack-ab-probe` (disposable). Findings so far: pack separated a data layer + tests + stricter validation; no-pack put SQL in route handlers (the anecdote reproduced); single-column retrofit was absorbable by both; pack cost ~2× tokens.
- **Project Stakes** is prose-verified only — no live run confirming a Spike actually drops the right ceremony while keeping the floor.
- **Requirement Pressure-Test** (v12.14) prose-verified only — no live run vs a real vague idea / inherited change / big brief (watch Non-dev scaling).
- **Tiering post-restart confirmation:** activation confirmed live in OpenCode; remaining = after restart the primary actually delegates a bounded scan to the Light agent (user eyeballing).
- **Notify-hook live-fire:** the hook's own `curl` to the baked-in Pack source URL is unexercised (sandbox-blocked here); URL-extraction + reachability + compare all verified.
- **KEY VALIDATION** (blocked on rig): full pack on a real quantized 12B at 8–16k under LEAN.
- **upgrade.md** prose-verified only — no end-to-end migration dry-run against a real older-version project.
- **PROBE 2** (opencode.json edit-ask live-fire), **PROBE 3** (semgrep CI on first push).
- Accepted wart: the pack-dev repo's own Part 2 ships as placeholders (it's the template), so the proactive tier-map offer fires every pack-dev session and can't be resolved without polluting the template — the maintainer just declines.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`; `revised` retired); its own
    logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then the
    last entries of pack-dev/DECISION_LOG.md as needed. Pack is at v12.15. No
    build task queued — ask the user. Most actionable open item: the 2nd A/B pair
    (relational + login feature) to inform deferred content-level trims. main is
    2 commits ahead of origin (local); pushing needs user confirmation.
