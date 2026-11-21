# Cross-corpus numeric rubric disclosure review

Reviewer: core27. Frozen 2026-11-15T01:36:40.495093+00:00. **Scoped HOLD: confirmed student-facing answer disclosure in Core1.1 and Essential1.3; initial Trigonometry1 disclosure independently confirmed.** No canonical/archive/acceptance changes made. This report is a new concern review; earlier content/layout reports and packages remain immutable evidence, not silently rewritten.

## Method and coverage

Read all850rubric strings across170criteria in43canonical manuscripts:40expansion plus3frozen pilots. A digit scan identified11initial numeric descriptors;the currently corrected Trig manuscript leaves9. A supplemental number-word scan identified42candidate strings (including counts,zero,half,ordinal/idiomatic usages). Compared candidate text with final prompts/exemplars and,where necessary,complete related sections/materials. The ledger preserves every rubric string,all candidate classifications/reasons,full related final sections,43manuscript hashes and40current expansion content fingerprints. Legacy pilot manuscripts have exact hashes;the current expansion fingerprint helper requires verification files absent from those frozen pilots,so no new official pilot fingerprint is invented.

Actual output check: read XML/text for four Core1.1standardDOCX and corresponding fourPDFtext extracts;visually inspected one readable page of the actual final student PDF(p6). Read Essential1.3student finalDOCX/XML andPDFtext,and visually inspected its actualp5 after the number-word finding. Thus2readable PDFpages were inspected,not an all-page survey. Hashes for all18Core1.1currentWord/PDFfiles and the additional Essential1.3student finalpair are recorded.

## Confirmed findings

**CDR-C27-1 — Core1.1 criterion4 proficient discloses I4 answer.** The descriptor says “Correct reciprocal model,4portions,units,assumption/product check and concrete evidence-based written advice.” I4 asks for the number of full portions from7/2L divided by7/8L perportion;the result is4. The actual student FinalExplanationDOCX and PDFp6 visibly include this descriptor. TeacherKey also contains it,which is appropriate only in a private key. CBE_LessonSequence andSummaryTable do not contain this string. This is an exported student assessment disclosure,not merely unused metadata. A neutral descriptor can require the correct portion count/model/check without naming4.

**CDR-C27-2 — Essential1.3 criterion2 excellent/proficient disclose a requested root in words.** “the lost-zero explanation is precise” and “a valid zero-root explanation” name0 as the lost root. I2 asks learners to solve y²=4y,record all roots,and explain how division by y could lose one root. Independent factorisation y(y−4)=0 gives0and4;the prompt does not name the lost root. The actual student FinalExplanationDOCX and readablePDFp5 print both descriptors. This supplies one particular root,even though it supplies neither the complete solution nor the work. A neutral division-condition/lost-root explanation descriptor preserves the criterion without naming0. The below-expectations phrase “zero-product support” is a legitimate general-law reference and is not this defect. This partial disclosure was missed by digit-only screening.

**Initial CTG-E1 independently confirmed.** At the frozen Trig fingerprint,criterion3proficient names7.17m/8m results andcriterion4proficient names30°interpretation. I3/I4ask for exactly those quantities. These are answer values,not given input values. Trig had only five draft companions when identified;its new concern was canonical pre-standard-export disclosure. During this cross-review root changed the live descriptors. The initial descriptors/prompts/exemplars are bound to our preserved initial manuscript;current changed manuscript is separately recorded. This report does not issue a focused correction verdict.

Earlier Core1.1 and our Trig content reviews did not catch these rubric disclosures;their original reports remain preserved. The new findings require an explicit versioned correction/recheck rather than treating unchanged numeric task solutions as sufficient. No broad content re-review was performed.

## Other numeric descriptors

| Descriptor | Classification |
|---|---|
| Core1.1 C1 `including0/1` | Given0/1classification cases/general zero-as-fraction inclusion identity. It does not supply any of the six requested exact-value fraction answers. Reading the slash as fraction gives the generic representation of zero;minor wording ambiguity,not another concrete unknown-result disclosure. |
| Core1.1 C3 `4significant figures` | Required precision already in I3. |
| Core1.2 C3/C4 `3significant-figure` | Required precision already in the corresponding prompts. |
| Core1.3 C2 `99²` | Given expression;the computed9801is absent. |
| Trig C2 `90°` | Given endpoint/domain case;not its sought sine/cosine/tangent values. |
| CoreProbability C3 `total1` | Probability normalisation invariant;not the unknown event probabilities5/6and1/2. |
| Essential1.1 C3 `product of1` | Multiplicative-inverse definition/check invariant;not an unknown reciprocal. |

The42number-word candidates are individually classified in the ledger. Apart from Essential1.3above,they state requested response/component counts (e.g.two limits,four laws,three summaries),provided/domain conditions (e.g.zero denominator,zero thickness),a given half-displacement construction,an ordinal target(third angle),a general zero-product rule,an already requested zero crossing,or the idiom“one another.” They do not supply a sought numerical value. Model-decomposition/count language can cue the intended method,but no further concrete numerical answer disclosure was confirmed in this scoped review. This is not an exhaustive search for all possible nonnumeric conceptual hints.

## Binding and archive preservation

- `coremath_1_1` scan fingerprint: `9eb00d6141cd156a4404ce0986f06ea547a01afcb02c4ce2736e5b00a2b20dc5`;manuscriptSHA `76a8504cbf8cdf543d5a0570d579bc87f954e529c19403111cd01fe05aae498e`.
- `essmath_1_3` scan fingerprint: `1f02c60b4122722a1d83e9ad7476c0adb7a99bd749f914c7c673c64f7cea1c01`;manuscriptSHA `dd093eacb034733fc2c40dbe9618a31c5651fe7bc18d901423cb62add351e320`.
- `coremath_2_4` scan fingerprint: `0d4ab09fb5d757a52037056486d1f2228c5ab7473a69cf301dcc58a39f04a899`;manuscriptSHA `877a0f3d8d63103adb7d72eec086f1ef505a8c10f420696854a6998a3ce48a50`.

- Initial Trig fingerprint: `66b147720950899a52238f801fb1f94e56d716e96427e64434b1ce4d9dce2897`;preserved initial manuscriptSHA `8b1ff5405ce2bda4557e9014c2800a0c20d88487f97b8fa25780c44e9ea38206`.
- Old Core1.1 reviewed ZIP SHA: `68aea80bb21c98e9fb7e44bd94e8a45ed58539eaeb8693242a3da6363348d7da`. Read-only member checks confirm its canonical manuscript/materials and actual student finalDOCX/PDFmatch the current affected baseline bytes. No ZIP or receipt was replaced.

| Evidence | SHA-256 |
|---|---|
| `evidence/corpus_rubric_disclosure_core27/scan.py` | `24ed90e867b3c73fea92ce3727323e34ce2c446499e11f36bc83efdcf36cc919` |
| `evidence/corpus_rubric_disclosure_core27/candidate_ledger.json` | `2e0a2f161910825698bd6d3f79e1bf73f0a691690e2950bbaf95b62099cae5b7` |
| `evidence/corpus_rubric_disclosure_core27/frozen_coremath_1_1_manuscript.json` | `76a8504cbf8cdf543d5a0570d579bc87f954e529c19403111cd01fe05aae498e` |
| `evidence/corpus_rubric_disclosure_core27/frozen_essmath_1_3_manuscript.json` | `dd093eacb034733fc2c40dbe9618a31c5651fe7bc18d901423cb62add351e320` |
| `evidence/corpus_rubric_disclosure_core27/Core1_1_Final_student_p6.png` | `bca38e1d8528b8a3b7e1d4e7d6eec9cb3ea7cff838969cb0463674a1713c6624` |
| `evidence/corpus_rubric_disclosure_core27/Ess1_3_Final_student_p5.png` | `705b00d2edb44f468f879970b66905af8cea5deb117fe76578fcdb0691a5d18a` |

| Actual affected student artifact | SHA-256 |
|---|---|
| `data/curriculum_expansion_2026-11/outputs/v2/Core_Mathematics/SS1.1_Real_Numbers/Codex_Core_Mathematics_Real_Numbers_FinalExplanation.docx` | `40df1c2715352feabaf9ea64b69be0cb468c5e51564dfa502455dd266fe02781` |
| `data/curriculum_expansion_2026-11/outputs/PDF/Codex_Core_Mathematics_Real_Numbers_FinalExplanation.pdf` | `5d9f5e1bd209010038119a1fdbbe6084612f722bb27ffc33163d09a58a584e45` |
| `data/curriculum_expansion_2026-11/outputs/v2/Essential_Mathematics/SS1.3_Quadratic_Equations_I/Codex_Essential_Mathematics_Quadratic_Equations_I_FinalExplanation.docx` | `c3f7ecb40e8c5372c2b275bbb22a16928cbd7e0efd237a9666b878523dbc03ed` |
| `data/curriculum_expansion_2026-11/outputs/PDF/Codex_Essential_Mathematics_Quadratic_Equations_I_FinalExplanation.pdf` | `bd63534ea3ef1e8db1541bce7fb88cbbe07fd0a7797fd602bf22850bcabfd5c2` |

No authoring,archive mutation,re-render,acceptance-state change,physical classroom test or broader source/mathematics re-review was performed. Existing frozen package evidence must remain byte-exact while any corrected version receives a separate fingerprint/recheck/artifact/package chain.
