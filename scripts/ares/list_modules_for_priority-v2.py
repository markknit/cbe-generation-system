#!/usr/bin/env python3
"""
list_modules_for_priority.py
─────────────────────────────
Queries the ARES content index and produces a detailed module/channel listing
showing video counts, subjects, and sample titles to help prioritise
Whisper transcription.

Khan Academy is broken down by sub-topic using the content node hierarchy.

Usage:
    python3 scripts/ares/list_modules_for_priority.py \
        --config scripts/ares/ares_scan_config.yaml
"""

import argparse
import os
import re
import sqlite3
from pathlib import Path
from collections import defaultdict

import yaml


def get_db(config: dict) -> sqlite3.Connection:
    db_path = config.get("output_db", "ares_content.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", default="scripts/ares/ares_scan_config.yaml")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    conn = get_db(config)

    print("\n" + "═" * 80)
    print("  ARES VIDEO CONTENT — Module Listing for Transcription Priority")
    print("═" * 80)
    print(f"  {'Module':<44} {'Videos':>7}  {'Subjects'}")
    print("─" * 80)

    # ── Non-Khan-Academy modules ──────────────────────────────────────────────
    rows = conn.execute("""
        SELECT module, source, subject,
               COUNT(*) as total,
               SUM(CASE WHEN content_type='video' THEN 1 ELSE 0 END) as videos
        FROM content
        WHERE module NOT LIKE '%Khan Academy%'
        GROUP BY module, source
        HAVING videos > 0
        ORDER BY videos DESC
    """).fetchall()

    for r in rows:
        subj = r["subject"] or "General"
        print(f"  {r['module']:<44} {r['videos']:>7,}  [{r['source']}] {subj}")

    # ── Khan Academy — break down by subject/topic ────────────────────────────
    print("\n" + "─" * 80)
    print("  KHAN ACADEMY — breakdown by topic (from content titles)")
    print("─" * 80)

    # For Kolibri Khan Academy content, the topic hierarchy is in the path
    # and the kolibri_kind='topic' rows give us the tree structure.
    # We'll group by subject and then by top-level topic from titles.

    for ka_module in ["Khan Academy (English - US curriculum)", "Khan Academy (Kiswahili)"]:
        print(f"\n  ── {ka_module} ──")

        # Get all videos in this channel grouped by subject
        subject_rows = conn.execute("""
            SELECT subject,
                   COUNT(*) as videos
            FROM content
            WHERE module = ? AND content_type = 'video'
            GROUP BY subject
            ORDER BY videos DESC
        """, (ka_module,)).fetchall()

        if not subject_rows:
            print(f"    (no videos found)")
            continue

        for sr in subject_rows:
            subj = sr["subject"]
            count = sr["videos"]
            print(f"\n    {subj} ({count:,} videos)")

            # Sample 5 titles from this subject to show what's there
            samples = conn.execute("""
                SELECT title FROM content
                WHERE module = ? AND content_type = 'video' AND subject = ?
                ORDER BY title
                LIMIT 8
            """, (ka_module, subj)).fetchall()

            for s in samples:
                title = s["title"][:65] if s["title"] else "(untitled)"
                print(f"      • {title}")

            if count > 8:
                print(f"      ... and {count - 8:,} more")

    # ── Summary totals ────────────────────────────────────────────────────────
    print("\n" + "═" * 80)
    total_videos = conn.execute(
        "SELECT COUNT(*) FROM content WHERE content_type='video'"
    ).fetchone()[0]
    print(f"  Total videos in index: {total_videos:,}")

    # Count already transcribed
    done_file = Path("/home/markk/ares/cbe-generation-system/data/ares_index/whisper_completed.txt")
    if done_file.exists():
        done = len([l for l in done_file.read_text().splitlines() if l.strip()])
        print(f"  Already transcribed:   {done:,}")
        print(f"  Remaining:             {total_videos - done:,}")
    print()

    conn.close()


if __name__ == "__main__":
    main()
