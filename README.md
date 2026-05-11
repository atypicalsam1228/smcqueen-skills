# smcqueen-skills

A collection of Claude Code skills for career development, exam prep, compliance research, and knowledge management — all built around [Obsidian](https://obsidian.md) as the output format.

---

## Prerequisites

### 1. Download Obsidian

> **Required.** These skills output notes in Obsidian Flavored Markdown with wikilinks, callouts, and frontmatter. Without Obsidian, the output still works as plain markdown, but you lose cross-linking, graph view, and tag filtering.

**Download Obsidian:** https://obsidian.md

### 2. Install obsidian-skills (one-time setup)

These skills integrate with [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) for URL fetching (`defuddle`) and Obsidian-formatted output (`obsidian-markdown`).

**Option A — npx (recommended):**
```bash
npx skills add https://github.com/kepano/obsidian-skills
```

**Option B — manually:**
Add the repo contents to a `/.claude` folder at the root of your Obsidian vault, then open that vault folder in Claude Code.

### 3. Install defuddle (for URL fetching)

`defuddle` strips nav, ads, and clutter from web pages — producing clean markdown from job boards, articles, and career sites.

```bash
npm install -g defuddle
```

---

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **JD Skill Analyzer** | `/jd-skill-analyzer` | Analyze job descriptions to surface the skills, tools, certs, and keywords that appear most frequently. Works for any field — software, finance, healthcare, cybersecurity, marketing, and more. |
| **JD Skill Analyzer (by role)** | `/jd-skill-analyzer <role>` | Automatically search for live job postings by role name and analyze them — no URLs needed. |
| **JD Gap Compare** | `/jd-skill-analyzer compare` | Compare frequency results against your resume or profile to identify gaps and quick wins. |
| **JD Training Plan** | `/jd-skill-analyzer train` | Generate a hands-on training curriculum from gap analysis results. Module count is derived from the skills — never preset. |
| **RMF Vault** | `/rmf-vault` | Manage a compliance knowledge base stored as an Obsidian vault. |
| **Quiz Creator** | `/quiz-creator` | Generate exam-specific question banks from source documents and exam guides. |

---

## Workflow Example

```
# Search for BI analyst jobs and analyze skill frequency
/jd-skill-analyzer business intelligence analyst

# Compare against your resume
/jd-skill-analyzer compare

# Generate a training plan to close the gaps
/jd-skill-analyzer train
```

Results are saved as Obsidian notes with frontmatter, tags (`career/jd-analysis`, `career/training`), and `[[wikilinks]]` connecting the analysis to the training plan.

---

## Setup

1. Install [Obsidian](https://obsidian.md) and create a vault
2. Open your vault folder in [Claude Code](https://claude.ai/code)
3. Run: `npx skills add https://github.com/kepano/obsidian-skills`
4. Run: `npm install -g defuddle`
5. Clone this repo and copy the skill folders into your `~/.claude/skills/` directory

---

## License

MIT
