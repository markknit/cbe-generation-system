# Quiz <-> presentation contract (DRAFT 2026-11-23, for Mark)

Two projects share one source of lesson data and must change together:

- **`main` (cbe-generation-system):** writes the lesson plans (`*_data.json`) and the quizzes (`*_quiz.json`).
- **`presentations` branch:** reads both, builds the decks, and puts a quiz icon with a link on the slide where a quiz question belongs.

Neither side may change what the other depends on without a note here. The master copy of this contract should live on
`main` (control documents are edited only there); this file is the presentations branch's statement of what it needs.

## What the decks depend on (main must keep these true)

1. **Quiz identity comes from the lesson plan, not from the quiz.** quiz-id = `<subject>-g<grade>-<substrand with dots as dashes>-l<nn>`,
   built from `meta.subject`, `meta.grade`, `meta.substrandId` and the lesson `number`. If a lesson is renumbered, split, merged or moves
   sub-strand, its quiz must be regenerated for the new number, or the link will open the wrong quiz.
2. **Quiz title equals the lesson plan title.** `quiz_links.py check` compares them.
3. **Each question has `phase`** (one of `predict, observe, explain, dqb, model, end`) **and `placement`** (a sentence naming the lesson
   activity it follows). The deck uses these to choose the slide for the icon.
4. **Questions are self-contained** (nothing like "the slide above"), because a link opens one question on its own.
5. **No question IDs, links or student data inside the quiz JSON.** IDs are assigned by the registry on this branch.
6. The quiz file keeps its own `quizSchemaVersion`. Any change to the keys above is a change to this contract.

## What the presentations branch guarantees

- Question IDs (`q01...`) and versions (`v1...`) are assigned in `data/quiz_registry.json` and are stable across regeneration:
  an identical prompt keeps its ID; a reworded one (text at least 60% similar) keeps the ID it replaced; otherwise a new ID is issued
  and the old one is retired, never reused. The version bumps when the wording, a choice, the choice order, the correct answer or the
  rationale changes.
- Link format (PROVISIONAL, owned by the response-capture project, route not implemented):
  `http://ares.local/quiz/<quiz-id>/<version>/question/<question-id>`. No student, class or answer data in a link.
- The deck never edits a quiz or a lesson plan.

## Procedure when quizzes are regenerated

1. On `main`: regenerate and validate the quizzes (`scripts/validate_quiz.py`), then run the lesson-plan gates.
2. On `presentations`: `git merge main`, then `python3 scripts/quiz_links.py check` (must say OK).
3. Rebuild the registry. **Until decks with links are distributed, delete `data/quiz_registry.json` first** so every question starts at
   `v1` with clean IDs; after distribution, never delete it, only update it (`quiz_links.py registry`).
4. Rebuild the decks for the lessons whose quiz changed (the deck's input hash includes the quiz, so only those rebuild).

## Open items

- Which of the roughly 10 quizzes being rebuilt will be regenerated, and whether the Round 2 lesson splits (728 to 749) change any lesson numbers.
- Only 27 of 728 Grade 10 lessons have a quiz today; a link can appear only where a quiz exists.
- Mark to approve moving the master copy of this contract to `main` (suggested: a short section in `CONTRACT_CHANGELOG.md` plus a pointer
  from `config/quiz_generation.yaml`), so the quiz generator's validator can enforce items 1 to 4 itself.

## Text for the `main` session (copy into its notes)

> Presentation decks link to individual quiz questions. Quiz identity is `<subject>-g<grade>-<substrand>-l<nn>` from the lesson plan, so a
> renumbered or split lesson needs its quiz regenerated. Every question must keep `phase` and `placement`, titles must equal the lesson plan
> title, questions must be self-contained, and the quiz JSON must carry no IDs. The presentations branch assigns question IDs and versions in
> its own registry. Contract: `docs/presentations/QUIZ_DECK_CONTRACT.md` on branch `presentations`. Consistency check: `python3 scripts/quiz_links.py check`.
