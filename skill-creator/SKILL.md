# Skill Creator

Generate a fully configured, exam-specific quiz skill from a vault and exam guide. The output is a ready-to-use skill directory (like `/cmmc-quiz`) that handles question generation, coverage tracking, and quiz app builds — all pre-wired to your specific exam's structure, domain names, and source documents.

**This skill creates skills.** It is the bootstrap layer. Run it once per exam, then use the generated skill for everything else.

---

## Prerequisites

Before running `/skill-creator`:

1. **Exam guide** (required) — A PDF or markdown file listing domains, tasks, and skills with exam weights. This is the blueprint. Without it, coverage tracking is impossible and questions will be unbalanced.
2. **Vault** (recommended) — An Obsidian vault with source documents already ingested under `Sources/`. Minimal mode (flat folder) also works.
3. **Quiz output directory** — Where the Python server and HTML app will live (e.g., `~/repos/my-exam-quiz`).

> If you do not yet have an exam guide, stop here. Ask the user to provide one before proceeding. An exam guide is non-negotiable — it is what separates a structured question bank from random notes.

---

## Subcommands

| Command | Description |
|---------|-------------|
| `/skill-creator new` | Start interactive setup — prompts for all required inputs |
| `/skill-creator build <skill-name>` | Generate quiz app files for an already-configured skill |
| `/skill-creator` (no args) | Show this help |

---

## /skill-creator new

Interactive wizard that generates a complete, configured quiz skill.

### Step 1 — Gather Inputs (REQUIRED — ask all of these before doing anything else)

Ask the user in a single message:

```
To create your quiz skill I need the following:

1. Exam name — full name as it appears on the certification (e.g., "CMMC-AB Certified CMMC Professional (CCP) v7.4")
2. Exam guide path — path to the PDF or markdown file with domains/tasks/skills and exam weights
3. Vault path — where your source documents live (Obsidian vault root, or a flat folder)
4. Quiz output directory — where to create the Python quiz app (e.g., ~/repos/cissp-quiz)
5. Skill name — short kebab-case name for the skill (e.g., "cissp-quiz", "sec-plus-quiz")
   This becomes the slash command: /[skill-name]

Have all five? Paste them and I'll build the skill.
```

Do NOT proceed until all five are provided. Do not guess or assume defaults.

### Step 2 — Parse the Exam Guide

1. Read the exam guide at the provided path.
   - If PDF: extract with pdfplumber (text-based) or vision (image-based). Check `chars/page` ratio — if < 50, use vision.
   - If markdown: read directly.

2. Extract the complete exam structure:
   - All domains with weights (e.g., "Domain 1: Access Control — 15%")
   - All tasks within each domain
   - All skills within each task (the atomic test items)
   - Total question count and passing score
   - Question types used (single, multi-select, ordering)

3. Compute question targets per domain based on weights and total question count:
   ```
   D1 at 15% of 170 questions = ~26 questions
   D2 at 5% of 170 questions = ~9 questions
   ```

4. If the exam guide is ambiguous about skills (lists topics without numbered skills), infer a skill list from the topic headings and note it.

5. Output the parsed structure as a confirmation for the user before writing any files:
   ```
   ══════════════════════════════════════
     Exam Guide Parsed — Please Confirm
   ══════════════════════════════════════
     Exam:       [name]
     Domains:    N (D1: X%, D2: Y%, ...)
     Tasks:      N total
     Skills:     N total
     Q Types:    single, multi-select
     Total Qs:   N (~N per domain)
   ──────────────────────────────────────
     Proceed? (y/n or corrections)
   ══════════════════════════════════════
   ```

Wait for user confirmation before writing any files.

### Step 3 — Generate Coverage Map

Create `{VAULT_PATH}/{EXAM_DIR}/Sources/Generated-Questions/_coverage-map.md`:

```markdown
---
type: coverage-map
exam: {EXAM_NAME}
generated: {DATE}
updated: {DATE}
total_skills: {N}
covered: 0
partial: 0
gap: {N}
coverage_pct: 0
---

# {EXAM_NAME} Coverage Map

**Exam**: {EXAM_NAME}
**Source**: [[Sources/Exam-Prep/{exam-guide-filename}]]
**Total Skills**: {N} | **Covered**: 0 | **Gap**: {N} | **Coverage**: 0%

---

## Domain 1: {Name} ({weight}% — ~{target_questions} questions)

### Task 1.1 — {Description}

- [ ] 1.1.1 {Skill description} — GAP
- [ ] 1.1.2 {Skill description} — GAP
...
```

All skills start as GAP. This file is updated by the generated skill's `generate` and `gap-fill` commands.

### Step 4 — Inventory Source Documents

Scan `{VAULT_PATH}/Sources/` (or the flat folder) for all `.md` files:

1. Group them by domain relevance using filename keywords and first 200 characters of content.
2. Flag domains with thin source coverage (< 2 documents).
3. Generate a `DOMAIN-SOURCE-MAP.md` for the skill's `references/` folder:

```markdown
# Domain → Source Document Map

## Domain 1: {Name}
- [[Sources/path/to/doc1]] — description
- [[Sources/path/to/doc2]] — description

## Domain 2: {Name}
- [[Sources/path/to/doc3]] — description
⚠️ THIN COVERAGE — only 1 source for this domain
```

### Step 5 — Generate the Skill File

Create `~/.claude/skills/{SKILL_NAME}/SKILL.md` using the template in `references/SKILL-TEMPLATE.md`, filling in all placeholders.

The generated skill file MUST include:
- Pre-filled configuration (all 5 paths/names)
- Domain names from the exam guide (not inherited from any other exam's skill)
- Question targets per domain based on weights
- Domain → source mapping
- Coverage map path
- Git workflow matching the vault setup
- All subcommands from `/quiz-creator` pre-configured

**Critical anti-patterns to avoid (lessons from CMMC build):**

| Anti-Pattern | Prevention |
|---|---|
| HTML inherits domain names from a prior exam | `build` command injects domain config from exam guide — never copy HTML from another skill |
| Domain loop hardcoded to wrong count | `build` generates the loop bound from `len(domains)` dynamically |
| Questions generated before exam guide is parsed | Step 1 of every `generate` subcommand re-reads the coverage map; aborts if `total_skills: 0` |
| Gap-fill done as afterthought with uneven quality | `gap-fill` gets the same systematic treatment as `generate` — one focused question per GAP skill |
| Domain weights ignored, equal questions per domain | Question targets computed from weights in Step 2 and embedded in the skill |
| Coverage map not updated after generation | Generated skill's `generate` and `gap-fill` commands always update the map as the last step |

### Step 6 — Generate Quiz App Bootstrap

Create `{QUIZ_DIR}/` with:

1. **`quiz_server.py`** — Python stdlib HTTP server configured with:
   - `VAULT_PATH` pointing to the correct vault
   - `GENERATED_DIR` pointing to the exam's `Generated-Questions/` folder
   - `DOMAIN_NAMES` dict populated from the parsed exam guide (NOT copied from another app)
   - Domain count variable used in JS template, not hardcoded

2. **`quiz_app.html`** — Self-contained UI with:
   - `DOMAIN_SHORT` and `DOMAIN_FULL` populated from the exam guide's domain names
   - Domain loop: `for (let d = 1; d <= {DOMAIN_COUNT}; d++)` — number comes from the exam
   - `TOPICS` object populated with exam-relevant topic keywords (not AWS/cloud keywords)
   - Exam name in the page title and header
   - All other quiz features from the quiz-creator spec (shuffle, 3-retry, keyboard shortcuts, progress)

**The quiz app must be generated fresh from the exam guide, not adapted from a prior exam's app.**

### Step 7 — Output Summary

```
══════════════════════════════════════════════
  Skill Created: /{SKILL_NAME}
══════════════════════════════════════════════

  Exam:          {EXAM_NAME}
  Domains:       {N} ({D1}: {w}%, {D2}: {w}%, ...)
  Skills:        {N} skills, all marked GAP
  Coverage:      0% — ready for generation

  Files Created
  ────────────────────────────────────────────
  Skill:         ~/.claude/skills/{SKILL_NAME}/SKILL.md
  Source map:    ~/.claude/skills/{SKILL_NAME}/references/DOMAIN-SOURCE-MAP.md
  Coverage map:  {VAULT_PATH}/{EXAM_DIR}/Sources/Generated-Questions/_coverage-map.md
  Quiz server:   {QUIZ_DIR}/quiz_server.py
  Quiz app:      {QUIZ_DIR}/quiz_app.html

  Next Steps
  ────────────────────────────────────────────
  1. Add source documents to vault Sources/ for any thin domains flagged above
  2. Run: /{SKILL_NAME} generate all
  3. Run: /{SKILL_NAME} gap-fill
  4. Run: /{SKILL_NAME} launch

  Coverage target: 90%+ skills before exam
══════════════════════════════════════════════
```

---

## /skill-creator build <skill-name>

Rebuild the quiz app files for an existing skill (already has a SKILL.md).

Use this when:
- The quiz app HTML needs regenerating (e.g., after new domains are added)
- The quiz_server.py paths have changed
- The app was accidentally overwritten with a different exam's template

### Workflow

1. Read `~/.claude/skills/{skill-name}/SKILL.md` to get the configuration
2. Re-read the stored domain names and count
3. Regenerate `quiz_server.py` and `quiz_app.html` with correct values
4. Do NOT touch question files or coverage map

---

## Skill Template Reference

See `references/SKILL-TEMPLATE.md` for the full template used in Step 5.

---

## Coverage Tracking Protocol

The coverage map is the single source of truth. All commands in the generated skill follow this protocol:

```
generate domain N
  → for each question written: mark its skills as COVERED in _coverage-map.md
  → update frontmatter: covered++, gap--, coverage_pct = covered/total_skills * 100
  → update header line: "Covered: X | Gap: Y | Coverage: Z%"

gap-fill
  → read ALL [ ] GAP items from coverage map
  → generate one focused question per GAP
  → mark each as COVERED after writing
  → report final coverage %

gap-analysis
  → re-scan all question files for skill coverage
  → recompute coverage from scratch
  → update coverage map
  → report any regressions (skills that were COVERED but questions were deleted)
```

Never skip the coverage map update. It is the only way to know when you're done.

---

## Lessons Learned (Built from CMMC CCP Quiz Build)

These are specific failure modes encountered and the fixes that work.

### 1. Template Bleed — Wrong Exam Names in UI
**What happened:** The CMMC quiz HTML was adapted from an AWS quiz template. AWS domain names (FM Integration, Implementation, Safety & Security) appeared in the CMMC quiz UI for the first several sessions.

**Root cause:** `DOMAIN_SHORT`, `DOMAIN_FULL`, and `DOMAIN_SHORT_FC` were hardcoded strings from the source template. The loop `for (let d = 1; d <= 5; d++)` was also wrong (CMMC has 6 domains).

**Fix in this skill:** The `build` step generates `DOMAIN_SHORT` and `DOMAIN_FULL` from the parsed exam guide. The loop bound is a variable. Domain names are never inherited from a template.

---

### 2. Coverage Map Created After Questions
**What happened:** Questions were generated for several domains before the coverage map was formalized. This made it hard to know which skills were actually covered and which were just incidentally touched.

**Root cause:** The coverage map was treated as a tracking artifact rather than a planning artifact.

**Fix in this skill:** The coverage map is generated in Step 3, before any questions are written. Every skill starts as GAP. Generation fills the map; gap-fill closes the remaining holes.

---

### 3. Gap-Fill Was an Afterthought
**What happened:** The gap-fill pass was done at the end with less rigor than domain generation. Questions were sometimes shallower and covered less ground.

**Root cause:** No systematic process tied gap-fill to the coverage map at the skill level.

**Fix in this skill:** `gap-fill` is a first-class subcommand in every generated skill. It reads the coverage map directly, generates exactly one question per GAP skill, and updates the map immediately. The generated skill's `gap-fill` step uses the same question quality standards as `generate`.

---

### 4. Exam Weight Not Reflected in Question Count
**What happened:** Domain 4 (35% of CMMC CCP exam) got 20 questions. Domain 1 (5%) got 10. The ratio should have been ~60:9 to match exam weight.

**Root cause:** A flat "10 questions per domain" default was applied without adjusting for weight.

**Fix in this skill:** Step 2 computes per-domain question targets from the exam weight × total question count. These targets are embedded in the generated skill and displayed as guidance in each `generate` command.

---

### 5. Domain 6 Missing from Quiz UI
**What happened:** The quiz app showed domains 1-5 only. Domain 6 (Scoping, 15% of exam) had questions that loaded but were invisible in the "By Domain" section.

**Root cause:** Loop `for (let d = 1; d <= 5; d++)` was hardcoded to 5.

**Fix in this skill:** The loop bound is generated from `{DOMAIN_COUNT}` and written into the HTML at build time. Adding a domain to the exam guide and rebuilding correctly extends the UI.

---

### 6. Question Files Parsed but Server Cached Old Data
**What happened:** After adding `gap-fill-questions.md`, the quiz server still returned 105 questions instead of 128 because a stale Python process was running.

**Root cause:** Multiple Python processes from prior sessions were serving cached data.

**Fix in generated skill's `launch` command:** Always kill all processes on port 8765 before starting. The `launch` workflow is: `taskkill /F /IM python.exe` (Windows) or `pkill -f quiz_server.py` (Unix), then start fresh.

---

### 7. First Git Commit Missed All Untracked Files
**What happened:** The first `git commit` was a root-commit that included PDFs and vault index files that were large and unrelated to the question bank changes.

**Root cause:** `git add` was run without listing specific files, picking up everything untracked.

**Fix in generated skill's git workflow:** The generated skill always stages specific files by name: `git add Generated-Questions/domain-*.md Generated-Questions/gap-fill*.md Generated-Questions/_coverage-map.md`. Never `git add -A` for vault commits.

---

## File Naming Conventions (Enforced in Generated Skill)

| Content | Filename Pattern |
|---|---|
| Coverage map | `_coverage-map.md` (underscore prefix = skipped by parser) |
| Domain questions | `domain-{N}-{slug}-questions.md` |
| Gap-fill questions | `gap-fill-questions.md` |
| Topic deep-dives | `topic-{name}-questions.md` |
| Extended scenarios | `domain-{N}-{slug}-scenarios-extended.md` |

Consistent naming ensures the quiz server parser picks up all files and skips metadata files.
