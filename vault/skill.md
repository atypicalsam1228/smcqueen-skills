---
name: vault
description: "Generic Obsidian vault manager. Use when the user invokes /vault. Reads the vault registry, lets the user pick a vault or register a new one, then routes to the appropriate vault skill (aws-vault, cmmc-vault, etc.) or runs generically. Entry point for all vault operations."
---

# Vault Manager

Generic entry point for all Obsidian knowledge vaults. Reads the vault registry, selects the target vault, and delegates to the vault-specific skill or runs operations generically.

## Registry

Vault registry lives at:
```
C:/Users/samue/.claude/skills/vault/vaults.json
```

Read it at the start of every invocation to get the current vault list.

## Invocation Patterns

| User invokes | Behavior |
|---|---|
| `/vault` | Show registered vaults, ask which one, then show subcommand menu |
| `/vault <name>` | Select vault by name, show subcommand menu |
| `/vault <name> <subcommand>` | Select vault and run subcommand directly |
| `/vault <name> <subcommand> <args>` | Select vault and run subcommand with args |

Examples:
```
/vault                        → interactive picker
/vault cmmc                   → select CMMC vault, show menu
/vault cmmc status            → run status on CMMC vault
/vault aws ingest <path>      → ingest a file into AWS vault
/vault cmmc query "what is AC.1.001"
```

## Workflow

### Step 1: Read registry

Read `C:/Users/samue/.claude/skills/vault/vaults.json`.

### Step 2: Select vault

**If name provided in args:** Match against `name` field in registry. If not found, show error and list available names.

**If no name provided:** Display registered vaults and ask user to pick:

```
══════════════════════════════════════════
  Registered Vaults
══════════════════════════════════════════
  1. cmmc  — CMMC Knowledge Vault
             C:/Users/samue/OneDrive/Obsidian/CMMC_Vault
  2. aws   — AWS Learning Vault
             C:/Users/samue/OneDrive/Obsidian/aws_learn_vault
──────────────────────────────────────────
  N. Register a new vault
══════════════════════════════════════════
Which vault?
```

### Step 3: Select subcommand

**If subcommand provided in args:** Run it directly.

**If no subcommand provided:** Show menu:

```
══════════════════════════════════════════
  <display name>
══════════════════════════════════════════
  status   — Vault stats at a glance
  ingest   — Add document to Sources/
  extract  — Extract PDFs to markdown
  compile  — Process Capture/ into Wiki articles
  query    — Search vault with source verification
  lint     — Run health checks
  index    — Regenerate all indexes
══════════════════════════════════════════
What would you like to do?
```

### Step 4: Delegate or run generically

**If vault has a named skill** (e.g., `"skill": "cmmc-vault"`):
- Invoke the vault-specific skill with the selected subcommand and args
- The vault skill has full domain knowledge (practice identifiers, domain structure, etc.)

**If vault has no named skill** (generic vault):
- Run the operation using the vault's CLAUDE.md and directory structure
- Use the standard subcommand workflows defined below

---

## New Vault Registration

When user selects "Register a new vault":

1. **Ask for vault name** (short slug, kebab-case, e.g. `fedramp`, `hipaa`)
2. **Ask for vault path** (where Obsidian vault lives, e.g. `C:/Users/samue/OneDrive/Obsidian/MyVault`)
3. **Ask for git repo path** — suggest `C:/Users/samue/repos/<name>.git`
4. **Ask for domain names** — comma-separated list, or press Enter for generic defaults:
   ```
   Default domains: Sources, Exam-Prep, Policy, Reference
   ```
5. **Scaffold vault structure:**
   ```
   <vault_path>/
     Sources/
       <domain1>/
       <domain2>/
       _index.md
     Wiki/
       _index.md
     Capture/
       archived/
     Templates/
     Attachments/
       extract-temp/
     CLAUDE.md
     VAULT-INDEX.md
   ```
6. **Create CLAUDE.md** from the generic template below
7. **Initialize bare git repo:**
   ```bash
   git init --bare <git_dir>
   ```
8. **Register in vaults.json** — add entry with name, display, vault_path, git_dir, domains
9. **Confirm and show next steps:**
   ```
   Vault registered: <name>
   Path: <vault_path>
   Git:  <git_dir>

   Next steps:
     /vault <name> ingest <path>   — Add your first source document
     /vault <name> status          — Check vault status
   ```

---

## Generic Subcommand Workflows

Used when a vault has no dedicated skill. These mirror the aws-vault/cmmc-vault patterns but use the vault's own CLAUDE.md for domain context.

### status
- Count files in Sources/ subdirectories (exclude .gitkeep, _index.md)
- Count Wiki/ articles
- Count Capture/ pending files
- Read git log/status
- Display coverage matrix

### ingest `<path>`
- Validate file exists
- Inspect filename for domain indicators; if ambiguous ask user to pick from vault's domain list
- Kebab-case the filename
- Copy to `Sources/<domain>/`
- Update `Sources/_index.md` and domain `_index.md`

### extract `[path|all]`
- Find PDFs in Sources/ lacking companion .md
- Run pdfplumber to classify (text-extractable vs image-only)
- Text-extractable: extract with pdfplumber, write .md with frontmatter
- Image-only: use PyMuPDF + Claude vision
- **Stop and prompt user to review before compiling**

### compile
- **Require user confirmation that extractions have been reviewed**
- Scan Capture/ for unprocessed files
- Identify domain(s) per file
- Create/update Wiki articles with Obsidian syntax
- Archive processed captures
- Regenerate indexes

### query `<question>`
- Grep Wiki/ and Sources/ for relevant content
- Cross-check Wiki against Sources
- Return cited answer with `> [!quote]` callouts
- Offer to file new knowledge as Wiki article

### lint
- Orphan check, citation drift, missing frontmatter, broken links
- NEEDS SOURCE audit, syntax check, unextracted PDFs

### index
- Regenerate VAULT-INDEX.md, Sources/_index.md, Wiki/_index.md
- Create per-directory _index.md for dirs with 2+ files

---

## Generic CLAUDE.md Template

Used when scaffolding a new vault with no dedicated skill:

```markdown
# <Vault Display Name> — Operating Manual

Two-tier Obsidian knowledge vault managed by `/vault <name>`.

## Architecture

- **Sources/** — Authoritative documents. Read-only except via ingest/extract.
- **Wiki/** — LLM-maintained articles that cite Sources/.

## Rules

1. Sources/ is READ-ONLY except via ingest and extract.
2. Every Wiki article must cite Sources/ using `> [!quote]` callouts.
3. Use wikilinks `[[]]` for all internal references — never standard markdown links.
4. Review extracted .md files before compiling.
5. Regenerate indexes after any content change.

## Git

\`\`\`bash
git --git-dir=<git_dir> --work-tree=<vault_path> add -A
git --git-dir=<git_dir> --work-tree=<vault_path> commit -m "description"
\`\`\`

Do NOT auto-commit. The user decides when to snapshot.
```

---

## Review Before Compile Rule (Enforced for ALL Vaults)

After any extraction, always remind the user:

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

  When ready: /vault <name> compile
══════════════════════════════════════════
```

Never run compile automatically after extract.

---

## Git Workflow Reminder

After any vault operation that changes files, show:

```
Commit when ready:
  git --git-dir=<git_dir> --work-tree=<vault_path> add -A
  git --git-dir=<git_dir> --work-tree=<vault_path> commit -m "description"
```
