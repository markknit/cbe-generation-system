#!/usr/bin/env python3
"""
verify_three_criteria.py — independent check of EVERY Round 2 change (Mark, 2026-11-10, $20 cap)
=================================================================================================
Report only: changes nothing. For each module (Bio/Chem/Phys/Maths) all Round 2 edit/set records (ids with -r2-; the mechanical
four-level rubric records `-r2-rub-` are skipped) go to one strict reviewer who judges: teacher_aligned (matches the teacher decisions),
kicd_aligned (matches KICD sub-strand content), science_ok (correct at Grade 10 level), plus a concern note. Results: verification/<m>.json.
CBE_REVISED_DIR=<abs> venv/bin/python scripts/round2/verify_three_criteria.py [--only a,b] [--max-spend 18]
"""
import argparse, json, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_converge as fc  # noqa
import lesson_converge as lc  # noqa
import lesson_finalize as lf  # noqa

REV = fc.REV
OUT = REV / "verification"
_s = fc._s
SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"verdicts": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "properties": {"n": {"type": "integer"}, "teacher_aligned": {"type": "boolean"}, "kicd_aligned": {"type": "boolean"},
                   "science_ok": {"type": "boolean"}, "concern": _s()},
    "required": ["n", "teacher_aligned", "kicd_aligned", "science_ok", "concern"]}}}, "required": ["verdicts"]}
PROMPT = """You are a strict, independent reviewer of CHANGES already made to a Kenyan CBE Grade 10 lesson plan (lessons above in full, as they now stand) and its Final Explanation (FE).
Teacher decisions (typed by teachers, BINDING):
{dec}

KICD sub-strand content (verbatim source):
{unit}

For each numbered change judge:
 teacher_aligned: consistent with the teacher decisions/requests (does not reverse or override them; where the change responds to a teacher request, it does what was asked);
 kicd_aligned: consistent with the KICD content and learning outcomes (changes none, contradicts none; KICD names are display labels);
 science_ok: every scientific/mathematical statement in the NEW text is correct at Grade 10 level, and the new text agrees with the lesson plan (the lesson plan is the arbiter; for FE changes the FE must match the lessons).
Set a boolean false ONLY for a real problem you can state; put the specific problem in `concern` (otherwise concern = "none").
Do not flag style. Return one verdict per number.

CHANGES:
{items}
"""


def show(r):
    where = r.get("location") or r.get("where") or r.get("path", "")
    if r["kind"] == "set":
        body = "SET " + json.dumps(r.get("value"), ensure_ascii=False)[:700]
    else:
        body = f"OLD: {str(r.get('old',''))[:500]}\n   NEW: {str(r.get('new',''))[:500]}"
    return f"({r.get('target')}, L{r.get('lesson','-')}) {where}\n   {body}\n   WHY: {str(r.get('why',''))[:350]}"


def run_module(g, m, a):
    rf = json.loads((REV / "change_records" / f"{m}.json").read_text())
    recs = [r for r in (rf if isinstance(rf, list) else rf["records"])
            if "-r2-" in r["id"] and r["kind"] in ("edit", "set") and "-r2-rub-" not in r["id"]]
    if not recs:
        return {"module": m, "status": "NOTHING", "rows": []}
    mod = fc.load(REV / "modules" / f"{m}_data.js")
    prefix = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
    fmt = dict(dec=lc.decisions_text(m), unit=lf.kicd_text(mod))
    rows = []
    for s in range(0, len(recs), 30):
        if g._estimate_cost() > a.max_spend:
            return {"module": m, "status": "SKIPPED (spend cap)", "rows": rows}
        chunk = recs[s:s + 30]
        res = g.call_claude(PROMPT.format(items="\n".join(f"[{i}] {show(r)}" for i, r in enumerate(chunk)), **fmt), schema=SCHEMA, cache_prefix=prefix)
        if res is None:
            return {"module": m, "status": "CALL FAILED", "rows": rows}
        v = {x["n"]: x for x in res["verdicts"]}
        for i, r in enumerate(chunk):
            x = v.get(i)
            rows.append({"id": r["id"], "group": r.get("group"), "teacher_decision": r.get("teacher_decision"), "checked": x is not None,
                         **({k: x[k] for k in ("teacher_aligned", "kicd_aligned", "science_ok", "concern")} if x else {})})
    return {"module": m, "status": "ok", "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--max-spend", type=float, default=18.0)
    a = ap.parse_args()
    mods = sorted(p.stem for p in (REV / "change_records").glob("*.json") if p.stem.split("_")[0] in ("bio", "chem", "phys", "math"))
    if a.only:
        mods = [m for m in mods if m in a.only.split(",")]
    import generate_substrand as g
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_module, g, m, a): m for m in mods}
        for f in as_completed(futs):
            m = futs[f]
            try:
                res = f.result()
            except Exception as e:
                print(f"{m}: ERROR {e!r}", flush=True); continue
            (OUT / f"{m}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
            bad = [r for r in res["rows"] if r.get("checked") and not (r["teacher_aligned"] and r["kicd_aligned"] and r["science_ok"])]
            print(f"{m}: {res['status']} checked={len(res['rows'])} concerns={len(bad)} spend=${g._estimate_cost():.2f}", flush=True)
    print(f"estimated spend ${g._estimate_cost():.2f}")


if __name__ == "__main__":
    main()
