# Core Mathematics 2.7 — focused final PDF completion review

**PASS for the remaining standard-artifact propagation/layout gate, 2026-11-13. Unresolved confirmed artifact errors: 0.** This independently delegated recovery closes the unfinished check in `coremath_2_7_layout_review.md`; that original INCOMPLETE report remains unchanged. No canonical content, generated document or acceptance record was edited. Root supplied a fresh 97% weekly allowance and cleared pause at 23:13 UTC; the reviewer did not invoke subordinate usage helpers.

## Evidence continuity and exact scope

Accepted canonical fingerprint independently recomputed: `261cfa07c19ffbd3eb912f3e18573dde71de2328970b3c276b3224a3478b6378`. It exactly matches the accepted recovery review and incomplete final report. Independently recomputed SHA256s of CBE_LessonSequence, FinalExplanation, FinalExplanation_TeacherKey and SummaryTable, Word and PDF: all eight exactly match that report. Full current hashes are in `evidence/coremath_2_7_pdf_completion_check.json`.

The prior independent content/source/math review, corrected actual net embeddings and five draft-artifact checks remain valid at this unchanged fingerprint, as documented in `coremath_2_7_recovery_recheck.md`. The incomplete final report already records exact Word propagation, student/key isolation, all 70 standard PDF pages surveyed as contact sheets and readable targeted pages. This completion relies on those saved checks; it does not claim to repeat a full source/math review or visually read every line of every page.

## Reproduced failed comparison and resolution

The prior failing assertion was not saved with a string or stack location, so its exact historical execution point cannot be recovered. The underlying comparison problem is reproducible on the unchanged PDFs: whitespace-normalised substring search in `pdftotext -layout` output fails because parallel table cells are interleaved by visual line. Exact reproduced failing strings include:

- SummaryTable L1 learned: `Surface area sums exposed face areas in square units.` The first line ends `in`, then text from the explanation cell intervenes before `square units.` Plain reading-order extraction and bounded text blocks recover the complete canonical cell; all 42 summary cells pass.
- FinalExplanation rubric criterion 1: `Determine and justify basic/composite exposed surface areas`. Its line wraps are interleaved with adjacent descriptor cells in layout text. The canonical criterion is intact in bounded text blocks.
- Final lesson phase 1 learner text: `Read procedure,formula support and dimensions.` Adjacent resource, teacher-move and evidence columns interrupt the layout-mode string. The bounded learner cell is intact.

A plain reading-order comparison also leaves several apparent mismatches. The student criterion-3 row continues from p5 to p6; the key's capacity prompt/exemplar continue from p1 to p2, and its final excellent descriptor continues from p2 to p3. Recombining the same PDF column across those page boundaries recovers every canonical string. `evidence-gathering` wraps as `evidence-` / `gathering`, with the retained visible hyphen joined across line whitespace. Sequence p56 visibly prints `practical-` / `use`; Poppler's plain reading-order output drops the hyphen and gives `practicaluse`. Bbox text preserves it, and the actual page confirms the complete canonical compound. These are extraction/reading-order differences, not lost PDF content.

## Completed propagation and final isolation checks

`evidence/coremath_2_7_pdf_completion_check.py` is a reproducible, read-only content/artifact check which writes only its JSON evidence. Command from repository root:

```bash
venv/bin/python data/curriculum_expansion_2026-11/reviews/batch_02/evidence/coremath_2_7_pdf_completion_check.py
```

**110/110 checks pass:** instructions and all four prompts in student/key PDFs; all three criteria and all twelve level descriptors in each PDF; four teacher exemplars and their exclusion from student PDF; 42 summary cells; all 20 final-lesson phase entries. It extracts actual PDF bounding-box text, explicitly rejoins only identified same-cell page continuations, collapses whitespace and rejoins whitespace immediately after retained hyphens. It does not discard words, mathematical glyphs or punctuation to make strings match. Numeric tasks were previously independently accepted; this scope verifies propagation of their actual wording.

Final structured export independently inspected: all five final phases have both `video` and `reading` equal to null (10/10 slots). Generic Search ARES fallbacks in the teacher sequence are already documented in the incomplete report and are not selected external resources. The final lesson consistently requires individual work, with hints, comparisons and answer discussion withheld until collection.

## Actual page inspection and limits

Directly inspected preserved actual PDF renders for FinalExplanation pp5–6, FinalExplanation_TeacherKey pp1–2, CBE_LessonSequence p56 and SummaryTable p1. The exact current PDF hashes match those used to create the saved renders and incomplete review. Rubric/key continuations contain all text without overlap or clipping; student answer space remains blank; the key is clearly labelled not for students. No new full-page rendering or document regeneration was necessary. Additional retained page images are `evidence/coremath_2_7_completion_FinalExplanation_TeacherKey-2.png` and `evidence/coremath_2_7_completion_SummaryTable-1.png`; other inspected images remain at the paths in the incomplete report.

Nonblocking layout limitations persist: a student rubric row and teacher key section break across pages; narrow resource columns create long sequence rows and continuation fragments. Prior complete contact-sheet survey plus targeted readable samples and this full canonical-text propagation check support this scoped PASS; they are not an exhaustive visual line audit. Teacher-only confirmations remain prerequisites, real pacing, practical equipment/accessibility/safety, honest observed/not-observed evidence and preview of broad optional resource matches. No partner ingestion, classroom acceptance, publication or fresh whole-workspace technical audit is certified here.

**Final verdict: remaining Core 2.7 standard-artifact gate PASS at the unchanged accepted fingerprint and exact artifact hashes.** Together with the preserved prior content/draft and technical-audit evidence, this permits root to package the two-unit second batch. No mathematical or production change was needed to close the interrupted PDF comparison.
