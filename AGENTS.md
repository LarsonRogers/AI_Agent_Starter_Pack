# AGENTS.md — [PROJECT_NAME]

> **This file exists for ChatGPT Codex compatibility.** Codex reads `AGENTS.md`
> automatically, just as Claude Code reads `CLAUDE.md`.
>
> All project instructions live in `CLAUDE.md` — that is the canonical source of
> truth. This file summarizes the essentials and tells you where to look.

## Session Start (Run This First, Every Time)

Before anything else — before reading instructions, before asking questions,
before writing any code, determine which of these three situations applies:

**A — Resuming an active project (Captain's Log exists)**
Read `CAPTAINS_LOG.md`. Report to the developer: where the last session ended,
current codebase state, open watch items, and proposed next step. Wait for
confirmation before proceeding.

**B — First session on a new project (no log, no prior code)**
Read `ARCHITECTURE.md` and `CLAUDE.md`. Scan the repo. Report findings.
Create `CAPTAINS_LOG.md` with an initial entry. Confirm the first task
before writing any code.

**C — Inherited codebase (existing code, no log, starter pack just dropped in)**
This requires a full assessment before any code is written. Read and map the
entire repo, reconstruct a Captain's Log from git history (marked as
reconstructed), assess the architecture, surface problem areas, fill in the
project-specific sections of `ARCHITECTURE.md` and `CLAUDE.md`, then prepend
a live assessment entry to the log. See `ARCHITECTURE.md` → Session Protocols
→ Inherited Codebase for the full four-phase protocol.

Do not skip or abbreviate the assessment phase. The developer needs an honest
picture of what they have before deciding what to do with it.

---

The Captain's Log is the universal handoff artifact — written for humans and
for any coding agent on any platform. It is what makes it possible to switch
between Claude, Codex, Cursor, or any other agent without losing context.

---

## Before Writing Any Code

Read these files in order:

1. **`ARCHITECTURE.md`** — Structural rules, pre-edit protocol, and pattern registry.
   Read this first. These rules override everything else.
2. **`CLAUDE.md`** — Architecture, constraints, file structure, code style, workflow.
   This is the instruction manual for the entire project.
3. Any supplementary docs listed in the Related Docs table in `CLAUDE.md`.

## Quick Constraints

<!-- Copy the hardest constraints from CLAUDE.md here — the rules that would cause
     immediate breakage if violated. Keep it short. 5-8 bullets max. -->

- **[Language constraint]** — e.g., ES5 only, Python 3.10+, TypeScript strict
- **[Runtime constraint]** — e.g., no browser APIs in Node, no Node APIs in Max JS
- **[Formatting]** — e.g., run `npm run lint` after every change
- **[Testing]** — e.g., run `pytest` after every change, all tests must pass
- **[Files not to edit]** — e.g., never edit .amxd, package-lock.json, .env
- **[Session start]** — read `CAPTAINS_LOG.md` first to orient before touching anything
- **[Git]** — commit after each completed task, imperative mood messages
- **[Logs]** — update `CAPTAINS_LOG.md` (prepend) and `CHANGELOG.md` (append) after every commit
- **[Research]** — before writing code involving any external SDK, API, or platform,
  research current docs and source repos first. Do not rely on training data alone.
  Document findings in the Captain's Log. If web access is unavailable, ask for docs.
- **[Comments]** — every file gets a header, every function gets a docstring/JSDoc,
  every non-obvious decision gets a WHY comment. No magic values. No cryptic names.
- **[Handoff]** — a human dev must be able to orient in this codebase in under 30 min

## Project Summary

<!-- 3-4 sentences max. What it is, what it does, what the current task is. -->

[PROJECT_NAME] is ...

The current task is: [refactoring / feature work / bug fixes / ...]
