# ARCHITECTURE.md — [PROJECT_NAME]

> **For AI coding agents:** Read this file before reading `CLAUDE.md`.
> Read both before writing a single line of code.
> These rules are not negotiable and are not overridden by task prompts.

---

## Universal Structural Rules

These apply to every file, every function, every change — regardless of language or framework.

### Separation of Concerns

```
Layer           Responsibility                          What does NOT belong here
─────────────────────────────────────────────────────────────────────────────────
I/O / UI        Receive input, render output            Business logic, state mutation
Controllers     Route requests, coordinate layers       Direct data access, computation
Services        Business logic, workflows               I/O, rendering, DB calls
Data / Models   Storage, retrieval, schema              Logic, formatting, side effects
Utils / Helpers Pure transformations, no side effects   State, I/O, anything stateful
```

**Rule:** If you find yourself writing business logic inside an event handler,
callback, route handler, or UI component — stop. Extract it to a service or
helper first.

### Function Rules

- One function = one responsibility. If you need "and" to describe what it does, split it.
- Functions that compute should not also fetch, write, or render.
- Functions that fetch should not also transform or apply logic to the result.
- Prefer pure functions (same input → same output, no side effects) wherever possible.
- Side effects (I/O, mutation, network) are explicit, named, and isolated.
- Max ~30 lines per function as a soft ceiling. If it's longer, question why.

### State Management

- State lives in one place per concern. It is not duplicated across layers.
- Never mutate state inside a utility function.
- Never read global state inside a pure function.
- Side-effectful state changes are named like what they do: `updateUserSession()`,
  not `handleThing()`.

### Error Handling

- Errors propagate up — they are not silently swallowed at lower layers.
- Each layer handles only the errors it can meaningfully act on.
- Logging happens at the boundary where the error is caught, with context.

---

## Session Protocols

### Inherited Codebase (Existing project, no prior log)

This is the case when the starter pack has been dropped into an existing repo
that was not built with this setup. The codebase exists, but there is no
`CAPTAINS_LOG.md`, no filled-in `ARCHITECTURE.md`, and no established workflow.

**The agent must not write or change any code until the full assessment is complete.**

#### Phase 1 — Read and Map (no edits)

```
[ ] 1. Read ARCHITECTURE.md (this file) and CLAUDE.md in full
[ ] 2. List the entire repo structure — every directory and file
[ ] 3. Identify and read: entry points, config files, package manifests,
        dependency lists, any existing README or docs
[ ] 4. Read the git history — see Git History Reconstruction below
[ ] 5. Read the most-changed and most-central source files in full
[ ] 6. Identify the tech stack — languages, frameworks, runtimes, versions
```

#### Git History Reconstruction

For inherited codebases, the git history is a low-fidelity Captain's Log that
already exists. The agent must read and synthesize it into a reconstructed
`CAPTAINS_LOG.md` before the first live session entry is written.

**How far to go back:**
The agent judges based on repo size and history depth:
- Small repo or few commits — read the full history
- Medium repo — read until the history becomes redundant or pre-dates the
  current codebase shape (major refactors, renames, or rewrites are a natural
  stopping point)
- Large repo with hundreds of commits — focus on: the earliest commits
  (establish intent), major inflection points (large diffs, branching patterns,
  commit message tone changes), and the most recent 20-30 commits (current state)
- In all cases: read diffs for significant commits, not just messages

**Reconstruction commands:**
```bash
# Full log with dates and authors
git log --oneline --all

# Identify high-churn files (signals complexity and problem areas)
git log --all --format=format: --name-only | sort | uniq -c | sort -rg | head -20

# Read diff for a specific commit
git show [commit-hash]

# See what changed between two points
git diff [older-hash] [newer-hash] --stat
```

**Reconstructed entry format:**

Reconstructed entries use the standard Captain's Log format but are clearly
marked so any reader — human or agent — knows they were inferred from git
history rather than written live with full session context:

```markdown
## [Inferred Phase Name] — [date range: YYYY-MM-DD to YYYY-MM-DD]
> ⚠️ RECONSTRUCTED — inferred from git history, not written during a live session.
> Confidence: [High / Medium / Low] — [brief reason, e.g., "clear commit messages"
> or "sparse commits, intent inferred from diffs"]

**What was built / changed:**
- `[path/to/file.ext]` — [what changed, inferred from commits and diffs]

**Architectural decisions:**
- [Any decisions visible from commit messages or structural changes] — WHY: [inferred]

**Codebase state at end of this phase:**
- [What appeared to be working based on the code at this point in history]

**Watch items / observations:**
- [Anything notable — abandoned branches, reverted work, sudden direction changes]

---
```

Reconstructed entries are prepended oldest-first so the log reads
chronologically from bottom (oldest) to top (newest), with the first live
session entry at the very top.

#### Phase 2 — Assess and Report

After mapping, the agent must produce a written assessment covering:

```
1. Tech stack — what is confirmed present and at what versions
2. Inferred architecture — how the code is actually structured
   (even if poorly — describe what IS there, not what should be there)
3. Entry points — where execution begins, how requests/events flow
4. Problem areas — tech debt, dead code, inconsistent patterns,
   missing error handling, hardcoded values, security concerns
5. Unknown or unclear areas — anything ambiguous that needs developer input
6. Dependency health — outdated, deprecated, or abandoned packages
7. Test coverage — what is tested, what is not, whether tests pass
```

Do not soften the assessment. If the codebase is in poor shape, say so clearly
and specifically. The developer needs an honest picture before deciding what to do.

#### Phase 3 — Build Out Project Docs

After the developer has reviewed the assessment:

```
[ ] 1. Fill in the Project-Specific Architecture section of ARCHITECTURE.md
        based on what was found — actual structure, not ideal structure
[ ] 2. Fill in the Pattern Registry with any patterns that exist in the code
        (including anti-patterns worth flagging)
[ ] 3. Fill in the Tech Stack table in CLAUDE.md
[ ] 4. Fill in the File Structure section in CLAUDE.md
[ ] 5. Finalize CAPTAINS_LOG.md:
        - Reconstructed entries (from git history) are already present from Phase 1
        - Prepend a live first-session entry above them documenting:
            - The state of the codebase as inherited and assessed
            - Key findings from the assessment
            - What the developer has decided to do next
            - Watch items (known risks, problem areas to address)
        - This live entry is NOT marked as reconstructed — it was written with
          full session context and developer input
[ ] 6. Confirm the first task with the developer before writing any code
```

#### Phase 4 — Confirm and Begin

Only after Phases 1–3 are complete and the developer has confirmed the first task
should the agent write any code. From this point forward, standard session
protocols apply.

---

### First Session (No Captain's Log exists yet)

If `CAPTAINS_LOG.md` does not exist, the project is new or the log was never started.
The agent must:

```
[ ] 1. Read ARCHITECTURE.md and CLAUDE.md in full
[ ] 2. Scan the repo structure — list all files and directories (read only, no edits)
[ ] 3. Identify entry points, existing patterns, and any code already present
[ ] 4. Report findings to the developer:
        - What exists, what is wired up, what appears incomplete
        - Any immediate concerns or inconsistencies observed
[ ] 5. Create CAPTAINS_LOG.md with an initial entry documenting the starting state
[ ] 6. Ask the developer to confirm the task before writing any code
```

Do not assume a blank repo. Read first, report, confirm, then act.

---

### Session Resumption (Captain's Log exists)

At the start of every new session — before the developer says anything, before any
code is written — the agent must automatically run this protocol and report the result:

```
[ ] 1. Read CAPTAINS_LOG.md — most recent entry first
[ ] 2. Read ARCHITECTURE.md and CLAUDE.md
[ ] 3. Report to the developer (unprompted):
        a. Where we left off (last sprint/task completed)
        b. Current codebase state (what is working, what is stubbed, what is incomplete)
        c. Open watch items from the last session
        d. Proposed next step based on the log
[ ] 4. Wait for developer confirmation before touching anything
```

This report is the answer to "where did we leave off?" — the agent delivers it
automatically so the developer never has to ask twice.

**The Captain's Log is the universal handoff artifact.** It is written to be read
by humans and by any coding agent on any platform. A session started in Claude Code
can be handed to Codex, Cursor, Windsurf, or any other agent — the log provides
full context without requiring access to chat history.

---

## Pre-Edit Protocol (Mandatory)

Before making any changes to the codebase, the agent must complete this checklist
and report the results:

```
[ ] 1. Read CAPTAINS_LOG.md — orient to where the last session ended
[ ] 2. List all files relevant to the task (read only, no edits)
[ ] 3. Identify existing patterns used in those files (naming, structure, data flow)
[ ] 4. Identify where the relevant logic currently lives (layer, file, function)
[ ] 5. State the exact scope of the planned change (which files, which functions)
[ ] 6. Confirm no existing pattern already solves the problem
[ ] 7. Identify any external systems, SDKs, or APIs involved — if any, complete
        the External Research Protocol before proceeding
[ ] 8. Confirm git working tree is clean before starting (run: git status)
```

Do not proceed until this checklist is complete and confirmed.

---

## Scope Control

- One task prompt = one logical change. Do not bundle unrelated changes.
- Before editing, declare: "I will change X in Y. I will not touch Z."
- Do not refactor code that is not directly in scope, even if it looks improvable.
- Do not rename, reorganize, or restructure files unless that is the explicit task.
- If you discover a problem outside your scope, note it and stop. Do not fix it.

---

## Checkpoint / Rollback Strategy

```bash
# Before starting any task — verify clean state
git status                        # must show clean working tree
git log --oneline -5              # confirm you know where you are

# After each completed task — in this order:
# 1. Run tests — all must pass
# 2. Update CAPTAINS_LOG.md — prepend new entry (newest first)
# 3. Update CHANGELOG.md — append entry
# 4. Commit everything together
git add -A
git commit -m "[imperative mood description of what changed]"

# If something breaks — roll back to last commit
git reset --hard HEAD             # discard all uncommitted changes
git log --oneline -5              # confirm you're back to a good state
```

**Rule:** The agent must commit after every completed task before starting the next.
A task is not complete until tests pass and the commit is made.
If tests fail, roll back — do not accumulate broken state.

---

## Human Readability & Handoff Readiness

This codebase must be transferable to a human dev team at any time.
A developer who has never seen this project should be able to orient themselves
in under 30 minutes. Every change the agent makes must uphold this standard.

### Comment Standards

**What must be commented:**
- Every file: a 1-3 line header explaining what it is, what it owns, and what it does NOT do
- Every function: what it does, what it takes, what it returns, and any non-obvious side effects
- Every architectural decision: explain WHY a choice was made, not just what it does
  - e.g., `// Using a lookup table here instead of a switch — O(1) vs O(n), and easier to extend`
- Any logic that is non-obvious, stateful, or has subtle ordering requirements
- Any workaround or constraint imposed by a library, runtime, or external system

**What must NOT be in the code:**
- Magic values — no bare `7`, `"active"`, `3000` without a named constant and comment
- Cryptic abbreviations — `processUserAuthenticationRequest()` not `procUsrAuthReq()`
- Uncommented regex — every regex gets a comment stating what it matches and why
- Logic that only makes sense to the agent that wrote it — if you cannot explain it
  in plain English in a comment, restructure it until you can

### Avoiding Agent-isms

These patterns are common in agent-generated code and must be actively avoided:

```
BAD                                     GOOD
───────────────────────────────────────────────────────────────────
Deeply nested callbacks                 Named functions, flat structure
Inline magic numbers                    Named constants with comments
handleThing() / processThing()          Names that state the action and subject
Giant catch-all try/catch blocks        Specific error types, contextual logging
"Clever" one-liners                     Readable multi-line equivalents
Redundant comments ("// increment i")  Comments explaining WHY
```

### Changelog

The agent must append an entry to `CHANGELOG.md` (create it if it does not exist)
after every committed task. Format:

```markdown
## [date] — [one-line summary of what changed]
- What was added / changed / removed
- Why (the reason or requirement behind the change)
- Any decisions made and the rationale
- Any known limitations or follow-up work flagged
```

This log is the paper trail for the human team. It must be kept current.

### Captain's Log

The file `CAPTAINS_LOG.md` at the repo root is a running development log, newest entry first.
It exists so any new agent session — or human developer — can orient quickly and continue
without re-reading the full codebase.

**The agent must update the Captain's Log automatically after every committed task**,
not only when explicitly instructed. It is part of the commit gate — a task is not
complete until the log is updated.

#### When to update
- After every committed task, as the final step before moving to the next prompt
- At the start of a new session if the previous session ended without an update
- When explicitly asked to "update the captain's log"
- When inheriting an existing codebase — reconstruct from git history first,
  then prepend a live assessment entry (see Inherited Codebase protocol above)

#### How to update
- Prepend the new entry above the most recent existing entry (newest-first order)
- Do not summarize the entire codebase history — only what changed since the last entry
- Pull from: actual files changed, functions added or modified, decisions made,
  commands or routes registered, schema changes, and any context from the current session
- Be specific — reference actual function names, file paths, and identifiers
  rather than describing things generically

#### Entry format

Entries must be specific enough that a cold agent on a different platform can
read the log and continue work without accessing any chat history or prior session.
Reference actual file paths, function names, and identifiers — never describe
things generically.

```markdown
## [Sprint or Task Name] — [YYYY-MM-DD]

**Agent/Platform:** [e.g., Claude Code, Codex, Cursor — for audit trail]

**What was built / changed:**
- `[path/to/file.ext]` — [what changed and why, specific function or feature names]
- `[path/to/file.ext]` — [what changed]

**Architectural decisions:**
- [Decision made] — WHY: [rationale. This is the trail for the next agent and human team]

**Codebase state:**
- Working: [what is fully functional]
- Wired up but incomplete: [what exists but is stubbed, partial, or untested]
- Not started: [what is planned but not yet touched]

**Relevant files:**
- `[path/to/file.ext]` — [what this file is and its current state]

**Watch items for next session:**
- [Specific loose end, deferred decision, or known issue with enough detail to act on]
- [Any decision that was punted and needs resolution before the next feature]

---
```

The `---` separator is required between entries. Newest entry is always at the top.

#### Reading the log

The Session Resumption Protocol (above) requires the agent to read `CAPTAINS_LOG.md`
as the first act of every new session — before reading any other file, before asking
any questions. The most recent entry is the starting point. Watch items from that
entry are the first thing to address or confirm with the developer.

---

### External Research Protocol

Before writing any code that involves an external system, SDK, API, framework,
or platform the agent is not verified-current on, the agent must research it first.
Do not rely on training data alone — it may be stale, incomplete, or wrong.
This is especially critical for niche, underdocumented, or version-sensitive systems.

### When This Triggers

Research is required any time the task involves:
- A third-party SDK, API, or library
- A platform with its own scripting or plugin model (DAWs, hardware controllers,
  game engines, creative tools, etc.)
- A framework where version differences affect behavior
- Any system where the agent's knowledge cannot be independently verified
- Hardware-software integration where protocol details matter

### Research Steps

```
[ ] 1. Identify every external system relevant to the task
[ ] 2. For each system, search for:
        - Official documentation and SDK references
        - Source repos (GitHub, GitLab, etc.) — read actual code, not just docs
        - Known version constraints or breaking changes
        - Community resources: forums, issues, known workarounds
        - Any existing open-source implementations of similar problems
[ ] 3. Cross-reference findings — if sources conflict, flag it
[ ] 4. Document what was found before writing any code (see below)
[ ] 5. Flag anything that could not be verified — do not silently assume
```

### Platform-Specific Access

Agents handle web research differently — use whatever is available:

| Agent | Web access |
|-------|-----------|
| Claude Code | `WebSearch` tool (already permitted in settings.json) |
| Codex | Built-in web access if enabled; otherwise request docs from developer |
| Cursor / Windsurf | Use built-in search or ask developer to paste relevant references |
| Any agent | If web access is unavailable, explicitly list what docs are needed and ask |

If an agent has no web access and cannot verify external APIs or SDKs,
it must say so clearly and ask the developer to supply the relevant documentation
before proceeding. Do not guess at undocumented or version-sensitive behavior.

### Documenting Research

Findings must be recorded in the Captain's Log entry for the session:

```markdown
**External research conducted:**
- [System/SDK name] vX.X — [source URL or repo]
  Key findings: [what was confirmed, what version constraints apply]
  Gaps / unverified: [anything that could not be confirmed]
```

This ensures the next agent session — and any human developer — knows what
sources the code was based on and where assumptions were made.

---

## Pattern Registry Maintenance

When the agent introduces a new pattern — a new way of structuring a module,
handling errors, managing state, etc. — it must document it in the
Pattern Registry section below before committing. The registry is a handoff artifact,
not an afterthought.

---

## Pattern Registry

> **This section documents the established patterns in this project.**
> Before implementing anything, check here first.
> If a pattern exists for your problem, use it — do not invent an alternative.
> If you add a new pattern, document it here.

<!-- Fill in as your project grows. Examples below. -->

### [Pattern Name]
```
Purpose:     [What problem this pattern solves]
Location:    [Where to find the canonical example]
Usage:       [How to apply it]
Anti-pattern: [What NOT to do instead]
```

### [Pattern Name]
```
Purpose:
Location:
Usage:
Anti-pattern:
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
