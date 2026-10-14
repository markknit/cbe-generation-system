#!/usr/bin/env python3
"""
revise_build.py — render the REVISED documents for sub-strand(s) and produce the tracked-change versions
=======================================================================================================
  python3 scripts/revise_build.py MODULE [MODULE...]   (or --all)

For each module, in the revised master folder (default data/revised_2026-10/):
  baseline_outputs/v2/...   the module as it was (rendered once, same renderer => no spurious differences)
  outputs/v2/...            the REVISED documents + JSON (what you get if every change is accepted)
  tracked/v2/...            *_TRACKED.docx: the revised documents with every change as a Word tracked change
It then verifies (a) Accept All == revised and Reject All == original, (b) the contract / link / consistency
validators on the revised JSON. Nothing under data/outputs/ is touched.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REV = Path(os.environ.get("CBE_REVISED_DIR", ROOT / "data" / "revised_2026-10"))
PY = sys.executable
DOCS = ("CBE_LessonSequence", "FinalExplanation", "FinalExplanation_TeacherKey", "SummaryTable")


def render(modules_dir: Path, out_root: Path, module: str) -> list:
    env = {**os.environ, "CBE_DATA_DIR": str(modules_dir), "CBE_OUTPUT_ROOT": str(out_root),
           "CONSISTENCY_CHECK": "warn", "LINK_CHECK": "warn"}
    r = subprocess.run(["node", str(ROOT / "generators/generate.js"), module], capture_output=True, text=True, env=env)
    if r.returncode != 0 and "Done!" not in r.stdout:
        raise RuntimeError(f"render failed for {module}:\n{r.stdout[-800:]}\n{r.stderr[-800:]}")
    return re.findall(r"Saved: (\S+)", r.stdout)


def build(module: str) -> dict:
    mods, base = REV / "modules", REV / "baseline"
    for d in (mods, base):
        if not (d / f"{module}_data.js").exists():
            raise SystemExit(f"{d}/{module}_data.js missing (run revise_apply.py init)")
    # baseline once; revised every time
    base_files = render(base, REV / "baseline_outputs", module)
    new_files = render(mods, REV / "outputs", module)
    rep = {"module": module, "tracked": [], "problems": []}
    for nf in new_files:
        nf = Path(nf)
        if nf.suffix != ".docx":
            continue
        bf = Path(str(nf).replace(str(REV / "outputs"), str(REV / "baseline_outputs")))
        tf = Path(str(nf).replace(str(REV / "outputs"), str(REV / "tracked"))[:-5] + "_TRACKED.docx")
        tf.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run([PY, str(ROOT / "scripts/make_tracked_docx.py"), str(bf), str(nf), str(tf), "--verify"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            rep["problems"].append(f"tracked-change verification failed for {nf.name}: {r.stdout.strip()[-300:]}")
        rep["tracked"].append(tf.name)
    # validators on the revised JSON
    js = [f for f in new_files if f.endswith("_data.json")]
    for j in js:
        for script, name in (("check_resource_links.py", "links"), ("validate_consistency.py", "consistency")):
            r = subprocess.run([PY, str(ROOT / "scripts" / script), "--quiet", j], capture_output=True, text=True)
            fails = [l for l in r.stdout.splitlines() if l.strip().startswith("FAIL") and "FE-UNVERIFIED" not in l]
            if r.returncode != 0 and (name == "links" or fails):
                rep["problems"].append(f"{name}: " + "; ".join(fails[:3] or [r.stdout.strip()[-200:]]))
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modules", nargs="*")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    mods = a.modules or ([Path(f).name[:-len("_data.js")] for f in sorted(glob.glob(str(REV / "modules/*_data.js")))] if a.all else [])
    if not mods:
        sys.exit(__doc__)
    bad = 0
    for m in mods:
        rep = build(m)
        print(f"{m}: {len(rep['tracked'])} tracked documents" + ("" if not rep["problems"] else "  PROBLEMS"))
        for p in rep["problems"]:
            print("   ", p)
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
