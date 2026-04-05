#!/usr/bin/env python3
"""Search YouTube via yt-dlp and display structured results with metadata."""

import argparse
import io
import json
import subprocess
import sys
from datetime import datetime, timedelta

# Fix Windows encoding issues (cp1252 can't handle Unicode in video titles)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def human_number(n):
    """Convert a number to human-readable format (e.g., 1200000 -> 1.2M)."""
    if n is None:
        return "N/A"
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def format_duration(seconds):
    """Convert seconds to HH:MM:SS or MM:SS."""
    if seconds is None:
        return "N/A"
    seconds = int(seconds)
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def format_date(date_str):
    """Convert YYYYMMDD to a readable date."""
    if not date_str:
        return "N/A"
    try:
        dt = datetime.strptime(str(date_str), "%Y%m%d")
        return dt.strftime("%b %d, %Y")
    except ValueError:
        return str(date_str)


def search_youtube(query, count=20, months=6):
    """Search YouTube and return video metadata."""
    date_cutoff = (datetime.now() - timedelta(days=months * 30)).strftime("%Y%m%d")

    cmd = [
        "yt-dlp",
        f"ytsearch{count}:{query}",
        "--dump-json",
        "--skip-download",
        "--no-warnings",
        "--dateafter", date_cutoff,
    ]

    results = []
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            results.append(data)
        except json.JSONDecodeError:
            continue

    proc.wait()
    return results


def print_results(results, query):
    """Print formatted search results."""
    print(f"\n{'=' * 70}")
    print(f"  YouTube Search: \"{query}\"")
    print(f"  {len(results)} results found")
    print(f"{'=' * 70}\n")

    for i, video in enumerate(results, 1):
        title = video.get("title", "Unknown")
        channel = video.get("channel") or video.get("uploader", "Unknown")
        subs = video.get("channel_follower_count")
        views = video.get("view_count")
        duration = video.get("duration")
        upload_date = video.get("upload_date")
        url = video.get("webpage_url", "")

        # Calculate engagement ratio
        if views and subs and subs > 0:
            ratio = views / subs
            ratio_str = f"{ratio:.2f}x"
        else:
            ratio_str = "N/A"

        print(f"  [{i:>2}] {title}")
        print(f"       Channel:      {channel}")
        print(f"       Subscribers:  {human_number(subs)}")
        print(f"       Views:        {human_number(views)}")
        print(f"       Duration:     {format_duration(duration)}")
        print(f"       Uploaded:     {format_date(upload_date)}")
        print(f"       Views/Subs:   {ratio_str}")
        print(f"       URL:          {url}")
        print(f"  {'- ' * 35}")

    # Also output JSON for Claude to parse if needed
    print(f"\n<!-- JSON_DATA_START")
    summary = []
    for i, v in enumerate(results, 1):
        summary.append({
            "index": i,
            "title": v.get("title"),
            "channel": v.get("channel") or v.get("uploader"),
            "subscribers": v.get("channel_follower_count"),
            "views": v.get("view_count"),
            "duration_seconds": v.get("duration"),
            "upload_date": v.get("upload_date"),
            "url": v.get("webpage_url"),
            "views_to_subs_ratio": round(v["view_count"] / v["channel_follower_count"], 2)
                if v.get("view_count") and v.get("channel_follower_count") and v["channel_follower_count"] > 0
                else None,
        })
    print(json.dumps(summary, indent=2))
    print("JSON_DATA_END -->")


def main():
    parser = argparse.ArgumentParser(description="Search YouTube with structured results")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("--count", type=int, default=20, help="Number of results (default: 20)")
    parser.add_argument("--months", type=int, default=6, help="Filter to last N months (default: 6)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON only")
    args = parser.parse_args()

    query = " ".join(args.query)
    print(f"Searching YouTube for \"{query}\" (last {args.months} months)...", file=sys.stderr)

    results = search_youtube(query, count=args.count, months=args.months)

    if not results:
        print("No results found.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        for v in results:
            print(json.dumps(v))
    else:
        print_results(results, query)


if __name__ == "__main__":
    main()
