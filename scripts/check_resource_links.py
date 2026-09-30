#!/usr/bin/env python3
"""
check_resource_links.py — pipeline gate for resource links (all phases, all slots)
===================================================================================
Runs automatically at the end of every `generate.js` render, and on demand over
the whole corpus. Shares config/link_matching.yaml with src/ares_recommender.py,
so the rule that produces a link and the rule that checks it cannot drift.
Design: DESIGN_link_selection_v2.md §4.7.

HARD FAILURES (exit 1):
  T1  answer/exam material in a slot          (config exclude_patterns)
  T2  foreign-subject vocabulary in a title with no overlap with the lesson
  DEAD direct_url does not resolve on the reference ARES image
       (Kolibri node missing/unavailable, or web module file missing)
  SHAPE _data.json fails ares-contract.schema.json (needs `jsonschema`; falls
       back to a resourceLinks shape check, with a warning, if not installed)

WARNINGS (reported, exit 0):
  same resource in >= 3 phases of one lesson; a title reused >= 6 times across
  the files checked; per-subject fill rate; reference image not mounted.

Usage:
  python3 scripts/check_resource_links.py                    # whole corpus
  python3 scripts/check_resource_links.py path/to/X_data.json [...]
  python3 scripts/check_resource_links.py data/outputs/v2/Physics
  --quiet   only the summary and failures
"""
import glob
import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from urllib.parse import unquote, urlparse, parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import ares_recommender as ar  # noqa: E402

PHASES = ("predict", "observe", "explain", "dqb", "model")
SLOTS = ("video", "reading")
SCHEMA = os.path.join(ROOT, "ares-contract.schema.json")


def find_json(args: list[str]) -> list[str]:
    targets = args or [os.path.join(ROOT, "data", "outputs", "v2")]
    out = []
    for t in targets:
        if os.path.isdir(t):
            # Walks both the flat Grade 10 tree (v2/<Subject>/<SS>/) and
            # grade-segmented trees (v2/Grade<N>/<Subject>/<SS>/). The PDF
            # mirror holds no JSON, so it is naturally skipped.
            out += glob.glob(os.path.join(t, "**", "*_data.json"), recursive=True)
        else:
            out.append(t)
    return sorted(set(out))


class Reference:
    """What exists on the reference ARES image (see config)."""

    def __init__(self, cfg: dict):
        self.warnings = []
        ref = os.environ.get("KOLIBRI_REFERENCE_DB") or cfg.get("kolibri_reference_db")
        self.kolibri = None
        if ref and os.path.exists(ref):
            k = sqlite3.connect(f"file:{ref}?immutable=1", uri=True)
            self.kolibri = {r[0]: r[1] for r in k.execute("SELECT id, available FROM content_contentnode")}
        else:
            self.warnings.append(f"Kolibri reference DB not found ({ref}): Kolibri links not verified")
        web = os.environ.get("WEB_MODULES_REFERENCE_ROOT") or cfg.get("web_modules_reference_root")
        self.web_root = web if web and os.path.isdir(web) else None
        if not self.web_root:
            self.warnings.append(f"web modules reference root not found ({web}): web links not verified")

    def dead_reason(self, url: str) -> str:
        if not url:
            return "empty direct_url"
        u = urlparse(url)
        if ":8069" in u.netloc or "/learn/" in u.path:
            node = url.rstrip("/").rsplit("/", 1)[-1]
            if self.kolibri is None:
                return ""
            if node not in self.kolibri:
                return f"kolibri node {node} not on reference image"
            if not self.kolibri[node]:
                return f"kolibri node {node} content not downloaded (available=0)"
            return ""
        if "kiwix_launch" in u.path:
            target = unquote(parse_qs(u.query).get("target", [""])[0])
            if target.startswith("/modules/"):
                if self.web_root is None:
                    return ""
                p = os.path.join(self.web_root, target[len("/modules/"):])
                return "" if os.path.exists(p) else f"web module file missing: {target}"
            return "kiwix article link (cannot be verified; not an eligible source)"
        if "/KICD_Educhannel/" in u.path:
            if self.web_root is None:
                return ""
            base = os.path.dirname(self.web_root)
            rel = unquote(u.path).lstrip("/")
            ok = os.path.exists(os.path.join(base, "html", rel)) or os.path.exists(os.path.join(base, rel))
            return "" if ok else f"KICD file missing: {rel}"
        return f"unrecognised link form: {url[:60]}"


def schema_validator():
    try:
        import jsonschema
    except ImportError:
        return None
    with open(SCHEMA) as f:
        return jsonschema.Draft202012Validator(json.load(f))


def shape_errors_fallback(d: dict) -> list[str]:
    keys = {"title", "source", "content_type", "direct_url", "search_url", "search_terms",
            "exact_search_url", "has_transcript", "tier"}
    errs = []
    for L in d.get("LESSONS", []):
        rl = L.get("resourceLinks")
        if not isinstance(rl, dict) or set(rl) != set(PHASES):
            errs.append(f"L{L.get('number')}: resourceLinks phases {sorted(rl or {})}")
            continue
        for ph in PHASES:
            pr = rl[ph]
            if set(pr) != {"video", "reading", "fallback_search_url"} or \
                    not str(pr.get("fallback_search_url", "")).startswith("http"):
                errs.append(f"L{L['number']} {ph}: bad phase object")
            for s in SLOTS:
                r = pr.get(s)
                if r is not None and set(r) != keys:
                    errs.append(f"L{L['number']} {ph}.{s}: keys {sorted(set(r) ^ keys)}")
    return errs


def lesson_words(L: dict, cfg: dict) -> set[str]:
    q = ar.LessonQuery(L.get("substrand", ""), L.get("aresKeywords") or L.get("title", ""),
                       L.get("title", ""), "", cfg)
    words = set()
    for t in q.core_topics:
        words |= t
    for _, w, _ in q.gate_phrases:
        words |= w
    return words


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    args = [a for a in argv if not a.startswith("--")]
    cfg = ar.load_link_config()
    ref = Reference(cfg)
    validator = schema_validator()
    files = find_json(args)
    if not files:
        print("check_resource_links: no *_data.json found")
        return 1

    fails: list[str] = []
    warns: list[str] = list(ref.warnings)
    if validator is None:
        warns.append("jsonschema not installed: contract check limited to resourceLinks shape")
    title_uses = Counter()
    title_where = defaultdict(set)
    fill = defaultdict(lambda: [0, 0])  # subject -> [filled, total]
    counts = Counter()

    for fp in files:
        rel = os.path.relpath(fp, ROOT)
        with open(fp) as f:
            d = json.load(f)
        subject = d.get("META", {}).get("subject", "?")
        errs = ([e.message for e in validator.iter_errors(d)] if validator else shape_errors_fallback(d))
        for e in errs[:5]:
            fails.append(f"SHAPE {rel}: {e[:160]}")
        counts["SHAPE"] += len(errs)
        for L in d.get("LESSONS", []):
            rl = L.get("resourceLinks") or {}
            words = lesson_words(L, cfg)
            per_lesson = Counter()
            for ph in PHASES:
                for s in SLOTS:
                    r = (rl.get(ph) or {}).get(s)
                    fill[subject][1] += 1
                    if not r:
                        continue
                    fill[subject][0] += 1
                    title = r.get("title", "")
                    where = f"{rel} L{L.get('number')} {ph}.{s}"
                    title_uses[title] += 1
                    title_where[title].add(subject)
                    per_lesson[(s, title)] += 1
                    if cfg["_exclude_re"].search(title):
                        fails.append(f"T1 {where}: answer/exam material {title!r}")
                        counts["T1"] += 1
                    foreign = ar.foreign_vocab_hits(title, subject, cfg)
                    if foreign and not ({ar._norm(t) for t in ar._tokens(title)} & words):
                        fails.append(f"T2 {where}: foreign vocabulary {foreign} in {title!r}")
                        counts["T2"] += 1
                    dead = ref.dead_reason(r.get("direct_url", ""))
                    if dead:
                        fails.append(f"DEAD {where}: {dead} ({title!r})")
                        counts["DEAD"] += 1
            for (s, title), n in per_lesson.items():
                if n >= 3:
                    counts["REPEAT_IN_LESSON"] += 1
                    if not quiet:
                        warns.append(f"repeat: {rel} L{L.get('number')} {s} {title!r} in {n} phases")

    for title, n in title_uses.most_common():
        if n < 6:
            break
        counts["HIGH_REUSE_TITLES"] += 1
        if not quiet:
            warns.append(f"reuse: {title!r} x{n} across {sorted(title_where[title])}")

    print(f"check_resource_links: {len(files)} file(s)")
    print(f"  hard failures: T1={counts['T1']}  T2={counts['T2']}  DEAD={counts['DEAD']}  SHAPE={counts['SHAPE']}")
    print(f"  warnings: same resource in 3+ phases of a lesson={counts['REPEAT_IN_LESSON']}  "
          f"titles reused 6+ times={counts['HIGH_REUSE_TITLES']}")
    print("  fill rate (slots with a direct match / all slots):")
    for subj, (f_, t) in sorted(fill.items()):
        print(f"    {subj:<24} {f_:>5}/{t:<5} {100 * f_ / t:5.1f}%")
    for w in warns[: (10 if quiet else 60)]:
        print(f"  WARN {w}")
    for x in fails[:200]:
        print(f"  FAIL {x}")
    if len(fails) > 200:
        print(f"  ... {len(fails) - 200} more failures")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
