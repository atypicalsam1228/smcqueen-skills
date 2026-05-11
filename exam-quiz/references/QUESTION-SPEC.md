# Question Spec — Format, JSON Schema, and Quiz App Structure

Defines the question format for both Obsidian vault (.md) and the static quiz app (JSON + HTML).

> **Obsidian syntax reference:** Callout syntax (`[!question]`, `[!example]-`) and wikilink formatting used in the `.md` question files follow the [`obsidian-markdown`](https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-markdown) skill from `kepano/obsidian-skills`. The `-` suffix on `[!example]-` creates a collapsed (foldable) callout per the Obsidian Flavored Markdown spec.

---

## Obsidian Question Format (.md files)

Each question uses two nested callouts: `[!question]` for the stem + options, then `[!example]-` (collapsible) for the answer block. This matches the CMMC CCP quiz format.

```markdown
> [!question] [Short question title]
> [Full scenario question text — 2-4 sentences describing the situation and what needs to be determined]
>
> A. [Option A text]
> B. [Option B text]
> C. [Option C text]
> D. [Option D text]

> [!example]- Answer
> **Correct answer: [Letter]. [Correct option text]**
>
> **Why [Letter] is correct:** [2-3 sentences explaining the concept and why this is right]
>
> **Why the others are wrong:**
> - **[Letter]:** [Why this distractor is tempting and why it's wrong]
> - **[Letter]:** [Why this distractor is wrong]
> - **[Letter]:** [Why this distractor is wrong]
>
> *Domain [N] — Task [N.X]: [Task Name]*
```

### Complete Example

```markdown
> [!question] CloudWatch Alarm State After Recovery
> An EC2 instance is being monitored by a CloudWatch alarm configured to alert when
> CPU utilization exceeds 80% for 5 consecutive minutes. After the alarm triggers
> and the instance is recovered, the alarm state is still showing ALARM even though
> CPU is now at 12%. What is the most likely cause?
>
> A. The alarm has a cooldown period that prevents it from resetting for 15 minutes
> B. CloudWatch alarms require manual acknowledgment before returning to OK state
> C. Insufficient data points have been collected since recovery to evaluate the threshold
> D. The alarm action that fires on ALARM state is blocking the state transition

> [!example]- Answer
> **Correct answer: C. Insufficient data points have been collected since recovery to evaluate the threshold**
>
> **Why C is correct:** A CloudWatch alarm transitions from ALARM to OK only after
> it evaluates enough consecutive data points below the threshold (matching the configured
> evaluation period). If fewer data points exist than the evaluation period requires,
> the alarm may show INSUFFICIENT_DATA or remain in ALARM until enough points accumulate.
>
> **Why the others are wrong:**
> - **A:** CloudWatch alarms do not have a built-in cooldown period that prevents state transitions.
> - **B:** CloudWatch alarms do not require manual acknowledgment — they automatically transition states based on metric data.
> - **D:** Alarm actions (SNS publish, EC2 action) execute when state changes; they do not block state transitions.
>
> *Domain 1 — Task 1.1: CloudWatch Alarms and Metrics*
```

---

## JSON Schema (quiz app)

Each domain's questions are stored in a JSON file with this schema:

```json
{
  "exam_code": "SOA-C03",
  "domain": 1,
  "domain_name": "Monitoring, Logging, and Remediation",
  "domain_weight": "20%",
  "questions": [
    {
      "id": "soa-c03-d1-001",
      "title": "CloudWatch Alarm State After Recovery",
      "scenario": "An EC2 instance is being monitored by a CloudWatch alarm configured to alert when CPU utilization exceeds 80% for 5 consecutive minutes. After the alarm triggers and the instance is recovered, the alarm state is still showing ALARM even though CPU is now at 12%. What is the most likely cause?",
      "options": {
        "A": "The alarm has a cooldown period that prevents it from resetting for 15 minutes",
        "B": "CloudWatch alarms require manual acknowledgment before returning to OK state",
        "C": "Insufficient data points have been collected since recovery to evaluate the threshold",
        "D": "The alarm action that fires on ALARM state is blocking the state transition"
      },
      "correct": "C",
      "explanations": {
        "A": "CloudWatch alarms do not have a built-in cooldown period that prevents state transitions.",
        "B": "CloudWatch alarms do not require manual acknowledgment — they automatically transition states based on metric data.",
        "C": "CORRECT: A CloudWatch alarm transitions from ALARM to OK only after it evaluates enough consecutive data points below the threshold matching the configured evaluation period.",
        "D": "Alarm actions execute when state changes; they do not block state transitions."
      },
      "task": "1.1",
      "task_name": "CloudWatch Alarms and Metrics",
      "difficulty": "medium",
      "tags": ["cloudwatch", "alarms", "monitoring"]
    }
  ]
}
```

### Field Definitions

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | `<exam-code>-d<N>-<seq>` — must be unique |
| `title` | string | yes | Short title for coverage tracking |
| `scenario` | string | yes | Full question text |
| `options` | object | yes | Keys A, B, C, D — always exactly 4 |
| `correct` | string | yes | Single letter: "A", "B", "C", or "D" |
| `explanations` | object | yes | Keys A, B, C, D — prefix correct with "CORRECT: " |
| `task` | string | yes | e.g., "1.1", "3.4" |
| `task_name` | string | yes | Verbatim task name from exam guide |
| `difficulty` | string | yes | "easy", "medium", "hard" |
| `tags` | array | optional | Service names, concepts |

---

## Quiz App Structure

The static quiz app lives in `QUIZ_DIR/`:

```
QUIZ_DIR/
├── index.html          ← Single-page quiz app
├── questions.js        ← All questions merged into one JS data file
├── quiz_server.py      ← Flask dev server (port 8767)
└── static/
    ├── quiz.css        ← App styles
    └── quiz.js         ← App logic (separate from data)
```

### `questions.js` format

Generated by `/exam-quiz build` — merges all domain JSON files:

```javascript
const QUIZ_DATA = {
  exam: "SOA-C03",
  exam_name: "AWS Certified SysOps Administrator – Associate",
  domains: [
    {
      domain: 1,
      domain_name: "Monitoring, Logging, and Remediation",
      domain_weight: "20%",
      questions: [ /* ... array of question objects ... */ ]
    },
    /* ... remaining domains ... */
  ],
  total_questions: 106
};
```

### `index.html` Features

- Domain filter dropdown (All / Domain 1 / Domain 2 / ...)
- Difficulty filter (All / Easy / Medium / Hard)
- Shuffle button
- Question counter (X of N)
- Progress bar
- Answer buttons (A / B / C / D) that highlight green/red on selection
- Explanation panel (hidden until answer selected)
- "Next" button to advance
- Score tracker (correct/total for session)
- Flag button to mark questions for review
- Review mode: show only flagged questions

### `quiz.css` Requirements

- Clean, readable layout — no dark mode required
- Options displayed as clickable buttons, not radio inputs
- Correct answer highlights green, wrong answer highlights red
- Explanation panel uses monospace or readable font
- Mobile-responsive (works on tablet for studying)

---

## Question Quality Standards

### Required for every question

- Scenario is operational ("A company/engineer/team needs to...") — never "What is X?"
- All 4 distractors are real AWS features or plausible configurations
- The correct answer is unambiguously correct given current AWS behavior
- Per-option explanations explain WHY, not just restate the option text
- Task tag maps to a real task in the exam guide

### Difficulty calibration

| Level | Characteristics |
|---|---|
| easy | Tests a single concept; distractors are clearly different services or features |
| medium | Tests operational judgment; one distractor is plausible but subtly wrong |
| hard | Tests threshold/limit knowledge, edge cases, or "most likely cause" with multiple plausible options |

### Target distribution per domain

- 30% easy, 50% medium, 20% hard
- At least one question per task (≥ 3 questions for high-weight tasks)
- At least 2 "most likely cause" troubleshooting questions per domain
- At least 1 question that tests a high-frequency exam trap from the domain guide

---

## Coverage Map Update Rules

After generating questions for a domain, update `_coverage-map.md`:

| Questions added | New status |
|---|---|
| 0 | GAP |
| 1–2 | PARTIAL |
| ≥ 3 | COVERED |

Mark as GAP if the task appears in the exam guide task statements but has no questions yet — even if the domain guide covers it conceptually.
