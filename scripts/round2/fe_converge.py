#!/usr/bin/env python3
"""
fe_converge.py — make each revised Final Explanation (FE) follow its lessons, automatically, until it stops finding problems
==========================================================================================================================
Mark's rule (2026-11-09): the LESSON PLAN is the arbiter; the FE follows it; no new teacher review for routine mismatches;
never introduce a clear inaccuracy; teachers only get decisions that cannot be settled otherwise.

One round per module:
  1. REVIEW  K independent reviewer calls (claude-sonnet-5-5) see the FULL lesson text (not the digest the old reviewer saw:
             most of its false positives were things the digest had left out) and the FE. Every finding must quote the FE
             and, where relevant, the lesson. Arithmetic findings must carry a python expression.
  2. VERIFY  mechanically, no model: quotes must really occur in the FE / lessons (else the finding is dropped);
             arithmetic is recomputed in code (the finding stands only if the code disagrees with the FE).
  3. ADJUDICATE  one more call judges the remaining findings against the lessons (confirm / reject, with a reason).
  4. FIX     confirmed FE findings -> one call returns corrected sections; structure and size are checked; the change is
             applied through revise_apply as records `<m>-r2-fe-auto-NNN` (group R2-FE-AUTO), so the journal shows before/after.
  Stop when TWO consecutive rounds confirm nothing (CONVERGED) or after --max-rounds (RESIDUAL).
Findings that only the lessons can fix (lessons contradict each other, impossible figure, a lesson that is itself wrong) are
NEVER used to change the lessons: they go to the module's RESIDUAL list for the teachers, and the FE is worded so that it does
not depend on the contested point. Result per module: data/revised_2026-10_full/fe_converge/<m>.json.

COSTS API MONEY. CBE_REVISED_DIR=data/revised_2026-10_full venv/bin/python scripts/round2/fe_converge.py --only a,b [--max-spend 40]
"""
import argparse
import difflib
import json
import math
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REV = Path(os.environ["CBE_REVISED_DIR"])
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
PY = sys.executable
OUT = REV / "fe_converge"
SKIP_KEYS = {"resourceLinks", "aresKeywords", "aresQuery"}


def _s():
    return {"type": "string"}


REVIEW_SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"issues": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "properties": {"type": {"type": "string", "enum": ["FE_CONTRADICTS_LESSONS", "ARITHMETIC", "SCIENCE", "SELF_CONTRADICTION",
                                                        "RUBRIC_GAP", "LESSON_CONFLICT"]},
                   "where": _s(), "fe_quote": _s(), "lesson_quote": _s(), "problem": _s(), "suggested_fix": _s(),
                   "calc_expr": _s(), "calc_stated": _s()},
    "required": ["type", "where", "fe_quote", "problem"]}}},
    "required": ["issues"]}
ADJ_SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"verdicts": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "properties": {"n": {"type": "integer"}, "confirmed": {"type": "boolean"}, "reason": _s()},
    "required": ["n", "confirmed"]}}}, "required": ["verdicts"]}
FIX_SCHEMA = {"type": "object", "additionalProperties": False, "properties": {
    "instructions": _s(),
    "sections": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                            "properties": {"title": _s(), "prompt": _s(), "exemplar": _s()},
                                            "required": ["title", "prompt", "exemplar"]}},
    "cannot_fix": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                                              "properties": {"n": {"type": "integer"}, "reason": _s()}, "required": ["n"]}}},
    "required": ["instructions", "sections", "cannot_fix"]}


def load(path):
    return json.loads(subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(path)],
                                     capture_output=True, text=True, check=True).stdout)


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in SKIP_KEYS}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip().lower()


def quote_ok(q, hay):
    """a quote may use '...' / '…' for omissions: every fragment of >= 12 chars must occur in the haystack"""
    if not q.strip():
        return True
    frags = [f for f in re.split(r"\.\.\.|…", q) if len(norm(f)) >= 12]
    return bool(frags) and all(norm(f) in hay for f in frags) if frags else norm(q) in hay


SAFE = {k: getattr(math, k) for k in ("sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "log", "log10", "exp", "pi", "e", "radians", "degrees", "floor", "ceil")}
SAFE["abs"] = abs
SAFE["round"] = round


def calc_check(expr, stated):
    """True = FE is wrong (code disagrees), False = FE is right, None = cannot judge"""
    try:
        if not re.fullmatch(r"[0-9a-zA-Z_+\-*/().,\s^<>=]*", expr) or "__" in expr:
            return None
        val = eval(expr.replace("^", "**"), {"__builtins__": {}}, SAFE)
        sv = float(re.sub(r"[^0-9.\-eE]", "", stated))
        return abs(val - sv) > max(0.006 * abs(val), 0.0051)
    except Exception:
        return None


def full_lessons(mod):
    return json.dumps(strip(mod["LESSONS"]), ensure_ascii=False, indent=0)


def fe_view(mod):
    fe = mod["FINAL_EXPLANATION"]
    return {"instructions": fe.get("instructions", ""), "sections": fe["sections"], "rubric_criteria": [r["criterion"] for r in fe.get("rubric", [])]}


RULES = """You audit a Final Explanation (FE) against the LESSON PLAN of a Kenyan CBE Grade 10 sub-strand. THE LESSON PLAN IS THE AUTHORITY: the FE must follow it. The lessons are the full text above. Learners met the lesson content in class and the FE assesses it.
Report ONLY real defects, each backed by an exact quote (copy words exactly; "..." may mark omitted words):
- FE_CONTRADICTS_LESSONS: the FE states a number, name, place, dataset, method or term that the lessons contradict, or that appears in NO lesson in a way learners could have met (check ALL lessons before you claim something was not taught). fe_quote = the FE words, lesson_quote = the lesson words it conflicts with (or "" if absent from all lessons).
- ARITHMETIC: a calculation in the FE is wrong. calc_expr = a python expression for the correct value (math functions sqrt, sin, cos in RADIANS, pi allowed; use only numbers and operators), calc_stated = the number the FE states. fe_quote = the FE sentence.
- SCIENCE: a clear scientific or mathematical error in the FE (not a simplification stated in the lessons). Say what is correct.
- SELF_CONTRADICTION: two places in the FE disagree.
- RUBRIC_GAP: a rubric criterion (listed under rubric_criteria) that no FE prompt lets the learner demonstrate at all.
- LESSON_CONFLICT: two lessons contradict each other, or a lesson has an impossible figure, or a lesson is itself scientifically wrong, in a way that touches what the FE asks. (This cannot be fixed in the FE; quote both lessons in lesson_quote.)
Do NOT report: prompts that hint at or restate what the learner must explain (that is scaffolding, not a defect), style, wording preferences, extra detail that is correct, simplifications the lessons make, hedging, missing coverage of lesson content, or anything you are not sure about. If unsure, leave it out. Return {"issues": []} when there is nothing real. suggested_fix: the smallest change to the FE that fixes it ("" for LESSON_CONFLICT). Unused fields: empty string."""


def review(g, mod, prefix):
    fe = json.dumps(fe_view(mod), ensure_ascii=False, indent=1)
    r = g.call_claude(f"{RULES}\n\nTHE FINAL EXPLANATION UNDER AUDIT (JSON):\n{fe}", schema=REVIEW_SCHEMA, cache_prefix=prefix)
    if r is None:
        return None
    for it in r["issues"]:
        for k in ("lesson_quote", "suggested_fix", "calc_expr", "calc_stated"):
            it[k] = (it.get(k) or "").strip()
    return r["issues"]


def verify(issues, fe_hay, lesson_hay):
    keep, dropped = [], []
    seen = set()
    for it in issues:
        if not quote_ok(it["fe_quote"], fe_hay) or (it["type"] in ("LESSON_CONFLICT",) and not quote_ok(it["lesson_quote"], lesson_hay)) \
                or (it["lesson_quote"] and it["type"] == "FE_CONTRADICTS_LESSONS" and not quote_ok(it["lesson_quote"], lesson_hay)):
            dropped.append((it, "quote not found"))
            continue
        if it["type"] == "ARITHMETIC":
            wrong = calc_check(it["calc_expr"], it["calc_stated"]) if it["calc_expr"] and it["calc_stated"] else None
            if wrong is False:
                dropped.append((it, "recomputed in code: FE is right"))
                continue
            it["code_confirmed"] = wrong is True
        key = norm(it["fe_quote"])[:80] + it["type"]
        if key in seen:
            continue
        seen.add(key)
        keep.append(it)
    return keep, dropped


def adjudicate(g, mod, prefix, issues):
    if not issues:
        return [], []
    listing = "\n".join(f"[{i}] type={x['type']} where={x['where']}\n    FE: {x['fe_quote']}\n    LESSON: {x['lesson_quote']}\n    PROBLEM: {x['problem']}" for i, x in enumerate(issues))
    fe = json.dumps(fe_view(mod), ensure_ascii=False, indent=1)
    p = (f"You are the strict second reviewer. THE LESSONS (above) ARE THE AUTHORITY. Below are candidate defects found by another reviewer in the FE, and the FE.\n"
         f"For each candidate, search ALL the lessons yourself, then decide: confirmed=true only if it is a REAL defect that a careful teacher would want fixed (the FE contradicts what the lessons say, a real calculation/science error, a real self-contradiction, a prompt that really states its own answer, a real lesson conflict). "
         f"confirmed=false for anything the lessons do teach or allow, for style, for correct extra detail, for hedges, or if you are not sure. Give a one-line reason citing the lesson.\n\nFE:\n{fe}\n\nCANDIDATES:\n{listing}")
    r = g.call_claude(p, schema=ADJ_SCHEMA, cache_prefix=prefix)
    if r is None:
        return None
    ok = {v["n"]: v["confirmed"] for v in r["verdicts"]}
    why = {v["n"]: v.get("reason", "") for v in r["verdicts"]}
    rej = [{"type": x["type"], "problem": x["problem"][:200], "reason": why.get(i, "")[:200]} for i, x in enumerate(issues) if not ok.get(i)]
    return [x for i, x in enumerate(issues) if ok.get(i)], rej


def fix(g, mod, prefix, issues):
    fe = json.dumps(fe_view(mod), ensure_ascii=False, indent=1)
    listing = "\n".join(f"[{i}] ({x['type']}) {x['where']}: {x['problem']}\n    FE: {x['fe_quote']}\n    LESSON: {x['lesson_quote']}\n    SUGGESTED: {x['suggested_fix']}" for i, x in enumerate(issues))
    p = ("Correct the Final Explanation so that it follows the LESSONS (above, authoritative) and has none of the listed defects.\n"
         "Rules: change as little as possible, keep every section title and the section count; keep student prompts free of their own answers; "
         "keep prompt and exemplar consistent; do not invent facts, names or numbers that the lessons do not contain; every number you write must be "
         "recomputed correctly; do not touch anything that is not part of a listed defect. If a defect comes from a lesson that is itself wrong or from two lessons "
         "that disagree, do NOT copy the error: word the FE so that it does not depend on the contested point, and list it in cannot_fix with the reason. "
         "If you truly cannot fix an item without inventing content, list it in cannot_fix.\n"
         f"Return the full corrected `instructions` and all `sections` (title, prompt, exemplar).\n\nFE:\n{fe}\n\nDEFECTS:\n{listing}")
    return g.call_claude(p, schema=FIX_SCHEMA, cache_prefix=prefix)


def changed_fields(mod, new):
    fe = mod["FINAL_EXPLANATION"]
    ch = []
    if new["instructions"].strip() != fe.get("instructions", "").strip():
        ch.append(("instructions", fe.get("instructions", ""), new["instructions"]))
    for i, (o, n) in enumerate(zip(fe["sections"], new["sections"])):
        for k in ("prompt", "exemplar"):
            if o.get(k, "").strip() != n[k].strip():
                ch.append((f"sections[{i}].{k}", o.get(k, ""), n[k]))
    return ch


def apply_records(m, mod, changes, issues, round_no):
    rec_file = REV / "change_records" / f"{m}.json"
    d = json.loads(rec_file.read_text())
    recs = d if isinstance(d, list) else d.get("records", [])
    n0 = max([int(x["id"].rsplit("-", 1)[1]) for x in recs if x["id"].startswith(f"{m}-r2-fe-auto-")] + [0])
    types = sorted({x["type"] for x in issues})
    summary = "; ".join(f"{x['type']}: {x['problem'][:160]}" for x in issues[:4])
    out = []
    for j, (path, old, new) in enumerate(changes, 1):
        r = {"id": f"{m}-r2-fe-auto-{n0 + j:03d}", "kind": "set", "target": "final_explanation", "path": path, "value": new,
             "criteria": [14], "category": "consistency", "severity": "minor", "teacher_decision": False,
             "group": "R2-FE-AUTO", "why": f"Automatic Final Explanation check (round {round_no}): the lessons are the authority and the FE did not follow them. Findings ({', '.join(types)}), each confirmed by a second reviewer: {summary}"}
        if j == 1:
            r["group_headline"] = "Final Explanation brought in line with the lessons by the automatic consistency check"
        out.append(r)
    tmp = OUT / f"_{m}_records.json"
    tmp.write_text(json.dumps({"records": out}, ensure_ascii=False, indent=1))
    res = subprocess.run([PY, str(ROOT / "scripts/revise_apply.py"), "apply", m, str(tmp)], capture_output=True, text=True,
                         env={**os.environ, "CBE_REVISED_DIR": str(REV)})
    tmp.unlink()
    tail = (res.stdout.strip().splitlines() or [""])[-1]
    return "0 rejected" in tail, tail


def run_module(g, m, a):
    mod = load(REV / "modules" / f"{m}_data.js")
    hist, residual, clean, errors = [], {"cannot_fix": [], "lesson_conflicts": [], "unfixed": []}, 0, 0
    status = "RESIDUAL"
    lesson_hay = norm(" ".join(strings(strip(mod["LESSONS"]))))
    prefix = f"THE LESSON PLAN (authoritative), all lessons in full (JSON):\n{full_lessons(mod)}\n"
    for rnd in range(1, a.max_rounds + 1):
        if g._estimate_cost() > a.max_spend:
            status = "SKIPPED (spend cap)"
            break
        fe_hay = norm(" ".join(strings(fe_view(mod))))
        raw, failed = [], 0
        for _ in range(a.reviewers):
            r = review(g, mod, prefix)
            if r is None:
                failed += 1
                continue
            raw += r
        if failed:
            hist.append({"round": rnd, "error": f"{failed} reviewer call(s) failed: round does not count"})
            errors += 1
            if errors >= 3:
                status = "ERROR (reviewer calls keep failing)"
                break
            continue
        kept, dropped = verify(raw, fe_hay, lesson_hay)
        adj = adjudicate(g, mod, prefix, kept)
        confirmed, rejected = (None, []) if adj is None else adj
        if confirmed is None:
            hist.append({"round": rnd, "error": "adjudicator call failed: round does not count"})
            errors += 1
            if errors >= 3:
                status = "ERROR (adjudicator calls keep failing)"
                break
            continue
        conflicts = [x for x in confirmed if x["type"] == "LESSON_CONFLICT"]
        fixable = [x for x in confirmed if x["type"] != "LESSON_CONFLICT"]
        for c in conflicts:
            if not any(norm(c["problem"])[:60] == norm(p["problem"])[:60] for p in residual["lesson_conflicts"]):
                residual["lesson_conflicts"].append({k: c[k] for k in ("where", "problem", "lesson_quote")})
        h = {"round": rnd, "raw": len(raw), "verified": len(kept), "confirmed_fixable": len(fixable), "lesson_conflicts": len(conflicts), "fixed": 0,
             "rejected_by_second_reviewer": rejected, "dropped_by_code": [{"type": d[0]["type"], "why": d[1], "problem": d[0]["problem"][:160]} for d in dropped]}
        if not fixable:
            clean += 1
            hist.append(h)
            if clean >= 2:
                status = "CONVERGED"
                break
            continue
        clean = 0
        fx = fix(g, mod, prefix, fixable)
        if fx is None or len(fx["sections"]) != len(mod["FINAL_EXPLANATION"]["sections"]) or \
                [s["title"] for s in fx["sections"]] != [s["title"] for s in mod["FINAL_EXPLANATION"]["sections"]]:
            h["fix"] = "fixer call failed or changed the structure"
            hist.append(h)
            continue
        ch = changed_fields(mod, fx)
        big = [p for p, o, n in ch if difflib.SequenceMatcher(None, o, n).ratio() < 0.55]
        if big:
            h["fix"] = f"rejected: too large a rewrite in {big}"
            hist.append(h)
            residual["unfixed"].append(h["fix"])
            continue
        for c in fx["cannot_fix"]:
            if 0 <= c["n"] < len(fixable):
                residual["cannot_fix"].append({"problem": fixable[c["n"]]["problem"], "reason": c["reason"]})
        if ch:
            ok, tail = apply_records(m, mod, ch, fixable, rnd)
            h["fixed"] = len(ch) if ok else 0
            h["apply"] = tail
            mod = load(REV / "modules" / f"{m}_data.js")
        hist.append(h)
    if status == "RESIDUAL" and not residual["unfixed"] and not residual["cannot_fix"]:
        status = "RESIDUAL (max rounds reached with fixes still being found)"
    result = {"module": m, "status": status, "rounds": hist, "residual_for_teachers": residual}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{m}.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", required=True)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--max-spend", type=float, default=40.0)
    ap.add_argument("--max-rounds", type=int, default=6)
    ap.add_argument("--reviewers", type=int, default=2)
    a = ap.parse_args()
    import generate_substrand as g
    OUT.mkdir(exist_ok=True)
    mods = a.only.split(",")
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(run_module, g, m, a): m for m in mods}
        for f in as_completed(futs):
            m = futs[f]
            try:
                r = f.result()
                fixed = sum(h.get("fixed", 0) for h in r["rounds"])
                print(f"{m}: {r['status']} | rounds={len(r['rounds'])} fields_fixed={fixed} "
                      f"lesson_conflicts={len(r['residual_for_teachers']['lesson_conflicts'])} cannot_fix={len(r['residual_for_teachers']['cannot_fix'])}", flush=True)
            except Exception as e:  # keep the batch going
                print(f"{m}: ERROR {e!r}", flush=True)
    print(f"estimated spend this session: ${g._estimate_cost():.2f}")


main()
