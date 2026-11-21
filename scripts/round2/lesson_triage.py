#!/usr/bin/env python3
"""
lesson_triage.py — informed-judgement triage of the lesson items lesson_converge.py handed to teachers
=====================================================================================================
Mark, 2026-11-10: treat the 58 items the same, automate as far as possible, and sort them into the journal's colours:
  WHITE  = no teacher action: not a real problem (no change) OR a tiny unambiguous fix, applied and logged.
  YELLOW = a recommended fix is APPLIED (record `<m>-r2-les-tri-NNN`, teacher_decision=true) for a teacher to confirm.
  ORANGE = a real problem that needs a human choice: a FLAG record, no change.
Per MODULE (all its items in one call, with the full lessons, the teachers' binding decisions, and for each item whether
its quoted text already existed in the pre-revision baseline). Code rules override the model:
  * touches a teacher decision / learning outcome / KICD content / safety  -> ORANGE (never applied)
  * an edit must have `old` occurring exactly once in the field, 12..400 chars, new <= old+300, else ORANGE
  * SCIENCE fixes need a reference, else ORANGE
Writes data/revised_2026-10_full/lesson_triage/<m>.json. After lessons change, re-run fe_converge.py on those modules.
COSTS API MONEY. CBE_REVISED_DIR=<abs path> venv/bin/python scripts/round2/lesson_triage.py [--only a,b] [--max-spend 20] [--dry-run]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_converge as fc  # noqa: E402
import lesson_converge as lc  # noqa: E402

REV, ROOT, PY = fc.REV, fc.ROOT, fc.PY
_s = fc._s
OUT = REV / "lesson_triage"
VERDICT = {"type": "object", "additionalProperties": False, "properties": {"verdicts": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "properties": {
        "n": {"type": "integer"},
        "decision": {"type": "string", "enum": ["NOT_REAL", "FIX", "HUMAN"]},
        "tiny": {"type": "boolean"},
        "origin": {"type": "string", "enum": ["PRE_EXISTING", "INTRODUCED_BY_REVISION", "UNCLEAR"]},
        "touches_teacher_decision": {"type": "boolean"},
        "touches_outcome_kicd_or_safety": {"type": "boolean"},
        "lesson": {"type": "integer"},
        "path": _s(), "old": _s(), "new": _s(), "reference": _s(),
        "recommendation": _s(), "reason": _s()},
    "required": ["n", "decision", "recommendation", "reason"]}}}, "required": ["verdicts"]}

PROMPT = """You triage defects found in the LESSON PLAN of a Kenyan CBE Grade 10 sub-strand (all lessons in full above). Teachers wrote and reviewed this content; their typed decisions below are BINDING.
The lesson plan is the arbiter, and no clear inaccuracy may be introduced. For EACH listed item decide, using informed judgement:
- NOT_REAL: on reading the lessons the item is not a defect (a legitimate simplification, a reading error, an already-consistent passage). No change. Explain why in one line.
- FIX: a real defect where ONE reasonable correction exists, expressed as an exact find-and-replace: lesson (1-based number), path (field path inside the lesson, e.g. overview, teacherReflection, framework[2].teacherMoves, summary), old (exact text occurring ONCE in that field, 12-400 chars), new (the replacement; change as little as possible). When a fact appears in several places, the FIX must pick the value the rest of the plan, the teacher decisions or the science supports; if no one value is clearly right, use HUMAN. tiny=true only for a one-number/one-word/one-reference correction with a single right answer; otherwise tiny=false (a teacher should confirm). A SCIENCE fix needs a one-line standard reference in `reference`.
- HUMAN: a real problem that needs a human choice (alternative designs, restructuring a lesson, content a teacher must decide, timing gaps needing activity cuts, anything you cannot settle from the plan itself). Give your best recommendation anyway (what you would do and why) and the lesson number most affected.
Also give: origin (PRE_EXISTING = the problem is in text unchanged from the pre-revision baseline; INTRODUCED_BY_REVISION = the revision created it, e.g. renumbered/split lessons; UNCLEAR), touches_teacher_decision (the fix would reverse or alter a teacher decision), touches_outcome_kicd_or_safety (the fix would change a specific learning outcome, KICD content, a safety instruction).
Be decisive: the aim is a small list for humans. Do not invent facts. One-line recommendation and one-line reason each.

TEACHER DECISIONS (binding):
{dec}

BASELINE NOTE per item: {base}

ITEMS:
{items}
"""


def baseline_text(m):
    try:
        return fc.norm(" ".join(fc.strings(fc.strip(fc.load(REV / "baseline" / f"{m}_data.js")["LESSONS"]))))
    except Exception:
        return ""


def triage_module(g, m, a):
    src = json.loads((lc.OUT / f"{m}.json").read_text())
    mod = fc.load(REV / "modules" / f"{m}_data.js")
    hay = fc.norm(" ".join(fc.strings(fc.strip(mod["LESSONS"]))))
    base = baseline_text(m)
    done = OUT / f"_round1_{m}.json"
    seen = set()
    for fz in [OUT / f"{m}.json", *OUT.glob(f"_*{m}.json")]:
        if fz.exists():
            seen |= {fc.norm(r["item"]["quote_a"])[:60] for r in json.loads(fz.read_text()).get("items", [])}
    items = [x for x in src.get("for_teachers", []) if fc.norm(x["quote_a"])[:60] in hay and fc.norm(x["quote_a"])[:60] not in seen]   # skip items already gone or already triaged
    if not items:
        return {"module": m, "status": "NOTHING", "items": []}
    if g._estimate_cost() > a.max_spend:
        return {"module": m, "status": "SKIPPED (spend cap)", "items": []}
    notes = []
    for i, x in enumerate(items):
        qa = fc.norm(x["quote_a"])[:60] in base
        qb = (not x.get("quote_b")) or fc.norm(x["quote_b"])[:60] in base
        notes.append(f"[{i}] quoted text " + ("present in the pre-revision baseline" if qa and qb else "NEW or CHANGED by Round 2"))
    listing = "\n".join(f"[{i}] ({x['type']}) {x['where']}: {x['problem']}\n    QUOTE A: {x['quote_a']}\n    QUOTE B: {x.get('quote_b','')}\n    SUGGESTED CORRECT VALUE: {x.get('correct_value','')}" for i, x in enumerate(items))
    prefix = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
    r = g.call_claude(PROMPT.format(dec=lc.decisions_text(m), base="; ".join(notes), items=listing), schema=VERDICT, cache_prefix=prefix)
    if r is None:
        return {"module": m, "status": "CALL FAILED", "items": []}
    ver = {v["n"]: v for v in r["verdicts"]}
    out = []
    for i, x in enumerate(items):
        v = ver.get(i)
        if not v:
            out.append({"item": x, "color": "ORANGE", "why_orange": "no verdict returned", "recommendation": "", "reason": ""})
            continue
        row = {"item": x, "origin": v.get("origin", "UNCLEAR"), "recommendation": v["recommendation"], "reason": v["reason"],
               "decision": v["decision"], "lesson": v.get("lesson") or 0}
        if v["decision"] == "NOT_REAL":
            row["color"] = "WHITE"
        elif v["decision"] == "HUMAN":
            row["color"] = "ORANGE"
            row["why_orange"] = "needs a human choice"
        else:
            e = {"lesson": v.get("lesson", 0), "path": (v.get("path") or "").strip(), "old": v.get("old", ""), "new": v.get("new", "")}
            bad = None
            if v.get("touches_teacher_decision") or v.get("touches_outcome_kicd_or_safety"):
                bad = "touches a teacher decision, learning outcome, KICD content or safety"
            elif x["type"] == "SCIENCE" and not (v.get("reference") or "").strip():
                bad = "science fix without a reference"
            else:
                try:
                    field = lc.get_field(mod["LESSONS"][e["lesson"] - 1], e["path"])
                    if not isinstance(field, str) or field.count(e["old"]) != 1 or not (12 <= len(e["old"]) <= 400) or len(e["new"]) > len(e["old"]) + 300 or e["old"] == e["new"]:
                        bad = "edit text not unique or outside size limits"
                except Exception:
                    bad = "edit path invalid"
            if bad:
                row["color"], row["why_orange"] = "ORANGE", bad
            else:
                row["color"] = "WHITE" if v.get("tiny") else "YELLOW"
                row["edit"] = e
                row["reference"] = (v.get("reference") or "").strip()
        out.append(row)
    return {"module": m, "status": "ok", "items": out}


def write_records(m, res):
    """apply FIX edits (white/yellow) and ORANGE flags through revise_apply"""
    rf = REV / "change_records" / f"{m}.json"
    d = json.loads(rf.read_text())
    recs = d if isinstance(d, list) else d.get("records", [])
    n0 = max([int(x["id"].rsplit("-", 1)[1]) for x in recs if x["id"].startswith(f"{m}-r2-les-tri-")] + [0])
    out, first = [], True
    for row in res["items"]:
        it = row["item"]
        cat, crit = lc.CAT.get(it["type"], ("consistency", [14]))
        n0 += 1
        base = {"id": f"{m}-r2-les-tri-{n0:03d}", "criteria": crit, "category": cat, "group": "R2-LES-TRIAGE"}
        if first and row["color"] != "WHITE" or (first and "edit" in row):
            base["group_headline"] = "Lesson inconsistencies found by the automatic check, with a recommendation"
            first = False
        txt = f"Automatic lesson check ({it['type']}): {it['problem'][:300]} Recommendation: {row['recommendation'][:300]} Reason: {row['reason'][:200]} Origin: {row.get('origin','UNCLEAR')}."
        if "edit" in row:
            e = row["edit"]
            r = {**base, "kind": "edit", "target": "lesson", "lesson": e["lesson"], "path": e["path"], "old": e["old"], "new": e["new"],
                 "severity": "minor", "teacher_decision": row["color"] == "YELLOW", "why": txt}
            if cat == "science":
                r["reference"] = row.get("reference") or "standard textbook fact"
            out.append(r)
        elif row["color"] == "ORANGE":
            lesson = row.get("lesson") or 1
            out.append({**base, "kind": "flag", "target": "lesson", "lesson": lesson, "path": "title", "severity": "minor", "teacher_decision": True,
                        "why": txt + f" Not changed: {row.get('why_orange','needs a human choice')}."})
    if not out:
        return "no records"
    if not any("group_headline" in r for r in out):
        out[0]["group_headline"] = "Lesson inconsistencies found by the automatic check, with a recommendation"
    tmp = OUT / f"_{m}_records.json"
    tmp.write_text(json.dumps({"records": out}, ensure_ascii=False, indent=1))
    res2 = subprocess.run([PY, str(ROOT / "scripts/revise_apply.py"), "apply", m, str(tmp)], capture_output=True, text=True, env={**os.environ, "CBE_REVISED_DIR": str(REV)})
    tmp.unlink()
    return (res2.stdout.strip().splitlines() or [""])[-1] + ("" if res2.returncode == 0 else " | " + res2.stderr[-200:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--max-spend", type=float, default=20.0)
    ap.add_argument("--dry-run", action="store_true", help="classify and save, but apply nothing")
    a = ap.parse_args()
    mods = sorted(p.stem for p in lc.OUT.glob("*.json") if json.loads(p.read_text()).get("for_teachers"))
    if a.only:
        mods = [m for m in mods if m in a.only.split(",")]
    import generate_substrand as g
    OUT.mkdir(exist_ok=True)
    for m in mods:         # keep earlier results; only items not triaged before are processed now
        f1 = OUT / f"{m}.json"
        if f1.exists() and not a.dry_run:
            f1.rename(OUT / f"_prev{len(list(OUT.glob(f'_*{m}.json')))}_{m}.json")
    tally = {"WHITE": 0, "YELLOW": 0, "ORANGE": 0}
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(triage_module, g, m, a): m for m in mods}
        for f in as_completed(futs):
            m = futs[f]
            try:
                res = f.result()
            except Exception as e:
                print(f"{m}: ERROR {e!r}", flush=True)
                continue
            c = {k: sum(1 for r in res["items"] if r["color"] == k) for k in tally}
            for k in tally:
                tally[k] += c[k]
            tail = ""
            if res["status"] == "ok" and not a.dry_run:
                tail = write_records(m, res)
                res["applied"] = tail
            (OUT / f"{m}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
            print(f"{m}: {res['status']} white={c['WHITE']} yellow={c['YELLOW']} orange={c['ORANGE']} | {tail}", flush=True)
    print("TOTAL", tally, f"estimated spend ${g._estimate_cost():.2f}")


if __name__ == "__main__":
    main()
