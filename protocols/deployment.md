<!-- Starter Pack v11.51 — protocols/deployment.md -->
<!-- Load this file when: the user EXPLICITLY asks to deploy, publish, host, or
     share the app by link. OPT-IN ONLY. -->
<!-- Does NOT trigger when: the user asks to run, demo, or test the app (that is
     protocols/run-demo.md — local-run is the default path). The agent never
     proposes deployment as the default next step. -->
<!-- Do not load unless triggered — see AGENTS.md → Protocol Index -->

## Deployment Protocol (opt-in)

Local-run is the pack's default endpoint. Deployment happens only when the
user asks for it in their own words ("put this online", "give me a link I
can share", "deploy it"). The agent may mention that deployment is possible
when the user asks "how do I show this to someone?" — but the user chooses.

### Step 0 — Data-sensitivity gate (BEFORE any deploy step)

Answer from what the app actually does, not from intentions:

```
Does the app collect, store, process, or display ANY of:
- personal data about real people (names, emails, messages, photos, location)
- credentials, tokens, or keys of any kind
- business-confidential or client information
- health, financial, or other regulated data
- content the user has not explicitly agreed to make public
```

**If YES to any, or UNCERTAIN → HALT.**

```
"Before I help put this online: the app handles [specific data]. Once
deployed, that data lives on [provider]'s servers and may be reachable by
anyone with the link. This needs human review before any public deploy —
someone (you, or someone you trust who knows about data handling) must
explicitly sign off on:
  1. what data will live on the server,
  2. who can reach it, and
  3. that this is acceptable.
I can't make that call for you. I'll proceed only after you confirm that
review has happened."
```

Do not proceed on "it's fine, go ahead" alone if the data involves people
other than the user — restate what is at stake once, then require the
explicit confirmation. Record the gate outcome (what data, who reviewed,
what was confirmed) in the development log before any deploy command runs.

**If NO to all → proceed to Step 1.** Record the assessment ("no
sensitive data: app stores only [X]") in the development log.

### Step 1 — Choose the simplest viable target

- Prefer: static hosting for static apps; the stack's mainstream
  platform-as-a-service otherwise. Optimize for free tier, no
  server-administration burden, and easy deletion.
- Present ONE recommendation in plain English (what it is, what it costs,
  what account the user must create) plus at most one alternative if there
  is a genuine trade-off.
- Creating accounts, adding deploy configs, and CI/CD changes are
  default-policy confirm items — list them before starting.

### Step 2 — Deploy

- The user creates the account and owns the credentials; the agent never
  receives or stores them (hard guardrail). Auth flows that need a human
  (logins, dashboard clicks) are the user's steps — the agent writes them
  out RUNBOOK-style.
- Environment variables and secrets go through the provider's secret
  storage, never into the repo.
- After deploy: run the full-demo procedure (protocols/run-demo.md) against
  the live URL — the user must see the deployed version run.

### Step 3 — Record and extend the runbook

- Add a `## Deployed version` section to RUNBOOK.md: the URL, how to
  redeploy, how to take it DOWN (deletion path is mandatory — the user must
  always know how to turn it off).
- Development log entry: provider, what was deployed, gate outcome,
  redeploy/teardown steps.

---
