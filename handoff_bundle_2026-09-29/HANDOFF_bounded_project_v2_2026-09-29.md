# Handoff — Grade 10 Bounded Project (v2): Link-Selection Fix + Quick Check Quizzes + Attribution, then Grade 11 Readiness
*Prepared 2026-09-29, for the Claude Code session on jhm-spark*

**This document supersedes** `HANDOFF_bounded_project_2026-09-26.md` and
the Phase 2/3 sections of `HANDOFF_grade10_regen_and_pipeline_2026-09-25.md`.
If either is in the repo, do not follow its presentation or quiz steps.
`HANDOFF_resource_link_quality_2026-09-25.md` remains valid and is
referenced below.

## What changed and why

- **Presentations are deferred.** Teaching staff are still reviewing the
  presentation design. Do not build `build_pptx.js` in this project.
- **Quizzes ship now, as standalone files.** Per lesson: a Quick Check deck
  (.pptx + .pdf) and a teacher Answer Key (.html + .pdf).
- **Attribution and licensing text is added to every output** (new requirement).
- **Grade 11 follows immediately**, so the project ends with a Grade 11
  readiness check.

## Scope decisions (confirmed by Mark, 2026-09-29)

1. **Do NOT regenerate lesson plan content.** No Claude API calls that
   rewrite lesson text, overviews, frameworks, Final Explanations or Summary
   Tables. The existing `_data.js` / `_data.json` lesson content stays as-is.
   This project only:
   - re-runs resource-link matching (local FTS5 lookup, not an API call),
   - generates new quiz content (the only new API cost),
   - re-renders the docx files (to pick up fixed links and attribution text).
   If anything in the code makes it hard to re-render without regenerating
   content, stop and report rather than working around it.
2. **Attribution year follows the current year** at generation time.
3. **"Answer sheet" means the teacher answer key.** A printable student
   answer slip is not in scope.

---

## Global objectives (apply to every phase)

1. **Fix the link-selection process, not just today's data.** The deliverable
   is a matcher that doesn't recreate the audit's problems on the next run,
   plus an automated check that catches regressions during generation.
2. **Generalize.** All new code is parameterized by grade and subject using
   the existing required `--grade` mechanism and grade-nested lookups from
   the Grade 11 prep work. No hardcoded "Grade 10", subject names, or
   STEM-only assumptions in new code paths. Test against Grade 10 only.
3. **Don't break the partner contract** (`ares-contract.schema.json`,
   validated by Lesson3). All additions are additive. Before writing quiz
   data anywhere, check whether the contract schema allows unknown
   properties (`additionalProperties`). If it is strict, store quiz data in
   a separate file (e.g. `<prefix>_quiz.json`) rather than inside
   `_data.json`. Attribution text is render-time only; do not add it to the
   JSON contract. Document any unavoidable contract impact in
   `PARTNER_CONTRACT_NOTES.md`.
4. **Know the cost before spending it.** A cost estimate is required before
   the full run (Phase 5).
5. **Design for the deferred presentations.** Each quiz question carries
   `phase` and `placement`, so a future presentation generator can insert
   questions inline without regenerating them.

---

## Reference materials in this bundle

| Path | What it is |
|---|---|
| `HANDOFF_resource_link_quality_2026-09-25.md` | Original link audit findings and required fixes |
| `resource_link_priority_targets.csv` | 233 flagged links in 3 confidence tiers |
| `audit_resource_links.py` | Audit script; baseline Tier 1/2/3 = 34 / 25 / 174 |
| `config/attribution.yaml` | **Single source of truth** for all attribution/licensing text |
| `samples/Attribution_Placement_Sample.docx` (+pdf) | Where the header block and per-lesson footer go in a lesson plan |
| `samples/quiz/` | Target output for 4 lessons (Biology, Physics, Chemistry, Mathematics): Quick Check .pptx/.pdf, Answer Key .html/.pdf, and the `_quiz.json` data each was built from |
| `samples/quiz/quiz_lib.js`, `build_quiz_samples.js` | How the samples were built (reference, not production code) |
| `presentation_examples_deferred/` | Full presentation examples under teacher review. **Reference only, do not build.** |

---

## PHASE 0 — Establish current state (Step 0)

Earlier handoffs may already have been partly executed on this server.
Before changing anything, report:
- `git log --oneline -15` and `git status`.
- Whether `DESIGN_link_selection_v2.md` exists, and whether any link-matcher
  changes have already been committed.
- Current output path convention for grade (e.g. whether `data/outputs/v2/`
  already has a grade segment from the `--grade` patch). Use that
  convention; do not invent a new one.
- Whether `ares-contract.schema.json` permits additional properties.
- Current STATUS.md Active Threads.

**Stop and report.** Do not redo work that is already done and approved.

## PHASE 1 — Link-selection redesign: design doc first

Follow `HANDOFF_resource_link_quality_2026-09-25.md`: diagnose root cause
for at least 3 Tier 2 examples (query built, DB results and ranks, why the
wrong result won). Then write `DESIGN_link_selection_v2.md` covering:
- the specific mechanism changes: at minimum an exam/answer-key exclusion
  (`answer|topical-test|kcse\s?\d{4}|exam` or a real content-type filter)
  and a minimum-relevance threshold that falls back to the ARES search link
  rather than forcing a poor match;
- a subject/domain guard (the Tier 2 cases are cross-subject leaks such as
  "Genetics vocabulary" in Mathematics);
- how recurrence is prevented: an automated check that runs inside the
  generation pipeline and fails or warns before a bad match ships;
- how "no confident match" is represented in the data and rendered in the
  docx (clearly, not as a weak link presented as a good one);
- how the design works for any grade and subject, including non-STEM.

**Stop for Mark's review of the design doc before implementing.**

## PHASE 2 — Implement and verify the link fix

Implement the approved design. Re-run matching for the Tier 1/2
sub-strands first, re-render their docx, re-run `audit_resource_links.py`,
and report before/after Tier 1/2/3 counts against 34 / 25 / 174. Also spot
check 10 Tier 3 rows by hand and report how many were real problems.

Also check link functionality: confirm each `direct_url` resolves to an
existing item in the ARES content DB (ids exist, not just well-formed).
Report any dead links.

**Stop and report.**

## PHASE 3 — Quiz generation and attribution rendering

### 3a. Quiz schema (per lesson)
```js
quiz: [
  {
    prompt: "string",          // self-contained question text
    choices: ["", "", "", ""], // exactly 4
    correctIndex: 0,           // 0-3
    rationale: "string",       // one or two sentences, teacher-facing
    phase: "observe",          // one of: predict | observe | explain | dqb | model | end
    placement: "string",       // the specific activity in THIS lesson's framework it follows
  },
]
```
Store per Global Objective 3 (inside `LESSONS[i].quiz` only if the contract
allows it; otherwise in a separate quiz file). Document in `SCHEMA.md`.

### 3b. Generation rules (enforce in the prompt AND in an automated validator)
- **5 to 10 questions per lesson**, multiple choice, exactly 4 options, one
  unambiguous correct answer.
- **Grounded only in that lesson's own content**: its `slo` and
  `framework` text. Never test content from a later lesson (no spoilers).
- **Anchor lessons** (typically Lesson 1, where the phenomenon is
  deliberately unresolved): a correct answer may be "this has not been
  explained yet", never a premature explanation.
- **Self-contained**: every question must include any numbers or context it
  needs. There is no presentation around it yet, so "the pallet leg" or
  "the shadow" without description is not acceptable. (The samples show
  two questions rewritten for exactly this reason.)
- **Distractors** should reflect real misconceptions, ideally the ones the
  lesson's `formativeAssessment` text names. No "all of the above" or
  "none of the above".
- **`placement` names a real activity from the lesson plan** (e.g.
  "Part B: shoe-pressure investigation"), so a teacher can find it in the
  docx. Do not reference slide names from the deferred presentations.
- **Show your working** in rationales for numeric questions, and verify
  the arithmetic programmatically where possible.
- Automated validator checks at minimum: count 5-10; 4 choices; no duplicate
  choices; `correctIndex` in range; valid `phase`; non-empty
  `placement`/`rationale`; banned phrases; correct-answer letter
  distribution across the whole corpus is not heavily skewed to one letter.
  The validator runs in the pipeline, like the link check.

Generate quiz content with one small API call per lesson (or batched),
reading the existing lesson content as input. Use the Batch API for the
full run. Checkpoint so it can resume.

### 3c. Quiz outputs (per lesson)
Match `samples/quiz/`:
- `..._L<n>_QuickCheck.pptx` and `.pdf`: title slide, one question per slide
  with a small "Use after: <phase>" teacher cue, closing slide with no
  assumed collection method. Printable as a paper quiz.
- `..._L<n>_AnswerKey.html` (for a second window while teaching) and `.pdf`
  (printable; generate via docx and LibreOffice, as the pipeline already
  does, because LibreOffice's HTML-to-PDF output is poor): quick marking
  grid, each question with its correct answer, rationale, and where it is
  used.
- Answers never appear in the student-facing deck, including speaker notes.
- Output alongside the sub-strand's existing outputs, in a `quiz/`
  subfolder, following the grade-aware path convention found in Phase 0.

### 3d. Attribution rendering
Read everything from `config/attribution.yaml`; never hardcode the text.
Replace `{YEAR}` with the current year at render time.
- **Top of every sub-strand document** (Lesson Sequence, Final Explanation,
  Summary Table): the full `substrand_header` block, in the document body,
  after the title. Not in Word's repeating page header.
- **After every lesson** in the Lesson Sequence: the `lesson_footer` line.
- **Quick Check deck title slide** and **bottom of each Answer Key**: the
  `lesson_footer` line.
- Render the license name as a hyperlink **and** print the URL visibly.
  Printed copies lose hyperlinks, and schools are offline.
- See `samples/Attribution_Placement_Sample.docx` for placement.
- Make sure existing docx generation still satisfies the partner contract
  checks after the attribution block is added.

**Stop and report** with rendered outputs for at least 4 lessons across 4
subjects, including at least one anchor lesson and one middle-of-sequence
lesson, plus validator results.

## PHASE 4 — Pilot and cost estimate

Run the full new pipeline (link matching, quiz generation, re-render with
attribution) on 2-3 sub-strands not used in Phase 3. Measure actual tokens.
Extrapolate the cost for all Grade 10 sub-strands in STATUS.md's existing
Cost Tracking table format. Also estimate the per-sub-strand quiz cost for
Grade 11 planning.

**Stop for Mark's confirmation before Phase 5.**

## PHASE 5 — Full Grade 10 run

Across all Grade 10 sub-strands: corrected links (skip re-matching if the
Phase 2 fix already ran on a sub-strand and nothing has changed since),
quiz generation, docx re-render with attribution, Quick Check and Answer
Key outputs. Lesson content is not regenerated.

## PHASE 6 — Verification

- `audit_resource_links.py` on the full corpus: final Tier 1/2/3 counts.
- Quiz validator across the full corpus: zero hard failures; report
  answer-letter distribution.
- Manual spot check of quiz quality (no spoilers, self-contained, correct
  answers) on at least 8 sub-strands spanning all subjects.
- Diff check: confirm lesson content in `_data.json` is unchanged apart from
  `resourceLinks` (and `quiz`, if stored there).
- Attribution present in every document, deck and answer key; the year
  renders correctly; no literal `{YEAR}`.
- `ares-contract.schema.json` validation passes.

**Stop and report.**

## PHASE 7 — Documentation

Update `SCHEMA.md`, `WORKFLOW.md`, `SYSTEM_OVERVIEW.md`, `CLAUDE.md`
(attribution config, quiz outputs, link check), and `STATUS.md` (Active
Threads and session log per the `/update` protocol). Write
`PARTNER_CONTRACT_NOTES.md`. Record in STATUS.md that presentations are
deferred pending teacher review, and where the examples live.

Sync outputs per the usual workflow (git; Drive sync script for docx/pdf).

## PHASE 8 — Grade 11 readiness (no bulk Grade 11 generation in this project)

Confirm the new pieces work for Grade 11 without code changes:
- Link matching, the link check, quiz generation, the quiz validator,
  attribution rendering and quiz outputs all run with `--grade 11`.
- Grade-nested lookups resolve Grade 11 values (Grade 11 reuses Grade 10
  strand numbers, so an un-nested lookup silently produces wrong content).
- Follow the existing Grade 11 plan: a **single Grade 11 Biology pilot**
  goes through the complete pipeline (lesson generation, link matching,
  quizzes, attribution) before any bulk Grade 11 run. Confirm the Grade 11
  curriculum text source (OCR'd from scanned PDFs) exists and is used.

**Stop and report** Grade 11 readiness, any gaps, and a Grade 11 cost
estimate. Bulk Grade 11 generation needs Mark's separate go-ahead.

---

## Deferred (explicitly out of scope)
- Presentation generation (`build_pptx.js`). Examples are in
  `presentation_examples_deferred/`; teacher feedback will shape it later.
- Response collection (paper for now; digital or clicker-based later).
- Student answer slips.
