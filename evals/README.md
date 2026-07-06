# Evals — does the kit change behavior at the decision points?

Each case in `evals.json` plants a situation where an undisciplined model reliably takes
the cheap path (fix without reproducing; a fourth speculative edit; "all tests pass"
without a run) and asserts, by regex over the agent's output, that the kit-driven run
takes the charter's path instead. The scenarios mirror `doctrine/worked-examples.md`.

## Running a case (v13: manual per-case; automated harness is v13.1)

```bash
# 1. copy the case's fixture dir somewhere disposable, cd into it
# 2. run the case's setup[] commands from evals.json (git init, commit, apply patch...)
# 3. KIT ARM:
claude -p "<the case's prompt>" \
  --append-system-prompt "$(cat /path/to/kit/adapters/system-prompt/fablized-full.md)"
# 4. BASELINE ARM: identical, without --append-system-prompt
# 5. apply the case's assertions (case-insensitive regex) to each arm's full output
```

For small-context targets substitute `fablized-compact.md` or `fablized-micro.md` — that
is the honest test of the profile actually being shipped to that model.

## Acceptance rule — per target model (Amendment 01)

The kit is judged **kit-vs-baseline on each target tier**, never kit-alone:

- A case passes an arm when all `must_appear` regexes match, each `must_appear_any`
  group has ≥1 match, and no `must_not_appear` matches.
- **The kit earns its keep on a model only where the kit arm passes cases the baseline
  arm fails.** A case both arms pass is redundant on that model (keep it — it is a
  guarantee for weaker models, not a trim signal). A case the kit arm *fails* on a small
  model is a real finding: if kit overhead measurably hurts (protocol tokens displacing
  code context), prune to the laws/protocols that pay for themselves and record the
  result as a **named build variant** — never silently thin the doctrine.

Record results per model (model id, date, arm outputs kept) so the claim "validated on
X" always names X.
