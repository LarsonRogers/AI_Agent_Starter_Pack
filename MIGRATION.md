# Migrating to v13.1

Supported paths:

- **v12.x → v13.1 directly** — no intermediate v13.0 checkout is required. Follow the
  v12.x path, then the v13.0 additions that apply to your selected adapters.
- **v13.0 → v13.1** — follow the short adapter/runtime list below.
- **v12.x → exact v13.0** — pin tag `v13.0` and use the `MIGRATION.md` shipped at that tag.

## From v13.0

1. Copy the new Python runtime tools and keep the `.sh` files only as compatibility
   wrappers. Use `python tools/land.py`, `python tools/delegate.py`, and
   `python tools/local_tier_canary.py` on Windows or any host without Bash.
2. Copy `config/local-tier/local-tier.env.example` to the user config location and keep
   only supported `LOCAL_TIER_*` / `CANARY_*` keys. The file is parsed as inert data; move
   service-only variables such as `LLAMA_API_KEY` to the separate service environment file.
3. Review the safer harness defaults before replacing local policy: network, edits, shell,
   and web access now ask first or start disabled.
4. Replace downstream CI with `templates/agent-ci.yml`; the pack repository's active CI now
   validates the pack itself. Run `python tools/build.py --check` in both CI and pre-commit.
5. Treat old `evals/results.md` as historical. Use `python evals/run_evals.py` for
   behavior-first kit-vs-baseline results on each deployed model/profile.

## From v12.x

v13 retired the old upgrade protocol machinery (version greps, upgrade.md); this one
page replaces it. The build itself now does the careful part.

## The path

1. **Replace the pack files** in your project with the current v13.1 set (copy in `core/`,
   `tools/`, `docs/fablized/`, `.claude/`, `.githooks/`, `templates/`,
   `adapters/` as needed for your harness — see README → Install).
2. **Run `python tools/build.py`.** The build is Part-2-safe: it detects your filled
   `# Part 2 — Project Specifics (agent-maintained)` section (v12 uses this exact
   heading) and **preserves it verbatim**, regenerating only Part 1 — the old policy
   prose is replaced by the v13 charter + guardrails around your untouched project
   specifics.
3. `git config core.hooksPath .githooks` (once per clone) to enable the commit gate.
4. Run `python tools/validate_repo.py` and `python tools/build.py --check` before
   accepting the migration diff.

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

- After confirming a clean rollback commit, remove the old `protocols/` directory
  (superseded by `docs/fablized/` + `.claude/skills/`; otherwise it remains as dead
  and potentially conflicting guidance).
- If you customized `.claude/settings.json` or `opencode.json`, diff your versions
  against the v13 ones and merge your edits forward (permission rules you added,
  allowlists, etc.).
- `DECISION_LOG.md` and `HANDOFF.md` are untouched by design — your history and
  resume state carry straight through.
