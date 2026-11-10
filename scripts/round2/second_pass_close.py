#!/usr/bin/env python3
"""
second_pass_close.py — second independent check, then close (Mark, 2026-11-10, $8 cap)
=======================================================================================
Scope: yellow (teacher_decision) edit/set records of groups R2-LES-PROPOSED-*, R2-LES-CLOSE-*, R2-FE-REVIEW that PASSED the first
three-criteria check (verification/<m>.json). Not in scope: R2-KICD-RUBRIC (model-drafted Below descriptors stay for a teacher read).
Second reviewer (adversarial, sees lessons + the current Final Explanation) judges teacher_aligned, kicd_aligned, science_ok,
material (changes what is taught/assessed, a learning outcome, safety, timing structure, or invents data) and
touches_teacher_decision (reverses/alters a teacher's typed instruction). A GROUP is closed (teacher_decision=false, note appended to why)
only if EVERY yellow member passed both checks and none is material/touches a teacher decision.
Results: verification2/<m>.json. CBE_REVISED_DIR=<abs> venv/bin/python scripts/round2/second_pass_close.py [--only a,b] [--max-spend 7.5] [--commit-only]
"""
import argparse, json, sys, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_converge as fc  # noqa
import lesson_converge as lc  # noqa
import lesson_finalize as lf  # noqa
import verify_three_criteria as v1  # noqa

REV = fc.REV
OUT = REV / "verification2"
_s = fc._s
IN_SCOPE = lambda r: r["kind"] in ("edit", "set") and r.get("teacher_decision") and re.match(r"R2-(LES-(PROPOSED|CLOSE)-\d+|FE-REVIEW)$", r.get("group") or "")
SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"verdicts": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "properties": {"n": {"type": "integer"}, "teacher_aligned": {"type": "boolean"}, "kicd_aligned": {"type": "boolean"}, "science_ok": {"type": "boolean"},
                   "material": {"type": "boolean"}, "touches_teacher_decision": {"type": "boolean"}, "concern": _s()},
    "required": ["n", "teacher_aligned", "kicd_aligned", "science_ok", "material", "touches_teacher_decision", "concern"]}}}, "required": ["verdicts"]}
PROMPT = """You are the SECOND, adversarial reviewer of changes already made to a Kenyan CBE Grade 10 lesson plan and its Final Explanation (FE). Both are shown above exactly as they stand now. A first reviewer passed these changes; try to find what it missed.
Teacher decisions (typed by teachers, BINDING):
{dec}

KICD sub-strand content (verbatim source):
{unit}

For each numbered change judge:
 teacher_aligned: consistent with the teacher decisions/requests;
 kicd_aligned: consistent with the KICD content and learning outcomes;
 science_ok: every scientific/mathematical statement in the NEW text is correct at Grade 10 level, numbers recompute, and the text agrees with the lessons (the lessons are the arbiter; an FE change must match them);
 material: TRUE if the change alters what is taught or assessed in a way a teacher should choose (a learning outcome or assessment criterion, safety instructions, lesson timing structure, invented data/content) rather than a wording, number-agreement or consistency fix;
 touches_teacher_decision: TRUE if it reverses, narrows or overrides something a teacher typed above.
Check the new text is actually present and coherent in the current lesson/FE. Set a flag only for a real problem you can state in `concern` (otherwise concern = "none").

CHANGES:
{items}
"""


def run_module(g, m, a):
    rf = json.loads((REV / "change_records" / f"{m}.json").read_text())
    p1 = {x["id"]: x for x in json.loads((REV / "verification" / f"{m}.json").read_text())["rows"]} if (REV / "verification" / f"{m}.json").exists() else {}
    recs = [r for r in (rf if isinstance(rf, list) else rf["records"]) if IN_SCOPE(r)]
    ok1 = lambda r: (lambda x: bool(x and x.get("teacher_aligned") and x.get("kicd_aligned") and x.get("science_ok")))(p1.get(r["id"]))
    recs = [r for r in recs if ok1(r)]
    if not recs:
        return {"module": m, "status": "NOTHING", "rows": []}
    mod = fc.load(REV / "modules" / f"{m}_data.js")
    prefix = (f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n\n"
              f"THE FINAL EXPLANATION as it stands (JSON):\n{json.dumps(fc.strip(mod['FINAL_EXPLANATION']), ensure_ascii=False, indent=0)}\n")
    fmt = dict(dec=lc.decisions_text(m), unit=lf.kicd_text(mod))
    rows = []
    for s in range(0, len(recs), 30):
        if g._estimate_cost() > a.max_spend:
            return {"module": m, "status": "SKIPPED (spend cap)", "rows": rows}
        chunk = recs[s:s + 30]
        res = g.call_claude(PROMPT.format(items="\n".join(f"[{i}] {v1.show(r)}" for i, r in enumerate(chunk)), **fmt), schema=SCHEMA, cache_prefix=prefix)
        if res is None:
            return {"module": m, "status": "CALL FAILED", "rows": rows}
        v = {x["n"]: x for x in res["verdicts"]}
        for i, r in enumerate(chunk):
            x = v.get(i)
            rows.append({"id": r["id"], "group": r.get("group"), "checked": x is not None,
                         **({k: x[k] for k in ("teacher_aligned", "kicd_aligned", "science_ok", "material", "touches_teacher_decision", "concern")} if x else {})})
    return {"module": m, "status": "ok", "rows": rows}


def commit(m):
    p = REV / "change_records" / f"{m}.json"
    rf = json.loads(p.read_text())
    recs = rf if isinstance(rf, list) else rf["records"]
    f2 = OUT / f"{m}.json"
    if not f2.exists():
        return "no second pass"
    res = {x["id"]: x for x in json.loads(f2.read_text())["rows"]}
    p1 = {x["id"]: x for x in json.loads((REV / "verification" / f"{m}.json").read_text())["rows"]}
    good = lambda x: bool(x and x.get("checked") and x["teacher_aligned"] and x["kicd_aligned"] and x["science_ok"] and not x["material"] and not x["touches_teacher_decision"])
    groups = {}
    for r in recs:
        if IN_SCOPE(r):
            groups.setdefault(r["group"] + ("" if r["group"] != "R2-FE-REVIEW" else ":" + r["id"]), []).append(r)   # FE-REVIEW records are independent of each other
    closed = held = 0
    for k, members in groups.items():
        if all(good(res.get(r["id"])) for r in members):
            for r in members:
                r["teacher_decision"] = False
                r["why"] += " Closed 2026-11-10: passed two independent three-criteria checks (teacher request, KICD, science), not material, no teacher decision altered."
            closed += len(members)
        else:
            held += len(members)
    p.write_text(json.dumps(rf, ensure_ascii=False, indent=1))
    return f"closed {closed}, held {held}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only"); ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--max-spend", type=float, default=7.5); ap.add_argument("--commit-only", action="store_true")
    a = ap.parse_args()
    mods = sorted(p.stem for p in (REV / "change_records").glob("*.json") if p.stem.split("_")[0] in ("bio", "chem", "phys", "math"))
    if a.only:
        mods = [m for m in mods if m in a.only.split(",")]
    OUT.mkdir(exist_ok=True)
    if a.commit_only:
        for m in mods:
            print(m, commit(m))
        return
    import generate_substrand as g
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_module, g, m, a): m for m in mods}
        for f in as_completed(futs):
            m = futs[f]
            try:
                res = f.result()
            except Exception as e:
                print(f"{m}: ERROR {e!r}", flush=True); continue
            (OUT / f"{m}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
            bad = [r for r in res["rows"] if r.get("checked") and not (r["teacher_aligned"] and r["kicd_aligned"] and r["science_ok"] and not r["material"] and not r["touches_teacher_decision"])]
            print(f"{m}: {res['status']} checked={len(res['rows'])} not-clean={len(bad)} spend=${g._estimate_cost():.2f}", flush=True)
    print(f"estimated spend ${g._estimate_cost():.2f}")


if __name__ == "__main__":
    main()
