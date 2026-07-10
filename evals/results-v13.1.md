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

Model: `qwen2.5-coder:7b` (Ollama, Q4_K_M) on 2026-07-10. Profile:
`fablized-micro.md`, 358 words, 800-word budget. The canary reported approximately 64 tok/s
at 48C.

Codex 0.144.1 and OpenCode could reach the model, but Ollama returned requested tool calls as
plain JSON message content rather than structured tool-call events. The repeated comparison
therefore used a fixture-scoped JSON tool-loop adapter with path confinement and an allowlist
for verification commands. Three runs used the same final adapter version and fresh fixtures.

| Case | Kit passes | Baseline passes |
|---|---:|---:|
| `bugfix-reproduce-first` | 2/3 | 0/3 |
| `stuck-investigation` | 0/3 | 0/3 |
| `landing-audit` | 0/3 | 0/3 |

Two of three complete runs met the formal acceptance rule through the bugfix lift, with no
baseline regression and the context budget passing. This is **partial, unstable evidence—not
a promotion result**: the kit never passed investigation or landing, one earlier diagnostic
edited the protected reproduction instead of the implementation, and the model sometimes
exhausted the tool-step limit. The micro loop can elicit a correct reproduce-first fix from
this model, but it does not reliably enforce falsification, scope audit, or honest landing.

Testing also exposed two provider/OS defects in the runner: Windows-invalid model IDs in
artifact paths and unrecognized `write_file`/`replace_text` edit events. Both were corrected
with unit coverage; fixture copies now exclude runtime caches as well.
