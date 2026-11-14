# GS2.1 independent correction-pass1 recheck

**Verdict: ACCEPTED for the scoped content correction.** All three confirmed initial findings PT21-C27-1/2/3 are closed. Reviewer: core27. No author files, acceptance state, pipeline or outputs edited; no build/render run. This is a focused correction recheck, with the initial full-content review retained as evidence.

Current fingerprint: `058b76342d5c1528a43d4754c9661107d8fd7a7b12f5cd1ed7d458b5e9066e4c`.

Initial fingerprint: `cc8de7966bcfcb21987c42594ae16f797fa6fa197da958d8a7f9b5027a94a561`. Immutable initial report `gensci_2_1_initial_core27.md` remains SHA-256 `489712bd6e7ce32f7392617cddd9f4370afcabe71b8af9aa9fa57b5c75d006fa`.

## Exact delta and closure

Recovered the five original canonical files from the current repository HEAD and verified each byte hash against the frozen initial binding before using them as a comparison base. Preserved those exact before-files in the new evidence directory. Recursive comparison finds exactly15 changed JSON paths: PT7 student/key appendices; twelve outcome arrays (three affected lessons/tasks in each of manuscript lessons, blueprint lesson_map, assessment_map and assessment_tasks); and the L7 phase3 array, where only learner activity and evidence/check strings changed. No other canonical field changed. Source JSON, source verification, all other materials, arithmetic registry, unit, final prompts/exemplars, rubric, safety, minutes and all other lesson content are unchanged. Full before/after values are in `evidence/gensci_2_1_core27_pass1/delta.json`.

- **PT21-C27-1 closed:** PT7 explicitly asks learners to formulate sodium chloride and magnesium oxide from supplied valencies and show simplest combining ratios rather than just copy a formula. The teacher key correctly gives Na1/Cl1→1:1→NaCl and Mg2/O2→2:2 simplified to1:1→MgO. These are valency labels, not a new elemental diatomicity claim. L7 phase3 elicits construction and checks both formulae/ratios. That supports formative outcome e; unsupported d has been removed from all four linked arrays. The formula names appear earlier as oxidation examples, which is appropriate for this scaffolded formative task; the explicit ratio-construction evidence must be checked, and no blind or independent final-performance claim is inferred.
- **PT21-C27-2 closed:** all four L11/F11 linked arrays now claim f only; unchanged actual balancing/tally tasks support that claim.
- **PT21-C27-3 closed:** b is removed from all four L14/F14 linked arrays; actual classification remains in L3/F3, L12/F12 and final I1. Ion formation remains in L5/F5 and L6/F6; formula formulation remains in L7/F7, L8/F8, L9/F9, L13/F13 and final I3. All seven final lesson outcomes remain present. No source outcome or required source content/project was removed.

## Actual five-Word propagation and bindings

Current five actual Word companions pass466/466 propagation/structure checks and4/4 source-hash checks. Focused exact-delta/coverage/isolation checks pass36/36. The revised PT7 student prompt reaches StudentMaterials and MaterialsTeacherKey; revised teacher ratios reach MaterialsTeacherKey; both revised phase cells reach CompactTeacherGuide. Comparing every extracted paragraph with frozen initial Word text finds exactly two guide paragraph replacements, two teacher-key paragraph replacements and one student-material paragraph replacement, all matching the reviewed canonical corrections. AssessmentMaterials and StudentSummaryTable texts are byte-identical to the initial extracted text. All45 student-summary evidence cells remain empty; PT15 remains isolated from teaching materials, and its teacher answer remains absent from the student assessment reference. Attribution markers remain in all five companions. There are no media/embedded objects, consistent with the unit's learner-drawn diagram tasks and no supplied media assets.

New ZIP hashes reflect rebuilt files; unchanged assessment/summary text is established by paragraph/text comparison, not ZIP identity. All five current files and canonical-input hashes were rechecked immediately before this report was finalized and match the new binding.

| Actual companion | SHA-256 |
|---|---|
| AssessmentMaterials | `c74967f63cd86bfc086b4cce69ebc7f7d2c2896029cd857d30c70f268f306b36` |
| CompactTeacherGuide | `1c72a4068fad3af73f744177e2f987f92e22528b4b520c8e89d7beba3a8b840b` |
| MaterialsTeacherKey | `fc4d77ec6c2aac4f53562e7791514535d18995f3c9f8c109d64c5c90d6cdf913` |
| StudentMaterials | `3c89c4a9ec31bd990cf2dd196aad0b8233be52562afc3eec650c814064949bd9` |
| StudentSummaryTable | `e060332e8fd9a1a2ca630b92ebd0282dfce3eda04d368ac42214554cb43f8de0` |

Exact input/source hashes, reproducible checks, new extracted Word texts and the complete paragraph deltas are in `evidence/gensci_2_1_core27_pass1/`. The original review/evidence directory is unchanged.

## Limits retained

This recheck does not repeat unchanged full chemistry/source review or inspect rendered deliverable pages/PDFs. Initial169/169 independent chemistry derivations remain applicable; the newly explicit NaCl/MgO ratios were independently checked here. Actual five-model construction, actual common-substances chart, approved animation viewing, digital access, observed collaboration/material costs, local safety/access decisions and classroom/project/final pacing remain separately unconfirmed. The source specifies no official lesson allocation. No real learner or classroom performance is certified. The final artifact/layout gate is still separate.
