#!/usr/bin/env python3
"""Write data/revised_2026-10/audit/<module>.md: the known audit items for each sub-strand
(teacher-review list items + Final Explanation reviewer findings + template problems + table audit)."""
import json, os, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
REV = Path(os.environ.get("CBE_REVISED_DIR", ROOT / "data" / "revised_2026-10"))
out = REV / "audit"; out.mkdir(parents=True, exist_ok=True)
items = {}
mod = None
for ln in (ROOT / "TEACHER_REVIEW_LIST_2026-10-04.md").read_text().splitlines():
    m = re.match(r"^## ([a-z0-9_]+)(?: —|\s*\()", ln)
    if m and not ln.startswith("## Template"):
        mod = m.group(1); items.setdefault(mod, {"lesson": [], "fe": [], "other": []}); continue
    if ln.startswith("- **[") and mod:
        items[mod]["lesson"].append(ln[2:])
for f in sorted((ROOT / "logs/final_explanation_issues").glob("*.json")):
    d = json.loads(f.read_text())
    if d.get("status") == "needs_review":
        items.setdefault(d["name"], {"lesson": [], "fe": [], "other": []})
        for u in d.get("unresolved", []):
            if (u.get("kind") or "final_explanation") == "final_explanation":
                items[d["name"]]["fe"].append(f"**{u.get('where','')}**: {u.get('problem','')}")
TEMPLATE = {"bio_2_1": "Teacher template filed here is actually the 2.2 Transport System in Plants plan (wilting spinach); the sub-strand has no correct template. Keep the existing phenomenon.",
            "math_3_3": "Teacher template filed here is the Physics Temperature and Thermal Expansion plan; no correct template. Keep the existing phenomenon.",
            "chem_2_1": "Template has activities but no real phenomenon.", "math_2_2": "Template has activities but no real phenomenon."}
for m, t in TEMPLATE.items():
    items.setdefault(m, {"lesson": [], "fe": [], "other": []})["other"].append("Template problem: " + t)
TABLES = {"essmath_1_2": "Lesson 2 learnerExperience holds a markdown table (now rendered full-width; make sure the text around it still reads correctly)",
          "essmath_2_2": None, "math_3_1": "Lesson 7 learnerExperience holds a markdown table (rendered full-width)"}
for m in list(items) + ["essmath_1_2", "math_3_1"]:
    pass
for f in sorted((ROOT / "generators/data").glob("*_data.js")):
    name = f.name[:-8]
    if name.startswith("g11_"):
        continue
    it = items.get(name, {"lesson": [], "fe": [], "other": []})
    body = [f"# Known audit items: {name}", ""]
    for key, head in (("lesson", "Lesson-sequence items (teacher review list)"), ("fe", "Final Explanation reviewer findings (unverified; some are false alarms)"), ("other", "Other")):
        body.append(f"## {head}")
        body += [f"- {x}" for x in it[key]] or ["- none"]
        body.append("")
    (out / f"{name}.md").write_text("\n".join(body))
print(len(list(out.glob('*.md'))), "audit files in", out)
