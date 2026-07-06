# Part 2 — Project Specifics (agent-maintained)

Bounded living summary: rewrite sections to stay current, never append-only. Caps:
Pattern Registry ≤ 40 lines, Architecture ≤ 60, everything else at template size. Over
a cap, compress — superseded detail moves to DECISION_LOG.md.

## Project Summary

[PROJECT_NAME] is ...

## Project Options

Set once, at the first session: infer each default from the brief, confirm all three in
one sentence, then **delete the blocks that are off** — they cost context every
session. Record the choices in the first log entry.

- **Demo gate:** [on if the user is non-technical or others will use the app; off for a
  developer running their own tools]
- **Architecture sizing:** [on for greenfield apps; off for scripts, libraries, or an
  existing structure]
- **Accessibility baseline:** [on if the project has user-facing UI]

### Demo gate (delete this block if off)

A task changing user-visible behavior is done only when the user has SEEN it run —
passing tests are invisible to a non-developer. Maintain `RUNBOOK.md` (start steps /
"you should see" / stop / if-it-fails) from the first runnable state, updated in the
same commit as any run-step change. Only the user may defer a demo; log the deferral.

### Architecture sizing (delete this block if off)

Sized on day one, written down, one WHY per layer:
S1 single-file tool · S2 UI + logic + storage · S3 client + server · S4 + database.
Growth triggers forcing a LOGGED resize (never silent drift): authentication (≥ S3) ·
shared multi-user data (S4) · a second consumer (extract a service layer) · a file past
~300 lines or a module doing two jobs.

### Accessibility baseline (delete this block if off)

For user-facing UI, part of done — not polish: semantic elements (button/a/label — no
clickable divs) · alt text on images · full keyboard reachability with visible focus ·
~4.5:1 body-text contrast · color never the only signal for state.

## Stakes

[Spike = throwaway · Standard = default · Production = shipped, shared, or real data.
The safety floor never scales down; ratchet rules live in guardrails.]

## Tier map (used by the delegation protocol)

- Provider / environment: [NOT SET]
- Capable (session model, never downgraded): [NOT SET]
- Light (bounded rubric checks): [model, or "none — single-tier (YYYY-MM-DD)"]

## Quick constraints

- Language / runtime: [NOT SET]
- Do not edit: [lockfiles, generated files, `.env*`, `secrets/**`, build output]
- Lint: [cmd] · Format: [cmd] · Typecheck: [cmd] · Test: [cmd] · Build: [cmd]
- Run lint + tests after every change; `tools/land.sh` enforces them at landing.
- Commit per logical change, imperative mood.

## Tech stack

[language / runtime / framework / test + lint tooling, with versions]

## File structure

[actual layout — one line per top-level directory, with its job]

## Pattern Registry (cap: 40 lines)

### [Pattern name]
Purpose: [one sentence] · Location: [canonical example file] ·
Usage: [how to apply] · Anti-pattern: [what NOT to do]

## Architecture (cap: 60 lines)

[rung + WHY it fits · structure, one line per layer · data flow · key invariants —
the rules that cause system-level failures if broken]
