# Partner Contract Notes: Bounded Project v2 (2026-09-29 → 2026-09-30)

For the team maintaining the Lesson3 teacher lesson-plan editor, which
validates our `*_data.json` against `ares-contract.schema.json`.

**Summary: the contract is unchanged. Nothing was added to or removed from
`_data.json`, and all 85 Grade 10 exports still validate.** What changed is
the *values* inside `resourceLinks`, plus some new files beside `_data.json`
that the contract doesn't cover.

---

## 1. `_data.json`: same schema, different link values

- **Schema:** unchanged. All 85 files validate against
  `ares-contract.schema.json` (checked 2026-09-30, `jsonschema`, draft 2020-12).
- **Lesson content:** unchanged. Every field except `resourceLinks` is
  byte-identical to the previous release (diff-checked on all 85 files).
- **`resourceLinks` values:** re-selected by a new relevance-ranked matcher.
  This fixed wrong-subject links, answer keys surfaced as resources, and
  dead links (design: `DESIGN_link_selection_v2.md`). Three things behave
  differently. All of them are allowed by the existing schema, but code
  written against the old data may have assumed otherwise:

  | Change | Before | Now | What to check in Lesson3 |
  |---|---|---|---|
  | `video` / `reading` can be `null` | 0 of 7,280 slots were null | 830 null (315 video, 515 reading) | The editor displays and round-trips `null` without error. `fallback_search_url` is always present and usable. |
  | `direct_url` hosts | All 7,280 were Kolibri links | 6,263 Kolibri (`http://ares.local:8069/en/learn/#/topics/c/<id>`) + 187 direct web modules (`http://ares.local/modules/...`) | No hardcoded assumption that `direct_url` is a Kolibri link. |
  | `tier` meaning | Primary ranking key | Still the channel quality tier (0 = best), but ranked *after* relevance | Don't treat `tier` as a relevance or quality score for the link itself. |

- The hostname is `ares.local` throughout (0 `ares.edu`). This has been true
  since 2026-08-02, and nothing changed here in v2.

## 2. New files the contract does not cover

These are additive and live beside `_data.json`. Lesson3 can ignore them
until it wants quizzes.

| File | Where | Format |
|---|---|---|
| `<prefix>_quiz.json` | Same folder as `_data.json` | `docs/SCHEMA.md`, "Quick Check quiz file", `quizSchemaVersion: "1.0.0"` |
| `quiz/*_QuickCheck.pptx`, `quiz/*_AnswerKey.html`, `quiz/*_AnswerKey.docx` | `quiz/` subfolder | Rendered outputs |

- **Quiz data is deliberately not in `_data.json`.** The contract is
  `additionalProperties: false` at every level, so a `quiz` field would fail
  validation. If Lesson3 later wants quizzes in the same file, that needs a
  contract change on both sides. Until then the separate file is the
  interface.
- **Coverage is partial:** 27 of 728 Grade 10 lessons have quizzes (8
  sub-strands, 196 questions), for review before the remaining 701 are
  generated. A missing quiz file, or a quiz file without some lesson
  numbers, is expected.
- Each question has `phase` (`predict | observe | explain | dqb | model |
  end`) and `placement` (the activity it follows), so it can be placed
  inline later.

## 3. Attribution: render-time only

The credit and licence text (CC BY-NC 4.0; SeaVuria and ARES) appears in
every docx, deck and answer key. It is **not** in `_data.json` and needs no
contract field. The source is `config/attribution.yaml`. If Lesson3 renders
its own documents from `_data.json`, it has to add attribution itself.

## 4. Unchanged, for the record

- Field names, required sets, the phase-label set and the lesson count per
  sub-strand.
- Grade 10 output paths: still flat `v2/<Subject>/SS<n>_<Name>/`. New grades
  will use `v2/Grade{N}/<Subject>/...`, the only planned path change, and it
  does not affect existing files.

## Open item

- Partner confirmation that Lesson3 handles `null` resource slots. This
  continues the earlier `resourceLinks` heads-up tracked in `STATUS.md`
  Active Threads.
