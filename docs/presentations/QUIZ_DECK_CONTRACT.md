# Three-project contract: lessons and quizzes, decks, classroom runtime (DRAFT v2, 2026-11-23, for Mark)

Status: **DRAFT. Not yet acknowledged by Project 3.** Nothing here binds a project until its owner has acknowledged it (section 9).
Where this draft states Project 3's side, it is what Project 3 has told this project so far or this project's proposal. Project 3 must
confirm or correct it. Items marked **[P3 TO CONFIRM]** are open questions, not facts.

## 1. The three projects

| | Project | Where it runs | Owns |
|---|---|---|---|
| **P1** | Lesson plans and quizzes (`cbe-generation-system`, branch `main`, Claude Code CLI) | jhm-spark | `*_data.json` lesson plans, `*_quiz.json` quizzes, the data contract, the quiz generator and validator, control documents |
| **P2** | Teacher presentations (branch `presentations`, worktree `cbe-presentations`, Claude Code CLI) | jhm-spark | deck specs, decks (`.pptx`), figure generators, `data/quiz_registry.json`, the slide-to-question list (`<deck>.quizlinks.csv`) |
| **P3** | Classroom runtime (Codex CLI, another device) | other device | running a presentation with the teacher, serving and triggering quiz questions, capturing responses, the Kolibri integration for student data, reports |

Single flow: **P1 writes the lesson and the quiz; P2 turns them into a deck that carries quiz icons with links; P3 runs the deck, serves
the question behind each link, captures responses and reports.** Each arrow below is an interface with one owner.

## 2. Principles

1. **One owner per fact.** Lesson content: P1. Quiz content: P1. Question IDs and versions: P2's registry. Link route and response storage: P3.
   Student data: P3 and Kolibri only. Nobody else holds or edits another owner's fact; they read it.
2. **Identity comes from the lesson plan.** Every ID is derived from `subject, grade, substrand id, lesson number`. A change to those is a
   change to every downstream project.
3. **No student data outside P3/Kolibri.** Not in a quiz file, a deck, a link, a registry, a log or a report produced by P1 or P2.
4. **Provisional until acknowledged.** A change to an interface is made in this document first, acknowledged, then implemented.
5. **Control documents are edited only on `main`.** The master copy of this contract should move to P1's repo (see section 10); until
   then it lives on `presentations` and is copied to P3 by Mark.

## 3. Interface A: P1 -> P2 (lesson plans and quizzes)

P2 reads, never writes. P1 guarantees:
1. Lesson plans conform to `ares-contract.schema.json` and pass `validate_corpus.js` (P2 reads only `*_data.json`).
2. A quiz belongs to a lesson by `meta.subject`, `meta.grade`, `meta.substrandId` and lesson `number`. A renumbered, split, merged or moved
   lesson needs its quiz regenerated for the new number.
3. Quiz title equals lesson plan title. Each question has `phase` (`predict, observe, explain, dqb, model, end`) and `placement` text
   naming a lesson activity. Questions are self-contained. The quiz JSON carries no IDs, links or student data.
4. `quizSchemaVersion` changes only through a note in this document.
Check (P2 side): `python3 scripts/quiz_links.py check`. Today: 105 quizzes, all pass.

## 4. Interface B: P2 -> P3 (decks, links, registry)

P2 guarantees:
1. **Link format** `http://ares.local/quiz/<quiz-id>/<version>/question/<question-id>`, with
   quiz-id `<subject>-g<grade>-<substrand, dots as dashes>-l<nn>`, e.g. `bio-g10-1-2-l01`; question-id `q01...`; version `v1...`.
   Subject codes: bio, chem, phys, math, cmath, emath, gsci. **PROVISIONAL: P3 owns the route and may change it; the template is one
   line in `scripts/quiz_links.py` and `generators/presentations/lib/quizlinks.js`.**
2. **A link carries no class, student, card number or answer.** The deck shows only an icon; the teacher starts capture inside ARES.
3. **IDs are stable.** `data/quiz_registry.json` keeps them: identical prompt keeps its ID; a reworded question (text at least 60% similar)
   keeps the ID it replaced; otherwise a new ID; a retired ID is never reused. **Version** bumps when the wording, a choice, the choice order,
   the correct answer or the rationale changes (phase and placement never do). Retired IDs and history are kept in the registry.
4. **Registry is published to P3** (a copy of `data/quiz_registry.json`, plus the quiz JSON it points to). The quiz JSON has no IDs, so P3
   needs the registry to map `(quiz-id, version, question-id)` to question text, choices and the correct answer. **[P3 TO CONFIRM how
   P3 will receive it: file copy, git, Drive.]**
5. **Slide-to-question list** `<deck>.quizlinks.csv`: slide number, quiz id, version, question id, url, phase, placement. P3 may use it to
   know which slide a question belongs to. Slide numbers move when a deck is rebuilt, so P3 must not store slide numbers as identity;
   identity is the question ID.
6. Decks are `.pptx`, with the icon as a hyperlink. Generated decks are not committed; they are shared through Drive after Mark approves.
   **[P3 TO CONFIRM: how does P3 receive and open decks (PowerPoint, Google Slides, a web view)? Does a hyperlink icon work in that
   path, and does `ares.local` resolve on the teacher's device?]**

## 5. Interface C: P3 -> P2 and P1 (what P3 needs and may ask for)

P3 must:
1. Treat `(quiz-id, version, question-id)` as the identity of a question and store every response against it, **including the version**, so a
   later rewording does not silently merge old and new answers.
2. Resolve any link whose version is older than the current one (a teacher opens an old deck): show the question as it was in that version, or
   show the current one and record which version was shown. **[P3 TO CONFIRM which.]** The registry's `history` keeps the old question IDs
   per version; **P2 currently stores only the hash and prompt of the current version, not the old text.** If P3 needs old text, the quiz
   archive must be kept; this is an open item (section 8).
3. Never write back into P1 or P2 files. Requests go through this document.
4. Keep student and class data inside P3 and Kolibri. Reports to teachers are P3's.

## 6. What must not drift (single-source table)

| Fact | Owner | Read by | Where it lives |
|---|---|---|---|
| Lesson plan text, lesson numbers, titles | P1 | P2, P3 | `*_data.json` |
| Quiz questions, choices, answer, rationale, phase, placement | P1 | P2, P3 | `*_quiz.json` |
| Question ID and version | P2 | P3 | `data/quiz_registry.json` |
| Link format | P3 (route), P2 (template) | all | this document, section 4.1 |
| Which slide carries which question | P2 | P3 | `<deck>.quizlinks.csv` |
| Responses, classes, learner identity, reports | P3 / Kolibri | nobody else | P3 |
| This contract | P1 (master), P2 (draft) | all | this file until moved |

## 7. Change procedure

1. Whoever wants a change writes it in this document under "Proposed changes" with the date and the affected interface.
2. The owner of each affected project acknowledges in section 9.
3. Only then is it implemented, in the order P1, P2, P3.
4. A change to question or lesson identity (lesson renumbering, quiz regeneration) is announced to P2 and P3 **before** it lands, with the
   list of lessons affected.

## 8. Open items

1. **P1:** which quizzes (about 10) are being rebuilt, and do the Round 2 splits (728 to 749) renumber any lesson? Only 27 of 728 Grade 10
   lessons have a quiz today; links appear only where a quiz exists.
2. **P1:** add to the quiz validator: title equals lesson plan title, lesson number exists in the plan (today only P2's check does this).
3. **P2/P3:** whether the registry must keep full old text per version (section 5.2).
4. **P3:** the route, the delivery path for decks, and that `ares.local` resolves in the classroom.
5. **P3:** what P3 needs from a quiz that it does not get today (for example a time limit, a points value, a media attachment). It must say so
   here before P1 adds a field.
6. **All:** where the master copy lives, who may edit it, and how it is distributed to the P3 device.
7. **P3:** how Kolibri is keyed to a learner and a class, and what P3 sends back, if anything, for use in P1 or P2 (the default is nothing).

## 9. Acknowledgement (nothing binds until all three are filled)

| Project | Owner | Acknowledged (date) | Notes or changes requested |
|---|---|---|---|
| P1 lesson plans and quizzes | | | |
| P2 presentations | | | |
| P3 classroom runtime | | | |

## 10. Procedure when quizzes are regenerated (P1 -> P2 -> P3)

1. P1: regenerate and validate (`scripts/validate_quiz.py`), announce the affected lessons to P2 and P3 (section 7.4).
2. P2: `git merge main`, run `python3 scripts/quiz_links.py check` (must say OK).
3. P2: rebuild the registry. **Before any deck with links is distributed, delete `data/quiz_registry.json` first** so every question starts
   at `v1` with clean IDs. After distribution it is never deleted, only updated (`quiz_links.py registry`).
4. P2: rebuild the affected decks, then publish the registry and decks to P3.
5. P3: take the new registry and confirm that every link in the new decks resolves.

## 11. Packet for Project 3 (copy into its session)

> Three projects share one design. P1 (`cbe-generation-system`) writes lesson plans and quizzes. P2 (presentations branch) builds decks and
> puts a quiz icon with a link on the slide where a question belongs. P3 (you) runs the deck, serves the question behind each link, captures
> responses and reports through Kolibri. Please read `docs/presentations/QUIZ_DECK_CONTRACT.md` (copy attached), answer every item marked
> **[P3 TO CONFIRM]**, add anything P3 needs that the contract lacks to section 8, and report back whether you acknowledge it. Until then
> treat the link format as provisional and do not rely on it. Your side owns the route, response storage, student data and reports.
> Do not add student data to any link, quiz file or deck. Identity of a question is `(quiz-id, version, question-id)`; store the version
> with every response.
