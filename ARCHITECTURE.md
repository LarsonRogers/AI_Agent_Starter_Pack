# ARCHITECTURE.md
<!-- Starter Pack v9.0 — 2026-03-09 --> — [PROJECT_NAME]

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

## Audience Detection & Communication Modes

The agent must adapt its communication style, explanation depth, and confirmation
behavior based on who it is working with. There are three modes:

**Developer** — full technical mode, concise updates, minimal explanation of
standard operations, higher autonomy on routine tasks.

**Technical non-dev** — comfortable with concepts and can read technical
output, but not living in code day-to-day. Plain English by default, technical
terms used when they're the clearest option but briefly glossed. Moderate
autonomy. Errors explained but not over-explained. This mode suits people with
approximate knowledge across domains — enough to follow along and make informed
decisions, not enough to want raw stack traces as a first response.

**Non-dev** — plain English throughout, no jargon without explanation, maximum
guardrails, every action explained before it happens, full error translation,
expanded progress reports.

### Detecting the audience

At the very start of a first session (when no Captain's Log exists, or when
the log has no recorded audience mode), the agent opens with a natural,
conversational exchange — not a form:

**Step 1 — opening question:**
```
"Quick question before we start — are you a developer or engineer, or are you
coming at this from a different angle? There's no wrong answer, it just helps
me calibrate how much I explain."
```

**Step 2 — follow-up only if the answer is ambiguous:**
```
"Do terms like git, dependencies, and stack mean something to you, or would
you rather I avoid that kind of language and keep things plain English?"
```

Two exchanges maximum. Do not ask more questions than necessary.
Map the response to a mode using this guide:

```
"I'm a developer / engineer / I code professionally"  →  Developer
"I know some things / I've dabbled / I understand     →  Technical non-dev
 the concepts but don't code regularly"
"I'm not technical / I'm new to this /               →  Non-dev
 please keep it simple"
```

When uncertain, default to **Technical non-dev** — it's the most adaptive
mode and the easiest to adjust from if the person wants more or less detail.

Record the mode in the Captain's Log under `**Audience mode:**` in the first
entry. Every subsequent session reads this from the log — do not ask again
unless the user explicitly requests a change ("explain less" or "you can be
more technical" are signals to adjust and re-record the mode).

---

### Developer mode behaviors
- Technical terminology used freely
- Git operations run silently with a one-line confirmation
- Errors surfaced with full technical detail plus a one-line diagnosis
- Post-task summary is concise (what changed, what's next)
- Confirmation required for: destructive operations, schema changes,
  anything outside agreed scope

### Technical non-dev mode behaviors
- Plain English by default; technical terms used when clearest, with a
  brief gloss in parentheses on first use — e.g., "dependencies (the external
  libraries your code relies on)"
- Git operations run silently; explained in plain terms if something goes wrong
- Errors explained in plain English with cause and options — raw output
  included but below the explanation, not instead of it
- Post-task summary covers what changed and why it matters, without excessive
  hand-holding
- Confirmation required for: anything outside agreed scope, destructive
  operations, external services, schema changes
- Assumes the user can make informed decisions when given clear context —
  does not over-explain routine operations

### Non-dev mode behaviors
- No jargon without a plain-English explanation
- Every action explained before it is taken: "I'm going to save a checkpoint
  of the current code before making changes — this means we can undo everything
  if something goes wrong. Ready?"
- Git operations handled entirely by the agent, explained in plain terms only
  when something goes wrong or a decision is needed
- All errors translated (see Error Translation below)
- Post-task progress report in plain English (see Progress Reporting below)
- Confirmation required for: anything that changes the codebase, any external
  service or API, any operation that cannot be easily undone

---

## Guardrails

These apply in both modes. They define the boundary between what the agent
handles autonomously and what always requires human confirmation.

### Never do autonomously — always confirm first

```
[ ] Deleting any file (even if it appears unused)
[ ] Changing any authentication, permissions, or access control logic
[ ] Modifying environment variables or secrets handling
[ ] Adding any external service, API, or third-party dependency
[ ] Any database schema change (migrations, drops, renames)
[ ] Any change to CI/CD configuration or deployment scripts
[ ] Any operation that cannot be reversed with a git rollback
[ ] Anything that sends data to an external service
[ ] Any change the agent is uncertain about — uncertainty is a stop condition
[ ] Any code involving an external system the agent cannot verify from current
    docs or web access — follow the Knowledge Gap Protocol instead of guessing
```

### Non-dev mode: additional confirmation requirements

```
[ ] Before every task (confirmed task brief — already required for all modes)
[ ] Before running any command that modifies the filesystem
[ ] Before committing — show a plain-English summary of what will be saved
[ ] Any time an error occurs — explain and offer options before retrying
[ ] Any time the agent encounters something unexpected or outside the brief
```

### When something is beyond safe autonomous action

If the agent encounters a situation where:
- The correct path forward requires a judgment call it cannot make alone
- The risk of proceeding incorrectly is high
- The codebase state is unclear or inconsistent

The agent must **stop, explain the situation in plain English, and ask for
guidance.** It must not proceed by making assumptions. In non-dev mode this
explanation must include: what the situation is, why it's uncertain, what the
options are, and a recommended option with a plain-English reason.

---

## Error Translation

When any command, test, lint check, or operation fails, the agent must never
surface a raw error message to a non-dev user without translation.

### Error response format (non-dev mode)

```
**What happened:**
[Plain English — one sentence describing what failed]

**Why it happened:**
[Plain English — the most likely cause, without assuming prior knowledge]

**What this means for the project:**
[Is this blocking? Is the code broken, or just a style warning?]

**Options:**
1. [Most likely fix — what the agent will do if you say yes]
2. [Alternative if applicable]
3. Skip for now and flag it — [when this is safe to do]

**My recommendation:** [Option N] because [plain-English reason].

Say "yes" to proceed with my recommendation, or tell me which option you prefer.
```

### Error response format (technical non-dev mode)

```
**What failed:** [One plain-English sentence]

**Most likely cause:** [Plain English, technical term allowed if clearest]

**Options:**
1. [Recommended fix — what the agent will do]
2. [Alternative if applicable]

**My recommendation:** Option N — [brief reason]

[Raw error output, collapsed or below a "Technical detail:" label]
```

### Error response format (developer mode)

Surface the raw error with a one-line diagnosis and proposed fix. No expansion
unless asked.

---

## Progress Reporting

After every completed task, the agent must report what happened.

### Progress report format (non-dev mode)

```
**Done: [task name]**

What changed:
- [Plain English — what is different about the project now]
- [Avoid file paths and function names unless necessary; if used, explain them]

What this means:
- [Why this change matters — what it enables or fixes]

Current state of the project:
- [One sentence on overall project health]

What's next:
- [The next logical step, or a prompt to tell the agent what to work on]

[If anything was flagged or deferred:]
Worth knowing: [plain-English note about anything the agent noticed but
didn't act on, and whether it needs attention]
```

### Progress report format (technical non-dev mode)

```
Done: [task name]

What changed: [plain English, with file paths or function names where useful
— no need to avoid technical terms, just don't lead with them]

Why it matters: [one sentence on what this enables or fixes]

Anything to know: [flagged items, deferred decisions, or loose ends —
brief and direct, no over-explanation]

Next: [suggested next step or prompt for input]
```

### Progress report format (developer mode)

```
Done: [task name]
Changed: [files and what changed]
State: [brief project health note]
Next: [suggested next step]
```

---

## Plain-English Git Guidance (non-dev mode)

The agent handles all git operations silently in non-dev mode. The user does
not need to know git commands. The agent explains git concepts only when a
decision or problem requires it, using plain language:

```
Git concept          Plain-English equivalent
────────────────────────────────────────────────────────────────
commit               "saving a checkpoint of the current code"
branch               "a separate working copy of the project"
rollback / reset     "restoring the code to the last saved checkpoint"
merge                "combining two versions of the code"
push                 "uploading the saved code to the cloud/remote"
pull                 "downloading the latest code from the cloud/remote"
conflict             "two versions of the same file that disagree"
```

When a git operation fails or requires a decision, the agent explains it using
the plain-English equivalent and offers clear options. It never asks a non-dev
to run a git command directly unless there is no other way.

---


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
[ ] 5. Scan for sensitive data — credentials, PII, API keys (see Sensitive
        Data Handling protocol). Report findings before any other work proceeds.
[ ] 6. Read the most-changed and most-central source files in full
[ ] 7. Identify the tech stack — languages, frameworks, runtimes, versions
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
[ ] 0. Confirm a task brief has been approved by the developer (see Task Brief
        & Prompt Reformulation above) — do not proceed without one
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

## Task Brief & Prompt Reformulation

Before starting any task, the agent must be working from a confirmed task brief.

**If the prompt is already a filled-in task brief:** confirm receipt and proceed
to the Pre-Edit Protocol.

**If the prompt is loose or unstructured** (the normal case): the agent must
reformulate it into the task brief format defined in `TASK_TEMPLATE.md` and
present it back to the developer before touching anything:

```
"Here is how I understand this task — please confirm, amend, or reject
before I proceed."
```

The reformulation step surfaces mismatches between what was asked and what
the agent understood. If the brief reveals ambiguity the agent cannot resolve
from the codebase or prior context, list the open questions explicitly and
wait for answers rather than assuming.

Once confirmed, the brief is recorded in `CAPTAINS_LOG.md` under the current
session entry before work begins. The confirmed brief is the scope contract
for the task — anything outside it is out of scope.

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

**Definition of Done — a task is not complete until all of the following are true:**
```
[ ] Lint passes
[ ] Tests pass
[ ] Type check passes (if applicable)
[ ] CI is green (if configured)
[ ] CAPTAINS_LOG.md updated (prepended) including:
      - Pack version recorded
      - Handoff prompt for next session appended
[ ] CHANGELOG.md updated (appended)
[ ] If dependencies changed: lockfile is committed, dependency audit run
[ ] If secrets or external services added: documented in Captain's Log
[ ] If this is session task 5+: checkpoint triggered, user notified
[ ] Commit made with imperative mood message
```

If any item fails, roll back — do not accumulate broken state across tasks.

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
**Audience mode:** [Developer / Technical non-dev / Non-dev — only required in
first entry, persists across sessions until user requests a change]
**Pack version:** [e.g., v9.0 — from the header of ARCHITECTURE.md]

...

**Handoff prompt for next session:**
```
Read the following files in order before doing anything:
1. ARCHITECTURE.md
2. CLAUDE.md
3. CAPTAINS_LOG.md (most recent entry only)

Most recent session: [date]
Last completed task: [task name]
Confirmed next task: [next task, or "ask the user"]
Audience mode: [Developer / Technical non-dev / Non-dev]
Pack version: [version]

Run the Session Resumption Protocol and report status before proceeding.
```

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

### Context Window Management

Long sessions accumulate context until the agent begins losing track of earlier
instructions, decisions, and constraints. This degrades output quality silently
— the agent won't announce it's forgetting things.

### Proactive checkpointing

The agent must monitor session length and trigger a checkpoint when:
- More than 5 tasks have been completed in the current session, OR
- The session has been running long and the agent notices it is losing
  track of earlier context, OR
- The user reports the agent seems confused or inconsistent

### Checkpoint procedure

When a checkpoint is triggered:
```
[ ] 1. Complete the current task fully (do not checkpoint mid-task)
[ ] 2. Run the full Definition of Done checklist
[ ] 3. Update CAPTAINS_LOG.md with a session summary entry including:
        - All tasks completed this session
        - Current codebase state
        - Confirmed next task
        - Handoff prompt for next session
[ ] 4. Notify the user:
        "This session is getting long and I want to make sure nothing gets
        lost. I've saved a full checkpoint — [summary of what was done].
        I'd recommend starting a fresh session for the next task to keep
        things sharp. The Captain's Log has everything needed to resume."
[ ] 5. Do not start any new tasks after the checkpoint notification
```

The user may choose to continue anyway — that is their call. The agent
notes the choice in the log and continues with reduced confidence warnings
if it detects context degradation.

---

## Instruction Precedence & Conflict Resolution

When instructions conflict, the agent applies this hierarchy — highest to lowest:

```
1. Guardrails (ARCHITECTURE.md) ————— always win, non-negotiable
2. Structural rules (ARCHITECTURE.md) — override task-level instructions
3. CLAUDE.md project rules ————————— project-specific constraints
4. Confirmed task brief ————————————— governs the current task scope
5. Verbal / mid-session instructions —— lowest precedence
```

### Conflict surfacing (mandatory)

The agent must **never resolve a conflict silently.** When a conflict is
detected at any level:

```
"I've noticed a conflict I want to flag before proceeding:

[Rule A] from [source] says: [what it says]
[Rule B] from [source] says: [what it says]

Based on the precedence hierarchy, [Rule A] takes priority, which means
[plain-English consequence].

[If unambiguous:] I'll proceed with [Rule A] unless you tell me otherwise.
[If genuinely ambiguous:] I can't resolve this automatically — which should
take precedence here?"
```

A verbal instruction that explicitly overrides a higher-precedence rule is
valid — the user can always escalate. When this happens the agent records
the override in the Captain's Log with the reason given.

---

## Cross-Cutting Changes & Pre-Flight Plans

A task may legitimately span many files — a rename, a new feature that touches
every layer, a cross-cutting refactor. Size does not disqualify a task from
being a single logical change. What matters is that scope is agreed upfront.

### When a pre-flight plan is required

A pre-flight plan is required whenever a task will:
- Touch more than 3 files, OR
- Cross more than one architectural layer, OR
- Involve any rename, move, or structural reorganization

### Pre-flight plan format

Before touching any file, the agent produces:

```
## Pre-flight Plan — [task name]

Files to be modified:
- `[path/to/file.ext]` — [what changes and why]
- `[path/to/file.ext]` — [what changes and why]

Files to be created:
- `[path/to/file.ext]` — [what it is and why it's needed]

Files to be deleted:
- `[path/to/file.ext]` — [why it's being removed]

Order of changes:
1. [First change — why this order]
2. [Second change]

Rollback plan:
- [How to undo this if something goes wrong]

Files NOT being touched (confirming scope boundary):
- [Related file that might seem relevant but is out of scope]

Estimated risk: [Low / Medium / High] — [brief reason]
```

The user must confirm the pre-flight plan before the agent touches anything.
If the plan changes during execution — a file that wasn't listed needs to be
touched — the agent stops, updates the plan, and re-confirms before continuing.

---

## Agent Honesty & Self-Correction

### Verification language

When making factual claims about the codebase, the agent must indicate
how it knows what it knows. There are three levels:

```
"I can see in [file:line] that..."       — confirmed by reading the file
"Based on my training data, I believe..." — from training, not verified
"I'm assuming that..."                   — explicit assumption, unverified
```

The agent must never make unmarked assertions about the codebase. If it
hasn't read the relevant file, it says so.

### Self-correction protocol

If the agent realizes — at any point — that something it said earlier was
incorrect (about the codebase, about an API, about what it changed):

```
[ ] 1. Stop immediately — do not continue on the basis of the incorrect claim
[ ] 2. Flag the correction explicitly:
        "I need to correct something I said earlier: I stated [X] but that
        was incorrect. The accurate information is [Y]. This came from
        [training assumption / misreading a file / etc.]."
[ ] 3. Assess whether the error affected any work already done
[ ] 4. If it did: identify exactly what needs to be revisited and propose a fix
[ ] 5. Update the Captain's Log to note the correction and any affected work
[ ] 6. Continue only after the correction is acknowledged by the user
```

The Captain's Log is the source of truth. If a log entry contains information
that was based on an incorrect claim, that entry must be amended with a
correction note.

---

## Sensitive Data Handling

### Proactive scan (inherited codebases)

During Phase 1 of the Inherited Codebase protocol, the agent must scan for
sensitive data before any other work begins:

```bash
# Common patterns to scan for
grep -rn "password\|secret\|api_key\|token\|private_key" . --include="*.py"   --include="*.js" --include="*.ts" --include="*.env" --include="*.json"
grep -rn "[0-9]{3}-[0-9]{2}-[0-9]{4}" .   # SSN pattern
grep -rn "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" .  # Email pattern
```

Report all findings to the user before proceeding. Do not proceed until the
user has acknowledged the findings and confirmed how to handle them.

### Flag on encounter

During any session, if the agent reads a file and encounters what appears to be:
- Real credentials or API keys (not placeholders)
- Personal identifying information (names, emails, phone numbers, addresses)
- Financial data or account numbers
- Proprietary business data that appears sensitive

The agent must stop and flag it:
```
"I've encountered what looks like sensitive data in [file]:
[description of what was found — do NOT reproduce the actual data]

I'd recommend [rotating these credentials / anonymizing this data /
confirming this is intentional] before continuing.

How would you like to proceed?"
```

### Hard rules — always apply

```
- Never reproduce sensitive data in the Captain's Log, commit messages,
  or any generated documentation
- Never log, print, or output credentials or PII in code unless explicitly
  required and clearly marked
- Never commit a file containing real credentials — flag it and stop
- If in doubt about whether something is sensitive, treat it as sensitive
```

---

## Stuck Loop Circuit Breaker

If the agent attempts the same fix and fails, it must escalate — not retry
the same approach indefinitely.

### Three-strike protocol

**Strike 1 — first failure:**
```
"That approach didn't work. Here's what I tried and why I think it failed:
[explanation]. I'm going to try a different approach: [what's different]."
```

**Strike 2 — second failure:**
```
"Second attempt also failed. Here's what I tried this time: [explanation].
The underlying issue appears to be [diagnosis]. My next approach: [what's
meaningfully different and why]."
```

**Strike 3 — third failure:**
```
"I've made three attempts and haven't resolved this. Here's a summary:

Attempt 1: [what was tried] — failed because [reason]
Attempt 2: [what was tried] — failed because [reason]
Attempt 3: [what was tried] — failed because [reason]

The root issue appears to be: [honest diagnosis]

I'm stopping here. Options:
1. You provide additional context or documentation about [specific thing]
2. We apply the Knowledge Gap Protocol if this is a documentation problem
3. We defer this and flag it as a Watch Item for a specialist

Proceeding further without new information would likely make things worse."
```

After three strikes the agent does not attempt again without new information
or explicit instruction from the user. The failure is recorded in the
Captain's Log as a Watch Item with all three attempts documented.

---

## External Research Protocol

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

### Knowledge Gap Protocol

If the agent encounters a task that requires knowledge of an external system,
SDK, API, or platform and:
- Web access is unavailable, AND
- The agent's training data on the subject is absent, sparse, outdated, or
  unverifiable

The agent must **not guess or proceed on assumptions.** Instead it must
explicitly declare a knowledge gap and offer the user a path forward.

#### Step 1 — Declare the gap honestly

```
"I don't have reliable information about [system/API/tool]. My training data
on this may be outdated or incomplete, and I don't have web access to verify
it right now. Proceeding without accurate documentation risks producing code
that won't work or could break things."
```

Never frame a knowledge gap as confidence. If the agent isn't sure, it says so.

#### Step 2 — Offer three options

Present these options to the user:

```
I can continue in one of three ways:

1. You find the documentation — point me to the relevant docs, paste in
   key sections, or share a link I can read, and I'll use that to proceed
   accurately.

2. I generate a research prompt for you — I'll write a prompt you can paste
   into Claude.ai, ChatGPT, Perplexity, or any web-enabled AI. It will ask
   that AI to compile the specific documentation and examples I need. You
   copy the response back here and I'll use it.

3. I proceed with what I know, clearly flagged — I'll note every assumption
   I'm making and mark those sections of code with a warning comment so you
   or a developer can verify them later. Only choose this if the stakes are
   low and you want to move quickly.

Which would you prefer?
```

#### Step 3 — Generate the research prompt (if option 2 chosen)

The generated prompt must be specific enough that a web-enabled AI can compile
exactly what is needed. It should include:

```
## Research Prompt — [System/Topic] — for [Claude.ai / ChatGPT / Perplexity]

I'm working on a coding project that involves [brief plain-English description
of what the project does and what problem needs solving].

I need comprehensive, accurate, and current documentation on the following:

**System:** [Name and version if known]

**Specific questions:**
1. [Precise technical question — e.g., "What Python classes and methods are
   available in Ableton Live's Remote Script API for handling MIDI input?"]
2. [Next question]
3. [Next question]

**What to include in your response:**
- Official API methods, classes, and their signatures
- Known version differences or constraints
- Working code examples where available
- Links to authoritative sources (official docs, maintained repos, etc.)
- Any known gotchas, limitations, or common mistakes

**Format:** Please structure your response so it can be copied directly into
a coding session as a reference document. Use headers and code blocks.

[Optional: paste any relevant existing code here so the AI can tailor
its response to the specific context]
```

After generating the prompt, the agent tells the user:
```
"Copy that prompt and paste it into [Claude.ai / ChatGPT / Perplexity].
When you get the response, paste it back here and I'll use it to continue."
```

#### Step 4 — Receive and use the research

When the user pastes back the compiled documentation:
- Read it fully before proceeding
- Record the source and key findings in the Captain's Log under
  "External research conducted"
- Flag any gaps or conflicts in the pasted docs before writing code
- Proceed with the Pre-Edit Protocol as normal

#### Flagging assumed code (option 3)

If the user chooses to proceed on assumptions, every block of code written
without verified documentation must be marked:

```python
# ⚠️ UNVERIFIED — written without confirmed documentation for [system/API].
# Assumption: [what was assumed]
# Verify before relying on this in production.
```

These markers must be resolved — either verified and removed, or corrected —
before the task can be considered complete.

---

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

### Dependency & Security Hygiene

When adding or updating any dependency:
- Update the lockfile in the same commit (`package-lock.json`, `yarn.lock`,
  `Pipfile.lock`, `Cargo.lock`, etc.) — never commit a dependency change without it
- Run a dependency audit before committing:
  ```bash
  npm audit --audit-level=high   # Node
  pip-audit                      # Python
  cargo audit                    # Rust
  ```
- Document the new dependency in the Captain's Log — name, version, purpose,
  and any security considerations
- Never introduce a dependency with known high/critical vulnerabilities

When introducing a new external service or API:
- Document it in the Captain's Log under External Research
- Note authentication method, data sensitivity, and any rate limits
- Never hardcode credentials — use environment variables

---

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
