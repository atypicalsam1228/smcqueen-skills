---
name: quiz-creator
description: "Generate exam-style practice quiz apps from source documents. Scrapes AWS docs, generates scenario-based questions by domain, builds a local Python+HTML quiz app with progress tracking. Use when the user invokes /quiz-creator or asks to create practice quizzes, generate exam questions, build a quiz app, or study for a certification."
---

# Quiz Creator

Generate exam-style practice quiz applications from authoritative source documents. Produces a self-contained Python + HTML app with domain-grouped questions, detailed answer explanations, and progress tracking.

## Configuration

```
QUIZ_DIR: C:/Users/samue/repos/aip-c01-quiz
VAULT_PATH: C:/Users/samue/OneDrive/Obsidian/aws_learn_vault
GENERATED_DIR: {VAULT_PATH}/Sources/Exam-Prep/Generated-Questions
```

> **To adapt for another project:** Change `QUIZ_DIR` and `VAULT_PATH` above. The quiz app files live in `QUIZ_DIR`; generated question markdown goes into the vault at `GENERATED_DIR`.

## Subcommand Selection

Parse the first argument after `/quiz-creator` to determine the subcommand:

| User invokes | Subcommand |
|---|---|
| `/quiz-creator generate <domain> [count]` | generate |
| `/quiz-creator scrape <topic>` | scrape |
| `/quiz-creator build` | build |
| `/quiz-creator status` | status |
| `/quiz-creator launch` | launch |
| `/quiz-creator` (no args) | Show available subcommands |

If no subcommand is given or it's unrecognized, show the list with one-line descriptions and ask the user to pick one.

---

## /quiz-creator generate <domain> [count]

Generate exam-style questions for a specific domain from vault source material.

### Arguments

- `<domain>`: Domain number (1-5) or `all` for all domains
- `[count]`: Number of questions per domain (default: 10, split 7 single-answer + 3 multi-select)

### Workflow

1. **Read the exam guide** to understand domain tasks and skills:
   - `{VAULT_PATH}/Sources/Exam-Prep/ai-professional-01.md`
   - Extract the specific Task/Skill items for the requested domain

2. **Identify source material** for the domain:
   - Scan `{VAULT_PATH}/Sources/` for relevant documents
   - Read `references/DOMAIN-SOURCE-MAP.md` for the recommended source-to-domain mapping
   - Read substantial portions of each source to understand what's available
   - If sources are insufficient, recommend scraping additional docs first

3. **Generate questions** following these quality requirements:
   - **Scenario-based**: Each question starts with a company/developer facing a real problem (2-3 paragraphs)
   - **Multi-service**: Most questions involve 2+ AWS services in the scenario
   - **Plausible distractors**: Wrong answers must be real AWS services/features used incorrectly
   - **Sourced explanations**: Every explanation (correct AND incorrect) cites specific source doc content explaining WHY
   - **Exam-aligned**: Map each question to a specific Task/Skill from the exam guide
   - **Question types**: 70% single-answer (A-D), 30% multi-select (A-E, "Select TWO")

4. **Write the question file** to `{GENERATED_DIR}/domain-{N}-generated.md`:

```markdown
---
type: generated-questions
domain: {N}
domain_name: "{Domain Name}"
question_count: {count}
sources:
  - "[[Sources/path/to/source1]]"
  - "[[Sources/path/to/source2]]"
generated: {date}
---

# Domain {N}: {Domain Name}

## Question 1

> [!question] Question — Descriptive Title (Task X.Y)
> Real-world scenario text (2-3 paragraphs)...
>
> Which solution will meet these requirements?
>
> **A.** Option text
>
> **B.** Option text
>
> **C.** Option text
>
> **D.** Option text

> [!example]- Answer: B
> **Correct Answer:** B
>
> **A. Incorrect.** Detailed explanation citing source doc...
>
> **B. Correct.** Detailed explanation citing source doc...
>
> **C. Incorrect.** Detailed explanation...
>
> **D. Incorrect.** Detailed explanation...

## Question 2
...
```

For multi-select questions:
```markdown
> Which combination of steps will meet these requirements? (Select TWO.)
>
> **A.** through **E.**

> [!example]- Answer: B, D
```

5. **Output summary:**
```
══════════════════════════════════════
  Questions Generated
══════════════════════════════════════
  Domain:    {N} - {Domain Name}
  Questions: {count} ({single} single + {multi} multi-select)
  File:      {GENERATED_DIR}/domain-{N}-generated.md
  Sources:   {N} documents referenced
──────────────────────────────────────
  Run /quiz-creator launch to test
  Commit when ready
══════════════════════════════════════
```

---

## /quiz-creator scrape <topic>

Scrape AWS documentation pages to fill source material gaps.

### Workflow

1. **Determine what to scrape:**
   - If `<topic>` is a URL, scrape that URL directly
   - If `<topic>` is a service name (e.g., "bedrock-agents"), use Firecrawl to find the right AWS docs page
   - If `<topic>` is a domain number, scrape recommended gap-fill docs from `references/DOMAIN-SOURCE-MAP.md`

2. **Scrape using Firecrawl:**
   ```bash
   firecrawl scrape "<url>" --only-main-content -o .firecrawl/{topic}.md
   ```

3. **Clean the scraped content:**
   - Remove cookie banners and navigation elements (everything before first `# ` heading)
   - Remove blocked widget notices at the end
   - Add YAML frontmatter:
     ```yaml
     ---
     type: scraped-source
     source_url: "{url}"
     topic: "{topic description}"
     scraped: {date}
     ---
     ```

4. **Copy to vault Sources/**:
   - Determine the correct subdirectory (AWS-Gen-AI, AWS-Core, AWS-ML, AWS-Security, etc.)
   - Copy to `{VAULT_PATH}/Sources/{subdirectory}/{filename}.md`

5. **Update the scraped sources README**:
   - Append an entry to `{VAULT_PATH}/Sources/scraped-sources-readme.md`

6. **Output:**
   ```
   Scraped: {topic}
     URL:  {url}
     Dest: Sources/{subdirectory}/{filename}.md
     Size: {lines} lines

   Run /quiz-creator generate to create questions from this source
   ```

---

## /quiz-creator build

Build or rebuild the quiz app from scratch. Creates `quiz_server.py` and `quiz_app.html`.

### Workflow

1. **Create project directory** at `{QUIZ_DIR}/` if it doesn't exist.

2. **Generate `quiz_server.py`** — Python stdlib HTTP server that:
   - Parses single-question files (BenchPrep practice/bonus format)
   - Parses multi-question generated files (split on `## Question N`)
   - Extracts domain metadata from frontmatter
   - Serves HTML and JSON API endpoints:
     - `GET /` — serve quiz_app.html
     - `GET /api/questions` — all parsed questions as JSON
     - `GET /api/progress` — read progress.json
     - `POST /api/progress` — write progress.json
   - Auto-opens browser on startup

3. **Generate `quiz_app.html`** — Self-contained UI with:
   - **Start screen**: Domain mode buttons (D1-D5), plus All/BenchPrep/Generated/Missed/Random/Shuffle
   - **Quiz screen**: Question display with radio/checkbox options, domain-grouped sidebar with expandable sections
   - **Results screen**: Overall score, per-domain breakdown with progress bars, missed question review
   - **Features**: Keyboard shortcuts (1-5, Enter, arrows, F), flag/bookmark, progress persistence

4. **Test:**
   ```bash
   cd {QUIZ_DIR} && python quiz_server.py
   ```

---

## /quiz-creator status

Show current state of the quiz system.

### Workflow

1. **Count questions** by source:
   - BenchPrep practice questions (from Practice-Questions/)
   - BenchPrep bonus questions (from Bonus-Questions/)
   - Generated questions per domain (from Generated-Questions/)

2. **Show source material coverage:**
   - List source documents per domain
   - Flag domains with thin coverage

3. **Output:**
   ```
   ══════════════════════════════════════
     Quiz Creator Status
   ══════════════════════════════════════
     Questions
     ────────────────────────────────────
     Domain 1 (FM Integration):      10
     Domain 2 (Implementation):      10
     Domain 3 (Safety/Security):     10
     Domain 4 (Optimization):        10
     Domain 5 (Testing):             10
     BenchPrep Practice:             14
     BenchPrep Bonus:                 2
     ────────────────────────────────────
     Total:                          66

     Source Coverage
     ────────────────────────────────────
     AWS-Gen-AI:    10 files
     AWS-Core:       2 files
     Exam-Prep:      1 file + 6 Skill Builder
     ────────────────────────────────────

     Quiz App: {QUIZ_DIR}/quiz_server.py
     Progress: {exists/none}
   ══════════════════════════════════════
   ```

---

## /quiz-creator launch

Stop any existing quiz server and launch a fresh one.

### Workflow

1. Kill any existing process on port 8765:
   ```bash
   for pid in $(netstat -ano | grep "8765.*LISTENING" | awk '{print $5}' | sort -u); do
       taskkill //PID $pid //F 2>/dev/null
   done
   ```

2. Launch the server:
   ```bash
   cd {QUIZ_DIR} && python quiz_server.py
   ```

3. Report the URL: `http://localhost:8765`

---

## Domain Reference

| Domain | Name | Exam Weight |
|--------|------|-------------|
| 1 | Foundation Model Integration, Data Management, and Compliance | 31% |
| 2 | Implementation and Integration | 26% |
| 3 | AI Safety, Security, and Governance | 20% |
| 4 | Operational Efficiency and Optimization for GenAI Applications | 12% |
| 5 | Testing, Validation, and Troubleshooting | 11% |

## Question Format Rules

### Callout format (must match for parser compatibility)

- Questions use `> [!question] Question — Title (Task X.Y)` callout
- Options use `> **A.** Option text` format (each on its own `>` line)
- Answers use `> [!example]- Answer: B` callout (dash after `]` is required)
- Multi-select answers: `> [!example]- Answer: B, D`
- Explanations use `> **A. Correct/Incorrect.** Explanation text` format

### File naming

- Generated files: `domain-{N}-generated.md` in `Generated-Questions/`
- One file per domain, multiple questions per file separated by `## Question N`

## Question JSON Structure

The parser produces this structure per question:

```json
{
  "id": "d1-01",
  "source_file": "domain-1-generated.md",
  "title": "Descriptive Title",
  "type": "single|multi-select|ordering",
  "select_count": 1,
  "body": "Scenario text...",
  "options": [{"letter": "A", "text": "..."}],
  "correct_answers": ["B"],
  "correct_order": null,
  "explanations": {"A": {"correct": false, "text": "..."}},
  "set": "generated",
  "domain": 1,
  "domain_name": "Foundation Model Integration, Data Management, and Compliance"
}
```

## Related Skills

| Skill | Relationship |
|---|---|
| `/aws-vault` | Manages the vault where source docs and generated questions live |
| `/firecrawl` | Scrapes AWS documentation for source material |
| `/web-research` | Research topics online before generating questions |
| `/notebooklm` | Analyze source docs to identify testable concepts per domain |
| `/guided-learning` | Teach concepts that quiz results reveal as weak areas |

## Git Workflow

After any changes, remind the user:

```
Commit quiz app changes:
  cd C:/Users/samue/repos/aip-c01-quiz
  git add -A && git commit -m "description"

Commit vault changes (generated questions, scraped sources):
  git --git-dir=C:/Users/samue/repos/aws_learn_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/aws_learn_vault add -A
  git --git-dir=C:/Users/samue/repos/aws_learn_vault.git --work-tree=C:/Users/samue/OneDrive/Obsidian/aws_learn_vault commit -m "description"
```

Do NOT auto-commit. The user decides when to snapshot.
