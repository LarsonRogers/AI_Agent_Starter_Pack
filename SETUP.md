# Setup Guide
<!-- Starter Pack v11.5 -->

No coding experience required. If you are a developer, skip to
Developer Quick Setup at the bottom.

---

> **Note:** This pack includes a `protocols/` folder containing 16 protocol
> files that the agent loads on demand. The entire folder must be present in
> your project for full operation — check the file list below.

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

**Git (strongly recommended — required for most agent features).** Git saves
checkpoints of your code so mistakes can be undone. The agent handles git
for you — you just need it installed. Download at https://git-scm.com

Without git: the agent can still read, analyze, and answer questions about
your code. But it cannot make safe commits, roll back mistakes, reconstruct
history, or run the full checkpoint and refactor workflows. If you're doing
any active coding work, install git first.

To verify git is installed: open a terminal and type `git --version`.
If you see a version number, you're good. If not, download from the link above.

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
├── PROTOCOLS.md
├── protocols/
│   ├── refactor.md
│   ├── inherited-codebase.md
│   ├── placeholder-inference.md
│   └── ... (16 protocol files total)
├── SETUP.md
├── TASK_TEMPLATE.md
├── README.md
├── CAPTAINS_LOG.md        ← created by agent on first session
├── CHANGELOG.md           ← created by agent after first commit
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

> **Not comfortable with the terminal or command line?**
> You don't need to be. Skip to **[Generic Agent Path](#generic-agent-path-no-cli-required)**
> further down this page — it uses only copy-paste in your browser or IDE.
> The steps below are for developers using Claude Code or Codex CLI.

### Step 2 — Start your agent session

Open a terminal in your project folder and start your agent:
- Claude Code: type `claude` and press Enter
- Codex: type `codex` and press Enter
- Others: follow their startup instructions, then point them to `ARCHITECTURE.md`

**That's it.** The agent takes it from here. No manual editing of pack
placeholders required — the agent infers your project details, presents them
for confirmation, and fills everything in itself.

*Optional advanced config (developers only):* `.claude/settings.json` and
`.github/workflows/agent-ci.yml` can be manually adapted to your stack after
the first session, but are not required for normal use.

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

## What a good first session looks like

Here is a concrete example of what the agent should say and do in a
compliant first session on a new project. If yours looks different,
see "If something goes wrong" below.

---

**You start the session. The agent responds first — unprompted:**

> "Quick question before we start — are you a developer or engineer, or
> are you coming at this from a different angle? There's no wrong answer,
> it just helps me calibrate how much I explain."

**You say:** "Non-developer, first time using this."

**Agent responds:**

> "Got it — I'll explain everything in plain English and walk you through
> each step before doing anything. I've recorded that for future sessions
> so you won't be asked again.
>
> Now let me scan the project to understand what we're working with...
>
> Here's what I found:
> - This appears to be a new project — only starter pack files present
> - No prior work logged
>
> Based on the repo name and any files I can see, here's what I've inferred:
>
> Project name: [inferred name]
> Language/runtime: [inferred or 'I couldn't determine this — what are you building with?']
> Lint command: [inferred or 'not configured yet']
> Test command: [inferred or 'not configured yet']
>
> Say 'confirmed' to accept these, or tell me what to change."

**You say:** "Confirmed."

**Agent responds:**

> "Done — I've filled those in. I've also created a Captain's Log to track
> our work across sessions.
>
> What would you like to work on first? Describe it in plain English and
> I'll make sure I understand it correctly before starting."

---

---

**✓ Normal path — agent is compliant if it:**
- Asks one or two questions about your background before doing anything
- Scans the repo and reports what it found
- Presents inferred project details for confirmation before filling them in
- Creates a Captain's Log entry
- Waits for your go-ahead before writing any code

---

**✗ Recovery path — agent is non-compliant if it:**
- Starts writing or editing code immediately without asking questions
- Never presents inferred project details for confirmation
- Doesn't create a Captain's Log entry
- Asks you to manually edit any of the pack files

**If any of these happen**, paste this into the chat to reset:
```
Stop. Read AGENTS.md and follow the session start protocol from the
beginning. Do not write any code until the protocol is complete.
```

---

## If something goes wrong

**"The agent says there are unfilled placeholders"**
This shouldn't happen — the agent fills these in automatically. If it does,
tell it: *"Run the Placeholder Inference Protocol and present your inferred
values for my confirmation."*

**"The agent says it can't find a protocol file"**
The `protocols/` folder and `PROTOCOLS.md` are both required. Check that
the entire `protocols/` folder was copied into your project root. If files
are missing, copy them from the original zip. Without the protocols folder,
several key agent behaviors are unavailable and the agent will halt rather
than guess.

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
Before doing anything else, read AGENTS.md at the repo root and follow
the session start protocol exactly as written. Do not write any code
or make any changes until the protocol is complete.
```

That's it. The agent takes over from there — same protocols, same behavior,
regardless of platform. `AGENTS.md` is the bootstrap entry point for all
agents — it will direct the agent to read the other files in the right order.

**If your agent can't read files directly**, paste the contents of
`AGENTS.md` into the chat manually. It's a short file — open it in any
text editor, select all, and paste. The agent will then ask you for
`ARCHITECTURE.md` and `CLAUDE.md` if it needs them.

---

## Appendix: Glossary for Non-Developers

Terms the pack uses that may be unfamiliar:

**CLI (Command Line Interface)** — A text-based way to interact with your
computer by typing commands into a terminal window. Many developer tools are
CLI-only. If this is unfamiliar, use the Generic Agent Path instead — it
requires no CLI.

**Git** — A tool that saves snapshots of your code over time, like a detailed
undo history. Each snapshot is called a "commit." If something breaks, you
can roll back to any previous snapshot. The agent handles git for you.

**Repo (repository)** — Your project folder when it's being tracked by git.
"The repo root" means the top-level folder of your project.

**Terminal** — A text-based window where you type commands. Also called
"command line," "command prompt," or "shell." The agent runs inside it.

**Dotfiles / hidden folders** — Files and folders whose names start with a dot
(`.claude/`, `.codex/`). They're hidden by default in most file browsers.
See the appendix below for how to show them.

**CI (Continuous Integration)** — An automated system that runs tests every
time code is saved, usually on a service like GitHub Actions. Optional for
most projects. The pack includes a CI template but you don't need to use it.

**Lint / linter** — A tool that automatically checks code for common mistakes,
style inconsistencies, and potential bugs — like spell-check for code.

**Type check** — A tool that verifies variables and functions are used
correctly according to their declared types. Only relevant for some languages
(TypeScript, Python with type hints). The agent will tell you if it applies.

**Tests / test suite** — Code that automatically verifies your project behaves
correctly. The agent runs these after every change to make sure nothing broke.

**Lockfile** — A file (like `package-lock.json` or `poetry.lock`) that records
the exact versions of all installed packages. Auto-generated — never edit it.

**Allow list** — A list of commands the agent is permitted to run automatically
without asking. Configured in `.claude/settings.json`. Comes pre-set with
safe defaults; you don't need to change it.

**Stack** — The combination of programming languages, frameworks, and tools
used to build a project. "What's your stack?" means "what technology are
you using?"

**Dependency / package** — A piece of software your project relies on, written
by someone else. Installing a dependency means adding it to your project.
The agent will always ask before adding new ones.

---

## Appendix: Opening a Terminal in Your Project Folder

If "open a terminal in your project folder" is unfamiliar, here's exactly
how to do it on each platform.

**Mac**
1. Open Finder and navigate to your project folder
2. Right-click (or Control-click) the folder
3. Select "New Terminal at Folder"
   — If you don't see this option: go to System Settings → Privacy & Security
     → Developer Tools, or open Terminal from Applications → Utilities,
     then type `cd ` (with a space), drag your project folder into the Terminal
     window, and press Enter

**Windows**
1. Open File Explorer and navigate to your project folder
2. Click in the address bar at the top (where the folder path is shown)
3. Type `cmd` and press Enter — a terminal opens in that folder
   — Alternatively: hold Shift and right-click the folder, select
     "Open PowerShell window here" or "Open command window here"

**Linux**
1. Open your file manager and navigate to your project folder
2. Right-click the folder and select "Open Terminal Here"
   — On Ubuntu/GNOME: this option appears directly in the right-click menu
   — On other distros: if not available, open Terminal from your applications
     menu, then type `cd ` (with a space), drag the folder into the terminal
     window, and press Enter
   — Alternatively from any terminal: `cd /path/to/your/project`

**Verifying hidden files were copied correctly**
After copying the pack files, check that the hidden folders are present:
- Mac: press Cmd+Shift+Period in Finder to show hidden files.
  You should see `.claude`, `.codex`, and `.github` folders.
- Windows: in File Explorer, click View → Show → Hidden items.
  You should see the same three folders.
- Linux: hidden folders start with `.` — run `ls -la` in your terminal
  to see them, or enable "Show Hidden Files" in your file manager (usually
  Ctrl+H).

If any are missing, copy them from the zip again — they're required for
Claude Code and Codex to pick up their settings automatically.

**Verifying all protocol files are present**
Run this in your project folder to confirm the full protocols/ directory
copied correctly:

**Mac / Linux (terminal):**
```bash
ls protocols/ | wc -l
```
You should see `16`.

**Windows (Command Prompt):**
```cmd
dir /b protocols
```
Count the lines in the output — you should see 16 files listed.

**No terminal? Use your file explorer instead:**
Open your project folder, then open the `protocols` subfolder.
Count the files inside — there should be exactly 16.
If there are fewer, copy the `protocols/` folder from the zip again. If the number is lower, copy the protocols/ folder
from the zip again. A missing protocol file won't cause an immediate error
but will cause the agent to halt when that protocol is triggered.

**Verifying setup worked**
When you start your first agent session, the agent should:
1. Greet you and ask two quick questions about your background
2. Scan the repo and report what it found
3. Present inferred project details for your confirmation
4. Wait for your go-ahead before doing anything

If the agent starts writing code immediately without any of the above,
paste this into the chat:
```
Stop. Read AGENTS.md and follow the session start protocol before doing
anything else.
```

---

## Developer Quick Setup

1. Copy all files into repo root (preserve `.claude/`, `.codex/`, `.github/`)
2. Start your agent — it handles placeholder inference and fills in
   `CLAUDE.md` and `AGENTS.md` from repo context
3. Enable web search in your agent's settings for best results
4. Adapt `.github/workflows/agent-ci.yml` to your stack
5. Add project-specific lint/test commands to `.claude/settings.json` allow list
