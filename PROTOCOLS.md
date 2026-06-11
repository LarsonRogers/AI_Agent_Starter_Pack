# PROTOCOLS.md — Protocol Index
<!-- Starter Pack v11.51 — 2026-03-09 -->

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
| `protocols/external-research.md` | External SDK, API, platform, or framework work where behavior is version-sensitive or unverifiable |
| `protocols/external-research.md` | Web access unavailable, training data unverifiable |
| `protocols/pattern-registry.md` | Same structural approach in 2+ files touched this session, or a new approach replaced one causing bugs/confusion |
| `protocols/refactor.md` | Explicit structural improvement, no new features |
| `protocols/binary-files.md` | Binary files encountered or being committed; >1MB threshold applies at commit-time |
| `protocols/testing-strategy.md` | Writing or evaluating tests |
| `protocols/communication.md` | First session (audience detection); any non-dev or technical non-dev session; any error reported to a non-developer |
| `protocols/log-format.md` | Writing or reconstructing a log/changelog entry |
| `protocols/safe-deletion.md` | Any file deletion request |
| `protocols/code-quality.md` | Writing or modifying code (not read-only or docs-only sessions) |
| `protocols/environment.md` | Any environment-specific code or config |

---

> Total protocol content: one file per protocol, ~300–2,300 tokens each.
> Verify count: `ls protocols/ | wc -l` (see SETUP.md for expected number).
> A typical session loads 1–3 protocols: ~500–4,000 tokens beyond core.
> Loading all protocols at once is only appropriate when explicitly
> auditing the pack.
