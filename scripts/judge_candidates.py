#!/usr/bin/env python3
"""
judge_candidates.py — judge the matcher's TOP CANDIDATES, not just what it picked
=================================================================================
scripts/judge_links.py only judges links already shown. The matcher ranks by
keyword score, so a good resource ranked 4th is never seen. This enumerates each
lesson's top candidates (video and reading) that passed the matcher's gate, has
the independent judge rule on them (title + source + short description), and
stores the verdicts in config/link_judgments.json. The matcher then PREFERS
verified fits, uses partial only when nothing fits, and shows nothing otherwise.

  python3 scripts/judge_candidates.py [--top 10] [--rounds 2] [--workers 4] [--dry-run]

Round 2 looks deeper for lessons that still have fewer than 3 usable
(non-off-topic) candidates in a kind. Run scripts/generate_link_queries.py first
(wider retrieval), and re-render afterwards (node generators/generate.js --all).
"""
import argparse
import glob
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import ares_recommender as ar  # noqa: E402
from judge_links import SCHEMA, save  # noqa: E402

DB = ROOT / "data" / "ares_index" / "ares_content.db"


def lessons():
    for f in sorted(glob.glob(str(ROOT / "data/outputs/v2/**/*_data.json"), recursive=True)):
        if "/PDF/" in f:
            continue
        d = json.load(open(f))
        for L in d["LESSONS"]:
            yield d["META"]["subject"], d["META"].get("grade", ""), L


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    import generate_substrand as g

    rec = ar.AresRecommender(str(DB))
    if not rec._ready:
        sys.exit("ARES content DB not usable")
    judgments = ar.load_judgments()
    all_l = list(lessons())

    def collect(round_no):
        jobs = []
        for subj, grade, L in all_l:
            topic = ar.strip_substrand_label(L.get("substrand", ""))
            q = ar.LessonQuery(L.get("substrand", ""), L.get("aresKeywords") or L.get("title", ""),
                               L.get("title", ""), subj, rec.cfg)
            todo = []
            for kind in ("video", "reading"):
                passed, _ = rec._candidates(q, kind)
                usable = [c for c in passed if judgments.get(ar.judgment_key(subj, topic, L["title"], c["title"])) != "off_topic"]
                judged_ok = [c for c in usable if c["title"] and ar.judgment_key(subj, topic, L["title"], c["title"]) in judgments]
                if round_no > 1 and len(judged_ok) >= 3:
                    continue
                depth = a.top * round_no
                for c in usable[:depth]:
                    k = ar.judgment_key(subj, topic, L["title"], c["title"])
                    if k not in judgments and all(c["title"] != t[0] for t in todo):
                        r = c["row"]
                        todo.append((c["title"], kind, str(r["source"] or ""), str(r["description"] or "")[:220]))
            if todo:
                jobs.append((subj, grade, topic, L, todo))
        return jobs

    def judge(job):
        subj, grade, topic, L, todo = job
        listing = "\n".join(f"{i}. [{kind}, {src}] {t} — {desc}" for i, (t, kind, src, desc) in enumerate(todo))
        prompt = f"""You are checking resources linked to a Kenyan CBE Grade {grade} lesson. Judge each by its title and description as a teacher would.

Subject: {subj} - {topic}
Lesson {L.get('number')}: {L.get('title')}
Keywords: {L.get('aresKeywords', '')}
Overview: {(L.get('overview') or '')[:700]}

Resources:
{listing}

"fits" = a teacher would plausibly use it for THIS lesson's content at Grade {grade} level; "partial" = right broad topic but the wrong specific topic or an unsuitable level; "off_topic" = a different topic or subject, or clearly far beyond the lesson. Be strict. "why": at most 10 words."""
        r = g.call_claude(prompt, schema=SCHEMA)
        return job, (r or {}).get("verdicts")

    for rnd in range(1, a.rounds + 1):
        jobs = collect(rnd)
        n_titles = sum(len(j[4]) for j in jobs)
        print(f"round {rnd}: {len(jobs)} lesson(s), {n_titles} candidate titles to judge; est ~${n_titles * 0.0012:.2f}")
        if a.dry_run or not jobs:
            if a.dry_run:
                return 0
            break
        done = 0
        with ThreadPoolExecutor(a.workers) as ex:
            for fut in as_completed([ex.submit(judge, j) for j in jobs]):
                (subj, grade, topic, L, todo), verdicts = fut.result()
                if not verdicts:
                    print(f"  FAILED {subj} {topic} L{L.get('number')}")
                    continue
                for v in verdicts:
                    if 0 <= v["id"] < len(todo):
                        judgments[ar.judgment_key(subj, topic, L.get("title", ""), todo[v["id"]][0])] = v["verdict"]
                done += 1
                if done % 40 == 0:
                    save(judgments)
                    print(f"  {done}/{len(jobs)}")
        save(judgments)
        rec._judgments = dict(judgments)
    from collections import Counter
    print("Cache:", dict(Counter(judgments.values())))
    print(f"Estimated spend this run: ${g._estimate_cost():.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
