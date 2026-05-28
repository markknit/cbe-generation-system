#!/usr/bin/env python3
"""
run_whisper_batch.py  (v2 — faster-whisper backend)
─────────────────────────────────────────────────────
Batch-transcribes all ARES video files using faster-whisper, which is
4-8x faster than openai-whisper on GPU due to the CTranslate2 backend.

Transcripts are written as .json files alongside each video.
Resumable — already-transcribed files are skipped automatically.

Usage:
    python3 scripts/ares/run_whisper_batch.py
    python3 scripts/ares/run_whisper_batch.py --model medium
    python3 scripts/ares/run_whisper_batch.py --dry-run
    python3 scripts/ares/run_whisper_batch.py --source web
    python3 scripts/ares/run_whisper_batch.py --source kolibri
    python3 scripts/ares/run_whisper_batch.py --limit 10   # test run

Install:
    pip install faster-whisper
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

PROJECT_ROOT = Path("/home/markk/ares/cbe-generation-system")
LOG_FILE     = PROJECT_ROOT / "data/ares_index/whisper_batch.log"
DONE_FILE    = PROJECT_ROOT / "data/ares_index/whisper_completed.txt"
FAIL_FILE    = PROJECT_ROOT / "data/ares_index/whisper_failed.txt"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_completed() -> set:
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
        count_before = len(videos)
        for ext in VIDEO_EXTENSIONS:
            videos.extend(root.rglob(f"*{ext}"))
        logging.info(f"  [{source['name']}] {len(videos) - count_before:,} video files found")
    return videos


def format_duration(seconds: float) -> str:
    if seconds <= 0:
        return "unknown"
    return str(timedelta(seconds=int(seconds)))


# ─── Transcription ────────────────────────────────────────────────────────────

def transcribe(
    video_path: Path,
    model,
    language: str | None,
    log: logging.Logger,
) -> bool:
    """
    Transcribe a single video using faster-whisper.
    Writes output as <video_stem>.json alongside the video.
    Returns True on success.
    """
    try:
        segments, info = model.transcribe(
            str(video_path),
            language=language or None,
            beam_size=5,
            vad_filter=True,          # skip silent sections — speeds up transcription
            vad_parameters=dict(
                min_silence_duration_ms=500,
            ),
        )

        # Consume the generator and build output
        segment_list = []
        full_text_parts = []
        for seg in segments:
            segment_list.append({
                "id":    seg.id,
                "start": round(seg.start, 3),
                "end":   round(seg.end, 3),
                "text":  seg.text.strip(),
            })
            full_text_parts.append(seg.text.strip())

        output = {
            "text":     " ".join(full_text_parts),
            "language": info.language,
            "duration": round(info.duration, 2) if hasattr(info, "duration") else None,
            "segments": segment_list,
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
        description="Batch Whisper transcription using faster-whisper + GPU."
    )
    parser.add_argument(
        "--model", default="large-v3",
        choices=["tiny", "base", "small", "medium", "large-v2", "large-v3"],
        help="Whisper model (default: large-v3)",
    )
    parser.add_argument(
        "--language", default="en",
        help="Language hint (default: en). Set to '' for auto-detect.",
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
        help="Stop after N transcriptions (0 = no limit)",
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
    log.info(f"faster-whisper batch — model: {args.model}  language: {args.language}")
    log.info("═" * 60)

    # Load faster-whisper
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        log.error("faster-whisper not installed. Run: pip install faster-whisper")
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
        log.info("Nothing to do.")
        return

    # Load model onto GPU
    log.info(f"\nLoading {args.model} model onto GPU...")
    try:
        model = WhisperModel(
            args.model,
            device="cuda",
            compute_type="float16",   # float16 is fastest on Blackwell
        )
        log.info("Model loaded successfully.")
    except Exception as e:
        log.error(f"Failed to load model: {e}")
        log.error("Trying CPU fallback...")
        model = WhisperModel(args.model, device="cpu", compute_type="int8")

    # Run transcription
    start_time = time.time()
    success = 0
    fail    = 0
    limit   = args.limit or len(pending)

    for i, video_path in enumerate(pending[:limit], 1):
        elapsed = time.time() - start_time
        if i > 1 and elapsed > 0:
            rate = (i - 1) / elapsed
            remaining = (min(limit, len(pending)) - i + 1) / rate
            eta = datetime.now() + timedelta(seconds=remaining)
            eta_str = f"ETA {format_duration(remaining)} (~{eta.strftime('%a %b %d %H:%M')})"
        else:
            eta_str = "calculating..."

        log.info(f"[{i}/{min(limit, len(pending))}] {video_path.name}  {eta_str}")

        ok = transcribe(video_path, model, args.language or None, log)

        if ok:
            mark_completed(str(video_path))
            success += 1
            log.info(f"  ✓ Done")
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
