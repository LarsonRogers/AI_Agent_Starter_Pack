---
name: stuck
title: Stuck
description: Thrash-breaker. Use when two fix attempts have failed, when the same command has been re-run without changes hoping for different output, when an approach previously abandoned is being retried, or when progress has stalled for several tool-call rounds. Converts thrash into either a new fact or a well-formed escalation.
---

# Stuck

Being stuck is not the failure. The failure is what weaker processes do next: try harder
along the same axis, with escalating randomness and apologies. This protocol replaces that
with the only two moves that work: **get a new fact** or **escalate well**.

## 1. Full stop

No more edits. No more re-runs. The next edit you make will be after this protocol produces
a reason for it.

## 2. Write the ledger honestly

Two columns:

```
FACTS (observed, with source):        BELIEFS (never directly verified):
- ...                                 - ...
```

Be ruthless about the sort. "The config is loaded" — did you *observe* it loading (log,
print, debugger), or does it just seem obvious? Most stuckness is a belief sitting in the
facts column. The defect is almost always inside a step you skipped verifying because it was
"obviously fine."

## 3. Attack your strongest belief

Pick the belief you are *most* confident in and design the cheapest direct observation of it:

- Is the code you're editing the code that's running? (add a deliberate syntax error or
  print — does the failure change?)
- Is the test running the file you think it runs? Is the build actually rebuilding?
- Is the environment what you assume (versions, env vars, cwd, which binary)?
- Is the input what you assume? (print it at the boundary, don't recall it)

This single move resolves the majority of stuck states.

## 4. Change altitude, not effort

If step 3 didn't crack it, the problem may be at a different layer than the one you're
digging in:

- **Down:** data, encoding, filesystem, network, clock, concurrency.
- **Up:** the requirement or test expectation itself is wrong; the task as stated is the bug.
- **Sideways:** shrink the reproduction further; build a minimal fresh example that *works*
  and diff it against the failing case — walk the differences.

Also ask: has this ever worked? If yes, what changed since (diff, dependency bump, data)?
If no, stop debugging a regression that is actually a never-worked.

## 5. Budget check

You get **one** pass through steps 2–4 per stuck event. If you emerge with a new fact,
return to the deep-debug protocol with it. If you emerge with nothing new, do not loop —
escalate. Time spent past this point has sharply negative value: it produces increasingly
random edits that someone must review and revert.

## 6. Escalate well

A good escalation is a gift; a bad one ("it doesn't work, what should I do?") wastes the
one resource that can unblock you. Format:

```
STUCK REPORT
Goal: <one sentence>
Repro: <exact command + failure output>
Facts: <observed, with how observed>
Hypotheses tested and dead: <H → evidence that killed it>
Strongest surviving belief I could not verify: <...>
Specific question / decision needed: <one thing>
```

State the code in exactly the condition the report describes — no half-applied experiments
left in the tree. If you tried approaches, say which are still in the diff.

## The prohibitions

- Never retry an approach that already failed **unchanged**. If retrying, name what is
  different this time.
- Never "fix" the stuck state by weakening the check that detects the problem.
- Never apologize-and-loop. One sentence acknowledging the miss, then the protocol.
- Never present exhaustion as completion ("this should work now" on attempt five). Landing
  rules still apply: unverified is unverified.
