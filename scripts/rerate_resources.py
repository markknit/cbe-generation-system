#!/usr/bin/env python3
"""
rerate_resources.py — re-rate the ARES resources of existing deck specs with the 4-level scale
(best_match / preview_first / use_later / do_not_use). One small call per lesson; slides are untouched. Presentations branch.

  python3 scripts/rerate_resources.py --data <data.json> [--lessons 1,3-12] [--dry-run]

Why: the first scale had no way to say "a good resource, but show it after the Explain phase", so 59 of 89 resources
were marked DO NOT USE (Mark's review, 2026-10-22). The previous ratings are kept in logs/rerate/L<n>.before.json.
"""
import argparse, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import generate_deck as g  # noqa: E402
from deck_spec_schema import obj, S  # noqa: E402

SCHEMA = obj(notes={"type": "array", "items": obj(key=S, match={"type": "string", "enum": ["best_match", "preview_first", "use_later", "do_not_use"]}, note=S)})

RULES = """You rate the ARES resources (videos, readings, exercises) attached to ONE science lesson, for the teacher's hidden 'ARES resources' slide. You see the lesson plan (the source of truth), the titles and overviews of ALL lessons, the deck's slide list, and each resource's slot key, title, source and type. You do NOT see the resource content: judge from its title, source and type.

Scale:
- best_match: fits what students do in the phase of its slot (key prefix = phase: predict / observe / explain / dqb / model) and does not pre-empt anything.
- preview_first: related and probably useful, but not an exact match; the teacher should preview it first. Say what to check.
- use_later: a good resource for this lesson's topic that would give an answer away or pre-empt a discovery if shown too early. The note MUST say when to use it: after which slide or activity of THIS lesson (name the slide from the slide list, e.g. 'after the card sort', 'as revision after Explain'), or in which later lesson ('in Lesson 5').
- do_not_use: ONLY if the resource is off topic, clearly the wrong level for Grade 10, or for another subject. Give the reason. Do not use it for resources that are merely badly timed: those are use_later.

Rules: The lesson plan placed each resource in a phase slot (e.g. explain.video). A resource in an Explain, Driving Question Board or Model Building slot is normally best_match, preview_first or use_later. A resource in a Predict or Observe slot that explains the idea students are meant to find out is use_later (after the Explain phase). A resource about content that a LATER lesson teaches is use_later ('in Lesson N') if it suits that lesson, do_not_use only if it suits no lesson of the unit. Notes: plain English, one or two short sentences, at most 25 words. Return exactly one entry for every resource key given, using the keys exactly as given."""


def parse(spec, n):
    out = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-"); out |= set(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return sorted(x for x in out if 1 <= x <= n)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); ap.add_argument("--lessons", default=""); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.data)); n = len(data["LESSONS"])
    lessons = parse(a.lessons, n) if a.lessons else list(range(1, n + 1))
    sub = os.path.basename(os.path.dirname(os.path.abspath(a.data)))
    sd = os.path.join(ROOT, g.CFG["spec_root"], data["META"]["subject"], sub)
    client = None
    if not a.dry_run:
        g.load_env(); import anthropic; client = anthropic.Anthropic()
    total = 0.0
    for ln in lessons:
        sp = os.path.join(sd, f"L{ln}.spec.json"); spec = json.load(open(sp))
        lesson = next(l for l in data["LESSONS"] if l["number"] == ln)
        res = g.resources_for(a.data, ln)
        cur = {r["key"]: r for r in spec["glance"]["resource_notes"]}
        body = {"lesson_number": ln, "lesson_plan": {k: v for k, v in lesson.items() if k not in ("resourceLinks",)},
                "all_lessons": [{"number": l["number"], "title": l["title"], "overview": l["overview"]} for l in data["LESSONS"]],
                "deck_slides": [{"phase": s["phase"], "title": s["title"]} for s in spec["slides"]],
                "resources": [{"key": r["key"], "also_in_slots": r["also"], "title": r["title"], "source": r["source"], "type": r["content_type"], "current_rating": (cur.get(r["key"]) or {}).get("match")} for r in res]}
        if a.dry_run:
            print(f"L{ln}: {len(res)} resources, input chars {len(json.dumps(body))}"); continue
        for attempt in (1, 2):
            out, u = g.call(client, g.CFG["model"], RULES, json.dumps(body, ensure_ascii=False), SCHEMA, f"rerate L{ln}", max_tokens=16000)
            total += g.cost(u)
            keys = [x["key"] for x in out["notes"]]
            if sorted(keys) == sorted(r["key"] for r in res):
                break
            print(f"  L{ln}: keys differ ({set(keys) ^ {r['key'] for r in res}}), retrying")
        else:
            print(f"  L{ln}: FAILED to get matching keys"); continue
        os.makedirs(os.path.join(ROOT, "logs", "rerate"), exist_ok=True)
        json.dump(spec["glance"]["resource_notes"], open(os.path.join(ROOT, "logs", "rerate", f"L{ln}.before.json"), "w"), indent=1, ensure_ascii=False)
        spec["glance"]["resource_notes"] = out["notes"]
        spec["build_log"].append({"slide": "Lesson at a glance / ARES resources", "type": "resource_note", "sow_says": "The lesson plan attaches resources to phase slots by topic match.", "deck_does": "Resources re-rated on the 4-level scale (best match / preview first / use later / do not use) after Mark's review, 2026-10-22: well-matched but badly timed resources are 'use later' with when to use them.", "why": "The first 3-level scale marked 59 of 89 resources DO NOT USE because it had no way to say 'good, but after Explain'."})
        json.dump(spec, open(sp, "w"), indent=1, ensure_ascii=False)
        c = {m: sum(1 for x in out["notes"] if x["match"] == m) for m in ("best_match", "preview_first", "use_later", "do_not_use")}
        print(f"L{ln}: {c}")
    print(f"estimated API cost: ${total:.2f}")


if __name__ == "__main__":
    main()
