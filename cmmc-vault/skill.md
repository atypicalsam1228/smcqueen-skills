---
name: cmmc-vault
description: "Manage the CMMC knowledge Obsidian vault — compile captures into wiki articles, query with source verification, lint for health, regenerate indexes, show status, ingest documents, and extract text from PDFs. Use when the user invokes /cmmc-vault or asks about CMMC vault maintenance, article compilation, source ingestion, PDF extraction, vault health, or index regeneration."
---

# CMMC Knowledge Vault Manager

Manage a two-tier CMMC (Cybersecurity Maturity Model Certification) knowledge base stored as an Obsidian vault. All output uses **Obsidian Flavored Markdown** — wikilinks, callouts, embeds, and typed properties.

- **Sources/** — Authoritative CMMC model documents, NIST publications, DoD policy, assessment guides. Read-only. Ground truth.
- **Wiki/** — LLM-maintained articles that cite and link back to Sources. You own this layer.

**Before writing any vault content**, read `references/VAULT-CONVENTIONS.md` for Obsidian syntax rules and `references/CMMC-PRACTICE-IDENTIFIERS.md` for practice domain/ID formats.

## Configuration

```
VAULT_PATH: C:/Users/samue/OneDrive/Obsidian/CMMC_Vault
GIT_DIR: C:/Users/samue/repos/cmmc_vault.git
GIT_CMD: git --git-dir=C:/Users/samue/repos/cmmc_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/CMMC_Vault
```

> **To adapt for another user:** Change `VAULT_PATH` and `GIT_DIR` above. Everything else is relative to `VAULT_PATH`.

## Architecture Rules (Always Enforced)

1. **Sources/ is READ-ONLY.** Never create, modify, or delete files there — except via `ingest` (adds new documents) and `extract` (creates markdown from PDFs).
2. **Wiki/ articles MUST cite Sources/.** Every practice or policy reference uses an Obsidian callout with a wikilink to the source. If no source exists yet, use a `[!danger]` callout with `NEEDS SOURCE`.
3. **Indexes are regenerated** after any content change.
4. **All Wiki notes use typed YAML frontmatter** with `sources` and `related` as link-type properties (see Frontmatter section).
5. **Never summarize or paraphrase source text.** Use `> [!quote]` callouts for exact documentation language. The Wiki adds context, cross-references, assessment tips, and implementation guidance — not restatements.
6. **Use Obsidian Flavored Markdown.** Wikilinks (`[[]]`) for internal links, embeds (`![[]]`) for inline source content, callouts for structured annotations. Never use standard markdown links for internal vault files.
7. **The canonical rulebook is `CLAUDE.md` at the vault root.** Read it if you need the full operating manual. This skill is the invocation interface.

## Obsidian Syntax Quick Reference

### Wikilinks (always use for internal references)

```markdown
[[ac-access-control-overview]]                                  # link to wiki note
[[Sources/NIST-800-171/sp800-171r2#3.1 Access Control|AC]]     # link to source heading
[[Sources/Exam-Prep/ccp-course-workbook|CCP Workbook]]          # display text
```

### Embeds (inline source content)

```markdown
![[Sources/NIST-800-171/sp800-171r2#3.1 Access Control]]
```

### Callouts (knowledge signals)

```markdown
> [!quote] NIST SP 800-171 Rev 2
> "Limit system access to authorized users, processes acting on behalf of authorized users,
> and devices (including other systems)."
> — [[Sources/NIST-800-171/sp800-171r2#3.1.1|AC.1.001 Source]]

> [!danger] NEEDS SOURCE
> No authoritative source for CMMC Level 3 delta requirements. Ingest via `/cmmc-vault ingest`.

> [!warning] Citation Drift
> Wiki content conflicts with [[Sources/CMMC-Model/cmmc-model-v2-0]]. Needs revision.

> [!example] Implementation Guidance
> Implement MFA for all privileged accounts using PIV/CAC or software token (TOTP).

> [!info] Cross-Domain
> Maps to: AC (access control policies), IA (MFA requirements), AU (logon audit events)

> [!question] CCP Exam Tip
> Q: Which CMMC practice requires limiting system access to authorized users?
> A: AC.1.001 — maps to NIST SP 800-171 3.1.1.
```

### Callout type reference

| Callout | Use For |
|---|---|
| `> [!quote]` | Verbatim source citations |
| `> [!danger]` | Missing sources, knowledge gaps |
| `> [!warning]` | Citation drift, stale content |
| `> [!example]` | Implementation patterns, SSP language |
| `> [!info]` | Cross-domain relationships, context |
| `> [!tip]` | Best practices, assessment tips |
| `> [!question]` | Exam-style questions and answers |
| `> [!abstract]` | Executive summaries at top of articles |

Use `> [!quote]-` (with minus) for foldable long source quotations.

## Subcommand Selection

Parse the first argument after `/cmmc-vault` to determine the subcommand:

| User invokes | Subcommand |
|---|---|
| `/cmmc-vault compile` | compile |
| `/cmmc-vault query <question>` | query |
| `/cmmc-vault lint` | lint |
| `/cmmc-vault index` | index |
| `/cmmc-vault status` | status |
| `/cmmc-vault ingest <path>` | ingest |
| `/cmmc-vault extract [path\|all]` | extract |
| `/cmmc-vault` (no args) | Show available subcommands |

If no subcommand is given or it's unrecognized, show the list with one-line descriptions and ask the user to pick one.

ARGUMENTS are passed after the subcommand name. Parse them from the skill invocation args.

---

## /cmmc-vault compile

Process the `Capture/` inbox and compile raw material into Wiki articles.

> [!warning] Review Extractions Before Compiling
> **Never compile immediately after extraction.** Always review `.md` extraction files first:
> - Check that headings, tables, and key content extracted correctly
> - Large PDFs (>100 pages) may have artifacts or encoding issues
> - Image-only PDFs will have near-empty extractions — re-extract with vision before compiling
> - Only proceed with compile once the user confirms extractions look accurate

### Workflow

1. **Scan inbox.** Read all files in `VAULT_PATH/Capture/` (skip `archived/` and `.gitkeep`).
   - If Capture/ is empty, report "Nothing to compile" and exit.

2. **For each file**, identify:
   - Which CMMC practice domain(s) it relates to (use `references/CMMC-PRACTICE-IDENTIFIERS.md` to match domain abbreviations and practice IDs)
   - What type of content it is (CMMC model requirement, NIST control, assessment evidence, exam notes, SSP guidance, etc.)
   - Which CMMC level(s) it covers (Level 1 / Level 2 / Level 3)
   - Whether it is CCP/CCA exam-relevant

3. **Search existing Wiki articles** for overlap:
   - Use Grep to find related content in `VAULT_PATH/Wiki/`
   - If a relevant article exists, update it with new information
   - If no relevant article exists, create a new one

4. **Create/update Wiki articles** using Obsidian conventions:
   - Use typed frontmatter with `sources:` and `related:` as link properties
   - Every practice or policy reference uses a `> [!quote]` callout with a wikilink:
     ```markdown
     > [!quote] NIST SP 800-171 Rev 2
     > "Limit system access to authorized users, processes acting on behalf of authorized users..."
     > — [[Sources/NIST-800-171/sp800-171r2#3.1.1|3.1.1 Access Control]]
     ```
   - If no source file exists for a reference, use a danger callout:
     ```markdown
     > [!danger] NEEDS SOURCE: AC.1.001
     > No authoritative source document ingested for this practice.
     > Run `/cmmc-vault ingest` to add the source.
     ```
   - For exam-related content, use `> [!question]` callouts and tag with `exam-prep/ccp` or `exam-prep/cca`
   - Use wikilinks (`[[related-article]]`) for all internal cross-references
   - Add cross-domain mappings using `> [!info]` callouts
   - Place files in `Wiki/` — create subdirectories when a topic accumulates 3+ notes

5. **Archive processed captures:**
   - Move each processed file to `Capture/archived/` with date prefix: `2026-04-27_original-filename.md`

6. **Regenerate indexes** (run the index subcommand workflow).

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
     Run /cmmc-vault lint to check vault health
     Commit changes when ready
   ══════════════════════════════════════════
   ```

---

## /cmmc-vault query <question>

Search the vault, verify against authoritative sources, and return a cited answer.

### Workflow

1. **Search Wiki/** for relevant articles:
   - Use Grep with the question's key terms against `VAULT_PATH/Wiki/`
   - Read matching articles for context

2. **Search Sources/** for authoritative text:
   - Use Grep against `VAULT_PATH/Sources/` for practice IDs, domain names, key terms
   - Use `references/CMMC-PRACTICE-IDENTIFIERS.md` to identify the correct domain and practice IDs
   - Read matching source passages

3. **Cross-check:** If Wiki content conflicts with Sources, flag the drift:
   ```
   > [!warning] Citation Drift Detected
   > Wiki article "xyz.md" says X, but Sources say Y.
   > Updating wiki article to match authoritative source.
   ```
   Fix the Wiki article immediately.

4. **Compose answer:**
   - Lead with practical guidance from Wiki articles
   - Include verbatim source quotes using `> [!quote]` callouts with wikilinks
   - Note cross-domain implications using `> [!info]` callouts
   - When question is exam-related, include CCP/CCA domain context (e.g., "This falls under CMMC Domain: Access Control (AC)")
   - If sources are missing, use `> [!danger] NEEDS SOURCE` callouts

5. **Offer to file:** If the answer adds new knowledge not already in the Wiki, ask:
   ```
   This answer contains new insights. File it as a Wiki article? (y/n)
   ```
   If yes, create the article following compile workflow conventions with full Obsidian syntax.

---

## /cmmc-vault lint

Run health checks on the vault and report issues.

### Checks

1. **Orphan check:** Find Wiki notes with no incoming `[[wikilinks]]` from other Wiki notes.
   - Grep all Wiki files for `[[filename]]` patterns, compare against list of all Wiki files.

2. **Citation drift:** For each Wiki article that quotes Sources/:
   - Extract quoted text from `> [!quote]` callouts
   - Read the referenced Source file via the wikilink
   - Flag any quotes that don't match the source text

3. **Missing frontmatter:** Check all Wiki notes have required YAML fields:
   - `type`, `domain`, `cmmc-level`, `status`, `tags`, `created`, `updated`, `sources`, `related`
   - Verify `sources` and `related` use wikilink format (`"[[...]]"`)
   - Report files missing any required field

4. **Gap analysis:** List Sources/ domains that have zero Wiki coverage:
   - For each domain directory in Sources/ with files (not just .gitkeep), check if any Wiki article references it
   - Report uncovered domains and specific source files with no Wiki citations

5. **Broken links:** Find `[[wikilinks]]` pointing to non-existent files.

6. **NEEDS SOURCE audit:** Find all `> [!danger] NEEDS SOURCE` callouts in Wiki articles.

7. **Syntax check:** Verify Wiki articles use Obsidian conventions:
   - Flag standard markdown links `[text](path.md)` used for internal vault files (should be `[[wikilinks]]`)
   - Flag source citations not using `> [!quote]` callout format

8. **Unextracted PDFs:** Scan Sources/ for `.pdf` files that have no corresponding `.md` extraction alongside them.
   - Report count and suggest running `/cmmc-vault extract all`.

9. **Output report:**
   ```
   ══════════════════════════════════════════
     CMMC Vault Health Report
   ══════════════════════════════════════════

     Stats
     ──────────────────────────────────────
     Source files:        N (across N domains)
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

     Gap Analysis
     ──────────────────────────────────────
     Domains with no Wiki coverage:
       - NIST-800-172 (N source files, 0 wiki articles)
       - ...

     Recommendations
     ──────────────────────────────────────
     - <specific actionable suggestions>
   ══════════════════════════════════════════
   ```

---

## /cmmc-vault index

Regenerate all index files in the vault.

### Workflow

1. **VAULT-INDEX.md** (vault root):
   - List all Wiki articles grouped by domain, with one-line summaries
   - Use wikilinks: `- [[Wiki/article-name]] — one-line description`
   - List Sources ingestion status per domain (file count)
   - Include quick reference links to subcommands

2. **Sources/_index.md:**
   - Update the ingestion status table: count files per domain directory (exclude .gitkeep, _index.md)
   - Mark domains as "Pending" (0 files), "Partial" (some files), or "Ingested" (comprehensive)

3. **Wiki/_index.md:**
   - List all Wiki articles with one-line descriptions using wikilinks
   - Group by domain tag from frontmatter

4. **Per-directory _index.md:**
   - For any directory under Wiki/ or Sources/ with 2+ content files (not .gitkeep), create or update `_index.md`
   - Format: `- [[filename]] — one-line description`

5. **Output:** Report how many index files were created/updated.

---

## /cmmc-vault status

Show vault statistics at a glance.

### Workflow

1. **Count files** in each directory:
   - Sources: count per domain subdirectory (exclude .gitkeep and _index.md)
   - Wiki: count total articles and group by domain frontmatter tag
   - Capture: count pending files in inbox

2. **Coverage matrix:**
   ```
   ══════════════════════════════════════════
     CMMC Vault Status
   ══════════════════════════════════════════

     Sources (Authoritative)
     ──────────────────────────────────────
     CMMC-Model:        N files
     NIST-800-171:      N files
     NIST-800-172:      N files
     Assessment-Guides: N files
     DoD-Policy:        N files
     CUI-Categories:    N files
     Exam-Prep:         N files
     ──────────────────────────────────────
     Total:             N source files

     Wiki (LLM-Maintained)
     ──────────────────────────────────────
     Articles:          N total
       access-control:           N
       asset-management:         N
       audit-accountability:     N
       configuration-management: N
       identification-auth:      N
       incident-response:        N
       maintenance:              N
       media-protection:         N
       personnel-security:       N
       physical-protection:      N
       recovery:                 N
       risk-management:          N
       security-assessment:      N
       situational-awareness:    N
       system-comms-protection:  N
       system-info-integrity:    N
       cui-handling:             N
       assessment-prep:          N
       cross-domain:             N

     Capture Inbox:    N files pending

     Git
     ──────────────────────────────────────
     Last commit:      <hash> <date>
                       <message>
     Working tree:     clean | N modified files
   ══════════════════════════════════════════
   ```

3. Read git log and status via:
   ```bash
   git --git-dir=C:/Users/samue/repos/cmmc_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/CMMC_Vault log -1 --oneline
   git --git-dir=C:/Users/samue/repos/cmmc_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/CMMC_Vault status --short
   ```

---

## /cmmc-vault ingest <path>

Add a user-provided document into Sources/ as an authoritative reference.

This is one of two exceptions to the "never modify Sources/" rule — it adds new documents the user has downloaded or created.

### Workflow

1. **Validate** the file exists at `<path>`.
   - If not found, report the error and exit.
   - Supported formats: `.md`, `.pdf`, `.txt`, `.html`, `.docx`
   - For non-markdown formats, note the format — PDFs can be extracted later with `/cmmc-vault extract`.

2. **Determine domain:**
   - Use `references/CMMC-PRACTICE-IDENTIFIERS.md` to match practice domains in the content
   - Inspect filename and content for domain indicators (CMMC, NIST, CUI, DFARS, assessment, exam, etc.)
   - If ambiguous, ask the user:
     ```
     Which domain does this document belong to?
     1. CMMC-Model
     2. NIST-800-171
     3. NIST-800-172
     4. Assessment-Guides
     5. DoD-Policy
     6. CUI-Categories
     7. Exam-Prep
     8. Other (new domain directory)
     ```

3. **Name the file:**
   - Convert to kebab-case: `cmmc-model-v2-0.pdf`
   - If the user provided a good name, keep it (just kebab-case it)
   - Ensure the name is wikilink-friendly (no special characters that break `[[links]]`)
   - Confirm with user if the name is unclear

4. **Copy to Sources/:**
   - Copy (not move — preserve the user's original) to `VAULT_PATH/Sources/<domain>/<filename>`
   - If "Other" domain, create the new directory under Sources/

5. **Update indexes:**
   - Update the domain's `_index.md` with the new file entry using wikilinks
   - Update `Sources/_index.md` if this is the first file for a domain (Pending → Partial)

6. **Output:**
   ```
   Ingested: <filename>
      -> Sources/<domain>/<filename>

   Run /cmmc-vault extract <path> to extract text from this PDF
   Run /cmmc-vault compile to generate Wiki articles
   Commit changes when ready
   ```

---

## /cmmc-vault extract [path|all]

Extract text content from PDF files in Sources/ and create markdown versions alongside the originals.

This is the second exception to the "never modify Sources/" rule — it creates `.md` extractions of PDF source documents.

### Workflow

1. **Determine scope:**
   - If `<path>` argument given: extract that single PDF
   - If `all` argument given: find all `.pdf` files under `Sources/` that lack a corresponding `.md` file (same name, `.md` extension)
   - If no argument: list unextracted PDFs with count and ask user to choose `all` or a specific path

2. **For each PDF, classify extraction method:**
   Run a Python snippet to test:
   ```python
   import pdfplumber
   with pdfplumber.open(pdf_path) as pdf:
       text = pdf.pages[0].extract_text() if pdf.pages else ""
       has_text = len(text or "") > 100
   ```
   - If `has_text` is True: classify as **text-extractable** (use pdfplumber)
   - If `has_text` is False: classify as **image-only** (use PyMuPDF + Claude vision)

3. **Text-extractable PDFs** (e.g., `sp800-171r2.pdf`):
   - Extract all pages with pdfplumber:
     ```python
     import pdfplumber
     with pdfplumber.open(pdf_path) as pdf:
         for page in pdf.pages:
             text = page.extract_text()
             tables = page.extract_tables()
     ```
   - Clean up formatting: preserve headings, lists, tables
   - Convert tables to markdown table format where detected
   - Add YAML frontmatter:
     ```yaml
     ---
     type: extracted-source
     source_pdf: "[[Sources/<domain>/filename.pdf]]"
     pages: N
     extraction_method: pdfplumber
     extracted: 2026-04-27
     ---
     ```
   - Save as `.md` alongside the PDF (same directory, same base name)

4. **Image-only PDFs** (screenshot captures, scanned documents):
   - Extract each page as PNG using PyMuPDF:
     ```python
     import fitz
     doc = fitz.open(pdf_path)
     for i, page in enumerate(doc):
         pix = page.get_pixmap(dpi=200)
         pix.save(output_path)
     ```
   - Save PNGs to `VAULT_PATH/Attachments/extract-temp/`
   - Read each PNG using Claude's Read tool (vision capability) to transcribe visible text
   - For exam question screenshots:
     - Structure content using `> [!question]` and `> [!example]` callouts
     - Capture the question text, all answer choices, and any explanations visible
   - For course/workbook screenshots:
     - Capture content, diagrams descriptions, key concepts, practice requirements
   - Combine all pages into a single `.md` file
   - Add YAML frontmatter:
     ```yaml
     ---
     type: extracted-source
     source_pdf: "[[Sources/<domain>/filename.pdf]]"
     pages: N
     extraction_method: vision
     extracted: 2026-04-27
     ---
     ```
   - Save alongside the PDF (same directory)
   - Clean up temp PNGs from `Attachments/extract-temp/`

5. **Filename shortening for screenshot/capture PDFs:**
   - Long filenames with random suffixes get shortened:
     - `Certified-CMMC-Professional-CCP-Course-Workbook-*` → `ccp-course-workbook.md`
     - `CCP-Addl-Practices-Questions-*` → `ccp-additional-practice-questions.md`
     - `CMMC-Assessment-Process-CAP-*` → `cmmc-assessment-process-cap.md`
     - `DigitalDistro_CCP-Field-Guide-*` → `ccp-field-guide-exam-prep.md`
     - `CCP-Class-Links-*` → `ccp-class-links.md`
   - The `source_pdf:` frontmatter field preserves the link to the original

6. **Update indexes:**
   - Update the domain directory's `_index.md` with new `.md` entries
   - Update `Sources/_index.md` file counts

7. **Output summary:**
   ```
   ══════════════════════════════════════════
     Extract Complete
   ══════════════════════════════════════════
     PDFs processed:       N
     Text-extracted:       N  (via pdfplumber)
     Vision-extracted:     N  (via PyMuPDF + Claude vision)
     Pages processed:      N total
     Markdown files created: N
   ──────────────────────────────────────────
     Run /cmmc-vault compile to generate Wiki articles
     from extracted content
     Commit changes when ready
   ══════════════════════════════════════════
   ```

---

## Frontmatter Convention

All Wiki notes use this YAML frontmatter with Obsidian-typed properties:

```yaml
---
type: concept
domain: access-control
cmmc-level: level-2
status: draft
tags:
  - access-control
  - AC.1.001
  - nist-800-171
created: 2026-04-27
updated: 2026-04-27
sources:
  - "[[Sources/NIST-800-171/sp800-171r2]]"
  - "[[Sources/CMMC-Model/cmmc-model-v2-0]]"
related:
  - "[[Wiki/ac-access-control-overview]]"
  - "[[Wiki/ia-identification-authentication]]"
---
```

### Property types

| Property | Obsidian Type | Values |
|---|---|---|
| `type` | text | concept, pattern, practice-overview, architecture, exam-note, guide, ssp-template, session-log |
| `domain` | text | access-control, asset-management, audit-accountability, configuration-management, identification-auth, incident-response, maintenance, media-protection, personnel-security, physical-protection, recovery, risk-management, security-assessment, situational-awareness, system-comms-protection, system-info-integrity, cui-handling, assessment-prep, cross-domain |
| `cmmc-level` | text | level-1, level-2, level-3, all-levels |
| `status` | text | draft, review, final |
| `tags` | list | Freeform, hierarchical allowed (e.g., `access-control/AC.1.001`) |
| `created` | date | YYYY-MM-DD |
| `updated` | date | YYYY-MM-DD |
| `sources` | links | Wikilinks to Sources/ files — renders in graph view |
| `related` | links | Wikilinks to other Wiki articles — renders in graph view |

The `sources` and `related` link properties make source-to-wiki relationships visible in Obsidian's **graph view**.

## File Naming

- Kebab-case: `ac-access-control-overview.md`
- Prefix with domain abbreviation for practice-specific notes: `ac-`, `ia-`, `cm-`, etc.
- Atomic: one concept per note
- Descriptive: filename communicates content without opening
- Wikilink-friendly: avoid special characters that break `[[links]]`
- Prefer flat/shallow over deep nesting

## Git Workflow

After any operation that changes files, remind the user:

```
Commit changes:
   git --git-dir=C:/Users/samue/repos/cmmc_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/CMMC_Vault add -A
   git --git-dir=C:/Users/samue/repos/cmmc_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/CMMC_Vault commit -m "description"
```

Do NOT auto-commit. The user decides when to snapshot.

## Related Skills

| Skill | Relationship |
|---|---|
| `/fedramp` | Cross-reference for FedRAMP/CMMC control overlaps |
| `/nist-800-53` | Cross-reference NIST 800-53 controls that map to CMMC practices |
| `/rmf-vault` | Sister vault for broader RMF/compliance content |
| `/web-research` | Research CMMC topics, DoD memos, and CMMC-AB updates online |
| `/firecrawl` | Scrape CMMC-AB, NIST, and DoD documentation pages into markdown |
| `/notebooklm` | Analyze and enrich source material before compilation |
| `/aws-vault` | Sister vault for AWS cloud content relevant to FedRAMP/CMMC cloud implementations |
| `defuddle` | Clean markdown extraction from government doc pages |

## Obsidian Skills

The vault includes Obsidian Skills from `kepano/obsidian-skills` at `.claude/obsidian-skills/`. These teach proper Obsidian syntax:

- **obsidian-markdown** — Wikilinks, embeds, callouts, properties, tags
- **obsidian-bases** — Database-like `.base` files with filters and formulas
- **json-canvas** — Visual canvas files for mind maps and flowcharts
- **obsidian-cli** — Vault interaction via command line
- **defuddle** — Clean web page extraction

When creating complex vault features (e.g., a CMMC practice tracker dashboard), reference the appropriate obsidian-skill for syntax details.
