# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-16 · **Pack version:** v12.16 · **Audience mode:** Developer

**Latest (v12.16):** A/B **probe-2 (security)** run + recorded (pack-dev/ab-test-pack-value.md → Results). Finding: both arms got IDOR/ownership right unprompted; the divergence was **CSRF** — no-pack shipped login/edit/delete with no CSRF and rationalized it; the pack's **independent-review gate caught it as a blocker and forced the fix** (+ closed a username-enumeration channel). Acted on it: **re-weighted secure-coding.md** toward the high-miss items (CSRF / sessions+rate-limit / authz-on-every-endpoint / enumeration) with a "verify these hardest" block, reframing the basics as "capable model usually handles — confirm, don't belabor" (weak/local models still apply them in full). No checklist item deleted. Independent review APPROVE, 0 blockers (2 minors fixed). Resolves the deferred trim question: KEEP the review + secure-coding gates — they caught a live vuln.

**Prior (v12.15):** Added a **Project Stakes** dial (`protocols/project-stakes.md`) — Spike / Standard / Production, proposed at setup — that scales process ceremony (enforcement-tooling bundle, doc set, test depth, demo formality) but **never the safety floor** (secrets+secret-hook, secure-coding self-check, review-when-triggered, the day-one architecture sketch). Default = Standard (≈ current behavior); Spike auto-escalates up on real-data/auth/deploy. Born from the A/B probe (the pack applied full production ceremony to a toy, ~2× tokens). 7 consumers wired, protocols 32→33. Independent review APPROVE, 0 blockers (3 minors fixed). The *safe* minimization (gates ceremony, removes nothing); content-level trims await the 2nd A/B pair.

**Recent arc (v12.6→v12.15):** upgrade.md (migration) · model-tiering corrected + shipped templates + agent-driven activation + proactive offer + baked-in update source · update-check + notify-hook · Requirement Pressure-Test (v12.14) · Project Stakes (v12.15). Full detail in DECISION_LOG.md.

**Confirmed next task:** ask the user — no build task queued. Pending the maintainer's call: option **(c) a FRESH replication pair** (new repos, 2× per arm) to fight N=1, now that probe-1 (architecture) + probe-2 (security) are both run and their findings acted on (v12.15 stakes dial, v12.16 secure-coding re-weight).

**Branch:** `main` — v12.16 committed locally, 1 commit ahead of origin. Pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- **A/B replication (option c)** — probe-1 (architecture) + probe-2 (security) are DONE and recorded in pack-dev/ab-test-pack-value.md (Results — run 1); scratch repos at `I:/mega/megasync/projects/pack-ab-probe` (disposable). What's left is a FRESH N>1 replication to confirm the pattern isn't a single-run fluke (esp. whether no-pack reliably ships the CSRF gap and the pack's review reliably catches it). Maintainer deciding whether to spend on it.
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
    last entries of pack-dev/DECISION_LOG.md as needed. Pack is at v12.16. No
    build task queued — ask the user. A/B probe-1 (architecture) + probe-2
    (security) are done and acted on (v12.15 stakes dial, v12.16 secure-coding
    re-weight); the open option is a fresh N>1 replication. main is 1 commit
    ahead of origin (local); pushing needs user confirmation.
