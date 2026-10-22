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
| Presentation HANDOFF + initiation prompt | **Drafted 2026-10-21** (`HANDOFF_presentations_2026-10-21.md`); Mark to review | Locked decisions, open questions (logos, lesson-length source, Drive destination), phased plan (Phase 0 preconditions to Phase 4 distribution). First build session starts at Phase 0. |
| SeaVuria Build Manual in repo | Committed 2026-10-20 (design input only; not signed off) | `docs/presentations/BUILD_MANUAL.md` (+ `.docx` source) and `OVERRIDES.md` (draft; where the manual conflicts with CLAUDE.md Branch Policy, the overrides win). Science manual is current (Mark, 2026-10-21); the Biology-only "Cells" manual may be used for that one lesson only. `main`'s CLAUDE.md points here. |
| Manual vs branch-rule conflicts | **Decided 2026-10-21 (Mark); recorded in OVERRIDES.md** | Footer: `config/attribution.yaml` is the guide (`slide_footer` added on `main` 2026-10-21; YAML now says "ARES Education"). ARES links: on the slide as a clickable icon, not a visible URL. Science errors: flag in the build log, fix only on `main`. Maths: processed last, probably no separate process. Still open: icon design, `slide_footer`, teacher review. |
| Output commit policy | **Decided 2026-10-21 (Mark):** decks/PDFs gitignored, shared via Drive; only `data/outputs/presentations/_samples/` committed | Applied on `main` (`75b4fad2`: CLAUDE.md, `.gitignore`, WORKFLOW.md). Drive destination for decks still to be decided and added on `main`. |

## Known Issues / Lessons Learned

*(none yet)*

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
  - **Ambiguous: 24 lessons** say 40 minutes but allow an 80-minute double period as an option (phys_2_1, phys_3_2, phys_3_3, phys_3_4, phys_1_4, chem_1_1, chem_1_3, bio_1_2 L2). Proposed rule (Mark to confirm): the leading figure is the deck's length; the option goes in the build log. One lesson, chem_1_3 L4, also gives per-phase minutes inside the string.
  - Note "2 lessons (80 minutes)" (bio_3_2 L7–10, phys_4_1 L5, phys_4_2 L5) leads with "2 lessons", so the parser must read the minutes figure, not the first number.
- **`UNIT.totalDuration` is NOT reliable** (11 of 28 modules, e.g. bio_1_1: lessons sum 840 min, totalDuration says 480; phys_1_2: 400 vs 240). It assumes 40 minutes per lesson. Don't use it; use per-lesson `duration`.
- Nothing committed or changed apart from this file. Still open: logos (Mark); confirm the 40/80 rule above; HANDOFF review; Drive destination; Maths guidance. For `main` (not edited here): CLAUDE.md lines 258–259 still say presentations are deferred/"don't build it", contradicting the Branch Policy.

## Updates — 2026-10-22 (second entry) — Mark's decision: lesson-length rule
- **Decided (Mark):** the leading 40/80 figure in each lesson's `duration` string is the deck length; optional double-period extensions (24 lessons) are noted in the build log only. HANDOFF §3 and open question 2 updated to match.
- Phase 0 still open: logos (Mark); HANDOFF review; Drive destination; Maths guidance.
