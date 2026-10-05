#!/usr/bin/env python3
"""
judge_via_agents.py — link-relevance judging done in Claude Code instead of the API
===================================================================================
Same job as scripts/judge_candidates.py (rule fits / partial / off_topic on the
matcher's candidate resources per lesson) but the judging is done by Claude Code
agents reading JSON files, so it costs plan usage instead of API dollars.

  python3 scripts/judge_via_agents.py export OUTDIR [--top 10] [--chunks 8]
      Writes OUTDIR/chunk_N.json: {"lessons": [{"subject","grade","topic","lesson","title",
      "keywords","overview","items":[{"key","title","kind","source","desc","verdict":null}]}]}.
      Only candidates with no verdict in config/link_judgments.json are included.
  python3 scripts/judge_via_agents.py import OUTDIR
      Reads every OUTDIR/chunk_N.judged.json (same shape, "verdict" filled with
      fits | partial | off_topic) and merges them into config/link_judgments.json.

Verdict definitions (same as the API judge): fits = a teacher would plausibly use it
for THIS lesson's content at the grade level; partial = right broad topic but the
wrong specific topic or an unsuitable level; off_topic = a different topic or
subject, or clearly far beyond the lesson. Be strict.
"""
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
import ares_recommender as ar  # noqa: E402

DB = ROOT / "data" / "ares_index" / "ares_content.db"


def export(outdir: Path, top: int, chunks: int):
    outdir.mkdir(parents=True, exist_ok=True)
    rec = ar.AresRecommender(str(DB))
    if not rec._ready:
        sys.exit("ARES content DB not usable")
    judgments = ar.load_judgments()
    lessons = []
    for f in sorted(glob.glob(str(ROOT / "data/outputs/v2/**/*_data.json"), recursive=True)):
        if "/PDF/" in f:
            continue
        d = json.load(open(f))
        subj, grade = d["META"]["subject"], d["META"].get("grade", "")
        for L in d["LESSONS"]:
            topic = ar.strip_substrand_label(L.get("substrand", ""))
            q = ar.LessonQuery(L.get("substrand", ""), L.get("aresKeywords") or L.get("title", ""),
                               L.get("title", ""), subj, rec.cfg)
            items, seen = [], set()
            for kind in ("video", "reading"):
                passed, _ = rec._candidates(q, kind)
                usable = [c for c in passed
                          if judgments.get(ar.judgment_key(subj, topic, L["title"], c["title"])) != "off_topic"]
                for c in usable[:top]:
                    k = ar.judgment_key(subj, topic, L["title"], c["title"])
                    if k in judgments or k in seen:
                        continue
                    seen.add(k)
                    r = c["row"]
                    items.append({"key": k, "title": c["title"], "kind": kind, "source": str(r["source"] or ""),
                                  "desc": str(r["description"] or "")[:220], "verdict": None})
            if items:
                lessons.append({"subject": subj, "grade": grade, "topic": topic, "lesson": L.get("number"),
                                "title": L.get("title", ""), "keywords": L.get("aresKeywords", ""),
                                "overview": (L.get("overview") or "")[:600], "items": items})
    n_items = sum(len(x["items"]) for x in lessons)
    per = max(1, -(-len(lessons) // chunks))
    for i in range(chunks):
        part = lessons[i * per:(i + 1) * per]
        if part:
            (outdir / f"chunk_{i + 1}.json").write_text(json.dumps({"lessons": part}, ensure_ascii=False, indent=1))
    print(f"{len(lessons)} lessons, {n_items} candidate resources -> {outdir} ({chunks} chunks)")


def import_(outdir: Path):
    judgments = ar.load_judgments()
    n = bad = 0
    from judge_links import save
    for f in sorted(glob.glob(str(outdir / "chunk_*.judged.json"))):
        for L in json.load(open(f))["lessons"]:
            for it in L["items"]:
                v = it.get("verdict")
                if v in ("fits", "partial", "off_topic"):
                    judgments[it["key"]] = v
                    n += 1
                else:
                    bad += 1
    save(judgments)
    from collections import Counter
    print(f"merged {n} verdicts ({bad} items had none). Cache now {len(judgments)}: {dict(Counter(judgments.values()))}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("export", "import"):
        sys.exit(__doc__)
    outdir = Path(a[1])
    if a[0] == "export":
        top = int(a[a.index("--top") + 1]) if "--top" in a else 10
        chunks = int(a[a.index("--chunks") + 1]) if "--chunks" in a else 8
        export(outdir, top, chunks)
    else:
        import_(outdir)
