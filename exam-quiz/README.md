# exam-quiz

Stage 3 of the exam prep pipeline. Generates practice questions from study guides + NotebookLM data and builds a runnable static quiz app. Run after `/exam-prep` has produced domain guides.

## Prerequisites

### 1. Obsidian

Download and install Obsidian: **https://obsidian.md/download**

Your question files (`.md`) are written to the Obsidian vault so you can review them alongside your study guides.

### 2. Python (for the quiz server)

```bash
pip install flask
```

### 3. Completed study guides

Run `/exam-prep generate all` first. The quiz generator reads domain guides to extract self-check questions and scenario content.

---

## Quick Start

```bash
# 1. Run after /exam-prep generate all
/exam-quiz setup

# 2. Generate questions for all domains
/exam-quiz generate all

# 3. Build the static quiz app
/exam-quiz build

# 4. Launch the quiz server (http://localhost:8767)
/exam-quiz launch
```

---

## What Gets Generated

- `<exam-code>-quiz-domain-<N>-<slug>.md` — Obsidian question files (`[!question]` / `[!example]-` callout blocks)
- `domain-<N>-<slug>.json` — JSON question data for the quiz app
- `_coverage-map.md` — Task coverage tracker (COVERED / PARTIAL / GAP per task)
- `index.html` — Static quiz app with domain/difficulty filters, score tracking, flag for review

---

## Full Pipeline

```
/exam-notebooklm   ← Stage 1: create notebook, add sources
/exam-prep         ← Stages 0+1+2: scaffold vault + study guides
/exam-quiz         ← Stage 3: generate quiz questions + quiz app
```

## Related Skills

- `/exam-notebooklm` — create and populate the NotebookLM notebook
- `/exam-prep` — prerequisite: generates the study guides this skill reads from
