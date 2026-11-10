#!/usr/bin/env python3
"""
lesson_converge.py — audit and (conservatively) correct the LESSONS of the revised modules, in a loop
=====================================================================================================
Same loop as fe_converge.py, with the lessons as the object (Mark, 2026-11-09). The lessons carry teacher content and
Round 2 teacher decisions, so the safeguards are tighter:

  * the reviewers get the module's teacher decisions (round2/slices) as BINDING: never report or reverse them;
  * every finding needs exact quotes (verified in code); arithmetic / minute sums are recomputed in code;
  * the second reviewer decides, per finding, `confirmed` AND `autofix_ok`: autofix only when the correction is unambiguous
    (one right value), changes no teacher decision, learning outcome or KICD content, and (for science) names a reference;
  * the fixer returns tiny exact find/replace edits (old text must occur exactly once in that field; small size limit),
    applied through revise_apply as records `<m>-r2-les-auto-NNN` (group R2-LES-AUTO) so the journal shows before/after;
  * anything real but not unambiguous (a value to choose, an impossible figure, a pedagogical choice) goes to the module's
    residual list FOR TEACHERS and is not repeated in later rounds.
Stop after TWO consecutive rounds with nothing new to fix (CONVERGED) or --max-rounds. After lessons change, the module's
FE must be re-converged (fe_converge.py).

COSTS API MONEY. CBE_REVISED_DIR=data/revised_2026-10_full venv/bin/python scripts/round2/lesson_converge.py --only a,b [--max-spend 40]
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

ROOT, REV, PY = fc.ROOT, fc.REV, fc.PY
OUT = REV / "lesson_converge"
_s = fc._s
ID_MAP = json.loads((REV / "round2/id_map.json").read_text())["map"] if (REV / "round2/id_map.json").exists() else {}
OLD_ID = {v: k for k, v in ID_MAP.items()}

TYPES = ["ARITHMETIC", "INTERNAL_CONTRADICTION", "SCIENCE", "CROSS_REFERENCE", "TIMING", "IMPOSSIBLE_FIGURE"]
REVIEW_SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"issues": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "properties": {"type": {"type": "string", "enum": TYPES}, "where": _s(), "quote_a": _s(), "quote_b": _s(), "problem": _s(),
                   "correct_value": _s(), "calc_expr": _s(), "calc_stated": _s()},
    "required": ["type", "where", "quote_a", "problem"]}}}, "required": ["issues"]}
ADJ_SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"verdicts": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "properties": {"n": {"type": "integer"}, "confirmed": {"type": "boolean"}, "autofix_ok": {"type": "boolean"},
                   "reference": _s(), "reason": _s()}, "required": ["n", "confirmed"]}}}, "required": ["verdicts"]}
FIX_SCHEMA = {"type": "object", "additionalProperties": False, "properties": {
    "edits": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                         "properties": {"n": {"type": "integer"}, "lesson": {"type": "integer"}, "path": _s(), "old": _s(), "new": _s()},
                                         "required": ["n", "lesson", "path", "old", "new"]}},
    "cannot_fix": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                              "properties": {"n": {"type": "integer"}, "reason": _s()}, "required": ["n"]}}},
    "required": ["edits"]}

RULES = """You audit the LESSON PLAN of a Kenyan CBE Grade 10 sub-strand (all lessons in full above) for real, checkable defects. Teachers wrote and reviewed this content; do not second-guess their teaching choices.
Report ONLY these, each with exact quotes (copy words exactly; "..." may mark omitted words):
- ARITHMETIC: a calculation, total, average or conversion in a lesson is wrong. calc_expr = python expression for the CORRECT value (numbers and operators; sqrt, sin, cos in RADIANS, pi allowed), calc_stated = the number the lesson states.
- TIMING: the minutes of a lesson's phases (in teacherMoves/pacing text) do not add up to the lesson duration, or a lesson says it takes a different time from its `duration` field. calc_expr = the sum as an expression, calc_stated = the duration the lesson claims.
- INTERNAL_CONTRADICTION: two places in the lessons disagree about a fact, number, name, dataset, material, sequence or outcome (quote_a and quote_b).
- CROSS_REFERENCE: a lesson refers to another lesson, activity, card, table or material that does not exist or is elsewhere (e.g. 'in Lesson 7' but it is taught in Lesson 5).
- SCIENCE: a clear scientific or mathematical error (not a simplification a Grade 10 lesson legitimately makes). Give the correct statement in correct_value and a standard textbook-level basis.
- IMPOSSIBLE_FIGURE: a number that is physically/realistically impossible in the story (give why).
Do NOT report: style, wording, pedagogy, level of detail, anything in the TEACHER DECISIONS list below (those are binding, never report them or their consequences), simplifications, hedged statements, missing content, or anything you are not sure about. Prefer silence to a doubtful finding. Return {"issues": []} if nothing is real. `where` = 'Lesson N, field'. Unused fields: empty string."""


def decisions_text(m):
    """the teachers' typed instructions for this module (original ids), as a binding list"""
    old = OLD_ID.get(m, m)
    f = REV / "round2/slices" / f"{old}.json"
    if not f.exists():
        return "(none for this module)"
    d = json.loads(f.read_text())
    out = []
    for k, v in d.items():
        t = v.get("typed") or ""
        if isinstance(t, list):          # Physics flagged-items slices store [['typed', text], ...]
            t = " ".join(str(x[-1]) if isinstance(x, (list, tuple)) else str(x) for x in t)
        t = str(t).strip()
        if t and v.get("decision") in ("EDIT", "EDIT?", "ACCEPT+COMMENT"):
            out.append(f"- {t[:350]}")
    return "\n".join(out[:80]) or "(none for this module)"


def get_field(lesson, path):
    cur = lesson
    for tok in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        cur = cur[int(tok[1:-1])] if tok.startswith("[") else cur[tok]
    return cur


def review(g, mod, prefix, dec):
    unit = json.dumps(fc.strip({k: v for k, v in mod["UNIT"].items() if k in ("totalDuration", "phenomenon", "drivingQuestion", "substrand")}), ensure_ascii=False)
    r = g.call_claude(f"{RULES}\n\nTEACHER DECISIONS (binding):\n{dec}\n\nUNIT: {unit}", schema=REVIEW_SCHEMA, cache_prefix=prefix)
    if r is None:
        return None
    for it in r["issues"]:
        for k in ("quote_b", "correct_value", "calc_expr", "calc_stated"):
            it[k] = (it.get(k) or "").strip()
    return r["issues"]


def verify(issues, hay):
    keep, dropped, seen = [], [], set()
    for it in issues:
        if not fc.quote_ok(it["quote_a"], hay) or (it["quote_b"] and not fc.quote_ok(it["quote_b"], hay)):
            dropped.append((it, "quote not found"))
            continue
        if it["type"] in ("ARITHMETIC", "TIMING") and it["calc_expr"] and it["calc_stated"]:
            wrong = fc.calc_check(it["calc_expr"], it["calc_stated"])
            if wrong is False:
                dropped.append((it, "recomputed in code: the lesson is right"))
                continue
            it["code_confirmed"] = wrong is True
        key = fc.norm(it["quote_a"])[:80]
        if key in seen:
            continue
        seen.add(key)
        keep.append(it)
    return keep, dropped


def adjudicate(g, prefix, issues, dec):
    if not issues:
        return [], []
    listing = "\n".join(f"[{i}] type={x['type']} where={x['where']}\n    QUOTE A: {x['quote_a']}\n    QUOTE B: {x['quote_b']}\n    PROBLEM: {x['problem']}\n    CORRECT: {x['correct_value']}\n    CODE-CONFIRMED: {x.get('code_confirmed', False)}" for i, x in enumerate(issues))
    p = ("You are the strict second reviewer of a lesson-plan audit. The lessons are above. For each candidate defect, check ALL lessons yourself. "
         "confirmed=true only if it is a REAL, checkable defect (a wrong calculation or total, two places that really disagree, a wrong cross-reference, a clear scientific/maths error, an impossible figure); false for anything the lessons support, simplifications, style, teaching choices, doubts, or anything covered by a TEACHER DECISION below. "
         "autofix_ok=true ONLY if the correction is unambiguous (exactly one right value or wording, and you can state it), needs no teaching or content choice, does not change a teacher decision, a learning outcome or KICD content, and would not make other lessons or the Final Explanation disagree (if a number is used elsewhere, the fix must keep them consistent or be a pure error fix). "
         "For SCIENCE, autofix_ok needs a one-line standard reference in `reference`. A TIMING mismatch of 5 minutes or less IS unambiguous: autofix_ok=true, fixed by changing the minutes of the LAST phase listed (or the one with an explicit buffer) so the phases add up to the stated lesson duration; the lesson duration itself is never changed. If real but a choice or judgement is needed, confirmed=true and autofix_ok=false (it goes to the teachers). One-line reason each.\n\n"
         f"TEACHER DECISIONS (binding):\n{dec}\n\nCANDIDATES:\n{listing}")
    r = g.call_claude(p, schema=ADJ_SCHEMA, cache_prefix=prefix)
    if r is None:
        return None
    ver = {v["n"]: v for v in r["verdicts"]}
    conf = []
    rej = []
    for i, x in enumerate(issues):
        v = ver.get(i, {})
        if v.get("confirmed"):
            x["autofix_ok"] = bool(v.get("autofix_ok")) and (x["type"] != "SCIENCE" or bool((v.get("reference") or "").strip()))
            x["reference"] = (v.get("reference") or "").strip()
            if x["type"] == "TIMING" and x["autofix_ok"]:
                # mechanical gate: only gaps of 5 minutes or less may be auto-fixed; anything else goes to teachers
                try:
                    gap = abs(float(eval(x["calc_expr"], {"__builtins__": {}}, {})) if re.fullmatch(r"[0-9+\-*/().\s]*", x["calc_expr"]) else float("nan") - float(re.sub(r"[^0-9.\-]", "", x["calc_stated"])))
                except Exception:
                    gap = None
                if gap is None or gap != gap or gap > 5:
                    x["autofix_ok"] = False
            conf.append(x)
        else:
            rej.append({"type": x["type"], "problem": x["problem"][:200], "reason": (v.get("reason") or "")[:200]})
    return conf, rej


def fix(g, prefix, issues):
    listing = "\n".join(f"[{i}] ({x['type']}) {x['where']}: {x['problem']}\n    QUOTE A: {x['quote_a']}\n    QUOTE B: {x['quote_b']}\n    CORRECT: {x['correct_value']}" for i, x in enumerate(issues))
    p = ("Correct the listed defects in the LESSONS (above) with the SMALLEST possible exact find-and-replace edits. For each edit give: n (the defect), lesson (number, 1-based), path (a field path inside the lesson such as overview, teacherReflection, summaryTablePrompt.explained, slo.knowledge, slo.purposeInStoryline (the slo fields are ALWAYS under `slo.`), framework[2].teacherMoves, framework[0].learnerExperience, framework[3].sensemakingStrategy, framework[4].formativeAssessment), old (exact current text, 12-400 characters, must occur EXACTLY ONCE in that field) and new. "
         "Change only the wrong words or number. If a number is used in several lessons or in a data table, edit every place so they agree (one edit each). Do not change teaching, structure, learning outcomes or anything not listed. If a defect cannot be fixed with exact small edits, put it in cannot_fix.\n\nDEFECTS:\n" + listing)
    return g.call_claude(p, schema=FIX_SCHEMA, cache_prefix=prefix)


CAT = {"ARITHMETIC": ("consistency", [14]), "TIMING": ("timing", [3]), "INTERNAL_CONTRADICTION": ("consistency", [14]),
       "CROSS_REFERENCE": ("consistency", [14]), "SCIENCE": ("science", [6]), "IMPOSSIBLE_FIGURE": ("consistency", [14])}


def apply_edits(m, edits, issues, rnd):
    rf = REV / "change_records" / f"{m}.json"
    d = json.loads(rf.read_text())
    recs = d if isinstance(d, list) else d.get("records", [])
    n0 = max([int(x["id"].rsplit("-", 1)[1]) for x in recs if x["id"].startswith(f"{m}-r2-les-auto-")] + [0])
    out = []
    for j, e in enumerate(edits, 1):
        it = issues[e["n"]] if 0 <= e["n"] < len(issues) else issues[0]
        cat, crit = CAT[it["type"]]
        r = {"id": f"{m}-r2-les-auto-{n0 + j:03d}", "kind": "edit", "target": "lesson", "lesson": e["lesson"], "path": e["path"],
             "old": e["old"], "new": e["new"], "criteria": crit, "category": cat, "severity": "minor", "teacher_decision": False,
             "group": "R2-LES-AUTO",
             "why": f"Automatic lesson check (round {rnd}), {it['type']}: {it['problem'][:300]} Confirmed by a second reviewer; correction is unambiguous."}
        if cat == "science":
            r["reference"] = it["reference"] or "standard textbook fact"
        if j == 1:
            r["group_headline"] = "Lesson text corrected by the automatic consistency check"
        out.append(r)
    tmp = OUT / f"_{m}_records.json"
    tmp.write_text(json.dumps({"records": out}, ensure_ascii=False, indent=1))
    res = subprocess.run([PY, str(ROOT / "scripts/revise_apply.py"), "apply", m, str(tmp)], capture_output=True, text=True, env={**os.environ, "CBE_REVISED_DIR": str(REV)})
    tmp.unlink()
    tail = (res.stdout.strip().splitlines() or [""])[-1]
    return tail


def run_module(g, m, a):
    mod = fc.load(REV / "modules" / f"{m}_data.js")
    dec = decisions_text(m)
    hist, errors, clean, status = [], 0, 0, "RESIDUAL"
    residual, seen_res = [], set()
    for rnd in range(1, a.max_rounds + 1):
        if g._estimate_cost() > a.max_spend:
            status = "SKIPPED (spend cap)"
            break
        hay = fc.norm(" ".join(fc.strings(fc.strip(mod["LESSONS"]))))
        prefix = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
        raw, failed = [], 0
        for _ in range(a.reviewers):
            r = review(g, mod, prefix, dec)
            if r is None:
                failed += 1
            else:
                raw += r
        if failed:
            hist.append({"round": rnd, "error": f"{failed} reviewer call(s) failed: round does not count"})
            errors += 1
            if errors >= 3:
                status = "ERROR (reviewer calls keep failing)"
                break
            continue
        kept, dropped = verify(raw, hay)
        kept = [x for x in kept if fc.norm(x["quote_a"])[:80] not in seen_res]      # already handed to the teachers
        adj = adjudicate(g, prefix, kept, dec)
        if adj is None:
            hist.append({"round": rnd, "error": "adjudicator call failed: round does not count"})
            errors += 1
            if errors >= 3:
                status = "ERROR (adjudicator calls keep failing)"
                break
            continue
        conf, rej = adj
        auto = [x for x in conf if x["autofix_ok"]]
        for x in conf:
            if not x["autofix_ok"]:
                seen_res.add(fc.norm(x["quote_a"])[:80])
                residual.append({"type": x["type"], "where": x["where"], "problem": x["problem"], "quote_a": x["quote_a"][:300], "quote_b": x["quote_b"][:300], "correct_value": x["correct_value"]})
        h = {"round": rnd, "raw": len(raw), "verified": len(kept), "confirmed": len(conf), "autofix": len(auto), "to_teachers": len(conf) - len(auto), "fixed": 0,
             "rejected_by_second_reviewer": rej, "dropped_by_code": [{"type": d[0]["type"], "why": d[1], "problem": d[0]["problem"][:160]} for d in dropped]}
        if not auto:
            clean += 1
            hist.append(h)
            if clean >= a.clean_rounds:
                status = "CONVERGED"
                break
            continue
        clean = 0
        fx = fix(g, prefix, auto)
        if fx is None:
            h["fix"] = "fixer call failed"
            hist.append(h)
            continue
        good = []
        for e in fx["edits"]:
            try:
                field = get_field(mod["LESSONS"][e["lesson"] - 1], e["path"])
            except Exception:
                h.setdefault("rejected_edits", []).append(f"bad path {e['path']}")
                continue
            if not isinstance(field, str) or field.count(e["old"]) != 1 or not (12 <= len(e["old"]) <= 400) or len(e["new"]) > len(e["old"]) + 300 or e["old"] == e["new"]:
                h.setdefault("rejected_edits", []).append(f"L{e['lesson']} {e['path']}: old text not unique/within limits")
                continue
            good.append(e)
        for c in fx.get("cannot_fix", []):
            if 0 <= c["n"] < len(auto):
                x = auto[c["n"]]
                seen_res.add(fc.norm(x["quote_a"])[:80])
                residual.append({"type": x["type"], "where": x["where"], "problem": x["problem"], "quote_a": x["quote_a"][:300], "quote_b": x["quote_b"][:300], "correct_value": x["correct_value"], "note": "fixer could not make an exact small edit: " + c.get("reason", "")})
        if good:
            tail = apply_edits(m, good, auto, rnd)
            h["apply"] = tail
            h["fixed"] = len(good) if "0 rejected" in tail else 0
            mod = fc.load(REV / "modules" / f"{m}_data.js")
        hist.append(h)
    # drop teacher items whose wording was changed by a later fix (the quote no longer exists)
    final_hay = fc.norm(" ".join(fc.strings(fc.strip(mod["LESSONS"]))))
    residual = [x for x in residual if fc.norm(x["quote_a"])[:60] in final_hay]
    if status == "RESIDUAL" and not residual:
        status = "RESIDUAL (max rounds reached with fixes still being found)"
    res = {"module": m, "status": status, "rounds": hist, "for_teachers": residual}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{m}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", required=True)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--max-spend", type=float, default=40.0)
    ap.add_argument("--max-rounds", type=int, default=4)
    ap.add_argument("--clean-rounds", type=int, default=1, help="consecutive rounds with nothing to fix that end the loop (lessons are long: 1 by default)")
    ap.add_argument("--reviewers", type=int, default=2)
    a = ap.parse_args()
    import generate_substrand as g
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_module, g, m, a): m for m in a.only.split(",")}
        for f in as_completed(futs):
            m = futs[f]
            try:
                r = f.result()
                print(f"{m}: {r['status']} | rounds={len(r['rounds'])} edits_applied={sum(h.get('fixed', 0) for h in r['rounds'])} for_teachers={len(r['for_teachers'])}", flush=True)
            except Exception as e:
                print(f"{m}: ERROR {e!r}", flush=True)
    print(f"estimated spend this session: ${g._estimate_cost():.2f}")


if __name__ == "__main__":
    main()
