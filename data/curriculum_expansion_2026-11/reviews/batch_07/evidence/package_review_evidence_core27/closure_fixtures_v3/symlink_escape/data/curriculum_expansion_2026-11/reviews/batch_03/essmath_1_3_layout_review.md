# Essential Mathematics 1.3 — independent final artifact/layout review

**PASS for all nine current Word/PDF types, 2026-11-13. New confirmed artifact errors: 0; unresolved confirmed errors: 0.** Canonical content remains accepted at `1f02c60b4122722a1d83e9ad7476c0adb7a99bd749f914c7c673c64f7cea1c01`. The independent initial report remains unchanged. No content, output or acceptance JSON was edited by this reviewer.

Root supplied94% weekly allowance at23:24:44UTC and continues usage checks. Root's resource-curation finding preceded this final review; current output is the corrected revision. No new source/math review was repeated because the accepted canonical fingerprint is unchanged.

## Current artifact identity

All18 exact artifact hashes were independently computed from the actual files. The five draft companion Word hashes also match those inspected during initial content review; root rebuilt the four standard types after resource curation.

|Type|PDF pages|DOCX SHA256|PDF SHA256|
|---|---:|---|---|
|CBE_LessonSequence|39|`17873ecbd81adebb298fadb0bdb31ea3aa702f4aea481d98ef335957ceffa698`|`d2c5cd155bbb159458bbe5168d6e50fe6a2461fa5c725b5f6a2fcba0e55a5d51`|
|CompactTeacherGuide|10|`e73b8174f3839a9c68eecd87670f080ada024b85df34997f85df89291d350073`|`834d4cb53b400ffe19ddcee06a24f4f180cdaf7b396e4da14ad25f151aa3fbed`|
|StudentMaterials|2|`7e5bd3af2d543aea1f4050edaebc6e9b89fa83fea485d282397960cdcced2539`|`0ef9bd001988a64a099f870ba237d527971c20c7f81ae8141d44fd8bae2dca26`|
|MaterialsTeacherKey|3|`9454f67e5ca4c52563e5b0aa766d6489b915d25e2f89008ee04b74051bcba156`|`8aa000fa9b870b0dcc08dbffe553553fea973e41e59889f2db542ceb6e83cc57`|
|FinalExplanation|6|`c3f7ecb40e8c5372c2b275bbb22a16928cbd7e0efd237a9666b878523dbc03ed`|`bd63534ea3ef1e8db1541bce7fb88cbbe07fd0a7797fd602bf22850bcabfd5c2`|
|FinalExplanation_TeacherKey|3|`87c95d93950783017c6e9f0b5b25211f506148340f55ad9c9d0068b4fe06e5f4`|`b7c0f361389f115a4cf71a3e8ebcfb83256842cc3e53c26bd6683069f200669b`|
|SummaryTable|2|`156c7ca2f8488573e58153c2825b46c9dffff20f518a5edbab5e2ae8e6644831`|`8a28150b07688b5669718ab6673f0b103f4901c6592462283015af8f410e01b0`|
|StudentSummaryTable|1|`27ab5d19047d4e72c088117accb3b249ca42da96ad778ef1ab6b4d1126f83a94`|`2041d648bdfa2c1a9c8862044272b65686b15167823a408a7b55459792f1a508`|
|AssessmentMaterials|1|`326070c4e4a888ab12bbea975b12625fba725e5150e562fc3d875fc99be387a3`|`97ceef697f26f81be9247d1274e1533f5ec1d88e96b70f1118972ca13589e05a`|

## Canonical propagation and isolation

Reproducible evidence: `evidence/essmath_1_3_artifact_review_check.py` and its JSON result. From the repository root:

```bash
venv/bin/python data/curriculum_expansion_2026-11/reviews/batch_03/evidence/essmath_1_3_artifact_review_check.py
```

**620/620 canonical checks pass in actual Word and620/620 in actual PDF.** Coverage includes all9 lesson titles,180 phase entries, lesson reflections and rendered overview/outcome/safety fields in the full sequence; all guide phase entries and its rendered preparation fields; all27 teacher summary entries in both the sequence and summary document; student/key instructions, four prompts, three criteria and twelve level descriptors; every teacher exemplar; and all student/teacher material-card texts in their correct companions. OpenAI/ChatGPT/Codex attribution is present in Word XML and extracted PDF for all9types.

Word comparisons normalise whitespace. PDF comparisons use actual bounding-box text in reading order, with per-column streams for same-cell page continuations.608/620 pass after normal whitespace collapse/retained-hyphen line joining;12 additional entries require ignoring whitespace only because Poppler adds spaces at wrapped algebra/long comma-separated lists. No word, operator, exponent, sign or punctuation is deleted to make a match. Five entries use a column stream because a cell continues across a page or intervening adjacent column. Visual samples below confirm the corresponding text remains readable.

Separately inspected actual Word table cells: all four final student answer rows contain only `Write your answer here:`; all9 student summary rows have three blank response cells. Final teacher exemplars are absent from FinalExplanation, StudentMaterials and AssessmentMaterials in Word and PDF. QE9 and its final-only modelling data are withheld from teaching StudentMaterials and supplied separately in AssessmentMaterials. The full teacher materials key is clearly labelled and includes QE9 solutions for teacher preparation; the final key visibly says not to give it to students. All five final phases forbid comparison, hints and answer discussion before collection.

## Actual PDF visual coverage

Rendered every current PDF page at90dpi with `pdftoppm`. Surveyed all67pages in12 contact sheets. Then inspected18 readable full-page samples plus one bottom-of-page detail crop:

|Type|Complete page survey|Direct readable samples|
|---|---:|---|
|CBE_LessonSequence|39pages|8,20,35–37|
|CompactTeacherGuide|10pages|10|
|StudentMaterials|2pages|1–2; additional p1 bottom detail|
|MaterialsTeacherKey|3pages|2–3|
|FinalExplanation|6pages|3,5–6|
|FinalExplanation_TeacherKey|3pages|1–2|
|SummaryTable|2pages|2|
|StudentSummaryTable|1page|1|
|AssessmentMaterials|1page|1|

All contact sheets,18 readable samples and the additional detail are retained as31 images under `evidence/essmath_1_3_*`; hashes and rendering method are in `evidence/essmath_1_3_visual_manifest.json`. The current artifact hashes above bind the PDFs actually rendered.

No clipping, overlapping text, missing mathematical signs or inaccessible page continuation was observed in the samples. Specifically checked: final non-monic/zero-root prompt and blank answer space; student rubric continuation from p5 to p6; key section3 prompt continuation from p1 to p2; final isolation instructions; exact factor/sign notation in materials/key; actual attribution/footers; blank student table; and final phase rows. StudentMaterials p1's QE5 ending and footer are complete in the retained detail crop. SummaryTable's lesson7 title continues onto p2 while its response cells are on p1; the continuation is readable and the27 canonical summary entries are complete. Teacher key mathematical exemplars fit their cells without lost terms.

The contact-sheet survey is a complete page inventory/layout survey, not an exhaustive readable visual audit of every line. Exact text propagation covers all declared strings above; direct visual inspection is the stated sample.

## Resources after root correction

Read the root's preserved pre-review curation evidence and independently inspected the current export's14 non-null selected slots. The remaining five unique titles are `Solving quadratics by factoring`, its Kiswahili-dubbed counterpart, `Quadratics by factoring`, `Quadratics by factoring (intro)` and `Zero product property`. All selected titles are in the per-module allowlist. Quadratic systems, formula, square-root and complex-root solving titles removed by root do not remain selected in the current export. This closes root's earlier method/topic-scope issue for the inspected revision; it was not an error newly found in accepted canonical lesson content.

Some retained selections are ahead of the particular lesson sequence: Lesson2 models equations without solving, while its optional videos solve by factoring; Lesson4's optional zero-product reading anticipates Lesson6. Actual sequence pp8 and20 visibly label the resources “Related topic: not an exact match for this lesson.” They are supplementary metadata matches, not the required QE-card tasks. Teachers should preview and use only relevant portions or defer them until the taught method is appropriate. The English/Kiswahili title/source metadata does not verify language accessibility or full media content/playback; none was claimed or tested here.

All10 final video/reading slots are independently verified null. Generic Search ARES fallback links remain in the teacher sequence resource column; these are not selected media and do not override the final no-hints/individual-work restrictions. Optional links and their media were not fetched in this scoped review.

## Limits and final verdict

Nonblocking layout limits are long resource-column rows, continuation fragments and the noted rubric/summary/key page splits. Nonblocking classroom decisions remain prerequisite readiness, real40-minute pacing, accessible notation and preview/provision of appropriate references/media. Root's scoped technical audit is separate; this review does not certify partner R1 ingestion, classroom acceptance, publication or an unrelated whole-workspace audit.

**Final artifact verdict: PASS for the exact9Word+9PDF files above at the unchanged accepted fingerprint.** No reviewer content correction or artifact rebuild is required. Root's prior resource-curation correction remains preserved separately, with this review certifying the corrected current files and the stated coverage/limits.
