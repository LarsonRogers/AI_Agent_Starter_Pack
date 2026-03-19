# PROTOCOLS.md — Protocol Index
<!-- Starter Pack v11.36 — 2026-03-09 -->

> **For AI coding agents:** This file is a routing index only.
> Each protocol lives in its own file in the `protocols/` directory.
> Load only the file triggered by your current situation.
> Do not load protocol files speculatively — see trigger conditions below.
> The canonical trigger table with full conditions is in
> `ARCHITECTURE.md` → Protocol Index.

---

## Available Protocols

| Protocol file | Load when |
|---------------|-----------|
| `protocols/conflict-examples.md` | Surfacing a conflict or verifying conflict behavior |
| `protocols/edge-cases.md` | Pack files missing, git unavailable, no file-read, no file-write, placeholder conflicts, CAPTAINS_LOG missing/corrupt |
| `protocols/known-limitations.md` | Auditing the pack — never during normal work |
| `protocols/read-only.md` | Review, audit, analysis — no edits intended |
| `protocols/inherited-codebase.md` | No Captain's Log, non-pack source files present |
| `protocols/placeholder-inference.md` | First session, any type — fills REQUIRED placeholders |
| `protocols/context-window.md` | 5+ tasks in session or detected context degradation |
| `protocols/cross-cutting.md` | Task touches 3+ files, crosses architectural layers, or involves rename/move/structural reorganization |
| `protocols/sensitive-data.md` | Inherited repos (proactive) or sensitive data encountered |
| `protocols/stuck-loop.md` | 3 failed attempts on the same problem |
| `protocols/validation-fallback.md` | Lint, test, or CI commands missing or unconfigured |
| `protocols/external-research.md` | External SDK, API, or platform work |
| `protocols/external-research.md` | Web access unavailable, training data unverifiable |
| `protocols/pattern-registry.md` | Documenting a new reusable pattern before committing |
| `protocols/refactor.md` | Explicit structural improvement, no new features |
| `protocols/binary-files.md` | Binary or large files (>1MB) encountered or committed |
| `protocols/testing-strategy.md` | Writing or evaluating tests |

---

> Total protocol content: one file per protocol, ~300–1,900 tokens each.
> Verify count: `ls protocols/ | wc -l` (see SETUP.md for expected number).
> A typical session loads 1–3 protocols: ~500–4,000 tokens beyond core.
> Loading this index file costs ~400 tokens. Loading all protocols at once
> would cost ~11,800 tokens — only do this if explicitly auditing the pack.
