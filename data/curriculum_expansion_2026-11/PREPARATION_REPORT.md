# Preparation checkpoint — 2026-11-12

**Tooling and the next three-unit trial are prepared. No remaining lessons have been generated.** Full-curriculum source verification remains staged by batch, with seven Core units blocked pending a readable source.

## Delivered

- Inventoried 43 existing unit IDs: three completed pilot units (31 reviewed lessons) and 40 remaining units. Of these 40, 33 have current-PDF source crops, three have visually accepted exact source records, 30 await transcription checks and seven lack readable current-PDF requirements. See `inventory/source_inventory.json` and `inventory/progress.json`.
- Verified the next trial's source packs and wrote preparation plans: General Science 1.1 Introduction to General Science, Essential Mathematics 1.1 Real Numbers, Core Mathematics 2.6 Area of a Part of a Circle. Core source states 12 lessons; the other two tables state no allocation. Plans cover prerequisites, real material/solution requirements, outcome evidence and review risks. They contain no lesson manuscripts.
- Generalised the reviewed compiler to canonical source, blueprint, material and manuscript JSON. No per-unit Python authoring script is required. All work stays in an isolated expansion workspace.
- Added preliminary source/asset/reference/arithmetic/time/coverage checks, explicit formative/final assessment tasks and rubric links, source/count provenance checks, placeholder checks, independent-assessment template guards and hash-bound content acceptance before standard rendering.
- Added incremental rebuilds and PDF conversion: changing a unit rebuilds affected outputs; unchanged inputs/current outputs skip work. A failed conversion cannot pass by reusing an old PDF. Final audit rejects stale/missing builds, verifies nine document pairs, current R1, attribution, selected student/key separation checks, blank student summaries and independent-final resource policy.
- Saved a three-unit batch policy, two-correction-pass review procedure, metrics fields and checkpoint/handoff instructions. New content still needs substantive independent review and final visual review. Automated validation cannot establish task correctness, safety, assessment meaning or classroom pacing.

## Verification

- 16/16 offline mutation tests pass, including deliberately bad answers, missing assets/cards/source evidence, source changes, overrun phases, overclaimed rubric evidence, stale content acceptance, modified fixture content and changed/missing cached outputs. Test log: `evidence/pipeline_tests.log`.
- Three isolated copied pilot modules compile to exactly the reviewed data objects (31 lessons, 47 registered calculations). All 27 Word body texts match after two administrative wording normalisations; no teaching/assessment content was changed.
- All 27 Word/PDF pairs pass artifact audit; all 27 PDF page counts equal their reviewed references. Sample page 1 layouts from three document types/subjects were visually checked with no clipping/overlap observed. This regression sample does not claim a fresh full independent review.
- An unchanged rerun skips all three content builds, all three standard builds and all PDF conversion (`evidence/fixture_cache.log`).
- All 157 tracked files in the frozen pilot are byte-identical to the preceding commit. The historical untracked Review_Package extraction was preserved/excluded. Production and baseline modules were untouched; no separately billed model calls, push, publication or partner change.

## Source blocker and next checkpoint

Blocked: Core 1.1,1.2,1.3,2.1,2.2,2.3,2.4. The local PDF repeats contents-page captures in place of requirements; older OCR cannot validate these units. The official KICD page links a viewable file whose owner disables download; the Drive connector could not retrieve it. A permitted readable authoritative copy is needed. Do not invent requirements, rely on the old generated lessons or work around the owner's restriction.

The next authoring phase is the three selected units, followed by a report/checkpoint before scaling. Source acceptance for the other 30 located units should happen immediately before their batch; blocked units stay out of the queue. Resolve the Essential Probability internal/source identifier discrepancy before its batch. New lesson totals cannot yet be stated: baseline 320 is not an approved new allocation.

The 10% weekly clean-stop policy remains active. Last prep reading: 41% remaining at 2026-11-13 07:54 UTC (dated account-wide observation, not a permanent value). `/restart` must obtain a fresh reading. Teacher acceptance and partner R1 ingestion remain open; the installed partner R0 still rejects current exports.

Operational instructions and acceptance formats: `README.md`. Takeover: `../../HANDOFF_remaining_curricula_2026-11-12.md`.
