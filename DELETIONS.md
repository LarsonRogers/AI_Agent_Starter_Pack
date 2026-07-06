# DELETIONS.md — v13 merge deletion manifest (Phase 0 output)

> **Phase 0 gate: APPROVED 2026-07-06** with salvage resolution: the five flagged
> items all survive. Safety floor + Spike ratchet → `core/guardrails.md` (always-on);
> deploy data-sensitivity gate → `security-review` skill (always-on, loads on trigger);
> demo gate + RUNBOOK, S1–S4 sizing + growth triggers, accessibility baseline →
> deletable per-project blocks in `core/part2-template.md` behind a three-toggle
> "Project Options" onboarding block (defaults inferred from the brief, confirmed in
> one sentence, off = block deleted from the project's Part 2). `cross-cutting.md`
> deletion stands, with its "files NOT being touched" idea folded into BRIEFING
> guidance. All other dispositions stand as tabled.

Per marching-orders decision 6: nothing below is deleted until this manifest is
approved. Column meanings:

- **Basis** — `decided(N)` = already decided by marching-orders decision N
  (listed here for the record); `filter` = deletion-filter candidate ("would
  Opus 4.8 get this wrong without the file?") awaiting your call.
- **Salvage** — unique content worth folding into a surviving skill/file, if any.

## protocols/ — superseded by Fablized protocols (decided)

| File | Basis | Rationale | Salvage |
|---|---|---|---|
| protocols/stuck-loop.md | decided(2) | Fablized `stuck` supersedes (facts-vs-beliefs + attack-strongest-belief is strictly stronger than three-strikes narration) | The strike-3 escalation options (user context / Knowledge Gap / defer as watch item) — `stuck` §6's "specific question/decision needed" mostly covers; the Knowledge-Gap route reference is the only unique bit |
| protocols/task-workflow.md | decided(3) | Fablized `preflight` supersedes the Pre-Edit checklist | The checkpoint/rollback micro-procedure (clean tree before task; tests+log+handoff+commit after; `git reset --hard HEAD` on breakage) — not in preflight/landing; candidate for `session-continuity` |
| protocols/upgrade.md | decided(7) | Versioning machinery retires in favor of plugin packaging + git tags | The pack-owned vs project-owned file-ownership table is the only content of lasting value — could survive as a short README note for manual migrations |
| protocols/update-check.md | decided(7) | Same | None (mechanism-specific) |

## protocols/ — consolidated into the 4 new skills (decided(5); listed so the manifest is complete)

| File | Consolidates into | Salvage risk to watch |
|---|---|---|
| protocols/secure-coding.md | `security-review` | Carry the "where capable models actually miss" high-miss set (CSRF/sessions/authz/enumeration) verbatim-ish — it is validated content (A/B caught a real CSRF miss) |
| protocols/sensitive-data.md | `security-review` | Carry: scan-can-fail planted-secret test; "clean scan ≠ no privileged data" scope warning; permission-rules-are-not-a-boundary note |
| protocols/environment.md | `security-review` | Carry: no debug flags committed; new env vars documented; never log secrets/PII |
| protocols/safe-deletion.md | `destructive-ops` | Carry: untracked-file-with-no-backup rule (blanket overrides never relax it) |
| protocols/binary-files.md | `destructive-ops` | Carry: never text-read binaries; >1MB commit confirm; generated-output exception wording |
| protocols/model-tiering.md | `delegation` (rewritten per decision 5) | Carry: three-part Light gate (rubric / mechanically checkable / caught downstream); never-downgraded hard list; fail-safe = run Capable, never skip. The long per-harness switch mechanics compress hard — agent files (decision 9) replace most of it |
| protocols/session-start.md | `session-continuity` (slimmed) | Keep only: read HANDOFF + log tail → report where we left off → wait. Router ceremony dropped on purpose |
| protocols/log-format.md | `session-continuity` | Carry: DECISION_LOG entry format (append-only, deltas-only, specific identifiers) + HANDOFF overwrite format + regenerate-HANDOFF-from-log rule. CAPTAINS_LOG migration: drop (pre-v12 era) |

## protocols/ — deletion-filter candidates (your call at the Phase 0 gate)

| File | Basis | Rationale (would Opus 4.8 get this wrong without it?) | Salvage |
|---|---|---|---|
| protocols/communication.md | filter | Frontier models calibrate register to the user unprompted; audience-mode removal is explicitly the point (non-goal: don't restore) | Error-translation format for non-devs is genuinely good UX prose, but it's a behavior a strong model does when asked; suggest: none |
| protocols/testing-strategy.md | filter | Charter law 7 + landing §3 carry the load-bearing part (verify the verifier) | "Never mock the thing under test" + critical-path coverage floor are the two lines a mid model does get wrong; candidates for one line each in `security-review` (critical paths) or nowhere |
| protocols/code-quality.md | filter | Floor moved to charter (laws 8, 9, 11) | **Accessibility baseline checklist** (semantic elements, keyboard reachability, contrast) is real unique content nothing in Fablized covers — candidate for a compact block in `core/part2-template.md` or README; agent-isms table is redundant with law 9 |
| protocols/context-window.md | filter | Harnesses now manage context/compaction natively; LEAN profile was for ≤16k local models | Checkpoint-then-fresh-session advice → one line in `session-continuity` if anything |
| protocols/validation-fallback.md | filter | Landing §2 states the rule better ("Unverified — couldn't run X because Y; to verify, do Z") | None |
| protocols/external-research.md | filter | Law 1 (never call an API you haven't seen defined) + frontier web access cover the core | Two unique bits: (a) Knowledge-Gap 3-option flow incl. the "option 3 only when user selects it" guardrail linkage; (b) dependency hygiene (lockfile same-commit, audit, license check). (b) is a candidate for `security-review`; (a) for `guardrails.md` (one clause) |
| protocols/conflict-examples.md | filter | Worked examples of precedence; a strong model resolves precedence from the rules alone | None |
| protocols/edge-cases.md | filter | Mostly missing-file/version-mismatch machinery that decision 7 retires | Corrupt-log definition + "regenerate HANDOFF from log" → already carried into `session-continuity` via log-format salvage |
| protocols/pattern-registry.md | filter | Bounded Part 2 registry survives as a section of `core/part2-template.md`; the maintenance protocol around it is ceremony | The 40-line hard cap + template block → keep in part2-template itself |
| protocols/project-stakes.md | filter | Stakes-scaling is judgment a strong model applies; the pack's floor list is the part worth keeping | **Safety-floor list + Spike auto-ratchet triggers** (real data / auth / deploy / others rely on it) → strong candidate to fold into `core/guardrails.md` as ~6 lines |
| protocols/product-definition.md | filter | Idea→brief elicitation is native strong-model behavior | **S1–S4 sizing rungs + growth triggers** and the **Data & trust threat-model block** are the two validated bits (day-one architecture was 2/2 in A/B testing) — candidates for `part2-template.md` (sizing) and `security-review` (threat model) |
| protocols/inherited-codebase.md | filter | Read-before-touch is law 1; assessment shape is native behavior | Git-history reconstruction commands: nice, not load-bearing; sensitive-data scan-first ordering → one line in `security-review` |
| protocols/refactor.md | filter | Preflight's "behavior-preserving" class + law 7 carry the core (baseline first, prove equivalence) | "Tests must pass BEFORE refactoring begins" is the one line worth a mention in preflight-adjacent docs; suggest: none (preflight class covers) |
| protocols/requirements.md | filter | Pressure-testing vague asks is native; BRIEFING template externalizes the answers | The interrogation category list (assumptions/edges/failures/conflicts/hidden deps/concrete success) overlaps BRIEFING fields ~1:1; none |
| protocols/read-only.md | filter | Preflight class "investigation → findings with claim tags, no changes" is the same rule, stronger | "End with: no changes were made" closing line; none |
| protocols/placeholder-inference.md | filter | Part 2 template will carry its own fill-me markers; infer-present-confirm is native | The "user never edits pack files by hand" stance → one line in README |
| protocols/run-demo.md | filter | Landing covers agent-side verification — but NOT the user-facing demo gate | **RUNBOOK.md convention + "user has seen it run" demo gate** is the pack's most non-dev-protective unique content and nothing in Fablized replaces it. If any filter candidate deserves survival as salvage, it's this — candidate: compact block in `session-continuity` or `guardrails.md`. Flagging hard rather than quietly deleting |
| protocols/deployment.md | filter | Deploy mechanics are native; opt-in-only stance is a policy line | **Data-sensitivity gate (two signals, escalate-only, either can only HALT)** is a real safety mechanism — candidate for `security-review` (~8 lines). Teardown-with-verification pattern: nice-to-have |
| protocols/enforcement-tooling.md | filter | Hook layer (decision 8) mechanizes the deterministic part; gate setup is native | **"Verify every gate can fail"** (plant a violation, watch it fail) is verify-the-verifier applied to tooling — law 7 states the principle, but the tooling application is a good 3 lines for `security-review`; ratchet/baseline mode for inherited repos: one line there too |
| protocols/cross-cutting.md | filter | Not in the expected-deletions list, but not among the 8 skills either — flagging rather than assuming. Preflight §8 (scope fence) + BRIEFING cover intent | The pre-flight plan format (files touched/order/rollback/files-NOT-touched) is a decent delegation artifact — candidate: fold the "files NOT being touched" line into BRIEFING's Non-goals guidance; otherwise none |

## Root files not in the v13 target tree

| File | Basis | Rationale | Salvage |
|---|---|---|---|
| SETUP.md | filter | README rewrite (Phase 6) owns install-per-harness; plugin install replaces manual copying for Claude Code | Non-dev glossary + no-terminal path are well-made but serve the retired audience-mode layer; suggest a much shorter "non-developers" README section |
| GUIDE.md | filter | Concepts move to README (layers, how to edit doctrine) | The A/B evidence summary (CSRF catch, day-one architecture) is worth 3 lines in README as the "why" |
| WALKTHROUGH.md | filter | `doctrine/worked-examples.md` is the v13 equivalent (decision-point traces) | None beyond what README/evals carry |
| 12-11.zip | decided(7) | Committed zip snapshots deleted | None (snapshots exist in git history) |
| AI_Agent_Starter_Pack_12-8.zip | decided(7) | Same | None |
| .claude/hooks/check-pack-update.sh | decided(7) | Update-check machinery retires; plugin versioning replaces | Its stderr-guard/exit-0 hygiene style is the model for the new Phase 4 hooks (kept as reference until then) |
| TASK_TEMPLATE.md | decided(3) | Content merges into templates/BRIEFING.md | Port: task-type split (coding vs read-only acceptance criteria), Constraints ("do not modify / do not change"), Open questions, References — fields BRIEFING lacks |

## pack-dev/ — moves to `archive/pack-dev` branch (decided(7); not deleted, relocated)

| File | Action |
|---|---|
| pack-dev/DECISION_LOG.md, HANDOFF.md, README.md, ab-test-pack-value.md, known-limitations.md, star-subset-run-plan.md, validation-matrix.md | `git branch archive/pack-dev` before removal from `v13-merge`, so full history + tip remain reachable by name. Nothing lost, out of the distributed tree |

## Explicitly NOT deleted (for clarity)

- `.claude/settings.json`, `opencode.json`, `.codex/config.toml` — kept + extended (decision 8)
- `.claude/agents/*.example`, `.opencode/agent/*.example`, `.codex/agents/*.example` — become real agent files (decision 9)
- `.github/workflows/agent-ci.yml`, `.github/dependabot.yml` — kept (enforcement chassis; CI template is project-facing, not versioning machinery)
- `.gitignore`, `.gitattributes` — kept
- `protocols/review.md` — not deleted: rebuilt as the `reviewer` subagent consuming the landing report (decision 4)
- This file — deleted only after you approve and the deletions are executed (per marching orders)
