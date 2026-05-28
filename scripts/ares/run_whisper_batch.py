#!/usr/bin/env python3
"""
run_whisper_batch.py  (v5 — --language flag added)
────────────────────────────────────────────────────
Batch-transcribes ARES video files using openai-whisper + PyTorch CUDA.

Usage:
    python3 scripts/ares/run_whisper_batch.py --priority --language en
    python3 scripts/ares/run_whisper_batch.py --priority
    python3 scripts/ares/run_whisper_batch.py
    python3 scripts/ares/run_whisper_batch.py --dry-run --priority
    python3 scripts/ares/run_whisper_batch.py --limit 10 --priority
"""

import argparse
import json
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import yaml

# ─── Configuration ────────────────────────────────────────────────────────────

PROJECT_ROOT  = Path("/home/markk/ares/cbe-generation-system")
LOG_FILE      = PROJECT_ROOT / "data/ares_index/whisper_batch.log"
DONE_FILE     = PROJECT_ROOT / "data/ares_index/whisper_completed.txt"
FAIL_FILE     = PROJECT_ROOT / "data/ares_index/whisper_failed.txt"
CONFIG_FILE   = PROJECT_ROOT / "scripts/ares/ares_scan_config.yaml"

KOLIBRI_STORAGE = Path("/mnt/sda3/Kolibri_Data-current/Content/storage")
KICD_EDUCHANNEL = Path("/mnt/sda3/var/www/KICD_Educhannel")

VIDEO_SOURCES = [
    {"name": "kicd_educhannel", "path": str(KICD_EDUCHANNEL)},
    {"name": "web",             "path": "/mnt/sda3/var/www/modules"},
    {"name": "kolibri",         "path": "/mnt/sda3/Kolibri_Data-current"},
]

VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogv", ".m4v", ".avi", ".mkv"}

# ─── Priority configuration ───────────────────────────────────────────────────

PRIORITY_CHANNELS_ALL = {
    "MIT Blossoms",
    "PhET Interactive Simulations (English)",
    "TED-Ed Lessons",
    "Kenya Curriculum Tools 2025",
    "TESSA - Teacher Resources",
}

PRIORITY_CHANNELS_STEM_ONLY = {
    "Khan Academy (English - US curriculum)",
    "Ubongo Kids",
}

STEM_KEYWORDS = {
    "math", "algebra", "geometry", "calculus", "trigonometry", "statistics",
    "probability", "equation", "fraction", "ratio", "arithmetic", "quadratic",
    "logarithm", "vector", "matrix", "coordinate", "polynomial", "derivative",
    "integral", "function", "graph", "number", "theorem", "proof",
    "biology", "cell", "genetics", "evolution", "organism", "photosynthesis",
    "respiration", "ecology", "anatomy", "enzyme", "dna", "chromosome",
    "mitosis", "meiosis", "osmosis", "diffusion", "bacteria", "virus",
    "protein", "nutrition", "biodiversity", "species", "mutation",
    "chemistry", "chemical", "atom", "molecule", "reaction", "periodic",
    "acid", "base", "bond", "element", "compound", "oxidation", "electron",
    "ionic", "covalent", "titration", "stoichiometry", "mole", "polymer",
    "organic", "electrolysis", "salt", "alkali", "reduction",
    "physics", "force", "motion", "energy", "electricity", "wave",
    "gravity", "momentum", "pressure", "circuit", "magnetic", "optics",
    "velocity", "acceleration", "thermodynamics", "nuclear", "radioactive",
    "current", "voltage", "frequency", "amplitude", "light", "heat",
    "science", "stem", "experiment", "hypothesis", "laboratory",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_completed() -> set:
    if not DONE_FILE.exists():
        return set()
    return set(l.strip() for l in DONE_FILE.read_text().splitlines() if l.strip())


def mark_completed(path: str) -> None:
    os.makedirs(DONE_FILE.parent, exist_ok=True)
    with open(DONE_FILE, "a") as f:
        f.write(path + "\n")


def mark_failed(path: str, reason: str) -> None:
    os.makedirs(FAIL_FILE.parent, exist_ok=True)
    with open(FAIL_FILE, "a") as f:
        f.write(f"{path}\t{reason}\n")


def transcript_exists(video_path: Path) -> bool:
    return video_path.with_suffix(".json").exists()


def format_duration(seconds: float) -> str:
    if seconds <= 0:
        return "unknown"
    return str(timedelta(seconds=int(seconds)))


def is_stem_title(title: str) -> bool:
    title_lower = title.lower()
    return any(kw in title_lower for kw in STEM_KEYWORDS)


def resolve_kolibri_file(checksum: str) -> Path | None:
    if not checksum or len(checksum) < 2:
        return None
    storage_dir = KOLIBRI_STORAGE / checksum[0] / checksum[1]
    for ext in [".mp4", ".webm", ".ogv", ".m4v"]:
        candidate = storage_dir / f"{checksum}{ext}"
        if candidate.exists():
            return candidate
    return None


# ─── Video collection ─────────────────────────────────────────────────────────

def collect_priority_videos(db_path: str, log: logging.Logger) -> list:
    videos = []
    seen = set()

    def add(path: Path):
        s = str(path)
        if s not in seen and path.exists():
            seen.add(s)
            videos.append(path)

    # KICD Educhannel — all videos
    if KICD_EDUCHANNEL.exists():
        kicd_count = 0
        for ext in VIDEO_EXTENSIONS:
            for p in KICD_EDUCHANNEL.rglob(f"*{ext}"):
                add(p)
                kicd_count += 1
        log.info(f"  KICD Educhannel: {kicd_count:,} videos")
    else:
        log.warning(f"  KICD Educhannel not found: {KICD_EDUCHANNEL}")

    if not Path(db_path).exists():
        log.warning(f"  DB not found — skipping Kolibri priority lookup")
        return videos

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    for channel in sorted(PRIORITY_CHANNELS_ALL):
        rows = conn.execute(
            """SELECT kolibri_checksum, title FROM content
               WHERE kolibri_channel = ? AND content_type = 'video'
               AND kolibri_checksum IS NOT NULL AND kolibri_checksum != ''""",
            (channel,)
        ).fetchall()
        resolved = 0
        for row in rows:
            path = resolve_kolibri_file(row["kolibri_checksum"])
            if path:
                add(path)
                resolved += 1
        log.info(f"  {channel}: {len(rows):,} videos in DB, {resolved:,} resolved on disk")

    for channel in sorted(PRIORITY_CHANNELS_STEM_ONLY):
        rows = conn.execute(
            """SELECT kolibri_checksum, title FROM content
               WHERE kolibri_channel = ? AND content_type = 'video'
               AND kolibri_checksum IS NOT NULL AND kolibri_checksum != ''""",
            (channel,)
        ).fetchall()
        resolved = 0
        stem_matched = 0
        for row in rows:
            if not is_stem_title(row["title"] or ""):
                continue
            stem_matched += 1
            path = resolve_kolibri_file(row["kolibri_checksum"])
            if path:
                add(path)
                resolved += 1
        log.info(f"  {channel}: {len(rows):,} total, {stem_matched:,} STEM-matched, "
                 f"{resolved:,} resolved on disk")

    conn.close()
    return videos


def collect_all_videos(log: logging.Logger) -> list:
    videos = []
    for source in VIDEO_SOURCES:
        root = Path(source["path"])
        if not root.exists():
            log.warning(f"  Source not found: {root}")
            continue
        before = len(videos)
        for ext in VIDEO_EXTENSIONS:
            videos.extend(root.rglob(f"*{ext}"))
        log.info(f"  [{source['name']}] {len(videos) - before:,} videos found")
    return videos


# ─── Transcription ────────────────────────────────────────────────────────────

def transcribe(video_path: Path, model, language: str | None,
               log: logging.Logger) -> bool:
    try:
        result = model.transcribe(
            str(video_path),
            fp16=True,
            verbose=False,
            language=language,   # None = auto-detect; "en" = force English
        )

        output = {
            "text":     result.get("text", "").strip(),
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
        description="Batch Whisper transcription for ARES content."
    )
    parser.add_argument(
        "--model", default="medium",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
    )
    parser.add_argument(
        "--priority", action="store_true",
        help="Process priority channels only",
    )
    parser.add_argument(
        "--language", default=None,
        help="Force language code (e.g. 'en' for English). Default: auto-detect.",
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

    mode = "PRIORITY" if args.priority else "FULL"
    lang_str = args.language or "auto-detect"
    log.info("═" * 60)
    log.info(f"Whisper batch [{mode}] — model: {args.model}  language: {lang_str}")
    log.info("═" * 60)

    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            log.info(f"GPU: {torch.cuda.get_device_name(0)}")
        else:
            device = "cpu"
            log.warning("CUDA not available — running on CPU")
    except ImportError:
        device = "cpu"

    db_path = str(PROJECT_ROOT / "data/ares_index/ares_content.db")
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            cfg = yaml.safe_load(f)
        db_path = cfg.get("output_db", db_path)

    log.info("Collecting video files...")
    if args.priority:
        all_videos = collect_priority_videos(db_path, log)
    else:
        all_videos = collect_all_videos(log)

    completed = load_completed()
    pending = [
        v for v in all_videos
        if str(v) not in completed and not transcript_exists(v)
    ]
    already_done = len(all_videos) - len(pending)

    log.info(f"Total collected     : {len(all_videos):,}")
    log.info(f"Already transcribed : {already_done:,}")
    log.info(f"Pending             : {len(pending):,}")

    if args.dry_run:
        log.info(f"\nDRY RUN — first 30 pending files:")
        for v in pending[:30]:
            log.info(f"  {v}")
        if len(pending) > 30:
            log.info(f"  ... and {len(pending)-30:,} more")
        return

    if not pending:
        log.info("Nothing to do.")
        return

    try:
        import whisper
    except ImportError:
        log.error("openai-whisper not installed.")
        sys.exit(1)

    log.info(f"\nLoading {args.model} onto {device.upper()}...")
    model = whisper.load_model(args.model, device=device)
    log.info("Model loaded.")

    start_time = time.time()
    success = 0
    fail = 0
    limit = args.limit or len(pending)

    for i, video_path in enumerate(pending[:limit], 1):
        elapsed = time.time() - start_time
        if i > 1 and elapsed > 0:
            rate = (i - 1) / elapsed
            eta_sec = (min(limit, len(pending)) - i + 1) / rate
            eta_dt = datetime.now() + timedelta(seconds=eta_sec)
            eta_str = f"ETA {format_duration(eta_sec)} (~{eta_dt.strftime('%a %b %d %H:%M')})"
        else:
            eta_str = "calculating..."

        log.info(f"[{i}/{min(limit, len(pending))}] {video_path.name}  {eta_str}")

        t0 = time.time()
        ok = transcribe(video_path, model, args.language, log)
        elapsed_this = time.time() - t0

        if ok:
            mark_completed(str(video_path))
            success += 1
            log.info(f"  ✓ {elapsed_this:.1f}s")
        else:
            mark_failed(str(video_path), "failed")
            fail += 1
            log.warning(f"  ✗ Failed")

        if i % 50 == 0:
            elapsed = time.time() - start_time
            log.info(f"─── {i} done | {success} OK | {fail} failed | "
                     f"{format_duration(elapsed)} elapsed")

    total = time.time() - start_time
    log.info("═" * 60)
    log.info(f"Batch complete. OK={success:,}  Failed={fail:,}  "
             f"Time={format_duration(total)}")
    log.info("═" * 60)


if __name__ == "__main__":
    main()
