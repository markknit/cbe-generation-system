#!/usr/bin/env python3
"""
review_lesson_consistency.py — do the lessons of a sub-strand agree with EACH OTHER?
====================================================================================
Lessons are generated in parallel batches with no shared dataset, so within one
sub-strand lesson 2 can say a runner slowed at 15-30 km and lesson 8 at 25-35 km
(Core Mathematics 2.9, found 2026-10-03). Nothing else in the pipeline can see
this. One model call per sub-strand reads ALL its lessons (overview, summary,
every phase's learner experience and teacher moves) and lists contradictions of
fact: numbers, outcomes, characters, places, the phenomenon's data.

  python3 scripts/review_lesson_consistency.py [--only a,b] [--workers 4] [--dry-run]

Writes logs/lesson_drift/<module>.json and logs/lesson_drift/SUMMARY.md (ranked,
worst first). Reports only; changes no lesson. ~$0.05 per sub-strand.
"""
import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import generate_substrand as g  # noqa: E402

OUTDIR = ROOT / "logs" / "lesson_drift"
SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {"conflicts": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "properties": {
            "lessons": {"type": "string"},
            "severity": {"type": "string", "enum": ["major", "minor"]},
            "fact": {"type": "string"},
            "versions": {"type": "string"}},
        "required": ["lessons", "severity", "fact", "versions"]}}},
    "required": ["conflicts"],
}


def load(path: Path) -> dict:
    out = subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(path)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def digest(m: dict) -> str:
    parts = [f"PHENOMENON: {m['UNIT'].get('phenomenon', '')}\n"]
    for l in m["LESSONS"]:
        stp = l.get("summaryTablePrompt") or {}
        parts.append(f"=== LESSON {l['number']}: {l['title']}\nOverview: {l.get('overview', '')}\n"
                     f"Observed: {stp.get('observed', '')}\nLearned: {stp.get('learned', '')}\n"
                     f"Explained: {stp.get('explained', '')}")
        for ph in l.get("framework", []):
            parts.append(f"  [{ph.get('phase', '')}] Learners: {(ph.get('learnerExperience') or '')[:700]} "
                         f"| Teacher: {(ph.get('teacherMoves') or '')[:500]}")
    return "\n".join(parts)


def review(name: str, m: dict):
    prompt = f"""You are checking ONE sub-strand of a Kenyan CBE Grade {m['META']['grade']} {m['META']['subject']} lesson sequence ({m['META']['substrand_name']}). The lessons were written separately. Find places where lessons CONTRADICT EACH OTHER about a fact.

{digest(m)}

Report only real contradictions of fact between two or more lessons: different numbers, times, quantities or units for the same thing; opposite outcomes (who won, which is larger, what happened); different characters, places or datasets for the same phenomenon; an impossible or unrealistic figure the lessons depend on; a term defined differently. Do NOT report style, different examples that don't conflict, or things one lesson says that another simply doesn't mention.
severity "major": a teacher following the sequence would teach students two incompatible things, or a dataset/outcome the sequence builds on changes between lessons. "minor": a small numeric or wording inconsistency that would not mislead.
Return {{"conflicts": []}} if there are none. Otherwise one entry per conflict: "lessons" (e.g. "2, 5, 8"), "fact" (what is contradicted), "versions" (what each lesson says)."""
    r = g.call_claude(prompt, schema=SCHEMA)
    return None if r is None else r["conflicts"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    files = sorted((ROOT / "generators" / "data").glob("*_data.js"))
    if a.only:
        want = set(a.only.split(","))
        files = [f for f in files if f.name.removesuffix("_data.js") in want]
    print(f"{len(files)} sub-strands, est ~${len(files) * 0.055:.2f}")
    if a.dry_run:
        return
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rows = []

    def work(f):
        name = f.name.removesuffix("_data.js")
        m = load(f)
        return name, m, review(name, m)

    with ThreadPoolExecutor(a.workers) as ex:
        for fut in as_completed([ex.submit(work, f) for f in files]):
            name, m, conf = fut.result()
            if conf is None:
                print(f"  FAILED {name}")
                continue
            (OUTDIR / f"{name}.json").write_text(json.dumps(
                {"name": name, "subject": m["META"]["subject"], "substrand": m["META"]["substrand_name"],
                 "lessons": len(m["LESSONS"]), "conflicts": conf}, indent=2, ensure_ascii=False))
            major = sum(1 for c in conf if c["severity"] == "major")
            rows.append((major, len(conf) - major, name, m["META"]["subject"], m["META"]["substrand_name"], len(m["LESSONS"])))
            print(f"  {name}: {major} major, {len(conf) - major} minor")
    rows.sort(key=lambda r: (-r[0], -r[1]))
    n_maj = sum(1 for r in rows if r[0])
    lines = [f"# Lesson-sequence consistency review ({len(rows)} sub-strands)", "",
             f"- with at least one MAJOR contradiction: **{n_maj}** ({100 * n_maj // max(len(rows), 1)}%)",
             f"- with only minor: {sum(1 for r in rows if not r[0] and r[1])}",
             f"- clean: {sum(1 for r in rows if not r[0] and not r[1])}", "",
             "| major | minor | module | subject | sub-strand | lessons |", "|---|---|---|---|---|---|"]
    lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |" for r in rows]
    (OUTDIR / "SUMMARY.md").write_text("\n".join(lines) + "\n")
    print(f"\n{n_maj} of {len(rows)} sub-strands have a major contradiction. See logs/lesson_drift/SUMMARY.md")
    print(f"Estimated spend this run: ${g._estimate_cost():.2f}")


if __name__ == "__main__":
    main()
