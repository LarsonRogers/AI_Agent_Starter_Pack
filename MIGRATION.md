# Migrating a v12.x project to v13

v13 retired the old upgrade protocol machinery (version greps, upgrade.md); this one
page replaces it. The build itself now does the careful part.

## The path

1. **Replace the pack files** in your project with the v13 set (copy in `core/`,
   `tools/`, `docs/fablized/`, `.claude/`, `.githooks/`, `templates/`,
   `adapters/` as needed for your harness — see README → Install).
2. **Run `python tools/build.py`.** The build is Part-2-safe: it detects your filled
   `# Part 2 — Project Specifics (agent-maintained)` section (v12 uses this exact
   heading) and **preserves it verbatim**, regenerating only Part 1 — the old policy
   prose is replaced by the v13 charter + guardrails around your untouched project
   specifics.
3. `git config core.hooksPath .githooks` (once per clone) to enable the commit gate.

## What to expect

- **Refusal, not guessing:** the build refuses (named reason, nonzero exit) only if
  that Part 2 heading is missing or renamed in your AGENTS.md — restore the heading
  and rerun. `--force-part2` exists but is the **destructive** overwrite-with-skeleton
  path; don't use it on a project whose Part 2 you want to keep.
- **New v13 fields stay absent until you say yes:** a preserved v12 Part 2 lacks the
  v13 tier-map endpoint fields. Leave them absent — the probe-then-offer onboarding
  treats a missing endpoint as unresolved and resolves it interactively at session
  start (probes localhost for Ollama / llama-server / LM Studio / vLLM, proposes what
  it finds, or asks the tier question once). Nothing writes Part 2 without your yes.
- **Windows / CRLF checkouts:** if git normalized your AGENTS.md to CRLF, the
  preserved Part 2 comes back LF-normalized — content-identical, line endings only.

## Remaining manual steps

- Delete the old `protocols/` directory (superseded by `docs/fablized/` +
  `.claude/skills/`; the old files would otherwise sit as dead references).
- If you customized `.claude/settings.json` or `opencode.json`, diff your versions
  against the v13 ones and merge your edits forward (permission rules you added,
  allowlists, etc.).
- `DECISION_LOG.md` and `HANDOFF.md` are untouched by design — your history and
  resume state carry straight through.
