#!/usr/bin/env python3
"""
scan_ares_content.py  (v2 — multi-source)
──────────────────────────────────────────
Builds a unified SQLite index of all ARES content from three sources:

  1. Web root  — standard file walk of the nginx-served directory
  2. Kiwix     — reads .zim archive metadata (and optionally articles) via libzim
  3. Kolibri   — queries channel SQLite databases for content node metadata

All three sources write to the same database so the lesson plan generator can
search across everything in one query.

Usage:
    python3 scan_ares_content.py --config ares_scan_config.yaml
    python3 scan_ares_content.py --config ares_scan_config.yaml --source web
    python3 scan_ares_content.py --config ares_scan_config.yaml --source kiwix
    python3 scan_ares_content.py --config ares_scan_config.yaml --source kolibri
    python3 scan_ares_content.py --config ares_scan_config.yaml --fast

Dependencies:
    pip3 install pyyaml libzim pdfminer.six --break-system-packages
    (libzim required for Kiwix; pdfminer.six optional for PDF text extraction)
"""

import argparse
import json
import logging
import math
import os
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

# ─── Optional imports ─────────────────────────────────────────────────────────

try:
    from libzim import Archive as ZimArchive
    LIBZIM_AVAILABLE = True
except ImportError:
    LIBZIM_AVAILABLE = False

try:
    from html.parser import HTMLParser
    HTML_PARSER_AVAILABLE = True
except ImportError:
    HTML_PARSER_AVAILABLE = False

try:
    import pdfminer.high_level as pdfminer_hl
    PDF_EXTRACT_AVAILABLE = True
    PDF_BACKEND = "pdfminer"
except ImportError:
    try:
        import pypdf  # noqa: F401
        PDF_EXTRACT_AVAILABLE = True
        PDF_BACKEND = "pypdf"
    except ImportError:
        PDF_EXTRACT_AVAILABLE = False
        PDF_BACKEND = None


# ─── Database schema ──────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS content (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    source              TEXT NOT NULL,        -- 'web', 'kiwix', 'kolibri'
    path                TEXT NOT NULL,        -- relative path or logical identifier
    filename            TEXT,
    content_type        TEXT NOT NULL,        -- video/audio/pdf/html/image/exercise/topic/zim
    title               TEXT,
    description         TEXT,
    subject             TEXT,
    module              TEXT,                 -- e.g. "Khan Academy", "Wikipedia EN", channel name
    size_bytes          INTEGER,
    duration_seconds    REAL,
    transcript_path     TEXT,
    transcript_text     TEXT,
    extracted_text      TEXT,
    keywords            TEXT,
    -- Kiwix-specific
    zim_file            TEXT,                 -- which .zim archive this came from
    article_count       INTEGER,              -- only for zim-level entries
    -- Kolibri-specific
    kolibri_id          TEXT,                 -- content_id from Kolibri DB
    kolibri_channel     TEXT,                 -- channel name
    kolibri_kind        TEXT,                 -- original kind string
    kolibri_available   INTEGER DEFAULT 1,
    -- Housekeeping
    last_scanned        TEXT NOT NULL,
    UNIQUE(source, path)
);

CREATE TABLE IF NOT EXISTS modules (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT UNIQUE NOT NULL,
    source          TEXT,
    content_count   INTEGER DEFAULT 0,
    video_count     INTEGER DEFAULT 0,
    pdf_count       INTEGER DEFAULT 0,
    html_count      INTEGER DEFAULT 0,
    exercise_count  INTEGER DEFAULT 0,
    subjects        TEXT
);

CREATE TABLE IF NOT EXISTS scan_runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at      TEXT NOT NULL,
    finished_at     TEXT,
    source          TEXT NOT NULL,
    root_path       TEXT NOT NULL,
    files_scanned   INTEGER DEFAULT 0,
    files_indexed   INTEGER DEFAULT 0,
    errors          INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_content_source  ON content(source);
CREATE INDEX IF NOT EXISTS idx_content_subject ON content(subject);
CREATE INDEX IF NOT EXISTS idx_content_type    ON content(content_type);
CREATE INDEX IF NOT EXISTS idx_content_module  ON content(module);
CREATE INDEX IF NOT EXISTS idx_content_title   ON content(title);
CREATE INDEX IF NOT EXISTS idx_kolibri_id      ON content(kolibri_id);

CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
    title, description, extracted_text, transcript_text, keywords,
    content='content', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS content_ai AFTER INSERT ON content BEGIN
    INSERT INTO content_fts(rowid, title, description, extracted_text, transcript_text, keywords)
    VALUES (new.id, new.title, new.description, new.extracted_text, new.transcript_text, new.keywords);
END;
CREATE TRIGGER IF NOT EXISTS content_ad AFTER DELETE ON content BEGIN
    INSERT INTO content_fts(content_fts, rowid, title, description, extracted_text, transcript_text, keywords)
    VALUES ('delete', old.id, old.title, old.description, old.extracted_text, old.transcript_text, old.keywords);
END;
CREATE TRIGGER IF NOT EXISTS content_au AFTER UPDATE ON content BEGIN
    INSERT INTO content_fts(content_fts, rowid, title, description, extracted_text, transcript_text, keywords)
    VALUES ('delete', old.id, old.title, old.description, old.extracted_text, old.transcript_text, old.keywords);
    INSERT INTO content_fts(rowid, title, description, extracted_text, transcript_text, keywords)
    VALUES (new.id, new.title, new.description, new.extracted_text, new.transcript_text, new.keywords);
END;
"""


def init_db(db_path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def upsert_content(conn: sqlite3.Connection, row: dict) -> None:
    cols = list(row.keys())
    placeholders = ", ".join("?" * len(cols))
    col_names = ", ".join(cols)
    updates = ", ".join(f"{c}=excluded.{c}" for c in cols if c not in ("source", "path"))
    conn.execute(
        f"""
        INSERT INTO content ({col_names}) VALUES ({placeholders})
        ON CONFLICT(source, path) DO UPDATE SET {updates}
        """,
        list(row.values()),
    )


# ─── Text utilities ───────────────────────────────────────────────────────────

STOP_WORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","are","was","were","be","been","being","have","has",
    "had","do","does","did","will","would","could","should","may","might",
    "not","no","so","yet","as","if","that","this","it","its","they","them",
    "their","he","she","we","you","who","what","which","where","when","how",
    "all","each","every","more","most","also","just","about","into","such",
    "other","than","then","both","either","whether",
}


def extract_keywords(text: str, n: int = 20) -> list:
    if not text:
        return []
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    words = [w for w in words if w not in STOP_WORDS]
    if not words:
        return []
    counts = Counter(words)
    total = len(words)
    scored = [
        (w, (c / total) * math.log(1 + total / c))
        for w, c in counts.items()
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [w for w, _ in scored[:n]]


def classify_subject(text: str, path_str: str, subject_kw: dict) -> str:
    combined = (path_str + " " + text[:3000]).lower()
    scores = {}
    for subject, keywords in subject_kw.items():
        score = sum(1 for kw in keywords if kw.lower() in combined)
        if score > 0:
            scores[subject] = score
    return max(scores, key=scores.get) if scores else "General"


class _HTMLStripper(HTMLParser if HTML_PARSER_AVAILABLE else object):
    SKIP = {"script", "style", "noscript", "head"}
    def __init__(self):
        if HTML_PARSER_AVAILABLE:
            super().__init__()
        self._parts = []
        self._skip = False
    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.SKIP:
            self._skip = True
    def handle_endtag(self, tag):
        if tag.lower() in self.SKIP:
            self._skip = False
    def handle_data(self, data):
        if not self._skip and data.strip():
            self._parts.append(data.strip())
    def get_text(self):
        return " ".join(self._parts)


def extract_html_title(content: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return ""


def extract_html_text(content: str, limit: int = 20000) -> str:
    if not HTML_PARSER_AVAILABLE:
        text = re.sub(r"<[^>]+>", " ", content)
        return re.sub(r"\s+", " ", text).strip()[:limit]
    p = _HTMLStripper()
    try:
        p.feed(content)
        return p.get_text()[:limit]
    except Exception:
        return ""


def extract_pdf_text(path: Path, limit: int = 20000) -> str:
    if not PDF_EXTRACT_AVAILABLE:
        return ""
    try:
        if PDF_BACKEND == "pdfminer":
            import io
            buf = io.StringIO()
            pdfminer_hl.extract_text_to_fp(open(str(path), "rb"), buf, output_type="text")
            return buf.getvalue()[:limit]
        else:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            return " ".join(p.extract_text() or "" for p in reader.pages)[:limit]
    except Exception:
        return ""


def read_whisper_transcript(path: Path, limit: int = 20000) -> tuple:
    """Returns (text, duration_seconds)."""
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
        suffix = path.suffix.lower()
        if suffix == ".json":
            data = json.loads(raw)
            if not isinstance(data, dict):
                return "", 0.0
            text = data.get("text", "")
            if not text:
                text = " ".join(s.get("text", "") for s in data.get("segments", []))
            duration = 0.0
            segs = data.get("segments", [])
            if segs:
                duration = float(segs[-1].get("end", 0.0))
            return text[:limit], duration
        elif suffix in (".srt", ".vtt"):
            lines = []
            last_end = 0.0
            for line in raw.splitlines():
                line = line.strip()
                if not line or re.match(r"^\d+$", line) or line.startswith("WEBVTT"):
                    continue
                m = re.match(r"[\d:,.]+\s+-->\s+([\d:,.]+)", line)
                if m:
                    t = m.group(1).replace(",", ".")
                    parts = t.split(":")
                    try:
                        if len(parts) == 3:
                            last_end = int(parts[0])*3600 + int(parts[1])*60 + float(parts[2])
                        elif len(parts) == 2:
                            last_end = int(parts[0])*60 + float(parts[1])
                    except Exception:
                        pass
                    continue
                lines.append(re.sub(r"<[^>]+>", "", line))
            return " ".join(lines)[:limit], last_end
    except Exception:
        pass
    return "", 0.0


def find_transcript(video_path: Path, transcript_root: Path,
                    t_exts: set, tj_exts: set, store_text: bool, limit: int) -> tuple:
    """Returns (transcript_path_str, transcript_text)."""
    stem = video_path.stem
    parent = video_path.parent
    candidates = []
    for ext in list(tj_exts) + list(t_exts):
        candidates.append(parent / (stem + ext))
        if transcript_root != video_path.parent:
            candidates.append(transcript_root / (stem + ext))
    for c in candidates:
        if c.exists():
            text, _ = read_whisper_transcript(c, limit) if store_text else ("", 0.0)
            return str(c), text
    return "", ""


# ══════════════════════════════════════════════════════════════════════════════
# SOURCE 1: Web root scanner
# ══════════════════════════════════════════════════════════════════════════════

def scan_web(source_cfg: dict, config: dict, conn: sqlite3.Connection,
             log: logging.Logger, fast: bool = False) -> dict:
    root = Path(source_cfg["path"])
    source_name = source_cfg["name"]
    log.info(f"[Web] Scanning: {root}")

    ext_cfg = config.get("file_extensions", {})
    video_exts  = set(ext_cfg.get("video", [".mp4", ".webm"]))
    audio_exts  = set(ext_cfg.get("audio", [".mp3"]))
    pdf_exts    = set(ext_cfg.get("pdf", [".pdf"]))
    html_exts   = set(ext_cfg.get("html", [".html", ".htm"]))
    image_exts  = set(ext_cfg.get("image", [".jpg", ".png"]))
    t_exts      = set(ext_cfg.get("transcript", [".srt", ".vtt"]))
    tj_exts     = set(ext_cfg.get("transcript_json", [".json"]))
    all_indexed = video_exts | audio_exts | pdf_exts | html_exts | image_exts

    skip_dirs    = set(config.get("skip_directories", []))
    max_bytes    = config.get("max_extract_size_mb", 10) * 1024 * 1024
    subject_kw   = config.get("subject_keywords", {})
    do_html      = config.get("extract_html_text", True) and not fast
    do_pdf       = config.get("extract_pdf_text", True) and not fast
    do_kw        = config.get("extract_keywords", True) and not fast
    kw_count     = config.get("keyword_count", 20)
    t_root       = Path(config.get("whisper_transcript_root", str(root)))
    store_t      = config.get("store_transcript_text", True)
    t_limit      = config.get("transcript_text_limit", 20000)
    now_str      = datetime.utcnow().isoformat()

    stats = {"scanned": 0, "indexed": 0, "errors": 0}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in skip_dirs and not d.startswith(".")]

        for filename in filenames:
            if filename.endswith(".php"):
                continue  # skip PHP — not executable by scanner
            filepath = Path(dirpath) / filename
            suffix = filepath.suffix.lower()
            if suffix not in all_indexed:
                continue

            stats["scanned"] += 1
            rel_path = str(filepath.relative_to(root))

            try:
                size_bytes = filepath.stat().st_size

                if suffix in video_exts:
                    content_type = "video"
                elif suffix in audio_exts:
                    content_type = "audio"
                elif suffix in pdf_exts:
                    content_type = "pdf"
                elif suffix in html_exts:
                    content_type = "html"
                else:
                    content_type = "image"

                title = ""
                extracted_text = ""

                if content_type == "html" and do_html and size_bytes <= max_bytes:
                    raw = filepath.read_text(encoding="utf-8", errors="replace")
                    title = extract_html_title(raw)
                    extracted_text = extract_html_text(raw)
                elif content_type == "pdf" and do_pdf and size_bytes <= max_bytes:
                    extracted_text = extract_pdf_text(filepath)

                if not title:
                    title = filepath.stem.replace("-", " ").replace("_", " ").title()

                subject = classify_subject(
                    extracted_text or title, rel_path, subject_kw
                )

                keywords_str = ""
                if do_kw:
                    kws = extract_keywords(extracted_text or title, kw_count)
                    keywords_str = ", ".join(kws)

                t_path, t_text = "", ""
                if content_type in ("video", "audio"):
                    t_path, t_text = find_transcript(
                        filepath, t_root, t_exts, tj_exts, store_t, t_limit
                    )

                upsert_content(conn, {
                    "source": "web",
                    "path": rel_path,
                    "filename": filename,
                    "content_type": content_type,
                    "title": title,
                    "description": "",
                    "subject": subject,
                    "module": source_name,
                    "size_bytes": size_bytes,
                    "duration_seconds": None,
                    "transcript_path": t_path,
                    "transcript_text": t_text,
                    "extracted_text": extracted_text[:20000],
                    "keywords": keywords_str,
                    "zim_file": None,
                    "article_count": None,
                    "kolibri_id": None,
                    "kolibri_channel": None,
                    "kolibri_kind": None,
                    "kolibri_available": 1,
                    "last_scanned": now_str,
                })
                stats["indexed"] += 1

                if stats["indexed"] % 200 == 0:
                    conn.commit()
                    log.info(f"  [Web] {stats['indexed']} files indexed...")

            except Exception as e:
                stats["errors"] += 1
                log.error(f"  [Web] Error: {rel_path}: {e}")

    conn.commit()
    log.info(f"  [Web] Done. Scanned={stats['scanned']} Indexed={stats['indexed']} Errors={stats['errors']}")
    return stats


# ══════════════════════════════════════════════════════════════════════════════
# SOURCE 2: Kiwix ZIM scanner
# ══════════════════════════════════════════════════════════════════════════════

def scan_kiwix(source_cfg: dict, config: dict, conn: sqlite3.Connection,
               log: logging.Logger) -> dict:
    root = Path(source_cfg["path"])
    scan_articles    = source_cfg.get("scan_articles", False)
    max_articles     = source_cfg.get("max_articles_per_zim", 500)
    skip_above_gb    = source_cfg.get("skip_zim_above_gb", 0)   # 0 = no limit
    skip_above_bytes = skip_above_gb * 1024**3 if skip_above_gb else 0
    import fnmatch as _fnmatch
    zim_patterns  = source_cfg.get("scan_zim_patterns", [])
    subject_kw    = config.get("subject_keywords", {})
    do_kw         = config.get("extract_keywords", True)
    kw_count      = config.get("keyword_count", 20)
    now_str       = datetime.utcnow().isoformat()

    log.info(f"[Kiwix] Scanning: {root}")

    if not LIBZIM_AVAILABLE:
        log.error("[Kiwix] libzim not installed. Run: pip3 install libzim --break-system-packages")
        return {"scanned": 0, "indexed": 0, "errors": 1}

    stats = {"scanned": 0, "indexed": 0, "errors": 0}
    zim_files = list(root.rglob("*.zim"))

    if not zim_files:
        log.warning(f"  [Kiwix] No .zim files found under {root}")
        return stats

    log.info(f"  [Kiwix] Found {len(zim_files)} .zim file(s)")

    for zim_path in zim_files:
        stats["scanned"] += 1
        rel_path = str(zim_path.relative_to(root))
        zim_size = zim_path.stat().st_size

        # Skip ZIM files above the configured size threshold
        if skip_above_bytes and zim_size > skip_above_bytes:
            size_gb = zim_size / 1024**3
            log.info(f"  [Kiwix] SKIPPING (>{skip_above_gb} GB): {rel_path} ({size_gb:.1f} GB)")
            stats["scanned"] -= 1  # don't count skipped files
            continue

        log.info(f"  [Kiwix] Reading: {rel_path} ({zim_size/1024**3:.2f} GB)")

        try:
            zim = ZimArchive(str(zim_path))

            # ── Read ZIM metadata ─────────────────────────────────────────────
            # Standard Kiwix metadata keys:
            # Title, Description, Language, Publisher, Creator, Date, Subject,
            # Tags, Name, Flavour, Scraper
            meta_keys = list(zim.metadata_keys)

            def get_meta(key: str) -> str:
                try:
                    val = zim.get_metadata(key)
                    if isinstance(val, (bytes, bytearray)):
                        return val.decode("utf-8", errors="replace").strip()
                    return str(val).strip()
                except Exception:
                    return ""

            title       = get_meta("Title") or _zim_title_from_path(zim_path)
            description = get_meta("Description")
            language    = get_meta("Language")
            subject_raw = get_meta("Subject") or get_meta("Tags")
            publisher   = get_meta("Publisher") or get_meta("Creator")
            entry_count = zim.entry_count
            article_count = zim.article_count

            # Use Subject metadata if available; otherwise classify from title+description
            subject = classify_subject(
                f"{subject_raw} {description} {title}",
                rel_path,
                subject_kw,
            )

            # Module name: publisher > inferred from filename
            module = publisher or _infer_module_from_zim_name(zim_path.stem)

            combined_text = " ".join(filter(None, [title, description, subject_raw]))
            keywords_str = ""
            if do_kw:
                kws = extract_keywords(combined_text, kw_count)
                keywords_str = ", ".join(kws)

            # ── Write ZIM-level entry ─────────────────────────────────────────
            upsert_content(conn, {
                "source": "kiwix",
                "path": rel_path,
                "filename": zim_path.name,
                "content_type": "zim",
                "title": title,
                "description": description,
                "subject": subject,
                "module": module,
                "size_bytes": zim_path.stat().st_size,
                "duration_seconds": None,
                "transcript_path": None,
                "transcript_text": None,
                "extracted_text": combined_text[:20000],
                "keywords": keywords_str,
                "zim_file": rel_path,
                "article_count": article_count,
                "kolibri_id": None,
                "kolibri_channel": None,
                "kolibri_kind": None,
                "kolibri_available": 1,
                "last_scanned": now_str,
            })
            stats["indexed"] += 1

            log.info(
                f"    Title: {title} | Articles: {article_count:,} | "
                f"Subject: {subject} | Module: {module}"
            )

            # ── Optionally index individual articles ──────────────────────────
            # Respect the name whitelist: if scan_zim_patterns is set, only
            # scan articles in ZIM files whose filename matches a pattern.
            name_allowed = (
                not zim_patterns
                or any(_fnmatch.fnmatch(zim_path.name, pat) for pat in zim_patterns)
            )
            if scan_articles and article_count > 0 and name_allowed:
                if zim_patterns:
                    log.info(f"    → Article scan enabled (matched pattern whitelist)")
                indexed_articles = _scan_zim_articles(
                    zim, rel_path, title, module, subject_kw, do_kw, kw_count,
                    now_str, conn, max_articles, log,
                )
                stats["indexed"] += indexed_articles
            elif scan_articles and not name_allowed:
                log.info(f"    → Article scan skipped (not in scan_zim_patterns whitelist)")

        except Exception as e:
            stats["errors"] += 1
            log.error(f"  [Kiwix] Error reading {rel_path}: {e}")

    conn.commit()
    log.info(f"  [Kiwix] Done. Scanned={stats['scanned']} Indexed={stats['indexed']} Errors={stats['errors']}")
    return stats


def _zim_title_from_path(path: Path) -> str:
    """Derive a readable title from the ZIM filename."""
    stem = path.stem
    # kiwix filenames: wikipedia_en_all_maxi_2023-05 → Wikipedia EN All
    parts = stem.split("_")
    meaningful = [p.title() for p in parts if not re.match(r"^\d{4}-\d{2}$", p)
                  and p not in ("all", "mini", "maxi", "nopic", "en", "sw")]
    return " ".join(meaningful) if meaningful else stem


def _infer_module_from_zim_name(stem: str) -> str:
    """Infer the content provider from a Kiwix ZIM filename stem."""
    stem_lower = stem.lower()
    if "wikipedia" in stem_lower:
        lang = "EN"
        m = re.search(r"wikipedia_([a-z]{2,3})_", stem_lower)
        if m:
            lang = m.group(1).upper()
        return f"Wikipedia {lang}"
    if "khan" in stem_lower or "khanacademy" in stem_lower:
        return "Khan Academy"
    if "ted" in stem_lower:
        return "TED"
    if "wikivoyage" in stem_lower:
        return "Wikivoyage"
    if "wiktionary" in stem_lower:
        return "Wiktionary"
    if "stackexchange" in stem_lower or "stackoverflow" in stem_lower:
        return "Stack Exchange"
    if "ck12" in stem_lower or "ck-12" in stem_lower:
        return "CK-12"
    if "gutenberg" in stem_lower:
        return "Project Gutenberg"
    if "phet" in stem_lower:
        return "PhET"
    return stem.split("_")[0].title()


# ─── ZIM entry iterator ───────────────────────────────────────────────────────

# MIME types to skip when walking ZIM entries — not useful for lesson plans
_SKIP_MIMES = (
    "image/", "video/", "audio/",
    "text/css", "application/javascript", "text/javascript",
    "application/x-font", "font/",
)

# Path prefixes used in old ZIM namespace scheme that are not articles
_SKIP_PATH_PREFIXES = ("-/", "I/", "A/search", "A/index")


def _iter_zim_article_entries(zim, max_articles: int, log: logging.Logger):
    """
    Yield non-redirect HTML article entries from a ZIM archive.

    Uses Archive._get_entry_by_id(i) which is available in all libzim
    Python binding versions, including those where Archive is not directly
    iterable. Filters out redirects, images, CSS, JS, and metadata paths.

    Yields (entry, item, mime, content_bytes) tuples.
    """
    total = zim.all_entry_count
    yielded = 0

    for i in range(total):
        if max_articles and yielded >= max_articles:
            return
        try:
            entry = zim._get_entry_by_id(i)

            if entry.is_redirect:
                continue

            path = entry.path

            # Skip metadata and non-article namespaces (old ZIM format)
            skip = False
            for prefix in _SKIP_PATH_PREFIXES:
                if path.startswith(prefix):
                    skip = True
                    break
            if skip:
                continue

            # Get the item to check MIME type
            try:
                item = entry.get_item()
                mime = item.mimetype or ""
            except Exception:
                continue

            # Skip non-text content
            if any(mime.startswith(m) for m in _SKIP_MIMES):
                continue

            # Only yield HTML entries (where text extraction is possible)
            if "html" not in mime and "text/plain" not in mime:
                continue

            try:
                content_bytes = bytes(item.content)
            except Exception:
                content_bytes = b""

            yield entry, item, mime, content_bytes
            yielded += 1

        except Exception:
            continue


def _scan_zim_articles(
    zim, zim_rel_path: str, zim_title: str, module: str,
    subject_kw: dict, do_kw: bool, kw_count: int,
    now_str: str, conn: sqlite3.Connection,
    max_articles: int, log: logging.Logger,
) -> int:
    """
    Walk HTML articles inside a ZIM archive and index each one.
    Returns count of articles indexed.
    """
    count = 0
    try:
        for entry, item, mime, content_bytes in _iter_zim_article_entries(
            zim, max_articles, log
        ):
            path_str = entry.path
            title = entry.title or path_str.split("/")[-1]

            # Extract text
            extracted_text = ""
            try:
                html = content_bytes.decode("utf-8", errors="replace")
                extracted_text = extract_html_text(html, limit=5000)
            except Exception:
                pass

            subject = classify_subject(
                f"{title} {extracted_text[:1000]}", path_str, subject_kw
            )

            keywords_str = ""
            if do_kw:
                kws = extract_keywords(f"{title} {extracted_text}", kw_count)
                keywords_str = ", ".join(kws)

            upsert_content(conn, {
                "source": "kiwix",
                "path": f"{zim_rel_path}::{path_str}",
                "filename": path_str.split("/")[-1],
                "content_type": "html",
                "title": title,
                "description": "",
                "subject": subject,
                "module": module,
                "size_bytes": len(content_bytes),
                "duration_seconds": None,
                "transcript_path": None,
                "transcript_text": None,
                "extracted_text": extracted_text[:10000],
                "keywords": keywords_str,
                "zim_file": zim_rel_path,
                "article_count": None,
                "kolibri_id": None,
                "kolibri_channel": None,
                "kolibri_kind": None,
                "kolibri_available": 1,
                "last_scanned": now_str,
            })
            count += 1

            if count % 200 == 0:
                conn.commit()
                log.info(f"      {count} articles indexed from {zim_rel_path}")

    except Exception as e:
        log.warning(f"    Article walk error for {zim_rel_path}: {e}")

    return count


# ══════════════════════════════════════════════════════════════════════════════
# SOURCE 3: Kolibri channel database scanner
# ══════════════════════════════════════════════════════════════════════════════

def scan_kolibri(source_cfg: dict, config: dict, conn: sqlite3.Connection,
                 log: logging.Logger) -> dict:
    root = Path(source_cfg["path"])
    subject_kw  = config.get("subject_keywords", {})
    do_kw       = config.get("extract_keywords", True)
    kw_count    = config.get("keyword_count", 20)
    kind_map    = config.get("kolibri_kind_map", {})
    now_str     = datetime.utcnow().isoformat()

    log.info(f"[Kolibri] Scanning: {root}")

    stats = {"scanned": 0, "indexed": 0, "errors": 0}

    # Kolibri channel databases live at:
    #   <root>/content/databases/*.sqlite3
    # Try multiple possible locations in case the directory structure differs.
    db_search_paths = [
        root / "content" / "databases",
        root / "databases",
        root,
    ]

    channel_dbs = []
    for search_path in db_search_paths:
        if search_path.exists():
            found = list(search_path.glob("*.sqlite3"))
            if found:
                channel_dbs.extend(found)
                log.info(f"  [Kolibri] Found {len(found)} channel DB(s) in {search_path}")
                break

    # Also look for a main Kolibri DB (different schema)
    main_db_candidates = [
        root / "db.sqlite3",
        root / "kolibri.sqlite3",
    ]

    if not channel_dbs:
        # Last resort: find any sqlite3 file
        channel_dbs = list(root.rglob("*.sqlite3"))
        log.warning(f"  [Kolibri] No databases/ dir found. Found {len(channel_dbs)} .sqlite3 file(s) by rglob.")

    if not channel_dbs:
        log.error(f"  [Kolibri] No SQLite databases found under {root}")
        return stats

    for db_file in channel_dbs:
        if db_file in main_db_candidates:
            continue  # skip main app DB — different schema
        stats["scanned"] += 1
        log.info(f"  [Kolibri] Reading channel DB: {db_file.name}")

        try:
            ch_conn = sqlite3.connect(str(db_file))
            ch_conn.row_factory = sqlite3.Row

            # ── Discover schema ────────────────────────────────────────────────
            tables = {
                row[0] for row in
                ch_conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            }

            # Kolibri channel DB table names vary by version:
            # v0.13+: content_contentnode
            # Older:  contentnode
            node_table = None
            for candidate in ("content_contentnode", "contentnode"):
                if candidate in tables:
                    node_table = candidate
                    break

            if not node_table:
                log.warning(f"    No content node table found in {db_file.name}. Tables: {tables}")
                ch_conn.close()
                continue

            # ── Get channel name ───────────────────────────────────────────────
            channel_name = db_file.stem[:32]
            if "content_channelmetadata" in tables:
                meta = ch_conn.execute(
                    "SELECT name FROM content_channelmetadata LIMIT 1"
                ).fetchone()
                if meta:
                    channel_name = meta["name"]
            elif "channelmetadata" in tables:
                meta = ch_conn.execute(
                    "SELECT name FROM channelmetadata LIMIT 1"
                ).fetchone()
                if meta:
                    channel_name = meta["name"]

            log.info(f"    Channel: {channel_name}")

            # ── Discover available columns ─────────────────────────────────────
            cols = {
                row[1] for row in
                ch_conn.execute(f"PRAGMA table_info({node_table})")
            }

            # Build SELECT dynamically based on available columns
            select_cols = ["id", "title", "kind"]
            optional = {
                "description": "description",
                "available": "available",
                "lang_id": "lang_id",
                "content_id": "content_id",
                "channel_id": "channel_id",
                "coach_content": "coach_content",
            }
            for col, alias in optional.items():
                if col in cols:
                    select_cols.append(col)

            sql = f"SELECT {', '.join(select_cols)} FROM {node_table}"
            # Skip topics (navigation nodes) — usually not useful for lesson resource matching
            # but keep them if that's all there is
            rows = ch_conn.execute(sql).fetchall()

            log.info(f"    {len(rows)} content nodes found")
            channel_stats: Counter = Counter()

            for row in rows:
                d = dict(row)
                kolibri_kind = d.get("kind", "")
                content_type = kind_map.get(kolibri_kind, kolibri_kind or "other")

                title = (d.get("title") or "").strip()
                description = (d.get("description") or "").strip()
                if not title:
                    continue

                node_id = d.get("content_id") or d.get("id") or ""
                available = int(d.get("available", 1))

                # Build a logical path for this content node
                logical_path = f"{db_file.stem}/{kolibri_kind}/{node_id}"

                subject = classify_subject(
                    f"{title} {description}", logical_path, subject_kw
                )

                keywords_str = ""
                if do_kw:
                    kws = extract_keywords(f"{title} {description}", kw_count)
                    keywords_str = ", ".join(kws)

                # Try to find the actual file on disk
                # Kolibri stores files as: content/storage/<a>/<b>/<hash>.<ext>
                file_path = _find_kolibri_file(root, node_id)

                upsert_content(conn, {
                    "source": "kolibri",
                    "path": logical_path,
                    "filename": f"{node_id[:8]}...{node_id[-4:]}",
                    "content_type": content_type,
                    "title": title,
                    "description": description,
                    "subject": subject,
                    "module": channel_name,
                    "size_bytes": file_path.stat().st_size if file_path else None,
                    "duration_seconds": None,
                    "transcript_path": None,
                    "transcript_text": None,
                    "extracted_text": "",
                    "keywords": keywords_str,
                    "zim_file": None,
                    "article_count": None,
                    "kolibri_id": str(node_id),
                    "kolibri_channel": channel_name,
                    "kolibri_kind": kolibri_kind,
                    "kolibri_available": available,
                    "last_scanned": now_str,
                })
                stats["indexed"] += 1
                channel_stats[content_type] += 1

            log.info(f"    Indexed: {dict(channel_stats)}")
            ch_conn.close()

            if stats["indexed"] % 500 == 0:
                conn.commit()

        except Exception as e:
            stats["errors"] += 1
            log.error(f"  [Kolibri] Error reading {db_file.name}: {e}")
            import traceback; traceback.print_exc()

    conn.commit()
    log.info(f"  [Kolibri] Done. DBs={stats['scanned']} Indexed={stats['indexed']} Errors={stats['errors']}")
    return stats


def _find_kolibri_file(kolibri_root: Path, content_id: str) -> Path | None:
    """
    Kolibri stores files at content/storage/<a>/<b>/<content_id>.<ext>
    where <a> and <b> are the first two hex chars of content_id.
    """
    if not content_id or len(content_id) < 2:
        return None
    storage = kolibri_root / "content" / "storage" / content_id[0] / content_id[1]
    if storage.exists():
        # Find any file starting with this content_id
        matches = list(storage.glob(f"{content_id}.*"))
        if matches:
            return matches[0]
    return None


# ══════════════════════════════════════════════════════════════════════════════
# Module summary updater
# ══════════════════════════════════════════════════════════════════════════════

def update_module_summary(conn: sqlite3.Connection) -> None:
    """Rebuild the modules summary table from current content."""
    conn.execute("DELETE FROM modules")
    rows = conn.execute(
        """
        SELECT module, source,
               COUNT(*) AS total,
               SUM(CASE WHEN content_type='video' THEN 1 ELSE 0 END) AS videos,
               SUM(CASE WHEN content_type='pdf'   THEN 1 ELSE 0 END) AS pdfs,
               SUM(CASE WHEN content_type='html'  THEN 1 ELSE 0 END) AS htmls,
               SUM(CASE WHEN content_type='exercise' THEN 1 ELSE 0 END) AS exercises,
               GROUP_CONCAT(DISTINCT subject) AS subjects
        FROM content
        GROUP BY module, source
        """
    ).fetchall()
    for r in rows:
        conn.execute(
            """
            INSERT INTO modules (name, source, content_count, video_count, pdf_count, html_count, exercise_count, subjects)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (r["module"], r["source"], r["total"], r["videos"], r["pdfs"],
             r["htmls"], r["exercises"], r["subjects"]),
        )
    conn.commit()


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Scan ARES content (web + Kiwix + Kolibri) and build a unified index."
    )
    parser.add_argument("--config", "-c", default="ares_scan_config.yaml")
    parser.add_argument(
        "--source",
        choices=["web", "kiwix", "kolibri", "all"],
        default="all",
        help="Which source to scan (default: all)",
    )
    parser.add_argument(
        "--fast", action="store_true",
        help="Skip text extraction from HTML/PDF (faster, less searchable)",
    )
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    db_path  = config.get("output_db", "ares_content.db")
    log_file = config.get("log_file", "scan.log")
    json_dir = config.get("output_json_dir", "")

    os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout),
        ],
    )
    log = logging.getLogger("ares_scan")

    conn = init_db(db_path)
    now_str = datetime.utcnow().isoformat()
    total_stats = {"scanned": 0, "indexed": 0, "errors": 0}

    sources = config.get("content_sources", [])
    for source_cfg in sources:
        source_type = source_cfg.get("type", "web")
        source_name = source_cfg.get("name", source_type)

        if args.source != "all" and source_type != args.source:
            continue

        run_id = conn.execute(
            "INSERT INTO scan_runs (started_at, source, root_path) VALUES (?, ?, ?)",
            (now_str, source_type, source_cfg["path"]),
        ).lastrowid
        conn.commit()

        if source_type == "web":
            stats = scan_web(source_cfg, config, conn, log, fast=args.fast)
        elif source_type == "kiwix":
            stats = scan_kiwix(source_cfg, config, conn, log)
        elif source_type == "kolibri":
            stats = scan_kolibri(source_cfg, config, conn, log)
        else:
            log.warning(f"Unknown source type '{source_type}' for '{source_name}' — skipping")
            continue

        conn.execute(
            """UPDATE scan_runs SET finished_at=?, files_scanned=?, files_indexed=?, errors=?
               WHERE id=?""",
            (datetime.utcnow().isoformat(),
             stats["scanned"], stats["indexed"], stats["errors"], run_id),
        )
        conn.commit()

        for k in total_stats:
            total_stats[k] += stats.get(k, 0)

    log.info("Rebuilding module summary...")
    update_module_summary(conn)

    # JSON export
    if json_dir:
        os.makedirs(json_dir, exist_ok=True)
        total = conn.execute("SELECT COUNT(*) FROM content").fetchone()[0]
        by_source = conn.execute(
            "SELECT source, COUNT(*) n FROM content GROUP BY source"
        ).fetchall()
        summary = {
            "scan_date": now_str,
            "total_items": total,
            "by_source": {r["source"]: r["n"] for r in by_source},
            "stats": total_stats,
        }
        with open(os.path.join(json_dir, "scan_summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

    conn.close()

    log.info("═" * 60)
    log.info("SCAN COMPLETE")
    log.info(f"  Total scanned : {total_stats['scanned']:,}")
    log.info(f"  Total indexed : {total_stats['indexed']:,}")
    log.info(f"  Total errors  : {total_stats['errors']:,}")
    log.info(f"  Database      : {db_path}")
    log.info("═" * 60)


if __name__ == "__main__":
    main()
