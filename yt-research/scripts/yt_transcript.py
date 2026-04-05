#!/usr/bin/env python3
"""Extract transcripts from YouTube videos via yt-dlp auto-captions."""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile


def clean_vtt(text):
    """Strip VTT formatting, timestamps, and deduplicate lines."""
    # Remove VTT header
    text = re.sub(r"WEBVTT.*?\n\n", "", text, flags=re.DOTALL)
    # Remove timestamps and positioning
    text = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}.*\n", "", text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Remove blank lines and deduplicate consecutive identical lines
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    deduped = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return " ".join(deduped)


def get_transcript(url, lang="en"):
    """Download and extract transcript for a single video."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_template = os.path.join(tmpdir, "%(id)s")
        cmd = [
            "yt-dlp",
            url,
            "--write-auto-sub",
            "--sub-lang", lang,
            "--skip-download",
            "--no-warnings",
            "-o", output_template,
        ]

        proc = subprocess.run(cmd, capture_output=True, text=True)

        # Find the subtitle file
        for f in os.listdir(tmpdir):
            if f.endswith((".vtt", ".srt")):
                with open(os.path.join(tmpdir, f), "r", encoding="utf-8") as fh:
                    raw = fh.read()
                return clean_vtt(raw)

    return None


def get_video_info(url):
    """Get basic video metadata."""
    cmd = [
        "yt-dlp", url,
        "--dump-json",
        "--skip-download",
        "--no-warnings",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0 and proc.stdout.strip():
        return json.loads(proc.stdout.strip())
    return {}


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube video transcripts")
    parser.add_argument("urls", nargs="+", help="YouTube video URLs")
    parser.add_argument("--lang", default="en", help="Subtitle language (default: en)")
    parser.add_argument("--output-dir", help="Save transcripts to directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    results = []

    for url in args.urls:
        print(f"Extracting transcript: {url}", file=sys.stderr)
        info = get_video_info(url)
        transcript = get_transcript(url, lang=args.lang)

        entry = {
            "url": url,
            "title": info.get("title", "Unknown"),
            "channel": info.get("channel") or info.get("uploader", "Unknown"),
            "duration_seconds": info.get("duration"),
            "upload_date": info.get("upload_date"),
            "transcript": transcript,
            "has_transcript": transcript is not None,
        }
        results.append(entry)

        if not args.json and not args.output_dir:
            print(f"\n{'=' * 70}")
            print(f"  {entry['title']}")
            print(f"  {entry['channel']}")
            print(f"  {url}")
            print(f"{'=' * 70}")
            if transcript:
                print(f"\n{transcript}\n")
            else:
                print("\n  [No transcript available]\n")

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        for entry in results:
            safe_title = re.sub(r'[^\w\s-]', '', entry["title"])[:80].strip()
            safe_title = re.sub(r'\s+', '_', safe_title)
            filepath = os.path.join(args.output_dir, f"{safe_title}.txt")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Title: {entry['title']}\n")
                f.write(f"Channel: {entry['channel']}\n")
                f.write(f"URL: {entry['url']}\n")
                f.write(f"Upload Date: {entry.get('upload_date', 'N/A')}\n")
                f.write(f"\n{'=' * 50}\nTRANSCRIPT\n{'=' * 50}\n\n")
                f.write(entry["transcript"] or "[No transcript available]")
            print(f"Saved: {filepath}", file=sys.stderr)

    if args.json:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
