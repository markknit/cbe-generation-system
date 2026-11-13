# Remaining curricula: preparation and operating guide

Prepared 2026-11-12. **Ready for a three-unit authoring trial; no new lessons authored.**

The reviewed pilot remains frozen at `../codex_pilot_2026-11/`. The reusable compiler was exercised on isolated copies under `/tmp/cbe-preparation-fixture`; those copies are regression evidence, not new curriculum deliverables. No production modules, partner files or Drive documents were changed.

## Readiness and source authority

`inventory/source_inventory.json` inventories all 43 existing unit IDs: three reviewed pilots and 40 remaining units. Of the remaining units, 33 have current-PDF crops; three of these have accepted transcriptions (`gensci_1_1`, `essmath_1_1`, `coremath_2_6`). The other 30 need visual transcription verification just before their authoring batch. Seven Core units are blocked by unreadable/repeated contents-page captures: 1.1–1.3 and 2.1–2.4. Do not use old OCR or old lesson prose to fill these requirements.

The local July 2025 PDFs are single physical pages containing tall page captures. Crop coordinates and printed page numbers are recorded separately. The old OCR disagrees with missing regions in the current Core PDF; the current pixels are authoritative. OCR files in this workspace are explicitly unaccepted candidates. The official [KICD Grade Ten page](https://kicd.ac.ke/cbc-materials/curriculum-designs/grade-ten/) links a Core file, but its owner disables download. No restricted-download workaround was attempted. A readable, permitted authoritative replacement is still needed for the seven blocked units.

`essmath_3_2` is an internal baseline ID; its located requirements table appears to print “4.2 Probability I”. Resolve that source/identifier discrepancy explicitly before authoring, rather than silently renaming it.

`source_status=verified` means the canonical source record was visually checked and its JSON, crop, PDF and written evidence have matching hashes. It does not accept lesson content. The trial's source JSONs retain source wording, including apparent grammar errors, with bullet layout/line breaks normalised. A fresh independent reviewer must compare the pixels again. Source lessons: Core 2.6 explicitly states **12**; the selected Science/Essential tables state no allocation. Old eight-lesson counts are inventory only. Forty remaining units do not imply a final count of 320 newly designed lessons.

## Canonical files and stages

Policy and trial selection: `../../config/curriculum_expansion_plan.json`. Progress: `inventory/progress.json`. Trial preparation plans: `blueprints/<module>.preparation.json` (plans, not compiler-ready blueprints).

1. Verify the source against the full crop, including continuation pages. Write `sources/<module>.json` and `<module>.verification.json`; record the PDF/crop/evidence hashes. Re-run `scripts/prepare_curriculum_sources.py` to refresh inventory. It retains verified status only while hashes match. The crop inventory can be regenerated from original PDFs with `venv/bin/python scripts/prepare_curriculum_sources.py`; OCR line metadata is a candidate cache, not a requirements source.
2. Write `materials/<module>.json` first: real student tasks, separately labelled teacher solutions/preparation, declared asset paths and registered numeric checks. Use `materials/diagrams/<card-id>.png` for compiler-inserted figures. Arbitrary `assets` declarations are checked for existence but must also be explicitly supplied/placed; declaration alone does not embed them. Independently solve every task; an expression matching its declared answer does not verify that the expression models the problem correctly.
3. Write `blueprints/<module>.json`: allocation rationale, prerequisites, lesson/outcome map, formative versus independent-final task map and rubric evidence. Honour an explicit source lesson count. A different count requires recorded user override evidence. Never invent a count for tables that do not provide one.
4. Write `manuscripts/<module>.json`: complete lesson prose, five phases totalling 40 minutes, supplied material references, final assessment, exemplars and four rubric levels. The existing pilot canonical records show the complete object shapes. Use JSON as the content source; do not create a new Python authoring program for every module.
5. Run preliminary checks. Fix confirmed issues before independent content review. Reviewers read source pixels, canonical records, tasks/solutions and rubric evidence before the author's self-review. Preserve original findings; distinguish confirmed error, reasoned alternative and teacher judgement. Reviewers save findings progressively. Any parallel reviewer launch needs user authorization; this preparation phase did not launch agents.
6. Correct confirmed defects, then obtain an independent focused recheck. At most two correction passes; record remaining teacher judgements rather than endlessly rewriting them. An unresolved confirmed content error prevents acceptance. Save the acceptance record only after the reviewer accepts the actual fingerprint.
7. Render final standard documents only after accepted content. Convert changed Word files, audit all nine Word/PDF types, then visually inspect the exported pages (tables, figure labels, clipping, assessment isolation, blank student rows, attribution). Record page/sample coverage and unresolved teacher decisions in `reviews/<module>/layout_review.md`. Structural/text audit does not replace visual review.
8. Package only the audited, visually reviewed outputs with source/review manifests and hashes. Packaging is a manual gated step in this version; there is no automatic publication or partner delivery. Run partner checks before any future delivery; installed partner R0 still rejects R1. Report the three-unit trial checkpoint before scaling.

## Running the pipeline

From the repository root, using `venv/bin/python`:

```bash
python3 scripts/check_codex_usage.py
venv/bin/python scripts/curriculum_pipeline.py check gensci_1_1
venv/bin/python scripts/curriculum_pipeline.py build gensci_1_1
# Independent review and content_acceptance.json must now exist.
venv/bin/python scripts/curriculum_pipeline.py render gensci_1_1
venv/bin/python scripts/curriculum_pipeline.py pdf gensci_1_1
venv/bin/python scripts/curriculum_pipeline.py audit gensci_1_1
```

The example is for the next phase; it will presently stop because no manuscript/material bank/compiler blueprint exists. `build` produces compiled lesson data and five review companions; it does not signify content acceptance. `render` adds four standard Word documents plus structured R1 JSON. Local link/consistency gates run in the standard renderer. Nine document types per unit: CBE sequence, compact teacher guide, student materials, materials teacher key, final assessment, final assessment key, teacher summary, blank student summary and isolated assessment materials.

Incremental builds hash canonical inputs, assets, attribution, relevant compiler/renderer/matcher code and the local resource DB version. Output hashes are checked too. Missing/modified output forces rebuilding; changing content invalidates review acceptance. PDF conversion uses an isolated temporary directory/profile and atomically replaces only successfully produced files. The final audit refuses stale builds/PDFs. The standard matcher uses the existing local resource index and makes no model calls. Resources in independent-final slots remain null; normal document fallback text remains available.

No command should target the frozen original pilot. For offline regression:

```bash
venv/bin/python scripts/test_curriculum_pipeline.py
venv/bin/python scripts/prepare_curriculum_fixtures.py --help
venv/bin/python scripts/curriculum_pipeline.py --workspace /tmp/cbe-preparation-fixture --fixture check
```

Fixture mode checks unchanged original canonical pilot content; it cannot certify new content. Rendering also makes a live usage check. `--fixture` is never an authoring acceptance shortcut.

## Explicit assessment/review evidence

Additional blueprint fields (use meaningful skill names in new units):

```json
{
  "assessment_tasks": [
    {"id":"F1","kind":"formative","outcomes":["a"],"materials":["A1"],"skills":["classify_and_justify"]},
    {"id":"I1","kind":"independent_final","section":1,"outcomes":["a"],"materials":["A9"],"skills":["classify_and_justify"]}
  ],
  "rubric_links": [
    {"criterion":1,"tasks":["I1"],"required_skills":["classify_and_justify"]}
  ]
}
```

These IDs make missing/overclaimed evidence detectable. An independent reviewer must still verify that the task actually elicits the declared skill. `section` and `criterion` are one-based. All rubric links must reference final tasks, while attitude/project evidence may be formative where the source requires it. The older `assessment_map` remains required for compiler compatibility.

`reviews/<module>/content_acceptance.json` records:

```json
{
  "verdict":"accepted",
  "unresolved_confirmed_errors":0,
  "content_fingerprint":"SHA-256 from content_fingerprint(workspace, module)",
  "evidence":[{"path":"repository-relative review/recheck path","sha256":"evidence file SHA-256"}]
}
```

Compute fingerprints with `scripts/curriculum_pipeline.py`'s `content_fingerprint`, imported with `PYTHONPATH=scripts`. Evidence must describe the actual accepted revision. Acceptance is a procedural reviewer judgement with hash binding, not cryptographic proof of reviewer identity. Record reviewer, findings, correction pass and any teacher-only judgement in the linked report; do not mint acceptance from a passing preflight.

## Checkpoint and efficiency measurement

Update the progress ledger after each small saved unit/stage. Record actual lesson count, elapsed active time, confirmed findings, correction passes, unresolved teacher judgements and weekly quota before/after each batch. Account quota includes other concurrent use; do not present its difference as exact per-unit usage or monetary savings. Teacher correction time is unknown until measured.

The 10% weekly threshold remains in force: check before units/reviewer batches, after units and at least every five minutes of active work. Unknown usage stops new authoring/reviews. At or below10%, take the next small clean boundary, execute the project's `/update` workflow, commit the exact handoff locally and end the turn. `/restart` verifies; explicit resume plus fresh permitted quota resumes. No automatic account switch, credit purchase, push, promotion or Drive publication.
