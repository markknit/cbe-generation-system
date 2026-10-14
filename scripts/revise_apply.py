#!/usr/bin/env python3
"""
revise_apply.py — apply a reviewer's change records to the REVISED copy of a data module
=========================================================================================
The revised corpus lives in its own master folder (default data/revised_2026-10/); the source
modules in generators/data/ are never touched.

  python3 scripts/revise_apply.py init                       # copy Grade 10 modules into the workspace (never overwrites)
  python3 scripts/revise_apply.py apply MODULE RECORDS.json [--dry-run]
  python3 scripts/revise_apply.py status                     # records per module
  python3 scripts/revise_apply.py dump MODULE OUT.json       # readable JSON of the CURRENT revised module (UNIT, LESSONS, FINAL_EXPLANATION)

Workspace layout:
  modules/<m>_data.js        the edited data modules (source of the revised documents)
  baseline/<m>_data.js       untouched copy, the "before" for tracked changes
  change_records/<m>.json    every change, with why / criterion / reference (feeds the journal)

RECORDS.json: {"records": [ {
    "id": "gensci_3_1-001",          # unique per module
    "kind": "edit" | "set" | "flag",
    "target": "unit" | "lesson" | "final_explanation",
    "lesson": 3,                      # target=lesson only
    "path": "framework[2].teacherMoves",
    "old": "exact text (kind=edit: must occur exactly once in the field)", "new": "replacement",
    # kind=set: "value": <any JSON>, replaces the whole value at path (old is recorded automatically)
    # kind=flag: no edit; a teacher-review note ("why" says what is wrong and what is suggested)
    "criteria": [1, 4],               # which of the 14 guidelines
    "category": "science|pedagogy|consistency|language|inclusion|safety|local|assessment|timing|link|format",
    "severity": "minor" | "substantial",
    "teacher_decision": true|false,   # a judgement call a teacher should confirm (shown flagged in the journal)
    "why": "...", "reference": "required when category=science",
    "group": "G3",                    # optional: records that stem from ONE root fix share a group key;
    "group_headline": "...",          #   the root record carries a one-line plain-English headline (the journal shows one item per group)
    "location": "optional human-readable override of where the change is" } ] }
The Summary Table is re-derived from the lessons after every apply. Edits that do not apply
(path missing, old text not found exactly once) are rejected and reported, never forced.
"""
import argparse
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REV = Path(os.environ.get("CBE_REVISED_DIR", ROOT / "data" / "revised_2026-10"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
from repair_lesson_drift import get_parent, replace_lessons_block  # noqa: E402
from rebuild_consistency import replace_block  # noqa: E402

REQ = ("id", "kind", "target", "criteria", "category", "severity", "why")


def load_module(path: Path) -> dict:
    out = subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(path)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def init():
    (REV / "modules").mkdir(parents=True, exist_ok=True)
    (REV / "baseline").mkdir(exist_ok=True)
    (REV / "change_records").mkdir(exist_ok=True)
    n = 0
    for f in sorted(glob.glob(str(ROOT / "generators/data/*_data.js"))):
        name = Path(f).name
        if name.startswith("g11_"):
            continue                     # Grade 11 is decided separately
        for d in ("modules", "baseline"):
            dst = REV / d / name
            if not dst.exists():
                shutil.copy(f, dst)
                n += 1
    print(f"workspace {REV}: {len(list((REV / 'modules').glob('*_data.js')))} modules ({n} files copied)")


def resolve(m: dict, r: dict):
    """Return the container dict the record's path is relative to, or None."""
    if r["target"] == "unit":
        return m["UNIT"]
    if r["target"] == "final_explanation":
        return m["FINAL_EXPLANATION"]
    return next((l for l in m["LESSONS"] if l.get("number") == r.get("lesson")), None)


def apply_one(m: dict, r: dict):
    if r["kind"] == "flag":
        return True, ""
    cont = resolve(m, r)
    if cont is None:
        return False, "no such lesson/target"
    try:
        parent, key = get_parent(cont, r["path"])
        cur = parent[key]
    except (KeyError, IndexError, TypeError):
        return False, "path not found"
    if r["kind"] == "set":
        r["old"] = json.dumps(cur, ensure_ascii=False) if not isinstance(cur, str) else cur
        parent[key] = r["value"]
        r["new"] = r["value"] if isinstance(r["value"], str) else json.dumps(r["value"], ensure_ascii=False)
        return True, ""
    if not isinstance(cur, str):
        return False, "path is not a string field (use kind=set)"
    old, new = r.get("old", ""), r.get("new", "")
    n = cur.count(old) if old else 0
    if n != 1 or old == new:
        return False, f"old text occurs {n} times (need exactly 1)" if old else "empty or no-op edit"
    parent[key] = cur.replace(old, new, 1)
    return True, ""


def where(m: dict, r: dict) -> str:
    if r.get("location"):
        return r["location"]
    p = r.get("path", "")
    if r["target"] == "lesson":
        base = f"Lesson {r['lesson']}"
        mm = re.match(r"framework\[(\d+)\]\.(\w+)", p)
        if mm:
            les = next((l for l in m["LESSONS"] if l.get("number") == r["lesson"]), {})
            fw = les.get("framework", [])
            i = int(mm.group(1))
            ph = fw[i]["phase"] if i < len(fw) else f"phase {i + 1}"
            return f"{base}, {ph}, {mm.group(2)}"
        return f"{base}, {p}"
    if r["target"] == "final_explanation":
        mm = re.match(r"sections\[(\d+)\]\.(\w+)", p)
        if mm:
            secs = m["FINAL_EXPLANATION"].get("sections", [])
            i = int(mm.group(1))
            return f"Final Explanation, {secs[i]['title'] if i < len(secs) else 'section ' + str(i + 1)}, {mm.group(2)}"
        return f"Final Explanation, {p}"
    return f"Unit overview, {p}"


def apply(module: str, records_file: str, dry: bool):
    from generate_substrand import derive_summary_table  # needs the venv
    mod = REV / "modules" / f"{module}_data.js"
    if not mod.exists():
        sys.exit(f"{mod} missing: run `revise_apply.py init`")
    m = load_module(mod)
    spec = json.loads(Path(records_file).read_text())
    store = REV / "change_records" / f"{module}.json"
    hist = json.loads(store.read_text()) if store.exists() else {"module": module, "records": []}
    have = {r["id"] for r in hist["records"]}
    applied, rejected = [], []
    for r in spec["records"]:
        miss = [k for k in REQ if k not in r]
        if miss:
            rejected.append((r.get("id"), f"missing fields {miss}")); continue
        if r["id"] in have:
            rejected.append((r["id"], "id already applied")); continue
        if r["category"] == "science" and not r.get("reference"):
            rejected.append((r["id"], "science change without a reference")); continue
        if r["kind"] == "flag":
            r["where"] = where(m, r)
            applied.append(r); continue
        ok, why = apply_one(m, r)
        if ok:
            r["where"] = where(m, r)
            applied.append(r)
        else:
            rejected.append((r["id"], why))
    allr = hist["records"] + applied
    for g in sorted({r["group"] for r in allr if r.get("group")}):
        if not any(r.get("group") == g and r.get("group_headline") for r in allr):
            print(f"  warning: group {g} has no record with group_headline")
    print(f"{module}: {len(applied)} applied, {len(rejected)} rejected")
    for i, why in rejected:
        print(f"  rejected {i}: {why}")
    if dry:
        return 0 if not rejected else 2
    if any(r["kind"] != "flag" for r in applied):
        src = mod.read_text()
        src = replace_lessons_block(src, m["LESSONS"])
        src = replace_block(src, "FINAL_EXPLANATION", m["FINAL_EXPLANATION"])
        src = replace_block(src, "UNIT", m["UNIT"])
        src = replace_block(src, "SUMMARY_TABLE", derive_summary_table(
            m["UNIT"], m["LESSONS"], m["META"]["substrand_id"], m["META"]["substrand_name"]))
        mod.write_text(src)
    stamp = datetime.datetime.now().isoformat(timespec="seconds")
    for r in applied:
        r["applied_at"] = stamp
    hist["records"].extend(applied)
    store.write_text(json.dumps(hist, indent=1, ensure_ascii=False))
    return 0 if not rejected else 2


def status():
    for f in sorted((REV / "change_records").glob("*.json")):
        h = json.loads(f.read_text())
        rs = h["records"]
        print(f"{h['module']}: {len(rs)} records, {sum(r['kind'] == 'flag' for r in rs)} flags, "
              f"{sum(r['severity'] == 'substantial' for r in rs)} substantial")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["init", "apply", "status", "dump"])
    ap.add_argument("module", nargs="?")
    ap.add_argument("records", nargs="?")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.cmd == "init":
        init()
    elif a.cmd == "status":
        status()
    elif a.cmd == "dump":
        m = load_module(REV / "modules" / f"{a.module}_data.js")
        out = {"META": m["META"], "UNIT": m["UNIT"],
               "LESSONS": [{k: v for k, v in l.items() if k != "resourceLinks"} for l in m["LESSONS"]],
               "FINAL_EXPLANATION": m["FINAL_EXPLANATION"]}
        Path(a.records).write_text(json.dumps(out, indent=1, ensure_ascii=False))
        print(f"dumped {a.module} -> {a.records}")
    else:
        sys.exit(apply(a.module, a.records, a.dry_run))
