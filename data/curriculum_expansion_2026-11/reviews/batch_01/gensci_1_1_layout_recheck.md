# General Science1.1 final artifact resource recheck

Status: COMPLETE — scoped final artifact PASS. The resource-selection HOLD is closed after inspecting the actual rebuilt guide; initial layout HOLD report preserved. Root verified shared usage24% at2026-11-13 08:52:18UTC, exit0/no pause; no sandbox escalation requested.

## Final scoped artifact verdict

**PASS within the actual reviewed artifact scope.** The unrelated-resource finding in gensci_1_1_layout_review.md is closed. Canonical content fingerprint independently recomputed unchanged: `fdbf788509d17e2bcf9b83537e6157ac32405419bb49339d0f3ac330a020865c`. This closes the artifact hold without changing canonical content/acceptance. No content or acceptance JSON edits by reviewer.

## Actual correction evidence

Read current resource_policy.json, workspace wrapper scripts/curriculum/resource_recommender.py and helper resource_policy.py. The module-specific allowed-title list is `gensci_1_1: []`; the wrapper passes the actual CBE_MODULE_NAME into exclusion logic and excludes an unvetted title for that module. Independent-assessment exclusion remains separate and takes priority. This is workspace curation over the existing matcher; no production-default matching change is required by the correction.

Inspected actual generated GS1.1 _link_matching JSON:7 lesson records×10 phase/type slots=70 slots; **all70 picked values are null**. Diagnostics retain candidate-pool information/runners-up, but those are not selected recommendations. Lesson7 has independent-assessment suppression reasons; other lessons use the module-vetting reason.

Inspected actual rebuilt CBE DOCX body and hyperlink relationships: **zero selected local topic-resource hyperlinks**, with only search/fallback and licensing links remaining. The previous hotel-manager/salary, power-series, multiplication-rule, compound-event probability, extrema and unvetted median/range titles are absent from both the actual DOCX body and complete extracted PDF text. Null blocks do not replace any required GS11–GS17 task or primary-source summary; supplied card references and official-page source activity remain intact. The final still uses GS17/independent-only instructions, not resource searching. Search placeholders remain teacher-preparation pointers and are not independent-task materials.

The rebuilt guide remains31 PDF pages. Visually inspected current PDF **pp3,11,15,23,27,28** with pdftoppm/view_image: the previously problematic L1/L3/L4/L6 blocks now show no selected match, and L7 Predict/Observe/Explain retains null selections and individual-only work. No new clipping/overlap or missing activity text identified in those samples. This is6 of31 pages, not an exhaustive visual review; complete guide text and DOCX hyperlinks were checked. Existing long null/search columns and page-spanning table rows are unchanged exporter behaviour.

## Other three standard outputs after the rebuild

Their binary hashes changed, so did not assume the earlier hash bindings still applied. Extracted current student FinalExplanation, FinalExplanation_TeacherKey and teacher SummaryTable PDF text and DOCX bodies: all three match the prior-reviewed text/body after whitespace normalisation. Rechecked79 current canonical-content conditions: exact common timing, all prompts/full rubrics, teacher exemplars confined to teacher key, and all seven teacher-summary rows; all pass. No new visual audit of those three was needed because the current body and PDF text are unchanged; their prior visual sample coverage/limits remain in the initial layout report. This is not a claim that a new independent Word rendering was performed.

The five companion types were reviewed earlier. Parent’s whole-batch27-pair technical audit is a separate technical check; this reviewer’s closure is based on the actual GS1.1 evidence above rather than treating another subject’s pass as evidence for this one. New current output hashes are recorded below. Initial content/layout reports remain unchanged as history.

## Limits retained

No live ARES playback, classroom trial or practical experiment was performed. Null recommendations mean no local item is being endorsed, not that no suitable resource could ever exist. Human confirmation remains needed for real device availability, individual observation, print-only digital-not-observed records, safe paper/water preparation, accessibility, actual40-minute pacing and correct GS17-only final distribution. Content and scoped artifact acceptance do not establish lasting attitude change, employment qualifications, universal transfer, classroom certification or cost/superiority claims.

## Current hash bindings

- `data/curriculum_expansion_2026-11/outputs/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science_CBE_LessonSequence.docx` SHA256 `ce7900b37a3ed3a4004b08d769e701e81912e53f4b311b84cfb4f1e709e63038`
- `data/curriculum_expansion_2026-11/outputs/PDF/Codex_General_Science_Introduction_to_General_Science_CBE_LessonSequence.pdf` SHA256 `1c36d6ba6cffe641cf29f11ad6fa1d7a8d2d45a8052a1435e9a902ac241e6b9d`
- `data/curriculum_expansion_2026-11/outputs/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science_FinalExplanation.docx` SHA256 `f85ba8dbccd73d2aacb65215c9524ff07e5f03accb8fd0e6d3260dfa88fbbcb4`
- `data/curriculum_expansion_2026-11/outputs/PDF/Codex_General_Science_Introduction_to_General_Science_FinalExplanation.pdf` SHA256 `4d465eb6b1e91135291e90d4f785f2e29f00d589a9f2eedcdb6883b001de2e23`
- `data/curriculum_expansion_2026-11/outputs/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science_FinalExplanation_TeacherKey.docx` SHA256 `c2af0486d4bd3d0bca101cadf6c07cbcf7a252d0dd4b261e3a0ed86a925741a5`
- `data/curriculum_expansion_2026-11/outputs/PDF/Codex_General_Science_Introduction_to_General_Science_FinalExplanation_TeacherKey.pdf` SHA256 `7abb34615438ce632dd93c606b7df629de00700f765824f5769762414fae50d8`
- `data/curriculum_expansion_2026-11/outputs/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science_SummaryTable.docx` SHA256 `6cd5ff12d0143b742153c8afaa7318ceceeebc62879256e8709dd3699a819d4c`
- `data/curriculum_expansion_2026-11/outputs/PDF/Codex_General_Science_Introduction_to_General_Science_SummaryTable.pdf` SHA256 `43ed943daa83a0cb9d4fb82f11b77aa79b6d403e14052c7a641950a4620df1c2`
- `data/curriculum_expansion_2026-11/resource_policy.json` SHA256 `87410e4d953c5300457db9d6a193e5218e71e3a30fb7868a74aa49bc43c63d46`
- `scripts/curriculum/resource_recommender.py` SHA256 `de179b8dd2279af86bf516dc38c576e251a1fd8e55401ea3eea3dbe97a9e7c20`
- `scripts/curriculum/resource_policy.py` SHA256 `a6c91efb58ad607aa87b8011d8fc1e87bdff0860c5060c2dd7f1d5110fa4267b`
- `data/curriculum_expansion_2026-11/outputs/_link_matching/v2/General_Science/SS1.1_Introduction_to_General_Science/Codex_General_Science_Introduction_to_General_Science.json` SHA256 `e36f1ac17b16c46924d0e497d2b156fd8c80dd0f34dfed73448dc0404c1d863a`

Preserved initial layout-report SHA256: `4060c76fcf540b8d88bfe9260e4d193693903d765d6e47413f4eecb20e94de4d`.
