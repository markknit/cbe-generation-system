# Remaining three curricula: working checkpoint and takeover

2026-11-12. **Current stage: weekly-usage guard configured and verified; remaining curriculum authoring has not started.** Mark wants the remaining lessons for General Science, Essential Mathematics and Core Mathematics created using the reviewed OpenAI-only approach. He specified the clean-pause and takeover policy below before work begins.

## Locked decisions

- Weekly stop threshold: **10% remaining or lower**, stored in `config/codex_usage_guard.json`.
- Check before each module/reviewer batch, after a completed unit, and at least every five minutes during active long work. Use `python3 scripts/check_codex_usage.py`.
- At the threshold, launch no new lesson/module/reviewer work. Reach the next small clean stopping point, checkpoint unfinished work, and perform `.claude/skills/update/SKILL.md` directly. This is the `/update` workflow; no literal UI command submission is necessary. Interpret a user-typed `?/update` as the same update request.
- Save exact completed/pending items, paths, reviewer states, checks, blockers and next action in STATUS.md and this handoff. Commit locally, report paused, then end the turn. Do not push/publish without authorization.
- Do not automatically switch accounts, consume quota resets or purchase credits. No separately billed model API generation is authorized for this route.
- Usage-unavailable exit 20 prevents launching further authoring/reviewers until a fresh reading is verified. Exit 10 requests a clean pause; exit 0 permits already authorized work. The helper latches a stop request; `--resume` clears it only after explicit resume and fresh quota above the threshold.

## Takeover from the same point

The next user needs this same checkout and work files, using their own authorized sign-in. They run `/restart` to verify branch, git state, control documents and this handoff. The Codex usage check in `/restart` is `python3 scripts/check_codex_usage.py --read-only`; it does not mutate the pause latch or resume generation.

After the next user explicitly asks to resume, run `python3 scripts/check_codex_usage.py --resume`, verify exit 0 and continue the exact recorded next action. Never restart completed modules merely because the account/session changed. No credentials are stored in this handoff. A different machine/checkout requires an explicitly authorized transfer of the local commit and working files first; nothing is automatically pushed.

This is an active-work checkpoint policy, not an installed idle-time watcher. Save each lesson/review incrementally because server resets or quota depletion can still interrupt work between checks. Running reviewers should write their own findings progressively and save at the next clean boundary when asked to stop.

## Existing completed work

Reviewed pilot: `data/codex_pilot_2026-11/INDEPENDENT_REPORT.md` and `Review_Package_Reviewed.zip`, committed in `73f97e98`. Pilot units: `gensci_2_4`, `essmath_2_8`, `coremath_2_5`; 31 lessons, 27 DOCX and 27 PDF. Three initial subject reviews and focused rechecks are complete; do not redo them. The original draft ZIP/report/extraction are historical snapshots.

Disk inventory of the existing baseline modules: General Science 16, Essential Mathematics 13, Core Mathematics 14, totaling 43. Three units have reviewed pilot replacements; the other 40 baseline units are the initial queue to reconcile against authoritative curriculum sources, not an assertion of official lesson counts. Reviewers found defects in old prose, so use source requirements rather than treating the baseline as a reliable authoring source.

## Exact next action

Inventory the remaining authoritative curriculum sections and prepare the per-module source/outcome/material/assessment plan for the 40 remaining units, applying the reviewed pilot process and usage guard. The available Core Mathematics PDF has an obscured Trigonometry 1 requirements table; identify source gaps rather than inventing requirements or claiming a full-curriculum result. Lesson allocations are teaching-design decisions unless a readable official source explicitly provides them.

Keep authoring/manuscripts/materials/solutions and independent review records separately inspectable. Source pixels override OCR; solve all tasks, provide actual handouts, distinguish formative from final evidence, and preserve original reviewer findings. Use no more than two correction passes before recording unresolved teacher judgements. Promotion, publication and partner delivery remain separate from isolated authoring.

## Existing acceptance/delivery limits

Teacher pacing, prerequisites, practical feasibility and classroom acceptance remain open. Partner rendering works, but installed R0 ingestion rejects R1 schemaVersion 1.1.0 and belowExpectations. Do not downgrade our schema or edit the partner checkout merely to make ingestion pass. Baseline defects are documented separately and were not repaired by the pilot.

The live weekly percentage is now readable through the documented account interface; exact monetary subscription cost and teacher correction time remain unmeasured. Runtime account-specific usage snapshots/latch are gitignored in `data/codex_usage_guard/`. Use fresh readings, not the dated readings in a session log.
