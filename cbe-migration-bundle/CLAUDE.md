# CLAUDE.md — Kenya CBE Lesson Plan Generation System

> This file is read automatically by Claude Code at the start of every session.
> Keep it concise and actionable. Full context is in PROJECT_CONTEXT.md.

---

## Project Identity

**Goal:** Generate Kenya Competency-Based Education (CBE) lesson plan documents at scale (~2,000 lessons across Biology, Physics, Chemistry, Mathematics — Grade 10).

**Server:** `jhm-spark` | **User:** `markk` | **Project root:** `/home/markk/ares/cbe-generation-system`

**Curriculum authority:** KICD (Kenya Institute of Curriculum Development), March 2025 edition.
All learning outcomes, strand/sub-strand names, core competencies, values, PCIs, and key inquiry questions **must match the official KICD curriculum document verbatim** unless explicitly instructed otherwise.

---

## Repository Layout

```
/home/markk/ares/cbe-generation-system/
├── venv/                        # Python virtual environment (activate before running Python)
├── src/                         # Python generation scripts (legacy / API orchestration)
├── generators/                  # JS docx generators (primary output method — see below)
│   ├── biology_1_3_cell_structure.js
│   ├── biology_1_4_chemicals_of_life.js
│   └── template/                # Shared helper functions (to be extracted)
├── data/
│   ├── raw/
│   │   ├── curriculum_pdfs/     # Official KICD curriculum PDFs
│   │   └── template_examples/   # Reference lesson plan documents
│   └── outputs/
│       └── docx/                # Generated .docx files
├── config/
│   └── generation_config.yaml
└── PROJECT_CONTEXT.md           # Full project history and context restoration
```

---

## Document Generation: How It Works

### Primary method: JavaScript + `docx` npm package

All lesson plan `.docx` files are generated using Node.js with the `docx` library (v9.x).

```bash
# Check node and docx are available
node --version          # should be v18+
npm list -g docx        # should show docx@9.x

# Run a generator
node generators/biology_1_4_chemicals_of_life.js

# Validate output
python3 scripts/office/validate.py data/outputs/docx/output.docx
```

### Why not python-docx?
Earlier work used `python-docx` but it produced formatting issues with complex tables. The JS `docx` library gives precise control over column widths, cell shading, and DXA measurements required for the lesson plan format.

### Claude API model
```
claude-sonnet-4-6
```
Update this string in `src/` Python files if a new model is released. Use `grep -rn "claude-sonnet\|claude-opus\|claude-haiku" src/` to find all occurrences.

---

## Document Format Standards

All generated `.docx` files must follow these standards exactly:

| Property | Value |
|---|---|
| Page orientation | Portrait |
| Page size | US Letter (12240 × 15840 DXA) |
| Margins | 0.75 inch all sides (1080 DXA) |
| Font | Arial throughout |
| Body text size | 18pt (size: 18 in docx-js = 9pt; use size: 18 for ~9pt) |
| Heading colour | Dark blue `#1F3864` |

**Critical docx-js rules (do not violate):**
- Never use `\n` inside text — use separate `Paragraph` elements
- Never use unicode bullet characters — use `LevelFormat.BULLET` with numbering config
- Always set both `columnWidths` array on the table AND `width` on each cell
- Always use `WidthType.DXA` — never `WidthType.PERCENTAGE`
- Always use `ShadingType.CLEAR` — never `ShadingType.SOLID`
- Content width with 0.75" margins on US Letter = **9360 DXA**

---

## Lesson Plan Template Structure

Every lesson plan document contains:

### A. Sub-Strand Overview Table (one per document)
Rows (in order):
1. Grade Level
2. Subject
3. Strand (official KICD number and name)
4. Sub-Strand (official KICD number and name)
5. Total Duration (n of X lessons × 40 minutes)
6. Sub-Strand Content (bullet list — verbatim from KICD)
7. Specific Learning Outcomes (a–e — verbatim from KICD)
8. Core Competencies (from KICD + supplemented)
9. Core Values (from KICD + supplemented)
10. Pertinent & Contemporary Issues (from KICD)
11. Key Inquiry Questions (verbatim from KICD)
12. Anchoring Phenomenon (invented or from template doc if provided)
13. Driving Question (invented or from template doc if provided)
14. Storyline Thread (invented or from template doc if provided)

### B. Per-Lesson Structure (repeated for each lesson)
Each lesson has five sections:

**Section A — Specific Learning Outcomes table**
Rows: Purpose | Knowledge (bullets) | Skills (bullets) | Attitudes (bullets) | Purpose in Storyline | Safety Notes

**Section B — Lesson Overview**
2 paragraphs of prose.

**Section C — Lesson Implementation Framework**
6-column table. Column 1 = Phase label. Columns 2–6 = content.

| Phase | Learner Experience | Resource | Teacher Actions | Sensemaking Strategy | Assessment Strategy |
|---|---|---|---|---|---|
| Predict Phase | | | | | |
| Observe Phase | | | | | |
| Explain Phase | | | | | |
| Driving Question Board (DQB) Creation | | | | | |
| Model Building Phase | | | | | |

**Section D — Reflection Questions**
Exactly 8 numbered questions.

**Section E — Summary / Consolidation Prompt**
1 italic paragraph.

---

## Colour Palette

```javascript
const C = {
  darkBlue:    "1F3864",   // section headers, lesson titles
  medBlue:     "2E75B6",   // Learner Experience, Teacher Actions column headers
  lightBlue:   "D5E8F0",   // label cells, knowledge/skills rows
  teal:        "1F6B75",   // Resource, Sensemaking column headers, section B/C titles
  lightTeal:   "D9EEF1",   // Storyline, Purpose in Storyline label
  green:       "375623",
  lightGreen:  "E2EFDA",   // Values label
  orange:      "C55A11",
  lightOrange: "FCE4D6",   // Safety Notes label, PCIs label; Section D title
  purple:      "7030A0",
  lightPurple: "EAD1F5",   // Key Inquiry Questions, Phenomenon, DQ, Storyline label; Section E title
  grey:        "F2F2F2",   // alternating content cells (odd columns)
  white:       "FFFFFF",
};
```

Phase row colours (Section C, column 1):
- Predict Phase → `lightPurple`
- Observe Phase → `lightTeal`
- Explain Phase → `lightGreen`
- DQB Creation → `lightOrange`
- Model Building Phase → `lightBlue`

---

## Naming Conventions

### Generator scripts
```
generators/[subject]_[strand]_[substrand]_[topic_slug].js
```
Example: `generators/biology_1_4_chemicals_of_life.js`

### Output files
```
[Subject]_[StrandCode]_[Topic]_CBE_LessonSequence_L[x]-[y].docx
```
Examples:
- `Biology_CellStructure_CBE_LessonSequence_L1-3.docx`
- `Biology_ChemicalsOfLife_CBE_LessonSequence_L1-5.docx`

---

## Curriculum Coverage Plan

Target: ~2,000 lessons across Grade 10 (Biology, Physics, Chemistry, Mathematics).

### Biology Grade 10 — Status

| Sub-Strand | Total Lessons | Generated | Status |
|---|---|---|---|
| 1.1 Introduction to Biology | 6 | 0 | Not started |
| 1.2 Specimen Collection and Preservation | 14 | 0 | Not started |
| 1.3 Cell Structure and Specialisation | 20 | 3 | ✅ In progress |
| 1.4 Chemicals of Life | 24 | 5 | ✅ In progress |
| 2.1 Nutrition (Plants) | 12 | 0 | Not started |
| 2.2 Transport (Plants) | 22 | 0 | Not started |
| 2.3 Gaseous Exchange and Respiration (Plants) | 22 | 0 | Not started |
| 3.1 Nutrition (Animals) | 12 | 0 | Not started |
| 3.2 Transport (Animals) | 24 | 0 | Not started |
| 3.3 Gaseous Exchange and Respiration (Animals) | 24 | 0 | Not started |
| **Total** | **180** | **8** | |

Physics, Chemistry, Mathematics: not yet started.

---

## When Generating New Lessons

### If an introduction/template document is provided
Read it first. Extract: phenomenon, driving question, storyline, lesson sequence. Use these verbatim or near-verbatim. Do not invent alternatives.

### If no template document exists
Invent the phenomenon, driving question, and storyline. Follow these criteria:
- **Kenya-relevant:** drawn from Kenyan context (people, places, industries, food, wildlife, current events)
- **Visually compelling and observable:** something students can see or directly experience
- **Teacher-friendly:** explainable without specialist equipment
- **Grade 10 appropriate:** interesting to a 15–16 year old
- **Scientifically rich:** connects to multiple learning outcomes in the sub-strand

### Always verify against the official KICD curriculum document before generating
The curriculum `.docx` file for Biology is at:
`data/raw/curriculum_pdfs/Biology_Grade_10_Curriculum.docx`

Extract the correct sub-strand with:
```bash
python3 -c "
from docx import Document
doc = Document('data/raw/curriculum_pdfs/Biology_Grade_10_Curriculum.docx')
for ti, table in enumerate(doc.tables):
    print(ti, table.rows[0].cells[0].text[:60])
"
```

---

## Production Run Notes

- **Cost:** ~\$0.09 per lesson with `claude-sonnet-4-6`
- **Speed:** ~2.5 minutes per lesson (API-bound)
- **Throughput for 2,000 lessons:** ~83 hours sequential; parallelise with batch processing
- **Venv activation:** `source /home/markk/ares/cbe-generation-system/venv/bin/activate`
- **API key:** stored in `.env` at project root

---

## Quick Start for a New Sub-Strand

```bash
cd /home/markk/ares/cbe-generation-system

# 1. Check the curriculum for the sub-strand
python3 scripts/extract_curriculum.py --substrand "1.5"

# 2. Copy the nearest existing generator as a template
cp generators/biology_1_4_chemicals_of_life.js generators/biology_1_5_[topic].js

# 3. Update: strand/substrand metadata, curriculum data, phenomenon, lessons data array

# 4. Generate
node generators/biology_1_5_[topic].js

# 5. Validate
python3 scripts/office/validate.py data/outputs/docx/[output].docx
```
