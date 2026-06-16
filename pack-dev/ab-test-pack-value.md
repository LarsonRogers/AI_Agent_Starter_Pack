# A/B Test Protocol — Does the pack make a meaningful difference?

<!-- PACK-DEV ARTIFACT. Not part of the distributed pack. A methodology for
     comparing Claude Code WITHOUT the pack vs WITH the pack on the same project. -->

## Hypothesis

Claude Code alone writes good code but skips **process**: it under-architects,
builds an under-interrogated version of the request, and silently omits
security/tests — problems that surface *after* MVP. The pack's value is process
discipline (day-one architecture, requirement interrogation, security passes,
independent review, decision trail, demo gates), so its payoff lands post-MVP
and on ambitious projects, not on throwaways.

Origin: a real vibe-coded app where Claude "just didn't architect application
layers," discovered only after the MVP.

## What this measures — and what it does NOT

- **Does NOT measure:** line-level code quality. Both arms write solid code; a
  side-by-side of two MVPs will look equivalent and falsely read as "no
  difference."
- **DOES measure** the trajectory: architecture-fit under growth, building the
  *right* thing, security on auth/data code, recoverability, and "looked-done-
  but-wasn't" incidents.

Two traps this design avoids:
1. You can't hold "the project" constant — the pack changes the *interaction*
   (it interrogates and architects before coding). So evaluate the whole run,
   not just final code.
2. Stopping at MVP under-credits the pack — its tax is upfront, its return is
   post-MVP. The sequence below deliberately runs past MVP.

---

## The fixed prompt (paste verbatim into BOTH arms)

Deliberately under-specified — a real "vibe" prompt. Do NOT tighten it; the
vagueness is where requirement-interrogation and day-one architecture earn their
keep. It sits squarely in the pack's claimed-value regime (multi-user, shared
data, two entities, identity/permissions — it crosses the growth triggers).

> "I want a little web app for my book club. People should be able to add books
> we're reading and write short reviews, and everyone can see them."

That's the entire starting prompt. Nothing more until the agent asks.

**Persona rule:** when either agent asks a question, answer as the *same*
non-technical book-club organizer in both arms. Never volunteer to the no-pack
arm a decision (data model, permissions, auth) that you'd only have given because
the pack asked — that would do the pack's job for it and erase its lever. If the
no-pack agent doesn't ask, you don't tell.

## The run sequence (BOTH arms, in order, past MVP)

Each step is one work cycle. Run identically in both arms.

```
1. MVP            — add a book, write a review, see the list. (Walking skeleton
                    + first feature.)
2. 2nd entity     — per-book page showing all its reviews + a 1–5 star rating
                    with an average. (Forces a real Book↔Review relationship and
                    an aggregate — not flat storage.)
3. Schema change  — per-user "reading status" (want-to-read / reading / finished)
                    on each book. (A user↔book association + a migration over
                    data that already exists.)
4. Security feature— real login: reviews are attributed to who wrote them, and
                    only the author can edit or delete their own review.
                    (Authn + ownership/authz — classic IDOR territory.)
```

Steps 2–4 are the divergence points. Step 1 rarely separates the arms; the debt
shows up when the data model and permissions get stressed.

## Controls

- Same model, same Claude Code version, same machine, both arms.
- Fresh empty repo per arm. WITH-pack arm: drop the pack in first (Type B first
  session); NO-pack arm: nothing but `git init`.
- Same starting prompt + same persona answers (above).
- Capture per arm: the full transcript, the git history, the final repo, and
  (pack arm) DECISION_LOG/HANDOFF/AGENTS Part 2.
- Note wall-clock and token cost per step — the pack *should* cost more upfront;
  that's a tradeoff to report, not a loss.

---

## Scoring rubric (define before running; score after)

Score each dimension **0–3** per arm (0 = absent/harmful, 1 = poor, 2 = adequate,
3 = strong). Score from the trajectory + final state, not vibes.

| # | Dimension | What "3" looks like |
|---|-----------|---------------------|
| 1 | **Architecture fit** | Layers sized to the brief on day one; steps 2–4 slotted in without a painful refactor or UI-writes-storage tangle. |
| 2 | **Requirements fit** | Built what the organizer actually meant; permissions/visibility resolved *before* coding, not reworked after. |
| 3 | **Security** | Step 4 has real ownership checks (author-only edit/delete), input validation, no injection, secrets handled. |
| 4 | **Correctness / demo** | Each step actually works end-to-end and was shown running, not assumed done. |
| 5 | **Maintainability + trail** | A cold agent could extend it; decisions/architecture are recorded (not in the dev's head). |
| 6 | **Silent-wrong incidents** | (Count, not 0–3) Times something looked finished but wasn't — fewer is better. Log each. |
| 7 | **Rework / churn** | (Count) Times work had to be undone/redone because of an early wrong turn. |
| 8 | **Cost** | (Context, not scored) Tokens + wall-clock per step. |

### The decisive question (the origin anecdote, isolated)

> At step 3 or 4, did the app need an **architecture refactor that day-one
> layering would have avoided**? No-pack typically yes (the Step 3b failure);
> pack typically no. This single observation is worth more than the aggregate.

## Judging — and an honesty caveat about it

- **Blind on code + behavior:** hand a fresh-context agent both final repos +
  git histories (strip the pack's meta-docs so the arm isn't obvious) and have it
  score dimensions 1–4 + count 6–7 without knowing which is which.
- **Non-blind, separately:** dimension 5 (trail) is *itself* part of the pack's
  value and can't be blinded — score it openly and label it so.
- **Same-model self-judging is weak.** A fresh Claude judge is better than the
  author grading itself, but YOUR eye on dimensions 1–2 (architecture, right-
  thing-built) is what makes the result credible. Don't outsource those entirely.

## Statistical honesty

- **N=1 per arm is an anecdote, not evidence** — LLM runs vary. For signal, run
  2–3 per arm and look at the *pattern* (especially the decisive question). One
  run is suggestive; say so.
- Pre-register the rubric (this file) so scoring isn't rationalized after seeing
  results.

---

## Cheaper variant — the architecture probe (~30 min, isolates the anecdote)

If a full 4-step dual-build is too much, test the one thing you actually hit:

1. Both arms get the fixed prompt; run **only to MVP**.
2. Check one question: did the agent **decide and record a layer/structure
   choice before coding** (pack: product-definition Step 3b → S1–S4 sketch in
   AGENTS Part 2) vs dive straight into code?
3. Then ask both for step 2 (the 2nd entity) and watch whether the no-pack MVP's
   shape makes it awkward.

This won't measure security or requirements depth, but it directly probes the
"didn't architect layers" failure for a fraction of the cost.

## Expected outcome (stated up front, to be honest about bias)

The pack likely does NOT visibly improve line-level code. It likely shows up in
dimensions 1–3 and 5–6, and costs more on dimension 8. If it *doesn't* separate
on the decisive question across 2–3 runs, that's a real finding — log it; the
pack should earn its overhead or be trimmed.
