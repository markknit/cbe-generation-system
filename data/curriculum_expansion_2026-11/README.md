# Remaining curricula: preparation and operating guide

Updated 2026-11-14 22:08 UTC. **PAUSED at the requested2% threshold.** Both new Core captures resolved all seven source gaps;all40 expansion sources verified. Packaged:36expansionunits/430lessons,pluspilot31 =39units/461lessons. Authored/contentaccepted:38expansionunits/456lessons,pluspilot31 =41units/487lessons. Core2.1 finalPASS awaits packaging;Core2.2 readablevisualreview pending;Rotation materials prepared;Trigonometry1 unstarted. See `BATCH_07_STATUS.md` and `evidence/batch_07_pending_at_quota.json` for exact resume actions.

The reviewed pilot remains frozen at `../codex_pilot_2026-11/`. The reusable compiler was exercised on isolated copies under `/tmp/cbe-preparation-fixture`; those copies are regression evidence, not new curriculum deliverables. No production modules, partner files or Drive documents were changed.

## Readiness and source authority

`inventory/source_inventory.json` inventories all 43 existing unit IDs: three reviewed pilots and 40 expansion units. All 40 expansion units now have current-PDF crops and accepted transcriptions. The original seven Core capture gaps (1.1–1.3 and2.1–2.4) are now resolved by the newly supplied PDF/PNG. Their per-unit source overrides preserve all prior source identities and packages. Only Core2.3and2.4 have no manuscript;Core2.3has materials prepared. Five newly written Core units are at the exact stages in Batch07. Use the new source crops and bound transcriptions, not old OCR or lesson prose.

The local July 2025 PDFs are single physical pages containing tall page captures. Crop coordinates and printed page numbers are recorded separately. The old OCR disagrees with missing regions in the current Core PDF; the current pixels are authoritative. OCR files in this workspace are explicitly unaccepted candidates. The official [KICD Grade Ten page](https://kicd.ac.ke/cbc-materials/curriculum-designs/grade-ten/) links a Core file, but its owner disables download. No restricted-download workaround was attempted. The user subsequently supplied fresh readable captures for those seven units; the restriction was not bypassed.

`essmath_3_2` is an internal baseline ID; its located requirements table appears to print “4.2 Probability I”. The completed package retains both identifiers and requires teacher/source confirmation of the “maximum of two experiments and two outcomes” interpretation before classroom implementation.

`source_status=verified` means the canonical source record was visually checked and its JSON, crop, PDF and written evidence have matching hashes. It does not accept lesson content. The trial's source JSONs retain source wording, including apparent grammar errors, with bullet layout/line breaks normalised. A fresh independent reviewer must compare the pixels again. Source lessons: Core 2.6 explicitly states **12**; the selected Science/Essential tables state no allocation. Old eight-lesson counts are inventory only. Forty remaining units do not imply a final count of 320 newly designed lessons.

## Canonical files and stages

Policy and trial selection: `../../config/curriculum_expansion_plan.json`. Progress: `inventory/progress.json`. Trial preparation plans: `blueprints/<module>.preparation.json` (plans, not compiler-ready blueprints).

1. Verify the source against the full crop, including continuation pages. Write `sources/<module>.json` and `<module>.verification.json`; record the PDF/crop/evidence hashes. For an incremental refresh, run `scripts/prepare_curriculum_sources.py --modules MODULE...`; the unfiltered command reconstructs inventories and can reset custom stage metadata. Preserve a before/after hash guard for completed work. Re-run the scoped command to refresh inventory. It retains verified status only while hashes match. The crop inventory can be regenerated from original PDFs with `venv/bin/python scripts/prepare_curriculum_sources.py`; OCR line metadata is a candidate cache, not a requirements source.
2. Use module-specific unique card IDs and check global `materials/diagrams` for unintended legacy-ID matches before building; inspect actual Word media. Write `materials/<module>.json` first: real student tasks, separately labelled teacher solutions/preparation, declared asset paths and registered numeric checks. Use `materials/diagrams/<card-id>.png` for compiler-inserted figures. Arbitrary `assets` declarations are checked for existence but must also be explicitly supplied/placed; declaration alone does not embed them. Independently solve every task; an expression matching its declared answer does not verify that the expression models the problem correctly.
3. Write `blueprints/<module>.json`: allocation rationale, prerequisites, lesson/outcome map, formative versus independent-final task map and rubric evidence. Honour an explicit source lesson count. A different count requires recorded user override evidence. Never invent a count for tables that do not provide one.
4. Set `isolate_final_materials=true` in the new blueprint to withhold final-only data cards from teaching StudentMaterials. Shared teaching/final cards remain shared only when explicitly justified. Write `manuscripts/<module>.json`: complete lesson prose, five phases totalling 40 minutes, supplied material references, final assessment, exemplars and four rubric levels. The existing pilot canonical records show the complete object shapes. Use JSON as the content source; do not create a new Python authoring program for every module.
5. Run preliminary checks. Fix confirmed issues before independent content review. Reviewers read source pixels, canonical records, tasks/solutions and rubric evidence before the author's self-review. Preserve original findings; distinguish confirmed error, reasoned alternative and teacher judgement. Reviewers save findings progressively. The user’s standing three-independent-reviewer instruction carries forward under remaining-lesson development. Preparation launched none; subsequent batches reuse the three reviewer agents. No additional authoring agents are authorized by that review instruction.
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

The example uses an authored draft. All 38 currently authored expansion modules have accepted fingerprints; future drafts must obtain their own independent acceptance before `render`. `build` produces compiled lesson data and five review companions; it does not signify content acceptance. `render` adds four standard Word documents plus structured R1 JSON. Local link/consistency gates run in the standard renderer. Nine document types per unit: CBE sequence, compact teacher guide, student materials, materials teacher key, final assessment, final assessment key, teacher summary, blank student summary and isolated assessment materials.

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

The active weekly threshold is2% (Mark's explicit change on2026-11-14; see `config/codex_usage_guard.json`). Check before units/reviewer batches, after units and at least every five minutes of active work. Unknown usage stops new authoring/reviews. At or below2%, take the next small clean boundary, execute the project's `/update` workflow, commit the exact handoff locally and end the turn; Mark will perform the full reset. `/restart` verifies; explicit resume plus fresh permitted quota resumes. No automatic account switch, credit purchase, push, promotion or Drive publication.


HISTORICAL QUOTA STOP2026-11-14 04:35UTC:remaining10/exit10/pause_requestedtrue.273expansionauthored/263finalPASS;21packages240lessons;Volume12+Stats11finalPASSpackagepending. Probability10draftunbuilt/unreviewed. Withfrozenpilot304authored/294reviewed.16nodrafts(7Coreblocked+9GS).24verifiedsources/9locatedpending. Superseded by explicit threshold change/resume recorded in handoff and latest STATUS log. Root/evidence/quota_pause_2026-11-14.json remains the historical stop snapshot.
