# Essential Mathematics 1.1 — standard artifact/layout review

**Status: COMPLETE — scoped final-artifact review PASS; no blocking regression found.**

Date:2026-11-13. Reviewer: same independent Codex agent; exact model identifier not exposed. This review covers the four newly rendered standard document types, following the separately completed five-type draft review. It is not a baseline audit or a re-solution of unchanged mathematics. Root supplied verified live usage24% at08:52:18UTC, EXIT0/no pause; review finished within the five-minute check interval without local usage escalation. No content, acceptance record or earlier report was edited.

## Accepted content and actual artifact comparison

Recomputed live content fingerprint with the repository `content_fingerprint` function: **e8310e22c9a00ae5c8a4104744c80a4894f9a5a8d3708f143eb1fad77f4b8539**. It matches `reviews/essmath_1_1/content_acceptance.json` and the parent’s accepted value. Earlier mathematical/content verdict therefore applies to the current canonical source/blueprint/materials/manuscript set.

Read actual DOCX body text and extracted PDF text for CBE_LessonSequence, student FinalExplanation, FinalExplanation_TeacherKey and teacher SummaryTable. Checked every canonical final instruction, section title/prompt and rubric descriptor against student DOCX; every exemplar as well against teacher-key DOCX: **zero missing canonical strings**. All five final-lesson phase instruction sets occur unchanged in standard guide DOCX. All eight lesson titles and their three canonical summary statements occur in SummaryTable. PDF/DOCX word comparisons show only PDF line-end hyphen joins (e.g. “whole-portion”→“wholeportion”); no lost mathematical instruction or answer text found.

Actual student FinalExplanation retains “Work independently using RN8 and a calculator; no teaching cards”, exact-fraction/intermediate-work/≈ requirements and observation without calculation hints. Teacher key explicitly says “do not give to students”; expected rational forms, operations, reciprocals, full-portion count and remainder match accepted text. Student FinalExplanation contains no teacher exemplar or distinctive final results such as55/24,7/60,√3/3 or0.577. Its rubric describes expected performances without inserting numerical solutions. RN8 is distributed separately in AssessmentMaterials; teaching StudentMaterials remains withoutRN8, and teacher SummaryTable is distinctly “Teacher Reference (Pre-filled)”. No new final-data/key leakage found.

## Visual coverage and layout

CBE_LessonSequence: **all35pages** broadly scanned as a labelled5×7 contact sheet at thumbnail size; detailed readable pages1,19,23,31–34 (overview, reciprocal teaching start, fictional-context teaching start, complete four-page independent final lesson). Contact scan detects broad pagination/bounds, not every small line. Detailed text checks extend beyond those visual samples.

Student FinalExplanation: **all5pages** inspected at1300-pixel scale, including actual negative signs, square exponents, reciprocal radical and exact-working prompts. Four answer areas provide substantial writing room. FinalExplanation_TeacherKey: **all3pages** inspected in detail, including exemplar cells and complete rubric. Teacher SummaryTable: **both2pages** inspected in detail. Headers, tables, key labels, source outcome wording, ≈/√/−/² symbols and OpenAI attribution are legible in the inspected images; no clipping, collision or missing text found.

**Minor nonblocking layout observations:**

- Student final rubric criterion3 splits between pp4–5, stranding the end of “observed device use is accurate” on p5. Its text is present and recoverable; keeping rubric rows together would improve print usability.
- Teacher-key section3 prompt continues from p1 to p2; exemplar remains on p1. SummaryTable’s eight lesson rows split6/2 over two pages, with text intact. These are pagination choices, not incorrect/missing content.
- Standard CBE rows are stretched over several pages by repeated optional resource-search fallback text. Each lesson currently occupies four pages. The previously checked compact guide provides the concise working reference. Reducing repeated fallback blocks would reduce print bulk but is not required for correctness.

## Resources and independent final conditions

Inspected actual `outputs/_link_matching/v2/Essential_Mathematics/SS1.1_Real_Numbers/Codex_Essential_Mathematics_Real_Numbers.json`: **no selected resource in any of80slots** (8lessons×10video/reading slots), including **all10final-lesson slots null**. Therefore there is no selected resource title whose relevance or answer leakage needs validating in this unit. This does not mean the whole ARES library contains no useful material; it means this render selected none.

Standard guide still displays clearly labelled generic “Search ARES” fallback links and “No closely matching…” text; they are optional search entry points, not supplied teaching dependencies. Final student document has no selected supplementary resource. Its RN8-only/no-teaching-card instructions and all five final guide phases explicitly require individual work without hints/comparison/answer discussion before collection. Teachers should keep optional searches closed during independent work. The curriculum’s required local numerical tasks, calculator use and data do not depend on discovering a resource through these links. No live-link availability certification is implied by this scoped check.

## Verdict and residual teacher limits

**PASS for the four newly rendered types at the hashes below.** No correction pass is required for a blocking content or artifact defect found here. This completes the requested independent standard-artifact/layout check alongside the initial five-type review; root’s separate27-pair batch audit is not reproduced or independently relabelled as this review’s work.

Classroom confirmation remains necessary: root-capable/accessibly configured calculator availability, feasible individual observation, prerequisite support, actual40-minute pacing and print legibility on school equipment. The accepted rubric still has close3/4descriptors, so moderation examples may help consistent marking. This is desk-review acceptance of the inspected artifacts, not a claim of classroom effectiveness, complete mastery, cost savings or official endorsement.

## Current artifact hashes

Common filename prefix: `Codex_Essential_Mathematics_Real_Numbers_`. DOCX directory: `outputs/v2/Essential_Mathematics/SS1.1_Real_Numbers/`; PDF directory: `outputs/PDF/`.

| Type | DOCX SHA256 | PDF SHA256 |
|---|---|---|
| CBE_LessonSequence | fd25b1a604e02f959c87c5ab48992ce6d2bd2bca54da63ba2758924947dc355a | dd647b05d509ac74826b7b5099039e3a2441ced01a508ddd8c2221900613ff41 |
| FinalExplanation | 11affae16d78aeb5d9487d8e2853fa553dde2e1d668b45b26ee0d9e0bb1ebbe1 | f57b887a69e1c9cd5c948595063338364962476a78b15dd1792127c69b1f1b4c |
| FinalExplanation_TeacherKey | f53c7d5c629c65abe9146265e6de79ab4b4cd64e1987450a16d10bc38ec9a302 | d00ade2f7c1a64db93116caad9cdf313e1177f6dee8ae75543674cde71aa2306 |
| SummaryTable | 597082043c5c20c74ada0cdc7fcb6abb98f182fba6261807ccedf1f70b9dff53 | 9f5d3fb80bd05bcf1cdb1bec30086dde737dbe8fb46efb216ddaa94ec6e490da |

Later changes to canonical content or these rendered artifacts require a focused recheck; this verdict is not approval of unseen future outputs.
