#!/usr/bin/env python3
"""
triage_phenomenon.py — does each sub-strand's anchoring phenomenon match the teachers'?
=======================================================================================
Teacher templates (data/raw/CBE LESSON TEMPLATES/v2_owner_inventory) state a
phenomenon. Until 2026-10-04 the generator read the wrong template cell, so most
sub-strands were built on a model-invented phenomenon. Word overlap cannot tell a
paraphrase ("heart beats faster when you run" / "Kipchoge's heart rate after a
race") from a different scenario, so one small model call per sub-strand decides:

  same       the generated phenomenon is the same idea as the teachers'
  different  a different scenario/question
  unclear    the template text is not a phenomenon (e.g. a resource list) or is
             missing: needs a human look at the template

Writes logs/phenomenon_triage.json and prints the 'different' list.
  python3 scripts/triage_phenomenon.py [--grade 10] [--exclude a,b,c]
~$0.01 per sub-strand.
"""
import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import generate_substrand as g  # noqa: E402

SCHEMA = {"type": "object", "additionalProperties": False,
          "properties": {"verdict": {"type": "string", "enum": ["same", "different", "unclear"]},
                         "why": {"type": "string"}},
          "required": ["verdict", "why"]}


def load(path):
    out = subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(require(process.argv[1])))", str(path)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grade", type=int, default=10)
    ap.add_argument("--exclude", default="")
    a = ap.parse_args()
    skip = set(filter(None, a.exclude.split(",")))
    rows = {}
    for f in sorted(glob.glob(str(ROOT / "generators/data/*_data.js"))):
        name = Path(f).name.removesuffix("_data.js")
        if name in skip:
            continue
        m = load(f)
        meta = m["META"]
        if int(meta["grade"]) != a.grade:
            continue
        t = g.find_v2_templates(a.grade, meta["subject"].lower().replace(" ", "_"), meta["substrand_id"])
        if not t.get("lesson"):
            continue
        tp = g.extract_template_docx(str(t["lesson"]))
        ph = tp.get("phenomenon", "")
        if len(ph) < 30:
            rows[name] = {"verdict": "unclear", "why": "no phenomenon could be read from the template", "template": t["lesson"].name}
            continue
        prompt = f"""A Kenyan Grade {a.grade} {meta['subject']} sub-strand ({meta['substrand_name']}) was supposed to be built around a phenomenon chosen by the teachers. Compare.

TEACHERS' TEMPLATE (raw text from their planning document; it may include resource links and a driving question):
{ph[:1800]}
{('Teachers' + chr(39) + ' driving question: ' + tp['teacher_driving_question'][:400]) if tp.get('teacher_driving_question') else ''}

PHENOMENON IN THE GENERATED LESSONS:
{m['UNIT'].get('phenomenon', '')[:1800]}

Verdict:
- "same": the generated phenomenon is the same idea or question as the teachers' (different wording or added Kenyan detail is fine).
- "different": a different scenario or question.
- "unclear": the teachers' text is not really a phenomenon (a resource list, an activity list, or belongs to another topic).
One-line "why"."""
        r = g.call_claude(prompt, schema=SCHEMA)
        rows[name] = {**(r or {"verdict": "unclear", "why": "judge failed"}), "template": t["lesson"].name,
                      "subject": meta["subject"], "lessons": len(m["LESSONS"]),
                      "substrand": meta["substrand_id"]}
    (ROOT / "logs" / "phenomenon_triage.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    for v in ("different", "unclear", "same"):
        names = [k for k, r in rows.items() if r["verdict"] == v]
        print(f"{v}: {len(names)}  {' '.join(names)}")
    print(f"Estimated spend: ${g._estimate_cost():.2f}")


if __name__ == "__main__":
    main()
