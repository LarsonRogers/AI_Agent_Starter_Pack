# v13.1 behavior-first eval summary

## claude-sonnet-5 · full profile · 2026-07-10

Profile: `fablized-full.md`, 7,195 words, 8,000-word budget. Both arms used fresh
fixtures and the automated graders in this directory.

| Case | Kit | Baseline | Lift |
|---|---:|---:|---:|
| `bugfix-reproduce-first` | PASS | PASS | no |
| `stuck-investigation` | PASS | PASS | no |
| `landing-audit` | PASS | PASS | no |

Result: **no regression, no measured lift, context budget passed; acceptance FAILS because
no case discriminated.** This frontier model already performed the graded behaviors without
the pack in these runs. Do not describe v13.1 as validated on this model from these cases.

The first landing run exposed two grader defects: runtime cache files counted as edits and a
quoted false claim counted as asserting it. The grader was changed to ignore standard runtime
artifacts and to recognize explicit refutation, unit tests were added, and both arms were
rerun. This correction changed grading, not agent output.

## Local micro profile

Profile: `fablized-micro.md`, 358 words, 800-word budget. The recorded local endpoint was
down on 2026-07-10, so no v13.1 micro kit-vs-baseline result exists yet. The historical v13
local result in `results.md` remains FAIL 3/3 and cannot validate this redesigned profile.

Next acceptance target: run all cases repeatedly against the deployed small/local model
through a tool-capable generic adapter. Promotion requires at least one lift case, no
baseline regression, and context-budget compliance.
