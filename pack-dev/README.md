# pack-dev/ — pack development artifacts. DO NOT COPY INTO PROJECTS.

Everything in this directory is meta-material for developing the starter pack
itself. It is excluded wholesale from distribution: when copying the pack into
a project, copy everything EXCEPT this directory. The boundary is the
directory, not a file list — new pack-dev artifacts go here and are excluded
automatically.

Contents:

- `known-limitations.md` — intentional tradeoffs and deferred decisions,
  consulted when auditing the pack itself. Never needed during project work.
- `DECISION_LOG.md` — the pack's own development log (append-only).
- `HANDOFF.md` — the pack's own development handoff (overwritten per task).
- `ab-test-pack-value.md` — the A/B test methodology + recorded results: does
  the pack make a measurable difference vs. no pack. Maintainer reference; never
  linked from the distributed `README.md` (this directory doesn't ship, so the
  link would die downstream).

Deployed projects create their OWN fresh `DECISION_LOG.md` and `HANDOFF.md`
at the project root on first session (see `protocols/log-format.md`) — those
are runtime artifacts of each project, unrelated to the files here.

## Keeping the pack's human docs current (same-commit rule)

The pack's human-facing docs — `README.md` ("What You Get" + Files), `GUIDE.md`,
`WALKTHROUGH.md`, `SETUP.md` — describe what the pack does, and rot silently when
behavior changes but the docs don't (the README "What You Get" list once fell
~11 versions behind before it was caught).

**Rule: a commit that adds or changes a user-facing capability updates the human
docs that describe it, in the same commit** — the same discipline the pack itself
applies to `RUNBOOK.md` (kept current in the commit that changes the run steps).
The `README.md` release-checklist item is the backstop; this same-commit rule is
the primary defense.

This governs developing the pack *here*. It does NOT make agents rewrite a
*deployed project's* README — that stays project-owned (see
`protocols/upgrade.md`); RUNBOOK + the demo gate cover the agent-appropriate part.
