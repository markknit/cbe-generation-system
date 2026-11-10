#!/usr/bin/env python3
"""
fe_vs_lessons_check.py — does each revised Final Explanation (FE) still match its revised lessons?  (free, local, no API)

Round 2 changed lessons (trims, splits, replaced lessons, science and fact fixes) and the FE only where a reviewer touched it.
This compares, per module, the BASELINE lessons, the REVISED lessons and the REVISED FE (rubric excluded):

  REMOVED   a number or proper noun that was in the baseline lessons, is gone from the revised lessons, and is STILL in
            the FE: the FE probably refers to content that no longer exists (strongest signal)
  LESSONREF the FE says "Lesson N": listed when the lesson numbering of the module changed (splits, replaced lessons),
            or when N is larger than the lesson count; the teacher must check that Lesson N is still the lesson meant
  MINUTES   the FE still mentions an 80-minute lesson
  TITLEREF  an FE reference like 'Lesson N' whose baseline lesson title shares no words with the revised lesson N title

  CBE_REVISED_DIR=data/revised_2026-10_full venv/bin/python scripts/round2/fe_vs_lessons_check.py [module ...] [--json OUT.json]

Heuristic: it finds candidates for a human or model to check; it cannot judge science or arithmetic.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REV = Path(os.environ["CBE_REVISED_DIR"])


def load(path):
    out = subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


NUM = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?(?![\w])")
NAME = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{3,}\b")
STOP = set("Lesson Part Explain Describe Calculate Predict Observe Model Table Figure Day Week Grade Question Answer Section Then That This When What Where Which While With".split())


def tokens(text):
    t = {n for n in NUM.findall(text) if len(n) >= 2 or "." in n}
    t |= {w for w in NAME.findall(text) if w not in STOP}
    return t


def check(m):
    base = load(REV / "baseline" / f"{m}_data.js")
    rev = load(REV / "modules" / f"{m}_data.js")
    bl, rl = base["LESSONS"], rev["LESSONS"]
    fe = dict(rev["FINAL_EXPLANATION"])
    fe.pop("rubric", None)
    fe_text = "\n".join(strings(fe))
    b_text = "\n".join(strings(bl))
    r_text = "\n".join(strings(rl))
    res = {"module": m, "lessons_before": len(bl), "lessons_after": len(rl), "REMOVED": [], "LESSONREF": [], "MINUTES": [], "TITLEREF": []}
    removed = (tokens(b_text) - tokens(r_text)) & tokens(fe_text)
    # a token that the FE itself introduces (not in baseline lessons) is excluded by construction
    res["REMOVED"] = sorted(removed)
    changed_numbering = [x.get("title") for x in bl] != [x.get("title") for x in rl]
    refs = sorted({int(n) for n in re.findall(r"\bLessons?\s+(\d+)", fe_text)} | {int(n) for n in re.findall(r"\bL(\d+)\b", fe_text)})
    for n in refs:
        if n > len(rl):
            res["LESSONREF"].append(f"Lesson {n} > lesson count {len(rl)}")
    if changed_numbering and refs:
        for n in refs:
            if n <= len(rl) and n <= len(bl):
                tb = set(re.findall(r"[a-z]{4,}", (bl[n - 1].get("title") or "").lower()))
                tr = set(re.findall(r"[a-z]{4,}", (rl[n - 1].get("title") or "").lower()))
                if not tb & tr:
                    res["TITLEREF"].append(f"FE cites Lesson {n}: was '{bl[n-1].get('title','')[:50]}', now '{rl[n-1].get('title','')[:50]}'")
    if re.search(r"\b80[- ]?min", fe_text):
        res["MINUTES"].append("FE mentions an 80-minute lesson")
    return res


def main():
    argv = sys.argv[1:]
    jout = argv.pop(argv.index("--json") + 1) if "--json" in argv else None
    args = [a for a in argv if not a.startswith("--")]
    mods = args or sorted(p.name[:-len("_data.js")] for p in (REV / "modules").glob("*_data.js"))
    out = [check(m) for m in mods]
    flagged = [r for r in out if r["REMOVED"] or r["LESSONREF"] or r["MINUTES"] or r["TITLEREF"]]
    for r in out:
        if r in flagged:
            print(f"{r['module']} ({r['lessons_before']}->{r['lessons_after']} lessons): "
                  f"REMOVED={len(r['REMOVED'])} LESSONREF={len(r['LESSONREF'])} TITLEREF={len(r['TITLEREF'])} MINUTES={len(r['MINUTES'])}")
    print(f"{len(flagged)} of {len(out)} modules have candidates")
    if jout:
        Path(jout).write_text(json.dumps(out, indent=1))


main()
