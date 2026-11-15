# Core1.2 independent correction-pass1 recheck — core27

Verdict: **ACCEPTED for content**. The three reported correction areas are closed,including this reviewer's CIL12-C27-1 mapping finding. Actual device/group/action/access/pacing caps remain. Focused recheck only;no author edits,build,render or acceptance-state change performed.

Current fingerprint: `05f9afafa0f5e2ebfb5d2cc365e9ee2ff3978665664fc522ca026cfee4b22d0b`. Initial report remains immutable at SHA256 `dbfeb07eff4a6304df6d39074fc61bbded5b9e88213ec00b45dd8e3d82b6d169`;old fingerprint `d94af2a1939d656839200f8c98cba4f3eda3e8811db5ac4028217f96f4ec822f`.

## Exact diff and closure

Compared current source/materials/blueprint/manuscript against the frozen initial snapshots. Exactly8 JSON paths changed:3 blueprint outcome arrays and5 manuscript paths. No source/materials changes.

1. L4 knowledge,phase3 check andsummary observed now explicitly say **for positive x,x^(1/n) is the positive nth root of x**. This correctly names the expression and its radicand;1/n itself is the index,not the root value. Negative powers invert the result. Positive-domain scope is retained. Allthree canonical occurrences agree.
2. L12 phase3 learner action now correctly states **10^(3.0791)=10^3×10^(0.0791) is the antilog of3.0791**. The log value3.0791 is not itself equal to that inverse quantity. The exponent-sum identity is mathematically correct;independent arithmetic confirms the equality. Existing finite-table approximation reasoning and acceptance of a reasoned direct-arithmetic preference are unchanged.
3. L13/F13 now maps **c only** in manuscript L13 plus blueprint lesson_map,assessment_tasks andassessment_map. Unsupported b,d,g task evidence is no longer claimed. The g narrowing is conservative where reviewers differed;it does not remove substantive g coverage in L12/I4. b remains L2/L3/I1 andd L6/I2. No new tasks are required to close the surplus-link finding.

Full materials—including14cards,all inputs/teacher keys,tables and37 registered calculations—are byte-identical. Final instructions,all4prompts/exemplars and rubric are unchanged. All14lesson timings and source/verification/PDF/crop/evidence bindings are unchanged. Thus initial independent164/164 numerical/assertion evidence and full source/task reasoning carry forward;no new full-scope rerun was needed.

## Actual rebuilt five Word companions

436/436 propagation/structure assertions,26/26 focused diff/closure/retained-coverage assertions and4/4 source-binding assertions pass. The corrected L4 sentence appears twice in actual CompactTeacherGuide (knowledge andphase check);old sentence is absent. Its summary version is canonical teacher content;StudentSummaryTable correctly keeps learner responses blank rather than printing that answer. The corrected L12 antilog sentence appears in the actual guide andold sentence is absent. Complete unchanged14student/key cards propagate correctly in the rebuilt files.

HeldCIL14 remains in AssessmentMaterials andabsent from teaching StudentMaterials;exact private key block remains excluded from assessment handout. Fourteen summary rows/42blank response cells andattribution in allfivefiles remain. No embedded media/OLE introduced. Allfive DOCX ZIP hashes changed after rebuild;current exact hashes below supersede the initial file binding while initial evidence is preserved.

This is content/Word-text closure,not final standard-output/PDF layout acceptance. Device provision/model-specific entries/displays/individual observation must be actual;unavailable/notobserved components remain pending. Group chart/discussion/resource care and lasting attitudes cannot be inferred from written outputs. Prerequisites,actual access/observation turns,14lesson pacing and40-minute final workload remain teacher-confirmation matters.

## Exact current bindings

Canonical and verification:

- `data/curriculum_expansion_2026-11/sources/coremath_1_2.json` — `533a4d3973b7a1aec806e47a85fe2f05be0c1606f5de0c83274f504294fc028d`
- `data/curriculum_expansion_2026-11/materials/coremath_1_2.json` — `8b76985b9c55ca167f0ee78d2feb36c8dd6e982bed042bf04b597f87e2739e1d`
- `data/curriculum_expansion_2026-11/blueprints/coremath_1_2.json` — `66cd5f0866afefd2b43c6ebaabd522c4bc807cab220d2e15b3aa4f36aac04181`
- `data/curriculum_expansion_2026-11/manuscripts/coremath_1_2.json` — `a5f3520b45345f95b681f0d820d431c158ffcf79e723b770430ce31a6ace89ba`
- `data/curriculum_expansion_2026-11/sources/coremath_1_2.verification.json` — `b95b951b0c81250ed9e32e1d0d61cf5f32df975d4781c119ff8fb35ed0f34675`

Unchanged source files:

- `CBE_Curriculums/Grade 10/STEM/Grade10_CoreMath.pdf` — `700b55379210dda0ee24561d43a872f965eba9568ec8092b6e9116d7f3609b2c`
- `data/curriculum_expansion_2026-11/sources/coremath_1_2_source.png` — `dd0269249f57784269456348c9c5b3db5a3308fe00776879af3cdbae8cca1559`
- `data/curriculum_expansion_2026-11/evidence/coremath_1_2_source_verification.md` — `f1a05a407c3024b3a33145d67799eb39c7ad02c43b868d992ffdbdb6ffebf172`

Actual rebuilt five DOCX companions:

- `AssessmentMaterials` — `263b6774f005c46e0777022545a2dc7533c81c8825bd21a13b2346462814e642` (`data/curriculum_expansion_2026-11/outputs/v2/Core_Mathematics/SS1.2_Indices_and_Logarithms/Codex_Core_Mathematics_Indices_and_Logarithms_AssessmentMaterials.docx`)
- `CompactTeacherGuide` — `8999e4bc79ac0c59a081d4ffac4b9c3bffcc9bc9a151a66d0a89267ee532c84e` (`data/curriculum_expansion_2026-11/outputs/v2/Core_Mathematics/SS1.2_Indices_and_Logarithms/Codex_Core_Mathematics_Indices_and_Logarithms_CompactTeacherGuide.docx`)
- `MaterialsTeacherKey` — `00d8370adc6fc6ff8f42bbb1d71f3658135b2ff439e5015a6677cd286f9186da` (`data/curriculum_expansion_2026-11/outputs/v2/Core_Mathematics/SS1.2_Indices_and_Logarithms/Codex_Core_Mathematics_Indices_and_Logarithms_MaterialsTeacherKey.docx`)
- `StudentMaterials` — `0bc01dc41060dc1248a2db0db45a91f0dafb0845693c5d0333af563a9f1513f1` (`data/curriculum_expansion_2026-11/outputs/v2/Core_Mathematics/SS1.2_Indices_and_Logarithms/Codex_Core_Mathematics_Indices_and_Logarithms_StudentMaterials.docx`)
- `StudentSummaryTable` — `306f18d0340a20c0fd46c22f0c3c9061c77c6f9651bcab26b356acc7904cb0e7` (`data/curriculum_expansion_2026-11/outputs/v2/Core_Mathematics/SS1.2_Indices_and_Logarithms/Codex_Core_Mathematics_Indices_and_Logarithms_StudentSummaryTable.docx`)

Evidence: `reviews/batch_07/evidence/coremath_1_2_core27_pass1/` contains `exact_delta.json`,`binding.json`,`focused_checks.json`,`check.py` andfive extracted actual Word texts. Initial snapshots/independent calculations remain in `coremath_1_2_core27/`. Current fingerprint andfiveWord hashes rechecked unchanged immediately before this report freeze.
