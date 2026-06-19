# Walkthrough — building something small, end to end
<!-- Starter Pack v12.19 — 2026-06-18 -->
<!-- HUMAN-FACING DOC — for the user, NOT the agent. Agents must NOT load this
     file: it is not a protocol, is never in the session-start read order, and
     has no Protocol Index row. If you are an agent and reached this file, stop
     reading it — it is reference for people, not instructions for you. -->

A narrated example of the whole process: one loose idea → a working, extendable
app, showing what the agent *does* at each step and the artifacts it leaves
behind. Nothing here is special-cased — it is the pack's normal Type B (new
project) flow.

The example: **a little web app for a book club.** Read it once and the rest of
the pack will make sense.

> New here? `SETUP.md` covers installing the pack. `GUIDE.md` is the concepts +
> best-practices handbook. This file is the story that ties them together.

---

## 0. You start with a loose prompt

> *"I want a little web app for my book club. People should be able to add books
> we're reading and write short reviews, and everyone can see them."*

That's it. You do **not** write a spec — under-specifying is the point (see
GUIDE.md → "Give it a loose prompt"). The agent does the rest.

## 1. Session start (who are you, what kind of session)

The agent reads `AGENTS.md` (always), sees there's no `DECISION_LOG.md` and no
source files → **Type B, new project**. It asks one or two quick questions to set
your **Audience Mode** (Developer / Technical non-dev / Non-dev) and adapts its
explanation depth from then on.

## 2. Product definition — turning the idea into a plan

The agent runs the product-definition protocol, in order:

- **Elicit** the idea conversationally (what, who, where, must-do, must-NOT-do,
  any data about people).
- **Pressure-test it** (the requirement pressure-test) — surfaces the vague bits
  *before* coding: "When you say everyone can see reviews — anyone with the link,
  or just club members? Can someone edit or delete a review later, and only their
  own?" Each question says *why it's asking*. (It won't grill you over a trivial
  ask — only the risky unknowns.)
- **Write a Product Brief** for you to confirm:

  ```
  ## Product Brief — Book Club Shelf
  What it is:   a shared page where a book club adds books and short reviews
  Who it's for: members of one small club
  MVP:          add a book · write a review · see everyone's reviews
  NOT in MVP:   accounts/login · ratings · private clubs
  Success:      a member can add a book, post a review, and others see it
  Data & trust: names are optional free text; no accounts; small trusted group;
                worst case — a stranger posts spam
  ```

- **Recommend a stack** in plain English with a one-line WHY ("a small web app
  with a tiny server and a local database — fewest moving parts, runs on your
  machine, easy to verify").
- **Size the architecture (S1–S4)** *on day one* and write it down: this is
  multi-user shared data, so a real data layer — `views` → `routes` → `data
  layer (all the database code)` — with the rule *"routes never touch the
  database directly."* (That one decision is what keeps it maintainable as it
  grows — see §6.)
- **Set the model tier map** (which model runs which work) and **Project Stakes**.
  If you enable a cheaper Light tier, it also asks once whether to note in each
  work summary when it used that cheaper model — so you can see how often.
  Here it proposes **Standard** — "a real app a few people use, but no accounts
  or sensitive data yet" — not Spike (it's meant to be kept) and not Production
  (no real data / deploy). Stakes decides how much tooling and ceremony to set up.

## 3. The walking skeleton (backlog item 1)

The first backlog item is always *"get something minimal running end to end"* —
**not** a feature. It includes setting up the quality gates, **scaled to the
Standard stakes**: linter, formatter, type checks, tests, a secrets pre-commit
hook, and CI — each one **demonstrated catching a planted failure** so you know
it actually works. You see the app start in your browser. Then `RUNBOOK.md`,
`BACKLOG.md`, `DECISION_LOG.md`, and `HANDOFF.md` exist.

## 4. The first feature — the task loop

You say *"let people add a book."* The agent:

1. **Reformulates it into a task brief** and shows it back — *"confirm, amend, or
   reject."* The confirmed brief is the scope contract.
2. Reads the relevant files (pre-edit), writes the code in the right layer,
   writes tests.
3. **Demo gate** — shows you it running ("open the page, add a book — it appears
   in the list"). Tests passing isn't enough; you have to have *seen it run*.
4. **Closes the loop**: appends a `DECISION_LOG.md` entry, overwrites
   `HANDOFF.md`, commits.

A decision-log entry looks like:

```
## [2026-01-12] Add "add a book" form and listing — Claude Code
- Did: books table + POST /books (routes) → repo.addBook (data layer); index view lists books
- Decisions: book title required, author optional — WHY: matches the brief's MVP
- State: can add a book and see it in the shared list; reviews next
- Watch: no input length cap yet — fine until real users
```

## 5. Stopping and resuming later

You close your laptop. Next session (or a *different* agent / harness), the agent
reads `HANDOFF.md` and reports, unprompted: *"Last session we added book listing;
next up is posting reviews. Want me to continue?"* The handoff carries a
ready-to-paste resume prompt, so you can switch between Claude Code, Codex, and
OpenCode without losing the thread.

## 6. A growth moment — where the discipline pays off

Weeks later: *"Can people log in, and only the person who wrote a review edit or
delete it?"* This trips a **growth trigger** — adding authentication:

- **Project Stakes escalates** from Standard toward Production (logged) — accounts
  mean it's not a throwaway anymore.
- That fires the **security pass** (focused on the holes models actually miss —
  CSRF, session handling, access control) **and an independent fresh-context
  review** of the finished work.
- In a real head-to-head test, an agent *without* the pack shipped this exact
  feature with **no CSRF protection and rationalized it away**; with the pack, the
  **independent review caught it as a blocker and it got fixed** before "done."
  That is the whole point of the gate — it catches what looks finished but isn't.
- Because the data layer was decided on day one (§2), the new ownership check
  ("only the author can edit/delete") slots into the data layer cleanly instead
  of being smeared across the routes.

## What you end up with

A working, runnable app — *and* a decision log of how it got there, a current
handoff, a backlog of what's next, a runbook, quality gates that actually fail on
bad code, and an architecture that didn't rot as it grew. Any agent on any
supported harness can pick it up cold.

---

**Next:** `GUIDE.md` — the concepts behind each step and how to drive the agent
well (including the few things *you* should do: give loose prompts, answer the
pressure-test honestly, and never pressure it to skip the demo, the security
pass, or the review).
