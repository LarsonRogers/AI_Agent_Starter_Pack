<!-- Starter Pack v11.51 — protocols/log-format.md -->
<!-- Load this file when: writing, reconstructing, or formatting a development log
     entry or changelog entry (every committed task, checkpoints, handoffs,
     inherited-codebase reconstruction). -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->

## Captain's Log — Entry Format & Maintenance

The file `CAPTAINS_LOG.md` at the repo root is a running development log,
newest entry first. It exists so any new agent session — or human developer —
can orient quickly and continue without re-reading the full codebase. It is
the universal handoff artifact: a session started in Claude Code can be handed
to Codex or any other agent — the log provides full context without requiring
access to chat history.

### When to update

- After every committed task, as the final step before moving to the next prompt
  (part of the Definition of Done — a task is not complete until the log is updated)
- At the start of a new session if the previous session ended without an update
- When explicitly asked
- When inheriting an existing codebase — reconstruct from git history first,
  then prepend a live assessment entry (see protocols/inherited-codebase.md)

### How to update

- Prepend the new entry above the most recent existing entry (newest-first order)
- Do not summarize the entire codebase history — only what changed since the last entry
- Pull from: actual files changed, functions added or modified, decisions made,
  commands or routes registered, schema changes, and current-session context
- Be specific — reference actual function names, file paths, and identifiers
  rather than describing things generically

### Entry format

Entries must be specific enough that a cold agent on a different platform can
read the log and continue work without accessing any chat history.

```markdown
## [Sprint or Task Name] — [YYYY-MM-DD]

**Agent/Platform:** [e.g., Claude Code, Codex — for audit trail]
**Audience mode:** [Developer / Technical non-dev / Non-dev — only required in
first entry, persists across sessions until user requests a change]
**Pack version:** [e.g., v11.51 — from the header of ARCHITECTURE.md]

**Handoff prompt for next session:**
```
Read the instruction files per the session start protocol, then
CAPTAINS_LOG.md (most recent entry only).

Most recent session: [date]
Last completed task: [task name]
Confirmed next task: [next task, or "ask the user"]
Audience mode: [Developer / Technical non-dev / Non-dev]
Pack version: [version]

Run the Session Resumption Protocol and report status before proceeding.
```

**What was built / changed:**
- `[path/to/file.ext]` — [what changed and why, specific function or feature names]

**Architectural decisions:**
- [Decision made] — WHY: [rationale. This is the trail for the next agent and human team]

**Codebase state:**
- Working: [what is fully functional]
- Wired up but incomplete: [what exists but is stubbed, partial, or untested]
- Not started: [what is planned but not yet touched]

**Relevant files:**
- `[path/to/file.ext]` — [what this file is and its current state]

**Watch items for next session:**
- [Specific loose end, deferred decision, or known issue with enough detail to act on]

---
```

The `---` separator is required between entries. Newest entry is always at the top.

### Reading the log

Read the most recent entry only, after the instruction files, so standing
rules are loaded when interpreting watch items and the handoff prompt. If
earlier entries contain unresolved watch items referenced in the most recent
entry, load those specific earlier entries to resolve context.

---

## Changelog

Append an entry to `CHANGELOG.md` (create it if it does not exist) after every
committed task. Format:

```markdown
## [date] — [one-line summary of what changed]
- What was added / changed / removed
- Why (the reason or requirement behind the change)
- Any decisions made and the rationale
- Any known limitations or follow-up work flagged
```

This log is the paper trail for the human team. It must be kept current.

---
