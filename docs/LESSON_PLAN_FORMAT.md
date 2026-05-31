# Lesson Plan Document Format

## Document Types (Three per Sub-Strand)

### 1. CBE Lesson Sequence (`*_CBE_LessonSequence.docx`)

The main teacher-facing document. Landscape US Letter, Arial throughout.

**Structure:**

```
Title block (subject + subtitle)

Sub-Strand Overview Table
  ├── Grade Level, Subject, Strand, Sub-Strand
  ├── Total Duration
  ├── Sub-Strand Content (bullet list from KICD)
  ├── Learning Outcomes (a–e, verbatim KICD)
  ├── Core Competencies
  ├── Core Values
  ├── Science & Engineering Practices (NGSS)
  ├── Pertinent & Contemporary Issues (PCIs)
  ├── Career Connections
  ├── Focus for Lessons
  ├── Driving Question / Key Inquiry Questions
  ├── Anchoring Phenomenon
  └── Storyline Thread

[Repeated for each lesson:]

  Section A — Specific Learning Outcomes
    ├── Purpose
    ├── Knowledge (bullets)
    ├── Skills (bullets)
    ├── Attitudes (bullets)
    ├── Key Inquiry Question
    ├── Purpose in Storyline
    └── Safety Notes

  Section B — Lesson Overview (prose)

  Section C — Lesson Implementation Framework (6-column table)
    ┌─────────┬──────────────────┬──────────┬──────────────┬─────────────┬──────────────┐
    │ Phase   │ Learner          │ Resource │ Teacher      │ Sensemaking │ Formative    │
    │         │ Experience       │ (ARES)   │ Moves        │ Strategy    │ Assessment   │
    ├─────────┼──────────────────┼──────────┼──────────────┼─────────────┼──────────────┤
    │ Predict │                  │          │              │             │              │
    │ Observe │                  │          │              │             │              │
    │ Explain │                  │          │              │             │              │
    │ DQB     │                  │          │              │             │              │
    │ Model   │                  │          │              │             │              │
    └─────────┴──────────────────┴──────────┴──────────────┴─────────────┴──────────────┘

  Section D — Teacher Reflection (3–5 numbered questions)

  Section E — Summary Table Prompt
    ├── What did I observe?
    ├── What did I learn?
    └── How does this explain the phenomenon?

Differentiation and Inclusion Table
  ├── English Language Learners
  ├── Students with learning difficulties
  └── Gifted and advanced learners
```

---

### 2. Final Explanation (`*_FinalExplanation.docx`)

Student assessment document. Landscape US Letter.

**Structure:**
- Header with student name/class/date fields
- Instructions (what to use, what to include, word count requirement)
- 4–5 content sections, each with:
  - Section prompt (what to explain)
  - Exemplar answer (model response with Kenyan contexts)
- Assessment rubric (4 criteria × 3 levels: Excellent/Proficient/Developing)

---

### 3. Summary Table (`*_SummaryTable.docx`)

Teacher reference document (pre-filled). Landscape US Letter.

**Structure:**
- Sub-strand and driving question header
- Instructions note (teacher reference only)
- One row per lesson:
  - Lesson number and title
  - What did I observe?
  - What did I learn?
  - How does this explain the phenomenon?

---

## Section C Phase Colours

| Phase | Background colour |
|---|---|
| Predict Phase | `#EAD1F5` (light purple) |
| Observe Phase | `#D9EEF1` (light teal) |
| Explain Phase | `#E2EFDA` (light green) |
| Driving Question Board (DQB) Creation | `#FCE4D6` (light orange) |
| Model Building Phase | `#D5E8F0` (light blue) |

---

## Resource Column Content

The Resource column in each Section C phase is auto-populated at generation time by querying the ARES content database. A typical Resource cell contains:

```
[Video: Introduction to Photosynthesis](http://ares.edu:8069/en/learn/#/topics/c/abc123)
[Reading: Khan Academy — Plant Biology](http://ares.edu:8069/en/learn/#/topics/c/def456)

🔍 Search ARES for similar videos/readings
   [photosynthesis Kenya biology](http://ares.edu/www2/search.php?...)
```

If no matching ARES content is found, only the generic search link appears.

---

## Pedagogical Framework

All lessons follow the **5-phase phenomenon-driven inquiry model**:

1. **Predict Phase** — Students write/draw initial ideas before any instruction. Connects to the anchoring phenomenon. Surfaces prior knowledge and misconceptions.

2. **Observe Phase** — Evidence gathering through practical work, video, simulation, or reading. Students collect data and make observations.

3. **Explain Phase** — Sensemaking. Students use observations to build explanations. Teacher facilitates with specific questioning moves and WAIT TIME (10–15 seconds minimum).

4. **Driving Question Board (DQB) Creation** — Students add questions or update existing questions. Tracks the class's growing understanding across the unit.

5. **Model Building Phase** — Students revise their cumulative explanatory model. The model is deliberately incomplete in Lesson 1 and evolves across all lessons.

**Key principles:**
- Every lesson connects back to the anchoring phenomenon
- The DQB is a living artifact — questions from Lesson 1 are answered by the final lesson
- Teacher moves are specific and actionable (quoted phrases, cold-call counts, WAIT TIME)
- Kenya-relevant contexts throughout (local food, scientists, places, current issues)
- NGSS Science and Engineering Practices are embedded, not bolted on

---

## KICD Compliance Requirements

The following elements must use **verbatim KICD language**:

- Specific Learning Outcomes (a–e)
- Sub-strand content bullet list
- Key Inquiry Questions
- Core Competencies (from KICD, supplemented)
- Core Values (from KICD, supplemented)
- Pertinent and Contemporary Issues (PCIs)

The following are invented/generated:

- Anchoring Phenomenon
- Driving Question
- Storyline Thread
- All lesson content (framework, overview, reflection, summary)
- Final Explanation sections and exemplars
- Differentiation strategies

When a teacher-authored template exists, the phenomenon and lesson sequence from the template take precedence over AI-generated content.
