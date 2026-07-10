# Task briefing template

A large share of a top-tier model's advantage is that it *reconstructs missing context on
its own*: it infers the real goal, finds the landmines, decides when to stop. A lower-tier
model performs dramatically better when that context is handed to it up front. This
template is for whoever delegates — a human, or an orchestrating model spawning subagents.
Filling it takes two minutes and replaces the most expensive part of the capability gap.

Rule of thumb: **anything left blank, the model will fill with a guess.** Blank
"Non-goals" → scope creep. Blank "Done means" → success theater. Blank "Landmines" → the
model steps on them.

```markdown
## Goal
<One sentence. The observable outcome, not the activity.
 "Users can reset passwords via email" — not "work on the password reset flow.">

## Why (one line)
<The purpose behind the goal, so correct judgment calls are possible when the letter of
 the goal underdetermines a decision.>

## Done means
<The concrete check that proves completion. A command to run and what its output must
 show, a scenario to execute, a state to demonstrate. Must be able to fail.>

## Non-goals
<The adjacent things NOT to do. "Do not touch the auth middleware." "No refactoring of X
 even though it's ugly." "Performance is out of scope." Also list files that might look
 relevant but are NOT to be touched — an explicit not-touched list is the cheapest scope
 fence there is.>

## Constraints
<Hard limits distinct from scope: "Do not modify: <files/systems off-limits>."
 "Do not change: <behavior, interface, or schema that must stay the same>.">

## Starting points
<Files, symbols, docs, and a prior-art example to imitate:
 - behavior lives around: <file/dir>
 - imitate: <file:line — an existing example of the same kind of thing>
 - the design doc / ticket / prior discussion: <link>>

## Useful capabilities
<Relevant installed tools or skills. If a known uninstalled skill would materially improve
correctness or verification, name it as a recommendation — never install it implicitly.>

## Landmines
<Known traps a newcomer would hit: the test suite that needs env var X, the module that
 looks dead but isn't, the flaky test to ignore, the file that is generated — don't edit.>

## Premises you may trust vs. must verify
<Split what you've already confirmed ("the bug reproduces with cmd Y — trust this") from
 what is folklore ("we think it started after the v2 upgrade — verify before relying").>

## Budget & escalation
<When to stop and ask rather than push on: "If the fix requires schema changes, stop and
 report." "If not reproducible within ~15 minutes, escalate with a stuck report.">

## Open questions
<Anything the executor cannot resolve from the codebase or this briefing alone. If a
 question affects the approach, it must be answered before work starts — otherwise the
 blank becomes a guess.>
```

Task type note: for an **investigation** briefing (analysis, review, audit — no code
changes), say so in Goal and require the deliverable as findings with claim tags; the
"Done means" is then the questions the findings must answer, not a command.

## For orchestrators (model-to-model delegation)

- One goal per briefing. Two goals in a briefing yields two half-done tasks.
- Name the task class and dispatch with it (`python tools/delegate.py --task-class
  bugfix|investigation|landing`) — the executor gets a class-shaped micro slice and its
  output skeleton, and the result is verified fail-closed against that skeleton. No fitting
  class → omit the flag (universal loop) and expect only landing format + claim tags back.
- Paste **evidence, not conclusions**, into Starting points: the actual error text, the
  actual log lines. Conclusions inherited from another model arrive premise-shaped and
  will be swallowed (failure mode #7) unless marked "must verify."
- Require the deliverable back in landing format (verified / assumed / noticed-but-not-
  done / remaining risk) so results from multiple subagents are comparable and auditable.
- If the sub-task is investigation, say explicitly that the deliverable is *findings with
  claim tags, no code changes* — otherwise something will get "fixed" along the way.
