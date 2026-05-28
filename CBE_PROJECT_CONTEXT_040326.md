# PROJECT_CONTEXT.md — Kenya CBE Lesson Plan Generation System
## Full Context Restoration Document

> Use this document to fully restore context when returning to this project after a break,
> or when handing off to a new Claude session / Claude Code.
> For operational instructions, see CLAUDE.md.

---

## What This Project Is

A system to generate ~2,000 Kenya Competency-Based Education (CBE) lesson plans as formatted Word documents (.docx), covering Grade 10 Biology, Physics, Chemistry, and Mathematics. The lesson plans will be:

- Hosted on ARES Education offline servers (Rachel 4 Plus devices running Ubuntu 24.04 as WiFi hotspots) in Kenyan schools
- Aligned to the official KICD (Kenya Institute of Curriculum Development) March 2025 curriculum
- Generated using the Claude API (`claude-sonnet-4-6`)
- Structured using a specific phenomenon-driven, inquiry-based pedagogy

---

## Server and Infrastructure

| Property | Value |
|---|---|
| Server name | `jhm-spark` |
| Primary user | `markk` |
| Project path | `/home/markk/ares/cbe-generation-system` |
| GPU | NVIDIA GB10 (Blackwell, 580.126.09 driver) |
| Python | 3.12.3 |
| Java | 1.8.0_482 |
| Apache Spark | 3.5.x (installed at `/opt/spark`) |
| Venv | `venv/` inside project root |
| API key | `.env` file at project root |

**Activating the venv:**
```bash
source /home/markk/ares/cbe-generation-system/venv/bin/activate
# Prompt should show (venv) prefix
```

**History note:** The project was previously run under user `james` at `/home/ares/cbe-generation-system` and then under user `james` at `~/ares/cbe-generation-system`. It has since been migrated to user `markk`. If old path references appear in scripts, update them to `/home/markk/ares/cbe-generation-system`.

---

## Curriculum Reference

**Official document:** KICD Biology Grade 10 Curriculum Design, March 2025
- ISBN: 978-9914-52-915-9
- File: `data/raw/curriculum_pdfs/Biology_Grade_10_Curriculum.docx`

### Strand and Sub-Strand Summary (Biology Grade 10)

| Code | Sub-Strand | Lessons |
|---|---|---|
| 1.1 | Introduction to Biology | 6 |
| 1.2 | Specimen Collection and Preservation | 14 |
| 1.3 | Cell Structure and Specialisation | 20 |
| 1.4 | Chemicals of Life | 24 |
| 2.1 | Nutrition (Plants) | 12 |
| 2.2 | Transport (Plants) | 22 |
| 2.3 | Gaseous Exchange and Respiration (Plants) | 22 |
| 3.1 | Nutrition (Animals) | 12 |
| 3.2 | Transport (Animals) | 24 |
| 3.3 | Gaseous Exchange and Respiration (Animals) | 24 |
| **Total** | | **180** |

**Official KICD key inquiry questions for 1.3:**
1. Why do plant and animal cells differ?
2. How are cells specialised?

**Official KICD key inquiry questions for 1.4:**
1. How are chemicals important in cells?
2. How is the presence of chemicals of life determined?

---

## What Has Been Built So Far

### Sub-Strand 1.3 — Cell Structure and Specialisation (Lessons 1–3 of 20)

**Output file:** `Biology_CellStructure_CBE_LessonSequence_L1-3.docx`

**Phenomenon (from teacher template document `Biology_10_1_3_Cell_structure_and_specialization_-_Introduction.docx`):**
A salamander grows from a single fertilised cell into a complex organism — visible in a time-lapse video (National Geographic Short Film Showcase).

**Driving Question:** How does a single cell become a complex, specialised organism — and what does the internal structure of a cell tell us about what it can do?

**Lessons:**
| # | Title | Key Content |
|---|---|---|
| 1 | Why Study Cells? — Phenomenon, Microscopy and the Basics | Salamander phenomenon, DQB creation, light vs electron microscope, microscope parts |
| 2 | Cell Structures Under the Electron Microscope | Organelle identification from EM images, functions, secretory pathway concept |
| 3 | Plant vs Animal Cells — Differences and Preparing Temporary Slides | EM comparison, temporary slide preparation (iodine stain, onion/kale), DQB update |

**Notes on 1.3:**
- The teacher template document existed and was used for phenomenon/driving question/storyline
- Lessons 4–5 (specialised cells, cell organisation) still need to be generated
- Core competencies used: all 7 from template (Communication & Collaboration, Self-Efficacy, Critical Thinking, Digital Literacy, Learning to Learn, Citizenship, Creativity & Innovation)
- Core values used: 8 (Nationalism, Respect, Responsibility, Integrity, Peace & Social Justice, Love, Unity, Excellence)

---

### Sub-Strand 1.4 — Chemicals of Life (Lessons 1–5 of 24)

**Output file:** `Biology_ChemicalsOfLife_CBE_LessonSequence_L1-5.docx`

**Phenomenon (invented — no template document existed):**
Eliud Kipchoge's sub-2-hour marathon (1:59:40, Vienna, 12 October 2019). His sports science team calculated precise chemical intake before, during, and after. Every chemical of life was critical to the achievement.

**Why this phenomenon was chosen:**
- Kenya-relevant: Kipchoge is universally known in Kenya
- Observable: time-lapse highlights video available; pre-race nutrition plan is a real document
- Teacher-friendly: no specialist equipment needed beyond the video
- Scientifically rich: connects to all 5 classes of chemicals of life + enzymes + water + mineral salts

**Driving Question:** What chemicals does the human body need to run, grow, and stay alive — and how can we detect them in the foods we eat every day?

**Storyline Thread:**
| Lesson | Chemical Focus | Practical | Kenyan Food Connection |
|---|---|---|---|
| 1 | Carbohydrates | Iodine test (starch) + Benedict's test (reducing sugars) | Ugali, banana, sugar cane juice, potato |
| 2 | Proteins + Lipids | Biuret test + ethanol emulsion test | Eggs, boiled beans, milk, nyama choma, avocado, cooking oil |
| 3 | Enzymes (catalase) | H₂O₂ + fresh liver/potato; glowing splint for O₂ | Fresh liver or potato (catalase source) |
| 4 | Factors affecting enzymes | Temperature/pH controlled experiment + graph plotting | Physiological context: Kipchoge's rising temperature, lactic acid, glucose depletion |
| 5 | Vitamins, water, mineral salts + food labels | DCPIP test for vitamin C; food label analysis | Oranges, lemon, guava, pawpaw; real Kenyan packaged food labels |

**Official KICD core competencies for 1.4:**
- Critical Thinking and Problem Solving
- Learning to Learn

**Official KICD values for 1.4:**
- Love (sharing resources during enzyme experiments)
- Unity (collaborating during catalase investigation)

**Notes on 1.4:**
- No template introduction document existed — phenomenon and storyline were invented from scratch
- Lessons 6–24 still need to be generated (deeper enzyme kinetics, water functions, mineral salt deficiencies, full food testing coverage)
- The DCPIP vitamin C test is standard KICD-mandated content
- Food label examination is explicitly mandated: "examine packaging labels of common food products, appreciate the quality, quantity, and safety of the chemical components indicated (preservatives, colourings and expiry)"

---

## Document Generation Architecture

### Primary Generation Method: JavaScript + `docx` npm package

All lesson plan `.docx` files are built with Node.js using the `docx` library (v9.5.3).

**Why this approach:**
- Early work used Python `python-docx` but it produced formatting issues with complex multi-column tables
- The `docx` JS library gives precise DXA-level control over column widths and cell shading
- Validation is done with a Python script that checks paragraph counts and XML integrity

**Generator script locations (in this conversation — copy to jhm-spark):**
- `generate_cell_structure.js` → `generators/biology_1_3_cell_structure.js`
- `generate_chemicals_of_life.js` → `generators/biology_1_4_chemicals_of_life.js`

**To run:**
```bash
node generators/biology_1_4_chemicals_of_life.js
python3 scripts/office/validate.py data/outputs/docx/Biology_ChemicalsOfLife_CBE_LessonSequence_L1-5.docx
```

### Claude API Integration (Python, for AI-assisted content generation)

The `src/` directory contains Python scripts that use the Claude API to generate lesson content. The current model string is `claude-sonnet-4-6`.

**Previous model:** `claude-sonnet-4-5-20250929` — updated to `claude-sonnet-4-6` using:
```bash
sed -i 's/claude-sonnet-4-5-20250929/claude-sonnet-4-6/g' /home/markk/ares/cbe-generation-system/src/*.py
```

**Performance characteristics:**
- Cost: ~$0.09 per lesson
- Time: ~2.5 minutes per lesson (API-bound)
- For 2,000 lessons: ~$180 total, ~83 hours sequential

---

## Lesson Plan Pedagogical Framework

All lessons follow a **5-phase phenomenon-driven inquiry model**:

1. **Predict Phase** — Students draw/write initial ideas before instruction; connects to the anchoring phenomenon
2. **Observe Phase** — Evidence gathering (practical, video, reading, simulation)
3. **Explain Phase** — Sense-making, applying knowledge to explain observations
4. **Driving Question Board (DQB) Creation/Update** — Students track their growing understanding; questions are added and answered across lessons
5. **Model Building Phase** — Students revise a cumulative explanatory model; the model evolves across all lessons in the sub-strand

**Key pedagogical principles:**
- Every lesson connects back to the anchoring phenomenon
- The DQB is a living class artifact — questions from Lesson 1 are revisited in Lesson 5
- The model is revised with each new piece of evidence (not redrawn from scratch)
- Teacher actions include specific questioning moves: cold-calling, WAIT TIME (10–15 seconds), Think-Pair-Share
- Assessment is predominantly formative; summative checks appear at Lesson 5

---

## Formatting Decisions Made (Do Not Change Without Good Reason)

These decisions were made and refined through iteration with the teacher:

| Decision | Value | Reason |
|---|---|---|
| Section C column 1 | Phase label column (900 DXA wide) | Teacher feedback: rows needed clear phase identification |
| Section C column widths | [900, 1692, 1692, 1692, 1692, 1692] | Maximises content space while keeping phase label readable |
| Sub-strand overview | Separate row for Sub-Strand Content vs Learning Outcomes | Distinguishes curriculum content list from outcome statements |
| Colour for Predict phase | lightPurple | Visual consistency across all documents |
| Colour for Observe phase | lightTeal | |
| Colour for Explain phase | lightGreen | |
| Colour for DQB Creation | lightOrange | |
| Colour for Model Building | lightBlue | |
| 8 reflection questions | Fixed at 8 per lesson | Sufficient depth; not overwhelming |
| Summary prompt | 1 italic paragraph at end | Consistent with template document style |

---

## Files Referenced in This Conversation

| File | Description | Location on jhm-spark |
|---|---|---|
| `Biology_Grade_10_Curriculum.docx` | Official KICD curriculum | `data/raw/curriculum_pdfs/` |
| `Biology_10_1_3_Cell_structure_and_specialization_-_Introduction.docx` | Teacher-authored intro doc for 1.3; contains phenomenon/DQ/storyline | `data/raw/template_examples/` |
| `generate_cell_structure.js` | JS generator for 1.3 (Lessons 1–3) | `generators/biology_1_3_cell_structure.js` |
| `generate_chemicals_of_life.js` | JS generator for 1.4 (Lessons 1–5) | `generators/biology_1_4_chemicals_of_life.js` |
| `Biology_CellStructure_CBE_LessonSequence_L1-3.docx` | Output — 1.3 lessons | `data/outputs/docx/` |
| `Biology_ChemicalsOfLife_CBE_LessonSequence_L1-5.docx` | Output — 1.4 lessons | `data/outputs/docx/` |

---

## Pending Work / Next Steps

### Immediate (before scaling)
- [ ] Mark indicated "major changes" and "more detailed guidelines" are coming — review these before generating more lessons
- [ ] Formalise the project structure on jhm-spark (create `generators/`, `scripts/`, proper directory layout)
- [ ] Copy JS generator scripts from this conversation to jhm-spark
- [ ] Copy CLAUDE.md and PROJECT_CONTEXT.md to project root on jhm-spark

### Content to generate
- [ ] Biology 1.3: Lessons 4–5 (specialised cells, cell organisation, final model)
- [ ] Biology 1.4: Lessons 6–24 (remaining chemical content, full enzyme kinetics)
- [ ] All other Biology sub-strands (2.1 through 3.3)
- [ ] Physics, Chemistry, Mathematics Grade 10 (curriculum documents not yet uploaded)

### System improvements (pending new guidelines)
- [ ] Parallel processing for API calls
- [ ] Upload reference .docx templates to server
- [ ] Quality assurance / review workflow
- [ ] Teacher feedback integration loop

---

## How to Restore This Context in a New Session

Paste the following into a new Claude conversation or Claude Code session:

```
I am working on the Kenya CBE Lesson Plan Generation System on server jhm-spark,
user markk, path /home/markk/ares/cbe-generation-system.

Please read PROJECT_CONTEXT.md for full context.

The system generates Grade 10 Biology lesson plans as .docx files using Node.js
and the docx library. Two lesson sequences have been generated so far:
- Biology 1.3 Cell Structure and Specialisation (Lessons 1-3 of 20)
- Biology 1.4 Chemicals of Life (Lessons 1-5 of 24)

CLAUDE.md contains all operational instructions and formatting standards.
```

---

## Key Design Principles to Preserve

1. **Curriculum fidelity first.** Official KICD wording for learning outcomes, competencies, values, PCIs, and key inquiry questions must be used verbatim. Never paraphrase official curriculum text.

2. **Phenomenon drives everything.** Every lesson activity, DQB question, model revision, and reflection question must connect back to the anchoring phenomenon. A lesson plan that does not reference the phenomenon in each phase has failed the model.

3. **Kenya context is non-negotiable.** Resources, food examples, scientists referenced, and phenomena must be drawn from Kenyan context wherever possible. Do not default to Western examples (e.g. don't use "pizza" when "ugali" is correct; don't use a generic athlete when Kipchoge exists).

4. **Teachers are the users.** Write teacher actions that are specific and actionable. Include WAIT TIME instructions, cold-call counts, and specific probing questions. A teacher who has never seen this pedagogy before should be able to follow the lesson from the document alone.

5. **The model is cumulative.** Each Model Building Phase builds on the previous lesson's model. The first model (Lesson 1) is deliberately incomplete. The final model (last lesson of the sub-strand) should be able to answer the driving question completely with evidence from every lesson.
