# Remaining three curricula: working checkpoint and takeover

2026-11-13, resumed at23:13UTC after explicit user instruction. Fresh allowance97% cleared the prior10% pause. **58new lessons content/artifact-reviewed across6expansion units;89including the frozen pilot.** Quota is not currently paused. The separate usage guard remains in force.

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

## Completed reviewed milestones

- Frozen pilot:31 lessons across `gensci_2_4`,`essmath_2_8`,`coremath_2_5`,27 DOCX/PDF pairs. Keep `data/codex_pilot_2026-11/Review_Package_Reviewed.zip` unchanged.
- Batch01:27 lessons in GS1.1,Essential1.1,Core2.6;27 pairs. Frozen `Batch_01_Reviewed.zip` remains byte-identical to its receipt.
- Batch02:22 lessons in Essential1.2(8) andCore2.7(14);18 pairs plus2 R1 exports packaged as `Batch_02_Reviewed.zip`,receipt `evidence/batch_02_package.json`. All77 registered calculations and fresh selected-unit18pair audit pass. Independent Core completion closes the interrupted PDF check with110/110 canonical checks,unchanged fingerprint/all8standard artifact hashes and10null final resource slots. Original incomplete report and quota checkpoint preserved; no content/output correction or regeneration was needed.

Core completion:`reviews/batch_02/coremath_2_7_pdf_completion_review.md`;reproducible check/script+JSON in its evidence folder. The unsaved historical assertion's execution point is unknown. Reproduced apparent missing strings resolve as table-cell extraction order,page continuations and retained line-end hyphens. Prior70page contact survey plus targeted readable pages support a scoped review,not exhaustive line-level visual/classroom validation. Batch02 report/archive freezes its earlier milestone counts; subsequent progress is below.

## Latest completed unit and exact next action

Essential1.3 Quadratic Equations(I):9 new40minute lessons,9 complete material cards and19registered calculations. Canonical files in sources/materials/blueprints/manuscripts;content fingerprint `1f02c60b4122722a1d83e9ad7476c0adb7a99bd749f914c7c673c64f7cea1c01`. Independent initial review accepted every source/fixed task,all9records/assessment/rubric and5actual draft companions with0confirmed errors and0content corrections. Acceptance JSON binds `reviews/batch_03/essmath_1_3_initial.md`.

All9Word/PDF pairs built and technical audit PASS,with final independent PASS below. Root corrected one render-only resource-scope mismatch before final review:systems,formula,completing-square and complex/square-root methods were matched to factorisation-only tasks. Evidence/initial titles and final allowed titles are in `evidence/essmath_1_3_resource_curation.json`. Only4standard pairs were rebuilt;canonical content/fingerprint stayed unchanged. The global policy change conservatively stales old standard cache signatures; do not rerender frozen deliveries casually. Existing archives retain their exact policies and outputs.

Independent final report `reviews/batch_03/essmath_1_3_layout_review.md` now issues PASS for all9Word/PDF pairs.620/620canonical checks pass in each format;67pages surveyed/18readable samples+detail. Final data/key isolation,blank response cells,all9attribution blocks and10final null slots pass. Report retains nonblocking page-split/resource preview/classroom limits. `Batch_03_Reviewed.zip` and its receipt/manifest package this one-unit milestone;no content correction was needed. Do not repeat completed source/math/content/artifact reviews at this unchanged fingerprint.

**Exact next action:** run `python3 scripts/check_codex_usage.py`,then author Core2.8 VectorsI materials/solutions first from verified `sources/coremath_2_8.json` and its pixels. Create a justified lesson allocation,blueprint,complete manuscript and observable final evidence,then normal check/build→independent content review→acceptance→render/PDF→audit→visual review gates. Next is GS1.3 NutritioninAnimals; use safe actual food-test protocols and honest observed/not-observed practical evidence. Neither unit has new lesson prose yet. No fresh teacher-permission question is required for the already authorised routine workflow.

After this checkpoint continue already authorised remaining authoring. Core2.8 VectorsI andGS1.3 Nutrition inAnimals have visually verified source transcriptions; Cell remains source-verified but needs genuine/credited microscopy materials. Other24located packs need transcription verification;seven Core units1.1–1.3/2.1–2.4 remain source-blocked. No new lesson total is inferred from baseline eight-lesson defaults. Essential Probability internal3.2/printed4.2 discrepancy remains explicit.

## Progress and remaining scope

58new content/artifact-reviewed lessons across6expansion units. With the31lesson frozen pilot:89content/artifact-reviewed across9authored units.34units remain unauthored. Nine expansion source records are verified:6now authored plusCell/Core2.8/GS1.3. The source inventory's40remaining count denotes the original queue,not live progress.

Partner recheck on6exports/58lessons:6bundles renderPASS;R0enforcing ingestionFAIL,0/6conform,27drift findings. Indices fidelity3/7fails on attribution/rubric text while links and structure pass. Evidence in `evidence/batch_03_partner_verdict.json` and logs. Partner checkout unchanged;do not downgrade R1 or edit it to mask incompatibility. No paid modelAPI calls,push,promotion orDrive publication.

## Review,source and classroom limits

Standing independently delegated review authorization continues;only reviews are delegated,not authoring. Root centrally verifies quota before reviewer batches/units and at least every5minutes. No subordinate helper escalation. Explicit user resume has already authorised this session; do not ask routine repeated review permission. If quota stops again,apply the locked handoff policy above. Resume the exact next unauthored unit after interruptions,keeping completed9at its accepted fingerprint.

Teacher confirmations remain prerequisites,actual pacing,safe/local equipment and reference provision,accessibility and real observed/not-observed practical/digital evidence. Optional resource metadata relevance is not full media playback/content verification;preview and limit use. Classroom acceptance and partner ingestion are not certified by a desk/artifact PASS.

Official Core download is restricted;no bypass. Older OCR cannot supply missing current requirements. Temporary Cell images discussed previously remain exploratory/unselected;do not label infected maize,specialised frog barrier tissue or a green alga as generic typical land-plant/animal cells. No new microscopy asset has been selected in this resume.
