# CLAUDE.md — Kenya CBE Lesson Plan Generation System

> **Last updated: 2026-05-31**
> Auto-read by Claude Code at session start. Keep concise and actionable.
> Full documentation in `docs/` — see README.md, SYSTEM_OVERVIEW.md, WORKFLOW.md.

---

## Project Identity

**Goal:** Generate ~2,000 Kenya CBE lesson plans as `.docx` files (Grade 10 Biology, Chemistry, Physics, Mathematics).
**Server:** `jhm-spark` | **User:** `markk` | **Root:** `/home/markk/ares/cbe-generation-system`
**Branch:** `main` | **Remote:** `markknit/cbe-generation-system`
**Model:** `claude-sonnet-4-6`

---

## Current Status (May 2026)

- **Biology:** All 9 sub-strands complete (8 lessons each + FE + ST)
- **Chemistry, Physics, Mathematics:** Pending teacher review of Biology before proceeding
- See `docs/STATUS.md` for full coverage tracker

---

## Repository Layout

```
/home/markk/ares/cbe-generation-system/
├── generators/
│   ├── generate.js                  # Universal entry point
│   ├── aresResources.js             # ARES resource injection
│   ├── lib/
│   │   ├── docx_kit.js              # Formatting primitives
│   │   ├── sections.js              # Section builders (sectionA–E)
│   │   └── build_docs.js            # buildSoW, buildFinalExplanation, buildSummaryTable
│   └── data/
│       ├── SCHEMA.md                # Data module field documentation
│       └── *_data.js                # One per sub-strand (THE source of truth)
├── src/
│   ├── generate_substrand.py        # Claude API content pipeline (main script)
│   └── ares_recommender.py          # ARES FTS search
├── scripts/
│   ├── patch_lesson.js              # Repair stub lessons
│   ├── patch_fe.js                  # Repair missing Final Explanations
│   └── repair_stubs.py              # Batch repair utility
├── data/
│   ├── raw/
│   │   ├── curriculum_pdfs/         # KICD Grade 10 PDFs (Biology, Chemistry, Physics, Math)
│   │   └── CBE LESSON TEMPLATES/    # Teacher-authored SoW docx templates
│   └── outputs/docx/                # Generated output files
├── docs/                            # Documentation (README, SYSTEM_OVERVIEW, STATUS, WORKFLOW)
├── .env                             # ANTHROPIC_API_KEY
└── package.json                     # Node.js dependencies (docx npm package)
```

---

## Quick Start

```bash
# Environment
cd /home/markk/ares/cbe-generation-system
source venv/bin/activate

# Generate a sub-strand (batch mode — 50% cheaper)
python3 src/generate_substrand.py \
  --subject chemistry --substrand 1.4 \
  --output chem_1_4 --lessons 8 --batch

# Collect batch results
python3 src/generate_substrand.py --collect chem_1_4 --wait --run

# Regenerate docx from existing data file
node generators/generate.js bio_1_4

# Regenerate all sub-strands
node generators/generate.js --all

# Check for stub lessons after batch collect
node /tmp/check_data.js    # see WORKFLOW.md for the check_data.js template

# Repair a stub lesson
node scripts/patch_lesson.js bio_2_3 3 /tmp/bio_2_3_lesson3.json

# Repair a missing Final Explanation
node scripts/patch_fe.js bio_3_2 /tmp/bio_3_2_fe.json
```

---

## Document Format Standards

| Property | Value |
|---|---|
| Page orientation | **Landscape** |
| Page size | US Letter (12240 × 15840 DXA) |
| Margins | 0.75 inch all sides (1080 DXA) |
| Content width | 13680 DXA |
| Font | Arial throughout |
| Body text | 18 (≈9pt) |

**Section C column widths (DXA):**
```
[900,  2300,  2556,  3324,  2300,  2300]
 A     B      C      D      E      F
Phase  LE     Res    TM     SM     FA
```
A=Phase, B=Learner Experience, C=Resource (ARES), D=Teacher Moves (widest), E=Sensemaking, F=Formative Assessment

**Critical docx-js rules:**
- Never use `\n` inside text — use separate `Paragraph` elements
- Always use `WidthType.DXA` — never `WidthType.PERCENTAGE`
- Always use `ShadingType.CLEAR` — never `ShadingType.SOLID`
- Always set both `columnWidths` array on table AND `width` on each cell

---

## Each Sub-Strand Produces Three Output Files

```
data/outputs/docx/<Subject>/<SubStrand>/
├── <prefix>_CBE_LessonSequence.docx     # Main teacher document
├── <prefix>_FinalExplanation.docx       # Student assessment
└── <prefix>_SummaryTable.docx           # Teacher reference
```

JSON export also produced since May 2026:
```
└── <prefix>_data.json                   # Structured data for downstream tools
```

---

## Curriculum Authority

**KICD March 2025 curriculum** — verbatim for:
- Specific Learning Outcomes (a–e)
- Sub-strand content bullet list
- Key Inquiry Questions
- Core Competencies, Values, PCIs

Phenomenon, Driving Question, Storyline, and all lesson content are generated.

---

## ARES Resource Integration

Resources auto-injected into Section C Resource column at generation time.
- Kolibri: `http://ares.edu:8069/en/learn/#/topics/c/<node_id>`
- Content DB: `data/ares_index/ares_content.db` (630MB — **gitignored, jhm-spark only**)

---

## Git Sync

```bash
# jhm-spark → GitHub
git add -A && git commit -m "..." && git push origin main

# GitHub → Windows
git pull

# After force push (diverged history)
git fetch origin && git reset --hard origin/main
```

**Never commit:** `data/ares_index/ares_content.db`, `venv/`, `.env`
Check before push: `find . -size +50M -not -path './.git/*' -not -path './venv/*'`
