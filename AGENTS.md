# AGENTS.md — [PROJECT_NAME]
<!-- Starter Pack v11.0 — 2026-03-09 -->

> **This file is the entry point for ChatGPT Codex and any agent that reads
> `AGENTS.md` automatically.** It contains bootstrapping instructions and a
> condensed reference — but `ARCHITECTURE.md` and `CLAUDE.md` are the
> authoritative sources for all rules and protocols. If this file conflicts
> with either of those, the other file wins. Do not edit policy here.

---

## Step 1 — Read these files before anything else

In this exact order:

Read in this canonical order every session:

1. `ARCHITECTURE.md` — core rules, guardrails, and behavioral protocols
2. `CLAUDE.md` — project-specific stack, style, and task instructions
3. `CAPTAINS_LOG.md` — most recent entry only (if it exists)
4. `PROTOCOLS.md` — triggered sections only, loaded after the log
   (trigger table: Step 2b below; canonical source: ARCHITECTURE.md → Protocol Index)

This order is authoritative. ARCHITECTURE.md and CLAUDE.md load first so
standing rules are active before the log is read and protocols are triggered.

Do not write any code until all four are read and the session start
protocol in `ARCHITECTURE.md` is complete.

---

## Step 2 — Determine your session type

Check whether `CAPTAINS_LOG.md` exists:

**A — Log exists** → Session Resumption Protocol (ARCHITECTURE.md)
**B — No log, new project** → First Session Protocol (ARCHITECTURE.md)
**C — No log, existing codebase** → Inherited Codebase Protocol (PROTOCOLS.md)
**D — Refactor session** → Refactor Protocol (PROTOCOLS.md)

---

## Step 2b — When to load PROTOCOLS.md sections

Do not read PROTOCOLS.md in full every session. Load specific sections
when the situation requires it. The canonical Protocol Index with all
trigger conditions lives in `ARCHITECTURE.md` → Protocol Index.

Quick reference:

| Situation | Load this section |
|-----------|------------------|
| No log, existing codebase | Inherited Codebase Protocol |
| First session on any project | Placeholder Inference Protocol |
| Explicit refactor task | Refactor Protocol |
| 5+ tasks in session or context degradation | Context Window Management |
| Binary / large files encountered | Binary & Large File Handling |
| Sensitive data found or suspected | Sensitive Data Handling |
| 3 failed attempts on same problem | Stuck Loop Circuit Breaker |
| Lint / test commands missing | Validation Tooling Fallback |
| External SDK / API / platform work | External Research Protocol |
| Web access unavailable, training data unverifiable | Knowledge Gap Protocol |
| Change touches 3+ files or layers | Cross-Cutting Changes |
| Writing or evaluating tests | Testing Strategy |
| Review / audit / analysis only (no edits) | Read-Only / Meta-Review Protocol |
| Surfacing a conflict or verifying conflict behavior | Conflict Resolution Examples |
| Pack files missing, git unavailable, placeholder conflicts | Edge-Case Handling |
| Auditing the pack for issues | Known Limitations & Deferred Decisions |

---

## Step 3 — Apply core principles

A condensed reference — full protocols are in `ARCHITECTURE.md`:

- Hard guardrails are non-overridable. Default policies require confirmation
  but can be unlocked by explicit user instruction.
- Detect audience mode from Captain's Log. If absent, ask two questions.
  Default to Technical non-dev.
- Reformulate every prompt into a task brief. Confirm before starting.
- Never resolve instruction conflicts silently — surface and apply hierarchy.
- Pre-flight plan required for any change touching 3+ files or layers.
- Honest verification language on all codebase claims.
- Three-strike circuit breaker on repeated failures.
- Scan for sensitive data on inherited repos. Flag on encounter always.
- Checkpoint after 5 tasks. Append handoff prompt to Captain's Log entry.
- Record pack version in every Captain's Log entry.
- Never guess on unknown external systems — Knowledge Gap Protocol.
- Validation tooling missing? Report, propose, never skip silently.
- Never edit starter pack files (ARCHITECTURE.md, PROTOCOLS.md, AGENTS.md,
  TASK_TEMPLATE.md) unless explicitly instructed to update the pack.
  Exception — CLAUDE.md: designated placeholder sections (project name, tech
  stack, validation commands, file structure) may be written during the
  Placeholder Inference Protocol. Policy sections of CLAUDE.md are never
  edited without explicit instruction.
- Never read, edit, or commit binary files without explicit awareness.
  Never commit files over 1MB without confirmation. Verify .gitignore on first session.
- No hardcoded environment-specific values — URLs, ports, endpoints go in config.
  No dev/debug flags in committed code.
- Tests must verify behavior not implementation. Cover failure modes, not just
  happy paths. If no tests exist, flag before any refactor.

---

## Quick Constraints
<!-- Fill in the hardest project-specific constraints from CLAUDE.md.
     These are filled in by the agent during the Placeholder Inference Protocol.
     Do not edit manually. -->

- **[Language/runtime]** —
- **[Files not to edit]** —
- **[Lint command]** —
- **[Test command]** —

---

## Project Summary
<!-- Filled in by the agent. Do not edit manually. -->

[PROJECT_NAME] is ...
