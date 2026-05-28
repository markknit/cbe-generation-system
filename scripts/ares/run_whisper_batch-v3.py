#!/usr/bin/env python3
"""
run_whisper_batch.py  (v3 — openai-whisper Python API, direct CUDA)
────────────────────────────────────────────────────────────────────
Uses openai-whisper's Python API directly with PyTorch CUDA — bypasses
the CTranslate2 ARM64 limitation. PyTorch CUDA is confirmed working on
the GB10 Blackwell chip.

Resumable — already-transcribed files are skipped automatically.

Usage:
    python3 scripts/ares/run_whisper_batch.py
    python3 scripts/ares/run_whisper_batch.py --model medium
    python3 scripts/ares/run_whisper_batch.py --limit 3    # test run
    python3 scripts/ares/run_whisper_batch.py --source web
    python3 scripts/ares/run_whisper_batch.py --source kolibri
    python3 scripts/ares/run_whisper_batch.py --dry-run
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# ─── Configuration ────────────────────────────────────────────────────────────

VIDEO_SOURCES = [
    {"name": "web",     "path": "/mnt/sda3/var/www/modules"},
    {"name": "kolibri", "path": "/mnt/sda3/Kolibri_Data-current"},
]

VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogv", ".m4v", ".avi", ".mkv"}

KNOWN_TOTAL  = 13258   # 666 web + 12592 kolibri (from initial find count)

PROJECT_ROOT = Path("/home/markk/ares/cbe-generation-system")
LOG_FILE     = PROJECT_ROOT / "data/ares_index/whisper_batch.log"
DONE_FILE    = PROJECT_ROOT / "data/ares_index/whisper_completed.txt"
FAIL_FILE    = PROJECT_ROOT / "data/ares_index/whisper_failed.txt"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_completed() -> set:
    if not DONE_FILE.exists():
        return set()
    return set(l.strip() for l in DONE_FILE.read_text().splitlines() if l.strip())


def mark_completed(path: str) -> None:
    with open(DONE_FILE, "a") as f:
        f.write(path + "\n")


def mark_failed(path: str, reason: str) -> None:
    with open(FAIL_FILE, "a") as f:
        f.write(f"{path}\t{reason}\n")


def transcript_exists(video_path: Path) -> bool:
    return video_path.with_suffix(".json").exists()


def collect_videos(source_filter: str | None = None) -> list:
    videos = []
    for source in VIDEO_SOURCES:
        if source_filter and source["name"] != source_filter:
            continue
        root = Path(source["path"])
        if not root.exists():
            logging.warning(f"Source path does not exist: {root}")
            continue
        before = len(videos)
        for ext in VIDEO_EXTENSIONS:
            videos.extend(root.rglob(f"*{ext}"))
        logging.info(f"  [{source['name']}] {len(videos) - before:,} video files found")
    return videos


def format_duration(seconds: float) -> str:
    if seconds <= 0:
        return "unknown"
    return str(timedelta(seconds=int(seconds)))


# ─── Transcription ────────────────────────────────────────────────────────────

def transcribe(video_path: Path, model, log: logging.Logger) -> bool:
    """
    Transcribe one video using the openai-whisper Python API.
    Writes <video_stem>.json alongside the video file.
    """
    try:
        result = model.transcribe(
            str(video_path),
            fp16=True,          # float16 — fastest on Blackwell
            verbose=False,
        )

        # Build output matching Whisper JSON format
        output = {
            "text": result.get("text", "").strip(),
            "language": result.get("language", ""),
            "segments": [
                {
                    "id":    seg.get("id"),
                    "start": round(seg.get("start", 0), 3),
                    "end":   round(seg.get("end", 0), 3),
                    "text":  seg.get("text", "").strip(),
                }
                for seg in result.get("segments", [])
            ],
        }

        out_path = video_path.with_suffix(".json")
        out_path.write_text(
            json.dumps(output, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True

    except Exception as e:
        log.error(f"  Transcription error: {e}")
        return False


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Batch Whisper transcription using openai-whisper + PyTorch CUDA."
    )
    parser.add_argument(
        "--model", default="medium",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Whisper model (default: medium)",
    )
    parser.add_argument(
        "--source", choices=["web", "kolibri"],
        help="Scan only this source (default: both)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List pending files without transcribing",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Stop after N files (0 = no limit)",
    )
    args = parser.parse_args()

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
    log.info(f"openai-whisper batch — model: {args.model}")
    log.info("═" * 60)

    # Confirm GPU
    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            log.info(f"GPU: {torch.cuda.get_device_name(0)}  "
                     f"CUDA {torch.version.cuda}  "
                     f"Capability {torch.cuda.get_device_capability()}")
        else:
            device = "cpu"
            log.warning("CUDA not available — running on CPU (slow)")
    except ImportError:
        device = "cpu"
        log.warning("torch not found — running on CPU")

    # Load whisper
    try:
        import whisper
    except ImportError:
        log.error("openai-whisper not installed. Run: pip install openai-whisper")
        sys.exit(1)

    # Collect pending videos
    log.info("Scanning for video files...")
    all_videos = collect_videos(source_filter=args.source)
    completed  = load_completed()
    pending    = [
        v for v in all_videos
        if str(v) not in completed and not transcript_exists(v)
    ]
    already_done = len(all_videos) - len(pending)

    log.info(f"Total found         : {len(all_videos):,}")
    log.info(f"Already transcribed : {already_done:,}")
    log.info(f"Pending             : {len(pending):,}")

    if args.dry_run:
        log.info("\nDRY RUN — first 20 pending:")
        for v in pending[:20]:
            log.info(f"  {v}")
        return

    if not pending:
        log.info("Nothing to do — all videos already transcribed.")
        return

    # Load model — do this once, keep in memory for the whole batch
    log.info(f"\nLoading {args.model} model onto {device.upper()}...")
    try:
        model = whisper.load_model(args.model, device=device)
        log.info("Model loaded.")
    except Exception as e:
        log.error(f"Failed to load model: {e}")
        sys.exit(1)

    # Run
    start_time = time.time()
    success = 0
    fail    = 0
    limit   = args.limit or len(pending)

    for i, video_path in enumerate(pending[:limit], 1):
        elapsed = time.time() - start_time
        if i > 1 and elapsed > 0:
            rate = (i - 1) / elapsed
            remaining_n = min(limit, len(pending)) - i + 1
            eta_sec = remaining_n / rate
            eta_dt  = datetime.now() + timedelta(seconds=eta_sec)
            eta_str = (f"ETA {format_duration(eta_sec)} "
                       f"(~{eta_dt.strftime('%a %b %d %H:%M')})")
        else:
            eta_str = "calculating..."

        log.info(f"[{i}/{min(limit, len(pending))}] {video_path.name}  {eta_str}")

        t0 = time.time()
        ok = transcribe(video_path, model, log)
        elapsed_this = time.time() - t0

        if ok:
            mark_completed(str(video_path))
            success += 1
            log.info(f"  ✓ Done in {elapsed_this:.1f}s")
        else:
            mark_failed(str(video_path), "failed")
            fail += 1
            log.warning(f"  ✗ Failed")

        if i % 50 == 0:
            elapsed = time.time() - start_time
            log.info(
                f"─── {i} processed | {success} OK | {fail} failed | "
                f"elapsed: {format_duration(elapsed)}"
            )

    total = time.time() - start_time
    log.info("═" * 60)
    log.info(f"Batch complete.")
    log.info(f"  Successful : {success:,}")
    log.info(f"  Failed     : {fail:,}")
    log.info(f"  Total time : {format_duration(total)}")
    log.info("═" * 60)
    log.info("Next: run index_transcripts.py to link transcripts into the DB")


if __name__ == "__main__":
    main()
