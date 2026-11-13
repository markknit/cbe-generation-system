# Remaining three curricula: working checkpoint and takeover

2026-11-12. **Current stage: reusable tooling and the next three-unit trial prepared; remaining curriculum authoring has not started.** Mark wants the remaining lessons for General Science, Essential Mathematics and Core Mathematics created using the reviewed OpenAI-only approach. He specified the clean-pause and takeover policy below before work begins.

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

## Preparation checkpoint and exact next action

Read `data/curriculum_expansion_2026-11/PREPARATION_REPORT.md` and its `README.md`, plus `config/curriculum_expansion_plan.json`. Tooling and the next trial are prepared; this is the phase checkpoint before new lessons. No new manuscripts have been created. After Mark proceeds to authoring, check live usage and create the three trial units in the isolated expansion workspace: `gensci_1_1` (Introduction to General Science), `essmath_1_1` (Real Numbers), `coremath_2_6` (Area of a Part of a Circle). Start with their `blueprints/<module>.preparation.json`, then actual materials/solutions, compiler-ready blueprint and manuscript. Core has 12 official lessons; the other two selected source tables give no allocation. Derive their lesson count from required scope and prerequisites.

Source inventory: 43 existing IDs, 3 reviewed pilots, 40 remaining. 33 remaining units have located current-PDF crops; 3 trial source records are visually verified, 30 await transcription checks immediately before their batch. **Seven Core units are blocked**, not just Trigonometry: 1.1–1.3 and 2.1–2.4. The local PDF repeats contents-page captures in their requirements region; old OCR cannot fill the gap. The official KICD copy is viewable but owner download-restricted and connector retrieval failed. A permitted readable authoritative replacement is still needed; no restricted-download workaround. The async source-copy question is unanswered. `essmath_3_2` also retains a printed source identifier discrepancy (4.2 Probability I) to resolve before its batch.

Pipeline commands: `venv/bin/python scripts/curriculum_pipeline.py check|build|render|pdf|audit MODULE`. Do not literally pass the pipe-separated list; choose one stage. Preflight/source verification and content acceptance are mandatory. `build` creates compiled data and review companions; `render` requires hash-current independent content acceptance before standard documents. Final audit rejects stale builds/PDFs; visual review and packaging remain explicit manual gates. No reviewer agents launched during preparation; obtain the applicable user authorization before a fresh parallel reviewer batch. Preserve original findings and cap corrections at two passes, recording teacher-only judgements separately. Report the three-unit trial before scaling.

Verified preparation evidence: 16 offline mutation tests pass; three isolated copied pilot units compile exactly to reviewed data, 27 Word texts match after two administrative wording normalisations, 27 PDF page counts match, all 27 Word/PDF pairs pass audit. Limited three-page layout regression sample passes; original 157 tracked pilot files unchanged. An unchanged rerun skips all builds/conversions. Evidence saved under the expansion workspace; ephemeral fixture copies are at `/tmp/cbe-preparation-fixture` and can be recreated with `scripts/prepare_curriculum_fixtures.py`. The reviewed pilot's 31 lessons do not count as newly authored expansion work.

Update `inventory/progress.json` at each saved stage, including lesson counts, findings, correction passes, elapsed work and dated batch quota readings. Quota is account-wide, not an exact per-unit cost meter. Follow the 10% clean-stop policy above. All preparation is saved in a local commit; no push, promotion, partner changes or Drive publication. Production/baseline modules and the historical untracked pilot extraction were preserved.

## Existing acceptance/delivery limits

Teacher pacing, prerequisites, practical feasibility and classroom acceptance remain open. Partner rendering works, but installed R0 ingestion rejects R1 schemaVersion 1.1.0 and belowExpectations. Do not downgrade our schema or edit the partner checkout merely to make ingestion pass. Baseline defects are documented separately and were not repaired by the pilot.

The live weekly percentage is now readable through the documented account interface; exact monetary subscription cost and teacher correction time remain unmeasured. Runtime account-specific usage snapshots/latch are gitignored in `data/codex_usage_guard/`. Use fresh readings, not the dated readings in a session log.
