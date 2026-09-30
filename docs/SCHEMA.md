# SCHEMA.md — Data File Schema Contract
## Kenya CBE Lesson Plan Generation System

> This document is the authoritative reference for `_data.js` field names.
> The `_data.js` file is the source of truth; `docx` and `_data.json` are
> generated artifacts. All field names here are canonical. Do not introduce
> synonyms.

---

## Style conventions

- Use bare JS keys (no quotes): `totalDuration:` not `"totalDuration":`
- All `_data.js` files are CommonJS modules (`'use strict'`)
- String values use single quotes in JS files; JSON export uses double quotes

---

## Top-level exports

Every `_data.js` declares a top-level `schemaVersion` and exports six members:

```js
module.exports = { schemaVersion, META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE };
```

| Member | Type | Notes |
|---|---|---|
| `schemaVersion` | string | Semver (`^\d+\.\d+\.\d+$`) of the contract this file conforms to. Currently `'1.0.0'`. |
| `META` | object | Output config + document titles. |
| `UNIT` | object | Sub-strand overview. |
| `LESSONS` | array | One object per lesson. |
| `FINAL_EXPLANATION` | object \| null | Student assessment doc; `null` if not yet authored. |
| `SUMMARY_TABLE` | object \| null | Teacher reference table; `null` if not yet authored. |


---

## Contract conformance

Field *names* and *style* are governed by this document. Machine-validated
*presence* of required fields is governed by the colleague's JSON Schema,
`ares-contract.schema.json`
(raw: `https://raw.githubusercontent.com/james-beep-boop/Lesson3/main/app/src/ingest/ares-contract.schema.json`).
Validate with `npx tsx scripts/contract-drift.ts -- generators/data` (run from the colleague's `app/`).

Current contract version: **1.0.0**, declared per file via the top-level `schemaVersion`.

Required fields (everything else is optional):

- **Top-level:** `schemaVersion`, `META`, `UNIT`, `LESSONS`, `FINAL_EXPLANATION`, `SUMMARY_TABLE` — the last two may be `null`.
- **META:** `subject`, `grade`, `substrand_id`, `substrand_name`, `titleDoc`.
- **UNIT:** `gradeLevel`, `subject`, `strand`, `substrand`, `totalDuration`, `content`, `learningOutcomes`, `coreCompetencies`.

---

## META fields

| Field | Type | Description |
|---|---|---|
| `subject` | string | e.g. `'Biology'` |
| `grade` | number | e.g. `10` |
| `substrand_id` | string | e.g. `'1.4'` |
| `substrand_name` | string | e.g. `'Chemicals of Life'` |
| `outputDir` | string | Relative output path |
| `filePrefix` | string | Filename stem for outputs |
| `titleDoc` | string | Document title (all caps) |
| `subtitleDoc` | string | Document subtitle |
| `col3Label` | string | Section C column 3 header (typically `'Teacher Moves'`) |
| `col5Label` | string | Section C column 5 header |

---

## UNIT fields

| Field | Type | Canonical name | Notes |
|---|---|---|---|
| Grade level | string | `gradeLevel` | e.g. `'10'` |
| Subject | string | `subject` | |
| Strand | string | `strand` | Full KICD strand label |
| Sub-strand | string | `substrand` | Full KICD sub-strand label |
| Total duration | string | `totalDuration` | ⚠ NOT `duration` |
| Learning outcomes | string | `learningOutcomes` | Verbatim from KICD |
| Core competencies | string | `coreCompetencies` | |
| Values | string | `values` | |
| Science & Engineering Practices | string | `sep` | |
| PCIs | string | `pcis` | |
| Careers | string | `careers` | |
| Focus summary | string | `focus` | 2–3 sentence overview |
| Phenomenon | string | `phenomenon` | Anchoring phenomenon description |
| Supporting phenomena | string | `supportingPhenomena` | Optional; additional phenomena used across lessons |
| Sub-strand content | string | `content` | **Required** (contract). KICD content summary; renders as the "Sub-Strand Content" overview row. |
| Driving question | string | `drivingQuestion` | Includes KICD key inquiry questions |
| Storyline thread | string | `storylineThread` | ⚠ NOT `storyline` |

---

## LESSON fields

Each element of the `LESSONS` array:

| Field | Type | Canonical name | Notes |
|---|---|---|---|
| Lesson number | number | `number` | |
| Title | string | `title` | |
| Duration | string | `duration` | Lesson-level; stays as `duration` |
| Sub-strand label | string | `substrand` | |
| ARES keywords | string | `aresKeywords` | |
| Specific learning outcomes | object | `slo` | See SLO fields below |
| Overview | string | `overview` | 2–3 paragraph prose |
| Framework | array | `framework` | See Framework fields below |
| Teacher reflection | string | `teacherReflection` | |
| Summary table | object | `summaryTablePrompt` | Optional; pre-filled student prompts |

### SLO fields (inside `slo`)

| Field | Canonical name |
|---|---|
| Purpose statement | `purpose` |
| Knowledge bullets | `knowledge` |
| Skills bullets | `skills` |
| Attitudes bullets | `attitudes` |
| Key inquiry question | `keyInquiry` |
| Purpose in storyline | `purposeInStoryline` |
| Safety notes | `safetyNotes` |

### Framework row fields (each element of `framework`)

| Field | Canonical name |
|---|---|
| Phase name | `phase` |
| Learner experience | `learnerExperience` |
| Resource | `resource` |
| Teacher moves | `teacherMoves` |
| Sensemaking strategy | `sensemakingStrategy` |
| Formative assessment | `formativeAssessment` |

---

## FINAL_EXPLANATION fields

`object | null` — the student assessment document; `null` until authored.

| Field | Type | Canonical name | Notes |
|---|---|---|---|
| Subject label | string | `subjectLabel` | All-caps sub-strand label, e.g. `'CHEMICALS OF LIFE'` |
| Instructions | string | `instructions` | Student-facing task instructions |
| Sections | array | `sections` | One per question section; see below |
| Rubric | array | `rubric` | Optional; scoring criteria; see below |

### Section fields (each element of `sections`)

| Field | Canonical name | Notes |
|---|---|---|
| Title | `title` | e.g. `'SECTION 1: ...'` |
| Prompt | `prompt` | Question prompt |
| Exemplar | `exemplar` | Optional; model answer / teacher reference |

### Rubric row fields (each element of `rubric`)

| Field | Canonical name |
|---|---|
| Criterion | `criterion` |
| Excellent | `excellent` |
| Proficient | `proficient` |
| Developing | `developing` |

> The v1.0.0 contract enumerates the Biology 3-level set above. Subject-specific
> frameworks (KICD 4-Level for Mathematics; Beginning/Developing/Proficient/Advanced
> for Chemistry and Physics) carry more or differently-named levels — confirm the
> rubric shape with the contract owner before generating Chemistry/Physics FE, or
> omit `rubric` (it is optional) until the contract defines those variants.

---

## SUMMARY_TABLE fields

`object | null` — the teacher reference table; `null` until authored.

| Field | Type | Canonical name | Notes |
|---|---|---|---|
| Sub-strand label | string | `subStrand` | e.g. `'Sub-Strand 1.4: Chemicals of Life'` |
| Driving question | string | `drivingQuestion` | |
| Lessons | array | `lessons` | One row per lesson; see below |

### Lesson row fields (each element of `lessons`)

| Field | Canonical name |
|---|---|
| Lesson number | `number` |
| Title | `title` |
| What did I observe? | `observed` |
| What did I learn? | `learned` |
| How does this explain the phenomenon? | `explained` |

---

## Known legacy inconsistencies (now resolved)

| File(s) | Was | Now |
|---|---|---|
| bio_2_1, math_2_2, math_2_3, math_2_4 | `duration:` (UNIT level) | `totalDuration:` |
| bio_1_1, bio_1_2, bio_1_3, bio_2_2, bio_2_3, bio_3_1, bio_3_2, bio_3_3 | `storyline:` / `"storyline":` | `storylineThread:` |
| bio_1_4 | `const UNIT = {}` (empty) | Fully populated |
| bio_1_2, bio_2_2, bio_2_3, bio_3_1, bio_3_2, bio_3_3 | JSON-quoted keys `"field":` | Bare JS keys `field:` |

---

## JSON export

`build_docs.js` writes a `*_data.json` alongside each docx output.
The JSON export uses the same field names as above (camelCase throughout).
The colleague's teacher editing tool should treat `*_data.json` as
read-only input and submit edits via the agreed patch format (see
`docs/EDITING_CONTRACT.md` once drafted).

**Attribution is not in the JSON.** The licence and credit text
(`config/attribution.yaml`) is added at render time to the docx, decks and
answer keys only. The contract has no field for it, and none is needed.

---

## `resourceLinks` (per lesson, JSON export only)

Written by `generators/aresResources.js` from `src/ares_recommender.py`.
Shape: `ares-contract.schema.json` `$defs/resourceLinks` (strict). There is
one entry for each of the five phases, `predict`, `observe`, `explain`,
`dqb` and `model`:

```js
resourceLinks: {
  predict: {
    video:   { title, source, content_type, direct_url, search_url,
               search_terms, exact_search_url, has_transcript, tier } | null,
    reading: { ...same fields... } | null,
    fallback_search_url: "http://ares.local/www2/search.php?..."   // always present
  },
  observe: {...}, explain: {...}, dqb: {...}, model: {...}
}
```

- **`null` is normal (since 2026-09-29).** The matcher leaves a slot empty
  when no candidate passes the relevance gate, where it used to show a weak
  or wrong link. On 2026-09-30, 830 of 7,280 slots were `null` (315 video,
  515 reading). Consumers must handle it. `fallback_search_url` is always a
  usable link.
- `direct_url` is either a Kolibri link (`http://ares.local:8069/en/learn/#/topics/c/<id>`,
  6,263 records) or a direct web-module link (`http://ares.local/modules/...`,
  187 records: SeaVuria videos, PhET sims).
- `tier` is the source channel's quality tier (0 = best). It is not a
  relevance score, and relevance now outranks it.
- The host comes from `ARES_HOST` (default `ares.local`).
- The docx renders one link per filled slot, plus the search link. The JSON
  also carries `search_url` / `exact_search_url` alternatives.

---

## Quick Check quiz file — `<filePrefix>_quiz.json` (added 2026-09-29)

Sits next to `<filePrefix>_data.json` in the sub-strand's output directory.
**It is a separate file on purpose:** the partner contract
(`ares-contract.schema.json`) is `additionalProperties: false` throughout, so a
`quiz` field inside `_data.json` would be rejected. `_data.json` is unchanged.

Written by `src/generate_quiz.py`, validated by `scripts/validate_quiz.py`,
rendered by `generators/build_quiz.js` into `quiz/` (Quick Check `.pptx`,
Answer Key `.html` + `.docx`; PDFs via `generate_pdfs.js`). Settings:
`config/quiz_generation.yaml`.

```js
{
  quizSchemaVersion: "1.0.0",
  meta: { subject, grade, substrandId, substrandName, filePrefix },
  lessons: [
    {
      number: 2, title: "…", model: "claude-sonnet-5-5", generatedAt: "ISO-8601",
      quiz: [
        {
          prompt: "string",          // self-contained question text
          choices: ["", "", "", ""], // exactly 4; order is shuffled (seeded) after generation
          correctIndex: 0,           // 0-3
          rationale: "string",       // teacher-facing; never names an answer letter
          phase: "observe",          // predict | observe | explain | dqb | model | end
          placement: "string",       // the activity in THIS lesson plan the question follows
          check: "150/10000"         // optional: arithmetic whose value is in the correct choice
        }
      ]
    }
  ]
}
```

- 5–10 questions per lesson (5–7 normal; the validator warns above 7). `phase`
  and `placement` let a future presentation generator insert questions
  inline without regenerating them.
- A quiz file may cover only some lessons. On 2026-09-30, 8 files held
  quizzes for 27 of 728 Grade 10 lessons, pending review.
- `check` is present only for calculated answers. The validator evaluates it
  (degrees for trig) and fails the lesson if the value is not in the correct
  choice, allowing for the rounding shown.
- Answers never appear in the student deck, including speaker notes.
