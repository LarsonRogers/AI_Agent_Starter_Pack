# AI Agent Starter Pack

A platform-agnostic instruction set for AI coding agents. Drop it into any repo
and any agent — Claude Code, Codex, Cursor, Windsurf, Aider, or others — will
orient itself, follow consistent architectural rules, and maintain a running
handoff log so nothing is lost between sessions or platforms.

Works for developers and non-developers alike. The agent detects who it is
working with and adapts its communication, explanation depth, and confirmation
behavior accordingly.

## What You Get

A coding agent that:
- Asks two quick questions, detects who it's working with, and adapts —
  three modes: Developer, Technical non-dev (knows concepts, doesn't code
  daily), and Non-dev. Defaults to Technical non-dev when uncertain.
  Mode is recorded and persists — never asked again
- Reads the codebase before touching anything
- Reformulates your prompts into confirmed task briefs before writing any code
- Follows consistent rules for code structure, commenting, and git workflow
- Explains failures in plain English and offers clear options — never leaves
  you stranded with a cryptic error message
- Maintains a Captain's Log so any session — human or agent — can pick up
  exactly where the last one left off
- Produces code that is readable and transferable to a human dev team
- Enforces guardrails — never deletes files, touches secrets, or makes
  irreversible changes without explicit confirmation

## Setup

1. Copy all files into your repo root, preserving the `.claude/` and `.codex/`
   directory structure.
2. Start your agent session. The agent handles the rest.

That's it. The agent reads the docs, assesses the codebase, fills in what it
needs to know, and tells you what it found before writing a single line of code.

## Use Cases

**New project**
Start a session. The agent bootstraps from scratch — scans the empty repo,
creates the Captain's Log, and asks you to confirm the first task.

**Active project**
Every session resumes automatically from the Captain's Log. Switch between
Claude, Codex, Cursor, or any other agent without losing context. The log
is the handoff.

**Inherited or unmaintained codebase**
Drop the pack in and start a session. The agent reads the git history and
reconstructs a Captain's Log from it — entries are clearly marked as
reconstructed with a confidence rating so you always know what was inferred
vs. written live. It then runs a full assessment: maps the repo, identifies
problem areas and tech debt, documents the inferred architecture, and gives
you an honest report. A live assessment entry is prepended to the top of the
log. You get a navigable project history and architectural overview before
a single line is changed.

## Getting Started

See `SETUP.md` for the human bootstrap checklist — fill in project-specific
placeholders before your first agent session. The agent will detect any
remaining placeholders and halt until they are resolved.

## Files

```
SETUP.md              — Start here. Human bootstrap checklist — what to fill
                        in before your first agent session.

TASK_TEMPLATE.md      — Structured task brief template. Use this when giving
                        tasks to the agent to prevent scope creep and ambiguity.

ARCHITECTURE.md       Agent instruction manual — structural rules, session
                      protocols, handoff and commenting standards, pattern
                      registry, Captain's Log format.

CLAUDE.md             Project instruction manual — tech stack, code style,
                      validation commands, file structure, git workflow,
                      and task prompts. Filled in by the agent on first session.

AGENTS.md             Entry point for Codex and other agents that look for
                      this filename. Summarizes key rules and points to
                      ARCHITECTURE.md and CLAUDE.md.

.claude/settings.json Claude Code permissions — auto-approves edits and
                      common commands, denies destructive operations and
                      access to secrets.

.codex/config.toml    Codex CLI config — approval policy, sandbox permissions,
                      and instruction file references.
```

## Starting a Session

**CLI agents** (Claude Code, Codex CLI): run from the repo root — the agent
reads the docs automatically on startup.

**Web-based agents** (Codex Web, Cursor, v0, etc.): paste this as your
opening prompt:

```
You are an AI coding agent working on this project. Before doing anything
else, read AGENTS.md at the repo root and follow the session start protocol
exactly as written. Do not write any code until the protocol is complete.
```

The docs handle everything from there. The opening prompt just ensures the
agent reads before it acts.

---

## Evaluation Harness (recommended practice)

Not included in this pack because it is project-specific, but worth building:
maintain a small set of benchmark tasks with known expected outcomes and run
them whenever you update the starter pack instructions. This lets you detect
regressions in agent behavior — over-editing, missing tests, weak commit
hygiene, ignoring scope boundaries — before they affect real work.

---

## Agent Compatibility

Instructions are written in plain markdown and are agent-agnostic.
Any agent that can read files can follow them.

| Agent | Entry point |
|-------|-------------|
| Claude Code | `CLAUDE.md` (auto-read on session start) |
| Codex CLI | `AGENTS.md` (auto-read on session start) |
| Cursor, Windsurf, Aider, others | Point to `ARCHITECTURE.md` then `CLAUDE.md` |
