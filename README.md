# AI Agent Starter Pack

A platform-agnostic instruction set for AI coding agents. Drop it into any repo
and any agent — Claude Code, Codex, Cursor, Windsurf, Aider, or others — will
orient itself, follow consistent architectural rules, and maintain a running
handoff log so nothing is lost between sessions or platforms.

## What You Get

A coding agent that:
- Reads the codebase before touching anything
- Follows consistent rules for code structure, commenting, and git workflow
- Maintains a Captain's Log so any session — human or agent — can pick up
  exactly where the last one left off
- Produces code that is readable and transferable to a human dev team

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

## Files

```
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

## Agent Compatibility

Instructions are written in plain markdown and are agent-agnostic.
Any agent that can read files can follow them.

| Agent | Entry point |
|-------|-------------|
| Claude Code | `CLAUDE.md` (auto-read on session start) |
| Codex CLI | `AGENTS.md` (auto-read on session start) |
| Cursor, Windsurf, Aider, others | Point to `ARCHITECTURE.md` then `CLAUDE.md` |
