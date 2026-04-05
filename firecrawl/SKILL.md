---
name: firecrawl
description: |
  Web scraping, search, crawling, and page interaction via the Firecrawl CLI. Use this skill whenever the user wants to search the web, find articles, research a topic, look something up online, scrape a webpage, grab content from a URL, extract data from a website, crawl documentation, download a site, or interact with pages that need clicks or logins. Also use when they say "fetch this page", "pull the content from", "get the page at https://", or reference scraping external websites. This provides real-time web search with full page content extraction and interact capabilities — beyond what Claude can do natively with built-in tools. Do NOT trigger for local file operations, git commands, deployments, or code editing tasks.
allowed-tools:
  - Bash(firecrawl *)
  - Bash(npx firecrawl *)
---

# Firecrawl CLI

Web scraping, search, and page interaction CLI. Returns clean markdown optimized for LLM context windows.

Run `firecrawl --help` or `firecrawl <command> --help` for full option details.

## Prerequisites

Must be installed and authenticated. Check with `firecrawl --status`.

```
  🔥 firecrawl cli v1.8.0

  ● Authenticated via FIRECRAWL_API_KEY
  Concurrency: 0/100 jobs (parallel scrape limit)
  Credits: 500,000 remaining
```

- **Concurrency**: Max parallel jobs. Run parallel operations up to this limit.
- **Credits**: Remaining API credits. Each scrape/crawl consumes credits.

If not ready, see [rules/install.md](rules/install.md). For output handling guidelines, see [rules/security.md](rules/security.md).

## Workflow

Follow this escalation pattern — start simple, escalate only when needed:

1. **Search** — No specific URL yet. Find pages, answer questions, discover sources.
2. **Scrape** — Have a URL. Extract its content directly.
3. **Map + Scrape** — Large site or need a specific subpage. Use `map --search` to find the right URL, then scrape it.
4. **Crawl** — Need bulk content from an entire site section (e.g., all /docs/).
5. **Interact** — Scrape first, then interact with the page (pagination, modals, form submissions, multi-step navigation).

| Need | Command | When |
|---|---|---|
| Find pages on a topic | `search` | No specific URL yet |
| Get a page's content | `scrape` | Have a URL, page is static or JS-rendered |
| Find URLs within a site | `map` | Need to locate a specific subpage |
| Bulk extract a site section | `crawl` | Need many pages (e.g., all /docs/) |
| AI-powered data extraction | `agent` | Need structured data from complex sites |
| Interact with a page | `scrape` + `interact` | Content requires clicks, form fills, pagination, or login |
| Download a site to files | `download` | Save an entire site as local files |

**Scrape vs interact:**

- Use `scrape` first. It handles static pages and JS-rendered SPAs.
- Use `scrape` + `interact` when you need to interact with a page, such as clicking buttons, filling out forms, navigating through a complex site, infinite scroll, or when scrape fails to grab all the content you need.
- Never use interact for web searches — use `search` instead.

**Avoid redundant fetches:**

- `search --scrape` already fetches full page content. Don't re-scrape those URLs.
- Check `.firecrawl/` for existing data before fetching again.

## Output & Organization

Unless the user specifies to return in context, write results to `.firecrawl/` with `-o`. Add `.firecrawl/` to `.gitignore`. Always quote URLs — shell interprets `?` and `&` as special characters.

```bash
firecrawl search "react hooks" -o .firecrawl/search-react-hooks.json --json
firecrawl scrape "<url>" -o .firecrawl/page.md
```

Naming conventions:

```
.firecrawl/search-{query}.json
.firecrawl/search-{query}-scraped.json
.firecrawl/{site}-{path}.md
```

Never read entire output files at once. Use `grep`, `head`, or incremental reads:

```bash
wc -l .firecrawl/file.md && head -50 .firecrawl/file.md
grep -n "keyword" .firecrawl/file.md
```

Single format outputs raw content. Multiple formats (e.g., `--format markdown,links`) output JSON.

## Working with Results

```bash
# Extract URLs from search
jq -r '.data.web[].url' .firecrawl/search.json

# Get titles and URLs
jq -r '.data.web[] | "\(.title): \(.url)"' .firecrawl/search.json
```

## Parallelization

Run independent operations in parallel. Check `firecrawl --status` for concurrency limit:

```bash
firecrawl scrape "<url-1>" -o .firecrawl/1.md &
firecrawl scrape "<url-2>" -o .firecrawl/2.md &
firecrawl scrape "<url-3>" -o .firecrawl/3.md &
wait
```

## Credit Usage

```bash
firecrawl credit-usage
firecrawl credit-usage --json --pretty -o .firecrawl/credits.json
```

---

# Command Reference

## search

Web search with optional content scraping. Returns search results as JSON, optionally with full page content.

**When to use:** You don't have a specific URL yet. First step in the escalation pattern.

```bash
# Basic search
firecrawl search "your query" -o .firecrawl/result.json --json

# Search and scrape full page content from results
firecrawl search "your query" --scrape -o .firecrawl/scraped.json --json

# News from the past day
firecrawl search "your query" --sources news --tbs qdr:d -o .firecrawl/news.json --json
```

| Option | Description |
|---|---|
| `--limit <n>` | Max number of results |
| `--sources <web,images,news>` | Source types to search |
| `--categories <github,research,pdf>` | Filter by category |
| `--tbs <qdr:h\|d\|w\|m\|y>` | Time-based search filter |
| `--location` | Location for search results |
| `--country <code>` | Country code for search |
| `--scrape` | Also scrape full page content for each result |
| `--scrape-formats` | Formats when scraping (default: markdown) |
| `-o, --output <path>` | Output file path |
| `--json` | Output as JSON |

**Tips:**
- `--scrape` fetches full content — don't re-scrape URLs from search results.
- Always write results to `.firecrawl/` with `-o` to avoid context window bloat.
- Use `jq` to extract URLs: `jq -r '.data.web[].url' .firecrawl/search.json`

---

## scrape

Scrape one or more URLs. Returns clean, LLM-optimized markdown. Multiple URLs are scraped concurrently.

**When to use:** You have a specific URL and want its content. Step 2 in the escalation pattern.

```bash
# Basic markdown extraction
firecrawl scrape "<url>" -o .firecrawl/page.md

# Main content only, no nav/footer
firecrawl scrape "<url>" --only-main-content -o .firecrawl/page.md

# Wait for JS to render, then scrape
firecrawl scrape "<url>" --wait-for 3000 -o .firecrawl/page.md

# Multiple URLs
firecrawl scrape https://example.com https://example.com/blog https://example.com/docs

# Ask a question about the page
firecrawl scrape "https://example.com/pricing" --query "What is the enterprise plan price?"
```

| Option | Description |
|---|---|
| `-f, --format <formats>` | Output formats: markdown, html, rawHtml, links, screenshot, json |
| `-Q, --query <prompt>` | Ask a question about the page content (5 credits) |
| `-H` | Include HTTP headers in output |
| `--only-main-content` | Strip nav, footer, sidebar — main content only |
| `--wait-for <ms>` | Wait for JS rendering before scraping |
| `--include-tags <tags>` | Only include these HTML tags |
| `--exclude-tags <tags>` | Exclude these HTML tags |
| `-o, --output <path>` | Output file path |

**Tips:**
- Prefer plain scrape over `--query`. Scrape to a file, then read/grep — you save credits.
- Try scrape before interact. Only escalate when you need interaction.
- Always quote URLs.

---

## map

Discover URLs on a site. Use `--search` to find a specific page within a large site.

**When to use:** You need to find a specific subpage on a large site. Step 3 in the escalation pattern.

```bash
# Find a specific page on a large site
firecrawl map "<url>" --search "authentication" -o .firecrawl/filtered.txt

# Get all URLs
firecrawl map "<url>" --limit 500 --json -o .firecrawl/urls.json
```

| Option | Description |
|---|---|
| `--limit <n>` | Max number of URLs to return |
| `--search <query>` | Filter URLs by search query |
| `--sitemap <include\|skip\|only>` | Sitemap handling strategy |
| `--include-subdomains` | Include subdomain URLs |
| `--json` | Output as JSON |
| `-o, --output <path>` | Output file path |

**Tips:**
- Map + scrape is a common pattern: `map --search` to find the URL, then `scrape` it.

---

## crawl

Bulk extract content from a website. Crawls pages following links up to a depth/limit.

**When to use:** You need content from many pages on a site. Step 4 in the escalation pattern.

```bash
# Crawl a docs section
firecrawl crawl "<url>" --include-paths /docs --limit 50 --wait -o .firecrawl/crawl.json

# Full crawl with depth limit
firecrawl crawl "<url>" --max-depth 3 --wait --progress -o .firecrawl/crawl.json

# Check status of a running crawl
firecrawl crawl <job-id>
```

| Option | Description |
|---|---|
| `--wait` | Wait for crawl to complete before returning |
| `--progress` | Show progress while waiting |
| `--limit <n>` | Max pages to crawl |
| `--max-depth <n>` | Max link depth to follow |
| `--include-paths <paths>` | Only crawl URLs matching these paths |
| `--exclude-paths <paths>` | Skip URLs matching these paths |
| `--delay <ms>` | Delay between requests |
| `--max-concurrency <n>` | Max parallel crawl workers |
| `-o, --output <path>` | Output file path |

**Tips:**
- Always use `--wait` when you need results immediately.
- Use `--include-paths` to scope the crawl — don't crawl entire sites unnecessarily.
- Crawl consumes credits per page. Check `firecrawl credit-usage` before large crawls.

---

## agent

AI-powered autonomous extraction. The agent navigates sites and extracts structured data (takes 2-5 minutes).

**When to use:** You need structured data from complex multi-page sites, or want the AI to figure out where the data lives.

```bash
# Extract structured data
firecrawl agent "extract all pricing tiers" --wait -o .firecrawl/pricing.json

# With a JSON schema for structured output
firecrawl agent "extract products" --schema '{"type":"object","properties":{"name":{"type":"string"},"price":{"type":"number"}}}' --wait -o .firecrawl/products.json

# Focus on specific pages
firecrawl agent "get feature list" --urls "<url>" --wait -o .firecrawl/features.json
```

| Option | Description |
|---|---|
| `--urls <urls>` | Starting URLs for the agent |
| `--model <model>` | Model to use: spark-1-mini or spark-1-pro |
| `--schema <json>` | JSON schema for structured output |
| `--schema-file <path>` | Path to JSON schema file |
| `--max-credits <n>` | Credit limit for this agent run |
| `--wait` | Wait for agent to complete |
| `-o, --output <path>` | Output file path |

**Tips:**
- Always use `--wait` to get results inline.
- Use `--schema` for predictable output — otherwise the agent returns freeform data.
- Agent runs consume more credits. Use `--max-credits` to cap spending.
- For simple single-page extraction, prefer `scrape` — faster and cheaper.

---

## interact (instruct)

Interact with scraped pages in a live browser session. Scrape a page first, then use natural language prompts or code to click, fill forms, navigate, and extract data.

**When to use:** Content requires interaction — clicks, form fills, pagination, login. Last resort in the escalation pattern. Never use for web searches.

```bash
# 1. Scrape a page (scrape ID is saved automatically)
firecrawl scrape "<url>"

# 2. Interact with the page using natural language
firecrawl interact --prompt "Click the login button"
firecrawl interact --prompt "Fill in the email field with test@example.com"
firecrawl interact --prompt "Extract the pricing table"

# 3. Or use code for precise control
firecrawl interact --code "agent-browser click @e5" --language bash
firecrawl interact --code "agent-browser snapshot -i" --language bash

# 4. Stop the session when done
firecrawl interact stop
```

| Option | Description |
|---|---|
| `--prompt <text>` | Natural language instruction (use this OR --code) |
| `--code <code>` | Code to execute in the browser session |
| `--language <lang>` | Language for code: bash, python, node |
| `--timeout <seconds>` | Execution timeout (default: 30, max: 300) |
| `--scrape-id <id>` | Target a specific scrape (default: last scrape) |
| `-o, --output <path>` | Output file path |

### Profiles

Persist browser state (cookies, localStorage) across scrapes:

```bash
# Session 1: Login and save state
firecrawl scrape "https://app.example.com/login" --profile my-app
firecrawl interact --prompt "Fill in email with user@example.com and click login"

# Session 2: Come back authenticated
firecrawl scrape "https://app.example.com/dashboard" --profile my-app
```

**Tips:**
- Always scrape first — `interact` requires a scrape ID.
- Use `firecrawl interact stop` to free resources when done.

---

## download

> **Experimental.** Combines `map` + `scrape` to save an entire site as local files.

**When to use:** Save an entire site or section to local files for offline access.

```bash
# Interactive wizard
firecrawl download https://docs.example.com

# With screenshots
firecrawl download https://docs.example.com --screenshot --limit 20 -y

# Multiple formats per page
firecrawl download https://docs.example.com --format markdown,links --screenshot --limit 20 -y

# Filter to specific sections
firecrawl download https://docs.example.com --include-paths "/features,/sdks"

# Skip translations
firecrawl download https://docs.example.com --exclude-paths "/zh,/ja,/fr,/es,/pt-BR"
```

| Option | Description |
|---|---|
| `--limit <n>` | Max pages to download |
| `--search <query>` | Filter URLs by search query |
| `--include-paths <paths>` | Only download matching paths |
| `--exclude-paths <paths>` | Skip matching paths |
| `--allow-subdomains` | Include subdomain pages |
| `-y` | Skip confirmation prompt (always use in automated flows) |

All scrape options also work: `-f`, `-H`, `-S`, `--screenshot`, `--only-main-content`, `--include-tags`, `--exclude-tags`, `--wait-for`
