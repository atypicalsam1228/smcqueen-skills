---
name: quiz-static-deploy
description: Use when a Python-server quiz app needs to be deployed as a static site to Vercel, Netlify, or GitHub Pages so it is accessible on mobile devices or without running a local server.
---

# Quiz Static Deploy

## Overview

Converts a Python-server quiz app (reads markdown files from local vault at runtime) into a dual-mode app that works both locally (Python server) and as a static site (Vercel/Netlify). **The local server is never modified.**

## How It Works

Add a single runtime flag to the HTML. The app detects its environment and switches data sources automatically:

| Mode | Host | Questions | Progress |
|------|------|-----------|----------|
| Local | `localhost` | `/api/questions` | `/api/progress` (file) |
| Static | Any other host | `./questions.json` | `localStorage` |

## Step 1 — Add Dual-Mode Detection to HTML

At the top of the `<script>` block in the quiz HTML:

```javascript
const IS_STATIC = location.hostname !== 'localhost' && location.hostname !== '127.0.0.1';
```

### Patch the init fetch

```javascript
const [questionsData, progressData] = IS_STATIC
  ? await Promise.all([
      fetch('./questions.json').then(r => r.json()).then(d => d.questions ?? d),
      Promise.resolve(JSON.parse(localStorage.getItem('quiz-progress') || '{}'))
    ])
  : await Promise.all([
      fetch('/api/questions').then(r => r.json()),
      fetch('/api/progress').then(r => r.json()).catch(() => ({}))
    ]);
```

### Patch saveProgress()

```javascript
async function saveProgress() {
  if (IS_STATIC) { localStorage.setItem('quiz-progress', JSON.stringify(progress)); return; }
  try { await fetch('/api/progress', { method: 'POST', ... }); } catch (e) {}
}
```

Apply the same pattern to any other `/api/*` fetch calls (flashcards, etc.).

## Step 2 — Create export_questions.py

```python
"""Export parsed questions to questions.json for static deployment."""
import json
from pathlib import Path
import quiz_server  # reuses the existing parser

questions = quiz_server.parse_all_questions()
try:
    flashcards = quiz_server.parse_all_flashcards()
except Exception:
    flashcards = []

out = Path(__file__).parent / "questions.json"
out.write_text(json.dumps({"questions": questions, "flashcards": flashcards},
               ensure_ascii=False, indent=2), encoding="utf-8")

# Vercel serves index.html — keep it in sync with the quiz HTML file
src = Path(__file__).parent / "quiz_app.html"   # adjust name if different
dst = Path(__file__).parent / "index.html"
dst.write_bytes(src.read_bytes())

print(f"Exported {len(questions)} questions -> {out}")
```

Run this once, then again whenever new questions are generated.

## Step 3 — Add vercel.json

```json
{
  "outputDirectory": ".",
  "buildCommand": null
}
```

No framework, no build step. Vercel serves the directory as-is.

## Step 4 — Deploy

```bash
npx vercel login          # one-time
python export_questions.py
npx vercel --prod
```

Get the live URL from the output (e.g. `https://my-quiz.vercel.app`).

## iPhone Home Screen

Safari → live URL → Share → **Add to Home Screen**

Progress persists in the phone's browser `localStorage`.

## Update Workflow

After generating new questions:

```bash
python export_questions.py && npx vercel --prod
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 404 on root URL | Vercel needs `index.html` — `export_questions.py` copies the quiz HTML to `index.html` |
| Questions not loading | `questions.json` must be in the same directory as `index.html`; check `outputDirectory: "."` in `vercel.json` |
| Progress lost on reload | `saveProgress()` must write to `localStorage` when `IS_STATIC` — check the patch was applied |
| Old questions after update | Re-run `export_questions.py` before deploying — it re-parses the vault fresh |
| Local server broken | `IS_STATIC` is `false` on `localhost` — local code path is never reached |
