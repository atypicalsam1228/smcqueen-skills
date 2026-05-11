---
name: exam-quiz
description: "Stage 3 of the exam prep pipeline. Generates domain question files and a runnable quiz app from study guide + NotebookLM data. Produces Obsidian-format question .md files with [!question]/[!example]- callout blocks and a static HTML quiz app. Works with any certification exam."
---

# Exam Quiz — Practice Question Generation

Generates practice questions from completed study guides and NotebookLM data. Run after `/exam-prep` has produced domain guides. Questions are written in scenario format with per-option reasoning, tagged by domain and task, and exported to both Obsidian-format .md files and a runnable static quiz app.

## Configuration

```
EXAM_NAME:        e.g., "AWS Certified SysOps Administrator – Associate (SOA-C03)"
EXAM_CODE:        e.g., "SOA-C03"
NOTEBOOK_ID:      e.g., "806bd12a-4494-4630-9771-33fdc2f24db3"
STUDY_GUIDE_DIR:  e.g., "C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer/Wiki/study-guide"
QUIZ_DIR:         e.g., "C:/Users/samue/repos/soa-c03-quiz"
VAULT_QUIZ_DIR:   e.g., "C:/Users/samue/OneDrive/Obsidian/AWS_Cloud_Ops_Engineer/Wiki/quiz"
DOMAINS:          Inherited from /exam-prep configuration
```

## Subcommands

| Subcommand | Purpose |
|---|---|
| `setup` | Scaffold quiz directories, create coverage map, verify study guides exist |
| `generate [domain\|all]` | Generate question files for one or all domains |
| `gap-fill [domain]` | Add questions for tasks with GAP or PARTIAL coverage |
| `build` | Compile question files into a static quiz app |
| `launch` | Start the quiz server |
| `status` | Show question counts and coverage map |

---

## /exam-quiz setup

### Workflow

1. Verify study guide files exist in `STUDY_GUIDE_DIR/`
2. Verify NotebookLM notebook is accessible: `notebooklm source list -n <NOTEBOOK_ID> --json`
3. Create `VAULT_QUIZ_DIR/` if it doesn't exist
4. Create `QUIZ_DIR/` scaffold if it doesn't exist:
   ```
   QUIZ_DIR/
   ├── questions/          ← JSON question files per domain
   ├── static/             ← quiz app HTML/CSS/JS
   └── quiz_server.py      ← Flask dev server
   ```
5. Create `_coverage-map.md` in `VAULT_QUIZ_DIR/`:
   - One row per domain → task, status = NOT_STARTED
6. Report: study guides found, notebook status, output paths

### Output

```
✓ Study guides found: 5 domains
✓ Notebook ready: 63 sources
✓ Quiz dir: C:/Users/samue/repos/soa-c03-quiz/
✓ Vault quiz dir: Wiki/quiz/
✓ Coverage map created: Wiki/quiz/_coverage-map.md

Run: /exam-quiz generate all
```

---

## /exam-quiz generate [domain|all]

Core command. Reads the domain study guide, queries NotebookLM for additional questions, assembles question files.

### Workflow (per domain)

**Step 1 — Read the domain study guide:**
- Extract all `[!question]` self-check questions (reformat for quiz)
- Extract all `[!example]` exam scenarios (convert to full questions with distractors)
- Extract task names and key facts from the domain summary table

**Step 2 — Query NotebookLM for scenario questions:**

```
QUESTIONS: "Generate 8-10 [EXAM_CODE]-style scenario questions for Domain [N] [Name].
Requirements:
- Each question must be a realistic operational scenario ('A company needs...', 'An engineer notices...')
- 4 answer options (A/B/C/D) with one correct and three plausible distractors
- For each option: brief explanation of why it is correct or incorrect
- Cover different tasks across the domain — don't cluster on one task
- Include at least 2 'most likely cause' troubleshooting questions
- Include at least 1 question where the distractor is a real AWS feature
- Difficulty: mix of straightforward (30%), moderate (50%), hard (20%)
Format: question, options A-D, correct answer, per-option explanation, domain tag, task tag"
```

**Step 3 — Query for trap questions:**

```
TRAPS: "Generate 3-4 questions for [EXAM_CODE] Domain [N] that specifically test
the high-frequency exam traps in this domain. These questions should have tempting
wrong answers that reflect real misconceptions (not obviously wrong distractors).
Same format: question, A-D options, correct answer, per-option explanation."
```

**Step 4 — Assemble question files:**

- Vault format: write `[EXAM_CODE]-quiz-domain-[N]-[slug].md` to `VAULT_QUIZ_DIR/`
  - `[!question]` callout for each question
  - `[!example]-` (collapsible) callout for each answer block
- JSON format: write `domain-[N]-[slug].json` to `QUIZ_DIR/questions/`
  - See `references/QUESTION-SPEC.md` for JSON schema

**Step 5 — Update coverage map:** mark all tasks as COVERED in `_coverage-map.md`

### Output

```
✓ Domain 1 generated: Wiki/quiz/soa-c03-quiz-domain-1-monitoring.md
  - 7 self-check questions converted
  - 10 new scenario questions from NLM
  - 4 trap questions
  Total: 21 questions across 6 tasks

Progress: 1/5 domains complete (21 total questions)
```

---

## /exam-quiz gap-fill [domain]

Adds questions for tasks with GAP or PARTIAL status in `_coverage-map.md`.

### Workflow

1. Read `_coverage-map.md` — identify tasks with GAP or PARTIAL status
2. For each gap task, query NLM:
   ```
   "Generate 3-4 additional questions specifically for [EXAM_CODE] Domain [N] Task [X.Y]:
   [Task Name]. These should be harder than baseline — test edge cases, thresholds,
   and less-obvious service behaviors. Same scenario format with A-D options and
   per-option reasoning."
   ```
3. Append questions to the existing domain question file
4. Update `_coverage-map.md`: GAP → COVERED, PARTIAL → COVERED

---

## /exam-quiz build

Compiles question files into a static HTML quiz app.

### Workflow

1. Read all `QUIZ_DIR/questions/*.json` files
2. Merge into a single `questions.js` data file
3. Generate `index.html` using the quiz template (see `references/QUESTION-SPEC.md` for app structure)
4. Copy static assets (CSS, JS) to `QUIZ_DIR/static/`
5. Report: total questions, domain breakdown, output path

### Quiz App Features

- Domain filter (all / domain N)
- Shuffle questions
- Show/hide answer explanations
- Track score for current session
- Flag questions for review
- Progress bar

### Output

```
✓ Build complete
  Questions: 106 across 5 domains
  Output: C:/Users/samue/repos/soa-c03-quiz/index.html
  
Run: /exam-quiz launch
```

---

## /exam-quiz launch

Starts the quiz server.

### Workflow

```bash
cd <QUIZ_DIR>
python quiz_server.py
# Server starts on port 8767
# Opens browser to http://localhost:8767
```

If `quiz_server.py` doesn't exist, generate it:

```python
from flask import Flask, send_from_directory
import os

app = Flask(__name__)
QUIZ_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_from_directory(QUIZ_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(QUIZ_DIR, filename)

if __name__ == '__main__':
    app.run(port=8767, debug=True)
```

---

## /exam-quiz status

Shows question generation progress.

### Output

```
Exam: SOA-C03 — AWS Certified CloudOps Engineer Associate
Notebook: 806bd12a (63 sources, all READY)
Study Guide Dir: Wiki/study-guide/ (5 domain guides)
Quiz Dir: C:/Users/samue/repos/soa-c03-quiz/

Domain Question Files:
  ✓ Domain 1 — Monitoring (20%)      21 questions   soa-c03-quiz-domain-1-monitoring.md
  ✓ Domain 2 — Reliability (16%)     18 questions   soa-c03-quiz-domain-2-reliability.md
  ✓ Domain 3 — Deployment (18%)      22 questions   soa-c03-quiz-domain-3-deployment.md
  ✗ Domain 4 — Security (16%)        NOT GENERATED
  ✗ Domain 5 — Networking (18%)      NOT GENERATED

Coverage Map: Wiki/quiz/_coverage-map.md
  Total tasks: 27
  Covered: 15 (56%)
  Partial: 3 (11%)
  Gap: 9 (33%)

Next: /exam-quiz generate domain4
```

---

## File Naming Convention

```
<exam-code>-quiz-domain-<N>-<slug>.md    ← Obsidian question file
domain-<N>-<slug>.json                   ← JSON for quiz app
_coverage-map.md                         ← Task coverage tracker
```

Examples for SOA-C03:
```
soa-c03-quiz-domain-1-monitoring.md
soa-c03-quiz-domain-2-reliability.md
domain-1-monitoring.json
_coverage-map.md
```

---

## Coverage Map Format

`_coverage-map.md` tracks question coverage per task:

```markdown
# [EXAM_CODE] Quiz Coverage Map

| Domain | Task | Task Name | Status | Questions |
|---|---|---|---|---|
| 1 | 1.1 | CloudWatch Alarms and Metrics | COVERED | 4 |
| 1 | 1.2 | CloudWatch Logs | COVERED | 3 |
| 1 | 1.3 | EventBridge and Automation | PARTIAL | 2 |
| 1 | 1.4 | X-Ray and Application Signals | GAP | 0 |
| 2 | 2.1 | Auto Scaling | COVERED | 4 |
...
```

Status values:
- `COVERED` — ≥ 3 questions for this task
- `PARTIAL` — 1–2 questions for this task
- `GAP` — 0 questions for this task

---

## Related Skills

- `/exam-notebooklm` — Stage 1: set up and populate the NotebookLM notebook
- `/exam-prep` — Stages 1+2: study guide generation (prerequisite for this skill)

## Reference Files

- `references/QUESTION-SPEC.md` — Question format, JSON schema, quiz app structure
