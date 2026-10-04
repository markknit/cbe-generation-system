# Generation Status — Kenya CBE Grade 10 Lesson Plans

*Last updated: 2026-10-01*

---

## How this file is used — read this first

This file is the **single source of truth for project continuity** across
sessions, tools, and resets (Claude.ai, Claude Code, or a fresh person
picking this up cold). If you're starting a new session, **read the
Active Threads table below before doing anything else** — do not assume
you know current state from memory, training data, or a prior
conversation's summary.

**When this file gets updated — not optional, not "when convenient":**
- As part of finishing any real unit of work (a fix, a migration, a
  decision) — updating Active Threads and appending a session-log entry
  is part of what "done" means for that task, not a separate step to
  remember afterward.
- On demand, via the `/update` skill (Claude Code: `.claude/skills/update/`)
  or by typing `/update` in a Claude.ai session in this project — forces
  an update right now, e.g. at the end of a day, before a server reset,
  or before switching tools, so nothing is lost between sessions.

**Before trusting this file, re-verify it — don't just read it:** the
`/restart` skill (Claude Code: `.claude/skills/restart/`) or typing
`/restart` in a Claude.ai session re-reads this file plus `CLAUDE.md`
(and, in Claude Code, runs `WORKFLOW.md`'s Step 0 live checks) and
reports any drift before continuing. `/update` is the write side of
continuity; `/restart` is the read/verify side — use it at the start of
a work day or any time something feels stale.

**Why this exists:** this project has had multiple documented incidents
(see "Known Issues / Lessons Learned" below) where a fact was true when
written and silently went stale because nothing forced a re-check.
Continuity information is exactly as vulnerable to this as any other
fact — arguably more so, since "what's currently in progress" changes
every session. This file's job is to make "what's actually going on
right now" checkable in one place, not reconstructed from memory.

---

## Active Threads

| Item | Status | Notes |
|---|---|---|
| **Partner validator findings on Core Mathematics 2.9 (2026-10-03)** — Summary Table / Final Explanation not in sync with lessons | **Fixed in code and data; awaiting human review of flagged Final Explanations, lesson-drift decision, PDF rebuild. Do not distribute yet.** | Done: Summary Tables derived from lessons (95/95); Final Explanation rebuilt after lessons with reviewer: **42 clean, 44 written but flagged `needs_review`** (best attempt, 143 residual findings across the 53 flagged); student + teacher-key docs; validator wired into `generate.js` (blocks flagged modules until `rebuild_consistency.py --clear MODULE --by NAME`); T3/T4 link rules; link judge pass 1 applied; all 95 re-rendered. **Open:** (1) **9 Physics modules** (`phys_1_4 1_5 2_1 3_1 3_2 3_3 3_4 4_1 4_2`) still have the OLD Final Explanation: their calls hit *credit balance too low*; rerun `python3 scripts/rebuild_consistency.py --final-explanations --only <those>` (~$3). (2) **Link judge pass 2** for the ~535 replacement links: `python3 scripts/judge_links.py`, then `node generators/generate.js --all`, repeat to 0 new (~$1). (3) Review the 53 flagged Final Explanations (`logs/final_explanation_issues/`). (4) Lesson drift (below). (5) Rebuild PDFs + index (`generate_pdfs.js`, `generate_teacher_index.js`) once the above settle. Backup: `/home/markk/ares/backups/cbe_outputs_2026-10-03_pre-consistency-fix_c8f9e49.tar.gz`. |
| **Lesson-sequence drift (lessons contradict each other)** | **Measured 2026-10-03; decision needed** | `logs/lesson_drift/SUMMARY.md`: reviewer found at least one MAJOR contradiction in **91 of 95** sub-strands (mean 2.7 major each; severity labels are the reviewer's and generous; spot checks looked real: wrong cross-references such as "in Lesson 2 they added Heron's formula" when Lesson 2 teaches the sine rule, and one plot with four different sets of dimensions). Not fixed. Options: fix cross-references/datasets per sub-strand, regenerate worst sub-strands with a shared fact sheet, or accept and tell teachers. Cause: parallel batch generation, no shared dataset. |
| Attribution wording per partner review | **Recommendations written, nothing applied** | `ATTRIBUTION_RECOMMENDATIONS_2026-10-03.md`. Needs Mark: entity names/jurisdictions/numbers, © holder wording, placement choice, legal review. |
| `ares.local` mDNS alias + nginx `server_name` fix | Done (jhm-spark + tsavo3 test server) | Verified: `ping ares.local` resolves; nginx reload succeeded |
| `resourceLinks` field in JSON export | Done — but the counts below were superseded twice | The field itself is fine. The old note here ("126 JSON files, 13,440 `ares.local` URLs, 0 remaining `ares.edu`") was true at `5071ea4` and went stale twice over: the corpus is now **85 files / 25,480 `ares.local` URLs**, and in between, every one of those URLs had silently reverted to `ares.edu` — see the row below. |
| Full corpus regeneration (`ARES_HOST=ares.local`) | **Was reverted 2026-07-30, restored 2026-08-02 (`9b33dce`)** | `5071ea4` did the migration correctly. `f6d6fab`'s `generate.js --all` then silently reverted it corpus-wide, because `src/ares_recommender.py` still **defaulted** `ARES_HOST` to `ares.edu` and `generate.js` shells out to that module. Root cause now fixed: the default is `ares.local`, with WORKFLOW.md Step 6 warning + a new Step 6c verification grep. Current state verified: **0 `ares.edu`**, 25,480 `ares.local` URLs across 85 JSON exports, 14,560 `ares.local` hyperlinks across the 85 Lesson Sequence docx, PDFs spot-checked clean. |
| Provisioning script for ~100 school servers (`install.sh`) | **Written + committed 2026-08-02 (`b913eb5`) — still not tested live** | Was recorded here as "Built" since 2026-07-05 but **did not exist** on jhm-spark, in git, or in any zip on this box — same failure as `sync_to_drive.bat`. Reconstructed from the spec preserved in this file. Now `deploy/install.sh` + `deploy/ares-mdns-alias.{sh,service}`, built into a zip by `scripts/build_school_payload.sh`. The builder **refuses to build if any PDF references `ares.edu`** (the gate whose absence let the dead-link regression ship) and **derives** the deployed `generate_teacher_index.js` from the repo copy, removing the documented manual-sync drift. `index.htmlf` was not recoverable and is deliberately not invented — bundled only if `deploy/index.htmlf` is supplied. **Live test on one server is still the open item.** |
| Avahi/internet-dependency for `install.sh` | **Resolved — no reinstall needed** | `dpkg.log` history on `tsavo3` confirms `avahi-daemon`/`avahi-utils` present since Dec 2024, routinely updated since — baked into the Clonezilla golden image, not a live-internet install. Script has zero internet dependency as written. |
| Partner heads-up on `resourceLinks` schema impact | Message drafted, sent to partner by Mark | Awaiting partner's schema check — not blocking distribution |
| Tracking/attribution for the Grade 10 module link + PDF resource links | Not started | Deliberately scoped as a separate task, not bundled into today's work |
| Continuity protocol (`STATUS.md` + `/update` skill + `/restart` skill) | **Done — confirmed** | `CLAUDE.md`/`STATUS.md` continuity fixes confirmed pushed (`git log`/`git status` on jhm-spark, 2026-07-06: `HEAD`/`main`/`origin/main` all at `b477ef1`, clean tree). `/restart` skill added (`33ceab5`) and documented in `CLAUDE.md` (`222d681`, spacing fix `aa54484`) and this file (`68e7b47`). Tested live — see 2026-07-06 session-log entry below. |
| `.gitignore` scoped to allow `.claude/skills/` | Done, committed `2c7c938` | Was blanket-excluding all of `.claude/`; narrowed to `.claude/settings.local.json` only |
| Lesson-count tables below (Summary + per-subject) | **Done — refreshed from disk 2026-08-02** | Longest-standing open item in this file, flagged stale since 2026-07-05. Now derived from `generators/data/*_data.js` cross-checked against files on disk: **7 subjects, 85 sub-strands, 728 lessons, 340 output files + 255 PDFs**, all complete with no partial sets. The old tables were not just undercounting — Chemistry and Physics were marked NOT STARTED while fully generated, three subjects were absent entirely, and Biology's sub-strand numbering had been renumbered, so old and new IDs do not map onto each other. The Summary section now carries the two commands that regenerate the numbers, so the next drift is checkable rather than discovered. |
| Session-tooling commits `8d3fe16` / `1f4f6f8` / `9937ed3` | Done, recorded 2026-07-31 | Token-optimizer marketplace, tooling-defect fixes, code-review-graph install. Were pushed to `origin/main` without a STATUS.md entry — caught by `/restart` on 2026-07-31, see session log + Known Issues below. |
| code-review-graph CLAUDE.md wording — "ALWAYS use graph tools before Grep/Glob/Read" | **Done — scoped 2026-07-31** | Rewritten against measured coverage, not assumption: graph indexes exactly the 183 tracked `.js`/`.py`/`.sh` files and **0 of 52 tracked `.md` files**; all 85 `*_data.js` are bare `File` nodes (object-literal exports, no functions to graph). Section now states explicitly that reading `STATUS.md` is a plain `Read` no graph tool substitutes for, and that data-file inspection is `Read`/`grep` work. Two installer claims corrected: `semantic_search_nodes_tool` is FTS-only here (0 nodes embedded), and `tests_for` coverage checks are meaningless (1 Test node repo-wide). |
| `.claude/settings.json` Read deny rules | Done, `1f4f6f8` — with a known limit | 6 narrow rules (ares_index DB, `venv/`, `.env`, docx/pdf under `data/outputs`, archived `data/outputs/docx`). **Gate the Read tool only, not bash** — a recursive `grep` over `data/outputs/` still lands in context. Deliberately excludes `*_data.json` and `data/raw/curriculum_pdfs`. |
| Kenyan-terminology wording pass | Blocked | Waiting on example lessons from reviewing teachers. **Not the same thing as the SoW templates in `data/raw/CBE LESSON TEMPLATES/`** — conflating the two came up on 2026-09-19 and is easy to do. Templates are *structural input* to generation (`find_v2_templates()`); this thread needs *reviewer feedback* on wording in already-generated lessons. Supplying templates does not unblock it. |
| Grade-aware pipeline (plumbing) | **Done — 2026-09-19 (`a546ee3`, `77f3591`, `da26382`)** | `build_docs.js` + `generate_substrand.py` + `generate_teacher_index.js` no longer assume Grade 10. `--grade` is now **required** on `generate_substrand.py` with no default. Highest-severity fix: `SUBSTRAND_NAMES` was keyed by subject only, so a Grade 11 run of `biology 2.1` would have silently generated a full lesson sequence about Grade 10's "Plant Nutrition" while labelling it GRADE 11 (Grade 11 reuses the same strand numbering with different topics). Pure plumbing — no curriculum content involved. Origin: partner's Lesson3 editor flagged 3 hardcoded `GRADE 10` strings; tracing them found the larger problem. Handoff: `HANDOFF_grade_aware_pipeline_2026-09-18.md`. |
| Grade 10 output tree left flat — migration **deferred**, not forgotten | **Deferred 2026-09-19 (Mark's call), with a trigger** | New grades emit `v2/Grade{N}/<Subject>/...`; Grade 10 stays at `v2/<Subject>/...`. The handoff (§6) called for migrating Grade 10 too; that was reconsidered because Grade 10 is stable and moving it churns **teacher-visible Google Drive paths** (job 2 is `/MIR` — a migration deletes and re-uploads all 255 PDFs) for no present benefit. **Revisit at the next full-corpus regeneration** — the pending Kenyan-terminology pass is the likely trigger — so the Drive re-sync is paid once, not twice. The exception lives in exactly two places, both commented: `_v2_output_dir()` in `generate_substrand.py` (path construction) and `collectSubjectRoots()` in `generate_teacher_index.js` (the walker). **If you migrate, both simplify — delete the branches, don't add a third shape.** |
| Grade 11 Biology — curriculum extraction + sub-strand inventory | **Done — 2026-09-19 (`a3bcd6f`, `4539435`)** | OCR'd with the new `scripts/extract_curriculum_ocr.py` (17 slices @ 200 dpi, tesseract 5.3.4 `--psm 4`) → `data/raw/curriculum_text/grade11_biology.txt`, 53,129 chars / 1,281 lines, no dedup needed. Wired into `CURRICULUM_TEXT_MAP[11]['biology']`. **All 10 sub-strands hand-verified from rendered page images** (page ix summary table), not from OCR text — closes the handoff's §8 open item for Biology. Grade 11 has **10** sub-strands to Grade 10's 9, and **every shared number is a different topic** (2.1 = Reproduction in Plants, not Plant Nutrition). Pipeline confirmed end-to-end up to the API boundary. |
| Grade 11 Biology — **full generation** | **Done 2026-10-01 — all 10 sub-strands, 78 lessons + quizzes; awaiting Mark's review** | Layout (Mark, 2026-10-01): `v2/Grade11/Biology/Lesson_Plans/SS<id>_<name>/` (3 docx + `_data.json` + `_quiz.json`) and `v2/Grade11/Biology/Quizzes/SS<id>_<name>/` (decks + answer keys). All 10 pass the link gate (0/0/0/0); `validate_corpus.js` PASS; 95/95 exports partner-schema valid; quizzes 78/78 lessons, 576 questions, 0 failures. Lessons ~$3.06 for the 9 new sub-strands (+$0.41 pilot), quizzes ~$2.30. **PDFs + teacher-index entry done 2026-10-01 (Mark approved): 186 Grade 11 PDFs (30 lesson docs + 78 Quick Checks + 78 Answer Keys), index now 95 sub-strands / 285 documents.** Committed and pushed `f17e779` (2026-10-01); not yet synced to Drive. Review flags: 1.4 L7–10 and 2.2 L8–10 had no teacher spine row; 2.2 L7 'Plant Hormones' and L9 'Role of Hormones' may overlap. |
| Other five Grade 11 STEM subjects | **3 of 5 ready 2026-10-01; 2 blocked on replacement source PDFs** | **Ready** (OCR'd, sub-strand lists hand-verified against each PDF's rendered summary-table image, in `SUBSTRAND_NAMES[11]` + `CURRICULUM_TEXT_MAP[11]`, every sub-strand slices): Chemistry 6, Physics 13, Core Mathematics 17 (incl. the new 4.0 Calculus: 4.1 Functions, 4.2 Differentiation I). No templates for these yet, so they would generate from the curriculum alone. **Blocked: General Science and Essential Mathematics.** Their `CBE_Curriculums/Grade 11/STEM/` October 2025 PDFs are broken screen captures that repeat the 'National Goals of Education' front matter and never reach the curriculum tables (images viewed directly). Mark needs replacement copies from KICD. |
| Non-STEM Grade 11 sources | Not found — out of scope | `CBE_Curriculums/Grade 11/` has only a `STEM/` subfolder; no `General/` counterpart to Grade 10's (English, History and Citizenship). Needs sourcing before any non-STEM Grade 11 work. |
| Non-STEM subject expansion | Not started | Planned after Grade 11 |
| Partner-reported General Science defects (`safety<N>otes` key, missing `summaryTablePrompt.explained`) | **Done — repaired 2026-08-02, root cause fixed** | Reported via `Gnerator_issues.txt` (note: filename is misspelt, no `e`) by the partner building the teacher lesson-plan editor, whose import checker caught both. 35 corrupted `slo` keys across 15 `gensci_*` files + 2 lessons missing `explained`. Root cause: `scripts/repair_stubs.py:209` did `LESSON_SCHEMA.replace('N', str(lesson_num))` — a bare `N` placeholder that also hit `safetyNotes`. Fixed to `{{LESSON_NUMBER}}`. **Both defects rendered as silently EMPTY docx cells** — see Known Issues. Full re-render done; corpus now 0/0/0 on the partner's three checks. |
| Contract validation on the repair path | **Done — added 2026-08-02** | `scripts/patch_lesson.js` now validates every incoming lesson before writing (exact `slo` key set, all 3 `summaryTablePrompt` cells, 5 canonical phases in order, non-empty required fields) and refuses with a diagnostic instead of writing. This is the chokepoint both `repair_stubs.py` and the manual Quick Start repair use. New `scripts/validate_corpus.js` runs the same contract over **all 85** data files / 728 lessons (`check_new_subjects_quality.js` only ever covered the 43 new-subject files, and nothing covered Bio/Chem/Physics/Maths). |
| Phase-composition defects in `chem_1_2` L2 and `math_2_3` L2 | **Done — regenerated 2026-08-02 (`9b33dce`)** | Surfaced by `scripts/validate_corpus.js`. Both had a duplicated `Observe Phase` where `Explain Phase` belongs, so 3 rows got the wrong ARES resource bucket + default grey shading via `sections.js`'s silent fallbacks. **Not a relabel** — the content itself sat under the wrong phase (`chem_1_2` had bottle-tops/maize physical modelling under the DQB label and prediction-revision under Model Building; `math_2_3` had its DQB evidence-card activity under Model Building and no genuine Model Building step at all). Both regenerated with the five phase labels pinned by `const` in the tool schema, so a duplicate/mislabelled phase is now structurally impossible. |
| `aresKeywords` missing on `phys_3_1` L6 | **Done — added 2026-08-02 (`9b33dce`)** | Only lesson in the corpus without it. **Correction to the earlier note here:** this did *not* mean "no ARES resource lookup" — `sections.js:151` falls back to `lesson.aresKeywords \|\| lesson.title`, so the lookup worked but on weaker terms than its siblings'. Keywords written from that lesson's own content. |
| `scripts/sync_to_drive.bat` | **Now actually exists — written 2026-08-02** | It did not. `CLAUDE.md:95` listed it, and this file claimed twice (in the "Documentation drift" entry below, and in the 2026-07-04 log) that it was committed and its destinations were `grep`-able from jhm-spark. All three were false — no `.bat` was tracked or on disk. Written from the spec in `WORKFLOW.md` Step 8 + `docs/PDF_GENERATION.md`; masks verified against the real trees (255 docx + 85 json; 255 pdf + 1 html). Drive destinations now also in WORKFLOW.md's Environment Reference table, which `CLAUDE.md` already designated the single source of truth for sync destinations but which had no Drive rows. |
| `patch_lesson.js --force` | Added 2026-08-02 (`9b33dce`) | For deliberately replacing a lesson whose content is *wrong* rather than *absent* (needed for the two phase repairs above). Skips only the stub-repair guard — **never** the contract validation. |
| **Bounded project v2** (link-selection fix + Quick Check quizzes + attribution, then Grade 11 readiness) | **Phase 5 done 2026-09-30 *without* the remaining quizzes (Mark: review the 27 existing quizzes with the partner first); Phase 6 checks pass. Remaining quizzes (701 lessons, est. ~$21) deferred — generate, then rerun `build_quiz.js` + `generate_pdfs.js` + `generate_teacher_index.js`. Phase 7 docs done 2026-09-30; Drive sync is Mark's step on Windows. Phase 8 in progress: Grade 11 Biology 2.1 pilot done 2026-10-01 (see the Grade 11 pilot row), awaiting Mark's review. Bulk Grade 11 needs a separate go-ahead.** | Phase 3: quiz generator `src/generate_quiz.py` (structured outputs, per-lesson validation, seeded choice shuffle, batch + checkpoint), validator `scripts/validate_quiz.py`, renderer `generators/build_quiz.js` (validator-gated; QuickCheck .pptx, AnswerKey .html/.docx into `quiz/`; PDFs via `generate_pdfs.js`, now also .pptx), attribution `generators/lib/attribution.js` in all 3 docx + every lesson footer + decks + keys. Quiz data in separate `<prefix>_quiz.json` (schema in `docs/SCHEMA.md`). 5 sample lessons generated (Bio 2.1 L2, Phys 1.1 L2, Chem 3.1 L4, Maths 3.1 L4, anchor Phys 2.1 L1): 0 validator failures; 20/20 hand-checked answers correct. Sonnet 5.5 vs Opus 5.5 compared: similar quality, Sonnet kept the anchor lesson spoiler-free more strictly → Sonnet 5.5 stays default. API spend so far $1.68. Spec: `handoff_bundle_2026-09-29/HANDOFF_bounded_project_v2_2026-09-29.md`. Design approved: `DESIGN_link_selection_v2.md` (§7 = implementation differences). New matcher in `src/ares_recommender.py`, rules in `config/link_matching.yaml`, gate `scripts/check_resource_links.py` wired into `generate.js` (non-zero exit on answer-key / wrong-subject / dead link / contract failure). All 85 sub-strands re-rendered (docx + JSON; PDFs regenerated in Phase 5, 2026-09-30: 309 PDFs). Gate: T1/T2/DEAD/SHAPE = 0/0/0/0 corpus-wide (was 45/166/45/0 across all phases). **Live-verified on demo.aresedu.dev: 1,707/1,707 distinct links OK** (`scripts/verify_links_live.py`). Web-module links now direct (the tracker page rejects non-`/kiwix/` targets). Strict-equivalent synonyms added per Mark. Handoff audit (predict): Tier 2 25→0, Tier 3 174→28; its Tier 1 reads 34→32 but **all 32 are "worked example" titles** matched by its bare `exam` regex (0 real answer keys). Lesson content unchanged (diff check: only `resourceLinks` differs, 85/85). Fill rate drops to 72–99% by subject: no-match cells now say so instead of showing a weak link; content-gap list in the 2026-09-29 session log. Link verification uses the ARES system disk mounted on jhm-spark (Kolibri DB + `/var/www/modules`). Attribution config moved to `config/attribution.yaml` with SeaVuria's Kenyan NGO no. 872-850A-BF11 added. Quiz model: **`claude-sonnet-5-5`** (confirmed on the account; it rejects forced `tool_choice`, so the quiz generator uses structured outputs). Autonomy (Mark): repair same-class issues, report at end. API credits added ($50). |
| **Sonnet 5.5 minimum for all API calls** (Mark, 2026-09-30) | **Done — first live run 2026-10-01 (Grade 11 Bio 2.1 pilot), worked** | No code path defaults to `claude-sonnet-4-6` (or any 4.x model) any more. `src/generate_substrand.py` moved from forced `tool_choice` (which Sonnet 5.5 rejects with a 400) to structured outputs (`output_config.format`) for the live path and both batch request types; adaptive thinking, effort `high` (env `CLAUDE_EFFORT`), `max_tokens` 16000 because thinking counts against it; JSON read from the text block, since a thinking block can come first; refusals retried; count-schema `minimum`/`maximum` dropped (clamped in code). Batch collect still reads old `tool_use` results. `scripts/repair_stubs.py` and the May-era legacy scripts are also on 5.5, with a `content[0].text` fix and non-default `temperature` removed. Checked against the API with free `count_tokens` calls (all 5 schemas OK), **not** by a real generation. Live-tested by the 2026-10-01 pilot: 9/9 batch requests OK. Measured **~$0.05 per lesson**, about 25% cheaper than 4.6 without thinking on the same sub-strand. `LESSON_TOOL_SCHEMA` `phase` is now an enum (both models drifted on free-text labels). |
| Presentations (`build_pptx.js`) | **Deferred — pending teacher review of the design** | Per the v2 handoff, do not build yet. Reference examples (not to build from): `handoff_bundle_2026-09-29/presentation_examples_deferred/` (4 answer keys, an illustrative Biology L2 deck, `build_*_L*.js` prototypes). Quiz questions already carry `phase` + `placement` so they can be inserted inline later without regeneration. |
| Quiz review + remaining 701 Grade 10 quizzes | **Waiting on Mark + partner review of the 27 existing quizzes** | 8 sub-strands have quizzes (see the 2026-09-30 answer on which lessons). After review: `generate_quiz.py --batch --all --grade 10` (~$21), then `build_quiz.js`, `generate_pdfs.js`, `generate_teacher_index.js` (WORKFLOW.md Step 6q). **Also decide:** whether `index.html` should link the quiz decks/answer keys. It doesn't today, though they're in the PDF tree and on Drive. |
| Partner: Lesson3 handling of `null` resource slots | **Open — covered in `PARTNER_CONTRACT_NOTES.md`** | Schema unchanged and all 85 exports validate, but 830/7,280 slots are now `null` (were 0) and 187 `direct_url`s are `/modules/` web links, not Kolibri. Send the partner the notes file. |
| Grade 11 Biology template gaps (for the teachers) | **Open — needs teacher input before bulk Grade 11 Biology** | All 10 templates are filed and parse. **1.4 Cell Division: 10 lessons but 6 spine rows; 2.2: 10 lessons but 7 spine rows** (the lessons without a row get no teacher plan). 1.2 has 'N/A' lessons (its 9-row spine sets the count). 2.3 asks for 5 lessons (below the usual 6; the teacher's figure is used). 2.2's lesson-number cells are blank or garbled (rows are numbered in order). Harmless: 7 of the forms still print the blank form's 'Grade 10' header. |
| New Grade 10 STEM subjects (General Science, Core Mathematics, Essential Mathematics) | **Done — Phase 3 complete, committed `f6d6fab`** | All 43 sub-strands / 344 lessons generated, docx+PDF regenerated, teacher index rebuilt, pushed to `origin/main`. Handoff: `HANDOFF_new_stem_subjects_2026-07-28.md` (Rev 2). See 2026-07-30 session-log entry below for the bugs found/fixed along the way (subject-label bug, 34 stub lessons, 1 missing FE). Replacement Core Mathematics source PDF referenced in the handoff was never supplied but generation proceeded — flag if a full curriculum-text re-check against it is still wanted. Summary/per-subject tables below still need the separate full refresh already flagged as stale. |

---

## Summary

**Refreshed 2026-08-02 from disk**, not from memory. Every number below is
derived from `generators/data/*_data.js` (the source of truth) cross-checked
against the files actually present under `data/outputs/v2/`. Regenerate with:

```bash
node scripts/validate_corpus.js    # contract check, 85 files / 728 lessons
grep -h '"outputDir"' generators/data/*.js | sort -u | wc -l    # sub-strand count
```

| Subject | Sub-strands | Lessons | Output dir | Files |
|---|---|---|---|---|
| Biology | 9 | 90 | `v2/Biology/` | complete |
| Chemistry | 7 | 67 | `v2/Chemistry/` | complete |
| Physics | 12 | 101 | `v2/Physics/` | complete |
| Mathematics | 14 | 126 | `v2/Maths/` | complete |
| General Science | 16 | 128 | `v2/General_Science/` | complete |
| Core Mathematics | 14 | 112 | `v2/Core_Mathematics/` | complete |
| Essential Mathematics | 13 | 104 | `v2/Essential_Mathematics/` | complete |
| **Total** | **85** | **728** | 7 subjects | **340 files + 255 PDFs** |

**All 85 sub-strands are complete.** Each produces 4 files (Lesson Sequence,
Final Explanation, Summary Table, `_data.json`) plus 3 PDFs — verified present,
no gaps, no partial sets. Totals: **340 output files + 255 PDFs + 1 index.html**.

> **What the previous version of this table said, and why it was wrong.** It
> claimed 12/33 sub-strands across 4 subjects and ~96 lessons, flagged stale
> since 2026-07-05. It was not merely undercounting: Chemistry and Physics were
> listed as NOT STARTED when both are fully generated, three subjects did not
> exist in it at all, and **Biology's sub-strand numbering has since been
> renumbered** — the old table's 1.1 "Introduction to Biology" and 1.4
> "Chemicals of Life" do not map onto today's 1.1 Cell Structure / 1.2
> Chemicals of Life. Treat any pre-2026-08-02 copy of these tables as a
> different document, not a stale version of this one.

---

## Biology Grade 10 — complete (9 sub-strands, 90 lessons)

| Sub-strand | Name | Lessons | Data module |
|---|---|---|---|
| 1.1 | Cell Structure | 12 | `bio_1_1` |
| 1.2 | Chemicals of Life | 6 | `bio_1_2` |
| 1.3 | Cell Biology | 8 | `bio_1_3` |
| 2.1 | Plant Nutrition | 10 | `bio_2_1` |
| 2.2 | Plant Transport | 8 | `bio_2_2` |
| 2.3 | Plant Gaseous Exchange and Respiration | 12 | `bio_2_3` |
| 3.1 | Animal Nutrition | 10 | `bio_3_1` |
| 3.2 | Animal Transport | 12 | `bio_3_2` |
| 3.3 | Animal Gaseous Exchange and Respiration | 12 | `bio_3_3` |

Lesson counts vary 6–12 by design (dynamic, non-hardcoded — commit `02da69b`). **SS2.1 Plant Nutrition is 10, not 12** — confirmed intentional, see the Known Issues entry on it. SS1.3 Cell Biology has no teacher template; it was generated from curriculum text only.

---

## Chemistry Grade 10 — complete (7 sub-strands, 67 lessons)

| Sub-strand | Name | Lessons | Data module |
|---|---|---|---|
| 1.1 | Introduction to Chemistry | 10 | `chem_1_1` |
| 1.2 | The Atom | 9 | `chem_1_2` |
| 1.3 | The Periodic Table | 10 | `chem_1_3` |
| 1.4 | Chemical Bonding | 13 | `chem_1_4` |
| 1.5 | Periodicity | 7 | `chem_1_5` |
| 2.1 | Introduction to Salts | 8 | `chem_2_1` |
| 3.1 | Acids and Bases | 10 | `chem_3_1` |

Counts vary 7–13. Sub-strand IDs are not contiguous (1.1–1.5, 2.1, 3.1) — that reflects the curriculum, not missing work.

---

## Physics Grade 10 — complete (12 sub-strands, 101 lessons)

| Sub-strand | Name | Lessons | Data module |
|---|---|---|---|
| 1.1 | Pressure | 9 | `phys_1_1` |
| 1.2 | Mechanical Properties of Materials | 6 | `phys_1_2` |
| 1.3 | Temperature and Thermal Expansion | 6 | `phys_1_3` |
| 1.4 | Energy, Work, Power and Machines | 8 | `phys_1_4` |
| 1.5 | Moments of Equilibrium | 6 | `phys_1_5` |
| 2.1 | Properties of Waves | 12 | `phys_2_1` |
| 3.1 | Radioactivity and Stability of Isotopes | 7 | `phys_3_1` |
| 3.2 | Current Electricity | 12 | `phys_3_2` |
| 3.3 | Introduction to Electronics | 7 | `phys_3_3` |
| 3.4 | Electrostatics | 9 | `phys_3_4` |
| 4.1 | Greenhouse Effect and Climate Change | 7 | `phys_4_1` |
| 4.2 | Introduction to Space Physics | 12 | `phys_4_2` |

Counts vary 6–12. `phys_3_1` L6 had no `aresKeywords` until 2026-08-02.

---

## Mathematics Grade 10 — complete (14 sub-strands, 126 lessons)

| Sub-strand | Name | Lessons | Data module |
|---|---|---|---|
| 1.1 | Real Numbers | 7 | `math_1_1` |
| 1.2 | Indices | 8 | `math_1_2` |
| 1.3 | Quadratic Equations | 7 | `math_1_3` |
| 1.4 | Congruence | 8 | `math_1_4` |
| 2.1 | Similarity and Enlargement | 12 | `math_2_1` |
| 2.2 | Area of Polygons | 8 | `math_2_2` |
| 2.3 | Area of Part of a Circle | 10 | `math_2_3` |
| 2.4 | Surface Area and Volume of Solids | 10 | `math_2_4` |
| 3.1 | Trigonometry I | 10 | `math_3_1` |
| 3.2 | Rotation | 10 | `math_3_2` |
| 3.3 | Vectors I | 8 | `math_3_3` |
| 3.4 | Linear Motion | 10 | `math_3_4` |
| 4.1 | Statistics I | 9 | `math_4_1` |
| 4.2 | Probability I | 9 | `math_4_2` |

Counts vary 7–12. **Note the directory is `v2/Maths/`, while `META.subject` is `Mathematics`** — both are correct and long-standing; don't 'fix' either. The old table here described `math_2_2`/`2_3`/`2_4` as legacy pre-pipeline output; all 14 are now standard pipeline output.

---

## General Science Grade 10 — complete (16 sub-strands, 128 lessons)

| Sub-strand | Name | Lessons | Data module |
|---|---|---|---|
| 1.1 | Introduction to General Science | 8 | `gensci_1_1` |
| 1.2 | The Cell | 8 | `gensci_1_2` |
| 1.3 | Nutrition in Animals | 8 | `gensci_1_3` |
| 1.4 | Transport in Plants | 8 | `gensci_1_4` |
| 1.5 | Respiration | 8 | `gensci_1_5` |
| 1.6 | Plant Growth and Development | 8 | `gensci_1_6` |
| 1.7 | Microorganisms | 8 | `gensci_1_7` |
| 2.1 | The Periodic Table | 8 | `gensci_2_1` |
| 2.2 | Chemical Families | 8 | `gensci_2_2` |
| 2.3 | Chemical Bonding | 8 | `gensci_2_3` |
| 2.4 | Acids, Bases and Salts | 8 | `gensci_2_4` |
| 2.5 | Rates of Reactions | 8 | `gensci_2_5` |
| 3.1 | Turning Effect of Force | 8 | `gensci_3_1` |
| 3.2 | Linear Motion | 8 | `gensci_3_2` |
| 3.3 | Waves | 8 | `gensci_3_3` |
| 3.4 | Magnetism and Electromagnetic Induction | 8 | `gensci_3_4` |

Uniform 8 lessons per sub-strand. This subject carried both defects the partner's importer found on 2026-08-02 (35 `safety<N>otes` keys, 2 missing `summaryTablePrompt.explained`) — all repaired.

---

## Core Mathematics Grade 10 — complete (14 sub-strands, 112 lessons)

| Sub-strand | Name | Lessons | Data module |
|---|---|---|---|
| 1.1 | Real Numbers | 8 | `coremath_1_1` |
| 1.2 | Indices and Logarithms | 8 | `coremath_1_2` |
| 1.3 | Quadratic Expressions and Equations | 8 | `coremath_1_3` |
| 2.1 | Similarity and Enlargement | 8 | `coremath_2_1` |
| 2.2 | Reflection and Congruence | 8 | `coremath_2_2` |
| 2.3 | Rotation | 8 | `coremath_2_3` |
| 2.4 | Trigonometry 1 | 8 | `coremath_2_4` |
| 2.5 | Area of Polygons | 8 | `coremath_2_5` |
| 2.6 | Area of a Part of a Circle | 8 | `coremath_2_6` |
| 2.7 | Surface Area and Volume of Solids | 8 | `coremath_2_7` |
| 2.8 | Vectors | 8 | `coremath_2_8` |
| 2.9 | Linear Motion | 8 | `coremath_2_9` |
| 3.1 | Statistics I | 8 | `coremath_3_1` |
| 3.2 | Probability I | 8 | `coremath_3_2` |

Uniform 8 lessons per sub-strand. Generated against the *original* curriculum text — the replacement Core Mathematics PDF referenced in `HANDOFF_new_stem_subjects_2026-07-28.md` was never supplied, and no re-check against it has been done.

---

## Essential Mathematics Grade 10 — complete (13 sub-strands, 104 lessons)

| Sub-strand | Name | Lessons | Data module |
|---|---|---|---|
| 1.1 | Real Numbers | 8 | `essmath_1_1` |
| 1.2 | Indices | 8 | `essmath_1_2` |
| 1.3 | Quadratic Equations | 8 | `essmath_1_3` |
| 2.1 | Similarity and Enlargement | 8 | `essmath_2_1` |
| 2.2 | Reflection | 8 | `essmath_2_2` |
| 2.3 | Trigonometry | 8 | `essmath_2_3` |
| 2.4 | Area of Polygons | 8 | `essmath_2_4` |
| 2.5 | Area of Part of a Circle | 8 | `essmath_2_5` |
| 2.6 | Surface Area of Solids | 8 | `essmath_2_6` |
| 2.7 | Volume and Capacity | 8 | `essmath_2_7` |
| 2.8 | Commercial Arithmetic 1 | 8 | `essmath_2_8` |
| 3.1 | Statistics 1 | 8 | `essmath_3_1` |
| 3.2 | Probability I | 8 | `essmath_3_2` |

Uniform 8 lessons per sub-strand. Unaffected by the 2026-07-30 stub-lesson defects.

---
## Known Issues / Lessons Learned

### Batch API — JSON truncation
Claude occasionally generates JSON that is truncated or contains apostrophes in string values, causing parse failures. This results in stub lessons (empty content). **Standard practice:**
1. After every batch collect, run `node /tmp/check_data.js` to identify stubs
2. Use `scripts/patch_lesson.js` and `scripts/patch_fe.js` to repair

### Final Explanation generation
FE prompts with long context (full lesson titles + detailed instructions) can exceed output token limits. Use the short-prompt approach in `scripts/gen_bio33_fe.py` as a template — pre-fill section structure and ask Claude to fill content only.

### Git and large files
`data/ares_index/ares_content.db` (630MB) is gitignored. It lives on jhm-spark only. Always check for large files before pushing:
```bash
find . -size +50M -not -path './.git/*' -not -path './venv/*'
```

### Sub-strand naming in batch collect
The `--collect` command requires `--subject`, `--substrand`, `--output` to be omitted (it reads from the checkpoint file). If the checkpoint was not saved (e.g. script crashed after submit), manually create `.{name}_batch_id.txt` and `.{name}_batch_id.json` before collecting.

### Documentation drift — stated facts going stale silently (2026-07-04)
Two independent incidents, same root cause, same day:
1. `SYSTEM_OVERVIEW.md`, `WORKFLOW.md`, and `STATUS.md` all stated
   `data/outputs/docx/` as the output path — true when written, but
   superseded by `data/outputs/v2/` at some prior restructure. Nothing
   flagged the mismatch; it was only caught by manually grepping
   `outputDir` across every `*_data.js` file and cross-checking against
   the real filesystem.
2. `WORKFLOW.md` stated the git branch as
   `claude/setup-cbe-generation-ZKiIi` in four separate places. That
   branch no longer exists on the remote; `main` has for some time. Same
   pattern: a value copied forward as fact, never re-verified, repeated
   in multiple places so partial fixes could leave it inconsistent.

**Neither was caused by carelessness reading the docs** — a careful
reader would copy the stated value exactly, because nothing in the text
distinguished "true when written" from "true now." The fix is structural,
not a request for more vigilance:
- `WORKFLOW.md` now opens with a **Step 0** verification block
  (`git branch --show-current`, a live `outputDir` grep, a `soffice`
  check) to be run before any task touching git, paths, or sync — with
  an explicit rule that a mismatch against the Environment Reference
  table gets fixed immediately, not deferred.
- `WORKFLOW.md`'s **Environment Reference table is now the single source
  of truth** for branch name, output paths, and Drive sync destinations.
  Other docs (`SYSTEM_OVERVIEW.md`, `PDF_GENERATION.md`, this file) point
  back to it instead of restating the values independently.
- The Windows Drive-sync `.bat` file is now committed as
  `scripts/sync_to_drive.bat`, so its actual configured destinations are
  `grep`-able from jhm-spark instead of only checkable by someone
  physically at the Windows machine.

### `resourceLinks` in JSON export (2026-07-05)
- New field added to every lesson object in the JSON export, populated
  from `getAllPhaseResources()` output (`sections.js`, one new line —
  `lesson.resourceLinks = aresRes;` — placed just after the resource
  lookup call, exploiting JS object-reference semantics rather than
  requiring any change to `build_docs.js`'s serialization).
- Full corpus regenerated and verified: all 126 JSON files contain the
  field, 0 missing.
- **Partner impact not yet confirmed** — if `ares-contract.schema.json`
  uses `additionalProperties: false` near the lesson object, this new
  field could cause their checker to reject every document. Flagged to
  partner; check not yet done as of this writing.

### `ares.edu` → `ares.local` hostname migration (2026-07-05)
- Root cause: `ares.edu` only ever resolved via a local DNS server
  (`dnsmasq`) that requires this box to control DHCP — works when a box
  is its own hotspot, silently fails when plugged into an existing
  school router (which doesn't hand out this box as the DNS server).
  mDNS (`.local`) resolves via broadcast regardless of who runs DHCP,
  which is why `ares.local` works in both deployment modes.
- Fix: `src/ares_recommender.py`'s `ARES_HOST` env var (already existed,
  previously unused) set to `ares.local`; full corpus regenerated.
  `nginx`'s `server_name` directive updated to include `ares.local`
  alongside `ares.edu`/`www.ares.edu` (config lives in whichever file is
  actually symlinked in `sites-enabled/` — confirmed to vary in name
  across at least one box, don't assume a filename like `default`).
- A persistent mDNS alias requires a systemd service
  (`ares-mdns-alias.service`, publishes `ares.local` via `avahi-publish`
  and re-publishes on IP change) — a one-off `avahi-publish` command
  does NOT survive reboot and will silently regress if treated as done.
- **Discovered mid-fix, unrelated to hostnames:** `ares.edu` was also
  never actually reachable via mDNS in the first place — mDNS resolvers
  only ever resolve `.local` names by protocol; no configuration could
  have made `ares.edu` work over mDNS.
- Deployment to the ~100 school servers is via a provisioning script
  (`install.sh`, distributed as a zip with the PDF payload) rather than
  git — those servers aren't running this repo directly.

### Lesson-count discrepancy — Bio 2.1 Plant Nutrition (clarified 2026-07-05)
- `STATUS.md` said 12 lessons; actual current content has 10, under a
  different phenomenon (sukuma wiki, not the uploaded pumpkin reference
  doc) and a different filename convention (no `_L1-12` suffix).
- **Confirmed intentional, not corruption:** commit `02da69b`'s message
  explicitly states dynamic, non-hardcoded lesson counts as a deliberate
  design change; a current teacher template for the sukuma wiki version
  exists (`v2_owner_inventory/Biology/SS2.1_Plant_Nutrition`). The
  uploaded pumpkin reference document is from the superseded
  `data/outputs/docx/` tree.
- Lesson counts across all 42 sub-strands now range 6–13 (confirmed via
  direct inspection of every `*_data.js` file) — this is expected, not a
  bug, per the same intentional design.
- This is exactly why the Summary/per-subject tables above are flagged
  stale rather than corrected in place: the real counts are now known
  file-by-file, but a full authoritative refresh of this document hasn't
  been done yet, and shouldn't be improvised from a partial check.

### `generate_teacher_index.js` — two legitimate deployed copies (2026-07-05)
- One copy lives in this repo (`generators/generate_teacher_index.js`),
  using a relative `PDF_ROOT` path — correct for jhm-spark's own
  `data/outputs/v2/PDF/` tree.
- A second copy is bundled in the school-server provisioning package
  with `PDF_ROOT = __dirname` instead — correct because that copy always
  sits directly inside the deployed `PDF/` folder on every server.
- This is a real, permanent difference (not a mistake to unify) — but it
  means any future logic change to this script must be applied in both
  places manually. No automated sync between them exists.

### `CLAUDE.md` UTF-16 encoding + terminal-paste corruption (2026-07-05/06)
- `CLAUDE.md` was discovered saved as **UTF-16LE**, not UTF-8 — cause
  unknown; worth watching whether other project docs are similarly
  affected if this happens again. Converted and re-saved as plain UTF-8,
  no BOM, LF line endings.
- While fixing stale content in the same pass, two independent
  terminal-paste failure modes surfaced when transferring the corrected
  file via `python3 -c "...sys.stdin.read()"` + manual paste:
  1. **Long pastes can be silently truncated** by the terminal's paste
     buffer — a ~245-line paste landed as 60 lines with no error.
  2. **Box-drawing Unicode characters (`├ │ └`) are excluded from this
     chat interface's "Copy" button**, forcing manual reconstruction —
     which itself is error-prone (in one instance, the reconstruction
     accidentally included a command line from the surrounding
     instructions as if it were file content).
  3. Separately, at least one paste attempt resulted in the target file
     being fully truncated to 0 bytes — exact cause not diagnosed
     (suspected: a `'w'`-mode write with no actual stdin content, e.g.
     Ctrl-D pressed before pasting).
- **Resolution:** stopped using terminal copy-paste for this file
  entirely. Replaced the Repository Layout and output-file-listing tree
  diagrams with plain ASCII (full relative paths, no box-drawing
  characters), and delivered the corrected file as a direct download for
  transfer via `scp`/SFTP instead of paste.
- **Going forward:** for any file long enough to risk truncation, or
  containing special/Unicode characters, prefer direct file
  download + `scp`/SFTP transfer over terminal paste, chunked or
  otherwise. Chunking with placeholder blank-line markers
  (`%%%BLANK%%%`, converted back with `sed` after paste) is a viable
  fallback if direct transfer isn't available, but verify line count
  after every single chunk, not just at checkpoints — this incident
  involved two different corruption modes in adjacent attempts.

### Continuity rule held for content work, lapsed for tooling work (2026-07-31)

Three commits (`8d3fe16`, `1f4f6f8`, `9937ed3`) landed on `origin/main`
between 2026-07-30 and 2026-07-31 with **no Active Threads row and no
session-log entry** — the first time this file has fallen behind `main`
since the continuity protocol was established. Caught only because
`/restart` compares `git log` against this file; nothing else would have
surfaced it.

**The pattern worth noting:** the rule ("update STATUS.md as part of
finishing the work") has been followed reliably for *generation* work —
sub-strands, repairs, corpus runs — and silently skipped for *tooling*
work — settings, skills, MCP servers, plugin installs. Plausibly because
tooling changes don't feel like they change "project status," and because
some of them are performed by an installer rather than typed out. But
`9937ed3` appended a mandatory behavioral instruction to `CLAUDE.md`
telling every future session to prefer graph tools over `Grep`/`Read` —
that is a change to how sessions operate, and it went unrecorded.

Two follow-on consequences of the same lapse:
- `CLAUDE.md`'s header still read *Last updated: 2026-07-05* while
  carrying a section added 2026-07-31, and its Repository Layout section
  lists neither `.claude/skills/restart/` nor any of the four
  graph skills. A reader trusting the header would date the MCP section
  three weeks earlier than it is.
- This file's own header said *Last updated: 2026-07-05* despite two
  2026-07-30 entries. Fixed in the same pass.

**Takeaway:** "files changed" in the continuity rule means *any* tracked
file, including `.claude/`, `.mcp.json`, and `.gitignore` — not just
`generators/data/` and `data/outputs/`. Installer-generated changes count,
and arguably need *more* recording than hand-made ones, since nobody
composed a rationale for them at the time.

### The same bug was fixed twice on symptoms, then re-fired (2026-08-02)

A partner's import checker found 35 `slo` keys corrupted to `safety<N>otes` and
2 lessons missing `summaryTablePrompt.explained`, all in General Science. Root
cause was one line — `scripts/repair_stubs.py:209`:

```python
f"{LESSON_SCHEMA.replace('N', str(lesson_num))}"
```

`LESSON_SCHEMA` contains exactly two capital `N`s: `"number": N` (intended) and
`safetyNotes` (collateral). So every repaired lesson got its safety guidance
filed under an unreadable key.

**The part worth remembering: this had already been fixed once.**
`scripts/fix_safetynotes.py` is committed (`3b75018`, "safetyNotes keys") and
does precisely this repair — it was written for an earlier repair pass over
Bio/Chem/Physics/Maths, which is why those subjects are clean. Nobody fixed
`repair_stubs.py`, so the 2026-07-30 General Science repair pass re-created the
identical defect. Re-running the cleanup script without fixing line 209 would
have guaranteed a third occurrence. **A fix that cleans data without fixing the
code that produced it is a fix with a timer on it.**

**Why nothing caught it for three days:** both defects render as *silently
empty* cells, not errors.
- `generators/lib/sections.js:118` reads `lesson.slo.safetyNotes` → `undefined`
  → `docx_kit.js`'s `cell()` takes its non-string `else` branch → docx-js emits
  an empty cell. No crash, and no literal "undefined" in the output (verified).
- `generators/lib/build_docs.js:211` reads `l.explained || ''` → blank column.

So 35 teacher-facing lesson plans shipped with a blank Safety Notes row —
including lessons involving razor blades, dilute HCl/H₂SO₄, and CuSO₄ disposal —
and every generation run reported success. The text was never lost, only
filed under a key nothing reads. **Silent fallbacks (`|| ''`, `undefined` into a
renderer) turn a data defect into an invisible one; anywhere the pipeline has
one, a contract check has to sit upstream of it.**

**Also worth noting: the gate that existed was structurally blind here.**
`check_new_subjects_quality.js` was already widened once (2026-07-30) after
exactly this class of miss, but only to *all gensci/coremath/essmath files* —
it still checked nothing about `slo` key names or `summaryTablePrompt`
completeness, and nothing at all outside the three new subjects. Widening a
gate's *file coverage* does not widen *what it checks*.

**Fixes applied:** `{{LESSON_NUMBER}}` placeholder in `repair_stubs.py`; a
refuse-before-write contract validator in `scripts/patch_lesson.js` (the
chokepoint both repair paths use); and `scripts/validate_corpus.js` running the
same contract over all 85 files / 728 lessons. The corpus validator immediately
earned its keep by surfacing two unrelated pre-existing defects (see Active
Threads).

### A default that contradicts a completed migration will silently undo it (2026-08-02)

The `ares.edu` → `ares.local` migration (2026-07-05, `5071ea4`) was completed
and verified: 0 `ares.edu` remaining. On 2026-08-02 the entire corpus was found
back on `ares.edu` — all 85 JSON exports, all 85 Lesson Sequence docx (~160 dead
hyperlinks each), and all 255 PDFs.

Nobody reverted anything. `src/ares_recommender.py` still had:

```python
ARES_HOST = os.environ.get("ARES_HOST", "ares.edu")
```

`generate.js` shells out to that module via `generators/aresResources.js`, so
**any** regeneration without `ARES_HOST` exported rewrites every link back to the
old host. `f6d6fab`'s `generate.js --all` (the new-STEM-subjects run) did exactly
that on 2026-07-30, reverting all 42 original sub-strands and generating the 43
new ones the same way. Bisect: `5071ea4` = 280 `ares.local` / 0 `ares.edu`;
`f6d6fab` onward = 0 / 280.

**Three things made this invisible for three days:**
1. Nothing errors. A wrong-but-well-formed hostname generates, renders and
   converts to PDF perfectly.
2. The failure is off-box. `ares.edu` resolves fine wherever a dnsmasq instance
   controls DHCP — it dies silently behind a school router, which is the
   deployment mode `.local` was adopted for. You cannot see it from jhm-spark.
3. `STATUS.md` asserted "0 remaining `ares.edu`" the whole time, because that
   line was written when it was true and nothing re-checked it.

**This is the same shape as the `safetyNotes` bug found the same day** (see the
entry above): a migration or repair was applied to *data*, the *default that
produces the data* was left alone, and the next regeneration quietly undid the
work. Two independent instances in one corpus, both caught only by accident.

**The generalisable rule: after fixing data, find the line that produced the bad
data and change that too — then re-derive the data and confirm.** A verified-once
count in a status document is not a guard; it degrades into a stale claim the
moment a producing default disagrees with it.

**Fixes:** default is now `ares.local` with a comment saying why it must not be
changed back (`ARES_HOST` override still works for a specific box);
`WORKFLOW.md` Step 6 carries the warning and a new **Step 6c** gives a two-line
`grep` to verify the host *before* distributing. Verified after regeneration:
0 `ares.edu`, 25,480 `ares.local` URLs, 14,560 docx hyperlinks.

### Third-party installers can append behavioral instructions to `CLAUDE.md` (2026-07-31)

`code-review-graph install --platform claude-code` (`9937ed3`) modified
six tracked files, including appending an "ALWAYS use graph tools before
Grep/Glob/Read" section to `CLAUDE.md` and adding `PostToolUse`/
`SessionStart` hooks to `.claude/settings.json`. The settings merge was
additive and left the `1f4f6f8` deny rules intact — verified, not assumed.

The `CLAUDE.md` wording is unreviewed third-party text now carrying the
same authority as hand-written project rules, and it is overbroad here:
this project's most-read files are Markdown control documents and
`*_data.js` content modules, which a code-structure graph does not index
usefully. Left in place for now and tracked in Active Threads rather than
edited blind. **Lesson for future installs: diff what an installer wrote
into `CLAUDE.md` and `.claude/settings.json` before committing, and treat
any instruction text it adds as a proposal, not as project policy.**

---

### 2026-09-30 / 10-01 — four silent failures caught before the Grade 11 pilot

- **A model upgrade is not a string swap.** Sonnet 5.5 rejects forced `tool_choice`,
  and `generate_substrand.py` relied on it in 3 places. Changing `MODEL` alone would
  have 400'd every lesson request. Check a new model's breaking changes (forced tool
  use, thinking, sampling params, `content[0]` being a thinking block) before
  switching, and validate request shapes with free `count_tokens` calls before spending.
- **The template format changed with no error.** The Grade 11 templates use a new
  Teacher Planning Template form (content in tables). The Grade 10 extractor
  "succeeded", returning the phenomenon and empty strings for the rest, so a pilot
  would have run without the teacher's lesson spine. Whenever new templates arrive,
  run `extract_template_docx()` on one and look at what came back before generating.
  The lesson-count regex would also have read the form's printed hint ("5 to 8
  lessons") as the count.
- **Free-text schema fields drift.** With `phase` as an unconstrained string, both
  Sonnet 5.5 and 4.6 decorated the labels in every lesson. Only the link gate's SHAPE
  check caught it. Any field with a fixed vocabulary should be an `enum` in the
  generation schema, not just a check after the fact.
- **The grade-aware pass (2026-09-19) missed a hardcoded `Grade: 10`** in the UNIT
  prompt. A grep for literal `Grade 10` / `Grade: 10` in prompt strings is now part
  of checking a new grade. Related: Grade 11 OCR curriculum text went in whole (all
  10 sub-strands) until `slice_curriculum_text()` was added.

## Cost Tracking

| Run | Sub-strands | Lessons | Mode | Approx. cost |
|---|---|---|---|---|
| Bio 1.4 (test) | 1 | 6 | Synchronous | ~$0.70 |
| Bio 1.4 (batch) | 1 | 6 | Batch | ~$0.35 |
| Bio 1.2, 2.2, 2.3, 3.1, 3.2, 3.3 | 6 | 8 each | Batch | ~$2.10 |
| **Biology total** | **9** | **~72** | Mixed | **~$5–8** |
| **Projected remaining** | **24** | **~192** | Batch | **~$14** |
| **Full 2,000-lesson target** | **~110** | **~2,000** | Batch | **~$114** |
| Quiz samples, Phase 3 (Sonnet 5.5 + Opus 5.5 comparison, live) | 5 | 5 (+5 redo) | Live | $2.10 (measured) |
| **Quiz pilot, Phase 4** (Sonnet 5.5): gensci 1.3, coremath 2.4, bio 1.2 | 3 | 22 | Batch | **$0.59 (measured; $0.027/lesson, 8.5k in / 3.6k out)** |
| **Quizzes, rest of Grade 10** (estimate) | 82 | 701 | Batch | **~$19 (+~$2 retries) ≈ $21** |
| Quizzes per Grade 11 sub-strand (planning) | 1 | ~8–10 | Batch | ~$0.23–0.27 per sub-strand |
| **Grade 11 Bio 2.1 pilot, Sonnet 5.5** (lessons + FE + ST + UNIT) | 1 | 8 | Batch | **~$0.41 measured (~$0.05/lesson)** |
| Grade 11 Bio 2.1 comparison, Sonnet 4.6 no thinking (evaluation only) | 1 | 8 | Batch | ~$0.55 measured |
| Grade 11 Biology, remaining 9 sub-strands (estimate) | 9 | ~70 | Batch | **~$4** |

---
## Updates — 2026-06-18

### Data file fixes (all committed to main)
- `bio_1_4_data.js`: UNIT block was empty (`{}`); fully populated with phenomenon, driving question, storyline thread, learning outcomes, competencies, values, SEP, PCIs, careers, focus, totalDuration
- All 9 Biology + 3 Math data files: UNIT-level `duration` → `totalDuration` (bio_2_1, math_2_2, math_2_3, math_2_4 patched)
- All 9 Biology data files: `storyline` / `"storyline"` → `storylineThread` (8 files patched; bio_2_1 and math files were already correct)

### New documentation
- `docs/SCHEMA.md` created — canonical field name reference and contract for colleague's JSON editing tool

### Remaining known inconsistency (cosmetic, non-functional)
- JSON-quoted keys (`"totalDuration":`) in bio_1_2, bio_2_2, bio_2_3, bio_3_1, bio_3_2, bio_3_3 — these work correctly but don't match the bare JS key style convention. Deferred to future cleanup.

---
## Updates — 2026-07-04

### New module: PDF generation for teacher distribution
- `generators/generate_pdfs.js` added — converts every `.docx` under
  `data/outputs/v2/` (Lesson Sequence, Final Explanation, Summary Table)
  to PDF via headless LibreOffice, batched for efficiency, logging and
  continuing past individual failures rather than halting the run.
- Output lands in a parallel `data/outputs/v2/PDF/` tree, mirroring the
  `Subject/SubStrand/` structure of the source docx exactly.
- `generators/generate_teacher_index.js` added — generates a static,
  self-contained `index.html` at the root of `v2/PDF/` listing every
  subject/sub-strand with links to its PDFs, for browsing on the offline
  ARES appliance over the school mesh network.
- Both `.docx` and PDF outputs now sync to Google Drive via separate
  robocopy jobs, tracked in `scripts/sync_to_drive.bat` (see
  `WORKFLOW.md` Environment Reference for current destinations — not
  restated here, see the Known Issues entry below for why). **How content
  moves from Drive to each school's offline appliance is still
  unresolved** — flagged as an open item in `docs/PDF_GENERATION.md`.
- Rationale, design decisions, and open items are documented in
  `docs/PDF_GENERATION.md`.
- Corrected stale `data/outputs/docx/` path references in this file and
  in `SYSTEM_OVERVIEW.md` / `WORKFLOW.md` — the current, authoritative
  output root is `data/outputs/v2/`, per each data file's `outputDir`.

---
## Updates — 2026-07-05

### Hostname migration + resource-link improvements
- Migrated all Resource-column links from `ares.edu` to `ares.local`
  across the entire corpus (42 sub-strands, 384 lessons, 126 docx, 126
  PDFs) — see "Known Issues" for full rationale. Zero `ares.edu`
  references remain; verified via full-corpus grep.
- Added `resourceLinks` field to the JSON export (every lesson, every
  phase) — see "Known Issues" for shape and partner-schema caveat.
- `nginx` `server_name` updated (jhm-spark test box) to accept
  `ares.local`; `ares-mdns-alias.service` created for persistent mDNS
  advertisement surviving reboots.
- `generators/generate_teacher_index.js` added to this repo (previously
  existed only as a standalone deployment on the ARES test server,
  which was itself a gap — see "Known Issues").

### Provisioning package for school-wide deployment
- Built `install.sh` + payload structure for deploying the `ares.local`
  mDNS fix, nginx config change, PDF content, and updated module landing
  page (`index.htmlf`) to ~100 independently-managed school servers.
- Not yet tested on real hardware as of this writing — Mark testing on
  one server before wide rollout.

### Continuity protocol established
- This file is now the designated single source of truth for project
  continuity (see "How this file is used" at the top).
- Added an `Active Threads` table (top of this file) and a `/update`
  skill (Claude Code: `.claude/skills/update/`) to force a continuity
  update on demand, independent of task completion.

### Still open going into next session
- `install.sh` live-tested on one real server
- Partner's `ares-contract.schema.json` checked against `resourceLinks`
- Tracking/attribution for the lesson-plan module link (scoped as
  separate task, not started)
- Full refresh of this file's Summary/per-subject lesson-count tables
- Kenyan-terminology wording pass (blocked on teacher-provided examples)
- Grade 11 STEM expansion, then non-STEM subject expansion (both not started)

---
## Updates — 2026-07-06 (triggered by `/update`)

### `CLAUDE.md` corrected and continuity protocol committed
- `CLAUDE.md` fixed: UTF-16 → UTF-8, stale content updated (branch,
  paths, `ares.edu` → `ares.local`), new "FIRST: Read STATUS.md's Active
  Threads" instruction added, box-drawing tree diagrams replaced with
  plain ASCII after terminal-paste corruption — full incident in "Known
  Issues" above.
- `.claude/skills/update/SKILL.md` and a `.gitignore` fix (was
  blanket-excluding `.claude/`, narrowed to `.claude/settings.local.json`)
  committed as `2c7c938`.
- Confirmed avahi-daemon/avahi-utils has been part of the Clonezilla
  golden image since at least December 2024 (routine version-upgrade
  history in `dpkg.log`), not something installed live — `install.sh`
  has no internet dependency for any of its ~100 target servers.
- **Not yet confirmed by this session:** whether the corrected
  `CLAUDE.md` and this `STATUS.md` update have actually been
  `git commit`/`git push`ed on jhm-spark. Verify with `git log --oneline
  -3` before treating this entry as fully closed.

---
## Updates — 2026-07-06 (second session, triggered by `/update`)

### Verified: continuity protocol commit/push (previously unconfirmed)
- Ran `git log --oneline -5` and `git status` on jhm-spark. Confirmed
  `HEAD`, `main`, `origin/main`, `origin/HEAD` all at `b477ef1`
  ("STATUS.md: continuity update via /update"), on top of
  `a0f40fe`/`2c7c938`. Working tree clean. Closes the item flagged
  unconfirmed at the end of the previous `/update` entry.

### New skill: `/restart` — continuity verification checkpoint
- Added `.claude/skills/restart/SKILL.md` (commit `33ceab5`) — re-reads
  `STATUS.md`/`CLAUDE.md`/`WORKFLOW.md`'s Environment Reference, runs
  WORKFLOW.md's Step 0 live checks, and reports drift before continuing,
  without discarding session context. Complementary to `/update`:
  `/update` is the write side of continuity, `/restart` is the
  read/verify side.
- Also usable by typing `/restart` in a Claude.ai session in this
  project (paragraph added to project custom instructions).
- Documented in `CLAUDE.md` (`222d681`, spacing fix `aa54484`) and in
  this file's "How this file is used" section (`68e7b47`).

### `/restart` tested live — found real drift, plus one operational caveat
- Triggered `/restart` in a Claude.ai chat. It correctly re-fetched
  `STATUS.md`/`CLAUDE.md` from GitHub and flagged that the Active
  Threads continuity-protocol row was still worded as unconfirmed, and
  that no session-log entry existed yet for today's `/restart` work —
  both real gaps, both closed by this `/update`.
- **Caveat surfaced:** `raw.githubusercontent.com` (used for the
  Claude.ai auto-fetch at conversation start, and for `/restart`) lags
  behind `git push` by a CDN cache interval — the fetch returned
  pre-push content (`Last updated: 2026-07-05`, no `/restart` mentions)
  even after four confirmed commits landed on `origin/main`. Expected
  CDN behavior, not a bug in `/restart` or the repo — but worth knowing:
  **if a Claude.ai session's `/restart` shows no drift right after a
  push, that isn't proof the push isn't reflected yet; cross-check with
  a live `git log` on jhm-spark if the timing is tight.**

### Still open going into next session
- `install.sh` live-tested on one real server
- Partner's `ares-contract.schema.json` checked against `resourceLinks`
- Tracking/attribution for the lesson-plan module link (scoped as
  separate task, not started)
- Full refresh of this file's Summary/per-subject lesson-count tables
- Kenyan-terminology wording pass (blocked on teacher-provided examples)
- Grade 11 STEM expansion, then non-STEM subject expansion (both not started)

---
## Updates — 2026-07-30 — New STEM subjects Phase 3 completed (resumed after interruption)

A prior session had gotten partway through `HANDOFF_new_stem_subjects_2026-07-28.md`
Phase 3 (full-batch generation of General Science / Core Mathematics / Essential
Mathematics, 43 sub-strands / 344 lessons) and was interrupted mid-flight. This
session used `/restart` to reconstruct exactly where it had left off from git
history, file mtimes, and the handoff document, then finished the phase.

### What the interrupted session had already done
- Phase 2 pilots (`gensci_1_3`, `coremath_2_2`, `essmath_2_8`) generated and
  passing `check_new_subjects_quality.js`.
- A real bug found and fixed in `src/generate_substrand.py`: `args.subject
  .capitalize()` mangled `general_science` → `General_science` instead of
  `General Science`. Fixed via a new `_subject_display()` helper.
- A retroactive patch (`/tmp/fix_subject_labels.js`, not committed — ad hoc)
  had corrected the 3 pilots' `META.subject`/`filePrefix`/`titleDoc`, but
  **missed the nested `UNIT.subject` field**, which feeds the "Subject:" row
  in the Lesson Sequence docx (`generators/lib/sections.js`).
- Because `filePrefix` changed, the pilots' old docx/json were deleted in
  prep for regeneration but `generate.js` was never re-run — they had zero
  output files at the point of interruption.
- Phase 3 had already run live generation for the remaining ~40 sub-strands,
  all of which inherited the same `UNIT.subject` bug.
- One sub-strand (`gensci_1_6`) had a leftover, already-`ended`
  (9/9 succeeded) batch checkpoint from an earlier abandoned batch attempt,
  superseded by a live run.

### What this session found and fixed on top of that
- **`UNIT.subject` bug**: extended the fix to all 43 data files (source of
  truth: each file's already-correct `META.subject`). Quality gate re-ran
  clean afterward.
- **`gensci_1_6` missing Final Explanation entirely** (`FINAL_EXPLANATION`
  absent) — generated via the API and patched with `scripts/patch_fe.js`.
- **34 stub lessons across 14 General Science sub-strands** (`gensci_1_2`,
  `1_4`, `1_5`, `1_6` [all 8 lessons], `1_7`, `2_1`–`2_5`, `3_1`–`3_4`) —
  the documented "Batch API — JSON truncation" failure mode, at larger
  scale than previously seen. Core Mathematics and Essential Mathematics
  were completely unaffected. Repaired all 34 via the `patch_lesson.js`
  workflow (individual API calls per stub, same pattern as
  `scripts/repair_stubs.py`).
- Removed the orphaned `.gensci_1_6_batch_id.{json,txt}` checkpoint files
  (batch already collected).

### Verification before commit
- Full stub/FE/ST scan across all 43 new sub-strand data files: clean —
  no stubs, FE and ST present for all.
- `node check_new_subjects_quality.js`: PASS.
- `node generators/generate.js --all`: 0 errors, all 43 new sub-strands
  produced 4 files each (docx ×3 + json).
- `node generators/generate_pdfs.js`: 255 converted, 0 failed.
- `node generators/generate_teacher_index.js`: 7 subjects, 85 sub-strands,
  255 documents indexed.

### Committed and pushed
- `f6d6fab` on `main` (649 files: all General Science / Core Mathematics /
  Essential Mathematics docx+json+PDF, the fixed `generators/data/*.js`
  files, `src/generate_substrand.py`). Confirmed pushed to `origin/main`.

### Still open going into next session
- Full refresh of this file's Summary/per-subject lesson-count tables
  (already stale before this session; now further behind since it doesn't
  reflect the new subjects at all)
- Whether to formally verify the 43 sub-strand names against the
  replacement Core Mathematics PDF referenced in the handoff (never
  supplied to jhm-spark) — generation proceeded on the original curriculum
  text without it
- Everything else listed in the previous session's "still open" list above
  (install.sh live test, partner schema check, terminology pass, Grade 11
  expansion, etc.) — untouched by this session

---
## Updates — 2026-07-30 (continued) — Process retrospective and fixes

Mark asked for a retrospective on three concerns from the session above:
the resume-and-repair work took much longer than expected, API cost ran
well over the documented estimate, and the session needed more approval
round-trips than felt warranted. Root cause in all three cases: the one
automated gate this project had (`check_new_subjects_quality.js`) only ever
checked the 3 Phase-2 pilots, so it reported "PASS, safe to proceed" while
structurally blind to the 40 sub-strands Phase 3 actually generated. Fixes:

- **`check_new_subjects_quality.js` rewritten** (commit `bb0faf9`) to glob
  every `gensci_`/`coremath_`/`essmath_` data file instead of naming a fixed
  list, plus a new check (#6: `META.subject` == `UNIT.subject`) added to
  catch the exact partial-patch bug this session hit earlier. Widening the
  gate immediately proved the point: it surfaced a real, previously
  undetected defect — **39/43 files had non-canonical phase-label formats**
  (e.g. `"Phase 1 — PREDICT (15 minutes)"` instead of the locked
  `"Predict Phase"`). Not cosmetic: `generators/lib/sections.js` keys ARES
  resource-category matching and row-color lookups off that exact string,
  both with silent fallbacks — so 1195 rows across the new corpus were
  silently getting the wrong ARES resource bucket and default grey shading.
  Fixed as a zero-cost deterministic remap (verified safe: every lesson's
  framework array has exactly 5 entries, self-numbered 1-5 matching array
  position in all 344 lessons) — no regeneration/API cost needed, just
  docx/PDF re-render. Committed and pushed as part of `bb0faf9`.
- **`WORKFLOW.md`** (commit `9d0d373`): `--batch` is now a hard default
  beyond a 1-3 sub-strand pilot (was "preferred") — `--run` is 2x batch
  pricing and a resumed session can otherwise silently inherit whatever
  mode the interrupted session was using. Added a 15-20% repair-pass
  contingency to the cost estimate table, since the documented ~$114
  figure assumed zero-defect generation and this run's actual defect rate
  (34 stub lessons + 1 missing FE + 1195 mislabeled rows, all repaired via
  extra live-mode calls) was well above zero.
- **`src/generate_substrand.py`** (commit `9d0d373`): now tracks real token
  usage (sync and batch) per run and logs it with an estimated cost to the
  new `logs/api_cost_log.md`, so future cost estimates can be checked
  against this pipeline's actual observed spend instead of a generic table.
- **`CLAUDE.md`** (commit `9d0d373`): added an "Autonomy checkpoints" policy
  to the Project Rigor Assessment section — for resume/repair/extend tasks,
  ask once up front whether to keep fixing-and-regenerating on standing
  authorization vs. check in per discovery, instead of re-asking separately
  each time a new problem of the same kind turns up. Level 2/3 phase-
  boundary checkpoints are unaffected by this.

### Still open going into next session
- Whether actual spend on the next bulk run tracks the new 15-20%
  contingency, or whether the estimate itself needs further revision
  (check `logs/api_cost_log.md` once there's another real run to compare)
- Everything else already listed above (Summary/per-subject table refresh,
  Core Mathematics replacement-PDF verification, install.sh live test,
  partner schema check, terminology pass, Grade 11 expansion)

---
## Updates — 2026-07-31 (triggered by `/restart`, then `/update`)

No generation, repair, or content work this session. A `/restart` was run
to re-ground a fresh session; it found real drift, and this entry closes it.

### `/restart` live checks — all clean, don't re-run without cause
- Branch `main`; working tree clean; `HEAD` == `origin/main` == `9937ed3`.
- `soffice` present at `/usr/bin/soffice`.
- `outputDir` across all 85 `generators/data/*.js` files: every value under
  `v2/<Subject>/<SubStrand>`. No stale `data/outputs/docx/` paths remain in
  any data file.
- `WORKFLOW.md` Environment Reference (line 315) matches all of the above.

### Drift found and fixed by this entry
- Three commits were on `origin/main` with no record in this file:
  `8d3fe16` (token-optimizer plugin marketplace, project scope),
  `1f4f6f8` (tooling-defect fixes: stale `.claude/commands/commit.md`
  rewritten — it was carried over from an unrelated project and told
  sessions to put status in `CLAUDE.md`, directly contradicting this
  project's rule; missing YAML frontmatter added to
  `.claude/skills/restart/SKILL.md`; 6 narrow Read deny rules added),
  and `9937ed3` (code-review-graph 2.3.7 installed, MCP server + 4 skills
  + `CLAUDE.md` section + hooks). All three now have Active Threads rows.
- Both `STATUS.md` and `CLAUDE.md` had `Last updated: 2026-07-05` headers
  despite carrying much newer content. This file's header corrected to
  2026-07-31; `CLAUDE.md`'s corrected in the same commit, along with its
  Repository Layout section, which listed neither `.claude/skills/restart/`
  nor the four graph skills.
- Two Known Issues entries added — see "Continuity rule held for content
  work, lapsed for tooling work" and "Third-party installers can append
  behavioral instructions to `CLAUDE.md`."

### Still open going into next session
- **Scope the code-review-graph `CLAUDE.md` wording** (new this session) —
  "ALWAYS use graph tools before Grep/Glob/Read" is unreviewed third-party
  text and is wrong for `.md` control docs and `*_data.js` modules.
- **Full refresh of the Summary/per-subject lesson-count tables** — now
  quantified: tables say 12/33 across 4 subjects, disk has 85 across 7.
  Longest-standing open item in this file (flagged since 2026-07-05).
- Whether actual spend on the next bulk run tracks the new 15–20%
  contingency (`logs/api_cost_log.md` — no new run since it was added).
- Core Mathematics replacement-PDF verification (PDF never supplied).
- `install.sh` live test on one real ARES server.
- Partner's `ares-contract.schema.json` checked against `resourceLinks`.
- Kenyan-terminology wording pass (blocked on teacher-provided examples).
- Tracking/attribution for the Grade 10 module link.
- Grade 11 STEM expansion, then non-STEM expansion.

---
## Updates — 2026-07-31 (second entry) — code-review-graph wording scoped

Closed the "needs scoping" item opened earlier today. No code or content
changed; `CLAUDE.md` + `STATUS.md` only.

### Measured graph coverage — verified, don't re-derive
- Indexed: **exactly the 183 tracked `.js`/`.py`/`.sh` files** (`git ls-files
  '*.js' '*.py' '*.sh' | wc -l` == 183 == graph `files_count`).
- **0 of 52 tracked `.md` files indexed** — languages are python/bash/
  javascript only. Every control document in this project is invisible to
  the graph.
- All 85 `generators/data/*_data.js` are indexed as bare `File` nodes with
  no contained functions — they export object literals, so there is no call
  graph to build. The graph knows these files exist and nothing about what
  is in them.
- `embeddings_count` == 0, so `semantic_search_nodes_tool` silently falls
  back to FTS keyword matching (`search_mode: "fts"` in its own response).
  It is a symbol lookup, not concept search.
- 1 `Test` node repo-wide. `query_graph_tool` pattern="tests_for" cannot
  function as a coverage signal here in either direction.

### What changed in `CLAUDE.md`
- The blanket "ALWAYS use graph tools BEFORE Grep/Glob/Read" replaced with
  a scoped rule: prefer the graph for executable-code questions, and a
  "What the graph does not cover" section listing the three blind spots
  above. Explicitly states that reading `STATUS.md`'s Active Threads — this
  project's mandatory first action — is a plain `Read` with no graph
  substitute, which the original wording implicitly discouraged.
- Notes that past data-integrity bugs (stub lessons, `UNIT.subject`
  mismatch, phase-label drift) were all found by `Read`/`grep` over data
  files, precisely the reads the original wording deprioritized.
- Workflow step 4 (`tests_for` coverage check) struck through with a
  pointer to the caveat.
- A short provenance banner marks the section as installer-generated and
  hand-scoped, so a future reader doesn't mistake it for original policy.

### Still open going into next session
- **Full refresh of the Summary/per-subject lesson-count tables** — now the
  longest-standing open item (flagged 2026-07-05); 12/33 across 4 subjects
  on paper vs. 85 across 7 on disk.
- Everything else from this morning's entry is unchanged: cost-contingency
  check against `logs/api_cost_log.md`, Core Mathematics replacement-PDF
  verification, `install.sh` live test, partner schema check, terminology
  pass, module-link tracking, Grade 11 expansion.

---
## Updates — 2026-08-02 — Partner-reported General Science defects repaired

Mark's partner, who is building a teacher-facing lesson-plan editor with a
validating importer, ran our JSON export through his checker and found two
defect classes. Saved to `Gnerator_issues.txt` at the repo root (filename is
misspelt — no `e` — worth knowing if you go looking for it).

### What was reported, and what was actually true
- **35 `slo` keys corrupted to `safety<N>otes`** across 15 `gensci_*` files
  (partner found the pattern; confirmed on disk, digit always == lesson number).
- **2 lessons missing `summaryTablePrompt.explained`** (`gensci_2_2` L5,
  `gensci_3_2` L7). Confirmed as exactly 2, corpus-wide.
- Both General Science only. Bio/Chem/Physics/Maths/Core/Essential clean.
- **One root cause for both, and it is the repair path, not the generator.**
  `src/generate_substrand.py` has a strict tool schema (`additionalProperties:
  False`, all 3 `summaryTablePrompt` fields required) and could not have emitted
  either defect. `repair_stubs.py` / `patch_lesson.js` send a prompt-string
  schema with **zero** validation. Confirming evidence: both
  `explained`-missing lessons are also in the corrupted-key set — i.e. both are
  repaired-stub lessons from the 2026-07-30 pass.

### Two things worse than reported
1. **The 35 lessons had a silently blank Safety Notes row in the distributed
   docx and PDFs.** The partner's checker sees JSON, so it couldn't see this.
   Details and the general lesson in Known Issues above.
2. **This bug had already been fixed once, on symptoms only** (`3b75018`), and
   re-fired. See Known Issues.

### What was done
- `scripts/repair_stubs.py`: bare `N` placeholder → `{{LESSON_NUMBER}}`.
- Re-ran the existing `scripts/fix_safetynotes.py` over `generators/data/`:
  35 keys repaired. Verified the diff is *purely* key renames — 35 lines
  changed, 0 differing by anything other than the key name, so no safety text
  was altered.
- Regenerated `summaryTablePrompt` for the 2 lessons via 2 live API calls
  (`claude-sonnet-4-6`, the project's documented model, for voice consistency),
  using a forced tool schema. **Three review iterations were needed** and this
  is the useful part: pass 1 cited the wrong lesson numbers; pass 2 fabricated a
  verbatim "Driving Question Board note" quotation that appears nowhere in the
  lesson. Added grounding rules (authoritative numbered lesson list, no
  quotation marks at all) plus a programmatic reject for quote marks and
  unresolvable lesson citations. **Do not accept generated cross-references or
  quoted material into teacher-facing content without checking them against the
  source lesson — two of three passes had a fabrication a reader could not have
  spotted.**
- Contract validation added at the chokepoint (`scripts/patch_lesson.js`) and
  corpus-wide (`scripts/validate_corpus.js`, new). Both tested against all
  three real defect shapes; each is refused with a diagnostic and nothing is
  written.
- Re-rendered the 15 affected sub-strands, then all PDFs + teacher index.

### Verification
- `node scripts/validate_corpus.js gensci_` → PASS (16 files / 128 lessons).
- `node check_new_subjects_quality.js` → PASS, all 43 files (existing gate
  unbroken).
- Corpus-wide JSON re-scan, matching the partner's own three checks:
  85 files parse, **0** `safety*otes` keys, **0** missing `safetyNotes`,
  **0** missing `summaryTablePrompt.explained`.
- `generate_pdfs.js`: 255 converted, 0 failed. Teacher index: 7 subjects,
  85 sub-strands, 255 documents.
- Confirmed end-to-end at the *rendered* layer, not just the data layer:
  `gensci_1_6`'s 8 previously-empty Safety Notes rows now carry their text in
  both the docx and the extracted PDF text.

### Note on the diff size
335 files changed, but only 15 `generators/data/*.js` are source. All 255 PDFs
show as modified because `generate_pdfs.js` has no incremental mode — it
re-converts the whole tree, so unchanged subjects get byte-different PDFs.
Harmless, but it makes the commit look far larger than the change.

### Still open going into next session
- **`chem_1_2` L2 and `math_2_3` L2 phase composition** (new; needs a content
  judgment call, see Active Threads) and **`phys_3_1` L6 `aresKeywords`** (new,
  minor).
- Whether the partner's `ares-contract.schema.json` also needs the
  `resourceLinks` check closed out — still unconfirmed, and now more relevant
  since his importer is clearly doing real schema validation.
- **Full refresh of the Summary/per-subject lesson-count tables** — still the
  longest-standing open item (flagged 2026-07-05); 12/33 across 4 subjects on
  paper vs 85 across 7 on disk / 728 lessons.
- Everything else unchanged: cost-contingency check against
  `logs/api_cost_log.md`, Core Mathematics replacement-PDF verification,
  `install.sh` live test, terminology pass, module-link tracking, Grade 11
  expansion.

---
## Updates — 2026-08-02 (second entry) — ares.local restored; chem/math/phys fixes

Continuation of the same session. Mark authorised commit+push of the General
Science repair (`ff1bec4`), then asked for the three remaining open defects to
be fixed. Doing that surfaced a much larger, unrelated regression.

### The three requested fixes (all done, `9b33dce`)
- **`phys_3_1` L6 `aresKeywords`** — written from that lesson's own content.
  Corrected my own earlier claim: the missing field did not disable ARES lookup
  (`sections.js:151` falls back to `lesson.title`), it just weakened it.
- **`chem_1_2` L2 and `math_2_3` L2** — regenerated (2 API calls). The tool
  schema now pins each of the five phase labels with `const`, so the model
  cannot emit a duplicate or mislabelled phase at all. Activities re-homed to
  the phase they actually belong to; `math_2_3` gained the genuine Model
  Building step it never had.
- **`patch_lesson.js --force`** — needed because the stub guard (correctly)
  refuses lessons that already have content. Skips that guard only; contract
  validation still runs.

### The regression found while verifying the above
Checking `phys_3_1`'s regenerated `resourceLinks` showed `http://ares.edu:...`.
**The whole `ares.local` migration had been silently reverted on 2026-07-30**
and every distributed docx/PDF since then carried dead resource links. Full
root-cause writeup in Known Issues ("A default that contradicts a completed
migration will silently undo it"). Fixed at the source, corpus regenerated,
verified 0 `ares.edu`.

Worth recording that I nearly mis-attributed this: my first read was that I had
introduced it with the day's regenerations. Checking `35bf147` for a Biology
file I had never touched showed 280 `ares.edu` already present, which is what
pointed at `f6d6fab` and the default. **When a regression appears right after
your own change, bisect a file your change did not touch before concluding
anything.**

### Verification (after the full-corpus regeneration)
- `node scripts/validate_corpus.js` → **PASS**, 85 files / 728 lessons, 0
  errors, **0 warnings** (the `aresKeywords` warning is now gone too).
- `node check_new_subjects_quality.js` → PASS, all 43 files.
- Partner's three checks, corpus-wide: 0 `safety<N>otes`, 0 missing
  `safetyNotes`, 0 missing `summaryTablePrompt.explained`.
- Phase composition: 0 non-canonical across all 728 lessons.
- Hostnames: 0 `ares.edu`; 25,480 `ares.local` URLs in JSON; 14,560
  `ares.local` hyperlinks across the 85 Lesson Sequence docx; PDFs spot-checked
  in Biology / General Science / Maths, 0 `ares.edu`.
- `generate_pdfs.js`: 255 converted, 0 failed. Index: 7 subjects, 85
  sub-strands, 255 documents.
- `HEAD` == `origin/main` == `9b33dce`, working tree clean.

### Two things Mark should decide on
1. **The distributed PDFs on the ~100 school servers are stale.** Everything
   deployed between 2026-07-30 and today has `ares.edu` links that fail behind
   a school router. The corpus is fixed here, but the provisioning payload
   needs rebuilding and redeploying — `install.sh` has still never been
   live-tested either.
2. **Tell the partner.** His importer found the two General Science defects; he
   has not seen the hostname regression, and if he has imported anything since
   2026-07-30 his copy has `ares.edu` links. Also still unconfirmed whether his
   `ares-contract.schema.json` accepts the `resourceLinks` field at all.

### Still open going into next session
- The two items above (school-server redeploy; partner notification + schema
  confirmation).
- **Full refresh of the Summary/per-subject lesson-count tables** — still the
  longest-standing open item (flagged 2026-07-05). Authoritative numbers as of
  today: **85 sub-strands, 7 subjects, 728 lessons, 255 documents.**
- Cost-contingency check against `logs/api_cost_log.md` (today's spend was ~4
  small live calls, not a bulk run, so still no comparison point).
- Core Mathematics replacement-PDF verification; `install.sh` live test;
  Kenyan-terminology pass; module-link tracking; Grade 11 expansion.

---
## Updates — 2026-08-02 (third entry) — sync_to_drive.bat actually written

Mark asked what commands the Windows box needs besides `git pull`. Answering
that surfaced the **fourth** stale-fact instance of the day, and the most
pointed one.

### `scripts/sync_to_drive.bat` never existed
Three places asserted it did — `CLAUDE.md:95` (Repository Layout), this file's
"Documentation drift" Known Issues entry ("*is now committed as
`scripts/sync_to_drive.bat`, so its actual configured destinations are
`grep`-able from jhm-spark*"), and the 2026-07-04 session log ("*tracked in
`scripts/sync_to_drive.bat`*"). No `.bat` was tracked in git or present on disk.

The sting: committing that file was written up as one of the *structural fixes
for stale facts* inside the very entry about stale facts. **A remediation
recorded as done, but never done, is worse than one recorded as open** — it
actively suppresses the re-check that would have caught it.

### Written now, from the surviving spec
`WORKFLOW.md` Step 8 and `docs/PDF_GENERATION.md` did preserve the destinations
and the rationale, so the script was reconstructed rather than guessed. Masks
verified against the real trees first: docx tree is exactly 255 `.docx` + 85
`.json`; PDF tree is 255 `.pdf` + 1 `.html`.

Design decisions worth keeping:
- **docx job uses `/E`, not `/MIR`.** That destination is the editable master
  ("anyone doing manual content edits"), so `/PURGE` there could delete a
  human's file. Accepts stale-file accumulation as the cheaper failure.
- **PDF job uses `/MIR` with no file mask.** Pure generated output where
  sub-strand renames orphan files, so purging is wanted. **No mask is
  deliberate:** `/MIR` plus a file mask is a robocopy trap — source files the
  mask excludes count as absent, so `/PURGE` can delete destination files that
  do not match it. Dropping the mask removes that failure mode *and*
  structurally guarantees `index.html` syncs, which the old masked job had to
  remember separately or silently skip.
- `preview` argument runs both jobs with `/L` — writes nothing, and lists what
  `/MIR` would delete. Mark was unsure about `/MIR` vs `/E`; this makes the
  answer checkable instead of trusted.
- `/FFT` because Google Drive's virtual filesystem otherwise re-copies every
  unchanged file each run; `/R:2 /W:5` instead of robocopy's 1,000,000 retries.
- Pre-flight aborts if the source PDF tree or `G:\My Drive` is missing —
  without that, a mirror job against an absent source purges the destination.
- Exit codes: robocopy 0–7 are success, ≥8 is failure; the script reports both
  jobs and returns 1 only on a real failure.

### Also added
- **`.gitattributes`** with `*.bat text eol=crlf`. The repo is authored on Linux
  and the script runs on Windows; `cmd.exe` can mis-parse labels and `goto` in
  an LF-only `.bat`, failing at runtime rather than parse time. Scoped to
  `*.bat` only — a blanket `* text=auto` would renormalise every tracked file
  and show up as hundreds of spurious modifications.
- `.gitignore`: `logs/sync_to_drive_*.log` (machine-local run logs) and
  `.claude/settings.local.json.tmp.*`.
- **WORKFLOW.md Environment Reference** gained rows for the sync script, both
  Drive destinations, and the ARES hostname. `CLAUDE.md` already declared that
  table the single source of truth for "sync destinations" — it had none.

### Not verified, and cannot be from here
**The script has never been run.** It is reconstructed from documentation, and
`robocopy`/`cmd.exe` do not exist on jhm-spark. Static checks only: balanced
`if` blocks, `goto :failed` resolves, 2 robocopy calls, git stores LF and will
check out CRLF. **Mark should run `scripts\sync_to_drive.bat preview` on the
Windows box first** and confirm the destinations and the `/MIR` delete list look
right before running it for real. If the original job used different masks or
`/MIR` on the docx side, this changes behaviour — the preview will show that.

---
## Updates — 2026-08-02 (fourth entry) — school-server payload written

Mark asked to proceed with the Windows sync (his to run — jhm-spark has no
`robocopy` and no `G:` drive) and with rebuilding the school-server payload.

### `install.sh` did not exist either
Recorded here as "Built, not yet tested live" since 2026-07-05. Searched
jhm-spark: not in the repo, not in git history, not in `~/Downloads` (which
holds only older unrelated handoff material), no zip anywhere. **Fifth**
stale-fact instance of the day, and the second deliverable in a row that the
docs asserted existed and could not be produced.

The spec survived in this file and `docs/PDF_GENERATION.md`, so it was
reconstructed rather than guessed:
`deploy/install.sh`, `deploy/ares-mdns-alias.sh`, `deploy/ares-mdns-alias.service`,
plus `scripts/build_school_payload.sh` to assemble the zip.

### Two decisions that outlast this session
- **A builder, not a hand-made zip.** The old payload was assembled by hand and
  never committed, so its contents were unverifiable after the fact. The builder
  writes `MANIFEST.txt` into every build recording git commit, PDF count and
  verified link host.
- **The `ares.edu` check is a hard gate, not a warning.** `build_school_payload.sh`
  refuses to build if any PDF references `ares.edu`. That is precisely the check
  whose absence let a corpus-wide dead-link regression ship undetected for three
  days: such a payload installs cleanly and fails silently on every school
  network. Warnings get skimmed; a refusal does not.
- **The deployed `generate_teacher_index.js` is derived, not duplicated.** It is
  produced by rewriting `PDF_ROOT` to `__dirname`, with an assertion that the
  rewrite took. The 2026-07-05 entry below notes the two copies must
  legitimately differ with "no automated sync between them" — that drift is now
  structurally impossible.

### What was verified, on jhm-spark
`bash -n` clean; build produces `dist/ares-cbe-payload-20260802.zip` (42MB,
255 PDFs + index.html, `0755` preserved on both shell scripts, manifest pinned
to `6ef2e6e`); `ares.edu` gate passes; `PDF_ROOT` assertion holds; `install.sh`
refuses cleanly as non-root, rejects unknown args, `--help` works; the nginx
logic was exercised against a synthetic ares-style config — config detection,
web-root extraction (`/var/www/ares`), `server_name` patch preserving
`ares.edu`/`www.ares.edu`, and the already-present idempotency guard all behave
correctly; `primary_ip` returns this box's LAN address. `dist/` is gitignored
(42MB would breach the 50MB pre-push check).

One bug found and fixed during testing: `set -o pipefail` plus `grep` returning
1 on zero matches aborted the builder **on the success path**. Worth remembering
— a "no matches" grep inside a pipeline is a script-killer under `pipefail`.

### NOT verified — this is the remaining risk
**`install.sh` has never run against a real ARES server**, as root, with live
nginx and avahi. It edits nginx config and installs a systemd unit. It is
idempotent, backs up to `/var/backups/ares-cbe-<stamp>`, and rolls back the
nginx change if `nginx -t` fails — but that is design, not evidence.

Procedure for Mark, on ONE server first:
```
unzip ares-cbe-payload-20260802.zip && cd ares-cbe-payload-20260802
sudo ./install.sh --dry-run     # read this output before going further
sudo ./install.sh
```
Then test `ping ares.local` **from a different device on the same network** —
resolving it on the server itself proves almost nothing about mDNS.

### Still open going into next session
- **`install.sh` live test on one server** (unchanged in substance since
  2026-07-05, but now there is an actual script to test).
- **`deploy/index.htmlf`** — the module landing page was never recoverable. If
  Mark still has it, dropping it at `deploy/index.htmlf` makes the installer
  deploy it; otherwise the installer leaves each server's existing page alone.
- **Windows Drive sync** — Mark to run `scripts\sync_to_drive.bat preview` then
  the real thing.
- **Partner notification** — the two reported defects are fixed, but he has not
  been told about the `ares.edu` regression, and the `resourceLinks` schema
  question is still unanswered.
- **Summary/per-subject lesson-count table refresh** — authoritative numbers are
  85 sub-strands / 7 subjects / 728 lessons / 255 documents.

---
## Updates — 2026-08-02 (fifth entry) — lesson-count tables refreshed

Closed the longest-standing open item in this file, flagged stale since
2026-07-05. The Summary and all per-subject tables are now derived from disk.

### Authoritative numbers
**7 subjects, 85 sub-strands, 728 lessons, 340 output files + 255 PDFs + 1
index.html.** All 85 complete — 4 files each (3 docx + `_data.json`) and 3 PDFs
each, no partial sets. Per subject: Biology 9/90, Chemistry 7/67, Physics
12/101, Mathematics 14/126, General Science 16/128, Core Mathematics 14/112,
Essential Mathematics 13/104.

Derived from `generators/data/*_data.js` (source of truth), then re-derived by a
second independent method — counting directories and files under
`data/outputs/v2/` and summing `LESSONS` across the 85 JSON exports. Both
methods agree exactly.

### The old tables were not a stale version of these
Worth stating plainly, because "just update the numbers" would have been wrong:
- Chemistry and Physics were headed **NOT STARTED** while both are fully
  generated (67 and 101 lessons).
- General Science, Core Mathematics and Essential Mathematics did not appear at
  all — 43 sub-strands / 344 lessons missing from the document.
- **Biology's sub-strand numbering had been renumbered.** The old table's 1.1
  "Introduction to Biology" and 1.4 "Chemicals of Life" do not map onto today's
  1.1 Cell Structure / 1.2 Chemicals of Life. Old and new IDs are not
  comparable, so no row-by-row reconciliation was possible or attempted.
- The old Mathematics table described `math_2_2`/`2_3`/`2_4` as legacy
  pre-pipeline output; all 14 are standard pipeline output now.

### Structural change, not just a data refresh
The Summary section now carries the two commands that re-derive these numbers
(`scripts/validate_corpus.js` and an `outputDir` count). This file has been
burned repeatedly by counts that were true when written — the point is that the
next reader can *check* in five seconds instead of trusting a date. `CLAUDE.md`'s
pointer to this section was updated in the same pass; it still told readers the
tables needed a refresh.

Deliberately left alone: the **Cost Tracking** table below still projects from
~110 sub-strands / ~2,000 lessons and per-run figures from May–June 2026. It is
a forecast, not a state snapshot, and revising it needs real spend data from
`logs/api_cost_log.md` — which has had no bulk run since it was added. Flagging
rather than improvising.

### Still open
Unchanged from the previous entry: `install.sh` live test on one server;
`deploy/index.htmlf` if Mark still has it; Windows Drive sync run; partner
notification + `resourceLinks` schema confirmation; Core Mathematics
replacement-PDF verification; cost-contingency check once there is another bulk
run; Kenyan-terminology pass (blocked on teacher examples); Grade 11 expansion.

---

## Updates — 2026-09-19 — grade-aware pipeline (handoff Rev 1, Phases 0–3)

Worked from `HANDOFF_grade_aware_pipeline_2026-09-18.md`, which arrived via
`git pull` (`f5bb508`) along with two patches. Phases 0–3 done; **stopped
before Phase 4** (curriculum extraction + pilot generation) pending Mark's
go-ahead, per the handoff's own instruction and because Phase 4 crosses into
Grade 11 content ahead of the terminology pass.

### What was wrong
The pipeline assumed Grade 10 everywhere, because only Grade 10 existed when
it was written. Surfaced by the partner's Lesson3 editor flagging three
hardcoded `GRADE 10` strings in `build_docs.js`; those turned out to be the
visible tip.

The one that mattered: **`SUBSTRAND_NAMES` was keyed by subject only, not by
grade.** Grade 11 reuses Grade 10's strand/sub-strand numbering with different
topics, so `--grade 11 --subject biology --substrand 2.1` would have looked up
Grade 10's "Plant Nutrition" instead of Grade 11's "Reproduction in Plants",
fed that into the generation prompt, and produced a complete, coherent lesson
sequence **about the wrong topic, labelled GRADE 11**. Not a wrong label — 
wrong content. Nothing would have failed or warned.

### Applied
- `a546ee3` — `build_docs.js` reads `META.grade`. No `|| 10` fallback: a
  missing grade throws rather than printing a plausible-but-wrong grade on a
  student assessment. All 85 data modules already carry `"grade": 10`
  (verified), so Grade 10 is unaffected.
- `77f3591` — `generate_substrand.py` grade-aware throughout; `--grade`
  required with no default. `SUBSTRAND_NAMES`, `LESSON_COUNTS`,
  `CURRICULUM_PDF_MAP`, `CURRICULUM_TEXT_MAP` all nested by grade first.
- `da26382` — `generate_teacher_index.js` walks both tree shapes.

### Phase 3 was changed, deliberately
The handoff called for migrating existing Grade 10 output under
`v2/Grade10/`. Mark reconsidered (the original "same convention per grade"
decision was offhand, not considered): Grade 10 is stable, and migrating
churns teacher-visible Drive paths — job 2 of `sync_to_drive.bat` is `/MIR`,
so it would delete and re-upload all 255 PDFs — for no benefit today.
Deferred to the next full-corpus regeneration so the churn is paid once.

**The migration was never what bought correctness.** The actual defect was
that `generate_teacher_index.js` did a fixed two-level walk: Grade 11 sitting
one level deeper would have been read as subject=`Grade11`,
sub-strand=`Biology`, yielded no PDFs at that depth, and been dropped by the
existing empty-group guard — **an index.html with all of Grade 11 silently
missing, no error.** Same failure shape as the `SUBSTRAND_NAMES` bug. That fix
was needed whether or not Grade 10 moved; migration only decided whether the
walker is uniform or carries a documented exception.

### Verified, not assumed
- Both patches applied clean against live `main` (Phase 0 found no drift).
- Grade 10 end-to-end: regenerated `bio_1_1`, extracted the docx XML, confirmed
  it still renders `FINAL EXPLANATION: BIOLOGY GRADE 10` / `SUMMARY TABLE:
  BIOLOGY GRADE 10`. Output churn reverted afterwards.
- Teacher index: regenerated and **diffed byte-for-byte against the committed
  `index.html` — identical apart from the generated-at timestamp.** Then built
  a stub `v2/PDF/Grade11/Biology/SS2.1_.../` tree, confirmed it renders with
  correct `Grade11/`-prefixed hrefs and that grade appears as a browsing
  dimension only when >1 grade exists, then removed the stub.
- `LESSON_COUNTS` confirmed **unread repo-wide** (only its definition site) —
  resolves the handoff's §8 open question. It is genuinely inert.
- `--grade` enforced by argparse; grade 10 vs 11 produce distinct system
  prompts and distinct output dirs; `SUBSTRAND_NAMES[11]` does not leak
  Grade 10 names.

### Two corrections to the handoff
- Its §5 test claim `SUBSTRAND_NAMES[11]['biology'].get('2.1') → None` is
  wrong — `SUBSTRAND_NAMES[11]` is empty, so that expression raises
  `KeyError`. The **live code** is fine; it uses `.get()` chains and prints a
  visible WARNING. Only the handoff's stated test was wrong.
- Its §3/§5/§10 promise full corrected `build_docs.js` and
  `generate_substrand.py` as a fallback "if the patch doesn't apply cleanly."
  Those files were **not** in the pull — only the two patches. Moot here
  (both applied clean), but the stated fallback did not exist.

### Deviation from the supplied patch
`_v2_output_dir()` keeps Grade 10 flat. The patch emitted `v2/Grade10/...`
unconditionally, which would have created a **third** tree shape the first
time an existing Grade 10 sub-strand was regenerated, since all 85 data
modules hardcode the flat `outputDir`.

### Still open
- **Phase 4 not started** — needs an explicit go-ahead, and it starts Grade 11
  content ahead of the still-blocked terminology pass.
- Phase 4 will hit a rough edge: with `CURRICULUM_PDF_MAP[11]` empty, the
  fallback at `generate_substrand.py:1544` resolves to an empty path and
  `extract_curriculum_pdf` fails on the project root — a confusing error
  rather than a clear "grade 11 curriculum source not registered". Worth a
  guard before the pilot.
- **Phase 4 explicitly held** — Mark's call, 2026-09-19. Not blocked on any
  technical problem; the plumbing is ready and waiting. Do not start OCR
  extraction or any Grade 11 generation without a fresh go-ahead.
- Pushed to `origin/main` 2026-09-19 (`f5bb508..3c6f1c4`), working tree clean.
- Unchanged from the previous entry: `install.sh` live test; `deploy/index.htmlf`;
  Windows Drive sync run; partner `resourceLinks` schema confirmation; Core
  Mathematics replacement-PDF verification; cost contingency; Kenyan-terminology
  pass (blocked on teacher examples).

---

## Updates — 2026-09-19 (second entry) — Grade 11 Biology extracted; pilot blocked on credits

Continues the entry above. Handoff Phase 4 is done apart from the pilot
generation run itself.

### Template lookup was a third instance of the same bug
`find_v2_templates()` was keyed by subject + sub-strand only, with no grade —
the same defect as `SUBSTRAND_NAMES`, and missed by the handoff patch.
`v2_owner_inventory/Biology/SS2.1_*` matched for **any** grade, so a Grade 11
run would have fed Grade 10's `SS2.1_Plant_Nutrition` template into generating
Reproduction in Plants. Now segmented like `_v2_output_dir()`. Also fixed
`st_args` on the collect path, which built a namespace with no grade at all.

That makes three sites found so far (`SUBSTRAND_NAMES`, `find_v2_templates`,
and the `build_docs.js` titles). The pattern is worth stating plainly: **any
lookup keyed by sub-strand number is suspect until proven grade-aware**,
because the numbering is stable across grades while the content is not.

### Curriculum-source guard
An unregistered grade/subject fell through `CURRICULUM_PDF_MAP` as an empty
path, resolved to `PROJECT_ROOT`, and failed inside the PDF extractor looking
like a broken parser. Now exits early naming the exact dict entry to add.

### The extraction script now exists
`scripts/extract_curriculum_ocr.py`. The Grade 10 run was done off-server and
**only ever written up in prose** — no script was committed, so the method had
to be rebuilt from `data/raw/curriculum_text/README.md` in order to run it
again. Same class of loss as `sync_to_drive.bat` and `install.sh`: documented,
believed to exist, absent. That README now points at the script instead of
describing commands to reconstruct.

### Grade 11 Biology
- `tesseract` was **not installed on jhm-spark** — the Grade 10 OCR never ran
  here. Installed 5.3.4 (needed sudo, so Mark ran it).
- Extracted: 17 slices @ 200 dpi, `--psm 4`, 53,129 chars / 1,281 lines. No
  dedup needed (no 400+ char duplicate blocks), matching General Science and
  Essential Mathematics at Grade 10.
- Verified: all 10 sub-strands findable by name *and* number; `SUMMARY
  STRANDS`, `STRAND 1.0/2.0/3.0`, `ESSENCE STATEMENT`, `APPENDIX` all present.
- **Inventory hand-read from rendered images** (page ix), per §6.5, then the
  document was read to its end to confirm nothing follows strand 3.0 but the
  appendix — i.e. no Strand 4.0 hiding past the summary table, which is a real
  possibility at Grade 11 (Core Maths has one).

**10 sub-strands vs Grade 10's 9, and not one shared number is the same topic:**

| # | Grade 10 | Grade 11 |
|---|---|---|
| 1.1 | Cell Structure | Taxonomy I |
| 1.2 | Chemicals of Life | Ecology |
| 1.3 | Cell Biology | Taxonomy II |
| 1.4 | *(none)* | Cell Division |
| 2.1 | Plant Nutrition | Reproduction in Plants |
| 2.2 | Plant Transport | Growth and Development in Plants |
| 2.3 | Plant Gaseous Exchange and Respiration | Excretion in Plants |
| 3.1 | Animal Nutrition | Reproduction in Animals |
| 3.2 | Animal Transport | Growth and Development in Animals |
| 3.3 | Animal Gaseous Exchange and Respiration | Excretion and Homeostasis in Animals |

That table is the concrete measure of what the subject-only lookup would have
produced: not one wrong sub-strand, but **every** one.

### API credits are exhausted — pilot cannot run
A verification command went further than intended and invoked a real API call
(it was meant to test the source-resolution guard only). It spent nothing,
because it failed immediately: `Your credit balance is too low to access the
Anthropic API`. No files written, no batch state created.

Worth recording rather than burying: it confirms the handoff's "confirm
account API access before Phase 4's pilot" precondition, which would otherwise
have been discovered at the moment of the pilot run itself.

### Still open
- **Pilot run** — needs API credits, plus Mark's Grade 11 Biology templates in
  `v2_owner_inventory/Grade11/Biology/` using **Grade 11** sub-strand names.
- Other five Grade 11 STEM subjects — extraction is one command each now, but
  each needs its own hand-verification pass.
- `LESSON_COUNTS[11]` not populated; still inert repo-wide, so this is
  future-proofing only.
- Unchanged: `install.sh` live test; `deploy/index.htmlf`; Windows Drive sync
  run; partner `resourceLinks` schema confirmation; Core Mathematics
  replacement-PDF verification; Kenyan-terminology pass (blocked on teacher
  *examples* — not the same thing as templates, see Active Threads).

---
## Updates — 2026-09-29 — Bounded project v2: Phase 0 + Phase 1 (design only)

Restarted after several weeks on hold. The handoff bundle (`handoff_bundle_2026-09-29.zip`)
has been extracted to `handoff_bundle_2026-09-29/` in the repo root. The partner schema
`ares-contract.schema.json` was supplied to the repo root.

### Phase 0 findings
- Repo identical to `origin/main` (`6ab9bef`); nothing to pull.
- No earlier link-fix work: no design doc, no recommender changes since `9b33dce`.
- Output convention unchanged: Grade 10 flat under `v2/<Subject>/`, new grades under `v2/Grade{N}/`.
- Partner schema is strict (`additionalProperties: false` at every level). **All 85
  current `_data.json` exports validate against it** (`jsonschema` installed into the venv
  for this check). Quiz data will therefore go in a separate `<prefix>_quiz.json`.
- Sample-naming discrepancy to confirm: the bundle's quiz samples call Pressure
  "Physics SS1.2"; in this repo Pressure is **SS1.1** (`phys_1_1`).

### Phase 1 — diagnosis (full write-up in `DESIGN_link_selection_v2.md`)
- Four cases traced against the live DB. Wrong-domain picks enter the pool through
  boilerplate or single weak words (`strand` from "Sub-Strand", `anchoring` from
  "Anchoring Phenomenon", a lone `semiconductor`). They win because ranking is by
  channel tier. The one relevance term, `hit_counts`, is looked up by the wrong key
  and is always 0.
- The answer key is a different root cause: it was on-topic, its exam-prep channel is
  in the top tier, and nothing excludes answer material.
- The audit script only checks the predict phase. Across all phases the Tier 1/2
  counts are 170/125, exactly 5× the handoff baseline.
- The handoff's regex `exam` would also match ~1,830 "example"/"examine" titles.
  The design uses word boundaries.
- No live Kolibri is reachable from jhm-spark. 262 of 542 shipped Kolibri IDs exist
  only in channel metadata and are unverified on a real server.

### Still open
- **Mark: review `DESIGN_link_selection_v2.md`** (gate before Phase 2).
- Top up API credits before Phase 3 (quiz generation).
- A server to live-check Kolibri IDs against (optional, see design §6).

### Phase 2 — link fix implemented (same day)
- Matcher rebuilt per the approved design, plus the changes in design §7:
  web modules are eligible if verified on the reference image (so SeaVuria
  videos and PhET sims can win), a wider exam exclusion list, whole-phrase and
  position-weighted relevance gate, and a floor on per-phase variety.
- Removed two more silent fallbacks in the render path (`aresResources.js`
  empty-on-error, `sections.js` stub module), both of which produced contract-
  invalid empty links. They now fail the render.
- Results, whole corpus (85 sub-strands, 7,280 slots):
  - New gate: T1 45→0, T2 166→0, DEAD 45→0, SHAPE 0.
  - Handoff audit (predict phase): T1 34→32 (all "worked example" titles —
    its regex's false positives; 0 real answer keys), T2 25→0, T3 174→28.
  - Hand check of 10 remaining Tier 3 rows: 0 real problems (1 weak but on topic).
  - Content diff: only `resourceLinks` changed in all 85 JSON files.
- **Content-library gaps** (share of slots with no confident match): Physics
  1.5 Moments 75%, Biology 3.1 Animal Nutrition 75%, Gen Sci 1.3 Nutrition in
  Animals 69%, Biology 3.2 Animal Transport 58%, Gen Sci 1.1 Intro 56%, Ess
  Maths 2.8 Commercial Arithmetic 50%, then 8 more sub-strands at 29–38%;
  41 of 85 have none. Some are true gaps; some would come back with synonym
  support ("torque" for moments). The gate is deliberately precision-first.
- PDFs and the teacher index are stale relative to the docx until Phase 5.

### Phase 2 follow-up (Mark's review: synonyms, demo server, hold push)
- Synonyms added: 51 strict-equivalent groups. See design §7.1 for the
  rejected candidates and why. Fill rate: Physics 88%, Biology 73%, General
  Science 78%, Chemistry 90%, the maths subjects 94–100%.
- **Found and fixed:** Phase 2's web-module links went through
  `/tracker/kiwix_launch.html`, which only accepts `/kiwix/` targets, so they
  would have shown "Invalid target". They are now direct `/modules/` links,
  and the checker rejects the old form.
- Live check against demo.aresedu.dev: 1,707/1,707 distinct links OK.
- Push held until Phase 5 (Mark), so PDFs and docx ship together.

### Phase 3 — quizzes + attribution (same day)
- Attribution from `config/attribution.yaml` in all three sub-strand docx
  (header block under the title), after every lesson, on deck title slides and
  at the bottom of answer keys. The license name is hyperlinked and the URL is
  printed.
- Quiz pipeline built, and its validator gates both generation and rendering.
  Fixed three validator false positives found on real output: algebra "(H/A)"
  read as an answer letter, maths symbols stripped before the duplicate check,
  and rounded answers ("about 2.8") failing the arithmetic check.
- Sample outputs are in `data/outputs/v2/<Subject>/<SS>/quiz/` and
  `data/outputs/v2/PDF/<Subject>/<SS>/quiz/`. The Opus comparison files
  (`*_quiz_opus.json`) are kept for review only; the renderer ignores them.
- Sonnet 5.5 pricing (docs, 2026-09-29): $2/$10 per MTok, batch $1/$5.
  Measured per lesson: ~8.7k input, ~4.5k output tokens.

## Updates — 2026-09-30 — Phase 4 pilot + cost estimate
- Mark reviewed the sample quizzes: good, but 10 questions is too many. The
  normal range is now **5–7**, with 8–10 only for content-heavy lessons
  (`questions_typical_max: 7`; validator warns above it). The 5 samples were
  regenerated and now have 7–8 questions.
- Pilot (Batch API, Sonnet 5.5): General Science 1.3, Core Maths 2.4,
  Biology 1.2. **22/22 lessons valid on the first try**, 160 questions (7.3
  per lesson), answer letters A 28% / B 24% / C 28% / D 21%. Cost $0.59
  measured, $0.027 per lesson. Docx re-rendered with attribution; link gate
  passes.
- Validator: the distractor-overlap warning now uses exact rounding (the 1%
  tolerance was flagging legitimate near-miss distractors, e.g. 33.1 m
  against 32.8 m).
- Prompt: added "at most one question about classroom routine". The pilot's
  General Science anchor lesson had two of them (hand signals, sticky-note
  colours). Applies to future runs; the pilot quizzes were not regenerated.
- Estimate for the rest of Grade 10: 701 lessons, **about $21** including
  retries. See Cost Tracking.

## Updates — 2026-09-30 (second entry, triggered by `/restart`) — Sonnet 5.5 minimum; doc drift fixed
- `/restart` found: `CLAUDE.md` and WORKFLOW.md still named `claude-sonnet-4-6`;
  this file's header date was a day behind; stale July copies `docs/STATUS.md`
  and `docs/WORKFLOW.md` still existed; `logs/quiz_generation/` and the handoff
  zip were untracked. Git state matched (4 commits ahead, push held for Phase 5).
- **Mark: Sonnet 5.5 is the minimum model for every activity.** A string swap
  would have broken lesson generation, because `generate_substrand.py` forced
  `tool_choice` in 3 places and Sonnet 5.5 rejects that. Moved to structured
  outputs, the same way `generate_quiz.py` already worked. Details are in the
  new Active Threads row. Price constants are now $2/$10 sync and $1/$5 batch.
- Server-side refusal fallbacks deliberately **not** enabled: the `"default"`
  routing can pick a model below Sonnet 5.5, and the Batches API rejects it.
- Removed `docs/STATUS.md` / `docs/WORKFLOW.md` (git history keeps them).
  The root copies are now the only ones, and `CLAUDE.md`'s layout says so.
  `PROJECT_CONTEXT.md` refs repointed, and `check_new_stem_subjects_status.sh`
  no longer looks in `docs/`.
- `handoff_bundle_*.zip` gitignored (the extracted folder is tracked).
  `logs/quiz_generation/` (batch IDs, `usage.jsonl` spend record, 2 Opus
  failure dumps) goes in with the next commit, like `logs/api_cost_log.md`.
- Left as-is on purpose, because they are historical records: `docs/snapshots/`,
  `docs/session-handoff-*`, `cbe-migration-bundle/`,
  `CBE_PROJECT_CONTEXT_040326.md`, `HANDOFF.md`, older session-log lines here,
  and the Sonnet 4.5-era `START_HERE.md` / `PROJECT_STATUS.md` /
  `IMPLEMENTATION_GUIDE.md`.
- **Pushed to `origin/main` at `af44ece` (Mark's instruction).** This also
  published the 4 Phase 1–4 commits that had been held for Phase 5, so the
  "push held until Phase 5" note above no longer applies. `origin` now has
  re-rendered docx/JSON with PDFs **still stale** (Phase 5 regenerates them).
  Don't Drive-sync PDFs from this state expecting the new links.

## Updates — 2026-09-30 (third entry) — Phase 5 without new quizzes; Phase 6 checks
- **Mark: skip the remaining quiz generation for now.** The 27 existing
  quizzes go to the partner for review first, and the other 701 lessons get
  quizzes later. No API calls this phase.
- Ran `generate.js --all` → `build_quiz.js` → `generate_pdfs.js` →
  `generate_teacher_index.js`, all exit 0. 85/85 link gates PASS
  (T1/T2/DEAD/SHAPE 0), 27 quizzes rendered, **309 PDFs, 0 failed**
  (255 lesson docs + 27 decks + 27 answer keys), index 85 sub-strands /
  255 documents. **PDFs now carry the Phase 2 links and attribution. They
  were from 2026-08-02 until this run.**
- Phase 6 checks (quiz-dependent items cover only the 27 existing quizzes):
  - Partner schema: 85/85 valid. `validate_corpus.js`: 728 lessons, 0 violations.
  - Content diff: all 85 `_data.json` byte-identical to HEAD (links were
    already re-matched 2026-09-29; this run only re-rendered).
  - Attribution: 282/282 docx, 27/27 decks, 54/54 answer-key html have
    CC BY-NC 4.0, and no literal `{YEAR}` anywhere (renders © 2026).
  - Quiz validator: 27 lessons, 196 questions, 0 failures, 13 warnings
    (mostly "no quiz for lessons ..." on sample sub-strands). Letters
    A 30% / B 25% / C 26% / D 19%.
  - Links in PDFs: 3,754 hyperlinks, 0 `ares.edu`, and every PDF has every
    docx link. LibreOffice writes `%27` as `'`, which is the same URL.
    (JSON holds more URLs per slot, i.e. direct plus search alternatives; the
    docx renders one. The 85 docx-only links are the licence link.)
  - `audit_resource_links.py --all-phases`: T1 127, **all "example"-titled
    false positives** from the audit's bare `exam` regex (0 real answer
    keys); T2 0; T3 462 across 110 resources, top ones on-topic but
    heavily reused (e.g. "Determine rotations" in the Rotation
    sub-strands, torque resources in Moments). There's no earlier
    all-phases T3 baseline to compare against.
- `logs/link_matching/.../General_Science_Chemical_Families.json` changed
  only in the order of tied rejected candidates. The chosen links are
  unchanged.
- Not done: the manual quiz spot check on 8+ sub-strands. Only 8
  sub-strands have quizzes, and they're with Mark/partner for review.

## Updates — 2026-09-30 (fourth entry) — Phase 7 documentation
- Pushed `1fb10d0` (Phase 5) to `origin/main` on Mark's instruction.
- **New `PARTNER_CONTRACT_NOTES.md`.** The contract is unchanged (85/85
  validate). `resourceLinks` values changed: 830 null slots, where the
  pre-v2 release (`6ab9bef`) had 0 of 7,280, and 187 direct `/modules/`
  links, where before all were Kolibri. Quiz data is in a separate file
  because the contract is strict. Attribution is render-time only.
- `docs/SCHEMA.md`: new `resourceLinks` section (it had none), an attribution
  note, and quiz coverage and question-count notes.
- `WORKFLOW.md`: link-gate and attribution notes under Step 6. The link check
  is relabelled **Step 6a** (two steps were both "6c"; older log entries'
  "Step 6c verification grep" means 6a). New **Step 6q** for quizzes. Step 6b
  now covers .pptx/quiz. Step 6c notes the index doesn't link quizzes.
- `SYSTEM_OVERVIEW.md` (root; `docs/` copy synced, identical): link gate,
  attribution, the v2 matcher, a Quick Check quiz components table, data
  flow 9a. Also **fixed stale content**: the resource section still showed
  `ares.edu` hosts and the Kiwix tracker wrapper.
- `CLAUDE.md`: layout rows for the quiz/attribution/link-check files and
  configs, `build_quiz.js` in Quick Start, quiz outputs, and presentations
  deferred.
- Active Threads: added presentations (deferred), quiz review / remaining
  quizzes, and the partner null-slot check.
- **Drive sync not run.** It's the Windows step: `git pull`, then
  `scripts\sync_to_drive.bat preview`, then `sync_to_drive.bat`. PDF job 2
  is `/MIR`, so Drive will match this run exactly, including the new
  `quiz/` folders.
- `scripts/sync_to_drive.bat` job 1 now also copies `*.pptx`. Without it,
  the 27 Quick Check decks would never reach Drive, because the PDF tree has
  only their PDFs and job 1's mask was `*.docx *.json`. **Untested: it's
  Windows-only.** Run `sync_to_drive.bat preview` first and check job 1
  lists `quiz\*.pptx`. Job 2 (no mask) already covers the 309 PDFs + 28
  HTML files.

## Updates — 2026-09-30 (fifth entry) — Grade 11 Biology templates; pipeline fixes before the pilot
- Mark pushed 9 Grade 11 Biology templates (`96e9f0d`) to `data/raw/Grade 11/Biology/`.
  `git mv`'d to `data/raw/CBE LESSON TEMPLATES/v2_owner_inventory/Grade11/Biology/SS<id>_<Grade 11 name>/`,
  which is where `find_v2_templates()` looks. All filenames matched the hand-verified
  Grade 11 names. There is no template for 1.4 Cell Division, which will be generated
  from the curriculum alone.
- **The templates are a new form.** It's the "CBE Phenomenon-Driven Lesson Sequence —
  Teacher Planning Template", Parts 1–8 in tables. `extract_template_docx()` was written
  for the Grade 10 scheme-of-work layout and recovered only the phenomenon. It missed the
  driving question, key concepts, prior knowledge, constraints, the teacher's model
  final explanation, and the whole Part 4 lesson spine, which the form calls "the part
  AI cannot invent". **Fixed before the pilot:**
  - `_parse_planning_form()` reads Parts 1–8. It only activates when it finds a
    "LESSON SPINE" table: 0 of the 74 Grade 10 templates.
  - Each lesson prompt (live and batch) now gets **its own spine row**, plus the
    teacher's sense-making, formative-assessment, constraint and other notes.
    It used to get the same generic evidence text for every lesson.
  - The UNIT prompt gets the driving question, KIQs, key concepts, hook, prior
    knowledge, constraints, the competency/value/PCI/career notes, and the spine,
    with the instruction "storylineThread MUST follow" it.
  - The FE prompts get the teacher's Part 6 model explanation and final product.
  - Lesson count comes from the form's "Number of lessons" entry. The old regex
    would have read the form's printed hint "Most sub-strands run 5 to 8 lessons"
    as 8 for every template. The teacher's figure wins even outside 6–14, with a
    note. If the entry is blank, the spine length is used.
- **Bug fixed: the UNIT prompt hardcoded `Grade: 10`.** The 2026-09-19 grade-aware
  pass missed it. It now uses `args.grade`.
- **Grade 11 curriculum is now sliced to the sub-strand** (`slice_curriculum_text()`,
  Grade 11+ only). Before, the whole 53k-char OCR file went to every request. Sections
  are now 2.5k–6.7k chars, found for all 10 sub-strands. Grade 10 text-source subjects
  are unchanged.
- Template data quality, for Mark (doesn't affect the 2.1 pilot):
  - 2.2 says 10 lessons but its spine has 7 rows.
  - 1.2 says "N/A" lessons, so its 9-row spine sets the count.
  - 2.3 asks for 5 lessons, below the usual 6.
  - 7 of 9 still print the blank form's "Grade 10" header. Harmless: the parser
    ignores it, and the grade comes from `--grade`.
  - 2.2's spine has blank or garbled lesson numbers, so rows are numbered in order.
- Pilot requests built offline and priced with free `count_tokens`. Input tokens:
  UNIT 6.2k, each lesson ~3.8k, FE 2.0k. Output, including thinking, is unknown
  until the run. **Estimate ~$0.4–0.8; ceiling ~$1.10** if every request hit
  `max_tokens` 16000.

## Updates — 2026-10-01 — Grade 11 Biology 2.1 pilot (Sonnet 5.5) + Sonnet 4.6 comparison
- Mark synced the missing 1.4 Cell Division template (`403fe31`, into the old raw folder;
  rebased onto the local filing commit and `git mv`'d into `SS1.4_Cell_Division/`). It parses:
  10 lessons, but only **6 spine rows**, the same gap as 2.2 (10 lessons / 7 rows).
- **Pilot:** `--grade 11 --subject biology --substrand 2.1 --output g11_bio_2_1 --batch`,
  then `--collect ... --wait --run`. 8 lessons (from the template form), Sonnet 5.5, 9/9 OK.
- **Comparison:** the same run on `claude-sonnet-4-6` as the project ran it before
  2026-09-30 (no thinking), via an evaluation-only wrapper. The wrapper is kept beside
  the output (`compare_sonnet46/.../run_sonnet46.py`), not in `src/`. The 4.6 data
  module was moved out of `generators/data/` so `generate.js --all` never picks it up.
- **Both failed the link gate on SHAPE (40 / 35).** Neither model used the canonical
  phase labels ("Phase 1: Predict (about 15 minutes) - ...", "Predict Phase (15 minutes)").
  The lesson schema allowed any string. The content order was right in all 16 lessons.
  **Fixes:**
  - **Root cause:** `LESSON_TOOL_SCHEMA` `phase` is now an `enum` of `CANONICAL_PHASES`,
    which structured outputs enforces (schema accepted by `count_tokens`).
  - **Repair:** relabelled by position after a keyword check at every position, through
    `patch_lesson.js --force` (contract-validated), then re-rendered. Both now pass the
    gate (0/0/0/0), and `validate_corpus.js` passes.
  - The per-phase timings the models put in the labels were dropped; Grade 10 lessons
    don't carry them either.
- **Cost (logs/api_cost_log.md, collect step; the UNIT call adds about $0.04–0.06):**
  Sonnet 5.5 $0.37 (batch 34.6k in / 58.3k out) vs Sonnet 4.6 $0.49 (25.2k / 50.5k).
  **5.5 is about 25% cheaper despite thinking.** Its lower per-token price outweighs
  the extra output.
- **Quality, checked mechanically:** both reproduce all 5 KICD outcomes verbatim, use
  the teacher's driving question, write safety notes for L2/L5 as the teacher asked,
  and use Kenyan crops in all 8 lessons. 5.5 builds the teacher's 45–50-student constraint
  into 8/8 lessons, against 4.6's 4/8. 4.6 is ~25% longer per lesson. In the one lesson
  read closely (L3), 4.6 had two science errors and 5.5 had none: 4.6 called avocado
  "Type A" protandrous (both types are protogynous) and gave passion fruit as the
  heterostyly example (it is self-incompatible). This is not a full review; Mark and
  the partner should read both.

## Updates — 2026-10-01 (second entry, triggered by `/update`) — continuity
- Pushed the pilot (`1ffe869`). `origin/main` = local, clean tree.
- **Waiting on Mark:**
  - (1) Review the 2.1 pilot: Sonnet 5.5 in `v2/Grade11/...`, 4.6 in `compare_sonnet46/...`.
  - (2) Go-ahead for the other 9 Grade 11 Biology sub-strands (~$4); get the 1.4/2.2
    spines completed first.
  - (3) Partner review of the 27 Grade 10 quizzes, then the remaining 701 (~$21).
  - (4) Windows Drive sync with the new `*.pptx` job-1 mask (`preview` first).
  - (5) Send `PARTNER_CONTRACT_NOTES.md` to the partner.
- **Not done yet for the pilot:** no PDFs, so it isn't in the teacher index, and no
  quizzes for it. Run `generate_pdfs.js` + `generate_teacher_index.js` only after
  Mark approves the pilot, because the index is teacher-facing and Drive job 2 mirrors it.
- Known Issues gained a 2026-09-30/10-01 entry: model upgrade ≠ string swap, silent
  template-format change, free-text schema drift, and the missed hardcoded grade.
- Don't re-check unless something changes: all 10 Grade 11 Biology templates parse;
  Grade 10 templates (74) are untouched by the form parser; 85/85 Grade 10 exports
  validate against the partner schema.

## Updates — 2026-10-01 (third entry) — pilot quizzes; three more Grade 11 subjects
- **2.1 pilot quizzes:** batch on Sonnet 5.5, 7/8 valid first time. L8 (the final
  synthesis lesson) had 12 questions, over the 10 maximum, and was regenerated live:
  7 questions, valid. 59 questions total; answer letters A 15 / B 25 / C 25 / D 34%.
  Spot check: 5/5 answers correct (one each from L1, L3, L4, L5, L8). ~$0.25.
  Rendered to `quiz/` (24 files). `build_quiz.js` also copies answer-key HTML into
  `v2/PDF/`, which Drive job 2 mirrors to teachers, so `v2/PDF/Grade11/` was deleted
  again until Mark approves the pilot. **Remember to re-run `build_quiz.js` (and
  `generate_pdfs.js` / `generate_teacher_index.js`) at approval.**
- **OCR (`extract_curriculum_ocr.py`, default slice mode; all five sources are one tall
  page):** chemistry, physics, general_science, core_mathematics, essential_mathematics →
  `data/raw/curriculum_text/grade11_*.txt` (+ `.raw.txt` audit copies).
- **Hand verification from images:** Chemistry 6, Physics 13, Core Maths 17 sub-strands,
  all consistent with the OCR sections. Names normalised to Title Case; "(I)"/"(II)"
  written as "I"/"II".
- **General Science and Essential Maths sources are unusable.** Viewing the embedded
  images (Ess Maths image 12, Gen Sci image 20) shows page after page of the same
  "National Goals of Education" front matter. Ess Maths' dedup removed 154 blocks
  (93.6k → 11.0k chars); General Science dedup removed 0, because the OCR of each copy
  differed slightly. Neither file contains a single sub-strand opener. Not registered.
- `slice_curriculum_text()` fixes:
  - It now accepts "1.1The Mole" (OCR drops the space).
  - It now stops at the strand-level "Assessment Rubric" / `STRAND` / `APPENDIX`
    heading. KICD puts a whole strand's rubrics after its last sub-strand, so Core
    Maths 1.7 had been 13k chars, mostly other sub-strands' rubrics.
  - The stop is **case-sensitive**: the per-page "Strand Sub Strand ..." column header
    must not end a section. A case-insensitive first try cut Biology 2.1 short, and
    comparing it against the pilot's 3,101-char input caught it.
  - All 46 sub-strands across the 4 usable subjects slice to 1.7k–5.4k chars.

## Updates — 2026-10-01 (fourth entry) — Grade 11 Biology complete; layout + attribution changes
- **Mark's decisions:**
  - (1) Attribution block moved: after the sub-strand overview, just before Lesson 1, in
    the Lesson Sequence, and at the end of the Final Explanation and Summary Table.
    The per-lesson footers stay. The code is shared (`build_docs.js`), so Grade 10 docx
    change on their next render. **Not re-rendered yet.**
  - (2) Grade 11+ layout: parallel `Lesson_Plans/` and `Quizzes/` trees per subject
    (`_v2_output_dir()`, `build_quiz.js`, `generate_teacher_index.js` updated). Grade 10
    keeps flat folders and `quiz/` subfolders. The 2.1 pilot was `git mv`'d into the new
    layout and re-rendered.
- **Generation:** the 9 remaining sub-strands were submitted as batches (`g11_bio_<x>_<y>`,
  lesson counts from the template forms: 8, 9, 8, 10, 10, 5, 7, 6, 7). 79/79 requests
  succeeded, with no stubs, refusals or truncations. All pass the gate first time: the
  phase enum works (no SHAPE failures, compared with 40 in the pilot).
- **Quizzes:** one 70-lesson batch, 66 valid. Failures:
  - 3 Taxonomy I lessons failed "duplicate choices". **This was a validator false
    positive:** binomial-nomenclature questions offer "Zea mays" / "Zea Mays" /
    "zea mays", and the check ignored case. The duplicate check is now case-sensitive,
    and case-only differences are a warning. Same class as the Phase 3 validator fixes.
    The whole corpus re-validated with 0 failures.
  - 1 lesson (3.1 L6) had 11 questions.
  - All 4 regenerated live and are now valid.
- Spot checks: 5/5 quiz answers correct across 1.2, 1.4, 2.3, 3.2 and 3.3.
- Costs are in `logs/api_cost_log.md` and `logs/quiz_generation/usage.jsonl`.

## Updates — 2026-10-01 (fifth entry) — Grade 11 Biology PDFs + index; the 596 uncommitted files explained

- Investigated the 596 modified files in the working tree. They are a **re-render, not a content change**: 0 `*_data.json` changed, the Lesson Sequence docx text is identical to HEAD (1,449 text runs both sides; spot-checked Bio 1.1) apart from the attribution block moving (`b020fd0`), the PDFs are regenerated, `index.html` only has a new timestamp, and one link-matching log (`General_Science_Chemical_Families.json`) has reordered runners-up. Committed with the Grade 11 PDFs as `f17e779`.
- Ran `build_quiz.js`, `generate_pdfs.js` (495 converted, 0 failed; it always converts every docx/pptx under `v2/`, so Grade 10 PDFs get rewritten each run) and `generate_teacher_index.js`. `v2/PDF/Grade11/` now holds 186 PDFs plus 78 answer-key html.
- Open: review the Grade 11 flags (1.4 L7–10, 2.2 L8–10, 2.2 L7/L9 overlap) and Drive sync (Mark, Windows).

## Updates — 2026-10-03 — partner validator review: cross-document consistency

**What the partner found** (Core Mathematics 2.9, `Editor Review output.docx`): Summary Table describing a different lesson sequence; Final Explanation with its own contradictory dataset; irrelevant resource links; student document containing exemplars; attribution wording/placement points. All content findings were confirmed against the data. The attribution *placement* finding is outdated (Mark moved it 2026-10-01; the YAML comment still said TOP).

**Root cause (not the 2026-09-30/10-01 regeneration, which changed only `resourceLinks`, attribution placement and quiz files):** (1) Final Explanation was a batch request alongside the lessons, so it saw only the driving question; (2) Summary Table was a separate call that could retitle lessons: 73 of 85 Grade 10 sub-strands had at least one retitled lesson (172 of 728), and 634 lesson rows had text differing from the lesson's own summary; (3) nothing compared the documents; (4) **lessons generated in parallel batch do not share an anchor dataset**, so lessons within a sub-strand can contradict each other (Core Math 2.9: B's slowdown at 15-30 / 20-30 / 25-35 / 25-38 km; L4/L6 say A won by a final sprint, L8 says B sprinted). This last one is unfixed and probably corpus-wide for data-heavy sub-strands (unmeasured).

**Done (no API spend):** backup; `scripts/rebuild_consistency.py`; `derive_summary_table` (no API); FE generation moved after lessons with a second-call reviewer (`generate_final_explanation`, up to 4 rounds, keeps the best attempt, lesson-vs-lesson conflicts logged separately to `logs/lesson_conflicts/`); `scripts/validate_consistency.py` in `generate.js`; student/teacher-key FE docs (index entry added; **PDFs + index not rebuilt**); T3 relevance rule (`conflict_qualifiers`); `patch_lesson.js` ST refresh; WORKFLOW.md section; full re-render. After re-render: link gate 0/0/0/0/0; validator's only failure is the pilot's `FE-UNVERIFIED` on coremath_2_9. Link relevance, old vs new matcher, on the gate's own rules: answer/exam 45->0, wrong-subject vocab 166->0, other-sub-topic 110->0 of ~7,000 links; 830 -> 835 null slots (fill rate unchanged to the decimal for most subjects). Independent precision (does an LLM judge agree the links fit the lesson?) **not yet measured**.

**Paid, pilot only (~$1.50 total, 4 runs on coremath_2_9):** run 1 failed (reviewer mixed issue types; loop kept last not best), run 2 passed round 1, runs 3-4 with a stricter reviewer (cross-part numbers) did not converge in 3-4 rounds (1/5/6/1 issues). The currently written 2.9 FE is the run-2 version (hand-checked arithmetic: correct; one cross-part inconsistency remains, A at 19 vs 21 km/h) and is flagged unverified. **Other 94 not run**, per Mark's "pilot, then continue if clean".

**Needs Mark:** (a) whether to accept a Final Explanation as "reviewed" after N rounds with residual minor issues (queued for human review) vs requiring zero; (b) whether to fix the lessons' anchor-data drift (generate a shared fact sheet in `generate_unit` for new sub-strands; for existing ones, a lesson-consistency review ~$5 to size it, then decide on regeneration) — this changes teacher-facing lesson content, so it is Mark's call; (c) attribution items; (d) approve link-precision audit (~$0.50) and the 94-module FE run.

## Updates — 2026-10-03 (second entry) — drift measured, reviewer standard, link judge

- **Mark's decisions:** reviewer standard = write best attempt, flag for human review, validator blocks until cleared; run the drift check; build the link judge; spend approved.
- **Final Explanation rebuild (all 95, live):** $28.28 vs ~$18 estimated (4 rounds + reviewer). 42 clean; 53 flagged; 44 of those have a written best attempt, 9 Physics have none (credit balance ran out near the end of the run; old text kept). `--apply-held`, `--clear` added to `scripts/rebuild_consistency.py`.
- **Drift review** (`scripts/review_lesson_consistency.py`, $6.43): see Active Threads row.
- **Link matcher:** audit of 60 lessons by an independent judge (titles only, strict): old matcher fits 9% / partial 39% / off-topic 52%; new (10/1) 39 / 46 / 15. Added: `scripts/judge_links.py` + `config/link_judgments.json` (4,529 verdicts: 1,646 fits, 2,001 partial, 882 off_topic); matcher refuses cached off_topic; gate T4; extra conflict terms ("time dilation", "length contraction"). After pass 1 + re-render: T1-T4/DEAD/SHAPE all 0; fill rate dropped (Biology 73.8->68.8%, Chemistry 89.6->84.3, General Science 78.1->73.0, others <=1.5 pts); 535 replacement links still unjudged. **Not re-audited** after the judge (no credits).
- **Total API spend this session ~$42** (FE rebuild 28.3, drift 6.4, judge 5.0, audit 0.4, pilots ~1.9). The $50 added 2026-09-30 is exhausted: top up before the next paid step.

## Updates — 2026-10-03 (third entry) — credits added; Physics FE done; link judge converged

- **Physics Final Explanations (9 modules):** 1 clean, 8 flagged needs_review (best attempt written). Total flagged now **52 of 95** (43 clean; see `logs/final_explanation_issues/`); all need human review or `--clear` before distribution.
- **Link judge** converged in 5 passes (5,134 verdicts). Replacements for rejected links were themselves often off-topic (pass 2: 188 of 459; pass 3: 43 of 98; pass 4: 25 of 31): the matcher's weaker candidates are poor, so the right outcome for many slots is empty. Fill rate now: Biology 67.3%, Chemistry 83.6%, Core Math 95.5%, Essential Math 92.3%, General Science 70.7%, Maths 98.8%, Physics 85.1%.
- **Re-audit, same 60 lessons, independent judge:** old matcher fits 11 / partial 34 / off-topic 54; new matcher **49 / 47 / 4** (was 39/46/15 before the judge). Residual off-topic ~4% includes judge noise (the audit judge and the cache judge disagree on a few titles).
- API spend this session now ~$47.

## Updates — 2026-10-03 (fourth entry) — lesson-drift repair + link tightening; credits ran out again

- **Mark's decisions:** accept the drift recommendation (edit-based repair of the ~10 worst sub-strands + shared fact sheet for new generation); do link-tightening items 1-5.
- **Built:** `scripts/repair_lesson_drift.py` (model proposes EXACT find/replace edits; applied only if the old text occurs once; audit trail in `logs/lesson_repairs/<module>.json`), `scripts/fix_lesson_drift.sh` (repair -> derive ST -> re-review, <=3 rounds, then FE rebuild), `scripts/generate_link_queries.py` (806 lessons, `config/link_queries.json`; widen retrieval + gate), `scripts/judge_candidates.py` (judge the matcher's top candidates, not just picks), `scripts/link_gap_report.py` (-> `logs/link_gaps.md`), matcher now ranks by verdict (verified fits first, partial only if nothing fits, nothing otherwise; phases spread across distinct fits), docx labels partial links "Related topic: not an exact match" (non-enumerable `_fit`, so the strict contract JSON is unchanged; the partner's editor will not see the label).
- **Drift repair results so far:** coremath_2_9 4 -> 2 major (3 rounds); math_4_1 6 -> 0 major (2 rounds); FE rebuilt for both (see flags in logs/final_explanation_issues/). **essmath_2_8, phys_2_1, phys_1_3, phys_1_1, gensci_2_4, essmath_2_6, essmath_2_5, essmath_2_4, coremath_3_1: NOT repaired** (calls returned no response: credits exhausted partway; essmath_2_8 failed from round 1, cause unconfirmed, could be output truncation). **The drift reviewer is noisy**: identical text scored 5, 5, 7 majors on essmath_2_8. Treat counts as +/-2.
- **Link tightening:** queries generated ($3.03); candidate judging ran ~60% before credits ran out (cache 11,197 at that point: 3,752 fits, 4,828 partial, 2,617 off-topic; $5.09). **No re-render has been done since the matcher change**: the docx/JSON links on disk still reflect the previous matcher. Remaining: finish `judge_candidates.py`, `node generators/generate.js --all`, `judge_links.py` pass, `link_gap_report.py`, re-run `audit_link_relevance.py` (same 60 lessons), PDFs + index.
- **API credits exhausted again** (~$60 spent this session). Estimated to finish: ~$20.

## Updates — 2026-10-04 — credits added; drift repair + link tightening completed; PDFs rebuilt

- **Repair script fix:** `repair_lesson_drift.py` calls overran the 16k output limit on large conflict sets (the essmath_2_8 "no response"); now chunks 3 conflicts per call, falling back to one at a time.
- **Drift repair results** (major contradictions, reviewer-counted, +/-2 noise): coremath_2_9 4->2, math_4_1 6->0, essmath_2_8 6->4, phys_2_1 5->4, phys_1_3 5->3, phys_1_1 5->4, gensci_2_4 5->2, essmath_2_6 5->1, essmath_2_5 5->4, essmath_2_4 5->3, **coremath_3_1 5->6 (no net fix; 3 conflicts unresolved)**. Rounds 2-3 sometimes made counts worse; the data on disk is the last round, not the best. Residual contradictions stay in `logs/lesson_drift/<module>.json`. **Not done:** the other ~84 sub-strands, and the shared fact sheet for new generation (`generate_unit`).
- **Link tightening done:** judge verdicts 12,277 (cache); matcher prefers verified fits, partial only if none fit, a fit repeats in at most 2 phases while alternatives exist (3+-phase repeats 785 -> 323); docs label partial links; 806 lessons got search phrases. Gate fix: T3 now uses the same lesson vocabulary as the matcher (it had flagged "Planet Orbits" on a Space Physics lesson). Fill: Biology 69.0%, Chemistry 85.8, Core Math 99.1, Essential Math 96.6, Gen Sci 73.0, Maths 99.2, Physics 87.1 (higher than before the judge because labelled partials are included again).
- **Measured (same 60 lessons, independent judge):** old matcher fits 11 / partial 39 / off-topic 51; now **52 / 44 / 4**. Lessons with a verified fit: 635 of 806 (78%); 106 partial-only; 65 no links. Gap list for the content team: `logs/link_gaps.md`. The remaining gap is a library-content gap, not a matcher problem.
- **Gates:** links T1-T4/DEAD/SHAPE 0; `validate_corpus.js` PASS; consistency validator: 47 Final Explanations flagged `needs_review` (down from 52); all else clean. PDFs regenerated (590 converted, 0 failed) and teacher index rebuilt (95 sub-strands, 380 documents, now including the teacher-key PDFs).
- **Still open:** human review of the 47 flagged Final Explanations; remaining lesson-drift decision for the other sub-strands; attribution decisions; commit + Drive sync (Mark). Committed and pushed 2026-10-04 as `69f3583` (1,302 files: scripts, config caches, regenerated docx/JSON/PDFs/index). `Editor Review output.docx` (partner report, contains the partner's local file paths) was committed with it. Drive sync is still Mark's step.

## Updates — 2026-10-04 (second entry) — 84 sub-strands repaired in Claude Code; prevention built into the pipeline

- **Mark's decision:** do the remaining drift fixes (safe classes auto, science/structural to a teacher list) and build prevention for future grades; do the fixes in Claude Code, not the API.
- **Repairs (no API spend):** 8 parallel Claude Code agents, 84 sub-strands, via new `scripts/apply_edits.py` (exact-once find/replace; audit `logs/lesson_repairs/<module>.cc.json`). **709 edits applied, 0 rejected**; `validate_corpus.js` PASS after every module. Of the reviewer's conflicts the agents verified: 138 cross-reference and 81 dataset (fixed), **196 false positives (~33%)**, 114 science and 68 structural (not edited). Larger dataset rewrites worth a human glance: coremath_2_7 (box/drum volumes recalculated), math_4_2 (notebook data and tree diagram), math_3_3, essmath_2_2 (name aligned to the last lesson, not Lesson 1). Final Explanations aligned where a changed fact appeared in them.
- **Teacher/author review list:** `TEACHER_REVIEW_LIST_2026-10-04.md`, 215 items across 83 sub-strands (science + structural + residuals of the 11 API-repaired). Includes real content errors, e.g. coremath_2_3 says rotation gives opposite congruence; essmath_2_1's phenomenon uses 4/9 cups for k=2/3 volume; chem_3_1 calls Jik NaOH; essmath_3_1's stated mean/mode/median are impossible; bio_1_2 cites food tests no lesson performs; math_1_1 says √4's reciprocal is irrational.
- **Prevention (src/lesson_consistency.py, wired into generate_substrand.py):** fact sheet (anchor data, characters, outcome, conventions, lesson map) generated after the UNIT and carried into every lesson prompt (batch + live); after lessons, review -> repair majors -> keep best; Final Explanation uses the fact sheet as authority. Tested on coremath_2_9's unit ($0.12, numbers hand-checked). WORKFLOW.md documents it plus a pilot-first rule for new grades/subjects.
- **Re-derived** Summary Tables (40 modules changed), re-rendered all 95 (links T1-T4/DEAD/SHAPE 0), PDFs + index rebuilt. Consistency validator: 47 Final Explanations still flagged needs_review.
- **Not done:** re-running the drift reviewer on the 84 (~$5, optional; reviewer is noisy); `scripts/repair_lesson_drift.py` / `review_lesson_consistency.py` still carry their own copies of the logic now in `src/lesson_consistency.py` (consolidate later).

## Updates — 2026-10-04 (third entry) — drift reviewer re-run after the Claude Code repairs

- Re-ran `review_lesson_consistency.py` on all 95 ($6.39); previous reports kept in `logs/lesson_drift_before_cc_repair_2026-10-04/`. Headline unchanged: 91 of 95 with at least one major.
- On the 84 repaired in Claude Code: majors 204 -> 182 (-11%); 35 sub-strands improved, 30 same, 19 worse. About 104 of the 182 resemble an earlier finding (mostly the 182 science/structural items deliberately left for teachers); about 78 look new by wording, of which a spot check shows several are old findings reworded (Jik, the Laikipia farm dimensions) and some are genuine leftovers.
- Conclusion: this reviewer cannot serve as an acceptance test. It re-reports the unedited items by design, re-words findings between runs, and ~33% of its findings were false positives when checked. Per-module reports refreshed in `logs/lesson_drift/`.

## Updates — 2026-10-04 (fourth entry) — committed; verification pass starting

- Committed and pushed `7cb36a1` (84-module repairs, fact sheet + consistency pass, teacher list, re-render, PDFs).
- **In progress:** Claude Code verification pass (Mark approved option 1): agents check the 215 current major findings in 91 sub-strands against the text, fix real cross-reference/dataset leftovers via `scripts/apply_edits.py`, and classify the rest (science / structural / false positive / already listed) for the teacher list.

## Updates — 2026-10-04 (fifth entry) — verification pass done

- 8 Claude Code agents (no API) checked every current MAJOR drift finding (230 across 91 sub-strands) against the lesson text: **63 false positive, 96 already on the teacher list, 39 real cross-reference/dataset conflicts fixed (94 edits, 0 rejected), 21 new science, 11 new structural.** Includes fixes the API pass could not apply (coremath_2_9 runner speeds) and corrected arithmetic (phys_3_2 bill KES 1,179 at Ksh 12/kWh; essmath_2_8 savings; coremath_3_2 trip fraction).
- **Teacher list rebuilt, deduplicated and verified:** `TEACHER_REVIEW_LIST_2026-10-04.md`, **207 items in 83 sub-strands (128 science, 79 structural)**; every item was judged real by an agent reading the text. Worst structural cases (rewrite/regenerate candidates): essmath_3_1, essmath_2_1, coremath_1_3, coremath_3_1, gensci_2_2 (missing halogen lesson), phys_2_1 (Doppler lesson cited but absent), math_2_1, bio_1_2.
- Summary Tables re-derived (9 changed), all 95 re-rendered (links 0 failures), PDFs + index rebuilt (590, 0 failed). `validate_corpus.js` PASS. 47 Final Explanations still flagged needs_review.
- With the reviewer's false positives removed, the remaining real between-lesson problems are the 207 listed items: science explanations and structure, not facts/references.

## Updates — 2026-10-04 (sixth entry) — 8 sub-strands regenerated; science fixes; teacher list 207 -> 103

- **Regenerated with the fact sheet (batch):** gensci_2_2 (pilot), essmath_3_1, essmath_2_1, coremath_1_3, coremath_3_1, phys_2_1, math_2_1, bio_1_2. **All 8: 0 major lesson contradictions** after the in-pipeline check (gensci_2_2 needed no repair at all). Cost ~$6.80 total (~$0.56-1.08 each). Their links were judged and re-rendered.
- **Bug found + fixed:** the generator built file names from the folder map, so a regenerated Maths sub-strand came out as `Maths_*` beside the existing `Mathematics_*` files. `_SUBJECT_FILE_PREFIX` added (Mathematics), math_2_1's META fixed, duplicate files deleted.
- **Science-fix pass (Claude Code, no API):** 119 science items in 61 sub-strands -> 46 fixed (124 edits), 33 not real, 19 teaching choices, 26 need a rewrite. **Independent check of every fix by separate agents: 0 reverted**, 7 small adjustments, plus 7 extra errors fixed (e.g. 1 TB = 2^40, tan not sin for a height, flame colours are electron emission not combustion, expected not guaranteed profit, rounding 5 285 m²).
- **Teacher list now 103 items in the remaining sub-strands** (was 207): 57 structural, 26 science-needs-rewrite, 19 teaching choices, 1 other. `TEACHER_REVIEW_LIST_2026-10-04.md`.
- **Open: quizzes are now stale** for the regenerated bio_1_2 (L1-L6) and phys_2_1 (L1): they were generated from the old lessons. Regenerate with `generate_quiz.py` (~$0.30) then `build_quiz.js` — needs Mark's go-ahead.
- Gates: links 0 failures; contract PASS; 43 Final Explanations flagged needs_review (was 47). PDFs + index rebuilt (590, 0 failed). Lessons with a verified-fit link: 79%.

- Committed and pushed 2026-10-04 as `e15b776`. Stale quizzes (bio_1_2, phys_2_1) deferred by Mark. Drive sync still Mark's step.
