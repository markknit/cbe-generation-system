# General Science1.1 final artifact/layout review

Status: COMPLETE INITIAL ARTIFACT REVIEW — HOLD standard-guide artifact acceptance for one resource-selection defect. Canonical content acceptance is unchanged. 2026-11-13.

Scope: the four newly rendered types only: CBE_LessonSequence(31 PDF pages), FinalExplanation student(6), FinalExplanation_TeacherKey(3), SummaryTable teacher(2). Five companion types were inspected in the initial/recheck workflow and were not fully re-audited here. No content, acceptance record, renderer or policy edits by reviewer. No baseline audit. Root usage verification:30% at08:41:08UTC,29% at08:43:44UTC, no pause; central guard monitoring continues.

Accepted canonical content fingerprint independently recomputed unchanged: `fdbf788509d17e2bcf9b83537e6157ac32405419bb49339d0f3ac330a020865c`.

## New artifact finding — Medium: unrelated selected resources in the standard guide

Exact location: generated CBE_LessonSequence DOCX hyperlinks and PDF resource blocks, especially Lesson1 p3, Lesson3 pp11–14, Lesson4 pp15–17 and Lesson6 pp23–25. Named examples:

- “Assistant hotel manager: What I do and how much I make”, displayed p3 and in several L1/L6 blocks, e.g.pp23–25; local ID428eb9c13a4c50139009d6de23a09a96.
- “Power series intro”, pp4–5 and24–25; ID4d712cc02f845dcb8322b2e816ccb9b3.
- “Interpreting general multiplication rule”, L3; ID0a78dfd326875e48969ea9f76ec02553.
- “Interpret probabilities of compound events”, pp12–14; ID7a220f987ad65aeeb0784812796bdf04.
- “Worked example: absolute and relative extrema”, pp15–17; IDab36225658c25b3eb82ce81f5ff49e84.

Evidence: titles concern hospitality salary, advanced series/extrema, and probability rules, while these lessons concern everyday science questions, paper water-rise means, causal confounds and source-bounded scientific careers. The standard guide flags these as “Related topic: not an exact match for this lesson”, which honestly signals imperfect matching but does not make the items relevant support. The accepted canonical material already supplies its actual scientific tasks/primary source summaries. The hospitality salary title is especially poorly aligned with the deliberate source/training/salary limits. “Median & range puzzlers” is closer to introductory data analysis, but has not been vetted as a needed activity either; no relevance guarantee inferred from its arithmetic topic alone.

This is a generated optional-resource curation defect, not a new error in the accepted canonical scientific explanations. No claim is made that the actual local media are broken or were watched. The repeated blocks also dominate page count, but page count itself is not the defect.

Proposed correction: use a workspace-only per-module vetted-title allowlist, initially empty for this module unless a suitable local item is actually checked. Suppress uncurated selected items rather than force weak matches. Retain supplied GS11–GS17 and official source summaries. Preserve independent-final null selection policy. Rebuild the standard guide and independently confirm actual DOCX/PDF/hyperlinks and any changed layout; do not alter production matcher defaults or invalidate unchanged content unnecessarily. Parent has acknowledged this artifact fix and will request a focused recheck. Current artifact acceptance is withheld until the actual rebuilt guide is seen.

## Verified propagation and separation

Read all four new DOCX bodies/relationships and all four complete extracted PDF texts. Compared184 accepted-content strings/checks against DOCX: student/key instructions, all four prompts, complete four-level rubric descriptors, four teacher exemplars present only in the teacher key, all seven teacher-summary rows, and standard lesson activity/strategy/evidence checks. All passed.

Student FinalExplanation p1 correctly has4 minutes procedure+28 sections(16+12)+4 separate open-question reflection+4 checking=40. Teacher key p1 gives the same instructions. Standard L7 pp27–30 preserves individual-only/no hints/no discussion before collection and separate reflection without section4 double-counting. The accepted GS1 device observation/print-only-not-observed wording propagates to standard L5.

The final2 scoring clarification appears fully in teacher key p1: mean comparison can be descriptive analysis; accept that distinction; tentative material/exposure contribution does not establish either cause. MeansX14/Y8mm and controlled-comparison guidance remain in the teacher key, without those answers in the student assessment. Student assessment contains prompts, answer spaces and rubric, not teacher exemplars. Teacher key is labelled “do not give to students”; teacher SummaryTable is labelled pre-filled teacher reference. GS17 itself is supplied by the already-reviewed separate AssessmentMaterials handout. The student task’s “using GS17 only; no teaching cards” instruction remains; no live digital research is introduced into the final.

Final-resource policy: standard Lesson7 has no selected video/reading resources in the actual final pages; only null/no-match and search fallback blocks remain. Those fallback links are not required independent-task material. Do not use them during assessment. The new unrelated-selection finding concerns other lessons, not a failure to null final recommendations.

## Exact visual coverage and pagination observations

Actually viewed rasterised PDF pages with pdftoppm/view_image:

- CBE_LessonSequence:pp3,11,19,27,28,31(6 of31).
- Student FinalExplanation:pp1,3,5,6(4 of6).
- FinalExplanation_TeacherKey:pp1,2,3(all3).
- Teacher SummaryTable:pp1,2(both).

Other pages were text-inspected and some additionally rasterised; they are not claimed visually inspected. DOCX XML/body inspection verifies content, not independent Word-engine pagination. No exhaustive-all-pages visual claim is made.

Sampled headings, tables, answer space and attribution are legible; no clipping/overlap or lost text confirmed. Student assessment rubric row3 continues fromp5 top6, with remaining text present; teacher key career row crossesp1→p2 and rubric row4 startsp3, complete and readable. Teacher summary L6 title leaves “defensible?” as a continuation line atp2; awkward but nonblocking, with all row text supplied. Standard resource columns span multiple pages and create long blank adjacent table cells; that is existing exporter behaviour, with the relevance defect handled separately. New artifact headers/attribution correctly identify ChatGPT/Codex, OpenAI.

## Verdict and next step

Canonical content remains accepted at the fingerprint above; prompts/keys/rubric/timing/scoring propagation and student/teacher separation pass this scoped audit. Final standard-guide artifact acceptance is **HOLD** solely for the selected-resource relevance defect. Recheck the corrected actual guide after workspace-only curation and render; no reauthoring or baseline audit required. No evidence supports a classroom-pacing/practical-safety certification. Teacher device availability/individual observation, print-only evidence limits, preparation, accessibility and classroom timing remain as in the content recheck. Final artifact hashes below bind this initial rendered snapshot, not a future rebuild.

## Initial rendered snapshot hashes

- `outputs/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science_CBE_LessonSequence.docx` SHA256 `2d6de44eeff4e13fda35d7d9040c3d99d60eed54a38e5b99902b017a1591b65e`
- `outputs/PDF/Codex_General_Science_Introduction_to_General_Science_CBE_LessonSequence.pdf` SHA256 `4e73ab6108599dfd7b2b63030fb47cdea22299801a2cb5c7f6a7525bb75d9467`
- `outputs/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science_FinalExplanation.docx` SHA256 `4860e21170a1fd71a9c752089fb7c2b094b41e557b31391d05820942ae00fd04`
- `outputs/PDF/Codex_General_Science_Introduction_to_General_Science_FinalExplanation.pdf` SHA256 `a02d0a3e5cf39ee95e42bd8d1e82771003bab74c87bb3b10d3bd0bc9875829b4`
- `outputs/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science_FinalExplanation_TeacherKey.docx` SHA256 `42cde7acc8e691b61161cad11c1af60366b0f07becf15ceffd76a81fc4d3ef36`
- `outputs/PDF/Codex_General_Science_Introduction_to_General_Science_FinalExplanation_TeacherKey.pdf` SHA256 `3e8b63445f3d24981ef717248b7055e32418c26361f42b78be1bae3bb100ebc9`
- `outputs/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science_SummaryTable.docx` SHA256 `2d834fc0927edfd6f6612a3fca09d90df55d54fa5292da08c2250f58247e9286`
- `outputs/PDF/Codex_General_Science_Introduction_to_General_Science_SummaryTable.pdf` SHA256 `f55155d624c65f2bccd4b7913e58dbb94836d9255786b13fa8622814e91cae13`
- `data/curriculum_expansion_2026-11/resource_policy.json` SHA256 `87410e4d953c5300457db9d6a193e5218e71e3a30fb7868a74aa49bc43c63d46`
- `scripts/curriculum/resource_recommender.py` SHA256 `de179b8dd2279af86bf516dc38c576e251a1fd8e55401ea3eea3dbe97a9e7c20`
