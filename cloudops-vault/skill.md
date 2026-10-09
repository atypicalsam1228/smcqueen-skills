---
name: cloudops-vault
description: "Manage the AWS CloudOps Engineer (SOA-C03) Obsidian vault — compile captures into wiki articles, query with source verification, lint for health, regenerate indexes, show status, ingest documents, extract text from PDFs, and interact with the linked NotebookLM notebook. Use when the user invokes /cloudops-vault or /vault cloudops, or asks about vault maintenance, SOA-C03 article compilation, source ingestion, PDF extraction, vault health, index regeneration, or NotebookLM for SOA-C03."
---

# AWS CloudOps Engineer Vault Manager (SOA-C03)

Manage a two-tier Obsidian knowledge base for the AWS Certified CloudOps Engineer — Associate (SOA-C03) exam. All output uses **Obsidian Flavored Markdown** — wikilinks, callouts, embeds, and typed properties.

- **Sources/** — Authoritative SOA-C03 documentation, exam guides, domain study notes. Read-only. Ground truth.
- **Wiki/** — LLM-maintained articles that cite and link back to Sources. You own this layer.

**Before writing any vault content**, read `references/VAULT-CONVENTIONS.md` for Obsidian syntax rules and `references/SOA-C03-DOMAIN-IDENTIFIERS.md` for domain/service identification.

## Configuration

```
VAULT_PATH:    C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer
GIT_DIR:       C:/Users/samue/repos/aws_cloudops_vault.git
GIT_CMD:       git --git-dir=C:/Users/samue/repos/aws_cloudops_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer
NOTEBOOKLM_ID: 806bd12a-4494-4630-9771-33fdc2f24db3
```

## SOA-C03 Domain Structure

| Directory | Exam Domain | Weight |
|-----------|-------------|--------|
| `Sources/Monitoring-Logging/` | Monitoring, Logging, and Remediation | 22% |
| `Sources/Reliability/` | Reliability and Business Continuity | 22% |
| `Sources/Deployment-Automation/` | Deployment, Provisioning, and Automation | 22% |
| `Sources/Networking/` | Networking and Content Delivery | 18% |
| `Sources/Security-Compliance/` | Security and Compliance | 16% |
| `Sources/Cost-Performance/` | Cost and Performance Optimization | integrated into Domain 1 |
| `Sources/Exam-Prep/` | Practice exams, study guides, tips | — |

## Architecture Rules (Always Enforced)

1. **Sources/ is READ-ONLY.** Never create, modify, or delete files there — except via `ingest` (adds new documents) and `extract` (creates markdown from PDFs).
2. **Wiki/ articles MUST cite Sources/.** Every claim uses an Obsidian callout with a wikilink to the source. If no source exists, use `> [!danger] NEEDS SOURCE`.
3. **Indexes are regenerated** after any content change.
4. **All Wiki notes use typed YAML frontmatter** with `sources` and `related` as link-type properties.
5. **Never summarize or paraphrase source text.** Use `> [!quote]` callouts for exact documentation language. Wiki adds context, cross-references, and exam tips.
6. **Use Obsidian Flavored Markdown.** Wikilinks (`[[]]`), embeds (`![[]]`), callouts. Never standard markdown links for internal vault files.
7. **The canonical rulebook is `CLAUDE.md` at the vault root.** This skill is the invocation interface.

## Obsidian Syntax Quick Reference

### Wikilinks

```markdown
[[SOA-C03-Domain1-Monitoring]]                                      # link to wiki note
[[Sources/Monitoring-Logging/soa-c03-domain1-monitoring-logging-remediation#CloudWatch]]
[[Sources/Exam-Prep/soa-c03-study-guide|SOA-C03 Study Guide]]
```

### Callouts

```markdown
> [!quote] SOA-C03 Exam Guide
> "Domain 1 accounts for 22% of the exam..."
> — [[Sources/Exam-Prep/soa-c03-study-guide]]

> [!danger] NEEDS SOURCE
> No authoritative source for ECS task networking. Run `/vault cloudops ingest`.

> [!warning] Citation Drift
> Wiki content conflicts with [[Sources/Networking/...]]. Needs revision.

> [!example] SOA-C03 Scenario
> CloudWatch Composite Alarm: CPU > 90% AND Latency > 2s → SNS → SSM runbook

> [!question] SOA-C03 Exam Tip
> Q: Which service tracks EC2 memory utilization natively?
> A: None — must install CloudWatch Agent for custom memory metrics.

> [!warning] Common Gotcha
> NAT Gateway is IPv4 only. IPv6 outbound from private subnet → Egress-only Internet Gateway.
```

### Callout Type Reference

| Callout | Use For |
|---------|---------|
| `> [!quote]` | Verbatim source citations |
| `> [!danger]` | Missing sources, knowledge gaps |
| `> [!warning]` | Gotchas, common mistakes, citation drift |
| `> [!example]` | Scenario walkthroughs, implementation patterns |
| `> [!info]` | Cross-service relationships, context |
| `> [!tip]` | Best practices, recommendations |
| `> [!question]` | Exam-style Q&A |
| `> [!abstract]` | Executive summaries at top of articles |

Use `> [!warning]-` or `> [!quote]-` (with minus) for foldable callouts.

## Subcommand Selection

Parse the first argument after `/cloudops-vault` (or `/vault cloudops`) to determine the subcommand:

| User invokes | Subcommand |
|---|---|
| `status` | status |
| `ingest <path>` | ingest |
| `extract [path\|all]` | extract |
| `compile` | compile |
| `query <question>` | query |
| `notebooklm <subcommand> [args]` | notebooklm |
| `lint` | lint |
| `index` | index |
| (no args) | Show available subcommands |

---

## /cloudops-vault status

Show vault statistics at a glance.

### Workflow

1. Count files per Sources/ domain subdirectory (exclude `.gitkeep`, `_index.md`).
2. Count Wiki/ articles (total + by domain tag).
3. Count Capture/ pending files.
4. Read git log/status.

```
══════════════════════════════════════════
  AWS CloudOps Engineer Vault (SOA-C03)
══════════════════════════════════════════

  Sources (Authoritative)
  ──────────────────────────────────────
  Monitoring-Logging:     N files  (22%)
  Reliability:            N files  (22%)
  Deployment-Automation:  N files  (22%)
  Networking:             N files  (18%)
  Security-Compliance:    N files  (16%)
  Cost-Performance:       N files
  Exam-Prep:              N files
  ──────────────────────────────────────
  Total:                  N source files

  Wiki (LLM-Maintained)
  ──────────────────────────────────────
  Articles:               N total

  Capture Inbox:          N files pending

  NotebookLM
  ──────────────────────────────────────
  Notebook ID:    806bd12a-4494-4630-9771-33fdc2f24db3
  Sources:        63 (as of 2026-05-03)
  Run: /cloudops-vault notebooklm status

  Git
  ──────────────────────────────────────
  Last commit:    <hash> <date> <message>
  Working tree:   clean | N modified files
══════════════════════════════════════════
```

Run git commands via:
```bash
git --git-dir=C:/Users/samue/repos/aws_cloudops_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer log -1 --oneline
git --git-dir=C:/Users/samue/repos/aws_cloudops_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer status --short
```

---

## /cloudops-vault ingest <path>

Add a user-provided document into Sources/ as an authoritative reference.

### Workflow

1. **Validate** the file exists at `<path>`. Supported: `.md`, `.pdf`, `.txt`, `.html`, `.docx`.
2. **Determine domain** using `references/SOA-C03-DOMAIN-IDENTIFIERS.md`. If ambiguous, ask:
   ```
   Which domain does this document belong to?
   1. Monitoring-Logging  (22%)
   2. Reliability         (22%)
   3. Deployment-Automation (22%)
   4. Networking          (18%)
   5. Security-Compliance (16%)
   6. Cost-Performance
   7. Exam-Prep
   8. Other (new directory)
   ```
3. **Name the file** in kebab-case. Confirm if unclear.
4. **Copy to** `VAULT_PATH/Sources/<domain>/<filename>`. Preserve the user's original.
5. **Update indexes**: domain `_index.md` + `Sources/_index.md`.
6. **Output:**
   ```
   Ingested: <filename>
      → Sources/<domain>/<filename>

   Run /cloudops-vault extract <path>  to extract text from this PDF
   Run /cloudops-vault compile         to generate Wiki articles
   ```

---

## /cloudops-vault extract [path|all]

Extract text from PDF files in Sources/ and create markdown versions alongside them.

### Workflow

1. **Determine scope**: single path, `all` (unextracted PDFs), or prompt if no arg.
2. **Classify each PDF**:
   - Run pdfplumber on page 1; if `len(text) > 100` → text-extractable; else → image-only.
3. **Text-extractable**: extract with pdfplumber, clean formatting, convert tables to markdown, add frontmatter, save as `.md` alongside the PDF.
4. **Image-only**: extract pages as PNG via PyMuPDF → save to `Attachments/extract-temp/` → Read each PNG with vision → transcribe content → save as `.md` → clean up PNGs.
5. **Frontmatter** on all extractions:
   ```yaml
   ---
   type: extracted-source
   source_pdf: "[[Sources/<domain>/filename.pdf]]"
   pages: N
   extraction_method: pdfplumber | vision
   extracted: YYYY-MM-DD
   ---
   ```
6. **Update indexes** after extraction.
7. **Always stop and show the review prompt:**
   ```
   ══════════════════════════════════════════
     Extraction complete. DO NOT compile yet.
   ══════════════════════════════════════════
     Review these files before running compile:
     - <list extracted .md files>

     Check for:
     - Garbled headings or tables
     - Near-empty files (image-only PDFs)
     - Encoding artifacts

     When ready: /cloudops-vault compile
   ══════════════════════════════════════════
   ```

---

## /cloudops-vault compile

Process the `Capture/` inbox and compile raw material into Wiki articles.

> **Never compile immediately after extraction.** Always review `.md` extraction files first and get user confirmation.

### Workflow

1. **Scan inbox.** Read all files in `VAULT_PATH/Capture/` (skip `archived/`, `.gitkeep`). If empty, exit.
2. **For each file**, identify:
   - Which SOA-C03 domain(s) it covers (use `references/SOA-C03-DOMAIN-IDENTIFIERS.md`)
   - Content type (service doc, architecture pattern, exam note, scenario walkthrough, etc.)
3. **Search existing Wiki/** for overlap via Grep. Update existing article or create new one.
4. **Create/update Wiki articles** with Obsidian conventions:
   - Typed frontmatter with `sources:` and `related:` as link properties
   - `> [!quote]` callouts for source text with wikilinks
   - `> [!question]` for exam tips and gotchas
   - `> [!warning]` for common mistake callouts
   - `> [!danger] NEEDS SOURCE` if a reference has no source file
   - `> [!info]` for cross-service relationships
5. **Archive**: move each processed file to `Capture/archived/` with date prefix `YYYY-MM-DD_`.
6. **Regenerate indexes.**
7. **Output summary:**
   ```
   ══════════════════════════════════════════
     Compile Complete
   ══════════════════════════════════════════
     Files processed:    N
     Articles created:   N
     Articles updated:   N
     NEEDS SOURCE tags:  N
   ──────────────────────────────────────────
     Run /cloudops-vault lint to check vault health
   ══════════════════════════════════════════
   ```

---

## /cloudops-vault query <question>

Search the vault, verify against authoritative sources, and return a cited answer.

### Workflow

1. **Search Wiki/** for relevant articles via Grep on key terms.
2. **Search Sources/** for authoritative text. Use `references/SOA-C03-DOMAIN-IDENTIFIERS.md` to identify correct service names.
3. **Cross-check**: if Wiki content conflicts with Sources, flag citation drift and fix the Wiki article immediately.
4. **Compose answer**:
   - Lead with practical guidance from Wiki
   - Include verbatim source quotes via `> [!quote]` callouts with wikilinks
   - Note SOA-C03 domain context (e.g., "This falls under Domain 1: Monitoring, Logging, and Remediation — 22%")
   - Add exam gotchas via `> [!warning]` where relevant
   - Flag missing sources with `> [!danger] NEEDS SOURCE`
5. **Offer to file**: if the answer adds new knowledge not already in the Wiki, ask to create a Wiki article.

---

## /cloudops-vault notebooklm <subcommand> [args]

Interact with the linked NotebookLM notebook (`806bd12a-4494-4630-9771-33fdc2f24db3`). All commands use the `-n 806bd12a-4494-4630-9771-33fdc2f24db3` flag.

### Subcommands

| Subcommand | Action |
|------------|--------|
| `status` | `notebooklm status` — show current context and source count |
| `list` | `notebooklm source list -n <ID>` — list all 63+ sources |
| `add <url-or-path>` | `notebooklm source add <url-or-path> -n <ID>` — add source |
| `ask "<question>"` | `notebooklm ask "<question>" -n <ID>` — query notebook |
| `generate <type>` | Generate artifact (study-guide, mind-map, quiz, flashcards, audio) |
| `download <type> <path>` | Download artifact to vault Sources/Exam-Prep/ |
| `sync` | Generate domain notes for all 6 SOA-C03 domains and download to Sources/ |

### notebooklm sync

The `sync` subcommand regenerates domain study notes from NotebookLM and saves them to the vault. Use when NotebookLM has new sources and you want to refresh the vault.

Workflow:
1. For each SOA-C03 domain, run `notebooklm ask` with a comprehensive domain prompt and `--save-as-note`
2. Download the report/study guide to `Sources/Exam-Prep/`
3. Write updated domain source files to `Sources/<domain>/`
4. Run compile to update Wiki articles

### Generation types available

| Type | Command | Output |
|------|---------|--------|
| Study guide | `notebooklm generate report --format study-guide` | → `Sources/Exam-Prep/soa-c03-study-guide.md` |
| Mind map | `notebooklm generate mind-map` | → `Sources/Exam-Prep/soa-c03-mind-map.md` |
| Quiz | `notebooklm generate quiz` | → `Sources/Exam-Prep/soa-c03-quiz.json` |
| Flashcards | `notebooklm generate flashcards` | → `Sources/Exam-Prep/soa-c03-flashcards.md` |
| Podcast | `notebooklm generate audio` | → download as .mp3 |

> **Ask before generating** — audio, quiz, and flashcard generation can hit rate limits.

---

## /cloudops-vault lint

Run health checks on the vault and report issues.

### Checks

1. **Orphan check**: Wiki notes with no incoming `[[wikilinks]]` from other Wiki notes.
2. **Citation drift**: `> [!quote]` callouts where the quoted text doesn't match the linked source.
3. **Missing frontmatter**: Wiki notes missing required YAML fields (`type`, `domain`, `status`, `tags`, `created`, `updated`, `sources`, `related`).
4. **Gap analysis**: Sources/ domains with zero Wiki coverage.
5. **Broken wikilinks**: `[[links]]` pointing to non-existent files.
6. **NEEDS SOURCE audit**: Count all `> [!danger] NEEDS SOURCE` callouts.
7. **Syntax check**: Flag standard markdown links used for internal files (should be `[[wikilinks]]`).
8. **Unextracted PDFs**: Sources/ PDFs with no corresponding `.md` extraction.

### Output

```
══════════════════════════════════════════
  CloudOps Vault Health Report (SOA-C03)
══════════════════════════════════════════

  Stats
  ──────────────────────────────────────
  Source files:        N (across 7 domains)
  Wiki articles:       N
  Last commit:         <date> — <message>

  Issues Found
  ──────────────────────────────────────
  Orphan notes:        N
  Citation drift:      N
  Missing frontmatter: N
  Broken wikilinks:    N
  NEEDS SOURCE tags:   N
  Non-Obsidian syntax: N
  Unextracted PDFs:    N

  Domain Gap Analysis
  ──────────────────────────────────────
  Domains with no Wiki coverage:
    - <domain> (N source files, 0 wiki articles)

  Recommendations
  ──────────────────────────────────────
  - <specific actionable suggestions>
══════════════════════════════════════════
```

---

## /cloudops-vault index

Regenerate all index files in the vault.

### Workflow

1. **VAULT-INDEX.md** (vault root): all Wiki articles grouped by domain; Sources ingestion status.
2. **Sources/_index.md**: count files per domain; mark Pending/Partial/Ingested.
3. **Wiki/_index.md**: all articles with one-line descriptions grouped by domain tag.
4. **Per-directory `_index.md`**: any directory with 2+ content files gets an `_index.md`.

---

## Frontmatter Convention

```yaml
---
type: concept
domain: monitoring-logging
status: draft
tags:
  - cloudwatch
  - composite-alarms
  - soa-c03/domain1
created: 2026-05-04
updated: 2026-05-04
sources:
  - "[[Sources/Monitoring-Logging/soa-c03-domain1-monitoring-logging-remediation]]"
related:
  - "[[Wiki/SOA-C03-Domain1-Monitoring]]"
---
```

### Domain tag values

| domain | Tags |
|--------|------|
| `monitoring-logging` | `soa-c03/domain1`, `cloudwatch`, `cloudtrail`, `x-ray` |
| `reliability` | `soa-c03/domain2`, `auto-scaling`, `disaster-recovery`, `rds` |
| `deployment-automation` | `soa-c03/domain3`, `cloudformation`, `ssm`, `cdk` |
| `networking` | `soa-c03/domain4`, `vpc`, `route53`, `cloudfront` |
| `security-compliance` | `soa-c03/domain5`, `iam`, `kms`, `guardduty` |
| `cost-performance` | `soa-c03/domain6`, `savings-plans`, `compute-optimizer` |
| `exam-prep` | `soa-c03/exam`, `practice`, `gotchas` |

## Git Workflow

After any operation that changes files:

```
Commit changes:
  git --git-dir=C:/Users/samue/repos/aws_cloudops_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer add -A
  git --git-dir=C:/Users/samue/repos/aws_cloudops_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer commit -m "description"
```

Do NOT auto-commit. The user decides when to snapshot.

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `/notebooklm` | Direct NotebookLM access; this skill's `notebooklm` subcommand wraps it |
| `/vault` | Generic vault manager; delegates to this skill for `cloudops` vault |
| `/aws-vault` | Sister vault for AIP-C01 AWS GenAI exam content |
| `/firecrawl` | Scrape AWS documentation pages into markdown for ingestion |
| `/web-research` | Research SOA-C03 topics before filing into vault |
