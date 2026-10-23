#!/usr/bin/env python3
"""
make_art.py — produce the illustrations a deck spec asks for (presentations branch).

  python3 scripts/make_art.py data/presentations_specs/Biology/SS1.1_Cell_Structure/L2.spec.json [--n 4] [--redo ID]

For every art id used by the spec (title-slide hero + `illustration` blocks) that has no final picture yet:
  1. scripts/gen_art.py   -> N candidates on the Spark GPU (style preset, seeds recorded in meta.json)
  2. scripts/pick_art.py  -> the local vision model ranks the candidates (advisory)
  3. post-process the chosen one: square crop, 1024 px, rounded corners -> data/presentations_art/final/<id>.png
  4. record prompt / alt / seed / model in data/presentations_art/catalogue.json
Existing ids are REUSED as they are (consistency across the 12 lessons). `--redo ID` regenerates one id.
Candidates stay in data/presentations_art/candidates/ (not committed); final pictures and the catalogue are.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "data", "presentations_art")
FINAL = os.path.join(ART, "final")
CAND = os.path.join(ART, "candidates")
CAT = os.path.join(ART, "catalogue.json")


def requests(spec):
    out = {}
    h = spec.get("hero") or {}
    if h.get("art_id"):
        out[h["art_id"]] = {"prompt": h.get("prompt", ""), "alt": h.get("alt", "")}
    for sl in spec["slides"]:
        for b in sl["blocks"]:
            if b["type"] == "illustration" and b.get("items"):
                out.setdefault(b["items"][0], {"prompt": (b["items"][1] if len(b["items"]) > 1 else ""), "alt": b.get("text", "")})
    return out


def finish(src, dest, px=1024, radius=64):
    from PIL import Image, ImageDraw
    im = Image.open(src).convert("RGB")
    w, h = im.size
    d = min(w, h)
    im = im.crop(((w - d) // 2, (h - d) // 2, (w - d) // 2 + d, (h - d) // 2 + d)).resize((px, px), Image.LANCZOS)
    mask = Image.new("L", (px, px), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, px - 1, px - 1), radius=radius, fill=255)
    out = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    out.save(dest, optimize=True)


def main():
    import fcntl
    os.makedirs(ART, exist_ok=True)
    lock = open(os.path.join(ART, ".lock"), "w")
    fcntl.flock(lock, fcntl.LOCK_EX)           # one GPU: parallel deck runs queue here; also keeps catalogue.json consistent
    return _main()


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--redo", action="append", default=[])
    ap.add_argument("--lesson", default="")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    cat = json.load(open(CAT)) if os.path.exists(CAT) else {}
    todo = {k: v for k, v in requests(spec).items() if k in a.redo or not os.path.exists(os.path.join(FINAL, k + ".png"))}
    if not todo:
        print("art: nothing to generate (all ids exist)")
        return 0
    failed = []
    for aid, rq in todo.items():
        if not rq["prompt"].strip():
            print(f"art: '{aid}' has no prompt and no existing picture"); failed.append(aid); continue
        print(f"art: generating '{aid}': {rq['prompt'][:90]}")
        rc = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "gen_art.py"), "--id", aid, "--prompt", rq["prompt"], "--n", str(a.n), "--size", "1024x1024", "--out", CAND], cwd=ROOT).returncode
        if rc:
            print(f"art: gen_art.py failed for '{aid}' (exit {rc})"); failed.append(aid); continue
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "pick_art.py"), os.path.join(CAND, aid)], cwd=ROOT)  # advisory; falls back to candidate 0
        meta = json.load(open(os.path.join(CAND, aid, "meta.json")))
        chosen = meta.get("chosen") or os.path.join(CAND, aid, "cand_0.png")
        if not os.path.isabs(chosen):
            chosen = os.path.join(CAND, aid, os.path.basename(chosen))
        finish(chosen, os.path.join(FINAL, aid + ".png"))
        cat[aid] = {"prompt": rq["prompt"], "alt": rq["alt"], "chosen": os.path.basename(chosen), "model": meta.get("model"), "seeds": meta.get("seeds") or meta.get("seed"),
                    "first_used": a.lesson or os.path.basename(a.spec), "created": datetime.datetime.now().isoformat(timespec="seconds")}
        json.dump(cat, open(CAT, "w"), indent=1, ensure_ascii=False)
        print(f"art: '{aid}' -> final/{aid}.png")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
