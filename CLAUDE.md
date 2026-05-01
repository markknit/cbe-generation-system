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

## CURRENT TASK STATUS: Seavuria Reformatting — COMPLETED (Needs User Review)

**Script**: `src/reformat_seavuria.py`
**Status**: Script runs successfully. All 9 output files generated in `data/outputs/Seavuria_Reformatted/`.

### What was done this session
A complete rewrite of the builder section of `src/reformat_seavuria.py` was performed.

**All fixes applied:**
1. **Font**: Changed from Calibri → **Arial** (matching Bio reference)
2. **Phase names**: Now use full Bio-reference names: "Predict Phase", "Observe Phase", "Explain Phase", "Driving Question Board (DQB) Creation", "Model Building Phase"
3. **Table A structure** (per lesson): Corrected to match Bio reference exactly:
   - R0: navy "LESSON N: Title" (merged)
   - R1: teal "A. SPECIFIC LEARNING OUTCOMES" (merged, 11pt)
   - R2: lt-blue "Purpose" (added — was missing)
   - R3: lt-blue "Knowledge" (no colon)
   - R4: lt-blue "Skills" (no colon)
   - R5: lt-blue "Attitudes" (was "Attitudes & Values:")
   - R6: purple-lt "Key Inquiry Question" (no colon)
   - R7: teal-lt "Purpose in Storyline" (no colon)
   - R8: orange-lt "Safety Notes" (was "Safety:")
   - Removed the incorrect "B. Lesson Overview" merged row that was previously inside Table A
   - Col widths: [2.083, 7.417] (matching Bio)
4. **Table B**: Changed label to "B. LESSON OVERVIEW" (11pt) — content now includes inquiry question + overview + materials
5. **Table C**: 
   - Single table per lesson (was TWO — now P1 and P2 combined in one table)
   - Col widths: [0.625, 1.775, 1.775, 1.775, 1.775, 1.775] (matching Bio)
   - Header: "C. LESSON IMPLEMENTATION FRAMEWORK" (uppercase, 11pt)
6. **Table D**: Header now "D. TEACHER REFLECTION" (uppercase, 11pt)
7. **Table E**: 
   - Col widths: [2.083, 7.417] (was [2.5, 7.0])
   - Header: "E. SUMMARY TABLE PROMPT  (pre-filled example for this lesson)" (uppercase, 11pt)
   - Content cells now PRE-FILLED from summary_table_rows data
8. **Overview Table 0**: Now has navy "SUB-STRAND OVERVIEW" banner as first row
9. **Para spacing**: 1 empty para between tables, 2 between lessons (matching Bio)
10. **Final Explanation**: 
    - Section headers now UPPERCASE
    - Model answers added to all response cells (no more "[Write your response here]" placeholder)
    - Instructions header: "INSTRUCTIONS FOR STUDENTS" (uppercase, 11pt)
    - Student name/class/date fields have underscores (matching Bio)
11. **Summary Table**:
    - All header labels now uppercase with 11pt
    - Chemistry: ALL 13 lesson rows now populated with substantive content (lessons 2-12 were previously empty)
    - Physics: ALL 6 lesson rows now populated (lessons 2, 4, 5, 6 were previously empty)
    - Math: was already complete, verified correct

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

### Source content files (READ-ONLY, do not modify)
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

### Reference format files (READ-ONLY, do not modify)
```
data/outputs/docx/Grade 10 Bio/Bio 2.1 Plant Nutrition/docx/
  Biology_PlantNutrition_CBE_LessonSequence_L1-12.docx
  Biology_PlantNutrition_FinalExplanation.docx
  Biology_PlantNutrition_SummaryTable.docx
```

---

## VERIFIED LOCKED FORMAT (from actual Bio reference diagnostics)

### All Documents
- **Page size**: 11.000" × 8.500" (US Letter Landscape)
- **Margins**: 0.750" all sides
- **Title para**: 14pt bold, color `1F3864`
- **Subtitle para**: 11pt not-bold, color `1F6B75`
- **Font**: **Arial** (NOT Calibri)

### Lesson Sequence — per-lesson structure (confirmed from Bio reference)
```
TABLE 9r×2c (cols 2.083+7.417)  — Table A: LESSON BANNER + SPECIFIC SLOs
  PARA: [empty]
TABLE 2r×1c (col 9.5")          — Table B: B. LESSON OVERVIEW
  PARA: [empty]
TABLE 7r×6c (0.625+1.775×5)     — Table C: C. LESSON IMPLEMENTATION FRAMEWORK
  PARA: [empty]
TABLE 2r×1c (col 9.5")          — Table D: D. TEACHER REFLECTION
  PARA: [empty]
TABLE 4r×2c (cols 2.083+7.417)  — Table E: E. SUMMARY TABLE PROMPT (pre-filled...)
  PARA: [empty]
  PARA: [empty]   ← two empty paras between lessons
```

### Table A Row Layout (confirmed)
- R0: fill=1F3864 "LESSON N: Title" (merged, 11pt bold white)
- R1: fill=1F6B75 "A. SPECIFIC LEARNING OUTCOMES" (merged, 11pt bold white)
- R2: fill=D5E8F0 "Purpose" | fill=FFFFFF content (9pt)
- R3: fill=D5E8F0 "Knowledge" | fill=FFFFFF content (9pt)
- R4: fill=D5E8F0 "Skills" | fill=FFFFFF content (9pt)
- R5: fill=D5E8F0 "Attitudes" | fill=FFFFFF content (9pt)
- R6: fill=EAD1F5 "Key Inquiry Question" | fill=FFFFFF content (9pt)
- R7: fill=D9EEF1 "Purpose in Storyline" | fill=FFFFFF content (9pt)
- R8: fill=FCE4D6 "Safety Notes" | fill=FFFFFF content (9pt)

### Table C Phase Names (confirmed)
- "Predict Phase" (fill EAD1F5)
- "Observe Phase" (fill D9EEF1)
- "Explain Phase" (fill E2EFDA)
- "Driving Question Board (DQB) Creation" (fill FCE4D6)
- "Model Building Phase" (fill D5E8F0)

---

## How to Start Next Session
1. `git pull origin claude/setup-cbe-generation-ZKiIi`
2. Read `CLAUDE.md` (this file)
3. User may request further adjustments after reviewing the output files on Windows
4. To regenerate: `cd /home/user/cbe-generation-system && python src/reformat_seavuria.py`
5. Commit and push when done

## If Further Fixes Are Needed
- All format changes are in `src/reformat_seavuria.py`
- Parser functions (lines ~788–953): DO NOT CHANGE — they work correctly
- Builder functions start at the `# LESSON SEQUENCE BUILDER` section
- META dict contains all content: summary_table_rows, final_explanation_sections, substrand_overview_rows
- Run `python src/reformat_seavuria.py` to regenerate all 9 files
