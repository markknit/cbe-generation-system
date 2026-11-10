#!/usr/bin/env python3
"""
review_fe.py — REVIEW-ONLY pass: does each revised Final Explanation still agree with its revised lessons?
=========================================================================================================
Uses the same independent reviewer call the generator uses (generate_substrand.verify_final_explanation: recomputes
tables, compares FE with the lessons, looks for science/maths errors and self-contradictions). It changes NOTHING in the
modules; it writes data/revised_2026-10_full/fe_review/<module>.json = {"issues": [...]} and a summary.
COSTS API MONEY (live calls, claude-sonnet-5-5). Needs ANTHROPIC_API_KEY (.env).

  CBE_REVISED_DIR=data/revised_2026-10_full venv/bin/python scripts/round2/review_fe.py [--only a,b] [--workers 4] [--max-spend 15] [--dry-run]
"""
import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REV = Path(os.environ["CBE_REVISED_DIR"])
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))


def load(path):
    return json.loads(subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(path)],
                                     capture_output=True, text=True, check=True).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-spend", type=float, default=15.0)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    mods = sorted(p.name[:-len("_data.js")] for p in (REV / "modules").glob("*_data.js"))
    if a.only:
        mods = [m for m in mods if m in a.only.split(",")]
    out_dir = REV / "fe_review"
    out_dir.mkdir(exist_ok=True)
    if a.dry_run:
        print(f"would review {len(mods)} modules (about $0.10 each, est. ${len(mods) * 0.10:.2f})")
        return
    import generate_substrand as g

    class A:
        pass

    def work(m):
        if g._estimate_cost() > a.max_spend:
            return m, "SKIPPED (spend cap)", None
        mod = load(REV / "modules" / f"{m}_data.js")
        meta = mod["META"]
        ar = A()
        ar.grade, ar.subject = int(meta["grade"]), meta["subject"].lower()
        ar.substrand, ar.substrand_name = meta["substrand_id"], meta["substrand_name"]
        ar.lessons, ar.output = len(mod["LESSONS"]), m
        fe = dict(mod["FINAL_EXPLANATION"])
        issues = g.verify_final_explanation(mod["UNIT"], mod["LESSONS"], fe, ar)
        if issues is None:
            return m, "REVIEW CALL FAILED", None
        (out_dir / f"{m}.json").write_text(json.dumps({"module": m, "issues": issues}, indent=1, ensure_ascii=False))
        return m, "ok", issues

    res = {}
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for fut in as_completed([ex.submit(work, m) for m in mods]):
            m, st, issues = fut.result()
            res[m] = (st, issues)
            print(f"{m}: {st}" + ("" if issues is None else f" {len(issues)} issue(s)"), flush=True)
    print(f"estimated spend this session: ${g._estimate_cost():.2f}")
    n_issue = sum(1 for st, i in res.values() if i)
    print(f"{n_issue} of {len(res)} modules have issues; failed/skipped: {sum(1 for st, i in res.values() if i is None)}")


main()
