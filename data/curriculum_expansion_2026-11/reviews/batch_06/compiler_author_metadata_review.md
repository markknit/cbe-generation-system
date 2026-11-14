# Compiler author-metadata export fix — independent review

**SCOPED PASS. No blocking code finding.** Reviewed the complete current git diff in `scripts/curriculum/compiler.py`, its export/writer context, the R1 schema and pipeline gate. The change removes exactly the two named UNIT author notes and section-level marks from exported bundles. Canonical authored content and its fingerprints remain intact; other unknown keys still reach the strict contract validator.

Exact compiler SHA-256: `cf8b6f489a5c85b3870b2eafdc199d68bbfadde42433a7f6bad64421bc37a691`. Compared HEAD compiler SHA-256: `d25bd88ddd005f306ccc7a5628f6dd7afdf8eb57a641adb0dff17f59c4c09d92`. R1 schema SHA-256: `6a103c32ea4ef00dd919f73918e45cb0dbc7c597cb768f0a77d45ed93063e501`.

## Meaningful isolated regression

[Reproducible offline regression](evidence/compiler_author_metadata_regression.py) and [results/bindings](evidence/compiler_author_metadata_regression.json), evidence SHA-256 `db5035fdfd8ce66c3dbe63545745609bd459cbc0999bce7d5d7413e56f1313e8`, pass **46/46 checks** using old/new compiler code against isolated canonical copies of GS1.7, GS1.6, Essential2.7 and Core3.2. All three Word writer functions were stubbed; no Word/PDF rendering or frozen production rebuild occurred. Temporary module/check files were confined to a temporary workspace.

The test confirms:

- GS1.7 old export fails R1 only for the two UNIT extras and three section marks (four error objects, with the two UNIT names aggregated). The corrected export passes after adding an isolated, test-only complete null-selection resource map and syntactically valid dummy fallback. No resource recommender or real resource selection was run.
- Exact old/new bundle comparison permits only `UNIT.keyInquiryQuestions`, `UNIT.teacherConfirmationRequired` and `FINAL_EXPLANATION.sections[*].marks` omissions. All META, lesson content/timings, summaries, final instructions/prompts/exemplars/rubric and source learning-outcome text remain equal. The other three tested units produce identical complete old/new bundles.
- Injected unknown UNIT, section and top-level-final keys remain in export and fail R1. A UNIT-only excluded name injected at section level also fails. This verifies the change is path-specific and does not hide unrelated unknown authoring fields behind a broad allowlist.
- Every canonical input byte and content fingerprint remains unchanged by compilation. Independently changing each excluded note/mark in the isolated manuscript changes its canonical fingerprint even when the projected export remains equal. Thus these notes are still bound by content review rather than silently removed from the content source.
- GS1.7 inquiry wording remains in its canonical source and exported authoritative driving question. Teacher-confirmation notes remain canonical, and the blueprint's substantive confirmation list is unchanged. No clinical, project or source instruction was rewritten.
- Production canonical and existing GS1.7 Word files were hash-checked unchanged during the successful isolated run. No acceptance, cache, preflight, production audit or pipeline mutation command was invoked by this test.

## Code assessment and scope

The UNIT dictionary comprehension excludes a two-name set at the intended level. The new assessment/section dictionaries omit only `marks`; they preserve the other final fields and do not mutate the loaded canonical objects. The existing strict R1 gate is unchanged. Existing content signatures include compiler bytes, so derived outputs can be invalidated while canonical content fingerprints stay stable. The current authored-workspace contract requires complete final assessments; this review covers that supported input shape.

This is a narrow compiler/export acceptance, not a fresh whole-workspace cache or artifact audit. It does not resolve selected-resource relevance or certify classroom readiness. GS1.7 final artifact review will bind the next frozen snapshot after the parent removes the irrelevant resource selections. No production code/content/output or acceptance state was edited by this reviewer.
