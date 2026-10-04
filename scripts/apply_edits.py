#!/usr/bin/env python3
"""
apply_edits.py — apply exact find/replace edits to one data module, safely
==========================================================================
Used for drift repairs done in Claude Code (no API calls). Same rule as
scripts/repair_lesson_drift.py: an edit is applied only if `old` occurs EXACTLY
ONCE in the named string field; anything else is rejected and reported.

  python3 scripts/apply_edits.py MODULE --dump OUT.json     # readable JSON of LESSONS + FINAL_EXPLANATION
  python3 scripts/apply_edits.py MODULE EDITS.json [--dry-run]

EDITS.json: {"edits": [ {"target": "lesson" | "final_explanation",
                         "lesson": 3,                      # lesson number (target=lesson only)
                         "path": "framework[2].teacherMoves",   # or "overview", "sections[1].exemplar", ...
                         "old": "exact text", "new": "replacement",
                         "class": "cross_reference" | "dataset" | "other",
                         "conflict": "short description"} ],
             "classified": [ {"conflict": "...", "class": "science" | "structural" | "false_positive" | ..., "note": "..."} ] }
Applied/rejected edits and the classification are appended to
logs/lesson_repairs/<module>.cc.json (the audit trail). The data module is
rewritten only if at least one edit applied and --dry-run is not set.
"""
import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from repair_lesson_drift import apply_edit, get_parent, replace_lessons_block  # noqa: E402
from rebuild_consistency import replace_block  # noqa: E402


def load(mod: Path) -> dict:
    out = subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(mod)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def apply_fe(fe: dict, e: dict):
    try:
        parent, key = get_parent(fe, e["path"])
        text = parent[key]
    except (KeyError, IndexError, TypeError):
        return False, "path not found"
    if not isinstance(text, str):
        return False, "path is not a string field"
    n = text.count(e["old"])
    if not e["old"] or e["old"] == e["new"] or n != 1:
        return False, f"old text occurs {n} times (need exactly 1)" if e["old"] else "empty edit"
    parent[key] = text.replace(e["old"], e["new"], 1)
    return True, ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("module")
    ap.add_argument("edits", nargs="?")
    ap.add_argument("--dump")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    mod = (ROOT / "generators" / "data" / f"{a.module}_data.js").resolve()
    m = load(mod)
    if a.dump:
        slim = {"META": {k: m["META"].get(k) for k in ("subject", "grade", "substrand_name")},
                "LESSONS": [{k: v for k, v in l.items() if k != "resourceLinks"} for l in m["LESSONS"]],
                "FINAL_EXPLANATION": m["FINAL_EXPLANATION"]}
        Path(a.dump).write_text(json.dumps(slim, indent=1, ensure_ascii=False))
        print(f"dumped {a.module} -> {a.dump}")
        return 0
    spec = json.loads(Path(a.edits).read_text())
    lessons, fe = m["LESSONS"], m["FINAL_EXPLANATION"]
    applied, rejected = [], []
    for e in spec.get("edits", []):
        ok, why = (apply_fe(fe, e) if e.get("target") == "final_explanation" else apply_edit(lessons, e))
        (applied if ok else rejected).append({**e, **({} if ok else {"rejected": why})})
    print(f"{a.module}: {len(applied)} applied, {len(rejected)} rejected")
    for e in rejected:
        print(f"  rejected {e.get('target', 'lesson')} L{e.get('lesson', '-')} {e['path']}: {e['rejected']}")
    if a.dry_run:
        return 0
    log = ROOT / "logs" / "lesson_repairs" / f"{a.module}.cc.json"
    log.parent.mkdir(parents=True, exist_ok=True)
    hist = json.loads(log.read_text()) if log.exists() else []
    hist.append({"when": datetime.datetime.now().isoformat(timespec="seconds"), "by": "claude-code",
                 "applied": applied, "rejected": rejected, "classified": spec.get("classified", [])})
    log.write_text(json.dumps(hist, indent=2, ensure_ascii=False))
    if applied:
        src = replace_lessons_block(mod.read_text(), lessons)
        src = replace_block(src, "FINAL_EXPLANATION", fe)
        mod.write_text(src)
        print(f"  wrote {mod.name}")
    return 0 if not rejected else 2


if __name__ == "__main__":
    sys.exit(main())
