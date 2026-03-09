# Setup Guide
<!-- Starter Pack v10.4 -->

No coding experience required. If you are a developer, skip to
Developer Quick Setup at the bottom.

---

## What is this?

A set of instruction files you drop into a code project. Once in place,
any AI coding agent — Claude, Codex, Cursor, and others — reads these files
and knows how to work on your project safely and consistently.

Think of it as a rulebook the agent reads before touching anything. It tells
the agent how to talk to you, how to save its work, what it is and isn't
allowed to do on its own, and how to hand off to another agent or a human
developer when needed.

---

## What you need

**An AI coding agent.** This pack works with:
- **Claude Code** — install via `npm install -g @anthropic-ai/claude-code`
  or follow the guide at https://docs.anthropic.com/claude-code
- **Codex CLI** — install via `npm install -g @openai/codex`
  or follow the guide at https://platform.openai.com/docs/codex
- **Cursor, Windsurf, or others** — follow their own installation guides

**A code project.** This can be a new empty folder, an existing project,
or a project you've downloaded from the internet.

**Git (recommended).** Git saves checkpoints of your code so mistakes can
be undone. The agent handles git for you — you just need it installed.
Download at https://git-scm.com

---

## Setup — two steps

### Step 1 — Copy the starter pack files into your project folder

Copy everything from this pack into the root of your project (the top-level
folder, not inside any subfolder). Your project should now contain:

```
your-project/
├── ARCHITECTURE.md
├── AGENTS.md
├── CLAUDE.md
├── SETUP.md
├── TASK_TEMPLATE.md
├── README.md
├── .claude/
│   └── settings.json
├── .codex/
│   └── config.toml
└── .github/
    └── workflows/
        └── agent-ci.yml
```

Note: files and folders starting with `.` may be hidden by default.
On Mac: press Cmd+Shift+Period to show hidden files.
On Windows: View → Show → Hidden items.

### Step 2 — Start your agent session

Open a terminal in your project folder and start your agent:
- Claude Code: type `claude` and press Enter
- Codex: type `codex` and press Enter
- Others: follow their startup instructions, then point them to `ARCHITECTURE.md`

**That's it.** The agent takes it from here. You don't need to edit any files
manually — the agent will figure out your project details, present them to you
for confirmation, and fill everything in itself.

---

## What happens in your first session

**1. The agent asks who you are**
Two quick questions to understand how much explanation is useful to you.
Answer honestly — it adjusts how it communicates, not what it can do.
Three modes: Developer, Technical non-dev, Non-dev. It records your answer
and never asks again.

**2. The agent figures out your project**
It scans the repo, infers your project name, tech stack, and other details,
then presents them to you:

> *"Here's what I've inferred for this project — confirm or edit any of
> these before I fill them in: Project name: [X], Language: [Y]..."*

Say "confirmed" to accept, or tell it what to change. No file editing needed.

**3. The agent reports what it found**
If you have an existing codebase, it maps the structure, identifies any
problem areas, and tells you what it found before touching anything.

**4. You tell it what to work on**
Describe what you want in plain language. The agent will reflect back what
it understood and ask you to confirm before starting. From there, it works,
saves checkpoints, and reports back in plain English after each task.

---

## If something goes wrong

**"The agent says there are unfilled placeholders"**
This shouldn't happen — the agent fills these in automatically. If it does,
tell it: *"Run the Placeholder Inference Protocol and present your inferred
values for my confirmation."*

**"The agent seems confused or has lost track"**
Tell it: *"Check the Captain's Log and tell me where we left off."*
Or start a fresh session — it will resume from the log automatically.

**"I want to switch to a different agent"**
Start a new session with the new agent and say:
*"Read AGENTS.md and follow the session start protocol."*
The Captain's Log has everything needed to continue.

**"The agent is asking me to run commands I don't understand"**
Ask it: *"Explain what that command does in plain English before I run it."*
The agent should never ask you to run something without explaining it first.

---

## Generic Agent Path (no CLI required)

If you're using a web-based or IDE agent — Cursor, Windsurf, ChatGPT web,
Gemini, or any agent without automatic file reading — follow this path
instead of the CLI instructions above.

**Step 1 — Copy the pack files into your project** (same as the main setup)

**Step 2 — Open your agent and paste this starter prompt:**

```
Before doing anything else, read these files from my project in this order:
1. ARCHITECTURE.md
2. CLAUDE.md
3. CAPTAINS_LOG.md (most recent entry only, if it exists)

Then follow the session start protocol in ARCHITECTURE.md exactly.
Do not write any code or make any changes until the protocol is complete.
```

That's it. The agent takes over from there — same protocols, same behavior,
regardless of platform.

**If your agent can't read files directly**, paste the contents of
`ARCHITECTURE.md` and `CLAUDE.md` into the chat manually. They're plain
text files — you can open them in any text editor, select all, and paste.

---

## Developer Quick Setup

1. Copy all files into repo root (preserve `.claude/`, `.codex/`, `.github/`)
2. Start your agent — it handles placeholder inference and fills in
   `CLAUDE.md` and `AGENTS.md` from repo context
3. Enable web search in your agent's settings for best results
4. Adapt `.github/workflows/agent-ci.yml` to your stack
5. Add project-specific lint/test commands to `.claude/settings.json` allow list
