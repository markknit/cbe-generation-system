#!/usr/bin/env python3
"""
generate_quiz.py — Quick Check quiz content, one API call per lesson
=====================================================================
Reads a sub-strand's existing <prefix>_data.json (lesson content is NEVER
regenerated or modified) and writes <prefix>_quiz.json next to it. The quiz
lives in its own file because the partner contract (ares-contract.schema.json)
is additionalProperties:false throughout. Schema: generators/data/SCHEMA.md.

Every lesson's questions are validated (scripts/validate_quiz.py) before they
are saved; choices are then shuffled with a seed derived from the lesson, so
answer letters are balanced across the corpus and reproducible.

Usage (grade-aware: pick files by path, or --all [--grade N]):
  python3 src/generate_quiz.py --live PATH/X_data.json [--lessons 1,4] [--model M]
  python3 src/generate_quiz.py --batch --all --grade 10        # submit; checkpointed
  python3 src/generate_quiz.py --collect [--wait]               # collect pending batches
Options: --force (regenerate lessons that already have a valid quiz),
         --out-suffix S (write <prefix>_quiz<S>.json, e.g. for model comparisons)
Settings: config/quiz_generation.yaml.
"""
import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import random
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import validate_quiz as vq  # noqa: E402

STATE_DIR = os.path.join(ROOT, "logs", "quiz_generation")
BATCH_STATE = os.path.join(STATE_DIR, "batches.json")
USAGE_LOG = os.path.join(STATE_DIR, "usage.jsonl")

SYSTEM = """You write short multiple-choice "Quick Check" quizzes for Kenyan CBE lesson plans \
(KICD competence-based curriculum). A teacher uses each question at a specific point in ONE \
lesson to check understanding. The quiz is printed or projected on its own, with no slides \
around it.

Rules:
1. Write {qmin} to {qmax} questions. Use the lower end for short or simple lessons.
2. Ground every question ONLY in the lesson content provided: its learning outcomes and \
its framework activities. Never test anything the lesson has not yet taught, including \
ideas from later lessons in the sequence.
3. Each question has exactly 4 choices and exactly one unambiguously correct answer. \
Do not use "all of the above", "none of the above" or combinations like "A and B".
4. Every question must be self-contained: include every number, name and piece of context \
a student needs. Never refer to "the diagram", "the slide", "the video", "the shadow" or \
anything the student cannot see in the question itself.
5. Distractors should be real misconceptions, ideally the ones named in the lesson's \
formative assessment or teacher moves text. They must be plausible and clearly wrong.
6. "phase" is the lesson-plan phase the question follows: predict, observe, explain, dqb, \
model, or end (after the whole lesson). "placement" names the specific activity in THIS \
lesson plan that the question follows, using the lesson's own wording so a teacher can \
find it (e.g. "Part B: shoe-pressure investigation").
7. "rationale" is teacher-facing, one or two sentences on why the answer is correct. For \
calculations, show the working. Never refer to answer letters or positions: the choices \
are shuffled after you write them.
8. For every question whose correct answer is a calculated number, set "check" to a plain \
arithmetic expression (Python syntax; sqrt, sin/cos/tan in degrees, log10 allowed) that \
evaluates to the number in the correct choice. Otherwise set "check" to "".
9. Use Kenyan context and English spelling as the lesson does. Keep language simple and \
clear for Grade {grade} students.
{anchor}"""

ANCHOR_RULE = """10. This is the ANCHOR lesson: the phenomenon is deliberately left unexplained. \
Questions may check what students observed, predicted or wondered, but must NOT state or \
reward the scientific explanation. Where a question asks why something happens, the correct \
answer may be that it has not been explained yet."""

QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "choices": {"type": "array", "items": {"type": "string"}},
                    "correctIndex": {"type": "integer", "enum": [0, 1, 2, 3]},
                    "rationale": {"type": "string"},
                    "phase": {"type": "string",
                              "enum": ["predict", "observe", "explain", "dqb", "model", "end"]},
                    "placement": {"type": "string"},
                    "check": {"type": "string"},
                },
                "required": ["prompt", "choices", "correctIndex", "rationale", "phase", "placement", "check"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["questions"],
    "additionalProperties": False,
}


def load_cfg():
    return vq.load_config()


def lesson_payload(data: dict, lesson: dict, cfg: dict) -> str:
    unit = data.get("UNIT") or {}
    total = len(data["LESSONS"])
    phase_map = cfg["phase_map"]
    fw = []
    for f in lesson.get("framework", []):
        fw.append({
            "phase": phase_map.get(f.get("phase"), f.get("phase")),
            "learnerExperience": f.get("learnerExperience", ""),
            "teacherMoves": f.get("teacherMoves", ""),
            "sensemakingStrategy": f.get("sensemakingStrategy", ""),
            "formativeAssessment": f.get("formativeAssessment", ""),
        })
    body = {
        "subject": data["META"]["subject"],
        "grade": data["META"]["grade"],
        "subStrand": f'{data["META"]["substrand_id"]} {data["META"]["substrand_name"]}',
        "anchoringPhenomenon": unit.get("phenomenon", ""),
        "lessonNumber": lesson["number"],
        "lessonsInSequence": total,
        "lessonTitle": lesson["title"],
        "overview": lesson.get("overview", ""),
        "learningOutcomes": {k: v for k, v in (lesson.get("slo") or {}).items() if k != "safetyNotes"},
        "framework": fw,
    }
    return ("Write the Quick Check quiz for this lesson. Lesson content (JSON):\n\n"
            + json.dumps(body, ensure_ascii=False, indent=1))


def is_anchor(lesson: dict) -> bool:
    return lesson["number"] == 1 or "anchor" in lesson.get("title", "").lower()


def request_params(data, lesson, cfg, model):
    system = SYSTEM.format(qmin=cfg["questions_min"], qmax=cfg["questions_max"],
                           grade=data["META"]["grade"], anchor=ANCHOR_RULE if is_anchor(lesson) else "")
    return {
        "model": model,
        "max_tokens": cfg["max_tokens"],
        "system": system,
        "messages": [{"role": "user", "content": lesson_payload(data, lesson, cfg)}],
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": cfg["effort"],
                          "format": {"type": "json_schema", "schema": QUIZ_SCHEMA}},
    }


def shuffle_choices(quiz: list, seed: str) -> list:
    """Seeded shuffle per question: balanced answer letters, reproducible."""
    out = []
    for i, q in enumerate(quiz):
        rng = random.Random(hashlib.sha256(f"{seed}|{i}".encode()).hexdigest())
        order = list(range(len(q["choices"])))
        rng.shuffle(order)
        q = dict(q)
        q["correctIndex"] = order.index(q["correctIndex"])
        q["choices"] = [q["choices"][j] for j in order]
        out.append(q)
    return out


def finalize(raw_text: str, data: dict, lesson: dict, cfg: dict):
    """Parse model output, validate, shuffle. Returns (quiz, errors, warnings)."""
    quiz = json.loads(raw_text)["questions"]
    for q in quiz:
        if not q.get("check"):
            q.pop("check", None)
    errs, warns = vq.validate_lesson_quiz(quiz, lesson, cfg)
    quiz = shuffle_choices(quiz, f'{data["META"]["filePrefix"]}|G{data["META"]["grade"]}|L{lesson["number"]}')
    return quiz, errs, warns


def quiz_path(data_path: str, suffix: str = "") -> str:
    return data_path.replace("_data.json", f"_quiz{suffix}.json")


def load_quiz_file(path: str, data: dict) -> dict:
    if os.path.exists(path):
        return json.load(open(path))
    M = data["META"]
    return {"quizSchemaVersion": "1.0.0",
            "meta": {"subject": M["subject"], "grade": M["grade"], "substrandId": M["substrand_id"],
                     "substrandName": M["substrand_name"], "filePrefix": M["filePrefix"]},
            "lessons": []}


def save_lesson(path: str, data: dict, lesson: dict, quiz: list, model: str, usage: dict):
    qf = load_quiz_file(path, data)
    qf["lessons"] = [L for L in qf["lessons"] if L["number"] != lesson["number"]]
    qf["lessons"].append({"number": lesson["number"], "title": lesson["title"], "model": model,
                          "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                          "quiz": quiz})
    qf["lessons"].sort(key=lambda L: L["number"])
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(qf, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def _save_failure(tag, model, attempt, msg, errs):
    """Keep rejected model output for diagnosis (logs/quiz_generation/failures/)."""
    d = os.path.join(STATE_DIR, "failures")
    os.makedirs(d, exist_ok=True)
    text = next((b.text for b in msg.content if b.type == "text"), "")
    name = f"{tag.replace(' ', '_')}_{model}_a{attempt}.json"
    with open(os.path.join(d, name), "w") as f:
        json.dump({"errors": errs, "stop_reason": msg.stop_reason, "output": text}, f, ensure_ascii=False, indent=1)


def log_usage(entry: dict):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(USAGE_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def usage_dict(u) -> dict:
    keys = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
    return {k: getattr(u, k, 0) or 0 for k in keys}


def select_files(args) -> list[str]:
    if args.all:
        files = glob.glob(os.path.join(ROOT, "data", "outputs", "v2", "**", "*_data.json"), recursive=True)
    else:
        files = [os.path.abspath(p) for p in args.paths]
    if args.grade is not None:
        files = [f for f in files if json.load(open(f))["META"]["grade"] == args.grade]
    return sorted(files)


def pending_lessons(data_path, data, args):
    wanted = {int(x) for x in args.lessons.split(",")} if args.lessons else None
    done = set()
    qp = quiz_path(data_path, args.out_suffix)
    if os.path.exists(qp) and not args.force:
        done = {L["number"] for L in json.load(open(qp))["lessons"]}
    return [L for L in data["LESSONS"] if (wanted is None or L["number"] in wanted) and L["number"] not in done]


def run_live(client, files, args, cfg, model):
    failed = []
    for dp in files:
        data = json.load(open(dp))
        for lesson in pending_lessons(dp, data, args):
            tag = f'{data["META"]["filePrefix"]} L{lesson["number"]}'
            for attempt in (1, 2):
                t0 = time.time()
                with client.messages.stream(**request_params(data, lesson, cfg, model)) as stream:
                    msg = stream.get_final_message()
                u = usage_dict(msg.usage)
                log_usage({"mode": "live", "model": model, "lesson": tag, "attempt": attempt,
                           "seconds": round(time.time() - t0, 1), **u})
                if msg.stop_reason != "end_turn":
                    errs, quiz, warns = [f"stop_reason={msg.stop_reason}"], None, []
                else:
                    text = next(b.text for b in msg.content if b.type == "text")
                    quiz, errs, warns = finalize(text, data, lesson, cfg)
                if not errs:
                    save_lesson(quiz_path(dp, args.out_suffix), data, lesson, quiz, model, u)
                    print(f"  OK   {tag}: {len(quiz)} questions  in={u['input_tokens']} out={u['output_tokens']}"
                          + (f"  ({len(warns)} warning(s))" if warns else ""))
                    for w in warns:
                        print(f"       WARN {w}")
                    break
                print(f"  FAIL {tag} attempt {attempt}: {'; '.join(errs)[:300]}")
                _save_failure(tag, model, attempt, msg, errs)
            else:
                failed.append(tag)
    return failed


def run_batch_submit(client, files, args, cfg, model):
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    reqs, index = [], {}
    for dp in files:
        data = json.load(open(dp))
        for lesson in pending_lessons(dp, data, args):
            cid = hashlib.sha1(f"{dp}|{lesson['number']}|{args.out_suffix}".encode()).hexdigest()[:24]
            index[cid] = {"data_path": os.path.relpath(dp, ROOT), "lesson": lesson["number"],
                          "out_suffix": args.out_suffix}
            reqs.append(Request(custom_id=cid, params=MessageCreateParamsNonStreaming(
                **request_params(data, lesson, cfg, model))))
    if not reqs:
        print("Nothing to submit: every selected lesson already has a quiz (use --force to redo).")
        return
    batch = client.messages.batches.create(requests=reqs)
    os.makedirs(STATE_DIR, exist_ok=True)
    state = json.load(open(BATCH_STATE)) if os.path.exists(BATCH_STATE) else {}
    state[batch.id] = {"model": model, "submitted": dt.datetime.now(dt.timezone.utc).isoformat(),
                       "requests": index, "collected": False}
    json.dump(state, open(BATCH_STATE, "w"), indent=1)
    print(f"Submitted batch {batch.id}: {len(reqs)} lesson(s). Collect with: python3 src/generate_quiz.py --collect --wait")


def run_collect(client, args, cfg):
    if not os.path.exists(BATCH_STATE):
        print("No batches recorded.")
        return []
    state = json.load(open(BATCH_STATE))
    failed = []
    for bid, st in state.items():
        if st["collected"]:
            continue
        b = client.messages.batches.retrieve(bid)
        while args.wait and b.processing_status != "ended":
            print(f"  {bid}: {b.processing_status} {b.request_counts}")
            time.sleep(60)
            b = client.messages.batches.retrieve(bid)
        if b.processing_status != "ended":
            print(f"  {bid}: {b.processing_status} (not ready)")
            continue
        retry = []
        for r in client.messages.batches.results(bid):
            meta = st["requests"][r.custom_id]
            dp = os.path.join(ROOT, meta["data_path"])
            data = json.load(open(dp))
            lesson = next(L for L in data["LESSONS"] if L["number"] == meta["lesson"])
            tag = f'{data["META"]["filePrefix"]} L{lesson["number"]}'
            if r.result.type != "succeeded":
                print(f"  FAIL {tag}: batch result {r.result.type}")
                retry.append(tag)
                continue
            msg = r.result.message
            u = usage_dict(msg.usage)
            log_usage({"mode": "batch", "batch": bid, "model": st["model"], "lesson": tag, **u})
            text = next((b_.text for b_ in msg.content if b_.type == "text"), "")
            try:
                quiz, errs, warns = finalize(text, data, lesson, cfg)
            except (ValueError, KeyError) as e:
                quiz, errs, warns = None, [f"unparseable output: {e}"], []
            if errs:
                print(f"  FAIL {tag}: {'; '.join(errs)[:300]}")
                retry.append(tag)
                continue
            save_lesson(quiz_path(dp, meta.get("out_suffix", "")), data, lesson, quiz, st["model"], u)
        st["collected"] = True
        st["failed"] = retry
        json.dump(state, open(BATCH_STATE, "w"), indent=1)
        print(f"  {bid}: collected; {len(retry)} lesson(s) need a re-run (they have no quiz yet, so a"
              f" plain re-submit picks them up)")
        failed += retry
    return failed


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--batch", action="store_true")
    mode.add_argument("--collect", action="store_true")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--grade", type=int)
    ap.add_argument("--lessons")
    ap.add_argument("--model")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--wait", action="store_true")
    ap.add_argument("--out-suffix", default="")
    args = ap.parse_args()

    import anthropic
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(ROOT, ".env"))
    except ImportError:
        pass
    client = anthropic.Anthropic()
    cfg = load_cfg()
    model = args.model or cfg["model"]
    if args.collect:
        failed = run_collect(client, args, cfg)
    else:
        files = select_files(args)
        if not files:
            sys.exit("No _data.json files selected (give paths, or --all [--grade N]).")
        if args.batch:
            run_batch_submit(client, files, args, cfg, model)
            return
        failed = run_live(client, files, args, cfg, model)
    if failed:
        print(f"{len(failed)} lesson(s) without a valid quiz: {', '.join(failed[:20])}")
        sys.exit(1)


if __name__ == "__main__":
    main()
