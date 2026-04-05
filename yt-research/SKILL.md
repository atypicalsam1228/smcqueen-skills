---
name: yt-research
description: "Search YouTube and analyze video content for research. Use this skill whenever the user wants to search YouTube, find videos on a topic, analyze YouTube video transcripts, research what YouTube creators are saying about something, compare video content, extract insights from YouTube, or get structured video metadata. Triggers on: YouTube search, video research, transcript analysis, 'what are people saying about X on YouTube', video summaries, yt-dlp searches."
---

# YouTube Research

Search YouTube for videos and optionally analyze their content via transcripts. Requires `yt-dlp` (install with `pip install yt-dlp` if missing).

## Workflow

When the user wants to research a topic on YouTube, ask them which mode they prefer:

**Mode 1 — Browse & Pick**: Search first, show results, then let the user choose which videos to pull transcripts from and analyze in depth. Best when the user wants to be selective or is exploring a broad topic.

**Mode 2 — Auto-Analyze**: Search and automatically pull transcripts from the top results, then synthesize findings across all videos. Best when the user has a focused research question and wants a quick overview of what creators are saying.

If the user's intent clearly matches one mode, go ahead without asking. For example, "what are the top videos about X" is browse mode, while "research what YouTube says about X" is auto-analyze mode.

## Scripts

Both scripts live in this skill's `scripts/` directory.

### Search: `yt_search.py`

```bash
python scripts/yt_search.py "search query" --count 20 --months 6
```

| Flag | Default | Description |
|------|---------|-------------|
| `--count` | 20 | Number of results to return |
| `--months` | 6 | Only include videos from the last N months |
| `--json` | off | Output raw JSON (one object per line) |

The script outputs a formatted results list to stdout with metadata for each video (title, channel, subscribers, views, duration, upload date, URL, views/subs engagement ratio). It also appends a hidden JSON block that you can parse for structured data.

### Transcripts: `yt_transcript.py`

```bash
python scripts/yt_transcript.py URL1 URL2 ... --lang en --output-dir ./transcripts
```

| Flag | Default | Description |
|------|---------|-------------|
| `--lang` | en | Subtitle language code |
| `--output-dir` | (none) | Save each transcript to a text file in this directory |
| `--json` | off | Output structured JSON with metadata + transcript text |

Extracts auto-generated or manual captions. Some videos may not have captions available — the script notes this in the output.

## Mode 1: Browse & Pick

1. Run `yt_search.py` with the user's query
2. Present the formatted results to the user
3. Ask which videos they want to analyze (by number, range, or description)
4. Run `yt_transcript.py` on the selected URLs
5. Analyze the transcripts based on what the user is looking for — summarize key points, extract arguments, compare perspectives, etc.

## Mode 2: Auto-Analyze

1. Run `yt_search.py` with the user's query. For auto-analyze, `--count 10` is a good default unless the user specifies otherwise — 20 transcripts is a lot of text.
2. Parse the JSON data from the output to get the URLs
3. Run `yt_transcript.py --json` on all the URLs
4. Read the transcripts and synthesize a research summary:
   - Key themes and consensus points across videos
   - Notable disagreements or unique perspectives
   - Which channels/videos were most substantive
   - Specific claims or data points worth highlighting
   - A ranked list of the most useful videos for the user to watch themselves

## Analysis Guidelines

When analyzing transcripts, tailor the analysis to the user's research question. Some useful frames:

- **Topic overview**: What are the main points creators make? Where do they agree/disagree?
- **Factual extraction**: Pull out specific claims, statistics, or recommendations
- **Sentiment/stance**: How do different creators feel about the topic?
- **Quality filter**: Flag videos that are mostly filler vs. genuinely informative
- **Source comparison**: How do different channels' perspectives or expertise levels compare?

Always cite which video a point comes from (by title and channel) so the user can verify.

## Important Notes

- yt-dlp must be installed (`pip install yt-dlp`). Check before running and install if missing.
- Transcript extraction takes a few seconds per video — for large batches, let the user know it'll take a moment.
- Not all videos have captions. Note which ones failed and still analyze what's available.
- The engagement ratio (views/subscribers) helps identify videos that broke out of a channel's typical audience — high ratios often mean the content resonated broadly.
