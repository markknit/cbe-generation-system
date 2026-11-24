#!/usr/bin/env python3
"""
quiz_links.py - stable quiz and question IDs plus the slide-to-question list for deck quiz links.

Link convention (PROVISIONAL, from the response-capture project; the route is not implemented yet):
    http://ares.local/quiz/<quiz-id>/<version>/question/<question-id>
  quiz-id      stable per lesson: <subject>-g<grade>-<substrand with dots as dashes>-l<nn>, e.g. bio-g10-1-2-l01
  version      v1, v2, ...: bumps when a question's wording, a choice, the choice order, the correct answer or the
               rationale (answer key) changes. Phase and placement text are cosmetic and never bump it.
  question-id  q01, q02, ...: independent of slide number. A question keeps its ID when its prompt text is unchanged;
               a question reworded in place keeps the ID of the question it replaced; new questions get new numbers;
               a retired ID is never reused.
No student data, class, card number or answer appears in a link.

The quiz JSON (*_quiz.json) belongs to `main` and is never edited here, so the IDs live in a registry owned by this
branch: data/quiz_registry.json. Commit it: it is what keeps IDs stable between runs.

  python3 scripts/quiz_links.py registry            # create or update the registry from every *_quiz.json
  python3 scripts/quiz_links.py registry --check    # exit 1 if the registry is out of date (no write)
The slide-to-question list is written by the deck build, beside each deck: <deck>.quizlinks.csv (slide, quiz id, version,
question id, url, phase, placement). Placement logic: generators/presentations/lib/quizlinks.js.
"""
import argparse
import csv
import difflib
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "data", "quiz_registry.json")
URL = "http://ares.local/quiz/{quiz}/{ver}/question/{q}"
SUBJ = {"Biology": "bio", "Chemistry": "chem", "Physics": "phys", "Mathematics": "math", "Core Mathematics": "cmath",
        "Essential Mathematics": "emath", "General Science": "gsci"}


def h(obj):
    return hashlib.sha1(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]


def qkey(q):  # what a learner or the answer key would notice
    return {"prompt": q["prompt"].strip(), "choices": [c.strip() for c in q["choices"]], "correct": q["correctIndex"], "rationale": q.get("rationale", "").strip()}


def quiz_id(meta, n):
    subj = SUBJ.get(meta["subject"])
    if not subj:
        sys.exit(f"unknown subject '{meta['subject']}': add it to SUBJ")
    ss = re.sub(r"[^0-9a-z]+", "-", str(meta["substrandId"]).lower()).strip("-")
    return f"{subj}-g{meta['grade']}-{ss}-l{int(n):02d}"


def load_quizzes():
    for f in sorted(glob.glob(os.path.join(ROOT, "data/outputs/v2/**/*_quiz.json"), recursive=True)):
        if "/PDF/" in f:
            continue
        d = json.load(open(f))
        for l in d["lessons"]:
            if l.get("quiz"):
                yield os.path.relpath(f, ROOT), d["meta"], l


def update_entry(old, quiz, source):
    """Return the new registry entry for one lesson's quiz, keeping IDs and bumping the version when needed."""
    qs = quiz
    keys = [qkey(q) for q in qs]
    hashes = [h(k) for k in keys]
    prompts = [k["prompt"] for k in keys]
    if not old:
        ids = [f"q{i + 1:02d}" for i in range(len(qs))]
        return {"source": source, "version": "v1", "content_hash": h(hashes), "next_q": len(qs) + 1,
                "questions": [{"id": i, "hash": x, "prompt": p} for i, x, p in zip(ids, hashes, prompts)], "retired": [], "history": []}
    if old["content_hash"] == h(hashes):
        old["source"] = source
        return old
    # match by identical prompt first, then reworded questions in order take the unmatched old IDs
    by_prompt = {q["prompt"]: q["id"] for q in old["questions"]}
    taken, ids = set(), [None] * len(qs)
    for i, p in enumerate(prompts):
        if p in by_prompt and by_prompt[p] not in taken:
            ids[i] = by_prompt[p]; taken.add(ids[i])
    free = {q["id"]: q["prompt"] for q in old["questions"] if q["id"] not in taken}
    nxt = old["next_q"]
    for i, p in enumerate(prompts):  # a reworded question (similar text) keeps the ID of the question it replaced
        if ids[i] is None and free:
            best = max(free, key=lambda k: difflib.SequenceMatcher(None, free[k], p).ratio())
            if difflib.SequenceMatcher(None, free[best], p).ratio() >= 0.6:
                ids[i] = best; free.pop(best)
    for i in range(len(qs)):
        if ids[i] is None:
            ids[i] = f"q{nxt:02d}"; nxt += 1
    retired = old["retired"] + list(free)
    ver = "v" + str(int(old["version"][1:]) + 1)
    hist = old["history"] + [{"version": old["version"], "content_hash": old["content_hash"], "questions": [q["id"] for q in old["questions"]]}]
    return {"source": source, "version": ver, "content_hash": h(hashes), "next_q": nxt,
            "questions": [{"id": i, "hash": x, "prompt": p} for i, x, p in zip(ids, hashes, prompts)], "retired": retired, "history": hist}


def registry(a):
    reg = json.load(open(REG)) if os.path.exists(REG) else {"link_format": URL, "provisional": True, "quizzes": {}}
    before = json.dumps(reg, sort_keys=True)
    reg["link_format"], reg["provisional"] = URL, True
    seen = set()
    for source, meta, l in load_quizzes():
        qid = quiz_id(meta, l["number"])
        if qid in seen:
            sys.exit(f"duplicate quiz id {qid}")
        seen.add(qid)
        e = update_entry(reg["quizzes"].get(qid), l["quiz"], source)
        e.update({"subject": meta["subject"], "grade": meta["grade"], "substrand": meta["substrandName"], "lesson": l["number"], "lesson_title": l["title"]})
        reg["quizzes"][qid] = e
    gone = [k for k in reg["quizzes"] if k not in seen]
    if gone:
        print("WARNING: in the registry but no longer in any quiz file (kept, not deleted):", ", ".join(gone))
    changed = json.dumps(reg, sort_keys=True) != before
    if a.check:
        print("registry is up to date" if not changed else "registry is OUT OF DATE: run `quiz_links.py registry`")
        sys.exit(1 if changed else 0)
    if changed:
        json.dump(reg, open(REG, "w"), indent=1, ensure_ascii=False)
        open(REG, "a").write("\n")
    bumped = [(k, v["version"]) for k, v in reg["quizzes"].items() if v["version"] != "v1"]
    print(f"{'wrote' if changed else 'unchanged'} {os.path.relpath(REG, ROOT)}: {len(reg['quizzes'])} quizzes, "
          f"{sum(len(v['questions']) for v in reg['quizzes'].values())} questions; versions above v1: {bumped or 'none'}")


def check(a):
    """Consistency between the quiz files and the lesson plans they belong to (the contract in docs/presentations/QUIZ_DECK_CONTRACT.md)."""
    import yaml
    cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "quiz_generation.yaml")))
    phases = set(cfg["phases"]); problems, n = [], 0
    for f in sorted(glob.glob(os.path.join(ROOT, "data/outputs/v2/**/*_quiz.json"), recursive=True)):
        if "/PDF/" in f:
            continue
        q = json.load(open(f)); rel = os.path.relpath(f, ROOT)
        dp = f.replace("_quiz.json", "_data.json")
        plan = {}
        if os.path.exists(dp):
            d = json.load(open(dp)); plan = {l["number"]: l for l in d.get("lessons", [])}
        else:
            problems.append(f"{rel}: no _data.json beside the quiz")
        for l in q["lessons"]:
            if not l.get("quiz"):
                continue
            n += 1; tag = f"{rel} L{l['number']}"
            if plan and l["number"] not in plan:
                problems.append(f"{tag}: the lesson plan has no lesson {l['number']} (renumbered or split?)")
            elif plan and plan[l["number"]].get("title", "").strip() != l["title"].strip():
                problems.append(f"{tag}: quiz title differs from the lesson plan title (plan: {plan[l['number']].get('title', '')[:60]!r})")
            for i, x in enumerate(l["quiz"], 1):
                if x.get("phase") not in phases:
                    problems.append(f"{tag} Q{i}: phase {x.get('phase')!r} is not one of {sorted(phases)}")
                if not (x.get("placement") or "").strip():
                    problems.append(f"{tag} Q{i}: no placement text")
                if re.search(r"\b(the|this) (slide|picture|photo|image|figure)\b|\bshown (above|below)\b", x["prompt"], re.I):
                    problems.append(f"{tag} Q{i}: the question depends on something the student cannot see")
    print(f"checked {n} quizzes")
    for p in problems:
        print("  PROBLEM", p)
    print("contract check: " + ("OK" if not problems else f"{len(problems)} problem(s)"))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("registry"); r.add_argument("--check", action="store_true"); r.set_defaults(f=registry)
    c = sub.add_parser("check"); c.set_defaults(f=check)
    a = ap.parse_args()
    a.f(a)
