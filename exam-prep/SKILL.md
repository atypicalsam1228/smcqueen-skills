---
name: exam-prep
description: "Stages 0+1+2 of the exam prep pipeline. Scaffolds an Obsidian vault, verifies a NotebookLM notebook, and generates a full CMMC-format study guide with community intel callouts embedded directly in every domain guide. Produces: vault structure + CLAUDE.md, master index, per-domain guides with [!warning]/[!tip]/[!danger] intel callouts distributed throughout, and a standalone exam-intel file. Works with any certification exam."
---

# Exam Prep — Obsidian Vault + NotebookLM + Study Guide Generation

Combines Obsidian vault scaffolding (Stage 0), NotebookLM source verification (Stage 1), and full study guide generation (Stage 2). Produces domain guides in the CMMC CCP format: self-check questions, task breakdowns, embedded intel callouts per task, domain summary tables, and a high-frequency trap section at the end of every domain.

**The key output difference from a basic study guide:** Community intel (Reddit passer quotes, exam traps, gotchas) is embedded directly in each task section — not in a separate file. Every domain guide ends with a `[!danger] High-Frequency Exam Traps` table drawn from community sources.

## Configuration

Set these at the start of a session or hardcode for a specific exam:

```
EXAM_NAME:       e.g., "AWS Certified SysOps Administrator – Associate (SOA-C03)"
EXAM_CODE:       e.g., "SOA-C03"
NOTEBOOK_ID:     e.g., "806bd12a-4494-4630-9771-33fdc2f24db3"
VAULT_PATH:      e.g., "C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer"
OUTPUT_DIR:      e.g., "Wiki/study-guide"
DOMAINS:         List of domains with weights — from exam guide or task statements
```

## Subcommands

| Subcommand | Purpose |
|---|---|
| `setup` | Scaffold Obsidian vault, verify notebook, parse domain list |
| `generate [domain\|all]` | Generate domain study guide(s) with embedded intel |
| `intel` | Generate standalone exam-intel file (format, community data, trap table) |
| `master` | Generate master index file linking all domain guides |
| `status` | Show which domains have been generated |
| `update <domain>` | Regenerate a single domain guide (re-queries NotebookLM) |

---

## /exam-prep setup

Prepares both the Obsidian vault and the NotebookLM workspace before generating. Safe to re-run — skips steps that are already complete.

### Workflow

**Stage 0 — Obsidian Vault Scaffolding**

1. **Check if vault exists** at `<VAULT_PATH>/`
   - If it doesn't exist: create the directory
   - If it exists: verify it's an Obsidian vault (check for `.obsidian/` folder or any `.md` files); report "Vault exists, skipping scaffold"

2. **Create standard folder structure** (skip any that already exist):
   ```
   <VAULT_PATH>/
   ├── Sources/
   │   ├── Exam-Prep/          ← official exam guide, task statements, sample questions
   │   └── <domain-dirs>/      ← one per domain (e.g., Monitoring-Logging/, Security-Compliance/)
   ├── Wiki/
   │   ├── study-guide/        ← OUTPUT_DIR — domain guides written here
   │   └── quiz/               ← exam-quiz output directory
   └── Capture/                ← drop zone for raw notes
   ```
   Domain subdirectory names are derived from domain slugs:
   - "Monitoring, Logging, and Remediation" → `Sources/Monitoring-Logging/`
   - "Reliability and Business Continuity" → `Sources/Reliability/`
   - "Deployment, Provisioning, and Automation" → `Sources/Deployment-Automation/`
   - "Security and Compliance" → `Sources/Security-Compliance/`
   - "Networking and Content Delivery" → `Sources/Networking/`
   - "Cost and Performance Optimization" → `Sources/Cost-Performance/`

3. **Write `CLAUDE.md`** at `<VAULT_PATH>/CLAUDE.md` — the vault operating manual:
   ```markdown
   # [EXAM_NAME] Vault — Operating Manual

   [One-sentence description of the vault purpose.]

   ## Linked NotebookLM

   Notebook ID: `<NOTEBOOK_ID>`
   [Source count] sources ingested covering exam guide, study resources, practice questions, and community experience reports.

   ## [EXAM_CODE] Exam Domains

   | Domain | Weight |
   |--------|--------|
   [one row per domain from DOMAINS config]

   ## Architecture

   - **Sources/** — Authoritative documents, organized by [EXAM_CODE] domain. Read-only except via ingest/extract.
   - **Wiki/** — LLM-maintained articles that cite Sources/.
   - **Capture/** — Drop zone for raw notes; processed into Wiki via compile.

   ## Domain → Directory Mapping

   | Domain | Directory |
   |--------|-----------|
   [one row per domain → Sources/slug/ mapping]

   ## Rules

   1. Sources/ is READ-ONLY except via ingest and extract.
   2. Every Wiki article must cite Sources/ using `> [!quote]` callouts.
   3. Use wikilinks `[[]]` for all internal references — never standard markdown links.
   4. Review extracted .md files before compiling.
   5. Regenerate indexes after any content change.
   ```

4. **Register vault** in `/vault` skill registry at `~/.claude/skills/vault/vaults.json`:
   - Read the file (create with `{"vaults": []}` if missing)
   - Check if an entry for `EXAM_CODE` already exists
   - If not: append `{"name": "<EXAM_CODE>", "path": "<VAULT_PATH>", "notebook_id": "<NOTEBOOK_ID>", "created": "<date>"}`
   - Write updated file
   - This enables `/vault <EXAM_CODE>` to manage the vault in future sessions

**Stage 1 — NotebookLM Verification**

5. **Verify NotebookLM:** Run `notebooklm source list -n <NOTEBOOK_ID> --json`
   - If 0 sources: "Notebook is empty. Run `/exam-notebooklm add <exam> <sources>` first."
   - If sources PROCESSING: "X sources still processing. Run `/exam-notebooklm verify` and wait."
   - If all READY: proceed

6. **Parse domains:** If `DOMAINS` not configured, query NLM:
   `notebooklm ask "List all exam domains for [EXAM_NAME] with their names and percentage weights" -n <NOTEBOOK_ID>`

7. **Create `_index.md`** in `<VAULT_PATH>/<OUTPUT_DIR>/` listing domains to generate

### Output

```
Stage 0 — Obsidian Vault
✓ Vault scaffolded: C:/Users/samue/OneDrive/Obsidian/AZ-900/
  Created: Sources/, Wiki/study-guide/, Wiki/quiz/, Capture/
  Created: Sources/Exam-Prep/, Sources/Fundamentals/, Sources/Azure-Services/
✓ CLAUDE.md written
✓ Vault registered: vaults.json → AZ-900

Stage 1 — NotebookLM
✓ Notebook ready: 41 sources
✓ Domains detected: 6
  - Domain 1: Cloud Concepts (25-30%)
  - Domain 2: Azure Architecture and Services (35-40%)
  - Domain 3: Azure Management and Governance (30-35%)

Next: /exam-prep generate all
```

---

## /exam-prep generate [domain|all]

The core command. Generates one or all domain study guide files with embedded intel.

### Workflow (per domain)

**Step 1 — Three parallel NotebookLM queries:**

```
CONTENT: "For [EXAM_NAME] Domain N ([name]): explain every task statement and skill,
key service behaviors, operational patterns, decision matrices, and comparison tables
the exam tests. Be specific — include thresholds, limits, feature names, and exact
service configurations."

TRAP:    "For [EXAM_NAME] Domain N ([name]): what are ALL the specific exam traps,
gotchas, common wrong answers, and distractor patterns? For each trap: describe
the distractor, what it tests, and the correct answer. Draw from community passers
and official exam guide nuances."

INTEL:   "For [EXAM_NAME] Domain N ([name]): what does community and Reddit intel say?
Include: high-frequency topics passers were surprised by, what they wish they had
studied, specific service sub-features that appear on the exam (not just the parent
service), and any domain-specific question strategies."
```

**Step 2 — Self-check questions query:**

```
SELFCHECK: "Generate 5-6 self-check questions for [EXAM_NAME] Domain N that test
operational judgment, not service definitions. Format: question + concise expected
answer covering the key insight. Make them progressively harder."
```

**Step 3 — Assemble the domain guide file** using the format in `references/STUDY-GUIDE-FORMAT.md`:

- Frontmatter with type, domain, status, tags, sources, related
- Abstract callout summarizing the domain and exam weight
- Self-check questions (from SELFCHECK query)
- Per-task sections — each containing:
  - `[!quote]` with a verbatim source citation
  - Concept explanation + comparison tables
  - `[!warning]` callouts for traps specific to that task (from TRAP query)
  - `[!example]` exam scenario with correct answer + reasoning
  - `[!tip]` community intel insight (from INTEL query)
- Domain Summary table (key facts, critical comparisons)
- `[!danger] High-Frequency Exam Traps` — domain-specific trap table from TRAP + INTEL queries
- Common Wrong Answers table

**Step 4 — Write file:**
`<VAULT_PATH>/<OUTPUT_DIR>/<exam-code>-study-guide-domain-<N>-<slug>.md`

### Intel Callout Placement Rules

Follow `references/INTEL-QUERY-TEMPLATES.md` for how to distribute intel:

| Callout | When to place | Content |
|---|---|---|
| `[!warning] Exam Trap: <Name>` | Immediately after the concept it traps | Distractor pattern + correct answer |
| `[!tip]` | After a concept with strong community signal | Reddit passer insight or high-frequency observation |
| `[!danger] High-Frequency Exam Traps` | End of domain, before Common Wrong Answers | Domain-scoped trap table from community |
| `[!quote]` | Start of each task section | Verbatim from NLM source with wikilink |
| `[!example]` | After decision tables or operational patterns | Scenario + answer + reasoning |

**Minimum per domain guide:**
- ≥ 3 `[!warning]` callouts
- ≥ 1 `[!danger]` trap table
- ≥ 2 `[!quote]` source citations
- ≥ 2 `[!example]` exam scenarios
- ≥ 1 `[!tip]` community intel per major task

### Output

```
✓ Domain 1 generated: Wiki/study-guide/soa-c03-study-guide-domain-1-monitoring.md
  - 6 self-check questions
  - 7 tasks covered
  - 5 [!warning] callouts
  - 1 [!danger] trap table (12 rows)
  - 3 [!quote] citations
  - 4 [!example] scenarios
  - 3 [!tip] community intel

Progress: 1/5 domains complete
```

---

## /exam-prep intel

Generates the standalone exam-intel file covering cross-domain community data.

### Workflow

Run these queries against NotebookLM:

```
FORMAT:    "What is the exact exam format for [EXAM_NAME]? Include: question count,
time limit, passing score, question types, can you go back, unscored questions,
lab component (if any), and what the community says about how the exam actually feels."

CHANGES:   "What changed between the previous version and [EXAM_CODE]? New services,
removed services, domain weight changes, new topic areas, format changes."

RESOURCES: "What study resources do community passers recommend for [EXAM_NAME]?
Include specific names, what they're praised for, and what to avoid."

SCORES:    "What practice exam scores did real passers report before taking [EXAM_NAME]?
Show that you don't need 90%+ — include specific examples."

STRATEGY:  "What question strategies did passers use for [EXAM_NAME]? Include named
techniques, elimination patterns, time management, and review strategies."

TRAPS:     "List ALL high-frequency exam trap patterns for [EXAM_NAME] across all
domains. Format: Trap | What Gets Tested | Correct Answer."
```

### Output File Structure

```markdown
# [EXAM_CODE] Exam Intel — Community Passers & Reality

> [!abstract] [Summary]

## Exam Format Reality
## What to Study — Priority Order
## [Previous Version] → [EXAM_CODE]: What Changed
## Practice Resources — What Passers Used
## Practice Score Reality Check
## Study Timelines
## Question Strategy
## High-Frequency Trap Patterns    ← cross-domain table
## Specific Exam-Day Gotchas
## What NOT to Study
## Final Week Tips
## Recommended Resources
```

Output path: `<VAULT_PATH>/<OUTPUT_DIR>/<exam-code>-exam-intel.md`

---

## /exam-prep master

Generates the master index file linking all domain guides.

### Workflow

1. Read all generated domain guides from output dir
2. Query NLM: `"Summarize the study priority and allocation for [EXAM_NAME] — which domains to study first and why, based on exam weight and community reports"`
3. Assemble master file using the format:
   - Abstract
   - Exam blueprint table (domain | weight | study guide link)
   - ASCII study priority bar chart
   - Study allocation tip (community-sourced)
   - Exam Reality Check (key community quotes)
   - How to Use This Guide
   - Links to exam intel and all domain guides

Output path: `<VAULT_PATH>/<OUTPUT_DIR>/<exam-code>-study-guide.md`

---

## /exam-prep status

Shows generation progress across all domains.

### Output

```
Exam: SOA-C03 — AWS Certified CloudOps Engineer Associate
Notebook: 806bd12a (63 sources, all READY)
Output: Wiki/study-guide/

Domain Guides:
  ✓ Domain 1 — Monitoring (22%)       soa-c03-study-guide-domain-1-monitoring.md
  ✓ Domain 2 — Reliability (22%)      soa-c03-study-guide-domain-2-reliability.md
  ✗ Domain 3 — Deployment (22%)       NOT GENERATED
  ✗ Domain 4 — Security (16%)         NOT GENERATED
  ✗ Domain 5 — Networking (18%)       NOT GENERATED

Supporting Files:
  ✓ Exam Intel                         soa-c03-exam-intel.md
  ✗ Master Index                       NOT GENERATED

Next: /exam-prep generate domain3
```

---

## /exam-prep update <domain>

Regenerates a single domain guide by re-querying NotebookLM. Use when:
- New sources have been added to the notebook
- The existing guide needs more depth
- A specific domain needs exam intel refreshed

### Workflow

1. Run the same three queries (CONTENT, TRAP, INTEL) for the specified domain
2. Overwrite the existing domain guide file
3. Report what changed (line count before/after, new callout counts)

---

## File Naming Convention

```
<exam-code>-study-guide.md                         ← master index
<exam-code>-study-guide-domain-<N>-<slug>.md       ← domain guides
<exam-code>-exam-intel.md                          ← standalone intel file
```

Examples for SOA-C03:
```
soa-c03-study-guide.md
soa-c03-study-guide-domain-1-monitoring.md
soa-c03-study-guide-domain-2-reliability.md
soa-c03-exam-intel.md
```

---

## Obsidian Conventions

All generated files must conform to Obsidian Flavored Markdown. The **`obsidian-markdown`** skill from [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills) is the authoritative reference for all Obsidian-specific syntax used here. Install it alongside this skill:

```bash
npx skills add kepano/obsidian-skills
```

Key conventions applied in every generated file:

| Element | Correct syntax | Wrong |
|---|---|---|
| Internal vault links | `[[Wiki/study-guide/filename\|Display Text]]` | `[text](path/to/file.md)` |
| Source citations | `[[Sources/path/to/source\|Source Title]]` | bare URL or standard link |
| Callouts | `> [!type] Optional Title` | `> **Note:**` or HTML |
| Foldable callouts | `> [!type]-` (collapsed) / `> [!type]+` (expanded) | n/a |
| Frontmatter | YAML between `---` delimiters | JSON or inline properties |
| Tags in frontmatter | `tags:\n  - soa-c03/domain1` (list form) | `tags: soa-c03` (string form) |
| Embeds | `![[filename]]` | `![](path)` for vault files |

**Callout types used by this skill** (defined in `obsidian-markdown/references/CALLOUTS.md`):

| Type | Purpose |
|---|---|
| `[!abstract]` | Domain summary, key takeaways |
| `[!question]` | Self-check questions |
| `[!quote]` | Verbatim source citations |
| `[!warning]` | Per-task exam traps |
| `[!example]` | Scenario questions with answers |
| `[!tip]` | Community intel insights |
| `[!danger]` | High-frequency trap tables at domain end |
| `[!info]` | Administrative notes |

When writing vault files, invoke the `obsidian-markdown` skill to verify syntax correctness if unsure.

---

## Full Pipeline

```
/exam-notebooklm create <exam>        ← Stage 1: create notebook, add sources
/exam-prep setup                      ← Stage 0+1: scaffold vault + verify notebook
/exam-prep generate all               ← Stage 2: generate all domain guides
/exam-prep intel                      ← Stage 2: generate exam intel file
/exam-prep master                     ← Stage 2: generate master index
/exam-quiz generate all               ← Stage 3: generate quiz questions
/exam-quiz build && /exam-quiz launch ← Stage 3: build and run quiz app
```

## Related Skills

- `/exam-notebooklm` — Stage 1: set up and populate the NotebookLM notebook
- `/exam-quiz` — Stage 3: generate practice quiz questions and runnable quiz app
- `/vault` — Generic vault manager; `setup` registers the exam vault here for future sessions
- `/cloudops-vault` — Vault manager for the SOA-C03 vault specifically

## Reference Files

- `references/STUDY-GUIDE-FORMAT.md` — Complete domain guide template with all callout types
- `references/INTEL-QUERY-TEMPLATES.md` — NLM query templates and intel placement rules
