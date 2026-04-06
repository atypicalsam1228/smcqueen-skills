# Quiz Creator Skill

Generate exam-style practice quiz applications from authoritative source documents. Built for AWS certification prep but adaptable to any exam.

## What It Does

The complete quiz creation pipeline:

1. **Scrape** — Pull AWS documentation pages into your vault as authoritative sources using Firecrawl
2. **Generate** — Create scenario-based exam questions from source docs, organized by exam domain
3. **Build** — Produce a self-contained Python + HTML quiz app (zero dependencies)
4. **Launch** — Start the local quiz server and open in browser

## Architecture

```
Vault (Sources/)                    Quiz App
┌──────────────────┐               ┌──────────────────────┐
│ AWS-Gen-AI/      │──┐            │ quiz_server.py       │
│ AWS-Core/        │  │  parse     │   - Markdown parser  │
│ Exam-Prep/       │  ├──────────► │   - HTTP server      │
│   Practice-Q/    │  │            │   - JSON API         │
│   Bonus-Q/       │  │            ├──────────────────────┤
│   Generated-Q/   │──┘            │ quiz_app.html        │
│     domain-1.md  │               │   - Start screen     │
│     domain-2.md  │               │   - Domain sidebar   │
│     domain-3.md  │               │   - Quiz UI          │
│     domain-4.md  │               │   - Results + scores │
│     domain-5.md  │               │   - Progress persist │
└──────────────────┘               └──────────────────────┘
```

## Quick Start

```bash
# Generate questions for all domains
/quiz-creator generate all

# Generate 15 questions for Domain 1 only
/quiz-creator generate 1 15

# Scrape a missing AWS doc
/quiz-creator scrape https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html

# Build the quiz app from scratch
/quiz-creator build

# Launch the quiz
/quiz-creator launch
```

## Question Format

Questions are stored as Obsidian-compatible markdown in the vault using callout syntax:

```markdown
## Question 1

> [!question] Question — Descriptive Title (Task 1.2)
> A company is building a generative AI application...
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

## Quiz App Features

- **66 questions** across 5 exam domains + 16 BenchPrep originals
- **Domain-grouped sidebar** with expandable sections and per-domain scoring
- **Multiple quiz modes**: By domain, all, BenchPrep only, generated only, missed, random, shuffled
- **Detailed explanations** for every answer (correct and incorrect)
- **Progress tracking** persisted to JSON — resume across sessions
- **Per-domain results** with progress bars on the results screen
- **Keyboard shortcuts**: 1-5 select, Enter check/next, arrows navigate, F flag
- **Zero dependencies** — Python stdlib only, runs anywhere

## File Layout

```
~/.claude/skills/quiz-creator/
├── SKILL.md                          # Skill definition
├── README.md                         # This file
└── references/
    └── DOMAIN-SOURCE-MAP.md          # Domain → source document mapping

~/repos/aip-c01-quiz/
├── quiz_server.py                    # Parser + HTTP server
├── quiz_app.html                     # Self-contained quiz UI
└── progress.json                     # Auto-created session data

~/OneDrive/Obsidian/aws_learn_vault/Sources/
├── Exam-Prep/Generated-Questions/    # Generated question files
│   ├── domain-1-generated.md
│   ├── domain-2-generated.md
│   ├── domain-3-generated.md
│   ├── domain-4-generated.md
│   └── domain-5-generated.md
└── scraped-sources-readme.md         # Index of scraped docs
```

## AIP-C01 Exam Domains

| # | Domain | Weight | Questions |
|---|--------|--------|-----------|
| 1 | Foundation Model Integration, Data Management, and Compliance | 31% | 10 |
| 2 | Implementation and Integration | 26% | 10 |
| 3 | AI Safety, Security, and Governance | 20% | 10 |
| 4 | Operational Efficiency and Optimization | 12% | 10 |
| 5 | Testing, Validation, and Troubleshooting | 11% | 10 |

## Related Skills

- `/aws-vault` — Manages the Obsidian vault where sources and questions live
- `/firecrawl` — Scrapes AWS documentation pages
- `/notebooklm` — Analyze sources to identify testable concepts
- `/web-research` — Research topics before question generation
- `/guided-learning` — Teach weak areas identified by quiz results
