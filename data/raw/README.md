# Raw Data Directory

This directory contains source materials for CBE lesson generation.

## Directory Structure

### `curriculum_pdfs/`
**Purpose:** Official KICD curriculum documents

**Contents:** 
- KICD Grade 10-12 curriculum PDFs for various subjects
- Used to extract: learning outcomes, strands, sub-strands, competencies, values, PCIs

**Example files:**
- `KICD_Grade_10_CBC_Physics_Curriculum_March_2025.pdf`
- `KICD_Grade_10_CBC_Biology_Curriculum_March_2025.pdf`

### `template_examples/`
**Purpose:** Reference lesson plans showing desired structure and formatting

**Contents:**
- Example CBE lesson plans (DOCX or PDF)
- Used as reference for: lesson organization, level of detail, pedagogical approach, formatting

**Example files:**
- `Biology_CellStructure_CBE_LessonSequence_v1.docx`

## Adding New Files

1. **Curriculum PDFs:** Place in `curriculum_pdfs/` and update `config/generation_config.yaml`
2. **Template Examples:** Place in `template_examples/`

## File Naming Convention

**Curricula:** `KICD_Grade_[XX]_CBC_[Subject]_Curriculum_[Date].pdf`
**Templates:** `[Subject]_[Topic]_CBE_LessonSequence_v[X].docx`
