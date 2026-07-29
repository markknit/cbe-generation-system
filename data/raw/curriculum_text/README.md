# Extracted curriculum text — Grade 10 STEM (KICD July 2025)

Generated 2026-07-28. Drop this whole folder at
`data/raw/curriculum_text/` in `cbe-generation-system` and commit it, so the
three source PDFs never need re-OCRing.

## Files

| File | Lines | Contents |
|---|---:|---|
| `general_science.txt` | 1,652 | General Science Grade 10 — deduped |
| `general_science.raw.txt` | 1,652 | same, before dedup (audit copy) |
| `core_mathematics.txt` | 1,534 | Core Mathematics Grade 10 — deduped |
| `core_mathematics.raw.txt` | 1,839 | same, before dedup (audit copy) |
| `essential_mathematics.txt` | 1,496 | Essential Mathematics Grade 10 — deduped |
| `essential_mathematics.raw.txt` | 1,496 | same, before dedup (audit copy) |

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
