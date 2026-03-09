# Setup Guide

This guide walks you through getting started — no coding experience required.
If you are a developer, skip to the Developer Quick Setup at the bottom.

---

## What is this?

This starter pack is a set of instruction files you drop into a code project.
Once in place, any AI coding agent — Claude, Codex, Cursor, and others — will
read these files and know how to work on your project safely and consistently.

Think of it as a rulebook the AI reads before touching anything. It tells the
agent how to communicate with you, how to save its work, what it is and is not
allowed to do on its own, and how to hand off to another agent or a human
developer when needed.

---

## What you need before starting

**An AI coding agent.** This pack works with:
- **Claude Code** — Anthropic's coding agent. Install it by running
  `npm install -g @anthropic-ai/claude-code` in a terminal, or follow the
  setup guide at https://docs.anthropic.com/claude-code
- **Codex CLI** — OpenAI's coding agent. Install it by running
  `npm install -g @openai/codex` in a terminal, or follow the setup guide
  at https://platform.openai.com/docs/codex
- **Cursor, Windsurf, or others** — follow their own installation guides,
  then point them to `ARCHITECTURE.md` and `CLAUDE.md` when starting a session

**A code project.** This can be:
- A new empty folder where you want to build something
- An existing project on your computer
- A project you've downloaded or cloned from the internet

**Git (optional but recommended).** Git is a tool that saves checkpoints of
your code so you can undo mistakes. The AI agent can explain and handle this
for you if you're not familiar with it. To install git, visit https://git-scm.com

---

## Setup steps

### Step 1 — Copy the starter pack into your project

Copy all the files and folders from this starter pack into the root folder
of your project (the top-level folder, not inside any subfolder).

Your project folder should now contain:
```
your-project/
├── ARCHITECTURE.md
├── AGENTS.md
├── CLAUDE.md
├── SETUP.md               ← this file
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

Note: files and folders starting with `.` may be hidden by default on Mac and
Windows. That's fine — the agent can still read them.

### Step 2 — Fill in your project name

Open `CLAUDE.md` and `AGENTS.md` in any text editor (Notepad, TextEdit, or
VS Code all work). Find every place that says `[PROJECT_NAME]` and replace it
with the name of your project.

That's the only change you need to make manually. The agent will fill in
everything else during your first session.

### Step 3 — Enable web search for your agent (recommended)

The agent uses web search to look up documentation and coding references
before writing code. This makes its output significantly more accurate,
especially for niche tools and libraries.

- **Claude Code:** web search is already enabled in the included settings file
- **Codex:** log into your OpenAI account at https://platform.openai.com,
  go to Settings, and enable web browsing/search if available
- **Cursor / Windsurf:** check their settings panel for a web search toggle

### Step 4 — Start your agent session

Open a terminal in your project folder and start your agent:
- Claude Code: type `claude` and press Enter
- Codex: type `codex` and press Enter
- Others: follow their startup instructions and point them to `ARCHITECTURE.md`

The agent will take it from here. It will:
1. Ask whether you are a developer or new to coding
2. Look at what's in your project
3. Tell you what it found in plain English
4. Ask you what you want to do before touching anything

---

## What to expect in your first session

The agent will ask a quick question or two before doing anything — just to
understand how much context and explanation is useful to you. There are three
modes it can work in:

- **Developer** — technical language, minimal explanation of standard operations
- **Technical non-dev** — plain English by default, technical terms used when
  they're the clearest option with a brief explanation, no over-simplification.
  Good for people who understand concepts but don't code regularly.
- **Non-dev** — everything explained in plain English, every action described
  before it happens, maximum guardrails

Answer honestly — the agent will pick the right mode and record it so it never
asks again. You can always say "explain less" or "you can be more technical" to
adjust mid-project, and it will adapt.

After that, the agent will look through your project, tell you what it found,
and wait for you to tell it what you want to work on.

From there, every task works like this:
1. You describe what you want in plain language
2. The agent reflects back what it understood and asks you to confirm
3. You say yes (or correct it)
4. The agent does the work, saving checkpoints along the way
5. The agent tells you what it did in plain English and what's next

---

## If something goes wrong

The agent is designed to explain failures in plain English and give you clear
options. You should never see a confusing technical error without an explanation
of what it means and what to do about it.

If the agent seems confused or stuck:
- Ask it to "summarize where we are and what the current task is"
- Ask it to "check the captain's log and tell me where we left off"
- If all else fails, start a new session — the agent will read the captain's
  log and resume from where things were last stable

---

## Developer Quick Setup

1. Copy all files into repo root
2. Replace `[PROJECT_NAME]` in `CLAUDE.md` and `AGENTS.md`
3. Fill in Tech Stack table, Validation Commands, File Structure, and Code
   Style in `CLAUDE.md`
4. Fill in Project-Specific Architecture and Pattern Registry in `ARCHITECTURE.md`
5. Add lint/test commands to the `allow` list in `.claude/settings.json`
6. Adapt `.github/workflows/agent-ci.yml` to your stack
7. Enable web search in your agent's settings
8. Run your agent from the repo root — it handles the rest
