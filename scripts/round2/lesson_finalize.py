#!/usr/bin/env python3
"""
lesson_finalize.py — second pass over the triage results (Mark, 2026-11-10)
===========================================================================
Rule: a YELLOW/WHITE change that (1) aligns with the teachers' responses, (2) aligns with KICD and (3) is scientifically correct is
PROCESSED NOW (no longer asked of teachers; stays documented in the journal as a completed change). ORANGE is kept only for items that
are MATERIAL and cannot be made by the system alone; every other orange item gets a concrete fix applied.
Per module, call A proposes (for orange) or assesses (for applied yellow/white edits); call B (independent) verifies. Both must say
teacher_aligned & kicd_aligned & science_ok (& not material for orange) for a change to be final. Code limits on every edit:
old unique in its field, 12..600 chars, new <= old + 400. Records: applied yellow/white edits get teacher_decision=false and a note;
new edits `<m>-r2-les-fin-NNN`; resolved orange flags are removed from change_records. Report: lesson_triage/<m>.json is updated
(`final`), plus lesson_finalize/<m>.json. COSTS API MONEY. After this, re-run fe_converge.py on modules with new lesson edits.
CBE_REVISED_DIR=<abs> venv/bin/python scripts/round2/lesson_finalize.py [--only a,b] [--max-spend 10]
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_converge as fc  # noqa: E402
import lesson_converge as lc  # noqa: E402
import lesson_triage as lt  # noqa: E402

REV = fc.REV
_s = fc._s
OUT = REV / "lesson_finalize"
EDIT = {"type": "object", "additionalProperties": False, "properties": {"lesson": {"type": "integer"}, "path": _s(), "old": _s(), "new": _s()}, "required": ["lesson", "path", "old", "new"]}
SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"verdicts": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "properties": {"n": {"type": "integer"}, "edits": {"type": "array", "items": EDIT},
                   "teacher_aligned": {"type": "boolean"}, "kicd_aligned": {"type": "boolean"}, "science_ok": {"type": "boolean"},
                   "material": {"type": "boolean"}, "reference": _s(), "reason": _s()},
    "required": ["n", "teacher_aligned", "kicd_aligned", "science_ok", "material", "reason"]}}}, "required": ["verdicts"]}

COMMON = """The lessons are above. Teacher decisions (BINDING, typed by the teachers; a change must not reverse or alter them):
{dec}

KICD sub-strand content (verbatim source for outcomes/content; a change must not alter or contradict it):
{unit}

For each numbered item below, judge three things about the change:
 teacher_aligned: consistent with the teacher decisions and the teachers' own text (it does not reverse or override them);
 kicd_aligned: consistent with the KICD sub-strand content and learning outcomes above (it changes none and contradicts none);
 science_ok: every scientific/mathematical statement in the new text is correct at Grade 10 level (give a one-line standard reference in `reference` if the change touches science).
 material: TRUE only if settling the item needs a real human choice: redesigning or restructuring a lesson/activity, inventing new data or content, cutting teaching time, or anything that could alter what is taught or how it is assessed. FALSE for wording, cross-reference, label, consistency and number-agreement fixes where one reasonable answer exists.
The lesson plan is the arbiter; never introduce an inaccuracy. {task}

ITEMS:
{items}
"""
TASK_A = "For ORANGE items (no change yet): propose the complete fix as exact find-and-replace edits (several edits, across lessons, if one fact is repeated; each `old` must occur ONCE in that field, 12-600 chars; `new` at most 400 chars longer) and judge the three criteria for YOUR proposal; if no safe complete fix exists, return edits=[] and material=true with the reason. For items marked APPLIED (change already made) return edits=[] and judge the applied change."
TASK_B = "You are the INDEPENDENT verifier. Judge each item's change (applied or proposed, shown in full) strictly; if you find any problem, set the relevant boolean false and say why. Return edits=[]."


def kicd_text(mod):
    return json.dumps(fc.strip({k: v for k, v in mod["UNIT"].items() if k not in ("storyline", "phenomenon")}), ensure_ascii=False)[:7000]


def find_rec(recs, m, prefixes, problem, kind):
    key = problem[:80]
    return [x for x in recs if any(x["id"].startswith(f"{m}-r2-les-{p}-") for p in prefixes) and x["kind"] == kind and key in x.get("why", "")]


def run_module(g, m, a):
    tri = json.loads((REV / "lesson_triage" / f"{m}.json").read_text())
    mod = fc.load(REV / "modules" / f"{m}_data.js")
    rf = json.loads((REV / "change_records" / f"{m}.json").read_text())
    recs = rf if isinstance(rf, list) else rf["records"]
    items, blocks = [], []
    for i, r in enumerate(tri["items"]):
        it = r["item"]
        if r["color"] == "WHITE" and "edit" not in r:
            continue                      # not a real problem: nothing to finalise
        if r.get("final"):
            continue
        applied = None
        if "edit" in r:
            e = r["edit"]
            applied = f"APPLIED edit, lesson {e['lesson']} {e['path']}:\n   OLD: {e['old'][:500]}\n   NEW: {e['new'][:500]}"
        items.append((i, r, applied))
        blocks.append(f"[{len(items)-1}] ({it['type']}) {it['where']}: {it['problem']}\n   QUOTE A: {it['quote_a']}\n   QUOTE B: {it.get('quote_b','')}\n   Earlier recommendation: {r['recommendation']}\n   STATUS: {'ORANGE (not changed)' if applied is None else applied}")
    if not items:
        return {"module": m, "status": "NOTHING", "rows": []}
    if g._estimate_cost() > a.max_spend:
        return {"module": m, "status": "SKIPPED (spend cap)", "rows": []}
    prefix = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
    fmt = dict(dec=lc.decisions_text(m), unit=kicd_text(mod), items="\n".join(blocks))
    A = g.call_claude(COMMON.format(task=TASK_A, **fmt), schema=SCHEMA, cache_prefix=prefix)
    if A is None:
        return {"module": m, "status": "CALL FAILED (A)", "rows": []}
    va = {v["n"]: v for v in A["verdicts"]}
    # build what B must verify: applied edits and proposed edits in full
    blocks2 = []
    for k, (i, r, applied) in enumerate(items):
        v = va.get(k, {})
        shown = applied or ("PROPOSED edits:\n" + "\n".join(f"   L{e['lesson']} {e['path']}: OLD: {e['old'][:400]}  NEW: {e['new'][:400]}" for e in v.get("edits", [])) if v.get("edits") else "NO EDIT PROPOSED (kept for a human)")
        blocks2.append(blocks[k].rsplit("   STATUS:", 1)[0] + f"   CHANGE TO JUDGE: {shown}")
    B = g.call_claude(COMMON.format(task=TASK_B, **{**fmt, "items": "\n".join(blocks2)}), schema=SCHEMA, cache_prefix=prefix)
    if B is None:
        return {"module": m, "status": "CALL FAILED (B)", "rows": []}
    vb = {v["n"]: v for v in B["verdicts"]}
    rows = []
    for k, (i, r, applied) in enumerate(items):
        a_, b_ = va.get(k, {}), vb.get(k, {})
        ok3 = all(x.get(c) for x in (a_, b_) for c in ("teacher_aligned", "kicd_aligned", "science_ok")) and not (a_.get("material") or b_.get("material"))
        row = {"i": i, "applied": applied is not None, "edits": a_.get("edits", []) if applied is None else [], "ok": ok3,
               "A": {k2: a_.get(k2) for k2 in ("teacher_aligned", "kicd_aligned", "science_ok", "material", "reason", "reference")},
               "B": {k2: b_.get(k2) for k2 in ("teacher_aligned", "kicd_aligned", "science_ok", "material", "reason")}}
        # code limits on proposed edits
        if applied is None and ok3:
            if not row["edits"]:
                row["ok"] = False
            for e in row["edits"]:
                try:
                    f = lc.get_field(mod["LESSONS"][e["lesson"] - 1], e["path"])
                    if not isinstance(f, str) or f.count(e["old"]) != 1 or not (12 <= len(e["old"]) <= 600) or len(e["new"]) > len(e["old"]) + 400 or e["old"] == e["new"]:
                        row["ok"], row["why_not"] = False, "edit not exact/unique or too large"
                except Exception:
                    row["ok"], row["why_not"] = False, "edit path invalid"
            if row["ok"]:
                # edits must not overlap each other on the same field text
                seen = set()
                for e in row["edits"]:
                    key = (e["lesson"], e["path"], e["old"])
                    if key in seen:
                        row["ok"], row["why_not"] = False, "duplicate edit"
                    seen.add(key)
        rows.append(row)
    return {"module": m, "status": "ok", "rows": rows}


def commit(m, res):
    """apply the outcome: mark confirmed applied edits as completed; apply orange fixes; remove resolved orange flags"""
    p = REV / "change_records" / f"{m}.json"
    rf = json.loads(p.read_text())
    recs = rf if isinstance(rf, list) else rf["records"]
    tri = json.loads((REV / "lesson_triage" / f"{m}.json").read_text())
    new_recs, drop_ids, log = [], set(), []
    for row in res["rows"]:
        r = tri["items"][row["i"]]
        it = r["item"]
        if row["applied"]:
            hit = find_rec(recs, m, ["tri"], it["problem"], "edit")
            if row["ok"] and len(hit) == 1:
                hit[0]["teacher_decision"] = False
                hit[0]["why"] += " Verified by two independent checks: consistent with the teachers' responses, with KICD, and scientifically correct; processed as final."
                r["color"], r["final"] = "WHITE", "completed (3 criteria met)"
                log.append(f"{it['type']} completed")
            elif row["ok"] and not hit:
                r["color"], r["final"] = "WHITE", "completed (same passage as another verified edit)"
                log.append(f"{it['type']} duplicate completed")
            else:
                r["final"] = "kept yellow"
                log.append(f"{it['type']} stays yellow (criteria not all met)")
        elif row["ok"]:
            fl = find_rec(recs, m, ["tri"], it["problem"], "flag")
            for x in fl:
                drop_ids.add(x["id"])
            for e in row["edits"]:
                cat, crit = lc.CAT.get(it["type"], ("consistency", [14]))
                new_recs.append({"kind": "edit", "target": "lesson", "lesson": e["lesson"], "path": e["path"], "old": e["old"], "new": e["new"], "criteria": crit,
                                 "category": cat, "severity": "minor", "teacher_decision": False, "group": "R2-LES-FINAL",
                                 "why": f"Automatic lesson check ({it['type']}): {it['problem'][:300]} Fix applied: {r['recommendation'][:250]} Verified by two independent checks: consistent with the teachers' responses, with KICD, and scientifically correct; processed as final.",
                                 **({"reference": row["A"].get("reference") or "standard textbook fact"} if cat == "science" else {})})
            r["color"], r["final"] = "WHITE", "fixed by the finalise pass"
            log.append(f"{it['type']} orange -> fixed")
        else:
            r["final"] = "orange kept: " + ((row["A"].get("reason") or "")[:160])
    if drop_ids:
        recs2 = [x for x in recs if x["id"] not in drop_ids]
        rf2 = recs2 if isinstance(rf, list) else {**rf, "records": recs2}
        p.write_text(json.dumps(rf2, ensure_ascii=False, indent=1))
    else:
        p.write_text(json.dumps(rf, ensure_ascii=False, indent=1))
    msg = ""
    if new_recs:
        import subprocess, os
        n0 = max([int(x["id"].rsplit("-", 1)[1]) for x in recs if x["id"].startswith(f"{m}-r2-les-fin-")] + [0])
        for j, x in enumerate(new_recs, 1):
            x["id"] = f"{m}-r2-les-fin-{n0 + j:03d}"
        new_recs[0]["group_headline"] = "Lesson inconsistencies fixed by the automatic check and verified twice"
        t = OUT / f"_{m}_new.json"
        t.write_text(json.dumps({"records": new_recs}, ensure_ascii=False, indent=1))
        rr = subprocess.run([sys.executable, str(fc.ROOT / "scripts/revise_apply.py"), "apply", m, str(t)], capture_output=True, text=True, env={**os.environ, "CBE_REVISED_DIR": str(REV)})
        t.unlink()
        msg = (rr.stdout.strip().splitlines() or [""])[-1] + ("" if rr.returncode == 0 else " | " + rr.stderr[-200:])
    (REV / "lesson_triage" / f"{m}.json").write_text(json.dumps(tri, ensure_ascii=False, indent=1))
    return log, msg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--max-spend", type=float, default=10.0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--commit-only", action="store_true", help="apply the saved lesson_finalize/<m>.json results without new API calls")
    a = ap.parse_args()
    mods = sorted(p.stem for p in (REV / "lesson_triage").glob("*.json") if not p.stem.startswith("_"))
    if a.only:
        mods = [m for m in mods if m in a.only.split(",")]
    import generate_substrand as g
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit((lambda *x: None) if a.commit_only else run_module, g, m, a): m for m in mods}
        for f in as_completed(futs):
            m = futs[f]
            try:
                res = json.loads((OUT / f"{m}.json").read_text()) if a.commit_only else f.result()
            except Exception as e:
                print(f"{m}: ERROR {e!r}", flush=True)
                continue
            if not a.commit_only:
                (OUT / f"{m}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
            if res["status"] != "ok":
                print(f"{m}: {res['status']}", flush=True)
                continue
            log, msg = ([], "dry-run") if a.dry_run else commit(m, res)
            print(f"{m}: ok={sum(1 for r in res['rows'] if r['ok'])}/{len(res['rows'])} {log} {msg}", flush=True)
    print(f"estimated spend ${g._estimate_cost():.2f}")


if __name__ == "__main__":
    main()
