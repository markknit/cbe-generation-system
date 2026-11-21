#!/usr/bin/env python3
"""
revise_lessons.py: replace a revised module's whole lesson list (split / merge / insert lessons) and keep everything consistent.
(Round 2, 2026-11-09. revise_apply.py edits fields only; it cannot change the number of lessons.)

  export CBE_REVISED_DIR=$PWD/data/revised_2026-10_full
  venv/bin/python scripts/round2/revise_lessons.py MODULE NEW.json [--dry-run]

NEW.json: {"lessons": [ <lesson object>, ... in teaching order ],       # complete list, final order
           "unit": {"totalDuration": "...", ...},                       # optional UNIT fields to overwrite
           "final_explanation": {"path": value, ...},                   # optional: top-level FE fields to overwrite
           "group": "R2-SPLIT", "why": "Teacher request ... (journal item ids)",
           "origin": {"<new position>": "<what it came from, e.g. 'L5 first half (old numbering)'>"} }
Lessons are renumbered by position (1..N): any 'number' you give is ignored. Every lesson must keep the contract
(5 canonical phases in order, all fields). The tool then: rewrites const LESSONS and UNIT in the module, re-derives
SUMMARY_TABLE (display id/name from UNIT.substrand), and appends ONE change record per lesson that is new or whose
content changed (kind=set, target=lesson, category=timing/pedagogy, teacher_decision=true because new lessons are
model-drafted and need a teacher's read-through). Then run revise_build.py + validate_corpus.js yourself.
Also run scripts/round2/sync_display_labels.py afterwards: the subtitle carries the lesson count.
"""
import datetime, json, os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "src"))
if "CBE_REVISED_DIR" not in os.environ:
    sys.exit("set CBE_REVISED_DIR in the same command (else the old workspace is used)")
import revise_apply as ra                                   # noqa: E402
from repair_lesson_drift import replace_lessons_block       # noqa: E402
from rebuild_consistency import replace_block               # noqa: E402
from generate_substrand import derive_summary_table         # noqa: E402

PHASES = ["Predict Phase", "Observe Phase", "Explain Phase", "Driving Question Board (DQB) Creation", "Model Building Phase"]
ap = sys.argv[1:]
dry = "--dry-run" in ap
ap = [a for a in ap if not a.startswith("--")]
module, newf = ap[0], ap[1]
mod = ra.REV / "modules" / f"{module}_data.js"
m = ra.load_module(mod)
spec = json.loads(Path(newf).read_text())
new = spec["lessons"]
errs = []
for i, l in enumerate(new, 1):
    l["number"] = i
    ph = [p.get("phase") for p in l.get("framework", [])]
    if ph != PHASES:
        errs.append(f"lesson {i}: phases {ph}")
    for k in ("title", "duration", "overview", "teacherReflection", "slo", "summaryTablePrompt"):
        if not l.get(k):
            errs.append(f"lesson {i}: missing {k}")
if errs:
    sys.exit("refused:\n  " + "\n  ".join(errs))
old = m["LESSONS"]
old_by_json = {json.dumps({k: v for k, v in l.items() if k != "number"}, sort_keys=True): l["number"] for l in old}
changed = []
for l in new:
    key = json.dumps({k: v for k, v in l.items() if k != "number"}, sort_keys=True)
    if key not in old_by_json:
        changed.append(l["number"])
print(f"{module}: {len(old)} -> {len(new)} lessons; {len(changed)} new/changed: {changed}")
if dry:
    sys.exit(0)
m["LESSONS"] = new
m["UNIT"].update(spec.get("unit", {}))
for k, v in spec.get("final_explanation", {}).items():
    m["FINAL_EXPLANATION"][k] = v
src = mod.read_text()
src = replace_lessons_block(src, new)
src = replace_block(src, "UNIT", m["UNIT"])
src = replace_block(src, "FINAL_EXPLANATION", m["FINAL_EXPLANATION"])
sid, sname = ra.display_id_name(m)
src = replace_block(src, "SUMMARY_TABLE", derive_summary_table(m["UNIT"], new, sid, sname))
mod.write_text(src)
store = ra.REV / "change_records" / f"{module}.json"
hist = json.loads(store.read_text())
nxt = 1 + max([int(re.findall(r"(\d+)$", r["id"])[0]) for r in hist["records"] if re.search(r"-split-\d+$", r["id"])] or [0])
stamp = datetime.datetime.now().isoformat(timespec="seconds")
origin = spec.get("origin", {})
for n in changed:
    l = new[n - 1]
    hist["records"].append({
        "id": f"{module}-split-{nxt:03d}", "kind": "set", "target": "lesson", "lesson": n, "path": "title",
        "old": "", "new": l["title"], "criteria": [3], "category": "timing", "severity": "substantial",
        "teacher_decision": True, "group": spec.get("group", "R2-SPLIT"),
        "why": spec.get("why", "Teacher request: lesson split / lesson count change.")
               + f" Lesson {n} is a model-drafted lesson ({origin.get(str(n), 'new or reworked lesson')}); a teacher should read it through.",
        "where": f"Lesson {n} (new or reworked by the split)", "applied_at": stamp})
    nxt += 1
store.write_text(json.dumps(hist, indent=1, ensure_ascii=False))
print("written; now run revise_build.py, validate_corpus.js (CBE_DATA_DIR=...modules) and sync_display_labels.py")
