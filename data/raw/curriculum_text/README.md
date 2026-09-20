# Extracted curriculum text — KICD STEM curricula

Grade 10 generated 2026-07-28; Grade 11 Biology added 2026-09-19. Committed so
the source PDFs never need re-OCRing.

> **The extraction is now a committed script:**
> `scripts/extract_curriculum_ocr.py`. It did not exist for the Grade 10 run —
> that was done off-server and only written up in prose, so it had to be
> rebuilt from this README in September. Use the script rather than
> reconstructing the commands again; it carries the pixel/point conversion
> and the dedup thresholds described below.
>
> ```bash
> python3 scripts/extract_curriculum_ocr.py \
>     --pdf "CBE_Curriculums/Grade 11/STEM/Biology Grade 11 - October 2025.pdf" \
>     --out grade11_biology
> ```

## Files

| File | Lines | Contents |
|---|---:|---|
| `general_science.txt` | 1,652 | General Science Grade 10 — deduped |
| `general_science.raw.txt` | 1,652 | same, before dedup (audit copy) |
| `core_mathematics.txt` | 1,534 | Core Mathematics Grade 10 — deduped |
| `core_mathematics.raw.txt` | 1,839 | same, before dedup (audit copy) |
| `essential_mathematics.txt` | 1,496 | Essential Mathematics Grade 10 — deduped |
| `essential_mathematics.raw.txt` | 1,496 | same, before dedup (audit copy) |
| `grade11_biology.txt` | 1,281 | Biology Grade 11 — deduped (nothing removed) |
| `grade11_biology.raw.txt` | 1,303 | same, before dedup (audit copy) |

Note the Grade 11 naming: `grade11_<subject>`. The Grade 10 files predate
multi-grade support and keep their bare subject names.

## Grade 11 Biology (added 2026-09-19)

Source: `CBE_Curriculums/Grade 11/STEM/Biology Grade 11 - October 2025.pdf` —
one page, 595 × 16,234 pt, image-only, DRAFT-watermarked. Sliced into 17
1,000-pt windows with 30-pt overlap at 200 dpi, OCR'd with `tesseract --psm 4`
(tesseract 5.3.4).

No deduplication was needed — the 30-pt overlap produced no 400+ character
duplicate blocks, the same result as General Science and Essential
Mathematics. The 1,303 → 1,281 line difference is blank-line normalisation
when blocks are rejoined, not removed content; the script's marker check
confirms nothing was lost.

Verified after extraction: all 10 sub-strands findable by both name and
number, and `SUMMARY STRANDS`, `STRAND 1.0/2.0/3.0`, `ESSENCE STATEMENT` and
`APPENDIX` all present.

**The sub-strand inventory was read by hand from rendered page images** (page
ix, "SUMMARY STRANDS AND SUB STRANDS"), not from this OCR text, per caveat 3
below, and is recorded in `SUBSTRAND_NAMES[11]['biology']`. Grade 11 Biology
has 10 sub-strands to Grade 10's 9, and **every shared number is a different
topic** — 2.1 is Reproduction in Plants at Grade 11, Plant Nutrition at
Grade 10.

Keep the `.raw.txt` copies. They are the fallback if dedup ever turns out to
have removed something it shouldn't have.

## How these were produced

**General Science** and **Essential Mathematics** are single-page PDFs roughly
19,600 and 17,900 points tall. Rendered at 200 dpi in 1,000-point vertical
windows with 30-point overlap (21 and 19 slices respectively), then OCR'd with
`tesseract --psm 4`.

> ⚠ `pdftoppm`'s `-x -y -W -H` are in **pixels at the render resolution**, not
> PDF points. Convert with `y_px = y_points * dpi / 72`. Getting this wrong
> silently renders the wrong region and looks like missing content.

**Core Mathematics** came from the 28-page replacement PDF Mark supplied on
2026-07-28 (`KICD_Grade_10_Core_Mathematics.pdf`), not the 21,691-point copy in
`CBE_Curriculums/`. Embedded page images were extracted losslessly with
`pdfimages -j` (1922×2526 @ 242 ppi each) and OCR'd the same way. The
replacement is materially easier to work with and is the copy that should be
committed to the repo.

## Deduplication

The Core Mathematics KICD source has a genuine defect: large boilerplate blocks
repeat verbatim about 20 times. Slice overlap also introduces small duplicates
in the two sliced documents.

Dedup is **fuzzy and deliberately conservative**. Exact matching fails because
OCR renders each repeat with slightly different character errors, so blocks are
compared with `difflib.SequenceMatcher` at a 0.92 threshold. Only blocks of
400+ characters are eligible.

That 400-character gate matters. An earlier, looser pass removed a legitimate
Appendix 1 row ("Area of a Part of a Circle") because appendix rows are
near-identical to their siblings by construction — they differ only in the
topic name. Restricting dedup to large prose blocks fixes that at the cost of
leaving some smaller repeated table fragments in place. Redundant table rows
are cheap; losing curriculum content is not.

Result: Core Mathematics 1,839 → 1,534 lines. The main boilerplate block drops
from 20 occurrences to 2. General Science and Essential Mathematics needed no
dedup — the 30-point overlap didn't produce any 400+ character duplicates.

Verified after dedup: every marker present in the raw text is still present in
the deduped text, and all 43 sub-strands across the three subjects are findable.

## Caveats — read before relying on these

1. **This is OCR, not clean extraction.** Table structure is flattened. Column
   boundaries are lost, so a row's cells run together on one line.
2. **The DRAFT watermark drops characters.** Verify anything numeric — lesson
   counts, angle values, page references — against the source PDF.
3. **These are not the authority on sub-strand inventories.** The verified
   inventories were read by hand from rendered page images and are recorded in
   `HANDOFF_new_stem_subjects_2026-07-28.md` §3. If the OCR text disagrees with
   that table, the table wins.
4. **Phase 0 verification still applies.** These files shorten Phase 0; they do
   not replace it.

## Wiring into the pipeline

`extract_curriculum_pdf()` (pdfminer) silently fails on all three sources — no
text layer. Add a branch that reads `data/raw/curriculum_text/<subject>.txt`
when it exists, and point `CURRICULUM_PDF_MAP` at these files:

```python
CURRICULUM_TEXT_MAP = {
    'general_science':       'data/raw/curriculum_text/general_science.txt',
    'core_mathematics':      'data/raw/curriculum_text/core_mathematics.txt',
    'essential_mathematics': 'data/raw/curriculum_text/essential_mathematics.txt',
}
```
