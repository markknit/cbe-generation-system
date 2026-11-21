# Focused recheck — Respiration technical wording

**ACCEPTED — focused technical wording recheck complete. The remaining-field finding is CLOSED.** The initial full source/science/protocol report remains unchanged. No new artifact PASS is claimed; a fresh successful render/PDF audit and independent final artifact inspection remain required.

New accepted content fingerprint: `01967adc9a78e29cbb5a5f86132951f8461d9b546b25e036a5dda62ae9dc49ff`. The initial fingerprint `3537f7d2f4dfac84255b6a03fe07da50b157e3940ca6befa5a17cf3d63154c8b` is superseded for current content binding, without altering its historical report/evidence.

The supplied pass-1 diagnostic described three intended corrections. Independent reverse reconstruction of the current canonical files proves only two strings changed: reversing unit.focus alone yields initial manuscript SHA-256 `991469c5122f6f7cdfdd57244293aa6792114c41bc112494cd4517b92ec7800f`; reversing RS11.teacher alone yields initial material SHA-256 `e79201c2bc3636c66b2b57d715d0926c3831520ebd17317d90a003a16cf58363` exactly.

At the first checkpoint, the remaining lesson-11 Explain learner action still read `Check undefinedquotient,products/ATP,temperature and no-tasting/performed-evidence limits.` Its science was valid, but the substring could still fail the placeholder audit. I reported this exact remaining field. The author confirmed an attempted replacement had targeted the wrong phase column and corrected `lessons[10].phases[2][0]` before this verdict.

## Exact changes and independent reconstruction

[Diff/reconstruction script](evidence/gensci_1_5_recheck_diff.py) and [binding/results](evidence/gensci_1_5_recheck_diff.json) independently verify exactly three current string changes from the initially accepted canonical files:

| Field | Current wording |
|---|---|
| unit.focus phrase | `RQ with zero-denominator limits` |
| Lesson 11 Explain learner action | `Check cases with no defined quotient,products/ATP,temperature and no-tasting/performed-evidence limits.` |
| RS11.teacher phrase | `With zero oxygen consumption,RQ has no defined finite value and cannot identify a substrate` |

Reversing only these replacements reproduces the exact original manuscript/material bytes and SHA-256 values. Source record, source verification and blueprint hashes are unchanged. Current manuscript SHA-256 is `1f2e3ebc4cd0a330fa58d0b031b40356e28469b606176a4dda6272de591ba565`; current material SHA-256 is `fa851506bc879e9c6ae1157abfcc456744eceb16465362d146e009eca2d91e8d`. Neither current canonical file contains the placeholder substring.

These changes retain the accepted mathematical/scientific meanings: zero oxygen consumption does not produce RQ zero or a unique substrate diagnosis; the relevant cases have no conventional defined finite quotient. All numbers, pathway/function answers, controls, project approval conditions, no-brewing/no-food-release restrictions, actual-action limits, final prompts/exemplars/rubric and 17 calculation records are unchanged. No full source/protocol/math re-review was necessary. The initial report, independent-solution evidence and saved original WSU PDF remain hash-identical.

## Current five actual Word companions

[Current propagation check](evidence/gensci_1_5_recheck_check.py) and [results/current five Word hashes](evidence/gensci_1_5_recheck_check.json) pass **342/342** canonical propagation checks. All five binary hashes differ after rebuilding; their body text is independently bridged against the preserved initial extracts:

- CompactTeacherGuide changes only the corrected lesson-11 action.
- MaterialsTeacherKey changes only the RS11 teacher phrase.
- StudentMaterials, StudentSummaryTable and AssessmentMaterials body text is exactly unchanged.

The unit-focus change belongs to the later standard sequence/export and is not falsely claimed as visible in a companion that does not print that field. This body-text bridge does not assert all Word package parts or binary metadata are unchanged.

The twelve summary rows remain blank; full teacher answers/final exemplars remain absent from student companions; RS12 remains isolated from teaching StudentMaterials. No unexpected media payload appears and all five preserve OpenAI/ChatGPT/Codex attribution. Lesson phase sums remain 40 minutes. Updated current body extracts are saved separately as `gensci_1_5_*_recheck_review_text.txt`; the original extracts were not overwritten.

## Audit and scope limits

The author's diagnostic records that an earlier failed-audit shell sequence briefly copied a Core Mathematics 3.2 audit under the Respiration snapshot name. That mislabeled snapshot was removed and is not used as evidence here. Its recorded hash/module is diagnostic provenance, not Respiration acceptance. This focused verdict covers the current canonical three-string delta and five actual Word companions only. Standard final Word/PDF files and exports must be refreshed against the new fingerprint and receive a fresh successful, correctly scoped audit and independent final-artifact review.

School/teacher approval, controlled preparation and adult monitoring/chilling/disposal, actual individual project/record actions, pacing and all original classroom limits remain pending exactly as in the initial review. No input, production artifact, acceptance record or shared pipeline state was modified by the reviewer.
