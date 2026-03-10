<!-- Starter Pack v11.3 — protocols/read-only.md -->
<!-- Load this file when: review, audit, analysis, or any task with no intended edits -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->

## Read-Only / Meta-Review Protocol

Use this protocol when the task is analysis, review, audit, or documentation
only — no code changes, no commits, no Definition of Done workflow.

### When this applies

```
- Code review or audit request
- Architecture assessment
- Documentation review
- Security or dependency scan
- "Tell me what this does" / "What's wrong with this?"
- Any task where the user explicitly says no changes should be made
```

### Trigger recognition

If a task brief contains any of the following signals, default to this
protocol unless the user explicitly requests edits:

```
"review", "audit", "assess", "analyze", "explain", "summarize",
"what does this do", "what's wrong", "check this", "look at this",
"read-only", "no changes", "don't touch anything"
```

### Protocol

```
[ ] 1. Confirm read-only mode with the user before starting:
        "I'll treat this as a read-only review — no edits or commits.
        Confirm, or let me know if you'd like me to make changes too."
[ ] 2. Read the relevant files — do not stage, modify, or create any file
[ ] 3. Produce the requested analysis, review, or report
[ ] 4. Deliver findings in the format appropriate to audience mode:
        - Developer: prioritized list, concise, specific file/line references
        - Technical non-dev: plain English with technical detail where useful
        - Non-dev: plain English, options and recommendations, no jargon
[ ] 5. End with a clear prompt:
        "No changes were made. Want me to act on any of these findings?"
[ ] 6. Do NOT update CAPTAINS_LOG.md unless the user asks
[ ] 7. Do NOT run lint, tests, or commit checks
```

### Suspended in read-only mode

Pre-edit protocol, task brief / scope contract, Definition of Done checklist,
checkpoint / rollback strategy, Captain's Log update (unless requested).

### Still active in read-only mode

Audience mode communication, sensitive data handling (never reproduce
credentials or PII), honest verification language, hard guardrails.

---

### Inherited Codebase (Existing project, no prior log)

When the task is read-only and no Captain's Log exists, skip the full
Inherited Codebase Protocol onboarding flow. Instead:

```
[ ] 1. Read available source files to understand the codebase at a surface level
[ ] 2. Deliver your analysis or review findings
[ ] 3. End with: "No changes were made. Want me to act on any of these findings?"
[ ] 4. If the user confirms they want work done, exit read-only mode and
       run the Inherited Codebase Protocol (protocols/inherited-codebase.md)
       before touching any files.
```

Do not fill placeholders, do not create CAPTAINS_LOG.md, do not run
audience detection until the user confirms active work is needed.