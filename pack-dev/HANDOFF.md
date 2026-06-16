# Handoff — AI Agent Starter Pack (pack development)
<!-- PACK-DEV ARTIFACT: tracks development of the pack itself. Not a template;
     never copied into deployed projects (see pack-dev/README.md). This repo's
     logs live in pack-dev/ because the repo IS the pack source — deployed
     projects keep theirs at the project root. Overwritten per task. -->

**As of:** 2026-06-16 · **Pack version:** v12.14 · **Audience mode:** Developer
**Latest (v12.14):** Added a shared **Requirement Pressure-Test** (`protocols/requirements.md`) — a bounded, audience-scaled interrogation that surfaces risky unknowns (assumptions, edges, failure modes, conflicts, hidden deps, concrete success) BEFORE committing to a build/change. Harness-neutral (the portable technique, NOT the Claude-only grill-me skill). Invoked from three callers with a per-context lens + gate: product-definition Step 1b (always), inherited-codebase Phase 2b (after assessment), and large/ambiguous/cross-cutting task briefs (gated, not universal). Protocols 31→32. Independent review APPROVE, 0 blockers.
**Prior:** v12.13 access-method caveat; v12.12 proactive ask-once tier-map offer. Root cause of "OpenCode never spawns lower-tier sub-agents": tier setup lived only in on-demand `model-tiering.md`, so a plain session never triggered it. Fix: an always-on clause in `AGENTS.md` Session Start (piggybacked on the existing Pack-profile read) offers tiering **once** when the Light row is still a bare `[placeholder]`; a real model or `none — single-tier (decided YYYY-MM-DD)` is resolved → silent; read-only skipped. "Resolved" is defined once (Part 2 comment); the decline path in `model-tiering.md` writes the dated sentinel (durable anti-nag). Independent review APPROVE, 0 blockers (1 minor fixed). The activation machinery itself is already confirmed working live (the user's OpenCode ran it end-to-end in their separate project).

**Confirmed next task:** ask the user — no build task queued. The model-tiering arc is feature-complete (correct mechanism → shipped templates → agent-driven activation → proactive offer → baked-in update source).

**Branch:** `main` — v12.14 committing now; will be ahead of origin until pushed. Pushing needs user confirmation.

**Open watch items (OPEN — none silently closed):**
- **Tiering post-restart confirmation:** activation is now confirmed live in OpenCode (file created, model set, Model Tiers updated); the only remaining bit is verifying that after restart the primary actually *delegates a bounded scan to* the Light agent — the user is eyeballing this in their project.
- Notify-hook live-fire: the hook's own `curl` to the baked-in Pack source URL is unexercised (sandbox-blocked here); URL-extraction + reachability + compare all verified.
- Requirement Pressure-Test (v12.14) is prose-verified only — no live run yet against a real vague idea / inherited change / big task brief to confirm it surfaces real unknowns WITHOUT nagging (watch the Non-dev audience-scaling especially).
- KEY VALIDATION (blocked on rig): full pack on a real quantized 12B at 8-16k under LEAN.
- upgrade.md prose-verified only — no end-to-end migration dry-run against a real older-version project.
- PROBE 2 (opencode.json edit-ask live-fire), PROBE 3 (semgrep CI on first push).
- Accepted wart: the pack-dev repo's own Part 2 ships as placeholders (it's the template), so the new offer fires every pack-dev session and can't be resolved without polluting the template — the maintainer just declines.

**Resume prompt (paste into any agent):**

    This is the pack-development repo (branch `main`; `revised` retired); its
    own logs live in pack-dev/. Read AGENTS.md, then pack-dev/HANDOFF.md, then
    the last entries of pack-dev/DECISION_LOG.md as needed. v12.12: session start
    now PROACTIVELY offers tier-map setup once (ask-once, recorded-state anti-nag)
    when the Light row is an unfilled [placeholder] — closing the gap where agents
    sat silently single-tier. The model-tiering arc is feature-complete. No build
    task queued — ask the user. Open: post-restart delegation confirmation +
    notify-hook live-fire. main will be ahead of origin after this commit; pushing
    needs user confirmation.
