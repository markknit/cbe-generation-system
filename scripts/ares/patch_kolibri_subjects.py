#!/usr/bin/env python3
"""
patch_kolibri_subjects.py
─────────────────────────
Re-reads Kolibri channel SQLite databases and updates the ARES content index
with richer subject, grade-level, and content-kind metadata pulled from
Kolibri's own tagging system.

This script does NOT rescan files — it only updates existing rows in the DB.
Run it on the ARES server after the initial scan, or on jhm-spark after
copying the Kolibri channel databases across.

Why this helps:
  The initial scan classified subjects using keyword matching on titles and
  file paths — most content came back as "General". Kolibri's channel databases
  contain explicit subject tags, grade levels, and learning activity labels
  that are far more accurate. This patch extracts those and updates the index.

Usage:
    python3 patch_kolibri_subjects.py --config ares_scan_config.yaml
    python3 patch_kolibri_subjects.py --config ares_scan_config.yaml --dry-run
    python3 patch_kolibri_subjects.py --config ares_scan_config.yaml --report
"""

import argparse
import json
import logging
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import yaml


# ─── Kolibri subject tag normalisation ────────────────────────────────────────
# Kolibri channels use various subject tag formats. These mappings normalise
# them to the four subjects used in the CBE lesson plan system.

SUBJECT_TAG_MAP = {
    # Biology
    "biology":                    "Biology",
    "life science":               "Biology",
    "life sciences":              "Biology",
    "living things":              "Biology",
    "natural science":            "Biology",
    "natural sciences":           "Biology",
    "science":                    "Biology",   # default science → Biology (most common)
    "health":                     "Biology",
    "environment":                "Biology",
    "ecology":                    "Biology",
    "anatomy":                    "Biology",
    "nutrition":                  "Biology",
    "genetics":                   "Biology",
    # Chemistry
    "chemistry":                  "Chemistry",
    "physical science":           "Chemistry",
    "physical sciences":          "Chemistry",
    "matter":                     "Chemistry",
    "chemical":                   "Chemistry",
    # Physics
    "physics":                    "Physics",
    "forces":                     "Physics",
    "energy":                     "Physics",
    "electricity":                "Physics",
    "magnetism":                  "Physics",
    "waves":                      "Physics",
    "optics":                     "Physics",
    # Mathematics
    "mathematics":                "Mathematics",
    "math":                       "Mathematics",
    "maths":                      "Mathematics",
    "arithmetic":                 "Mathematics",
    "algebra":                    "Mathematics",
    "geometry":                   "Mathematics",
    "statistics":                 "Mathematics",
    "numeracy":                   "Mathematics",
    "number":                     "Mathematics",
}


def normalise_subject_from_tags(tags: str | None) -> str | None:
    """
    Given a comma/semicolon-separated tag string from Kolibri, return the best
    matching subject, or None if no match.
    """
    if not tags:
        return None
    tag_list = re.split(r"[,;|]", tags.lower())
    for tag in tag_list:
        tag = tag.strip()
        if tag in SUBJECT_TAG_MAP:
            return SUBJECT_TAG_MAP[tag]
        # Partial match
        for key, subject in SUBJECT_TAG_MAP.items():
            if key in tag or tag in key:
                return subject
    return None


def grade_level_from_tags(tags: str | None) -> str | None:
    """Extract a grade level string from Kolibri tags."""
    if not tags:
        return None
    m = re.search(r"grade\s*(\d+)", tags, re.IGNORECASE)
    if m:
        return f"Grade {m.group(1)}"
    m = re.search(r"\bK?(\d+)\b", tags)
    if m:
        num = int(m.group(1))
        if 1 <= num <= 12:
            return f"Grade {num}"
    return None


# ─── Kolibri schema discovery ─────────────────────────────────────────────────

def get_kolibri_tables(ch_conn: sqlite3.Connection) -> dict:
    """Return a dict of table names present in this channel DB."""
    tables = {
        row[0] for row in
        ch_conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    return tables


def get_node_table(tables: set) -> str | None:
    for candidate in ("content_contentnode", "contentnode"):
        if candidate in tables:
            return candidate
    return None


def get_columns(ch_conn: sqlite3.Connection, table: str) -> set:
    return {row[1] for row in ch_conn.execute(f"PRAGMA table_info({table})")}


# ─── Main patch logic ─────────────────────────────────────────────────────────

def patch(config: dict, dry_run: bool = False, report_only: bool = False) -> None:
    db_path = config.get("output_db", "ares_content.db")
    kolibri_root = None
    for src in config.get("content_sources", []):
        if src.get("type") == "kolibri":
            kolibri_root = Path(src["path"])
            break

    if not kolibri_root:
        print("ERROR: No Kolibri source found in config content_sources.")
        sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    log = logging.getLogger("kolibri_patch")

    if not os.path.exists(db_path):
        log.error(f"Index DB not found: {db_path}")
        sys.exit(1)

    index_conn = sqlite3.connect(db_path)
    index_conn.row_factory = sqlite3.Row

    if report_only:
        _report(index_conn)
        index_conn.close()
        return

    # Find channel databases
    db_dirs = [
        kolibri_root / "content" / "databases",
        kolibri_root / "databases",
        kolibri_root,
    ]
    channel_dbs = []
    for d in db_dirs:
        if d.exists():
            found = list(d.glob("*.sqlite3"))
            if found:
                channel_dbs = found
                log.info(f"Found {len(found)} channel DB(s) in {d}")
                break

    if not channel_dbs:
        channel_dbs = list(kolibri_root.rglob("*.sqlite3"))
        log.warning(f"Used rglob — found {len(channel_dbs)} DB(s)")

    total_updated = 0
    total_skipped = 0
    subject_changes: Counter = Counter()
    channel_stats: dict = defaultdict(lambda: {"updated": 0, "subjects": Counter()})

    for db_file in channel_dbs:
        log.info(f"\nProcessing: {db_file.name}")
        try:
            ch_conn = sqlite3.connect(str(db_file))
            ch_conn.row_factory = sqlite3.Row
            tables = get_kolibri_tables(ch_conn)
            node_table = get_node_table(tables)

            if not node_table:
                log.warning(f"  No content node table — skipping")
                ch_conn.close()
                continue

            cols = get_columns(ch_conn, node_table)

            # Get channel name
            channel_name = db_file.stem
            for meta_table in ("content_channelmetadata", "channelmetadata"):
                if meta_table in tables:
                    row = ch_conn.execute(
                        f"SELECT name FROM {meta_table} LIMIT 1"
                    ).fetchone()
                    if row:
                        channel_name = row["name"]
                    break

            # ── Build SELECT based on available columns ──────────────────────
            # Priority columns for subject extraction:
            #   tags, subject, grade_levels, learning_activities, categories
            # Kolibri v0.15+ uses content_tags many-to-many; older versions
            # have a tags column directly on contentnode.

            select_cols = ["id"]
            if "content_id" in cols:
                select_cols.append("content_id")
            if "title" in cols:
                select_cols.append("title")
            if "kind" in cols:
                select_cols.append("kind")
            if "available" in cols:
                select_cols.append("available")

            # Subject-relevant columns (vary by Kolibri version)
            tag_cols = []
            for c in ("tags", "subject", "grade_levels", "learning_activities",
                      "categories", "lang_id", "coach_content"):
                if c in cols:
                    select_cols.append(c)
                    if c in ("tags", "subject", "categories", "grade_levels"):
                        tag_cols.append(c)

            rows = ch_conn.execute(
                f"SELECT {', '.join(select_cols)} FROM {node_table}"
            ).fetchall()

            log.info(f"  Channel: {channel_name} | {len(rows)} nodes | tag cols: {tag_cols}")

            # ── Check for content_tags many-to-many table ────────────────────
            # Kolibri 0.15+ stores tags separately
            has_tags_table = "content_contenttag" in tables or "content_tags" in tables
            tags_table = "content_contenttag" if "content_contenttag" in tables else (
                "content_tags" if "content_tags" in tables else None
            )

            # Build a node_id → tags lookup if the separate table exists
            tag_lookup: dict = {}
            if tags_table:
                try:
                    tag_cols_in_table = get_columns(ch_conn, tags_table)
                    # Typical structure: contentnode_id (or node_id), tag_name (or name)
                    id_col = next(
                        (c for c in ("contentnode_id", "node_id", "content_id") if c in tag_cols_in_table),
                        None
                    )
                    name_col = next(
                        (c for c in ("tag_name", "name", "value") if c in tag_cols_in_table),
                        None
                    )
                    if id_col and name_col:
                        for tag_row in ch_conn.execute(
                            f"SELECT {id_col}, {name_col} FROM {tags_table}"
                        ):
                            nid = tag_row[0]
                            tag = tag_row[1]
                            if nid not in tag_lookup:
                                tag_lookup[nid] = []
                            tag_lookup[nid].append(str(tag))
                        log.info(f"  Loaded {len(tag_lookup)} tag associations from {tags_table}")
                except Exception as e:
                    log.warning(f"  Could not read tags table: {e}")

            channel_updated = 0
            for row in rows:
                d = dict(row)
                node_id = d.get("content_id") or d.get("id") or ""
                kind = d.get("kind", "")
                title = d.get("title", "")

                # ── Collect all tag text ──────────────────────────────────────
                tag_parts = []
                for tc in tag_cols:
                    val = d.get(tc)
                    if val:
                        tag_parts.append(str(val))

                # Add from many-to-many table if available
                if node_id in tag_lookup:
                    tag_parts.extend(tag_lookup[node_id])
                if d.get("id") in tag_lookup:
                    tag_parts.extend(tag_lookup[d["id"]])

                combined_tags = " ".join(tag_parts)

                # ── Determine best subject ────────────────────────────────────
                new_subject = normalise_subject_from_tags(combined_tags)

                # If tags gave nothing, try the title keywords as a fallback
                if not new_subject and title:
                    new_subject = normalise_subject_from_tags(title)

                if not new_subject:
                    total_skipped += 1
                    continue

                # ── Find matching row in index DB ─────────────────────────────
                # Match by kolibri_id or by title+channel combo
                existing = index_conn.execute(
                    "SELECT id, subject, kolibri_id FROM content WHERE kolibri_id = ?",
                    (str(node_id),),
                ).fetchone()

                if not existing and title:
                    existing = index_conn.execute(
                        """SELECT id, subject, kolibri_id FROM content
                           WHERE kolibri_channel = ? AND title = ? AND source = 'kolibri'
                           LIMIT 1""",
                        (channel_name, title),
                    ).fetchone()

                if not existing:
                    total_skipped += 1
                    continue

                old_subject = existing["subject"]
                if old_subject == new_subject:
                    total_skipped += 1
                    continue

                if not dry_run:
                    index_conn.execute(
                        "UPDATE content SET subject = ? WHERE id = ?",
                        (new_subject, existing["id"]),
                    )

                total_updated += 1
                channel_updated += 1
                subject_changes[f"{old_subject} → {new_subject}"] += 1
                channel_stats[channel_name]["updated"] += 1
                channel_stats[channel_name]["subjects"][new_subject] += 1

                if total_updated % 500 == 0 and not dry_run:
                    index_conn.commit()
                    log.info(f"  {total_updated} updates committed so far...")

            log.info(f"  Updated {channel_updated} nodes in {channel_name}")
            ch_conn.close()

        except Exception as e:
            log.error(f"Error processing {db_file.name}: {e}")
            import traceback; traceback.print_exc()

    if not dry_run:
        index_conn.commit()
        # Rebuild module summary
        _rebuild_modules(index_conn, log)

    index_conn.close()

    # ── Summary report ────────────────────────────────────────────────────────
    print(f"\n{'═'*60}")
    print(f"  Kolibri Subject Patch {'(DRY RUN — no changes made)' if dry_run else 'Complete'}")
    print(f"{'═'*60}")
    print(f"  Rows updated : {total_updated:,}")
    print(f"  Rows skipped : {total_skipped:,}  (no tag data or already correct)")

    if subject_changes:
        print(f"\n  Subject reassignments:")
        for change, count in subject_changes.most_common():
            print(f"    {change:<40} ×{count:,}")

    if channel_stats:
        print(f"\n  By channel:")
        for ch, stats in sorted(channel_stats.items(), key=lambda x: -x[1]["updated"]):
            subj_str = ", ".join(
                f"{s}:{c}" for s, c in stats["subjects"].most_common()
            )
            print(f"    {ch:<42} {stats['updated']:>5,} updates  [{subj_str}]")
    print()


def _rebuild_modules(conn: sqlite3.Connection, log: logging.Logger) -> None:
    log.info("Rebuilding module summary table...")
    conn.execute("DELETE FROM modules")
    rows = conn.execute(
        """
        SELECT module, source,
               COUNT(*) AS total,
               SUM(CASE WHEN content_type='video'    THEN 1 ELSE 0 END) AS videos,
               SUM(CASE WHEN content_type='pdf'      THEN 1 ELSE 0 END) AS pdfs,
               SUM(CASE WHEN content_type='html'     THEN 1 ELSE 0 END) AS htmls,
               SUM(CASE WHEN content_type='exercise' THEN 1 ELSE 0 END) AS exercises,
               GROUP_CONCAT(DISTINCT subject) AS subjects
        FROM content
        GROUP BY module, source
        """
    ).fetchall()
    for r in rows:
        conn.execute(
            """INSERT INTO modules
               (name, source, content_count, video_count, pdf_count,
                html_count, exercise_count, subjects)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (r["module"], r["source"], r["total"], r["videos"],
             r["pdfs"], r["htmls"], r["exercises"], r["subjects"]),
        )
    conn.commit()
    log.info("Module summary rebuilt.")


def _report(conn: sqlite3.Connection) -> None:
    """Show current subject distribution before patching."""
    print(f"\n{'─'*60}")
    print("  Current subject distribution (Kolibri content only)")
    print(f"{'─'*60}")
    rows = conn.execute(
        """SELECT subject, COUNT(*) n FROM content
           WHERE source='kolibri' GROUP BY subject ORDER BY n DESC"""
    ).fetchall()
    total = sum(r["n"] for r in rows)
    for r in rows:
        pct = 100 * r["n"] // max(total, 1)
        print(f"  {r['subject']:<24} {r['n']:>7,}  ({pct}%)")
    print(f"\n  Total Kolibri items: {total:,}")

    print(f"\n{'─'*60}")
    print("  Channels with the most 'General' content (patch targets)")
    print(f"{'─'*60}")
    rows = conn.execute(
        """SELECT kolibri_channel, COUNT(*) n FROM content
           WHERE source='kolibri' AND subject='General'
           GROUP BY kolibri_channel ORDER BY n DESC LIMIT 15"""
    ).fetchall()
    for r in rows:
        print(f"  {r['kolibri_channel']:<44} {r['n']:>6,}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Enrich ARES index subject tags from Kolibri channel metadata."
    )
    parser.add_argument("--config", "-c", default="ares_scan_config.yaml")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would change without writing to the DB",
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Show current subject distribution only (no changes)",
    )
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    patch(config, dry_run=args.dry_run, report_only=args.report)


if __name__ == "__main__":
    main()
