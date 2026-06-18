# Guide — how the pack works and how to drive it well
<!-- Starter Pack v12.18 — 2026-06-18 -->
<!-- HUMAN-FACING DOC — for the user, NOT the agent. Agents must NOT load this
     file: it is not a protocol, is never in the session-start read order, and
     has no Protocol Index row. If you are an agent and reached this file, stop
     reading it — it is reference for people, not instructions for you. -->

The conceptual handbook. `SETUP.md` installs the pack; `WALKTHROUGH.md` shows one
project end to end; **this** explains *how it all works* and *how to get the most
out of it.* You don't need to read it to start — the agent drives itself — but it
makes you a much better operator.

---

## The mental model

- **`AGENTS.md` is the single source of truth.** Part 1 is fixed policy
  (guardrails, session protocols, the Definition of Done). Part 2 is *your*
  project's specifics, which the agent fills in and keeps current. Codex and
  OpenCode read it directly; Claude Code reads it through `CLAUDE.md`.
- **Protocols load on demand.** The ~30 files in `protocols/` are detailed
  procedures. The agent only loads the one its current situation triggers (via
  the Protocol Index in AGENTS.md), so context stays lean. You never manage this.
- **The breadcrumb system is how nothing gets lost.** `DECISION_LOG.md` is an
  append-only history (what changed, why, watch items). `HANDOFF.md` is a small,
  always-current "where are we + how to resume" snapshot, overwritten every task.
  Together they let *any* agent on *any* harness pick the project up cold.

## Does the discipline actually help?

An informal A/B comparison — the same vague "book club app" prompt built twice by
the same model, once with the pack and once without, then pushed past MVP to a
login feature — found two consistent differences (small sample, directional, not
a controlled study):

- **Structure.** Without the pack, the app put database access straight inside the
  request handlers — fine at first, painful as it grows. With the pack, the data
  layer was decided and written down on day one and held as features were added.
  (The day-one architecture sketch earning its keep.)
- **The non-obvious security miss.** Both versions got the *obvious* access control
  right (only a review's author can edit it). But the un-packed version shipped
  login with **no CSRF protection** and waved it off — while the pack's security
  pass and independent review caught and fixed it.

The takeaway isn't "the pack writes better code line-for-line" — both wrote solid
code. It's that the pack catches what a capable model does *competently but
incompletely*: the structure that bites later, and the security hole it doesn't
think to mention. That's what the ceremony buys — and why the **Spike** stakes
level exists for when you don't need it.

## The four dials

The agent sets these once at setup (and you can change them). They tune behavior
without changing the rules:

| Dial | Options | What it controls |
|------|---------|------------------|
| **Audience Mode** | Developer · Technical non-dev · Non-dev | How much it explains, how it phrases errors |
| **Model Tiers** | Capable + optional Light | Routes bounded, rule-bound checks to a cheaper/faster model; judgment + safety work stay on the main one; can optionally report in each work summary when it used the cheaper model |
| **Pack profile** | FULL · LEAN | Resident footprint — LEAN is for small-context / local models |
| **Project Stakes** | Spike · Standard · Production | How much *process ceremony* (tooling, docs, tests, demos) — see below |

## Project Stakes — the one to understand

Tells the agent how much rigor the project deserves, so a throwaway isn't
burdened with production machinery and a real system isn't under-built:

- **Spike** — throwaway / experiment. Light tooling, minimal docs.
- **Standard** (default) — a real thing a few people use. The sensible middle.
- **Production** — shipped, shared, or handling real/sensitive data. Full rigor.

It scales the *expensive* stuff (CI, dependency/security scanning, the full doc
set, coverage targets, demo formality). It **never** scales the **safety floor**:
secrets are always protected, the security self-check always runs on
auth/data/input code, the independent review always fires when triggered, and the
day-one architecture sketch is always made. A Spike automatically **ratchets up**
the moment real data, accounts, or a deploy appears — a throwaway can't quietly
become a real system at throwaway rigor.

## The lifecycle (session types)

The agent figures this out automatically at session start:

- **New project (B)** — you have an idea, no code. Runs product definition.
- **Resuming (A)** — a decision log exists. Reads the handoff, reports where you
  left off.
- **Inherited code (C)** — existing code, no pack history. Assesses the codebase
  before touching anything, then asks what you want to do.
- **Refactor (D)** — explicit structural goal, no new features.

## How to drive it well (the actual best practices)

1. **Give it a *loose* prompt; don't over-specify.** "A site where my club shares
   books" beats a three-page spec. Over-specifying does the agent's
   requirement-interrogation *for* it and you lose that safety net.
2. **Answer the pressure-test honestly.** On vague or ambitious work it will ask
   pointed questions (edge cases, who-can-do-what, what "done" means). That's it
   preventing the wrong thing from getting built. (It won't grill you over a
   one-line fix.)
3. **Treat the task brief as a contract.** It reformulates your prompt and asks
   you to *confirm, amend, or reject*. Correct it there — that's the cheapest
   place to fix a misunderstanding.
4. **Declare a Spike for throwaways.** If you just want to try something, say so —
   you'll skip the production ceremony. (The safety floor still holds.)
5. **Let it set up tooling and tiers at first session,** and **restart the harness
   when it tells you to** (newly added sub-agents/config load at startup).
6. **Trust the gates — don't pressure it to skip them.** The demo ("you've seen it
   run"), the security pass, and the independent review exist because "looks done"
   and "is done" differ. In testing, the review caught a real security hole an
   unguided agent shipped. Skipping them is borrowing trouble.
7. **Switching agents or machines?** Paste the resume prompt from `HANDOFF.md`.
   The project is portable across Claude Code, Codex, and OpenCode.
8. **Keep the pack current.** Ask "is the pack up to date?" — it can check the
   upstream version and, if you want, migrate your project to a newer pack without
   touching your project's own code or history.

## Guardrails worth knowing

- **Hard guardrails — never overridable, by anyone.** It will never commit
  secrets/credentials, never run a locally-irreversible destructive operation
  (dropping a database table, deleting cloud resources, purging backups) even if
  asked, and never edits its own policy files except when you explicitly tell it
  to update the pack. Ask it to bypass one and it declines and explains why.
- **Default policies — require your confirmation, but you can override.** Adding a
  dependency or external service, changing auth/access control, schema changes,
  deleting a file, anything that sends data out, changing CI/CD. It asks first;
  you can grant standing permission ("you don't need to ask each time"), which it
  logs.

## Common situations

- **Inherited a messy codebase?** It assesses honestly before changing anything
  and tells you what it found, then asks your goal.
- **It keeps failing the same way?** A circuit breaker stops it after three
  distinct attempts and escalates to you instead of looping.
- **It doesn't know an API/SDK and can't look it up?** It says so and offers a
  research prompt rather than guessing.
- **You just want a review, no changes?** Say "review only / don't change
  anything" — it runs read-only and ends with findings, touching nothing.

## Anti-patterns (don't do these)

- Don't hand-edit the pack's policy files (`AGENTS.md` Part 1, `protocols/`) —
  the agent maintains the project parts for you; edit those only when you mean to
  change the pack itself.
- Don't pressure it to skip the demo, security pass, or review to "go faster."
- Don't treat a Spike as a license to ship — escalate it (or let it auto-escalate)
  the moment it handles real data or accounts.

## FAQ

**Do I need to know how to code?** No. Set Audience Mode to Non-dev and it
explains everything in plain language and handles the technical parts.

**Does it work without Claude Code?** Yes — Claude Code, Codex, and OpenCode are
first-class; any agent that can read files can follow `AGENTS.md` (it's
self-contained markdown).

**What's the cheapest way to run it on a small/local model?** Set Pack profile to
LEAN — it trims the resident footprint and checkpoints more often, without
relaxing any safety rule.

**Where do I look when something's unclear?** `AGENTS.md` is authoritative; its
Authority Matrix says which file wins on any topic. `WALKTHROUGH.md` shows the
flow; this guide explains the why.
