# AI Agent Starter Pack — v13

A cross-harness agent kit whose **doctrine core is Fablized** — a charter of 12 decision
procedures distilled from watching top-tier models work, plus eight protocols that load
at phase boundaries — and whose **chassis** is the pack's project policy: guardrails,
delegation tiers, session continuity, and deterministic enforcement. One source of
truth in `core/`; everything a harness reads is generated from it.

The premise: the gap between a strong and a weak coding agent is mostly **behavior at a
small number of recurring decision points** — whether to read before writing, reproduce
before fixing, re-diagnose after two failed attempts, verify before claiming done. The
kit installs those behaviors as loadable procedure, and backs them with gates that
don't depend on the model at all.

## The layers

| Layer | What it does | Where |
|---|---|---|
| **Charter** | 12 laws + cadence + self-check tells; always loaded | `core/charter.md` → generated into every adapter |
| **Guardrails** | hard limits, confirm-first defaults, safety floor, precedence | `core/guardrails.md` |
| **Protocols (8)** | preflight · deep-debug · stuck · landing · secure-coding · destructive-ops · delegation · session-continuity | `core/protocols/` → skills, rules, or files per harness |
| **Part 2** | your project's specifics, agent-maintained; three onboarding toggles (demo gate, sizing, accessibility) that delete when off | template in `core/part2-template.md`, lives in your `AGENTS.md` |
| **Subagents** | `light-checker` (cheap rubric scans) + `reviewer` (fresh-context, consumes the landing report) | `.claude/agents/`, `.opencode/agent/`, `.codex/agents/` |
| **Deterministic gates** | `tools/land.sh` landing gate · `.githooks/pre-commit` (secrets, size, GENERATED-file guard) · notify hooks | `tools/`, `.githooks/`, `.claude/hooks/` |
| **Evals** | kit-vs-baseline behavior cases per target model | `evals/` |

## Install

**Claude Code (plugin):**

```bash
claude --plugin-dir /path/to/this/repo     # try it
# or add the repo as a marketplace source and: /plugin install agent-starter-pack
```

**Claude Code (drop-in):** copy `AGENTS.md`, `CLAUDE.md`, `docs/fablized/`,
`.claude/`, `tools/`, `.githooks/`, `templates/` into your repo root.

**Codex CLI / OpenCode / anything AGENTS.md:** copy `AGENTS.md` + `docs/fablized/`
(+ `.codex/` or `.opencode/` + `opencode.json` for permissions/agents, `tools/`,
`.githooks/`, `templates/`).

**Cursor:** `adapters/cursor/.cursor/rules/` (self-contained).
**Gemini CLI:** `adapters/gemini/GEMINI.md` + `docs/fablized/`.
**Copilot:** `adapters/copilot/.github/copilot-instructions.md` + `docs/fablized/`.
**Direct API / other harnesses:** one file from `adapters/system-prompt/` (table below).

**Every install, once per clone:**

```bash
git config core.hooksPath .githooks    # enables the pre-commit gate
```

## Context cost per adapter

Counts are words (≈ tokens × 0.74); `python tools/build.py` reprints them.

| Adapter | Words | Use when |
|---|---|---|
| `AGENTS.md` (charter + guardrails + Part 2) | ~1,794 | any file-reading harness; protocols load on demand from `docs/fablized/` |
| `fablized-full.md` | ~6,279 | direct API, ≥64k context, long tasks |
| `fablized-compact.md` | ~2,593 | tight context; digests instead of full protocols |
| `fablized-micro.md` | ~1,063 (build fails >1,200) | local/small models (Qwen 3.6-class, 8–32K): charter digest + guardrail one-liners + four protocol digests, fully inlined |
| per-skill (loads only when triggered) | 548–759 each | Claude Code / Cursor auto-loading |

**Small-model rule (important):** skill/rule **auto-triggering is a frontier-harness
feature — never assume it below that tier.** Compact and micro inline everything;
the file-referencing adapters say "open `docs/fablized/<name>.md` now" explicitly.
For weak models the discipline is carried by the deterministic gates (`land.sh`,
pre-commit), which work identically under any harness or a bare loop.

Anthropic-API-compatible endpoints (e.g. Qwen 3.7-Max) can drive Claude Code directly
via `ANTHROPIC_BASE_URL` — then the full `.claude/` asset set applies unchanged; the
micro/shell profile is for local weights and minimal harnesses.

## Tiering (delegation protocol)

- **Standard:** session model = capable; cheaper API model = light (pin it in the
  agent files + Part 2 tier map).
- **Hybrid local+API:** the local model is the **light** tier; the API model is
  capable and the reviewer — review goes *up*, never sideways.
- **Fully offline:** single-tier; the reviewer degrades to `tools/land.sh` + the
  diff-connect checklist in the delegation protocol. Machine-checked landing beats
  author self-review.

## Local endpoint (homelab) profile

The Light tier can be a single local GPU on the same box as the orchestrator.
GPU-agnostic; the shipped example values are Volta-class (V100 32GB: llama.cpp/GGUF
only, `nvidia-smi -pl` 140–180W, slow prefill / adequate decode).

- **Serve:** fill `config/local-tier/llama-server.args.example` (model path, context,
  `CUDA_VISIBLE_DEVICES`, port; `--api-key` required even on loopback; bind
  `127.0.0.1` only, never `0.0.0.0`). Run it **persistent** — a service, so the
  KV/prompt cache survives across agent turns. Slots: one heavy task, or two light
  tasks sharing the KV budget. Model files and agent workspaces belong on SSD/NVMe —
  cold-load time is part of every availability check.
- **Pick the service wrapper (human decision, no auto-detection):**
  `config/local-tier/local-tier.service` (systemd) or
  `config/local-tier/local-tier-windows.md` (NSSM, or Task Scheduler with no
  installs). **Mixed GeForce + datacenter box?** Run the per-device dual-driver test
  first: under the one Windows driver package, run `nvidia-smi` per device plus a
  small CUDA workload pinned to each device in turn; if either card misbehaves under
  the unified driver, dual-boot Linux for the serving card is the fallback. Both
  wrappers reapply the power cap at every service start — caps do not survive
  reboots.
- **Record it:** AGENTS.md Part 2 → Model Tiers gains `endpoint URL · model id ·
  auth: <path outside repo> · service name · decided YYYY-MM-DD`.
- **Dispatch:** always through `tools/delegate.sh` (health check → mkdir lock →
  timeout → BRIEFING + micro prompt → landing-format response → one JSONL metrics
  line in `var/metrics/local-tier.jsonl`, gitignored — this feeds the per-model eval
  gate). The API key is read at runtime from `~/.config/fablized/local-tier.env` —
  outside the repo, never echoed.
- **Canary:** `.claude/hooks/local-tier-canary.sh` is registered as a SessionStart
  hook — one line per session: `local tier: up|down, <model>, ~<tok/s>, <temp>`,
  with a configurable tok/s band and temperature threshold (`CANARY_MIN_TOKS`,
  `CANARY_MAX_TEMP`). It doubles as the regression detector for driver updates and
  cooling drift.
- **Host hygiene (documented, not enforced):** volume encryption (BitLocker/LUKS)
  for workspaces, briefings, transcripts, and metrics; exclude all agent working
  directories from cloud sync (OneDrive/Dropbox/Drive); loopback only. Remote/LAN
  transport is out of scope for v13 — SSH tunnel or WireGuard is the pointer if the
  endpoint ever leaves the box.
- **Sensitivity routing (delegation protocol):** privileged/local-only material is
  handled in fully local single-tier sessions — the frontier orchestrator neither
  composes nor reads those briefings; routing the payload locally does not protect
  content the orchestrator itself wrote.

## Running the evals

See `evals/README.md`. Three cases (reproduce-first, stuck-report, landing-audit),
each run **kit-vs-baseline per target model**; acceptance for any non-Claude target is
the kit arm beating the baseline arm on that model. If kit overhead hurts a small
model, prune to what pays for itself and record it as a **named build variant** —
never silently thin the doctrine.

## Editing the doctrine

Edit **only** `core/`, then:

```bash
python tools/build.py     # regenerates every adapter; fails over word budgets
```

Never hand-edit generated files (they carry a GENERATED marker; the pre-commit hook
blocks it — with one deliberate exemption: AGENTS.md, whose Part 2 is agent-maintained
per project). **Deployed projects must not run `build.py`** — it regenerates the Part 2
skeleton and would clobber a filled Part 2; rebuilding is a kit-development activity.
The word-budget gate covers the shipped skeleton only; a filled Part 2's size is
governed by its own line caps and the delete-off-blocks rule. Charter and the four Fablized protocol texts are frozen doctrine — the
sanctioned condensation surface is `core/digests.md`. After editing a full protocol,
update its digest; a drifted digest quietly forks the doctrine. Maintenance loop:
recurring failure → entry in `doctrine/failure-modes.md` → promote to a protocol step
or law only if the entry alone doesn't stop it.

## Skill-name collisions

Harnesses can ship built-in skills/commands, and other plugins can claim the same
names — a same-named skill may silently shadow the kit's. A SessionStart hook
(`.claude/hooks/skill-shadow-check.sh`, notify-only) compares the kit's skill names
against known built-ins, user-level `~/.claude/skills`, and installed plugins, and
prints one warning line on collision. Detection is best-effort (built-ins aren't
enumerable from disk); if it fires, rename the kit skill in `core/protocols/`, update
its digest heading, and rebuild. This is why the security protocol is named
`secure-coding` — `security-review` collides with a Claude Code built-in.

## Harness parity notes

- **Claude Code** gets everything: skills, subagents, notify hooks, plugin packaging.
- **OpenCode** gets permissions (`opencode.json`) + subagents; no hook system — the
  deterministic gates (`land.sh`, pre-commit) carry enforcement. Restart after adding
  agent files.
- **Codex** gets `.codex/config.toml` + subagents; no permission-ask layer for pack
  files and no hooks — same answer: the git-level gates are the floor, and the
  guardrails file is the contract. Restart after adding agent files.
- Versioning: Claude Code installs get plugin versions; every other harness pins by
  git tag (this release: `v13.0-rc1`).

## Repo map

```
core/                 SOURCE OF TRUTH: charter, guardrails, part2 template, 8 protocols, digests
tools/build.py        regenerates everything below; enforces word budgets
tools/land.sh         landing gate (validation cmds, done-check, scaffolding, banned phrases)
.githooks/pre-commit  secrets / oversize / GENERATED-file guard
AGENTS.md, CLAUDE.md, docs/fablized/, .claude/skills/, adapters/   GENERATED
.claude/agents/, .opencode/agent/, .codex/agents/                  subagents (light-checker, reviewer)
templates/BRIEFING.md delegation payload
doctrine/             failure-modes bestiary (maintenance surface), worked examples
evals/                behavior cases + fixtures + acceptance rules
```

## Why believe any of this

In A/B testing of the predecessor pack, the two reproduced wins were **day-one
architecture that held as features grew** and **an independent review catching a
shipped CSRF hole the unguided model rationalized away** — both mechanisms survive
here (sizing block; secure-coding high-miss set + reviewer agent). The honest
limits: the kit adds no reasoning depth, and compliance varies by model — test a
candidate on one real task against `doctrine/failure-modes.md` before trusting it,
or just run the evals.
