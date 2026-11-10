#!/usr/bin/env python3
"""
propose_orange2.py — proposed answers for the REMAINING orange flags (Round 2 flags of Bio/Chem/Phys/Maths other than the lesson-check ones)
(Mark, 2026-11-10, $3 cap). Per module one call: for each flag a recommended answer, exact find-and-replace edits (lesson or Final Explanation, checked for exact match),
an alternative and knock-on effects. Edits are applied as yellow [DECISION] records `<m>-r2-prop2-NNN` (group R2-PROPOSED2) and the flag is removed; flags with no safe
edits (e.g. 'write four new lessons') stay orange with the PROPOSED ANSWER text appended. Whole set per flag applies or not at all (dry-run first).
CBE_REVISED_DIR=<abs> venv/bin/python scripts/round2/propose_orange2.py [--only a,b] [--max-spend 3] [--apply-only]
"""
import argparse, json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_converge as fc, lesson_converge as lc, lesson_finalize as lf
REV = fc.REV; _s = fc._s
OUT = REV / "lesson_proposals2"
E = {"type": "object", "additionalProperties": False, "properties": {"target": {"type": "string", "enum": ["lesson", "final_explanation"]}, "lesson": {"type": "integer"}, "path": _s(), "old": _s(), "new": _s()}, "required": ["target", "lesson", "path", "old", "new"]}
SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"proposals": {"type": "array", "items": {"type": "object", "additionalProperties": False,
    "properties": {"n": {"type": "integer"}, "answer": _s(), "edits": {"type": "array", "items": E}, "alternative": _s(), "knock_on": _s()}, "required": ["n", "answer"]}}}, "required": ["proposals"]}
P = """Teachers will review the open items below in this Kenyan CBE Grade 10 lesson plan (all lessons above) and its Final Explanation (FE, above). The system could not settle them alone. For EACH item propose ONE concrete recommended answer a teacher can approve or edit:
- answer: 2-4 plain sentences: exactly what to change and why (the lesson plan is the arbiter; the FE follows the lessons; follow the teacher decisions below; keep KICD outcomes; no scientific inaccuracy; no invented data).
- edits: exact find-and-replace edits that carry it out (target 'lesson' with lesson number, or 'final_explanation' with lesson 0; `path` inside that lesson or the FE; `old` occurring ONCE in that field, 12-600 chars; `new` at most 400 chars longer). Include every place the same fact appears. Use [] when the answer needs something larger than wording edits (for example writing new lessons or trimming lesson structure) and say so in the answer.
- alternative: one genuinely different option in one sentence.
- knock_on: other lessons or the FE that would also need a change, or 'none'.

TEACHER DECISIONS (binding):
{dec}

OPEN ITEMS:
{items}
"""
ap = argparse.ArgumentParser(); ap.add_argument("--only"); ap.add_argument("--max-spend", type=float, default=3.0); ap.add_argument("--apply-only", action="store_true"); a = ap.parse_args()
OUT.mkdir(exist_ok=True)
PIPE = set(json.loads((REV / "round2" / "pipeline_flags.json").read_text())["ids"])
sel = lambda m, x: x["kind"] == "flag" and x.get("applied_at", "") >= "2026-11-09" and x["id"] not in PIPE and "PROPOSED ANSWER" not in x["why"] and "-r2-les-tri-" not in x["id"]
mods = sorted(p.stem for p in (REV / "change_records").glob("*.json") if p.stem.split("_")[0] in ("bio", "chem", "phys", "math"))
if a.only: mods = [m for m in mods if m in a.only.split(",")]
if not a.apply_only:
    import generate_substrand as g
    for m in mods:
        cf = REV / "change_records" / f"{m}.json"
        d = json.loads(cf.read_text()); recs = d if isinstance(d, list) else d["records"]
        flags = [x for x in recs if sel(m, x)]
        if not flags: continue
        if g._estimate_cost() > a.max_spend: print(m, "SKIPPED (cap)"); continue
        mod = fc.load(REV / "modules" / f"{m}_data.js")
        prefix = (f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n\n"
                  f"THE FINAL EXPLANATION (JSON):\n{json.dumps(fc.strip(mod['FINAL_EXPLANATION']), ensure_ascii=False, indent=0)}\n")
        items = "\n".join(f"[{i}] ({x.get('target')}, lesson {x.get('lesson', '-')}) {x.get('where') or x.get('location') or ''}: {x['why'][:1500]}" for i, x in enumerate(flags))
        r = g.call_claude(P.format(dec=lc.decisions_text(m), items=items), schema=SCHEMA, cache_prefix=prefix)
        if r is None: print(m, "CALL FAILED"); continue
        pv = {p["n"]: p for p in r["proposals"]}; saved = []
        for i, x in enumerate(flags):
            p = pv.get(i)
            if not p: continue
            ok = []
            for e in p.get("edits", []):
                try:
                    obj = mod["FINAL_EXPLANATION"] if e["target"] == "final_explanation" else mod["LESSONS"][e["lesson"] - 1]
                    fld = lc.get_field(obj, e["path"])
                    if isinstance(fld, str) and fld.count(e["old"]) == 1 and e["old"] != e["new"] and len(e["new"]) <= len(e["old"]) + 400: ok.append(e)
                except Exception: pass
            complete = bool(p.get("edits")) and len(ok) == len(p["edits"])
            saved.append({"id": x["id"], "answer": p["answer"], "edits": ok if complete else [], "alternative": p.get("alternative", ""), "knock_on": p.get("knock_on", "")})
            txt = f" PROPOSED ANSWER (for the teacher to approve or edit): {p['answer'].strip()}"
            if p.get("alternative"): txt += f" Alternative: {p['alternative'].strip()}"
            if p.get("knock_on") and p["knock_on"].lower().strip(". ") != "none": txt += f" Also affects: {p['knock_on'].strip()}"
            x["_txt"] = txt
        for x in flags:
            if "_txt" in x: x["why"] += x.pop("_txt")
        cf.write_text(json.dumps(d, ensure_ascii=False, indent=1))
        (OUT / f"{m}.json").write_text(json.dumps(saved, ensure_ascii=False, indent=1))
        print(m, len(saved), "proposals", f"({sum(1 for s in saved if s['edits'])} with exact edits)", flush=True)
    print(f"estimated spend ${g._estimate_cost():.2f}")
# ---- apply: yellow records for flags with complete exact edits
def run(m, recs, dry):
    t = OUT / f"_{m}_apply.json"; t.write_text(json.dumps({"records": recs}, ensure_ascii=False, indent=1))
    r = subprocess.run([sys.executable, str(fc.ROOT / "scripts/revise_apply.py"), "apply", m, str(t)] + (["--dry-run"] if dry else []), capture_output=True, text=True, env={**os.environ, "CBE_REVISED_DIR": str(REV)})
    t.unlink(); return r.stdout + r.stderr
for pf in sorted(OUT.glob("[a-z]*.json")):
    m = pf.stem
    if a.only and m not in a.only.split(","): continue
    props = [p for p in json.loads(pf.read_text()) if p["edits"]]
    if not props: continue
    cf = REV / "change_records" / f"{m}.json"
    d = json.loads(cf.read_text()); recs = d if isinstance(d, list) else d["records"]; byid = {x["id"]: x for x in recs}
    n0 = max([int(x["id"].rsplit("-", 1)[1]) for x in recs if x["id"].startswith(f"{m}-r2-prop2-")] + [0])
    sets = [(p["id"], byid[p["id"]], p["edits"]) for p in props if p["id"] in byid and byid[p["id"]]["kind"] == "flag"]
    while sets:
        out, k = [], n0
        for fid, fl, edits in sets:
            why = fl["why"].replace("PROPOSED ANSWER (for the teacher to approve or edit):", "PROPOSED ANSWER, now built in (keep it, or edit it in place):")
            for e in edits:
                k += 1
                rec = {"id": f"{m}-r2-prop2-{k:03d}", "kind": "edit", "target": e["target"], "path": e["path"], "old": e["old"], "new": e["new"], "criteria": fl.get("criteria", [14]),
                       "category": fl["category"], "severity": "minor", "teacher_decision": True, "group": "R2-PROPOSED2", "why": why, "_fid": fid}
                if e["target"] == "lesson": rec["lesson"] = e["lesson"]
                if fl["category"] == "science": rec["reference"] = fl.get("reference", "standard textbook fact")
                out.append(rec)
        out[0]["group_headline"] = "Open question settled with a proposed answer built in (keep or edit)"
        clean = lambda L: [{k2: v for k2, v in o.items() if k2 != "_fid"} for o in L]
        dry = run(m, clean(out), True)
        bad = {o["_fid"] for o in out if f"rejected {o['id']}" in dry}
        if not bad: break
        print(m, "dropping sets with rejected edits:", bad); sets = [s for s in sets if s[0] not in bad]
    if not sets: continue
    print(m, run(m, clean(out), False).strip().splitlines()[-1])
    drop = {s[0] for s in sets}
    d = json.loads(cf.read_text()); recs = d if isinstance(d, list) else d["records"]
    cf.write_text(json.dumps({**d, "records": [x for x in recs if x["id"] not in drop]}, ensure_ascii=False, indent=1))
