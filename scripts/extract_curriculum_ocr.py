#!/usr/bin/env python3
"""OCR-extract a KICD curriculum PDF into plain text.

The KICD STEM curriculum PDFs are screenshot exports with no text layer, so
pdfminer (and therefore extract_curriculum_pdf()) silently returns nothing for
them. This script renders the pages and OCRs them instead.

This codifies the method used for the Grade 10 STEM subjects on 2026-07-28,
which until now existed only as prose in data/raw/curriculum_text/README.md and
HANDOFF_new_stem_subjects_2026-07-28.md §6.2 — the script itself was never
committed, so it had to be rebuilt from the write-up. Keep this file with the
output it produces.

Two source shapes, both seen in practice:

  slice mode  - one enormous single page (e.g. 595 x 16,234 pt). Rendered in
                overlapping vertical windows, because rendering 16,000 pt in one
                go at 200 dpi is an unreasonable bitmap.
  pages mode  - a normal multi-page PDF carrying one embedded image per page.
                Images are pulled losslessly with pdfimages -j.

Usage:
    python3 scripts/extract_curriculum_ocr.py \
        --pdf "CBE_Curriculums/Grade 11/STEM/Biology Grade 11 - October 2025.pdf" \
        --out biology_g11

    # multi-page source with embedded page images
    python3 scripts/extract_curriculum_ocr.py --pdf foo.pdf --out bar --mode pages

Writes data/raw/curriculum_text/<out>.raw.txt (never dedupe this — it is the
audit copy) and <out>.txt (deduped, what the pipeline reads).
"""

import argparse
import difflib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEXT_DIR = PROJECT_ROOT / 'data' / 'raw' / 'curriculum_text'

# Dedup tuning. Do not loosen either of these without re-reading §6.4 of
# HANDOFF_new_stem_subjects_2026-07-28.md: a looser earlier pass silently
# deleted a real Appendix 1 row ("Area of a Part of a Circle") because appendix
# rows differ from their siblings only in the topic name. Blocks shorter than
# MIN_DEDUP_CHARS are never eligible, so only long boilerplate prose can be
# removed. Redundant table rows are cheap; losing curriculum content is not.
SIMILARITY_THRESHOLD = 0.92
MIN_DEDUP_CHARS = 400


def require_tools(names):
    missing = [n for n in names if shutil.which(n) is None]
    if missing:
        sys.exit(
            f"ERROR: required tool(s) not found: {', '.join(missing)}\n"
            f"  Install with: sudo apt-get install -y tesseract-ocr poppler-utils"
        )


def pdf_geometry(pdf: Path):
    """Return (pages, width_pt, height_pt) from pdfinfo."""
    out = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True, check=True).stdout
    pages = int(re.search(r'^Pages:\s+(\d+)', out, re.M).group(1))
    m = re.search(r'^Page size:\s+([\d.]+) x ([\d.]+)', out, re.M)
    return pages, float(m.group(1)), float(m.group(2))


def has_text_layer(pdf: Path) -> bool:
    out = subprocess.run(['pdffonts', str(pdf)], capture_output=True, text=True).stdout
    # Two header lines always print; any third line means an embedded font.
    return len([ln for ln in out.splitlines() if ln.strip()]) > 2


def ocr_image(img: Path) -> str:
    """OCR one image with the settings the Grade 10 extraction used.

    --psm 4 = "single column of text of variable sizes", which handles these
    curriculum tables better than the default page-segmentation mode.
    """
    res = subprocess.run(
        ['tesseract', str(img), 'stdout', '--psm', '4'],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        sys.exit(f"ERROR: tesseract failed on {img.name}:\n{res.stderr.strip()}")
    return res.stdout


def render_slices(pdf: Path, tmp: Path, dpi: int, window_pt: float, overlap_pt: float):
    """Render one tall page as overlapping vertical windows. Returns image paths."""
    _, width_pt, height_pt = pdf_geometry(pdf)

    # pdftoppm's -x -y -W -H are in PIXELS at the render resolution, not PDF
    # points. This conversion is the single most expensive mistake available
    # here: get it wrong and it renders the wrong region, which looks exactly
    # like missing source content rather than like a bug.
    def to_px(points: float) -> int:
        return int(round(points * dpi / 72.0))

    width_px = to_px(width_pt)
    step_pt = window_pt - overlap_pt
    images = []
    y_pt = 0.0
    index = 0

    while y_pt < height_pt:
        this_window = min(window_pt, height_pt - y_pt)
        prefix = tmp / f'slice_{index:03d}'
        subprocess.run([
            'pdftoppm', '-r', str(dpi), '-png', '-f', '1', '-l', '1',
            '-x', '0', '-y', str(to_px(y_pt)),
            '-W', str(width_px), '-H', str(to_px(this_window)),
            str(pdf), str(prefix),
        ], check=True, capture_output=True)

        produced = sorted(tmp.glob(f'slice_{index:03d}*.png'))
        if not produced:
            sys.exit(f"ERROR: pdftoppm produced no output for slice {index} at y={y_pt:.0f}pt")
        images.extend(produced)
        print(f"  rendered slice {index:>3}  y={y_pt:>9.0f}pt  h={this_window:>6.0f}pt")
        index += 1
        y_pt += step_pt

    return images


def render_page_images(pdf: Path, tmp: Path):
    """Pull embedded page images losslessly. Returns image paths."""
    subprocess.run(['pdfimages', '-j', str(pdf), str(tmp / 'page')],
                   check=True, capture_output=True)
    images = sorted(p for p in tmp.iterdir() if p.suffix in {'.jpg', '.ppm', '.png'})
    if not images:
        sys.exit("ERROR: pdfimages extracted no images — is this really an image-only PDF?")
    for img in images:
        print(f"  extracted {img.name}")
    return images


def split_blocks(text: str):
    return [b for b in re.split(r'\n\s*\n', text) if b.strip()]


def dedupe(text: str):
    """Fuzzy-dedupe large repeated prose blocks. Returns (text, removed_count)."""
    blocks = split_blocks(text)
    kept, removed = [], 0

    for block in blocks:
        if len(block) < MIN_DEDUP_CHARS:
            kept.append(block)
            continue
        duplicate = False
        for existing in kept:
            if len(existing) < MIN_DEDUP_CHARS:
                continue
            if difflib.SequenceMatcher(None, block, existing).ratio() >= SIMILARITY_THRESHOLD:
                duplicate = True
                break
        if duplicate:
            removed += 1
        else:
            kept.append(block)

    return '\n\n'.join(kept), removed


def verify_no_content_lost(raw: str, deduped: str):
    """Every sub-strand-ish marker in raw must survive into deduped.

    This is the check that caught the over-aggressive first pass in the Grade 10
    run. It compares marker COUNTS, not just presence — inspection missed it.
    """
    pattern = re.compile(r'\b\d+\.\d+\b')
    raw_markers = set(pattern.findall(raw))
    lost = sorted(m for m in raw_markers if m not in set(pattern.findall(deduped)))
    return lost


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--pdf', required=True, help='source curriculum PDF')
    ap.add_argument('--out', required=True,
                    help="output basename, e.g. 'biology_g11' -> biology_g11.txt")
    ap.add_argument('--mode', choices=['slice', 'pages', 'auto'], default='auto',
                    help="'auto' picks slice for 1-page sources, pages otherwise")
    ap.add_argument('--dpi', type=int, default=200)
    ap.add_argument('--window', type=float, default=1000.0, help='slice height in PDF points')
    ap.add_argument('--overlap', type=float, default=30.0, help='slice overlap in PDF points')
    ap.add_argument('--keep-images', metavar='DIR',
                    help='also copy rendered images here (for hand-verification)')
    args = ap.parse_args()

    pdf = Path(args.pdf)
    if not pdf.is_absolute():
        pdf = PROJECT_ROOT / pdf
    if not pdf.exists():
        sys.exit(f"ERROR: source PDF not found: {pdf}")

    require_tools(['pdfinfo', 'pdftoppm', 'pdfimages', 'pdffonts', 'tesseract'])

    pages, width_pt, height_pt = pdf_geometry(pdf)
    mode = args.mode
    if mode == 'auto':
        mode = 'slice' if pages == 1 else 'pages'

    print(f"Source : {pdf.name}")
    print(f"Geometry: {pages} page(s), {width_pt:.0f} x {height_pt:.0f} pt")
    print(f"Mode   : {mode}")

    if has_text_layer(pdf):
        print("  NOTE: this PDF has an embedded text layer — extract_curriculum_pdf()")
        print("        (pdfminer) may work directly and would be cleaner than OCR.")

    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = TEXT_DIR / f'{args.out}.raw.txt'
    out_path = TEXT_DIR / f'{args.out}.txt'

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        if mode == 'slice':
            images = render_slices(pdf, tmp, args.dpi, args.window, args.overlap)
        else:
            images = render_page_images(pdf, tmp)

        print(f"\nOCR: {len(images)} image(s) with tesseract --psm 4 ...")
        chunks = []
        for i, img in enumerate(images):
            chunks.append(ocr_image(img))
            print(f"  ocr {i + 1}/{len(images)}")

        if args.keep_images:
            dest = Path(args.keep_images)
            dest.mkdir(parents=True, exist_ok=True)
            for img in images:
                shutil.copy2(img, dest / img.name)
            print(f"  kept {len(images)} image(s) in {dest}")

    raw_text = '\n\n'.join(chunks)
    raw_path.write_text(raw_text, encoding='utf-8')

    deduped, removed = dedupe(raw_text)
    lost = verify_no_content_lost(raw_text, deduped)
    if lost:
        # Keep the raw file; refuse to write a deduped copy that lost content.
        sys.exit(
            f"ERROR: dedup dropped marker(s) present in raw text: {', '.join(lost)}\n"
            f"  Raw text kept at {raw_path}. Deduped output NOT written.\n"
            f"  Raise MIN_DEDUP_CHARS or SIMILARITY_THRESHOLD and re-run."
        )
    out_path.write_text(deduped, encoding='utf-8')

    raw_lines = len(raw_text.splitlines())
    out_lines = len(deduped.splitlines())
    print(f"\nWrote {raw_path.relative_to(PROJECT_ROOT)}  ({raw_lines} lines)")
    print(f"Wrote {out_path.relative_to(PROJECT_ROOT)}  ({out_lines} lines, "
          f"{removed} duplicate block(s) removed)")
    print("\nThis text is NOT authoritative for sub-strand names or counts.")
    print("Hand-verify those against rendered page images before entering them")
    print("into SUBSTRAND_NAMES — see the README in that directory.")


if __name__ == '__main__':
    main()
