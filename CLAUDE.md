# CLAUDE.md — Project Context for AI Assistant Sessions

## Repository
- **Branch**: `claude/setup-cbe-generation-ZKiIi`
- **Remote**: `markknit/cbe-generation-system`
- **Local path (Linux)**: `/home/user/cbe-generation-system`
- **Local path (Windows)**: `C:\Users\mrkni\cbe-generation-system`

## Workflow
User works on Windows, pushes via git. This Linux env pulls and runs Python scripts.
After every session: commit and push all changes so nothing is lost.

---

## CURRENT TASK STATUS: Seavuria Reformatting — Round 4 Complete (Awaiting User Review)

**Script**: `src/reformat_seavuria.py`
**Status**: Script runs successfully. All 9 output files generated in `data/outputs/Seavuria_Reformatted/`.
**Last commit**: `2f927d5` — "Round 4 formatting fixes: SLO bullets, FE sub-headers, summary table bullets"

### Output files (9 total in `data/outputs/Seavuria_Reformatted/`)
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

---

## COMPLETE HISTORY OF FIXES (all rounds)

### Round 1 fixes
1. Sub-strand overview sections 3, 5, 10: bullet/bold formatting
2. Table C cells: bullet/bold in Learner Experience column
3. Table A/B: reorganised content to correct sections
4. Safety notes: now shows actual content when it exists
5. Final Assessment: bullets and bolding

### Round 2 fixes
1. Sub-strand overview: cycling row colors (C_LT_BLUE, C_PURPLE_LT, C_TEAL_LT, C_GREEN_LT, C_ORANGE_LT)
2. **Table A** restructured to 5 rows (was 9):
   - R0: navy "LESSON N: Title" (merged)
   - R1: teal "A. SPECIFIC LEARNING OUTCOMES" (merged, 11pt)
   - R2: lt-blue "Knowledge" | content
   - R3: lt-blue "Skills" | content
   - R4: lt-blue "Attitudes" | content
3. **Table B** rebuilt as 5-row 2-col table:
   - R0: teal merged "B. LESSON OVERVIEW"
   - R1: purple-lt "Key Inquiry Question" | content
   - R2: teal-lt "Purpose in Storyline" | content
   - R3: orange-lt "Safety Considerations" | content
   - R4: lt-blue "Materials Needed" | content
4. Section C/D/E: more bullets and bolding

### Round 3 fixes
1. **parse_source()**: Added `elif section == "A": buffer.append(text)` in the `heading 4` branch so Physics "Knowledge:", "Skills:", "Attitudes:" labels are captured (not skipped)
2. **parse_section_a()**: Rewrote to use `iter_block_items()` — captures table rows (Core Competencies, Values tables) as bullets; handles H4 sub-sections with `after_h4` flag
3. **parse_doc_sections()**: Rewrote to use `iter_block_items()` — captures table rows as `("h3", header)` and `("bullet", row)` items (for rubric tables in Section E)
4. **Safety/Materials parser**: Fixed inline capture — `inline = ln.split(":", 1)[1].strip()` to seed list with content on same line as label
5. **_build_section_table()**: Now calls `_enrich_content(content)` instead of raw content
6. **_enrich_content()**: Added — re-processes `text` items through `_text_to_rich()` and promotes short bullet-ending-`:` to h3
7. **_to_slo_list()**: Added — prefixes each `\n`-separated line with `- ` for multi-line SLO text (Physics style)

### Round 4 fixes (this session)
1. **Table A SLO cells**: Applied `_to_slo_list()` wrapper to Knowledge/Skills/Attitudes cell writes
2. **parse_framework_sections()**: New function — parses the "Framework" H2 section from source Final Explanation docx, splits at H3 boundaries, runs body text through `_text_to_rich()` so "Guiding Questions:", "What to Include:", "Suggested Diagrams:" become bold h3 entries
3. **build_final_explanation_docx()**: Now uses `parse_framework_sections()` for sections 1–N instead of hardcoded META prompts; falls back to META if parse returns nothing; model answers still come from META by position
4. **Space before Example**: Added `_tbl_no_spacing(doc)` after Assessment Rubric table and before tail sections loop
5. **Summary Table bullets**: Added `_prose_to_bullets()` helper — splits multi-sentence prose on sentence boundaries (`. [A-Z]`); applied to all 4 data columns in summary table rows

---

## KEY FUNCTIONS MAP (src/reformat_seavuria.py)

### Parsers (read source .docx files)
| Function | Purpose | Lines (approx) |
|---|---|---|
| `iter_block_items(doc)` | Yields (kind, obj) for paragraphs AND tables in order | ~788 |
| `parse_source(doc_path)` | Parses lessons from CBE LessonSequence source | ~800 |
| `parse_section_a(doc_path)` | Parses sub-strand overview H3 sections | ~900 |
| `parse_doc_sections(doc_path, prefixes)` | Parses H2 sections from Final Explanation / Summary Table source | ~1191 |
| `parse_framework_sections(doc_path)` | Parses "Framework" H2 → per-H3 content lists | ~1256 |

### Text helpers
| Function | Purpose |
|---|---|
| `_text_to_rich(text)` | Converts plain text to `[(kind, str), ...]` — detects bullets/h3/quotes |
| `_enrich_content(content)` | Post-processes parsed content: re-runs `text` items through `_text_to_rich()` |
| `_to_slo_list(text)` | Prefixes each `\n`-separated line with `- ` for SLO fields |
| `_prose_to_bullets(text)` | Splits prose sentences into bullet list for summary table cells |

### Cell writers
| Function | Purpose |
|---|---|
| `_cell_para(cell, text, ...)` | Single paragraph, manual bold/size/color |
| `_cell_para_lines(cell, content, size_pt)` | Renders rich `[(kind, str)]` content |
| `_cell_para_auto(cell, text, size_pt)` | Auto-detects bullets/h3 via `_text_to_rich()` |

### Builders (write output .docx)
| Function | Purpose |
|---|---|
| `_build_table0_overview(doc, meta)` | Sub-strand overview table |
| `_build_table_A(doc, lesson)` | Lesson banner + SLOs (5r × 2c) |
| `_build_table_B(doc, lesson)` | Lesson overview (5r × 2c) |
| `_build_table_C(doc, lesson)` | Implementation framework (7r × 6c) |
| `_build_table_D(doc, lesson)` | Teacher reflection (2r × 1c) |
| `_build_table_E(doc, lesson)` | Summary table prompt (4r × 2c) |
| `_build_section_table(doc, header, content, ...)` | Generic 2-row section table |
| `build_lesson_sequence_docx(subject_key)` | Builds full CBE LessonSequence doc |
| `build_final_explanation_docx(subject_key)` | Builds Final Explanation doc |
| `build_summary_table_docx(subject_key)` | Builds Summary Table doc |

### Content (META dict, per subject)
- `meta["substrand_overview_rows"]` — sub-strand overview label/value pairs
- `meta["summary_table_rows"]` — list of 5-tuples per lesson for summary table
- `meta["summary_table_headers"]` — column headers for summary table
- `meta["final_explanation_sections"]` — list of (title, prompts, model_answer) — NOW used only for model_answer fallback; prompts come from parsed source
- `meta["final_explanation_rubric"]` — rubric headers + rows

### Subject keys
- `"chemistry"` → Chemistry_10_SubStrand1.4_ChemicalBonding
- `"mathematics"` → Mathematics_10_SubStrand1.3_QuadraticEquations
- `"physics"` → Physics_10_SubStrand1.4_ThermalExpansion

---

## SOURCE FILES (READ-ONLY — never modify)
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

## REFERENCE FORMAT FILES (READ-ONLY — never modify)
```
data/outputs/docx/Grade 10 Bio/Bio 2.1 Plant Nutrition/docx/
  Biology_PlantNutrition_CBE_LessonSequence_L1-12.docx
  Biology_PlantNutrition_FinalExplanation.docx
  Biology_PlantNutrition_SummaryTable.docx
```

---

## VERIFIED LOCKED FORMAT (from Bio reference diagnostics)

### All Documents
- **Page size**: 11.000" × 8.500" (US Letter Landscape)
- **Margins**: 0.750" all sides
- **Title para**: 14pt bold, color `1F3864`
- **Subtitle para**: 11pt not-bold, color `1F6B75`
- **Font**: Arial (NOT Calibri)

### Color constants (in script)
| Constant | Hex | Usage |
|---|---|---|
| C_NAVY | 1F3864 | Lesson banner, section headers |
| C_TEAL | 1F6B75 | A./B. section headers |
| C_MED_BLUE | 2E74B5 | Table C header, FE section headers |
| C_PURPLE | 7030A0 | Summary table col 5 header |
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

## HOW TO START NEXT SESSION
1. `git pull origin claude/setup-cbe-generation-ZKiIi`
2. Read `CLAUDE.md` (this file) — everything you need is here
3. User will provide review feedback from Windows; make fixes, then:
4. `cd /home/user/cbe-generation-system && python src/reformat_seavuria.py`
5. Commit and push when done

## KNOWN PARSER QUIRKS (do not regress)
- **Chemistry SLOs**: stored as one long dash-concatenated string in `Body Text` style — `_text_to_rich()` splits on ` - ` with 2+ occurrences
- **Physics SLOs**: Knowledge/Skills/Attitudes labels use `Heading 4` style; items use `normal` style on separate lines — `parse_source()` detects H4 in section A and adds to buffer; `_to_slo_list()` prefixes lines with `- `
- **Safety/Materials**: content is inline on same line as label ("Safety Considerations: item1 - item2") — parser splits on `:` and seeds the list with inline content
- **Sub-strand overview tables** (Core Competencies, Values): captured via `iter_block_items()` in `parse_section_a()`; first column of each non-header row → bullet
- **Final Explanation Framework**: parsed via `parse_framework_sections()` — splits on H3 boundaries; body text run through `_text_to_rich()` so "Guiding Questions:" etc. become h3
- **Rubric tables in Section E** (Final Model Rubric, Summary Table Rubric): captured via `iter_block_items()` in `parse_doc_sections()`; header row → h3, data rows → bullet with first 2 cols joined by " | "
