# Essential Mathematics 2.8 — correction pass 1 focused recheck

**Status: COMPLETE — P1–P6 closed for the scoped correction pass; no new blocking regression found.**

Date: 2026-11-12. Reviewer: same independent Codex agent; inherited exact model identifier not exposed. The initial `essmath_2_8.md` remains unchanged (SHA256 `634559a2cedb4b8bd5fb1dafdc9dba224662abef787e910b0af7e655fc1e19d0`). This is focused correction verification, not a second full content/baseline audit. No paid API calls or content edits. Only this report and scratch under `/tmp/essreview/recheck` were written.

## Scope and evidence

Re-read current source outcome c, blueprint assessment map, manuscript lessons3,5,9 and final rubric; checked the compiled module’s corresponding fields and final-lesson strategies. Extracted current text from all eight originally rebuilt PDF/DOCX types, including word/footer XML in each DOCX package for attribution. Then checked the added ninth type, `AssessmentMaterials`, in DOCX and PDF. This separate handout was added after the initial eight-type correction build.

Paths below are relative to `data/codex_pilot_2026-11`. PDF names use prefix `outputs/PDF/Codex_Essential_Mathematics_Commercial_Arithmetic_1_`; corresponding DOCX files are in `outputs/v2/Essential_Mathematics/SS2.8_Commercial_Arithmetic_1/` with the same prefix and type names.

Visual sample (one-based PDF pages): CBE_LessonSequence35–38 (all four final-lesson pages); CompactTeacherGuide4,6,10 (lessons3,5,9); FinalExplanation5–6; FinalExplanation_TeacherKey2; StudentSummaryTable1; SummaryTable1; StudentMaterials2; MaterialsTeacherKey3; AssessmentMaterials1, including enlarged footer crop. This sample covers affected final instructions, rubric, blank summary, role preparation and footer layout; it is not every page of the rebuilt package. Text and DOCX XML checks extend beyond the visual sample.

## Original findings

| Finding | Status | Correction verified and evidence |
|---|---|---|
| **P1 — independent assessment conflicts with group strategies** | **Closed** | Manuscript lesson9 and compiled LESSONS[8] now use “Read and interpret the task individually; clarify wording without discussing methods or answers” and “Independent written working: no peer comparison, group solution or teacher exemplars before original work is collected.” All five final phases now preserve individual work/collection rather than applying generic paired/shared strategies. These exact corrected instructions appear in CBE pp35–38 and compact p10, and their DOCX equivalents. Student FinalExplanation still states independent30-minute work, calculator access and rounding. Teacher Observe also forbids optional ARES resources/search until original work is collected. No old “Evidence-first group work”, “then paired comparison” or “Revise a shared model” remains in the final-lesson sections of either rendered guide. |
| **P2 — final rubric asks unelicited comparison/loss** | **Closed** | Manuscript and compiled final rubric, student FinalExplanation pp5–6 and TeacherKey p2 now say “Prepare a usable budget and calculate discounted costs” and “Calculate commission and percentage profit using the correct base”. No final comparison or loss performance is required by those criteria. Blueprint assessment_map explicitly assigns E2 quotation comparison/reverse discount, E3 reverse commission rate, E4 loss and E5/E6 reverse conversion to formative evidence; independent final profit and foreign→KES choice are identified separately. Earlier tasks remain intact. This closes the rubric/evidence-description mismatch; teachers must actually retain that formative evidence rather than infer every subskill from the final alone. |
| **P3 — source outcome c inserts ‘the’** | **Closed** | `sources/essmath_2_8.json` outcomes[c] now reads exactly “determine commission and percentage commissions in different situations”, matching the initially inspected source crop. Compiled UNIT.learningOutcomes and guide text use this wording; “in the different situations” is absent from both guide PDFs. Source typo “prepare budget to for” remains honestly preserved. |
| **P4 — missing blank student summary** | **Closed** | New `StudentSummaryTable.docx` and one-page PDF are present. XML contains one header row and nine correctly titled lesson rows with three genuinely empty evidence cells each. PDF p1 visually confirms those blank cells and separates teacher exemplars. Existing teacher SummaryTable p1’s statement about a blank student version now points to an actually supplied artifact. This eighth type is distinct from the prefilled teacher reference and discloses no expected numerical answers. |
| **P5 — Claude attribution contradicts OpenAI pilot** | **Closed** | All eight rebuilt PDF texts and all eight complete DOCX word/footer XML packages contain accurate OpenAI attribution and no “Claude”/“Anthropic”. Body attribution where applicable reads “with lesson drafting and compilation assisted by AI (ChatGPT/Codex, OpenAI)”; footer reads “with AI assistance from ChatGPT/Codex, OpenAI”. No exact underlying model is guessed. Added ninth AssessmentMaterials type also passes. Attribution is in the footer XML for several types, including StudentSummaryTable, so inspecting document.xml alone would incorrectly suggest it is absent. |
| **P6 — unsupplied role/currency labels** | **Closed** | Manuscript L3 Predict, compiled lesson3, standard guide and compact p4 now say “Write salesperson, employer and buyer on three paper slips before class, or assign these roles orally; no money changes hands.” L5 equivalents and compact p6 say “Before class, write USD and KES on paper slips…or label the directions on the board.” Explicit preparation plus oral/board fallback resolves the missing-prop dependency. Numerical E3/E5 data remain supplied. This does not claim a new tabulated exchange-rate chart has been added; E5 is still a complete prose rate record, as noted initially. |

Dependencies are now propagated from source/manuscript through compiled module to the inspected guide/assessment/student exports. The original report’s baseline B findings remain historical baseline findings; this correction pass did not edit or re-audit the baseline.

## Additional assessment safeguards and handout

The current `_link_matching/v2/Essential_Mathematics/SS2.8_Commercial_Arithmetic_1/Codex_Essential_Mathematics_Commercial_Arithmetic_1.json` has ten final-lesson resource slots with no picked resource; final-lesson guide text has no selected resource titles. Generic “Search ARES” fallback links remain visible in the standard guide. This is not an answer resource supplied for assessment: the teacher’s final Observe instruction explicitly says not to open resources or search before collection. The compact guide has no such phase links. Suppression and timing rule were checked together; no claim of testing every external URL is made.

Added `AssessmentMaterials.docx`/PDF contains **E9 only**, with exactly the same data as materials.json E9.student (whitespace-normalized match), a title and attribution. It contains no E1–E8 practice, teacher key, worked example, arithmetic result or suggested method. This is an appropriate isolated data handout to distribute with student FinalExplanation. Both handout and assessment remain separately needed; neither silently embeds the other. One-page PDF body and footer are readable and do not overlap. “Teacher review copy” remains a pilot status subtitle; it is not a teacher-answer designation.

The existing StudentMaterials still contains E1–E9 question data without teacher answers; MaterialsTeacherKey has expected results and do-not-distribute instructions. StudentSummaryTable is blank; SummaryTable remains explicitly prefilled teacher reference. No new numerical teacher-key leakage into intended student artifacts was found.

## Recomputed values and regression observations

No numerical question data were intentionally changed in this pass. Independently recomputed affected coverage examples and final answers:

- E2: P2160;Q2137.50;Q cheaper22.50; reverse3.75/75×100=5%.
- E3:15000×4%=600;450/18000×100=2.5%; doubled first commission1200.
- E4: A600 profit=25% of2400;B300 loss=15% of2000.
- E5/E6: USD50→6400KES at dealer buy128;USD50 costs6600KES at sell132;6600/132=50USD;6400/132=48.484848…→48.48USD,loss1.52USD.
- E7:1200+2137.50+1800+600=5737.50;unallocated262.50.
- E9/final:20×120×.85=2040;allocation2040+500+300=2840;unallocated1160;commission8000×.03=240;profit2000−1600=400 and25%;sell USD20→2500KES;buy USD20 costs2600KES. These agree with current key/student data.

Final minute vector remains4+30+2+1+3=40; total9×40=360. Correction did not add a new assessed task or increase the30-minute student working period.

No new blocking mathematical, leakage, preparation or layout regression found in the scoped checks. The student FinalExplanation rubric’s final row still breaks across pp5–6; that split existed in the original PDF and is not caused by this correction. Text is present on both pages and not clipped, but keeping a rubric row together would improve print usability. Standard final lesson still spans four pages because of repeated generic resource-search filler; compact p10 is readable on one page. Expanded OpenAI footers fit within the inspected margins without overlap; some footer type is small and should be checked on the school’s actual printer.

## Residual classroom limits

Closure verifies corrected documents, not classroom effectiveness. Teachers still need to confirm prerequisite percentage/decimal fluency, access and reading support, pacing, and handling time for the six-page final plus separate E9 handout. The exact40-minute schedule has no explicit distribution/collection allowance. Retain formative evidence for quotation comparison, loss, unknown percentage rates and reverse conversion; the independent final remains intentionally narrower. None of this pass establishes full independent mastery of every subskill, superiority to baseline, or cost savings.
