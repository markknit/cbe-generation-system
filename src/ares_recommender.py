"""
ares_recommender.py — ARES Content Recommendation Module
=========================================================
Queries the ARES content index (SQLite/FTS5) and returns resource
recommendations for lesson plan Section C Resource cells.

ARES URL patterns (confirmed from live server):

  All Kolibri/web content goes through the tracker:
    http://ares.edu/tracker/kiwix_launch.html?target=<encoded_path>

  Kolibri content item:
    target = /kolibri/en/learn/#/topics/c/<kolibri_id>

  Kolibri search:
    target = /kolibri/en/learn/#/search?query=<terms>

  Web modules:
    target = /modules/<path>

  KICD Educhannel (no tracker yet):
    http://ares.edu/KICD_Educhannel/<path>

  Kiwix: search-only — article deep-links not reliably constructable from DB.

Override host: export ARES_HOST=10.42.0.1  (or ares.local, localhost, ares.edu)
"""

import os
import re
import sqlite3
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote, quote_plus

# ---------------------------------------------------------------------------
# ARES host — ares.edu is the safest default (in hosts file on all servers)
# ---------------------------------------------------------------------------

ARES_HOST = os.environ.get("ARES_HOST", "ares.edu")

def _tracker_url(target_path: str) -> str:
    """Wrap any internal path in the ARES tracker."""
    return f"http://{ARES_HOST}/tracker/kiwix_launch.html?target={quote(target_path, safe='')}"

def _kolibri_content_url(kolibri_id: str) -> str:
    target = f"/kolibri/en/learn/#/topics/c/{kolibri_id}"
    return _tracker_url(target)

def _kolibri_search_url(terms: str) -> str:
    target = f"/kolibri/en/learn/#/search?query={quote_plus(terms)}"
    return _tracker_url(target)

def _web_url(path: str) -> str:
    target = f"/modules/{path.lstrip('/')}"
    return _tracker_url(target)

def _kicd_url(path: str) -> str:
    # No tracker yet for KICD Educhannel
    clean = path.lstrip('/')
    if not clean.startswith('KICD_Educhannel/'):
        clean = f"KICD_Educhannel/{clean}"
    return f"http://{ARES_HOST}/{clean}"

# ---------------------------------------------------------------------------
# Channel tier table
# ---------------------------------------------------------------------------

def _channel_tier(kolibri_channel: str, source: str) -> int:
    ch = (kolibri_channel or "").lower()
    tier0 = [
        "ck-12", "ck12",
        "khan academy (english",
        "mit blossoms",
        "phet",
        "ted-ed",
        "tessa",
        "kicd",
        "kenya curriculum",
    ]
    tier1 = [
        "khan academy (kiswahili",
        "khan academy",
    ]
    for pattern in tier0:
        if pattern in ch:
            return 0
    for pattern in tier1:
        if pattern in ch:
            return 1
    if source == "kiwix":
        return 1
    if source == "web":
        return 2
    return 2

# ---------------------------------------------------------------------------
# Phase keyword boosts
# ---------------------------------------------------------------------------

PHASE_BOOST = {
    "predict": ["phenomenon", "prior knowledge", "initial"],
    "observe": ["experiment", "investigation", "lab", "simulation", "practical"],
    "explain": ["explanation", "concept", "theory", "mechanism"],
    "dqb":     ["question", "inquiry"],
    "model":   ["model", "diagram", "structure"],
    "final":   ["summary", "assessment", "evidence"],
}

VIDEO_TYPES   = {"video"}
READING_TYPES = {"html", "html5", "pdf", "document", "exercise"}

# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------

@dataclass
class AresResource:
    title:          str
    channel:        str
    source:         str
    content_type:   str
    direct_url:     str
    search_url:     str
    search_terms:   str
    kolibri_id:     str = ""
    tier:           int = 2
    subject_match:  bool = False
    has_transcript: bool = False

    @property
    def is_video(self) -> bool:
        return self.content_type in VIDEO_TYPES

    @property
    def type_label(self) -> str:
        labels = {"html": "HTML", "html5": "HTML",
                  "pdf": "PDF", "exercise": "EXERCISE", "video": "VIDEO"}
        return labels.get(self.content_type, self.content_type.upper())

    @property
    def display_source(self) -> str:
        return self.channel if self.channel else self.source

# ---------------------------------------------------------------------------
# Search term builders — video and reading get different terms
# ---------------------------------------------------------------------------

def _make_search_terms(substrand: str, topic: str, phase: str,
                       content_kind: str = "") -> str:
    """
    Build a short, deduplicated search string.
    content_kind: 'video' | 'reading' | '' — biases the trailing qualifier.
    """
    stop = {
        "with", "that", "this", "from", "have", "been", "their",
        "which", "also", "into", "about", "what", "study", "lesson",
        "introduction", "overview",
    }
    words = re.findall(r"[A-Za-z]{4,}", f"{topic} {substrand}")
    seen: set[str] = set()
    clean: list[str] = []
    for w in words:
        wl = w.lower()
        if wl not in stop and wl not in seen:
            seen.add(wl)
            clean.append(w)

    base = clean[:4]

    if content_kind == "video":
        qualifier = "video"
    elif content_kind == "reading":
        qualifier = "notes"
    else:
        qualifier = ""

    if qualifier and qualifier.lower() not in {w.lower() for w in base}:
        base.append(qualifier)

    return " ".join(base[:5])

# ---------------------------------------------------------------------------
# Recommender
# ---------------------------------------------------------------------------

class AresRecommender:

    def __init__(self, db_path: str):
        self.db_path = str(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        self._ready = False
        self._init_db()

    def _init_db(self):
        try:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("SELECT id FROM content LIMIT 1")
            self._ready = True
        except Exception as e:
            print(f"[AresRecommender] WARNING: cannot open DB: {e}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def recommend_pair(
        self,
        substrand: str,
        topic: str,
        subject: str = "",
        phase: str = "observe",
        n_candidates: int = 60,
    ) -> tuple[Optional[AresResource], Optional[AresResource]]:
        if not self._ready:
            return None, None
        candidates = self._search(substrand, topic, subject, phase,
                                  n=n_candidates)
        videos   = [c for c in candidates if c.is_video]
        readings = [c for c in candidates if not c.is_video]

        best_video   = videos[0]   if videos   else None
        best_reading = readings[0] if readings else None

        # Assign distinct search terms and URLs per content kind
        video_terms   = _make_search_terms(substrand, topic, phase, "video")
        reading_terms = _make_search_terms(substrand, topic, phase, "reading")

        if best_video:
            best_video.search_terms = video_terms
            best_video.search_url   = _kolibri_search_url(video_terms)
        if best_reading:
            best_reading.search_terms = reading_terms
            best_reading.search_url   = _kolibri_search_url(reading_terms)

        return best_video, best_reading

    def recommend_all_phases(
        self,
        substrand: str,
        lesson_topic: str,
        subject: str = "",
    ) -> dict:
        return {
            phase: self.recommend_pair(substrand, lesson_topic, subject, phase)
            for phase in ("predict", "observe", "explain", "dqb", "model")
        }

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def _keywords(self, substrand: str, topic: str, phase: str) -> list[str]:
        stop = {
            "and","or","the","a","an","of","in","to","for","with","on","at",
            "from","by","is","are","how","does","what","why","do","be",
            "this","that","its","their","which","have","has","study","lesson",
        }
        raw = f"{topic} {substrand} {' '.join(PHASE_BOOST.get(phase.lower(), []))}"
        words = re.findall(r"[a-zA-Z]{3,}", raw.lower())
        seen: set[str] = set()
        result = []
        for w in words:
            if w not in stop and w not in seen:
                seen.add(w)
                result.append(w)
        return result

    def _build_direct_url(self, source: str, kid: str, path: str) -> str:
        """Construct the correct tracked URL for this content item."""
        if source == "kolibri" and kid:
            return _kolibri_content_url(kid)
        elif source == "web" and path:
            if path.startswith("KICD_Educhannel/"):
                return _kicd_url(path)
            return _web_url(path)
        # kiwix — no reliable article deep-link
        return ""

    def _search(
        self,
        substrand: str,
        topic: str,
        subject: str,
        phase: str,
        n: int = 60,
    ) -> list[AresResource]:
        keywords = self._keywords(substrand, topic, phase)
        if not keywords:
            return []

        # Placeholder — overwritten per-kind in recommend_pair()
        search_terms = _make_search_terms(substrand, topic, phase)
        search_url   = _kolibri_search_url(search_terms)
        subj_lower   = subject.lower()

        hit_counts: dict[int, int] = {}
        rows_by_id:  dict[int, sqlite3.Row] = {}
        cur = self._conn.cursor()

        for kw in keywords:
            try:
                cur.execute(
                    """
                    SELECT c.id,
                           c.title,
                           c.source,
                           c.content_type,
                           c.kolibri_kind,
                           c.subject,
                           c.path,
                           c.kolibri_id,
                           c.kolibri_channel,
                           c.transcript_path
                    FROM content_fts f
                    JOIN content c ON c.id = f.rowid
                    WHERE content_fts MATCH ?
                    AND c.content_type NOT IN ('topic')
                    LIMIT 80
                    """,
                    (kw,),
                )
                for row in cur.fetchall():
                    rid = row["id"]
                    hit_counts[rid] = hit_counts.get(rid, 0) + 1
                    rows_by_id[rid] = row
            except sqlite3.OperationalError as e:
                print(f"[AresRecommender] FTS error on '{kw}': {e}")

        if not rows_by_id:
            return []

        resources: list[AresResource] = []

        for rid, row in rows_by_id.items():
            src     = str(row["source"] or "")
            ctype   = str(row["content_type"] or row["kolibri_kind"] or "unknown").lower()
            kid     = str(row["kolibri_id"] or "")
            path    = str(row["path"] or "")
            channel = str(row["kolibri_channel"] or "")

            direct_url    = self._build_direct_url(src, kid, path)
            tier          = _channel_tier(channel, src)
            subject_match = subj_lower in str(row["subject"] or "").lower()

            resources.append(AresResource(
                title=str(row["title"] or "Untitled"),
                channel=channel,
                source=src,
                content_type=ctype,
                direct_url=direct_url,
                search_url=search_url,
                search_terms=search_terms,
                kolibri_id=kid,
                tier=tier,
                subject_match=subject_match,
                has_transcript=bool(row["transcript_path"]),
            ))

        resources.sort(key=lambda r: (
            r.tier,
            0 if r.subject_match else 1,
            0 if r.direct_url else 1,
            -hit_counts.get(r.kolibri_id, 0),
        ))

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

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):  return self
    def __exit__(self, *_): self.close()

# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_resource_cell(
    video: Optional[AresResource],
    reading: Optional[AresResource],
) -> str:
    """Plain-text output for CLI testing."""
    parts = []
    fallback = _kolibri_search_url("biology")

    if video:
        parts.append(
            f"📹 VIDEO: {video.title}\n"
            f"   Source: {video.display_source}\n"
            f"   Link:   {video.direct_url or '(no direct link)'}\n"
            f"   Search: {video.search_url}\n"
            f"   Terms:  \"{video.search_terms}\""
        )
    else:
        parts.append(f"📹 VIDEO: None found.\n   Search: {fallback}")

    if reading:
        parts.append(
            f"📖 {reading.type_label}: {reading.title}\n"
            f"   Source: {reading.display_source}\n"
            f"   Link:   {reading.direct_url or '(no direct link — use search)'}\n"
            f"   Search: {reading.search_url}\n"
            f"   Terms:  \"{reading.search_terms}\""
        )
    else:
        parts.append(f"📖 READING: None found.\n   Search: {fallback}")

    return "\n\n".join(parts)


def format_resource_cell_structured(
    video: Optional[AresResource],
    reading: Optional[AresResource],
    search_terms: str = "",
) -> dict:
    """Structured dict consumed by aresResources.js."""
    fallback_search_url = _kolibri_search_url(search_terms or "biology")

    def _to_dict(r: Optional[AresResource]) -> Optional[dict]:
        if r is None:
            return None
        return {
            "title":          r.title,
            "source":         r.display_source,
            "content_type":   r.content_type,
            "direct_url":     r.direct_url,
            "search_url":     r.search_url,
            "search_terms":   r.search_terms,
            "has_transcript": r.has_transcript,
            "tier":           r.tier,
        }

    return {
        "video":               _to_dict(video),
        "reading":             _to_dict(reading),
        "fallback_search_url": fallback_search_url,
    }

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli():
    import argparse, json

    parser = argparse.ArgumentParser(description="ARES resource recommender")
    parser.add_argument("--db",         required=True)
    parser.add_argument("--substrand",  required=True)
    parser.add_argument("--topic",      required=True)
    parser.add_argument("--subject",    default="")
    parser.add_argument("--phase",      default="observe",
                        choices=["predict","observe","explain","dqb","model","final"])
    parser.add_argument("--all-phases", action="store_true")
    parser.add_argument("--text",       action="store_true")
    args = parser.parse_args()

    with AresRecommender(args.db) as rec:
        if args.all_phases:
            all_recs = rec.recommend_all_phases(
                args.substrand, args.topic, args.subject)
            if args.text:
                for phase, (v, r) in all_recs.items():
                    print(f"\n{'='*60}\n{phase.upper()}\n{'='*60}")
                    print(format_resource_cell(v, r))
            else:
                output = {
                    phase: format_resource_cell_structured(v, r, args.topic)
                    for phase, (v, r) in all_recs.items()
                }
                print(json.dumps(output, indent=2))
        else:
            video, reading = rec.recommend_pair(
                args.substrand, args.topic, args.subject, args.phase)
            if args.text:
                print(format_resource_cell(video, reading))
            else:
                print(json.dumps(
                    format_resource_cell_structured(video, reading, args.topic),
                    indent=2))

if __name__ == "__main__":
    _cli()
