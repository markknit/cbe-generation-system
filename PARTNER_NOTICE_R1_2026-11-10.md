# Contract change notice for Lesson3: revision R1 (schemaVersion 1.1.0)

Date: 10 November 2026. From: the CBE generation system (Grade 10 Biology, Chemistry, Physics, Mathematics).
Full detail: `CONTRACT_CHANGELOG.md` in the repository `markknit/cbe-generation-system`. This note is the short version.

## 1. The one change

The data contract (`ares-contract.schema.json`) now has **one new required field**. Nothing else in the contract changed.

Where: each row of `FINAL_EXPLANATION.rubric[]`.

| CBE level | JSON key | Status |
|---|---|---|
| Exceeds Expectations (4) | `excellent` | unchanged |
| Meets Expectations (3) | `proficient` | unchanged |
| Approaches Expectations (2) | `developing` | unchanged |
| Below Expectations (1) | `belowExpectations` | **NEW, required string** |

Before (R0, 1.0.0):

```json
{ "criterion": "…", "excellent": "…", "proficient": "…", "developing": "…" }
```

After (R1, 1.1.0):

```json
{ "criterion": "…", "excellent": "…", "proficient": "…", "developing": "…", "belowExpectations": "…" }
```

- `additionalProperties` is still `false` on the row: a row missing the new key, or with any other extra key, is invalid.
- `rubric` is still optional on `FINAL_EXPLANATION`. When present, every row needs all five keys.
- No field was renamed, removed or retyped. The old keys keep their names, so your change is additive, not a migration.
- Why: Kenya's CBE scale has four levels, and teachers asked for all four in the Grade 10 documents.

## 2. Version number

`schemaVersion` changes from `"1.0.0"` to `"1.1.0"`. The schema enum accepts **only** `1.1.0`, so old 1.0.0 files no longer validate.
Every data file we produce carries `"schemaVersion": "1.1.0"`.

## 3. What we ask Lesson3 to do

1. Take the updated `ares-contract.schema.json` (the `rubric.items` block and the `schemaVersion` enum).
2. Add `belowExpectations: string` to your rubric-row type, ingest and export.
3. Editor and export: show and edit a fourth column, "Below Expectations (1)", and round-trip the field. Column titles: Exceeds (4), Meets (3), Approaches (2), Below (1).
4. Update golden fixtures and checks (`contract-drift`, `contract-check`, `corpus-resource-check`). Every Grade 10 export in the new corpus carries the field in every rubric row.
5. Decide how to treat lesson plans already stored under 1.0.0 (no `belowExpectations`): re-import them, or tolerate the missing field on old records.
6. Tell us if you would rather the keys be renamed to `exceeds` / `meets` / `approaches` / `below`. That would be a separate revision (R2) and needs Mark's approval; we have not planned it.

## 4. Check a file yourself

```bash
python3 -c "import json,jsonschema;jsonschema.validate(json.load(open('FILE_data.json')),json.load(open('ares-contract.schema.json')))"
```

(jsonschema, draft 2020-12.)

## 5. Timing: which files are in which state

- The schema and the source data in the repository (`main`) are already at 1.1.0 and pass our validator (95 files / 806 lessons).
- The **already rendered exports** (`data/outputs/v2/**/_data.json`, docx, PDF) are **still 1.0.0 with three levels** until we regenerate them at promotion. If you run `run_lesson3_checks.sh` against those exports now, it will report 1.0.0 files.
- The revised Grade 10 corpus (teacher-reviewed changes, kept in a separate workspace) is at 1.1.0 and has all four levels in every rubric row (407 rows). It has not yet replaced the live data. We will tell you when the new exports are ready.
- Grade 11 Biology is also at 1.1.0 in source; its rendered files will follow later.

## 6. Other changes you will see when the new exports arrive (not contract changes)

The shape is the same, but the values differ from the last release:

- **Content:** many lesson, Final Explanation and rubric texts were edited after teacher review. Field names, required sets and the phase-label set are unchanged.
- **Lesson counts:** four Mathematics sub-strands were split into more lessons at teachers' request (sub-strand 2.6 now 12 lessons, 3.1 now 16, 3.2 now 12, 2.9 now 13). The corpus goes from 728 to 749 lessons. The schema has no fixed lesson count, so this is allowed.
- **Names and numbering:** some sub-strand names and numbers now follow KICD (for example "Vectors I", and renumbered Physics and Chemistry sub-strands). We have applied these as display labels only. Renaming module ids, folders and file prefixes to match is still undecided. If we do it, it will be a scripted rename at promotion, and it would change `substrand_id` and file paths. We will keep changes like this to a minimum where feasible and tell you as they are made. We cannot promise advance notice: the lesson plans come first, and Lesson3 is there to support them.
- **Resource links:** unchanged in shape, as described in `PARTNER_CONTRACT_NOTES.md` (null `video` / `reading` slots are still allowed).

## 7. What has not changed

`resourceLinks` shape, the quiz files (`quizSchemaVersion` 1.0.0, separate from `_data.json`), attribution (render-time only), and every other field and constraint in the contract.
