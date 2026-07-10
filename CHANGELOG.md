# Changelog

## 13.1.0-dev

- Add adaptive reasoning depth, alternative generation, discriminating tests, and explicit
  disconfirmation without requesting private chain-of-thought.
- Add installed-skill awareness and approval-gated recommendations for useful missing skills.
- Replace ceremony-first manual evals with an automated, provider-neutral A/B runner and
  behavioral graders.
- Make eval artifacts portable across Windows model IDs, recognize common provider edit-tool
  names, and exclude runtime caches from disposable fixtures.
- Replace the large micro prompt with a 358-word named operating loop and an 800-word gate.
- Add cross-platform Python landing, pre-commit, local-tier transport, and canary tools.
- Parse local-tier config as inert data, enforce explicit loopback, and keep secrets and
  briefing payloads out of command arguments and proxies.
- Change harness defaults to ask-first/network-off and add reproducible pack CI.
- Add a synchronized version source, MIT license, migration notes, and repository validator.
- Add task-class micro slices (bugfix / investigation / landing, ≤400 words each) with
  literal output skeletons, dispatched by `delegate.py --task-class` — a 7B holds one task
  shape, not the whole doctrine (evals 2026-07-10).
- Verify light-tier results fail-closed in `delegate.py`: fabricated run-claims a single-shot
  completion cannot back, missing per-class deliverables, and untagged output are rejected
  (exit 5, metrics status `rejected`); refutation-quotes are exempt.
- Record the light tier's measured scope in Part 2 (bugfix slices + rubric scans only) and
  the class-scoped dispatch rule in the delegation protocol.
