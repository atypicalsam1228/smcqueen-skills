---
name: web-research
description: "Web research pipeline using Firecrawl, NotebookLM, and Obsidian. Use this skill whenever the user wants to search the web for articles, research a topic using online sources, find what experts or publications say about something, verify claims across web sources, cross-reference articles, get a cited research report, or save research findings to their Obsidian vault. Triggers on: web search, article research, 'find articles about', 'research what experts say', 'verify these sources', 'cross-reference', cited reports, source verification, 'what does the evidence say about', web scraping for research."
---

# Web Research Pipeline

Research any topic using web sources with verification and permanent storage.

**Pipeline:** Firecrawl (scrape/search) → NotebookLM (verify & aggregate with citations) → Obsidian (store for long-term use)

## Prerequisites

Check these before starting any workflow:

1. **Firecrawl CLI** — required for all modes. Test with `firecrawl --status`. If unavailable, fall back to WebSearch + WebFetch.
2. **notebooklm-py** — required for Deep Research and Verify modes. Check with `notebooklm status`. If unavailable, fall back to Claude-native synthesis.
3. **Obsidian vault** — at `C:/Users/samue/OneDrive/Obsidian/rmf_obsidian/`. If the path doesn't exist, skip the save step and present output in conversation only.

**Important:** Firecrawl commands need Node.js on PATH. If `firecrawl` is not found, try with the full path or ensure PATH includes both `/c/Program Files/nodejs` and `/c/Users/samue/AppData/Roaming/npm`.

## Mode Selection

Infer the mode from what the user says, or ask if unclear:

| User says something like... | Mode |
|---|---|
| "search the web for...", "find articles about...", "what's out there on..." | Browse & Analyze |
| "research [topic]", "give me a cited report on...", "what does the evidence say about...", "deep dive on..." | Deep Research |
| "verify these claims", "cross-reference these sources", "check if this is accurate" + provides URLs | Verify |

If the user's intent is ambiguous, ask: "Would you like me to do a quick browse of what's out there, or a deep research pass with cited sources and a report?"

## Mode 1: Browse & Analyze

Best for: exploring a topic, seeing what's out there, selective reading.

### Steps

1. **Search** — Use Firecrawl CLI to find relevant pages:
   ```bash
   firecrawl search "user's query" --limit 10 -o .firecrawl/results.json --json
   ```
   This returns results with titles, URLs, and snippets. Add `--scrape` to also get full page content inline.

2. **Present results** — Show a structured list:
   ```
   ======================================================================
     Web Search: "query"
     N results found
   ======================================================================

     [ 1] Article Title
          Source:    domain.com
          Date:      Mar 15, 2026
          URL:       https://...
          Snippet:   First 1-2 sentences of content
     - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   ```

3. **User selects** — Ask which articles to read in depth (by number)

4. **Scrape selected** — Use Firecrawl to scrape each selected URL for full clean markdown:
   ```bash
   firecrawl scrape "URL" --only-main-content -o .firecrawl/page.md
   ```

5. **Synthesize** — Analyze the scraped content:
   - Key findings and takeaways from each source
   - Where sources agree or disagree
   - Notable claims, data points, or recommendations
   - Always cite which source a point comes from

6. **Save to Obsidian** — Offer to save findings (see Obsidian Output section below)

## Mode 2: Deep Research

Best for: thorough investigation with cross-referenced, cited findings and a downloadable report.

### Steps

1. **Search** — Use Firecrawl to find relevant sources:
   ```bash
   firecrawl search "user's query" --limit 15 --scrape -o .firecrawl/deep-results.json --json
   ```
   The `--scrape` flag pulls full page content along with search results.

2. **Auto-select sources** — Pick the top 5-8 most relevant results based on:
   - Relevance to the research question
   - Source credibility (prefer known publications, official docs, established blogs)
   - Recency
   - Diversity of perspective

3. **Create NotebookLM notebook**
   ```bash
   notebooklm create "Research: {topic} — {date}"
   ```

4. **Add sources to notebook** — Add each selected URL as a separate source. This preserves NotebookLM's citation system so each claim can be traced back to its origin.
   ```bash
   notebooklm source add "https://example.com/article1"
   notebooklm source add "https://example.com/article2"
   ```
   Also run NotebookLM's own web research for additional coverage:
   ```bash
   notebooklm source add-research "{topic}" --mode deep
   ```

5. **Wait for processing** — Sources need time to be indexed:
   ```bash
   notebooklm source list
   ```
   Check that sources show as processed before querying.

6. **Query with citations** — Ask the research question and get cited answers:
   ```bash
   notebooklm ask "{research question}" --json
   ```
   The `--json` flag returns structured data with citations pointing to specific sources. Ask 2-3 targeted follow-up questions to get comprehensive coverage:
   - Main findings and consensus
   - Key disagreements or debates
   - Practical recommendations or implications

7. **Generate report** — Create a formal briefing document:
   ```bash
   notebooklm generate report --format briefing-doc --wait
   notebooklm download report ./report.md
   ```

8. **Present to user** — Show the key findings from the NotebookLM queries, highlighting:
   - Cross-referenced findings (claims supported by multiple sources)
   - Source-specific insights (unique points from individual sources)
   - Confidence levels (well-supported vs. single-source claims)

9. **Save to Obsidian** — Save two files to the appropriate vault folder (see Obsidian Output section):
   - The detailed research note (`{date}_{topic}.md`) with frontmatter, all findings, and sources
   - A `README.md` executive briefing generated from the NotebookLM report

## Mode 3: Verify

Best for: fact-checking claims, cross-referencing specific articles the user has already found.

### Steps

1. **Collect URLs** — The user provides specific URLs or articles to verify

2. **Scrape sources** — Use Firecrawl to get clean content from each URL:
   ```bash
   firecrawl scrape "URL" --only-main-content -o .firecrawl/source.md
   ```
   Briefly summarize what each source says so the user can confirm these are the right articles.

3. **Create NotebookLM notebook**
   ```bash
   notebooklm create "Verify: {topic} — {date}"
   ```

4. **Add sources** — Add each URL to the notebook:
   ```bash
   notebooklm source add "URL"
   ```

5. **Verify claims** — Ask targeted verification questions with `--json`:
   - "Do sources agree on [specific claim]?"
   - "What evidence supports or contradicts [claim]?"
   - "Are there any conflicting statements across these sources?"

6. **Present findings** — For each claim being verified:
   - **Supported**: which sources confirm it, with citations
   - **Contradicted**: which sources disagree, with citations
   - **Unverifiable**: claim not addressed by available sources

7. **Save to Obsidian** — Save two files to the appropriate vault folder (see Obsidian Output section):
   - The detailed verification note (`{date}_{topic}.md`) with findings and sources
   - A `README.md` executive briefing generated from the NotebookLM report

## Obsidian Output

After completing research, offer to save findings to the Obsidian vault. Route to the appropriate folder based on topic:

| Topic matches... | Save to |
|---|---|
| NIST 800-53, security controls | `Frameworks/NIST-800-53/` |
| FedRAMP, cloud authorization, ATO | `Frameworks/FedRAMP/` |
| NIST AI RMF, AI risk | `Frameworks/NIST-AI-RMF/` |
| OWASP, LLM security | `Frameworks/OWASP-LLM/` |
| NIST 800-171, CUI, CMMC | `Frameworks/NIST-800-171/` |
| Cross-framework, general compliance | `Frameworks/Cross-Framework/` |
| Verification results, decisions | `Decision-Records/` |
| Everything else | `Capture/` |

**Vault path:** `C:/Users/samue/OneDrive/Obsidian/rmf_obsidian/`

### Note format

```markdown
---
date: {YYYY-MM-DD}
type: {research | verification | analysis}
topic: "{topic}"
sources:
  - {url1}
  - {url2}
tags:
  - {relevant}
  - {tags}
notebooklm_notebook: "{notebook name if created}"
---

# {Descriptive Title}

## Summary
{2-3 sentence overview of key findings}

## Key Findings
{Numbered findings with source citations}

## Source Analysis
{Agreement/disagreement across sources, credibility notes}

## Sources
| # | Title | URL | Date |
|---|-------|-----|------|
| 1 | ... | ... | ... |
```

Use a filename like `{YYYY-MM-DD}_{topic-slug}.md` (e.g., `2026-04-05_zero-trust-best-practices.md`).

### README.md — Executive Briefing

For Deep Research and Verify modes, also generate a `README.md` in the same Obsidian folder. This serves as a polished executive briefing that anyone can read without context.

**How to generate it:**
1. After adding sources and running verification queries, generate a NotebookLM briefing document:
   ```bash
   notebooklm generate report --format briefing-doc --wait
   notebooklm download report ./{topic-slug}_briefing.md
   ```
2. Save the downloaded report as `README.md` in the same Obsidian folder where the research note was placed.

The README should contain (NotebookLM generates most of this automatically):
- Executive summary of the topic
- Detailed analysis of key themes with tables where appropriate
- Important quotes with context from the sources
- Actionable insights broken down by audience (e.g., primes vs. subs, small business vs. enterprise)

**Relationship between the two files:**
- The **research note** (`{date}_{topic}.md`) is the detailed reference — frontmatter, all sources listed, verification notes, preparation checklists, raw findings
- The **README.md** is the executive-friendly briefing — generated by NotebookLM from the same sources, polished and structured for quick consumption

If NotebookLM is unavailable, write the README manually using the same structure: executive summary, key themes analysis, important quotes, and actionable insights.

## Analysis Guidelines

When synthesizing research, consider these frames:

- **Source credibility**: Official publications and established organizations carry more weight than blog posts or opinion pieces. Note the source type.
- **Recency**: More recent sources may reflect current state better, but older foundational sources can provide important context.
- **Consensus vs. outliers**: When multiple sources agree, that's a stronger signal. Single-source claims should be flagged as such.
- **Factual extraction**: Pull out specific data points, statistics, dates, and recommendations — not just general themes.
- **Practical implications**: What should someone actually do based on these findings?

Always cite which source a claim comes from so the user can verify independently.

## Graceful Degradation

The skill should work even when components are unavailable:

- **Firecrawl unavailable** → Use WebSearch for discovery + WebFetch to scrape selected pages. Less clean extraction but functional.
- **NotebookLM unavailable** → Skip notebook creation. Use Firecrawl to scrape sources, load content into conversation context, and synthesize directly. Note that citations won't be as rigorous.
- **Obsidian vault not found** → Skip the save step. Present all output in the conversation and offer to save to an alternative location.
- **All three unavailable** → Use WebSearch + WebFetch + Claude-native synthesis. Still useful, just without verification layer or permanent storage.
