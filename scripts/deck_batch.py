#!/usr/bin/env python3
"""
deck_batch.py - batch-round deck generation with incremental rebuild (presentations branch).

Runs many lessons through the same pipeline as src/generate_deck.py, but each model stage is ONE Message Batch
for all lessons (50% price), and local steps (art, build, validate) run between batches:

  author-A -> author-B -> [art, build, validate] -> review -> (repair: A and/or B -> build ...) -> done

State lives in a run folder (resumable at any point; `status` shows where every lesson is).

  python3 scripts/deck_batch.py plan   --run RUN --data DATA.json [--lessons 1-12] [--out-tag TAG] [--skip-art]
  python3 scripts/deck_batch.py step   --run RUN        # submit the next batch / collect finished ones / run local steps
  python3 scripts/deck_batch.py run    --run RUN [--poll 60]   # step in a loop until every lesson is done
  python3 scripts/deck_batch.py status --run RUN

Incremental rebuild: a lesson is skipped when its INPUT HASH (lesson payload + system prompt + schemas + model/effort)
matches the hash stored beside its last good spec. Change the lesson data, the manual or the config and only the
affected lessons are rebuilt. `--force` ignores the hash.

--out-tag writes decks/specs under data/outputs/presentations_<TAG> and data/presentations_specs_<TAG>, so experiments
never overwrite the pilot decks.
"""
import argparse
import hashlib
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import generate_deck as gd  # noqa: E402
import openai_engine as oe  # noqa: E402
from deck_spec_schema import SPEC_A, SPEC_B, REVIEW, merge  # noqa: E402

RUNS = os.path.join(ROOT, "data", "presentations_specs", "_batch")
BATCH_DISCOUNT = 0.5
SCHEMA_VERSION = "deck-batch-1"


def run_dir(run):
    return os.path.join(RUNS, run)


def load(run):
    return json.load(open(os.path.join(run_dir(run), "state.json")))


def save(run, st):
    p = os.path.join(run_dir(run), "state.json")
    json.dump(st, open(p + ".tmp", "w"), indent=1, ensure_ascii=False)
    os.replace(p + ".tmp", p)


def jkey(data, lesson):
    return f"{os.path.basename(os.path.dirname(data))}_L{lesson}"


def cid(key, stage):
    import re
    return re.sub(r"[^A-Za-z0-9_-]", "-", f"{key}__{stage}")[:64]


def quiz_hash(meta, ln):
    """Quiz links are placed at build time from data/quiz_registry.json, so a quiz version or ID change must rebuild the deck."""
    import quiz_links as ql
    try:
        reg = json.load(open(ql.REG))["quizzes"].get(ql.quiz_id({"subject": meta["subject"], "grade": meta["grade"], "substrandId": meta["substrand_id"]}, ln))
    except FileNotFoundError:
        reg = None
    return json.dumps([reg["version"], [q["id"] for q in reg["questions"]]] if reg else None)


def input_hash(sysm, pay_text, model, effort, extra=""):
    h = hashlib.sha256()
    for part in (SCHEMA_VERSION, sysm, pay_text, model, effort, extra, gd.REVIEW_RULES, gd.PART_A, gd.PART_B,
                 json.dumps([SPEC_A, SPEC_B, REVIEW], sort_keys=True), str(gd.CFG["repair_rounds"])):
        h.update(part.encode("utf8")); h.update(b"\0")
    return h.hexdigest()[:16]


def paths(job):
    gd.args_data = job["data"]
    data = json.load(open(job["data"]))
    lesson = next(l for l in data["LESSONS"] if l["number"] == job["lesson"])
    return data, lesson


def dirs_for(job, title_short):
    data, lesson = paths(job)
    tag = job.get("out_tag")
    saved = dict(gd.CFG)
    if tag:
        gd.CFG["output_root"] = gd.CFG["output_root"] + "_" + tag
        gd.CFG["spec_root"] = gd.CFG["spec_root"] + "_" + tag
    try:
        return gd.paths_for(data, lesson, title_short)
    finally:
        gd.CFG.clear(); gd.CFG.update(saved)


def parse_lessons(spec, n):
    out = set()
    for part in spec.split(","):
        if "-" in part:
            x, y = part.split("-"); out |= set(range(int(x), int(y) + 1))
        elif part:
            out.add(int(part))
    return sorted(v for v in out if 1 <= v <= n)


def plan(a):
    os.makedirs(run_dir(a.run), exist_ok=True)
    p = os.path.join(run_dir(a.run), "state.json")
    st = json.load(open(p)) if os.path.exists(p) else {"jobs": {}, "batches": {}, "config": {}}
    # author_engine "openai" authors A/B with OpenAI (--model, e.g. gpt-6.1-sol); the REVIEWER always stays on Anthropic
    # (reviewer_model from config) so findings are comparable across arms.
    st["config"] = {"model": a.model or gd.CFG["model"], "reviewer_model": gd.CFG["reviewer_model"],
                    "author_engine": a.engine, "price_mult": a.price_mult, "reviewer_effort": gd.CFG["effort"],
                    "effort": a.effort or gd.CFG["effort"], "cache_ttl": a.cache_ttl, "skip_art": a.skip_art,
                    "repair_rounds": a.repair_rounds if a.repair_rounds is not None else gd.CFG["repair_rounds"]}
    sysm = gd.system_prompt()
    tpl = gd.template_labels()
    for dp in a.data:
        data = os.path.abspath(dp)
        d = json.load(open(data))
        picked = [x.split(":", 1)[1] for x in a.pick if x.split(":", 1)[0] in data]
        if a.pick and not picked:
            continue
        for ln in (parse_lessons(",".join(picked), len(d["LESSONS"])) if picked else parse_lessons(a.lessons, len(d["LESSONS"])) if a.lessons else range(1, len(d["LESSONS"]) + 1)):
            key = jkey(data, ln)
            job = {"data": data, "lesson": ln, "out_tag": a.out_tag, "stage": "A", "round": 0, "fix": None, "redo": "AB",
                   "usage": [], "rounds": [], "key": key}
            lesson = next(l for l in d["LESSONS"] if l["number"] == ln)
            pay = gd.payload(d, lesson, gd.resources_for(data, ln), tpl)
            pay_text = "# INPUT (the SoW lesson and everything you may use)\n" + json.dumps(pay, ensure_ascii=False, indent=1)
            stable = {k: v for k, v in pay.items() if k != "existing_illustrations_reuse_these_ids_when_they_fit"}  # catalogue grows as art is made
            job["hash"] = input_hash(sysm, json.dumps(stable, sort_keys=True), st["config"]["model"], st["config"]["effort"], quiz_hash(d["META"], ln))
            # incremental: unchanged inputs and a clean previous result -> skip
            if not a.force:
                sp = prior_spec_dir(job)
                hp = os.path.join(sp, f"L{ln}.inputhash") if sp else None
                if hp and os.path.exists(hp) and open(hp).read().strip() == job["hash"]:
                    job["stage"] = "done"; job["note"] = "unchanged (input hash matches)"
            st["jobs"][key] = job
    save(a.run, st)
    c = {}
    for j in st["jobs"].values():
        c[j["stage"]] = c.get(j["stage"], 0) + 1
    print(f"planned {len(st['jobs'])} lesson(s): {c}  run={a.run}")


def prior_spec_dir(job):
    data, lesson = paths(job)
    meta = data["META"]
    sub = os.path.basename(os.path.dirname(job["data"]))
    root = gd.CFG["spec_root"] + (("_" + job["out_tag"]) if job.get("out_tag") else "")
    p = os.path.join(ROOT, root, meta["subject"], sub)
    return p if os.path.isdir(p) else None


def pay_text_of(job, sysm_tpl):
    data, lesson = paths(job)
    pay = gd.payload(data, lesson, gd.resources_for(job["data"], job["lesson"]), sysm_tpl)
    return pay, "# INPUT (the SoW lesson and everything you may use)\n" + json.dumps(pay, ensure_ascii=False, indent=1)


def client():
    gd.load_env()
    import anthropic
    return anthropic.Anthropic()


def usd(u, batch=True):
    return gd.cost(u) * (BATCH_DISCOUNT if batch else 1)


def build_requests(st, stage_names):
    """Requests for every job waiting on one of the given model stages."""
    sysm = gd.system_prompt()
    tpl = gd.template_labels()
    cfg = st["config"]
    reqs, meta = [], {}
    for key, job in st["jobs"].items():
        if job["stage"] not in stage_names:
            continue
        pay, pay_text = pay_text_of(job, tpl)
        stage = job["stage"]
        tag = f"{stage}-r{job['round']}"
        oa = cfg.get("author_engine") == "openai" and stage in ("A", "B")
        if stage == "A":
            user, schema, nm = gd.msgs_a(pay_text, job["fix"], job.get("spec")), SPEC_A, "spec_a"
        elif stage == "B":
            user, schema, nm = gd.msgs_b(pay_text, job["a"], job["fix"]), SPEC_B, "spec_b"
        elif stage == "R":
            rv_user = "Review this deck spec.\n\n" + json.dumps({"sow": pay, "deck_spec": job["spec"]}, ensure_ascii=False)
        else:
            continue
        if oa:
            params = oe.responses_body(cfg["model"], sysm, user, schema, nm, effort=cfg["effort"], max_output_tokens=gd.CFG["max_tokens"])
        elif stage == "R":
            params = gd.call_params(cfg["reviewer_model"], gd.REVIEW_RULES, rv_user, REVIEW, max_tokens=16000, effort=cfg["reviewer_effort"], cache_ttl=cfg["cache_ttl"])
        else:
            params = gd.call_params(cfg["model"], sysm, user, schema, effort=cfg["effort"], cache_ttl=cfg["cache_ttl"])
        c = cid(key, tag)
        reqs.append({"custom_id": c, "params": params})
        meta[c] = {"key": key, "stage": stage, "engine": "openai" if oa else "anthropic"}
    return reqs, meta


def submit(run, st, stage_names, label):
    reqs, meta = build_requests(st, stage_names)
    if not reqs:
        return 0
    engine = next(iter(meta.values()))["engine"]
    if engine == "openai":
        bid = oe.create_batch([{"custom_id": r["custom_id"], "body": r["params"]} for r in reqs])
    else:
        bid = client().messages.batches.create(requests=reqs).id
    st["batches"][bid] = {"label": label, "meta": meta, "submitted": time.time(), "state": "in_progress", "n": len(reqs), "engine": engine}
    for m in meta.values():
        st["jobs"][m["key"]]["stage"] = st["jobs"][m["key"]]["stage"] + "*"  # in flight
    save(run, st)
    print(f"submitted {engine} batch {bid}: {label}, {len(reqs)} request(s)")
    return len(reqs)


def parse_msg(msg):
    if msg.stop_reason != "end_turn":
        raise RuntimeError(f"stop_reason={msg.stop_reason}")
    text = next(b.text for b in msg.content if b.type == "text")
    return json.loads(text), gd.usage_dict(msg.usage)


def log_usage(tag, model, u, stop, engine="anthropic"):
    os.makedirs(os.path.dirname(gd.USAGE_LOG), exist_ok=True)
    with open(gd.USAGE_LOG, "a") as f:
        f.write(json.dumps({"tag": tag, "model": model, "engine": engine, "batch": True, "stop": stop, "usd_est": u["usd"], **u}) + "\n")


def collect(run, st):
    done_any = False
    for bid, b in st["batches"].items():
        if b["state"] != "in_progress":
            continue
        engine = b.get("engine", "anthropic")
        if engine == "openai":
            bb = oe.retrieve_batch(bid)
            if bb["status"] in ("validating", "in_progress", "finalizing", "cancelling"):
                print(f"  batch {bid} ({b['label']}): {bb['status']} {bb.get('request_counts')}")
                continue
            results = ((c, resp, err) for c, resp, err in oe.batch_results(bb))
        else:
            cl = client()
            bb = cl.messages.batches.retrieve(bid)
            if bb.processing_status != "ended":
                c = bb.request_counts
                print(f"  batch {bid} ({b['label']}): {bb.processing_status} processing={c.processing} ok={c.succeeded} err={c.errored}")
                continue
            results = ((r.custom_id, r.result.message if r.result.type == "succeeded" else None, None if r.result.type == "succeeded" else f"batch result {r.result.type}") for r in cl.messages.batches.results(bid))
        seen = set()
        for custom, payload_, err in results:
            seen.add(custom)
            m = b["meta"][custom]
            job = st["jobs"][m["key"]]
            stage = m["stage"]
            job["stage"] = stage  # leave "in flight"
            if err:
                job["stage"] = "failed"; job["error"] = f"{stage}: {err}"
                continue
            try:
                if engine == "openai":
                    obj, u = oe.parse_response(payload_)
                    u["usd"] = round(oe.cost(u, batch=True), 4)
                else:
                    obj, u = parse_msg(payload_)
                    u["usd"] = round(usd(u) * (1 if stage == "R" else st["config"].get("price_mult", 1.0)), 4)
            except Exception as e:  # noqa: BLE001
                job["stage"] = "failed"; job["error"] = f"{stage}: {e}"
                continue
            model = st["config"]["reviewer_model" if stage == "R" else "model"]
            job["usage"].append({"step": {"A": "author-A", "B": "author-B", "R": f"review{job['round']}"}[stage], "engine": engine, **u})
            log_usage(f"batch {stage} {job['key']} r{job['round']}", model, u, "end_turn", engine)
            if stage == "A":
                job["a"] = obj; job["stage"] = "B"
            elif stage == "B":
                job["spec"] = merge(job["a"], obj); job["stage"] = "build" if st["config"].get("skip_art") else "art"
            else:
                job["review"] = obj; job["stage"] = "judge"
        for custom, m in b["meta"].items():  # a request missing from the results must not hang forever
            if custom not in seen and st["jobs"][m["key"]]["stage"].endswith("*"):
                st["jobs"][m["key"]]["stage"] = "failed"; st["jobs"][m["key"]]["error"] = f"{m['stage']}: no result returned"
        b["state"] = "ended"
        done_any = True
        save(run, st)
    return done_any


def write_spec(job):
    spec = job["spec"]
    deck_dir, spec_dir, fname = dirs_for(job, spec.get("lesson_title_short"))
    os.makedirs(spec_dir, exist_ok=True); os.makedirs(deck_dir, exist_ok=True)
    sp = os.path.join(spec_dir, f"L{job['lesson']}.spec.json")
    json.dump(spec, open(sp, "w"), indent=1, ensure_ascii=False)
    return sp, os.path.join(deck_dir, fname)


def art_command(sp, lesson):
    override = os.environ.get("DECK_ART_CMD")  # test hook: a stub that takes the spec path and lesson tag
    base = override.split() if override else [sys.executable, "scripts/make_art.py"]
    return base + [sp, "--lesson", f"L{lesson}"]


def make_art_for(job):
    sp, _ = write_spec(job)
    return gd.run(art_command(sp, job["lesson"]))


def art_worker(run, st, lock, stop):
    """One background worker for the single GPU: makes the pictures while the next batches are processing."""
    while not stop.is_set():
        with lock:
            job = next((j for j in st["jobs"].values() if j["stage"] == "art"), None)
            if job:
                job["stage"] = "art~"
        if not job:
            time.sleep(3)
            continue
        t0 = time.time()
        rc, out = make_art_for(job)
        with lock:
            if rc:
                job["stage"] = "failed"; job["error"] = "art step failed: " + out.strip()[-300:]
            else:
                job["stage"] = "build"
            job["art_seconds"] = round(time.time() - t0, 1)
            print(f"  {job['key']}: art {'FAILED' if rc else 'done'} in {job['art_seconds']}s", flush=True)
            save(run, st)


def local_steps(run, st, inline_art=True):
    """art (inline mode only), build/validate for jobs at 'build'; then decide review / repair / done for 'judge'."""
    cfg = st["config"]
    for key, job in st["jobs"].items():
        if job["stage"] == "art" and inline_art:
            rc, out = make_art_for(job)
            if rc:
                job["stage"] = "failed"; job["error"] = "art step failed: " + out.strip()[-300:]
            else:
                job["stage"] = "build"
        if job["stage"] == "build":
            sp, dp = write_spec(job)
            problems, _ = gd.build_and_validate(job["data"], job["lesson"], sp, dp)
            if cfg.get("skip_art"):  # no pictures were made on purpose: "not generated yet" is not a deck defect
                problems = [x for x in problems if "has not been generated" not in x]
            job.update(spec_path=sp, deck_path=dp, problems=problems)
            last = job["round"] >= cfg["repair_rounds"]
            if problems and not last:
                job["rounds"].append({"round": job["round"], "problems": problems, "review": None})
                start_repair(job, problems, [])
            else:
                job["stage"] = "R"  # review (no problems, or the last round)
            print(f"  {key}: r{job['round']} {len(problems)} validator/layout problem(s) -> stage {job['stage']}", flush=True)
        elif job["stage"] == "judge":
            review = job["review"]
            majors = [f for f in review["findings"] if f["severity"] == "major"]
            job["rounds"].append({"round": job["round"], "problems": job["problems"], "review": review})
            last = job["round"] >= cfg["repair_rounds"]
            print(f"  {key}: review {len(review['findings'])} finding(s), {len(majors)} major", flush=True)
            if (job["problems"] or majors) and not last:
                start_repair(job, job["problems"], majors)
            else:
                finish(job, review)
        save(run, st)


def start_repair(job, problems, majors):
    fix = {"validator_and_layout_problems": problems, "review_major_findings": majors}
    texts = problems + [f["problem"] + " " + f["slide"] for f in majors]
    redo = "B" if texts and all(gd.B_PROBLEM.search(t) for t in texts) else "AB"
    job.update(fix=fix, redo=redo, round=job["round"] + 1)
    prev_spec = job["spec"]
    if redo == "B":
        job["a"] = gd.part_a_of(prev_spec); job["spec"] = prev_spec; job["stage"] = "B"
    else:
        job["spec"] = prev_spec; job["stage"] = "A"  # msgs_a gets fix + the previous spec


def finish(job, review):
    spec_dir = os.path.dirname(job["spec_path"])
    n = job["lesson"]
    total = round(sum(x.get("usd", 0) for x in job["usage"]), 3)
    log = {"lesson": n, "usage": job["usage"], "rounds": job["rounds"], "final_problems": job["problems"], "review_final": review,
           "build_log": job["spec"]["build_log"], "total_usd_est": total, "batch": True, "input_hash": job["hash"],
           "model": None}
    json.dump(log, open(os.path.join(spec_dir, f"L{n}.buildlog.json"), "w"), indent=1, ensure_ascii=False)
    majors = [f for f in review["findings"] if f["severity"] == "major"]
    job["stage"] = "done"; job["total_usd"] = total; job["clean"] = not job["problems"] and not majors
    if job["clean"]:  # the hash marks a good result, so a later `plan` can skip this lesson
        open(os.path.join(spec_dir, f"L{n}.inputhash"), "w").write(job["hash"])


def status(st):
    c = {}
    for j in st["jobs"].values():
        c[j["stage"]] = c.get(j["stage"], 0) + 1
    spend = sum(j.get("total_usd", 0) for j in st["jobs"].values())
    print("stages:", c, f"| finished-lesson spend so far ${spend:.2f}")
    for k, j in st["jobs"].items():
        extra = j.get("error") or j.get("note") or ("clean" if j.get("clean") else ("problems left" if j["stage"] == "done" else ""))
        print(f"  {k:48s} {j['stage']:7s} round {j['round']} {extra}")


def advance(run, st, inline_art):
    collect(run, st)
    local_steps(run, st, inline_art)
    # submit whatever is waiting, one batch per model stage
    for stage, label in (("A", "author-A"), ("B", "author-B"), ("R", "review")):
        if any(j["stage"] == stage for j in st["jobs"].values()) and not any(
                b["state"] == "in_progress" and b["label"].startswith(label) for b in st["batches"].values()):
            submit(run, st, [stage], f"{label} round {max(j['round'] for j in st['jobs'].values())}")


def step(run):
    st = load(run)
    advance(run, st, inline_art=True)
    return st


def run_loop(run, poll):
    import threading
    st = load(run)
    lock, stop = threading.RLock(), threading.Event()
    w = threading.Thread(target=art_worker, args=(run, st, lock, stop), daemon=True)
    w.start()
    try:
        while True:
            with lock:
                advance(run, st, inline_art=False)
                if alldone(st):
                    break
            time.sleep(poll)
    finally:
        stop.set(); w.join(timeout=5)
    return st


def alldone(st):
    return all(j["stage"] in ("done", "failed") for j in st["jobs"].values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "step", "run", "status"])
    ap.add_argument("--run", required=True)
    ap.add_argument("--data", action="append", default=[])
    ap.add_argument("--lessons", default="")
    ap.add_argument("--pick", action="append", default=[], help="SUBSTR:LESSONS, e.g. Acids_and_Bases:4 (only lessons picked for data files whose path contains SUBSTR; repeatable)")
    ap.add_argument("--out-tag", default="")
    ap.add_argument("--model", default="")
    ap.add_argument("--price-mult", type=float, default=1.0, help="author-model price relative to Sonnet 5.5 list (Opus 5.5 = 2.0)")
    ap.add_argument("--engine", default="anthropic", choices=["anthropic", "openai"])
    ap.add_argument("--effort", default="")
    ap.add_argument("--cache-ttl", default=None, choices=[None, "5m", "1h"])
    ap.add_argument("--repair-rounds", type=int, default=None)
    ap.add_argument("--skip-art", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--poll", type=int, default=60)
    a = ap.parse_args()
    if a.cmd == "plan":
        if not a.data:
            sys.exit("plan needs --data")
        plan(a)
    elif a.cmd == "status":
        status(load(a.run))
    elif a.cmd == "step":
        status(step(a.run))
    else:
        status(run_loop(a.run, a.poll))


if __name__ == "__main__":
    main()
