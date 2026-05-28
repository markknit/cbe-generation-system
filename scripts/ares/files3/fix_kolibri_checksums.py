#!/usr/bin/env python3
"""
fix_kolibri_checksums.py
─────────────────────────
Reads the content_file table from each Kolibri channel database and adds
a checksum-to-contentnode mapping to the ARES content index. This allows
the Whisper batch script to resolve actual file paths on disk.

Adds a new column 'kolibri_checksum' to the content table and populates
it for all video entries using the content_file.checksum field.

Run once after the Kolibri rescan:
    python3 scripts/ares/fix_kolibri_checksums.py \
        --config scripts/ares/ares_scan_config.yaml
"""

import argparse
import logging
import os
import sqlite3
import sys
from pathlib import Path

import yaml

PROJECT_ROOT   = Path("/home/markk/ares/cbe-generation-system")
KOLIBRI_ROOT   = Path("/mnt/sda3/Kolibri_Data-current")
KOLIBRI_DB_DIR = KOLIBRI_ROOT / "Content" / "databases"
STORAGE_ROOT   = KOLIBRI_ROOT / "Content" / "storage"
VIDEO_EXTS     = {"mp4", "webm", "ogv", "m4v"}


def get_index_db(config: dict) -> sqlite3.Connection:
    db_path = config.get("output_db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_checksum_column(conn: sqlite3.Connection) -> None:
    """Add kolibri_checksum column if it doesn't exist."""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(content)")}
    if "kolibri_checksum" not in cols:
        conn.execute("ALTER TABLE content ADD COLUMN kolibri_checksum TEXT")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_kolibri_checksum ON content(kolibri_checksum)")
        conn.commit()
        logging.info("Added kolibri_checksum column to content table")
    else:
        logging.info("kolibri_checksum column already exists")


def process_channel_db(
    channel_db_path: Path,
    index_conn: sqlite3.Connection,
    log: logging.Logger,
) -> tuple:
    """
    Read content_file table from a channel DB.
    For each video file entry, find the matching content node in the
    index DB and update its kolibri_checksum field.
    Returns (matched, unmatched) counts.
    """
    matched = 0
    unmatched = 0

    try:
        ch_conn = sqlite3.connect(str(channel_db_path))
        ch_conn.row_factory = sqlite3.Row

        # Check tables exist
        tables = {r[0] for r in ch_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        if "content_file" not in tables:
            ch_conn.close()
            return 0, 0

        # Get channel name
        channel_name = channel_db_path.stem
        for meta_table in ("content_channelmetadata", "channelmetadata"):
            if meta_table in tables:
                row = ch_conn.execute(
                    f"SELECT name FROM {meta_table} LIMIT 1"
                ).fetchone()
                if row:
                    channel_name = row["name"]
                break

        # Get all video file entries (non-thumbnail, non-supplementary)
        video_files = ch_conn.execute("""
            SELECT cf.checksum, cf.extension, cf.contentnode_id
            FROM content_file cf
            WHERE cf.extension IN ('mp4', 'webm', 'ogv', 'm4v')
            AND cf.thumbnail = 0
            AND cf.available = 1
        """).fetchall()

        if not video_files:
            ch_conn.close()
            return 0, 0

        log.info(f"  {channel_name}: {len(video_files)} video file entries")

        for vf in video_files:
            checksum   = vf["checksum"]
            extension  = vf["extension"]
            node_id    = vf["contentnode_id"]

            # Verify file actually exists on disk
            file_path = STORAGE_ROOT / checksum[0] / checksum[1] / f"{checksum}.{extension}"
            if not file_path.exists():
                unmatched += 1
                continue

            # Find the content node in the index DB by kolibri_id
            # The kolibri_id was stored from content_contentnode.content_id
            # Try matching by contentnode_id first, then by content_id
            existing = index_conn.execute(
                """SELECT id FROM content
                   WHERE source = 'kolibri'
                   AND (kolibri_id = ? OR path LIKE ?)
                   LIMIT 1""",
                (node_id, f"%{node_id}%"),
            ).fetchone()

            if existing:
                index_conn.execute(
                    "UPDATE content SET kolibri_checksum = ? WHERE id = ?",
                    (checksum, existing["id"]),
                )
                matched += 1
            else:
                # Insert a minimal record if node not found
                # (can happen when DB versions differ)
                unmatched += 1

        ch_conn.close()

    except Exception as e:
        log.error(f"  Error processing {channel_db_path.name}: {e}")
        import traceback; traceback.print_exc()

    return matched, unmatched


def build_checksum_map(log: logging.Logger) -> dict:
    """
    Build a complete checksum → file_path map by reading ALL channel DBs.
    Also returns checksum → (channel_name, contentnode_id) for metadata lookup.
    """
    checksum_map = {}   # checksum → Path on disk
    meta_map = {}       # checksum → (channel_name, contentnode_id, title)

    db_dir = KOLIBRI_DB_DIR
    if not db_dir.exists():
        # Fallback: rglob
        dbs = list(KOLIBRI_ROOT.rglob("*.sqlite3"))
    else:
        dbs = list(db_dir.glob("*.sqlite3"))

    for db_path in dbs:
        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            tables = {r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}

            if "content_file" not in tables:
                conn.close()
                continue

            # Channel name
            channel_name = db_path.stem
            for mt in ("content_channelmetadata", "channelmetadata"):
                if mt in tables:
                    row = conn.execute(f"SELECT name FROM {mt} LIMIT 1").fetchone()
                    if row:
                        channel_name = row["name"]
                    break

            # Join content_file with content_contentnode for title
            has_node_table = "content_contentnode" in tables
            if has_node_table:
                rows = conn.execute("""
                    SELECT cf.checksum, cf.extension, cf.contentnode_id,
                           cn.title
                    FROM content_file cf
                    JOIN content_contentnode cn ON cn.id = cf.contentnode_id
                    WHERE cf.extension IN ('mp4','webm','ogv','m4v')
                    AND cf.thumbnail = 0
                """).fetchall()
            else:
                rows = conn.execute("""
                    SELECT cf.checksum, cf.extension, cf.contentnode_id,
                           '' as title
                    FROM content_file cf
                    WHERE cf.extension IN ('mp4','webm','ogv','m4v')
                    AND cf.thumbnail = 0
                """).fetchall()

            for row in rows:
                checksum  = row["checksum"]
                extension = row["extension"]
                file_path = (STORAGE_ROOT / checksum[0] / checksum[1]
                             / f"{checksum}.{extension}")
                if file_path.exists():
                    checksum_map[checksum] = file_path
                    meta_map[checksum] = {
                        "channel": channel_name,
                        "node_id": row["contentnode_id"],
                        "title":   row["title"] or "",
                    }

            conn.close()

        except Exception as e:
            log.warning(f"  Could not read {db_path.name}: {e}")

    log.info(f"Checksum map built: {len(checksum_map):,} video files resolved")
    return checksum_map, meta_map


def update_index_with_checksums(
    index_conn: sqlite3.Connection,
    checksum_map: dict,
    meta_map: dict,
    log: logging.Logger,
) -> int:
    """
    Update the index DB: for each checksum that resolves to a file,
    find or create a content row and set kolibri_checksum.
    Returns count of rows updated.
    """
    updated = 0
    inserted = 0

    for checksum, file_path in checksum_map.items():
        meta = meta_map.get(checksum, {})
        channel = meta.get("channel", "Kolibri")
        node_id = meta.get("node_id", "")
        title   = meta.get("title", file_path.stem)

        # Try to find existing row by node_id
        existing = None
        if node_id:
            existing = index_conn.execute(
                "SELECT id, kolibri_checksum FROM content WHERE kolibri_id = ? LIMIT 1",
                (node_id,),
            ).fetchone()

        if existing:
            if existing["kolibri_checksum"] != checksum:
                index_conn.execute(
                    "UPDATE content SET kolibri_checksum = ? WHERE id = ?",
                    (checksum, existing["id"]),
                )
                updated += 1
        else:
            # Row not found by node_id — check if checksum already exists
            existing2 = index_conn.execute(
                "SELECT id FROM content WHERE kolibri_checksum = ? LIMIT 1",
                (checksum,),
            ).fetchone()
            if not existing2:
                # Insert a minimal row so the checksum is queryable
                from datetime import datetime
                index_conn.execute(
                    """INSERT OR IGNORE INTO content
                       (source, path, filename, content_type, title,
                        subject, module, kolibri_id, kolibri_channel,
                        kolibri_checksum, last_scanned)
                       VALUES ('kolibri', ?, ?, 'video', ?, 'General', ?,
                               ?, ?, ?, ?)""",
                    (
                        f"kolibri_storage/{checksum}",
                        f"{checksum}.{file_path.suffix.lstrip('.')}",
                        title,
                        channel,
                        node_id,
                        channel,
                        checksum,
                        datetime.utcnow().isoformat(),
                    ),
                )
                inserted += 1

        if (updated + inserted) % 500 == 0 and (updated + inserted) > 0:
            index_conn.commit()

    index_conn.commit()
    log.info(f"  Updated: {updated:,}  Inserted: {inserted:,}")
    return updated + inserted


def main():
    parser = argparse.ArgumentParser(
        description="Fix Kolibri file resolution by mapping checksums to content nodes."
    )
    parser.add_argument("--config", "-c",
                        default="scripts/ares/ares_scan_config.yaml")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    log = logging.getLogger("kolibri_checksum_fix")

    with open(args.config) as f:
        config = yaml.safe_load(f)

    index_conn = get_index_db(config)
    ensure_checksum_column(index_conn)

    log.info("Building checksum → file path map from channel databases...")
    checksum_map, meta_map = build_checksum_map(log)

    if not checksum_map:
        log.error("No checksums resolved — check Kolibri paths")
        sys.exit(1)

    log.info("Updating index database...")
    total = update_index_with_checksums(index_conn, checksum_map, meta_map, log)
    log.info(f"Total rows updated/inserted: {total:,}")

    # Quick verification
    resolved = index_conn.execute(
        "SELECT COUNT(*) FROM content WHERE kolibri_checksum IS NOT NULL AND kolibri_checksum != ''"
    ).fetchone()[0]
    log.info(f"Rows with checksum in DB: {resolved:,}")

    # Sample
    samples = index_conn.execute(
        """SELECT kolibri_checksum, kolibri_channel, title FROM content
           WHERE kolibri_checksum IS NOT NULL AND content_type = 'video'
           LIMIT 5"""
    ).fetchall()
    log.info("Sample resolved entries:")
    for s in samples:
        log.info(f"  [{s['kolibri_channel']}] {s['title'][:50]}  → {s['kolibri_checksum']}")

    index_conn.close()
    log.info("Done. Re-run run_whisper_batch.py --priority --dry-run to verify.")


if __name__ == "__main__":
    main()
