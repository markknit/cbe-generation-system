# STATUS — Presentations branch

*Last updated: 2026-10-22*

The status file for the `presentations` branch (worktree
`/home/markk/ares/cbe-presentations`). For lesson-plan state, see
`STATUS.md` on `main`. The rules are in CLAUDE.md, "Branch Policy —
`presentations`".

## Active Threads

| Thread | Status | Notes |
|---|---|---|
| Branch + worktree setup | Done 2026-10-20 | Created from `main` at `805f9738`, pushed to `origin/presentations`; symlinks + `npm install` done; Step 0 passes in the worktree. Each session: `/restart`, then `git merge main`. |
| Teacher review of example decks | In progress; no longer gates the generator build (Mark 2026-10-21) | 4 examples in `handoff_bundle_2026-09-29/presentation_examples_deferred/` (Bio L2, Chem L4, Maths L4, Physics L2). Generator design waits on this feedback. |
| Presentation HANDOFF + initiation prompt | **Drafted 2026-10-21** (`HANDOFF_presentations_2026-10-21.md`); Mark to review | Locked decisions, open questions (logos, ~~lesson-length source~~ answered 2026-10-22, Drive destination), phased plan (Phase 0 preconditions to Phase 4 distribution). First build session starts at Phase 0. Lesson-length section updated 2026-10-22 (`e550bbc3`). |
| **Pilot: Bio 1.1 Cell Structure, all 12 lessons (Phase 1 -> sub-strand)** | **BUILT 2026-10-22; awaiting Mark's review, then a teacher check (Manual s14) of every deck.** 12/12: 0 layout errors, 0 validator errors, link gate 0, Spark vision reader 0 FAIL on about 300 slides. 2 automated-review majors left on L9 (SoW overruns the lesson length) and L8 hand-fixed. | Decks (gitignored) in `data/outputs/presentations/Grade10/Biology/SS1.1_Cell_Structure/`; specs, build logs, golden manifests, `BUILD_LOG_REPORT.md` (flags for teachers/lesson owners) in `data/presentations_specs/Biology/SS1.1_Cell_Structure/`; pictures in `data/presentations_art/final/`. Sample in `_samples/` is L2. Committed locally 2026-10-22 (not pushed). |
| SeaVuria Build Manual in repo | Committed 2026-10-20 (design input only; not signed off) | `docs/presentations/BUILD_MANUAL.md` (+ `.docx` source) and `OVERRIDES.md` (draft; where the manual conflicts with CLAUDE.md Branch Policy, the overrides win). Science manual is current (Mark, 2026-10-21); the Biology-only "Cells" manual may be used for that one lesson only. `main`'s CLAUDE.md points here. |
| Manual vs branch-rule conflicts | **Decided 2026-10-21 (Mark); recorded in OVERRIDES.md** | Footer: `config/attribution.yaml` is the guide (`slide_footer` added on `main` 2026-10-21; YAML now says "ARES Education"). ARES links: on the slide as a clickable icon, not a visible URL. Science errors: flag in the build log, fix only on `main`. Maths: processed last, probably no separate process. Still open: icon design, `slide_footer`, teacher review. |
| Output commit policy | **Decided 2026-10-21 (Mark):** decks/PDFs gitignored, shared via Drive; only `data/outputs/presentations/_samples/` committed | Applied on `main` (`75b4fad2`: CLAUDE.md, `.gitignore`, WORKFLOW.md). Drive destination for decks still to be decided and added on `main`. |
| Phase 0 preconditions (HANDOFF §5) | **Done 2026-10-22** except Mark's HANDOFF review: logos in `data/logos/` (checked: both PNGs opaque, white background, usable on a light footer band; ARES copy trimmed for equal visual weight); lesson length rule decided; Spark vision QA reader installed | See pilot row. |
| Needed change on `main` (not editable here) | **Open** | `CLAUDE.md` lines 258–259 still say presentations are deferred, "don't build it", contradicting Branch Policy. Fix on `main`, then merge in. |

## Known Issues / Lessons Learned

- **(2026-10-22) `UNIT.totalDuration` is not a usable lesson-length source.** It assumes 40 minutes per lesson and disagrees with the lessons in 11 of 28 Bio/Chem/Phys modules (e.g. `bio_1_1`: lessons sum 840 min, field says 480). **Structural fix:** the build reads per-lesson `duration` only, and the Phase 2 validator should also check that the slide timings equal that figure.

## Session Log

## Updates — 2026-10-20 — branch created
- Created `presentations` from `main` at `805f9738`, as a worktree at
  `../cbe-presentations`. Symlinked `data/ares_index` and `venv`; ran
  `npm install`.
- Still open: teacher review; HANDOFF; output commit policy.

## Updates — 2026-10-20 — build manual added
- Reviewed (by Claude.ai) the SeaVuria Science Lesson PowerPoint Build Manual v1.0 and the Biology-only Cells manual (Cells appears to be the earlier pilot-based version; Mark to confirm which is newer).
- Committed `docs/presentations/BUILD_MANUAL.md` (three raw-HTML callout tables converted to blockquotes), `OVERRIDES.md` (draft) and the Science manual `.docx`. CLAUDE.md pointer line added on `main` (`7714362c`) and merged here.
- Found: `origin/main` had a CLAUDE.md commit by Mark (`1c0e85d4`) with a truncated "Design Spes" sentence; left untouched, rebased on top of it.
- Still open: teacher review of the 4 example decks; Mark's decisions on OVERRIDES conflicts; Claude.ai project upload swap (Mark); finish/reconcile the CLAUDE.md design-spec line.

## Updates — 2026-10-21 — design-spec files tidied
- Mark confirmed: Science manual is current; Cells manual only for that lesson. Claude.ai is current.
- Mark's loose copies in `docs/` (`SeaVuria_..._Manual.docx` identical to the committed one; `.md` a rougher conversion) deleted; `docs/presentations/BUILD_MANUAL.md` is the single markdown copy.
- CLAUDE.md on `main` now has one design-spec statement naming the repo paths (`fe186afb`); merged here.
- Still open: Mark's decisions on OVERRIDES.md (footer attribution, link placement); teacher review of the 4 example decks; HANDOFF; output commit policy.

## Updates — 2026-10-21 — OVERRIDES decisions recorded
- Mark's decisions applied to `docs/presentations/OVERRIDES.md` rows 1, 2, 4, 6 (see Active Threads). Footer comparison done: manual vs YAML differ in year, "ARES Education" wording, URL, KICD line, AI credit.
- `slide_footer` added on `main` (`attribution.yaml`); "ARES Education" now in all three YAML lines. Generator must read the key (not built yet). Still open: icon design; teacher review of the 4 example decks; HANDOFF; output commit policy.

## Updates — 2026-10-21 (second entry) — answers from Mark
- Icon design: any icon for now, refined during testing. Teacher review of the 4 example decks does not gate work for now. Copyright wording "SeaVuria and ARES Education" agreed by Mark.
- Still open: presentation HANDOFF; output commit policy.

## Updates — 2026-10-21 (third entry) — output policy adopted, HANDOFF drafted
- Output policy adopted on `main` (`75b4fad2`); merged here. Final HANDOFF drafted: `HANDOFF_presentations_2026-10-21.md` (needs Mark's review).
- Still open: logos (Mark to supply); lesson-length source check; Drive destination for decks (WORKFLOW.md on `main`); Mark's review of the HANDOFF; Maths/Core Maths/Gen Sci/Ess Maths guidance.

## Updates — 2026-10-21 (fourth entry) — claude.ai project instructions refreshed
- Mark's claude.ai project instructions were still the original draft (stray header, three-file fetch list). Corrected text saved as `docs/presentations/PROJECT_INSTRUCTIONS_claude_ai.md` (fetch list now six files incl. HANDOFF, OVERRIDES, BUILD_MANUAL; standing rules match today's decisions). Mark to paste it into the project instructions; claude.ai skills already updated by Mark.
- Still open: Mark pastes the new instructions; logos; lesson-length source; Drive destination for decks.

## Updates — 2026-10-21 (fifth entry) — setup closed out
- Mark updated the claude.ai skills and project instructions; toolkit repo skills verified identical to the repo's. Setup (branch, design spec, overrides, HANDOFF, output policy, tooling sync) is complete; generator build not started.
- Next session: `/restart`, `git merge main`, then HANDOFF Phase 0 (logos, lesson-length source, HANDOFF review).
- Still open: logos (Mark); Drive destination for decks; Maths/Core Maths/Gen Sci/Ess Maths guidance.


## Updates — 2026-10-22 — Phase 0: lesson-length source checked; header fixed
- Header date corrected (was 2026-10-20). `/restart` passed first: 0 behind `main`, clean, control docs identical to `main`.
- **Lesson-length source (HANDOFF open question 2): found, usable with a rule.** Each lesson has `LESSONS[n].duration` (required by `ares-contract.schema.json`, type string). Surveyed all Bio/Chem/Phys `generators/data/*_data.js` (28 modules, 258 lessons): 168 are plain "40 minutes" (57) / "80 minutes" (111); every one of the 258 leads with 40 or 80 minutes (0 unparsable), but 66 carry free-text qualifiers (e.g. "80 minutes (2 x 40-minute periods)", "2 lessons (80 minutes)", "40 minutes (… double period of 80 if the practical is done in full)").
  - **Ambiguous: 24 lessons** say 40 minutes but allow an 80-minute double period as an option (phys_2_1, phys_3_2, phys_3_3, phys_3_4, phys_1_4, chem_1_1, chem_1_3, bio_1_2 L2). Rule (confirmed by Mark, next entry): the leading figure is the deck's length; the option goes in the build log. One lesson, chem_1_3 L4, also gives per-phase minutes inside the string.
  - Note "2 lessons (80 minutes)" (bio_3_2 L7–10, phys_4_1 L5, phys_4_2 L5) leads with "2 lessons", so the parser must read the minutes figure, not the first number.
- **`UNIT.totalDuration` is NOT reliable** (11 of 28 modules, e.g. bio_1_1: lessons sum 840 min, totalDuration says 480; phys_1_2: 400 vs 240). It assumes 40 minutes per lesson. Don't use it; use per-lesson `duration`.
- Committed and pushed as `e9f0c0b3`. The rule was confirmed by Mark in the next entry. For `main` (not edited here): CLAUDE.md lines 258–259 still say presentations are deferred/"don't build it", contradicting the Branch Policy.

## Updates — 2026-10-22 (second entry) — Mark's decision: lesson-length rule
- **Decided (Mark):** the leading 40/80 figure in each lesson's `duration` string is the deck length; optional double-period extensions (24 lessons) are noted in the build log only. HANDOFF §3 and open question 2 updated to match.
- Phase 0 still open: logos (Mark); HANDOFF review; Drive destination; Maths guidance.

## Updates — 2026-10-22 (third entry, `/update`) — Phase 0 progress recorded
- Verified from disk: branch `presentations`, 0 behind `main`, == origin at `e550bbc3`, working tree clean before this edit. Commits this session: `e9f0c0b3` (lesson-length survey, header), `e550bbc3` (Mark's 40/80 rule in HANDOFF §3 and Q2). No generator code, no lesson data, no shared pipeline files touched; nothing generated.
- Active Threads: added "Phase 0 preconditions" and "Needed change on `main`" rows; HANDOFF row notes corrected. Known Issues: `UNIT.totalDuration` entry.
- Checked, don't redo: duration survey (28 modules; re-run only if `generators/data` changes on `main`). Not checked: `data/ares_index` / `venv` symlinks (sandbox-blocked).
- Still open: logos (Mark); HANDOFF review (Mark); Drive destination for decks (add to WORKFLOW.md on `main`); Maths/Core Maths/Gen Sci/Ess Maths guidance; CLAUDE.md lines 258–259 fix on `main`.

## Updates — 2026-10-22 (fourth entry) — Pilot deck L2 built (path C), generator + validators + Spark QA in place
- **Decisions (Mark):** path C (Claude Code builds the generator; Sonnet 5.5 authors via API; Spark renders/QAs); start with `bio_1_1` L2; read `attribution.yaml` directly (shared `attribution.js` untouched); fix same-class issues and report at the end; Spark QA included now; reference templates in `data/Presentations-templates/` stay untracked.
- **Built (new files only, no shared pipeline file touched):** `generators/presentations/` (`build_deck.js`, `lib/{theme,measure,blocks,diagrams,attr,resources,unit}.js`, icons, trimmed ARES logo), `src/generate_deck.py` + `src/deck_spec_schema.py` (2-call structured authoring: A = slides, B = surrounding slides; author -> build -> validate -> independent review -> bounded repair), `scripts/validate_deck.js` (re-reads the .pptx), `config/deck_generation.yaml`, `config/deck_spec.schema.json`, `scripts/qa_slides_vlm.py` (Spark reader, written by a subagent). `OVERRIDES.md` row 16 corrected (review no longer gates).
- **Spark:** Qwen3-VL-32B on llama.cpp (`/home/markk/vlm-qa`, port 8090; `start_server.sh` / `stop_server.sh`). Measured by the subagent on 30 planted defects: logos 6/6, low contrast 6/6, clipped 4/6, overlap 4/6, 1/18 false positives; ~8 s/slide at 4 parallel. ADVISORY only. Carlito (Calibri-metric) font installed in `~/.fonts/carlito` for rendering and for exact text-fit measurement.
- **Result L2 vs reference L2 (same extraction on both):** slides 28 vs 21 (2 hidden each); notes 6,082 vs 3,248 words; checks with LOOK FOR/IF 11/11 vs 5/2 of the labels; footer text from the YAML (reference hard-codes it), 'Driving Question Board' spelled out, min text 10 pt (footer) vs 4 pt. Remaining weaknesses vs reference: plainer visuals (no kitchen/analogy graphic), card sort shows only the 6 cards the SoW names (reference invented 12).
- **Cost (estimated from token usage, $4.66 in total for this L2, 20 calls):** about $1.0 for a clean author+review pass, $1.6 with a repair round. Most of the $4.66 was repair loops caused by my own validator/layout bugs (placeholder regex matched 'fill'; the driving-question blob; glance overflow; repair feedback never reached Part B). **My earlier $3-5 estimate for the 12-lesson pilot was too low: expect about $12-20.** Logs: `logs/deck_usage.jsonl` (untracked).
- **Lessons:** (1) structured-output grammar limit: the full spec was rejected as 'too large'; split into two calls and collapsed the fixed-slide notes. (2) A validator bug looks like a model failure and triggers paid repair loops: run the free rebuild-from-saved-spec path first (`--spec`, `--reuse-a`). (3) The reviewer made one wrong claim (said US spelling is required); its prompt now forbids it. (4) `UNIT.drivingQuestion` in lesson data is a blob (driving question + KICD inquiry questions); slides use `lib/unit.js` to extract the quoted question. (5) Do not run `rm -rf *` after a `cd` in this repo: the safety check (rightly) blocked it.
- **Flags for `main`/lesson owners (from the build log, not fixed in the deck):** `UNIT.substrand` says 'Sub-Strand 1.3' while META says 1.1; unit text says 'Form 1 student' (should be Grade 10); platelets treated as cells in Lesson 2 text; the lesson's own mapping 'jiko boundary = membrane' vs 'door = membrane' is inconsistent; 'RED = plant eukaryotes only' conflicts with the bacterial cell wall; SoW activity times add up to about 89 minutes in an 80-minute lesson.
- Still open: Mark's review of the L2 deck and the questions in this session's report; scaling to the other 11 lessons; HANDOFF review; Drive destination; Maths guidance; CLAUDE.md lines 258-259 fix on `main`.

## Updates — 2026-10-22 (fifth entry) — design v2, art pipeline, local-model experiment
- **Design v2 (Mark: richer graphics, engaging for students):** icon library (`generators/presentations/assets/emoji`, 115 Noto Color Emoji, Apache-2.0, fetched by `fetch_icons.py`), blocks v2 (speech-bubble questions, numbered badges, icon rows, tiles, diagram split layout, illustration split layout), phase icon badges + soft backdrops, title-slide hero, summary icons. 16 new diagram templates in `diagrams_specialised.js` (agent-drawn, checked by me; `levels_of_organisation` reworked as a horizontal row with captions). Science points for a teacher to check: xylem drawn with lignin rings (real vessels often spiral/reticulate), phloem sieve plate detail, guard-cell nuclei, egg 'protective jelly coat' (human: zona pellucida), mixed muscle types in the levels example.
- **Art pipeline:** `scripts/gen_art.py` + `pick_art.py` (agent-written; Z-Image-Turbo, Apache-2.0, ~17 s/image, 24 GB; picker is a filter, not a ranker: its choice was in the author's acceptable set 6/6 but matched the favourite 4/6) and `scripts/make_art.py` (generates missing ids under a GPU lock, square 1024, rounded corners, catalogue with prompts/seeds). People come out looking about 10 years old, so prompts prefer objects/scenes and use people only for Amina. Every picture needs a human look before release (text/gibberish can appear on books/boards).
- **Sub-strand driver:** `scripts/generate_substrand_decks.py` (lesson 1 alone first, rest parallel; logs in `logs/deck_runs/`).
- **Local-model experiment (Mark asked: can the Spark replace the API?). Part B of L2, same prompt/schema/Part A:** Qwen3-VL-32B: 19 min (5.4 tok/s), 5 validator problems (6 of 12 unit-map titles, 'DQB' on a slide, two overflows), long unplain definitions that give away the three tenets, summary prompts copied from the teacher text, 50 build-log items (Sonnet 25, mostly filler). Qwen3-VL-30B-A3B: 3.5 min (30 tok/s), 3 problems, same plain-English and filler problems, but correct 12 unit-map titles. **Conclusion: not good enough for student-facing text; saving would be ~$0.2 of ~$1.7 per lesson. Keep Sonnet 5.5 for authoring and review. Local models remain useful for pictures and visual QA.** Details: `logs/exp_partb_*.json` (untracked).
- **Costs:** L2 total about $9.4 in API spend this session (several failed or repaired runs; $0.56 lost to a 48K max_tokens stop, now 80K); a clean pass is about $1.7 (author A $0.45-0.65, B $0.21, review $0.17-0.21, plus repair rounds).
- **Lessons:** (1) a background wrapper's `exit` echo is not the command's exit code: use `rc=$?; exit $rc`. (2) A reviewer must be told fidelity beats spoilers when the SoW itself leaks a result, or it forces unfaithful repairs. (3) Reserve a separate hidden slide when content cannot fit one; do not rely on the model obeying size limits. (4) Never `rm -rf *` after a `cd` here (blocked, rightly).
- Still open: Mark's review of the L2 deck and the whole sub-strand when done; commit/push (staged, not committed: Mark has not answered); logos are committed in `data/logos/`; HANDOFF review; Drive destination for decks; Maths guidance; CLAUDE.md lines 258-259 fix on `main`.

## Updates — 2026-10-22 (sixth entry) — all 12 Cell Structure decks built
- Ran L1 and L6 first (anchor + practical), fixed what they showed (hero-picture reuse rule, title-slide overlap, memory check in `gen_art.py` that ignored reclaimable cache, art-failure exit code), then L3-L12 three at a time. Batch cost about $14.0 for L3-L12; L1 $0.61, L6 $0.78, L2 $1.72 (final runs).
- Fixed after the batch (all free, no API): diagram-fit rule that rejected wide drawings (L10), tighter-spacing fallback and 16 pt floor for comparison boxes, five tiles on one row (L3, L9), reviewer told that manual-required elements (DQB vote, etc.) are not 'invented'. Hand edits logged in the build logs: L8 Predict slide now shows the five-cell picture; L10 goal 1 no longer states the Predict answer; L3 hero replaced (it showed the size comparison students predict).
- **Comparison with the references (L1, L2, L6):** notes 5,101/6,351/5,833 words vs 2,759/3,248/2,881; LOOK FOR on 15/22/17 slides vs 8/12/8; IF... on 15/22/17 vs 2/2/2; answer keys 6/12/14 vs 1/7/2; median text 16-18 pt vs 14; smallest text 10 pt (footer) vs 4-6 pt; footer text from the YAML.
- **For the lesson owners (see `BUILD_LOG_REPORT.md`):** 20 possible science errors, 17 term flags, 44 inconsistencies, 13 plan problems, 8 safety points, 9 trimmed-time notes, 20 added facts/cards to verify, 63 missing details. **L9's lesson plan holds about 100 minutes of activity in an 80-minute lesson** (each cell gets half the SoW time).
- **Costs, whole pilot (all calls incl. failed/repaired runs, estimated from tokens):** see `logs/deck_usage.jsonl` (untracked).
- Still open: Mark's review; teacher check of all 12 decks (science, practical feasibility, timings); commit/push (staged, Mark has not answered); Drive destination; Maths and other subjects; HANDOFF review; CLAUDE.md lines 258-259 on `main`; pictures need a human look (people look young; text can appear).

## Updates — 2026-10-22 (seventh entry) — resource labels fixed; deck size fixed; pilot committed
- **Mark's review of all 12 slides:** graphics and layout approved. His question: why 'Do not use' on most ARES resources? Measured: 59 of 89 do-not-use, 30 preview-first, 0 best-match. Cause: the lesson plans' matcher attaches resources by topic to phase slots without knowing lesson order, and the 3-level scale had no 'good, but later' option. **Fix:** 4-level scale (best match / preview first / **use later** with when / do not use only for off-topic or wrong level), new authoring rule 10, `scripts/rerate_resources.py` (one small call per lesson, $0.38 for all 12; previous ratings in `logs/rerate/`). Result: do-not-use 59 -> 4, use-later 48, preview-first 31, best-match 6. The hidden resources slide now shows tag, reason and when to use; links stay clickable for everything except do-not-use.
- **Deck size:** pptxgenjs embeds one copy of an image per use (logos on every slide): decks were ~12 MB. `build_deck.js` now de-duplicates identical media and the ARES logo is downscaled: 2-3 MB per deck, 27 MB for 12. Note: a full grade is still about 2 GB (pictures), above the ~1 GB the output policy assumed; pictures could be shrunk if needed.
- **Estimates given to Mark:** mean $1.5 per lesson (range $0.6-2.3, includes repairs and independent review): rest of Grade 10 Biology (78 lessons) about $115; Biology+Chemistry+Physics (246) about $370; all seven Grade 10 subjects (716) about $1,075; roughly half with the batch API (not built for decks yet). Whole pilot spend to date: about $25.9 (104 calls, includes every failed/repaired run).
- **Open question Mark asked: wait for the teachers' revision?** Recommendation recorded: yes, hold scaling to new sub-strands until the Grade 10 revision is signed off. Measured: the proposed revisions change 20.6% of the text fields of Cell Structure (104 of 504, in every lesson); decks built now are provisional and must be rebuilt from the signed-off data (`--data` path) and re-checked. Meanwhile: teacher review of the 12 pilot decks for design/format, batch mode, more diagram templates, share `BUILD_LOG_REPORT.md` with the teachers.
- Still open: PowerPoint (not just LibreOffice) check incl. Presenter View; human look at the 19 pictures; L9 plan holds about 100 minutes in an 80-minute lesson (SoW owner); Drive destination; Maths/other subjects; HANDOFF review; CLAUDE.md lines 258-259 on `main`; push (Mark asked for a commit only).
