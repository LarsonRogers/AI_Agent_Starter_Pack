# Behavioral evals

The evals test whether the pack changes actions and outcomes, not whether the model repeats
protocol vocabulary. Primary grading signals are:

- executable public and hidden behavior checks;
- protected-file integrity and final repository state;
- tool order, such as observing the reproduction before the first edit;
- report semantics only when the requested deliverable is itself a report.

`PREFLIGHT`, `[OBSERVED]`, and other literal labels are not pass conditions. A model can use
the right words while fabricating verification; `results.md` records that exact failure in
the former local-tier eval.

## Run kit vs. baseline

Prerequisites: Claude Code on `PATH`, an authenticated session, and the requested model.
The runner creates disposable fixture copies, so the fixture-only permission bypass never
touches a real repository.

```bash
python evals/run_evals.py --model claude-sonnet-5 --profile full
python evals/run_evals.py --model qwen2.5-coder:7b --profile micro --claude <compatible-cli>
```

Options:

- `--case <id>` selects one or more cases.
- `--arm kit|baseline|both` defaults to both.
- `--profile full|compact|micro` selects the shipped context profile.
- `--artifacts <dir>` changes the gitignored transcript/result directory.

The default invocation adapter targets Claude Code's `stream-json` interface. The core
runner and graders are provider-neutral: pass `--command-json` with an argv JSON array for
another harness. The runner supplies `{prompt_file}`, `{system_prompt_file}`, `{model}`,
`{arm}`, `{fixture}`, and `{transcript}` placeholders plus matching `FABLIZED_EVAL_*`
environment variables. Example shape:

```bash
python evals/run_evals.py --model local-model --profile micro \
  --command-json '["my-agent", "--prompt-file", "{prompt_file}", \
  "--system-file", "{system_prompt_file}", "--json"]'
```

The adapter must write JSONL tool events and a final result to stdout. Adding a provider is
therefore a thin edge adapter; no provider behavior belongs in the graders or doctrine.

## Acceptance

For a kit-vs-baseline run on one model/profile:

1. The prompt must remain inside its named word budget.
2. The kit may not regress a case the baseline passes.
3. The kit must pass at least one case the baseline fails.

For a kit-only diagnostic run, every selected case must pass. Kit-only results do not prove
lift and must not be described as validation against a model.

Run multiple repetitions before a release when the target is stochastic. Keep model id,
profile, date, runner version, and artifacts. Report success rate and median input/output
tokens and latency when the harness exposes them; a reasoning procedure that consumes the
context needed for the task has not earned its cost.

Tracked release summaries live in `results-v13.1.md`; raw transcripts remain gitignored.

## Small-model rule

Use the exact profile intended for deployment. `micro` is a named, aggressively condensed
operating loop with an 800-word hard ceiling; it is not the full doctrine silently truncated.
Promote a small model/profile only when it shows behavioral lift without task-success
regression. If more instructions reduce performance, change the named condensation in
`core/digests.md`, rebuild, and rerun both arms.

## Current cases

- `bugfix-reproduce-first`: hidden output boundaries, protected reproduction, and trace order.
- `stuck-investigation`: read-only fixture integrity plus the first directly verifiable cause.
- `landing-audit`: fixture integrity, scope-creep detection, and rejection of an unrun claim.

Add cases by pairing a fixture with a grader in `behavioral_graders.py`. Prefer executable
oracles and hidden inputs over text matching. Any semantic matcher must grade the requested
meaning, not a doctrine-specific phrase.
