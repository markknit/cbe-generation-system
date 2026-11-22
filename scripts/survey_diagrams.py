#!/usr/bin/env python3
"""
survey_diagrams.py - one batch pass over the lesson plans: which diagrams does each lesson's deck need?

Output feeds the decision on which diagram families to build (generators/presentations/lib/) before the mass run.
Presentations branch only. Reads lesson data (read-only). Uses the Message Batches API (50% price), Sonnet 5.5.

  python3 scripts/survey_diagrams.py submit [--limit N] [--grade 10] [--subject Physics]
  python3 scripts/survey_diagrams.py collect       # waits? no: run again until it prints "ended"
  python3 scripts/survey_diagrams.py summary

Files: data/presentations_specs/_survey/{manifest.json, survey.jsonl}
"""
import argparse
import glob
import hashlib
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import generate_deck as gd  # noqa: E402

OUT = os.path.join(ROOT, "data", "presentations_specs", "_survey")
MAN = os.path.join(OUT, "manifest.json")
RES = os.path.join(OUT, "survey.jsonl")
MODEL = "claude-sonnet-5-5"

KINDS = ["cell_or_organism_structure", "organ_or_body_system", "force_or_motion_diagram", "circuit_diagram",
         "ray_or_wave_diagram", "data_graph_or_chart", "lab_apparatus_setup", "atom_or_electron_model",
         "bonding_diagram", "periodic_table_view", "structural_formula_or_molecule", "process_or_cycle_flow",
         "geometry_figure", "coordinate_grid_transformation", "number_line", "statistics_chart",
         "probability_tree_or_venn", "vector_diagram", "map_or_field_scene", "other"]

SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["diagrams", "drawn_by_hand_only_note"],
    "properties": {
        "diagrams": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["kind", "what", "elements", "student_action", "slide_must_show_figure", "reuse_key"],
            "properties": {
                "kind": {"type": "string", "enum": KINDS},
                "what": {"type": "string"},          # what the drawing shows, one line
                "elements": {"type": "string"},      # what must appear and be labelled/measured, one or two lines
                "student_action": {"type": "string", "enum": ["shown_to_students", "students_label", "students_draw", "students_complete"]},
                "slide_must_show_figure": {"type": "boolean"},  # true only if the SLIDE itself must display a drawn figure
                "reuse_key": {"type": "string"},     # short snake_case name; the same drawing in another lesson gets the same key
            }}},
        "drawn_by_hand_only_note": {"type": "string"},  # drawings the lesson asks for that a slide cannot reasonably show; "" if none
    },
}

SYSTEM = """You are surveying Kenyan Grade 10 CBE lesson plans to decide which labelled teaching diagrams a slide deck for the lesson would need.
For ONE lesson plan, list every distinct diagram, figure, graph or technical drawing that a good classroom slide would SHOW or that students are asked to label, draw or complete, in the order of the lesson. Skip decorative scenes and photographs (a picture of a kitchen is not a diagram), tables, sorting cards, sticky-note posters, Driving Question Board charts and concept-map frames.
A drawing that students make freely on paper (their own predict sketch, their own model) is listed only if the slide must also SHOW a figure for them to copy, label or compare with (then set slide_must_show_figure true); a free sketch with nothing for the slide to show gets slide_must_show_figure false. slide_must_show_figure is true for: a figure the teacher shows, a figure students label or complete, a graph/grid/circuit/ray/apparatus/atom/bonding/geometry figure the slide has to draw.
Rules: one entry per distinct drawing (not per slide). `kind` must be the closest family from the list. `what` is one line. `elements` names what must appear and which parts are labelled, with any values (for example 'axes with time in s and distance in m; points plotted from the table; line of best fit'). `reuse_key` is a short snake_case name for the drawing so the same drawing in another lesson would get the same key. If the lesson needs no diagram, return an empty list. Use kind "other" only when no family fits, and say what it is in `what`. Be faithful to the lesson plan; do not invent drawings it does not use."""


def lessons(grade, subject):
    for f in sorted(glob.glob(os.path.join(ROOT, "data/outputs/v2/*/*/*_data.json"))):
        if "/PDF/" in f:
            continue
        d = json.load(open(f))
        if str(d["META"].get("grade")) != str(grade) or (subject and d["META"]["subject"] != subject):
            continue
        for l in d["LESSONS"]:
            yield f, d, l


def cid(f, n):
    return "s" + hashlib.sha1(f"{f}|{n}".encode()).hexdigest()[:20]


def submit(a):
    import anthropic
    gd.load_env()
    reqs, man = [], {}
    seen_subj = {}
    for f, d, l in lessons(a.grade, a.subject):
        if a.lesson and l["number"] != a.lesson:
            continue
        if a.limit and a.per_subject:
            s = d["META"]["subject"]
            if seen_subj.get(s, 0) >= a.limit:
                continue
            seen_subj[s] = seen_subj.get(s, 0) + 1
        elif a.limit and len(reqs) >= a.limit:
            break
        body = {"subject": d["META"]["subject"], "grade": d["META"]["grade"], "sub_strand": d["META"].get("substrand_name"),
                "lesson": {k: v for k, v in l.items() if k != "resourceLinks"}}
        c = cid(f, l["number"])
        man[c] = {"file": os.path.relpath(f, ROOT), "lesson": l["number"], "subject": d["META"]["subject"],
                  "sub_strand": d["META"].get("substrand_name"), "title": l["title"]}
        reqs.append({"custom_id": c, "params": {
            "model": MODEL, "max_tokens": 6000, "system": SYSTEM,
            "messages": [{"role": "user", "content": json.dumps(body, ensure_ascii=False)}],
            "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": SCHEMA}}}})
    if not reqs:
        sys.exit("no lessons selected")
    os.makedirs(OUT, exist_ok=True)
    chunks = [reqs[i:i + 2000] for i in range(0, len(reqs), 2000)]
    cl = anthropic.Anthropic()
    ids = []
    for ch in chunks:
        ids.append(cl.messages.batches.create(requests=ch).id)
    json.dump({"batches": ids, "lessons": man, "submitted": time.time(), "model": MODEL}, open(MAN, "w"), indent=1)
    if os.path.exists(RES):
        os.remove(RES)
    print(f"submitted {len(reqs)} lesson(s) in {len(ids)} batch(es): {ids}")


def collect(a):
    import anthropic
    gd.load_env()
    cl = anthropic.Anthropic()
    m = json.load(open(MAN))
    done = True
    for b in m["batches"]:
        bb = cl.messages.batches.retrieve(b)
        if bb.processing_status != "ended":
            print(b, bb.processing_status, bb.request_counts); done = False
    if not done:
        return
    n_ok = n_err = 0
    cost = 0.0
    with open(RES, "w") as out:
        for b in m["batches"]:
            for r in cl.messages.batches.results(b):
                info = m["lessons"][r.custom_id]
                if r.result.type != "succeeded" or r.result.message.stop_reason != "end_turn":
                    n_err += 1; out.write(json.dumps({**info, "error": r.result.type}) + "\n"); continue
                u = gd.usage_dict(r.result.message.usage)
                cost += gd.cost(u) * 0.5
                text = next(x.text for x in r.result.message.content if x.type == "text")
                out.write(json.dumps({**info, **json.loads(text)}, ensure_ascii=False) + "\n"); n_ok += 1
    print(f"ended: {n_ok} ok, {n_err} failed; estimated cost ${cost:.2f}")


def summary(a):
    import collections
    rows = [json.loads(x) for x in open(RES)]
    ok = [r for r in rows if "diagrams" in r]
    print(f"{len(ok)} lessons surveyed ({len(rows) - len(ok)} failed)")
    by = collections.defaultdict(lambda: collections.Counter())
    lessons_with = collections.Counter(); total = collections.Counter(); kinds = collections.Counter()
    act = collections.Counter(); keys = collections.defaultdict(set)
    for r in ok:
        s = r["subject"]; total[s] += 1
        fig = [d for d in r["diagrams"] if d["slide_must_show_figure"]]
        if fig:
            lessons_with[s] += 1
        for dg in fig:
            by[s][dg["kind"]] += 1; kinds[dg["kind"]] += 1; act[dg["student_action"]] += 1
            keys[dg["kind"]].add(dg["reuse_key"])
    print("\nLessons where the slide must show at least one figure:")
    for s in sorted(total):
        print(f"  {s:24s} {lessons_with[s]:4d} / {total[s]:4d}")
    print("\nDiagram kinds (count of drawings, distinct reuse keys):")
    for k, v in kinds.most_common():
        print(f"  {k:34s} {v:5d}  keys={len(keys[k])}")
    print("\nStudent action:", dict(act))
    print("\nBy subject:")
    for s in sorted(by):
        print(f"  {s}: " + ", ".join(f"{k} {v}" for k, v in by[s].most_common(6)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["submit", "collect", "summary"])
    ap.add_argument("--grade", default="10")
    ap.add_argument("--subject", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--lesson", type=int, default=0, help="only this lesson number (for test samples)")
    ap.add_argument("--per-subject", action="store_true", help="--limit applies per subject")
    a = ap.parse_args()
    {"submit": submit, "collect": collect, "summary": summary}[a.cmd](a)
