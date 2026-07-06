---
name: delegation
title: Delegation
description: Run before handing any sub-task to another model or agent — spawning a subagent, routing work to a cheaper model, splitting work across tiers, or requesting an independent review. Picks the tier (deterministic / light / capable), builds the briefing, and fixes the return format. Also governs tier setup for hybrid local+API and fully-offline environments.
---

# Delegation

Delegation fails two ways: sending judgment work to a model that cannot carry it, and
sending any work without the context its executor cannot reconstruct. This protocol
closes both — pick the tier by rule, then brief with the template, then require
results in a form you can audit.

## 1. Pick the tier

- **DETERMINISTIC** — a script or command settles it (file-exists, version grep,
  pattern scan, parse check). Never spawn an agent for what a command answers.
- **LIGHT** — allowed only when ALL three hold:
  (a) an explicit rubric or checklist governs the task — the sub-agent applies stated
  rules, forms no opinion; (b) the output is mechanically checkable — a list, a yes/no
  per item, a diff; (c) a wrong answer is caught downstream by a capable-tier check or
  a deterministic gate before it can cause harm.
- **CAPABLE** — everything with judgment or safety weight: independent review,
  security assessment, conflict resolution, architecture conformance, anything a
  guardrail depends on. **Never downgraded.** Any (a)–(c) failure → capable. Unsure →
  capable: an over-strong model costs money; an under-strong watchdog misses defects.

Fail-safe: no light model configured, or no way to route to it → run the task on the
capable tier. Tiering lowers cost, never coverage.

## 2. Tier maps (recorded in Part 2)

- **Standard:** session/API model as capable; a cheaper API model as light.
- **Hybrid (local + API):** the local model is the light tier; any permitted API model
  is the capable tier and the reviewer. This is the inversion to notice: when the
  main loop runs on a small local model, review and safety work go UP to the API
  model, not to another local instance.
- **Fully offline (single-tier):** everything runs on the one model. The reviewer
  role degrades to deterministic gates — `tools/land.sh` plus the diff-connect
  checklist below — instead of open-ended judgment review. A machine-checked landing
  beats a self-review by the author model.

For a local GPU endpoint, dispatch through `tools/delegate.sh` (health check, single-
flight lock, timeout, metrics) — never raw calls. Three rules specific to that setup:

- **Sensitivity routing.** Material marked privileged/local-only is handled in fully
  local single-tier sessions. The frontier orchestrator neither composes nor reads
  briefings for such tasks — routing the payload locally does not protect content the
  orchestrator itself wrote.
- **Failure policy.** Endpoint down or timed out → report it claim-tagged
  (`[OBSERVED] local tier unreachable: <check output>`), then queue or escalate to
  the capable tier per the briefing's Budget & escalation line. At most one retry,
  and only after a fresh health check passes. Never silent retry-loops.
- **Concurrency.** The orchestrator queues heavy tasks; it never fans out parallel
  heavy work to a single-GPU endpoint (one heavy task, or two light tasks sharing
  the KV budget).

## 3. Brief with `templates/BRIEFING.md`

One goal per briefing. Fill every field — anything left blank, the executor fills
with a guess. Paste evidence, not conclusions (actual error text, actual log lines);
mark anything unverified "must verify" so it is not swallowed as a premise. If the
sub-task is investigation, say the deliverable is findings with claim tags, no code
changes.

## 4. Require results in landing format

The deliverable comes back structured as a landing report: outcome first, verified
(with how), assumed/unverified, noticed-but-not-done, remaining risk. Results without
claim tags are unusable for auditing — send them back rather than re-verifying by
hand.

## 5. Record the tier

Wherever the result lands (log entry, report), name the tier that produced it. A
light-tier result must never read as capable-vetted — silence about scrutiny reads as
more scrutiny than was applied.

## Diff-connect checklist (offline reviewer degradation)

```
For every hunk in the diff: name the briefing line it serves — revert hunks with none.
Run tools/land.sh from the current tree; paste its output verbatim.
Break the done-check once on purpose; confirm it fails; restore — or mark Unverified.
List every touched file not named in the briefing, with one line of justification.
```

## Prohibitions

- Never downgrade review, security, or guardrail-adjacent work to the light tier, no
  matter how checklist-shaped it looks.
- Never delegate without a "done means" the executor can run and fail.
- Never accept "should work" or an untagged summary back from a sub-agent.
- Never leave Non-goals blank in a briefing — blank non-goals is delegated scope
  creep.

## Tells

You are misrouting if: you cannot say which downstream check would catch the
sub-agent being wrong; the briefing's Landmines section is empty for a codebase you
know has traps; you are delegating a decision to avoid making it; or you are about to
paste your conclusion into Starting points instead of the evidence for it.
