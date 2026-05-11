# Intel Query Templates — NotebookLM Query Patterns

Query templates used by `/exam-prep generate` for each domain. Three parallel domain queries + one self-check query. Six additional queries for `/exam-prep intel`.

---

## Per-Domain Queries (run in parallel for each domain)

### CONTENT Query

```
For [EXAM_NAME] Domain [N] ([Domain Name]): explain every task statement and skill,
key service behaviors, operational patterns, decision matrices, and comparison tables
the exam tests. Be specific — include thresholds, limits, feature names, and exact
service configurations. Cover what distinguishes correct answers from plausible
distractors. Focus on operational judgment scenarios, not service definitions.
```

### TRAP Query

```
For [EXAM_NAME] Domain [N] ([Domain Name]): what are ALL the specific exam traps,
gotchas, common wrong answers, and distractor patterns? For each trap: describe
the distractor (what the wrong answer looks like), what concept it tests, and the
correct answer. Draw from community passers, official exam guide nuances, and
service documentation edge cases. Include traps where the exam uses a real AWS
feature that sounds correct but is the wrong choice for the specific scenario.
```

### INTEL Query

```
For [EXAM_NAME] Domain [N] ([Domain Name]): what does community and Reddit intel say?
Include: high-frequency topics passers were surprised by, what they wish they had
studied more, specific service sub-features that appear on the exam (not just the
parent service), any domain-specific question strategies, and quotes from people
who passed describing what was actually tested. Flag topics that appear disproportionately
often relative to what basic study guides cover.
```

### SELFCHECK Query (sequential, after CONTENT)

```
Generate 5-6 self-check questions for [EXAM_NAME] Domain [N] ([Domain Name]) that test
operational judgment, not service definitions. Requirements:
- Questions must be scenario-based ("A company needs to...", "An engineer notices...")
- Questions should get progressively harder
- Format: question + concise expected answer covering the key insight
- Include at least one comparison question (which service, which configuration)
- Include at least one "most likely cause" or troubleshooting question
- Avoid questions answerable purely from memory (focus on judgment calls)
```

---

## Intel Placement Rules

After collecting CONTENT + TRAP + INTEL responses, distribute callouts using this logic:

| Callout | Trigger | Source query | Placement |
|---|---|---|---|
| `[!warning] Exam Trap: <Name>` | Task section has a known distractor pattern from TRAP query | TRAP | Immediately after the concept it traps — within the task section |
| `[!tip]` | Task section has community signal from INTEL query (surprise topics, frequency patterns) | INTEL | After the main concept explanation or comparison table within the task section |
| `[!example] Exam Scenario` | Task section has a decision matrix or operational pattern from CONTENT query | CONTENT | After comparison tables or decision matrices |
| `[!quote]` | Task section opens — use verbatim phrasing from a real source | CONTENT or source doc | First element of each task section |
| `[!danger] High-Frequency Exam Traps` | Always — one per domain guide | TRAP + INTEL combined | After Domain Summary table, before Common Wrong Answers |

---

## Distribution Heuristic

When assembling a domain guide with 4–7 task sections:

1. **TRAP response** → distribute `[!warning]` callouts across tasks where the trap applies, not all in one task
2. **INTEL response** → identify which 2–3 tasks have the strongest community signal; add `[!tip]` there
3. **CONTENT response** → use comparison tables from content to drive `[!example]` scenario placement
4. **`[!danger]` table** → combine all traps from the TRAP response into a single domain-level table (5–12 rows)

If TRAP or INTEL responses are thin (< 5 traps), re-query with:
```
What else do community passers say about [EXAM_NAME] Domain [N]? Focus on what surprised
them, what was tested more than expected, and what they got wrong first time.
```

---

## `/exam-prep intel` Queries (standalone exam intel file)

Run these 6 queries for the cross-domain intel file. Run FORMAT + CHANGES + STRATEGY in parallel, then RESOURCES + SCORES + TRAPS in parallel.

### FORMAT Query

```
What is the exact exam format for [EXAM_NAME]? Include: total question count,
time limit, passing score (raw and scaled if available), question types (multiple
choice, multiple response, ordering, matching), whether you can flag and return
to questions, whether there are unscored pilot questions, any lab component,
and what community passers say about how the exam actually feels compared to
practice exams. Include pacing guidance from passers.
```

### CHANGES Query

```
What changed between [PREVIOUS_VERSION] and [EXAM_CODE]? Include: new services added
to scope, services removed, domain weight changes, new topic areas that didn't
appear before, format changes, and any specific areas passers say feel different
from the previous version. What should someone who studied for [PREVIOUS_VERSION]
pay extra attention to?
```

### STRATEGY Query

```
What question strategies did passers use for [EXAM_NAME]? Include named techniques,
elimination patterns (what to look for to eliminate wrong answers), time management
strategies, what to do when stuck between two answers, how to handle multiple-response
questions, and any domain-specific strategies passers found effective.
```

### RESOURCES Query

```
What study resources do community passers recommend for [EXAM_NAME]? For each resource:
name it, describe what it's praised for, what its weaknesses are, and roughly
how many practice questions it provides. Include both paid and free options.
Flag which resources have questions closest to actual exam difficulty and style.
Also include what passers say to AVOID or consider low-signal.
```

### SCORES Query

```
What practice exam scores did real passers report before taking [EXAM_NAME]?
Include specific examples: "I scored X% on Tutorials Dojo and passed with Y."
Show the range of scores passers had. Clarify that scoring 75-85% on practice
exams is typically sufficient — most passers did NOT score 90%+ on practice
before the real exam. Include what score someone should target before booking
the real exam.
```

### TRAPS Query

```
List ALL high-frequency exam trap patterns for [EXAM_NAME] across all domains.
For each trap: Trap name | What domain it belongs to | What the distractor looks like
| What the correct answer is. Focus on patterns that appear multiple times across
the community, not one-off surprises. Organize by domain if there are many.
```

---

## Query Execution Notes

- Always use explicit notebook ID: `notebooklm ask "..." -n <NOTEBOOK_ID>`
- If a query returns a thin response (< 300 words), append: `"Be more specific — include named AWS services, specific thresholds, and concrete examples."`
- Rate limiting: if "No result found for RPC ID" error appears, wait 5 minutes and retry
- For the TRAP query, re-run with `--json` to check references — confirms the response is grounded in actual sources
- Domain queries can run in parallel across different domains; don't run multiple queries against the same notebook simultaneously
