#!/usr/bin/env python3
"""propose_orange.py — for each ORANGE flag (R2-LES-TRIAGE flags in change_records) write a concrete PROPOSED ANSWER for teachers to approve or edit.
Nothing is applied. The proposal (plain words + optional exact edits, checked for exact-match) is appended to the flag's `why` and saved in lesson_proposals/<m>.json.
COSTS API MONEY. CBE_REVISED_DIR=<abs> venv/bin/python scripts/round2/propose_orange.py [--only a,b] [--max-spend 4]"""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_converge as fc, lesson_converge as lc, lesson_finalize as lf
REV = fc.REV; _s = fc._s
OUT = REV / "lesson_proposals"
EDIT = lf.EDIT
SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"proposals": {"type": "array", "items": {"type": "object", "additionalProperties": False,
    "properties": {"n": {"type": "integer"}, "answer": _s(), "edits": {"type": "array", "items": EDIT}, "alternative": _s(), "knock_on": _s()},
    "required": ["n", "answer"]}}}, "required": ["proposals"]}
P = """Teachers will review the flagged problems below in this Kenyan CBE Grade 10 lesson plan (all lessons above). The system could not settle them alone because each needs a choice. For EACH item propose ONE concrete recommended answer a teacher can approve or edit:
- answer: 2-4 plain sentences: exactly what to change and why this choice is best (the lesson plan is the arbiter; follow the teacher decisions below; keep KICD outcomes; no scientific inaccuracy; keep each lesson's total time unchanged unless the item is about time, and then show the phase minutes adding up).
- edits: the exact find-and-replace edits that would carry it out (lesson, path inside that lesson, old text occurring ONCE in that field, new text), including every place the same fact appears so the plan stays consistent; use [] if the answer is a larger redesign (then say so).
- alternative: one genuinely different option in one sentence (what a teacher might prefer instead).
- knock_on: other lessons or the Final Explanation that would also need a change, or 'none'.

TEACHER DECISIONS (binding):
{dec}

FLAGGED ITEMS:
{items}
"""
ap = argparse.ArgumentParser(); ap.add_argument("--only"); ap.add_argument("--max-spend", type=float, default=4.0); a = ap.parse_args()
import generate_substrand as g
OUT.mkdir(exist_ok=True)
for f in sorted((REV / "change_records").glob("*.json")):
    m = f.stem
    if a.only and m not in a.only.split(","): continue
    d = json.loads(f.read_text()); recs = d if isinstance(d, list) else d["records"]
    flags = [x for x in recs if x["id"].startswith(f"{m}-r2-les-tri-") and x["kind"] == "flag" and "PROPOSED ANSWER" not in x["why"]]
    if not flags: continue
    if g._estimate_cost() > a.max_spend: print(m, "SKIPPED (cap)"); continue
    mod = fc.load(REV / "modules" / f"{m}_data.js")
    prefix = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
    items = "\n".join(f"[{i}] Lesson {x.get('lesson')}: {x['why']}" for i, x in enumerate(flags))
    r = g.call_claude(P.format(dec=lc.decisions_text(m), items=items), schema=SCHEMA, cache_prefix=prefix)
    if r is None: print(m, "CALL FAILED"); continue
    pv = {p["n"]: p for p in r["proposals"]}; saved = []
    for i, x in enumerate(flags):
        p = pv.get(i)
        if not p: continue
        ok = []
        for e in p.get("edits", []):
            try:
                fld = lc.get_field(mod["LESSONS"][e["lesson"] - 1], e["path"])
                if isinstance(fld, str) and fld.count(e["old"]) == 1 and e["old"] != e["new"]: ok.append(e)
            except Exception: pass
        txt = f" PROPOSED ANSWER (for the teacher to approve or edit; not applied): {p['answer'].strip()}"
        if ok: txt += " Ready-made edit(s): " + " | ".join(f"Lesson {e['lesson']} {e['path']}: replace \"{e['old'][:160]}\" with \"{e['new'][:300]}\"" for e in ok)
        elif p.get("edits"): txt += " (Wording needs a manual edit; the answer is the guide.)"
        if p.get("alternative"): txt += f" Alternative: {p['alternative'].strip()}"
        if p.get("knock_on") and p["knock_on"].lower().strip(". ") != "none": txt += f" Also affects: {p['knock_on'].strip()}"
        x["why"] += txt
        saved.append({"id": x["id"], "answer": p["answer"], "edits_exact_ok": ok, "alternative": p.get("alternative", ""), "knock_on": p.get("knock_on", "")})
    f.write_text(json.dumps(d if isinstance(d, list) else d, ensure_ascii=False, indent=1))
    (OUT / f"{m}.json").write_text(json.dumps(saved, ensure_ascii=False, indent=1))
    print(m, len(saved), "proposals", flush=True)
print(f"estimated spend ${g._estimate_cost():.2f}")
