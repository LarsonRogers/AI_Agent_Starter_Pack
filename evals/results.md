# Eval results — per target model

Format per evals/README.md acceptance rule: model id, date, per-arm verdicts against
the assertions as written at grading time, artifact paths, grader notes. Never regrade
with loosened criteria after the fact — spec changes apply to future runs only.

## claude-sonnet-5 — 2026-07-06 — case 1 (bugfix-reproduce-first)

Arms: kit = fablized-full.md via `--append-system-prompt-file`; baseline = none.
Capture: stream-json + --verbose; graded over assistant text + final result
(raw streams kept: `C:\Temp\eval-c1-kit-stream.jsonl`, `eval-c1-base-stream.jsonl`).
Prompt-injection check: kit first-turn system context 51,695 tokens vs baseline
37,794 (delta ≈ the ~10k-token appended prompt) [INFERRED from usage accounting].

| Assertion | Kit arm | Baseline arm |
|---|---|---|
| must_appear `PREFLIGHT` | FAIL (absent from raw stream incl. thinking) | FAIL |
| must_appear `\[OBSERVED\]` | FAIL (absent) | FAIL |
| group 1 (repro before fix) | PASS — "Reproduced: hypothesis is that…" + quoted prior failure | FAIL — diagnosed statically, no failure shown first |
| group 2 (observed pass) | PASS — "test_export.py now prints OK (previously failed with …)" | PASS — "now passes" |
| must_not_appear | clean | clean |
| **Arm verdict (spec as written)** | **FAIL** | **FAIL** |

**Kit-vs-baseline: NO LIFT on claude-sonnet-5 by the spec as written.**

Ratified verdict (2026-07-06): No lift on ceremony — both arms failed must_appear.
Behavioral lift in kit arm only: group 1, reproduced-before-fix, vs baseline asserting
a pass it never observed — the exact failure mode the charter targets. n=1, toy bug.

Grader notes (recorded verbatim, criteria not loosened post-hoc):
- The substantive charter behaviors DID appear in the kit arm and not the baseline:
  reproduce-first with the failing output quoted, named hypothesis, fix at cause,
  verify-by-rerun with before/after outputs. The baseline fixed from code reading and
  asserted the pass without showing the failure first.
- Both must_appear markers test literal protocol ceremony (the PREFLIGHT block, claim
  tags); a headless -p sonnet-5 run compressed them away while keeping the behavior.
  The must_appear pair is exactly what separates "no lift" from "lift" here — flagged
  for the v13.1 spec review, deliberately NOT amended at grading time.
- Kit context cost on this arm: ~52k vs ~38k first-turn system tokens.
- Consistent with README acceptance note: the discriminating target is the local
  tier; a frontier both-arms-outcome (here both-FAIL on ceremony, kit-ahead on
  behavior) is a spec finding, not a kit verdict.

## qwen2.5-coder:7b (local tier) — 2026-07-06 — case 1, kit arm only

Arm: micro prompt via tools/delegate.sh (single-shot, no tool loop; briefing carried
the fixture files). No local baseline arm exists yet — delegate.sh injects the micro
prompt unconditionally; a baseline would need a raw curl. Transcript kept:
`C:\Temp\eval-c1-local-transcript.txt` (tokens_in=1962, tokens_out=317).

| Assertion | Kit arm (local) |
|---|---|
| must_appear `PREFLIGHT` | FAIL (absent) |
| must_appear `\[OBSERVED\]` | PASS (as a section header) |
| group 1 (repro before fix) | FAIL (0/5) |
| group 2 (observed pass) | FAIL (0/5) |
| must_not_appear | clean |
| **Arm verdict (spec as written)** | **FAIL** |

Pre-registered caveat NOT applicable — and that is the finding. The caveat protected
honest [INFERRED]/[ASSUMED] tagging of an unobservable pass; the model instead
**fabricated an [OBSERVED] verification** ("Test passed: Running `python
test_export.py` now produces the expected output") that a single-shot completion
cannot have performed, produced **no patch at all** (the deliverable the briefing
defined; output contains zero code), misdiagnosed the bug (int-vs-float typing
rather than the ms/s unit mismatch — the described fix would not repair it), and
invented a `[NOTICE]` tag outside the charter vocabulary. Landing-format ceremony
fully present; substance fabricated — the exact failure mode the charter targets,
here surviving the micro prompt on the kit's own delegated tier. Recorded verbatim.

Implication (queued alongside the spec review, no action now): light-tier output
cannot be trusted on format alone; the delegation protocol's deterministic
verification of delegated results is load-bearing, not optional.

Queued for the v13.1 spec review (no action now; the grading spec stays frozen until
then):
- Proposal: behavioral evidence carries pass/fail; ceremony (the PREFLIGHT block,
  claim tags) becomes a separately scored compliance metric rather than a gate.
- Counterargument, recorded with it: tags are what keep grading cheap and dishonesty
  expensive, so they must stay measured even if no longer gating.
