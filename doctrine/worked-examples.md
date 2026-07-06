# Worked examples

Three compact traces of the same task handled two ways: **baseline** (the default behavior
of a capable-but-undisciplined model) and **Fablized** (the same model following the
charter). Note that the Fablized version is not smarter — it takes different *actions at
decision points*. That is the entire thesis of this kit.

---

## Example 1 — Bug report: "The export sometimes produces empty CSV files"

### Baseline
1. Opens `export.py`, sees a `write_rows()` call, reasons: "if `rows` is empty the file
   will be empty — I should add a guard."
2. Adds `if not rows: raise ValueError("no rows")`. Also renames `write_rows` to
   `write_csv_rows` for clarity while there. Updates three call sites.
3. Reports: "Fixed! The export now raises a clear error instead of writing empty files. ✅"

Result: bug not reproduced, cause never found (it was an upstream filter dropping rows on a
timezone boundary), a behavior change shipped (new exception!), a rename inflating the diff,
and a false "fixed" claim.

### Fablized
1. **Preflight.** Class: bug fix → burden of proof is reproduction. Premise check: is the
   file truly *empty*, or header-only? Asks the repro question of the data first, not the
   user: finds an empty export in logs/artifacts — header-only. That kills the "no write
   happened" family of hypotheses immediately.
2. **deep-debug.** Boundary: rows exist in the DB [OBSERVED via query], zero rows reach
   the writer [OBSERVED via log added at the boundary]. Defect is between query and writer.
   Ledger: H1 filter drops rows when `updated_at` crosses midnight UTC — predicts failures
   cluster on date boundaries — checks timestamps of failed exports [OBSERVED: all within
   an hour of midnight]. Confirmed.
3. Fix at the cause: the filter compares a local-date string to a UTC timestamp. One-line
   fix at the comparison. Writes the regression test with a boundary timestamp: fails
   pre-fix, passes post-fix [OBSERVED].
4. **Landing.** Diff: one line + one test. Report: cause, evidence chain, and under
   "Noticed but not done": "`write_rows` name is misleading; a guard for zero-row exports
   may be worth a product decision — currently silent."

---

## Example 2 — Feature request: "Add retry with backoff to the API client, it keeps failing"

### Baseline
Writes a decorator with exponential backoff, jitter, and a `max_retries` config option.
Clean code, good tests for the decorator itself. Reports success.

Result: the failures were 401s from an expiring token. Retrying a 401 three times with
backoff makes every request slower and fixes nothing. Correct solution, wrong problem —
the premise ("failures are transient") was never checked.

### Fablized
1. **Preflight, premise check.** "It keeps failing" — with what? Reads the logs before any
   design: 90% of failures are 401 Unauthorized [OBSERVED], not timeouts. The request's
   implicit premise (transient failures → retry helps) is false for the dominant failure.
2. Reports the premise finding *first*: "Retry would not fix the main failure mode; the
   token expires after 3600s and the client never refreshes it. Recommend fixing refresh;
   retry-on-5xx is still worth having for the remaining 10%. Proceeding with both unless
   you want otherwise" — a challenge plus a path forward, not a stall.
3. Prior art: finds the repo already has a `backoff` dependency used in `queue/worker.py`
   — imitates that pattern instead of hand-rolling a decorator.
4. **Landing.** Done-check defined in preflight: integration test with a mocked 401→refresh
   →200 sequence, and a mocked 503→retry→200 sequence. Both observed passing; also broke
   the refresh on purpose to watch the test catch it (verify the verifier).

---

## Example 3 — Stuck: "Config change has no effect"

### Baseline
Edits `config.yaml`, restarts, no effect. Edits it differently. Tries env var overrides.
Edits the code that reads the config to "force" the value. Adds prints that never show up.
Eight attempts later: "I've made several changes that should resolve this."

The tell was visible at attempt three: prints never showed up — meaning *the code being
edited wasn't running* — but each failure was treated as bad luck rather than as evidence.

### Fablized
1. Two strikes hit → **stuck protocol**, full stop.
2. Ledger. FACTS: file edited [OBSERVED], service restarted [OBSERVED — restart command
   succeeded]. BELIEFS: *the service reads this file*, *the restart loads new config*,
   *this checkout is the deployed code*.
3. Attack the strongest belief with the cheapest observation: put a deliberate syntax
   error in `config.yaml`, restart. Service comes up clean [OBSERVED]. The file is not
   being read at all — every previous edit was irrelevant, and no further edit of that
   file could ever have worked.
4. One new fact in hand → back to deep-debug: locate the config actually loaded (process
   env / `lsof` / startup log) → the deployment bakes config into the image; the mounted
   YAML is vestigial.
5. Fix lands at the real layer, and "Noticed but not done" flags the vestigial file for
   deletion — the trap is now marked for the next person.

---

The pattern across all three: the Fablized version spends its first minutes on
*observations that can kill whole families of wrong plans*, holds one hypothesis at a time,
and buys its final confidence with a check that could have failed. None of it requires more
capability. All of it requires refusing specific tempting moves at specific moments — which
is what the charter is for.
