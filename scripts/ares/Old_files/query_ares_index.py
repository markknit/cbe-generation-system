#!/usr/bin/env python3
"""
query_ares_index.py
────────────────────
CLI tool to search and inspect the ARES content index.
Used for testing, manual content review, and as the basis for the lesson
plan generation pipeline's resource recommendation module.

Usage:
    # Full-text search
    python3 query_ares_index.py search "photosynthesis chlorophyll"

    # Filter by subject
    python3 query_ares_index.py search "cell membrane" --subject Biology

    # Filter by content type
    python3 query_ares_index.py search "mitosis" --type video

    # Find content relevant to a lesson plan phase (main use case)
    python3 query_ares_index.py recommend \
        --substrand "Cell Structure and Specialisation" \
        --topic "organelles electron microscope" \
        --subject Biology \
        --phase observe \
        --n 5

    # Summary of what's in the index
    python3 query_ares_index.py summary

    # List all modules
    python3 query_ares_index.py modules

    # Inspect a single content item
    python3 query_ares_index.py get --path "khan/biology/cells/cell_membrane.mp4"
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

import yaml


# ─── DB connection ─────────────────────────────────────────────────────────────

def get_db(config: dict) -> sqlite3.Connection:
    db_path = config.get("output_db", "ares_content.db")
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found: {db_path}")
        print("Run scan_ares_content.py first.")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# ─── Search ───────────────────────────────────────────────────────────────────

def cmd_search(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    query = args.query
    subject = args.subject
    content_type = args.type
    n = args.n
    with_transcript_only = args.with_transcript

    conditions = []
    params: list = []

    if subject:
        conditions.append("c.subject = ?")
        params.append(subject)

    if content_type:
        conditions.append("c.content_type = ?")
        params.append(content_type)

    if with_transcript_only:
        conditions.append("c.transcript_path != '' AND c.transcript_path IS NOT NULL")

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    if query.strip():
        # Use FTS5 for full-text search
        sql = f"""
            SELECT c.id, c.path, c.filename, c.content_type, c.title,
                   c.subject, c.module, c.size_bytes, c.transcript_path,
                   c.keywords,
                   fts.rank AS score
            FROM content_fts fts
            JOIN content c ON c.id = fts.rowid
            {where_clause}
            AND content_fts MATCH ?
            ORDER BY fts.rank
            LIMIT ?
        """
        params_fts = params + [query, n]
        try:
            rows = conn.execute(sql, params_fts).fetchall()
        except sqlite3.OperationalError as e:
            # FTS MATCH can fail on some query syntax — fall back to LIKE
            print(f"FTS error ({e}), falling back to LIKE search...")
            rows = _fallback_search(conn, query, where_clause, params, n)
    else:
        # No query text — just apply filters
        sql = f"""
            SELECT c.id, c.path, c.filename, c.content_type, c.title,
                   c.subject, c.module, c.size_bytes, c.transcript_path,
                   c.keywords
            FROM content c
            {where_clause}
            ORDER BY c.title
            LIMIT ?
        """
        rows = conn.execute(sql, params + [n]).fetchall()

    _print_results(rows, verbose=args.verbose)


def _fallback_search(
    conn: sqlite3.Connection, query: str, where_clause: str, params: list, n: int
) -> list:
    terms = query.split()
    like_clauses = " AND ".join(
        "(c.title LIKE ? OR c.extracted_text LIKE ? OR c.transcript_text LIKE ? OR c.keywords LIKE ?)"
        for _ in terms
    )
    like_params = []
    for term in terms:
        like_params += [f"%{term}%"] * 4
    sep = " AND " if where_clause else "WHERE "
    sql = f"""
        SELECT c.id, c.path, c.filename, c.content_type, c.title,
               c.subject, c.module, c.size_bytes, c.transcript_path,
               c.keywords
        FROM content c
        {where_clause}
        {sep if not where_clause else 'AND '}({like_clauses})
        ORDER BY c.title
        LIMIT ?
    """
    return conn.execute(sql, params + like_params + [n]).fetchall()


def _print_results(rows: list, verbose: bool = False) -> None:
    if not rows:
        print("No results found.")
        return

    print(f"\n{'─'*70}")
    print(f"  {len(rows)} result(s) found")
    print(f"{'─'*70}")

    for i, row in enumerate(rows, 1):
        d = dict(row)
        has_transcript = bool(d.get("transcript_path"))
        t_marker = " 📝" if has_transcript else ""
        print(f"\n[{i}] {d.get('title', d['filename'])}{t_marker}")
        print(f"     Type    : {d['content_type']}  |  Subject: {d['subject']}  |  Module: {d['module']}")
        print(f"     Path    : {d['path']}")
        if verbose:
            print(f"     Size    : {_format_size(d.get('size_bytes', 0))}")
            if d.get("keywords"):
                print(f"     Keywords: {d['keywords']}")
            if has_transcript:
                print(f"     Transcript: {d['transcript_path']}")
        if "score" in d:
            print(f"     Score   : {d['score']:.4f}")

    print()


def _format_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


# ─── Recommend ────────────────────────────────────────────────────────────────

# Phase-specific search term boosts — used when recommending content for a
# specific lesson plan phase.
PHASE_BOOST_TERMS = {
    "predict": ["introduction", "overview", "what is", "phenomenon", "curiosity"],
    "observe": ["experiment", "practical", "demonstration", "observation", "video", "animation"],
    "explain": ["explanation", "concept", "theory", "how", "why", "mechanism"],
    "dqb": ["question", "review", "summary", "connect"],
    "model": ["diagram", "model", "structure", "system", "process", "cycle"],
}


def cmd_recommend(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    """
    Recommend ARES content for a specific lesson plan context.
    This is the core function called by the lesson generation pipeline.

    Returns ranked recommendations with:
    - Primary recommendation (best single resource)
    - Search terms for teacher to use in ARES
    - Up to n alternatives
    """
    substrand = args.substrand or ""
    topic = args.topic or ""
    subject = args.subject or ""
    phase = (args.phase or "").lower()
    n = args.n

    # Build search query from substrand + topic
    query_terms = []
    if substrand:
        # Extract key words from sub-strand name
        words = re.findall(r"\b[a-zA-Z]{4,}\b", substrand)
        query_terms.extend(words[:3])
    if topic:
        words = re.findall(r"\b[a-zA-Z]{4,}\b", topic)
        query_terms.extend(words[:4])
    if phase and phase in PHASE_BOOST_TERMS:
        query_terms.extend(PHASE_BOOST_TERMS[phase][:2])

    query = " ".join(set(query_terms))

    conditions = []
    params: list = []
    if subject:
        conditions.append("(c.subject = ? OR c.subject = 'General')")
        params.append(subject)

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    # Prioritise: videos with transcripts > videos > PDFs > HTML > images
    sql = f"""
        SELECT c.id, c.path, c.filename, c.content_type, c.title,
               c.subject, c.module, c.size_bytes, c.transcript_path,
               c.keywords, c.duration_seconds,
               fts.rank AS score,
               CASE c.content_type
                   WHEN 'video' THEN 1
                   WHEN 'audio' THEN 2
                   WHEN 'pdf'   THEN 3
                   WHEN 'html'  THEN 4
                   ELSE 5
               END AS type_priority,
               CASE WHEN (c.transcript_path IS NOT NULL AND c.transcript_path != '') THEN 0 ELSE 1 END AS no_transcript
        FROM content_fts fts
        JOIN content c ON c.id = fts.rowid
        {where_clause}
        {'AND' if where_clause else 'WHERE'} content_fts MATCH ?
        ORDER BY fts.rank, no_transcript, type_priority
        LIMIT ?
    """
    try:
        rows = conn.execute(sql, params + [query, n * 3]).fetchall()
    except sqlite3.OperationalError:
        rows = _fallback_search(conn, query, where_clause, params, n * 3)

    if not rows:
        print(f"\nNo recommendations found for: '{query}'")
        return

    results = [dict(r) for r in rows[:n]]

    print(f"\n{'═'*70}")
    print(f"  ARES Content Recommendations")
    print(f"{'═'*70}")
    print(f"  Sub-strand : {substrand}")
    print(f"  Topic      : {topic}")
    print(f"  Phase      : {phase.title() if phase else 'All phases'}")
    print(f"  Subject    : {subject or 'All'}")
    print(f"{'─'*70}")

    # Primary recommendation
    primary = results[0]
    has_t = bool(primary.get("transcript_path"))
    print(f"\n  ★ PRIMARY RECOMMENDATION")
    print(f"     Title    : {primary.get('title', primary['filename'])}")
    print(f"     Type     : {primary['content_type']}")
    print(f"     Module   : {primary['module']}")
    print(f"     Path     : {primary['path']}")
    if primary.get("duration_seconds"):
        mins = int(primary["duration_seconds"]) // 60
        secs = int(primary["duration_seconds"]) % 60
        print(f"     Duration : {mins}m {secs:02d}s")
    print(f"     Transcript available: {'Yes ✓' if has_t else 'No'}")

    # Suggested ARES search terms for the teacher
    kw_base = topic or substrand or subject
    search_terms = _generate_search_terms(kw_base, subject, phase)
    print(f"\n  SUGGESTED ARES SEARCH TERMS FOR TEACHER:")
    for term in search_terms:
        print(f"     • {term}")

    # Alternatives
    if len(results) > 1:
        print(f"\n  ALTERNATIVES:")
        for r in results[1:]:
            has_t2 = "📝" if r.get("transcript_path") else "  "
            print(f"     {has_t2} [{r['content_type']:6}] {r.get('title', r['filename'])}")
            print(f"            {r['path']}")

    print()

    # JSON output for pipeline use
    if args.json:
        output = {
            "query": {"substrand": substrand, "topic": topic, "subject": subject, "phase": phase},
            "search_terms": search_terms,
            "primary": primary,
            "alternatives": results[1:],
        }
        print(json.dumps(output, indent=2, default=str))


def _generate_search_terms(topic: str, subject: str, phase: str) -> list[str]:
    """
    Generate 3–5 search term suggestions for a teacher to use in ARES.
    These are the strings that will appear in the lesson plan document.
    """
    terms = []
    base = topic.strip() if topic else subject
    if base:
        terms.append(base)
    if subject and subject not in base:
        terms.append(f"{subject} {base}")
    if phase and phase in PHASE_BOOST_TERMS:
        for boost in PHASE_BOOST_TERMS[phase][:2]:
            terms.append(f"{base} {boost}")
    # Deduplicate, preserve order
    seen = set()
    unique = []
    for t in terms:
        tl = t.lower()
        if tl not in seen:
            seen.add(tl)
            unique.append(t)
    return unique[:5]


# ─── Summary ─────────────────────────────────────────────────────────────────

def cmd_summary(conn: sqlite3.Connection) -> None:
    total = conn.execute("SELECT COUNT(*) FROM content").fetchone()[0]
    print(f"\n{'═'*60}")
    print(f"  ARES Content Index Summary")
    print(f"{'═'*60}")
    print(f"  Total items indexed: {total:,}")

    print(f"\n  By content type:")
    rows = conn.execute(
        "SELECT content_type, COUNT(*) AS n FROM content GROUP BY content_type ORDER BY n DESC"
    ).fetchall()
    for r in rows:
        print(f"    {r['content_type']:<12} {r['n']:>6,}")

    print(f"\n  By subject:")
    rows = conn.execute(
        "SELECT subject, COUNT(*) AS n FROM content GROUP BY subject ORDER BY n DESC"
    ).fetchall()
    for r in rows:
        print(f"    {r['subject']:<24} {r['n']:>6,}")

    print(f"\n  By module:")
    rows = conn.execute(
        "SELECT name, source, content_count, video_count, pdf_count, html_count, exercise_count, subjects FROM modules ORDER BY content_count DESC"
    ).fetchall()
    for r in rows:
        src = f"[{r['source']}]" if r['source'] else ""
        print(f"    {r['name']:<34} {src:<10} {r['content_count']:>7,} items")
        if r['subjects']:
            print(f"      Subjects: {r['subjects']}")

    video_total = conn.execute(
        "SELECT COUNT(*) FROM content WHERE content_type IN ('video','audio')"
    ).fetchone()[0]
    transcribed = conn.execute(
        "SELECT COUNT(*) FROM content WHERE content_type IN ('video','audio') AND transcript_path != '' AND transcript_path IS NOT NULL"
    ).fetchone()[0]
    pct = 100 * transcribed // max(video_total, 1)
    print(f"\n  Transcript coverage: {transcribed}/{video_total} videos ({pct}%)")

    last_scan = conn.execute(
        "SELECT started_at, files_indexed FROM scan_runs ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if last_scan:
        print(f"\n  Last scan: {last_scan['started_at']} ({last_scan['files_indexed']:,} files indexed)")
    print()


# ─── Modules ─────────────────────────────────────────────────────────────────

def cmd_modules(conn: sqlite3.Connection) -> None:
    rows = conn.execute(
        "SELECT * FROM modules ORDER BY content_count DESC"
    ).fetchall()
    print(f"\n{'─'*60}")
    print(f"  {'Module':<30} {'Items':>6}  {'Videos':>7}  {'PDFs':>5}  {'HTML':>5}")
    print(f"{'─'*60}")
    for r in rows:
        print(f"  {r['name']:<30} {r['content_count']:>6,}  {r['video_count']:>7,}  {r['pdf_count']:>5,}  {r['html_count']:>5,}")
    print()


# ─── Get single item ─────────────────────────────────────────────────────────

def cmd_get(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = conn.execute(
        "SELECT * FROM content WHERE path LIKE ?", (f"%{args.path}%",)
    ).fetchone()
    if not row:
        print(f"Not found: {args.path}")
        return
    d = dict(row)
    print(f"\n{'═'*60}")
    for k, v in d.items():
        if v and k not in ("extracted_text", "transcript_text"):
            print(f"  {k:<20}: {v}")
    if args.text and d.get("extracted_text"):
        print(f"\n  Extracted text (first 500 chars):")
        print(f"  {d['extracted_text'][:500]}")
    if args.text and d.get("transcript_text"):
        print(f"\n  Transcript text (first 500 chars):")
        print(f"  {d['transcript_text'][:500]}")
    print()


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Query the ARES content index for lesson plan resource recommendations."
    )
    parser.add_argument("--config", "-c", default="ares_scan_config.yaml")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = subparsers.add_parser("search", help="Full-text search the index")
    p_search.add_argument("query", nargs="?", default="", help="Search terms")
    p_search.add_argument("--subject", choices=["Biology", "Chemistry", "Physics", "Mathematics", "General"])
    p_search.add_argument("--type", dest="type", choices=["video", "audio", "pdf", "html", "image"])
    p_search.add_argument("--with-transcript", action="store_true")
    p_search.add_argument("--n", type=int, default=10)
    p_search.add_argument("--verbose", "-v", action="store_true")

    # recommend
    p_rec = subparsers.add_parser("recommend", help="Get recommendations for a lesson plan segment")
    p_rec.add_argument("--substrand", help="Sub-strand name (e.g. 'Cell Structure and Specialisation')")
    p_rec.add_argument("--topic", help="Specific topic within the lesson")
    p_rec.add_argument("--subject", choices=["Biology", "Chemistry", "Physics", "Mathematics"])
    p_rec.add_argument("--phase", choices=["predict", "observe", "explain", "dqb", "model"])
    p_rec.add_argument("--n", type=int, default=5)
    p_rec.add_argument("--json", action="store_true", help="Also output raw JSON (for pipeline use)")

    # summary
    subparsers.add_parser("summary", help="Summary of index contents")

    # modules
    subparsers.add_parser("modules", help="List all detected ARES modules")

    # get
    p_get = subparsers.add_parser("get", help="Inspect a single content item")
    p_get.add_argument("--path", required=True, help="Path fragment to match")
    p_get.add_argument("--text", action="store_true", help="Show extracted text snippet")

    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    conn = get_db(config)

    if args.command == "search":
        cmd_search(conn, args)
    elif args.command == "recommend":
        cmd_recommend(conn, args)
    elif args.command == "summary":
        cmd_summary(conn)
    elif args.command == "modules":
        cmd_modules(conn)
    elif args.command == "get":
        cmd_get(conn, args)

    conn.close()


if __name__ == "__main__":
    main()
