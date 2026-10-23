#!/usr/bin/env python3
"""Advisory visual QA of rendered slide PNGs via a local VLM (OpenAI-compatible server).

Usage:
    python3 scripts/qa_slides_vlm.py <png-or-dir> [--json out.json] [--url URL]
        [--model NAME] [--parallel N] [--timeout S]

Exit codes: 0 = all slides pass, 1 = at least one slide FAILED (advisory),
2 = server unreachable / usage error / unusable reply for a slide.
Server setup: /home/markk/vlm-qa/README.md. Stdlib only.
"""
import argparse, base64, concurrent.futures as cf, json, os, re, sys, time
import urllib.error, urllib.request

DEFAULT_URL = os.environ.get("VLM_QA_URL", "http://127.0.0.1:8090")
SEVERITIES = ("minor", "major", "critical")

PROMPT = """You are a strict visual QA reviewer for a classroom PowerPoint slide (16:9) rendered to an image.
Answer this checklist by LOOKING at the image. Be literal; answer true only for what you can see.
1. footer_logos_visible: the bottom-right corner normally holds two logos (a small colourful logo and a "SEAVURIA" wordmark). Are logos clearly visible there? (false if the corner is blank or covered by a plain box)
2. text_cut_at_edge: is any text or shape cut off by, or touching, the right/left/bottom slide edge, or a word truncated mid-way?
3. overlapping_items: list places where text sits on top of other text or a shape so it is hard to read (empty list if none).
4. low_contrast_items: list text that is faint or washed out against its background (empty list if none).
5. tiny_text_items: list text too small to read from the back row of a classroom (empty list if none).
6. blank_regions: list large areas that look accidentally empty or where content seems missing (empty list if none).
Reply with ONLY this JSON, no prose:
{"footer_logos_visible": true, "text_cut_at_edge": false, "text_cut_where": "", "overlapping_items": [{"where": "", "evidence": ""}], "low_contrast_items": [{"where": "", "evidence": ""}], "tiny_text_items": [{"where": "", "evidence": ""}], "blank_regions": [{"where": "", "evidence": ""}]}"""


def die(msg, code=2):
    print("qa_slides_vlm: " + msg, file=sys.stderr)
    sys.exit(code)


def http(url, payload=None, timeout=300):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def check_server(base, timeout):
    try:
        models = http(base + "/v1/models", timeout=min(timeout, 10))
    except (urllib.error.URLError, OSError, ValueError) as e:
        die("VLM server not reachable at %s (%s).\n  Start it with /home/markk/vlm-qa/start_server.sh "
            "(see /home/markk/vlm-qa/README.md)." % (base, e))
    ids = [m.get("id") for m in models.get("data", [])]
    return ids[0] if ids else "default"


def _items(v):
    out = []
    for x in (v or []):
        if isinstance(x, dict) and (x.get("where") or x.get("evidence")):
            out.append((str(x.get("where", "")), str(x.get("evidence", ""))))
        elif isinstance(x, str) and x.strip():
            out.append((x, ""))
    return out


def parse_reply(text):
    """Turn the model's checklist answers into [{issue, severity, where, evidence}]."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON object in reply: %r" % text[:200])
    o = json.loads(m.group(0))
    issues = []
    if o.get("footer_logos_visible") is False:
        issues.append(("missing_logo", "major", "footer, bottom-right", "model reports no logos visible in footer corner"))
    if o.get("text_cut_at_edge") is True:
        issues.append(("clipped", "major", str(o.get("text_cut_where", "")) or "slide edge", "model reports text/shape cut off or touching slide edge"))
    for key, name, sev in (("overlapping_items", "overlap", "major"), ("low_contrast_items", "low_contrast", "major"),
                           ("tiny_text_items", "small_text", "minor"), ("blank_regions", "empty_region", "minor")):
        for where, ev in _items(o.get(key)):
            issues.append((name, sev, where, ev))
    issues = [{"issue": i, "severity": s, "where": w, "evidence": e} for i, s, w, e in issues]
    ok = not any(i["severity"] in ("major", "critical") for i in issues)
    return {"pass": ok, "issues": issues}


def review(path, base, model, timeout):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {
        "model": model, "temperature": 0, "max_tokens": 700,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
            {"type": "text", "text": PROMPT}]}],
    }
    t0 = time.time()
    try:
        resp = http(base + "/v1/chat/completions", payload, timeout)
        res = parse_reply(resp["choices"][0]["message"]["content"])
        res["error"] = None
    except Exception as e:  # keep going on other slides
        res = {"pass": None, "issues": [], "error": "%s: %s" % (type(e).__name__, e)}
    res["file"] = path
    res["seconds"] = round(time.time() - t0, 2)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="PNG file or directory of PNGs")
    ap.add_argument("--json", help="write full results to this file")
    ap.add_argument("--url", default=DEFAULT_URL, help="server base URL (default %(default)s)")
    ap.add_argument("--model", help="model name (default: first from /v1/models)")
    ap.add_argument("--parallel", type=int, default=4, help="concurrent requests (default 4; match server NP)")
    ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()

    if os.path.isdir(a.target):
        files = sorted(os.path.join(a.target, f) for f in os.listdir(a.target) if f.lower().endswith(".png"))
    elif os.path.isfile(a.target):
        files = [a.target]
    else:
        die("not found: " + a.target)
    if not files:
        die("no PNG files in " + a.target)

    base = a.url.rstrip("/")
    model = a.model or check_server(base, a.timeout)
    with cf.ThreadPoolExecutor(max_workers=max(1, a.parallel)) as ex:
        results = list(ex.map(lambda p: review(p, base, model, a.timeout), files))

    for r in results:
        if r["error"]:
            print("ERROR %s  %s" % (r["file"], r["error"]))
            continue
        print("%s %s  (%.1fs)" % ("PASS" if r["pass"] else "FAIL", r["file"], r["seconds"]))
        for i in r["issues"]:
            print("   - [%s] %s @ %s: %s" % (i["severity"], i["issue"], i["where"], i["evidence"]))
    out = {"model": model, "advisory": True, "results": results}
    if a.json:
        with open(a.json, "w") as f:
            json.dump(out, f, indent=2)
    if any(r["error"] for r in results):
        sys.exit(2)
    sys.exit(0 if all(r["pass"] for r in results) else 1)


if __name__ == "__main__":
    main()
