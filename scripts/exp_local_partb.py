#!/usr/bin/env python3
"""
exp_local_partb.py — EXPERIMENT (presentations branch): can a local model on the Spark write Part B of a deck spec
(title one-liner, unit-map titles, goals, key words, safety, glance, summary, notes of the fixed slides) well enough?

Uses exactly the same prompt, payload, schema (SPEC_B) and Part A as the API run, but calls a local llama.cpp server
(OpenAI-compatible, grammar-constrained JSON) instead of Sonnet 5.5. Then builds and validates the deck with the
normal builder and validator and prints how it did. Optional --review adds ONE paid Sonnet review call (about $0.17).

  python3 scripts/exp_local_partb.py --data <data.json> --lesson 2 --parta <spec.json with Part A> --label d32 [--review]
"""
import argparse
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import generate_deck as g  # noqa: E402
from deck_spec_schema import SPEC_B, merge  # noqa: E402


def local_chat(endpoint, model, system, user, schema, max_tokens, temperature=0.3):
    body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "max_tokens": max_tokens, "temperature": temperature, "stream": True,
            "response_format": {"type": "json_schema", "json_schema": {"name": "part_b", "strict": True, "schema": schema}}}
    req = urllib.request.Request(endpoint + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time(); text = []; n = 0; first = None
    with urllib.request.urlopen(req, timeout=7200) as r:
        for line in r:
            line = line.decode().strip()
            if not line.startswith("data:") or line.endswith("[DONE]"):
                continue
            ch = json.loads(line[5:])["choices"][0]
            d = ch.get("delta", {}).get("content")
            if d:
                if first is None: first = time.time() - t0
                text.append(d); n += 1
            if ch.get("finish_reason") and ch["finish_reason"] != "stop":
                print("  finish_reason:", ch["finish_reason"])
    secs = time.time() - t0
    return "".join(text), {"seconds": round(secs), "first_token_s": round(first or 0, 1), "chunks": n, "approx_tok_per_s": round(n / max(1, secs - (first or 0)), 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--lesson", type=int, required=True)
    ap.add_argument("--parta", required=True, help="spec JSON whose Part A (slides, minutes, hero) is reused")
    ap.add_argument("--label", required=True); ap.add_argument("--endpoint", default="http://localhost:8090"); ap.add_argument("--model", default="qwen3-vl-32b")
    ap.add_argument("--max-tokens", type=int, default=14000); ap.add_argument("--review", action="store_true")
    a = ap.parse_args()
    data = json.load(open(a.data)); lesson = next(l for l in data["LESSONS"] if l["number"] == a.lesson)
    pay = g.payload(data, lesson, g.resources_for(a.data, a.lesson), g.template_labels())
    pay_text = "# INPUT (the SoW lesson and everything you may use)\n" + json.dumps(pay, ensure_ascii=False, indent=1)
    sysm = g.system_prompt()
    A = g.part_a_of(json.load(open(a.parta)))
    totals = g.group_minutes(A)
    user = (pay_text + "\n\nBuild the deck spec for this lesson only. Follow the manual exactly.\n\n" + g.PART_B +
            "\n\n# GROUP TOTALS the glance rows must match\n" + json.dumps(totals) + "\n\n# PART A (final)\n" + json.dumps(A, ensure_ascii=False))
    print(f"[{a.label}] prompt chars: system {len(sysm)}, user {len(user)}; generating Part B locally...", flush=True)
    text, stats = local_chat(a.endpoint, a.model, sysm, user, SPEC_B, a.max_tokens)
    print(f"[{a.label}] done: {stats}")
    out = {"label": a.label, "stats": stats}
    try:
        B = json.loads(text)
    except Exception as e:
        out["parse_error"] = str(e)[:200]; out["raw_tail"] = text[-300:]
        json.dump(out, open(os.path.join(ROOT, "logs", f"exp_partb_{a.label}.json"), "w"), indent=1); print("JSON PARSE FAILED", e); return 1
    spec = merge(A, B)
    sdir = os.path.join(ROOT, "logs", "exp_partb"); os.makedirs(sdir, exist_ok=True)
    spec_path = os.path.join(sdir, f"L{a.lesson}.{a.label}.spec.json"); json.dump(spec, open(spec_path, "w"), indent=1, ensure_ascii=False)
    deck_path = os.path.join(sdir, f"L{a.lesson}.{a.label}.pptx")
    problems, _ = g.build_and_validate(a.data, a.lesson, spec_path, deck_path)
    out["validator_problems"] = problems
    print(f"[{a.label}] validator/layout problems: {len(problems)}"); [print("   -", p[:200]) for p in problems]
    if a.review:
        g.load_env(); import anthropic
        from deck_spec_schema import REVIEW
        client = anthropic.Anthropic()
        rv, u = g.call(client, g.CFG["reviewer_model"], g.REVIEW_RULES, "Review this deck spec.\n\n" + json.dumps({"sow": pay, "deck_spec": spec}, ensure_ascii=False), REVIEW, f"review exp {a.label}", max_tokens=16000)
        out["review"] = rv; out["review_cost_usd"] = round(g.cost(u), 3)
        print(f"[{a.label}] review: {len(rv['findings'])} findings, {sum(f['severity']=='major' for f in rv['findings'])} major, verdict {rv['verdict']}")
    json.dump(out, open(os.path.join(ROOT, "logs", f"exp_partb_{a.label}.json"), "w"), indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
