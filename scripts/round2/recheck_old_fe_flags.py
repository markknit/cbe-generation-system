#!/usr/bin/env python3
"""Re-check the older generation-time FE-UNVERIFIED logs (fe_issues/<m>.json) against the CURRENT lessons and FE.
Per module one call: each old issue -> RESOLVED (no longer true / already fixed) or OPEN (still a real defect, with one-line recommendation).
All RESOLVED -> status 'cleared' (revised copy of the log only). Any OPEN -> stays, recorded in fe_issues_recheck/<m>.json. COSTS API MONEY."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_converge as fc
REV = fc.REV
_s = fc._s
SCHEMA = {"type": "object", "additionalProperties": False, "properties": {"verdicts": {"type": "array", "items": {"type": "object", "additionalProperties": False,
    "properties": {"n": {"type": "integer"}, "state": {"type": "string", "enum": ["RESOLVED", "OPEN"]}, "reason": _s(), "recommendation": _s()},
    "required": ["n", "state", "reason"]}}}, "required": ["verdicts"]}
import generate_substrand as g
mods = sys.argv[1].split(",")
(REV / "fe_issues_recheck").mkdir(exist_ok=True)
for m in mods:
    f = REV / "fe_issues" / f"{m}.json"
    log = json.loads(f.read_text())
    if log.get("status") == "cleared" or not log.get("unresolved"):
        continue
    mod = fc.load(REV / "modules" / f"{m}_data.js")
    prefix = f"THE LESSON PLAN (JSON):\n{json.dumps(fc.strip(mod['LESSONS']), ensure_ascii=False)}\n\nTHE CURRENT FINAL EXPLANATION (student assessment) (JSON):\n{json.dumps(fc.fe_view(mod), ensure_ascii=False)}\n"
    items = "\n".join(f"[{i}] {x.get('where','')}: {x.get('problem','')}" for i, x in enumerate(log["unresolved"]))
    p = ("An OLD reviewer logged these problems against an EARLIER version of the Final Explanation (FE). Check each against the CURRENT FE and lessons above. "
         "RESOLVED = no longer true, or the FE/lessons now agree, or the point is a style preference. OPEN = still a real defect in the current text (wrong arithmetic, FE contradicting the lessons, a science error, a prompt that gives away its own answer, a self-contradiction); give a one-line recommendation. Be strict about 'real': do not keep style points open.\n\n" + items)
    r = g.call_claude(p, schema=SCHEMA, cache_prefix=prefix)
    if r is None:
        print(m, "CALL FAILED"); continue
    v = {x["n"]: x for x in r["verdicts"]}
    opens = [{"issue": log["unresolved"][i], "recommendation": v[i].get("recommendation", ""), "reason": v[i]["reason"]} for i in range(len(log["unresolved"])) if v.get(i, {}).get("state", "OPEN") == "OPEN"]
    (REV / "fe_issues_recheck" / f"{m}.json").write_text(json.dumps({"module": m, "open": opens, "verdicts": r["verdicts"]}, ensure_ascii=False, indent=1))
    if not opens:
        log["status"] = "cleared"; log["cleared_note"] = "re-checked 2026-11-10 against the current lessons and FE: all resolved"
        f.write_text(json.dumps(log, ensure_ascii=False, indent=1))
    print(m, "cleared" if not opens else f"{len(opens)} OPEN of {len(log['unresolved'])}", flush=True)
print(f"estimated spend ${g._estimate_cost():.2f}")
