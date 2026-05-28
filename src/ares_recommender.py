"""
ares_recommender.py — ARES Content Recommendation Module
=========================================================
Confirmed URL patterns from live ares.edu server:

  Kolibri content (direct, no tracker):
    http://ares.edu/kolibri/en/learn/#/topics/c/<kolibri_id>

  Kiwix content (via tracker, article path not constructable from DB):
    http://ares.edu/tracker/kiwix_launch.html?target=/kiwix/<zimname>/...
    → search-only for kiwix

  Web modules (via tracker):
    http://ares.edu/tracker/kiwix_launch.html?target=/modules/<path>

  KICD Educhannel (direct, no tracker):
    http://ares.edu/KICD_Educhannel/<path>

  ARES-wide search (used for ALL search links):
    http://ares.edu/www2/search.php?searchstring=<terms>&sources[]=kha&...

Override host: export ARES_HOST=10.42.0.1
"""

import os
import re
import sqlite3
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote, quote_plus

# ---------------------------------------------------------------------------
# ARES host
# ---------------------------------------------------------------------------

ARES_HOST = os.environ.get("ARES_HOST", "ares.edu")

# All content sources included in the ARES-wide search
_SEARCH_SOURCES = (
    "kha", "kicd", "khak", "wiki", "wikig", "wikih", "wikiSp", "wikiq",
    "wikic", "wikip", "wikia", "wikim", "ted", "ted11", "tedin",
    "g4st", "g4e", "g5st", "g5e", "dlc", "bg", "te", "phet", "mg",
    "gdl", "ck12", "tess", "uk", "kol", "edu", "sea", "bound", "cbc",
)

def _ares_search_url(terms: str) -> str:
    """ARES-wide search — works across all modules on the server."""
    base = f"http://{ARES_HOST}/www2/search.php"
    sources = "".join(f"&sources[]={s}" for s in _SEARCH_SOURCES)
    return f"{base}?searchstring={quote_plus(terms)}{sources}"

def _kolibri_content_url(kolibri_id: str, is_storage: bool = False) -> str:
    """
    Direct Kolibri content link via port 8069.
    kolibri_storage IDs are confirmed correct.
    channel_db IDs may differ on live server — link provided as best-effort;
    name-search fallback always shown alongside.
    """
    return f"http://{ARES_HOST}:8069/en/learn/#/topics/c/{kolibri_id}"

def _kiwix_url(db_path: str) -> str:
    """
    Kiwix article via tracker.
    DB path format: '<zimfile>.zim::A/<Article_Title>'
    Tracker target: /kiwix/<zimfile_without_ext>/A/<Article_Title>
    """
    if "::" not in db_path:
        return ""
    zim_part, article_path = db_path.split("::", 1)
    zim_name = zim_part.replace(".zim", "")
    target = f"/kiwix/{zim_name}/{article_path}"
    return f"http://{ARES_HOST}/tracker/kiwix_launch.html?target={quote(target, safe='/')}"

def _web_url(path: str) -> str:
    """Web module via tracker."""
    target = f"/modules/{path.lstrip('/')}"
    return f"http://{ARES_HOST}/tracker/kiwix_launch.html?target={quote(target, safe='/')}"

def _kicd_url(path: str) -> str:
    """KICD Educhannel — direct, no tracker."""
    clean = path.lstrip('/')
    if not clean.startswith('KICD_Educhannel/'):
        clean = f"KICD_Educhannel/{clean}"
    return f"http://{ARES_HOST}/{clean}"

# ---------------------------------------------------------------------------
# Channel tier
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
    for p in tier0:
        if p in ch:
            return 0
    for p in tier1:
        if p in ch:
            return 1
    if source == "kiwix":
        return 1
    if source == "web":
        return 2
    return 2

def _reading_tier(channel: str, source: str, content_type: str) -> int:
    ch = (channel or "").lower()
    base = _channel_tier(channel, source)
    if content_type in ("html", "html5", "exercise"):
        if "phet" in ch or "mit blossoms" in ch:
            return base + 1
    return base

# ---------------------------------------------------------------------------
# Phase boosts
# ---------------------------------------------------------------------------

PHASE_BOOST = {
    "predict": ["phenomenon", "prior knowledge", "initial"],
    "observe": ["experiment", "investigation", "lab", "simulation", "practical"],
    "explain": ["explanation", "concept", "theory", "mechanism"],
    "dqb":     ["question", "inquiry"],
    "model":   ["model", "diagram", "structure"],
    "final":   ["summary", "assessment", "evidence"],
}

VIDEO_TYPES = {"video"}

# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------

@dataclass
class AresResource:
    title:          str
    channel:        str
    source:         str
    content_type:   str
    direct_url:       str    # empty string if not linkable
    search_url:       str    # ARES-wide general topic search URL
    search_terms:     str    # general topic search terms
    exact_search_url: str = ""  # ARES search for exact resource title
    kolibri_id:     str = ""
    tier:           int = 2
    subject_match:  bool = False
    has_transcript: bool = False
    is_storage:     bool = False   # True = kolibri_storage path (IDs match live server)

    @property
    def is_video(self) -> bool:
        return self.content_type in VIDEO_TYPES

    @property
    def type_label(self) -> str:
        return {
            "html": "HTML", "html5": "HTML", "pdf": "PDF",
            "exercise": "EXERCISE", "video": "VIDEO",
        }.get(self.content_type, self.content_type.upper())

    @property
    def display_source(self) -> str:
        return self.channel if self.channel else self.source

# ---------------------------------------------------------------------------
# Search term builder — stem-based dedup, distinct per content kind
# ---------------------------------------------------------------------------

def _make_search_terms(substrand: str, topic: str, phase: str,
                       content_kind: str = "") -> str:
    stop = {
        "with", "that", "this", "from", "have", "been", "their", "which",
        "also", "into", "about", "what", "study", "lesson", "introduction",
        "overview", "phenomenon", "salamander", "trade", "handmade",
        "factory", "tools", "connecting", "preparing", "observing",
    }
    words = re.findall(r"[A-Za-z]{4,}", f"{topic} {substrand}")
    seen_stems: set[str] = set()
    clean: list[str] = []
    for w in words:
        wl = w.lower()
        stem = re.sub(r"(tion|ing|es|s)$", "", wl)
        if wl not in stop and stem not in seen_stems:
            seen_stems.add(stem)
            clean.append(w)

    base = clean[:4]

    qualifier = "video" if content_kind == "video" else \
                "notes" if content_kind == "reading" else ""
    if qualifier:
        qual_stem = re.sub(r"(tion|ing|es|s)$", "", qualifier)
        if qual_stem not in seen_stems:
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
            print(f"[AresRecommender] WARNING: {e}")

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
        candidates = self._search(substrand, topic, subject, phase, n=n_candidates)
        videos   = [c for c in candidates if c.is_video]
        readings = [c for c in candidates if not c.is_video]

        best_video   = videos[0]   if videos   else None
        best_reading = readings[0] if readings else None

        # Assign distinct search terms and ARES-wide search URLs per kind
        for kind, resource in (("video", best_video), ("reading", best_reading)):
            if resource:
                terms = _make_search_terms(substrand, topic, phase, kind)
                resource.search_terms     = terms
                resource.search_url       = _ares_search_url(terms)
                resource.exact_search_url = _ares_search_url(resource.title)

        return best_video, best_reading

    def recommend_all_phases(
        self, substrand: str, lesson_topic: str, subject: str = ""
    ) -> dict:
        return {
            phase: self.recommend_pair(substrand, lesson_topic, subject, phase)
            for phase in ("predict", "observe", "explain", "dqb", "model")
        }

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
        if source == "kolibri" and kid:
            is_storage = path.startswith("kolibri_storage/")
            return _kolibri_content_url(kid, is_storage)
        if source == "kiwix" and path and "::" in path:
            return _kiwix_url(path)
        if source == "web" and path:
            if path.startswith("KICD_Educhannel/"):
                return _kicd_url(path)
            return _web_url(path)
        return ""

    def _search(
        self, substrand: str, topic: str, subject: str,
        phase: str, n: int = 60,
    ) -> list[AresResource]:
        keywords = self._keywords(substrand, topic, phase)
        if not keywords:
            return []

        hit_counts: dict[int, int] = {}
        rows_by_id: dict[int, sqlite3.Row] = {}
        cur = self._conn.cursor()

        for kw in keywords:
            try:
                cur.execute(
                    """
                    SELECT c.id, c.title AS title, c.source, c.content_type,
                           c.kolibri_kind, c.subject, c.path,
                           c.kolibri_id, c.kolibri_channel, c.transcript_path
                    FROM content c
                    JOIN content_fts f ON f.rowid = c.id
                    WHERE content_fts MATCH ?
                    AND c.content_type NOT IN ('topic')
                    LIMIT 150
                    """,
                    (kw,),
                )
                for row in cur.fetchall():
                    rid = row["id"]
                    hit_counts[rid] = hit_counts.get(rid, 0) + 1
                    rows_by_id[rid] = row
            except sqlite3.OperationalError as e:
                print(f"[AresRecommender] FTS error: {e}")

        if not rows_by_id:
            return []

        subj_lower = subject.lower()
        # placeholder — overwritten per-kind in recommend_pair()
        placeholder_terms = _make_search_terms(substrand, topic, phase)
        placeholder_url   = _ares_search_url(placeholder_terms)

        resources: list[AresResource] = []
        for rid, row in rows_by_id.items():
            src     = str(row["source"] or "")
            ctype   = str(row["content_type"] or row["kolibri_kind"] or "unknown").lower()
            kid     = str(row["kolibri_id"] or "")
            path    = str(row["path"] or "")
            channel = str(row["kolibri_channel"] or "")

            is_storage = (src == "kolibri" and path.startswith("kolibri_storage/"))
            resources.append(AresResource(
                title=str(row["title"] or "Untitled"),
                channel=channel,
                source=src,
                content_type=ctype,
                direct_url=self._build_direct_url(src, kid, path),
                search_url=placeholder_url,
                search_terms=placeholder_terms,
                kolibri_id=kid,
                tier=_channel_tier(channel, src) if ctype == "video" else _reading_tier(channel, src, ctype),
                subject_match=subj_lower in str(row["subject"] or "").lower(),
                has_transcript=bool(row["transcript_path"]),
                is_storage=is_storage,
            ))

        # Sort: is_storage first (correct IDs), then tier, then subject match
        # For readings: prefer html/pdf over exercises
        TYPE_PREF = {"video": 0, "html": 0, "html5": 0, "pdf": 0,
                     "document": 0, "exercise": 1}
        resources.sort(key=lambda r: (
            r.tier,
            0 if r.is_storage else 1,
            0 if r.direct_url else 1,
            0 if r.subject_match else 1,
            TYPE_PREF.get(r.content_type, 1),
            -hit_counts.get(r.kolibri_id, 0),
        ))

        # Deduplicate videos and readings separately so HTML isn't crowded out
        # by kolibri_storage videos that share the same title
        seen_video: set[str] = set()
        seen_reading: set[str] = set()
        unique_video: list[AresResource] = []
        unique_reading: list[AresResource] = []

        for r in resources:
            norm = re.sub(r"[^a-z0-9]", "", r.title.lower())
            if r.is_video:
                if norm not in seen_video:
                    seen_video.add(norm)
                    unique_video.append(r)
            else:
                if norm not in seen_reading:
                    seen_reading.add(norm)
                    unique_reading.append(r)
            if len(unique_video) >= n and len(unique_reading) >= n:
                break

        # Interleave: return combined list, videos first then readings
        # recommend_pair() will split them back out
        return unique_video[:n] + unique_reading[:n]

    def close(self):
        if self._conn:
            self._conn.close()
    def __enter__(self): return self
    def __exit__(self, *_): self.close()

# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_resource_cell(
    video: Optional[AresResource],
    reading: Optional[AresResource],
) -> str:
    fallback = _ares_search_url("biology")
    parts = []

    if video:
        link_line = f"   Link:   {video.direct_url}" if video.direct_url else                     f"   Link:   {video.exact_search_url}  (search by name)"
        parts.append(
            f"📹 VIDEO: {video.title}\n"
            f"   Source: {video.display_source}\n"
            f"{link_line}\n"
            f"   Search (name):  {video.exact_search_url}\n"
            f"   Search (topic): {video.search_url}\n"
            f"   Terms:  \"{video.search_terms}\""
        )
    else:
        parts.append(f"📹 VIDEO: None found.\n   Search: {fallback}")

    if reading:
        link_line = f"   Link:   {reading.direct_url}" if reading.direct_url else                     f"   Link:   {reading.exact_search_url}  (search by name)"
        parts.append(
            f"📖 {reading.type_label}: {reading.title}\n"
            f"   Source: {reading.display_source}\n"
            f"{link_line}\n"
            f"   Search (name):  {reading.exact_search_url}\n"
            f"   Search (topic): {reading.search_url}\n"
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
    fallback = _ares_search_url(search_terms or "biology")

    def _to_dict(r: Optional[AresResource]) -> Optional[dict]:
        if r is None:
            return None
        return {
            "title":            r.title,
            "source":           r.display_source,
            "content_type":     r.content_type,
            "direct_url":       r.direct_url,
            "search_url":       r.search_url,
            "search_terms":     r.search_terms,
            "exact_search_url": r.exact_search_url,
            "has_transcript":   r.has_transcript,
            "tier":             r.tier,
        }

    return {
        "video":               _to_dict(video),
        "reading":             _to_dict(reading),
        "fallback_search_url": fallback,
    }

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli():
    import argparse, json
    parser = argparse.ArgumentParser()
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
                import json
                print(json.dumps({
                    phase: format_resource_cell_structured(v, r, args.topic)
                    for phase, (v, r) in all_recs.items()
                }, indent=2))
        else:
            video, reading = rec.recommend_pair(
                args.substrand, args.topic, args.subject, args.phase)
            if args.text:
                print(format_resource_cell(video, reading))
            else:
                import json
                print(json.dumps(
                    format_resource_cell_structured(video, reading, args.topic),
                    indent=2))

if __name__ == "__main__":
    _cli()
