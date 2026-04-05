---
name: python-training-projects
description: Add-on skill that reads an existing training project document and generates a new companion Python training .docx with line-by-line explanations (Phase 1), fill-in-the-blank exercises (Phase 2), or spec-only challenges with reference solutions (Phase 3). Use when the user provides a path to an existing project and specifies a phase.
origin: learned
user-invocable: true
---

# Python Training Project Generator (Add-On)

Generates a **new companion .docx** from an existing training project. Reads the source project's Python code, commands, and concepts, then builds Python-focused training exercises at the requested difficulty phase.

## When to Activate

- User provides a path to an existing project file and says "generate with Phase 1/2/3"
- User says "add Python training to [project path]"
- User pastes a path and asks for a Python training document at a specific phase

## Invocation Format

The user will provide:
1. **Path** to the existing project (generator script or .docx)
2. **Phase** (1, 2, or 3)

Example: "Here's the path: `C:\...\generate_scripting_project.py` — generate this with Phase 2 guidelines"

## Workflow

### Step 1 — Read the Source Project
- Open and read the existing generator script or .docx at the provided path
- Extract all Python code blocks, commands, and concepts used in the project
- Identify the module topic, scenario company, and section structure

### Step 2 — Build the Training Document
Create a new Python generator script that produces a companion .docx. The script goes in the same directory as the source project, named:
`generate_<topic>_python_training.py`

Use the same `python-docx` boilerplate and helper functions from the `cyber-training-project` skill (same styling, same helpers: `add_title`, `h1`, `h2`, `h3`, `para`, `bullet`, `numbered`, `note`, `code_block`, `summary_list`, `add_table`).

### Step 3 — Apply the Phase Guidelines

Build the document content according to the phase the user specified:

---

#### Phase 1 — Guided Walkthrough (Full Code + Explanations)

For every Python script or code block found in the source project:

1. Present the **full working code**
2. Below each code block, add an `h3('Line-by-Line Breakdown')` section that explains every Python construct used:
   - **Variables & data types** — what type it is, why that type was chosen
   - **String formatting** — f-strings, escapes, raw strings
   - **Conditionals** — if/elif/else logic and comparison operators
   - **Loops** — for/while, what's being iterated, range() vs iterating a collection
   - **Functions** — parameters, return values, why this logic is a function
   - **File I/O** — open modes ("r", "w", "a"), context managers (with), read/write methods
   - **Imports** — what the module does, why it's needed here
   - **Data structures** — lists, dicts, tuples, sets — when to use which
   - **Error handling** — try/except, what exceptions are being caught and why
   - **List comprehensions** — break down into equivalent for-loop, then show the compact form
   - **String methods** — .split(), .strip(), .replace(), .startswith(), etc.
   - **OS/system interaction** — subprocess, os, pathlib, sys.argv
3. End each section with an `h3('Try It Yourself')` mini-challenge — a small modification to the code just shown (e.g., "add a counter", "filter for a different condition", "write output to a file instead of printing")

**Document structure:**
```
add_title('Python Training: [Topic from source project]')
para('Phase 1 — Guided Walkthrough')
para('Companion to: [Source project title]')

h1('Overview')
h2('Scenario')              # Reuse the scenario from the source project
h2('What You Will Learn')   # Bullet list of Python constructs covered
h2('Prerequisites')         # What the student should already know
h2('Setup')                 # Any pip installs or sample data files needed

h1('1. [Section from source project]')
h2('The Code')
code_block([...])           # Full working code with inline comments
h3('Line-by-Line Breakdown')
para('...')                 # Explain each construct
h3('Try It Yourself')
para('...')                 # Small modification challenge

# Repeat for each code section in the source project

h1('Key Takeaways')         # 5-7 bullet summary of constructs learned
h1('Common Mistakes')       # 3-5 pitfalls for this topic
h1('Next Steps')            # What to learn next
```

---

#### Phase 2 — Fill-in-the-Blank (Partial Code + YOUR CODE HERE)

For every Python script or code block found in the source project:

1. Present **starter code** with key logic sections replaced by `# YOUR CODE HERE` placeholders
2. Each placeholder includes a comment describing what the missing code should do
3. Add an `h3('Hints')` section with 2-3 hints per exercise
4. Add an `h3('Solution')` section with the complete working code

**Rules for creating placeholders:**
- Remove 3-10 lines of logic per placeholder (not boilerplate like imports or file paths)
- Target the parts that exercise the Python constructs being taught
- Keep enough surrounding code that the student knows what inputs/outputs to work with
- Number the placeholders sequentially: `# YOUR CODE HERE (1 of 3)`, etc.

**Document structure:**
```
add_title('Python Training: [Topic from source project]')
para('Phase 2 — Fill-in-the-Blank Exercises')
para('Companion to: [Source project title]')

h1('Overview')
h2('Scenario')              # Reuse from source project
h2('What You Will Practice') # Bullet list of skills exercised
h2('Setup')                 # Sample data, pip installs

h1('Exercise 1 — [Description]')
h2('Starter Code')
code_block([...])           # Code with # YOUR CODE HERE gaps
h3('Hints')
bullet('...')               # 2-3 hints
h3('Solution')
code_block([...])           # Complete working code

# Repeat for each exercise

h1('Key Takeaways')
h1('Common Mistakes')
h1('Next Steps')
```

---

#### Phase 3 — Spec-Only Challenge (Description + Reference Solution)

For every major task or script in the source project:

1. Describe **what the script should do** in plain English
2. Provide numbered, specific, testable **requirements**
3. Show **sample input and expected output**
4. Include a **grading rubric** table
5. Provide the **reference solution** (the actual code from the source project, cleaned up)
6. Add **bonus challenges** for students who finish early

**Document structure:**
```
add_title('Python Training: [Topic from source project]')
para('Phase 3 — Spec-Only Challenges')
para('Companion to: [Source project title]')

h1('Overview')
h2('Scenario')              # Reuse from source project
h2('Skills Tested')         # What the student should be able to do
h2('Rules')                 # Allowed libraries, time limit, constraints

h1('Challenge 1 — [Title]')
h2('Brief')
para('...')                 # What the script does and why
h2('Requirements')
numbered('1. ...')          # Specific, testable requirements
numbered('2. ...')
h2('Sample Input')
code_block([...])
h2('Expected Output')
code_block([...])
h2('Grading Rubric')
add_table(['Criteria', 'Points', 'Notes'], [...])
h2('Reference Solution')
code_block([...])           # Complete working implementation
h2('Bonus Challenges')
bullet('...')               # Optional extensions

# Repeat for each challenge

h1('Key Takeaways')
h1('Next Steps')
```

---

### Step 4 — Run and Deliver
```powershell
cd "[same directory as source project]"
python generate_<topic>_python_training.py
```

Output: `<Topic>-Python-Training-Phase-<N>.docx` in the same directory as the source project.

### Step 5 — Prompt for Markdown Companion
After the .docx is generated, always ask:

> "Would you like me to also create a Markdown (.md) version with copyable code blocks?"

If yes, invoke the `docx-to-markdown` skill.

---

## Cross-Reference: python-patterns Skill

When building training documents, consult the `everything-claude-code:python-patterns` skill for:

- **Common Mistakes sections (all phases):** Use the anti-patterns list (mutable defaults, bare except, `type()` vs `isinstance()`, `== None` vs `is None`, `from X import *`) as the basis for every "Common Mistakes" section
- **Phase 1 explanations:** Name idiomatic patterns when teaching them (e.g., call out EAFP when explaining try/except, name the context manager pattern when explaining `with open()`)
- **Phase 2 exercises:** Use anti-patterns as "fix this code" fill-in-the-blank challenges
- **Phase 3 grading rubrics:** Include idiomatic checks — use `pathlib` not `os.path`, use `is None` not `== None`, use `.join()` not `+=` in loops, use generators for large data

Do NOT pull in advanced topics (concurrency, decorators, Protocol typing, package organization) for Phase 1 or 2 documents — save those for Phase 3 or standalone advanced modules.

---

## Content Standards

### Code Quality
- All code must be PEP 8 compliant
- Use f-strings for string formatting
- Prefer pathlib over os.path in new code
- Use `if __name__ == "__main__":` in standalone scripts
- Phase 2 and 3 code should include type hints

### Default Environment
- Python 3.11+ on Windows
- Use `python` (not `python3`)
- Pip installs: `python -m pip install`
- Shell commands in PowerShell syntax
- File paths use Windows conventions

### Encoding
- Always include `sys.stdout.reconfigure(encoding='utf-8')` at the top of generator scripts
- Use Unicode escapes for special characters: `\u2014` (em dash), `\u2022` (bullet)

---

## Completed Training Documents

| File | Source Project | Phase | Topic |
|------|---------------|-------|-------|
| (none yet) | — | — | — |

Update this table as training documents are generated.
