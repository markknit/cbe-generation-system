#!/usr/bin/env python3
"""apply_proposals.py — build the PROPOSED ANSWERS into the lessons (Mark, 2026-11-10: "build in the answers; teachers keep or edit in place").
For each orange flag with ready-made exact edits: apply them as records `<m>-r2-les-prop-NNN` (group R2-LES-PROPOSED, teacher_decision=true so the journal shows
[DECISION] with before/after), and remove the flag. Flags with no exact edits stay orange. Duplicate flags (answer says duplicate) are removed.
Whole sets apply or not at all (dry-run first). CBE_REVISED_DIR=<abs> venv/bin/python scripts/round2/apply_proposals.py [--only a,b]"""
import json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_converge as fc, lesson_converge as lc
REV = fc.REV
only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
def run(m, recs, dry):
    t = REV / "lesson_proposals" / f"_{m}_apply.json"
    t.write_text(json.dumps({"records": recs}, ensure_ascii=False, indent=1))
    r = subprocess.run([sys.executable, str(fc.ROOT / "scripts/revise_apply.py"), "apply", m, str(t)] + (["--dry-run"] if dry else []), capture_output=True, text=True, env={**os.environ, "CBE_REVISED_DIR": str(REV)})
    t.unlink()
    return r.stdout + r.stderr
for pf in sorted((REV / "lesson_proposals").glob("*.json")):
    m = pf.stem
    if pf.name.startswith("_") or (only and m not in only): continue
    props = json.loads(pf.read_text())
    cf = REV / "change_records" / f"{m}.json"
    d = json.loads(cf.read_text()); recs = d if isinstance(d, list) else d["records"]
    byid = {x["id"]: x for x in recs}
    n0 = max([int(x["id"].rsplit("-", 1)[1]) for x in recs if x["id"].startswith(f"{m}-r2-les-prop-")] + [0])
    sets, drop = [], set()
    for p in props:
        fl = byid.get(p["id"])
        if not fl or fl["kind"] != "flag": continue
        if not p["edits_exact_ok"]:
            if "duplicate" in p["answer"].lower()[:60]: drop.add(p["id"])
            continue
        why = fl["why"].replace(" PROPOSED ANSWER (for the teacher to approve or edit; not applied):", " PROPOSED ANSWER, now built into the lesson (keep it, or edit it in place):").split(" Ready-made edit(s):")[0]
        sets.append((p["id"], fl, why, p["edits_exact_ok"]))
    # all sets, dry-run; sets with a rejection are dropped from the batch
    while True:
        out, k = [], n0
        for fid, fl, why, edits in sets:
            for j, e in enumerate(edits):
                k += 1
                out.append({"id": f"{m}-r2-les-prop-{k:03d}", "kind": "edit", "target": "lesson", "lesson": e["lesson"], "path": e["path"], "old": e["old"], "new": e["new"],
                            "criteria": fl["criteria"], "category": fl["category"], "severity": "minor", "teacher_decision": True, "group": "R2-LES-PROPOSED", "why": why,
                            **({"reference": fl.get("reference", "standard textbook fact")} if fl["category"] == "science" else {}), "_fid": fid})
        if not out: break
        if out: out[0]["group_headline"] = "Teacher choice settled with a proposed answer built into the lesson (keep or edit)"
        dry = run(m, [{k2: v for k2, v in o.items() if k2 != "_fid"} for o in out], True)
        bad = {o["_fid"] for o in out if f"rejected {o['id']}" in dry}
        if not bad: break
        print(m, "dropping sets with rejected edits:", bad)
        sets = [s for s in sets if s[0] not in bad]
    if out:
        msg = run(m, [{k2: v for k2, v in o.items() if k2 != "_fid"} for o in out], False)
        print(m, msg.strip().splitlines()[-1])
        drop |= {s[0] for s in sets}
    if drop:
        d = json.loads(cf.read_text()); recs = d if isinstance(d, list) else d["records"]
        recs = [x for x in recs if x["id"] not in drop]
        cf.write_text(json.dumps(recs if isinstance(d, list) else {**d, "records": recs}, ensure_ascii=False, indent=1))
