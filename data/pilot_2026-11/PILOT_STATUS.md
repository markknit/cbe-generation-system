# Pilot: "checks built into the first pass" for GS / Essential / Core Maths, Grade 10 (2026-11-12)

**State: PAUSED, awaiting Mark's decision on the next step and cap. Option 2 is complete; total spend $7.65 of the $10 cap. Pilot files and code were committed in `77837f7c` and are on `origin/main`. Nothing from the pilot has been promoted to `generators/data`; Drive sync has not been verified.**

> **Next approach chosen, 2026-11-12:** Mark approved a separate OpenAI-only evaluation. See `data/codex_pilot_2026-11/REPORT.md`. This API experiment and its spend remain a historical baseline; resuming it is not the current next step.

## Why
Mark's question: the Round 2 process (generate, then several audit/repair rounds, then reconcile the Final Explanation) cost about $3.50-4 per
module on top of generation. For the 43 remaining Grade 10 STEM modules (General Science 16, Essential Maths 13, Core Maths 14), and later
Grade 11 and non-STEM, can the checks be built into the first pass instead? Priorities (Mark): accuracy first, cost second, speed least.

## Initial run (3 modules, 8 lessons each, new process)
1. KICD section for the sub-strand cut by hand from the repo OCR text (`data/pilot_2026-11/curriculum/*.txt`, 4-12k characters instead of the whole 70k).
2. `src/generate_substrand.py` as-is (fact sheet, 8 lessons, consistency pass, FE generated from the finished lessons with its own check loop,
   derived Summary Table) PLUS `scripts/pilot/authoring_checklist.txt` appended to the system prompt (the Round 2 audit rules written as writer rules).
3. ONE Opus 5.5 lesson audit (Round 2 rules, `lesson_converge.review`, quotes and arithmetic verified in code), Sonnet adjudication.
4. ONE Sonnet FE-versus-lessons audit (`fe_converge.review/verify/adjudicate`).
5. Baseline: the same Opus audit on the OLD first-generation module in `generators/data` (Essential and Core only).
Fixes were not applied in this initial run; see the Option 2 result below. Driver: `scripts/pilot/pilot_run.py`. Outputs: `data/pilot_2026-11/modules/pilot_*_data.js`, `result_*.json`, `run_*.log`.

## Results
| | gensci_2_4 (Acids, Bases and Salts) | essmath_2_8 (Commercial Arithmetic 1) | coremath_2_4 (Trigonometry 1) |
|---|---|---|---|
| New process, measured cost | $1.74 | $1.70 | $1.53 |
| of which generation / Opus audit / adjudication / FE check | 1.09 / 0.30 / 0.11 / 0.24 | 1.19 / 0.28 / 0.11 / 0.12 | 0.99 / 0.29 / 0.12 / 0.13 |
| Lesson defects confirmed in new module | 2 | 2 | 3 |
| Same audit on old first-gen module | not run | 6 | 13 |
| FE-vs-lessons defects confirmed | 0 | 0 | 0 |
| Baseline audit cost | - | $0.63 | $0.67 |

Defects found in the initial new modules (fixed in Option 2 below): gensci L3 "bleaching because basic" and L8 "H+/OH- explain salts in air"; essmath L7 promise that
L8 never tests, and currency round-trip loss computed wrongly; coremath L3 sin 35 RAD/GRAD error values wrong, flagpole 5.6 m vs 7.3 m (L7).
FE generator loop: gensci stopped with 3 style-level items (`logs/final_explanation_issues/pilot_gensci_2_4.json`); essmath and coremath clean.

## Cost comparison (estimate, 2 of the 3 numbers are measured)
- Old: first generation about $1.0-1.2 plus Round 2 loops $3.50-4 = about $4.6-5.2 per module.
- Initial estimate before Option 2: measured $1.53-1.74, plus estimated fixes and audit, about $2.1-2.6 per module. Superseded by the Option 2 estimate of $2.5-3.0 per module, or $110-130 for 43 modules. Untested levers: batch generation, fewer FE loop rounds, Sonnet audit for lower-risk subjects.

## Caveats
- n = 3 modules; baseline compared whole pipelines (old modules predate fact sheet and consistency pass), not the checklist alone. Sending only the KICD section was not isolated either.
- One Opus audit does not prove a module clean (benchmark 2026-11-12: Opus and Sonnet each miss defects the other finds). The Option 2 confirming audit found further issues in two modules.
- Core Maths: the repo OCR text `data/raw/curriculum_text/core_mathematics.txt` has Core 2.4 Trigonometry 1; the question whether the Core PDF equals the March Maths PDF is still unconfirmed.
- `src/generate_substrand.py` reads three optional env vars (`CBE_GEN_OUT_DIR`, `CBE_CURRICULUM_TEXT_FILE`, `CBE_EXTRA_SYSTEM_FILE`); defaults unchanged. Committed in `77837f7c`.

## To resume (needs Mark's go-ahead and a cap)
- Option 2 is complete; the two new findings and the FE re-check after lesson edits remain open (see below).
- Option 1: full 43, General Science first (cap about $50 for 16 modules), stop for review after the subject. Run the free steps first: KICD sub-strand and lesson-count table for all 43, hand-cut KICD sections (the repo slicer finds none for General Science), real lesson counts (the pilot used 8).
- Env for a run: `CBE_REVISED_DIR=<abs>/data/pilot_2026-11 CBE_GEN_OUT_DIR=<abs>/data/pilot_2026-11/modules CBE_EXTRA_SYSTEM_FILE=<abs>/scripts/pilot/authoring_checklist.txt venv/bin/python scripts/pilot/pilot_run.py --target <gensci_2_4|essmath_2_8|coremath_2_4> --max-spend N`.
- Before anything is used: nothing from the pilot goes to `generators/data` without Mark's approval.

## Option 2 result (2026-11-12, Mark's cap $1.5, spent $1.39) - `scripts/pilot/pilot_fix.py`, `result_option2.json`, `run_option2.log`
Applied the first audit's confirmed defects with exact find/replace edits (pre-fix files kept as `modules/pilot_*_prefix_data.js`), re-derived the Summary Table, then ran ONE confirming Opus lesson audit (+ adjudication where it reported something).
| | gensci_2_4 | essmath_2_8 | coremath_2_4 |
|---|---|---|---|
| Defects from audit 1 | 2 | 2 | 3 |
| Edits applied (failed) | 2 (0) | 2 (0) | 5 (0) |
| Confirming audit finds | 1 new | 0 (clean) | 1 new |
| Cost fix + audit + adjudication | $0.51 | $0.38 | $0.51 |
- New finding gensci L6 overview: class model named "Mombasa Kitchen Puzzle" vs "Mombasa Kitchen Model" everywhere else (naming, minor).
- New finding coremath L5: refers to a "tan column" in the Lesson 4 table that does not exist (cross-reference; real).
- Core Maths flagpole fix: Lesson 7's 7.3 m example was reworded to "a tall pole" (the school flagpole stays 5.6 m).
- NOT run (cap): FE re-check after the lesson edits. Free keyword scan of the FEs: gensci FE mentions H+ 4 times and hygroscop* 4 times (could depend on the changed L8 wording); coremath FE says "flagpole" 5 times and "sin 35" 5 times (values unchanged); essmath FE mentions "margin" once. Needs one FE check per module (about $0.12-0.24 each).
- Reading: one fix round plus one confirm audit is NOT enough to reach clean on 2 of 3 modules (a second fix round would be needed, about $0.4-0.5 per module). Real per-module cost to a clean module is therefore about $1.5-1.7 (generate + audit) + $0.4-0.5 per fix round, probably 2 rounds, + FE check = about $2.5-3.0, not $2.1-2.6. 43 modules: about $110-130.
- Total pilot spend: $6.26 + $1.39 = $7.65 of the $10 cap.
