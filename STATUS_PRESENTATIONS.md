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
| SeaVuria Science build manual (design spec) | Added 2026-10-20; overrides are a DRAFT | `docs/presentations/BUILD_MANUAL.md` (v1.0, teachers' spec) and `OVERRIDES.md` (where it conflicts with CLAUDE.md Branch Policy; overrides win). Open for Mark: link placement (hidden slide vs clickable while projecting) and footer/attribution rows. The Science manual `.docx` is not yet in the repo. |
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
- Added `docs/presentations/BUILD_MANUAL.md` (three raw-HTML callout tables converted to blockquotes) and `OVERRIDES.md` from Claude.ai's output.
- Not received/done: `STATUS_PRESENTATIONS_additions.md`, `main_CLAUDE_pointer.md` (CLAUDE.md pointer line on `main`), and the Science manual `.docx`; these rows/entry were written by Claude Code from the instructions, not pasted from the prepared additions.
- Still open: Mark reviews OVERRIDES (footer, link-placement); Claude.ai project upload swap (Mark).
