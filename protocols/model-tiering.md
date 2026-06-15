<!-- Starter Pack v12.2 — protocols/model-tiering.md -->
<!-- Load this file when: you are about to delegate a task to a sub-agent and
     must decide which model it runs on — a governance/watch check, a
     mechanical scan, or template-driven drafting. -->
<!-- Does NOT trigger when: the main agent does the work itself (it keeps the
     session model), or when a deterministic shell command settles the
     question (no model is involved at all). -->
<!-- Do not load unless triggered — see AGENTS.md → Protocol Index -->

## Model Tiering for Sub-Agents

Not every delegated task needs the strongest model. A bounded, rule-bound
check governed by an explicit rubric can run on a cheaper, faster model
without losing fidelity — but a judgment call dressed up as a checklist
cannot. This protocol decides which tier a sub-agent task runs on, so cost
is spent where judgment is needed and saved where it is not.

This is a cost optimization within already-bounded work, **not** a quality
shortcut. The safeguard is the selection rule below, not the model.

### The three tiers

```
DETERMINISTIC  — a script settles it; no LLM at all.
                 ls-vs-index, version grep, dead-link scan, YAML/JSON parse,
                 planted-secret scan, file-exists/path checks.
                 RULE: never spawn a sub-agent for what a command answers.

LIGHT          — bounded, rubric-driven sub-agent work with a mechanically
                 checkable output. Header/WHY-comment presence scans,
                 "every protocol has a trigger row," "every changed file has a
                 file header," template-driven DECISION_LOG/HANDOFF drafting,
                 mechanical reformatting, simple extraction/classification.
                 Model: cheap/fast tier (e.g. Haiku-class; in OpenCode/Codex
                 the provider's small model).

CAPABLE        — judgment and safety-critical work. Independent review
                 (protocols/review.md), secure-coding assessment, conflict
                 resolution, architecture-conformance judgement, anything
                 where a miss is a guardrail or correctness failure.
                 Model: the main session model. NEVER downgraded.
```

Tier names are by task property, not by model brand — model IDs drift and
differ across harnesses. The parenthetical model names are current examples,
not pins.

### Selection rule — the three-part gate

Route a task to the **Light** tier only when ALL THREE hold:

```
[ ] (a) An explicit rubric or checklist governs the task — the sub-agent is
        applying stated rules, not forming an opinion.
[ ] (b) The output is mechanically checkable — a list, a yes/no per item, a
        diff — something the caller can spot-verify without re-judging.
[ ] (c) A wrong answer is caught downstream — by a Capable-tier review, a
        deterministic gate, or the human demo — before it can cause harm.
        For anything feeding a guardrail-adjacent or safety decision, (c)
        must be a deterministic gate or a Capable-tier check: a human demo
        alone does not qualify, since a non-dev demo is not a defect backstop.
```

If any one fails → **Capable** tier. When unsure which side a task is on,
treat it as Capable: the cost of an over-strong model is money; the cost of
an under-strong watchdog is a missed defect.

### Never downgraded (hard list)

These always run on the Capable tier, regardless of how rule-bound they look:

```
- Independent review (protocols/review.md) — the reviewer is the safety net;
  a cheap reviewer that misses a blocker defeats the gate's entire purpose.
- Secure-coding assessment (protocols/secure-coding.md).
- Conflict resolution / instruction-precedence calls.
- Architecture-conformance and growth-trigger judgement.
- Any hard-guardrail decision.
```

### Honesty — record the tier

When a Light-tier sub-agent produces a result that feeds a decision or a log
entry, note the tier used (e.g. "header scan — Light tier"). A Light-tier
result must never be presented as if a Capable-tier agent vetted it — same
principle as the "could not verify" list in review.md: silence about the
level of scrutiny reads as more scrutiny than was applied.

Light-tier delegation is a **silent default** — the agent may route a
qualifying task to the Light tier without asking — but the tier is logged
wherever the result is recorded. Routing to the Light tier never changes
*what* work is done or *which* guardrails apply; it changes only which model
executes a downstream-checked scan. It is never license to self-delegate
guardrail-adjacent work — that is governed by AGENTS.md Part 1, unchanged.

### Harness-aware mechanism

The tiering principle is identical in all harnesses; only the knob differs.
All three default a sub-agent to inherit the session model when no model is
set, so tiering is opt-in per delegation.

```
Claude Code  — set `model:` in the sub-agent's `.claude/agents/*.md`
               frontmatter (haiku / sonnet / opus / inherit, or a full model
               ID), or pass `model` when spawning via the Agent/Task tool.
               Omit → inherit. A global floor can be set with the
               CLAUDE_CODE_SUBAGENT_MODEL env var; enterprise policy may
               restrict models via an availableModels allowlist (a blocked
               request falls back, it does not fail).

OpenCode     — define the agent under the `agent` key in opencode.json with
               `"mode": "subagent"` and `"model": "provider/model-id"`
               (e.g. "anthropic/claude-haiku-…"). Omit model → inherits the
               invoking agent's model.

Codex        — define the subagent in `.codex/agents/*.toml` with `model`
               (and optional `model_reasoning_effort`); omit → inherits the
               parent session. Caveat: subagent invocation has known rough
               edges in some Codex sessions (reported in openai/codex#15250
               as of 2026-06; verify against current Codex docs) — if a
               Codex subagent is not reachable, fall back to running the
               check in-session on the Capable model rather than skipping it.
```

If a harness cannot route to a cheaper model for a given task, run the task
on the Capable model — never skip the check to save cost. Tiering lowers
cost where possible; it never lowers coverage.
