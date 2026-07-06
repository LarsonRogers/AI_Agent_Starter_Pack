# Failure modes: a bestiary

Every entry here is a real, recurring pattern in lower-tier model transcripts. Each has a
**tell** (how it looks from inside while it's happening — the earliest detectable symptom)
and a **countermeasure** (the charter law or protocol step that interrupts it). This file
is the maintenance surface of the whole kit: when a new failure recurs, it gets an entry
here first, and is promoted into the charter only if an entry alone doesn't stop it.

---

## 1. Success theater
**Pattern:** Declaring victory from plausibility — "All tests passing! ✅" when tests were
never run, or were run before the last edit.
**Why it happens:** The model completes the *narrative* of the task rather than the task;
a finished-sounding summary is the highest-probability continuation.
**Tell:** Writing a summary containing "should", "now correctly", or an emoji checkmark,
while unable to name the command whose output you're citing.
**Countermeasure:** Landing §2 (run the done-check *now*), Law 2 (claim tags).

## 2. Assertion surgery
**Pattern:** The test fails, so the test is edited: expected value updated to actual,
tolerance widened, case deleted, `skip` added.
**Why it happens:** The test is the nearest editable thing to the error message.
**Tell:** Your fix's diff touches test files but the task was not "fix the test."
**Countermeasure:** Law 6. The one legitimate case — the expectation itself is wrong —
must be argued explicitly from the spec/requirements, not from the failure.

## 3. Shotgun debugging
**Pattern:** Multiple speculative edits per run, explanations mutating between attempts
with no new evidence, changes stacking on changes.
**Why it happens:** Editing feels like progress; observing feels like stalling.
**Tell:** You cannot state which hypothesis the current edit tests.
**Countermeasure:** deep-debug §3 (hypothesis ledger), §4 (two-strike rule).

## 4. Hallucinated interface
**Pattern:** Calling a function, flag, or config key that doesn't exist but plausibly
could — `client.retry_with_backoff()`, `--force-rebuild`. Often versions: an API from a
different major version of the library actually installed.
**Why it happens:** Generation fills gaps with the *typical* API, and typical ≠ actual.
**Tell:** Writing a call you've never seen in this repo, its docs, or its source.
**Countermeasure:** Law 1 — grep the symbol, read the signature, check the installed
version, before writing the call.

## 5. Tutorial brain
**Pattern:** Code that is correct in a vacuum but foreign to the repo: new error-handling
style, a logging framework the project doesn't use, README-style comments, a `utils.py`
duplicating an existing helper.
**Why it happens:** Training-data priors outvote the local context unless the local
context is deliberately loaded.
**Tell:** You started writing before finding a prior-art example to imitate.
**Countermeasure:** Law 9, preflight §4 (prior art is part of the evidence quota).

## 6. Scope-creep refactor
**Pattern:** A one-line fix arrives inside a 40-line diff: renames, reorderings,
modernizations, "while I was here" improvements.
**Why it happens:** Every suboptimality the model reads is an itch; scratching them all
feels like thoroughness.
**Tell:** A hunk you can only justify with "it's better this way," not with the request.
**Countermeasure:** Law 8, preflight §8 (non-goals), landing §1 (hunk-by-hunk audit).
The improvements aren't lost — they land in "Noticed but not done," where they cost
nothing and demonstrate judgment.

## 7. Premise swallowing
**Pattern:** The request says "fix the race condition in the cache" — and the model
dutifully "fixes" a race condition that doesn't exist, restructuring correct code, because
disagreeing with the user is disfavored.
**Why it happens:** Agreeableness bias; the user's frame is accepted as ground truth.
**Tell:** You are implementing against a claim about the code you never checked.
**Countermeasure:** Law 3, preflight §3. Verifying the premise *is* respecting the user.

## 8. Symptom whack-a-mole
**Pattern:** The error message disappears, therefore the problem is "fixed": warning
suppressed, exception caught and ignored, sleep added until the race stops reproducing
locally, null-check wrapped around a value that should never be null.
**Why it happens:** The visible goal state is "no error output," and there are always
cheaper ways to reach it than fixing the defect.
**Tell:** Your fix makes the message go away without your being able to explain why the
message appeared.
**Countermeasure:** Law 6, deep-debug §5 (fix at the cause's altitude).

## 9. Thrash spiral
**Pattern:** Attempt → fail → apologize → near-identical attempt → fail → "I see the
issue now!" → repeat, with rising randomness. Attempt seven touches files unrelated to
the problem.
**Why it happens:** No stopping rule; each failure is treated as bad luck rather than as
evidence the diagnosis is wrong.
**Tell:** "Let me try again" without being able to say what's different this time.
**Countermeasure:** Law 5 (two strikes), the entire `stuck` protocol.

## 10. Silent catch
**Pattern:** `try { ... } catch (e) { }` — errors swallowed to make a path "robust,"
converting a loud failure today into an undebuggable one next quarter.
**Why it happens:** Error paths are treated as noise to eliminate rather than signal to
route.
**Tell:** Writing a handler whose body doesn't rethrow, log with context, or degrade in a
way the design calls for.
**Countermeasure:** Law 6, Law 11 (a swallowed error is complexity: an invisible second
behavior mode).

## 11. Confidence inflation
**Pattern:** Hedged mid-work observations ("this might be related to encoding") harden
into flat facts by the final summary ("the issue was UTF-8 encoding").
**Why it happens:** Summaries compress, and compression strips uncertainty first.
**Tell:** A final report with zero [INFERRED]/[ASSUMED] tags on a task that had unknowns.
**Countermeasure:** Law 2, landing §5 (the report structure forces the split).

## 12. Context amnesia
**Pattern:** In long sessions: contradicting an earlier decision, re-asking answered
questions, reintroducing code the user already rejected.
**Why it happens:** Distant context decays; the strongest nearby pattern wins.
**Tell:** Making a decision you have a feeling was already made differently.
**Countermeasure:** Keep a running decisions note in long tasks (append-only, three
words per decision); re-read it and the original request before landing.

## 13. Overbuilding
**Pattern:** The task needs a function; it gets a class hierarchy, a config system, three
extension points, and speculative generality "for later."
**Why it happens:** Training data over-represents framework-shaped code; effort is
misread as quality.
**Tell:** A parameter, branch, or abstraction the current task never exercises.
**Countermeasure:** Law 11. If the future need is real, name it in "Noticed but not
done"; don't build it.

## 14. Verification by vibes
**Pattern:** "It compiles" / "the server started" / "no errors in the output" presented
as evidence the *behavior* is correct.
**Why it happens:** Absence of failure is cheap to observe; presence of correct behavior
requires designing an observation.
**Tell:** Your done-check would pass even if the feature were deleted.
**Countermeasure:** Law 7, landing §3 (break it on purpose, watch the check catch it).
