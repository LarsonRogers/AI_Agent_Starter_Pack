# AGENTS.md — [PROJECT_NAME]
<!-- Starter Pack v11.45 — 2026-03-09 -->

> **This file is the entry point for ChatGPT Codex and any agent that reads
> `AGENTS.md` automatically.** It contains bootstrapping instructions and a
> condensed reference — but `ARCHITECTURE.md` and `CLAUDE.md` are the
> authoritative sources for all rules and protocols. If conflicts arise,
> ARCHITECTURE.md governs. Do not edit policy here.

---

## Step 1 — Read these files before anything else

> **Before starting Step 1:** check the meta-review exception in Step 2.
> If the first message is a review/audit request, load `protocols/read-only.md`
> immediately instead of running this read order.

Read in this canonical order every session:

1. `ARCHITECTURE.md` — core rules, guardrails, and behavioral protocols
2. `CLAUDE.md` — project-specific stack, style, and task instructions
3. `CAPTAINS_LOG.md` — most recent entry only (if it exists)
4. `protocols/[triggered-file].md` — one file per triggered situation
   (trigger table: Step 2b below; canonical source: ARCHITECTURE.md → Protocol Index)

This order is authoritative. ARCHITECTURE.md and CLAUDE.md load first so
standing rules are active before the log is read and protocols are triggered.

Do not write any code until all four are read and the session start
protocol in `ARCHITECTURE.md` is complete.

---

## Step 2 — Determine your session type

**Meta-review exception — check this first:**
If the user's first message is clearly a review, audit, or analysis request
("review", "audit", "assess", "analyze", "explain", "summarize",
"what does this do", "what's wrong", "check this", "look at this",
"read-only", "no changes", "don't touch anything"), skip session-start
behaviors and load `protocols/read-only.md` immediately. Do not run audience
detection, placeholder inference, or the inherited codebase report. If work
is needed after the review, resume normal session-start at that point.
If the first message is evaluative in tone but does not match any keyword
above, ask one question before proceeding: "It looks like you may want a
review — should I analyze only, or also make changes?" Then route accordingly.
Does NOT trigger when: the same message explicitly requests edits or
implementation alongside the review (e.g., "audit this, then fix it") —
in that case run normal session-start and treat the review as the first task.

Otherwise, check whether `CAPTAINS_LOG.md` exists:

**A — Log exists** → Session Resumption Protocol (ARCHITECTURE.md)
**B — No log, new project** → First Session Protocol (ARCHITECTURE.md)
**C — No log, existing codebase** → load `protocols/inherited-codebase.md`
**D — Refactor session** (only when: no log OR resuming, AND user states explicit structural goal with no new features) → load `protocols/refactor.md`
  Note: when no log exists AND the codebase is inherited AND the goal is explicitly
  structural-only, D takes precedence over C. When intent is ambiguous, default to C.

---

## Step 2b — When to load protocol files

Do not speculatively load protocol files. Load only the file
when the situation requires it. The canonical Protocol Index with all
trigger conditions lives in `ARCHITECTURE.md` → Protocol Index.

Quick reference:

| Situation | Load this file |
|-----------|---------------|
| No log, existing codebase | `protocols/inherited-codebase.md` |
| First session on any project (except active read-only/meta-review) | `protocols/placeholder-inference.md` |
| Explicit refactor task | `protocols/refactor.md` |
| 5+ tasks in session or context degradation | `protocols/context-window.md` |
| Binary or large files (>1MB) encountered or being committed (size threshold applies at commit-time) | `protocols/binary-files.md` |
| Inherited repos (proactive scan) or on encounter | `protocols/sensitive-data.md` |
| 3 failed attempts on same problem | `protocols/stuck-loop.md` |
| Lint, test, or CI commands missing or unconfigured | `protocols/validation-fallback.md` |
| External SDK / API / platform work | `protocols/external-research.md` |
| Web access unavailable, training data unverifiable | `protocols/external-research.md` |
| Task touches 3+ files, crosses architectural layers, or involves rename/move/structural reorganization | `protocols/cross-cutting.md` |
| Writing or evaluating tests | `protocols/testing-strategy.md` |
| Review / audit / analysis only (no edits) | `protocols/read-only.md` |
| Surfacing a conflict or verifying conflict behavior | `protocols/conflict-examples.md` |
| Pack files missing, git unavailable, no file-read, no file-write, placeholder conflicts, CAPTAINS_LOG missing/corrupt | `protocols/edge-cases.md` |
| Auditing the pack for issues *(audit-only — skip during active coding)* | `protocols/known-limitations.md` |
| Same structural approach appears in 2+ touched files, or a new reusable pattern before committing, or a new approach replaced one that was causing bugs/confusion | `protocols/pattern-registry.md` |

---

## Step 3 — Apply core principles

A condensed reference — full protocols are in `ARCHITECTURE.md`:

- Hard guardrails are non-overridable. Default policies require confirmation
  but can be unlocked by explicit user instruction.
- Detect audience mode from Captain's Log. If absent, ask two questions.
  Default to Technical non-dev.
- Reformulate every coding prompt into a task brief. Confirm before starting.
  (Read-only sessions are exempt — the review request is the scope contract.)
- Never resolve instruction conflicts silently — surface and apply hierarchy.
- Pre-flight plan required for any change touching 3+ files or layers.
- Honest verification language on all codebase claims.
- Three-strike circuit breaker on repeated failures.
- Scan for sensitive data on inherited repos. Flag on encounter always.
- Checkpoint after 5 tasks. Append handoff prompt to Captain's Log entry.
- Record pack version in every Captain's Log entry.
- Never guess on unknown external systems — Knowledge Gap Protocol.
- Validation tooling missing? Report, propose, never skip silently.
- Never edit starter pack files (ARCHITECTURE.md, CLAUDE.md, PROTOCOLS.md,
  AGENTS.md, TASK_TEMPLATE.md, and all files in protocols/) unless explicitly
  instructed to update the pack.
  Exception — CLAUDE.md: designated placeholder sections (project name, tech
  stack, validation commands, file structure) may be written during the
  Placeholder Inference Protocol. Policy sections of CLAUDE.md are never
  edited without explicit instruction.
  Exception — AGENTS.md: the Quick Constraints and Project Summary placeholder
  sections (marked "Filled in by the agent") may be written during the
  Placeholder Inference Protocol. Policy and protocol sections of AGENTS.md
  are not editable without explicit instruction.
  Exception — ARCHITECTURE.md: the Project-Specific Architecture and Pattern
  Registry sections may be written during the Inherited Codebase Protocol
  (Phase 3), AND Pattern Registry entries may be added whenever
  protocols/pattern-registry.md is triggered. Core policy sections of
  ARCHITECTURE.md are never editable without explicit instruction to
  update the pack itself.
  Canonical rule source: ARCHITECTURE.md → Hard guardrails.
- Never attempt to text-read or edit files with known binary extensions —
  see `protocols/binary-files.md` for extension rules and examples.
  Never commit files over 1MB without confirmation. Verify .gitignore on first session.
- No hardcoded environment-specific values — URLs, ports, endpoints go in config.
  No dev/debug flags in committed code.
- Tests must verify behavior not implementation. Cover failure modes, not just
  happy paths. If no tests exist, flag before any refactor.

---

## Quick Constraints
<!-- Placeholder section — filled in by the agent during Placeholder Inference.
     Exempt from the pack-file edit guardrail per ARCHITECTURE.md exception.
     Do not edit manually outside of the Placeholder Inference Protocol.
     Runtime skip: if these placeholders are already filled, read and apply
     the values — do not re-run Placeholder Inference. -->

- **[Language/runtime]** —
- **[Files not to edit]** —
- **[Lint command]** —
- **[Test command]** —

---

## Project Summary
<!-- Filled in by the agent. Do not edit manually. -->

[PROJECT_NAME] is ...
