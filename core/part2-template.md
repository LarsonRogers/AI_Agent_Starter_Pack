# Part 2 — Project Specifics (agent-maintained)

Bounded living summary: rewrite to stay current, never append-only. Caps: Pattern
Registry ≤ 40 lines, Architecture ≤ 60. Over a cap, compress — superseded detail moves
to DECISION_LOG.md.

## Project Summary

[PROJECT_NAME] is ...

## Project Options

Set once at first session: infer each default from the brief, confirm all three in one
sentence, **delete the off blocks** — they cost context every session. Log the choices.

- **Demo gate:** [on if the user is non-technical or others will use the app; off for a
  dev running their own tools]
- **Architecture sizing:** [on for greenfield apps; off for scripts, libraries,
  existing structures]
- **Accessibility baseline:** [on if the project has user-facing UI]

### Demo gate (delete this block if off)

A task changing user-visible behavior is done only when the user has SEEN it run —
passing tests are invisible to a non-developer. Maintain `RUNBOOK.md` (start / "you
should see" / stop / if-it-fails) from first runnable state, updated in the same
commit as run steps. Only the user may defer a demo; log the deferral.

### Architecture sizing (delete this block if off)

Sized on day one, one WHY per layer:
S1 single-file tool · S2 UI + logic + storage · S3 client + server · S4 + database.
Growth triggers forcing a LOGGED resize (never silent drift): authentication (≥ S3) ·
shared multi-user data (S4) · a second consumer (extract a service layer) · a file past
~300 lines or a module doing two jobs.

### Accessibility baseline (delete this block if off)

Part of done, not polish: semantic elements (button/a/label, no clickable divs) · alt
text · full keyboard reachability, visible focus · ~4.5:1 text contrast · color never
the only signal.

## Stakes

[Spike = throwaway · Standard = default · Production = shipped, shared, or real data.
The safety floor never scales down; ratchet rules live in guardrails.]

## Tier map (delegation protocol)

- Provider / environment: [NOT SET]
- Capable (session model, never downgraded): [NOT SET]
- Light (bounded rubric checks): [model, or "none — single-tier (YYYY-MM-DD)"]
- Local endpoint (if Light is a local GPU): [URL · model id · auth: <path outside
  repo> · service name · decided YYYY-MM-DD]

## Quick constraints

- Language / runtime: [NOT SET]
- Do not edit: [lockfiles, generated files, `.env*`, `secrets/**`, build output]
- Lint: [cmd] · Format: [cmd] · Typecheck: [cmd] · Test: [cmd] · Build: [cmd]
- Run lint + tests after every change; `python tools/land.py` enforces them at landing.
- Commit per logical change, imperative mood.

## Tech stack

[language / runtime / framework / tooling, with versions]

## File structure

[one line per top-level directory, with its job]

## Pattern Registry (cap: 40 lines)

### [Pattern name]
Purpose · Location (canonical example) · Usage · Anti-pattern [fill per pattern]

## Architecture (cap: 60 lines)

[rung + WHY it fits · structure, one line per layer · data flow · key invariants —
the rules that cause system-level failures if broken]
