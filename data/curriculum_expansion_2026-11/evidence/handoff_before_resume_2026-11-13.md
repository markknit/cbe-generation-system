# Remaining three curricula: working checkpoint and takeover

2026-11-13. **PAUSED at the user’s 10% weekly threshold (09:43 UTC). 49 new lessons are content-accepted: 35 also have final-artifact PASS,14 Core lessons have an unfinished final PDF check.** Mark wants the remaining lessons for General Science, Essential Mathematics and Core Mathematics created using the reviewed OpenAI-only approach. He specified the clean-pause and takeover policy below before work begins.

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

**Do not launch authoring/reviewers while the quota pause is latched.** At2026-11-13T09:43:23.518964UTC the normal guard returned10% remaining, exit10, pause_requested=true, threshold_reached. Root stopped new work, asked the sole running reviewer to save/stop, and performed `/update`. No new content/review or optional package work after that boundary. Runtime latch remains in ignored data/codex_usage_guard/state.json. `/restart` uses read-only; after an explicit authorised resume, use `--resume` with fresh allowance above 10%.

Work persisted in `data/curriculum_expansion_2026-11/`. First batch is reviewed/packaged in local commit28153eb6:GS1.1(7), Essential1.1(8), Core2.6(12)=27 lessons,27 Word/PDF pairs,54 checks. `BATCH_01_STATUS.md` and `Batch_01_Reviewed.zip` remain frozen. Second batch:Essential1.2 Indices8 lessons/38 checks has content+scoped final artifact PASS; Core2.7 Surface Area and Volume14 lessons/39 checks has accepted content, all 9 document pairs built and technical audit PASS, but final PDF propagation review is incomplete. Read `BATCH_02_STATUS.md` and evidence/quota_stop_2026-11-13.json for current hashes/counts. No second reviewed ZIP exists yet.

**Exact next action after permitted resume:** finish the Core2.7 review in `reviews/batch_02/coremath_2_7_layout_review.md`. Its reviewer passed all canonical Word propagation, key separation and a 70-page visual contact survey/targeted samples. A subsequent PDF-text comparison raised AssertionError before completion; the exact failing string was not investigated before stop. No confirmed missing text or final artifact PASS/HOLD is established. Existing extracted PDF/Word texts are safely copied to `reviews/batch_02/recovery_extracts/coremath_2_7/` (temporary originals in /tmp/core27final). Identify that exact mismatch, distinguish extraction/normalisation from actual loss with a targeted page, then recheck final null slots/current fingerprint and issue a scoped final verdict. Do not redo completed mathematics/source review or reauthor14 lessons. Preserve incomplete report, append focused completion evidence separately.

Core current accepted fingerprint:261cfa07c19ffbd3eb912f3e18573dde71de2328970b3c276b3224a3478b6378. Indices:9ea6cbd6b6480e24570ebdeccb91f952363c892e8058b8dde520c0835c08f78c. Canonical complete JSON is under sources/materials/manuscripts/blueprints; working/coremath_2_7_lessons.json is an obsolete raw assembly snapshot. Content acceptance files already bind current independent reports. Core’s original net error/fix and prior interrupted-review evidence are preserved; recovery report explicitly accepts content and verifies corrected actual embeddings. Indices needs no repeat content or artifact review.

Counts:49 new lessons authored/content-accepted across5 expansion units;35 reviewed through artifacts plus14 pending final check. With frozen pilot31 lessons,80 are content-accepted,66 reviewed through artifacts across 8 authored units. 35 units have no new lessons:GS1.2 The Cell has verified source but needs genuine/credited microscopy assets;27 located units need transcription checks;7 Core units are blocked (1.1–1.3,2.1–2.4). Thus36 units are not fully closed if the one pending Core artifact review is counted. No new total lesson count is inferred from baseline eight-lesson records.

After Core is closed, package/checkpoint second batch, then continue already authorised remaining lessons. Preserve first-batch archive. Shared evidence/artifact_audit.json is latest selected-unit audit, not a cumulative verdict; dated snapshots now exist for batch1 and both batch2 units. New per-module resource-policy entries conservatively stale older standard-build cache signatures; first-batch archive retains its exact reviewed policy/output snapshot. Do not casually regenerate frozen deliveries or claim a fresh whole-workspace audit was run. Per-module accepted content/actual artifact manifests remain inspectable.

Standing three-independent-reviewer workflow continues without routine reauthorization; only reviews are delegated. A server restart removed the previous agents. Current recovery agent /root/review_core_recovery stopped cleanly and saved its incomplete final report. If it is no longer available after takeover, create a scoped replacement under standing review authorization and use saved evidence, not a complete restart. Root centrally checks/relays quota at least every 5minutes and before units/reviewers; subordinate usage-helper escalation previously hung 956seconds and must not be repeated. No fresh verified reading means no new work.

Source inventory original queue is40 (not live progressremaining). Six source records verified:five now authored plus Cell. Local Core PDF has repeated contents captures; older OCR cannot fill missing requirements. Official KICD file download is restricted, connector retrieval failed, and no browser surface was available. No bypass. Essential Probability internal3.2/printed4.2 discrepancy remains. Temporary cell images CIL12587(infected maize),10431(specialised frog barrier cells),9526(green alga) were exploratory/unselected and must not be labelled generic typical land-plant/animal cells without accurate context.

Partner rechecked all 5 exports / 49 lessons:5 bundles render; R0 ingestion fails 0/5 conform,23 drift findings. Indices adapter fidelity 3/7 also fails on attribution/rubric text; links roundtrip and structure pass. Partner checkout unchanged. Do not downgrade R1 or edit partner to mask this. No paid model API calls, push, promotion or Drive publication. Classroom/practical acceptance remains open.

## Existing acceptance/delivery limits

Teacher pacing, prerequisites, practical feasibility and classroom acceptance remain open. Partner rendering works, but installed R0 ingestion rejects R1 schemaVersion 1.1.0 and belowExpectations. Do not downgrade our schema or edit the partner checkout merely to make ingestion pass. Baseline defects are documented separately and were not repaired by the pilot.

The live weekly percentage is now readable through the documented account interface; exact monetary subscription cost and teacher correction time remain unmeasured. Runtime account-specific usage snapshots/latch are gitignored in `data/codex_usage_guard/`. Use fresh readings, not the dated readings in a session log.
