# CLAUDE.md — [PROJECT_NAME]

> **For AI coding agents (Claude Code, ChatGPT Codex, and others):**
> Read files in this exact order before making any changes:
> 1. `ARCHITECTURE.md` — structural rules, pre-edit protocol, pattern registry
> 2. This file (`CLAUDE.md`) — tech stack, style, workflow, task prompts
> 3. Any supplementary docs listed in the Related Docs table below
>
>
> **Every new session:** Determine your situation before doing anything else:
> - **Log exists** → read most recent entry, report status, wait for confirmation
> - **No log, new project** → scan repo, report findings, create log, confirm task
> - **No log, existing codebase** → full assessment first (read, map, report, fill in
>   project docs, create log) before any code is written
>
> See `ARCHITECTURE.md` → Session Protocols for the full protocol for each case.
>
> Do not write any code until all steps are complete.
> Claude Code reads this file automatically. Codex agents: see also `AGENTS.md`.
> All instructions are platform-neutral — follow them regardless of which agent you use.
>
> **For the developer:** This is your project instruction manual. `ARCHITECTURE.md`
> is your structural contract. Together they are the single source of truth.

<!--
AGENT COMPATIBILITY NOTE:
- Claude Code: reads CLAUDE.md automatically on session start
- ChatGPT Codex: reads AGENTS.md automatically, which redirects here
- Other agents (Cursor, Windsurf, Aider, etc.): should be pointed to this file
All instructions apply equally to all agents.
-->

---

## What This Project Is

<!-- Replace with a 2-3 sentence description of the project -->
[PROJECT_NAME] is ...

### License
<!-- e.g., MIT, GPL-3.0, proprietary -->

---

## Tech Stack & Constraints

<!-- List the languages, runtimes, and frameworks. Be specific about version
     constraints — this is what prevents agents from writing incompatible code. -->

| Technology | Version / Constraint | Notes |
|-----------|---------------------|-------|
| Language | e.g., Python 3.10+ | |
| Runtime | e.g., Node 18+ | |
| Framework | e.g., React 18 | |
| Linter | e.g., ESLint, Ruff | |
| Formatter | e.g., Prettier, Black | |
| Tests | e.g., pytest, vitest | |

### Language Rules
<!-- Specify hard constraints. Examples below — delete what doesn't apply. -->

```
# Python example:
- Type hints on all function signatures
- No bare except: — always catch specific exceptions
- f-strings preferred over .format()

# JavaScript example:
- ES6+ (or ES5 only if constrained like Max JS)
- Strict mode ('use strict';)
- No var — use const/let

# General:
- No hardcoded secrets, API keys, or passwords
- No TODO/FIXME in committed code without a linked issue
```

### Validation Commands
<!-- The agent should be able to run these to verify its work. -->
```bash
# Lint
[INSERT LINT COMMAND]           # e.g., npm run lint, ruff check .

# Format check
[INSERT FORMAT COMMAND]         # e.g., npx prettier --check ., black --check .

# Type check (if applicable)
[INSERT TYPE CHECK COMMAND]     # e.g., npx tsc --noEmit, mypy .

# Test
[INSERT TEST COMMAND]           # e.g., npm test, pytest

# Build (if applicable)
[INSERT BUILD COMMAND]          # e.g., npm run build, make
```

**Rule: Run lint and tests after every change.** If a linter or test command is
configured above, the agent must run it after each edit and fix any errors before
committing.

---

## File Structure

<!-- Show the project layout. Mark files the agent should NOT edit. -->
```
/                              # repo root
├── .claude/
│   └── settings.json          # Claude Code permissions
├── .codex/
│   └── config.toml            # Codex CLI config
├── CLAUDE.md                  # THIS FILE — canonical instructions
├── AGENTS.md                  # Codex entry point (points here)
├── src/                       # source code
├── tests/                     # test files
├── docs/                      # documentation
├── README.md
├── LICENSE
└── .gitignore
```

### Files the Agent Must NOT Edit
<!-- List binary files, generated files, config that shouldn't be touched -->
```
- *.amxd, *.maxpat          # Binary — edit in GUI only
- package-lock.json          # Auto-generated
- .env, .env.*               # Secrets
```

---

## Code Style

### Naming Conventions
<!-- Be explicit — agents follow rules literally -->
```
Files:          snake_case.js / snake_case.py / kebab-case.tsx
Functions:      camelCase (JS) / snake_case (Python)
Classes:        PascalCase
Constants:      UPPER_SNAKE_CASE
Private:        _prefixed (Python) / #private (JS class fields)
```

### Formatting Rules
```
Indentation:    [2 spaces / 4 spaces / tabs]
Line length:    [80 / 100 / 120] characters max
Trailing comma: [yes / no]
Semicolons:     [required / omitted] (JS)
Quotes:         [single / double]
```

### Documentation Rules

**Per file:**
- Every file starts with a 1-3 line header comment: what this file is, what it owns,
  and what it deliberately does NOT do (prevents scope creep over time)

**Per function:**
- All public functions: JSDoc (JS) or docstring (Python) — params, return value, side effects
- Private/internal functions: at minimum a single line stating the purpose

**Inline comments:**
- Explain WHY, not WHAT — the code shows what; the comment explains the reasoning
- Required for: non-obvious logic, ordering dependencies, workarounds, constraints
  imposed by external libraries or runtimes
- No commented-out code — delete it, git has history

**Handoff standard:**
- A developer joining this project cold must be able to understand any file's purpose
  within 2 minutes of reading it
- If a function or module would confuse a competent developer without a comment, add one
- Named constants over magic values — always. Document the constant's purpose and origin.

### Error Handling
```
- Never swallow errors silently
- Log with context: what failed, what input caused it, what to do about it
- Use specific exception types, not generic catch-all
- Gate debug logging behind a flag or log level
```

---

## Git Workflow

```bash
# Branch naming
feature/short-description
fix/short-description
refactor/short-description

# Commit messages — imperative mood, concise
"Add mode routing lookup table"        # good
"Added stuff"                          # bad
"Fix null check on LiveAPI discovery"  # good

# Commit after each logical change, not after each file
# The agent should commit after each completed prompt/task
```

---

## Task Prompts (for Claude Code, Codex, or any agent)

<!-- Replace with your actual phased tasks. Pattern:
     - Start with a read-only analysis step
     - One logical change per prompt
     - Git commit between each
     - Test between each -->

```
1. "Read the codebase. Summarize the structure, entry points, and any issues
   you see. Do NOT edit yet."

2. "[First refactoring/feature task with specific instructions]"

3. "[Next task...]"
```

---

## Related Docs

<!-- Link to supplementary docs if they exist -->
| Doc | Purpose |
|-----|---------|
| `ARCHITECTURE.md` | **Read first** — structural rules, pre-edit protocol, pattern registry |
| `AGENTS.md` | Codex entry point (redirects here) |
| `README.md` | User-facing documentation |

---

## Related Projects

<!-- Link to upstream, forks, or sibling projects -->
| Project | Relationship |
|---------|-------------|
