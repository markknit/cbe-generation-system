# OpenAI-only pilot: build and internal-check report

2026-11-12. **Draft production is complete; independent comparative review is pending.** This demonstrates a working authoring/export process. It does not yet establish that its content is more accurate or less expensive than the earlier approach.

## Review first

Open the compact teacher guide with its Student Materials and Materials Teacher Key.

- [Essential Mathematics guide](outputs/PDF/Codex_Essential_Mathematics_Commercial_Arithmetic_1_CompactTeacherGuide.pdf)
- [Core Mathematics guide](outputs/PDF/Codex_Core_Mathematics_Area_of_Polygons_CompactTeacherGuide.pdf)
- [General Science guide](outputs/PDF/Codex_General_Science_Acids_Bases_and_Salts_CompactTeacherGuide.pdf)

Standard CBE lesson sequences, student assessments, assessment teacher keys, summaries and structured exports are also supplied. Treat the entire package as a teacher-review draft.

| Subject/sub-strand | New design | Old corpus design | Compact guide |
|---|---:|---:|---:|
| Essential Mathematics 2.8, Commercial Arithmetic 1 |9×40=360 minutes|8×40=320 minutes|10 pages|
| Core Mathematics 2.5, Area of Polygons |12×40=480 minutes|7×80+1×40=600 minutes|13 pages|
| General Science 2.4, Acids, Bases and Salts |10×40=400 minutes|4×80+4×40=480 minutes|11 pages|

These are pilot lesson allocations, not official counts. The longer lesson count does not imply more teaching time; the earlier Core and Science units used double periods. Teacher checks of prerequisites, pacing and sufficient practice are outstanding. The Core selection changed because the available source PDF obscures the Trigonometry 1 requirements; Area of Polygons has readable source pages and a baseline corpus module. This changes the comparison with the earlier three-module API pilot.

## What was built

- Three source records with original PDF paths, hashes, visible printed page numbers, crops and transcribed outcomes/competencies/values/PCIs.
- Three blueprints mapping 19 curriculum outcomes to teaching tasks and assessment evidence.
- 31 fresh 40-minute lessons, authored in this Codex session, with explicit companion materials and teacher solutions. Earlier lesson prose was not used as the authoring source.
- 47 registered arithmetic checks; repeated selected results are populated from executable calculations. These checks do not establish that every unregistered claim, formula setup or teaching choice is correct.
- Five geometry sheets drawn from explicit dimensions and labels.
- 21 Word documents and 21 PDFs: standard lesson sequence, compact guide, student assessment, assessment key, summary, student materials and materials key for each subject. Three contract JSON exports are separate.

The compact guides put each lesson on one page, plus a unit overview. The unchanged standard renderer produces 51/39/43 pages for Core/Essential/Science because resource-search blocks expand its phase table. The compact guides avoid repeating those blocks; the standard exports retain the existing format and structured resources.

## Verification results

- Local corpus contract: PASS, 3 modules/31 lessons.
- Current R1 JSON Schema: PASS, all 3 exports, zero schema errors.
- Registered calculations: PASS, 47 of 47; all 31 phase-time totals equal 40 minutes.
- Declared teaching/assessment coverage: all 19 outcome identifiers mapped. This checks mapping records, not whether the activities genuinely achieve the outcomes.
- Resource-link gate: PASS for all 3; T1–T4, dead-link and shape counts 0. This is not a new live network check or human viewing of every recommendation.
- Cross-document gate: PASS for all 3 using the pilot’s own review-log directory; original-corpus review logs are preserved.
- PDF conversion: 21 of 21 present. Text scan found no unresolved template tokens, undefined/NaN/FILL/replacement-character markers. Sample standard-layout, material-diagram and compact-guide pages were visually inspected; this was not an exhaustive page-by-page inspection.
- Partner rendering/preview: all 3 bundles generated with no unrendered multi-row tables. **Partner ingestion compatibility: BLOCKED.** The installed partner schema accepts 1.0.0 and rejects 1.1.0 plus each fourth-level belowExpectations key. The contract-drift command exits 0 for a report containing 15 drift findings, so its wrapper’s “PASS” must not be read as conformance. The corpus-resource gate correctly failed. No downgrade or edit to the partner checkout was made. See evidence/lesson3_checks.log.

## Findings and remaining quality work

Internal checking corrected two General Science defects before this build: the water-losing example now explicitly identifies a hydrated salt, and the illustrative initial pH now matches the stated introductory strong-acid concentration model. The ledger is reviews/internal_review.json. Independent error counts are unavailable; do not compare these two writer-found defects with earlier model-review counts as if they measured the same thing.

General Science practical work is conditional on local equipment, trained supervision, risk assessment and disposal arrangements. Evidence-card fallbacks explicitly do not demonstrate hands-on skill. No school laboratory has been inspected. Source safety/science references and access limitations are recorded; teacher risk assessment remains necessary.

A fresh reviewer should independently solve the exercises, verify source fidelity and actual coverage, trace references, check scientific explanations, and assess practical/pacing feasibility. Reviewer-agent delegation was requested as an optional preference during this run; no answer has been received and no reviewer agents were started. Internal author review is not an independent review. Matched baseline review and teacher correction-time measurement are also outstanding.

## Expense evidence and decision

All AI authoring occurred in Codex.No separately billed model API calls were made by this workflow. Local scripts performed arithmetic, document assembly, matching and validation. Subscription usage is a real cost; its exact credits and monetary equivalent are not exposed to this session. The earlier API pilot’s 7.65 USD spend is separate.

There is therefore no defensible per-accepted-lesson or 43-module saving yet. The next evaluation needs actual usage readings before/after a bounded reviewed module, reviewer correction effort, and a comparison at similar curriculum scope and teaching time. The earlier 110–130 USD estimate does not transfer to this workflow.

**Decision at this checkpoint:** the production route works and provides inspectable source/material/solution records, with a more economical printed guide. Keep it as a pilot until independent review resolves content findings and teachers check feasibility. Partner R1 conformance is a delivery dependency. Wider generation and promotion have not started.
