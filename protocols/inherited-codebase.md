<!-- Starter Pack v11.8 — protocols/inherited-codebase.md -->
<!-- Load this file when: no Captain's Log exists and non-pack source files are present -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->


This is the case when the starter pack has been dropped into an existing repo
that was not built with this setup. The codebase exists, but there is no
`CAPTAINS_LOG.md`, no filled-in `ARCHITECTURE.md`, and no established workflow.

**The agent must not write or change any code until the full assessment is complete.**

#### Phase 1 — Read and Map (no edits)

```
[ ] 1. Read ARCHITECTURE.md and CLAUDE.md in full
[ ] 2. List the entire repo structure — every directory and file
[ ] 3. Identify and read: entry points, config files, package manifests,
        dependency lists, any existing README or docs
[ ] 4. Read the git history — see Git History Reconstruction below
[ ] 5. Scan for sensitive data — credentials, PII, API keys (see Sensitive
        Data Handling protocol). Report findings before any other work proceeds.
[ ] 6. Read the most-changed and most-central source files in full
[ ] 7. Identify the tech stack — languages, frameworks, runtimes, versions
```

#### Git History Reconstruction

For inherited codebases, the git history is a low-fidelity Captain's Log that
already exists. The agent must read and synthesize it into a reconstructed
`CAPTAINS_LOG.md` before the first live session entry is written.

**How far to go back:**
The agent judges based on repo size and history depth:
- Small repo or few commits — read the full history
- Medium repo — read until the history becomes redundant or pre-dates the
  current codebase shape (major refactors, renames, or rewrites are a natural
  stopping point)
- Large repo with hundreds of commits — focus on: the earliest commits
  (establish intent), major inflection points (large diffs, branching patterns,
  commit message tone changes), and the most recent 20-30 commits (current state)
- In all cases: read diffs for significant commits, not just messages

**Reconstruction commands:**
```bash
# Full log with dates and authors
git log --oneline --all

# Identify high-churn files (signals complexity and problem areas)
git log --all --format=format: --name-only | sort | uniq -c | sort -rg | head -20

# Read diff for a specific commit
git show [commit-hash]

# See what changed between two points
git diff [older-hash] [newer-hash] --stat
```

**Reconstructed entry format:**

Reconstructed entries use the standard Captain's Log format but are clearly
marked so any reader — human or agent — knows they were inferred from git
history rather than written live with full session context:

```markdown
## [Inferred Phase Name] — [date range: YYYY-MM-DD to YYYY-MM-DD]
> ⚠️ RECONSTRUCTED — inferred from git history, not written during a live session.
> Confidence: [High / Medium / Low] — [brief reason, e.g., "clear commit messages"
> or "sparse commits, intent inferred from diffs"]

**What was built / changed:**
- `[path/to/file.ext]` — [what changed, inferred from commits and diffs]

**Architectural decisions:**
- [Any decisions visible from commit messages or structural changes] — WHY: [inferred]

**Codebase state at end of this phase:**
- [What appeared to be working based on the code at this point in history]

**Watch items / observations:**
- [Anything notable — abandoned branches, reverted work, sudden direction changes]

---
```

Reconstructed entries are prepended oldest-first so the log reads
chronologically from bottom (oldest) to top (newest), with the first live
session entry at the very top.

#### Phase 2 — Assess and Report

After mapping, the agent must produce a written assessment covering:

```
1. Tech stack — what is confirmed present and at what versions
2. Inferred architecture — how the code is actually structured
   (even if poorly — describe what IS there, not what should be there)
3. Entry points — where execution begins, how requests/events flow
4. Problem areas — tech debt, dead code, inconsistent patterns,
   missing error handling, hardcoded values, security concerns
5. Unknown or unclear areas — anything ambiguous that needs developer input
6. Dependency health — outdated, deprecated, or abandoned packages
7. Test coverage — what is tested, what is not, whether tests pass
```

Do not soften the assessment. If the codebase is in poor shape, say so clearly
and specifically. The developer needs an honest picture before deciding what to do.

#### Phase 3 — Build Out Project Docs

After the developer has reviewed the assessment:

```
[ ] 1. Fill in the Project-Specific Architecture section of ARCHITECTURE.md
        based on what was found — actual structure, not ideal structure
[ ] 2. Fill in the Pattern Registry with any patterns that exist in the code
        (including anti-patterns worth flagging)
[ ] 3. Fill in the Tech Stack table in CLAUDE.md
[ ] 4. Fill in the File Structure section in CLAUDE.md
[ ] 5. Finalize CAPTAINS_LOG.md:
        - Reconstructed entries (from git history) are already present from Phase 1
        - Prepend a live first-session entry above them documenting:
            - The state of the codebase as inherited and assessed
            - Key findings from the assessment
            - What the developer has decided to do next
            - Watch items (known risks, problem areas to address)
        - This live entry is NOT marked as reconstructed — it was written with
          full session context and developer input
[ ] 6. Confirm the first task with the developer before writing any code
```

#### Phase 4 — Confirm and Begin

Only after Phases 1–3 are complete and the developer has confirmed the first task
should the agent write any code. From this point forward, standard session
protocols apply.

---


---
