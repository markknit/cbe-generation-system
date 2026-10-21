# STATUS — Presentations branch

*Last updated: 2026-10-20*

The status file for the `presentations` branch (worktree
`/home/markk/ares/cbe-presentations`). For lesson-plan state, see
`STATUS.md` on `main`. The rules are in CLAUDE.md, "Branch Policy —
`presentations`".

## Active Threads

| Thread | Status | Notes |
|---|---|---|
| Branch + worktree setup | Done 2026-10-20 | Created from `main` at `805f9738`, pushed to `origin/presentations`; symlinks + `npm install` done; Step 0 passes in the worktree. Each session: `/restart`, then `git merge main`. |
| Teacher review of example decks | Blocked: waiting on teaching staff | 4 examples in `handoff_bundle_2026-09-29/presentation_examples_deferred/` (Bio L2, Chem L4, Maths L4, Physics L2). Generator design waits on this feedback. |
| Presentation HANDOFF + initiation prompt | Not started | To be written once the review feedback is in. |
| SeaVuria Build Manual in repo | Committed 2026-10-20 (design input only; not signed off) | `docs/presentations/BUILD_MANUAL.md` (+ `.docx` source) and `OVERRIDES.md` (draft; where the manual conflicts with CLAUDE.md Branch Policy, the overrides win). Biology-only "Cells" manual treated as superseded (Mark to confirm which is newer). `main`'s CLAUDE.md points here. |
| Manual vs branch-rule conflicts | Decision pending (Mark) | Footer attribution (must come from `config/attribution.yaml`); ARES links on hidden slide vs clickable while projecting; deck-level science fixes vs "never edit lesson content"; scope beyond Grade 10 science. See OVERRIDES.md. Also: Mark's own 22:31 edit to CLAUDE.md on `main` names `SeaVuria_Science_Lesson_PPT_Build_Manual.md` (not the repo path) and its sentence is cut off ("Make sure it is"); needs finishing/reconciling with the pointer line. |
| Output commit policy | Decision pending (Mark) | ~1 GB per grade if committed; precedent: revised corpus is gitignored and shared via Drive. |

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
