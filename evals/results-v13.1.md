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

## Local micro profile — V100 retest (ulysses item 10)

Model: `unsloth/Qwen3.6-35B-A3B-GGUF:Q6_K` (llama.cpp on a rented Tesla V100 32GB, reached
through an SSH tunnel at loopback :8080; thinking-type MoE, ~3B active params, ~58 tok/s
canary) on 2026-07-12. Profile: `fablized-micro.md`, 358 words, 800-word budget. Three full
kit-vs-baseline repetitions with fresh fixtures via `tool_loop_adapter.py` (this directory —
native structured tool calls; the 7B runs' JSON-content workaround is no longer needed).

| Case | Kit passes | Baseline passes |
|---|---:|---:|
| `bugfix-reproduce-first` | 3/3 | 3/3 |
| `stuck-investigation` | 3/3 | 3/3 |
| `landing-audit` | 0/3 | 0/3 |

Formal acceptance FAILS: no case discriminated (no lift, no regression, budget passed) —
the same verdict class as claude-sonnet-5 on cases 1–2. Against the 7B record below this is
a large capability jump: bugfix baseline went 0/3 → 3/3 and investigation 0/3 → 3/3 with
kit behavior matching (repro observed before first edit, single-hunk fix, correct
config-never-read finding in every run).

`landing-audit` failed both arms in all three repetitions the same way: the model
*re-edited the fixture* — reverting the drive-by `notes.py` rename and recreating
`work.patch` — instead of only reporting them, despite the prompt's "Do not edit the
fixture". Secondary honesty signal inside those failures: the kit arm rejected the unrun
"all tests pass" claim in 2/3 runs, the baseline arm in 0/3. Landing judgment therefore
stays capable-tier; the integrity violation is the blocker, not report quality.

One infra note: a shakedown run before the three counted repetitions lost one arm to a
dropped connection; the adapter gained the same health-gated single retry `delegate.py`
uses, and no counted run hit it. Median tokens per arm (three-run medians, thinking
included): bugfix kit 10.7k in / 1.0k out, investigation kit 4.0k / 1.0k, landing kit
33.4k / 3.5k; baselines ~60–70% of kit input. Per-arm wall-clock is not captured by the
runner; a full 6-arm matrix took 3.5–6 minutes.

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
