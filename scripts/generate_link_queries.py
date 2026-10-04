#!/usr/bin/env python3
"""
generate_link_queries.py — ARES-style search phrases per lesson
===============================================================
Retrieval was driven by the lesson's aresKeywords, which are written for teachers,
not for a library whose titles look like "Position vs. time graphs" or "Finding
speed when objects travel in opposite directions". A model writes 6 short phrases
per lesson in that style (with US/UK wording variants). They are cached in
config/link_queries.json and widen the matcher's retrieval and relevance gate
(src/ares_recommender.py LessonQuery). They never decide what is SHOWN: the
independent judge does (scripts/judge_links.py, scripts/judge_candidates.py).

  python3 scripts/generate_link_queries.py [--workers 4] [--dry-run]
~$0.006 per lesson; skips lessons already in the cache.
"""
import argparse
import glob
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import ares_recommender as ar  # noqa: E402

SCHEMA = {"type": "object", "additionalProperties": False,
          "properties": {"phrases": {"type": "array", "items": {"type": "string"}}},
          "required": ["phrases"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    path = Path(ar._QUERIES_PATH)
    cache = ar.load_queries()
    jobs = []
    for f in sorted(glob.glob(str(ROOT / "data/outputs/v2/**/*_data.json"), recursive=True)):
        if "/PDF/" in f:
            continue
        d = json.load(open(f))
        subj, grade = d["META"]["subject"], d["META"].get("grade", "")
        for L in d["LESSONS"]:
            topic = ar.strip_substrand_label(L.get("substrand", ""))
            k = ar.query_key(subj, topic, L.get("title", ""))
            if k not in cache:
                jobs.append((k, subj, grade, topic, L))
    print(f"{len(jobs)} lesson(s) need queries; est ~${len(jobs) * 0.006:.2f}")
    if a.dry_run or not jobs:
        return 0
    import generate_substrand as g

    def work(job):
        k, subj, grade, topic, L = job
        prompt = f"""A teacher's lesson needs videos and readings from an offline library of Khan Academy, CK-12, PhET, TED-Ed and Kenyan school (KICD) resources. Their TITLES look like "Position vs. time graphs", "Average velocity and average speed from graphs", "Finding speed when objects travel in opposite directions", "Intro to vectors and scalars".

Grade {grade} {subj}, sub-strand: {topic}
Lesson {L.get('number')}: {L.get('title')}
Keywords: {L.get('aresKeywords', '')}
Overview: {(L.get('overview') or '')[:800]}

Write 6 short search phrases (2-4 words each) in the style of those library titles, covering the lesson's SPECIFIC concepts and skills (what a student must learn), including a US-textbook wording variant where the Kenyan term differs (e.g. gradient/slope, enlargement/dilation). Do NOT include classroom activity words (practical, discussion, model building, driving question), Kenyan place names, or single generic words like "motion" or "graph" alone."""
        r = g.call_claude(prompt, schema=SCHEMA)
        return k, (r or {}).get("phrases")

    n = 0
    with ThreadPoolExecutor(a.workers) as ex:
        for fut in as_completed([ex.submit(work, j) for j in jobs]):
            k, ph = fut.result()
            if ph:
                cache[k] = [p.strip().lower() for p in ph if p.strip()][:8]
                n += 1
                if n % 50 == 0:
                    path.write_text(json.dumps({"version": 1, "queries": dict(sorted(cache.items()))}, indent=0, ensure_ascii=False))
                    print(f"  {n}/{len(jobs)}")
    path.write_text(json.dumps({"version": 1, "queries": dict(sorted(cache.items()))}, indent=0, ensure_ascii=False))
    print(f"Wrote {n} lesson query sets ({len(cache)} total). Estimated spend: ${g._estimate_cost():.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
