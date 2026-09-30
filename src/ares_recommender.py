"""
ares_recommender.py — ARES Content Recommendation Module
=========================================================
Confirmed URL patterns (host is ARES_HOST, default `ares.local` — see below;
the `ares.edu` spellings in these examples are historical):

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

# DEFAULT IS `ares.local` AND MUST STAY THAT WAY.
#
# This default used to be "ares.edu". Because generate.js shells out to this
# module (via generators/aresResources.js), any regeneration run without
# ARES_HOST set in the environment silently rewrote every resource link back to
# ares.edu — which is exactly what happened on 2026-07-30 (`generate.js --all`
# during the new-STEM-subjects run), reverting the whole 2026-07-05 migration
# corpus-wide and leaving ~160 dead hyperlinks per Lesson Sequence in every
# distributed docx/PDF. Nothing errored; the links just stop resolving.
#
# Why .local: ares.edu only ever resolved via a dnsmasq instance on a box that
# controls DHCP. Plugged into an existing school router it fails silently. mDNS
# resolves `.local` by broadcast regardless of who runs DHCP, so it works in
# both deployment modes. See STATUS.md "ares.edu -> ares.local hostname
# migration" and "The same bug was fixed twice on symptoms, then re-fired".
#
# Override per-run for a specific box (e.g. export ARES_HOST=10.42.0.1), but do
# not change this default back.
ARES_HOST = os.environ.get("ARES_HOST", "ares.local")

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
    """Web module, linked directly.

    NOT via /tracker/kiwix_launch.html: that page rejects any target not
    starting with /kiwix/ ("Invalid target") — verified on the ARES disk image
    and on demo.aresedu.dev, 2026-09-29. /tracker/external_launch.html can log
    and redirect, but needs a module_id; click tracking is a separate open
    thread in STATUS.md.
    """
    return f"http://{ARES_HOST}/modules/{quote(path.lstrip('/'), safe='/')}"

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
        "seavuria",
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
# Matching rules — config/link_matching.yaml (shared with the pipeline gate)
# ---------------------------------------------------------------------------
# Design: DESIGN_link_selection_v2.md. In short: build the query from what the
# lesson is ABOUT (no structure/pedagogy words), retrieve with one bm25-ranked
# FTS query, hard-exclude answer/exam material, require a minimum relevance
# (else return None and let the search link stand), and only then use channel
# quality / link reliability / phase as tiebreaks.

_CONFIG_PATH = os.environ.get(
    "LINK_MATCHING_CONFIG",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "link_matching.yaml"),
)


def load_link_config(path: str = _CONFIG_PATH) -> dict:
    import yaml
    with open(path) as f:
        cfg = yaml.safe_load(f)
    cfg["_exclude_re"] = re.compile("|".join(cfg["exclude_patterns"]), re.I)
    cfg["_stop"] = {w.lower() for w in cfg["query_stopwords"]}
    cfg["_generic"] = {w.lower() for w in cfg.get("gate_generic_terms", [])}
    # Synonym groups -> one canonical token per group (see config comment).
    single, phrases, members = {}, [], {}
    for grp in cfg.get("synonyms") or []:
        canon = re.sub(r"[^a-z0-9]", "", grp[0].lower())
        members[canon] = [m.lower() for m in grp]
        for m in grp:
            words = m.lower().split()
            if len(words) > 1:
                phrases.append((len(m), re.compile(r"\b" + r"\s+".join(map(re.escape, words)) + r"\b"), canon))
            else:
                key = _norm(words[0])
                if key in single and single[key] != canon:
                    raise ValueError(f"link_matching.yaml: '{m}' is in two synonym groups")
                single[key] = canon
    cfg["_syn_single"] = single
    cfg["_syn_phrases"] = [(rx, c) for _, rx, c in sorted(phrases, key=lambda x: -x[0])]
    cfg["_syn_members"] = members
    return cfg


def canon_text(text: str, cfg: dict) -> str:
    """Lower-case text with multi-word synonyms collapsed to their canonical token."""
    t = (text or "").lower()
    for rx, canon in cfg.get("_syn_phrases", []):
        t = rx.sub(f" {canon} ", t)
    return t


def _canon(w: str, cfg: dict) -> str:
    """Singular form, then mapped to its synonym group's canonical token."""
    n = _norm(w)
    return cfg.get("_syn_single", {}).get(n, n)


def gate_words(text: str, cfg: dict) -> set[str]:
    """Canonical word set of a candidate's text, as the relevance gate sees it."""
    return {_canon(t, cfg) for t in _tokens(canon_text(text, cfg))}


def _norm(w: str) -> str:
    """Crude singular form, so 'waves' matches 'wave' and 'charges' 'charge'."""
    w = w.lower()
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 4 and w.endswith(("ches", "shes", "sses", "xes", "zes")):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is")):
        return w[:-1]
    return w


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9\-']*[a-z0-9]|[a-z]{3,}", (text or "").lower())


def _content_tokens(text: str, stop: set[str]) -> list[str]:
    out = []
    for t in _tokens(text):
        for part in t.split("-"):
            part = part.strip("'")
            if len(part) >= 3 and not part.isdigit() and part not in stop and _norm(part) not in stop:
                out.append(part)
    return out


_SUBSTRAND_PREFIX = re.compile(r"^\s*sub[\s\-]*strand\s*[\d.]*\s*[:\-–—]?\s*", re.I)


def strip_substrand_label(substrand: str) -> str:
    """'Sub-Strand 2.1: Properties of Waves' -> 'Properties of Waves'."""
    return _SUBSTRAND_PREFIX.sub("", substrand or "").strip()


def foreign_vocab_hits(title: str, subject: str, cfg: dict) -> list[str]:
    """Foreign-subject vocabulary in a title, for a lesson in `subject`."""
    words = {_norm(t) for t in _tokens(title)}
    low = (title or "").lower()
    hits = []
    for group, spec in (cfg.get("foreign_vocab") or {}).items():
        if subject in spec.get("home", []):
            continue
        for term in spec["terms"]:
            if " " in term:
                if re.search(r"\b" + re.escape(term) + r"\b", low):
                    hits.append(term)
            elif _norm(term) in words:
                hits.append(term)
    return sorted(set(hits))


class LessonQuery:
    """The lesson-side view used by both retrieval and the relevance gate."""

    def __init__(self, substrand: str, topic: str, title: str, subject: str, cfg: dict):
        stop, generic = cfg["_stop"], cfg["_generic"]
        self.subject = subject
        self.topic_name = strip_substrand_label(substrand)
        th = cfg["thresholds"]
        core = _content_tokens(self.topic_name, stop)
        topic_toks = _content_tokens(topic, stop)
        title_toks = _content_tokens(title, stop)
        detail = topic_toks + title_toks
        # Phrases from aresKeywords (comma-separated) kept whole for FTS.
        self.phrases = []
        for ph in re.split(r"[,;]", topic or ""):
            toks = _content_tokens(ph, stop)
            if len(toks) >= 2:
                self.phrases.append(" ".join(toks))
        self.core = list(dict.fromkeys(core))
        self.detail = [t for t in dict.fromkeys(detail) if _norm(t) not in {_norm(c) for c in core}]
        # Gate-side vocabulary is canonical: synonyms collapsed (config
        # `synonyms`), singular forms. Raw tokens above stay for search terms.
        ct = lambda text: canon_text(text, cfg)          # noqa: E731
        cn = lambda w: _canon(w, cfg)                     # noqa: E731
        self._members = cfg.get("_syn_members", {})
        self._syn_terms = {cn(t) for t in _content_tokens(ct(f"{self.topic_name} {topic} {title}"), stop)} \
            & set(self._members)
        # Core topics: the sub-strand name split on and/,/&; each topic must
        # match whole (all of its non-generic words).
        self.core_topics: list[frozenset] = []
        for part in re.split(r"\s*(?:,|&|\band\b)\s*", self.topic_name, flags=re.I):
            words = frozenset(cn(t) for t in _content_tokens(ct(part), stop)
                              if t not in generic and _norm(t) not in generic)
            if words and words not in self.core_topics:
                self.core_topics.append(words)
        # Gate phrases: each comma-separated aresKeywords phrase counts only if
        # ALL its (non-generic) words are present; ordered most-important-first.
        # Lesson-title words count singly at a flat, lower weight.
        core_norm = {cn(c) for c in _content_tokens(ct(self.topic_name), stop)}
        self.gate_phrases: list[tuple[str, frozenset, float]] = []
        seen: set[frozenset] = set()
        pos = 0
        for ph in re.split(r"[,;]", topic or ""):
            words = frozenset(cn(t) for t in _content_tokens(ct(ph), stop)
                              if t not in generic and _norm(t) not in generic)
            if not words or words <= core_norm or words in seen:
                continue
            seen.add(words)
            w = 1.0 / (1.0 + pos / th["detail_decay"])
            if len(words) >= 2:
                w *= th["multiword_bonus"]
            self.gate_phrases.append((" ".join(sorted(words)), words, w))
            pos += 1
        for t in _content_tokens(ct(title), stop):
            n = cn(t)
            if n not in core_norm and t not in generic and n not in generic \
                    and frozenset([n]) not in seen:
                seen.add(frozenset([n]))
                self.gate_phrases.append((n, frozenset([n]), th["title_term_weight"]))

    def fts_query(self, max_terms: int = 40) -> str:
        terms = []
        for t in self.core + self.detail:
            for v in {t, _norm(t), _norm(t) + "s"}:
                terms.append(f'"{v}"')
        terms += [f'"{p}"' for p in self.phrases]
        # Synonym expansion: search every written form of a group the lesson uses.
        for canon in sorted(self._syn_terms):
            terms += [f'"{m}"' for m in self._members[canon]]
        return " OR ".join(list(dict.fromkeys(terms))[: max_terms * 3])

    def search_terms(self, kind: str = "", n: int = 4) -> str:
        base = list(dict.fromkeys(self.core + self.detail))[:n]
        if kind == "video":
            base.append("video")
        elif kind == "reading":
            base.append("notes")
        return " ".join(base)


# ---------------------------------------------------------------------------
# Recommender
# ---------------------------------------------------------------------------

class AresRecommender:

    PHASES = ("predict", "observe", "explain", "dqb", "model")

    def __init__(self, db_path: str, config_path: str = _CONFIG_PATH):
        self.db_path = str(db_path)
        self.cfg = load_link_config(config_path)
        self._conn: Optional[sqlite3.Connection] = None
        self._ready = False
        self._available: Optional[set[str]] = None
        self._web_root = os.environ.get("WEB_MODULES_REFERENCE_ROOT") or self.cfg.get("web_modules_reference_root")
        if self._web_root and not os.path.isdir(self._web_root):
            self._web_root = None
        self._init_db()
        self._load_reference()

    def _init_db(self):
        try:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("SELECT id FROM content LIMIT 1")
            self._ready = True
        except Exception as e:
            print(f"[AresRecommender] WARNING: {e}")

    def _load_reference(self):
        ref = os.environ.get("KOLIBRI_REFERENCE_DB") or self.cfg.get("kolibri_reference_db")
        if ref and os.path.exists(ref):
            k = sqlite3.connect(f"file:{ref}?immutable=1", uri=True)
            self._available = {r[0] for r in k.execute(
                "SELECT id FROM content_contentnode WHERE available=1")}
            k.close()

    # -- retrieval + gate ---------------------------------------------------

    def _candidates(self, q: LessonQuery, kind: str) -> tuple[list[dict], list[dict]]:
        """Return (passed, rejected) candidate dicts for one slot kind, best first."""
        cfg, th = self.cfg, self.cfg["thresholds"]
        types = cfg["content_types"][kind]
        sources = cfg["eligible_sources"]
        sql = f"""
            SELECT c.id, c.title, c.source, c.content_type, c.subject, c.path,
                   c.filename, c.description, c.keywords, c.kolibri_id,
                   c.kolibri_channel, c.transcript_path, c.kolibri_available,
                   bm25(content_fts, 10.0, 3.0, 1.0, 1.0, 5.0) AS bm
            FROM content_fts JOIN content c ON c.id = content_fts.rowid
            WHERE content_fts MATCH ?
              AND c.content_type IN ({",".join("?" * len(types))})
              AND c.source IN ({",".join("?" * len(sources))})
            ORDER BY bm LIMIT ?"""
        try:
            rows = self._conn.execute(sql, (q.fts_query(), *types, *sources, th["candidates"])).fetchall()
        except sqlite3.OperationalError as e:
            print(f"[AresRecommender] FTS error: {e}")
            return [], []

        family = set(cfg.get("subject_families", {}).get(q.subject, [q.subject, "General"]))
        passed, rejected, seen = [], [], set()
        for row in rows:
            title = str(row["title"] or "")
            key = re.sub(r"[^a-z0-9]", "", title.lower())
            if not title or key in seen:
                continue
            seen.add(key)
            meta_words = gate_words(f"{title} {row['description'] or ''} {row['keywords'] or ''}", cfg)
            title_words = gate_words(title, cfg)
            core_hits = [" ".join(sorted(t)) for t in q.core_topics if t <= meta_words]
            matched = [(name, w) for name, words, w in q.gate_phrases if words <= meta_words]
            detail_hits = [name for name, _ in matched]
            c = {
                "row": row, "title": title, "bm25": row["bm"],
                "core_hits": core_hits, "detail_hits": detail_hits,
                "core_in_title": sum(1 for t in q.core_topics if t <= title_words),
                "subject": row["subject"], "reason": "",
            }
            blob = f"{title} {row['filename'] or ''} {row['path'] or ''}"
            kid = str(row["kolibri_id"] or "")
            path = str(row["path"] or "")
            c["detail_weight"] = round(sum(w for _, w in matched), 2)
            if cfg["_exclude_re"].search(blob) or path.startswith(tuple(cfg.get("excluded_path_prefixes", []))):
                c["reason"] = "excluded: answer/exam material"
            elif row["source"] == "web" and not self._web_file_exists(path):
                c["reason"] = "web file not on reference image"
            elif row["source"] == "kolibri" and (
                    not kid or (self._available is not None and kid not in self._available)
                    or (self._available is None and not row["kolibri_available"])):
                c["reason"] = "kolibri node not available on reference image"
            elif not ((len(core_hits) >= th["min_core_hits"]
                       and c["detail_weight"] >= th["min_detail_with_core"])
                      or c["detail_weight"] >= th["min_detail_weight"]):
                c["reason"] = "below relevance gate"
            elif foreign_vocab_hits(title, q.subject, cfg) and not c["core_in_title"]:
                c["reason"] = f"foreign vocabulary {foreign_vocab_hits(title, q.subject, cfg)}"
            if c["reason"]:
                rejected.append(c)
                continue
            rel = -row["bm"]
            rel *= 1 + th["core_in_title_bonus"] * c["core_in_title"] + 0.3 * c["detail_weight"]
            if row["subject"] not in family:
                rel *= th["off_family_factor"]
            channel = _channel_name(row)
            tier = _channel_tier(channel, row["source"]) if kind == "video" else \
                _reading_tier(channel, row["source"], row["content_type"])
            rel *= (1.10, 1.05, 1.0)[min(tier, 2)]
            rel *= 1.05 if path.startswith("kolibri_storage/") else 1.0
            c.update(score=rel, tier=tier)
            passed.append(c)
        passed.sort(key=lambda c: -c["score"])
        return passed, rejected

    def _to_resource(self, c: dict, q: LessonQuery, kind: str) -> AresResource:
        row = c["row"]
        src, kid, path = str(row["source"]), str(row["kolibri_id"] or ""), str(row["path"] or "")
        terms = q.search_terms(kind)
        return AresResource(
            title=c["title"],
            channel=_channel_name(row),
            source=src,
            content_type=str(row["content_type"]).lower(),
            direct_url=self._build_direct_url(src, kid, path),
            search_url=_ares_search_url(terms),
            search_terms=terms,
            exact_search_url=_ares_search_url(c["title"]),
            kolibri_id=kid,
            tier=c["tier"],
            subject_match=True,
            has_transcript=bool(row["transcript_path"]),
            is_storage=path.startswith("kolibri_storage/"),
        )

    # -- public API ----------------------------------------------------------

    def recommend_all_phases(self, substrand: str, lesson_topic: str, subject: str = "",
                             lesson_title: str = "") -> tuple[dict, dict]:
        """Return ({phase: (video|None, reading|None)}, diagnostics)."""
        q = LessonQuery(substrand, lesson_topic, lesson_title, subject, self.cfg)
        out = {p: [None, None] for p in self.PHASES}
        diag = {"query": {"core": q.core, "detail": q.detail[:25], "phrases": q.phrases[:15]},
                "slots": {}}
        if not self._ready:
            return {p: tuple(v) for p, v in out.items()}, diag
        for i, kind in enumerate(("video", "reading")):
            passed, rejected = self._candidates(q, kind)
            used: set[str] = set()
            for phase in self.PHASES:
                hints = {_norm(h) for h in self.cfg["phase_hints"].get(phase, [])}
                floor = self.cfg["thresholds"]["diversity_floor"] * passed[0]["score"] if passed else 0
                pool = [c for c in passed if c["title"] not in used and c["score"] >= floor] or passed
                if pool:
                    top = pool[0]["score"]
                    # Phase hint only reorders near-ties (within 10% of the best).
                    near = [c for c in pool if c["score"] >= 0.9 * top]
                    near.sort(key=lambda c: (-len(hints & {_norm(t) for t in _tokens(c["title"])}), -c["score"]))
                    pick = near[0]
                    used.add(pick["title"])
                    out[phase][i] = self._to_resource(pick, q, kind)
                diag["slots"][f"{phase}.{kind}"] = {
                    "picked": out[phase][i].title if out[phase][i] else None,
                    "score": round(pick["score"], 2) if pool else None,
                    "core_hits": pick["core_hits"] if pool else [],
                    "detail_hits": pick["detail_hits"][:8] if pool else [],
                    "detail_weight": pick["detail_weight"] if pool else 0,
                }
            diag[f"{kind}_pool"] = {
                "passed": len(passed),
                "runners_up": [c["title"] for c in passed[1:6]],
                "rejected_sample": [(c["title"], c["reason"]) for c in rejected[:8]],
                "rejected_by_reason": _count_reasons(rejected),
            }
        return {p: tuple(v) for p, v in out.items()}, diag

    def recommend_pair(self, substrand: str, topic: str, subject: str = "",
                       phase: str = "observe", lesson_title: str = ""):
        recs, _ = self.recommend_all_phases(substrand, topic, subject, lesson_title)
        return recs.get(phase, (None, None))

    def fallback_search_url(self, substrand: str, topic: str, subject: str = "", lesson_title: str = "") -> str:
        q = LessonQuery(substrand, topic, lesson_title, subject, self.cfg)
        return _ares_search_url(q.search_terms() or q.topic_name or subject)

    def _web_file_exists(self, path: str) -> bool:
        if not self._web_root:
            return True   # no reference image mounted: cannot verify, checker warns
        if path.startswith("KICD_Educhannel/"):
            return os.path.exists(os.path.join(os.path.dirname(self._web_root), "html", path)) \
                or os.path.exists(os.path.join(os.path.dirname(self._web_root), path))
        return os.path.exists(os.path.join(self._web_root, path))

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

    def close(self):
        if self._conn:
            self._conn.close()
    def __enter__(self): return self
    def __exit__(self, *_): self.close()


def _channel_name(row) -> str:
    """Kolibri channel, or for web modules the module folder (PhET, Seavuria, ...)."""
    ch = str(row["kolibri_channel"] or "")
    if not ch and row["source"] == "web":
        ch = str(row["path"] or "").split("/", 1)[0]
    return ch


def _count_reasons(rejected: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for c in rejected:
        key = c["reason"].split(" [")[0]
        counts[key] = counts.get(key, 0) + 1
    return counts

# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_resource_cell(
    video: Optional[AresResource],
    reading: Optional[AresResource],
    fallback: str,
) -> str:
    parts = []
    for label, r in (("📹 VIDEO", video), ("📖 READING", reading)):
        if r:
            parts.append(
                f"{label}: {r.title}\n"
                f"   Source: {r.display_source}\n"
                f"   Link:   {r.direct_url or r.exact_search_url}\n"
                f"   Search (topic): {r.search_url}\n"
                f"   Terms:  \"{r.search_terms}\""
            )
        else:
            parts.append(f"{label}: no confident match.\n   Search: {fallback}")
    return "\n\n".join(parts)


def format_resource_cell_structured(
    video: Optional[AresResource],
    reading: Optional[AresResource],
    fallback: str,
) -> dict:
    """Contract shape (ares-contract.schema.json $defs/phaseResources).
    None = no confident match; fallback_search_url is always present."""

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
    parser.add_argument("--title",      default="", help="lesson title (detail terms)")
    parser.add_argument("--subject",    default="")
    parser.add_argument("--phase",      default="observe",
                        choices=["predict", "observe", "explain", "dqb", "model"])
    parser.add_argument("--all-phases", action="store_true")
    parser.add_argument("--text",       action="store_true")
    args = parser.parse_args()

    with AresRecommender(args.db) as rec:
        if not rec._ready:
            raise SystemExit(f"ARES content DB not usable: {args.db}")
        recs, diag = rec.recommend_all_phases(args.substrand, args.topic, args.subject, args.title)
        fallback = rec.fallback_search_url(args.substrand, args.topic, args.subject, args.title)
        phases = recs if args.all_phases else {args.phase: recs[args.phase]}
        if args.text:
            for phase, (v, r) in phases.items():
                print(f"\n{'='*60}\n{phase.upper()}\n{'='*60}")
                print(format_resource_cell(v, r, fallback))
            return
        out = {p: format_resource_cell_structured(v, r, fallback) for p, (v, r) in phases.items()}
        if not args.all_phases:
            out = out[args.phase]
        # Diagnostics ride alongside; the JS bridge strips them before the
        # contract JSON is written (they go to logs/link_matching/ instead).
        out["_diagnostics"] = diag
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    _cli()
