#!/usr/bin/env python3
"""
sync_display_labels.py: make the teacher-visible sub-strand labels follow the KICD number/name (Mark, 2026-11-09, option b).

Display labels ONLY: META.titleDoc, META.subtitleDoc ('Sub-Strand X.Y (N Lessons)') and SUMMARY_TABLE.subStrand.
NEVER touched: META.substrand_id, substrand_name, outputDir, filePrefix, the module id, folders, file names
(partner contract keys, Drive links and the teacher index depend on them).
The KICD number/name come from UNIT.substrand (already set by Round 2); rules in revise_apply.display_id_name().
Re-run after any change that alters the lesson count (the subtitle carries it).

  export CBE_REVISED_DIR=$PWD/data/revised_2026-10_full
  venv/bin/python scripts/round2/sync_display_labels.py [--dry-run] [MODULE ...]
Writes data/revised_2026-10_full/round2/display_labels.json (what changed, per module).
"""
import json, os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("CBE_REVISED_DIR", str(ROOT / "data" / "revised_2026-10_full"))
import revise_apply as ra                       # noqa: E402
from rebuild_consistency import replace_block   # noqa: E402
from generate_substrand import derive_summary_table  # noqa: E402

# 2026-11-09 (Mark): the journal labelled "Core Mathematics" was the main Mathematics one; those modules are now math_*
JOURNALED = ("bio_", "chem_", "phys_", "math_")
# (bio_1_1/bio_1_3 collision resolved 2026-11-09 by relabel_ids.py: bio_1_3 is now the teacher-template KICD 1.3 module)
SUBTITLE_OVERRIDE = {}
dry = "--dry-run" in sys.argv
only = [a for a in sys.argv[1:] if not a.startswith("--")]
report = {}
for f in sorted((ra.REV / "modules").glob("*_data.js")):
    mod = f.name[:-len("_data.js")]
    if only and mod not in only:
        continue
    if not only and not mod.startswith(JOURNALED):   # no teacher journal received for math_/gensci_/essmath_: leave as is
        continue
    m = ra.load_module(f)
    mt = dict(m["META"])
    sid, sname = ra.display_id_name(m)
    new = dict(mt)
    if sname.lower() != mt["substrand_name"].lower():
        head = mt["titleDoc"].split(":", 1)[0]
        new["titleDoc"] = f"{head}: {sname.upper()}"
    sub = mt["subtitleDoc"]
    sub = re.sub(r"Sub-Strand\s+[\d.]+", f"Sub-Strand {sid}", sub, count=1)
    sub = re.sub(r"\(\d+ Lessons?\)", f"({len(m['LESSONS'])} Lessons)", sub, count=1)
    if mod in SUBTITLE_OVERRIDE:
        sub = SUBTITLE_OVERRIDE[mod].format(n=len(m["LESSONS"]))
    new["subtitleDoc"] = sub
    st = derive_summary_table(m["UNIT"], m["LESSONS"], sid, sname)
    changes = {k: [mt[k], new[k]] for k in ("titleDoc", "subtitleDoc") if mt[k] != new[k]}
    if (m.get("SUMMARY_TABLE") or {}).get("subStrand") != st["subStrand"]:
        changes["SUMMARY_TABLE.subStrand"] = [(m.get("SUMMARY_TABLE") or {}).get("subStrand"), st["subStrand"]]
    if not changes:
        continue
    report[mod] = changes
    if not dry:
        src = f.read_text()
        src = replace_block(src, "META", new)
        src = replace_block(src, "SUMMARY_TABLE", st)
        f.write_text(src)
out = ra.REV / "round2" / "display_labels.json"
if not dry:
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False))
print(f"{len(report)} modules {'would change' if dry else 'changed'}")
for k, v in report.items():
    print(k, {a: b[1] for a, b in v.items()})
