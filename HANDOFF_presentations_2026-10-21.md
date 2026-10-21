# HANDOFF — Lesson presentations (PowerPoint decks)

**Date:** 2026-10-21 · **Branch:** `presentations` (worktree `/home/markk/ares/cbe-presentations`) · **Rigor level:** 3 (partner and teachers depend on the output; large run; hard to redo)
**Status file:** `STATUS_PRESENTATIONS.md` · **Design spec:** `docs/presentations/BUILD_MANUAL.md` (source `.docx` beside it) · **Overrides:** `docs/presentations/OVERRIDES.md`

This document is binding for the first build session. Locked decisions below are not re-opened unless Mark says so. Read, in order: CLAUDE.md "Branch Policy", `STATUS_PRESENTATIONS.md`, this file, `OVERRIDES.md`, then the manual.

---

## 1. Goal

Generate one teacher-ready `.pptx` per lesson (16:9, Calibri) from the signed-off lesson data, following the SeaVuria Science Lesson PowerPoint Build Manual v1.0 as modified by OVERRIDES.md. The deck **is** the lesson plan for teachers: slides face students, speaker notes teach the teacher.

**Scope for now:** Grade 10 Biology, Chemistry, Physics (the manual's scope). General Science and Essential Mathematics are not covered by the manual; **Mathematics and Core Mathematics are processed last**, and Mark expects they will not need a separate process (undecided). Grade 11 and non-STEM: out of scope until decided.

## 2. Locked decisions

| # | Decision | Source |
|---|---|---|
| 1 | Design authority is `BUILD_MANUAL.md` (Science manual is current; the Biology-only "Cells" manual may be used for that one lesson only). **Where it conflicts with CLAUDE.md Branch Policy, OVERRIDES.md wins.** | Mark 2026-10-21 |
| 2 | **Footer text comes only from `config/attribution.yaml`**: `slide_footer` on every slide (`© {YEAR} SeaVuria and ARES Education · CC BY-NC 4.0`) + generated `[Subject] G10 · [SoW name] · Lesson #` + both logos; the full `lesson_footer` on the title slide and the last slide. Never hardcode credit text. The manual's own footer wording ("© 2026 …") is superseded. | Mark; `d3d2b875` |
| 3 | **ARES links go on the slides**, clickable in Slide Show, as an **icon** carrying the hyperlink (no visible long URL). Each icon needs alt text and a visible label; the plain URL goes in the speaker notes so printed copies keep it. Only `ares.local` links, taken from the lesson's `resourceLinks` in `_data.json`; every link passes `scripts/check_resource_links.py`; a failing link blocks the build. **No placeholders** (the manual's `REPLACE-WITH-REAL-ARES-LINK` is not used). Icon artwork: any icon for now, refined during testing. The manual's "never on student slides / hidden slide only" rule is superseded. | Mark 2026-10-21 |
| 4 | **Science errors, outdated terms and inconsistencies are flagged in the build log, never fixed in the deck.** Lesson-plan content changes only on `main`; the deck is then rebuilt from it. This overrides Manual Section 12 rows "Clear science error", "Inconsistent analogy…", "Outdated term…". Reason: prevent drift between decks and lesson plans. | Mark 2026-10-21 |
| 5 | **Output policy: decks and PDFs are gitignored and shared through Drive.** Only `data/outputs/presentations/_samples/` may be committed (small sample set). Never `git add -f` decks elsewhere. | Mark 2026-10-21; `75b4fad2` |
| 6 | Output location: `data/outputs/presentations/<Grade>/<Subject>/<SubStrand>/` (on the branch, gitignored). File name per Manual Section 4: `Subject_G10_SoWName_L#_Short_Title.pptx` (Subject = Bio, Chem or Phys). | Manual; WORKFLOW.md |
| 7 | **Lesson-plan content is read-only on this branch.** Source: the `_data.json` / `generators/data/*_data.js` on `main` as merged in. Never edit or regenerate lesson content here. | CLAUDE.md |
| 8 | **Never change shared pipeline files** (`generate_substrand.py`, `build_docs.js`, `generate.js`, the schema, `config/attribution.yaml`, `ares-contract.schema.json`) from this branch without a note in `STATUS_PRESENTATIONS.md` and Mark's approval. Control documents (CLAUDE.md, WORKFLOW.md, STATUS.md, attribution.yaml, schema) are edited only on `main`. | CLAUDE.md |
| 9 | Nothing from this branch is synced to teacher Drive folders until Mark approves it. | CLAUDE.md |
| 10 | One deck at a time with a build log; a teacher checks every deck before release (Manual Sections 2, 12, 14). Teacher review of the 4 example decks happens but **does not gate** the generator build for now. | Mark 2026-10-21 |
| 11 | Model: `claude-sonnet-5-5` minimum for any API call (project rule). Prefer batch mode where an API step exists. | CLAUDE.md |

## 3. Inputs the build reads

- **Lesson data** (per sub-strand, per lesson): `UNIT` (anchor phenomenon, driving question, titles, totalDuration), `LESSONS[n].framework` phases (`Predict Phase`, `Observe Phase`, `Explain Phase`, `Driving Question Board (DQB) Creation`, `Model Building Phase`: the contract enum), learner experience, teacher moves, sensemaking, formative assessment, `resourceLinks` (a slot may be `null`: see `docs/SCHEMA.md`), `SUMMARY_TABLE`, `FINAL_EXPLANATION`. Field documentation: `generators/data/SCHEMA.md`.
- **Quizzes** (`*_quiz.json`) carry `phase` + `placement`; the manual does not use them, so decks do not include quizzes unless Mark decides otherwise.
- **Lesson length:** the manual uses 40 min (single) or 80 min (double). Take it from the lesson data; if it is not explicit, flag it in the build log rather than guess.
- **Phase colours** (Manual Section 4): Predict 47C6E4, Observe D7DF23, Explain CF128C, Driving Question Board FCBA63, Model Building E44145. Slides write "Driving Question Board" in full; the data label stays exactly as in the contract.
- **Logos** (SeaVuria, ARES): not in the repo yet. **Mark must supply them** before the first real build.
- **Reference prototypes (not to build from):** `handoff_bundle_2026-09-29/presentation_examples_deferred/` (4 example decks/builders, pptxgenjs-based). `pptxgenjs` is already in `package.json`; reuse the approach, not the content.

## 4. Open questions (Mark / teachers; none block starting)

1. **Logos:** supply the two logo files and their allowed sizes.
2. **Lesson length source** in the data for 40 vs 80 minutes (verify; see §3).
3. **Safety slide, glance slide and practical detail:** the manual requires per-group materials, quantities and fallbacks. The lesson plans may not contain all of them. Policy proposed: take what exists, flag every gap in the build log, and **never invent** content (consistent with the manual's "do not invent an assessment").
4. **Formative-check placeholders:** allowed ("Formative check to be added" slide) but each is listed in the build log.
5. **General Science, Essential Mathematics, Core Mathematics, Mathematics:** no design guidance yet (Maths "has its own separate guidance", per the manual). Last in the queue.
6. **Manual rule vs the `Calibri` font:** the lesson docx files use Arial; decks use Calibri per the manual. Keep as is.
7. **Drive destination** for decks (and whether ARES upload is automated): to be added to the WORKFLOW.md Environment Reference **on `main`** once Mark decides.

## 5. Phased plan (pause and report between phases; Mark acknowledges each)

**Phase 0: Preconditions (no code)**
- `/restart` in the worktree, then `git merge main`. Confirm `.gitignore` ignores `data/outputs/presentations/*` except `_samples/`.
- Mark supplies logos (open question 1). Confirm the lesson-length source (open question 2).
- *Checkpoint report:* branch state, inputs present, open questions answered or deferred.

**Phase 1: Generator skeleton and golden fixture**
- Build the deck generator on the branch (pptxgenjs; reads lesson JSON and `config/attribution.yaml` via `generators/lib/attribution.js`; add reading of `slide_footer` there only after Mark's approval, since that is a shared file).
- Pick **one lesson** (the Biology Cells lesson Mark mentioned, or Bio SS2.1 L2, which has a prototype for comparison) and produce one deck.
- Commit a **golden fixture**: that deck's structural manifest (slide count and order, hidden flags, notes labels, footer text, link targets) as a small JSON in the branch, plus the deck itself in `_samples/`.
- *Checkpoint report:* the deck, the build log, manifest, and a list of manual rules the data could not satisfy.

**Phase 2: Validators wired into the build** (the build must be able to fail)
- Structure check against the manual: slide order (Section 5), slides 2 and 3 hidden, every slide has notes in the fixed label order, every student task has an ANSWER KEY, every "Check for understanding" slide has LOOK FOR and IF…, timings add up to exactly 40 or 80 minutes and match the TIME lines, Calibri throughout, footer and both logos on every slide, phase colours correct.
- Link check: every ARES link through `scripts/check_resource_links.py`; no placeholders; icon has alt text; URL in notes.
- Attribution check: footer strings equal the YAML output; no hardcoded credit text.
- Build-log check: every flagged item has lesson, slide, what the data says, what the deck does, why.
- Diff each build against the golden manifest for drift.
- *Checkpoint report:* validator results on the one deck; Mark approves scaling.

**Phase 3: One subject, then all science**
- Build Biology (9 sub-strands), report; then Chemistry (7), Physics (12). One lesson at a time with a build log each; stop at any validator failure.
- Teachers check decks using Manual Section 14; build logs go to the SoW owners (science corrections change lesson plans on `main`, never here).
- *Checkpoint report after each subject.*

**Phase 4: Distribution and merge**
- Mark approves; decks go to Drive per the (to-be-decided) destination; ARES upload is Mark's step.
- Merge back to `main` at a milestone per the Branch Policy: `git merge main` first; `scripts/check_resource_links.py`, `scripts/validate_corpus.js` and `scripts/run_lesson3_checks.sh` pass; Mark approves; then update the presentations row in `STATUS.md` on `main`.

**Later:** Mathematics / Core Mathematics / General Science / Essential Mathematics; Grade 11.

## 6. Known cautions

- **Never let a deck spoil a result** before students record it (comparison images and expected results go in Explain, never before Observe): Manual Sections 6 and 9.
- **Do not reorder lessons, add or cut activities, or change the anchor phenomenon.** The deck teaches the lesson plan; it does not redesign it (the golden rule).
- **The Grade 10 revision project is running in parallel** (`data/revised_2026-10_full/`, teachers reviewing). Until teachers sign off and `main`'s `generators/data` is updated, build decks from the **current `main` lesson data**, not the revised copy. After sign-off the decks need a rebuild from the updated data.
- **Existing lesson plans say "SeaVuria and ARES"; the YAML now says "…ARES Education"**: decks follow the YAML (Known Issues on `main`, 2026-10-21).
- The sandbox cannot read through the `data/ares_index` and `venv` symlinks from Claude Code; run resource-DB checks in a terminal if needed.
- Code-review-graph covers only `.js/.py/.sh` files, not the manual or markdown.
- Update `STATUS_PRESENTATIONS.md` (not `STATUS.md`) with `/update` on this branch; list any needed change to control documents as an open item for `main`.

## 7. Definition of done for the first milestone

One Grade 10 science lesson deck that (a) passes every Phase 2 validator, (b) has a complete build log, (c) has been checked by a teacher with Manual Section 14, (d) matches its golden manifest, (e) is in `_samples/`, and (f) Mark has approved scaling to the rest of the subject.
