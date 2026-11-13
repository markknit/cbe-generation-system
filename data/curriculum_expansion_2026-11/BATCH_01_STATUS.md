# Batch01 — independently reviewed and built

13 November 2026. **27 new lessons have passed independent content and scoped final-artifact review.** Teacher classroom acceptance remains open. The 31 reviewed lessons in the frozen pilot are separate: 58 reviewed lessons across six units in total.

| Unit | Lessons | Registered checks | Final review files |
|---|---:|---:|---:|
| General Science 1.1: Introduction to General Science |7|6|9 DOCX+9 PDF|
| Essential Mathematics 1.1: Real Numbers |8|26|9 DOCX+9 PDF|
| Core Mathematics 2.6: Area of a Part of a Circle |12|22|9 DOCX+9 PDF|

Three standing independent reviewers inspected the source pixels, canonical records, every task/solution and assessment/rubric, plus actual output text and declared visual samples. Initial reports and correction histories remain in `reviews/batch_01/`. Source/authoring records are canonical JSON; temporary authoring helpers are not needed to continue.

## Findings and closure

Five confirmed finding instances were corrected:Science digital-evidence route and final timing (content pass1),Core project-template preparation and draft export-availability wording (content pass1),and Science irrelevant selected ARES resources (final-artifact pass). Essential had no confirmed content defect and passed its initial independent review. No fixed finding quota was used. All changed content/output was focused-rechecked; accepted fingerprints and evidence hashes are recorded under `reviews/<module>/content_acceptance.json` and the batch final manifest. Source-project adaptations, inference terminology alternatives and teacher-only judgements remain explicitly distinguished from confirmed errors.

Final-only cards are withheld from teaching StudentMaterials through `isolate_final_materials=true`. The separate AssessmentMaterials supplies only the final data. Full material/assessment teacher keys and pre-filled teacher summaries are distinctly separated from student handouts. General Science has no vetted local ARES matches:its per-module empty allowlist suppresses unrelated hotel-management/advanced-math matches while retaining the supplied evidence and official-source cards. An audit gate now rejects unvetted selected titles for curated modules. Production matching defaults were not changed.

## Verification and limits

- All 3 preflights and 54 registered calculations pass; independent reviewers also solved unregistered tasks and checked model/units/geometry, rather than infer correctness from the registry.
- Local contract passes 3 files / 27 lessons. All 3 exported JSON records pass current R1 in the final artifact audit.
- 18 pipeline tests pass, including actual Word material isolation and scoped resource curation. The old reference modules/texts remain checked with documented administrative wording differences; frozen original pilot files are unchanged.
- All 27 Word/PDF pairs pass current nine-type artifact audit, input/output hash checks, attribution, selected student/key checks, blank student summaries and final-resource policy. Content acceptance binds the actual canonical revision, not a passing preflight.
- Final reviewers checked complete canonical propagation/text/links and specific visual pages/contact sheets. Exact scope is in their layout reports. This is scoped desk review, not a claim of exhaustive visual inspection of every guide line or classroom trial.
- Cosmetic pagination remains:some standard table/rubric rows split across pages, long fallback-resource blocks inflate the standard guides, and Core CM211 has a two-line continuation. Text is intact and compact guides provide the concise lesson reference. These are recorded as nonblocking print improvements, not silently counted as missing content.

Teacher checks remain for prerequisites, realistic 40-minute pacing, construction/measurement setup, accessible calculator/device stations, individual observation and physical/digital skill evidence. Print-only/diagram work is not proof of hands-on or device competence. No enduring attitude change, employment qualification, medical diagnosis or broad unfamiliar-domain transfer is inferred from desk-reviewed tasks. Source adaptation and actual practical safety remain local teacher decisions.

Partner R1 ingestion support is still a separate delivery blocker; see `evidence/batch_01_partner_verdict.json`. No partner or production files were changed, and nothing has been pushed, promoted, published or sent to Drive. No separately billed model-generation API calls.

## Continuing work

Thirty-seven units remain undeveloped:three next sources verified (GS 1.2 The Cell,Essential 1.2 Indices,Core 2.7 Surface Area and Volume of Solids),27 located sources need transcription checks,and seven Core units remain source-blocked. The source inventory’s 40-unit count is the original expansion queue, not the current work-remaining count; use `inventory/progress.json` for progress. Final remaining lesson counts depend on explicit source allocations/justified teaching plans, not old eight-lesson defaults.

The user’s earlier three-reviewer instruction carries forward under the remaining-lesson authorization; no repeated routine review permission is needed. Subordinate reviewer runtimes cannot access the usage endpoint:root centrally verifies at least every 5 minutes and before reviewer batches. Do not request an escalation or wait on approval for a local meter read. A fresh root reading supplies the team; unknown usage stops new work. At≤10% all work reaches the next small clean boundary, then `/update`, a local handoff commit and an ended turn.
