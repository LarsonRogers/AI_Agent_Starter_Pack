<!-- Starter Pack v11.6 — protocols/pattern-registry.md -->
<!-- Load this file when: documenting a new reusable pattern before committing -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->

## Pattern Registry Maintenance

When the agent introduces a new pattern — a new way of structuring a module,
handling errors, managing state, etc. — it must document it in the
Pattern Registry before committing. The registry is a handoff artifact,
not an afterthought.

**Target location:** `ARCHITECTURE.md` → Pattern Registry section.

**Required template — use exactly this format, one block per pattern:**

```
### [Pattern Name]
Purpose:      [One sentence: what problem this solves]
Location:     [File path of the canonical example]
Usage:        [How to apply it — what to do]
Anti-pattern: [What NOT to do instead — must be specific]
```

**Minimum bar for a pattern to be registered:**
- It is used or will be used in more than one place, OR
- It replaced a previous approach that was causing bugs or confusion

**Do not register:** one-off solutions, obvious language idioms, or
anything already covered by an existing pattern entry.

---
