<!-- Starter Pack v11.5 — protocols/known-limitations.md -->
<!-- Load this file when: auditing the pack — never needed during normal agent work -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->

## Known Limitations & Deferred Decisions

This section documents intentional design tradeoffs and explicitly deferred
items. These are not bugs or oversights — they are acknowledged limitations
with recorded rationale. Reviewers and agents should not flag these as issues.

| Item | Status | Rationale |
|------|--------|-----------|
| **Platform-specific config files** (`.claude/`, `.codex/`) | Intentional | Claude Code and Codex are the primary supported agents. Config files for each are provided as-is. Other agents use the Generic Agent Path in SETUP.md. Claiming full platform neutrality would require removing useful tooling. |
| **CLI-first operational assumptions** | Intentional | The pack targets developers and technical users as primary audience. Non-dev path is supported via SETUP.md Generic Agent Path and OS appendix. Full GUI-only agent support is out of scope. |
| **PROTOCOLS.md as external dependency** | Intentional | Splitting protocols into a separate on-demand file was an explicit context-window optimization. Agents must have access to PROTOCOLS.md. If it is missing, the agent should report it and halt rather than guess. |
| **Multi-agent concurrent editing** | Deferred | Branch-per-agent and merge conflict protocols are out of scope for a starter pack. Recommended convention: one agent per branch, human-managed merges. Add if a specific project requires it. |
| **Git unavailable fallback** | Deferred | Git is a hard dependency for rollback, log reconstruction, and checkpoint strategy. Environments without git are not supported. If git is unavailable, the agent should flag it immediately and defer all file-modifying tasks. |
| **Host platform system instruction conflicts** | Out of scope | If a runtime injects system-level instructions that conflict with this pack, behavior is undefined. This pack cannot govern instructions it cannot see. |
| **Unified checklist token (REQUIRED_BEFORE_CODING)** | Deferred | Current `⚠️ REQUIRED PLACEHOLDER` labels are sufficient for human and agent detection. A machine-parseable token adds complexity for marginal gain. Revisit if programmatic placeholder scanning becomes a use case. |
| **Read-order redundancy across files** | Intentional | Some repetition across ARCHITECTURE, CLAUDE, AGENTS, README is deliberate — agents that only read one file should still get the essential behavior. Canonical source is always ARCHITECTURE.md Session Resumption; others reference it. |
| **Screenshot / visual onboarding for non-devs** | Deferred | Out of scope for a text-based pack. A companion visual guide is a reasonable future addition but outside the markdown-only constraint. |
| **Task brief duplication (ARCHITECTURE + TASK_TEMPLATE)** | Intentional | TASK_TEMPLATE.md is the working document; ARCHITECTURE.md summarizes for agent reference. Both are needed for different audiences. They are watched for drift. |
| **Read-order redundancy (raised multiple times)** | Intentional | Session start and read-order summaries appear in ARCHITECTURE, CLAUDE, AGENTS, README, and SETUP. This is deliberate — agents reading only one file should still get core behavior. Canonical source is ARCHITECTURE.md Session Resumption. This tradeoff has been reviewed and accepted across multiple audit cycles. Do not re-flag. |
| **Generic agent paste path omits AGENTS trigger table** | Accepted limitation | SETUP.md generic path tells users to paste ARCHITECTURE and CLAUDE if file access is limited. This omits AGENTS trigger table. Tradeoff: keeping paste instructions simple matters more than completeness for first-time non-CLI users. Agents following ARCHITECTURE alone will still have the Protocol Index. |
| **"Platform-neutral" vs platform-specific config files** | Intentional | Behavioral rules are platform-neutral. Integration files (.claude/, .codex/) are platform-specific adapters. These are separate concerns. CLAUDE.md now states this explicitly. The claim of neutrality applies to behavior, not tooling. |
| **Non-dev "do exactly this" single boxed flow** | Deferred | SETUP.md already has a well-structured non-dev path, first-session transcript, normal/recovery distinction, glossary, and OS appendix. A single boxed canonical flow is a marginal improvement over the current structure. Revisit if user testing shows first-time failure. |
| **Canonical copy block for read-order (raised multiple times)** | Considered and declined | Proposal: maintain one verbatim copy block and reference it everywhere. Decision: the current pointer approach (each file states the order + references ARCHITECTURE as canonical) is more resilient to file-specific context than a shared block. Accepted tradeoff documented across multiple audit cycles. |
| **Failure-path detail for non-git / no-file-read / partial placeholders** | Resolved | These are now documented as deterministic action paths in the Edge-Case Handling table above. No longer a gap. |

---

---
