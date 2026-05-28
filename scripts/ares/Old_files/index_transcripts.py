#!/usr/bin/env python3
"""
index_transcripts.py
─────────────────────
Post-processes Whisper AI transcript files and links them into the ARES content
SQLite database. Run this after scan_ares_content.py, or after new transcripts
are produced, to update the database without re-scanning all content.

This is useful when Whisper transcription is run in batches over time — you can
add transcripts to the index incrementally without a full rescan.

Usage:
    # Process all transcripts found in the configured transcript root
    python3 index_transcripts.py --config ares_scan_config.yaml

    # Process transcripts in a specific directory only
    python3 index_transcripts.py --config ares_scan_config.yaml --transcript-dir /path/to/transcripts

    # Report on transcript coverage (no updates)
    python3 index_transcripts.py --config ares_scan_config.yaml --report-only
"""

import argparse
import json
import logging
import os
import re
import sqlite3
import sys
from pathlib import Path

import yaml


# ─── Transcript reading ───────────────────────────────────────────────────────

def read_whisper_json(path: Path, limit: int = 0) -> tuple[str, float]:
    """
    Read a Whisper JSON file.
    Returns (transcript_text, duration_seconds).
    duration_seconds is 0.0 if not available.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        if not isinstance(data, dict):
            return "", 0.0

        # Full text (Whisper always provides this)
        text = data.get("text", "").strip()

        # If text is empty, reconstruct from segments
        if not text and "segments" in data:
            text = " ".join(
                seg.get("text", "").strip() for seg in data["segments"]
            ).strip()

        # Duration from last segment end time
        duration = 0.0
        segments = data.get("segments", [])
        if segments:
            last = segments[-1]
            duration = float(last.get("end", 0.0))

        if limit:
            text = text[:limit]

        return text, duration

    except Exception as e:
        logging.warning(f"Failed to read Whisper JSON {path}: {e}")
        return "", 0.0


def read_whisper_srt(path: Path, limit: int = 0) -> tuple[str, float]:
    """
    Read a Whisper SRT file.
    Returns (transcript_text, duration_seconds).
    """
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        lines = []
        last_end = 0.0

        for line in raw.splitlines():
            line = line.strip()
            if not line or re.match(r"^\d+$", line):
                continue
            m = re.match(
                r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s+-->\s+"
                r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})",
                line,
            )
            if m:
                h, mi, s, ms = int(m[5]), int(m[6]), int(m[7]), int(m[8])
                last_end = h * 3600 + mi * 60 + s + ms / 1000
                continue
            lines.append(line)

        text = " ".join(lines)
        if limit:
            text = text[:limit]
        return text, last_end

    except Exception as e:
        logging.warning(f"Failed to read SRT {path}: {e}")
        return "", 0.0


def read_whisper_vtt(path: Path, limit: int = 0) -> tuple[str, float]:
    """
    Read a WebVTT file (Whisper --output_format vtt).
    Returns (transcript_text, duration_seconds).
    """
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        lines = []
        last_end = 0.0

        for line in raw.splitlines():
            line = line.strip()
            if not line or line.startswith("WEBVTT") or line.startswith("NOTE"):
                continue
            m = re.match(
                r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})\s+-->\s+"
                r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})",
                line,
            )
            if not m:
                # Handle short form MM:SS.mmm --> MM:SS.mmm
                m = re.match(
                    r"(\d{2}):(\d{2})\.(\d{3})\s+-->\s+"
                    r"(\d{2}):(\d{2})\.(\d{3})",
                    line,
                )
                if m:
                    mi, s, ms = int(m[4]), int(m[5]), int(m[6])
                    last_end = mi * 60 + s + ms / 1000
                continue
            h, mi, s, ms = int(m[5]), int(m[6]), int(m[7]), int(m[8])
            last_end = h * 3600 + mi * 60 + s + ms / 1000

            # strip inline VTT tags from content lines
            clean = re.sub(r"<[^>]+>", "", line)
            if clean:
                lines.append(clean)

        text = " ".join(lines)
        if limit:
            text = text[:limit]
        return text, last_end

    except Exception as e:
        logging.warning(f"Failed to read VTT {path}: {e}")
        return "", 0.0


def read_transcript(path: Path, limit: int = 0) -> tuple[str, float]:
    """Dispatch to the right reader based on file extension."""
    suffix = path.suffix.lower()
    if suffix == ".json":
        return read_whisper_json(path, limit)
    elif suffix == ".srt":
        return read_whisper_srt(path, limit)
    elif suffix in (".vtt",):
        return read_whisper_vtt(path, limit)
    return "", 0.0


# ─── Database helpers ─────────────────────────────────────────────────────────

def get_db(db_path: str) -> sqlite3.Connection:
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found: {db_path}")
        print("Run scan_ares_content.py first to create the database.")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def find_matching_video(conn: sqlite3.Connection, transcript_stem: str) -> sqlite3.Row | None:
    """
    Find a video/audio entry in the database whose filename stem matches
    the transcript file stem.
    """
    # Try exact filename stem match
    row = conn.execute(
        """
        SELECT id, path, filename, transcript_path
        FROM content
        WHERE content_type IN ('video', 'audio')
        AND LOWER(REPLACE(REPLACE(filename, '.', ' '), '-', ' ')) LIKE ?
        LIMIT 1
        """,
        (f"%{transcript_stem.lower()}%",),
    ).fetchone()
    return row


# ─── Main indexer ─────────────────────────────────────────────────────────────

def index_transcripts(
    config: dict,
    transcript_dir: str | None = None,
    report_only: bool = False,
) -> None:
    db_path = config.get("output_db", "ares_content.db")
    content_root = Path(config.get("ares_content_root", "/var/www/rachel"))
    t_root = Path(transcript_dir or config.get("whisper_transcript_root", str(content_root)))
    store_text = config.get("store_transcript_text", True)
    text_limit = config.get("transcript_text_limit", 20000)
    ext_config = config.get("file_extensions", {})
    t_exts = set(ext_config.get("transcript", [".srt", ".vtt"]))
    tj_exts = set(ext_config.get("transcript_json", [".json"]))
    all_t_exts = t_exts | tj_exts

    log = logging.getLogger("index_transcripts")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    conn = get_db(db_path)

    if report_only:
        _report(conn, content_root)
        conn.close()
        return

    log.info(f"Indexing transcripts from: {t_root}")
    updated = 0
    skipped_already_linked = 0
    skipped_no_match = 0
    errors = 0

    # Walk transcript root looking for transcript files
    for dirpath, dirnames, filenames in os.walk(t_root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        for filename in filenames:
            suffix = Path(filename).suffix.lower()
            if suffix not in all_t_exts:
                continue

            # Skip JSON files that are clearly not Whisper output
            # (Whisper JSON always has a "text" key at the top level)
            t_path = Path(dirpath) / filename
            if suffix == ".json":
                try:
                    probe = json.loads(t_path.read_text(encoding="utf-8", errors="replace"))
                    if not isinstance(probe, dict) or "text" not in probe:
                        continue
                except Exception:
                    continue

            stem = t_path.stem
            rel_path = str(t_path)

            # Check if this transcript is already linked
            existing = conn.execute(
                "SELECT id, transcript_path FROM content WHERE transcript_path = ?",
                (rel_path,),
            ).fetchone()

            if existing:
                skipped_already_linked += 1
                continue

            # Find matching video by stem
            video_row = find_matching_video(conn, stem)
            if not video_row:
                log.debug(f"No matching video for transcript: {filename}")
                skipped_no_match += 1
                continue

            # Read transcript content
            text, duration = read_transcript(t_path, limit=text_limit if store_text else 0)
            if not store_text:
                text = ""

            try:
                conn.execute(
                    """
                    UPDATE content
                    SET transcript_path=?,
                        transcript_text=?,
                        duration_seconds=COALESCE(NULLIF(duration_seconds,0), ?)
                    WHERE id=?
                    """,
                    (rel_path, text, duration if duration > 0 else None, video_row["id"]),
                )
                updated += 1
                log.info(f"Linked: {filename} → {video_row['path']}")
            except Exception as e:
                errors += 1
                log.error(f"DB update failed for {filename}: {e}")

    conn.commit()

    log.info("─" * 60)
    log.info(f"Transcript indexing complete.")
    log.info(f"  Linked (new)         : {updated}")
    log.info(f"  Already linked       : {skipped_already_linked}")
    log.info(f"  No matching video    : {skipped_no_match}")
    log.info(f"  Errors               : {errors}")
    conn.close()


def _report(conn: sqlite3.Connection, content_root: Path) -> None:
    """Print a coverage report: how many videos have transcripts."""
    total_video = conn.execute(
        "SELECT COUNT(*) FROM content WHERE content_type IN ('video','audio')"
    ).fetchone()[0]
    with_transcript = conn.execute(
        """SELECT COUNT(*) FROM content
           WHERE content_type IN ('video','audio')
           AND transcript_path != '' AND transcript_path IS NOT NULL"""
    ).fetchone()[0]
    without = total_video - with_transcript

    print("\n─── Transcript Coverage Report ───────────────────────────────")
    print(f"  Total video/audio files : {total_video}")
    print(f"  With transcript         : {with_transcript}  ({100*with_transcript//max(total_video,1)}%)")
    print(f"  Without transcript      : {without}")

    print("\n  By subject:")
    rows = conn.execute(
        """
        SELECT subject,
               COUNT(*) as total,
               SUM(CASE WHEN transcript_path != '' AND transcript_path IS NOT NULL THEN 1 ELSE 0 END) as transcribed
        FROM content
        WHERE content_type IN ('video','audio')
        GROUP BY subject
        ORDER BY total DESC
        """
    ).fetchall()
    for row in rows:
        pct = 100 * row["transcribed"] // max(row["total"], 1)
        print(f"    {row['subject']:<20} {row['transcribed']:>4}/{row['total']:<4} ({pct}%)")

    print("\n  By module:")
    rows = conn.execute(
        """
        SELECT module,
               COUNT(*) as total,
               SUM(CASE WHEN transcript_path != '' AND transcript_path IS NOT NULL THEN 1 ELSE 0 END) as transcribed
        FROM content
        WHERE content_type IN ('video','audio')
        GROUP BY module
        ORDER BY total DESC
        """
    ).fetchall()
    for row in rows:
        pct = 100 * row["transcribed"] // max(row["total"], 1)
        print(f"    {row['module']:<30} {row['transcribed']:>4}/{row['total']:<4} ({pct}%)")
    print()


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Link Whisper AI transcripts to ARES content index entries."
    )
    parser.add_argument("--config", "-c", default="ares_scan_config.yaml")
    parser.add_argument(
        "--transcript-dir",
        help="Override whisper_transcript_root from config",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Print transcript coverage report without making changes",
    )
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    index_transcripts(config, args.transcript_dir, args.report_only)


if __name__ == "__main__":
    main()
