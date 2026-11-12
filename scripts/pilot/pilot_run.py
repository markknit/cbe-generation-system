#!/usr/bin/env python3
"""
pilot_run.py - pilot of the 'checks built into the first pass' process (Mark, 2026-11-12, $10 cap)
===================================================================================================
Per target (e.g. gensci_2_4): (1) generate with the existing pipeline + authoring checklist into data/pilot_2026-11/modules,
(2) ONE Opus lesson audit (Round 2 rules, code-verified, Sonnet adjudicated), (3) ONE Sonnet FE-vs-lessons audit,
(4) optional baseline: the same Opus lesson audit on the existing first-generation module in generators/data.
Nothing in generators/data or the revised workspace is changed. Fixes are NOT applied (counts only).
CBE_REVISED_DIR=<abs>/data/pilot_2026-11 CBE_GEN_OUT_DIR=<abs>/data/pilot_2026-11/modules \
 CBE_EXTRA_SYSTEM_FILE=<abs>/scripts/pilot/authoring_checklist.txt venv/bin/python scripts/pilot/pilot_run.py --target gensci_2_4 --max-spend 10
"""
import argparse, json, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/round2")); sys.path.insert(0, str(ROOT / "src"))
import fe_converge as fc  # noqa
import lesson_converge as lc  # noqa
import generate_substrand as g  # noqa

PILOT = ROOT / "data/pilot_2026-11"
TARGETS = {  # name: (subject, substrand, curriculum slice)
    "gensci_2_4": ("general_science", "2.4", "gensci_2_4.txt"),
    "essmath_2_8": ("essential_mathematics", "2.8", "essmath_2_8.txt"),
    "coremath_2_4": ("core_mathematics", "2.4", "coremath_2_4.txt"),
}
PRICES = {"claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0)}
LEDGER = {"total": 0.0, "phases": {}}
_orig_call = g.call_claude


class Cap(Exception):
    pass


def usage():
    return g._USAGE["sync_input"], g._USAGE["sync_output"]


def live_total(snap):
    i, o = usage(); pi, po = PRICES[g.MODEL]
    return LEDGER["total"] + ((i - snap[0]) * pi + (o - snap[1]) * po) / 1e6


def run_phase(name, fn, cap, model):
    g.MODEL = model
    snap = usage()
    def capped(*a, **k):
        if live_total(snap) > cap:
            raise Cap(f"spend cap ${cap} reached in phase {name}")
        return _orig_call(*a, **k)
    g.call_claude = capped
    t0 = time.time()
    try:
        return fn()
    finally:
        g.call_claude = _orig_call
        c = round(live_total(snap) - LEDGER["total"], 4)
        LEDGER["phases"][name] = {"cost": c, "secs": round(time.time() - t0), "model": model}
        LEDGER["total"] = round(LEDGER["total"] + c, 4)
        print(f"[{name}] ${c}  running total ${LEDGER['total']}", flush=True)


def generate(target, lessons):
    subj, ss, cur = TARGETS[target]
    os.environ["CBE_CURRICULUM_TEXT_FILE"] = str(PILOT / "curriculum" / cur)
    sys.argv = ["generate_substrand.py", "--subject", subj, "--grade", "10", "--substrand", ss,
                "--output", f"pilot_{target}", "--lessons", str(lessons)]
    g.SYSTEM_PROMPT = g.build_system_prompt(10)
    g.main()


def lesson_audit(mod):
    prefix = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
    raw = lc.review(g, mod, prefix, "(none: this is newly written text)") or []
    hay = fc.norm(" ".join(fc.strings(fc.strip(mod["LESSONS"]))))
    kept, dropped = lc.verify(raw, hay)
    return raw, kept, dropped, prefix


def adjudicate_lessons(prefix, kept):
    r = lc.adjudicate(g, prefix, kept, "(none)")
    return r if r is not None else ([], [])


def fe_audit(mod):
    prefix = f"THE LESSON PLAN (authoritative), all lessons in full (JSON):\n{fc.full_lessons(mod)}\n"
    raw = fc.review(g, mod, prefix) or []
    kept, dropped = fc.verify(raw, fc.norm(" ".join(fc.strings(fc.fe_view(mod)))), fc.norm(" ".join(fc.strings(fc.strip(mod["LESSONS"])))))
    adj = fc.adjudicate(g, mod, prefix, kept)
    conf, rej = adj if adj else ([], [])
    return raw, kept, conf


def brief(i):
    return {k: i.get(k) for k in ("type", "where", "quote_a", "problem", "correct_value", "code_confirmed", "autofix_ok", "reference") if i.get(k) not in (None, "")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, choices=list(TARGETS))
    ap.add_argument("--max-spend", type=float, default=10.0)
    ap.add_argument("--spent-before", type=float, default=0.0, help="spend by earlier targets in this pilot, counted against the cap")
    ap.add_argument("--lessons", type=int, default=8)
    ap.add_argument("--no-gen", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    a = ap.parse_args()
    cap = a.max_spend - a.spent_before
    out = {"target": a.target, "phases": LEDGER["phases"]}
    outf = PILOT / f"result_{a.target}.json"
    path = Path(os.environ["CBE_GEN_OUT_DIR"]) / f"pilot_{a.target}_data.js"
    try:
        if not a.no_gen:
            run_phase("generate", lambda: generate(a.target, a.lessons), cap, "claude-sonnet-5-5")
        mod = fc.load(path)
        out["lessons"] = len(mod["LESSONS"]); out["fe_present"] = bool(mod.get("FINAL_EXPLANATION"))
        raw, kept, dropped, prefix = run_phase("opus_lesson_review", lambda: lesson_audit(mod), cap, "claude-opus-5-5")
        conf, rej = run_phase("adjudicate_lessons", lambda: adjudicate_lessons(prefix, kept), cap, "claude-sonnet-5-5")
        out["new"] = {"raw": len(raw), "verified": len(kept), "confirmed": len(conf), "confirmed_issues": [brief(i) for i in conf],
                      "rejected": rej, "dropped_by_code": [(d[0]["type"], d[1]) for d in dropped]}
        fraw, fkept, fconf = run_phase("sonnet_fe_audit", lambda: fe_audit(mod), cap, "claude-sonnet-5-5")
        out["fe"] = {"raw": len(fraw), "verified": len(fkept), "confirmed": len(fconf), "confirmed_issues": [{k: i.get(k) for k in ("type", "where", "fe_quote", "problem")} for i in fconf]}
        if a.baseline:
            old = fc.load(ROOT / "generators/data" / f"{a.target}_data.js")
            braw, bkept, bdropped, bprefix = run_phase("baseline_opus_review", lambda: lesson_audit(old), cap, "claude-opus-5-5")
            bconf, brej = run_phase("baseline_adjudicate", lambda: adjudicate_lessons(bprefix, bkept), cap, "claude-sonnet-5-5")
            out["baseline_old_module"] = {"lessons": len(old["LESSONS"]), "raw": len(braw), "verified": len(bkept), "confirmed": len(bconf),
                                          "confirmed_issues": [brief(i) for i in bconf]}
    except Cap as e:
        out["stopped"] = str(e)
        print("STOPPED:", e, flush=True)
    out["total_cost"] = LEDGER["total"]
    outf.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("total $", LEDGER["total"], "->", outf)


if __name__ == "__main__":
    main()
