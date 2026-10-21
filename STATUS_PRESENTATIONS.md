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
| SeaVuria Build Manual in repo | Committed 2026-10-20 (design input only; not signed off) | `docs/presentations/BUILD_MANUAL.md` (+ `.docx` source) and `OVERRIDES.md` (draft; where the manual conflicts with CLAUDE.md Branch Policy, the overrides win). Science manual is current (Mark, 2026-10-21); the Biology-only "Cells" manual may be used for that one lesson only. `main`'s CLAUDE.md points here. |
| Manual vs branch-rule conflicts | **Decided 2026-10-21 (Mark); recorded in OVERRIDES.md** | Footer: `config/attribution.yaml` is the guide (`slide_footer` added on `main` 2026-10-21; YAML now says "ARES Education"). ARES links: on the slide as a clickable icon, not a visible URL. Science errors: flag in the build log, fix only on `main`. Maths: processed last, probably no separate process. Still open: icon design, `slide_footer`, teacher review. |
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
