#!/usr/bin/env python3
"""
generate_substrand_decks.py — author, build and validate the decks of one sub-strand (presentations branch).

  python3 scripts/generate_substrand_decks.py --data data/outputs/v2/Biology/SS1.1_Cell_Structure/Biology_Cell_Structure_data.json [--lessons 1,3-12] [--parallel 3] [--first 1]

The `--first` lesson (default: lesson 1, the anchor phenomenon) runs alone first so that shared scenes and characters
(e.g. the healing finger) exist in the art catalogue before the other lessons reuse them; the rest run `--parallel` at a time.
Each lesson is the full pipeline of src/generate_deck.py (author -> art -> build -> validate -> review -> repair).
Per-lesson logs: logs/deck_runs/L<n>.log. Summary: data/presentations_specs/<Subject>/<SubStrand>/SUMMARY.json
"""
import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse(spec, n):
    out = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-"); out |= set(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return sorted(x for x in out if 1 <= x <= n)


def run_one(py, data, lesson):
    log = os.path.join(ROOT, "logs", "deck_runs"); os.makedirs(log, exist_ok=True)
    t0 = time.time()
    with open(os.path.join(log, f"L{lesson}.log"), "w") as f:
        rc = subprocess.run([py, os.path.join(ROOT, "src", "generate_deck.py"), "--data", data, "--lesson", str(lesson)], cwd=ROOT, stdout=f, stderr=subprocess.STDOUT).returncode
    return lesson, rc, round(time.time() - t0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--lessons", default="")
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--parallel", type=int, default=3)
    a = ap.parse_args()
    data = os.path.abspath(a.data)
    d = json.load(open(data)); n = len(d["LESSONS"])
    lessons = parse(a.lessons, n) if a.lessons else list(range(1, n + 1))
    py = sys.executable
    results = []
    first = [l for l in lessons if l == a.first]
    rest = [l for l in lessons if l != a.first]
    for l in first:
        print(f"lesson {l} (first, alone)...", flush=True); results.append(run_one(py, data, l)); print("  ->", results[-1], flush=True)
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as ex:
        futs = {ex.submit(run_one, py, data, l): l for l in rest}
        for fu in cf.as_completed(futs):
            results.append(fu.result()); print("  ->", results[-1], flush=True)
    results.sort()
    sub = os.path.basename(os.path.dirname(data))
    outp = os.path.join(ROOT, "data", "presentations_specs", d["META"]["subject"], sub, "SUMMARY.json")
    summary = []
    for l, rc, secs in results:
        bl = os.path.join(os.path.dirname(outp), f"L{l}.buildlog.json")
        info = {"lesson": l, "exit": rc, "seconds": secs}
        if os.path.exists(bl):
            b = json.load(open(bl)); info.update(cost_usd=b.get("total_usd_est"), problems=b.get("final_problems"), review=(b.get("review_final") or {}).get("verdict"), build_log_items=len(b.get("build_log", [])))
        summary.append(info)
    json.dump(summary, open(outp, "w"), indent=1)
    print(json.dumps(summary, indent=1))
    return 1 if any(r[1] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
