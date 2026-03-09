# AI Agent Starter Pack
<!-- Starter Pack v9.0 -->

A platform-agnostic instruction set for AI coding agents. Drop it into any repo
and any agent — Claude Code, Codex, Cursor, Windsurf, Aider, or others — will
orient itself, follow consistent rules, and maintain a running handoff log so
nothing is lost between sessions or platforms.

Works for developers and non-developers alike. The agent detects who it's
working with and adapts its communication style, explanation depth, and
confirmation behavior accordingly.

---

## What You Get

A coding agent that:

- **Adapts to who you are** — asks two quick questions, picks one of three
  modes (Developer, Technical non-dev, Non-dev), records it, never asks again
- **Reads before it touches anything** — full codebase assessment before the
  first line of code is written
- **Confirms before it acts** — reformulates your prompts into structured task
  briefs and waits for your approval before starting
- **Plans cross-cutting changes upfront** — any change touching multiple files
  or layers requires a confirmed pre-flight plan
- **Maintains a Captain's Log** — running handoff document so any agent on any
  platform can pick up exactly where the last session left off
- **Generates handoff prompts** — ready-to-paste prompt appended to every log
  entry for switching between Claude, Codex, Cursor, or any other agent
- **Enforces guardrails** — never deletes files, touches secrets, changes auth
  logic, or makes irreversible changes without explicit confirmation
- **Surfaces conflicts** — when instructions conflict, states which rule wins
  and why, never resolves silently
- **Translates errors** — explains failures in plain English with clear options,
  never leaves you with a raw stack trace
- **Has a circuit breaker** — three failed attempts triggers a stop-and-escalate,
  not an infinite retry loop
- **Handles knowledge gaps honestly** — if it doesn't know an API or SDK and
  can't look it up, it says so and offers to generate a research prompt you can
  take to a web-enabled AI
- **Scans for sensitive data** — flags credentials, PII, and secrets on
  inherited repos before any work begins
- **Checkpoints long sessions** — after 5 tasks, saves state and recommends a
  clean restart before context degrades
- **Produces handoff-ready code** — commented, documented, and readable by a
  human dev team from day one

---

## Setup

1. Copy all files into your repo root, preserving the `.claude/`, `.codex/`,
   and `.github/` directory structures.
2. Replace `[PROJECT_NAME]` in `CLAUDE.md` and `AGENTS.md`.
3. Start your agent session. The agent handles the rest.

See `SETUP.md` for a full walkthrough — including instructions for
non-developers and GitHub Desktop upload steps.

---

## Use Cases

**New project**
Start a session. The agent bootstraps from scratch — scans the repo, creates
the Captain's Log, and confirms the first task before writing anything.

**Active project**
Every session resumes automatically from the Captain's Log. Switch between
Claude, Codex, Cursor, or any other agent without losing context. The log
is the handoff.

**Inherited or unmaintained codebase**
Drop the pack in and start a session. The agent reconstructs a Captain's Log
from git history (entries marked as reconstructed with confidence ratings),
runs a full assessment — architecture, problem areas, tech debt, sensitive
data, dependency health — and gives you an honest report before anything
is changed.

---

## Files

```
SETUP.md                    Human bootstrap checklist and walkthrough.
                            Start here, especially if you're not a developer.

TASK_TEMPLATE.md            Structured task brief template. The agent uses
                            this to reformulate your prompts before starting
                            work. You can also fill it out yourself for
                            precise scope control.

ARCHITECTURE.md             The agent's primary instruction manual.
                            Session protocols, structural rules, guardrails,
                            error handling, Captain's Log format, and all
                            behavioral protocols. Agents read this first.

CLAUDE.md                   Project instruction manual — tech stack, code
                            style, validation commands, file structure, and
                            git workflow. Filled in by the agent on first
                            session.

AGENTS.md                   Entry point for Codex and other agents. Core
                            principles, session start protocol, and quick
                            constraints. Points to ARCHITECTURE.md and
                            CLAUDE.md for full detail.

.claude/settings.json       Claude Code permissions — auto-approves edits
                            and common commands, denies destructive ops
                            and secret access.

.codex/config.toml          Codex CLI config — approval policy, sandbox
                            permissions, instruction file references, and
                            web access notes.

.github/workflows/
  agent-ci.yml              CI template — lint, format, type check, tests,
                            secret scanning, dependency audit. Adapt to
                            your stack before use.
```

---

## Starting a Session

**CLI agents** (Claude Code, Codex CLI)
Run from the repo root — the agent reads the instruction files automatically
on startup.

**Web-based or IDE agents** (Cursor, Windsurf, ChatGPT Codex web, etc.)
Paste this as your opening message:

```
Before doing anything else, read AGENTS.md at the repo root and follow
the session start protocol exactly as written. Do not write any code
until the protocol is complete.
```

---

## Agent Compatibility

Instructions are plain markdown — any agent that can read files can follow them.

| Agent | Entry point |
|-------|-------------|
| Claude Code | `CLAUDE.md` (auto-read on session start) |
| Codex CLI | `AGENTS.md` (auto-read on session start) |
| Cursor, Windsurf, Aider, others | Point to `ARCHITECTURE.md` then `CLAUDE.md` |

---

## Evaluation Harness (recommended)

Not included — too project-specific to template. Worth building: a small set
of benchmark tasks with known expected outcomes. Run them when you update the
pack to catch regressions in agent behavior before they affect real work.

---

## Version

This is **Starter Pack v9.0**. The version is recorded in the header of
`ARCHITECTURE.md`, `CLAUDE.md`, and `AGENTS.md`, and in every Captain's Log
entry so there's always an audit trail of which instruction set was active
for any given session.
