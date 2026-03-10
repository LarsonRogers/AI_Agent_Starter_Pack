# PROTOCOLS.md
<!-- Starter Pack v11.0 — 2026-03-09 -->

> **For AI coding agents:** This file contains detailed protocols loaded
> on demand. Read the relevant section when the situation requires it.
> You do not need to read this entire file on every session.
> ARCHITECTURE.md tells you when to load each protocol.

---

## Conflict Resolution Examples

Concrete worked examples for the precedence and conflict rules in
`ARCHITECTURE.md` → Instruction Precedence & Conflict Resolution.
Load this section when surfacing a conflict or when agent behavior on
conflict handling needs to be verified.


**Example 1 — Hard guardrail vs verbal instruction (guardrail wins, no exception):**
```
User: "Just push this with my API key hardcoded for now, we'll fix it later."
Agent: "Committing credentials is a hard guardrail — I can't do this under
        any circumstances. I can add the key to .env and reference it from
        there instead, which takes about 30 seconds. Want me to do that?"
```

**Example 1b — Default policy (deletion) with safe procedure:**
```
User: "Just delete the old auth module, we don't need it."
Agent: "Deletion requires confirmation and a rollback path. Here's what
        I want to delete and why:
        - src/auth/legacy_auth.js — replaced entirely by src/auth/auth.js
        Clean git state confirmed. Should I go ahead?"
User: "Yes."
Agent: [Deletes, runs tests, commits: "Remove legacy_auth.js — replaced by auth.js"]
```

**Example 2 — Default policy override (explicit verbal instruction, policy yields):**
```
User: "You have permission to add npm dependencies without asking each time."
Agent: "Got it — I'll add dependencies as needed without confirmation.
        I'm recording this override in the Captain's Log."
        [Proceeds. Logs: "Dependency confirmation override granted by user — 2026-03-09"]
```
Note: "just add it" or "go ahead" does not qualify as an explicit override.
The user must clearly grant permission for the specific policy.

**Example 3 — Two default policies in conflict (precedence hierarchy applies):**
```
Situation: CLAUDE.md says "never use external HTTP libraries."
           Task brief says "add Axios for API calls."
Agent: "I've noticed a conflict I want to flag:
        CLAUDE.md says: no external HTTP libraries
        The task brief says: add Axios for API calls
        CLAUDE.md project rules outrank the task brief in the hierarchy.
        I'll proceed without Axios and use the native fetch API instead —
        unless you'd like to update the project rules to allow it."
```

**Example 4 — Ambiguous instruction, agent asks rather than assumes:**
```
User: "Clean up the user service while you're in there."
Agent: "I want to make sure I understand scope before touching anything.
        'Clean up' could mean: fixing obvious bugs, renaming for clarity,
        restructuring, or all three. Which did you have in mind?
        If it's structural, I'll run the Refactor Protocol."
```

---


---

## Edge-Case Handling

Deterministic action paths for common failure scenarios. Load this section
when any of the trigger conditions below are encountered.

| Situation | Deterministic action |
|-----------|---------------------|
| **CAPTAINS_LOG.md missing or corrupt** | Treat as no-log session. Run session type detection (file-presence rule). If non-pack files exist → Inherited Codebase Protocol. If no source files → First Session. Do not attempt to repair a corrupt log — note it and start fresh. |
| **PROTOCOLS.md missing** | Halt immediately. Report: "PROTOCOLS.md is missing from the repo root. Several required procedures are unavailable. Please restore it from the original pack zip before continuing." Do not attempt to guess or reconstruct protocol behavior. |
| **ARCHITECTURE.md or CLAUDE.md missing** | Halt immediately. Report which file is missing and ask the user to restore it. These are the primary instruction sources — proceeding without them produces undefined behavior. |
| **No git installed or git unavailable** | Report clearly what is unavailable: commits, rollbacks, history reconstruction, checkpoint strategy, and refactor protocol all require git. Offer read-only analysis and planning work only. Do not attempt to simulate git with manual file copies. |
| **No file-read capability (web/paste-only agent)** | Ask the user to paste AGENTS.md, then ARCHITECTURE.md, then CLAUDE.md in order. Proceed from pasted content. Note that PROTOCOLS.md sections cannot be loaded on demand — flag any triggered protocol as unavailable and describe the gap. |
| **Partially filled REQUIRED placeholders** | Do not proceed with coding tasks. Report exactly which placeholders remain unfilled. Offer to infer any missing values from repo context, or ask the user directly for values that cannot be inferred. Never assume a placeholder value silently. |
| **Conflicting inferred placeholder values** | Present all candidates to the user with source for each: "I found two possible project names: 'foo' (from package.json) and 'bar' (from README). Which is correct?" Wait for explicit choice before writing. |
| **Pack version mismatch detected** | See Pack Version Consistency Check in ARCHITECTURE.md — halt and report. |


## Known Limitations & Deferred Decisions

This section documents intentional design tradeoffs and explicitly deferred
items. These are not bugs or oversights — they are acknowledged limitations
with recorded rationale. Reviewers and agents should not flag these as issues.

| Item | Status | Rationale |
|------|--------|-----------|
| **Platform-specific config files** (`.claude/`, `.codex/`) | Intentional | Claude Code and Codex are the primary supported agents. Config files for each are provided as-is. Other agents use the Generic Agent Path in SETUP.md. Claiming full platform neutrality would require removing useful tooling. |
| **CLI-first operational assumptions** | Intentional | The pack targets developers and technical users as primary audience. Non-dev path is supported via SETUP.md Generic Agent Path and OS appendix. Full GUI-only agent support is out of scope. |
| **PROTOCOLS.md as external dependency** | Intentional | Splitting protocols into a separate on-demand file was an explicit context-window optimization. Agents must have access to PROTOCOLS.md. If it is missing, the agent should report it and halt rather than guess. |
| **Multi-agent concurrent editing** | Deferred | Branch-per-agent and merge conflict protocols are out of scope for a starter pack. Recommended convention: one agent per branch, human-managed merges. Add if a specific project requires it. |
| **Git unavailable fallback** | Deferred | Git is a hard dependency for rollback, log reconstruction, and checkpoint strategy. Environments without git are not supported. If git is unavailable, the agent should flag it immediately and defer all file-modifying tasks. |
| **Host platform system instruction conflicts** | Out of scope | If a runtime injects system-level instructions that conflict with this pack, behavior is undefined. This pack cannot govern instructions it cannot see. |
| **Unified checklist token (REQUIRED_BEFORE_CODING)** | Deferred | Current `⚠️ REQUIRED PLACEHOLDER` labels are sufficient for human and agent detection. A machine-parseable token adds complexity for marginal gain. Revisit if programmatic placeholder scanning becomes a use case. |
| **Read-order redundancy across files** | Intentional | Some repetition across ARCHITECTURE, CLAUDE, AGENTS, README is deliberate — agents that only read one file should still get the essential behavior. Canonical source is always ARCHITECTURE.md Session Resumption; others reference it. |
| **Screenshot / visual onboarding for non-devs** | Deferred | Out of scope for a text-based pack. A companion visual guide is a reasonable future addition but outside the markdown-only constraint. |
| **Task brief duplication (ARCHITECTURE + TASK_TEMPLATE)** | Intentional | TASK_TEMPLATE.md is the working document; ARCHITECTURE.md summarizes for agent reference. Both are needed for different audiences. They are watched for drift. |
| **Read-order redundancy (raised multiple times)** | Intentional | Session start and read-order summaries appear in ARCHITECTURE, CLAUDE, AGENTS, README, and SETUP. This is deliberate — agents reading only one file should still get core behavior. Canonical source is ARCHITECTURE.md Session Resumption. This tradeoff has been reviewed and accepted across multiple audit cycles. Do not re-flag. |
| **Generic agent paste path omits AGENTS trigger table** | Accepted limitation | SETUP.md generic path tells users to paste ARCHITECTURE and CLAUDE if file access is limited. This omits AGENTS trigger table. Tradeoff: keeping paste instructions simple matters more than completeness for first-time non-CLI users. Agents following ARCHITECTURE alone will still have the Protocol Index. |
| **"Platform-neutral" vs platform-specific config files** | Intentional | Behavioral rules are platform-neutral. Integration files (.claude/, .codex/) are platform-specific adapters. These are separate concerns. CLAUDE.md now states this explicitly. The claim of neutrality applies to behavior, not tooling. |
| **Non-dev "do exactly this" single boxed flow** | Deferred | SETUP.md already has a well-structured non-dev path, first-session transcript, normal/recovery distinction, glossary, and OS appendix. A single boxed canonical flow is a marginal improvement over the current structure. Revisit if user testing shows first-time failure. |
| **Canonical copy block for read-order (raised multiple times)** | Considered and declined | Proposal: maintain one verbatim copy block and reference it everywhere. Decision: the current pointer approach (each file states the order + references ARCHITECTURE as canonical) is more resilient to file-specific context than a shared block. Accepted tradeoff documented across multiple audit cycles. |
| **Failure-path detail for non-git / no-file-read / partial placeholders** | Resolved | These are now documented as deterministic action paths in the Edge-Case Handling table above. No longer a gap. |

---

---

## Read-Only / Meta-Review Protocol

Use this protocol when the task is analysis, review, audit, or documentation
only — no code changes, no commits, no Definition of Done workflow.

### When this applies

```
- Code review or audit request
- Architecture assessment
- Documentation review
- Security or dependency scan
- "Tell me what this does" / "What's wrong with this?"
- Any task where the user explicitly says no changes should be made
```

### Trigger recognition

If a task brief contains any of the following signals, default to this
protocol unless the user explicitly requests edits:

```
"review", "audit", "assess", "analyze", "explain", "summarize",
"what does this do", "what's wrong", "check this", "look at this",
"read-only", "no changes", "don't touch anything"
```

### Protocol

```
[ ] 1. Confirm read-only mode with the user before starting:
        "I'll treat this as a read-only review — no edits or commits.
        Confirm, or let me know if you'd like me to make changes too."
[ ] 2. Read the relevant files — do not stage, modify, or create any file
[ ] 3. Produce the requested analysis, review, or report
[ ] 4. Deliver findings in the format appropriate to audience mode:
        - Developer: prioritized list, concise, specific file/line references
        - Technical non-dev: plain English with technical detail where useful
        - Non-dev: plain English, options and recommendations, no jargon
[ ] 5. End with a clear prompt:
        "No changes were made. Want me to act on any of these findings?"
[ ] 6. Do NOT update CAPTAINS_LOG.md unless the user asks
[ ] 7. Do NOT run lint, tests, or commit checks
```

### Suspended in read-only mode

Pre-edit protocol, task brief / scope contract, Definition of Done checklist,
checkpoint / rollback strategy, Captain's Log update (unless requested).

### Still active in read-only mode

Audience mode communication, sensitive data handling (never reproduce
credentials or PII), honest verification language, hard guardrails.

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


---

### Placeholder Inference Protocol

The user never manually edits starter pack files. All placeholder substitution
is handled by the agent on first session.

**Required placeholders** — marked `⚠️ REQUIRED PLACEHOLDER` in CLAUDE.md.
The agent must resolve all of these before any coding task begins:
```
[PROJECT_NAME]        — infer from repo name, existing README, or package.json/pyproject.toml
[Tech Stack table]    — infer from files present: package.json, requirements.txt,
                        Cargo.toml, go.mod, etc.
[Validation Commands] — infer from package.json scripts, Makefile, or common
                        conventions for the detected stack. If genuinely unavailable,
                        mark with: # NOT CONFIGURED
[File Structure]      — infer from actual repo layout
```

**Deferred placeholders** — marked `DEFERRED` in CLAUDE.md. These are intentional
scaffolding filled as the project develops. The agent never halts on these:
```
[License]          — filled when known
[Task Prompts]     — filled by developer as work is planned
[Related Projects] — filled if/when relevant
[Pattern Name]     — Pattern Registry entries, filled as patterns emerge
[Key Invariants]   — filled as architecture solidifies
```

**The inference flow:**
```
[ ] 1. Scan all pack files for [BRACKETED] placeholders
[ ] 2. Categorize each as Required or Deferred (see above)
[ ] 3. For each Required placeholder, infer the most likely value from
        the repo contents, file names, and any existing documentation
[ ] 4. Present inferred values to the user in a single confirmation block:

        "Here's what I've inferred for this project — confirm or edit
        any of these before I fill them in:"

        Project name:      [inferred value]
        Language/runtime:  [inferred value]
        Lint command:      [inferred value]
        Test command:      [inferred value]
        [etc.]

        Say "confirmed" to accept all, or tell me which to change.

[ ] 5. Write confirmed values into CLAUDE.md and AGENTS.md
[ ] 6. Note any Required placeholders that could not be inferred — ask
        the user directly for those only
[ ] 7. Proceed — do not halt on Deferred placeholders
```

The user's only responsibility is confirming or editing the presented values.
No manual file editing required.

---


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


---

## Validation Tooling Fallback

When lint, test, type check, or CI commands are missing, placeholder, or
unavailable (common in inherited repos or early-stage projects):

```
[ ] 1. Report clearly which commands are missing or unconfigured:
        "I can't run [lint/tests/CI] — the command isn't configured yet."
[ ] 2. Propose alternatives where possible:
        - Suggest the standard tool for the detected stack
          (e.g., "ruff is standard for Python — want me to set it up?")
        - Offer to add the missing configuration as a separate task
[ ] 3. Mark the Definition of Done accordingly:
        - "Lint: skipped — not configured (flagged for setup)"
        - Never silently skip a validation step without noting it
[ ] 4. If CI is inaccessible from the agent environment (offline, no credentials):
        - Note it in the Captain's Log
        - Treat local test pass as the DoD gate
        - Flag CI verification as a Watch Item for the next human-accessible session
```

The agent never silently skips a validation step. Missing tooling is always
reported, with a proposed path to resolution.

---


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


---

## Refactor Protocol

A refactor session has one primary constraint that overrides everything else:
**do not break working behavior.** The goal is structural improvement, not
feature addition. The agent must treat behavioral equivalence as the definition
of success.

This is a distinct session type — not a normal task, not an inherited codebase
assessment. If the user says "refactor this," run this protocol.

### Phase 1 — Establish a working baseline (before any changes)

```
[ ] 1. Run all available tests — they must pass before anything is touched
        If tests fail before refactoring begins, stop and report:
        "Tests are already failing before I've made any changes. We need
        to fix these first, otherwise I can't tell if I've broken anything."
[ ] 2. If no tests exist, flag it clearly:
        "There are no automated tests. I can't verify behavioral equivalence
        after refactoring without a safety net. Options:
        1. I write basic tests first (recommended — separate task)
        2. We proceed carefully with manual verification checkpoints
        3. We note this as a known risk in the Captain's Log and proceed"
        Wait for user decision before continuing.
[ ] 3. Record the baseline commit:
        git add -A
        git commit -m "Baseline: pre-refactor, all tests passing"
        Note this commit hash in the Captain's Log — this is the rollback point
[ ] 4. Document current behavior: note what the code does, what inputs produce
        what outputs, any edge cases visible in tests or comments
```

### Phase 2 — Plan the refactor

```
[ ] 1. Identify the structural problems to address — be specific:
        "Function X does three things and should be split"
        "Module Y mixes data access and business logic"
        Not: "the code is messy"
[ ] 2. Define the target structure — what it should look like after
[ ] 3. Break into the smallest possible sequential steps — each step
        must leave the code in a working state
[ ] 4. Present the plan as a pre-flight plan (ARCHITECTURE.md →
        Cross-Cutting Changes) — confirm before starting
[ ] 5. Explicitly list what will NOT change:
        - Public interfaces / function signatures (unless agreed)
        - External behavior and outputs
        - Data formats going in and out
```

### Phase 3 — Execute incrementally

```
[ ] 1. One structural change at a time — commit after each
[ ] 2. After every change: run tests, confirm they still pass
[ ] 3. If tests fail after a change:
        - Do not proceed to the next step
        - Roll back the failing change: git reset --hard HEAD~1
        - Diagnose why it broke before trying again (three-strike rule applies)
[ ] 4. Never refactor and add features in the same step — if a
        feature opportunity is spotted, note it as a Watch Item and
        continue with structural changes only
[ ] 5. Commit messages during refactor follow this format:
        "Refactor: [what structural change was made]"
        e.g., "Refactor: extract validateUser from authController"
```

### Phase 4 — Verify behavioral equivalence

After all refactor steps are complete:

```
[ ] 1. Run the full test suite — all tests must pass
[ ] 2. Compare behavior against the baseline documentation from Phase 1
[ ] 3. If any behavior changed that wasn't intended, treat it as a bug
        introduced by the refactor and fix it before closing the task
[ ] 4. Record in the Captain's Log:
        - What was refactored and why
        - What structural changes were made
        - Confirmation that tests pass
        - Any behavioral edge cases that were clarified during the process
        - Any deferred improvements spotted but not acted on (Watch Items)
```

### Rollback to baseline

If the refactor goes sideways and cannot be cleanly resolved:

```bash
# Find the baseline commit hash (recorded in Captain's Log)
git log --oneline

# Roll back to known-good baseline
git reset --hard [baseline-commit-hash]

# Confirm you're back to green
# Run tests — they must pass
```

Never roll forward through a broken refactor. Always return to the
last known-good state and start the affected step again from scratch.

### Refactor scope rules

These are stricter than normal scope control:

- One structural concern per task brief — "extract service layer" is one task,
  "rename all variables" is a separate task, never combined
- No opportunistic fixes during refactor — if bugs are spotted, log them as
  Watch Items. Fix them in a separate session after the refactor is complete.
- No dependency updates during a refactor session — too many variables
- No style/formatting changes mixed with structural changes — they make
  diffs unreadable and obscure what actually changed

---

## Binary & Large File Handling

Binary files and large assets require special handling — the agent must not
attempt to read, edit, or commit them without explicit awareness of what
they are and how they should be managed.

### What counts as binary or large

```
Binary files:     .amxd, .maxpat, .als, .wav, .mp3, .aif, .png, .jpg,
                  .pdf, .zip, .exe, .dll, model weights, compiled outputs
Large files:      any file over ~1MB — check before staging
Generated files:  dist/, build/, __pycache__/, *.pyc, node_modules/
```

### Rules

```
[ ] Never attempt to read or parse binary files as text
[ ] Never stage or commit binary files unless explicitly instructed
[ ] Never stage or commit files over 1MB without confirming with the user
[ ] Never commit generated or compiled output — these belong in .gitignore
[ ] If a binary file needs to change, flag it:
    "This file ([name]) is a binary — it needs to be edited in [tool],
    not in code. I can't modify it directly."
```

### On first session — check .gitignore

During any codebase assessment, verify that a `.gitignore` exists and covers:
- Build output directories
- Dependency folders (node_modules/, venv/, etc.)
- Binary/compiled files specific to the stack
- `.env` files (already a hard guardrail but worth confirming)

If `.gitignore` is missing or incomplete, flag it and offer to create or
update it as a separate task before any other work begins.

### Large file storage

If a project needs to track large files (audio samples, model weights, etc.),
note Git LFS (Large File Storage) as the appropriate tool and flag it as a
setup task rather than committing large files directly.

---

## Testing Strategy

The agent must not write superficial tests that pass without actually
verifying behavior. Tests are the safety net — they need to catch real
breakage, not just confirm the code runs.

### What makes a test useful

```
Good test:    verifies a specific behavior or output given a specific input
              catches a real failure mode
              is independent of implementation details (tests what, not how)

Weak test:    just calls a function and checks it doesn't throw
              duplicates the implementation logic inside the assertion
              only tests the happy path when edge cases are the real risk
              passes before and after a bug is introduced
```

### When writing tests the agent must

```
[ ] Test behavior, not implementation — if the internals change but outputs
    stay the same, tests should still pass
[ ] Cover the happy path AND the most likely failure modes:
    - Null / empty / missing inputs
    - Boundary values (zero, negative, max)
    - Invalid types or formats
    - External service failures (mock them)
[ ] One assertion per test where possible — easier to diagnose failures
[ ] Name tests descriptively:
    "test_returns_error_when_input_is_empty" not "test_validate_1"
[ ] Never mock the thing being tested — only mock its dependencies
```

### Coverage guidance

The agent should aim for coverage that gives confidence, not a number:

```
Critical paths (auth, payments, data writes):  high coverage, edge cases included
Business logic / service layer:                high coverage
Controllers / route handlers:                  moderate — integration tests preferred
Utilities / pure functions:                    high — easy to test, high value
UI components:                                 smoke tests minimum
```

If a codebase has no tests, the agent must flag this before any refactor
(already in Refactor Protocol) and offer to write a baseline test suite
as a separate task before structural changes begin.

### When tests are impractical

Some code is genuinely hard to test automatically — hardware interfaces,
GUI interactions, real-time audio, external APIs in development. In these cases:

1. Note why automated testing is limited in the Captain's Log
2. Document manual verification steps that stand in for automated tests
3. Isolate the untestable code to minimize how much depends on it

---
