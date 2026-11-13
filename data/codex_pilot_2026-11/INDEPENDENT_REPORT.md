# OpenAI-only pilot: independent review and correction report

2026-11-12. Three independent subject reviews and focused correction rechecks are complete for the 31-lesson pilot. The reviewed draft is ready for teacher evaluation. This is not classroom acceptance, production promotion or proof of a monetary saving.

The initial independent reviewers reported 18 finding instances across the three subjects. Several were shared template/export issues. The pilot's closed numerical exercises agreed with independent recomputation; the review nevertheless found a misleading scale explanation, curriculum-transcription drift, assessment-administration contradictions and evidence/material gaps. These have been corrected or their claims explicitly limited. Initial reviews remain unchanged; the separate rechecks record the corrected state.

## Open the reviewed materials

Use each compact guide with its student materials. For the final independent lesson, distribute the separate **AssessmentMaterials** handout and student **FinalExplanation**, withholding earlier practice cards and both teacher keys. Blank **StudentSummaryTable** sheets are now supplied.

- [Essential Mathematics compact guide](outputs/PDF/Codex_Essential_Mathematics_Commercial_Arithmetic_1_CompactTeacherGuide.pdf)
- [Core Mathematics compact guide](outputs/PDF/Codex_Core_Mathematics_Area_of_Polygons_CompactTeacherGuide.pdf)
- [General Science compact guide](outputs/PDF/Codex_General_Science_Acids_Bases_and_Salts_CompactTeacherGuide.pdf)
- [Reviewed package](Review_Package_Reviewed.zip)

Each subject has nine DOCX/PDF types: standard CBE sequence, compact guide, student assessment, assessment key, teacher summary, student materials, materials teacher key, blank student summary and isolated assessment materials. Total: **27 DOCX + 27 PDF**, plus three R1 structured exports. Compact guides remain 10/13/11 pages for Essential/Core/Science. The original `REPORT.md`, `Review_Package.zip` and extracted `Review_Package/` are the pre-review snapshot, not this corrected deliverable.

## Review scope and comparison

| Unit | Pilot teaching time | Older baseline lesson records | Initial pilot findings | Baseline findings reported |
|---|---:|---:|---:|---:|
| Essential 2.8 Commercial Arithmetic (1) | 9 × 40 = 360 min | 8 × 40 = 320 min | 6 | 10 |
| Core 2.5 Area of Polygons | 12 × 40 = 480 min | 7 × 80 + 40 = 600 min | 7 | 12 |
| General Science 2.4 Acids, Bases and Salts | 10 × 40 = 400 min | 4 × 80 + 4 × 40 = 480 min | 5 | 10 |

These are reviewer finding instances, not error rates. The source crops do not specify lesson allocations; pilot counts are teaching-design decisions. The baseline Core and Science metadata each say 320 minutes, contradicting their own lesson durations. Core is 2.5, a different selection from the older paid API pilot's 2.4.

One fresh reviewer per subject read the source crop/record, blueprint, companion materials, manuscript, structured module and all original seven document types before inspecting baseline content. All closed numerical tasks, including unregistered values, were recomputed. Reviewers checked source wording, substantive outcomes, references, assessment keys/leakage, safety, practical fallbacks and timing. Full text/XML checks were combined with explicitly sampled PDF visual checks; not every rendered page was visually inspected. Author self-review and its report were excluded from the fresh reviews.

A server interruption stopped the first three reviewer attempts before reports were saved. Three fresh agents then completed the reviews with on-disk checkpoints. The same three completed focused correction checks; Science needed a second small correction pass. These are independent reviewers of the manuscript, using inherited Codex settings, not different-model-family or human corroboration. The runtime model identifier and exact subscription-credit consumption were not exposed and are not guessed.

## Corrections verified

- **Shared:** independent assessment strategies now require individual work; selected external recommendations are suppressed during assessment and searches deferred until collection. Blank student summaries and separate final-task data sheets are supplied. Pilot attribution accurately credits ChatGPT/Codex, OpenAI, while retaining framework/template credits.
- **Essential:** corrected source outcome c; narrowed the final rubric to performances actually elicited; blueprint separates final evidence from formative loss, quotation-comparison, reverse-rate and reverse-conversion checks. Role/currency slips now have explicit teacher preparation or oral alternatives.
- **Core:** corrected source competencies/values/PCI against an enlarged original-PDF crop. Explained the drawing scale as 1:500, with 1 cm² representing 25 m², retaining the correct 2100 m² result. Final tasks explicitly require Heron where the rubric requires it and disclose method cues. Added C13 local-object/material-reuse and use-of-area evidence within existing L7/L11 allocations; model-only fallbacks do not claim real collection/investigation. Teacher summaries now contain expected explanations.
- **Science:** replaced generic summary placeholders with concrete evidence/explanations; supplied an attributed printed G11 reference card for offline G9 work; removed the out-of-scope carboxylic-acid naming recommendation. Assessment claims now describe taught-model application/recall with limited numerical variation. The second pass removed an unsupported CDC reference name and clarified that basicity alone does not imply bleaching action.

See [correction ledger](reviews/corrections.json), [Essential initial review](reviews/independent/essmath_2_8.md) and [recheck](reviews/independent/essmath_2_8_recheck.md), [Core initial review](reviews/independent/coremath_2_5.md) and [recheck](reviews/independent/coremath_2_5_recheck.md), [Science initial review](reviews/independent/gensci_2_4.md) and [recheck](reviews/independent/gensci_2_4_recheck.md).

The source-summary card provides short attributed paraphrases rather than requiring live browsing in class. Sources include [WHO](https://www.who.int/news-room/fact-sheets/detail/sodium-reduction), [US EPA](https://www.epa.gov/nutrientpollution/basic-information-nutrient-pollution) and [University of Bristol](https://www.chm.bris.ac.uk/motm/bleach/Sodium%20Hypochlorite%20-%20Molecule%20of%20the%20Month%20October%202011.pdf); the card and science review state their scope and limits.

## Verification and delivery boundary

- Local corpus contract: three modules / 31 lessons, zero violations.
- Current R1 schema: three exports, zero errors.
- Registered calculations: 47/47 pass; all 31 phase allocations total 40 minutes. Independent solution ledgers also cover unregistered exercises.
- Resource-link and cross-document gates pass for all three. Pilot-only resource/attribution overrides preserve production defaults. This is not a new live check of every external resource.
- All 27 PDF/DOCX pairs present. Inventory, placeholder scan, accurate attribution, blank student rows, absence of teacher exemplars in student assessment, and final-resource selection checks pass. Artifact/source/build-script hashes recorded; reviewers visually rechecked affected/new samples.
- Partner rendering/preview passes for three bundles. **Partner ingestion remains blocked:** installed schema 1.0.0 rejects 1.1.0 and `belowExpectations`; 0/3 conform and 15 drift findings. The report-only command exits 0 despite drift; the enforcing ingestion check fails. The partner checkout was not changed. See `evidence/reviewed_lesson3_checks.log` and `evidence/reviewed_partner_verdict.json`.

## Baseline findings and their limits

The separate baseline reviews report 32 instances, including missing source outcomes/materials, inconsistent geometry or answer cues, assessment leakage and timing metadata. Science includes a wrong hydrogen gas-test instruction and contradictory ignition guidance. Essential includes incorrect percentage comparisons and financial interpretations. Core includes missing Heron/regular-heptagon coverage and incorrect geometric checks/answer keys. Exact evidence and recomputation are in the initial subject reports.

Those findings are report-only in this evaluation; baseline/production content has not been repaired or promoted. This three-unit, same-family, sequential review is not a blinded controlled experiment. Different content, scaffolding, duration and supplied assets prevent a numerical superiority or savings claim from the finding counts. They do provide concrete reasons to prefer source/material/solution records and external-to-the-writer checking as an authoring discipline.

## Cost evidence and remaining acceptance

No separately billed model API calls were made by this workflow. Subscription usage, retries after interruption, local compute and human review still have costs. Actual plan credits and teacher correction time were not measured, so there is no defensible monetary cost per accepted lesson or 43-module saving. The older API experiment's $7.65 ledger and $110–130 estimate are separate.

Teacher evaluation must still confirm pacing/prerequisites, access adjustments and sufficient practice. The exact 40-minute final schedules leave handling time to validate; the existing Essential rubric row spans two pages. Core local-object work and mathematical generality need classroom judgement. Science live work remains conditional on trained supervision, equipment, reagent identity, local risk assessment and disposal; evidence-card fallbacks do not demonstrate practical or digital skill.

**Checkpoint:** the reviewed pilot is available for teacher evaluation. Keep wider generation, promotion, Drive publication and partner delivery on hold pending the next user decision, classroom acceptance as appropriate, and partner R1 support. A bounded next evaluation should measure actual subscription usage and correction effort before extrapolating cost.
