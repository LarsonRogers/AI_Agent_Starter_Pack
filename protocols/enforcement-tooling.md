<!-- Starter Pack v12.12 — protocols/enforcement-tooling.md -->
<!-- Load this file when: the stack is chosen (product definition step 3, or
     inherited codebase Phase 3), validation commands are being set for the
     first time, or the walking skeleton is being built while CI still has
     placeholder jobs. -->
<!-- Does NOT trigger when: tooling is already configured and passing — this is
     a setup protocol, not a per-task check. -->
<!-- Do not load unless triggered — see AGENTS.md → Protocol Index -->

## Enforcement Tooling Protocol

Prose rules are read by a model and followed probabilistically. Tooling is
the model-independent layer: it fails the same way on a bad day. Every rule
the pack states about code quality, architecture boundaries, and secrets
gets mechanical teeth here — **set up by the agent, never left to the user.**

This setup is part of the walking skeleton (backlog item 1): the gates exist
before the first feature is written, not retrofitted after.

### The bundle (one confirmation, not six)

Installing dev tools is a default-policy item. Ask ONCE, as a bundle:

```
"I'm setting up the standard quality tooling for [stack] — these run
automatically and catch problems I might miss: [linter] (code errors),
[formatter] (consistent style), [type checker] (wrong-shape data),
[boundary checker] (keeps the architecture honest), and a pre-commit hook
that blocks commits containing secrets. All standard, free, local tools.
OK to install the bundle?"
```

On confirmation, set up all of:

| # | Gate | Python | JS/TS | Other stacks |
|---|------|--------|-------|--------------|
| 1 | Linter (STRICT config) | ruff | ESLint (+typescript-eslint, strict) | clippy / golangci-lint / stack standard |
| 2 | Formatter | ruff format or black | Prettier | rustfmt / gofmt |
| 3 | Type checker | mypy (strict on new code) | tsc --noEmit, strict: true | built-in |
| 4 | Import-boundary rules | import-linter | dependency-cruiser | go vet / ArchUnit-style tool, or document "none available" |
| 5 | Pre-commit secret scan | git pre-commit hook running the sensitive-data patterns (protocols/sensitive-data.md) against STAGED files — blocks the commit on a match | same | same |
| 6 | SAST | semgrep (`--config auto`) — the CI security job ships with it enabled; refine/pin rulesets here if the stack warrants (see protocols/secure-coding.md) | same | same |
| 7 | CI wiring | Replace the failing placeholder jobs in `.github/workflows/agent-ci.yml` with the real commands from rows 1–4, and set the real `package-ecosystem` in `.github/dependabot.yml` (it silently does nothing on a wrong value) | same | same |

Row 4 is the architecture made mechanical: derive the rules from
AGENTS.md → Part 2 → Project-Specific Architecture (the layer/dependency
decisions in the sketch become the tool's contracts — e.g., "nothing in
data/ imports from controllers/"). When the sketch changes, the rules
change in the same commit.

### Verify every gate can fail (mandatory, before trusting any of them)

A gate that has never failed proves nothing. For each tool, at setup time:

```
[ ] Plant a violation it must catch (an unused import, a forbidden
    cross-layer import, a synthetic AKIA-format key in a staged file)
[ ] Run the gate — it MUST fail, naming the planted violation
[ ] Remove the violation — the gate MUST pass
[ ] Record the demonstration in the decision log entry for the setup task
```

If a gate cannot be made to fail, it is not configured correctly — fix it
or report it; never assume it works.

### Strictness rules

- Configs start STRICT (recommended/strict presets, not defaults-off).
- Loosening any rule is a logged decision: which rule, WHY, recorded in the
  decision log. Never silently disable.
- Inline suppressions (`# noqa`, `eslint-disable`, `# type: ignore`) require
  a justification comment on the same line and are watch-item candidates.
- The agent fixes violations rather than weakening gates. A gate weakened to
  make a task pass is a failed task.

### Existing codebases (inherited projects)

A mature codebase may have hundreds of pre-existing violations. Do not
bulk-fix on day one and do not disable the tools:

```
[ ] 1. Run tools in report-only mode; record the violation count as the baseline
[ ] 2. Configure RATCHET mode: new/changed code must be clean; the baseline
        may only shrink (most tools support baseline files; otherwise scope
        gates to changed files)
[ ] 3. Log the baseline as a watch item; burn it down opportunistically in
        files already being touched (within scope-control rules)
```

### Record the results

- AGENTS.md → Part 2 → Validation Commands: the real commands, replacing
  any # NOT CONFIGURED markers
- AGENTS.md → Part 2 → Quick Constraints: lint + test one-liners
- Decision log: tools chosen, versions, configs, the can-fail demonstrations,
  any baseline/ratchet state
- CI placeholders replaced (row 6) — "CI is green" in the Definition of Done
  is only meaningful after this

---
