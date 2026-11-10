# Round 2 handoff: applying teacher journal decisions (written 2026-11-09)

## RELABEL 2026-11-09 (Mark) — READ FIRST: module ids changed
- **Maths:** the journal labelled "Core Mathematics" (ids `coremath_*`) was really the main **Mathematics** journal. The 14 edited `coremath_*` modules are now **`math_*`** (subject "Mathematics", folder `v2/Maths/SSx_Name`, prefix `Mathematics_Name`). The previous `math_*` modules and their renders are in `backup_alternates/math_original/`. **There is no Core Mathematics work in this workspace and no Core Mathematics journal**: the real Core Mathematics (`coremath_*`) starts later, from scratch, with no teacher reviews to use. Everything below that says `coremath_*` now means `math_*`.
- **Bio:** the teacher-template sequence filed as Biology 1.1 (content = KICD 1.3 'Cell Structure and Specialisation') is now **`bio_1_3`**; the generated 'Cell Biology' module that was `bio_1_3` is in `backup_alternates/bio_1_3_generated/`. `bio_1_1` is unused (KICD 1.1 Introduction to Biology is not built). New `bio_1_3` has the KICD four-level rubric row (`bio_1_3-r2-kicd-001`) and a re-review flag (`bio_1_3-r2-flag-002`).
- Old id -> new id: `round2/id_map.json`. Teacher input (`slices/`, `decoded/`) keeps the ORIGINAL ids, because that is what the teachers saw (slices/bio_1_3.json is the backup's). Tool: `scripts/round2/relabel_ids.py`.
- Baseline copies of the 14 maths and of bio_1_3 got the same naming change (subject label, folder, prefix, id) so the tracked-change files compare content only; no lesson content was changed in any baseline.
- **Maths rubrics (Mark, 2026-11-09):** the Maths KICD curriculum (not 'Core Maths') is the source; all 14 `math_*` FE rubrics now carry the KICD indicators and four levels verbatim (records `math_<x>-r2-kicd-001`). The earlier 'adopt the KICD rubric is not met literally' note in the ledger is superseded.
- **FE review pass (2026-11-09):** see STATUS.md eleventh entry. Findings `fe_review/` (+`fe_review_pass1/`), records `<m>-r2-fe-NNN` (group R2-FE-REVIEW), brief `round2/ROUND2_FE_BRIEF.md`, tools `scripts/round2/fe_vs_lessons_check.py` and `review_fe.py`. `fe_issues/` = FE issue logs for the revised ids. gensci_1_1..1_6 Below descriptors were rewritten (records `r2-rub-fix`).
- **Automatic FE convergence (2026-11-09):** tool `scripts/round2/fe_converge.py`, per-module results `fe_converge/<m>.json`, records `<m>-r2-fe-auto-NNN`; all 41 Bio/Chem/Phys/Maths modules converged. GS/EM/Core Maths are on hold (Mark). See STATUS.md twelfth entry.
- **Automatic lesson audit (2026-11-09):** tool `scripts/round2/lesson_converge.py`, results `lesson_converge/<m>.json`, records `<m>-r2-les-auto-NNN`; 12 modules unfinished (API credit ran out); Final Explanations must be re-converged afterwards. See STATUS.md thirteenth entry.
- Promotion note (not done): at promotion `generators/data` `math_*` and `bio_1_3` are replaced; `generators/data` `coremath_*` (the original generated Core Maths, same content as the new Maths baseline) and `bio_1_1` (the old teacher-template copy) must be archived first so the real Core Maths and KICD 1.1 can be built later.


**Read this, then `STATUS.md` Active Threads, then run `/restart`.** Rigor Level 3 (partner contract, validators, pause-and-report). Nothing here is committed, pushed, promoted to `generators/data`, or synced to Drive. Everything below is in the *revised workspace* `data/revised_2026-10_full/` only (set `export CBE_REVISED_DIR=$PWD/data/revised_2026-10_full`).

## What this task is
Mark's request: teachers reviewed the Round 1 revision journals (Biology, Chemistry, Physics, Core Mathematics; Grade 10). Use their responses to change the lesson plans and regenerate the final documents in the same format as before. Marking convention: white/unmarked items = accepted; orange/yellow items marked Accept or Edit; Edit text typed in the same cell; where boxes could not be ticked, red highlight = accepted, red label text = edit.

Source files: `Finished.zip` (repo root, untracked, do NOT commit; teacher documents). Files: `Journal_Biology.docx`, `Journal_Chemistry.docx` (the later one), `Journal_Core_Mathematics.docx`, `Flagged_Items_Physics.docx` (Physics source = flagged items only; non-flagged Physics items count as accepted, per Mark).

## Decisions already made by Mark (binding)
- Autonomy: fix and report at the end for same-kind issues; new-kind scope/cost/risk, pushes, first API spend still need confirmation (CLAUDE.md).
- Four CBE rubric levels (Exceeds, Meets, Approaches, Below Expectations): the partner contract (`ares-contract.schema.json`) has only `excellent`/`proficient`/`developing`. **Mark will notify the partner; contract + template change is required and is ON HOLD.** The 3-level headings came from the generator's first Bio 1.3 version (2026-05-26, commit `21cd8c66`), not from teacher templates or any recorded decision. All ~41 "four levels" items are marked R (rubric deferred) below; no rubric structure was changed. KICD PDFs contain four-level rubric tables (Mathematics: printed pp. 37-49).
- `Journal_Core_Mathematics.docx` (item ids `coremath_*`) was the main Mathematics journal, mislabelled (Mark, 2026-11-09): its decisions apply to Mathematics, the modules are now `math_*` (see RELABEL above). `Journal_Mathematics.docx` in older notes means the Round 1 journal of the previous `math_*` modules (now in backup). General Science (16) and Essential Mathematics (13) Round 2 journals were not received.
- Mark: "proceed with all updates... including lesson length for Mathematics". KICD Mathematics PDF: `data/raw/curriculum_pdfs/Grade10_Mathematics_Curriculum.pdf` (states 40 minutes per lesson). Rule used: no 80-minute double lessons in Core Mathematics; keep lesson count, trim each to 40 min, unless that module's own teachers said otherwise (e.g. "2 x 40", "split").
- Notification: a `PushNotification` tool exists; delivery to Mark is unconfirmed. Mark cannot stay in the window: send one when blocked on a decision or when a phase finishes.

## How it was run
Per module, one subagent got `ROUND2_BRIEF.md` (+ `ROUND2_COREMATH_ADDENDUM.md` for coremath) and `slices/<module>.json` (decoded teacher decisions). It applied changes ONLY through `python3 scripts/revise_apply.py apply MODULE RECORDS.json` (dry-run first), then `python3 scripts/revise_build.py MODULE`, and reported. Records are appended to `change_records/<module>.json`; Round 2 ids contain `r2`/`R2` or continue the numbering. Decoder scripts: `scripts/round2/` (`decode.py` journals, `decode_phys.py` flagged items; use `venv/bin/python -I`, needs lxml). Decoded decisions: `round2/decoded/`. `validate_corpus.js` only checks `generators/data/` unless run as `CBE_DATA_DIR=data/revised_2026-10_full/modules node scripts/validate_corpus.js <module>` (several agents used this successfully).

## Module ledger (agent reports; coremath_2_3/2_4/2_5/3_2 re-verified from the module files in session 2, 2026-11-09)
**Session-2 verification (2026-11-09):** `CBE_DATA_DIR=data/revised_2026-10_full/modules node scripts/validate_corpus.js` = PASS, 85 files / 728 lessons. Durations re-read from the modules for all 14 Core Maths: 40-minute everywhere EXCEPT `coremath_1_3` L8 (deliberate 2 x 40), `coremath_2_6` L5-L8 (still 80; teacher asked for a split into 12 lessons; UNIT.totalDuration there reads '12 lessons x 40 = 480', i.e. periods, while the module has 8 lessons) and `coremath_3_1` (L1,L2,L3,L5-L8 still 80; ledger said 'done' but only a flag was made; teachers asked for 16 lessons). These need Mark's decision (cross-cutting item 4). **Pitfall:** `revise_apply.py`/`revise_build.py` read `data/revised_2026-10` (an OLD workspace) unless `CBE_REVISED_DIR` is set in the same shell command.
R = four-level rubric deferred (every module has one).

### Biology (9) - all reported
| Module | Applied | Open |
|---|---|---|
| bio_1_3 (was bio_1_1; now the live KICD 1.3) | KICD names "1.3 Cell Structure and Specialisation" in headers/FE; egg-cell and pollen take-home cards (L8/L9) | META (title/subtitle/outputDir still 1.1); is "Evidence Card Set 10"/hierarchy template available; full L9 phloem-to-pollen swap or take-home OK? check card facts |
| bio_1_2 | Sub-strand shown as "1.4 Chemicals of Life" (KICD) in UNIT and 6 lessons | which of vitamin C test / catalase / factors (pH, substrate, enzyme conc.) to add; KICD 24 lessons vs 6; keep structure teaching vs KICD "exclude structure"; META/files rename |
| bio_1_3 OLD generated (now in backup_alternates/bio_1_3_generated) | L6 now 8 evidence cards (palisade, pollen core); every "six" -> "eight"; 80 min kept | Part A timing split (45-s CER) was invented, confirm; rename "Cell Biology" -> "Cell Structure and Specialisation"? |
| bio_2_1 | Strand/sub-strand = KICD ("2.0 Anatomy and Physiology of Plants", "2.1 Nutrition") | bio_2_1-059: teacher's typed word equation has a gap where the arrow goes: where does it go, use "Carbon IV Oxide" everywhere?; lesson count 10 vs KICD 12? |
| bio_2_2 | KICD names 2.0/2.2 "Transport" | -123 "MATCH KICD": girdling experiment format (take-home / school garden / photos only); KICD 22 lessons vs 8 |
| bio_2_3 | none | -143 "Edit to match KICD" too vague (rubric?) |
| bio_3_1 | KICD names 3.0/3.1 "Nutrition"; vulture wording softened | KICD 12 lessons vs 10; META/title "Animal Nutrition" |
| bio_3_2 | KICD names 3.0/3.2; teacher-own printed text for L4/L8; L11 apostrophes restored; NGSS labels -> KICD core competencies (68 records) | SUMMARY_TABLE.subStrand still "Animal Transport"; META |
| bio_3_3 | KICD names; amphibians+birds in L3 (3 min, time taken from comparison table); animation pressure pre-check | META names |

### Chemistry (7) - all reported
| Module | Applied | Open |
|---|---|---|
| chem_1_1 | none | -065: teacher asks partner to extend contract (Mark's action); add "record Below Expectations on the classroom rubric" note to FE now? |
| chem_1_2 | none | none |
| chem_1_3 | flag only | L1/L2 matcher picks spoil the card sort (needs `config/link_matching.yaml` exclusion + rerun + human viewing); teacher note: 10 lessons vs KICD 30, note-only? |
| chem_1_4 | L1 structure video removed (time reused); L7 data cards = melting points only, predict solubility/conductivity | where to show the removed structure visualisation (L4 B / L11); show removed animation after L8 tests?; leftover references in L7 later phases |
| chem_1_5 | "Kisumu Water and Sanitation Company" -> "a water treatment plant in Kisumu" (9 places); strand "1.0 Inorganic Chemistry" | -070: ionic radius / electron affinity / boiling-point additions need data values (not added); 34 vs 12 lessons recorded as risk flag |
| chem_2_1 | KICD number 2.2 in text; DQB colours green -> orange (L3); Bata Limuru/pharma silica-gel examples (L6) | META 2.1 vs 2.2; teacher text "silica gel = porous salt of sodium silicate" and "NCPB uses CaCl2 to test moisture in maize" NOT written (wrong/unverified): ask teacher |
| chem_3_1 | KICD 2.0/2.1 numbering in text; CuO + dilute H2SO4 teacher demo (L7, safety note) | META 3.1, SS3.1 folders, module id vs 2.1 |

### Physics (12) - all reported (source: Flagged_Items only)
| Module | Applied | Open |
|---|---|---|
| phys_1_1 | KICD content in L7-L9 (monsoon link, hydraulic brake and tyre calc [illustrative], pumps); retimed | numbering 1.2 (META.subtitleDoc/summary header); garage visit as field task?; kaskazi/kusi terms need teacher check |
| phys_1_2 | hardness scratch test (L5, 6 min); numbering 1.3 in lessons/FE | META/folder SS1.2 rename?; SUMMARY_TABLE.subStrand still 1.2 |
| phys_1_3 | SGR/railway removed -> bridge girder (25 m, 12.4 mm); numbering 1.4 not applied (META) | railway example only after Kenya Railways/engineer confirms; 1.4 numbering; KICD 12 lessons vs 6 |
| phys_1_4 | numbering 1.6 in text; rubber-band PE demo L3; L8 follow-up tasks (gears, hydraulic lift, shaduf/bellows [unverified]) | META.subtitleDoc 1.4; 9th period?; keep unused supporting phenomena? |
| phys_1_5 | tower-crane case study relabelled composite scenario; title "Moments and Equilibrium" | torque/couple, two supports, resolution of forces NOT written (no room in 6 lessons); META "Moments of Equilibrium" |
| phys_2_1 | strand "2.0 Waves and Optics"; L10 clip sound-only, no wavefront model until Explain | none |
| phys_3_1 | numbering 2.2; electroscope, burette, U-238 series (homework), Chernobyl case study; L5 worksheet instead of ARES module | does the ARES offline module exist; META 3.1; where deferred-content note lives |
| phys_3_2 | L5-L9 KICD additions (6-8 min each, text only, not re-timed); tariff labelled "assumed" | real tariff; confirm deferral list; feasibility of added minutes |
| phys_3_3 | none | -032: verify offline PhET simulation controls (human task) |
| phys_3_4 | numbering 3.1 in text; separation, field patterns, electroscope task (L7-L8), spray gun | META.subtitleDoc; dedicated electroscope lesson?; fingerprinting mechanism unverified |
| phys_4_1 | strand 4.0; Muriithi testimony labelled composite; L3 teacher-prep note | any real interview?; 1934 photo source/caption; PhET exact labels |
| phys_4_2 | none | KICD extension outcomes f-l to be reviewed by a teacher |

### Mathematics (14) — formerly `coremath_*`, renamed `math_*` 2026-11-09
| Module | Status | Applied | Open |
|---|---|---|---|
| math_1_1 | done | all 8 lessons 40 min; L5-L8 REPLACED by new KICD lessons (reciprocals, tables, calculators, application/close); rubric uses KICD 3 indicators + level wording | new L5-L8 are agent drafts, need teacher read-through; reciprocal tables availability |
| math_1_2 | done | 8 x 40 (320); L1 no longer links reciprocals to negative indices | L3 density; drop reciprocals from L1 entirely? |
| math_1_3 | done | L8 = two 40-min periods (teacher said 2x40; total 360, 9 periods); maximum-area content dropped, 91 m2 plot | KICD rubric for 1.3 (only a generic one found); residual "maximum" in L1/L5/L7 |
| math_2_1 | done | 8 x 40 = 320 | split into 14 instead of trim? practice-time check |
| math_2_2 | done | headlight claim fixed; L1+L2 merged, new L2 congruence; 8 x 40 | new L2 ordering; L7 "opposite congruence" wording |
| math_2_3 | done (session 2, 2026-11-09) | 8 x 40 = 320 (83 records, group R2-40MIN); no 80-min text left | L5 (Observe 17 min) and L8 (Explain 20 min) are tight: teachers to try the pacing |
| math_2_4 | done (session 2) | 8 x 40 = 320 (131 records r2-015..145); coastal cliff now 20 m / 35 deg in the supporting phenomenon (matches L7 demo), L7 Problem 3 reworded 'a taller coastal cliff' | teachers confirm cuts: L1 triangle count, L3/L4 fewer table rows, L7 Problem 2 now extension, L8 Mombasa example; L5/L8 tight |
| math_2_5 | done (session 2) | 8 x 40 = 320 (99 records); old 600-min total (item 001) superseded by Mark's rule; L5 video dropped, heptagon in-class 3 min; L6 shoelace extension now optional take-home; L8 written assessment cut 25 -> 16 min (flagged) | teachers confirm L8 assessment cut and L5/L6 moves; KICD 14 lessons vs 8; -078 rubric deferred |
| math_2_6 | done | L1-L4 trimmed to 40; L5-L8 STILL 80 min | teacher: "split 4 doubles into 40-min, shrink 4 others" -> 12 lessons x 40 (KICD 12): needs lesson insertion; -077 "drop lesson 3" conflicts |
| math_2_7 | done | 8 x 40 | "split" = trim (done) or 14 lessons? |
| math_2_8 | done | 8 x 40 (L1,3,4,5,7,8 trimmed); column vectors vertical (2 spots); labels "Vectors I" | META names; stacked-vector glyphs untested in docx/PDF |
| math_2_9 | done | 8 x 40 (L1,3,4,6,8 trimmed); digital extended activity L1/L8 | teachers asked split to ~13-15 lessons |
| math_3_1 | done | none (teachers asked for 16 lessons; flag with proposed split) | 16 lessons (L16 = summative assessment) needs lesson insertion |
| math_3_2 | done (session 2) | 8 x 40 (already trimmed in session 1); stale UNIT.totalDuration (600) fixed -> 320 (r2-001); L8 design-exchange-play game already present | -093: teacher wants 12 lessons (KICD 12), flagged r2-002 (needs lesson insertion); -094 keep Integrity/Financial Literacy: accepted; -092 rubric deferred |

## Session 3 (2026-11-09, later): decisions by Mark and what was done
- **Rubric (Mark: 'make the changes now, I'll inform the partner'):** contract revision R1 = new required `belowExpectations` on every FINAL_EXPLANATION rubric row. ALL contract changes are listed in `CONTRACT_CHANGELOG.md` (repo root; where-in-repo table + partner checklist). Done: 407 rows in the 85 revised modules (change records `<module>-r2-rub-NNN`), 50 rows in `generators/data/g11_bio_*`; schema, validator, renderer (4 columns), generator schema/prompt, repair scripts, docs. Escape hatch `CBE_LEGACY_RUBRIC=1` is used only by `revise_build.py` for the three-level baseline render. Only `coremath_1_1` (3 rows) and 21 `math_*` rows use KICD Below wording from the PDF; the other Core Maths criteria are teacher-written and match no KICD indicator, so 'adopt the KICD rubric' (journal items in coremath modules) is NOT met literally: Mark/teachers decide.
- **META/numbering (Mark: option b, display labels only):** `scripts/round2/sync_display_labels.py` sets META.titleDoc/subtitleDoc (number, name, lesson count) and SUMMARY_TABLE.subStrand from UNIT.substrand for bio_/chem_/phys_/coremath_ modules (10 changed). Ids, outputDir, filePrefix, folders untouched. `revise_apply.py` now derives the Summary Table label from UNIT.substrand (`display_id_name`) so it no longer reverts. Not applied to math_*, gensci_*, essmath_* (no journal). **Collision to decide:** bio_1_1 (now 'Cell Structure and Specialisation', KICD 1.3) and bio_1_3 (KICD 1.3 too) cover the same KICD sub-strand. Re-run the script after any lesson-count change.
- **Lesson splits (Mark: 'do the splits'), new tool `scripts/round2/revise_lessons.py` + `ROUND2_SPLIT_BRIEF.md`:** coremath_2_6 8->12, coremath_3_1 8->16 (L16 new summative assessment), coremath_3_2 8->12 (old L1, L6, L7, L8 split), coremath_2_9 8->13. All lessons 40 min, five phases, pacing line = 40, cross-references re-pointed, validators PASS (85 files / 749 lessons). Change records `<module>-split-NNN` (teacher_decision true). **Every new/reworked lesson is model-drafted and needs a teacher read-through.** NOT split (left as trimmed 8 x 40): coremath_1_2 (teachers gave conflicting requests), 2_1 and 2_7 (wording reads as 'make each 40 min', already done) - Mark can ask for splits.
- **Flags from agents:** coremath_2_6 lesson 3 kept (teacher -077 'drop lesson 3' conflicts with the 12-lesson count; flag r2-flag-001); 2_6 L11 test shortened to 26 min; 2_9 marathon '1.8 km ahead at minute 73' should be ~1.9 km (existing text, all lessons); 3_2 L12 fair-game example needs a maths check; 3_1 L16 time tight.
- **Tooling gotchas:** use `venv/bin/python` for revise_apply/revise_build (plain python3 lacks the anthropic and lxml packages: false 'tracked-change verification failed'); set `CBE_REVISED_DIR` in the same shell command.

## Session 3, later answers by Mark (2026-11-09)
- **bio_1_1 vs bio_1_3 (both KICD 1.3): RESOLVED 2026-11-09 (Mark).** The teacher-template sequence (was `bio_1_1`) is now the live `bio_1_3`; the generated 'Cell Biology' is kept in `backup_alternates/bio_1_3_generated/`. Flag `bio_1_3-r2-flag-002` asks teachers for a quick re-review. See RELABEL at the top.
- **schemaVersion bump to 1.1.0 everywhere + 4 levels on `main`:** done; see `CONTRACT_CHANGELOG.md` ('schemaVersion 1.0.0 -> 1.1.0: where and why').
- **Grade 11:** HOLD (Mark). The Grade 11 Biology data modules have four levels and version 1.1.0, but their docx/PDF/JSON outputs are NOT regenerated.

## Cross-cutting open decisions (for Mark)
1. **Rubric:** wait for the partner (4th level). Several teachers also ask for KICD rubric TABLES by sub-strand (criteria + 4 levels); the tables are in the Mathematics PDF.
2. **KICD numbering/names ("Align to KICD"):** Round 2 changed text inside UNIT/lesson `substrand`/FE `subjectLabel` only. `revise_apply` cannot edit `META` (substrand_id, substrand_name, titleDoc, subtitleDoc, outputDir, filePrefix), so documents are mixed (e.g. bio_1_1 headers say 1.3, title says 1.1). Choose: (a) rename META + folders + files (touches partner contract keys, Drive links, index), or (b) edit only `META.subtitleDoc`/Summary label and keep ids and paths (teachers said "retain internal identifiers"). `SUMMARY_TABLE.subStrand` was also not re-derived in several modules.
3. **Lesson counts vs KICD** (bio_1_2 6 vs 24, bio_2_2 8 vs 22, chem_1_3 10 vs 30, chem_1_5 12 vs 34, etc.): all kept; teachers mostly confirm they are condensed units. Decide whether any should be expanded (large new content).
4. **Core Mathematics lesson splitting** (2_6, 2_9, 3_1, 2_1, 2_7): teachers asked for "split doubles into 40-min lessons" (more lessons) but agents trimmed instead. Inserting lessons needs a tool that renumbers lessons, Summary Table and FE (coremath_1_1 replaced lessons via `set`, so replacement works; insertion is untested).
5. **Teacher-supplied facts that look wrong or unverifiable** (not written as fact): chem_2_1 silica gel/CaCl2 uses; phys_3_4 fingerprinting; phys_1_4 history (shaduf, bellows).
6. **Human verification tasks:** PhET controls (phys_3_3, phys_4_1), ARES offline modules (phys_3_1, bio_1_1 card set 10), Kiswahili terms (all subjects), tariff, photo sources, matcher picks (chem_1_3).
7. **Missing journals:** General Science, Essential Mathematics, and Core Mathematics (none will exist for Core Mathematics); non-flagged Physics items. Mathematics (`math_*`) is DONE, its journal was the one mislabelled 'Core Mathematics'.

## Next steps (in order)
1. `/restart`. Check `git status` (all Round 2 work is uncommitted in `data/revised_2026-10_full/` plus `scripts/round2/`).
2. ~~Finish the 4 interrupted Core Maths modules~~ DONE session 2 (2026-11-09). Remaining 80-minute modules `coremath_2_6` (L5-L8) and `coremath_3_1` wait for Mark's lesson-split decision.
3. Corpus validator PASS 2026-11-09 (85 / 728). Still to do: `python3 scripts/revise_build.py --all` and `python3 scripts/revise_build.py --all` (read REVIEWER_BRIEF.md for the journal/index rebuild: `build_revision_journal.js`).
4. Ask Mark the cross-cutting decisions above (1, 2, 4 first).
5. After sign-off (STATUS: Flagged_Items wins if journals differ): promote revised modules into `generators/data` + pipeline JSON, regenerate docx/PDF/teacher index, run `validate_corpus.js`, `scripts/check_resource_links.py`, `scripts/run_lesson3_checks.sh`, `validate_consistency.py`, and the `resourceLinks` host check (0 `ares.edu`). STOP for Mark's approval before commit, push or Drive sync.
6. General Science, Essential Mathematics: wait for journals. Core Mathematics (`coremath_*`, real): starts later, no teacher reviews.
