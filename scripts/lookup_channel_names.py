#!/usr/bin/env python3
"""
lookup_channel_names.py
=======================
Resolves Kolibri channel hex IDs to human-readable names.

Sources checked (in priority order):
  1. Kolibri channel database files (filename = channel_id)
  2. ares_content.db path column (channel_id prefix in paths)
  3. ares_content.db kolibri_channel column

Run from project root on jhm-spark:
    python3 scripts/lookup_channel_names.py

Outputs: data/channel_name_map.json
"""

import json
import glob
import os
import re
import sqlite3

# ── Config ────────────────────────────────────────────────────────────────────

KOLIBRI_DB_DIR  = "/mnt/sda3/Kolibri_Data-current/Content/databases"
CONTENT_DB      = "data/ares_index/ares_content.db"
OUTPUT_JSON     = "data/channel_name_map.json"

# The 463 hex IDs from the ARES_Tracking spreadsheet By Module tab
# (paste output of the identifiers list here, or read from a file)
# This script auto-reads them from a companion txt file if present,
# otherwise uses the hardcoded list below.

IDS_FILE = "data/hex_ids_to_resolve.txt"   # one ID per line


# ── Step 1: Build mapping from Kolibri channel DB filenames ──────────────────

def get_channel_names_from_dbs(db_dir: str) -> dict[str, str]:
    """
    Each channel DB is named <channel_id>.sqlite3 or <channel_id>-upgrade.sqlite3.
    Open each one and read the channel name from the metadata table.
    """
    mapping: dict[str, str] = {}
    db_files = glob.glob(os.path.join(db_dir, "*.sqlite3"))
    print(f"Found {len(db_files)} channel DB files")

    for db_path in db_files:
        basename = os.path.basename(db_path)
        # Extract channel_id from filename
        channel_id = basename.replace("-upgrade.sqlite3", "").replace(".sqlite3", "")

        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # Try ChannelMetadata table first (standard Kolibri)
            name = None
            for table in ("content_channelmetadata", "ChannelMetadata", "channel_metadata"):
                try:
                    cur.execute(f"SELECT name FROM {table} LIMIT 1")
                    row = cur.fetchone()
                    if row:
                        name = str(row["name"] or row[0])
                        break
                except sqlite3.OperationalError:
                    continue

            if not name:
                # Fallback: use DB filename as name hint
                name = f"[{channel_id[:8]}...]"

            mapping[channel_id] = name
            conn.close()

        except Exception as e:
            print(f"  Skip {basename}: {e}")

    print(f"Resolved {len(mapping)} channel IDs from DB files")
    return mapping


# ── Step 2: Build mapping from content.db path column ────────────────────────

def get_channel_names_from_content_db(content_db: str) -> dict[str, str]:
    """
    Kolibri content paths look like: <channel_id>/video/<content_id>
    Extract channel_id prefix → kolibri_channel name from content table.
    """
    mapping: dict[str, str] = {}
    try:
        conn = sqlite3.connect(content_db)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("""
            SELECT DISTINCT
                substr(path, 1, instr(path, '/') - 1) AS channel_prefix,
                kolibri_channel
            FROM content
            WHERE source = 'kolibri'
            AND path LIKE '%/%'
            AND kolibri_channel IS NOT NULL
            AND kolibri_channel != ''
        """)

        for row in cur.fetchall():
            prefix = str(row["channel_prefix"] or "").strip()
            name   = str(row["kolibri_channel"] or "").strip()
            # Strip -upgrade suffix from prefix if present
            clean_prefix = prefix.replace("-upgrade", "")
            if clean_prefix and name and len(clean_prefix) == 32:
                mapping[clean_prefix] = name

        conn.close()
        print(f"Resolved {len(mapping)} channel IDs from content.db paths")
    except Exception as e:
        print(f"content.db lookup error: {e}")

    return mapping


# ── Step 3: Load IDs to resolve ───────────────────────────────────────────────

def load_ids() -> list[str]:
    if os.path.exists(IDS_FILE):
        with open(IDS_FILE) as f:
            ids = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(ids)} IDs from {IDS_FILE}")
        return ids
    else:
        print(f"No {IDS_FILE} found — please create it with one hex ID per line")
        return []


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ids = load_ids()
    if not ids:
        print("No IDs to resolve. Create data/hex_ids_to_resolve.txt")
        return

    # Build combined mapping
    db_map      = get_channel_names_from_dbs(KOLIBRI_DB_DIR)
    content_map = get_channel_names_from_content_db(CONTENT_DB)

    # Merge — DB file names take priority over content.db path-derived names
    combined = {**content_map, **db_map}

    # Resolve each ID
    results: dict[str, str] = {}
    found = 0
    not_found = 0

    for hex_id in ids:
        # Try exact match
        name = combined.get(hex_id)
        if not name:
            # Try stripping -upgrade suffix
            name = combined.get(hex_id.replace("-upgrade", ""))
        if name:
            results[hex_id] = name
            found += 1
        else:
            results[hex_id] = ""
            not_found += 1

    print(f"\nResolution results:")
    print(f"  Found:     {found}")
    print(f"  Not found: {not_found}")
    print(f"  Total:     {found + not_found}")

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nOutput written to {OUTPUT_JSON}")

    # Print found mappings for quick review
    print("\n=== FOUND MAPPINGS ===")
    for hex_id, name in sorted(results.items(), key=lambda x: x[1]):
        if name:
            print(f"  {hex_id} → {name}")

    print("\n=== NOT FOUND ===")
    for hex_id, name in results.items():
        if not name:
            print(f"  {hex_id}")


if __name__ == "__main__":
    main()
