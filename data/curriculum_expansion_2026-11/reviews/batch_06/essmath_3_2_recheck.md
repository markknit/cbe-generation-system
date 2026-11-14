# Probability I — independent correction pass1 recheck

**HOLD — EM32-C1 is partially corrected but remains open in blueprint lesson_map lesson9.** No new numerical/content error was introduced. The exact reviewed content fingerprint is `547ab588a7ead1666b5ceda978e3b21756d758b492ce96c56deb2e8edf867324`; this is a bound HOLD revision, not an accepted fingerprint.

Reviewer: independent Codex/GPT-6 agent essential_source_review. Scoped recheck only; no author self-review consulted. Original [initial HOLD](essmath_3_2_initial.md) SHA-256 `874ffac162b08872ba94158900bf3f88f66755b6621f2ea9fc33bb79ff2cbd1c` remains unchanged. No canonical/output/pipeline/acceptance mutations or rebuilding were performed.

## Exact correction scope

[Binding](evidence/essmath_3_2_recheck/binding.json) records the actual four current canonical hashes, independently recomputed fingerprint, original report hash, all five current Word companion hashes and exact initial-byte reconstruction. The [read-only checker](evidence/essmath_3_2_recheck/check.py) restores c in memory to the three changed locations; serialising those restored records reproduces both initial blueprint/manuscript SHA-256 hashes exactly. This establishes that only those three outcome arrays changed; no prose, phase, final prompt/exemplar, answer, rubric or other mapping changed. Source/materials file hashes are identical to the initial review.

| Claim location | Current outcomes | Result |
|---|---|---|
| Manuscript Lesson9 | b,d,f,h,i | Corrected |
| Blueprint assessment_tasks F9 | b,d,f,h,i | Corrected |
| Blueprint assessment_map F9 | b,d,f,h,i | Corrected |
| Blueprint lesson_map lesson9 | b,**c**,d,f,h,i | Still overclaimed |

The original source outcome c is “determine the range of probability of an event.” EP9 still contains the same six audit claims/application/action-evidence prompts and no interval0–1 or impossible/certain-range question, as established in the full initial review. The one remaining c declaration therefore retains EM32-C1. Correct **blueprints/essmath_3_2.json → lesson_map row lesson9 → outcomes** by removing c. There is no row identified as “F9” in lesson_map; that collection uses numeric lesson identifiers. Preserve c in L1/final I1 and other substantive locations.

## Actual companions and unchanged evidence

All five actual Word companion bytes are identical to the initially reviewed companions: CompactTeacherGuide, StudentMaterials, MaterialsTeacherKey, StudentSummaryTable and AssessmentMaterials. Their hashes are recorded individually in the new binding. Those companions do not display the internal lesson outcome-ID arrays, so rebuilding identical rendered prose is unnecessary for this check. Initial 380/380 propagation/structural evidence, independently solved fixed tasks/9 arithmetic expressions,30 blank student-summary response cells, EP10 final isolation and five-file attribution remain valid at these exact unchanged bytes. No new propagation or isolation issue was caused by the scoped correction.

The changed manuscript/task/assessment-map arrays are semantically appropriate for EP9’s actual evidence. No complete source/math rerun or extra scope was undertaken. A later full nine-pair artifact/layout review remains separate from this focused content check.

## Source interpretation and classroom conditions retained

Detailed printed4.2/internal-overview3.2 remains explicit; no official erratum or renumbering is asserted. “Maximum of two experiments and two outcomes” remains ambiguous alongside the source’s suggested six-faced die. A coin and a two-label draw are two binary component stages with **four genuine joint outcomes**. Calling these outcomes descriptions does not settle a possible total-joint-outcome cap. The per-component interpretation is defensible as the stated teaching assumption, and teacher/source confirmation remains a substantive implementation condition; it has not been obtained by this review.

Actual F2/F3 single-chance and F6 paired individual actions/raw records, exact observed roles, impartial valid/invalid rules, safe accessible equipment and40-minute pacing remain teacher checks. Provided final records/writing do not certify performeda/e/g, digital use or lasting attitude. The initial safety/gambling-awareness boundaries remain unchanged.

## Disposition

Keep HOLD, correct the one remaining lesson_map array and obtain a second focused recheck bound to the resulting fingerprint. Do not issue content acceptance from this partial correction. This report and its manifest are saved; reviewer stops at this clean boundary.
