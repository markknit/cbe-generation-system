# Core Mathematics 2.9 Linear Motion — independent final artifact review

**Scoped PASS, 2026-11-14 UTC: actual9Word/PDF pairs, canonical propagation, graph preservation, assessment isolation/blank responses, attribution and resource metadata. Confirmed artifact errors0; unresolved confirmed errors0; artifact corrections0.**

Accepted/current content fingerprint: `cc948a571d5a63e09dfc897b03b086ac0920876d4f4e9a3166b1342171642a2b`. Initial report remains unchanged at SHA256`25d5b8544130e7b65bd3f31975d408756bc54b5109379ea0a2f5ecaee5856673`; content acceptance binds that report and fingerprint with0correction passes. Source/math/content review was not redone. No canonical files, output files or acceptance records were changed or rebuilt. Root centrally monitors usage.

This review binds the actual18frozen files below, their current accepted inputs and prior audit snapshot. It does not certify a new whole-workspace build signature after concurrent optional Cell/compiler work. Such work does not change these reviewed bytes. All18hashes agree with `evidence/batch_05_coremath_2_9_artifact_audit.json` (SHA256`4404f03c7ef67681eb93f170e1b5854ae6d2709e2ef17744949f2bb18967cae1`). Canonical input hashes and all18artifact hashes were rechecked immediately before writing this verdict.

## Actual propagation and procedural checks

Independent read-only check: **822/822canonical fields pass in Word;822/822pass in PDF**, covering both lesson formats'12titles/phase entries/prose/reflections, all final prompts/instructions/exemplars/rubric levels, teacher summaries and every student/teacher material. Evidence and reproducible checker: `evidence/coremath_2_9_artifact_review_check.py` / `.json`.

PDF text was checked through bbox blocks and per-column streams to preserve table-cell continuations.791fields match global bbox order,22require whitespace-only character comparison,6match continued rubric columns, and3match a body stream excluding intervening footer text. Whitespace and retained line-end-hyphen spacing are normalised; mathematical glyphs, signs, punctuation and nonspace characters are retained. No confirmed canonical text loss was found. Extraction success is separate from visual layout evidence below.

- StudentMaterials contains LM1–LM11, including both interpretation graphs; LM12 is absent in both formats.
- AssessmentMaterials contains only fresh LM12 datasets/independent instructions; no teaching cards, teacher solutions or answer graphs. Blank squared paper must be provided separately as specified.
- FinalExplanation has all four prompts and four genuinely blank answer areas (only the answer placeholder). Final exemplars are absent from all three student-facing material/assessment documents. Teacher key has all four exemplars, including signed area, zero crossing and relative-rate answers.
- StudentSummaryTable has12lesson rows and three blank response cells in each; the teacher SummaryTable remains explicitly pre-filled. Both formats preserve this distinction.
- Lesson12 final phases prohibit comparison, hints and discussion until collection; final10selected video/reading slots are null. Generic teacher resource-search placeholders remain in the CBE template, but are not selected resources or assessment instructions. Keep those teacher lookups and the generic peer-support/differentiation table outside the independent test procedure.
- All9Word/PDF pairs contain SeaVuria, ARES, ChatGPT/Codex, OpenAI and BY-NC4.0 attribution/licensing strings. Readable footer and standard attribution samples show readable text without overlap.

## Graph preservation through export

The four actual PDF images (LM5/LM8 in StudentMaterials and MaterialsTeacherKey) were extracted and compared as RGB pixels with the accepted originals: **4/4pixel-identical,1400×960**. PDF image listings show222×222ppi, hence no axis stretch. Actual Word image byte hashes agree with the two accepted assets, and all four extents are5760720×3950208EMU, preserving1400:960 exactly. Details in `evidence/coremath_2_9_frozen_artifact_binding.json`.

Readable exported pages show complete tick labels/units/zero axes, straight-segment model notes, lines and points. LM5 is on StudentMaterials p2/teacher key p3; LM8 on StudentMaterials p3/teacher key p4. The nonzero initial displacement, negative ordinate range and velocity zero crossing remain intact. No final graph/data is embedded in teaching graph assets. Pixel identity preserves the independently accepted coordinate/scale check; this gate does not repeat the complete source/mathematics review.

## Actual visual coverage and findings

**Every86PDFpages was viewed in14contact sheets at90dpi.22selected full-page images were viewed individually at120dpi.** All36saved images and SHA256s are in `evidence/coremath_2_9_visual_manifest.json`. This is an all-page layout survey plus readable targeted review, not a claim that every word on every page was read visually.

| Document | PDF pages surveyed | Readable full-page samples |
|---|---:|---|
| CBE_LessonSequence |51|20,32,47,49,51|
| CompactTeacherGuide |13|13|
| StudentMaterials |3|2,3|
| MaterialsTeacherKey |6|3,4,5,6|
| FinalExplanation |6|4,5,6|
| FinalExplanation_TeacherKey |3|1,2,3|
| SummaryTable |2|1,2|
| StudentSummaryTable |1|1|
| AssessmentMaterials |1|1|

Sample choices cover graph pixels/labels, signed velocity/area/unit notation, final datasets/exemplars/rubric levels, blank response cells, independent final phases, attribution, and table/page continuations. Contact sheets show no blank/missing content page, gross truncation, image distortion or overlapping layout. Readable samples preserve minus signs, fractions-as-text and superscript²; no confirmed clipping or mathematical-glyph substitution was found.

Nonblocking presentation/use limits, preserved rather than hidden:

- Rubric criterion3 continues from student final p5→6 and teacher key p2→3. Same columns carry its remaining descriptor text, then criterion4 and attribution. The full descriptors are present/readable, but the continuation has no repeated header. Keep adjacent pages together when printing/marking.
- Teacher SummaryTable splits the Lesson6title at p1→2. Its three summary statements remain complete on p1; p2 begins the title continuation before Lesson7. This is an awkward title fragment, not content loss.
- Student LM5 prompt crosses p1→2 before its graph; LM8 prompt is on p2 and graph on p3. Teacher LM8 answer continues p4→5 and LM11 solution begins p6. Samples show the actual continuations; distribute complete page sets.
- CBE resource columns make lessons span several sparse pages, sometimes with narrow resource-only continuations. No canonical row text was lost. CompactTeacherGuide gives the shorter table alternative. Tight authored token spacing around some variables/numbers remains as supplied; print size/accessibility should be checked with actual learners rather than inferred from text extraction.
- Final blank answer areas are provided, while plotted work requires the separate squared paper. The one-page student summary has compact handwriting space; an enlarged/extra-sheet accommodation may be needed. Existing teacher pacing/access confirmations remain, particularly two final graphs within40minutes.

## Selected resources and final null slots

Current structured export SHA256:`33a61a24ea9304cc03a90e3c3a0b757245ba3cc52bfed35abc5942d865ad2ee3`, matching the root resource-review ledger. Independently inspected actual selection metadata:40video slots across Lessons2,4,5,7,8,9,10,11; no selected readings. Only two titles occur:

- “Interpreting direction of motion from velocity-time graph” —26slots.
- “Interpreting direction of motion from position-time graph” —14slots.

Both are attributed to Khan Academy(English–US curriculum) and fit the unit's signed one-dimensional graph interpretation. They are optional related support, not exact activities or substitutes for the supplied tasks. Some appear before their graph lesson or alongside relative-motion work; teacher preview and limited use remain necessary. No full-media playback/content or external-link availability is certified. Lesson12's five phases each have video=null and reading=null (**10/10null**), consistent with independent assessment isolation. Generic ARES search links are not mistaken for selected media.

## Exact18-file binding

All Word files are under `outputs/v2/Core_Mathematics/SS2.9_Linear_Motion/`, PDFs under `outputs/PDF/`, each prefixed `Codex_Core_Mathematics_Linear_Motion_`. Names below specify the document type. Hashes bind actual current files, not regenerated equivalents.

| Type | DOCX SHA256 | PDF SHA256 |
|---|---|---|
| CBE_LessonSequence | `821fa89ae646a31926c0cd0ccff58511b8c9f4bbc104eec95364f5fa8bfd68dc` | `64416c5af8e10c1cc95440097474c448cfe255e9d8ae1aaa7fadb1d0b27e5869` |
| CompactTeacherGuide | `18ea1177c3af2aaacb772cc8fb88b2043b66052409a281cfc0b16cab50f1002a` | `a7c23878ecaf465b7f007b1beeff04c205ed8dd27eb683593d0e6af1d3d528c2` |
| StudentMaterials | `1efbe0de72b19d983f3400f16fddf104c109a8e2ce85e8cec8a90f15e579cc46` | `4b924cb681ea6045439d258b9cd1356df081f4fe58e7114f69a225396159e4e5` |
| MaterialsTeacherKey | `be8ed84604f7c298c2ed2c225cb9008ef137c4fc50a254d5d94b00b6c6c88550` | `a7249560e10c26d52cd2849538238935385c554222b5e9b7f30ca1ffea5e355b` |
| FinalExplanation | `cdcc2a6dd1cde94210cdb6016966ed0819a9af269a3146cdb07fdfc2a2b2249c` | `e9199e13d827724d4942a1ec6df07acb96ea4261dd03c36d668bb82dae63bb30` |
| FinalExplanation_TeacherKey | `08171685018ef2c908f94c1c2f8b54d57cb05a0caeeb37aaae016269647b8ef7` | `e8a84c77177503cfedeb180f154100f2d4daa77dc4d256672005a0775476a551` |
| SummaryTable | `cbd6b0c40760def0534a7c3ac639f509ed7752b59b334bd45e4bb29007a37b98` | `2ee360031302c5dcdd32786e59040127c174e318f9f1ef9fdddd5b603b8eb04e` |
| StudentSummaryTable | `5a032838e30bdf3de5732aa581c6284f6d11e5976e1d130491daf8e491d495a5` | `6f85031522ae62d4cdbc2699a61b13df43998ff05a43d4916855988ec7f56092` |
| AssessmentMaterials | `b5a661ab8654b44ce6fea634116eb13b9dac120683e29eef8547513464f9dcca` | `1f8d089da4b1b8fa9824e6265cb1842c007d1e451c9a16dcc353a7e07627e854` |

**Final disposition: scoped PASS for the frozen9pairs above, unchanged accepted fingerprint and explicitly limited visual/metadata scope.** Content acceptance remains separate from classroom pacing/practical/digital evidence, media preview and any future partner-ingestion verdict. No required artifact correction or rerender was found.
