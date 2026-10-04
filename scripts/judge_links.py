#!/usr/bin/env python3
"""
judge_links.py — independent relevance verdicts for linked resources
====================================================================
The matcher's gate is keyword-based, so it lets through links that share a
word with the lesson but not its topic ("Time dilation" on similar solids).
The 2026-10-03 audit measured the matcher at 15% off-topic. This adds an
independent check: a model (claude-sonnet-5-5) reads each lesson's context and
the TITLES of the resources linked to it, and rules fits / partial / off_topic.

Verdicts are cached in config/link_judgments.json (committed), keyed by
(subject, sub-strand, lesson title, resource title). The matcher then REFUSES
any resource cached as off_topic for that lesson, and the link gate (T4) fails
if one is shipped. Only off_topic is acted on; "partial" is kept.

Loop until nothing new is judged (each pass judges only titles with no verdict):
    python3 scripts/judge_links.py          # judge what is currently linked
    node generators/generate.js --all       # matcher now skips off-topic, picks next best
    python3 scripts/judge_links.py          # judge the replacements; repeat to 0 new

  --only subj/dir-substring   limit to matching *_data.json paths
  --workers N                 parallel calls (default 4)
  --dry-run                   count what would be judged and estimate cost
~$0.012 per lesson with unjudged titles.
"""
import argparse
import glob
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import ares_recommender as ar  # noqa: E402

CACHE = Path(ar._JUDGMENTS_PATH)
SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {"verdicts": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "properties": {"id": {"type": "integer"},
                       "verdict": {"type": "string", "enum": ["fits", "partial", "off_topic"]},
                       "why": {"type": "string"}},
        "required": ["id", "verdict", "why"]}}},
    "required": ["verdicts"],
}
_lock = threading.Lock()


def lesson_titles(L: dict) -> list[str]:
    seen, out = set(), []
    for d in (L.get("resourceLinks") or {}).values():
        for r in (d or {}).values():
            if isinstance(r, dict) and r.get("title") and r["title"] not in seen:
                seen.add(r["title"])
                out.append(r["title"])
    return out


def save(judgments: dict) -> None:
    with _lock:
        tmp = CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps({"version": 1, "judgments": dict(sorted(judgments.items()))},
                                  indent=0, ensure_ascii=False))
        os.replace(tmp, CACHE)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    judgments = ar.load_judgments()
    jobs = []
    for f in sorted(glob.glob(str(ROOT / "data/outputs/v2/**/*_data.json"), recursive=True)):
        if "/PDF/" in f or (a.only and a.only not in f):
            continue
        d = json.load(open(f))
        subj, grade = d["META"]["subject"], d["META"].get("grade", "")
        for L in d["LESSONS"]:
            topic = ar.strip_substrand_label(L.get("substrand", ""))
            todo = [t for t in lesson_titles(L)
                    if ar.judgment_key(subj, topic, L.get("title", ""), t) not in judgments]
            if todo:
                jobs.append((subj, grade, topic, L, todo))
    n_titles = sum(len(j[4]) for j in jobs)
    print(f"{len(jobs)} lesson(s) with unjudged links, {n_titles} titles; est ~${len(jobs) * 0.012:.2f}")
    if a.dry_run or not jobs:
        return 0

    import generate_substrand as g

    def work(job):
        subj, grade, topic, L, todo = job
        listing = "\n".join(f"{i}. {t}" for i, t in enumerate(todo))
        prompt = f"""You are checking resources linked to a Kenyan CBE Grade {grade} lesson. Judge each resource by TITLE only, as a teacher scanning a list would.

Subject: {subj} - {topic}
Lesson {L.get('number')}: {L.get('title')}
Keywords: {L.get('aresKeywords', '')}
Overview: {(L.get('overview') or '')[:700]}

Resources:
{listing}

For each, "fits" = a teacher would plausibly use it for THIS lesson's content at Grade {grade} level; "partial" = right broad topic but the wrong specific topic or an unsuitable level; "off_topic" = a different topic or subject, or clearly far beyond the lesson. Be strict. One-line "why"."""
        r = g.call_claude(prompt, schema=SCHEMA)
        return job, (r or {}).get("verdicts")

    done = off = 0
    with ThreadPoolExecutor(a.workers) as ex:
        for fut in as_completed([ex.submit(work, j) for j in jobs]):
            (subj, grade, topic, L, todo), verdicts = fut.result()
            if not verdicts:
                print(f"  FAILED {subj} {topic} L{L.get('number')}")
                continue
            for v in verdicts:
                if 0 <= v["id"] < len(todo):
                    judgments[ar.judgment_key(subj, topic, L.get("title", ""), todo[v["id"]])] = v["verdict"]
                    off += v["verdict"] == "off_topic"
            done += 1
            if done % 25 == 0:
                save(judgments)
                print(f"  {done}/{len(jobs)} lessons judged")
    save(judgments)
    print(f"Judged {done} lesson(s); {off} new off_topic verdict(s). Cache: {len(judgments)} entries.")
    print(f"Estimated spend this run: ${g._estimate_cost():.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
