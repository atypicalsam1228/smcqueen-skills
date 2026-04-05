---
name: rmf-vault
description: "Manage the RMF compliance Obsidian vault — compile captures into wiki articles, query with source verification, lint for health, regenerate indexes, show status, and ingest documents. Use when the user invokes /rmf-vault or asks about vault maintenance, compliance article compilation, source ingestion, vault health, or index regeneration."
---

# RMF Compliance Vault Manager

Manage a two-tier compliance knowledge base stored as an Obsidian vault. All output uses **Obsidian Flavored Markdown** — wikilinks, callouts, embeds, and typed properties.

- **Sources/** — Authoritative policy text (NIST, FedRAMP, OWASP). Read-only. Ground truth.
- **Wiki/** — LLM-maintained articles that cite and link back to Sources. You own this layer.

**Before writing any vault content**, read `references/VAULT-CONVENTIONS.md` for Obsidian syntax rules and `references/FRAMEWORK-IDENTIFIERS.md` for control ID formats.

## Configuration

```
VAULT_PATH: C:/Users/samue/OneDrive/Obsidian/rmf_obsidian
GIT_DIR: C:/Users/samue/repos/rmf_obsidian.git
GIT_CMD: git --git-dir=C:/Users/samue/repos/rmf_obsidian.git --work-tree=C:/Users/samue/OneDrive/Obsidian/rmf_obsidian
```

> **To adapt for another user:** Change `VAULT_PATH` and `GIT_DIR` above. Everything else is relative to `VAULT_PATH`.

## Architecture Rules (Always Enforced)

1. **Sources/ is READ-ONLY.** Never create, modify, or delete files there — except via the `ingest` subcommand which adds new documents.
2. **Wiki/ articles MUST cite Sources/.** Every claim or control reference uses an Obsidian callout with a wikilink to the source. If no source exists yet, use a `[!danger]` callout with `NEEDS SOURCE`.
3. **Indexes are regenerated** after any content change.
4. **All Wiki notes use typed YAML frontmatter** with `sources` and `related` as link-type properties (see Frontmatter section).
5. **Never summarize or paraphrase source text.** Use `> [!quote]` callouts for exact policy language. The Wiki adds context, cross-references, and implementation guidance — not restatements.
6. **Use Obsidian Flavored Markdown.** Wikilinks (`[[]]`) for internal links, embeds (`![[]]`) for inline source content, callouts for structured annotations. Never use standard markdown links for internal vault files.
7. **The canonical rulebook is `CLAUDE.md` at the vault root.** Read it if you need the full operating manual. This skill is the invocation interface.

## Obsidian Syntax Quick Reference

### Wikilinks (always use for internal references)

```markdown
[[least-privilege-implementation]]                         # link to wiki note
[[Sources/NIST-800-53/AC-access-control#AC-2|AC-2]]       # link to source heading
[[Sources/NIST-800-53/AC-access-control|AC Access Control]] # display text
```

### Embeds (inline source content)

```markdown
![[Sources/NIST-800-53/AC-access-control#AC-2 Account Management]]
```

### Callouts (compliance signals)

```markdown
> [!quote] NIST 800-53 AC-2
> "The organization manages information system accounts..."
> — [[Sources/NIST-800-53/AC-access-control#AC-2|AC-2]]

> [!danger] NEEDS SOURCE
> No authoritative source for OWASP LLM03. Ingest via `/rmf-vault ingest`.

> [!warning] Citation Drift
> Wiki content conflicts with [[Sources/NIST-800-53/AC-6]]. Needs revision.

> [!example] AWS Implementation
> Enforce least privilege using IAM permission boundaries.

> [!info] Cross-Framework Mapping
> Maps to: FedRAMP Moderate AC-6, 800-171 3.1.5, OWASP LLM06
```

### Callout type reference

| Callout | Use For |
|---|---|
| `> [!quote]` | Verbatim source citations |
| `> [!danger]` | Missing sources, compliance gaps |
| `> [!warning]` | Citation drift, stale content |
| `> [!example]` | Implementation patterns, AWS examples |
| `> [!info]` | Cross-framework mappings, context |
| `> [!tip]` | Best practices, recommendations |
| `> [!abstract]` | Executive summaries at top of articles |

Use `> [!quote]-` (with minus) for foldable long source quotations.

## Subcommand Selection

Parse the first argument after `/rmf-vault` to determine the subcommand:

| User invokes | Subcommand |
|---|---|
| `/rmf-vault compile` | compile |
| `/rmf-vault query <question>` | query |
| `/rmf-vault lint` | lint |
| `/rmf-vault index` | index |
| `/rmf-vault status` | status |
| `/rmf-vault ingest <path>` | ingest |
| `/rmf-vault` (no args) | Show available subcommands |

If no subcommand is given or it's unrecognized, show the list with one-line descriptions and ask the user to pick one.

ARGUMENTS are passed after the subcommand name. Parse them from the skill invocation args.

---

## /rmf-vault compile

Process the `Capture/` inbox and compile raw material into Wiki articles.

### Workflow

1. **Scan inbox.** Read all files in `VAULT_PATH/Capture/` (skip `archived/` and `.gitkeep`).
   - If Capture/ is empty, report "Nothing to compile" and exit.

2. **For each file**, identify:
   - Which framework(s) it relates to (use `references/FRAMEWORK-IDENTIFIERS.md` to match control IDs)
   - What type of content it is (control description, implementation pattern, policy excerpt, research notes, etc.)

3. **Search existing Wiki articles** for overlap:
   - Use Grep to find related content in `VAULT_PATH/Wiki/`
   - If a relevant article exists, update it with new information
   - If no relevant article exists, create a new one

4. **Create/update Wiki articles** using Obsidian conventions:
   - Use typed frontmatter with `sources:` and `related:` as link properties
   - Every control or requirement reference uses a `> [!quote]` callout with a wikilink:
     ```markdown
     > [!quote] NIST 800-53 AC-2
     > "The organization manages information system accounts, including establishing,
     > activating, modifying, reviewing, disabling, and removing accounts."
     > — [[Sources/NIST-800-53/AC-access-control#AC-2 Account Management|AC-2]]
     ```
   - If no source file exists for a reference, use a danger callout:
     ```markdown
     > [!danger] NEEDS SOURCE: NIST 800-53 AC-2
     > No authoritative source document ingested for this control.
     > Run `/rmf-vault ingest` to add the source.
     ```
   - Use wikilinks (`[[related-article]]`) for all internal cross-references
   - Add cross-framework mappings using `> [!info]` callouts
   - Place files in `Wiki/` — create subdirectories when a topic accumulates 3+ notes

5. **Archive processed captures:**
   - Move each processed file to `Capture/archived/` with date prefix: `2026-04-05_original-filename.md`

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
     Run /rmf-vault lint to check vault health
     Commit changes: use the bare repo git command
   ══════════════════════════════════════════
   ```

---

## /rmf-vault query <question>

Search the vault, verify against authoritative sources, and return a cited answer.

### Workflow

1. **Search Wiki/** for relevant articles:
   - Use Grep with the question's key terms against `VAULT_PATH/Wiki/`
   - Read matching articles for context

2. **Search Sources/** for authoritative text:
   - Use Grep against `VAULT_PATH/Sources/` for control IDs, key terms, framework-specific language
   - Use `references/FRAMEWORK-IDENTIFIERS.md` to identify the correct ID format
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
   - Note cross-framework implications using `> [!info]` callouts
   - If sources are missing, use `> [!danger] NEEDS SOURCE` callouts

5. **Offer to file:** If the answer adds new knowledge not already in the Wiki, ask:
   ```
   This answer contains new insights. File it as a Wiki article? (y/n)
   ```
   If yes, create the article following compile workflow conventions with full Obsidian syntax.

---

## /rmf-vault lint

Run health checks on the vault and report issues.

### Checks

1. **Orphan check:** Find Wiki notes with no incoming `[[wikilinks]]` from other Wiki notes.
   - Grep all Wiki files for `[[filename]]` patterns, compare against list of all Wiki files.

2. **Citation drift:** For each Wiki article that quotes Sources/:
   - Extract quoted text from `> [!quote]` callouts
   - Read the referenced Source file via the wikilink
   - Flag any quotes that don't match the source text

3. **Missing frontmatter:** Check all Wiki notes have required YAML fields:
   - `type`, `framework`, `status`, `tags`, `created`, `updated`, `sources`, `related`
   - Verify `sources` and `related` use wikilink format (`"[[...]]"`)
   - Report files missing any required field

4. **Gap analysis:** List Sources/ frameworks that have zero Wiki coverage:
   - For each framework directory in Sources/ with files (not just .gitkeep), check if any Wiki article references it
   - Report uncovered frameworks and specific source files with no Wiki citations

5. **Broken links:** Find `[[wikilinks]]` pointing to non-existent files.

6. **NEEDS SOURCE audit:** Find all `> [!danger] NEEDS SOURCE` callouts in Wiki articles.

7. **Syntax check:** Verify Wiki articles use Obsidian conventions:
   - Flag standard markdown links `[text](path.md)` used for internal vault files (should be `[[wikilinks]]`)
   - Flag source citations not using `> [!quote]` callout format

8. **Output report:**
   ```
   ══════════════════════════════════════════
     Vault Health Report
   ══════════════════════════════════════════

     Stats
     ──────────────────────────────────────
     Source files:        N (across N frameworks)
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

     Gap Analysis
     ──────────────────────────────────────
     Frameworks with no Wiki coverage:
       - OWASP-LLM (N source files, 0 wiki articles)
       - ...

     Recommendations
     ──────────────────────────────────────
     - <specific actionable suggestions>
   ══════════════════════════════════════════
   ```

---

## /rmf-vault index

Regenerate all index files in the vault.

### Workflow

1. **VAULT-INDEX.md** (vault root):
   - List all Wiki articles grouped by framework, with one-line summaries
   - Use wikilinks: `- [[Wiki/article-name]] — one-line description`
   - List Sources ingestion status per framework (file count)
   - Include quick reference links to subcommands

2. **Sources/_index.md:**
   - Update the ingestion status table: count files per framework directory (exclude .gitkeep)
   - Mark frameworks as "Pending" (0 files), "Partial" (some files), or "Ingested" (comprehensive)

3. **Wiki/_index.md:**
   - List all Wiki articles with one-line descriptions using wikilinks
   - Group by framework tag from frontmatter

4. **Per-directory _index.md:**
   - For any directory under Wiki/ or Sources/ with 2+ content files (not .gitkeep), create or update `_index.md`
   - Format: `- [[filename]] — one-line description`

5. **Output:** Report how many index files were created/updated.

---

## /rmf-vault status

Show vault statistics at a glance.

### Workflow

1. **Count files** in each directory:
   - Sources: count per framework subdirectory (exclude .gitkeep and _index.md)
   - Wiki: count total articles and group by framework frontmatter tag
   - Capture: count pending files in inbox

2. **Coverage matrix:**
   ```
   ══════════════════════════════════════════
     RMF Vault Status
   ══════════════════════════════════════════

     Sources (Authoritative)
     ──────────────────────────────────────
     NIST-800-53:    N files
     FedRAMP:        N files
     OWASP-LLM:     N files
     NIST-AI-RMF:   N files
     NIST-800-171:   N files
     ──────────────────────────────────────
     Total:          N source files

     Wiki (LLM-Maintained)
     ──────────────────────────────────────
     Articles:       N total
       nist-800-53:  N
       fedramp:      N
       owasp-llm:    N
       nist-ai-rmf:  N
       nist-800-171: N
       cross-framework: N

     Capture Inbox:  N files pending

     Git
     ──────────────────────────────────────
     Last commit:    <hash> <date>
                     <message>
     Working tree:   clean | N modified files
   ══════════════════════════════════════════
   ```

3. Read git log and status via:
   ```bash
   git --git-dir=C:/Users/samue/repos/rmf_obsidian.git --work-tree=C:/Users/samue/OneDrive/Obsidian/rmf_obsidian log -1 --oneline
   git --git-dir=C:/Users/samue/repos/rmf_obsidian.git --work-tree=C:/Users/samue/OneDrive/Obsidian/rmf_obsidian status --short
   ```

---

## /rmf-vault ingest <path>

Add a user-provided document into Sources/ as an authoritative reference.

This is the ONE exception to the "never modify Sources/" rule — it adds new documents the user has downloaded or created.

### Workflow

1. **Validate** the file exists at `<path>`.
   - If not found, report the error and exit.
   - Supported formats: `.md`, `.pdf`, `.txt`, `.html`, `.docx`
   - For non-markdown formats, convert to markdown first (use python-docx for .docx, or note that the file is stored as-is).

2. **Determine framework:**
   - Use `references/FRAMEWORK-IDENTIFIERS.md` to match control IDs in the content
   - Inspect filename and content for framework indicators (NIST, FedRAMP, OWASP, etc.)
   - If ambiguous, ask the user:
     ```
     Which framework does this document belong to?
     1. NIST-800-53
     2. FedRAMP
     3. OWASP-LLM
     4. NIST-AI-RMF
     5. NIST-800-171
     6. Other (new framework directory)
     ```

3. **Name the file:**
   - Convert to kebab-case: `nist-800-53-ac-2-account-management.md`
   - If the user provided a good name, keep it (just kebab-case it)
   - Ensure the name is wikilink-friendly (no special characters that break `[[links]]`)
   - Confirm with user if the name is unclear

4. **Copy to Sources/:**
   - Copy (not move — preserve the user's original) to `VAULT_PATH/Sources/<framework>/<filename>`
   - If "Other" framework, create the new directory under Sources/

5. **Update indexes:**
   - Update the framework's `_index.md` with the new file entry using wikilinks
   - Update `Sources/_index.md` if this is the first file for a framework (Pending → Partial)

6. **Output:**
   ```
   Ingested: <filename>
      -> Sources/<framework>/<filename>

   Run /rmf-vault compile to generate Wiki articles from this source
   Commit changes when ready
   ```

---

## Frontmatter Convention

All Wiki notes use this YAML frontmatter with Obsidian-typed properties:

```yaml
---
type: concept
framework: nist-800-53
status: draft
tags:
  - access-control
  - least-privilege
created: 2026-04-05
updated: 2026-04-05
sources:
  - "[[Sources/NIST-800-53/AC-access-control]]"
  - "[[Sources/FedRAMP/fedramp-moderate-baseline]]"
related:
  - "[[Wiki/fedramp-moderate-access-controls]]"
  - "[[Wiki/least-privilege-across-frameworks]]"
---
```

### Property types

| Property | Obsidian Type | Values |
|---|---|---|
| `type` | text | concept, pattern, decision-record, mapping, guide, session-log |
| `framework` | text | nist-800-53, fedramp, nist-ai-rmf, owasp-llm, nist-800-171, cross-framework |
| `status` | text | draft, review, final |
| `tags` | list | Freeform, hierarchical allowed (e.g., `access-control/least-privilege`) |
| `created` | date | YYYY-MM-DD |
| `updated` | date | YYYY-MM-DD |
| `sources` | links | Wikilinks to Sources/ files — renders in graph view |
| `related` | links | Wikilinks to other Wiki articles — renders in graph view |

The `sources` and `related` link properties make source-to-wiki relationships visible in Obsidian's **graph view**.

## File Naming

- Kebab-case: `least-privilege-implementation.md`
- Atomic: one concept per note
- Descriptive: filename communicates content without opening
- Wikilink-friendly: avoid special characters that break `[[links]]`
- Prefer flat/shallow over deep nesting

## Git Workflow

After any operation that changes files, remind the user:

```
Commit changes:
   git --git-dir=C:/Users/samue/repos/rmf_obsidian.git --work-tree=C:/Users/samue/OneDrive/Obsidian/rmf_obsidian add -A
   git --git-dir=C:/Users/samue/repos/rmf_obsidian.git --work-tree=C:/Users/samue/OneDrive/Obsidian/rmf_obsidian commit -m "description"
```

Do NOT auto-commit. The user decides when to snapshot.

## Related Skills

| Skill | Relationship |
|---|---|
| `/nist-800-53` | Embedded rule lookups — use for quick control checks. Vault has full source text and narratives. |
| `/fedramp` | Embedded AWS Config rules and baselines. Vault has source docs and implementation patterns. |
| `/nist-ai-rmf` | Subcategory lookups and gap analysis. Vault has function descriptions and cross-mappings. |
| `/firecrawl-scrape` | Scrape authoritative URLs into markdown for ingestion into the vault. |
| `/notebooklm` | Analyze and enrich source material before compilation. |
| `defuddle` | Clean markdown extraction from web pages — lighter than Firecrawl for simple pages. |

## Obsidian Skills

The vault includes Obsidian Skills from `kepano/obsidian-skills` at `.claude/obsidian-skills/`. These teach proper Obsidian syntax:

- **obsidian-markdown** — Wikilinks, embeds, callouts, properties, tags
- **obsidian-bases** — Database-like `.base` files with filters and formulas
- **json-canvas** — Visual canvas files for mind maps and flowcharts
- **obsidian-cli** — Vault interaction via command line
- **defuddle** — Clean web page extraction

When creating complex vault features (e.g., a compliance tracking dashboard), reference the appropriate obsidian-skill for syntax details.
