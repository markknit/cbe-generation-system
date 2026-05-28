"""
ares_recommender.py — ARES Content Recommendation Module
=========================================================
Queries the ARES content index (SQLite, FTS5) directly to find the best
video and non-video resources for each lesson phase.

Usage (standalone test):
    python3 ares_recommender.py \
        --db /home/markk/ares/cbe-generation-system/data/ares_index/ares_content.db \
        --substrand "Cell Structure and Specialisation" \
        --topic "organelles electron microscope" \
        --subject Biology \
        --phase observe

Usage (as module):
    from src.ares_recommender import AresRecommender, format_resource_cell

    rec = AresRecommender(db_path)
    video, reading = rec.recommend_pair(
        substrand="Cell Structure and Specialisation",
        topic="organelles electron microscope",
        subject="Biology",
        phase="observe",
    )
    cell_text = format_resource_cell(video, reading)
"""

import sqlite3
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Tier 0 = highest-quality curated sources; Tier 1 = encyclopaedia;
# Tier 2 = general ARES web content.  Lower tier number = preferred.
TIER_0_SOURCES = {
    "KICD Educhannel", "Khan Academy", "MIT Blossoms", "PhET",
    "TED-Ed", "CK-12", "TESSA", "Kenya Curriculum Tools",
}

# Extra keywords injected per phase to bias retrieval toward phase-appropriate content
PHASE_BOOST = {
    "predict":       ["prediction", "prior knowledge", "initial ideas", "phenomenon", "observe"],
    "observe":       ["experiment", "investigation", "lab", "video", "simulation", "activity"],
    "explain":       ["explanation", "concept", "theory", "mechanism", "how does"],
    "dqb":           ["question", "inquiry", "driving question", "wonder"],
    "model":         ["model", "diagram", "drawing", "build", "represent"],
    "final":         ["summary", "explain", "assessment", "evidence"],
}

# Content types treated as video
VIDEO_TYPES = {"video", "youtube", "mp4", "webm"}

# Content types treated as readable (non-video)
READING_TYPES = {"article", "pdf", "html", "webpage", "document", "text",
                 "ebook", "epub", "slideshow", "worksheet"}


# ---------------------------------------------------------------------------
# Data class for a single recommendation
# ---------------------------------------------------------------------------

@dataclass
class AresResource:
    title: str
    source: str                     # e.g. "Khan Academy", "CK-12"
    content_type: str               # e.g. "video", "article"
    ares_path: str                  # path on ARES server/device
    search_terms: str               # suggested search string for teacher
    tier: int = 2                   # 0 = premium, 1 = wiki, 2 = general
    subject_match: bool = False
    has_transcript: bool = False
    snippet: str = ""               # short text excerpt (from FTS snippet)

    @property
    def is_video(self) -> bool:
        return self.content_type.lower() in VIDEO_TYPES

    @property
    def emoji(self) -> str:
        return "📹" if self.is_video else "📖"


# ---------------------------------------------------------------------------
# Main recommender class
# ---------------------------------------------------------------------------

class AresRecommender:
    """
    Query the ARES SQLite content index for lesson resource recommendations.

    The DB is expected to have:
      - A table (or FTS virtual table) called `content` or `content_fts`
      - Columns: id, title, source, content_type, subject, path,
                 has_transcript, kolibri_checksum (nullable)

    Column names are detected at init time so the module works even if
    the schema was slightly renamed during indexing.
    """

    # Fallback column name aliases — map canonical name → possible DB names
    _COLUMN_ALIASES = {
        "id":              ["id", "rowid"],
        "title":           ["title", "name"],
        "source":          ["source", "module", "channel_name"],
        "content_type":    ["content_type", "type", "kind"],
        "subject":         ["subject", "subjects", "topic_subject"],
        "path":            ["path", "file_path", "url", "ares_path"],
        "has_transcript":  ["has_transcript", "transcript", "transcribed"],
    }

    def __init__(self, db_path: str):
        self.db_path = str(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        self._table: str = "content"
        self._fts_table: Optional[str] = None
        self._col: dict = {}          # canonical → actual column name
        self._ready = False
        self._init_db()

    # ------------------------------------------------------------------
    # DB setup
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        try:
            self._conn = self._connect()
            self._detect_schema()
            self._ready = True
        except Exception as e:
            print(f"[AresRecommender] WARNING: could not init DB at {self.db_path}: {e}")
            self._ready = False

    def _detect_schema(self):
        cur = self._conn.cursor()

        # Find main content table
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cur.fetchall()}

        for candidate in ("content", "ares_content", "items", "resources"):
            if candidate in tables:
                self._table = candidate
                break

        # Find FTS5 table (for full-text search)
        for t in tables:
            if "fts" in t.lower():
                self._fts_table = t
                break

        # Detect actual column names
        cur.execute(f"PRAGMA table_info({self._table})")
        actual_cols = {row["name"].lower() for row in cur.fetchall()}

        for canonical, aliases in self._COLUMN_ALIASES.items():
            for alias in aliases:
                if alias in actual_cols:
                    self._col[canonical] = alias
                    break
            if canonical not in self._col:
                # Use canonical name as fallback — query will fail gracefully
                self._col[canonical] = canonical

    # ------------------------------------------------------------------
    # Core recommendation logic
    # ------------------------------------------------------------------

    def recommend_pair(
        self,
        substrand: str,
        topic: str,
        subject: str = "",
        phase: str = "observe",
        n_candidates: int = 30,
    ) -> tuple[Optional[AresResource], Optional[AresResource]]:
        """
        Return (best_video, best_reading) for this lesson phase.
        Either may be None if no suitable content is found.
        """
        if not self._ready:
            return None, None

        candidates = self._search(substrand, topic, subject, phase, n=n_candidates)
        videos   = [c for c in candidates if c.is_video]
        readings = [c for c in candidates if not c.is_video]

        best_video   = videos[0]   if videos   else None
        best_reading = readings[0] if readings else None
        return best_video, best_reading

    def recommend_all_phases(
        self,
        substrand: str,
        lesson_topic: str,
        subject: str = "",
    ) -> dict[str, tuple[Optional[AresResource], Optional[AresResource]]]:
        """
        Return recommendations for all 5 lesson phases at once.
        Returns dict keyed by phase name.
        """
        results = {}
        for phase in ("predict", "observe", "explain", "dqb", "model"):
            results[phase] = self.recommend_pair(
                substrand=substrand,
                topic=lesson_topic,
                subject=subject,
                phase=phase,
            )
        return results

    # ------------------------------------------------------------------
    # Internal search
    # ------------------------------------------------------------------

    def _build_keywords(self, substrand: str, topic: str, phase: str) -> list[str]:
        """Extract individual search keywords from the inputs."""
        # Combine all input text
        raw = f"{substrand} {topic} {' '.join(PHASE_BOOST.get(phase.lower(), []))}"

        # Remove common stop words and split
        stop = {
            "and", "or", "the", "a", "an", "of", "in", "to", "for",
            "with", "on", "at", "from", "by", "is", "are", "how", "does",
            "what", "why", "do", "be", "this", "that",
        }
        words = re.findall(r"[a-zA-Z]{3,}", raw.lower())
        keywords = [w for w in words if w not in stop]

        # De-duplicate while preserving order
        seen: set[str] = set()
        unique = []
        for w in keywords:
            if w not in seen:
                seen.add(w)
                unique.append(w)
        return unique

    def _search(
        self,
        substrand: str,
        topic: str,
        subject: str,
        phase: str,
        n: int = 30,
    ) -> list[AresResource]:
        """
        Multi-keyword FTS search with score aggregation and ranking.
        Falls back to LIKE search if FTS is unavailable.
        """
        keywords = self._build_keywords(substrand, topic, phase)
        if not keywords:
            return []

        # Accumulate hit counts per row id
        hit_counts: dict[int, int] = {}
        rows_by_id: dict[int, sqlite3.Row] = {}

        cur = self._conn.cursor()
        c = self._col  # shorthand

        if self._fts_table:
            for kw in keywords:
                try:
                    cur.execute(
                        f"""
                        SELECT m.rowid,
                               m.{c['title']},
                               m.{c['source']},
                               m.{c['content_type']},
                               m.{c['subject']},
                               m.{c['path']},
                               m.{c['has_transcript']},
                               snippet({self._fts_table}, 0, '<', '>', '...', 20) AS snippet
                        FROM {self._fts_table} f
                        JOIN {self._table} m ON m.rowid = f.rowid
                        WHERE {self._fts_table} MATCH ?
                        LIMIT 50
                        """,
                        (kw,),
                    )
                    for row in cur.fetchall():
                        rid = row["rowid"]
                        hit_counts[rid] = hit_counts.get(rid, 0) + 1
                        rows_by_id[rid] = row
                except sqlite3.OperationalError:
                    # FTS table schema mismatch — fall through to LIKE
                    self._fts_table = None
                    break

        if not self._fts_table:
            # Plain LIKE fallback
            for kw in keywords[:6]:   # limit to avoid very slow queries
                like = f"%{kw}%"
                try:
                    cur.execute(
                        f"""
                        SELECT rowid,
                               {c['title']},
                               {c['source']},
                               {c['content_type']},
                               {c['subject']},
                               {c['path']},
                               {c['has_transcript']},
                               '' AS snippet
                        FROM {self._table}
                        WHERE lower({c['title']}) LIKE lower(?)
                           OR lower({c['subject']}) LIKE lower(?)
                        LIMIT 50
                        """,
                        (like, like),
                    )
                    for row in cur.fetchall():
                        rid = row["rowid"]
                        hit_counts[rid] = hit_counts.get(rid, 0) + 1
                        rows_by_id[rid] = row
                except sqlite3.OperationalError as e:
                    print(f"[AresRecommender] Search error: {e}")

        if not rows_by_id:
            return []

        # Build resource objects and rank
        resources: list[AresResource] = []
        subj_lower = subject.lower()

        for rid, row in rows_by_id.items():
            src = str(row[c["source"]] or "")
            tier = 0 if src in TIER_0_SOURCES else (1 if "wikipedia" in src.lower() else 2)

            resources.append(AresResource(
                title=str(row[c["title"]] or "Untitled"),
                source=src,
                content_type=str(row[c["content_type"]] or "unknown").lower(),
                ares_path=str(row[c["path"]] or ""),
                search_terms=self._make_search_terms(substrand, topic, phase),
                tier=tier,
                subject_match=subj_lower in str(row[c["subject"]] or "").lower(),
                has_transcript=bool(row[c["has_transcript"]]),
                snippet=str(row.get("snippet", "") or ""),
            ))

        # Sort: tier → subject match → hit count (desc)
        resources.sort(key=lambda r: (
            r.tier,
            0 if r.subject_match else 1,
            -hit_counts.get(list(rows_by_id.keys())[
                next(i for i, (rid2, _) in enumerate(rows_by_id.items()) if rid2 == id(r))
            ], 0) if False else 0,   # hit count handled below via separate sort key
        ))

        # Re-sort cleanly with hit count
        id_to_hits = {id(r): hit_counts.get(
            next((rid for rid, row in rows_by_id.items()
                  if str(row[c["title"]] or "") == r.title), 0), 0
        ) for r in resources}

        resources.sort(key=lambda r: (
            r.tier,
            0 if r.subject_match else 1,
            -id_to_hits.get(id(r), 0),
        ))

        # Deduplicate by normalised title
        seen_titles: set[str] = set()
        unique: list[AresResource] = []
        for r in resources:
            norm = re.sub(r"[^a-z0-9]", "", r.title.lower())
            if norm not in seen_titles:
                seen_titles.add(norm)
                unique.append(r)
            if len(unique) >= n:
                break

        return unique

    @staticmethod
    def _make_search_terms(substrand: str, topic: str, phase: str) -> str:
        """Generate a short ARES search string a teacher could type."""
        words = re.findall(r"[A-Za-z]{4,}", f"{topic} {substrand}")
        phase_hint = PHASE_BOOST.get(phase.lower(), [])
        combined = words[:3] + phase_hint[:1]
        return " ".join(combined)

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


# ---------------------------------------------------------------------------
# Formatting helpers (used by JS generator bridge)
# ---------------------------------------------------------------------------

def format_resource_cell(
    video: Optional[AresResource],
    reading: Optional[AresResource],
    include_path: bool = False,
) -> str:
    """
    Format a pair of recommendations as plain text for the Resource column
    of Section C.  Returns a multi-line string suitable for inserting into
    a docx paragraph sequence.

    Example output:
        📹 VIDEO: Organelles in Eukaryotic Cells
           Source: Khan Academy
           ARES search: "organelles electron microscope"

        📖 READING: Cell Organelles
           Source: CK-12 Flexbook
           ARES search: "cell organelles CK-12"
    """
    parts = []

    if video:
        line = f"📹 VIDEO: {video.title}"
        line += f"\n   Source: {video.source}" if video.source else ""
        line += f'\n   ARES search: "{video.search_terms}"'
        if include_path and video.ares_path:
            line += f"\n   Path: {video.ares_path}"
        parts.append(line)
    else:
        parts.append("📹 VIDEO: No video recommendation found for this phase.\n   Try: Khan Academy or KICD Educhannel on ARES.")

    if reading:
        line = f"📖 READING: {reading.title}"
        line += f"\n   Source: {reading.source}" if reading.source else ""
        line += f'\n   ARES search: "{reading.search_terms}"'
        if include_path and reading.ares_path:
            line += f"\n   Path: {reading.ares_path}"
        parts.append(line)
    else:
        parts.append("📖 READING: No reading recommendation found.\n   Try: CK-12 or Wikipedia on ARES.")

    return "\n\n".join(parts)


def format_resource_cell_structured(
    video: Optional[AresResource],
    reading: Optional[AresResource],
) -> dict:
    """
    Return a structured dict for use by the JS generator (via JSON bridge).
    The JS generator reads this and builds docx paragraph objects.

    Schema:
    {
      "video": {
        "title": str,
        "source": str,
        "search_terms": str,
        "has_transcript": bool
      } | null,
      "reading": {
        "title": str,
        "source": str,
        "search_terms": str
      } | null
    }
    """
    def _to_dict(r: Optional[AresResource]) -> Optional[dict]:
        if r is None:
            return None
        return {
            "title": r.title,
            "source": r.source,
            "search_terms": r.search_terms,
            "has_transcript": r.has_transcript,
            "content_type": r.content_type,
            "tier": r.tier,
        }

    return {
        "video": _to_dict(video),
        "reading": _to_dict(reading),
    }


# ---------------------------------------------------------------------------
# JSON bridge — called by JS generator via child_process.execSync
# ---------------------------------------------------------------------------

def _cli_recommend():
    """
    CLI entry point used by the JS generator bridge.
    Outputs a single JSON object to stdout.
    """
    import argparse, json

    parser = argparse.ArgumentParser(description="ARES resource recommender")
    parser.add_argument("--db", required=True, help="Path to ares_content.db")
    parser.add_argument("--substrand", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--subject", default="")
    parser.add_argument("--phase", default="observe",
                        choices=["predict", "observe", "explain", "dqb", "model", "final"])
    parser.add_argument("--all-phases", action="store_true",
                        help="Return recommendations for all 5 phases at once")
    parser.add_argument("--json", action="store_true", default=True,
                        help="Output JSON (default)")
    parser.add_argument("--text", action="store_true",
                        help="Output human-readable text instead of JSON")
    args = parser.parse_args()

    with AresRecommender(args.db) as rec:
        if args.all_phases:
            all_recs = rec.recommend_all_phases(
                substrand=args.substrand,
                lesson_topic=args.topic,
                subject=args.subject,
            )
            output = {
                phase: format_resource_cell_structured(v, r)
                for phase, (v, r) in all_recs.items()
            }
        else:
            video, reading = rec.recommend_pair(
                substrand=args.substrand,
                topic=args.topic,
                subject=args.subject,
                phase=args.phase,
            )
            if args.text:
                print(format_resource_cell(video, reading))
                return
            output = format_resource_cell_structured(video, reading)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    _cli_recommend()
