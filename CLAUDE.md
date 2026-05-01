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

## CURRENT TASK (In Progress — Pick Up Here)

### Task: Reformat Seavuria Lesson Plans — REWRITE NEEDED

**Script**: `src/reformat_seavuria.py`
**Status**: Parser works correctly. Builder produces **WRONG FORMAT**. Must be rewritten.

**What's wrong**: The current builder invents its own color scheme and table structure.
It must exactly replicate the **locked Biology Plant Nutrition format**.

**Reference format files** (READ-ONLY, do not modify):
```
data/outputs/docx/Grade 10 Bio/Bio 2.1 Plant Nutrition/docx/
  Biology_PlantNutrition_CBE_LessonSequence_L1-12.docx   ← locked lesson sequence format
  Biology_PlantNutrition_FinalExplanation.docx            ← locked final explanation format
  Biology_PlantNutrition_SummaryTable.docx                ← locked summary table format
```

**Source content files** (read to extract content):
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

**Required output** — 9 files in `data/outputs/Seavuria_Reformatted/`:
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

## LOCKED FORMAT SPECIFICATION

### All Documents
- **Page size**: 11.000" × 8.500" (US Letter Landscape)
- **Margins**: 0.750" all sides (uniform)
- **Title para**: 14pt bold, color `1F3864` (dark navy)
- **Subtitle para**: 11pt not-bold, color `1F6B75` (teal)
- **Font**: Calibri throughout

### Color Palette
| Name | Hex | Used For |
|------|-----|---------|
| Navy | `1F3864` | Titles, Phase col header, Table A banner |
| Teal | `1F6B75` | Subtitles, Table B/Resource/Sensemaking headers |
| Med Blue | `2E75B6` | Learner Exp/Teacher Actions/Assessment headers |
| Purple | `7030A0` | Table E header, Summary Table DQB col header |
| Orange | `C55A11` | Table D header |
| Lt Blue | `D5E8F0` | SLO labels, Key Inquiry bg, summary lesson# col |
| Teal Lt | `D9EEF1` | Observe phase row |
| Green Lt | `E2EFDA` | Explain phase row |
| Purple Lt | `EAD1F5` | Predict phase row, Table E row labels, DQB col |
| Orange Lt | `FCE4D6` | DQB phase row, Table D content |
| Model Blue | `D5E8F0` | Model Building phase row (same as Lt Blue) |
| Lt Gray | `F2F2F2` | Alternating content rows |
| White | `FFFFFF` | Main content rows |

### Document 1: Lesson Sequence (LessonSequence.docx)

**Structure per document**:
1. Title paragraph
2. Subtitle paragraph  
3. Sub-strand overview Table 0 (15r × 2c)
4. For each lesson: 5 tables (A through E) — NO extra paragraphs between tables within a lesson

**Table A — SLOs (9r × 2c)**, total width 9.5":
- R0: merged, fill `1F3864` (navy) — "LESSON N: Title"
- R1: merged, fill `1F6B75` (teal) — "A. Specific Learning Outcomes"
- R2: fill `D5E8F0` label col, white content — "Knowledge:"
- R3: fill `D5E8F0` label col, white content — "Skills:"
- R4: fill `D5E8F0` label col, white content — "Attitudes & Values:"
- R5: merged, fill `1F6B75` (teal) — "B. Lesson Overview"
- R6: R0=`EAD1F5` "Key Inquiry Question:", R1=white (question text)
- R7: R0=`D9EEF1` "Purpose in Storyline:", R1=white (purpose text)
- R8: R0=`FCE4D6` "Safety:", R1=white (safety text)

**Table B — Materials/Overview (2r × 1c)**:
- R0: fill `1F6B75` — "Materials"
- R1: fill `FFFFFF` — materials list text

**Table C — Implementation (7r × 6c)**, total width 9.5":
- R0: merged all 6 cols, fill `1F6B75` — "C. Lesson Implementation Framework — Period N (40 min)"
- R1: col headers: Phase=`1F3864`, Learner Exp=`2E75B6`, Resource=`1F6B75`, Teacher Actions=`2E75B6`, Sensemaking=`1F6B75`, Assessment=`2E75B6`
- R2: Phase="Predict", fill `EAD1F5` for Phase col; content cols alternate `FFFFFF`/`F2F2F2`
- R3: Phase="Observe", fill `D9EEF1` for Phase col
- R4: Phase="Explain", fill `E2EFDA` for Phase col
- R5: Phase="DQB", fill `FCE4D6` for Phase col
- R6: Phase="Model Building", fill `D5E8F0` for Phase col
- **Col widths**: Phase=1.0", Learner Exp=2.5", Resource=1.0", Teacher Actions=2.0", Sensemaking=1.5", Assessment=1.5" (total 9.5")

**Table D — Reflection (2r × 1c)**:
- R0: fill `C55A11` (orange) — "D. Teacher Reflection"
- R1: fill `FCE4D6` (light orange) — reflection questions text

**Table E — Summary Prompt (4r × 2c)**:
- R0: merged 2 cols, fill `7030A0` (purple) — "E. Summary Table Prompt"
- R1: R0=`EAD1F5` bold "What did I observe?", R1=white (student writes)
- R2: R0=`EAD1F5` bold "What did I learn?", R1=white (student writes)
- R3: R0=`EAD1F5` bold "How does this explain the phenomenon?", R1=white

### Document 2: Final Explanation (FinalExplanation.docx)

**8 tables total**:

**Table 0 (5r × 2c)** — Header block:
- R0: merged, fill `1F3864` — subject/grade/substrand title
- R1: merged, fill `1F6B75` — "Final Explanation Document"
- R2: R0=`D5E8F0` "Student Name:", R1=white
- R3: R0=`D5E8F0` "Class:", R1=white
- R4: R0=`D5E8F0` "Date:", R1=white

**Table 1 (2r × 1c)** — Instructions:
- R0: fill `1F6B75` — "Instructions"
- R1: fill `FFFFFF` — instructions text

**Tables 2–6 (3r × 1c each)** — One per section (5 sections):
- R0: fill `2E75B6` (medium blue) — section title (e.g., "Section 1: The Phenomenon")
- R1: fill `D5E8F0` (light blue) — prompt/question text
- R2: fill `FFFFFF` — example answer / student response area

**Table 7 (7r × 4c)** — Rubric:
- R0: merged, fill `1F3864` — "Assessment Rubric"
- R1: col headers — `2E75B6` / `1F6B75` / `2E75B6` / `1F6B75`
- R2–R6: R0=`D5E8F0` criterion label; R1-R3 alternating `FFFFFF`/`F2F2F2`

### Document 3: Summary Table (SummaryTable.docx)

**3 tables total**:

**Table 0 (4r × 2c)** — Header block:
- R0: merged, fill `1F3864` — subject/grade/substrand title
- R1: merged, fill `1F6B75` — "Summary Table"
- R2: R0=`D5E8F0` "Sub-Strand:", R1=white
- R3: R0=`D5E8F0` "Driving Question:", R1=white

**Table 1 (2r × 1c)** — Instructions:
- R0: fill `1F6B75` — "Instructions"
- R1: fill `FFFFFF` — instructions text

**Table 2 (N+1 rows × 5c)** — Main summary table:
- **Col widths**: Lesson#=0.833", Col2=2.167", Col3=2.167", Col4=2.167", DQB=2.167" (total 9.501")
- R0: headers — Lesson#=`1F3864`, Col2=`2E75B6`, Col3=`1F6B75`, Col4=`2E75B6`, DQB col=`7030A0`
- Data rows: Lesson# col=`D5E8F0`; DQB col=`EAD1F5`; other cols alternate `FFFFFF`/`F2F2F2`

---

## What the parser already does correctly (DO NOT change)
- `parse_source()` correctly extracts 13/7/6 lessons from chemistry/math/physics
- `iter_block_items()` — correct
- `is_impl_table()` — correct
- `META` dict — correct
- Only the **builder functions** need to be replaced

## Source table column mapping
Source 5-col tables have these headers:
`Learner Experience | Resource Link | Teacher Moves | Sensemaking Strategy | Formative Assessment`

These map to the 6-col locked format as:
- Phase → **extract from Learner Experience text** (first word/phrase before the activity) or leave blank for student to fill
- Learner Experience → Learner Experience
- Resource Link → Resource  
- Teacher Moves → Teacher Actions
- Sensemaking Strategy → Sensemaking Strategy
- Formative Assessment → Assessment Strategy

The source tables do NOT have a "Phase" column. Each row represents one phase. The phase names (Predict, Observe, Explain, DQB, Model Building) must be assigned based on row order or text cues in the Learner Experience column.

---

## How to Start Next Session
1. `git pull origin claude/setup-cbe-generation-ZKiIi`
2. Read `CLAUDE.md` (this file) and `PROJECT_CONTEXT.md` if it exists
3. Read the reference Bio docs to verify format details before writing
4. Rewrite the builder portion of `src/reformat_seavuria.py`
5. Test: `cd /home/user/cbe-generation-system && python src/reformat_seavuria.py`
6. Check output in `data/outputs/Seavuria_Reformatted/`
7. Commit and push when done
