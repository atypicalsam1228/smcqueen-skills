# JD Skill Analyzer

Analyze one or more job descriptions to surface the skills, tools, certifications, and keywords that appear most frequently. Outputs a ranked frequency table so you can prioritize what to study, add to your resume, or highlight in applications.

Works for any job field — software engineering, finance, healthcare, cybersecurity, marketing, legal, and more. Categories and terminology are inferred from the JDs themselves, not pre-set.

Results are saved as proper Obsidian notes with frontmatter, tags, and wikilinks — ready to drop into any vault.

---

## Prerequisites & Setup

This skill integrates with Obsidian via [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills). Install those skills first for the best experience:

### Install obsidian-skills (one-time)

**Option A — npx (recommended):**
```bash
npx skills add https://github.com/kepano/obsidian-skills
```

**Option B — manually for Claude Code:**
Add the repo contents to a `/.claude` folder at the root of your Obsidian vault, then open that vault folder in Claude Code.

### Install defuddle (for URL fetching)

`defuddle` strips nav, ads, and clutter from web pages — producing clean markdown for JD extraction. Much more reliable than raw WebFetch for job boards.

```bash
npm install -g defuddle
```

### Skills used from obsidian-skills

| Skill | Purpose in this workflow |
|-------|--------------------------|
| `defuddle` | Fetch and clean JD content from URLs |
| `obsidian-markdown` | Save analysis results as valid Obsidian notes |

> If defuddle is not installed, the skill falls back to WebFetch automatically.

---

## Subcommands

| Command | Description |
|---------|-------------|
| `/jd-skill-analyzer <role>` | Search for live JDs for a role and analyze them automatically |
| `/jd-skill-analyzer` | Analyze JDs you paste, provide as file paths, or provide as URLs |
| `/jd-skill-analyzer compare` | Compare frequency results against your resume/profile |
| `/jd-skill-analyzer train` | Generate a hands-on training curriculum from gap analysis results |
| `/jd-skill-analyzer train <role>` | Full pipeline: search → analyze → compare → train in one shot |
| `/jd-skill-analyzer save <name>` | Save current results to a named snapshot file |
| `/jd-skill-analyzer load <name>` | Load a previous snapshot and add more JDs to it |

---

## Search Mode (role provided as argument)

**Trigger:** User provides a job title or role description, e.g.:
- `/jd-skill-analyzer business intelligence analyst`
- `/jd-skill-analyzer senior data engineer remote`
- `/jd-skill-analyzer "product manager fintech"`

### Step 1 — Search for Live Job Postings

Use WebSearch to find real, current job postings for the role. Run these searches in parallel:

```
"{role}" job description site:indeed.com
"{role}" job description site:glassdoor.com
"{role}" job requirements responsibilities 2024 OR 2025
"{role}" job posting site:greenhouse.io OR site:lever.co OR site:jobs.ashbyhq.com
```

Collect the top 10–15 result URLs. Prioritize actual job posting pages over articles, listicles, or "how to become a X" content.

### Step 2 — Fetch Each Posting

Fetch all URLs in parallel using WebFetch. Apply the same extraction rules as manual URL mode:
- Extract only the job posting body (title, responsibilities, requirements, qualifications)
- Discard nav, footer, "similar jobs", cookie banners, and company marketing
- Skip any URL that returns a login wall or fewer than 150 words of useful content
- Target: 8–12 usable JDs. If fewer than 5 survive fetching, run additional searches to fill out the set.

Announce progress: "Found N job postings for [role] — analyzing..."

### Step 3 — Analyze and Output

Continue with Step 2 (Extract Skills), Step 3 (Aggregate), and Step 4 (Output) from the manual workflow below. Include in the output header:
- Role searched: `[role]`
- Sources: list the domains fetched from (e.g., "indeed.com ×4, greenhouse.io ×3, glassdoor.com ×2")

---

## Manual Workflow (no role argument)

### Step 1 — Collect Job Descriptions

Ask the user (single message):

```
Paste one or more job descriptions below, or provide file paths or URLs.
Separate multiple JDs with a line containing only: ---

I'll extract and rank every skill, tool, cert, and keyword across all of them.
```

Accept any of:

**Pasted text** — parse inline.

**File paths** — read with the Read tool.

**URLs** — fetch using defuddle (preferred) or WebFetch (fallback):

```bash
defuddle parse <url> --md
```

- defuddle strips nav, ads, sidebars, cookie banners, and "similar jobs" blocks automatically, producing clean markdown
- If defuddle is not installed, fall back to WebFetch with manual extraction
- Supported job boards: LinkedIn, Indeed, Glassdoor, Handshake, USAJobs, Dice, Workday, Greenhouse, Lever, company career pages
- If the result is a login wall or fewer than 150 words, skip it and tell the user: "This URL requires a login — paste the JD text directly instead."
- If a URL returns 404 or redirects away from the job posting, skip it and note it in the final summary
- Fetch all URLs in parallel before processing

Process each JD separately, then aggregate. Track total JD count.

### Step 2 — Extract Skills from Each JD

For each job description, extract items into these universal categories. Do NOT guess or invent — only include items explicitly present in the text.

**Categories:**

| Category | What to capture |
|----------|----------------|
| **Technical Skills** | Hard, domain-specific skills named in the JD (e.g., machine learning, financial modeling, network administration, clinical documentation, SEO, contract negotiation) |
| **Tools & Platforms** | Any software, SaaS product, cloud platform, hardware, or named system (e.g., Salesforce, Python, AutoCAD, AWS, QuickBooks, Epic, Adobe Creative Suite) |
| **Certifications & Licenses** | Any certification, license, or credential named (e.g., PMP, CPA, AWS SAA, PE license, RN license, Google Analytics, Series 7) |
| **Methodologies & Frameworks** | Named processes, standards, or approaches (e.g., Agile, Scrum, ITIL, Six Sigma, GAAP, SDLC, Lean, SOC 2, ISO 27001) |
| **Soft Skills** | Interpersonal and professional skills named explicitly (e.g., written communication, cross-functional collaboration, stakeholder management, problem-solving) |
| **Experience Markers** | Years of experience required, seniority level, education requirements (e.g., "5+ years", "Bachelor's required", "Master's preferred", "senior-level") |

**Dynamic category — Access & Credentials:** If 3 or more JDs in the dataset share a domain-specific access requirement (security clearance, medical license, bar admission, CDL, FAA certification, etc.), group those into a one-time **Access & Credentials** category for this run. Do not create this category if fewer than 3 JDs mention such requirements.

**Normalization:** Collapse name variations to one canonical form. Prefer the most widely recognized or official name. When uncertain, use whichever form appeared most across the JDs.
> Examples: "Amazon Web Services" → `AWS` | "JS" → `JavaScript` | "project management professional" → `PMP` | "k8s" → `Kubernetes`

**Boilerplate to ignore:** EEO statements, benefits descriptions, legal disclaimers, salary ranges, office address, and "about the company" paragraphs contain no skill signal — skip them entirely.

### Step 3 — Aggregate and Rank

After processing all JDs:

1. Count how many JDs each item appeared in (not raw occurrences — one count per JD regardless of how many times it appears)
2. Compute percentage: `count / total_JDs * 100`
3. Sort by count descending within each category
4. Omit any category that has zero items across all JDs

### Step 4 — Output Results

```
════════════════════════════════════════════════
  JD Skill Frequency Analysis
  {N} job descriptions analyzed
════════════════════════════════════════════════

## Technical Skills
Rank  Skill                          JDs   %
────  ─────────────────────────────  ───   ───
 1.   [top skill]                     8    80%
 2.   [next skill]                    7    70%
...

## Tools & Platforms
 1.   [top tool]                      7    70%
 2.   [next tool]                     5    50%
...

## Certifications & Licenses
 1.   [top cert]                      6    60%
...

## Methodologies & Frameworks
 1.   [top methodology]               5    50%
...

## Soft Skills
 1.   [top soft skill]                8    80%
...

## Experience Markers
 - 5+ years: 6 JDs
 - Bachelor's required: 8 JDs
 - Master's preferred: 3 JDs

────────────────────────────────────────────────
  Top 10 across all categories:
  [skill] (80%) | [skill] (70%) | ...

  Skipped URLs (login required or 404):
  - [url if any]
════════════════════════════════════════════════
```

---

## /jd-skill-analyzer compare

Compare frequency results against a resume or profile.

### Inputs
- Frequency results from the current or loaded session
- Resume: ask for a file path or pasted text

### Gap Analysis Output

```
════════════════════════════════════════════════
  Gap Analysis — Your Profile vs JD Frequency
════════════════════════════════════════════════

✅ PRESENT IN YOUR PROFILE (you're covered)
   [Skill] (80% of JDs) — on resume
   [Skill] (70% of JDs) — on resume

⚠️  PRESENT BUT NOT PROMINENT (surface it)
   [Skill] (70% of JDs) — experience exists, not listed clearly
   [Skill] (50% of JDs) — buried or mentioned once

❌ GAPS — Not in your profile
   [Skill] (40% of JDs)
   [Skill] (30% of JDs)

─────────────────────────────────────────────────
  Prioritize ⚠️ items first — they require
  phrasing changes, not new skills.
  For ❌ gaps above 40% frequency, consider
  adding to your study or development plan.
════════════════════════════════════════════════
```

---

## /jd-skill-analyzer save <name>

On first save, ask: "Where should I save results? (default: current directory as `jd-analysis-{name}-{YYYY-MM-DD}.md`)"

Save as a valid Obsidian note using `obsidian-markdown` conventions:

```markdown
---
title: JD Analysis — {role}
date: {YYYY-MM-DD}
tags:
  - career/jd-analysis
  - career/{role-slug}
role: {role}
jd_count: {N}
top_skills:
  - {skill1}
  - {skill2}
  - {skill3}
---

# JD Analysis — {role}

> [!summary] {N} job descriptions analyzed on {date}
> Top skills: {skill1} ({%}), {skill2} ({%}), {skill3} ({%})

## Technical Skills
...

## Tools & Platforms
...

## Related Notes
- [[{role}-training-plan-{date}]]
- [[Career/Resume]]
```

- Use `[[wikilinks]]` to cross-reference the training plan note if one was generated
- Use `> [!summary]` callout for the at-a-glance header
- Tags follow the `career/` namespace for easy vault filtering

---

## /jd-skill-analyzer load <name>

Load a previously saved snapshot by filename or name. Then ask: "Paste more JDs or URLs to add to this dataset, or run `compare` to analyze gaps."

Merges new JDs into existing counts before re-ranking.

---

## /jd-skill-analyzer train

Generate a hands-on training curriculum from gap analysis results. Module count is determined by the skills themselves — never preset.

### Triggers

- **After a `compare` run:** `/jd-skill-analyzer train` (uses the current session's gap results)
- **Full pipeline in one shot:** `/jd-skill-analyzer train <role>` (search → analyze → compare → train)
- **From a skill list:** `/jd-skill-analyzer train` with no prior session → prompts user to paste skills

### Step 1 — Collect Skills to Train On

Use whichever source is available (priority order):
1. ❌ and ⚠️ items from the current session's `compare` output
2. Top-frequency items from the current session's analysis (if no `compare` was run)
3. User-pasted skill list (if no session exists)

If fewer than 3 skills are available, tell the user and ask them to run `/jd-skill-analyzer <role>` first or paste a skill list.

### Step 2 — Group Skills into Modules (Dynamic)

Cluster skills into logical learning modules using these rules:

- **Conceptual proximity** — skills that build on each other go in the same module
- **Tool relationships** — a tool and its associated methodology belong together
- **Dependency order** — foundational skills come before advanced ones

**Module sizing:**
- No predetermined count — it comes entirely from the groupings
- 1–6 skills per module; split any cluster larger than 6 into two modules
- 3 tightly related skills = 1 module; 20 skills across 5 distinct domains = 5 modules

**Before generating, show the proposed grouping and ask for confirmation:**

```
I've grouped your {N} gap skills into {M} modules:

  Module 1: {Name}
    → {skill1}, {skill2}, {skill3}

  Module 2: {Name}
    → {skill4}, {skill5}
  ...

Does this look right? (yes / adjust)
```

Do not proceed until the user confirms or provides adjustments.

### Step 3 — Infer Field Context

From the role name or JD content, infer:
- **Field** (e.g., data analytics, software engineering, healthcare IT, finance, marketing)
- **Scenario type** (enterprise, consulting, startup, government, healthcare system, etc.)
- **Primary tools in use** so exercises are grounded in realistic tooling

Generate a fictional company appropriate to the field:

| Field | Example Fictional Company |
|-------|--------------------------|
| Data / Analytics | Meridian Analytics (mid-size retail analytics firm) |
| Healthcare IT | ClearPath Health Systems (regional hospital network) |
| Finance | Apex Capital Partners (asset management firm) |
| Software Engineering | Orbis Technologies (B2B SaaS startup) |
| Marketing | Broadleaf Agency (digital marketing consultancy) |
| Legal / Compliance | Harwick & Moore LLP (mid-size law firm) |

Invent a fitting company for fields not listed. Never reuse cybersecurity-specific companies.

### Step 4 — Generate the Curriculum

For each module, output the following structure:

---

**Module {N}: {Name}**
Skills covered: {skill1}, {skill2}, ...
Estimated time: {1.5–4 hours}
Prerequisites: {Module N-1 or "None — start here"}

---

For each skill within the module:

**1. What is this?**
Plain-English explanation assuming the learner has never encountered it. 1–2 paragraphs.

**2. Why does it matter for this role?**
Tie it to what employers in the JDs actually need it for. Concrete, not generic.

**3. Concept table**
| Term | What it means |
|------|--------------|
| ... | ... |

**4. Hands-on exercise** (using the fictional company scenario)
- Context: what situation you're in at the company
- Setup: what to install or prepare
- Tasks: numbered steps to complete
- Expected output: what success looks like

**5. Real-world reference**
One actual company, open-source project, published incident, or industry case study that illustrates why this skill matters in production.

---

**Module {N} closing:**
- Best practices summary table
- ✅ Checkpoint: "You can now..."
- 💡 Next: Module {N+1} — {Name} (or "You're ready to apply for {role} roles" if final module)

---

### Step 5 — Output

After generating, ask: "Save as an Obsidian note, plain markdown file, or display inline?"

**Obsidian note** — save with proper frontmatter and structure:

```markdown
---
title: Training Plan — {role}
date: {YYYY-MM-DD}
tags:
  - career/training
  - career/{role-slug}
role: {role}
modules: {M}
skills_covered: {N}
source: "[[jd-analysis-{role-slug}-{date}]]"
---

# Training Plan — {role}

> [!abstract] {M} modules · {N} skills · Generated {date}
> Based on gap analysis from [[jd-analysis-{role-slug}-{date}]]

## Module 1: {Name}
...
```

- Use `[[wikilink]]` to the analysis note it was generated from
- Use `> [!abstract]` callout for the summary header
- Tags follow the `career/` namespace

**Plain markdown** — save to user-specified path, or default to `{role}-training-plan-{YYYY-MM-DD}.md` in the current directory

**Inline** — display module by module in the conversation

---

## Training Quality Rules

- **No hardcoded module count.** Count always comes from the skill groupings.
- **No hardcoded field assumptions.** Infer everything from the role and JD content.
- **No assumed prior knowledge.** Every new concept gets a "What is this?" section.
- **Exercises must be doable.** Reference real tools with real setup steps. No toy or contrived examples.
- **Dependency order enforced.** Foundational modules always precede advanced ones.
- **One real-world reference per module minimum.** Exercises are grounded in production reality.
- **Fictional company used consistently** throughout all exercises in the curriculum — the learner is solving problems at that company, not doing abstract drills.

---

## Quality Rules

- **Never hallucinate skills.** Vague JD language ("strong technical background") produces no extracted items.
- **One count per JD per skill.** A skill mentioned 5 times in one JD still counts as 1.
- **Flag thin datasets.** If fewer than 3 JDs are provided, include a note that percentages are unreliable at this sample size.
- **Preserve raw JD count.** Always show "N job descriptions analyzed" in the output header.
- **Skip failed URL fetches gracefully.** List them at the bottom of the output, never abort the whole run.
