<!-- Starter Pack v11.47 — protocols/placeholder-inference.md -->
<!-- Load this file when: first session on any project type — fills REQUIRED placeholders -->
<!-- Does NOT trigger when: a read-only meta-review is active (placeholder inference
     stays suspended until the review is complete and normal session-start resumes). -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->

### Placeholder Inference Protocol

The user never manually edits starter pack files. All placeholder substitution
is handled by the agent on first session.

**Required placeholders** — marked `⚠️ REQUIRED PLACEHOLDER` in CLAUDE.md.
The agent must resolve all of these before any coding task begins:
```
[PROJECT_NAME]        — infer from repo name, existing README, or package.json/pyproject.toml
[Tech Stack table]    — infer from files present: package.json, requirements.txt,
                        Cargo.toml, go.mod, etc.
[Validation Commands] — infer from package.json scripts, Makefile, or common
                        conventions for the detected stack. If genuinely unavailable,
                        mark with: # NOT CONFIGURED
[File Structure]      — infer from actual repo layout
```

**Deferred placeholders** — marked `DEFERRED` in CLAUDE.md. These are intentional
scaffolding filled as the project develops. The agent never halts on these:
```
[License]          — filled when known
[Task Prompts]     — filled by developer as work is planned
[Related Projects] — filled if/when relevant
[Pattern Name]     — Pattern Registry entries, filled as patterns emerge
[Key Invariants]   — filled as architecture solidifies
```

**The inference flow:**
```
[ ] 1. Scan all pack files for [BRACKETED] placeholders
[ ] 2. Categorize each as Required or Deferred (see above)
[ ] 3. For each Required placeholder, infer the most likely value from
        the repo contents, file names, and any existing documentation
[ ] 4. Present inferred values to the user in a single confirmation block:

        "Here's what I've inferred for this project — confirm or edit
        any of these before I fill them in:"

        Project name:      [inferred value]
        Language/runtime:  [inferred value]
        Lint command:      [inferred value]
        Test command:      [inferred value]
        [etc.]

        Say "confirmed" to accept all, or tell me which to change.

[ ] 5. Write confirmed values into CLAUDE.md and AGENTS.md
[ ] 6. Note any Required placeholders that could not be inferred — ask
        the user directly for those only
[ ] 7. Proceed — do not halt on Deferred placeholders
```

The user's only responsibility is confirming or editing the presented values.
No manual file editing required.

---


---
