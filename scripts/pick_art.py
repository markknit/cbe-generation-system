#!/usr/bin/env python3
"""Rank illustration candidates with the local Qwen3-VL server and record the best one in meta.json.

Usage:
    python3 scripts/pick_art.py <candidates_dir>/<id> [--json out.json] [--url URL] [--parallel 4] [--no-write]

Reads <dir>/meta.json (its "scene" is the target description) and every cand_*.png. Each candidate is scored 0-10 on:
match (matches the description), no_text (no visible text/letters/gibberish), anatomy (no body/object errors),
style (clean flat vector style), safe (child-friendly, not graphic). Ranking = weighted mean; a candidate with
no_text < 6, anatomy < 5 or safe < 8 is marked "reject" and never chosen unless every candidate is rejected
(then the best is still recorded, with "chosen_warning"). The others are never deleted.
Writes "chosen" (file name), "chosen_path" and "scores" into meta.json. ADVISORY: the VLM misses small defects,
so a human still looks at the chosen image. Exit codes: 0 ok, 1 all candidates rejected, 2 server/usage error.
Server setup: /home/markk/vlm-qa/README.md. Stdlib only.
"""
import argparse, base64, concurrent.futures as cf, json, os, re, sys, time
import urllib.error, urllib.request

DEFAULT_URL = os.environ.get("VLM_QA_URL", "http://127.0.0.1:8090")
WEIGHTS = {"match": 3, "no_text": 2, "anatomy": 2, "style": 1, "safe": 1}

PROMPT = """You are a strict art reviewer choosing an illustration for a Kenyan Grade 10 science lesson slide.
Intended scene: "%s"
Look at the image and score each item from 0 (terrible) to 10 (perfect). Be literal and critical; do not give 10 easily.
- match: does the image show what the scene describes (every named object/person/action present, nothing important missing)?
- no_text: 10 = no letters, numbers, writing or gibberish glyphs anywhere (including on books, boards, signs, labels); 0 = clear text or text-like scribbles.
- anatomy: any people have correct faces, hands (5 fingers), limbs; objects are plausible and not duplicated or fused (e.g. two microscopes merged, floating parts).
- style: clean, flat vector, smooth outlines, bright friendly colours, consistent, uncluttered.
- safe: child-friendly, respectful, not graphic or frightening (10 = clearly fine for children).
Reply with ONLY this JSON, no prose:
{"match": 0, "no_text": 0, "anatomy": 0, "style": 0, "safe": 0, "problems": "one short sentence naming the worst defect, or none"}"""


def die(msg, code=2):
    print("pick_art: " + msg, file=sys.stderr)
    sys.exit(code)


def http(url, payload=None, timeout=300):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def score(path, scene, base, model, timeout):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {"model": model, "temperature": 0, "max_tokens": 250, "messages": [{"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
        {"type": "text", "text": PROMPT % scene.replace('"', "'")}]}]}
    res = {"file": os.path.basename(path), "error": None}
    try:
        txt = http(base + "/v1/chat/completions", payload, timeout)["choices"][0]["message"]["content"]
        m = re.search(r"\{.*\}", txt, re.S)
        if not m:
            raise ValueError("no JSON in reply: %r" % txt[:150])
        o = json.loads(m.group(0))
        for k in WEIGHTS:
            res[k] = max(0.0, min(10.0, float(o[k])))
        res["problems"] = str(o.get("problems", ""))[:300]
        res["total"] = round(sum(res[k] * w for k, w in WEIGHTS.items()) / sum(WEIGHTS.values()), 2)
        res["reject"] = bool(res["no_text"] < 6 or res["anatomy"] < 5 or res["safe"] < 8)
    except Exception as e:
        res["error"] = "%s: %s" % (type(e).__name__, e)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="candidate folder containing meta.json and cand_*.png")
    ap.add_argument("--json", help="also write the full ranking here")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--no-write", action="store_true", help="do not touch meta.json")
    a = ap.parse_args()

    mp = os.path.join(a.dir, "meta.json")
    if not os.path.isfile(mp):
        die("no meta.json in %s (run gen_art.py first)" % a.dir)
    meta = json.load(open(mp))
    scene = meta.get("scene") or meta.get("prompt")
    files = sorted(os.path.join(a.dir, f) for f in os.listdir(a.dir) if re.fullmatch(r"cand_\d+\.png", f))
    if not files:
        die("no cand_*.png in " + a.dir)
    base = a.url.rstrip("/")
    try:
        ids = [m.get("id") for m in http(base + "/v1/models", timeout=10).get("data", [])]
    except (urllib.error.URLError, OSError, ValueError) as e:
        die("VLM server not reachable at %s (%s).\n  Start it with /home/markk/vlm-qa/start_server.sh" % (base, e))
    model = ids[0] if ids else "default"

    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=max(1, a.parallel)) as ex:
        res = list(ex.map(lambda p: score(p, scene, base, model, a.timeout), files))
    bad = [r for r in res if r["error"]]
    for r in bad:
        print("ERROR %s  %s" % (r["file"], r["error"]), file=sys.stderr)
    ok = [r for r in res if not r["error"]]
    if not ok:
        die("no candidate could be scored")
    ranked = sorted(ok, key=lambda r: (r["reject"], -r["total"]))
    print("scene: %s" % scene)
    for i, r in enumerate(ranked, 1):
        print("%d. %s  total %.2f%s  match %.0f text %.0f anat %.0f style %.0f safe %.0f  | %s" % (
            i, r["file"], r["total"], "  REJECT" if r["reject"] else "", r["match"], r["no_text"], r["anatomy"],
            r["style"], r["safe"], r["problems"]))
    best = ranked[0]
    allrej = best["reject"]
    print("chosen: %s%s  (%.0fs)" % (best["file"], "  (WARNING: all candidates rejected, regenerate)" if allrej else "", time.time() - t0))
    if not a.no_write:
        meta["chosen"] = best["file"]
        meta["chosen_path"] = os.path.join(a.dir, best["file"])
        meta["scores"] = {r["file"]: {k: v for k, v in r.items() if k != "file"} for r in res}
        meta["picker"] = {"model": model, "advisory": True}
        if allrej:
            meta["chosen_warning"] = "all candidates failed the text/anatomy/safety gates; regenerate"
        else:
            meta.pop("chosen_warning", None)
        with open(mp, "w") as f:
            json.dump(meta, f, indent=2)
    if a.json:
        with open(a.json, "w") as f:
            json.dump({"dir": a.dir, "scene": scene, "chosen": best["file"], "ranking": ranked, "errors": bad}, f, indent=2)
    sys.exit(1 if allrej else 0)


if __name__ == "__main__":
    main()
