"""
lesson_consistency.py — keep the lessons of one sub-strand telling ONE story
============================================================================
Lessons are generated in parallel (batch mode), so before 2026-10-04 nothing
made them agree: 91 of 95 sub-strands had lessons contradicting each other
(different datasets, wrong "in Lesson N we..." references, the same idea
taught twice). Three parts, used by src/generate_substrand.py:

  generate_fact_sheet()  BEFORE lessons: the phenomenon's data, characters and
                         outcome, plus a lesson map (who teaches what, in what
                         order). Every lesson prompt carries it.
  review()               AFTER lessons: a second call lists contradictions
                         between lessons (and against the fact sheet).
  repair()               exact find/replace edits for the contradictions; an
                         edit applies only if its old text occurs once.

The fact sheet is pipeline-internal (logged to logs/fact_sheets/), never part
of the strict partner contract JSON.
"""
import json
import re

_s = lambda: {"type": "string"}   # noqa: E731

FACT_SHEET_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "anchorData": _s(), "characters": _s(), "outcome": _s(), "conventions": _s(),
        "lessonMap": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"number": {"type": "integer"}, "focus": _s(), "teaches": _s(),
                           "buildsOn": _s(), "usesData": _s()},
            "required": ["number", "focus", "teaches", "buildsOn", "usesData"]}},
    },
    "required": ["anchorData", "characters", "outcome", "conventions", "lessonMap"],
}

REVIEW_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {"conflicts": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "properties": {"lessons": _s(), "severity": {"type": "string", "enum": ["major", "minor"]},
                       "fact": _s(), "versions": _s()},
        "required": ["lessons", "severity", "fact", "versions"]}}},
    "required": ["conflicts"],
}

REPAIR_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "edits": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"lesson": {"type": "integer"}, "path": _s(), "old": _s(), "new": _s(),
                           "conflict": _s()},
            "required": ["lesson", "path", "old", "new", "conflict"]}},
        "unresolved": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"conflict": _s(), "why": _s()}, "required": ["conflict", "why"]}},
    },
    "required": ["edits", "unresolved"],
}


# ── Fact sheet ────────────────────────────────────────────────────────────────

def generate_fact_sheet(call, subject: str, grade, substrand: str, n_lessons: int,
                        unit: dict, curriculum_text: str = "", template_outline: str = "") -> dict | None:
    prompt = f"""You are planning ONE Kenyan CBE Grade {grade} {subject} sub-strand ({substrand}) of {n_lessons} lessons. The lessons will be written SEPARATELY, in parallel, by writers who cannot see each other's work. Write the shared FACT SHEET they will all follow, so every lesson tells the same story.

Driving question: {unit.get('drivingQuestion', '')}
Phenomenon: {unit.get('phenomenon', '')}
Storyline: {unit.get('storylineThread') or unit.get('storyline', '')}
{('Teacher outline of the lesson sequence:' + chr(10) + template_outline) if template_outline else ''}
KICD content (for scope):
{curriculum_text[:6000]}

Fields:
- "anchorData": every number, measurement, table and named value the phenomenon uses, stated ONCE and exactly (e.g. a split-time table with every row). Make figures realistic and CHECK all arithmetic and every comparison (who is ahead, what is larger) before you write it.
- "characters": the named people, places, objects and groups, with the one fact each lesson may rely on.
- "outcome": how the phenomenon resolves (what happened and why), in two or three sentences every lesson must agree with.
- "conventions": terms, symbols, units and definitions used throughout (e.g. distance vs displacement, which formula name).
- "lessonMap": one entry per lesson 1..{n_lessons}: "focus" (short title), "teaches" (the ONE new idea or skill), "buildsOn" (which earlier lesson numbers and what from them), "usesData" (which part of anchorData). No two lessons may teach the same new idea. Lesson 1 launches the phenomenon; lesson {n_lessons} is the final explanation."""
    return call(prompt, schema=FACT_SHEET_SCHEMA)


def fact_sheet_block(fs: dict | None, num: int | None = None) -> str:
    """The text every lesson prompt carries (and the reviewer/Final Explanation)."""
    if not fs:
        return ""
    lm = "\n".join(f"  Lesson {e['number']}: {e['focus']} | teaches: {e['teaches']} | builds on: {e['buildsOn']} | data: {e['usesData']}"
                   for e in fs.get("lessonMap", []))
    this = ""
    if num is not None:
        e = next((x for x in fs.get("lessonMap", []) if x["number"] == num), None)
        if e:
            this = (f"\nTHIS LESSON ({num}): teach {e['teaches']}; build on {e['buildsOn']}; "
                    f"use {e['usesData']}.\n")
    return f"""ESTABLISHED FACTS FOR THIS SUB-STRAND (shared by every lesson; use them EXACTLY):
ANCHOR DATA: {fs['anchorData']}
CHARACTERS/PLACES: {fs['characters']}
OUTCOME: {fs['outcome']}
CONVENTIONS: {fs['conventions']}
LESSON MAP:
{lm}
{this}RULES: do not invent different numbers, names or outcomes for the phenomenon; when you
refer to an earlier lesson, refer only to what the LESSON MAP says it taught; do not re-teach an
idea that the map gives to another lesson.
"""


# ── Review ────────────────────────────────────────────────────────────────────

def digest(unit: dict, lessons: list) -> str:
    parts = [f"PHENOMENON: {unit.get('phenomenon', '')}\n"]
    for l in lessons:
        stp = l.get("summaryTablePrompt") or {}
        parts.append(f"=== LESSON {l.get('number')}: {l.get('title', '')}\nOverview: {l.get('overview', '')}\n"
                     f"Observed: {stp.get('observed', '')}\nLearned: {stp.get('learned', '')}\n"
                     f"Explained: {stp.get('explained', '')}")
        for ph in l.get("framework", []) or []:
            parts.append(f"  [{ph.get('phase', '')}] Learners: {(ph.get('learnerExperience') or '')[:700]} "
                         f"| Teacher: {(ph.get('teacherMoves') or '')[:500]}")
    return "\n".join(parts)


def review(call, subject: str, grade, substrand: str, unit: dict, lessons: list,
           fact_sheet: dict | None = None) -> list | None:
    fs = ("\nThe lessons were meant to follow this FACT SHEET; also report a lesson that contradicts it:\n"
          + fact_sheet_block(fact_sheet)) if fact_sheet else ""
    prompt = f"""You are checking ONE sub-strand of a Kenyan CBE Grade {grade} {subject} lesson sequence ({substrand}). The lessons were written separately. Find places where lessons CONTRADICT EACH OTHER about a fact.
{fs}
{digest(unit, lessons)}

Report only real contradictions of fact between two or more lessons: different numbers, times, quantities or units for the same thing; opposite outcomes (who won, which is larger, what happened); different characters, places or datasets for the same phenomenon; an impossible or unrealistic figure the lessons depend on; a term defined differently; a lesson citing the wrong earlier lesson. Do NOT report style, different examples that don't conflict, or things one lesson says that another simply doesn't mention. Before reporting a calculation, recompute it: do not report a correct calculation.
severity "major": a teacher following the sequence would teach students two incompatible things, or a dataset/outcome the sequence builds on changes between lessons. "minor": a small numeric or wording inconsistency that would not mislead.
Return {{"conflicts": []}} if there are none. Otherwise one entry per conflict: "lessons" (e.g. "2, 5, 8"), "fact", "versions" (what each lesson says)."""
    r = call(prompt, schema=REVIEW_SCHEMA)
    return None if r is None else r["conflicts"]


# ── Repair ────────────────────────────────────────────────────────────────────

def _split_path(path: str):
    return [int(p) if p.isdigit() else p for p in re.findall(r"[^.\[\]]+", path)]


def apply_edit(lessons: list, e: dict):
    target = next((l for l in lessons if l.get("number") == e["lesson"]), None)
    if target is None:
        return False, "no such lesson"
    try:
        keys = _split_path(e["path"])
        cur = target
        for k in keys[:-1]:
            cur = cur[k]
        text = cur[keys[-1]]
    except (KeyError, IndexError, TypeError):
        return False, "path not found"
    if not isinstance(text, str):
        return False, "path is not a string field"
    if not e["old"] or e["old"] == e["new"]:
        return False, "empty or no-op edit"
    n = text.count(e["old"])
    if n != 1:
        return False, f"old text occurs {n} times (need exactly 1)"
    cur[keys[-1]] = text.replace(e["old"], e["new"], 1)
    return True, ""


def repair(call, subject: str, grade, substrand: str, lessons: list, conflicts: list,
           fact_sheet: dict | None = None, chunk: int = 3) -> dict:
    """Mutates `lessons`. Returns {"applied", "rejected", "unresolved"}."""
    last = lessons[-1]["number"] if lessons else 0
    valid_idx = "; ".join(f"lesson {l['number']}: 0-{len(l.get('framework', [])) - 1}" for l in lessons)
    authority = ("the FACT SHEET below is authoritative; change any lesson that disagrees with it.\n"
                 + fact_sheet_block(fact_sheet)) if fact_sheet else \
        (f"Lesson 1 (it launches the phenomenon and sets the data) and Lesson {last} win; if neither "
         f"speaks to it, the earliest lesson that establishes the fact wins.")
    out = {"applied": [], "rejected": [], "unresolved": []}

    def run(group):
        listing = "\n".join(f"{i + 1}. [{c['severity']}] lessons {c['lessons']}: {c['fact']}\n   {c['versions']}"
                            for i, c in enumerate(group))
        slim = [{k: v for k, v in l.items() if k != "resourceLinks"} for l in lessons]
        # The lessons (large, identical across the chunked calls of one repair round) go in a
        # cached prefix; the conflicts to fix go after it.
        prefix = f"""Kenyan CBE Grade {grade} {subject} sub-strand ({substrand}). THE LESSONS (JSON):
{json.dumps(slim, ensure_ascii=False, indent=1)}

VALID "framework" INDICES: {valid_idx}
"""
        prompt = f"""You are repairing contradictions BETWEEN THE LESSONS above. A reviewer found:

{listing}

For each contradiction, {authority}
Change the lessons that disagree, as little as possible: a number, a name, an outcome, a dataset value, a wrong "in Lesson N we did X" reference. If a changed number feeds a calculation, fix that arithmetic too and check it.

Return EXACT find-and-replace edits: "lesson" (number), "path" (e.g. "overview", "summaryTablePrompt.explained", "framework[3].teacherMoves", "slo.knowledge"), "old" (a short EXACT substring that occurs once in that field), "new", "conflict" (its number). Do not rewrite paragraphs or add teaching content. If a contradiction needs more than small edits, put it in "unresolved" with the reason."""
        r = call(prompt, max_tokens=16000, schema=REPAIR_SCHEMA, cache_prefix=prefix)
        if not r:
            if len(group) > 1:
                for c in group:
                    run([c])
                return
            out["unresolved"].append({"conflict": group[0]["fact"], "why": "repair call failed"})
            return
        for e in r["edits"]:
            ok, why = apply_edit(lessons, e)
            (out["applied"] if ok else out["rejected"]).append({**e, **({} if ok else {"rejected": why})})
        out["unresolved"].extend(r["unresolved"])

    for i in range(0, len(conflicts), chunk):
        run(conflicts[i:i + chunk])
    return out


def check_and_repair(call, subject: str, grade, substrand: str, unit: dict, lessons: list,
                     fact_sheet: dict | None = None, rounds: int = 2) -> dict:
    """Review -> repair majors -> review, up to `rounds` repairs. Keeps the
    version with the FEWEST majors (repairs can make things worse)."""
    import copy
    history = []
    conflicts = review(call, subject, grade, substrand, unit, lessons, fact_sheet)
    if conflicts is None:
        return {"status": "review_failed", "history": history, "lessons": lessons}
    best = (sum(c["severity"] == "major" for c in conflicts), copy.deepcopy(lessons), conflicts)
    for rnd in range(rounds):
        majors = [c for c in conflicts if c["severity"] == "major"]
        history.append({"round": rnd, "majors": len(majors), "minors": len(conflicts) - len(majors)})
        if not majors:
            break
        rep = repair(call, subject, grade, substrand, lessons, majors, fact_sheet)
        history[-1]["repair"] = {k: len(v) for k, v in rep.items()}
        history[-1]["edits"] = rep
        conflicts = review(call, subject, grade, substrand, unit, lessons, fact_sheet)
        if conflicts is None:
            break
        n = sum(c["severity"] == "major" for c in conflicts)
        if n < best[0]:
            best = (n, copy.deepcopy(lessons), conflicts)
    lessons[:] = best[1]
    return {"status": "ok", "majors": best[0], "conflicts": best[2], "history": history, "lessons": lessons}
