#!/usr/bin/env python3
"""
relabel_ids.py — Round 2 relabelling decided by Mark on 2026-11-09 (revised workspace only; generators/data untouched)

  1. MATHS: the journal labelled "Core Mathematics" was the main Mathematics journal. The 14 edited
     `coremath_*` modules become the Mathematics build (`math_*`); the previous `math_*` modules and all their
     renders go to backup_alternates/math_original/. The id `coremath_*` is then free for the real Core
     Mathematics, which starts later (no teacher journal exists for it).
  2. BIO:   `bio_1_1` (teacher-template sequence, KICD 1.3 'Cell Structure and Specialisation') becomes `bio_1_3`;
     the generated `bio_1_3` ('Cell Biology') goes to backup_alternates/bio_1_3_generated/. `bio_1_1` (KICD 1.1
     Introduction to Biology) is then unused.

  python3 scripts/round2/relabel_ids.py [--dry-run]     (CBE_REVISED_DIR must be set)

The mapping old id -> new id is written to round2/id_map.json. Teacher input (round2/slices, round2/decoded) keeps
its ORIGINAL ids on purpose: that is what the teachers saw.
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

REV = Path(os.environ["CBE_REVISED_DIR"])
DRY = "--dry-run" in sys.argv
BK = REV / "backup_alternates"
ROOTS = ["outputs", "tracked", "baseline_outputs", "outputs/_link_matching", "baseline_outputs/_link_matching"]


def say(*a):
    print(("[dry] " if DRY else "") + " ".join(str(x) for x in a))


def out_dir_of(module_file: Path) -> str:
    m = re.search(r'"outputDir":\s*"([^"]+)"', module_file.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def move(src: Path, dst: Path):
    if not src.exists():
        return
    say("move", src.relative_to(REV), "->", dst.relative_to(REV))
    if DRY:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise SystemExit(f"refusing to overwrite {dst}")
    shutil.move(str(src), str(dst))


def backup_module(mid: str, tag: str, od: str = None):
    """move one module's files and renders into backup_alternates/<tag>/ (same relative layout)"""
    od = od or out_dir_of(REV / "modules" / f"{mid}_data.js")
    for rel in (f"modules/{mid}_data.js", f"baseline/{mid}_data.js", f"change_records/{mid}.json", f"audit/{mid}.md"):
        move(REV / rel, BK / tag / rel)
    for root in ROOTS:
        if od:
            move(REV / root / od, BK / tag / root / od)


def rename_module(old: str, new: str, subs):
    """rename module files and apply text substitutions (list of (regex, repl)) inside them"""
    for rel in (f"modules/{old}_data.js", f"baseline/{old}_data.js", f"change_records/{old}.json", f"audit/{old}.md"):
        src = REV / rel
        if not src.exists():
            continue
        dst = REV / rel.replace(old, new)
        text = src.read_text(encoding="utf-8")
        for pat, rep in subs:
            text = re.sub(pat, rep, text)
        say("rename", rel, "->", dst.relative_to(REV))
        if not DRY:
            dst.write_text(text, encoding="utf-8")
            src.unlink()


def main():
    idmap = {}
    # ---- MATHS ----
    old_math = sorted(p.name[:-len("_data.js")] for p in (REV / "modules").glob("math_*_data.js"))
    core = sorted(p.name[:-len("_data.js")] for p in (REV / "modules").glob("coremath_*_data.js"))
    say(f"maths: {len(old_math)} old math_ modules, {len(core)} coremath_ modules")
    stale_od = {c: out_dir_of(REV / "modules" / f"{c}_data.js") for c in core}
    for m in old_math:
        backup_module(m, "math_original")
    for j in ("Journal_Mathematics.docx", "Flagged_Items_Mathematics.docx",
              "Journal_Core_Mathematics.docx", "Flagged_Items_Core_Mathematics.docx"):
        move(REV / "journal" / j, BK / "math_original" / "journal" / j)
    # the previous renders of the coremath_ modules (old Core_Mathematics folders) are stale after the relabel
    for c in core:
        for root in ROOTS:
            move(REV / root / stale_od[c], BK / "stale_renders" / root / stale_od[c])
    label_subs = [(r"CORE MATHEMATICS", "MATHEMATICS"), (r"Core Mathematics", "Mathematics"),
                  (r"Core_Mathematics", "Maths"), (r"Core_mathematics", "Maths"), (r"coremath_", "math_")]
    for c in core:
        new = c.replace("coremath_", "math_", 1)
        idmap[c] = new
        subs = list(label_subs)
        # outputDir/filePrefix: v2/Maths/SSx_Name, Mathematics_Name (the folder/prefix style the old main Maths used)
        subs.insert(0, (r'"filePrefix": "Core_Mathematics_', '"filePrefix": "Mathematics_'))
        rename_module(c, new, subs)
    # ---- BIO ----
    od13 = out_dir_of(REV / "modules" / "bio_1_3_data.js")
    backup_module("bio_1_3", "bio_1_3_generated", od13)
    move(REV / "round2/slices/bio_1_3.json", BK / "bio_1_3_generated/round2/slices/bio_1_3.json")
    od11 = out_dir_of(REV / "modules" / "bio_1_1_data.js")
    for root in ROOTS:           # the old SS1.1 renders are stale after the relabel
        move(REV / root / od11, BK / "stale_renders" / root / od11)
    bio_subs = [(r'"substrand_id": "1\.1"', '"substrand_id": "1.3"'),
                (r'"substrand_name": "Cell Structure"', '"substrand_name": "Cell Structure and Specialisation"'),
                (r'v2/Biology/SS1\.1_Cell_Structure"', 'v2/Biology/SS1.3_Cell_Structure_and_Specialisation"'),
                (r'"filePrefix": "Biology_Cell_Structure"', '"filePrefix": "Biology_Cell_Structure_and_Specialisation"'),
                (r"bio_1_1", "bio_1_3")]
    rename_module("bio_1_1", "bio_1_3", bio_subs)
    idmap["bio_1_1"] = "bio_1_3"
    if not DRY:
        (REV / "round2/id_map.json").write_text(json.dumps({
            "note": "old id (as the teachers saw it in the journals) -> id in this workspace after the 2026-11-09 relabel (Mark)",
            "map": idmap, "backups": {"math_original": "previous math_* modules", "bio_1_3_generated": "previous bio_1_3 (Cell Biology)"}},
            indent=1))
    say("done", len(idmap), "ids mapped")


main()
