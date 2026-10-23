"""JSON schema for a lesson deck spec (the contract between src/generate_deck.py and
generators/presentations/build_deck.js). Used as the structured-output schema for the authoring call and
written to config/deck_spec.schema.json. Presentations branch only.

Strict-mode rules: every property required, additionalProperties false; empty list / "" = nothing to say."""
import json
import os
import subprocess

S = {"type": "string"}
I = {"type": "integer"}
B = {"type": "boolean"}
SL = {"type": "array", "items": S}


def obj(**props):
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


def const(v):
    return {"type": "string", "enum": [v]}


NOTES = {"$ref": "#/$defs/notes"}
NOTES_DEF = obj(
    do=SL, say=SL, wait_time=S, look_for=SL, if_then=SL, why_this_works=S, answer_key=SL, science_note=S,
)

# One flat block type keeps the compiled grammar small (an 8-way anyOf was rejected as too large).
#   text      -> text (+ style)            bullets / numbered / cards -> items
#   callout   -> text (heading line) + items (sentence starters)
#   table     -> rows (first row = headers)
#   columns   -> items, each "Heading :: body text"
#   tiles     -> items, each "icon_name :: text" (big colourful icon cards)
#   illustration -> items = [art_id, scene prompt], text = alt text (a generated picture beside the slide text)
#   bullets / numbered / callout / columns items may start with "icon_name :: " to show a colourful icon
#   diagram   -> template + labels, text = caption
def _template_names():
    """Diagram templates come from the JS library, so adding a template needs no schema edit."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = subprocess.run(["node", "-e", "console.log(JSON.stringify(Object.keys(require('./generators/presentations/lib/diagrams.js').TEMPLATES)))"],
                         cwd=root, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


BLOCK = obj(
    type={"type": "string", "enum": ["text", "bullets", "numbered", "callout", "table", "cards", "columns", "tiles", "illustration", "diagram"]},
    style={"type": "string", "enum": ["normal", "question", "emphasis", "caption"]},
    text=S, items=SL, rows={"type": "array", "items": SL},
    template={"type": "string", "enum": ["none"] + _template_names()}, labels=SL,
)

PHASES = ["predict", "observe", "explain", "dqb", "model"]
SLIDE = obj(
    phase={"type": "string", "enum": PHASES},
    title=S, subtitle=S, check_for_understanding=B, student_task=B, minutes=I, time_note=S,
    timers={"type": "array", "items": obj(label=S, time=S)},
    blocks={"type": "array", "items": BLOCK},
    resources=SL,
    notes=NOTES,
)

BUILD_LOG_TYPES = ["science_flag", "term_flag", "inconsistency", "trimmed_time", "placeholder_check", "added_fact",
                   "sow_problem", "safety_flag", "resource_note", "missing_detail", "other"]
BUILD_LOG = {"type": "array", "items": obj(slide=S, type={"type": "string", "enum": BUILD_LOG_TYPES}, sow_says=S, deck_does=S, why=S)}

# The full spec is too large for one structured-output grammar, so authoring is two calls:
#   A: slides + the minutes of the fixed slides + build-log items found while writing them
#   B: everything around the slides (title slide, glance, goals, safety, summary...), given A's output
SPEC_A = obj(
    unit_map_minutes=I, goals_minutes=I, safety_minutes=I, summary_minutes=I,
    hero=obj(art_id=S, prompt=S, alt=S, icon=S),
    slides={"type": "array", "items": SLIDE},
    build_log=BUILD_LOG,
)
SPEC_B = obj(
    lesson_title_short=S, lesson_oneliner=S, purpose=SL, before_class=SL, do_not_show=SL, is_practical=B,
    so_far=S, unit_map_titles=SL,
    goals=SL, key_words={"type": "array", "items": obj(word=S, definition=S)},
    safety=obj(title=S, rules=SL),
    fixed_notes={"type": "array", "items": obj(slide={"type": "string", "enum": ["unit_map", "goals", "safety", "summary"]}, do=SL, say=SL, why_this_works=S)},
    glance=obj(
        rows={"type": "array", "items": obj(group={"type": "string", "enum": ["opening"] + PHASES + ["summary"]}, minutes=I, what=S)},
        materials=SL, fallback=S,
        resource_notes={"type": "array", "items": obj(key=S, match={"type": "string", "enum": ["best_match", "preview_first", "use_later", "do_not_use"]}, note=S)},
    ),
    summary=obj(observe_prompt=S, learn_prompt=S, explain_prompt=S, next_lesson=S,
                answer_observe=S, answer_learn=S, answer_explain=S, reflection=SL),
    build_log=BUILD_LOG,
)
SPEC_A["$defs"] = {"notes": NOTES_DEF}


def merge(a, b):
    """Merged spec in the shape build_deck.js and validate_deck.js read."""
    spec = {**a, **{k: v for k, v in b.items() if k != "build_log"}}
    spec.pop("$defs", None)
    empty = {"do": [], "say": [], "wait_time": "", "look_for": [], "if_then": [], "why_this_works": "", "answer_key": [], "science_note": ""}
    fn = {x["slide"]: {**empty, "do": x["do"], "say": x["say"], "why_this_works": x["why_this_works"]} for x in b["fixed_notes"]}
    spec.pop("fixed_notes", None)
    spec["unit_map_notes"] = fn.get("unit_map", empty)
    spec["goals_notes"] = fn.get("goals", empty)
    spec["safety"] = {**b["safety"], "minutes": a["safety_minutes"], "notes": fn.get("safety", empty)}
    spec["summary"] = {**b["summary"], "minutes": a["summary_minutes"], "notes": fn.get("summary", empty)}
    spec.pop("safety_minutes", None); spec.pop("summary_minutes", None)
    spec["build_log"] = list(a["build_log"]) + list(b["build_log"])
    return spec


REVIEW = obj(
    findings={"type": "array", "items": obj(
        slide=S, severity={"type": "string", "enum": ["major", "minor"]},
        category={"type": "string", "enum": ["spoiler", "science", "fidelity_to_sow", "missing_activity", "invented_content", "notes_quality",
                                              "student_text", "timing", "safety", "resource", "language", "other"]},
        problem=S, fix=S)},
    verdict={"type": "string", "enum": ["pass", "needs_repair"]},
)

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "config", "deck_spec.schema.json"), "w") as f:
        json.dump({"authoring_call_A": SPEC_A, "authoring_call_B": SPEC_B,
                   "note": "merge(A,B) gives the deck spec read by build_deck.js (safety.minutes and summary.minutes come from A)"}, f, indent=1)
    print("wrote config/deck_spec.schema.json")
