# CLAUDE.md — Project Context for AI Assistant Sessions

## Repository
- **Branch**: `claude/setup-cbe-generation-ZKiIi`
- **Remote**: `markknit/cbe-generation-system`
- **Local path (Linux)**: `/home/user/cbe-generation-system`
- **Local path (Windows)**: `C:\Users\mrkni\cbe-generation-system`

## Workflow
User works on Windows, pushes via git. This Linux env pulls and runs Python scripts.
After every session: commit and push all changes so nothing is lost.
To sync Windows ↔ Linux: `git pull origin claude/setup-cbe-generation-ZKiIi` on Windows.

---

## PROJECT 1: Seavuria Reformatting — COMPLETE ✅

**Script**: `src/reformat_seavuria.py`
**Status**: All 9 output files generated. Round 4 complete. Awaiting user review feedback.
**Last commit**: `2f927d5`

### Output files (`data/outputs/Seavuria_Reformatted/`)
```
Chemistry_10_SubStrand1.4_ChemicalBonding_CBE_LessonSequence.docx
Chemistry_10_SubStrand1.4_ChemicalBonding_FinalExplanation.docx
Chemistry_10_SubStrand1.4_ChemicalBonding_SummaryTable.docx
Mathematics_10_SubStrand1.3_QuadraticEquations_CBE_LessonSequence.docx
Mathematics_10_SubStrand1.3_QuadraticEquations_FinalExplanation.docx
Mathematics_10_SubStrand1.3_QuadraticEquations_SummaryTable.docx
Physics_10_SubStrand1.4_ThermalExpansion_CBE_LessonSequence.docx
Physics_10_SubStrand1.4_ThermalExpansion_FinalExplanation.docx
Physics_10_SubStrand1.4_ThermalExpansion_SummaryTable.docx
```

### Subject keys (reformat_seavuria.py)
- `"chemistry"` → Chemistry_10_SubStrand1.4_ChemicalBonding
- `"mathematics"` → Mathematics_10_SubStrand1.3_QuadraticEquations
- `"physics"` → Physics_10_SubStrand1.4_ThermalExpansion

### To regenerate Seavuria outputs
```bash
cd /home/user/cbe-generation-system
python src/reformat_seavuria.py
```

---

## PROJECT 2: May18 CBE Templates — COMPLETE ✅

**Script**: `src/reformat_may18.py`
**Status**: All 12 output files generated. Committed `0467c02`. Awaiting user review feedback.

### Output files (`data/outputs/May18_Reformatted/`)
```
Biology_10_SubStrand2.2_TransportSystemInPlants_CBE_LessonSequence.docx
Biology_10_SubStrand2.2_TransportSystemInPlants_FinalExplanation.docx
Biology_10_SubStrand2.2_TransportSystemInPlants_SummaryTable.docx
Chemistry_10_SubStrand1.5_Periodicity_CBE_LessonSequence.docx
Chemistry_10_SubStrand1.5_Periodicity_FinalExplanation.docx
Chemistry_10_SubStrand1.5_Periodicity_SummaryTable.docx
Mathematics_10_SubStrand2.1_SimilarityEnlargement_CBE_LessonSequence.docx
Mathematics_10_SubStrand2.1_SimilarityEnlargement_FinalExplanation.docx
Mathematics_10_SubStrand2.1_SimilarityEnlargement_SummaryTable.docx
Physics_10_SubStrand1.5_MomentsEquilibrium_CBE_LessonSequence.docx
Physics_10_SubStrand1.5_MomentsEquilibrium_FinalExplanation.docx
Physics_10_SubStrand1.5_MomentsEquilibrium_SummaryTable.docx
```

### Subject keys and lessons (reformat_may18.py)
| Key | Subject | Lessons | Topic |
|---|---|---|---|
| `"biology"` | Biology 10 Sub-Strand 2.2 | 22 | Transport System in Plants |
| `"physics"` | Physics 10 Sub-Strand 1.5 | 6 | Moments and Equilibrium |
| `"chemistry"` | Chemistry 10 Sub-Strand 1.5 | 7 | The Periodicity |
| `"maths"` | Mathematics 10 Sub-Strand 2.1 | 12 | Similarity and Enlargement |

### Source files (READ-ONLY)
```
data/raw/CBE_Templates_May_18/
  BIOLOGY TRANSPORT SYSTEM IN PLANT  SCHEME OF WORK  (1).docx
  Grade 10 1.5 Moments and equilibrium (1).docx
  The periodicity.docx
  maths _ Geometry and measurement;Similarity and enlargement.docx
```

### AI-generated content marking
All AI-generated/inferred content renders **italic** in outputs.
- `_G(text)` — converts text to `gen_*` rich-content tuples (italic)
- `_gc(cell, text)` — writes italic text into a cell
- `gen_h3`, `gen_bullet`, `gen_text` kinds in `_cell_para_lines()` apply `italic=True`
- `_apply_run()` in `reformat_seavuria.py` already supports `italic` parameter

### To regenerate May18 outputs
```bash
cd /home/user/cbe-generation-system
python src/reformat_may18.py
```

### May18 builder functions
| Function | Purpose |
|---|---|
| `build_lesson_sequence(subject_key)` | CBE LessonSequence doc from meta["lessons_data"] |
| `build_final_explanation(subject_key)` | Final Explanation doc from meta["final_explanation_sections"] |
| `build_summary_table(subject_key)` | Summary Table doc from meta["summary_table_rows"] |

### May18 META dict structure (per subject in ALL_META)
```python
{
  "subject": str,
  "grade": str,
  "substrand": str,
  "lessons": int,
  "driving_question": str,
  "substrand_overview_rows": [(label, value), ...],
  "summary_table_headers": [str, ...],
  "summary_table_rows": [(num, col2, col3, col4, col5), ...],
  "summary_instructions": str,
  "final_explanation_sections": [(title, prompts, model_answer), ...],
  "final_explanation_rubric": {"headers": [...], "rows": [...]},
  "lessons_data": [lesson_dict, ...],
}
```

### Lesson dict structure (May18)
```python
{
  "number": int,
  "title": str,
  "inquiry_question": str,
  "slo_knowledge": str,
  "slo_skills": str,
  "slo_attitudes": str,
  "overview_purpose": str,
  "materials": str,
  "safety": str,
  "period1_heading": str,
  "period1_table": [_pr(...), ...],   # list of 5-tuples
  "period2_heading": str,
  "period2_table": [],                 # empty list if no period 2
  "reflections": [],
}
```

### `_pr()` helper — 5-tuple for Table C phase rows
```python
_pr(learner_experience, resource, teacher_actions, sensemaking, assessment)
```

---

## HOW TO START NEXT SESSION

1. `git pull origin claude/setup-cbe-generation-ZKiIi`
2. Read `CLAUDE.md` (this file)
3. User will provide review feedback on output .docx files
4. For Seavuria fixes: edit `src/reformat_seavuria.py`, then `python src/reformat_seavuria.py`
5. For May18 fixes: edit `src/reformat_may18.py`, then `python src/reformat_may18.py`
6. Commit and push when done

---

## SHARED INFRASTRUCTURE (src/reformat_seavuria.py)

`reformat_may18.py` imports everything from `reformat_seavuria` via:
```python
import reformat_seavuria as _sv
```
Never modify `reformat_seavuria.py` for May18-only needs — add local helpers to `reformat_may18.py`.

### KEY FUNCTIONS MAP (reformat_seavuria.py)

#### Parsers (read source .docx files)
| Function | Purpose |
|---|---|
| `iter_block_items(doc)` | Yields (kind, obj) for paragraphs AND tables in order |
| `parse_source(doc_path)` | Parses lessons from CBE LessonSequence source |
| `parse_section_a(doc_path)` | Parses sub-strand overview H3 sections |
| `parse_doc_sections(doc_path, prefixes)` | Parses H2 sections from FE / Summary Table source |
| `parse_framework_sections(doc_path)` | Parses "Framework" H2 → per-H3 content lists |

#### Text helpers
| Function | Purpose |
|---|---|
| `_text_to_rich(text)` | Converts plain text to `[(kind, str), ...]` — detects bullets/h3/quotes |
| `_enrich_content(content)` | Post-processes parsed content through `_text_to_rich()` |
| `_to_slo_list(text)` | Prefixes each `\n`-separated line with `- ` for SLO fields |
| `_prose_to_bullets(text)` | Splits prose sentences into bullet list — **returns list, use `_cell_para_lines()`** |

#### Cell writers
| Function | Purpose |
|---|---|
| `_cell_para(cell, text, ...)` | Single paragraph, manual bold/size/color |
| `_cell_para_lines(cell, content, size_pt)` | Renders rich `[(kind, str)]` content; supports `gen_*` italic kinds |
| `_cell_para_auto(cell, text, size_pt)` | Auto-detects bullets/h3 via `_text_to_rich()`; input must be str not list |

#### Builders (reformat_seavuria.py — Seavuria subjects only)
| Function | Purpose |
|---|---|
| `_build_table0_overview(doc, meta)` | Sub-strand overview table |
| `_build_table_A(doc, lesson)` | Lesson banner + SLOs (5r × 2c) |
| `_build_table_B(doc, lesson)` | Lesson overview (5r × 2c) |
| `_build_table_C_period(doc, lesson, period_num)` | Implementation framework (7r × 6c) for one period |
| `_build_table_D(doc, lesson)` | Teacher reflection (2r × 1c) |
| `_build_table_E(doc, summary_row)` | Summary table prompt (4r × 2c) |
| `_build_section_table(doc, header, content, ...)` | Generic 2-row section table |
| `build_lesson_sequence_docx(subject_key, lessons)` | Builds full Seavuria CBE LessonSequence doc |
| `build_final_explanation_docx(subject_key)` | Builds Seavuria Final Explanation doc |
| `build_summary_table_docx(subject_key)` | Builds Seavuria Summary Table doc |

---

## VERIFIED LOCKED FORMAT

### All Documents
- **Page size**: 11.000" × 8.500" (US Letter Landscape)
- **Margins**: 0.750" all sides
- **Title para**: 14pt bold, color `1F3864`
- **Subtitle para**: 11pt not-bold, color `1F6B75`
- **Font**: Arial (NOT Calibri)

### Color constants
| Constant | Hex | Usage |
|---|---|---|
| C_NAVY | 1F3864 | Lesson banner, section headers |
| C_TEAL | 1F6B75 | A./B. section headers |
| C_MED_BLUE | 2E74B5 | Table C header, FE section headers |
| C_PURPLE | 7030A0 | Summary table col 5 header |
| C_ORANGE | FF6600 | Table D header |
| C_LT_BLUE | D5E8F0 | Knowledge/Skills/Attitudes labels |
| C_PURPLE_LT | EAD1F5 | Key Inquiry, Table C Predict phase |
| C_TEAL_LT | D9EEF1 | Purpose in Storyline, Observe phase |
| C_GREEN_LT | E2EFDA | Explain phase |
| C_ORANGE_LT | FCE4D6 | Safety, DQB Creation phase |
| C_WHITE | FFFFFF | Content cells |
| C_LT_GRAY | F2F2F2 | Alternating summary table rows |

### Lesson Sequence per-lesson structure
```
TABLE 5r×2c (cols 2.083+7.417)  — Table A: LESSON BANNER + SPECIFIC SLOs
  PARA: [empty]
TABLE 5r×2c (cols 2.083+7.417)  — Table B: B. LESSON OVERVIEW
  PARA: [empty]
TABLE 7r×6c (0.625+1.775×5)    — Table C: C. LESSON IMPLEMENTATION FRAMEWORK
  PARA: [empty]
TABLE 2r×1c (col 9.5")          — Table D: D. TEACHER REFLECTION
  PARA: [empty]
TABLE 4r×2c (cols 2.083+7.417)  — Table E: E. SUMMARY TABLE PROMPT
  PARA: [empty]
  PARA: [empty]   ← two empty paras between lessons
```

### Table C Phase Names and Colors
- Row 2: "Predict Phase" (fill EAD1F5)
- Row 3: "Observe Phase" (fill D9EEF1)
- Row 4: "Explain Phase" (fill E2EFDA)
- Row 5: "Driving Question Board (DQB) Creation" (fill FCE4D6)
- Row 6: "Model Building Phase" (fill D5E8F0)

---

## SOURCE FILES — READ-ONLY, NEVER MODIFY

### Seavuria
```
data/raw/Seavuria Lesson Plans/
  Chemistry_Chemical_Bonding_CBE_LessonSequence_COMPLETE.docx
  Mathematics_Quadratic_Equations_CBE_LessonSequence_COMPLETE.docx
  Physics_Temperature_Thermal_Expansion_CBE_LessonSequence_COMPLETE.docx
  FINAL_EXPLANATION_Chemical_Bonding.docx
  FINAL_EXPLANATION_Quadratic_Equations.docx
  FINAL_EXPLANATION_Temperature_Thermal_Expansion.docx
  SUMMARY_TABLE_Chemical_Bonding.docx
  SUMMARY_TABLE_Quadratic_Equations.docx
  SUMMARY_TABLE_Temperature_Thermal_Expansion.docx
```

### May18
```
data/raw/CBE_Templates_May_18/
  BIOLOGY TRANSPORT SYSTEM IN PLANT  SCHEME OF WORK  (1).docx
  Grade 10 1.5 Moments and equilibrium (1).docx
  The periodicity.docx
  maths _ Geometry and measurement;Similarity and enlargement.docx
```

### Reference format files
```
data/outputs/docx/Grade 10 Bio/Bio 2.1 Plant Nutrition/docx/
  Biology_PlantNutrition_CBE_LessonSequence_L1-12.docx
  Biology_PlantNutrition_FinalExplanation.docx
  Biology_PlantNutrition_SummaryTable.docx
```

---

## KNOWN QUIRKS — DO NOT REGRESS

### reformat_seavuria.py parser quirks
- **Chemistry SLOs**: stored as one long dash-concatenated string in `Body Text` style — `_text_to_rich()` splits on ` - ` with 2+ occurrences
- **Physics SLOs**: Knowledge/Skills/Attitudes labels use `Heading 4` style; items use `normal` style — `parse_source()` detects H4 in section A; `_to_slo_list()` prefixes lines with `- `
- **Safety/Materials**: content is inline on same line as label — parser splits on `:` and seeds list with inline content
- **Sub-strand overview tables**: captured via `iter_block_items()` in `parse_section_a()`; first column of each non-header row → bullet
- **Final Explanation Framework**: parsed via `parse_framework_sections()` — splits on H3 boundaries; body text through `_text_to_rich()`
- **Rubric tables in Section E**: captured via `iter_block_items()` in `parse_doc_sections()`; header row → h3, data rows → bullet with first 2 cols joined by " | "

### reformat_may18.py known issues / fixes applied
- **`_prose_to_bullets()` returns a list** — must call `_cell_para_lines(cell, result)`, NOT `_cell_para_auto(cell, result)`. Using `_cell_para_auto` causes `AttributeError: 'list' object has no attribute 'strip'`
- **`_cell_para_lines()` has no `fill` parameter** — shading must be set separately via `_shade(cell, color)` before calling `_cell_para_lines`
- **May18 has no source parsing** — all content comes from inline META dicts; `build_lesson_sequence()` does NOT call `parse_source()` or `parse_section_a()`

---

## SEAVURIA FIX HISTORY (reference)

### Round 1: Sub-strand overview bullets, Table C bold, Table A/B reorganisation, safety content, Final Assessment bullets
### Round 2: Cycling row colors in overview, Table A restructured to 5r×2c, Table B rebuilt as 5r×2c
### Round 3: parse_source() H4 branch for Physics, parse_section_a() rewrite, parse_doc_sections() rewrite, safety inline capture, _build_section_table() → _enrich_content(), _to_slo_list() added
### Round 4: _to_slo_list() applied to SLO cells, parse_framework_sections() added, build_final_explanation_docx() uses parsed framework, _tbl_no_spacing() before tail sections, _prose_to_bullets() added and applied to summary table
