# Contract changelog — `ares-contract.schema.json`

**This is the one place that lists every change to the partner data contract
(`*_data.json`).** Newest first. Every entry says what changed, exactly where
in this repo, what it looks like before and after, and what the partner (the
Lesson3 editor/ingest) has to change. If a change is not here, it was not made
to the contract. Add an entry here in the same commit as any schema change.

Each revision has an id (R0, R1, ...) and a `schemaVersion` (R0 = `1.0.0`, R1 = `1.1.0`). The schema's `enum` accepts
only the current version.

---

## R1 — 2026-11-09 — fourth rubric level `belowExpectations`; `schemaVersion` 1.1.0 (decided by Mark)

**Why:** Kenya's CBE scale has four levels: Exceeds, Meets, Approaches and Below
Expectations. Teachers asked for all four in the Grade 10 journals. The contract
had three. Mark decided on 2026-11-09 that the contract changes now and the
partner conforms.

### What changed in the contract

Only `FINAL_EXPLANATION.rubric[]` rows. **One new required string field.**
Nothing was renamed, removed or retyped; every other part of the contract is
unchanged.

| CBE level | JSON key | Status |
|---|---|---|
| Exceeds Expectations (4) | `excellent` | unchanged (name kept) |
| Meets Expectations (3) | `proficient` | unchanged (name kept) |
| Approaches Expectations (2) | `developing` | unchanged (name kept) |
| Below Expectations (1) | `belowExpectations` | **NEW, required** |

Before (R0):
```json
{ "criterion": "…", "excellent": "…", "proficient": "…", "developing": "…" }
```
After (R1):
```json
{ "criterion": "…", "excellent": "…", "proficient": "…", "developing": "…", "belowExpectations": "…" }
```
`additionalProperties` is still `false` on the row, so a file with the field
missing OR any other extra key is invalid. `rubric` itself is still optional
on `FINAL_EXPLANATION`; when present, every row needs all five keys.

The old keys keep their names on purpose, so the partner's change is additive
(one more field), not a migration. If the partner would rather rename the keys
to `exceeds` / `meets` / `approaches` / `below`, that is a separate R2 and Mark
must approve it.

### Where it lives in this repo (everything that was touched)

| What | File | Place |
|---|---|---|
| The contract itself | `ares-contract.schema.json` | `FINAL_EXPLANATION.rubric.items` (`required` + `properties`); also a note in the top-level `description` |
| Our validator (partner-equivalent check) | `generators/lib/lesson_contract.js` | the `FE.rubric.forEach(... need(...))` line (~165) |
| Word/PDF renderer (4 columns) | `generators/lib/build_docs.js` | rubric table, `RW3`/`RW3r` widths and header cells (~108-190) |
| Generation schema + prompt (new modules get 4 levels) | `src/generate_substrand.py` | `FE_TOOL_SCHEMA` rubric items (~638) and the "rubric" instruction line (~1129) |
| Stub/FE repair prompts | `scripts/repair_stubs.py` (`FE_SCHEMA`), `scripts/patch_batch_mode.py` | the rubric JSON examples |
| Documentation | `docs/SCHEMA.md` ("Rubric row fields"), `docs/LESSON_PLAN_FORMAT.md` | |
| The data | every `*_data.js` / `*_data.json` `FINAL_EXPLANATION.rubric[]` | revised corpus: `data/revised_2026-10_full/modules/`; Grade 11 Biology: `generators/data/` |

Not touched (legacy, not part of the live pipeline): `generators/math_*_*.js`,
`generators/biology_*.js`, `scripts/write_builders.py` and `src/reformat_*.py`.
They still print three levels; do not run them.

### Internal tooling note (not part of the contract)

`CBE_LEGACY_RUBRIC=1` (env var) makes our validator accept rubric rows with only three levels and lets the renderer
print an empty fourth cell. It exists for ONE purpose: `scripts/revise_build.py` renders the pre-revision baseline
(three levels) to produce the tracked-change Word files. It is read in `generators/lib/lesson_contract.js` and
`generators/lib/build_docs.js` and set in `scripts/revise_build.py`. It must never be set for a real release build.
The partner's validator needs nothing like it.

### Where the data stands (2026-11-09)

- Revised Grade 10 corpus (`data/revised_2026-10_full/modules`, 85 modules): every rubric row (407) has
  `belowExpectations`; `validate_corpus.js` with `CBE_DATA_DIR` on that folder passes (85 files / 728 lessons).
  Each row has a change record `<module>-r2-rub-NNN` in `change_records/`.
- Grade 11 Biology (`generators/data/g11_bio_*`, 10 modules): all 50 rubric rows have `belowExpectations`; `validate_corpus.js g11_bio` passes. Their already-rendered docx/PDF/`_data.json` under `data/outputs/v2/Grade11/` still show three levels until regenerated (not done).
- Unrevised Grade 10 in `generators/data/`: four levels too (backfill, see above).

### What the partner has to do

1. Take `ares-contract.schema.json` from this repo (the `rubric.items` block).
2. Ingest/type definitions: add `belowExpectations: string` to the rubric-row type.
3. Editor UI / export: show and edit a fourth column "Below Expectations (1)";
   round-trip the field. Existing column titles: Exceeds (4), Meets (3),
   Approaches (2), Below (1).
4. Validators and fixtures (`contract-drift`, `contract-check`, `corpus-resource-check`):
   update golden fixtures; every Grade 10 and Grade 11 export in the new
   corpus carries the field in every rubric row.
5. Existing stored lesson plans that were imported under R0 have no
   `belowExpectations`; decide whether to migrate (backfill from a re-import)
   or to tolerate the missing field on old records.

### How to check a file against R1

```bash
# our validator (revised corpus):
CBE_DATA_DIR=data/revised_2026-10_full/modules node scripts/validate_corpus.js
# raw JSON-schema check of one export (jsonschema, draft 2020-12):
python3 -c "import json,jsonschema;jsonschema.validate(json.load(open('FILE_data.json')),json.load(open('ares-contract.schema.json')))"
```

### schemaVersion 1.0.0 -> 1.1.0 (Mark, 2026-11-09): where and why

Why: a required field was added, so old files are no longer valid; the version number lets the partner (and our
validators) tell the two shapes apart. Every place that carries or defines the version was changed together:

| What | Where | Change |
|---|---|---|
| Contract | `ares-contract.schema.json`, `schemaVersion.enum` (+ description) | `["1.0.0"]` -> `["1.1.0"]` |
| All data modules | `generators/data/*_data.js` (95 files: 85 Grade 10 + 10 Grade 11 Biology) and `data/revised_2026-10_full/modules/*_data.js` (85) | `const schemaVersion = '1.1.0';` |
| Generator | `src/generate_substrand.py`, `SCHEMA_VERSION` (written into every new data file) | `'1.1.0'` |
| Legacy backfill script | `scripts/backfill_contract.js`, `SCHEMA_VERSION` | `'1.1.0'` (it only stamps the version, it does not add rubric fields) |
| Docs | `docs/SCHEMA.md` (version line and field table) | 1.1.0 |
| NOT changed | `data/revised_2026-10_full/baseline/` (the pre-revision snapshot used for tracked changes: stays R0/1.0.0 on purpose) | |
| NOT changed | `quizSchemaVersion` (separate quiz file contract, unaffected) | |
| NOT regenerated | the already rendered `data/outputs/v2/**/_data.json`, `*.docx`, PDFs, index | still R0 (version 1.0.0, three rubric levels) until regenerated at promotion; the partner's `run_lesson3_checks.sh` reads these exports, so it will report R0 files until then |

`main` rubric backfill (also Mark, 2026-11-09 'update to 4 levels as needed'): the 85 unrevised Grade 10 modules in
`generators/data/` got `belowExpectations` too, so `node scripts/validate_corpus.js` passes on `main` (95 files / 806
lessons). 385 of the 408 rows reuse the descriptor written for the same criterion in the revised corpus (label
'Below Expectations:' removed because these modules' other levels carry no label); 23 rows whose criterion differs
were drafted. Script: `scripts/round2/backfill_main_rubric.py`. These texts disappear at promotion, when the revised
modules replace these files.

### Open items for R1

- Descriptors for the new level are model-drafted: teachers should review them like the other Round 2 changes.
- Promotion of the revised corpus, regeneration of outputs (Grade 10 and the held Grade 11 Biology) and the Drive sync are
  not done.

---

## R0 — 2026-09-29 — baseline

`schemaVersion` `1.0.0`, three rubric levels. `resourceLinks` map per lesson;
see `PARTNER_CONTRACT_NOTES.md` for what changed in the values (not the shape)
on 2026-09-29/30.
