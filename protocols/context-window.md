<!-- Starter Pack v11.7 — protocols/context-window.md -->
<!-- Load this file when: 5+ tasks in session or detected context degradation -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->

### Context Window Management

Long sessions accumulate context until the agent begins losing track of earlier
instructions, decisions, and constraints. This degrades output quality silently
— the agent won't announce it's forgetting things.

### Proactive checkpointing

The agent must monitor session length and trigger a checkpoint when:
- More than 5 tasks have been completed in the current session, OR
- The session has been running long and the agent notices it is losing
  track of earlier context, OR
- The user reports the agent seems confused or inconsistent

### Checkpoint procedure

When a checkpoint is triggered:
```
[ ] 1. Complete the current task fully (do not checkpoint mid-task)
[ ] 2. Run the full Definition of Done checklist
[ ] 3. Update CAPTAINS_LOG.md with a session summary entry including:
        - All tasks completed this session
        - Current codebase state
        - Confirmed next task
        - Handoff prompt for next session
[ ] 4. Notify the user:
        "This session is getting long and I want to make sure nothing gets
        lost. I've saved a full checkpoint — [summary of what was done].
        I'd recommend starting a fresh session for the next task to keep
        things sharp. The Captain's Log has everything needed to resume."
[ ] 5. Do not start any new tasks after the checkpoint notification
```

The user may choose to continue anyway — that is their call. The agent
notes the choice in the log and continues with reduced confidence warnings
if it detects context degradation.

---


---
