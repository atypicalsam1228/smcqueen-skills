# Quiz Creator Skill

Generate exam-style practice quiz applications from authoritative source documents. Built for AWS AIP-C01 but adaptable to any certification exam.

## What It Does

The complete quiz creation pipeline:

1. **Setup** — Parse an exam guide/syllabus to extract domains, tasks, and skills as a coverage map
2. **Scrape** — Pull documentation pages into your vault as authoritative sources
3. **Generate** — Create constraint-based trade-off questions tagged by domain and task
4. **Gap Analysis** — Cross-reference questions against the exam guide to find uncovered skills
5. **Gap Fill** — Generate targeted questions for uncovered skills
6. **Build** — Produce a self-contained Python + HTML quiz app (zero dependencies)
7. **Launch** — Start the local quiz server and open in browser

## Pipeline Overview

```
 Upload Exam Guide         Ingest Source Docs        Generate Questions
 ┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐
 │ Extract domains │      │ PDFs, web scrapes │      │ Constraint-based │
 │ tasks, skills   │─────►│ screencaptures,  │─────►│ trade-off format │
 │ Build coverage  │      │ course material   │      │ Domain+task tags │
 │ map             │      │ test-taker intel  │      │ Detailed explain │
 └─────────────────┘      └──────────────────┘      └──────────────────┘
                                                            │
 ┌─────────────────┐      ┌──────────────────┐             │
 │ Study + retry   │      │ Build quiz app   │             ▼
 │ missed questions│◄─────│ Domain sets      │      ┌──────────────────┐
 │ Track progress  │      │ Topic drill-down │◄─────│ Gap analysis     │
 │ Improve scores  │      │ Answer shuffle   │      │ Fill uncovered   │
 └─────────────────┘      └──────────────────┘      │ skills           │
                                                     └──────────────────┘
```

## Architecture

```
Source Documents                    Quiz App
┌──────────────────────┐           ┌──────────────────────────┐
│ Sources/             │           │ quiz_server.py           │
│   AWS-Gen-AI/        │──┐       │   - Markdown parser      │
│   AWS-Core/          │  │       │   - Domain/task classify  │
│   Exam-Prep/         │  │ parse │   - Task interleaving    │
│     Practice-Q/      │  ├──────►│   - HTTP server + API    │
│     Bonus-Q/         │  │       ├──────────────────────────┤
│     Generated-Q/     │──┘       │ quiz_app.html            │
│       domain-1-5.md  │          │   - Domain sets (15-20q) │
│       trade-off.md   │          │   - Topic drill-down     │
│       agentic-ai.md  │          │   - Answer shuffling     │
│       safety-gov.md  │          │   - 3-retry missed Qs    │
│       svc-diff.md    │          │   - Progress tracking    │
│       gap-fill.md    │          │   - Keyboard shortcuts   │
│       skillbuilder.md│          └──────────────────────────┘
│       screencapture.md│
└──────────────────────┘
```

## Quiz App Features

- **202 questions** across 5 exam domains from 12 question files
- **Domain sets of 15-20 questions** — manageable ~30 min sessions
- **Task-balanced distribution** — round-robin interleaving so each set covers all tasks in the domain
- **Topic-focused mode** — drill down on RAG, Agents, Guardrails, Cost, Monitoring, etc.
- **Randomized answer order** — A-D positions shuffled each session, reshuffled on retry
- **3-attempt retry for missed questions** — immediate reinforcement with attempt history tracking
- **Auto domain classification** — keyword-based classifier for untagged questions
- **Auto task classification** — keyword-based task tagging for balanced interleaving
- **Multiple quiz modes**: domain sets, topics, all, missed, random 10, shuffled, BenchPrep, generated
- **Domain-grouped sidebar** with expandable sections and per-domain scoring
- **Detailed explanations** for every answer (correct and incorrect, 4+ sentences each)
- **Progress tracking** persisted to JSON — resume across sessions
- **Per-domain results** with progress bars and attempt history
- **Keyboard shortcuts**: 1-5 select, Enter check/next, arrows navigate, F flag
- **Zero dependencies** — Python stdlib only, runs anywhere

## Quick Start

```bash
# Step 1: Parse the exam guide (required)
/quiz-creator setup path/to/exam-guide.pdf

# Step 2: Generate questions for all domains
/quiz-creator generate all

# Step 3: Run gap analysis
/quiz-creator gap-analysis

# Step 4: Fill gaps
/quiz-creator gap-fill

# Step 5: Build and launch
/quiz-creator build
/quiz-creator launch
```

## Question Format

Questions are stored as Obsidian-compatible markdown using callout syntax:

```markdown
## Question 1

> [!question] Question — Descriptive Title (Domain 1)
> A company is building a generative AI application...
> The system must meet a 500ms latency SLA...
>
> Which solution will meet these requirements?
>
> **A.** Use Amazon Bedrock Knowledge Bases...
> **B.** Build a custom RAG pipeline...
> **C.** Use Amazon Kendra...
> **D.** Deploy SageMaker endpoints...

> [!example]- Answer: A
> **Correct Answer:** A
>
> **A. Correct.** Amazon Bedrock Knowledge Bases provides...
> **B. Incorrect.** While functional, this requires...
> **C. Incorrect.** Kendra provides search but...
> **D. Incorrect.** SageMaker endpoints add...
```

## AIP-C01 Implementation Stats

| # | Domain | Weight | Questions |
|---|--------|--------|-----------|
| 1 | Foundation Model Integration, Data Management, and Compliance | 31% | 55 |
| 2 | Implementation and Integration | 26% | 50 |
| 3 | AI Safety, Security, and Governance | 20% | 45 |
| 4 | Operational Efficiency and Optimization | 12% | 31 |
| 5 | Testing, Validation, and Troubleshooting | 11% | 21 |
| | **Total** | | **202** |

**Skill coverage: 83/89 exam guide skills (93%)**

## File Layout

```
~/.claude/skills/quiz-creator/
├── SKILL.md                                # Skill definition (subcommands + workflows)
├── README.md                               # This file
└── references/
    ├── DOMAIN-SOURCE-MAP.md                # AIP-C01: domain → source document mapping
    └── QUESTION-GENERATION-GUIDE.md        # How to generate high-quality exam questions

~/repos/aip-c01-quiz/
├── quiz_server.py                          # Parser + classifier + HTTP server (720 lines)
├── quiz_app.html                           # Self-contained quiz UI (1062 lines)
└── progress.json                           # Auto-created session data

~/OneDrive/Obsidian/aws_learn_vault/Sources/Exam-Prep/Generated-Questions/
├── _index.md                               # Question file index
├── domain-1-generated.md through domain-5-generated.md  # 50 original (revised)
├── trade-off-questions.md                  # 25 constraint-based trade-offs
├── domain-3-safety-governance.md           # 10 safety/governance deep-dive
├── agentic-ai-questions.md                 # 8 agentic AI questions
├── service-differentiation.md              # 10 service comparison questions
├── skillbuilder-extracted-questions.md     # 33 converted Skill Builder questions
├── screencapture-tradeoff-questions.md     # 30 screencapture trade-offs
└── gap-filling-questions.md                # 20 gap-filling questions
```

## Related Skills

- `/aws-vault` — Manages the Obsidian vault where sources and questions live
- `/firecrawl` — Scrapes documentation pages for source material
- `/notebooklm` — Analyze sources to identify testable concepts per domain
- `/web-research` — Research topics online before question generation
- `/guided-learning` — Teach weak areas identified by quiz results
