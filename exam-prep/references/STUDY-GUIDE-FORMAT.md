# Study Guide Format — Domain Guide Template

Complete template for `/exam-prep generate`. Every domain guide follows this structure exactly. Sections marked `[REQUIRED]` must appear in every domain guide.

> **Obsidian syntax reference:** All callout types, wikilink formats, embed syntax, and frontmatter conventions in this template come from the [`obsidian-markdown`](https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-markdown) skill (`kepano/obsidian-skills`). Install it alongside this skill for the authoritative syntax spec.

---

## File Header [REQUIRED]

```markdown
---
type: guide
domain: <domain-slug>
status: final
tags:
  - <exam-code>/domain<N>
  - study-guide
  - <primary-service-1>
  - <primary-service-2>
  - <primary-service-3>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources:
  - "[[Sources/Exam-Prep/<exam-code>-domain<N>-task-statements]]"
  - "[[Sources/Exam-Prep/<exam-code>-in-scope-services]]"
  - "[[Sources/<domain-dir>/<exam-code>-domain<N>-<slug>]]"
  - "[[Sources/Exam-Prep/<exam-code>-mind-map]]"
related:
  - "[[Wiki/study-guide/<exam-code>-study-guide]]"
  - "[[Wiki/<exam-code>-Domain<N>-<Name>]]"
---
```

---

## Title and Abstract [REQUIRED]

```markdown
# [EXAM_CODE] Study Guide — Domain N: [Domain Name] ([Weight]%)

> [!abstract]
> Domain N ([Domain Name]) carries **[Weight]%** of the exam. [2-3 sentences: what it tests, the core principle the exam uses to select correct answers for this domain, and what services/patterns dominate.] Memorize [the key distinction that separates wrong answers from right answers in this domain].
```

---

## Self-Check Questions [REQUIRED — 5–6 questions]

```markdown
---

## Self-Check Questions

Before reading, attempt these without notes:

> [!question] Self-Check 1
> [Scenario or operational question — not a definition question]
> **Expected answer:** [Detailed answer covering the key insight, correct AWS pattern, and why distractors are wrong]

> [!question] Self-Check 2
> [Scenario question — progressively harder than SC1]
> **Expected answer:** [Answer]

> [!question] Self-Check 3
> [Comparison or "which service" question]
> **Expected answer:** [Answer with explicit service comparison if relevant]

> [!question] Self-Check 4
> [Configuration or threshold question — tests specific knowledge]
> **Expected answer:** [Answer with specific thresholds, limits, or settings]

> [!question] Self-Check 5
> [Most complex — multi-service or "what is the most likely cause" question]
> **Expected answer:** [Answer]

> [!question] Self-Check 6 [optional — add if domain is large]
> [Question]
> **Expected answer:** [Answer]
```

---

## Task Sections [REQUIRED — one per task statement]

Each task section follows this pattern exactly. The `[!warning]` and `[!tip]` callouts are EMBEDDED here — not separated into a different file.

```markdown
---

## Task N.X — [Task Name]

> [!quote] [Source Name]
> "[Verbatim or close paraphrase from the NLM source that introduces this task]"
> — [[Sources/<domain-dir>/<source-file>|<Source Display Name>]]

### [Subtopic or Service Area]

[Concept explanation — prose or table. Focus on operational behavior the exam tests, not service overviews.]

| Column A | Column B | Column C |
|---|---|---|
| [Value] | [Value] | [Value] |

[Second subtopic or comparison table if needed]

> [!warning] Exam Trap: [Trap Name]
> [Description of the distractor pattern — what the wrong answer looks like and why it's tempting]
> **Correct answer:** [What you should pick instead and why]

[Additional concept explanation if needed]

> [!example] Exam Scenario — [Scenario Name]
> [3–5 sentence scenario describing the situation, requirement, and context]
> **Answer:** [Correct AWS answer] — [2–3 sentence reasoning covering why this is right and why the distractor is wrong]

> [!tip] [Short descriptive title]
> [Community intel insight — what Reddit passers said about this topic, what they were surprised by, or what they wish they had studied. Keep it specific and actionable.]
```

**Pattern repetition:** Every major task section should have:
- ≥ 1 `[!quote]` at the top
- ≥ 1 `[!warning]` trap (more if the task has multiple trap patterns)
- ≥ 1 `[!example]` scenario
- ≥ 1 `[!tip]` community intel (per major task — can be omitted for minor sub-tasks)

---

## Second Quote Option

If a task has two authoritative source points, use a second `[!quote]` mid-section:

```markdown
> [!quote] [Second Source Name]
> "[Quote from in-scope services list or another source]"
> — [[Sources/Exam-Prep/<source-file>|<Display Name>]]
```

---

## Domain Summary Table [REQUIRED]

```markdown
---

## Domain N Summary

> [!abstract] Domain N Key Takeaways

| Area | Critical Facts |
|---|---|
| [Service or concept] | [The one fact the exam tests about this — be specific: thresholds, limits, behavior] |
| [Service or concept] | [Critical fact] |
| [Service or concept] | [Critical fact] |
[... one row per major topic in the domain ...]
```

---

## High-Frequency Exam Traps [REQUIRED]

This `[!danger]` block belongs at the end of every domain guide, before Common Wrong Answers. It is the domain-scoped trap table drawn from the TRAP and INTEL queries.

```markdown
> [!danger] High-Frequency Exam Traps
> Community passers flag these patterns repeatedly for Domain N:
>
> | Distractor | What Gets Tested | Correct Answer |
> |---|---|---|
> | [What the wrong answer looks like] | [Concept being tested] | [What you should pick] |
> | [Distractor] | [Concept] | [Correct] |
> | [Distractor] | [Concept] | [Correct] |
> [... minimum 5 rows, target 8–12 for a full domain ...]
```

---

## Common Wrong Answers Table [REQUIRED]

```markdown
### Common Wrong Answers (Domain N)

| Distractor | Correct Answer |
|---|---|
| "[What a wrong answer typically says]" | **[Correct answer — bold the key term]** |
| "[Distractor]" | **[Correct answer]** |
| "[Distractor]" | **[Correct answer]** |
[... one row per major trap in the domain — can overlap with [!danger] table above but use different phrasing ...]
```

---

## Callout Type Reference

| Callout | Obsidian syntax | Purpose |
|---|---|---|
| Abstract | `> [!abstract]` | Domain summary, domain key takeaways |
| Question | `> [!question]` | Self-check questions |
| Quote | `> [!quote]` | Verbatim source citation with wikilink |
| Warning | `> [!warning] Exam Trap: <Name>` | Per-task trap with correct answer |
| Example | `> [!example] Exam Scenario — <Name>` | Scenario question with answer + reasoning |
| Tip | `> [!tip]` | Community intel insight |
| Danger | `> [!danger] High-Frequency Exam Traps` | Domain-scoped trap table at domain end |
| Info | `> [!info]` | Administrative notes (e.g., domain numbering) |

---

## Minimum Callout Counts (enforced by `/exam-prep generate`)

| Callout | Minimum per domain guide |
|---|---|
| `[!warning]` | ≥ 3 |
| `[!danger]` trap table | ≥ 1 (always at domain end) |
| `[!quote]` | ≥ 2 |
| `[!example]` | ≥ 2 |
| `[!tip]` | ≥ 1 per major task section |
| `[!question]` self-check | 5–6 |

---

## File Naming

```
<exam-code>-study-guide-domain-<N>-<slug>.md
```

Slug = lowercase domain name, spaces to hyphens, remove articles:
- "Monitoring, Logging, and Remediation" → `monitoring`
- "Reliability and Business Continuity" → `reliability`
- "Deployment, Provisioning, and Automation" → `deployment`
- "Security and Compliance" → `security`
- "Networking and Content Delivery" → `networking`
- "Cost and Performance Optimization" → `cost-performance`

---

## Obsidian Link Rules

- Internal file references: `[[Wiki/study-guide/filename|Display Text]]`
- Source citations: `[[Sources/path/to/source|Source Title]]`
- Never use standard markdown links `[text](url)` for internal references
- All callouts use `> [!type]` syntax — never `> **Note:**` or `> **Warning:**`
