# PROJECT_CONTEXT.md — Kenya CBE Lesson Plan Generation System

> **Last updated: 2026-05-31**

## Context Restoration Document

> Use this to restore context when returning after a break or starting a new session.
> For operational procedures see `docs/WORKFLOW.md`.
> For architecture details see `docs/SYSTEM_OVERVIEW.md`.
> For generation status see `docs/STATUS.md`.

---

## What This Project Is

A system to generate ~2,000 Kenya Competency-Based Education (CBE) lesson plans as formatted Word documents (`.docx`), covering Grade 10 Biology, Physics, Chemistry, and Mathematics. Lesson plans are:

- Hosted on ARES Education offline servers (Rachel 4 Plus devices, Ubuntu 24.04, WiFi hotspots) in Kenyan schools
- Aligned to the KICD (Kenya Institute of Curriculum Development) March 2025 curriculum
- Generated using the Claude API (`claude-sonnet-4-6`)
- Structured using a phenomenon-driven, inquiry-based pedagogy (NGSS Storyline model)
- Distributed as three documents per sub-strand: Lesson Sequence, Final Explanation, Summary Table

---

## Infrastructure

| Property | Value |
|---|---|
| Server | `jhm-spark` (NVIDIA Spark, GB10 Blackwell GPU, 128GB RAM) |
| User | `markk` |
| Project path | `/home/markk/ares/cbe-generation-system` |
| Python | 3.12.3 (venv at `venv/`) |
| Node.js | v22.x |
| API model | `claude-sonnet-4-6` |
| Git branch | `main` |
| GitHub | `markknit/cbe-generation-system` |

```bash
# Always activate venv before running Python
source /home/markk/ares/cbe-generation-system/venv/bin/activate
```

---

## Architecture (Current — May 2026)

The system has two distinct layers:

**Content layer (Python / Claude API):**
`src/generate_substrand.py` reads KICD curriculum PDFs and teacher template docx files, calls Claude API, and produces `generators/data/*_data.js` files containing all lesson content as structured JSON-like data.

**Document layer (Node.js / docx npm):**
`generators/generate.js` reads data files and produces three `.docx` files per sub-strand using the shared lib in `generators/lib/`.

```
KICD PDF + Teacher Template → Claude API → *_data.js → Node.js → .docx + .json
```

This separation means content and formatting are independent. Edit the `_data.js` file to change content; the generator always applies formatting correctly.

---

## Key Files

| File | Role |
|---|---|
| `generators/data/*_data.js` | **Source of truth** — all lesson content per sub-strand |
| `generators/lib/docx_kit.js` | All formatting primitives (colours, helpers, constants) |
| `generators/lib/sections.js` | Section builders (sectionA–E, overview table) |
| `generators/lib/build_docs.js` | Document assembly (SoW, FE, ST, JSON export) |
| `generators/generate.js` | Universal entry point |
| `generators/aresResources.js` | ARES content database integration |
| `src/generate_substrand.py` | Claude API pipeline (sync + batch modes) |
| `src/ares_recommender.py` | ARES FTS search (1.55M content items) |
| `scripts/patch_lesson.js` | Repair stub lessons in data files |
| `scripts/patch_fe.js` | Repair missing Final Explanations |
| `scripts/repair_stubs.py` | Batch repair utility |
| `data/ares_index/ares_content.db` | ARES content DB — 630MB, **jhm-spark only, gitignored** |
| `.env` | `ANTHROPIC_API_KEY` — **never committed** |

---

## Generation Status (May 2026)

### Biology — COMPLETE
All 9 sub-strands generated at 8 lessons each. Pending teacher review.

| Sub-strand | Name | Generated |
|---|---|---|
| 1.1 | Introduction to Biology | ✅ 8 lessons |
| 1.2 | Specimen Collection and Preservation | ✅ 8 lessons |
| 1.3 | Cell Structure and Specialisation | ✅ 8 lessons |
| 1.4 | Chemicals of Life | ✅ 6 lessons (exemplar) |
| 2.1 | Nutrition in Plants | ✅ 12 lessons |
| 2.2 | Transport in Plants | ✅ 8 lessons |
| 2.3 | Gaseous Exchange and Respiration in Plants | ✅ 8 lessons |
| 3.1 | Nutrition in Animals | ✅ 8 lessons |
| 3.2 | Transport in Animals | ✅ 8 lessons |
| 3.3 | Gaseous Exchange and Respiration in Animals | ✅ 8 lessons |

### Chemistry, Physics, Mathematics — Not started
Teacher templates available for all. Pending Biology teacher review before bulk generation.

See `docs/STATUS.md` for batch submission commands and full cost tracking.

---

## Lesson Plan Structure

Each sub-strand produces three deliverable files. The Lesson Sequence contains:

- **Sub-Strand Overview table** — all KICD metadata, phenomenon, driving question, storyline
- **Per lesson (repeated):**
  - Section A — Specific Learning Outcomes
  - Section B — Lesson Overview (prose)
  - Section C — 6-column Implementation Framework (Predict / Observe / Explain / DQB / Model phases)
  - Section D — Teacher Reflection
  - Section E — Summary Table Prompt
- **Differentiation and Inclusion table**

Section C column widths: `[900, 2300, 2556, 3324, 2300, 2300]` DXA
(Phase / Learner Experience / Resource-ARES / Teacher Moves / Sensemaking / Assessment)

---

## Pedagogical Framework

5-phase phenomenon-driven inquiry model per lesson:
1. **Predict Phase** — prior knowledge, initial ideas
2. **Observe Phase** — evidence gathering (practical, video, simulation, reading)
3. **Explain Phase** — sensemaking, applying knowledge
4. **Driving Question Board (DQB)** — tracking growing understanding
5. **Model Building Phase** — cumulative model revision across the unit

Every lesson connects to the anchoring phenomenon. The DQB is a living class artifact. Teacher moves include specific quotes, WAIT TIME (10–15 seconds), cold-call counts.

---

## Batch API Mode

All bulk generation uses the Anthropic Message Batches API:
- 50% cheaper than synchronous (`claude-sonnet-4-6` batch: $1.50/$7.50 per MTok)
- Asynchronous — submit at any time, collect within 24 hours (typically under 1 hour)
- 300K output tokens per request (vs 64K synchronous)

```bash
# Submit
python3 src/generate_substrand.py --subject chemistry --substrand 1.4 \
  --output chem_1_4 --lessons 8 --batch

# Collect (with auto-polling)
python3 src/generate_substrand.py --collect chem_1_4 --wait --run
```

**After every batch collect:** run `node /tmp/check_data.js` to identify any stub lessons (JSON parse failures). Use `scripts/patch_lesson.js` and `scripts/patch_fe.js` to repair.

---

## Cost Reference

| Mode | Input | Output | Typical sub-strand (8 lessons) |
|---|---|---|---|
| Synchronous | $3/MTok | $15/MTok | ~$0.70 |
| **Batch (use this)** | **$1.50/MTok** | **$7.50/MTok** | **~$0.35** |

Full 2,000-lesson target at batch pricing: **~$114**

---

## Design Principles

1. **KICD verbatim.** Learning outcomes, competencies, values, PCIs, key inquiry questions must match the official KICD curriculum exactly.

2. **Source of truth is the data file.** `generators/data/*_data.js` is the editable content artifact. The `.docx` files are always generated artifacts — never edit them directly.

3. **Phenomenon drives everything.** Every lesson phase must connect to the anchoring phenomenon. A lesson plan that doesn't reference the phenomenon has failed.

4. **Kenya context is non-negotiable.** Kenyan food, scientists, places, and current events throughout. Never default to Western examples.

5. **Teachers are the users.** Write teacher actions as specific and actionable. A teacher who has never seen this pedagogy should be able to follow the lesson from the document alone.

6. **API generates content; jhm-spark generates documents.** The API is stateless. jhm-spark holds all persistent state, runs all formatting, and ultimately serves content to schools.

---

## Restoration Prompt for New Session

```
I am working on the Kenya CBE Lesson Plan Generation System.
Server: jhm-spark | User: markk | Path: /home/markk/ares/cbe-generation-system
Branch: main

Current state: Biology complete (all 9 sub-strands, 8 lessons each).
Chemistry, Physics, Mathematics pending after teacher review of Biology.

Architecture: universal generator (node generators/generate.js) reads
generators/data/*_data.js files produced by src/generate_substrand.py
(Claude API pipeline with batch mode support).

Read CLAUDE.md, docs/SYSTEM_OVERVIEW.md, and docs/STATUS.md for full context.
```
