#!/usr/bin/env python3
"""
backfill_main_rubric.py: give the UNREVISED Grade 10 modules in generators/data/ the fourth rubric level (contract R1).
(Mark 2026-11-09: 'update to 4 levels as needed'.) These modules will be replaced by the revised ones at promotion;
this only keeps `main` valid against the contract meanwhile. Nothing else in the files is touched.

For each rubric row i of generators/data/<m>_data.js:
  - if the revised module (data/revised_2026-10_full/modules) has a row i with the SAME criterion text (case-insensitive):
    reuse its `belowExpectations`, minus a leading 'Below Expectations:' label when this module's other levels carry no
    level labels (the unrevised text has none), first letter capitalised;
  - otherwise the row is listed in --report and must be supplied via --extra EXTRA.json
    ({"<module>": {"<row index>": "<descriptor>"}}).
  venv/bin/python scripts/round2/backfill_main_rubric.py [--report OUT.json] [--extra EXTRA.json] [--dry-run]
"""
import json, os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("CBE_REVISED_DIR", str(ROOT / "data" / "revised_2026-10_full"))
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "src"))
import revise_apply as ra                          # noqa: E402
from rebuild_consistency import replace_block      # noqa: E402

arg = lambda k: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
extra = json.loads(Path(arg("--extra")).read_text()) if arg("--extra") else {}
dry = "--dry-run" in sys.argv
LABEL = re.compile(r"^\s*Below Expectations\s*:\s*", re.I)
missing, done, copied, supplied = {}, 0, 0, 0
for f in sorted((ROOT / "generators" / "data").glob("*_data.js")):
    mod = f.name[:-len("_data.js")]
    if mod.startswith("g11_"):
        continue
    m = ra.load_module(f)
    rub = (m.get("FINAL_EXPLANATION") or {}).get("rubric") or []
    if not rub or all("belowExpectations" in r for r in rub):
        continue
    rv = ra.load_module(ra.REV / "modules" / f.name).get("FINAL_EXPLANATION", {}).get("rubric") or []
    labelled = any(re.match(r"\s*(Exceeds|Meets|Approaches) Expectations", r.get("excellent", ""), re.I) for r in rub)
    new = []
    for i, r in enumerate(rub):
        r = dict(r)
        t = (extra.get(mod) or {}).get(str(i))
        if t:
            supplied += 1
        elif i < len(rv) and rv[i]["criterion"].strip().lower() == r["criterion"].strip().lower() and rv[i].get("belowExpectations"):
            t = rv[i]["belowExpectations"]
            if not labelled:
                t = LABEL.sub("", t)
                t = t[:1].upper() + t[1:]
            copied += 1
        else:
            missing.setdefault(mod, []).append({"row": i, "criterion": r["criterion"], "excellent": r["excellent"],
                                                "proficient": r["proficient"], "developing": r["developing"]})
            continue
        r["belowExpectations"] = t
        new.append(r)
    if len(new) == len(rub) and not dry:
        m["FINAL_EXPLANATION"]["rubric"] = new
        f.write_text(replace_block(f.read_text(), "FINAL_EXPLANATION", m["FINAL_EXPLANATION"]))
        done += 1
print(f"modules written: {done}; rows copied from revised: {copied}; rows supplied: {supplied}; modules still incomplete: {len(missing)}")
if arg("--report"):
    Path(arg("--report")).write_text(json.dumps(missing, indent=1, ensure_ascii=False))
