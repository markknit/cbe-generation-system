#!/usr/bin/env python3
"""
run_whisper_batch.py
─────────────────────
Batch-transcribes all video files in the ARES content directories using
Whisper AI and the jhm-spark GB10 GPU.

Transcripts are written as .json files alongside each video file.
The index_transcripts.py script can then link them into the ARES content DB.

Usage:
    python3 scripts/ares/run_whisper_batch.py
    python3 scripts/ares/run_whisper_batch.py --model medium
    python3 scripts/ares/run_whisper_batch.py --dry-run
    python3 scripts/ares/run_whisper_batch.py --source web
    python3 scripts/ares/run_whisper_batch.py --source kolibri

Progress is logged to data/ares_index/whisper_batch.log.
Completed files are tracked in data/ares_index/whisper_completed.txt.
Interrupted runs resume automatically — already-transcribed files are skipped.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# ─── Configuration ────────────────────────────────────────────────────────────

# Directories to scan for video files
VIDEO_SOURCES = [
    {
        "name": "web",
        "path": "/mnt/sda3/var/www/modules",
        "transcript_alongside": True,   # write .json next to video file
    },
    {
        "name": "kolibri",
        "path": "/mnt/sda3/Kolibri_Data-current",
        "transcript_alongside": True,
    },
]

VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogv", ".m4v", ".avi", ".mkv"}

PROJECT_ROOT = Path("/home/markk/ares/cbe-generation-system")
LOG_FILE     = PROJECT_ROOT / "data/ares_index/whisper_batch.log"
DONE_FILE    = PROJECT_ROOT / "data/ares_index/whisper_completed.txt"
FAIL_FILE    = PROJECT_ROOT / "data/ares_index/whisper_failed.txt"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_completed() -> set:
    """Load the set of already-transcribed video paths."""
    if not DONE_FILE.exists():
        return set()
    return set(DONE_FILE.read_text().splitlines())


def mark_completed(path: str) -> None:
    with open(DONE_FILE, "a") as f:
        f.write(path + "\n")


def mark_failed(path: str, reason: str) -> None:
    with open(FAIL_FILE, "a") as f:
        f.write(f"{path}\t{reason}\n")


def transcript_exists(video_path: Path) -> bool:
    """Return True if a Whisper JSON transcript already exists for this video."""
    return video_path.with_suffix(".json").exists()


def collect_videos(sources: list, source_filter: str | None = None) -> list:
    """Walk source directories and return list of video Paths."""
    videos = []
    for source in sources:
        if source_filter and source["name"] != source_filter:
            continue
        root = Path(source["path"])
        if not root.exists():
            logging.warning(f"Source path does not exist: {root}")
            continue
        for ext in VIDEO_EXTENSIONS:
            found = list(root.rglob(f"*{ext}"))
            videos.extend(found)
            logging.info(f"  [{source['name']}] Found {len(found)} {ext} files")
    return videos


def format_duration(seconds: float) -> str:
    return str(timedelta(seconds=int(seconds)))


def estimate_remaining(done: int, total: int, elapsed: float) -> str:
    if done == 0:
        return "unknown"
    rate = done / elapsed  # videos per second
    remaining = (total - done) / rate
    return format_duration(remaining)


# ─── Whisper runner ───────────────────────────────────────────────────────────

def transcribe(video_path: Path, model: str, language: str) -> bool:
    """
    Run Whisper on a single video file.
    Writes output as <video_stem>.json in the same directory as the video.
    Returns True on success.
    """
    output_dir = video_path.parent

    cmd = [
        "whisper",
        str(video_path),
        "--model", model,
        "--output_format", "json",
        "--output_dir", str(output_dir),
        "--device", "cuda",
        "--fp16", "True",
        "--verbose", "False",
    ]

    if language:
        cmd += ["--language", language]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800,   # 30 min max per file — catches hung processes
        )
        if result.returncode == 0:
            # Verify the output file was actually created
            expected = output_dir / (video_path.stem + ".json")
            if expected.exists():
                return True
            else:
                logging.warning(f"Whisper succeeded but output not found: {expected}")
                return False
        else:
            logging.error(f"Whisper failed: {result.stderr[-500:]}")
            return False
    except subprocess.TimeoutExpired:
        logging.error(f"Whisper timed out after 30 min: {video_path.name}")
        return False
    except Exception as e:
        logging.error(f"Whisper error on {video_path.name}: {e}")
        return False


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Batch Whisper transcription for ARES video content."
    )
    parser.add_argument(
        "--model", default="large-v3",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Whisper model size (default: large-v3)",
    )
    parser.add_argument(
        "--language", default="en",
        help="Language hint for Whisper (default: en). Use 'sw' for Kiswahili.",
    )
    parser.add_argument(
        "--source", choices=["web", "kolibri"],
        help="Scan only this source (default: both)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List videos that would be transcribed without running Whisper",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Stop after this many transcriptions (0 = no limit, useful for testing)",
    )
    args = parser.parse_args()

    # Logging
    os.makedirs(LOG_FILE.parent, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout),
        ],
    )
    log = logging.getLogger("whisper_batch")

    log.info("═" * 60)
    log.info(f"Whisper batch starting — model: {args.model}, language: {args.language}")
    log.info("═" * 60)

    # Collect videos
    log.info("Scanning for video files...")
    all_videos = collect_videos(VIDEO_SOURCES, source_filter=args.source)
    log.info(f"Total video files found: {len(all_videos):,}")

    # Filter already done
    completed = load_completed()
    pending = [
        v for v in all_videos
        if str(v) not in completed and not transcript_exists(v)
    ]
    already_done = len(all_videos) - len(pending)

    log.info(f"Already transcribed : {already_done:,}")
    log.info(f"Pending             : {len(pending):,}")

    if args.dry_run:
        log.info("\nDRY RUN — first 20 pending files:")
        for v in pending[:20]:
            log.info(f"  {v}")
        log.info(f"\n... and {max(0, len(pending)-20)} more.")
        return

    if not pending:
        log.info("Nothing to do — all videos already transcribed.")
        return

    # Confirm GPU
    try:
        import torch
        if not torch.cuda.is_available():
            log.warning("CUDA not available — Whisper will run on CPU (very slow)")
        else:
            log.info(f"GPU: {torch.cuda.get_device_name(0)}")
    except ImportError:
        log.warning("torch not importable — cannot confirm GPU availability")

    # Run
    start_time = time.time()
    success_count = 0
    fail_count = 0
    limit = args.limit or len(pending)

    for i, video_path in enumerate(pending[:limit], 1):
        elapsed = time.time() - start_time
        eta = estimate_remaining(i - 1, min(limit, len(pending)), elapsed) if i > 1 else "calculating..."

        log.info(f"[{i}/{min(limit, len(pending))}] {video_path.name}  ETA: {eta}")

        ok = transcribe(video_path, model=args.model, language=args.language)

        if ok:
            mark_completed(str(video_path))
            success_count += 1
            log.info(f"  ✓ Done")
        else:
            mark_failed(str(video_path), "transcription failed")
            fail_count += 1
            log.warning(f"  ✗ Failed — logged to whisper_failed.txt")

        # Progress summary every 50 files
        if i % 50 == 0:
            elapsed = time.time() - start_time
            log.info(f"─── Progress: {i} processed, {success_count} OK, "
                     f"{fail_count} failed, elapsed: {format_duration(elapsed)}")

    total_time = time.time() - start_time
    log.info("═" * 60)
    log.info(f"Batch complete.")
    log.info(f"  Successful : {success_count:,}")
    log.info(f"  Failed     : {fail_count:,}")
    log.info(f"  Total time : {format_duration(total_time)}")
    log.info(f"  Transcripts in: alongside each video file")
    log.info("═" * 60)
    log.info("Next step: run index_transcripts.py to link transcripts into the DB")


if __name__ == "__main__":
    main()
