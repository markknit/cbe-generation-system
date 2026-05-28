#!/usr/bin/env python3
"""
query_ares_index.py
────────────────────
CLI tool to search and inspect the ARES content index.
Used for testing, manual content review, and as the basis for the lesson
plan generation pipeline's resource recommendation module.

Usage:
    python3 query_ares_index.py search "photosynthesis chlorophyll"
    python3 query_ares_index.py search "cell membrane" --subject Biology
    python3 query_ares_index.py recommend \
        --substrand "Cell Structure and Specialisation" \
        --topic "organelles electron microscope" \
        --subject Biology --phase observe --n 5
    python3 query_ares_index.py summary
    python3 query_ares_index.py modules
    python3 query_ares_index.py get --path "some/path"
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


# ─── Path display ─────────────────────────────────────────────────────────────

def readable_path(path: str, module: str) -> str:
    """Replace hash-based internal paths with a human-readable module reference."""
    if not path:
        return f"[{module}]"
    if path.startswith("kolibri_storage/"):
        return f"[{module}] — search by title in ARES"
    if re.search(r"[0-9a-f]{32}", path):
        return f"[{module}] — search by title in ARES"
    return path


def format_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


# ─── Phase boost terms ────────────────────────────────────────────────────────

PHASE_BOOST_TERMS = {
    "predict": ["introduction", "overview", "phenomenon", "curiosity"],
    "observe": ["experiment", "practical", "demonstration", "observation", "video", "animation"],
    "explain": ["explanation", "concept", "theory", "how", "why", "mechanism"],
    "dqb":    ["question", "review", "summary", "connect"],
    "model":  ["diagram", "model", "structure", "system", "process", "cycle"],
}

# ─── Module tiers ─────────────────────────────────────────────────────────────
# Tier 0: dedicated curriculum/educational content
# Tier 1: good reference content (Wikipedia ZIMs via Kiwix)
# Tier 2: general/mixed web content

TIER_0_MODULES = {
    "KICD Educhannel",
    "Khan Academy (English - US curriculum)",
    "Khan Academy (Kiswahili)",
    "MIT Blossoms",
    "PhET Interactive Simulations (English)",
    "TED-Ed Lessons",
    "CK-12",
    "TESSA - Teacher Resources",
    "Kenya Curriculum Tools 2025",
    "Ubongo Kids",
}


def module_tier(module: str) -> int:
    if module in TIER_0_MODULES:
        return 0
    if "Wikipedia" in (module or "") or module == "Kiwix":
        return 1
    return 2


# ─── Search ───────────────────────────────────────────────────────────────────

def cmd_search(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    query = args.query
    subject = args.subject
    content_type = args.type
    n = args.n
    with_transcript_only = args.with_transcript

    conditions, params = [], []
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
        sql = f"""
            SELECT c.id, c.path, c.filename, c.content_type, c.title,
                   c.subject, c.module, c.size_bytes, c.transcript_path,
                   c.keywords, fts.rank AS score
            FROM content_fts fts
            JOIN content c ON c.id = fts.rowid
            {where_clause}
            {'AND' if where_clause else 'WHERE'} content_fts MATCH ?
            ORDER BY fts.rank
            LIMIT ?
        """
        try:
            rows = conn.execute(sql, params + [query, n]).fetchall()
        except sqlite3.OperationalError as e:
            print(f"FTS error ({e}), falling back to LIKE search...")
            rows = _fallback_search(conn, query, where_clause, params, n)
    else:
        sql = f"""
            SELECT c.id, c.path, c.filename, c.content_type, c.title,
                   c.subject, c.module, c.size_bytes, c.transcript_path, c.keywords
            FROM content c {where_clause}
            ORDER BY c.title LIMIT ?
        """
        rows = conn.execute(sql, params + [n]).fetchall()

    _print_results(rows, verbose=args.verbose)


def _fallback_search(conn, query, where_clause, params, n):
    terms = query.split()
    like_clauses = " AND ".join(
        "(c.title LIKE ? OR c.extracted_text LIKE ? OR c.transcript_text LIKE ? OR c.keywords LIKE ?)"
        for _ in terms
    )
    like_params = [p for term in terms for p in [f"%{term}%"] * 4]
    sep = "AND " if where_clause else "WHERE "
    sql = f"""
        SELECT c.id, c.path, c.filename, c.content_type, c.title,
               c.subject, c.module, c.size_bytes, c.transcript_path, c.keywords
        FROM content c {where_clause} {sep}({like_clauses})
        ORDER BY c.title LIMIT ?
    """
    return conn.execute(sql, params + like_params + [n]).fetchall()


def _print_results(rows, verbose=False):
    if not rows:
        print("No results found.")
        return
    print(f"\n{'─'*70}")
    print(f"  {len(rows)} result(s) found")
    print(f"{'─'*70}")
    for i, row in enumerate(rows, 1):
        d = dict(row)
        has_t = bool(d.get("transcript_path"))
        marker = " 📝" if has_t else ""
        print(f"\n[{i}] {d.get('title', d['filename'])}{marker}")
        print(f"     Type    : {d['content_type']}  |  Subject: {d['subject']}  |  Module: {d['module']}")
        print(f"     Path    : {readable_path(d['path'], d['module'])}")
        if verbose:
            print(f"     Size    : {format_size(d.get('size_bytes', 0))}")
            if d.get("keywords"):
                print(f"     Keywords: {d['keywords']}")
    print()


# ─── Recommend ────────────────────────────────────────────────────────────────

def cmd_recommend(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    """
    Recommend ARES content for a specific lesson plan context.

    Ranking priority:
      1. Title hit count  — search terms appearing in the title (most specific match)
      2. Total hit count  — how many search terms matched anywhere in the content
      3. Subject match    — exact subject match ranks above General
      4. Module tier      — curriculum content > Wikipedia > general web
      5. Transcript       — transcribed content ranks above untranscribed
      6. Content type     — video > audio > pdf > html
      7. FTS score        — tiebreaker
    """
    substrand = args.substrand or ""
    topic     = args.topic or ""
    subject   = args.subject or ""
    phase     = (args.phase or "").lower()
    n         = args.n

    # Build individual search terms (deduped, lowercase)
    raw_terms = []
    if substrand:
        raw_terms.extend(re.findall(r"\b[a-zA-Z]{4,}\b", substrand)[:3])
    if topic:
        raw_terms.extend(re.findall(r"\b[a-zA-Z]{4,}\b", topic)[:5])
    if phase and phase in PHASE_BOOST_TERMS:
        raw_terms.extend(PHASE_BOOST_TERMS[phase][:2])
    query_terms = list(dict.fromkeys(w.lower() for w in raw_terms))

    subject_filter = "(c.subject = ? OR c.subject = 'General')" if subject else ""
    subject_params = [subject] if subject else []

    # Search each term separately, accumulate per-row hit counts
    seen: dict = {}
    for term in query_terms:
        try:
            sql = f"""
                SELECT c.id, c.path, c.filename, c.content_type, c.title,
                       c.subject, c.module, c.size_bytes, c.transcript_path,
                       c.keywords, c.duration_seconds, fts.rank
                FROM content_fts fts
                JOIN content c ON c.id = fts.rowid
                WHERE content_fts MATCH ?
                {'AND ' + subject_filter if subject_filter else ''}
                AND c.content_type NOT IN ('topic', 'image', 'exercise', 'zim')
                ORDER BY fts.rank
                LIMIT 30
            """
            rows = conn.execute(sql, [term] + subject_params).fetchall()
            for row in rows:
                rid = row["id"]
                if rid not in seen:
                    seen[rid] = dict(row)
                    seen[rid]["hit_count"] = 1
                    seen[rid]["score"] = float(row["rank"] or 0)
                else:
                    seen[rid]["hit_count"] += 1
        except sqlite3.OperationalError:
            continue

    if not seen:
        print(f"\nNo recommendations found for: {query_terms}")
        return

    # Title hit count — terms appearing in the title indicate a more specific match
    term_set = set(query_terms)

    def title_hits(r: dict) -> int:
        title = (r.get("title") or "").lower()
        return sum(1 for t in term_set if t in title)

    def sort_key(r: dict) -> tuple:
        has_transcript = 0 if r.get("transcript_path") else 1
        ctype = {"video":0,"audio":1,"pdf":2,"html":3}.get(r.get("content_type",""),4)
        return (
            has_transcript + ctype,                                  # transcribed video first
            -title_hits(r),                                          # title specificity
            -r["hit_count"],                                         # overall term coverage
            0 if r.get("subject") == subject else 1,                 # subject match
            module_tier(r.get("module", "")),                        # module tier
            r["score"],                                              # FTS score
        )

    ranked = sorted(seen.values(), key=sort_key)

    # Deduplicate by title
    seen_titles: set = set()
    deduped = []
    for r in ranked:
        title_key = (r.get("title") or r.get("filename") or "").strip().lower()
        if title_key and title_key not in seen_titles:
            seen_titles.add(title_key)
            deduped.append(r)
        elif not title_key:
            deduped.append(r)

    results = deduped[:n]

    # ── Display ───────────────────────────────────────────────────────────────
    print(f"\n{'═'*70}")
    print(f"  ARES Content Recommendations")
    print(f"{'═'*70}")
    print(f"  Sub-strand : {substrand}")
    print(f"  Topic      : {topic}")
    print(f"  Phase      : {phase.title() if phase else 'All phases'}")
    print(f"  Subject    : {subject or 'All'}")
    print(f"{'─'*70}")

    primary = results[0]
    has_t   = bool(primary.get("transcript_path"))
    print(f"\n  ★ PRIMARY RECOMMENDATION")
    print(f"     Title    : {primary.get('title', primary['filename'])}")
    print(f"     Type     : {primary['content_type']}")
    print(f"     Module   : {primary['module']}")
    print(f"     Path     : {readable_path(primary['path'], primary['module'])}")
    if primary.get("duration_seconds"):
        mins = int(primary["duration_seconds"]) // 60
        secs = int(primary["duration_seconds"]) % 60
        print(f"     Duration : {mins}m {secs:02d}s")
    print(f"     Transcript: {'Yes ✓' if has_t else 'No'}")

    kw_base      = topic or substrand or subject
    search_terms = _generate_search_terms(kw_base, subject, phase)
    print(f"\n  SUGGESTED ARES SEARCH TERMS FOR TEACHER:")
    for term in search_terms:
        print(f"     • {term}")

    if len(results) > 1:
        print(f"\n  ALTERNATIVES:")
        for r in results[1:]:
            has_t2 = "📝" if r.get("transcript_path") else "  "
            title  = r.get("title") or r.get("filename") or r["path"].split("/")[-1]
            print(f"     {has_t2} [{r['content_type']:6}] {title[:60]}")
            print(f"            {readable_path(r['path'], r['module'])[:70]}")

    print()

    if args.json:
        output = {
            "query":        {"substrand": substrand, "topic": topic,
                             "subject": subject, "phase": phase},
            "search_terms": search_terms,
            "primary":      {k: v for k, v in primary.items()
                             if k not in ("score", "rank")},
            "alternatives": [{k: v for k, v in r.items()
                              if k not in ("score", "rank")}
                             for r in results[1:]],
        }
        print(json.dumps(output, indent=2, default=str))


def _generate_search_terms(topic: str, subject: str, phase: str) -> list:
    terms = []
    base = topic.strip() if topic else subject
    if base:
        terms.append(base)
    if subject and subject not in base:
        terms.append(f"{subject} {base}")
    if phase and phase in PHASE_BOOST_TERMS:
        for boost in PHASE_BOOST_TERMS[phase][:2]:
            terms.append(f"{base} {boost}")
    seen, unique = set(), []
    for t in terms:
        if t.lower() not in seen:
            seen.add(t.lower())
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
    for r in conn.execute(
        "SELECT content_type, COUNT(*) n FROM content GROUP BY content_type ORDER BY n DESC"
    ).fetchall():
        print(f"    {r['content_type']:<12} {r['n']:>6,}")

    print(f"\n  By subject:")
    for r in conn.execute(
        "SELECT subject, COUNT(*) n FROM content GROUP BY subject ORDER BY n DESC"
    ).fetchall():
        print(f"    {r['subject']:<24} {r['n']:>6,}")

    print(f"\n  By module:")
    for r in conn.execute(
        "SELECT name, source, content_count, video_count, pdf_count, html_count, subjects "
        "FROM modules ORDER BY content_count DESC"
    ).fetchall():
        src = f"[{r['source']}]" if r['source'] else ""
        print(f"    {r['name']:<34} {src:<10} {r['content_count']:>7,} items")
        if r['subjects']:
            print(f"      Subjects: {r['subjects']}")

    vt = conn.execute(
        "SELECT COUNT(*) FROM content WHERE content_type IN ('video','audio')"
    ).fetchone()[0]
    tr = conn.execute(
        "SELECT COUNT(*) FROM content WHERE content_type IN ('video','audio') "
        "AND transcript_path != '' AND transcript_path IS NOT NULL"
    ).fetchone()[0]
    print(f"\n  Transcript coverage: {tr}/{vt} videos ({100*tr//max(vt,1)}%)")

    ls = conn.execute(
        "SELECT started_at, files_indexed FROM scan_runs ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if ls:
        print(f"\n  Last scan: {ls['started_at']} ({ls['files_indexed']:,} files indexed)")
    print()


# ─── Modules ─────────────────────────────────────────────────────────────────

def cmd_modules(conn: sqlite3.Connection) -> None:
    rows = conn.execute("SELECT * FROM modules ORDER BY content_count DESC").fetchall()
    print(f"\n{'─'*72}")
    print(f"  {'Module':<32} {'Src':<8} {'Items':>7}  {'Video':>6}  {'PDF':>5}  {'HTML':>5}")
    print(f"{'─'*72}")
    for r in rows:
        print(f"  {r['name']:<32} {(r['source'] or ''):<8} {r['content_count']:>7,}  "
              f"{r['video_count']:>6,}  {r['pdf_count']:>5,}  {r['html_count']:>5,}")
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
        print(f"\n  Extracted text (first 500 chars):\n  {d['extracted_text'][:500]}")
    if args.text and d.get("transcript_text"):
        print(f"\n  Transcript text (first 500 chars):\n  {d['transcript_text'][:500]}")
    print()


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Query the ARES content index for lesson plan resource recommendations."
    )
    parser.add_argument("--config", "-c", default="ares_scan_config.yaml")
    subs = parser.add_subparsers(dest="command", required=True)

    p = subs.add_parser("search", help="Full-text search")
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--subject", choices=["Biology","Chemistry","Physics","Mathematics","General"])
    p.add_argument("--type", dest="type", choices=["video","audio","pdf","html","image"])
    p.add_argument("--with-transcript", action="store_true")
    p.add_argument("--n", type=int, default=10)
    p.add_argument("--verbose", "-v", action="store_true")

    p = subs.add_parser("recommend", help="Get resource recommendations")
    p.add_argument("--substrand")
    p.add_argument("--topic")
    p.add_argument("--subject", choices=["Biology","Chemistry","Physics","Mathematics"])
    p.add_argument("--phase", choices=["predict","observe","explain","dqb","model"])
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--json", action="store_true", help="Output JSON for pipeline use")

    subs.add_parser("summary", help="Index summary")
    subs.add_parser("modules", help="List modules")

    p = subs.add_parser("get", help="Inspect a single item")
    p.add_argument("--path", required=True)
    p.add_argument("--text", action="store_true")

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
