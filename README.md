# AI Agent Starter Pack
<!-- Starter Pack v12.16 — 2026-06-16 -->

An instruction set for AI coding agents. Drop it into any repo and any
supported agent — Claude Code, Codex, OpenCode first-class; others
best-effort — will orient itself, follow consistent rules, and maintain a
running handoff log so nothing is lost between sessions or platforms.

Works for developers and non-developers alike. The agent detects who it's
working with and adapts its communication style, explanation depth, and
confirmation behavior accordingly.

---

> **Note:** This pack requires the `protocols/` folder to be present in your
> repo root for full operation. If protocol files named in the AGENTS.md
> Protocol Index are missing, the agent will halt and report it rather than
> proceeding with undefined behavior.

## What You Get

A coding agent that:

- **Adapts to who you are** — asks one or two questions (second only if the first answer is ambiguous), picks one of three
  modes (Developer, Technical non-dev, Non-dev), records it, never asks again
- **Reads before it touches anything** — full codebase assessment before the
  first line of code is written, loads detailed protocols on demand to stay
  within context limits
- **Confirms before it acts** — reformulates your prompts into structured task
  briefs and waits for your approval before starting
- **Plans cross-cutting changes upfront** — any change touching multiple files
  or layers requires a confirmed pre-flight plan
- **Sizes the architecture on day one** — picks the simplest structure that fits
  (single-file tool → layered app) and writes the layer rules down before coding,
  instead of letting structure drift (the data layer that keeps a growing app
  maintainable, decided up front)
- **Scales rigor to the stakes** — a throwaway spike gets light tooling and
  minimal docs; a production app gets the full set (CI, security scanning,
  coverage); the safety floor (secrets, security pass, review) never scales down
- **Pressure-tests vague or ambitious requests** — interrogates assumptions, edge
  cases, and failure modes before building, so it builds the right thing — without
  grilling you over a one-line fix
- **Sets up quality gates before the first feature** — linter, formatter, type
  checks, tests, a secrets pre-commit hook, and CI, each demonstrated actually
  catching a planted failure before it's trusted
- **Runs a security pass with an independent review** — for anything touching
  input, auth, sessions, or stored data, with a focus on the holes models
  actually miss (CSRF, session handling, access control), checked by a
  fresh-context reviewer before work is called done
- **Routes cheap work to cheaper models (optional)** — bounded, rule-bound checks
  can run on a faster/cheaper model while judgment and safety work stay on the
  main one
- **Keeps itself current** — can check whether a newer pack version is published
  and migrate a project onto it without touching your project's own content
- **Maintains an append-only decision log** — structured entries (what, why,
  state, watch items) so any agent on any platform can trace how the project
  got here
- **Keeps a one-page handoff current** — HANDOFF.md is overwritten after every
  task with where-we-are and a ready-to-paste resume prompt for switching
  between agents
- **Enforces guardrails** — by default requires explicit confirmation for file
  deletion (see Safe Deletion Procedure), requires explicit confirmation for
  auth/access-control changes, never unsafely handles secrets, and never executes irreversible destructive operations (dropping tables,
  deleting cloud resources, purging backups) regardless of confirmation
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
   and `.github/` directory structures — **excluding the `pack-dev/`
   directory** (the pack's own development artifacts; never part of a
   project).
2. Start your agent session. The agent handles everything else.

No manual editing of pack placeholders required. The agent infers your project
details, presents them for confirmation, and fills in the pack files itself.
Optional: developers can manually adapt `.claude/settings.json` and the CI
workflow after first session.

See `SETUP.md` for a full walkthrough including non-developer instructions.

---

## Learn it

Three human-facing docs (read in any order — none of them is loaded by the agent):

- **`SETUP.md`** — install and bootstrap the pack into your repo.
- **`WALKTHROUGH.md`** — one small project built end to end, narrated, so you can
  see the whole process in motion.
- **`GUIDE.md`** — the concepts behind it and how to drive the agent well (the
  four dials, Project Stakes, the guardrails, and the best practices).

---

## Use Cases

Works for new projects, active projects, inherited codebases, and refactors.
See `SETUP.md` for what happens in each scenario.

---

## Authority

`AGENTS.md` is the single source of truth — policy (Part 1) and project
specifics (Part 2). If two files appear to conflict, the Authority Matrix
in `AGENTS.md` is authoritative. `CLAUDE.md` is only the Claude Code import
shim; `protocols/` files govern procedure detail; everything else is
human-facing documentation.

---

## Files

```
SETUP.md                    Human bootstrap checklist and walkthrough.
                            Start here, especially if you're not a developer.

WALKTHROUGH.md              Human-facing. One small project built end to end,
                            narrated. NOT loaded by the agent.

GUIDE.md                    Human-facing handbook — how it works, the four
                            dials, best practices. NOT loaded by the agent.

TASK_TEMPLATE.md            Structured task brief template. The agent uses
                            this to reformulate your prompts before starting
                            work. You can also fill it out yourself for
                            precise scope control.

AGENTS.md                   THE single source of truth — always loaded by
                            both harnesses (Codex directly; Claude Code via
                            the CLAUDE.md import). Part 1: guardrails,
                            policies, session protocols, Protocol Index,
                            Authority Matrix. Part 2: project specifics,
                            agent-maintained as a bounded living summary.

protocols/                  One file per protocol (~300–1,900 tokens each).
                            Agents load only the file triggered by their
                            current situation. Protocol files covering
                            inherited codebases, refactors, research,
                            sensitive data, testing, and more.

CLAUDE.md                   Claude Code import shim — `@AGENTS.md` plus
                            Claude-specific mechanics only. No project
                            content lives here.

.claude/settings.json       Claude Code permissions — auto-approves edits
                            and common commands, denies destructive ops
                            and secret access.

.codex/config.toml          Codex CLI config — approval policy, sandbox
                            permissions, instruction file references, and
                            web access notes.

opencode.json               OpenCode config — permission rules that ask
                            before pack-file edits and deny reads/edits of
                            secret files and dangerous commands. Defense-
                            in-depth, not a hard boundary (see
                            protocols/sensitive-data.md).

.github/workflows/
  agent-ci.yml              CI template — lint, format, type check, tests,
                            secret scanning, dependency audit. Adapt to
                            your stack before use.

.claude/agents/             Light-tier sub-agent templates (also .opencode/agent/
.opencode/agent/            and .codex/agents/) — fill-the-model `*.example`
.codex/agents/              files for routing cheap checks to a cheaper model.
                            Inert until you (or the agent) activate one.

.claude/hooks/              Optional, opt-in Claude Code launch hook that notifies
                            you when a newer pack version is published. Off until
                            registered; reads the upstream URL from AGENTS.md.

pack-dev/                   Pack development artifacts (known-limitations
                            ledger, the pack's own decision log + handoff).
                            NOT copied into projects — the whole directory
                            is excluded from distribution.

--- Agent-created files (not present until first session) ---

DECISION_LOG.md             Created on first session. Append-only structured
                            log — one compact entry per task: what changed,
                            decisions + why, state deltas, watch items. A
                            human changelog can be generated from it.

HANDOFF.md                  Overwritten after every task. Where-we-are
                            snapshot + resume prompt — the first thing a
                            new session reads after AGENTS.md.

BACKLOG.md                  Created by the product-definition protocol.
                            Ordered user-visible outcomes; completing an
                            item triggers a full demo.

RUNBOOK.md                  Created when the app first becomes runnable.
                            Plain-English "how to run this" — kept current
                            in the same commit as any run-step change.
```

---

## Starting a Session

**CLI agents** (Claude Code, Codex, OpenCode) — run from repo root, agent
reads instruction files automatically (Codex and OpenCode read AGENTS.md
directly; Claude Code reads it through the CLAUDE.md import).

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
| Claude Code | `CLAUDE.md` (auto-read; imports `AGENTS.md` at launch) |
| Codex CLI | `AGENTS.md` (auto-read on session start) |
| OpenCode | `AGENTS.md` (auto-read on session start) |
| Other agents (best-effort) | Paste `AGENTS.md` — it is self-contained |

---

## Evaluation Harness (recommended)

Not included — too project-specific to template. Worth building: a small set
of benchmark tasks with known expected outcomes. Run them when you update the
pack to catch regressions in agent behavior before they affect real work.

---

## Release Checklist

Before tagging a new pack version, verify:

- [ ] `ls protocols/` matches the AGENTS.md → Protocol Index exactly: every
      indexed file exists, no protocols/ file is missing from the index (both
      directions)
- [ ] Version string updated in ALL pack file headers — `grep -r "Starter Pack v"`
      over AGENTS.md, CLAUDE.md, TASK_TEMPLATE.md, SETUP.md, README.md,
      WALKTHROUGH.md, GUIDE.md, every `protocols/*.md`, and the agent/hook
      templates — all match
- [ ] If pack *behavior* changed: the human docs that describe it are updated —
      README "What You Get", WALKTHROUGH.md, GUIDE.md (they rot silently otherwise)

## Version

This is **Starter Pack v12.16**. The version is recorded in the header of
`AGENTS.md`, `CLAUDE.md`, and in every development log entry so there's
always an audit trail of which instruction set was active for any given
session.
