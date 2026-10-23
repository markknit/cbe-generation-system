#!/usr/bin/env python3
"""
render_and_qa.py — render deck(s) with LibreOffice (hidden slides included) and run the local vision reader over every slide
(presentations branch). Advisory only: the deterministic validator decides pass/fail.

  python3 scripts/render_and_qa.py <deck.pptx> [<deck.pptx> ...] [--out DIR] [--parallel 4]

Writes DIR/<deck>/s-NN.png and DIR/<deck>/qa.json; prints one line per deck and the slides the reader flagged.
Default DIR: data/outputs/presentations/_qa (gitignored with the other generated files).
"""
import argparse, json, os, re, subprocess, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def unhide(src, dst):
    zi = zipfile.ZipFile(src); zo = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    for it in zi.infolist():
        d = zi.read(it.filename)
        if re.match(r"ppt/slides/slide\d+\.xml$", it.filename):
            d = d.replace(b' show="0"', b"")
        zo.writestr(it, d)
    zo.close()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("decks", nargs="+"); ap.add_argument("--out", default=os.path.join(ROOT, "data", "outputs", "presentations", "_qa")); ap.add_argument("--parallel", default="4")
    a = ap.parse_args(); bad = 0
    prof = tempfile.mkdtemp(prefix="lo_qa_")
    for deck in a.decks:
        name = os.path.splitext(os.path.basename(deck))[0]; d = os.path.join(a.out, name); os.makedirs(d, exist_ok=True)
        tmp = os.path.join(d, "unhidden.pptx"); unhide(deck, tmp)
        subprocess.run(["soffice", f"-env:UserInstallation=file://{prof}", "--headless", "--convert-to", "pdf", "--outdir", d, tmp], capture_output=True, timeout=600)
        subprocess.run(["pdftoppm", "-r", "80", "-png", os.path.join(d, "unhidden.pdf"), os.path.join(d, "s")], check=True)
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "qa_slides_vlm.py"), d, "--json", os.path.join(d, "qa.json"), "--parallel", a.parallel], capture_output=True, text=True)
        if r.returncode == 2:
            print(f"{name}: VISION SERVER PROBLEM: {r.stderr.strip()[:200]}"); bad += 1; continue
        res = json.load(open(os.path.join(d, "qa.json")))["results"]
        fails = [x for x in res if str(x.get("verdict", x.get("status", ""))).upper() == "FAIL" or x.get("pass") is False]
        majors = [(os.path.basename(x.get("image", x.get("file", "?"))), i) for x in res for i in x.get("issues", []) if i.get("severity") == "major"]
        print(f"{name}: {len(res)} slides, {len(fails)} FAIL" + ("" if not fails else "  <- " + ", ".join(os.path.basename(x.get('image', x.get('file', '?'))) for x in fails)))
        for f, i in majors:
            print(f"    {f}: [{i.get('issue')}] {i.get('where','')}: {str(i.get('evidence',''))[:120]}")
        bad += bool(fails)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
