<!-- Starter Pack v11.30 — protocols/edge-cases.md -->
<!-- Load this file when: pack files missing, git unavailable, no file-read, no file-write, placeholder conflicts, CAPTAINS_LOG missing/corrupt -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->

## Edge-Case Handling

**Does NOT trigger for:** ordinary ambiguity that a single clarifying question
resolves (e.g., a missing placeholder value where the user can simply provide it).
Edge-case protocol is for structural failures — missing files, unavailable tools,
irreconcilable conflicts — not routine clarification needs.

Deterministic action paths for common failure scenarios. Load this section
when any of the trigger conditions below are encountered.

| Situation | Deterministic action |
|-----------|---------------------|
| **CAPTAINS_LOG.md empty (zero-byte or no entries)** | Treat as corrupt — same behavior as missing. Proceed to session type detection (file-presence rule). Do not attempt to parse or resume from an empty log. |
| **CAPTAINS_LOG.md missing or corrupt** | Treat as no-log session. Run session type detection (file-presence rule). If non-pack files exist → Inherited Codebase Protocol. If no source files → First Session. Do not attempt to repair a corrupt log — note it and start fresh. |
| **Single protocol file missing from protocols/** | Halt when the missing protocol is triggered. Report exactly which file is missing: "protocols/[filename].md is missing. I need it to proceed with [situation]. Please restore it from the original pack zip." Do not guess or reconstruct the protocol behavior. If unsure which file is missing, run `ls protocols/` and compare against the expected count in SETUP.md. |
| **Multiple protocol files missing from protocols/** | Halt immediately regardless of trigger state. Report all missing files by listing what is present vs expected: "The following protocol files are missing: [list]. The pack may have been copied incompletely. Please restore the full protocols/ directory from the original pack zip before continuing." Do not attempt to work around missing protocols or proceed with partial coverage. |
| **PROTOCOLS.md missing** | Halt immediately. Report: "PROTOCOLS.md is missing from the repo root. Several required procedures are unavailable. Please restore it from the original pack zip before continuing." Do not attempt to guess or reconstruct protocol behavior. |
| **ARCHITECTURE.md or CLAUDE.md missing** | Halt immediately. Report which file is missing and ask the user to restore it. These are the primary instruction sources — proceeding without them produces undefined behavior. |
| **No git installed or git unavailable** | Report clearly what is unavailable: commits, rollbacks, history reconstruction, checkpoint strategy, and refactor protocol all require git. Offer read-only analysis and planning work only. Do not attempt to simulate git with manual file copies. |
| **No file-write capability (read works, writes fail)** | Pivot immediately to analysis and planning mode only. Do not attempt edits or commits — report each intended change as: "I would do X — please execute this manually or switch to a write-capable environment." Continue providing analysis, review, and task planning. Notify the user at session start: "I can read and analyze but cannot write files in this environment. I will describe all changes for you to apply manually." |
| **No file-read capability (web/paste-only agent)** | Ask the user to paste AGENTS.md, then ARCHITECTURE.md, then CLAUDE.md in order. Proceed from pasted content. When a protocol is triggered, ask the user to paste the relevant `protocols/[filename].md` file directly — this is the supported path in paste-only sessions. If the user cannot provide the protocol file, flag the gap clearly: state which protocol was triggered, what behavior it governs, and that you will proceed with best-effort interpretation based on ARCHITECTURE.md guardrails only. Do not halt the session solely because a protocol file could not be loaded via file-read. |
| **Partially filled REQUIRED placeholders** | Do not proceed with coding tasks. Report exactly which placeholders remain unfilled. Offer to infer any missing values from repo context, or ask the user directly for values that cannot be inferred. Never assume a placeholder value silently. |
| **Conflicting inferred placeholder values** | Present all candidates to the user with source for each: "I found two possible project names: 'foo' (from package.json) and 'bar' (from README). Which is correct?" Wait for explicit choice before writing. |
| **Pack version mismatch detected** | See "Pack version consistency check" section in ARCHITECTURE.md — halt and report. |

