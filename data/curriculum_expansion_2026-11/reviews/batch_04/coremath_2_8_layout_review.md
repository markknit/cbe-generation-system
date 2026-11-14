# Core Mathematics 2.8 Vectors I — independent final artifact/layout review

**PASS for all nine current Word/PDF types,2026-11-14UTC. New confirmed artifact errors:0; unresolved confirmed errors:0.** Canonical fingerprint independently rechecked unchanged: `55241dac6a6d71774bfa105978bd7017128e421e2f1c0507284cb37685c2e53c`. The accepted initial review remains immutable; its task/source/math work was not repeated. No content, output or acceptance JSON was edited by this reviewer.

Root supplied87% weekly allowance at02:41UTC and owns usage checks. Root's post-render metadata curation preceded this final review, removing higher-level/out-of-scope resource selections without changing canonical content. This verdict concerns the corrected current files, not the preserved initial resource selections.

## Exact current artifact identity

Independently computed all18 hashes from the actual files. All five draft companion Word hashes also match initial content-review binding evidence.

|Type|PDF pages|DOCX SHA256|PDF SHA256|
|---|---:|---|---|
|CBE_LessonSequence|55|`9974640f876e97a9401ccd10ae905393896d1c1f41884b17c93628fb777fdeb2`|`dfa06c6c583ab827742448cb841fdf778653dec6d96f53a7109f86632e4ffe8c`|
|CompactTeacherGuide|14|`dcbbc8ca82b4cc3f435af1757591f4c75e2b3491ef691b639037208f3fb3265b`|`c85999be4217264bf2d3ed8949ff5ffa904b3691aecc514c1854bc1845ff93be`|
|StudentMaterials|4|`3ccde0060b4ba7b5a17e0e1f2faec47593f8d29b358b66d981e2295b3ddcfb5e`|`7397d714f423e13c7c58f123eff5e58e475ad37cc6edead9491d6e1a60085b7c`|
|MaterialsTeacherKey|6|`8d95969886d953d907da9d065bf75fabcd4219b37b5ba7a3126c524e7fd3b929`|`7b4d2ec336b2bcc9593ae9908cd7a1f919bd170e94ccce1acb376ec5715475da`|
|FinalExplanation|6|`721070502a403724ff4af3c11d5a9624336b26f52ea9176635db74100a45e9f8`|`4a26bab6d4c36226bc2249df9b9b8c29129a363977a59519af44183e707656a0`|
|FinalExplanation_TeacherKey|3|`a0735e9f3d71d8c348db89612c7be6390022c39ca98e79209f39e030a040f0e2`|`33668eb4d4c17203005cf883449d5a64529870406d786191ca01ab1f20ea8192`|
|SummaryTable|3|`98fa55bfe055d168fe6d1efc17c22e8c634d273eea74264958fe34c2e51520fe`|`59821dbadaf8746606cc18121924249d6701f32645f0760782050b81c819492b`|
|StudentSummaryTable|2|`3da118b4de73a41294495e9d8e389cc1f82d52a6f69281c937e005beea8a6733`|`4f46d93a68a10e67aa46ad63b4605f438ec9fb21a165aa913a104b05f926bf39`|
|AssessmentMaterials|2|`e0c8b53f62c10ea3bfefcb7e8e4e944d88f1d59c0ea1ce13ed307caada2456e5`|`ca2578a9078de409462aeef9ca34f1317bc289ea450e6f3083824c20622a212b`|

## Canonical propagation and assessment isolation

`evidence/coremath_2_8_artifact_review_check.py` and its JSON provide reproducible actual-file checks:

```bash
venv/bin/python data/curriculum_expansion_2026-11/reviews/batch_04/evidence/coremath_2_8_artifact_review_check.py
```

**886/886 Word and886/886 PDF canonical checks pass.** This covers all13 lesson titles,260 phase entries, reflections and rendered overview/outcome/preparation fields in the full sequence/guide; all39 summary entries in both full sequence and teacher summary; student/key instructions, four prompts, four criteria and all16 level descriptors; all four teacher exemplars; and all student/teacher material-card text in its correct companion.

PDF checks retain every non-whitespace character.870/886 match after collapsing whitespace/joining retained-hyphen line breaks;16 additional strings match with whitespace ignored because wrapped algebra/long punctuation-separated lists acquire PDF extraction spaces. Nine entries use per-column streams to rejoin same-cell continuation across pages/intervening columns. No operator, sign, exponent, word or punctuation was removed to force a pass. Direct visual samples below check readable notation and the relevant continuations.

Separately verified actual table contents: four final answer rows contain only `Write your answer here:`; all13 student summary rows have three empty response cells. Final exemplars are absent from FinalExplanation, StudentMaterials and AssessmentMaterials in actual Word/PDF. VX13 is absent from teaching StudentMaterials and released in AssessmentMaterials with an empty grid and no teacher answers. Teacher materials contain the labelled solved preparation, and the final key visibly says not to give it to students. Final phases consistently withhold hints, comparisons and answer discussion until collection. Attribution containing ChatGPT/Codex andOpenAI is present in Word XML and PDF text for all9types.

## Grids in actual exports

`evidence/coremath_2_8_grid_export_checks.json` records actual Word embeds/extents and `pdfimages -list` output. The grid images extracted from StudentMaterials p2, AssessmentMaterials p2 and MaterialsTeacherKey pp2/6 are each1400×1480pixels and **pixel-identical** (RGB comparison) to the accepted blank grid asset. PDF horizontal/vertical effective resolution is222/222ppi for all four occurrences, preserving square coordinate intervals. Word extents5760720×6089904EMU preserve the1400:1480 asset aspect ratio. The accepted asset hash is `dcd7241fcb689dff493efacbbe0965e39e6689731ea5c59f12e30475f39379f1`.

Directly viewed actual grid-containing pages: axes/zero labels,−6to8 ranges and east/north labels are readable, cells remain square, and no answer arrows/points appear. Grid labels are not clipped. The blank grid is allowed in both teaching and final packs; it does not disclose final solutions. Material/data isolation is verified separately above.

## Actual PDF visual coverage

Rendered every current PDF page using `pdftoppm` at90dpi. Surveyed all95pages in14contact sheets, then directly inspected22 readable full-page samples:

|Type|All-page survey|Direct readable samples|
|---|---:|---|
|CBE_LessonSequence|55|8,24,36,51–53|
|CompactTeacherGuide|14|14|
|StudentMaterials|4|2–4|
|MaterialsTeacherKey|6|4,6|
|FinalExplanation|6|5–6|
|FinalExplanation_TeacherKey|3|1–3|
|SummaryTable|3|2–3|
|StudentSummaryTable|2|2|
|AssessmentMaterials|2|1–2|

All14contact sheets and22 readable samples are retained as36images under `evidence/coremath_2_8_*`, with paths/hashes/rendering method in `evidence/coremath_2_8_visual_manifest.json`. The18 artifact hashes above bind the PDFs actually rendered. This is a complete page survey plus targeted readable checks, not a claim that every line on every page was visually read.

No missing/clipped mathematical signs, overlapping text or lost answer/data separation was observed in these samples. Specifically checked negative/fractional scalar columns, midpoint/reference explanations, final coordinate data, full grid bounds, teacher results, blank student cells, collection restrictions and attribution. Student rubric criterion3 continues from p5 to p6; key criterion3 continues p2 to p3. Both retain complete descriptor text; criterion4 remains complete. SummaryTable has a lesson-title continuation onto p2 and licensing continuation onto p3; StudentSummaryTable repeats its header and places lesson13 on p2 with blank cells. Material-card continuations remain readable, includingVX11 across student pp3–4.

Nonblocking layout limits persist: narrow resource columns produce long rows/continuation fragments; some rubric words wrap within a long punctuation-separated expression; table/card/licensing rows split across pages. Text/notation is preserved and the inspected continuations are readable. These are not newly confirmed content-loss defects.

## Selected resources after curation

Read `evidence/coremath_2_8_resource_curation.json` with the preserved initial and final ledgers. Independently inspected the current structured export's25 non-null slots/17 unique titles. Every selected title matches the module allowlist: basic vector/scalar introduction, components/endpoints, addition/subtraction, scalar multiplication, magnitude, or translation. Higher-level3D vector fields, multivariable calculus/curve normals/transpose, trigonometric direction and kinematics titles from the initial ledger no longer remain selected in the current export.

This is metadata relevance/scope review. Some matches are prerequisite/adjacent-topic supports rather than exact lesson matches: e.g. addition media in the notation lesson and introductory classification media in the midpoint lesson. Actual sequence samples display “Related topic: not an exact match for this lesson.” Teachers should preview/limit/defer relevant portions. Titles about magnitude/direction or translation/slope may contain additional material; no full playback/content/language suitability claim is made and no optional media was fetched here.

All10 final video/reading slots are independently verified null. Generic teacher Search ARES fallback links remain; these are not selected media and do not authorise their use to provide final hints. Canonical independent-work restrictions govern the final.

## Limits and verdict

Content/source/math acceptance remains in `coremath_2_8_initial.md`. Root's nine-type technical audit is a separate recorded gate. This review adds actual propagation, grid export, resource-metadata and visual/layout evidence for the current files; it does not certify partner R1 ingestion, teacher classroom acceptance, full media playback, publication or a whole-workspace audit.

Teacher confirmations remain actual prerequisite readiness,40-minute pacing (especially plotting in final sections1–2), accessible grid copies, actual pupil-created chart/route checking and honest observed/not-observed optional digital work. A printed route is not evidence of real-world safe access or navigation competence.

**Final artifact verdict: PASS for these exact9Word+9PDF files at the unchanged accepted fingerprint.** No reviewer correction/rebuild is required. Root's prior metadata correction remains preserved separately; this verdict supports packaging its corrected current revision with the stated teacher/layout limits.
