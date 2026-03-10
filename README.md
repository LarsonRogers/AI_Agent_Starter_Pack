# AI Agent Starter Pack
<!-- Starter Pack v11.21 -->

A platform-agnostic instruction set for AI coding agents. Drop it into any repo
and any agent — Claude Code, Codex, Cursor, Windsurf, Aider, or others — will
orient itself, follow consistent rules, and maintain a running handoff log so
nothing is lost between sessions or platforms.

Works for developers and non-developers alike. The agent detects who it's
working with and adapts its communication style, explanation depth, and
confirmation behavior accordingly.

---

> **Note:** This pack requires the `protocols/` folder and `PROTOCOLS.md` to be
> present in your repo root for full operation. If protocol files are missing,
> the agent will halt and report it rather than proceeding with undefined behavior.

## What You Get

A coding agent that:

- **Adapts to who you are** — asks two quick questions, picks one of three
  modes (Developer, Technical non-dev, Non-dev), records it, never asks again
- **Reads before it touches anything** — full codebase assessment before the
  first line of code is written, loads detailed protocols on demand to stay
  within context limits
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
2. Start your agent session. The agent handles everything else.

No manual editing of pack placeholders required. The agent infers your project
details, presents them for confirmation, and fills in the pack files itself.
Optional: developers can manually adapt `.claude/settings.json` and the CI
workflow after first session.

See `SETUP.md` for a full walkthrough including non-developer instructions.

---

## Use Cases

Works for new projects, active projects, inherited codebases, and refactors.
See `SETUP.md` for what happens in each scenario.

---

## Authority Matrix

If two files appear to conflict on a topic, this table is authoritative:

| Topic | Authoritative source |
|-------|---------------------|
| Hard guardrails (what agent can never do) | `ARCHITECTURE.md` → Hard Guardrails |
| Default policies (what requires confirmation) | `ARCHITECTURE.md` → Default Policies |
| Verbal override rules | `ARCHITECTURE.md` → Instruction Precedence |
| Session start read order | `ARCHITECTURE.md` → "How to determine your session type" |
| Placeholder inference procedure | `protocols/placeholder-inference.md` |
| Which protocol file to load when | `ARCHITECTURE.md` → Protocol Index (canonical); `AGENTS.md` → Step 2b (quick-reference mirror) |
| Project-specific tech stack and style | `CLAUDE.md` |
| All detailed protocols (inherited, refactor, research, etc.) | `protocols/` directory — one file per protocol |
| Session history and handoff | `CAPTAINS_LOG.md` |

When in doubt: `ARCHITECTURE.md` governs behavior. `CLAUDE.md` governs
project specifics. The `protocols/` files govern procedure detail. `AGENTS.md`
governs agent bootstrapping. Everything else is human-facing documentation.

---

## Files

```
SETUP.md                    Human bootstrap checklist and walkthrough.
                            Start here, especially if you're not a developer.

TASK_TEMPLATE.md            Structured task brief template. The agent uses
                            this to reformulate your prompts before starting
                            work. You can also fill it out yourself for
                            precise scope control.

ARCHITECTURE.md             The agent's primary instruction manual —
                            always loaded. Core rules, guardrails, session
                            protocols, error handling, and behavioral rules.

PROTOCOLS.md                Routing index — lists all available protocol
                            files with trigger conditions. ~400 tokens.
                            Points to protocols/ directory.

protocols/                  One file per protocol (~300–1,900 tokens each).
                            Agents load only the file triggered by their
                            current situation. Protocol files covering
                            inherited codebases, refactors, research,
                            sensitive data, testing, and more.

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

--- Agent-created files (not present until first session) ---

CAPTAINS_LOG.md             Created on first session. Running handoff log,
                            newest entry first. Enables any agent on any
                            platform to resume where the last session ended.

CHANGELOG.md                Created after first commit. Appended after every
                            committed task — what changed, why, and any
                            decisions made.
```

---

## Starting a Session

**CLI agents** (Claude Code, Codex CLI) — run from repo root, agent reads
instruction files automatically.

**Web / IDE agents** (Cursor, Windsurf, ChatGPT web, etc.) — paste this
as your opening message:

```
Before doing anything else, read AGENTS.md at the repo root and follow
the session start protocol exactly as written. Do not write any code
until the protocol is complete.
```

See `SETUP.md` for troubleshooting and detailed instructions by agent type.

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

## Release Checklist

Before tagging a new pack version, verify:

- [ ] Pack-file edit exceptions are in sync across ARCHITECTURE.md (hard guardrails),
      AGENTS.md (Step 3), and CLAUDE.md (safe-edit boundaries)
- [ ] Protocol Index trigger table in ARCHITECTURE.md matches AGENTS.md mirror row-for-row for file-backed protocols (AGENTS mirrors protocol files only — session-type entries like Session Resumption are not mirrored and should not be forced into AGENTS)
- [ ] All 16 protocol files present: `ls protocols/ | wc -l` returns 16
- [ ] Version string updated in all pack file headers

## Version

This is **Starter Pack v11.21**. The version is recorded in the header of
`ARCHITECTURE.md`, `CLAUDE.md`, `AGENTS.md`, `PROTOCOLS.md`, and in every
Captain's Log entry so there's always an audit trail of which instruction
set was active for any given session.
