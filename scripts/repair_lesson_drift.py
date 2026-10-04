#!/usr/bin/env python3
"""
repair_lesson_drift.py — make a sub-strand's lessons agree with each other, by minimal edits
============================================================================================
Input: the drift report from scripts/review_lesson_consistency.py
(logs/lesson_drift/<module>.json). For each MAJOR contradiction a model chooses
the authoritative version (Lesson 1 and the last lesson win; otherwise the
earliest lesson that establishes the fact) and proposes EXACT find-and-replace
edits to the lessons that disagree. Edits are applied mechanically:

  * `path` must name a string field of that lesson (e.g. "overview",
    "summaryTablePrompt.explained", "framework[2].teacherMoves");
  * `old` must occur in that field EXACTLY ONCE, or the edit is rejected;
  * nothing else in any lesson changes, so the diff is exactly the edit list.

Every applied/rejected edit is logged to logs/lesson_repairs/<module>.json (the
audit trail), and the module's data.js LESSONS block is rewritten. Afterwards,
in this order:
  python3 scripts/rebuild_consistency.py --summary-tables --only <module>
  python3 scripts/review_lesson_consistency.py --only <module>     # did it work?
  python3 scripts/rebuild_consistency.py --final-explanations --only <module>
  node generators/generate.js <module>

  python3 scripts/repair_lesson_drift.py MODULE [--minor] [--dry-run]
--minor also fixes the reviewer's minor findings (default: major only).
~$0.15 per sub-strand.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "edits": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"lesson": {"type": "integer"}, "path": {"type": "string"},
                           "old": {"type": "string"}, "new": {"type": "string"},
                           "conflict": {"type": "string"}},
            "required": ["lesson", "path", "old", "new", "conflict"]}},
        "unresolved": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"conflict": {"type": "string"}, "why": {"type": "string"}},
            "required": ["conflict", "why"]}},
    },
    "required": ["edits", "unresolved"],
}


def load_module(path: Path) -> dict:
    out = subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(path)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def split_path(path: str):
    return [int(p) if p.isdigit() else p for p in re.findall(r"[^.\[\]]+", path)]


def get_parent(lesson: dict, path: str):
    keys = split_path(path)
    cur = lesson
    for k in keys[:-1]:
        cur = cur[k]
    return cur, keys[-1]


def apply_edit(lessons: list, e: dict):
    """Return (ok, reason)."""
    target = next((l for l in lessons if l.get("number") == e["lesson"]), None)
    if target is None:
        return False, "no such lesson"
    try:
        parent, key = get_parent(target, e["path"])
        text = parent[key]
    except (KeyError, IndexError, TypeError):
        return False, "path not found"
    if not isinstance(text, str):
        return False, "path is not a string field"
    if not e["old"] or e["old"] == e["new"]:
        return False, "empty or no-op edit"
    n = text.count(e["old"])
    if n != 1:
        return False, f"old text occurs {n} times (need exactly 1)"
    parent[key] = text.replace(e["old"], e["new"], 1)
    return True, ""


def lessons_for_prompt(lessons: list) -> str:
    slim = [{k: v for k, v in l.items() if k != "resourceLinks"} for l in lessons]
    return json.dumps(slim, ensure_ascii=False, indent=1)


def replace_lessons_block(src: str, lessons: list) -> str:
    pat = re.compile(r"const LESSONS = \[.*?\n\];\n", re.S)
    if not pat.search(src):
        raise ValueError("const LESSONS block not found")
    body = json.dumps(lessons, indent=2, ensure_ascii=False)
    return pat.sub(lambda _m: f"const LESSONS = {body};\n", src, count=1)


PROMPT = """You are repairing contradictions BETWEEN LESSONS of one Kenyan CBE Grade {grade} {subject} sub-strand ({substrand}). The lessons were written separately. A reviewer found these contradictions:

{listing}

VALID "framework" INDICES per lesson (an index outside these does not exist): {valid_idx}

THE LESSONS (JSON; "number" identifies each):
{lessons}

For each contradiction choose the AUTHORITATIVE version: Lesson 1 (it launches the phenomenon and sets the data) and Lesson {last} (the final lesson) win; if neither speaks to it, the earliest lesson that establishes the fact wins. Then change the OTHER lessons, as little as possible, so every lesson tells the authoritative version. Examples of what to fix: a number, a name, an outcome, a dataset value, a wrong "in Lesson N we did X" cross-reference (make it point to the lesson that really did X).

Return EXACT find-and-replace edits:
- "lesson": the lesson number; "path": the string field, like "overview", "summaryTablePrompt.observed", "summaryTablePrompt.explained", "framework[0].learnerExperience", "framework[3].teacherMoves" (the index is the position in that lesson's "framework" list; "slo.knowledge", "teacherReflection" etc. also work);
- "old": a short EXACT substring of that field (copy it character for character; it must occur exactly once in that field; keep it as short as is still unique);
- "new": the replacement;
- "conflict": the number of the contradiction it fixes.
Rules: do NOT rewrite whole paragraphs; do NOT touch anything unrelated; do NOT invent new teaching content, only align facts. If a contradiction cannot be fixed by small edits (for example a whole lesson is built on a different dataset), put it in "unresolved" with the reason instead of making large edits. Keep numbers/units realistic (e.g. a marathon pace must be realistic)."""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("module")
    ap.add_argument("--minor", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    import generate_substrand as g

    mod = ROOT / "generators" / "data" / f"{a.module}_data.js"
    report = json.loads((ROOT / "logs" / "lesson_drift" / f"{a.module}.json").read_text())
    conflicts = [c for c in report["conflicts"] if a.minor or c["severity"] == "major"]
    if not conflicts:
        print(f"{a.module}: no {'conflicts' if a.minor else 'major conflicts'} to repair")
        return 0
    m = load_module(mod)
    lessons = m["LESSONS"]
    last = lessons[-1]["number"]

    valid_idx = "; ".join(f"lesson {l['number']}: 0-{len(l.get('framework', [])) - 1}" for l in lessons)
    CHUNK = 3     # a call with many conflicts overruns the output limit (seen: 7 conflicts, 16k tokens)
    applied, rejected, unresolved = [], [], []
    def run(chunk, label):
        listing = "\n".join(f"{i + 1}. [{c['severity']}] lessons {c['lessons']}: {c['fact']}\n   {c['versions']}"
                            for i, c in enumerate(chunk))
        prompt = PROMPT.format(grade=m['META']['grade'], subject=m['META']['subject'],
                               substrand=m['META']['substrand_name'], listing=listing, valid_idx=valid_idx,
                               lessons=lessons_for_prompt(lessons), last=last)
        print(f"{a.module}: conflicts {label} of {len(conflicts)}; asking the model...")
        r = g.call_claude(prompt, max_tokens=16000, schema=SCHEMA)
        if not r:
            if len(chunk) > 1:          # output overran: do them one at a time
                for k, c in enumerate(chunk):
                    run([c], f"{label.split('-')[0] if '-' in label else label}.{k + 1}")
                return
            print("  FAILED: no response")
            unresolved.append({"conflict": chunk[0]["fact"], "why": "repair call failed (output limit)"})
            return
        for e in r["edits"]:
            ok, why = apply_edit(lessons, e)
            (applied if ok else rejected).append({**e, **({} if ok else {"rejected": why})})
        unresolved.extend(r["unresolved"])

    for start in range(0, len(conflicts), CHUNK):
        chunk = conflicts[start:start + CHUNK]
        run(chunk, f"{start + 1}-{start + len(chunk)}")
    print(f"  edits: {len(applied)} applied, {len(rejected)} rejected, {len(unresolved)} unresolved")
    for e in rejected:
        print(f"    rejected L{e['lesson']} {e['path']}: {e['rejected']}")
    r = {"unresolved": unresolved}
    log = ROOT / "logs" / "lesson_repairs"
    log.mkdir(parents=True, exist_ok=True)
    (log / f"{a.module}.json").write_text(json.dumps(
        {"module": a.module, "conflicts_in": conflicts, "applied": applied, "rejected": rejected,
         "unresolved": r["unresolved"]}, indent=2, ensure_ascii=False))
    if a.dry_run:
        print("  dry run: data.js not written")
        return 0
    mod.write_text(replace_lessons_block(mod.read_text(), lessons))
    print(f"  wrote {mod.name}; audit trail: logs/lesson_repairs/{a.module}.json")
    print(f"  estimated spend this run: ${g._estimate_cost():.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
