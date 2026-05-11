---
name: exam-notebooklm
description: "Stage 1 of the exam prep pipeline. Sets up and populates a NotebookLM notebook for any certification exam. Ingests official exam guide, task statements, in-scope services, and community intel sources. Outputs a ready-to-query notebook ID for use with /exam-prep."
---

# Exam NotebookLM — Certification Source Ingestion

Sets up a NotebookLM notebook for a certification exam and ingests all authoritative sources. Run this before `/exam-prep` when starting a new exam or adding sources to an existing notebook.

## Configuration

```
NOTEBOOKS_REGISTRY: ~/.claude/skills/exam-notebooklm/notebooks.json
```

The registry persists exam → notebook_id mappings across sessions so you never lose track of which notebook belongs to which exam.

## Subcommands

| Subcommand | Purpose |
|---|---|
| `status [exam]` | Show notebook status, source count, processing state |
| `create <exam_name>` | Create a new notebook and register it |
| `add <exam> <url-or-path>` | Add a source to an exam's notebook |
| `add-intel <exam>` | Add community/Reddit intel sources interactively |
| `list <exam>` | List all sources in an exam's notebook |
| `verify <exam>` | Confirm all sources are READY (not processing) |
| `register <exam> <notebook_id>` | Register an existing notebook ID to an exam name |

---

## /exam-notebooklm status [exam]

Shows the current state of a registered notebook.

### Workflow

1. Run `notebooklm status` — verify CLI is authenticated
2. If `[exam]` provided, look up notebook_id from `notebooks.json`
3. Run `notebooklm source list -n <notebook_id> --json`
4. Report: notebook title, total sources, READY vs. PROCESSING counts

### Output

```
Notebook: AWS CloudOps Engineer SOA-C03 Exam Guide and Updates
ID: 806bd12a-4494-4630-9771-33fdc2f24db3
Sources: 63 total — 63 READY, 0 PROCESSING
Status: ✓ Ready for /exam-prep
```

---

## /exam-notebooklm create <exam_name>

Creates a new NotebookLM notebook and registers it.

### Workflow

1. Run `notebooklm status` — verify auth; if failing, tell user to run `notebooklm login`
2. Run `notebooklm create "<exam_name> Exam Prep" --json` — capture notebook_id
3. Read `notebooks.json` (create if missing); add entry: `{ "exam_name": "<exam_name>", "notebook_id": "<id>", "created": "<date>" }`
4. Write updated `notebooks.json`
5. Output notebook ID and confirm registration

### Output

```
Created notebook: AWS AZ-900 Exam Prep
Notebook ID: abc12345-...
Registered in notebooks.json as: AZ-900
Next step: /exam-notebooklm add AZ-900 <url-or-path>
```

---

## /exam-notebooklm add <exam> <url-or-path>

Adds a single source to an exam's notebook.

### Workflow

1. Look up notebook_id for `<exam>` from `notebooks.json`
2. Run `notebooklm source add "<url-or-path>" -n <notebook_id> --json`
3. Capture source_id and initial status
4. Report: source title, processing status

### Recommended Sources for AWS Exams

Add these in order:
```
1. Official exam guide PDF          — d1.awsstatic.com/training-and-certification/...
2. Official sample questions PDF    — d1.awsstatic.com/training-and-certification/...
3. Official in-scope services page  — docs.aws.amazon.com/aws-certification/...
4. AWS documentation per domain     — docs.aws.amazon.com/[service]/latest/userguide/
5. Community intel (Reddit posts, dev.to passing stories)
6. Tutorials Dojo or Neal Davis prep content (if available as URLs)
```

---

## /exam-notebooklm add-intel <exam>

Guides the user through adding community intel sources interactively.

### Workflow

1. Prompt: "Paste URLs for community intel sources (Reddit threads, dev.to posts, passing stories). One per line. Press Enter twice when done."
2. For each URL: `notebooklm source add "<url>" -n <notebook_id>`
3. After all added: `notebooklm source list -n <notebook_id>` — show updated count
4. Tip: "Reddit r/AWSCertifications, dev.to passing stories, and makeexams.com strategy guides are the highest-signal intel sources."

---

## /exam-notebooklm verify <exam>

Confirms all sources finished processing before running `/exam-prep`.

### Workflow

1. Run `notebooklm source list -n <notebook_id> --json`
2. Check status field for each source
3. If any PROCESSING: report count and advise waiting 1-5 minutes
4. If all READY: confirm notebook is ready for `/exam-prep`

### Output

```
✓ All 63 sources are READY
Notebook: 806bd12a-4494-4630-9771-33fdc2f24db3
Ready for: /exam-prep SOA-C03 generate all
```

---

## /exam-notebooklm register <exam> <notebook_id>

Registers an existing NotebookLM notebook (created via web UI or previous session).

### Workflow

1. Run `notebooklm source list -n <notebook_id>` — verify notebook exists and is accessible
2. Add to `notebooks.json`: `{ "exam_name": "<exam>", "notebook_id": "<notebook_id>" }`
3. Run `notebooklm status -n <notebook_id>` — capture title and source count
4. Confirm registration

**Example — registering the SOA-C03 notebook:**
```
/exam-notebooklm register SOA-C03 806bd12a-4494-4630-9771-33fdc2f24db3
```

---

## notebooks.json Format

```json
{
  "notebooks": [
    {
      "exam": "SOA-C03",
      "name": "AWS Certified CloudOps Engineer Associate",
      "notebook_id": "806bd12a-4494-4630-9771-33fdc2f24db3",
      "created": "2026-05-11",
      "source_count": 63
    }
  ]
}
```

---

## Related Skills

- `/exam-prep` — Uses the notebook created here to generate a full study guide
- `/exam-quiz` — Uses the notebook to generate practice questions
- `/cloudops-vault` — Vault manager for the SOA-C03 Obsidian vault (includes its own `notebooklm` subcommand for SOA-C03 specifically)

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| "Auth/cookie error" | Session expired | `notebooklm login` |
| "No notebook context" | notebook_id not set | Use `-n <id>` flag or `notebooklm use <id>` |
| Source stuck PROCESSING | Large PDF / slow ingestion | Wait 5-10 min, re-run `/exam-notebooklm verify` |
| "No result found for RPC ID" | Rate limiting | Wait 5-10 min and retry |
