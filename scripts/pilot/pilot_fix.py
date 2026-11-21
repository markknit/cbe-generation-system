#!/usr/bin/env python3
"""
pilot_fix.py - option 2 of the pilot (Mark, 2026-11-12, $1.5 cap): apply the audit's confirmed lesson defects to the pilot modules with
exact find/replace edits, then run ONE confirming Opus lesson audit. Writes ONLY inside data/pilot_2026-11 (the pre-fix file is kept as *_prefix_data.js).
CBE_REVISED_DIR=<abs>/data/pilot_2026-11 CBE_GEN_OUT_DIR=<abs>/data/pilot_2026-11/modules venv/bin/python scripts/pilot/pilot_fix.py --max-spend 1.5
"""
import argparse, json, os, re, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pilot_run as pr  # noqa
from pilot_run import fc, lc, g, PILOT, run_phase, LEDGER  # noqa


def locate(lesson, path):
    toks = re.findall(r"[^.\[\]]+|\[\d+\]", path)
    cur = lesson
    for t in toks[:-1]:
        cur = cur[int(t[1:-1])] if t.startswith("[") else cur[t]
    return cur, toks[-1]


def apply_edit(lessons, e):
    les = next((l for l in lessons if l["number"] == e["lesson"]), None)
    if les is None:
        return "no such lesson"
    try:
        parent, key = locate(les, e["path"])
        key = int(key[1:-1]) if key.startswith("[") else key
        text = parent[key]
    except Exception as ex:
        return f"bad path {e['path']}: {ex}"
    if not isinstance(text, str) or text.count(e["old"]) != 1:
        return f"old text occurs {text.count(e['old']) if isinstance(text, str) else 'n/a'} times"
    parent[key] = text.replace(e["old"], e["new"])
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-spend", type=float, default=1.5)
    ap.add_argument("--targets", default="gensci_2_4,essmath_2_8,coremath_2_4")
    a = ap.parse_args()
    report = {}
    try:
        for t in a.targets.split(","):
            res = json.load(open(PILOT / f"result_{t}.json"))
            issues = res["new"]["confirmed_issues"]
            for x in issues:
                x.setdefault("quote_b", ""); x["correct_value"] = x.get("correct_value", "")
            path = Path(os.environ["CBE_GEN_OUT_DIR"]) / f"pilot_{t}_data.js"
            pre = path.with_name(f"pilot_{t}_prefix_data.js")
            if not pre.exists():
                shutil.copy(path, pre)
            mod = fc.load(path)
            prefix = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
            fx = run_phase(f"{t}:fix", lambda: lc.fix(g, prefix, issues), a.max_spend, "claude-sonnet-5-5")
            r = {"issues": len(issues), "edits": [], "failed": [], "cannot_fix": (fx or {}).get("cannot_fix", [])}
            for e in (fx or {}).get("edits", []):
                err = apply_edit(mod["LESSONS"], e)
                (r["failed"] if err else r["edits"]).append({**{k: e[k] for k in ("n", "lesson", "path", "old", "new")}, **({"error": err} if err else {})})
            if r["edits"]:
                meta = mod["META"]
                st = g.derive_summary_table(mod["UNIT"], mod["LESSONS"], meta["substrand_id"], meta["substrand_name"])
                g.write_data_file(f"pilot_{t}", meta, mod["UNIT"], mod["LESSONS"], mod["FINAL_EXPLANATION"], st)
                mod = fc.load(path)
            prefix2 = f"THE LESSON PLAN, all lessons in full (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False, indent=0)}\n"
            raw = run_phase(f"{t}:confirm_audit", lambda: pr.lesson_audit(mod), a.max_spend, "claude-opus-5-5")
            raw_i, kept, dropped, _ = raw
            conf, rej = ([], [])
            if kept:
                conf, rej = run_phase(f"{t}:confirm_adjudicate", lambda: pr.adjudicate_lessons(prefix2, kept), a.max_spend, "claude-sonnet-5-5")
            r["confirm_audit"] = {"raw": len(raw_i), "verified": len(kept), "confirmed": len(conf), "issues": [pr.brief(i) for i in conf]}
            report[t] = r
    except pr.Cap as e:
        report["stopped"] = str(e)
        print("STOPPED:", e)
    report["cost"] = LEDGER["total"]; report["phases"] = LEDGER["phases"]
    (PILOT / "result_option2.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print("total $", LEDGER["total"])


if __name__ == "__main__":
    main()
