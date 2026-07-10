# AI Agent Starter Pack — v13.1.0-dev

A cross-harness agent kit whose **doctrine core is Fablized** — a charter of 12 decision
procedures distilled from watching top-tier models work, plus eight protocols that load
at phase boundaries — and whose **chassis** is the pack's project policy: guardrails,
delegation tiers, session continuity, and deterministic enforcement. One source of
truth in `core/`; everything a harness reads is generated from it.

The premise: a large part of the gap between strong and weak coding-agent performance is
**behavior at recurring decision points** — whether to generate alternatives before
anchoring, choose a discriminating observation, read before writing, reproduce before
fixing, re-diagnose after failed attempts, and try to disconfirm a result. The kit cannot
increase a model's intrinsic capability; it elicits and audits better reasoning actions,
then measures whether those actions improve executable outcomes.

## The layers

| Layer | What it does | Where |
|---|---|---|
| **Charter** | 12 laws + cadence + self-check tells; always loaded | `core/charter.md` → generated into every adapter |
| **Guardrails** | hard limits, confirm-first defaults, safety floor, precedence | `core/guardrails.md` |
| **Protocols (8)** | preflight · deep-debug · stuck · landing · secure-coding · destructive-ops · delegation · session-continuity | `core/protocols/` → skills, rules, or files per harness |
| **Part 2** | your project's specifics, agent-maintained; three onboarding toggles (demo gate, sizing, accessibility) that delete when off | template in `core/part2-template.md`, lives in your `AGENTS.md` |
| **Subagents** | `light-checker` (cheap rubric scans) + `reviewer` (fresh-context, consumes the landing report) | `.claude/agents/`, `.opencode/agent/`, `.codex/agents/` |
| **Deterministic gates** | cross-platform `tools/land.py` · pre-commit secrets/size/generated checks · notify hooks | `tools/`, `.githooks/`, `.claude/hooks/` |
| **Evals** | automated kit-vs-baseline grading of tool order, protected files, repo state, and hidden behavior | `evals/` |

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

Runtime tools require Python 3.11+. Shell entry points are compatibility wrappers; on
Windows, run `python tools/land.py` and `python tools/delegate.py` directly—WSL is not
required. Default harness configs keep network, shell, and edits ask-first; loosen them
only after recording a project-specific decision.

### Universality boundary

The canonical layer is plain Markdown in `core/` and has no provider dependency. Python
standard-library gates work without Claude, Codex, OpenCode, GitHub, or a network. Harness
configs, hooks, agents, and CI files are replaceable edge adapters generated or copied from
that core. Unsupported harnesses use `AGENTS.md` + protocol files or a system-prompt profile;
non-GitHub projects replace the CI template while keeping the same local gates. Provider-
specific behavior must not leak back into doctrine or behavioral graders.

**Every install, once per clone:**

```bash
git config core.hooksPath .githooks    # enables the pre-commit gate
python tools/validate_repo.py
python tools/build.py --check
```

## Context cost per adapter

Counts are words (≈ tokens × 0.74); `python tools/build.py` reprints them.

| Adapter | Words | Use when |
|---|---|---|
| `AGENTS.md` (charter + guardrails + Part 2) | ~1,796 | file-reading harnesses; protocols load on demand |
| `fablized-full.md` | ~7,230 | direct API, ≥64k context, full protocols |
| `fablized-compact.md` | ~2,815 | constrained context; full charter + protocol digests |
| `fablized-micro.md` | ~358 (build fails >800) | local/small models: one named reasoning/safety action loop, fully inlined |
| `fablized-micro-{bugfix,investigation,landing}.md` | ≤400 each | one task class per prompt, ends in a literal output skeleton; dispatched via `delegate.py --task-class` |
| per-skill (loads only when triggered) | 548–988 each | frontier harness auto-loading |

**Small-model rule (important):** skill/rule **auto-triggering is a frontier-harness
feature — never assume it below that tier.** Compact and micro inline their procedures;
the file-referencing adapters say "open `docs/fablized/<name>.md` now" explicitly.
The micro profile is a named condensation in `core/digests.md`, not an ad hoc truncation.
For weak models, Python landing and git-level gates provide the enforcement floor.

Anthropic-API-compatible endpoints (e.g. Qwen 3.7-Max) can drive Claude Code directly
via `ANTHROPIC_BASE_URL` — then the full `.claude/` asset set applies unchanged; the
micro profile is for local weights and minimal harnesses.

Preflight also checks the current harness's installed tools and skills. It uses a relevant
installed skill when useful and recommends an uninstalled skill only when the expected
correctness or verification benefit justifies the interruption; installation always needs
user approval. Provider catalogs remain lazy edge files (for Codex, see
`.codex/optional-skills.md`) so they do not tax every model's context.

## Tiering (delegation protocol)

- **Standard:** session model = capable; cheaper API model = light (pin it in the
  agent files + Part 2 tier map).
- **Hybrid local+API:** the local model is the **light** tier; the API model is
  capable and the reviewer — review goes *up*, never sideways.
- **Fully offline:** single-tier; the reviewer degrades to `python tools/land.py` + the
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
- **Dispatch:** always through `python tools/delegate.py` (health check → directory lock →
  timeout → BRIEFING + micro prompt → landing-format response → one JSONL metrics
  line in `var/metrics/local-tier.jsonl`, gitignored — this feeds the per-model eval
  gate). Pass `--task-class bugfix|investigation|landing` to swap the universal micro
  for that class's slice; the response is then verified fail-closed against the slice
  skeleton — a fabricated run-claim, missing deliverable, or untagged output exits 5
  with metrics status `rejected` and never counts as a result. A strict `KEY=VALUE`
  parser reads the API key from
  `~/.config/fablized/local-tier.env`; it never executes the file. Transport rejects
  non-loopback URLs, and Python holds credentials and briefing payloads in-process rather
  than exposing them as command arguments.
- **Canary:** `.claude/hooks/local-tier-canary.sh` is registered as a SessionStart
  hook — one line per session: `local tier: up|down, <model>, ~<tok/s>, <temp>`,
  with a configurable tok/s band and temperature threshold (`CANARY_MIN_TOKS`,
  `CANARY_MAX_TEMP`). It doubles as the regression detector for driver updates and
  cooling drift.
- **Host hygiene (documented, not enforced):** volume encryption (BitLocker/LUKS)
  for workspaces, briefings, transcripts, and metrics; exclude all agent working
  directories from cloud sync (OneDrive/Dropbox/Drive); loopback only. Remote/LAN
  transport is out of scope for v13.1 — SSH tunnel or WireGuard is the pointer if the
  endpoint ever leaves the box.
- **Sensitivity routing (delegation protocol) — three classes:** *open* (route
  normally) · *obfuscation-floored* (egress only via scrub → residual-verify →
  preview/confirm → send → rehydrate; surviving high-risk tokens block the send;
  cloud off-by-default, enablements logged — a contract the pack states, implemented
  externally) · *local-only* (the frontier orchestrator neither composes nor reads
  the briefing; routing the payload locally does not protect content the
  orchestrator itself wrote).
- **Endpoint onboarding (probe-then-offer):** with no endpoint recorded in Part 2,
  the canary's `--discover` mode probes localhost 11434 (Ollama), 8080
  (llama-server), 1234 (LM Studio), 8000 (vLLM), identifies server + models, and
  the agent proposes recording the hit as the Light tier — ask-first, never a
  silent Part 2 write. The single ask-once tier question fires only when no probe
  answers. Hookless harnesses run the same probe via the session-continuity
  protocol.
- **Reference implementation:** the pack ships interfaces, not services. The
  reference homelab is **windows-llm-lab-ulysses** (`local_ai`): serving registry +
  swap manager (`tiers.yaml`), the class-2 obfuscation floor
  (`cloud/obfuscate.py` block-on-residual, `cloud/escalation.py` gates),
  eval-gated tier promotion, a retrieval tier, and a dashboard. The interfaces this pack
  owns and that implementation consumes: the endpoint contract above, the
  `var/metrics/local-tier.jsonl` schema (timestamp, task id, model, tokens in/out,
  duration, status), and the three routing classes.

## Running the evals

See `evals/README.md` and run `python evals/run_evals.py --model <id> --profile <name>`.
The automated runner uses fresh fixtures per arm and grades executable oracles, protected
files, tool order, and report meaning. Acceptance requires no baseline regression, at least
one kit lift, and the named context budget. Small-model changes must earn their token cost;
condense only through a named digest/profile and rerun both arms.

## Editing the doctrine

Edit **only** `core/`, then:

```bash
python tools/build.py     # regenerates every adapter; fails over word budgets
python tools/build.py --check  # CI/pre-commit drift check; writes nothing
```

Never hand-edit generated files (they carry a GENERATED marker; the pre-commit hook
blocks it — with one deliberate exemption: AGENTS.md, whose Part 2 is agent-maintained
per project). `build.py` is **Part-2-safe**: if the existing AGENTS.md holds a filled
(non-skeleton) Part 2, a rebuild preserves it byte-for-byte and regenerates only
Part 1 (charter + guardrails); if the Part 2 heading can't be found at all, the build
refuses with a named reason rather than guess the boundary. `--force-part2` is the
explicit overwrite-with-skeleton path. The word-budget gate always evaluates the
shipped skeleton composition; a filled Part 2's size is governed by its own line caps
and the delete-off-blocks rule. Charter and the four Fablized protocol texts are frozen doctrine — the
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
`secure-coding` — its original name collided with a same-named Claude Code built-in
(the exact case the check's built-ins list still watches for).

## Harness parity notes

- **Claude Code** gets everything: skills, subagents, notify hooks, plugin packaging.
- **OpenCode** gets ask-first permissions (`opencode.json`) + subagents; no hook system —
  Python landing and pre-commit carry enforcement. Restart after adding
  agent files.
- **Codex** gets `.codex/config.toml` + subagents with workspace-write, network-off, and
  on-request approval defaults; it has no pack hooks, so Python landing + pre-commit remain
  the deterministic floor. Restart after adding agent files.
- **Pi / picode** loads AGENTS.md and skills natively — no separate adapter; the
  system-prompt adapter is the fallback. Caveat: Pi has no built-in permission
  system, so privileged work under Pi runs sandboxed (container/micro-VM) and
  relies on the Python landing + git-hook floor for enforcement.
- Versioning: Claude Code installs get plugin versions; every other harness pins by
  git tag. Development version: `13.1.0-dev`; `VERSION`, plugin metadata, and README are
  checked together by CI. Upgrading a v12.x project: see MIGRATION.md.

## Repo map

```
core/                 SOURCE OF TRUTH: charter, guardrails, part2 template, 8 protocols, digests
tools/build.py        regenerates everything below; enforces word budgets
tools/land.py         cross-platform landing gate; land.sh is a compatibility wrapper
tools/delegate.py     loopback-only local-tier transport; delegate.sh wraps it
tools/validate_repo.py metadata, config, action-pin, and line-ending validation
tools/pre_commit.py   cross-platform staged secrets / size / generated-output guard
.githooks/pre-commit  thin Git wrapper for tools/pre_commit.py
adapters/system-prompt/profiles.json generated word counts + hard budgets consumed by evals
AGENTS.md, CLAUDE.md, docs/fablized/, .claude/skills/, adapters/   GENERATED
.claude/agents/, .opencode/agent/, .codex/agents/                  subagents (light-checker, reviewer)
templates/BRIEFING.md delegation payload
doctrine/             failure-modes bestiary (maintenance surface), worked examples
evals/                automated A/B runner, graders, fixtures, current + historical results
```

`land.py` never executes commands read from `AGENTS.md` implicitly. Inspect the configured
lint/format/typecheck/test commands, then pass `--run-configured` (or set
`LAND_RUN_CONFIGURED=1`) in a trusted project. Claude's post-edit hook follows the same rule;
`FABLIZED_RUN_CONFIGURED_HOOKS=1` is an explicit project opt-in.

## Why believe any of this

In predecessor A/B work, reproduced wins included architecture that survived later growth
and an independent review catching a CSRF hole the unguided model rationalized away. The
v13 transcript results were candid but ceremony-heavy and showed the local micro profile
failing 3/3 without a baseline. They remain historical evidence, not validation of v13.1.

The current claim is narrower and testable: the pack attempts to improve reasoning
**performance** by generating alternatives, choosing discriminating observations, and
trying to falsify conclusions. It cannot make a model intrinsically smarter. Trust a
model/profile only after the automated behavior-first kit-vs-baseline gate shows lift on
that exact target without context-cost regression.
