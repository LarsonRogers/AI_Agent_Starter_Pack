# Evals — does the kit change behavior at the decision points?

Each case in `evals.json` plants a situation where an undisciplined model reliably takes
the cheap path (fix without reproducing; a fourth speculative edit; "all tests pass"
without a run) and asserts, by regex over the agent's output, that the kit-driven run
takes the charter's path instead. The scenarios mirror `doctrine/worked-examples.md`.

## Running a case (v13: manual per-case; automated harness is v13.1)

```bash
# 1. copy the case's fixture dir somewhere disposable, cd into it — a FRESH copy per
#    arm (the agent mutates the fixture), or reset between arms:
#    git reset --hard "$(git rev-list --max-parents=0 HEAD)" && git clean -fd
# 2. run the case's setup[] commands from evals.json (git init, commit, apply patch...)
# 3. KIT ARM — pin --model to the same id in BOTH arms (the acceptance rule is
#    per-model; note the id + date with the kept outputs). Headless -p needs a
#    permission grant: fixtures are throwaway temp dirs, so
#    --dangerously-skip-permissions is acceptable there (never on a real repo).
#    CAPTURE: default text output prints ONLY the final message — turn-by-turn
#    protocol evidence (PREFLIGHT, per-step claims) is discarded and the
#    must_appear greps read nothing. Capture stream-json (--print requires
#    --verbose with it) and keep the raw stream as the graded artifact.
#    SYSTEM PROMPT: use --append-system-prompt-file — the inline $(cat ...) form
#    exceeds the ~32K argv cap on Windows.
claude -p "<the case's prompt>" --model <model-id> --dangerously-skip-permissions \
  --output-format stream-json --verbose \
  --append-system-prompt-file /path/to/kit/adapters/system-prompt/fablized-full.md \
  2>&1 | tee kit-arm-stream.jsonl
# 4. BASELINE ARM: identical (same --model, same capture flags), without
#    --append-system-prompt-file
# 5. apply the case's assertions (case-insensitive regex) to each arm's full
#    captured stream (the .jsonl files)
```

For small-context targets substitute `fablized-compact.md` or `fablized-micro.md` — that
is the honest test of the profile actually being shipped to that model.

## Acceptance rule — per target model (Amendment 01)

The kit is judged **kit-vs-baseline on each target tier**, never kit-alone:

- A case passes an arm when all `must_appear` regexes match, each `must_appear_any`
  group has ≥1 match, and no `must_not_appear` matches.
- **The kit earns its keep on a model only where the kit arm passes cases the baseline
  arm fails.** A case both arms pass is redundant on that model (keep it — it is a
  guarantee for weaker models, not a trim signal). On a frontier target,
  both-arms-pass means no measured lift on that target — acceptable and expected;
  the discriminating target is the local tier (the tier-map model driven through the
  delegate/OpenCode path with the micro prompt). A case the kit arm *fails* on a small
  model is a real finding: if kit overhead measurably hurts (protocol tokens displacing
  code context), prune to the laws/protocols that pay for themselves and record the
  result as a **named build variant** — never silently thin the doctrine.

Record results per model (model id, date, arm outputs kept) so the claim "validated on
X" always names X.
