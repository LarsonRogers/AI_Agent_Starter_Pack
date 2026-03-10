<!-- Starter Pack v11.25 — protocols/sensitive-data.md -->
<!-- Load this file when: inherited repos (proactive scan) or sensitive data encountered -->
<!-- Does NOT trigger when: values are obviously synthetic (e.g., "example.com",
     "YOUR_API_KEY_HERE", "foo@bar.com", hardcoded test fixtures with no real
     credentials), or when the file is a documented sample/template with
     placeholder values only -->
<!-- Do not load unless triggered — see ARCHITECTURE.md → Protocol Index -->

## Sensitive Data Handling

### Proactive scan (inherited codebases)

During Phase 1 of the Inherited Codebase protocol, the agent must scan for
sensitive data before any other work begins:

```bash
# Common patterns to scan for
grep -rn "password\|secret\|api_key\|token\|private_key" . --include="*.py"   --include="*.js" --include="*.ts" --include="*.env" --include="*.json"
grep -rn "[0-9]{3}-[0-9]{2}-[0-9]{4}" .   # SSN pattern
grep -rn "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" .  # Email pattern
```

Report all findings to the user before proceeding. Do not proceed until the
user has acknowledged the findings and confirmed how to handle them.

### Flag on encounter

During any session, if the agent reads a file and encounters what appears to be:
- Real credentials or API keys (not placeholders)
- Personal identifying information (names, emails, phone numbers, addresses)
- Financial data or account numbers
- Proprietary business data that appears sensitive

The agent must stop and flag it:
```
"I've encountered what looks like sensitive data in [file]:
[description of what was found — do NOT reproduce the actual data]

I'd recommend [rotating these credentials / anonymizing this data /
confirming this is intentional] before continuing.

How would you like to proceed?"
```

### Hard rules — always apply

```
- Never reproduce sensitive data in the Captain's Log, commit messages,
  or any generated documentation
- Never log, print, or output credentials or PII in code unless explicitly
  required and clearly marked
- Never commit a file containing real credentials — flag it and stop
- If in doubt about whether something is sensitive, treat it as sensitive
```

---


---
