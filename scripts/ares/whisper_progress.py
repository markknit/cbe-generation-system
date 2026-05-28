#!/usr/bin/env python3
"""
whisper_progress.py  (v3 — phase-aware)
────────────────────────────────────────
Shows live progress of the Whisper batch transcription job.
Reads actual batch size and current file from the log so it works
correctly for both priority and full runs.

Usage:
    python3 scripts/ares/whisper_progress.py
    python3 scripts/ares/whisper_progress.py --watch      # refresh every 60s
    python3 scripts/ares/whisper_progress.py --watch 30   # refresh every 30s
"""

import argparse
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path("/home/markk/ares/cbe-generation-system")
DONE_FILE    = PROJECT_ROOT / "data/ares_index/whisper_completed.txt"
FAIL_FILE    = PROJECT_ROOT / "data/ares_index/whisper_failed.txt"
LOG_FILE     = PROJECT_ROOT / "data/ares_index/whisper_batch.log"

KICD_PATH    = "/mnt/sda3/var/www/KICD_Educhannel"
KOLIBRI_PATH = "/mnt/sda3/Kolibri_Data-current"


def load_completed() -> list:
    if not DONE_FILE.exists():
        return []
    return [l.strip() for l in DONE_FILE.read_text().splitlines() if l.strip()]


def load_failed() -> list:
    if not FAIL_FILE.exists():
        return []
    return [l.strip() for l in FAIL_FILE.read_text().splitlines() if l.strip()]


def get_batch_info() -> tuple:
    """
    Parse log to find batch total, already_done, start_time, recent lines.
    Anchors on 'Model loaded' to skip dry-run entries.
    Reads [X/Y] progress lines for the true batch total.
    """
    if not LOG_FILE.exists():
        return None, None, None, []

    lines = LOG_FILE.read_text().splitlines()

    batch_total  = None
    already_done = None
    start_time   = None
    recent       = []

    # Find most recent real run (anchored on Model loaded)
    last_model_load = -1
    for i, line in enumerate(lines):
        if "Model loaded" in line:
            last_model_load = i

    if last_model_load == -1:
        return None, None, None, lines[-6:]

    # Walk back to find batch header
    last_batch_start = last_model_load
    for i in range(last_model_load, -1, -1):
        if "Whisper batch" in lines[i]:
            last_batch_start = i
            break

    # Parse from batch start
    for line in lines[last_batch_start:]:
        if start_time is None:
            m = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
            if m:
                try:
                    start_time = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass

        m = re.search(r"Already transcribed\s+:\s+([\d,]+)", line)
        if m:
            already_done = int(m.group(1).replace(",", ""))

        # [X/Y] lines give the true batch total
        m = re.search(r"\[(\d+)/(\d+)\]", line)
        if m:
            batch_total = int(m.group(2))

    recent = [l.rstrip() for l in lines[-6:]]
    return batch_total, already_done, start_time, recent


def get_phase_breakdown(completed: list) -> dict:
    """Count completed files by source."""
    counts = {"kicd": 0, "kolibri": 0, "web": 0, "other": 0}
    for path in completed:
        if KICD_PATH in path:
            counts["kicd"] += 1
        elif KOLIBRI_PATH in path:
            counts["kolibri"] += 1
        elif "/var/www/" in path:
            counts["web"] += 1
        else:
            counts["other"] += 1
    return counts


def format_duration(seconds: float) -> str:
    if seconds <= 0:
        return "unknown"
    return str(timedelta(seconds=int(seconds)))


def bar(done: int, total: int, width: int = 40) -> str:
    if total == 0:
        return "[" + "░" * width + "]"
    filled = int(width * done / total)
    return "[" + "█" * filled + "░" * (width - filled) + "]"


def show_progress() -> None:
    batch_total, already_done, start_time, recent = get_batch_info()
    all_completed = load_completed()
    all_failed    = load_failed()
    total_done    = len(all_completed)
    total_failed  = len(all_failed)

    print("\n" + "═" * 62)
    print("  Whisper Batch Progress")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("═" * 62)

    if batch_total and already_done is not None:
        done_this_batch = max(0, total_done - already_done)
        remaining = max(0, batch_total - done_this_batch)
        pct = 100 * done_this_batch / batch_total if batch_total else 0

        print(f"\n  Overall batch progress:")
        print(f"  {bar(done_this_batch, batch_total)}")
        print(f"  {done_this_batch:,} / {batch_total:,}  ({pct:.1f}%)")
        print(f"  {total_failed:,} failed  |  {remaining:,} remaining")

        # Phase breakdown
        phases = get_phase_breakdown(all_completed)
        print(f"\n  By source:")
        print(f"    KICD Educhannel : {phases['kicd']:,}")
        print(f"    Kolibri (KA etc): {phases['kolibri']:,}")
        print(f"    Web modules     : {phases['web']:,}")

        # Rate and ETA — use last 100 completions for current rate
        if start_time and done_this_batch > 0:
            elapsed = (datetime.now() - start_time).total_seconds()

            # Overall rate
            overall_rate = done_this_batch / elapsed * 3600
            eta_sec = remaining / (done_this_batch / elapsed) if done_this_batch > 0 else 0
            eta_dt = datetime.now() + timedelta(seconds=eta_sec)

            print(f"\n  Rate     : {overall_rate:.1f} videos/hour (overall avg)")
            print(f"  Elapsed  : {format_duration(elapsed)}")
            print(f"  ETA      : {format_duration(eta_sec)}"
                  f"  (~{eta_dt.strftime('%a %b %d %H:%M')})")
    else:
        print(f"\n  Completed (all runs): {total_done:,}")
        print(f"  Failed              : {total_failed:,}")

    # Current file from log
    current_file = None
    if recent:
        for line in reversed(recent):
            m = re.search(r"\[\d+/\d+\] (.+?)  ETA", line)
            if m:
                current_file = m.group(1).strip()
                break

    if current_file:
        # Identify which source
        source = "Kolibri" if re.match(r"^[0-9a-f]{32}\.mp4$", current_file) else "KICD/Web"
        print(f"\n  Now processing [{source}]:")
        print(f"    {current_file[:60]}")

    print(f"\n  All-time completed : {total_done:,}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Show Whisper batch transcription progress."
    )
    parser.add_argument(
        "--watch", nargs="?", const=60, type=int, metavar="SECONDS",
        help="Refresh every N seconds (default: 60)",
    )
    args = parser.parse_args()

    if args.watch:
        try:
            while True:
                os.system("clear")
                show_progress()
                print(f"  (Refreshing every {args.watch}s — Ctrl-C to stop)\n")
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\nStopped.")
    else:
        show_progress()


if __name__ == "__main__":
    main()
