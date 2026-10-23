#!/usr/bin/env python3
"""
generate_deck.py — author one lesson deck (presentations branch).

  author (Sonnet 5.5, structured output) -> build (.pptx) -> validate -> independent review -> repair (bounded)

Reads the lesson data JSON (read-only), docs/presentations/BUILD_MANUAL.md + OVERRIDES.md (the spec),
config/deck_generation.yaml. Writes the deck spec + build log to data/presentations_specs/ and the deck to
data/outputs/presentations/ (gitignored; only _samples/ is committed).

  python3 src/generate_deck.py --data data/outputs/v2/Biology/SS1.1_Cell_Structure/Biology_Cell_Structure_data.json --lesson 2
  python3 src/generate_deck.py ... --count-tokens        # free: prompt size only, no generation
  python3 src/generate_deck.py ... --spec path.json      # skip authoring, rebuild + validate an existing spec
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from deck_spec_schema import SPEC_A, SPEC_B, REVIEW, merge  # noqa: E402

CFG = yaml.safe_load(open(os.path.join(ROOT, "config", "deck_generation.yaml")))
USAGE_LOG = os.path.join(ROOT, "logs", "deck_usage.jsonl")
ABBR = {"Biology": "Bio", "Chemistry": "Chem", "Physics": "Phys"}
PRICE = {"in": 2.0, "out": 10.0, "cache_read": 0.2, "cache_write": 2.5}  # $/MTok, sync (WORKFLOW.md; cache rates assumed)


def load_env():
    cands = [os.path.join(ROOT, ".env"), os.environ.get("DECK_ENV_FILE", ""), "/home/markk/ares/cbe-generation-system/.env"]
    for p in cands:
        if p and os.path.exists(p):
            for line in open(p):
                m = re.match(r"\s*(?:export\s+)?([A-Z_][A-Z0-9_]*)\s*=\s*(.*)\s*$", line)
                if m and m.group(1) not in os.environ:
                    os.environ[m.group(1)] = m.group(2).strip().strip('"').strip("'")
            return p
    return None


def node_json(code):
    return json.loads(subprocess.run(["node", "-e", code], cwd=ROOT, capture_output=True, text=True, check=True).stdout)


def template_labels():
    return node_json("const t=require('./generators/presentations/lib/diagrams.js').TEMPLATES;"
                     "console.log(JSON.stringify(Object.fromEntries(Object.entries(t).map(([k,v])=>[k,Object.keys(v.labels)]))))")


def resources_for(data_path, lesson_no):
    return node_json(f"const d=require({json.dumps(os.path.abspath(data_path))});const l=d.LESSONS.find(x=>x.number=={lesson_no});"
                     "console.log(JSON.stringify(require('./generators/presentations/lib/resources.js').resourceIndex(l).map(r=>({key:r.key,also:r.also,title:r.title,source:r.source,content_type:r.content_type}))))")


def lesson_length(lesson):
    m = re.search(CFG["lesson_length_regex"], str(lesson["duration"]))
    n = int(m.group(1)) if m else None
    if n not in CFG["lesson_lengths_allowed"]:
        raise SystemExit(f"lesson {lesson['number']}: duration '{lesson['duration']}' has no leading 40/80 minutes figure")
    return n


AUTHOR_RULES = """
# YOUR JOB
You are the deck builder described in the manual. Build the deck spec for ONE lesson (JSON, schema enforced). Code turns the spec into the .pptx.
Code does these for you; do NOT write them: footer text, logos, phase colours, fonts, the "CHECK FOR UNDERSTANDING" pill, timer pill styling, the hidden "How these lessons work" slide, the unit map layout (from the SoW lesson titles), the order and bold labels of speaker notes, and every "TIME:" line and "PHASE (N minutes total)" line (computed from your minutes). Never put label words (TIME, DO, SAY...) inside note text.

# HARD RULES
1. FIDELITY (golden rule). The deck teaches this lesson plan. Cover EVERY activity of EVERY phase in the SoW order. Do not add, cut or reorder activities, change names, numbers, materials or the phenomenon. Slide wording should come from the lesson plan's own words.
2. TIME. Unit map 1 minute and goals 1 minute (a quick read-through); the Summary Table slide is done at the end or as homework, so give it 2 minutes at most; give the Safety slide only the time it needs. All integer minutes. unit_map_minutes + goals_minutes + (safety.minutes if rules) + sum(slide.minutes) + summary.minutes MUST equal the lesson length exactly. glance.rows minutes must add up per group to the slide minutes (group "opening" = unit map + goals + safety; "summary" = summary.minutes; phase groups = the sum of that phase's slides). If the SoW's own times overrun the lesson length, trim PROPORTIONALLY (every phase and part loses a similar share; no phase may lose more than about a quarter of its SoW time) WITHOUT cutting an activity, and add a build_log item type "trimmed_time" with the original and new times.
3. FLAG, DO NOT FIX (Overrides). Never silently correct the SoW. A suspected science error, outdated term, inconsistent analogy/label or odd claim stays as the SoW says it on the slide; list it in build_log (science_flag / term_flag / inconsistency) with exact SoW words, what the deck does, and why you think it is a problem. Storyline/sequence problems: build_log type sow_problem. Do not use science_note to talk about the flagged error.
4. NO INVENTED CONTENT (one decision by Mark 2026-10-22): where the SoW names only SOME of the cards/items of a set activity (for example 'a set of 12 feature cards (e.g. ...)'), COMPLETE the set to the stated number, so the activity can run from the slide. Each added card must have a correct answer that follows from facts the lesson itself states or from the diagrams shown, and every added card goes in build_log (type added_fact, card text + its answer) for the teacher to check. For everything else: Never invent resources, links, quantities, concentrations, materials, results or activities. If the SoW omits something the manual wants (quantities per group, a formative check, a practical detail), write only what exists and add build_log type missing_detail (or, for a missing formative check, a slide with title "Formative check to be added" is NOT needed unless the manual requires one: say so in missing_detail). ANSWER KEYS may need established textbook facts the SoW does not state (e.g. a scientist's country or year). Allowed, but each such fact must be listed in build_log type added_fact with where you used it so a teacher can verify it.
5. NEVER SPOIL. Comparison images, expected results, labelled answers and the next lessons' discoveries never appear before students have recorded their own work. Read ALL lessons' titles and overviews (given) so no slide, key word or resource gives away a later lesson. Answer keys live only in the notes. Use do_not_show for "do not show slide X until..." warnings.
6. STUDENT SLIDES vs NOTES. Slides face students: short, plain English, one idea per slide, big text. Aim for at most ~35 words of student text per slide (tables and cards excepted); bullet items under 12 words; table cells short. Everything the teacher needs (what to do, say, look for, answers) goes in notes. A student-facing slide never contains teacher instructions or answers.
7. CHECKS (Manual section 8). Mark check_for_understanding true on slides where learning can go wrong: after predictions, during data collection, after the explanation, at the Driving Question Board, at Model Building. Every such slide needs look_for (specific, with how many students/books to check) and if_then (exact words to say). Set student_task true on any slide where students write, draw, fill in, sort or label: it then needs a model answer in answer_key (worked calculations with units where relevant).
8. PHASES. Slides run Predict, then Observe, then Explain, then Driving Question Board (phase "dqb"), then Model Building, each phase contiguous, in the SoW's order. Use ALL five phases. Predict: individual silent writing first, then pair talk, with a timer slide and a sharing slide ("BEFORE - Our Predictions", no corrections). Observe: record only what is seen/measured; for practicals a demonstration slide with numbered steps then a "Your turn" slide, with a recording format (table with units in headings or drawing guide). Explain: students return to predictions, build the explanation with small questions, name the idea AFTER they understand it, end with a short written explanation (Claim-Evidence-Reasoning or sentence starters). DQB: evidence notes use something seen or measured today; include a class vote. Model Building: ONE model revised in a new colour each lesson, list the revisions, ask for evidence, end with a one-sentence prediction for the next lesson.
9. TIMERS. Put a timer (label + m:ss) on slides with timed silent tasks, as the SoW states them. Timers are not slide minutes.
10. RESOURCES. Use ONLY the resource keys listed in the input. glance.resource_notes needs exactly one entry per listed key (use the primary key shown). match = best_match (fits what students do at the moment of its slot) / preview_first (related but not an exact match: the teacher previews it) / use_later (a good resource that would give an answer away or pre-empt a discovery if shown too early: the note must say WHEN to use it, e.g. "after the card sort" or "as revision after Explain" or "in Lesson 5") / do_not_use (ONLY for resources that are off topic, wrong level or for another subject, with the reason). The lesson plan placed each resource in a phase slot (key like explain.video): a resource in an Explain, Driving Question Board or Model Building slot is normally best_match, preview_first or use_later, not do_not_use; a resource in a Predict or Observe slot that explains the idea is normally use_later (after Explain). Put a key in slide.resources only where it genuinely fits that moment, only for best_match or preview_first, and never where it would spoil a result. Most slides have no resource.
11. DIAGRAMS. When the SoW has students study or label cell diagrams, SHOW them on slides (one diagram slide per cell type, in the SoW's order, so the lesson does not depend on printed cards); never cut a diagram the SoW uses. Use the diagram block with a template name and label names EXACTLY from the template's list (given). Use only labels this lesson's students should see at that moment (do not label what the SoW has not introduced). Caption (diagram.text) must say it is a drawing, e.g. "This is a drawing, not a photograph." Do not use a diagram block if the lesson needs a different drawing: describe the drawing task in text/bullets instead.
12. SAFETY. is_practical true if students or the teacher do a hands-on practical or demonstration with materials. Then safety.rules has at most 5 rules, specific to today's hazards, title "Safety first" style. If not a practical: is_practical false, safety.title "", rules [], minutes 0 and empty notes.
13. LANGUAGE. British spelling (colour, specialisation). "Grade 10", never "Form". Short sentences, common words. Kenyan names/places/foods only where the SoW uses them. Write "Driving Question Board" in full on slides (DQB is fine in notes). No deficit framing.
14. NOTES FIELDS. do: short bullets, include grouping and materials. say: natural spoken lines the teacher can read aloud (no surrounding quote marks). wait_time: e.g. "10 seconds after the question" (empty if none). look_for / if_then: specific. why_this_works: one or two sentences giving the reason behind the strategy. answer_key: one entry per student task. science_note: optional background, empty if none. Name the lesson's common misconception and how the slide addresses it (in why_this_works or look_for). Cold-calling: say who to choose and why. Link back to the anchor phenomenon whenever it fits.
15. ENGAGING VISUALS (students are Grade 10 learners: make every slide inviting, not a wall of text). EVERY lesson must use: at least 2 slides with "tiles" or with icon bullets/numbered rows ("icon_name :: text"); at least 3 illustrations in total (the hero counts) unless the lesson is purely a data lesson; a speech-bubble "question" text block on the slide where students answer the key question. Pick the block that shows the idea best: "tiles" for 3-6 concrete things students will recognise (kitchen features, materials, the scientists, equipment), each item "icon_name :: short text"; "numbered" for steps and routines; "bullets" for key ideas, where items may start with "icon_name :: " to give a colourful icon (use icons that genuinely fit the idea, never decoration for its own sake: only names from icon_names_you_may_use); "text" with style "question" for the question students answer (it is drawn as a speech bubble); "columns" for comparisons and Claim/Evidence/Reasoning; "diagram" for labelled science drawings. ILLUSTRATION blocks: a picture that sets the scene or the phenomenon (the home kitchen, Amina and her finger, the shamba, the lab bench, the classroom): block type "illustration", items = [art_id, scene prompt], text = alt text. At most one illustration per slide, at most 6 per lesson, never for labelled science diagrams (use diagram templates) and never to show a result before students find it. Scene prompt: 20-40 words describing a friendly flat cartoon scene in positive terms (the picture generator ignores negations, so never write 'no people' or 'without text'; say what IS there, e.g. 'an empty wooden bench holding a blue light microscope and three glass slides'). PREFER scenes of objects, places and plants without people: generated people look much younger than Grade 10 learners. Use a person only when the SoW's story needs one (e.g. the girl Amina), then describe one single person. Never include books, boards, signs or labels that would carry writing (a closed book with a pot picture on its cover is fine); a board may be described as 'covered in blank coloured sticky notes'. No injuries (a neat bandage is fine). Kenyan setting where the SoW gives one (jiko, sufuria, mwiko, shamba, sukuma wiki, maize). REUSE an art_id from existing_illustrations_reuse_these_ids_when_they_fit when it fits (keeps characters and scenes consistent across the 12 lessons); invent a new id only for a new scene (snake_case, describing the scene). The title slide needs a hero picture (hero: art_id, prompt, alt, icon) that shows THIS lesson's own subject (its practical, its key idea or its phenomenon scene); reuse an existing id only if that picture really shows this lesson's subject (for example the healing-finger scene for a lesson about the healing cut), never just because it exists; hero.icon is an icon name used if the picture is missing.
16. BLOCKS. A slide's body is a list of blocks, placed top to bottom (text is auto-sized, never below the legible minimum, so keep slides short). type "text": text + style (normal | question = the big question students answer | emphasis = a short coloured line | caption). "bullets"/"numbered": items. "callout": a tinted box; text = the main instruction, items = extra lines such as sentence starters. "table": rows, where the FIRST row is the header row (use an empty string "" for cells students must fill in; units in headings). "cards": items (one per card; for card sorts). "columns": items, each "Heading :: body text" (2-4 columns, e.g. Claim / Evidence / Reasoning, or a colour key). "diagram": template + labels (+ text = caption); template must be "none" for every other block type, labels [] and items [] where unused, rows [] where unused, text "" where unused, style "normal" where unused.
17. SIZE. Slide titles at most 70 characters, subtitle at most 25 words. Tables at most 6 rows x 4 columns. Cards at most 12, each under 12 words. A slide must fit: if a task needs more, split it into two slides (each with its own minutes).
18. UNIT PIECES. lesson_title_short: the short title for the slide (a part of the SoW lesson title, e.g. the part before the colon/subtitle). lesson_oneliner: one plain line for students. purpose/before_class: teacher notes (bullet strings; before_class = a checklist). so_far: one short student-friendly sentence on what the class has done in earlier lessons (from the earlier lesson overviews; empty-safe for lesson 1). goals: 1 to 3, each starting with a verb from the lesson's learning outcomes (State, Compare, Explain...), plain language. key_words: 3 to 6 with plain definitions. They are shown BEFORE Predict, so they must never answer the Predict question or a later discovery (choose vocabulary the lesson goals name, e.g. the theory or model words; leave structure names to be introduced on the slides where students meet them). summary: observe_prompt / learn_prompt / explain_prompt are ONE-LINE hints shown under the fixed headings 'What did I observe?', 'What did I learn?', 'How does this explain the phenomenon?' (do not repeat the headings; follow the lesson's summaryTablePrompt), model answers in answer_*, a next_lesson teaser (just the idea, no results, and WITHOUT the words 'Next lesson:') and 3-5 reflection questions.
19. BUILD LOG. Every flag, trim, added fact, missing detail and SoW problem goes in build_log (slide = slide title or "whole lesson"; sow_says = exact words; deck_does; why). Also record UNIT/lesson inconsistencies you notice (e.g. a unit label that does not match the sub-strand number).
"""

REVIEW_RULES = """
The manual itself REQUIRES these, so they are never 'invented content': the Predict timer slide and sharing slide, the hands-up count where a surprise exists, the class vote at the Driving Question Board on whether the evidence supports a claim, the revise-in-a-new-colour model step and the one-sentence prediction for the next lesson, the Claim-Evidence-Reasoning ending of Explain, the glance and resources slides, safety slides, check-for-understanding slides, and answer keys. Do not report them. Also, a hero picture counts as a spoiler if it shows a comparison or result that students are asked to predict or discover.
FIDELITY BEATS EVERYTHING ELSE. If the SoW itself gives a result away, or contains the odd instruction, the deck must follow the SoW; report that as MINOR (category other, 'for the SoW owner'), never as a major. Report a spoiler as major only when the DECK adds the leak (a slide, key word, label or resource) that the SoW does not.
You are an independent reviewer of a lesson deck spec. You did not write it. Read the SoW lesson (the source of truth), the other lessons' summaries, the resource list and the deck spec. Apply the manual's section 13 builder self-check and section 14 teacher check, and these overrides. Report only real problems, most important first. Be specific: slide title, what is wrong, how to fix.
Look hard for: (1) SPOILERS - any slide, key word, resource or diagram label that gives away a result or a later lesson before students find it; (2) FIDELITY - activities missing, added, reordered or reworded in ways that change the lesson, materials/numbers changed; (3) INVENTED content - quantities, resources, results, facts not in the SoW and not logged as added_fact; (4) SCIENCE - statements, labels, answer keys that are wrong or contradict each other (report them; the deck must not silently fix them: check the build_log flags them); (5) NOTES QUALITY - missing or vague LOOK FOR / IF, SAY lines that are not natural speech, answer keys that miss a student task; (6) STUDENT TEXT - too long, teacher instructions or answers on a student slide, jargon beyond the grade; (7) TIMING - unrealistic times for a large class, mismatch with SoW; (8) SAFETY; (9) RESOURCE matches (do_not_use reasons, a resource placed where it spoils); (10) LANGUAGE ('Form', DQB on slides, US spellings). BRITISH spelling is REQUIRED (colour, labelled, generalised, specialisation): never report British spelling as a problem. (11) TIMING FAIRNESS - report as major any phase that lost more than a quarter of its SoW time when the trim could have been spread, or fixed slides (unit map, goals, summary) that take more than 5 minutes together.
severity major = a teacher would be misled, a result is spoiled, or the lesson no longer matches the SoW; minor = polish. verdict = needs_repair if any major, else pass.
"""


def read(p):
    return open(os.path.join(ROOT, p), encoding="utf8").read()


def system_prompt():
    return ("# DESIGN SPEC (the manual) - follow it exactly\n\n" + read("docs/presentations/BUILD_MANUAL.md") +
            "\n\n# OVERRIDES - these win over the manual where they conflict\n\n" + read("docs/presentations/OVERRIDES.md") +
            "\n\n" + AUTHOR_RULES)


def icon_names():
    return sorted(json.load(open(os.path.join(ROOT, "generators", "presentations", "assets", "emoji", "catalogue.json"))))


def art_catalogue():
    p = os.path.join(ROOT, "data", "presentations_art", "catalogue.json")
    if not os.path.exists(p):
        return {}
    return {k: {"scene": v.get("prompt", ""), "alt": v.get("alt", "")} for k, v in json.load(open(p)).items()}


def drivingQ(u):
    s = str(u.get("drivingQuestion", ""))
    m = re.search(r'DRIVING QUESTION:\s*["\u201c]([^"\u201d]+)["\u201d]', s, re.I)
    return m.group(1).strip() if m else s.split("\n\n")[0]


def payload(data, lesson, resources, tpl_labels):
    L = {k: v for k, v in lesson.items() if k != "resourceLinks"}
    others = [{"number": l["number"], "title": l["title"], "duration": l["duration"], "overview": l["overview"]} for l in data["LESSONS"]]
    u = data["UNIT"]
    return {
        "lesson_length_minutes": lesson_length(lesson),
        "lesson_number": lesson["number"], "lessons_in_sub_strand": len(data["LESSONS"]),
        "meta": data["META"],
        "unit": {"phenomenon": u["phenomenon"], "drivingQuestion": drivingQ(u), "substrand": u["substrand"], "strand": u["strand"],
                 "learningOutcomes": u["learningOutcomes"], "storylineThread": u["storylineThread"]},
        "all_lessons_titles_and_overviews": others,
        "THIS_LESSON_FROM_THE_SOW": L,
        "ares_resources_key_and_details": resources,
        "diagram_templates_and_allowed_labels": tpl_labels,
        "icon_names_you_may_use": icon_names(),
        "existing_illustrations_reuse_these_ids_when_they_fit": art_catalogue(),
    }


def usage_dict(u):
    return {k: getattr(u, k, 0) or 0 for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")}


def cost(u):
    return (u["input_tokens"] * PRICE["in"] + u["output_tokens"] * PRICE["out"] + u["cache_read_input_tokens"] * PRICE["cache_read"] + u["cache_creation_input_tokens"] * PRICE["cache_write"]) / 1e6


def call(client, model, system, user, schema, tag, max_tokens=None):
    params = {
        "model": model, "max_tokens": max_tokens or CFG["max_tokens"],
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": user}],  # str or list of content blocks
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": CFG["effort"], "format": {"type": "json_schema", "schema": schema}},
    }
    t0 = time.time()
    with client.messages.stream(**params) as stream:
        msg = stream.get_final_message()
    u = usage_dict(msg.usage)
    os.makedirs(os.path.dirname(USAGE_LOG), exist_ok=True)
    with open(USAGE_LOG, "a") as f:
        f.write(json.dumps({"tag": tag, "model": model, "seconds": round(time.time() - t0, 1), "stop": msg.stop_reason, "usd_est": round(cost(u), 4), **u}) + "\n")
    print(f"  [{tag}] {msg.stop_reason}  in={u['input_tokens']} cache_r={u['cache_read_input_tokens']} cache_w={u['cache_creation_input_tokens']} out={u['output_tokens']}  ~${cost(u):.3f}  {time.time()-t0:.0f}s")
    if msg.stop_reason != "end_turn":
        raise RuntimeError(f"{tag}: stop_reason={msg.stop_reason}")
    text = next(b.text for b in msg.content if b.type == "text")
    return json.loads(text), u



PART_A = """PART A of 2. Return: unit_map_minutes, goals_minutes, safety_minutes (0 unless the lesson is a practical/demonstration, then the minutes for the Safety slide), summary_minutes, hero (the title-slide picture), ALL the phase slides (Predict, Observe, Explain, Driving Question Board, Model Building), and build_log items you find while writing them. Do NOT make the title, hidden, glance, unit map, goals, safety or summary slides: code and Part B produce those. unit_map_minutes + goals_minutes + safety_minutes + summary_minutes + the sum of slide minutes MUST equal lesson_length_minutes exactly."""

PART_B = """PART B of 2. Part A (the phase slides, their minutes and build-log items so far) is given below. Write everything around it and keep it consistent with Part A: lesson_title_short, lesson_oneliner, purpose, before_class, do_not_show, is_practical (true exactly when safety_minutes > 0), so_far, unit_map_titles (one short title per lesson of the sub-strand, in lesson order, at most 6 words, using ONLY words that appear in that lesson's SoW title, so the unit map shows every lesson without inventing names), goals, key_words, safety (title, rules; empty when not a practical), fixed_notes (speaker notes do / say / why_this_works for the unit map, goals, safety and summary slides: one entry each; the safety entry is empty when not a practical; the code adds TIME, the summary ANSWER KEY from your answer_* fields, and TEACHER REFLECTION from your reflection list), glance, summary, and NEW build_log items only (do not repeat Part A's). glance.rows: the minutes per group must equal EXACTLY the group totals given below (you may split a group into several rows to describe its parts, but each group's rows must sum to its total); the glance has one resource_notes entry for EVERY resource key listed in the input (primary key), including ones no slide uses. glance.materials: per group with quantities only where the SoW gives them; say so in build_log (missing_detail) where it does not. SIZE LIMITS (the glance is one hidden slide): glance.rows at most 8 rows, each 'what' at most 12 words; materials at most 8 items, each at most 10 words; fallback at most 40 words; each resource note at most 20 words."""


def group_minutes(a):
    g = {"opening": a["unit_map_minutes"] + a["goals_minutes"] + a["safety_minutes"], "summary": a["summary_minutes"]}
    for sl in a["slides"]:
        g[sl["phase"]] = g.get(sl["phase"], 0) + sl["minutes"]
    return g


B_PROBLEM = re.compile(r"glance|unit map|goals|key word|title slide|S11|S12|S7\b|L5|summary|Safety|Next lesson|slide [1-6]:|slide [1-6]\b", re.I)


def part_a_of(spec):
    return {"unit_map_minutes": spec["unit_map_minutes"], "goals_minutes": spec["goals_minutes"], "safety_minutes": spec["safety"]["minutes"], "hero": spec.get("hero", {"art_id": "", "prompt": "", "alt": "", "icon": ""}),
            "summary_minutes": spec["summary"]["minutes"], "slides": spec["slides"], "build_log": spec["build_log"]}


def author_spec(client, sysm, pay_text, fix=None, prev=None, tag="", redo="AB"):
    """Two structured calls (A: slides, B: the rest) -> merged spec. Returns (spec, usages)."""
    base = {"type": "text", "text": pay_text, "cache_control": {"type": "ephemeral"}}
    usages = []
    tail = ""
    if fix:
        tail = ("\n\n# PREVIOUS ATTEMPT (your Part A, which has problems)\n" + json.dumps({k: prev[k] for k in ("unit_map_minutes", "goals_minutes", "hero", "slides")} | {"safety_minutes": prev["safety"]["minutes"], "summary_minutes": prev["summary"]["minutes"]}, ensure_ascii=False) +
                "\n\n# PROBLEMS TO FIX (fix every one; change nothing else that is correct; return the COMPLETE corrected Part A)\n" + json.dumps(fix, ensure_ascii=False, indent=1))
    if redo == "B":
        a = part_a_of(prev)
    else:
        a, u = call(client, CFG["model"], sysm, [base, {"type": "text", "text": "Build the deck spec for this lesson only. Follow the manual exactly.\n\n" + PART_A + tail}], SPEC_A, f"author-A {tag}")
        usages.append({"step": "author-A", **u})
    totals = group_minutes(a)
    fixb = ""
    if fix:
        fixb = ("\n\n# PROBLEMS FOUND IN THE PREVIOUS ATTEMPT (fix those that concern Part B: the title/one-liner, so_far, goals, key words, safety, glance, summary, notes; Part A problems are already fixed)\n" + json.dumps(fix, ensure_ascii=False, indent=1))
    b_msg = ("Build the deck spec for this lesson only. Follow the manual exactly.\n\n" + PART_B + fixb +
             "\n\n# GROUP TOTALS the glance rows must match\n" + json.dumps(totals) +
             "\n\n# PART A (your own, final)\n" + json.dumps(a, ensure_ascii=False))
    b, u = call(client, CFG["model"], sysm, [base, {"type": "text", "text": b_msg}], SPEC_B, f"author-B {tag}")
    usages.append({"step": "author-B", **u})
    return merge(a, b), usages


def run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)


def build_and_validate(data_path, lesson_no, spec_path, deck_path):
    problems = []
    rc, out = run(["node", "generators/presentations/build_deck.js", data_path, str(lesson_no), spec_path, deck_path])
    problems += [l.strip()[6:] for l in out.splitlines() if l.strip().startswith("ERROR ")]
    if rc == 2 or not os.path.exists(deck_path):
        problems.append("BUILD CRASH: " + out.strip()[-600:])
        return problems, out
    rc, out2 = run(["node", "scripts/validate_deck.js", deck_path, spec_path, data_path, str(lesson_no), "--json"])
    try:
        for i in json.loads(out2):
            if i["severity"] == "ERROR":
                problems.append(f"{i['id']} slide {i['slide']}: {i['msg']}")
    except Exception:
        problems.append("VALIDATOR CRASH: " + out2.strip()[-600:])
    return problems, out + out2


def paths_for(data, lesson, title_short):
    meta = data["META"]
    sub = os.path.basename(os.path.dirname(os.path.abspath(args_data)))
    abbr = ABBR.get(meta["subject"], meta["subject"][:4])
    sow = re.sub(r"[^A-Za-z0-9]", "", meta["substrand_name"])
    short = re.sub(r"_+", "_", re.sub(r"[^A-Za-z0-9]+", "_", title_short or lesson["title"])).strip("_")
    deck_dir = os.path.join(ROOT, CFG["output_root"], f"Grade{meta['grade']}", meta["subject"], sub)
    spec_dir = os.path.join(ROOT, CFG["spec_root"], meta["subject"], sub)
    return deck_dir, spec_dir, f"{abbr}_G{meta['grade']}_{sow}_L{lesson['number']}_{short}.pptx"


def main():
    global args_data
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--lesson", type=int, required=True)
    ap.add_argument("--spec", help="existing spec JSON: skip authoring")
    ap.add_argument("--reuse-a", help="existing spec JSON: keep its slides (Part A), regenerate Part B only")
    ap.add_argument("--no-review", action="store_true")
    ap.add_argument("--count-tokens", action="store_true")
    ap.add_argument("--repair-rounds", type=int, default=CFG["repair_rounds"])
    a = ap.parse_args()
    args_data = a.data
    data = json.load(open(a.data))
    lesson = next(l for l in data["LESSONS"] if l["number"] == a.lesson)
    resources = resources_for(a.data, a.lesson)
    tpl = template_labels()
    sysm = system_prompt()
    pay = payload(data, lesson, resources, tpl)
    pay_text = "# INPUT (the SoW lesson and everything you may use)\n" + json.dumps(pay, ensure_ascii=False, indent=1)
    user = "Build the deck spec for this lesson only. Follow the manual exactly.\n\n" + pay_text

    client = None
    if a.count_tokens or not a.spec or not a.no_review:  # --spec still reviews (and may repair) unless --no-review
        env = load_env()
        import anthropic
        client = anthropic.Anthropic()
    if a.count_tokens:
        n = client.messages.count_tokens(model=CFG["model"], system=sysm, messages=[{"role": "user", "content": user}])
        print(f"prompt tokens: {n.input_tokens} (system chars {len(sysm)}, user chars {len(user)})")
        return 0

    log = {"lesson": a.lesson, "usage": [], "rounds": []}
    spec, review = None, None
    if a.spec:
        spec = json.load(open(a.spec))
    elif a.reuse_a:
        spec, us = author_spec(client, sysm, pay_text, fix=None, prev=json.load(open(a.reuse_a)), tag=f"L{a.lesson} reuseA", redo="B")
        log["usage"] += us
    else:
        spec, us = author_spec(client, sysm, pay_text, tag=f"L{a.lesson}")
        log["usage"] += us
    deck_dir, spec_dir, fname = paths_for(data, lesson, spec.get("lesson_title_short"))
    os.makedirs(spec_dir, exist_ok=True)
    spec_path = os.path.join(spec_dir, f"L{a.lesson}.spec.json")
    deck_path = os.path.join(deck_dir, fname)

    problems = []
    for rnd in range(a.repair_rounds + 1):
        json.dump(spec, open(spec_path, "w"), indent=1, ensure_ascii=False)
        rc_art, out_art = run([sys.executable, "scripts/make_art.py", spec_path, "--lesson", f"L{a.lesson}"])
        print("  " + out_art.strip().replace("\n", "\n  ")[-600:])
        if rc_art:
            print("ART STEP FAILED: stopping (no repair rounds are paid for a GPU problem). Fix the art step, then rerun with --spec", spec_path)
            log["final_problems"] = ["art step failed"]
            problems = ["art step failed"]
            break
        problems, out = build_and_validate(a.data, a.lesson, spec_path, deck_path)
        majors = []
        if client and not a.no_review and (not problems or rnd == a.repair_rounds):
            rv_user = ("Review this deck spec.\n\n" + json.dumps({"sow": pay, "deck_spec": spec}, ensure_ascii=False))
            review, u = call(client, CFG["reviewer_model"], REVIEW_RULES, rv_user, REVIEW, f"review L{a.lesson} r{rnd}", max_tokens=16000)
            log["usage"].append({"step": f"review{rnd}", **u})
            majors = [f for f in review["findings"] if f["severity"] == "major"]
            print(f"  review: {len(review['findings'])} finding(s), {len(majors)} major, verdict={review['verdict']}")
        log["rounds"].append({"round": rnd, "problems": problems, "review": review})
        print(f"round {rnd}: {len(problems)} validator/layout problem(s), {len(majors)} major review finding(s)")
        for p in problems:
            print("   -", p[:220])
        if not problems and not majors:
            break
        if rnd == a.repair_rounds or not client:
            break
        fix = {"validator_and_layout_problems": problems, "review_major_findings": majors}
        texts = problems + [f["problem"] + " " + f["slide"] for f in majors]
        redo = "B" if texts and all(B_PROBLEM.search(t) for t in texts) else "AB"
        print(f"  repair round {rnd + 1}: regenerating part(s) {redo}")
        spec, us = author_spec(client, sysm, pay_text, fix=fix, prev=spec, tag=f"L{a.lesson} repair{rnd + 1}", redo=redo)
        log["usage"] += us

    log["final_problems"] = problems
    log["review_final"] = review
    log["build_log"] = spec["build_log"]
    log["total_usd_est"] = round(sum(cost({**{"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}, **{k: v for k, v in x.items() if k != "step"}}) for x in log["usage"]), 3)
    json.dump(log, open(os.path.join(spec_dir, f"L{a.lesson}.buildlog.json"), "w"), indent=1, ensure_ascii=False)
    print(f"deck: {deck_path}\nspec: {spec_path}\nestimated API cost this run: ${log['total_usd_est']}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
