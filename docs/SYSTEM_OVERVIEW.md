# System Overview — Kenya CBE Lesson Plan Generation System

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           JHM-SPARK SERVER                              │
│                    /home/markk/ares/cbe-generation-system               │
│                                                                         │
│  ┌─────────────────────┐      ┌──────────────────────────────────────┐  │
│  │   CONTENT PIPELINE  │      │        DOCUMENT GENERATOR            │  │
│  │   (Python / src/)   │      │       (Node.js / generators/)        │  │
│  │                     │      │                                      │  │
│  │  generate_          │      │  generators/lib/                     │  │
│  │  substrand.py       │─────►│    docx_kit.js   (primitives)        │  │
│  │                     │      │    sections.js   (section builders)  │  │
│  │  ares_              │      │    build_docs.js (SoW / FE / ST)     │  │
│  │  recommender.py─────┼──┐   │                                      │  │
│  │                     │  │   │  generators/data/*_data.js           │  │
│  └──────────┬──────────┘  │   │    META + UNIT + LESSONS             │  │
│             │             │   │    + FINAL_EXPLANATION               │  │
│             │ API calls   │   │    + SUMMARY_TABLE                   │  │
│             ▼             │   └──────────────┬───────────────────────┘  │
│  ┌──────────────────────┐ │                  │                          │
│  │  ANTHROPIC API       │ │                  ▼                          │
│  │  claude-sonnet-4-6   │ │   data/outputs/docx/                        │
│  │  (remote)            │ │     Grade 10 Biology/                        │
│  │                     ◄┘ │     Grade 10 Chemistry/                      │
│  │  Generates:           │     Grade 10 Physics/                        │
│  │  • UNIT data          │     Grade 10 Math/                           │
│  │  • 8+ lessons         │                                              │
│  │  • Final Explanation  │   ┌──────────────────────────────────────┐   │
│  │  • Summary Table      │   │         ARES CONTENT DB              │   │
│  └──────────────────────┘   │  data/ares_index/ares_content.db     │   │
│                              │  1,555,000+ items (FTS5)             │   │
│  INPUT SOURCES:              │  Kolibri + Kiwix + Web modules       │   │
│  data/raw/curriculum_pdfs/   └──────────────────────────────────────┘   │
│  data/raw/CBE LESSON          GPU: NVIDIA GB10 Blackwell                │
│           TEMPLATES/          (Whisper transcription)                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Reference

### `src/generate_substrand.py` — Content Generation Pipeline

The main entry point for generating new sub-strand content.

**Modes:**
- **Synchronous** (`--run`): generates one lesson at a time, ~60s each
- **Batch** (`--batch`): submits all requests to Anthropic's Message Batches API (50% cheaper, async, up to 24hr turnaround)
- **Collect** (`--collect NAME`): retrieves batch results and assembles data file
- **Unit-only** (`--unit-only`): generates only the UNIT object for testing/inspection

**Flow:**
1. Extracts sub-strand content from KICD curriculum PDF (pdfminer)
2. Extracts phenomenon/structure from teacher template docx (python-docx) if available
3. Calls Claude API to generate UNIT data (1 call)
4. Calls Claude API to generate each lesson (1 call per lesson)
5. Calls Claude API to generate Final Explanation (1 call)
6. Calls Claude API to generate Summary Table (1 call)
7. Assembles `generators/data/<name>_data.js`
8. Optionally runs `node generators/generate.js <name>`

**Checkpointing:** After each successful lesson, saves `.{name}_checkpoint.json` so runs can be resumed with `--resume` if interrupted.

---

### `generators/generate.js` — Universal Document Generator

Reads a data module and produces three `.docx` files.

```bash
node generators/generate.js bio_1_4      # single sub-strand
node generators/generate.js --all        # all sub-strands in generators/data/
```

**Output per sub-strand:**
- `*_CBE_LessonSequence.docx`
- `*_FinalExplanation.docx`
- `*_SummaryTable.docx`

---

### `generators/lib/docx_kit.js` — Formatting Primitives

All shared constants and helper functions. No content knowledge.

| Export | Description |
|---|---|
| `W = 13680` | Content width in DXA (landscape Letter, 0.75" margins) |
| `C` | Colour palette (darkBlue, medBlue, teal, lightOrange, etc.) |
| `PHASE_COLOUR` | Phase → background colour mapping |
| `para(text, opts)` | Single paragraph |
| `bullet(text, opts)` | Bullet paragraph (em-dash, indented) |
| `cell(content, opts)` | Shaded TableCell (accepts string, Paragraph, or array) |
| `fullHeader(text, fill, ...)` | Full-width spanning header row |
| `labelRow(label, content, w)` | Two-column label/content row |
| `makeTable(rows, widths)` | Bordered table with fixed layout |

---

### `generators/lib/sections.js` — Section Builders

Builds each named section of a lesson plan document. Accepts both old (legacy generator) and new (data module) field naming conventions.

| Function | Output |
|---|---|
| `titleBlock(title, subtitle)` | Document header paragraphs |
| `subStrandOverview(unit)` | Sub-strand overview table (all metadata rows) |
| `sectionA(lesson)` | Specific Learning Outcomes table |
| `sectionB(lesson)` | Lesson Overview prose table |
| `sectionC(lesson, config)` | 6-column Implementation Framework table |
| `sectionD(lesson)` | Teacher Reflection table |
| `sectionE(lesson)` | Summary Table Prompt (3-question) |
| `differentiationTable(rows)` | Differentiation & Inclusion table |

**Section C column widths (DXA):**
```
[900, 2300, 2556, 3324, 2300, 2300]
 A     B     C     D     E     F
Phase  LE    Res   TM    SM    FA
```
A=Phase label, B=Learner Experience, C=Resource (ARES), D=Teacher Moves (widest), E=Sensemaking, F=Formative Assessment

---

### `generators/aresResources.js` — ARES Resource Integration

Queries the ARES content database and injects resource links into the Resource column of every lesson phase.

**URL patterns:**
- Kolibri content: `http://ares.edu:8069/en/learn/#/topics/c/<node_id>`
- Kiwix content: `http://ares.edu/tracker/kiwix_launch.html?target=/kiwix/<zim>/<path>`
- ARES search: `http://ares.edu/www2/search.php?searchstring=<terms>&sources[]=kha&...`

Each Resource cell contains: matched content links + a generic ARES search link.

---

### `generators/data/*_data.js` — Sub-Strand Data Modules

Each file exports five objects:

| Export | Description |
|---|---|
| `META` | Output paths, file prefix, document titles, column label overrides |
| `UNIT` | Sub-strand overview (strand, outcomes, competencies, phenomenon, etc.) |
| `LESSONS` | Array of lesson objects (SLO, overview, 5-phase framework, reflection, ST prompt) |
| `FINAL_EXPLANATION` | Assessment document data (instructions, sections, rubric) |
| `SUMMARY_TABLE` | Teacher reference table (lesson-by-lesson observed/learned/explained) |

See `generators/data/SCHEMA.md` for full field documentation.

---

### `src/ares_recommender.py` — ARES Content Search

FTS5 search across 1.55M ARES content items. Returns ranked results by tier, subject match, content type, and hit count. Called by `aresResources.js` via child process.

---

### Repair Utilities

| Script | Usage |
|---|---|
| `scripts/patch_lesson.js` | `node scripts/patch_lesson.js <name> <num> <json_file>` |
| `scripts/patch_fe.js` | `node scripts/patch_fe.js <name> <json_file>` |
| `scripts/repair_stubs.py` | Edit `REPAIRS` dict, then `python3 scripts/repair_stubs.py` |

---

## Data Flow (Single Sub-Strand)

```
1. KICD curriculum PDF          →  extract_curriculum_pdf()
2. Teacher template .docx       →  extract_template_docx()
3. Both + system prompt         →  Claude API (UNIT call)
4. UNIT + curriculum + template →  Claude API (×N lesson calls)
5. UNIT + lessons               →  Claude API (FE call)
6. Lessons                      →  Claude API (ST call)
7. All JSON                     →  generators/data/<name>_data.js
8. Data file                    →  node generators/generate.js
9.                              →  data/outputs/docx/<subject>/<ss>/
                                       *_CBE_LessonSequence.docx
                                       *_FinalExplanation.docx
                                       *_SummaryTable.docx
```

---

## Colour Palette

| Constant | Hex | Used for |
|---|---|---|
| `darkBlue` | `#1F3864` | Section headers, lesson titles |
| `medBlue` | `#2E75B6` | Learner Experience, Teacher Moves headers |
| `teal` | `#1F6B75` | Resource, Sensemaking headers; B/C section titles |
| `lightBlue` | `#D5E8F0` | Knowledge/Skills label cells |
| `lightGreen` | `#E2EFDA` | Attitudes, Values label cells |
| `lightOrange` | `#FCE4D6` | Safety Notes, PCIs; Section D header |
| `lightPurple` | `#EAD1F5` | Phenomenon, DQ, Storyline; Section E header |
| `lightTeal` | `#D9EEF1` | Purpose in Storyline, Career Connections |
| `grey` | `#F2F2F2` | Alternating content cells |

---

## Page Format

| Property | Value |
|---|---|
| Orientation | Landscape |
| Size | US Letter (12240 × 15840 DXA) |
| Margins | 0.75 inch all sides (1080 DXA) |
| Content width | 13680 DXA |
| Font | Arial throughout |
| Body text | 18 (≈9pt) |
| Section headers | 22 (≈11pt) |
| Title | 28 (≈14pt) |
