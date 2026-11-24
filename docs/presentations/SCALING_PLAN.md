# Presentation scaling plan (DRAFT, 2026-11-21)

Status: draft for Mark's review. Nothing here has been run. Numbers come from the
pilot logs (`logs/deck_usage.jsonl`, 115 rows, $25.87) and from vendor prices
found by web search. Vendor prices are third-party data, not yet checked on the
vendors' own pages.

## Base recommendation

- Author decks with **Sonnet 5.5 through the Batch API**.
- Keep the Spark for pictures (Z-Image-Turbo) and advisory visual QA (Qwen3-VL), not for writing.
- Measured pilot cost: about $1.50 per lesson live, so about $0.75-0.85 on batch.
  Lesson count (re-derived 2026-11-21 from `data/outputs/v2/**/*_data.json`): **728 Grade 10 lessons**
  (Biology 90, Chemistry 67, Physics 101, Mathematics 126, Core Mathematics 112, Essential Mathematics 104,
  General Science 128) and 78 Grade 11 Biology lessons so far. Grade 10 on batch is therefore roughly
  $550-620 (derived: 728 x $0.75-0.85). The earlier "about 1,280 lessons" figure was not supported by the disk
  and is withdrawn; the full Grade 11 count is not known yet.
- Four lessons have a duration the 40/80 rule cannot read (corrected 2026-11-21: two are Grade 10, two are
  Grade 11 Biology): Essential Maths SS2.7 L8 ("3 x 40-minute lessons", Grade 10), Maths SS1.4 Congruence L2
  ("60 minutes", Grade 10), Biology SS2.3 Excretion in Plants L2 ("2 double lessons ...") and L5 ("120 minutes ...")
  (both Grade 11). They need a decision before a full run.
- Cost is dominated by output tokens (author A 54%, B 26%, review 18%, re-rate 1.5%).

## Phase 0 (needs Mark's approval before any spend)

1. Batch-round driver and content-hash incremental rebuild.
2. 4-lesson cost-lever test.
3. One Physics, one Chemistry and one Maths pilot lesson.
4. Quiz rendering (approach still to be chosen, see below).
5. **Head-to-head model test (added 2026-11-21, at Mark's request).**

### Head-to-head model test

Question: does a more expensive or different-vendor model reduce repair rounds
and teacher-visible errors enough to pay for itself?

| Arm | Model | Notes |
|---|---|---|
| A (control) | Claude Sonnet 5.5, effort high | Current pipeline, no change (measured pilot baseline: about $1.50 per lesson live) |
| B | Claude Opus 5.5, effort high | Same pipeline, no new integration |
| C | OpenAI GPT-6.1 Sol, reasoning effort High | Mark's choice of OpenAI model (2026-11-21), over GPT-5.5 and GPT-5.6 Sol. Needs a new adapter: structured-output schema, validator hooks, batch driver |

Reasoning tokens are billed as output, so Sol at High may cost more per lesson than
its list price suggests. Its real cost is an output of this test, not an assumption.

- **Lessons:** 4, across subjects (include one Maths and one Physics or Chemistry lesson).
  Use the same lessons and the same frozen lesson data for every arm.
- **Measure per arm:** total cost per passing deck, tokens in and out, repair rounds used,
  validator errors, layout errors, independent reviewer findings, and a teacher-visible
  error count from a blind read.
- **Cost:** about $10-15 of API spend (estimate), plus 3-4 days to build the OpenAI adapter.
- **Policy:** CLAUDE.md sets Sonnet 5.5 as the minimum for API calls. Arm C is an exception
  and needs Mark's explicit approval. Arms A and B are within the rule.
- **Prices to verify before running** on the vendors' own pages: GPT-6.1 Sol listed at
  $2 / $10 per million tokens (cache $0.10, higher tier over 272K prompt tokens;
  prompts here are about 40-50K). Batch discount for this model is unconfirmed.
  Opus 5.5 listed at $4 / $20.
- **Decision rule:** switch the base model only if an arm cuts cost per *passing* deck
  and does not raise teacher-visible errors. Otherwise keep Sonnet 5.5.
- **Also consider (cheap):** use GPT-6.1 Sol only as a cross-vendor science and fidelity
  reviewer. A different vendor makes different mistakes. Estimated about $0.17 per lesson
  at the review stage's token profile (about $120 across 728 Grade 10 lessons). Test this
  in the same run.

## Open decisions for Mark

- Approve Phase 0 (about $15-25 and 3-5 days before the head-to-head adapter work).
- Quiz approach: (1) markers only, (2) separate quiz generation with the deck rendering
  from the quiz JSON, or (3) fully integrated. Also how many inline questions per lesson.
  Quiz questions need stable IDs and answers for the response-capture project.
- Approve the OpenAI exception for arm C (GPT-6.1 Sol, High).

## Not yet decided or done

- Teacher check of the 12 pilot decks, PowerPoint and Presenter View check.
- Promotion of the Round 2 revised lesson data (pilot decks are provisional: the revision
  changes about 21% of Cell Structure text fields).
- Link gate passes only after `main` regenerates outputs to contract R1.

## Decisions recorded 2026-11-21 (Mark)

- Quizzes stay separate from deck generation. Exception: the deck carries an icon with an embedded link that opens the
  quiz for that phase at a logical point. Needs: the response-capture project's URL scheme, stable question IDs
  (the quiz JSON has none today), and quizzes for the lessons that have none yet (105 of 806 lessons on disk).
- Diagram templates must exist for every subject, not only Biology (all 19 current templates are cell biology plus
  levels of organisation). Approach and sizing to be agreed before mass generation.
- Grade 10 lesson lengths (Mark, 2026-11-21): Essential Maths SS2.7 L8 (3 x 40 minutes) is split into an
  80-minute and a 40-minute lesson; Maths SS1.4 Congruence L2 (60 minutes) is stretched to 80 minutes if feasible.
  Both are lesson-plan edits, so they are done on `main` (this branch does not edit lesson content) and merged in.
  Until then both lessons are excluded from generation. Grade 11 Biology SS2.3 L2 and L5 wait for Grade 11.
- Round 2 note: `main`'s Round 2 splits (4 Maths modules, 21 new lessons: 728 to 749) are not promoted yet, so
  the Grade 10 count will change when `main` promotes them; the incremental rebuild handles the changed lessons.

## Built 2026-11-21 (not committed)

- `scripts/deck_batch.py`: batch-round driver, incremental rebuild by input hash, `--engine openai`, and a background
  GPU worker that makes pictures while the next batches process (tested with a stub; the real GPU path is untested
  in the driver).
- `scripts/survey_diagrams.py`: one batch pass over lesson plans listing the figures each slide must show.
- `src/openai_engine.py`: OpenAI Responses + Batch client (standard library only).

## Diagram survey result and figure generators (2026-11-21)

Survey of all 728 Grade 10 lessons (Sonnet 5.5 batch, about $9.26): 716 lessons need at least one slide figure; 2,100
drawings in total. Biggest families: geometry 607, process/cycle flow 246, lab apparatus 212, cell/organism 202, data graph
170, atom/electron 145, coordinate grid 112. Reuse keys do not repeat (579 keys for 607 geometry drawings), so templates
are built per family with parameters, not per drawing.

Built (not committed): `generators/presentations/lib/figures.js`, five parametric families (geometry, grid, circuit,
atoms, flow/cycle), a `figure` block type (schema field `figure`, a JSON string), authoring rule 11b. The generators check
the spec: labelled lengths and angles against coordinates (when scale is "exact"), ammeter/voltmeter placement, electrons
against proton number and charge, and shapes inside the grid window. Errors go to the existing repair loop.
Not yet built: lab apparatus (hardest, each setup differs), data graphs and charts, force/motion, ray/wave, vectors,
number lines, bonding, structural formulae, periodic table views.
Not yet tested with a model authoring real lessons (needs a decision on further Phase 0 spend).

## Quiz link IDs (2026-11-21)

Provisional link format from the response-capture project: `http://ares.local/quiz/<quiz-id>/<version>/question/<question-id>`
(route not implemented; contract provisional). Built `scripts/quiz_links.py` and `data/quiz_registry.json`:
- quiz-id `<subject>-g<grade>-<substrand>-l<nn>` (for example `bio-g10-1-2-l01`); question-id `q01...`; version `v1...`.
- The registry (committed, owned by this branch because `main` owns the quiz JSON) keeps IDs stable: a question keeps its ID
  if its text is unchanged or only reworded (similar text); new questions get new numbers; retired IDs are never reused.
  The version bumps when wording, choices, choice order, correct answer or rationale changes; phase and placement do not.
- 105 quizzes, 776 questions registered: Grade 10 has only 27 (Biology 7, Core Maths 8, General Science 8, Physics 2,
  Chemistry 1, Maths 1); the other 78 are Grade 11 Biology. So quiz links can appear in only 27 of 728 Grade 10 lessons
  until quizzes are generated for the rest.
- `quiz_links.py slidemap` proposes a slide per question from the deck manifest (spread across the question's phase,
  flagged "confirm the transition"). Slide numbers move when a deck changes, so regenerate the list after each build.
- Not built: the link icon on slides.

## Triage of the 147 "other" survey drawings (2026-11-22)

147 of the 2,100 drawings (7%) were classed "other" by the survey. Re-read with whole-word matching (a first pass matched "ion" inside "action" and "section" and was discarded): 38 are students' own cumulative model sketches, about 30 blank grids or tables, 17 concept maps or organisers, 34 unclassified single items (clock-hand sequences, number grids), 9 particle or atom models, 9 scene or object sketches, 7 nested-set or Venn diagrams, 3 scale sketches. No single family is large enough to justify a generator. Handling: blank grids and tables use the existing `table` block; concept maps use the `flow` family (labelled arrows are supported); students' own cumulative models stay text prompts on the slide (the model is drawn on paper); particle models and Venn diagrams wait until a real lesson needs them.

## Further figure families built (2026-11-22, not yet used by a model)

- `apparatus`: 13 bench parts with checks (sealed vessel over a flame, burner heating nothing, thermometer in no liquid, tube without a stopper, overlaps, wrong support). 3 setups rendered; 9 error cases caught.
- `graph`: line, scatter (with least-squares best-fit line) and bar charts. Checks: every axis label carries a unit in brackets, points inside the axes, joined lines have increasing x, best fit needs 3+ points and stays on the chart, at most 20 ticks. `hide_points` draws empty axes for students to plot. 5 charts rendered; 6 error cases caught.
- `forces`: free-body diagrams with arrows in proportion to the values. A diagram marked balanced must add to zero and one marked unbalanced must not. 3 rendered; 5 error cases caught.
- Bug found and fixed in `drawFigure`: float noise (`cos 270 deg = -1.8e-16`) flipped downward vertical arrows. Vertical and horizontal lines are now snapped.
- Still not built: ray and wave diagrams, vectors, number lines, statistics charts beyond bar charts, bonding, structural formulae, periodic table views.

## Remaining figure families built (2026-11-23, not yet used by a model)

- `waves` (transverse and longitudinal; v = f x wavelength checked), `rays` (reflection, refraction with Snell's law and total internal reflection, convex and concave lenses with the image computed from the lens equation), `numberline` (points, intervals with open and closed ends, jumps), `molecule` (structural formulae; every atom's valency and the formula are checked), `periodic` (first 20 or 36 elements with highlighted groups, periods or elements).
- Rendered 13 test figures and viewed them; 11 error cases are caught (reflection angle mismatch, refraction angle wrong, total internal reflection with a refracted angle, object at the focal point, wrong image distance, v = f x lambda mismatch, crest on a longitudinal wave, point off the line, wrong valency, formula mismatch, element outside the table).
- Still not built: vectors beyond the grid family, statistics charts beyond bar charts (histogram, box plot, pie), dot-and-cross bonding diagrams, cell and organism drawings beyond the existing templates.

## Quiz <-> deck contract (2026-11-23)

Drafted `docs/presentations/QUIZ_DECK_CONTRACT.md` and added `scripts/quiz_links.py check` (quiz vs lesson plan: lesson number, title, phase, placement, self-containment). All 105 existing quizzes pass. Roughly 10 quizzes are being rebuilt on `main`; the registry is rebuilt from scratch after that, before any deck with links is distributed.
