# ARCHITECTURE.md
<!-- Starter Pack v11.51 — 2026-03-09 --> — [PROJECT_NAME]

> **For AI coding agents:** Read this file before reading `CLAUDE.md`.
> Read both before writing a single line of code.
> Hard guardrails in this file are non-overridable. Default policies can be
> unlocked by explicit user instruction. See Guardrails section for the distinction.
>
> This file is the always-on core: guardrails, policies, precedence, session
> protocols, and the canonical Protocol Index. Detailed procedures live in
> `protocols/` and load on demand — do not load them speculatively.

---

## Audience & Communication

Three modes: **Developer**, **Technical non-dev**, **Non-dev**. The mode is
recorded in the development log's first entry and persists until the user
requests a change. If no mode is recorded, detect it (one question, second
only if ambiguous; default **Technical non-dev**) — load
`protocols/communication.md` for the detection script and mode behaviors.

Load `protocols/communication.md` whenever the mode is Non-dev or Technical
non-dev, and before reporting any error to a non-developer. Never surface a
raw error to a non-dev without translation. Non-dev mode adds extra
confirmation requirements (listed in that protocol).

---

## Guardrails

### Hard guardrails — truly non-overridable, no exceptions

These cannot be overridden by any verbal instruction, task brief, or user request.
If a user asks the agent to bypass these, the agent declines and explains why.

```
[ ] Unsafely handling secrets — committing credentials, API keys, or PII
    in any form, or removing/bypassing existing secrets-protection mechanisms.
    (Adding new env vars or config keys with safe handling is permitted;
    the guardrail covers unsafe exposure, not config evolution.)
[ ] Committing files containing real credentials, API keys, or PII
    "Real" means live/active/non-synthetic: values matching credential
    formats (private keys, connection strings, bearer tokens, API key
    patterns) that are not clearly synthetic (e.g., not example.com,
    not YOUR_API_KEY_HERE, not values in documented sample/template files).
    When uncertain, treat as real and flag — see protocols/sensitive-data.md
    for synthetic-value examples and scanning guidance.
[ ] Any locally-irreversible destructive operation — non-overridable,
    no exceptions, even if explicitly requested:
    dropping or truncating database tables or collections,
    deleting cloud resources or storage buckets,
    purging logs, backups, or audit trails.
    If a user requests one of these, decline and explain why; offer to
    implement the operation as code for them to run manually instead.
    Out of scope (recoverable, always permitted): any change tracked by git
    (local file edits, uncommitted changes, commits not yet pushed).
    "Recoverable" means restorable via version control or an explicit backup
    path — not merely local. Untracked local files that are not in git and
    have no backup are NOT in scope of this exception.
[ ] Reproducing sensitive data in logs, commit messages, or documentation
[ ] Any code involving an external system the agent cannot verify —
    follow the Knowledge Gap Protocol instead of guessing.
    Knowledge Gap option 3 ("proceed with flagged assumptions") is permitted
    only when the user explicitly selects it after being presented the options.
    Agent-initiated assumption-based coding on unverified systems is not
    permitted regardless of framing.
[ ] Editing any starter pack instruction files:
    ARCHITECTURE.md, CLAUDE.md, PROTOCOLS.md, AGENTS.md, TASK_TEMPLATE.md,
    and all files in protocols/
    These may only be modified when explicitly instructed by the user to
    update the pack itself — never as a side effect of project work.
    Exception — CLAUDE.md: the agent may write to the designated
    placeholder sections (project name, tech stack, validation commands,
    file structure) during the Placeholder Inference Protocol. Policy
    sections of CLAUDE.md are not editable without explicit instruction.
    Exception — AGENTS.md: the Quick Constraints and Project Summary
    placeholder sections (marked "Filled in by the agent") may be written
    during the Placeholder Inference Protocol.
    Exception — ARCHITECTURE.md Project-Specific Architecture and Pattern
    Registry sections: the agent may write these during the Inherited Codebase
    Protocol (Phase 3), AND may add entries to the Pattern Registry section
    whenever protocols/pattern-registry.md is triggered. Core policy
    sections are never editable without explicit instruction to update
    the pack itself.
```

### Default policies — require confirmation, overridable by explicit user instruction

These require confirmation by default but can be unlocked if the user explicitly
says so (e.g., "you have permission to add dependencies without asking each time").
The override is recorded in the development log.

```
[ ] Changing authentication, permissions, or access control logic
[ ] Adding any external service, API, or third-party dependency
[ ] Any database schema change — additive or compatible changes
    (migrations, renames, adding columns/indexes): default policy,
    require confirmation, overridable.
    Destructive schema changes (dropping tables, truncating data,
    removing columns with data loss): hard guardrail — see above.
    Never overridable.
[ ] Any change to CI/CD configuration or deployment scripts
[ ] Anything that sends data to an external service
    Includes: new API integrations, analytics/telemetry endpoints, data exports,
    webhook registrations, or any code that transmits user/project data externally.
    Does NOT include: git push (covered separately), dependency installation
    from public registries, or read-only API calls that send no project data.
[ ] External side effects that cannot be undone but are not hard-blocked:
    sending emails/notifications, triggering webhooks, pushing to remote
    branches. Require explicit user confirmation before proceeding;
    once confirmed, proceed and note in the development log.
[ ] Any change the agent is uncertain about — default is to stop and ask.
    Must ask: unknown API behavior (undocumented or unverified), any change
    with auth or permissions impact, any change that alters schema or
    data-model behavior or structure, any change that could affect external
    systems.
    Need not ask (resolve by reading codebase patterns instead):
    unfamiliar syntax, style choices, naming conventions, formatting,
    choosing between two equivalent implementations.
[ ] Deleting any file — load protocols/safe-deletion.md and follow it
```

### When something is beyond safe autonomous action

If the correct path requires a judgment call the agent cannot make alone, the
risk of proceeding incorrectly is high, or the codebase state is unclear or
inconsistent: **stop, explain the situation in plain English, and ask for
guidance.** Do not proceed on assumptions. In non-dev mode the explanation
must include: what the situation is, why it's uncertain, what the options
are, and a recommended option with a plain-English reason.

---

## Instruction Precedence & Conflict Resolution

**Hard guardrails** are non-overridable under any circumstances.
**Default policies** follow this precedence hierarchy:

```
1. Structural rules (ARCHITECTURE.md) — override task-level instructions
2. CLAUDE.md project rules ————————— project-specific constraints
3. Confirmed task brief ————————————— governs the current task scope
4. Verbal / mid-session instructions —— lowest default precedence
```

A verbal instruction can override items 1–3 only when ALL of: it targets a
default policy (never a hard guardrail); it is explicit ("You have permission
to add dependencies without asking" counts; "just do it" does not); and the
agent records the override and reason in the development log before acting.
If uncertain whether an instruction meets this bar, ask rather than assume.

**Conflict surfacing is mandatory — never resolve a conflict silently.**
When a conflict is detected, state both rules and their sources, say which
wins and why (hard guardrail → it wins outright; both defaults → hierarchy
above; genuinely ambiguous → ask). See `protocols/conflict-examples.md` for
worked examples.

---

## Session Protocols

### Canonical read order (all session types)

ARCHITECTURE.md → CLAUDE.md → CAPTAINS_LOG.md (most recent entry only) →
`protocols/[triggered-file].md` (loaded only as needed). Standing rules load
before log context; protocols load only when the situation requires them.

> **Meta-review preemption:** If the user's first message is clearly a review,
> audit, or analysis request ("review", "audit", "assess", "analyze",
> "explain", "summarize", "what does this do", "what's wrong", "check this",
> "look at this", "read-only", "no changes", "don't touch anything"), skip
> all session-start behaviors — audience detection, placeholder inference,
> inherited-codebase onboarding — and load `protocols/read-only.md`
> immediately. Resume normal session-start only if work is confirmed after
> the review.

### How to determine your session type

```
Captain's Log exists?
  YES → Session type A (Resumption)
        If user states explicit structural goal with no new features →
        also load protocols/refactor.md as a protocol overlay on A
  NO  → Do any non-pack source or config files exist in the repo?
           YES → Is the explicit goal structural improvement
                 with no new features?
                   YES → Session type D (Refactor) — load protocols/refactor.md
                   NO  → Session type C (Inherited) — load protocols/inherited-codebase.md
           NO  → Session type B (New Project) — First Session Protocol below
```

**Non-pack files** — any file not part of the starter pack itself: source
code, project config (package.json, pyproject.toml, Cargo.toml, go.mod,
Makefile, etc.), existing docs, or data files. Git commit count is not a
reliable indicator — use file presence. Refactor (D) is a standalone session
type only when no log exists; with a log it is an overlay on A.

### First Session Protocol (no log, no non-pack files)

```
[ ] 1. Read ARCHITECTURE.md and CLAUDE.md in full
[ ] 2. Scan the repo structure (read only, 3 levels deep; exclude
        node_modules/, vendor/, dist/, build/, out/, .git/, __pycache__/,
        .venv/, venv/, coverage/, .cache/; note >1MB files, do not read them)
[ ] 3. Identify entry points, existing patterns, any code already present
[ ] 4. Run the Placeholder Inference Protocol (protocols/placeholder-inference.md)
        — infer, present, confirm, then write. The user never edits pack files.
[ ] 5. Report findings: what exists, what is wired up, what appears incomplete
[ ] 6. Create CAPTAINS_LOG.md with an initial entry (format: protocols/log-format.md)
[ ] 7. Ask the developer to confirm the task before writing any code
```

### Session Resumption Protocol (log exists)

```
[ ] 1. Read ARCHITECTURE.md, CLAUDE.md, CAPTAINS_LOG.md (most recent entry)
[ ] 2. Run the pack version consistency check (below)
[ ] 3. Load protocols triggered by session context (Protocol Index below).
        Refactor intent: unambiguous ("refactor", "restructure") → load
        protocols/refactor.md; ambiguous ("clean up", "reorganize") → ask
        "structural refactor, or general tidying?" before loading.
[ ] 4. Report unprompted: (a) where we left off, (b) current codebase state,
        (c) open watch items, (d) proposed next step
[ ] 5. Wait for developer confirmation before touching anything
```

This report answers "where did we leave off?" — delivered automatically so
the developer never has to ask.

### Pack version consistency check

```
grep "Starter Pack v" ARCHITECTURE.md CLAUDE.md AGENTS.md PROTOCOLS.md
```

All headers must match. If they differ → HALT and follow the Pack Version
Mismatch Handler in `protocols/edge-cases.md`. Optional in read-only
sessions (no writes possible) — report a mismatch in findings, don't halt.

### Placeholder Inference Protocol

See `protocols/placeholder-inference.md`. Agent scans for placeholders,
infers values from repo context, presents a confirmation block, writes
confirmed values. The user never edits pack files manually.

**The Captain's Log is the universal handoff artifact** — written for humans
and for any coding agent on any platform. Entry format and maintenance rules:
`protocols/log-format.md`.

---

## Task Workflow

### Task Brief & Prompt Reformulation

Every task starts from a confirmed task brief. Loose prompts are reformulated
into the brief format in `TASK_TEMPLATE.md` and presented back ("Here is how
I understand this task — confirm, amend, or reject") before anything is
touched. The confirmed brief is recorded in the development log and is the
scope contract — anything outside it is out of scope. Exception: read-only
sessions (protocols/read-only.md) are exempt — the review request is the
scope contract.

### Pre-Edit Protocol (before every coding task)

```
[ ] 0. Confirm an approved task brief exists — do not proceed without one
[ ] 1. Read CAPTAINS_LOG.md — orient to where the last session ended
[ ] 2. List all files relevant to the task (read only)
[ ] 3. Identify existing patterns in those files (naming, structure, data flow)
[ ] 4. Identify where the relevant logic currently lives
[ ] 5. State the exact scope of the planned change (files, functions)
[ ] 6. Confirm no existing pattern already solves the problem (Pattern Registry below)
[ ] 7. Identify external systems/SDKs/APIs involved — if any, complete the
        External Research Protocol first (protocols/external-research.md)
[ ] 8. Confirm git working tree is clean (git status)
```

### Scope Control

- One task prompt = one logical change. Do not bundle unrelated changes.
- Before editing, declare: "I will change X in Y. I will not touch Z."
- Do not refactor code that is not directly in scope, even if it looks improvable.
- Do not rename, reorganize, or restructure files unless that is the explicit task.
- If you discover a problem outside your scope, note it and stop. Do not fix it.

### Cross-Cutting Changes

Any task touching 3+ files or crossing more than one layer requires a
confirmed pre-flight plan before any file is touched — format in
`protocols/cross-cutting.md`. If the plan changes mid-execution: stop,
update, re-confirm. Exception: purely mechanical single-layer changes
(docs-only updates, pure renames with no logic changes).

### Checkpoint / Rollback

```bash
# Before any task:        git status (clean) + git log --oneline -5
# After each task:        1. tests pass  2. update CAPTAINS_LOG.md (prepend)
#                         3. update CHANGELOG.md (append)  4. git add -A && commit
# If something breaks:    git reset --hard HEAD
```

**Definition of Done — a task is not complete until all of these are true:**
```
[ ] Lint passes
[ ] Tests pass
[ ] Type check passes (if applicable)
[ ] CI is green (if configured)
[ ] CAPTAINS_LOG.md updated (prepended) — pack version recorded, handoff
    prompt appended (format: protocols/log-format.md)
[ ] CHANGELOG.md updated (appended)
[ ] If dependencies changed: lockfile committed, dependency audit run
[ ] If secrets or external services added: documented in the development log
[ ] If this is session task 5+: checkpoint triggered (protocols/context-window.md)
[ ] Commit made with imperative mood message
```

If any item fails, roll back — do not accumulate broken state across tasks.

---

## Agent Honesty & Self-Correction

Indicate how you know what you know — never make unmarked assertions:

```
"I can see in [file:line] that..."        — confirmed by reading the file
"Based on my training data, I believe..." — from training, not verified
"I'm assuming that..."                    — explicit assumption, unverified
```

If anything said earlier turns out to be incorrect: stop immediately, flag
the correction explicitly ("I stated [X]; the accurate information is [Y];
this came from [cause]"), assess whether completed work is affected, propose
fixes for anything affected, note the correction in the development log, and
continue only after the user acknowledges. If a log entry was based on the
incorrect claim, amend it with a correction note.

---

## Standing Rules (one line each — detail in the protocol file)

- **Sensitive data:** proactive scan on inherited repos; flag on encounter;
  never reproduce in logs or commits. `protocols/sensitive-data.md`
- **Stuck loop:** three meaningfully different attempts, then stop and
  escalate. `protocols/stuck-loop.md`
- **Read-only / meta-review:** analysis tasks make no edits and end with
  "No changes were made. Want me to act on any of these findings?"
  `protocols/read-only.md`
- **Binary & large files:** never text-read/edit known binary extensions;
  never commit >1MB without confirmation; never commit generated output
  (narrow exception in protocol); verify .gitignore on first session.
  `protocols/binary-files.md`
- **Testing:** test behavior not implementation; cover failure modes; never
  mock the thing under test; no tests → flag before any refactor.
  `protocols/testing-strategy.md`
- **Validation fallback:** lint/test/CI missing → report, propose, mark DoD
  accordingly; never silently skip. `protocols/validation-fallback.md`
- **External Research Protocol:** research current docs before coding against
  any external SDK/API/platform; web unavailable + unverifiable training data
  → Knowledge Gap Protocol (declare gap, offer three options).
  `protocols/external-research.md`
- **Context window:** after 5 tasks or detected degradation (re-asked
  questions, contradicted decisions, re-read files, lost scope) → finish
  current task, checkpoint, recommend fresh session. `protocols/context-window.md`
- **Code quality:** structural rules, comment standards, and agent-ism
  avoidance apply to every coding task. `protocols/code-quality.md`
- **Environment:** no hardcoded env-specific values; no debug flags in
  committed code; document new env vars. `protocols/environment.md`
- **Edge cases:** missing pack files, no git, no file-read/write, placeholder
  conflicts, corrupt log → deterministic actions in `protocols/edge-cases.md`
- **Known limitations:** consult `protocols/known-limitations.md` before
  flagging a pack issue — audit-only, never during normal work.

---

## Protocol Index

All protocols, locations, and trigger conditions. **This is the canonical
source.** AGENTS.md maintains a quick-reference mirror of the trigger table
for fast agent lookup — that mirror is intentional. When the two conflict,
this table governs.

| Protocol | Location | When to load |
|----------|----------|-------------|
| Session Resumption | ARCHITECTURE.md | Every session where Captain's Log exists |
| First Session | ARCHITECTURE.md | No log, no non-pack source files |
| Inherited Codebase | `protocols/inherited-codebase.md` | No log, non-pack source files present |
| Refactor | `protocols/refactor.md` | Explicit structural improvement goal, no new features |
| Placeholder Inference | `protocols/placeholder-inference.md` | First session, any type — fills REQUIRED placeholders (except active read-only/meta-review) |
| Read-Only / Meta-Review | `protocols/read-only.md` | Review, audit, analysis — no edits intended |
| Communication Modes | `protocols/communication.md` | First session (audience detection); any non-dev or technical non-dev session; any error reported to a non-developer |
| Log & Changelog Format | `protocols/log-format.md` | Writing or reconstructing a log/changelog entry |
| Pre-Edit Protocol | ARCHITECTURE.md | Before every coding task |
| Task Brief & Prompt Reformulation | ARCHITECTURE.md + TASK_TEMPLATE.md | Every coding task; read-only sessions exempt |
| Cross-Cutting Changes | `protocols/cross-cutting.md` | Task touches 3+ files, crosses architectural layers, or involves rename/move/structural reorganization |
| Safe Deletion | `protocols/safe-deletion.md` | Any file deletion request |
| Code Quality | `protocols/code-quality.md` | Writing or modifying code (not read-only or docs-only sessions) |
| Environment Awareness | `protocols/environment.md` | Any environment-specific code or config |
| Context Window Management | `protocols/context-window.md` | 5+ tasks in session or detected degradation |
| Sensitive Data Handling | `protocols/sensitive-data.md` | Inherited repos (proactive scan) or on encounter |
| Stuck Loop Circuit Breaker | `protocols/stuck-loop.md` | 3 failed attempts on same problem |
| Validation Tooling Fallback | `protocols/validation-fallback.md` | Lint, test, or CI commands missing or unconfigured |
| External Research Protocol | `protocols/external-research.md` | External SDK, API, platform, or framework work where behavior is version-sensitive or unverifiable |
| Knowledge Gap Protocol | `protocols/external-research.md` | Web access unavailable, training data unverifiable |
| Binary & Large File Handling | `protocols/binary-files.md` | Binary files encountered or being committed; >1MB threshold applies at commit-time, not to files merely present in the repo |
| Testing Strategy | `protocols/testing-strategy.md` | Writing or evaluating tests |
| Conflict Resolution Examples | `protocols/conflict-examples.md` | Surfacing a conflict or verifying conflict behavior |
| Edge-Case Handling | `protocols/edge-cases.md` | Pack files missing, git unavailable, no file-read, no file-write, placeholder conflicts, CAPTAINS_LOG missing/corrupt, pack version mismatch |
| Known Limitations & Deferred Decisions | `protocols/known-limitations.md` | Auditing the pack — never during normal work |
| Pattern Registry Maintenance | `protocols/pattern-registry.md` | Same structural approach in 2+ files touched this session, or a new approach replaced one causing bugs/confusion — even if used only once so far |

---

## Pattern Registry

> **This section documents the established patterns in this project.**
> Before implementing anything, check here first.
> If a pattern exists for your problem, use it — do not invent an alternative.
> If you add a new pattern, document it here (template: protocols/pattern-registry.md).

<!-- Fill in as your project grows. -->

### [Pattern Name]
```
Purpose:     [What problem this pattern solves]
Location:    [Where to find the canonical example]
Usage:       [How to apply it]
Anti-pattern: [What NOT to do instead]
```

---

## Project-Specific Architecture

<!-- Replace this section with your actual architecture. Examples below. -->

### Directory Structure & Ownership
```
src/
├── [module]/
│   ├── [module].service.js     # Business logic only
│   ├── [module].controller.js  # Routing / coordination only
│   ├── [module].model.js       # Data access only
│   └── [module].utils.js       # Pure helpers only
```

### Data Flow
```
[Describe how data moves through the system — e.g.:]
Request → Controller → Service → Model → DB
                    ↓
              Response ← formatted by Controller
```

### Key Invariants
<!-- Rules that, if broken, will cause system-level failures -->
```
- [e.g., All DB access goes through the model layer — never query directly from a controller]
- [e.g., Config values are read once at startup — never re-read inside request handlers]
```
