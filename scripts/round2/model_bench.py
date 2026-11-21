#!/usr/bin/env python3
"""
model_bench.py - measured test of the Round 2 audit reviewers on KNOWN defects (Mark, 2026-11-12, $5 cap)
==========================================================================================================
Ground truth: defects the Round 2 pipeline already found and fixed (records *-r2-vfix-*, phys_1_3-r2-fe-auto-002/003).
For each case the fix is reverted IN THE PROMPT ONLY (no file is changed), the unchanged production reviewer prompt
(lesson_converge.RULES / fe_converge.RULES) is run once, and we record whether the known defect is reported, how many other
issues are reported, and the cost. Run once per model: CLAUDE_MODEL=claude-sonnet-5-5 or claude-opus-5-5.
Caveat: the ground truth was found by Sonnet-based loops, so it is biased toward Sonnet.
CBE_REVISED_DIR=<abs> CLAUDE_MODEL=<id> venv/bin/python scripts/round2/model_bench.py --label sonnet --max-spend 2.2
"""
import argparse, json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import fe_converge as fc  # noqa
import lesson_converge as lc  # noqa
import generate_substrand as g  # noqa

REV = fc.REV
OUT = REV / "model_bench"
# (module, task, revert record ids, short label)
CASES = [
    ("math_1_2", "fe", ["math_1_2-r2-vfix-001", "math_1_2-r2-vfix-002"], "FE rounding vs lesson"),
    ("bio_3_2", "lesson", ["bio_3_2-r2-vfix-001"], "open circulation 'oxygen-carrying fluid'"),
    ("phys_1_3", "fe", ["phys_1_3-r2-fe-auto-002", "phys_1_3-r2-fe-auto-003"], "FE <4C rise vs lesson"),
    ("chem_1_5", "fe", ["chem_1_5-r2-vfix-001"], "FE 'more electron shells' cause"),
    ("phys_3_1", "lesson", ["phys_3_1-r2-vfix-001"], "decay chain parenthetical"),
    ("phys_1_3", "lesson", ["phys_1_3-r2-vfix2-001"], "L4 <4C column wording"),
    ("chem_1_2", "fe", ["chem_1_2-r2-vfix-001"], "FE Bohr / flame colours"),
]


def rec(m, rid):
    d = json.loads((REV / "change_records" / f"{m}.json").read_text())
    return next(x for x in (d if isinstance(d, list) else d["records"]) if x["id"] == rid)


def esc(s):  # as it appears inside a json.dumps string
    return json.dumps(s, ensure_ascii=False)[1:-1]


def revert(text, m, rids):
    for rid in rids:
        r = rec(m, rid)
        nv = r["new"] if r.get("new") is not None else r.get("value")
        new, old = esc(str(nv)), esc(str(r["old"]))
        if text.count(new) != 1:
            raise SystemExit(f"{rid}: replacement text occurs {text.count(new)} times, cannot revert safely")
        text = text.replace(new, old)
    return text


def run_case(m, task, rids):
    mod = fc.load(REV / "modules" / f"{m}_data.js")
    lessons = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
    if task == "lesson":
        lessons = revert(lessons, m, rids)
        unit = json.dumps(fc.strip({k: v for k, v in mod["UNIT"].items() if k in ("totalDuration", "phenomenon", "drivingQuestion", "substrand")}), ensure_ascii=False)
        prompt = f"{lessons}\n{lc.RULES}\n\nTEACHER DECISIONS (binding):\n{lc.decisions_text(m)}\n\nUNIT: {unit}"
        schema = lc.REVIEW_SCHEMA
    else:
        fe = revert(json.dumps(fc.fe_view(mod), ensure_ascii=False, indent=1), m, rids)
        fe_old = fe
        lessons_fe = f"THE LESSON PLAN (authoritative), all lessons in full (JSON):\n{fc.full_lessons(mod)}\n"
        prompt = f"{lessons_fe}\n{fc.RULES}\n\nTHE FINAL EXPLANATION UNDER AUDIT (JSON):\n{fe_old}"
        schema = fc.REVIEW_SCHEMA
    t0 = time.time()
    r = g.call_claude(prompt, schema=schema)
    return (r or {}).get("issues") if r else None, round(time.time() - t0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--max-spend", type=float, default=2.2)
    a = ap.parse_args()
    if "opus" in g.MODEL:
        g.PRICE_PER_MTOK["sync"] = {"input": 4.0, "output": 20.0}
    OUT.mkdir(exist_ok=True)
    res = []
    for m, task, rids, label in CASES:
        before = g._estimate_cost()
        if before > a.max_spend:
            res.append({"module": m, "task": task, "label": label, "status": "SKIPPED (cap)"})
            print(f"{m} {task}: SKIPPED (cap)", flush=True)
            continue
        issues, secs = run_case(m, task, rids)
        cost = round(g._estimate_cost() - before, 3)
        res.append({"module": m, "task": task, "label": label, "reverted": rids, "cost": cost, "secs": secs,
                    "n_issues": None if issues is None else len(issues), "issues": issues})
        print(f"{m} {task} [{label}]: {'FAILED' if issues is None else str(len(issues)) + ' issues'} ${cost} {secs}s", flush=True)
    (OUT / f"{a.label}.json").write_text(json.dumps({"model": g.MODEL, "total_cost": round(g._estimate_cost(), 3), "results": res}, ensure_ascii=False, indent=1))
    print("model", g.MODEL, "total est. $", round(g._estimate_cost(), 3))


if __name__ == "__main__":
    main()
