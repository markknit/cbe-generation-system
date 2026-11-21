# Per-unit source override code review

Verdict: **PASS for the scoped source-preparation change**. No confirmed blocker or false-acceptance path introduced by this diff was found. No production preparation run, author/pipeline edits, source acceptance, build or render of curriculum outputs was performed. Only temporary tiny source-PDF fixture renders and new review evidence were written.

Reviewed the complete `scripts/prepare_curriculum_sources.py` and its diff against HEAD `2a769fa5a3ad3ee629f5833df5dba2a021ebd98a`, plus `config/curriculum_source_sections.json`. All original subject PDFs,section coordinates,render DPI and pixel width are unchanged. Config adds exactly seven overrides:coremath1.1–1.3 and2.1–2.4. All seven were blocked in the frozen HEAD inventory and absent from the original Core section map; no accepted unit is redirected.

## Findings and proof

Per-unit override correctly selects the replacement PDF path/hash,independent150dpi replacement render,matching OCR-line bank and override crop coordinates. The original base render/line bank remains the default for every nonoverridden unit. Replacement render is cached by resolved input-path string across units; crop geometry uses that image's width/height and rejects negative,reversed or beyond-height bounds. Records continue to identify physical PDF page1,appropriate PDF hash,crop rectangle,crop hash and candidate OCR hash. OCR lower bound is inclusive and upper bound exclusive. New located packs remain authoring_ready=false until existing source/verification/evidence checks succeed. OCR itself is clearly labelled candidate,not accepted verbatim source.

`--reuse-render-dir` still reuses original `cbe-prep-<subject>.png` renders. Overrides intentionally render their replacement PDF once even in reuse mode;the flag does not promise to skip every pdftoppm call. pdftoppm must therefore remain available. The PDF is a one-page screenshot capture,matching the hardcoded first-page flow. Read-only pdfinfo gives595.44×21691pt,consistent with1241×45190 at150dpi; all seven configured integer rectangles fit. The separately supplied PNG is1799×65535,so using a render of the designated PDF instead of directly cropping that PNG avoids coordinate-scale mismatch. This review does not certify the actual source wording/competency completeness of each new crop;the separate pixel/transcription gate remains required.

## Isolated regression coverage

Five scenarios,25 assertions all pass. Actual pdftoppm and Pillow execute against tiny one-page PDFs in temporary roots,with the frozen HEAD code first preparing the reference packs and accepting three fixture units through valid source/evidence bindings. The changed code then runs against those same roots.

- Fresh mode:three original accepted units retain byte-identical source,verification,materials,blueprint,manuscript,crop,OCR and per-unit inventory files;all three content fingerprints are identical and readiness remains verified. Both previously blocked units use the replacement PDF/hash/crop/OCR and stay unaccepted. Two base renders plus one shared replacement render occur.
- Reuse mode:the same preservation,selection,bounds and readiness assertions pass;only the shared replacement render executes. Boundary OCR lines at start/end−1 are included;before/end lines and old-bank content are excluded.
- Negative start,beyond-image end and incorrect replacement width each raise the expected explicit ValueError rather than creating a misleading crop for the failing unit.

Six additional static config checks pass:all old config unchanged,exact seven overrides,all formerly absent sections,single shared replacement PDF,all valid integer bounds,and all target units previously blocked. Unchanged nonoverride code/input mappings plus fixture identity support preserving old accepted packs. This is not a claim that a production rerun has already been performed or all real old crops have been rehashed after one;root should retain its before/after frozen-file check when running preparation.

## Limits

The preparation script intentionally refreshes inventory/candidate files;it is not an atomic transaction and a late invalid input can leave earlier units already refreshed (existing behavior). It never edits canonical source/transcription,materials,blueprint,manuscript or verification records. Existing preservation relies on retaining the same original PDFs/exact cached renders and renderer/encoder environment;source verification will expose crop mismatch. The added bounds check rejects rather than silently pads an invalid old or replacement rectangle. Trusted config/OCR generation and human source verification remain separate. No generic multi-page override or supplied-PNG override is claimed.

## Exact bindings

- `scripts/prepare_curriculum_sources.py` — `da02156b83ec285a8ac43482de69ad46716ac05499e3f1867017f6a624121e47`
- `config/curriculum_source_sections.json` — `c837d322e5203f2d7976960a7172af1afb6f9575c30f1100fe82a156d8628360`
- `CBE_Curriculums/Grade 10/STEM/Grade10_CoreMath.pdf` — `700b55379210dda0ee24561d43a872f965eba9568ec8092b6e9116d7f3609b2c`
- `data/curriculum_expansion_2026-11/inventory/coremath_new_capture_ocr_lines.json` — `a2993790715dbcb29c9bea6c6e42505c64f380999ecad4fa10c2bd4a3cda6e52`

Evidence: `reviews/batch_07/evidence/source_override_core27/fixture_checks.py`, `fixture_results.json`, `binding.json`, `diff_vs_HEAD.patch`, `old_prepare.py`, `reviewed_prepare.py`, `reviewed_config.json`. Temporary roots were removed. No accepted production files were modified.
