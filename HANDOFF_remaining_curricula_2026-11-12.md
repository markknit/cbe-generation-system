# Remaining three curricula: working checkpoint and takeover

2026-11-13. **Current stage: first expansion batch independently reviewed/built (27 lessons,27 Word/PDF pairs); continuing remaining authoring under standing authorization.** Mark wants the remaining lessons for General Science, Essential Mathematics and Core Mathematics created using the reviewed OpenAI-only approach. He specified the clean-pause and takeover policy below before work begins.

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

## Current checkpoint and exact next action

First expansion batch is COMPLETE for scoped independent content/artifact review:GS 1.1 seven lessons, Essential 1.1 eight, Core 2.6 twelve =27. `data/curriculum_expansion_2026-11/BATCH_01_STATUS.md` and `Batch_01_Reviewed.zip` are current report/archive. All 27 Word/PDF pairs and 3 R1 JSON exports pass audit;54 registered calculations and 18 pipeline tests pass. Accepted current fingerprints/evidence are in `reviews/<module>/content_acceptance.json`; final package manifest/receipt are under evidence. Initial reviews/findings and rechecks remain separate. Five finding instances closed (Science 2 content+1 resource, Core 2 content, Essential 0). No teacher classroom sign-off or production promotion.

Including the frozen pilot, six units/58 lessons have independent reviews. Thirty-seven units remain undeveloped. Sources for the next three are visually verified:Essential 1.2 Indices, Core 2.7 Surface Area and Volume of Solids, GS 1.2 The Cell. No official count appears in those selected tables. Begin with materials/solutions and a justified allocation; do not use old eight-lesson counts. Cell lessons need genuine, accurately identified microscopy images/schematics and traceable permission/credit. Exploratory public-domain microscopy downloads are only in `/tmp/cbe-cell-assets` and not selected/committed for teaching; an infected-maize image and specialised frog-cell image are not automatically typical plant/animal exemplars. Do not imply an illustration is a real micrograph. Temporary authoring helpers are not canonical; continue by editing full JSON records.

The user’s earlier explicit three-reviewer approach carries forward under the current remaining-lesson development instruction. The extra async confirmation question was unnecessary and is not a blocker. Reuse `/root/review_core_resumed`, `/root/review_essential_resumed`, `/root/review_science_resumed` for each applicable unit; do not redo completed reviews or seek routine authorization again. Preserve findings; at most two correction passes and focused rechecks. Complete/record each batch checkpoint before continuing; the remaining-lesson scope is already authorized. No separately billed model generation.

Root centrally checks account usage before units/reviewer batches and at least every 5 minutes during active work. Reviewer runtimes cannot query the endpoint reliably; an attempted escalation waited 956 seconds until root interrupted it. **Do not request subordinate usage escalation.** Relay a fresh root-verified reading; if no fresh reading is available, stop new authoring/reviewers. Last root reading 21% at 2026-11-13 09:00 UTC; no pause latch. At≤10%, save at the next small clean boundary, execute `/update`, commit the exact handoff locally and end turn.

Source status: the original 40-unit expansion queue contains 33 located pixel packs; six have verified source records (three now reviewed/built, three prepared next),27 need transcription checks, and seven Core units lack readable current-PDF requirements (1.1–1.3,2.1–2.4). Actual work remaining is 37, tracked in inventory/progress.json; source_inventory.remaining_units is the original queue count, not live completion. Core PDF repeats contents captures; older OCR is not proof. Official KICD file is viewable but download restricted, connector retrieval failed, and this session exposes no browser surface (CUA inventory empty). No replacement/bypass. A permitted readable source is still needed. Essential Probability internal 3.2/printed 4.2 discrepancy remains to resolve before its batch.

Pipeline: `venv/bin/python scripts/curriculum_pipeline.py check|build|render|pdf|audit MODULE` (choose one verb). Set new-blueprint `isolate_final_materials=true`; final-only data stay out of teaching packs. Content acceptance binds actual input hashes before render. Artifact audit rejects stale outputs and unvetted selections for curated modules. GS 1.1 has an empty vetted-title allowlist because general search returned unrelated hotel/advanced-math content; supplied source/task cards remain. Production matcher unchanged. Root source/asset/math/preflight checks never replace independent content or final layout review.

Partner checks rerun on these 3 files/27 lessons:render 3 bundles PASS; ingestion FAIL,0/3 conform,15 R1-vs-R0 findings. Partner checkout clean/unchanged. Current exports remain R1; do not downgrade or edit partner to mask the blocker. Report gate exit/status accurately—contract-drift report exit 0 is not conformance. No push, promotion, publication or Drive action.

## Existing acceptance/delivery limits

Teacher pacing, prerequisites, practical feasibility and classroom acceptance remain open. Partner rendering works, but installed R0 ingestion rejects R1 schemaVersion 1.1.0 and belowExpectations. Do not downgrade our schema or edit the partner checkout merely to make ingestion pass. Baseline defects are documented separately and were not repaired by the pilot.

The live weekly percentage is now readable through the documented account interface; exact monetary subscription cost and teacher correction time remain unmeasured. Runtime account-specific usage snapshots/latch are gitignored in `data/codex_usage_guard/`. Use fresh readings, not the dated readings in a session log.
