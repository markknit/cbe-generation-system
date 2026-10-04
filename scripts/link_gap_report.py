#!/usr/bin/env python3
"""
link_gap_report.py — which lessons have no verified-fit resource in ARES?
=========================================================================
After the matcher and the independent judge have done their best with the
library as it is, any lesson still without a "fits" link is a CONTENT GAP: more
tuning cannot fix it, adding material can. Reads the rendered *_data.json files
and config/link_judgments.json; writes logs/link_gaps.md (and prints a summary).

  python3 scripts/link_gap_report.py
"""
import glob
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import ares_recommender as ar  # noqa: E402


def main():
    j = ar.load_judgments()
    rows = defaultdict(list)
    tot = none = only_partial = fits_any = 0
    for f in sorted(glob.glob(str(ROOT / "data/outputs/v2/**/*_data.json"), recursive=True)):
        if "/PDF/" in f:
            continue
        d = json.load(open(f))
        subj = d["META"]["subject"]
        grade = d["META"].get("grade", "")
        for L in d["LESSONS"]:
            topic = ar.strip_substrand_label(L.get("substrand", ""))
            titles = {}
            for ph in (L.get("resourceLinks") or {}).values():
                for k in ("video", "reading"):
                    r = (ph or {}).get(k)
                    if r:
                        titles[r["title"]] = j.get(ar.judgment_key(subj, topic, L["title"], r["title"]), "unjudged")
            tot += 1
            v = set(titles.values())
            if "fits" in v:
                fits_any += 1
                continue
            if not titles:
                none += 1
                status = "NO LINKS"
            else:
                only_partial += 1
                status = f"only partial ({len(titles)})"
            rows[(f"Grade {grade}", subj, topic)].append((L["number"], L["title"], L.get("aresKeywords", ""), status))
    lines = ["# Content gaps: lessons with no verified-fit ARES resource", "",
             f"{tot} lessons. With at least one verified fit: **{fits_any}** ({100*fits_any//tot}%). "
             f"Only partial matches: **{only_partial}**. No links at all: **{none}**.", "",
             "Each lesson below needs new library content for its topic; keywords show what to look for.", ""]
    for (grade, subj, topic), items in sorted(rows.items()):
        lines.append(f"## {grade} {subj}: {topic} ({len(items)} lesson(s))")
        for n, t, kw, st in items:
            lines.append(f"- L{n} **{t[:90]}** — {st}. Keywords: {kw[:140]}")
        lines.append("")
    (ROOT / "logs" / "link_gaps.md").write_text("\n".join(lines))
    print(lines[2])


if __name__ == "__main__":
    main()
