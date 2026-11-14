# Remaining three curricula: working checkpoint and takeover

2026-11-13local/14NovemberUTC. **Full scope active:228new expansion lessons artifact-reviewed,259including frozenpilot;263new authored,294including pilot;17units without drafts.** Quota not paused;10%guardactive.

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

**Previous checkpoint next action (now underway;see Batch04 below):** run `python3 scripts/check_codex_usage.py`,then author Core2.8 VectorsI materials/solutions first from verified `sources/coremath_2_8.json` and its pixels. Create a justified lesson allocation,blueprint,complete manuscript and observable final evidence,then normal check/build→independent content review→acceptance→render/PDF→audit→visual review gates. Next is GS1.3 NutritioninAnimals; use safe actual food-test protocols and honest observed/not-observed practical evidence. Neither unit has new lesson prose yet. No fresh teacher-permission question is required for the already authorised routine workflow.

After this checkpoint continue already authorised remaining authoring. Core2.8 VectorsI andGS1.3 Nutrition inAnimals have visually verified source transcriptions; Cell remains source-verified but needs genuine/credited microscopy materials. Other24located packs need transcription verification;seven Core units1.1–1.3/2.1–2.4 remain source-blocked. No new lesson total is inferred from baseline eight-lesson defaults. Essential Probability internal3.2/printed4.2 discrepancy remains explicit.

## Progress and remaining scope

58new content/artifact-reviewed lessons across6expansion units. With the31lesson frozen pilot:89content/artifact-reviewed across9authored units.34units remain unauthored. Nine expansion source records are verified:6now authored plusCell/Core2.8/GS1.3. The source inventory's40remaining count denotes the original queue,not live progress.

Partner recheck on6exports/58lessons:6bundles renderPASS;R0enforcing ingestionFAIL,0/6conform,27drift findings. Indices fidelity3/7fails on attribution/rubric text while links and structure pass. Evidence in `evidence/batch_03_partner_verdict.json` and logs. Partner checkout unchanged;do not downgrade R1 or edit it to mask incompatibility. No paid modelAPI calls,push,promotion orDrive publication.

## Review,source and classroom limits

Standing independently delegated review authorization continues;only reviews are delegated,not authoring. Root centrally verifies quota before reviewer batches/units and at least every5minutes. No subordinate helper escalation. Explicit user resume has already authorised this session; do not ask routine repeated review permission. If quota stops again,apply the locked handoff policy above. Resume the exact next unauthored unit after interruptions,keeping completed9at its accepted fingerprint.

Teacher confirmations remain prerequisites,actual pacing,safe/local equipment and reference provision,accessibility and real observed/not-observed practical/digital evidence. Optional resource metadata relevance is not full media playback/content verification;preview and limit use. Classroom acceptance and partner ingestion are not certified by a desk/artifact PASS.

Official Core download is restricted;no bypass. Older OCR cannot supply missing current requirements. Temporary Cell images discussed previously remain exploratory/unselected;do not label infected maize,specialised frog barrier tissue or a green alga as generic typical land-plant/animal cells. No new microscopy asset has been selected in this resume.

## Live Batch04 continuation —2026-11-14UTC/13Novemberlocal

User explicitly authorises all remaining generation/verification without routine phase reauthorization. Read data/curriculum_expansion_2026-11/BATCH_04_STATUS.md and progress before older milestone totals above. Core2.8completed/packaged;GS1.3finalreviewer /root/science_review active;Essential2.1accepted after1photoorientation correction/rendering,reviewer /root/essential_source_review;Core reviewer /root/core27_pdf_completion checks Cell image candidates. Mutation commands must be serial to protect shared cache;reviews may run together. Root81%02:52UTC,no pause. Next rootauthor Core2.9materials/blueprint/manuscript from verifiedsource while completing final gates. Preserve HOLDs/fingerprints. Seven Core gaps remain;user source-path/link reply pending;continue available units.

## Latest live checkpoint —03:17UTC

Batch04all38lessons complete and individually packaged;Core2.9additional12complete/packaged. Exact unitZIP receipts/manifests verify9Word/PDFpairs+1R1export each;prior archives frozen. Total108newreviewed+31pilot=139across13units.30units no new drafts;Cell materials14cards/licensedassets are prepared,12lesson manuscript/blueprint next. Native Word source-image frames preserve original bytes with validated pixel boxes;21initialtests+newWebPguard=22passingtests;independent5imageactualPDFproofPASS,codeCIF-1focusedrecheck pending. Original fullFigure1 must be absent from teachingpack;crop frames are not redaction. ReviewsBATCH04/05 retain exactcurrenthashes and preframecompiler snapshot;do not rerun frozen units solely for newcompiler signatures.

Three reviewers exist:/root/core27_pdf_completion just completedCore2.9;/root/science_review completedNutrition;/root/essential_source_review doingCIF-1codefocusedrecheck. Use followup_task to start completed agents;send_message alone only queues. Earlier Nutrition dispatch was corrected before finalverdict/package. All pipeline mutation commands serialised to avoid sharedbuildstate overwrite. Source surveys completed all12remainingGSand9Essentialpacks(no allocations);22still need root exact transcription,7Coregaps remain. Cell imageblocker resolved by licensed primary examples with visibility/tissue limits;no lesson acceptance yet. Partner10exports/108lessons render10PASS,R0ingest0/10/47drift,Indicesfidelity3/7FAIL;no partner edits. Latestroot65%03:17UTC,no pause;continue allauthorisedwork until complete/source blocked or10%guard. User seven-Core source-link/path reply remains pending.


## Live checkpoint — 2026-11-14 03:27UTC

Cell12lesson manuscript/blueprint built with2registered calculations;full source/materials/everytask/5Word independent review running on /root/science_review.120authored expansion lessons/11units;108reviewed/10;with31frozenpilot139reviewed/151authored.29units no drafts. CIF-1code recheck CLOSED(reportSHA3a4bf0163ce14a08666b0bc4572d29ff04933311efd4ada9d96e87cdf934a00d),caption-only exacthashbridge saved separately. All4newpackage receipt hashes verified. Root63%03:24UTC;continue availableunits under standingauthorisation;no whole-workspace frozen-output rebuild. Next transcribe source for Essential2.2Reflection and Core3.1StatisticsI;science review may return while authoring. No author self-review before independent review. Commit excludes unrelated historicalpilotReview_Package.

## Live checkpoint — 2026-11-14 03:46UTC

Cell12/Reflection11content+artifactPASS/ZIPreceipts/manifests. CoreStatistics16contentPASS and finalreview /root/core27_pdf_completion running;all9pairs/audit saved. PlantTransport12fullcontentreview /root/science_review running. EssentialTrig12fullcontentreview /root/essential_source_review running. Root next authorCoreProbabilityI12officiallessons from viewedprinted48–49;sourceJSON/materialsnotwrittenyet. Full actualproject/performance evidence distinctions required;never countwrittenfictionaldataasperformedactions. Root52%03:45UTC,checkbeforeunits/reviewers/5min.171authoredexpansion/15units,131reviewed/12;25nodrafts,15verifiedsources/18locatedroottranscriptions/7Coreblocked. Allpipeline subprocess sessions completed;serialmutation rulecontinues. Local checkpoint51005f1a is previouscommit;thisnewworknotyetcommitted. SourceHTML/durableextraction whitespace retained as exactevidence;code/JSON/Markdown diffcheck clean. Do not endauthorisedwork at milestone;continueuntilallavailabledoneor10%guard.

## Live checkpoint — 2026-11-14 03:52UTC

Cell12/Reflection11/CoreStats16finalPASS+packages. Transport12/science_review andTrig12/essential_source_review contentPASS/finalreviewsrunning. CoreProbabilityI12/core27_pdf_completion fullcontentreviewrunning. Allpipeline mutation subprocess sessions complete;serialrulesremain.183authoredexpansion/16units,147reviewed/13;24nodrafts,16verifiedsource/17locatedtranscriptions/7Coregaps. Root47%03:51UTC. NextauthorGSRespiration:rootviewedprinted9–10fullsource;sourceJSONnotwrittenyet. PrimaryWSUprotocolPDF accessible viaOSU https://extension.oregonstate.edu/sites/default/files/documents/8836/fs173emakingyogurt.pdf ; sourceprojectNOALCOHOLBREWING,yeastactivityadaptationmustexplicit;safeapprovedlacticprojectacrosslessonswithteacheroutsideperiodlogging,neverfood/tastingclaim. RQCO2/O2undefinedzeroO2,substrateestimatesassumptionbound;sourceIntegritysays aerobicverbatim,butteachcorrectfermentation. Continueuntilallavailabledoneor10%guard;notjustcheckpoint.

## Live checkpoint — 2026-11-14 04:30UTC

263authoredexpansion/23units;228reviewed/20;17nodrafts(7Coreblocked+9GS+EssentialProbability).23verifiedsources/10locatedpending. NewlypackagedResp/Polygon/Circle/Growth;Surfacefinalreviewessential_source_review,Volumefinalreviewscience_review,EssentialStatscontentreviewcore27_pdf_completion. Allpipeline subprocesssessionscomplete;fail-fastserial rule. Root17%04:28UTC,no pause. NextrootEssentialProbability:sourceviewed32–35,printed4.2/internal3.2remainexplicit,maximumtwoexperiments/twooutcomes;designonlytwo binarycomponentexperiments,atmosttwo pertrial,declareinterpretationandteacherconfirmation;six-faced-diesuggestionnotfollowed. SourceJSON/materials/manuscriptnotwrittesyet. Do not inferprintedidcorrectionorofficialallocation. Preserveverbatimoutcomesa–i,performedA/Bsinglechanceandpairedindepactionsseparatefromwrittenfinal. Pauseat<=10,noseparatelybilledAPI/nopush/publication;savecurrentreviewstatesandsmallboundary.
