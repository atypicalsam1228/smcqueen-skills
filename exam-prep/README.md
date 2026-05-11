# exam-prep

Stages 0+1+2 of the exam prep pipeline. Scaffolds an Obsidian vault, verifies a NotebookLM notebook, and generates a full study guide with community intel callouts embedded in every domain guide. Works with any certification exam.

## Prerequisites

### 1. Obsidian

Download and install Obsidian: **https://obsidian.md/download**

Obsidian is the note-taking app where your study guides will live. After running `/exam-prep setup`, open Obsidian and point it at the vault path you configured — the folder structure and all generated guides will already be there.

### 2. NotebookLM

You need a Google account and a NotebookLM notebook pre-populated with exam sources. If you haven't done this yet, run `/exam-notebooklm` first to create and populate the notebook.

### 3. NotebookLM CLI

```bash
pip install notebooklm-py
notebooklm login
```

### 4. Obsidian Markdown skill (optional but recommended)

Installs the authoritative Obsidian Flavored Markdown syntax reference:

```bash
npx skills add kepano/obsidian-skills
```

This gives you the `obsidian-markdown` skill, which `/exam-prep` references for callout types, wikilink formatting, and frontmatter conventions.

---

## Quick Start

```bash
# 1. Set up notebook with exam sources
/exam-notebooklm create SOA-C03

# 2. Scaffold vault + verify notebook
/exam-prep setup

# 3. Open Obsidian → File → Open Vault → select your VAULT_PATH

# 4. Generate study guides
/exam-prep generate all

# 5. Generate exam intel file
/exam-prep intel

# 6. Generate master index
/exam-prep master
```

---

## Configuration

Set at session start or hardcode for a specific exam:

```
EXAM_NAME:    "AWS Certified SysOps Administrator – Associate (SOA-C03)"
EXAM_CODE:    "SOA-C03"
NOTEBOOK_ID:  "806bd12a-4494-4630-9771-33fdc2f24db3"
VAULT_PATH:   "C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer"
OUTPUT_DIR:   "Wiki/study-guide"
```

---

## What Gets Generated

Each domain guide includes:
- Self-check questions (5–6 per domain)
- Per-task sections with concept explanation + comparison tables
- `[!warning]` exam traps embedded per task
- `[!tip]` community intel (Reddit passer insights) per task
- `[!example]` scenario questions with answers
- `[!danger]` High-Frequency Exam Traps table at domain end
- Common Wrong Answers table

---

## Full Pipeline

```
/exam-notebooklm   ← Stage 1: create notebook, add sources
/exam-prep         ← Stages 0+1+2: scaffold vault + study guides
/exam-quiz         ← Stage 3: generate quiz questions + quiz app
```

## Related Skills

- `/exam-notebooklm` — create and populate the NotebookLM notebook
- `/exam-quiz` — generate practice questions and a runnable quiz app
- `/vault` — manage vaults registered during setup
