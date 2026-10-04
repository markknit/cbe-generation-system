#!/usr/bin/env python3
"""
audit_link_relevance.py — independent precision check of resource links
=======================================================================
The link gate's rules are the matcher's own, so "0 failures" proves the rules
work, not that links fit the lesson. This asks a model (claude-sonnet-5-5) to
judge, per lesson, whether each linked resource TITLE fits that lesson. Old and
new links for the same lesson are pooled and shuffled, so the judge cannot tell
which matcher produced which.

  python3 scripts/audit_link_relevance.py OLD_ROOT [--lessons 60] [--seed 7]

OLD_ROOT is a directory containing data/outputs/v2/**/_data.json from before the
matcher change (e.g. `git show 96d37b4~1:<path>` extracted to a scratch dir).
Judge sees only titles + lesson context, which is what a teacher sees.
Output: precision of each set, and the worst new links, for human review.
"""
import glob
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import generate_substrand as g  # noqa: E402

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {"verdicts": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "properties": {"id": {"type": "integer"},
                       "verdict": {"type": "string", "enum": ["fits", "partial", "off_topic"]},
                       "why": {"type": "string"}},
        "required": ["id", "verdict", "why"]}}},
    "required": ["verdicts"],
}


def titles(lesson):
    out = {}
    for ph, d in (lesson.get("resourceLinks") or {}).items():
        for k, r in (d or {}).items():
            if isinstance(r, dict) and r.get("title"):
                out[r["title"]] = out.get(r["title"], 0) + 1
    return out


def main():
    old_root = Path(sys.argv[1])
    n = int(sys.argv[sys.argv.index("--lessons") + 1]) if "--lessons" in sys.argv else 60
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
    rnd = random.Random(seed)
    new_files = sorted(f for f in glob.glob(str(ROOT / "data/outputs/v2/*/*/*_data.json")) if "Grade11" not in f)
    # stratified: round-robin over subjects
    by_subj = {}
    for f in new_files:
        by_subj.setdefault(f.split("/v2/")[1].split("/")[0], []).append(f)
    picks = []
    pools = {s: [(f, i) for f in fs for i in range(len(json.load(open(f))["LESSONS"]))] for s, fs in by_subj.items()}
    for s in pools:
        rnd.shuffle(pools[s])
    while len(picks) < n and any(pools.values()):
        for s in sorted(pools):
            if pools[s] and len(picks) < n:
                picks.append(pools[s].pop())
    res = {"old": [0, 0, 0], "new": [0, 0, 0]}   # fits, partial, off_topic (unique title per lesson)
    worst = []
    for f, i in picks:
        rel = Path(f).relative_to(ROOT)
        of = old_root / rel
        if not of.exists():
            continue
        new_l = json.load(open(f))["LESSONS"][i]
        old_l = json.load(open(of))["LESSONS"][i]
        tn, to = titles(new_l), titles(old_l)
        pool = sorted(set(tn) | set(to))
        rnd.shuffle(pool)
        if not pool:
            continue
        listing = "\n".join(f"{k}. {t}" for k, t in enumerate(pool))
        prompt = f"""You are checking resources linked to a Kenyan CBE Grade 10 lesson. Judge each resource by TITLE only, as a teacher scanning a list would.

Subject: {new_l.get('substrand', '')}
Lesson {new_l.get('number')}: {new_l.get('title')}
Keywords: {new_l.get('aresKeywords', '')}
Overview: {(new_l.get('overview') or '')[:700]}

Resources:
{listing}

For each, "fits" = a teacher would plausibly use it for THIS lesson's content; "partial" = right broad topic, wrong specific topic or level; "off_topic" = a different topic or subject. Be strict. One-line "why"."""
        r = g.call_claude(prompt, schema=SCHEMA)
        if not r:
            continue
        v = {x["id"]: x for x in r["verdicts"]}
        for k, t in enumerate(pool):
            x = v.get(k)
            if not x:
                continue
            idx = {"fits": 0, "partial": 1, "off_topic": 2}[x["verdict"]]
            if t in tn:
                res["new"][idx] += 1
                if idx == 2:
                    worst.append((str(rel.parts[3]), new_l.get("number"), t, x["why"]))
            if t in to:
                res["old"][idx] += 1
    for k in ("old", "new"):
        t = sum(res[k]) or 1
        print(f"{k.upper()}: {sum(res[k])} links judged | fits {100*res[k][0]/t:.0f}% | partial {100*res[k][1]/t:.0f}% | off-topic {100*res[k][2]/t:.0f}%")
    print(f"\nNEW links judged off-topic ({len(worst)}):")
    for w in worst[:40]:
        print(f"  {w[0]} L{w[1]}: {w[2]!r} -- {w[3][:110]}")
    print(f"\nEstimated spend: ${g._estimate_cost():.2f}")


if __name__ == "__main__":
    main()
