# Independent review: General Science 2.4 — Acids, Bases and Salts

Status: COMPLETE — independent desk review of the original pilot snapshot before parent-agent corrections/rebuild, with classroom and external-resource limits stated below. 2026-11-12. Later fixes require a separate verification; this report does not certify a regenerated snapshot.

Reviewer: inherited Codex settings. An exact model identifier is not exposed to this reviewer, so none is guessed. No paid API calls, manuscript edits, generator edits or shared-code edits were made. The author’s internal_review.json, REPORT.md and other author evaluations were not read. Fresh findings were recorded in this file before the baseline was opened.

Verdict: the pilot’s named reaction products and numerical answers are correct under its stated assumptions. The source outcomes are substantially mapped to activities. It still needs assessment-instruction, teacher-reference and export corrections before a classroom-ready claim. The baseline has additional confirmed science/safety and missing-material problems, but its different scope, duration and resource dependencies prevent a general superiority or cost-saving inference.

## Scope and evidence

Read sources/gensci_2_4.json, visually inspected sources/gensci_2_4_source.png and an enlarged competency crop, read sources/science_references.json, blueprints/gensci_2_4.json, materials/gensci_2_4.json (all G1–G10), manuscripts/gensci_2_4.json (all ten lessons and assessment), and modules/gensci_2_4_data.js. Compared all phase activities, strategies, assessment checks, summary fields and final-assessment data between manuscript and exported module: all 171 correspondence checks passed. This confirms propagation, not educational quality.

Pilot output directory: outputs/v2/General_Science/SS2.4_Acids_Bases_and_Salts, prefix Codex_General_Science_Acids_Bases_and_Salts. Inspected seven DOCX bodies/relationships through ZIP/XML and extracted all seven PDF bodies with pdftotext: CBE_LessonSequence (43 PDF pages), CompactTeacherGuide (11), StudentMaterials (3), MaterialsTeacherKey (4), SummaryTable (2), FinalExplanation (6), FinalExplanation_TeacherKey (3).

Visual PDF sampling used pdftoppm and view_image because fitz was unavailable in both checked Python interpreters. Actually viewed pilot CBE pp1,2,39,40; Compact pp2,11; StudentMaterials pp1,3; MaterialsTeacherKey pp2,4; Summary p1; student assessment pp1,5; assessment key p1. Additional pages were rasterised but are not claimed as visually inspected. No full-page visual review of all 72 pilot PDF pages or independent Word pagination check is claimed. Sampled pages were legible; some table rows split across pages. Body-text inspection plus visual samples does not exclude an unsampled layout defect.

Then inspected baseline generators/data/gensci_2_4_data.js and its four DOCX/PDF types in data/outputs/v2/General_Science/SS2.4_Acids,_Bases_and_Salts and data/outputs/v2/PDF/General_Science/SS2.4_Acids,_Bases_and_Salts: standard guide (60 PDF pages), summary (5), assessment (7), key (4). Visual samples: baseline guide pp27,30,45; summary p3; assessment p1; key p2. No baseline compact guide or separate student-material/teacher-material file was present in that output set.

All distinct scientific assertions in the supplied pilot text were reviewed, including pH limitations, acid/base models, physiological roles, reaction products, hygroscopy/deliquescence/efflorescence, environmental and health claims. Uncertain/specialist and safety claims were cross-checked with primary organisations listed below. No experiments were performed. This is not a laboratory risk assessment or a classroom trial. Optional ARES media were not watched: DOCX relationships contain 27 distinct ares.local URLs in the pilot (12 direct resources, 15 searches), and 32 in the baseline (18 direct, 14 searches). Their presence is checked; playback, exact contents and school installation availability are unverified. Those limits prevent declaring every external resource clean.

Severity: High = safety/correctness or material omission likely to prevent a central task; Medium = meaningful assessment/teaching/export defect; Low = limited reference/provenance/usability issue. Classroom judgments and deliberately narrower design choices are separately identified.

## Source fidelity and outcome coverage

The crop visibly contains six outcomes a–f and the two inquiry questions. Outcome wording, competency wording, values and PCIs in the source JSON/manuscript match the crop, allowing normalised layout and punctuation. No exact source transcription correction is confirmed. An early suspected competency omission disappeared on enlargement; it is not a finding. The crop does not specify a lesson allocation; the pilot correctly labels its ten-period allocation a design decision.

| Outcome | Teaching evidence | Observable assessment | Limit |
|---|---|---|---|
| a: distinguish with universal indicator/pH chart | G2 practical/chart and L1 classification | L1 individual chart classification; final section 1 | Paper fallback/G10 alone does not show practical indicator use. |
| b: explain biological/chemical roles | G3 digestion, respiration, antacid and bleach; L2 sorting/explanation; L3 neutralisation | L2 two roles and rejection of “all bases bleach”; final section 2 | Biological mechanism is brief; see classroom judgments. |
| c: identify products | G4 HCl/NaOH; G5 hydrogen carbonate plus paper carbonate; G6 Mg/HCl | L3–5 product checks; final section 3 | Same named reactions recur in final; transfer is limited. |
| d: salt behaviour in air | G7 mass/state data; G8 comparison planning | L6 mass/classification; L7 control/limitation; final section 4 | Fallback is interpretation, explicitly not hands-on competence. |
| e: applications | G9 cards; L8 use–benefit–risk–action table | L8 application; final section 5 | Cards are broad; not all source suggested sectors covered. |
| f: promote proper use | G9 poster and L9 peer/teacher check | Reasoned action in G9/L10 and final section 5 | Classroom communication is assessed; actual community sensitisation is not observed. |

The pilot omits or narrows several suggested source experiences: the broad household sample list, road-use example, soil/air-pollution details, and actual community distribution. These are scope differences, not proof that a mandatory outcome is absent. Digital research is conditional and correctly marked unobserved if unavailable; it must not be reported as completed in that case.

## Pilot confirmed findings

### P1 — Medium: independent assessment contains paired/group instructions

Location: manuscripts/gensci_2_4.json, lessons[9].phases[0][2], [1][2], [4][2]; propagated to modules/gensci_2_4_data.js, LESSONS[9].framework[].sensemakingStrategy; CompactTeacherGuide PDF p11 and standard guide pp39–40.

Exact conflicting text: “Complete the assessment independently.” alongside “Individual prediction, then paired comparison: keep the initial claim visible.” and “Evidence-first group work: record working or observations before comparing explanations.” The last phase also says “Revise a shared model”. The student assessment instructions themselves correctly say “Work independently”.

Evidence: following the strategy column permits discussion immediately before and during the supposedly independent assessment. This makes administration and independent attainment evidence ambiguous, even though no key is printed in the student assessment.

Correction: give Lesson 10 its own independent-reading, independent-response and private-reflection strategies. Specify collection of assessment scripts before any peer discussion; postpone shared-model work to feedback. Dependency: regenerate module, standard and compact guides; student assessment need only be changed if administration instructions are consolidated there.

### P2 — Medium: pre-filled teacher summary does not provide the promised example observations/explanations

Location: manuscript lessons[0]–[8].summary; module SUMMARY_TABLE.lessons; SummaryTable PDF pp1–2 and lesson-end summary prompts in standard guide.

Exact text: heading/instructions promise “each row is pre-filled with expected student responses”, but nine observation cells say “The named card or class practical provides the evidence.” The phenomenon-explanation column includes “Begin the shared chart with a separate pH classification column.” and “Add a separate acid–metal branch; no flame test is needed.”

Evidence: these are references/task directions, not observations or explanations a teacher can use as expected answers. G7, for example, supplies +0.30 g/+1.20 g/−0.80 g evidence, yet the summary supplies none of it. This weakens the stated teacher-reference and formative-check function.

Correction: give lesson-specific illustrative evidence and a short causal answer, distinguish actual class results from examples, and accept no-change results where justified. E.g. L6: “Under G7’s water-only assumption, A gained 0.30 g while solid, B gained 1.20 g and formed solution, C lost 0.80 g”; explanation should connect water gain/loss to each classification. Dependency: manuscript, module, standard guide, summary export. The same instructions refer to a blank “student version”; no separate blank SummaryTable file is present in the seven-type package. Supply it, or direct learners to reproduce the table in notebooks.

### P3 — Medium: G9’s offline reference fallback is not a supplied, identifiable learner reference

Location: materials/gensci_2_4.json G9.student; StudentMaterials PDF pp2–3; MaterialsTeacherKey p4. Quote: “otherwise use the printed teacher reference”. Teacher text says “For health use WHO sodium-reduction evidence”. G3 teacher key p2 also promises “University of Bristol/CDC hypochlorite explanations”, but sources/science_references.json lists Bristol, not a CDC entry.

Evidence: G9 itself supplies short application claims, and the source JSON supplies URLs, but the output set contains no separately identified printed reference/extract for learners to consult and cite. Teacher preparation does not identify which pages to print or reproduce. G9’s existing paragraph can support basic discussion, but the promised supporting-source fallback still requires unrecorded teacher work. The CDC name cannot be followed through the supplied reference list.

Correction: provide a concise, attributed offline reading/reference card with title, publisher, date and exact URL; or explicitly identify G9’s own printed claims as the fallback and distinguish them from independent research. Add a real CDC reference or remove that attribution. Dependency: G9/G3 materials and both material exports; reference JSON and preparation list. WHO supports the stated general sodium/raised-blood-pressure relationship and necessary physiological roles; the finding is missing resource packaging, not a false health statement. [WHO sodium reduction](https://www.who.int/news-room/fact-sheets/detail/sodium-reduction).

### P4 — Low: exported authorship attribution conflicts with the OpenAI-only pilot label

Location: CBE_LessonSequence PDF p1 labels “OpenAI-only evaluation”; p2 attribution says “with lesson drafting and compilation assisted by AI (Claude, Anthropic).” The same attribution appears in SummaryTable p2, FinalExplanation p6, teacher key p3 and corresponding DOCX text.

Evidence: the package makes incompatible production claims. The inherited layout/framework may legitimately retain prior organisational credit, but that does not justify attributing this pilot’s drafting to another provider.

Correction: make attribution accurately distinguish inherited framework/template credit from current pilot drafting. Dependency: shared export attribution/template configuration, then regenerate affected files; no chemistry rewrite needed.

### P5 — Low: optional resource matching distracts from the independent final and adds an unrelated organic topic

Location: standard CBE_LessonSequence PDF pp39–40, Lesson 10 Predict/Observe phase labels; corresponding DOCX hyperlinks. Exact resource title: “Carboxylic acid naming”, marked “Related topic: not an exact match for this lesson.” It is inserted beside “Complete the assessment independently”, and is repeated in later final-lesson phases. The compact guide does not include this resource.

Evidence: naming carboxylic acids is not required to interpret G10 pH, salt mass changes or the named inorganic reactions. The matching warning is honest and the item is optional, so this is not a false claim of an exact content match. Nevertheless, an external lesson suggestion in the independent assessment can distract or create inconsistent resource access; repeated long recommendation blocks materially expand the standard guide (43 pages versus 11 compact pages). The local linked media itself was not watched or claimed broken.

Correction: suppress resource recommendations during the independent final; filter or curate known unrelated matches elsewhere. Keep necessary G10 access explicit. Dependency: resource-matching/export wrapper and standard guide regeneration; core chemistry manuscript need not change.

## Pilot evidence checks and teaching judgments (not additional error counts)

All registered and unregistered numerical contexts were checked:

| Context | Independent calculation/classification |
|---|---|
| G7 A | 5.30 − 5.00 = +0.30 g; water gain while solid supports hygroscopic behaviour. |
| G7 B | 6.20 − 5.00 = +1.20 g; water uptake with solution formation is deliquescence. |
| G7 C | 4.20 − 5.00 = −0.80 g; efflorescence under the stated hydrate/water-of-crystallisation model. |
| G10 first | 5.80 − 5.00 = +0.80 g; deliquescence. |
| G10 second | 4.50 − 5.00 = −0.50 g; efflorescence under the stated model. |
| pH examples | 3 acidic, 8 basic, approximately 7 neutral for the stated aqueous/near-room-temperature model. pH is not identity or safety. |
| G4 concentration/volume | 0.1 mol/L × 0.002 L = 0.0002 mol HCl; 0.002 L of 0.1 mol/L NaOH supplies equal moles for 1:1 neutralisation. The key appropriately limits the equal-volume inference. |
| G2 preparation | 1 g per 100 mL is 10 g/L, approximately 0.119 mol/L NaHCO3; a mildly basic illustrative pH around 8 is plausible. Vinegar 1:4 is read as one part vinegar plus four water; clarify the mixing instruction for teachers. |
| Lesson schedule | Nine × (4+16+10+4+6) plus (4+30+2+1+3) = 400 minutes; all lessons sum to 40. |

Reaction checks: HCl + NaOH → NaCl + H2O; CH3COOH + NaHCO3 → CH3COONa + H2O + CO2; 2HCl + CaCO3 → CaCl2 + H2O + CO2; Mg + 2HCl → MgCl2 + H2. Word products in teaching and teacher keys agree. G5 correctly distinguishes hydrogen carbonate from carbonate in teacher guidance. G6 correctly narrows the demonstration to HCl/Mg rather than adopting the full RSC multi-acid procedure. [RSC microscale metal–acid procedure](https://edu.rsc.org/experiments/microscale-reactions-of-metals-with-acids/509.article).

Salt definitions are sound at this level: deliquescence involves sufficient water uptake to form solution and is a hygroscopic behaviour; loss of crystallisation water from washing soda is an accepted efflorescence example. The mass-only inference is appropriately conditioned. [IUPAC efflorescence](https://goldbook.iupac.org/terms/view/E01909/pdf), [OxyChem calcium-chloride information](https://www.oxycalciumchloride.com/siteassets/documents/product-info-sheets/granulated_prodinfosheet.pdf).

Safety: no tasting/direct smelling; labelled small samples, goggles, trays; no bleach practical; teacher-only HCl/NaOH and Mg/HCl; no ignition, sealed gas vessel or concentrated preparation by learners; supplier SDS/local disposal checks; explicit evidence-card fallbacks. The no-mixed-cleaners statement is consistent with [CDC bleach guidance](https://www.cdc.gov/natural-disasters/safety/how-to-safely-clean-and-sanitize-with-bleach.html), and alkaline bleach’s oxidation role is distinguishable from alkalinity alone. [Bristol bleach explanation](https://www.chm.bris.ac.uk/motm/bleach/bleachh.htm). Live G4/G6/G8 remain dependent on teacher preparation, supplier information and local laboratory approval. Prepared salt samples require lead time; the pilot explicitly avoids promising visible change in 40 minutes.

Student-file key separation: FinalExplanation contains prompts/blank space/rubric and no exemplar key. StudentMaterials omits teacher-key paragraphs. G10 is bundled with teaching cards rather than printed on the assessment; administer with G10 alone if a closed-resource assessment is intended. Otherwise G3/G5’s teaching statements will be available. No teacher-key leakage in the designated student files was confirmed.

Assessment novelty is limited: G10 repeats G2’s pH 3/8/7 and the same three named reaction pairs already taught; only salt masses change. That is a valid consolidation/recall choice, but it does not strongly support Lesson 10’s “new evidence” or summary’s “unfamiliar data” beyond mass subtraction. A teacher should decide whether to add a different pH example/manufacturer chart or a new closely related reaction context. Do not label this exercise broad transfer testing without that qualification.

Classroom judgment remains needed: reading G3 plus explaining H+/OH−, carbonate naming and oxidation may need prior particle/formula teaching beyond the blueprint’s two listed prerequisites. “Stomach acid supports digestion” and respiration’s CO2-in-water sentence provide a minimal role explanation; adding enzyme-conditions and a short biological-context diagram would make outcome b more substantive. The G9 instruction to make a use–benefit–risk–action table for three applications exceeds the detail supplied for “some medicines contain salts”; teachers may need a named example and reading. The generic repeated inquiry about reaction versus water exchange is poorly fitted to L8 communication, but this is a planning-quality judgment. Salt hydration/dehydration can involve changes of solid chemical form; do not teach “water exchange” as proof that no chemical change can occur. Forty-minute practical/setup/cleanup and poster timing require a classroom trial; no universal infeasibility is asserted.

## Baseline comparison under the same rubric

Comparison scope is the original generator and data/outputs baseline, not the later revised_2026-10_full output tree. Baseline metadata says eight lessons × 40 = 320 minutes, but lesson-entry durations total 480 minutes: 40+80+80+40+40+80+40+80. The pilot totals 400. The baseline adds a twelve-sample practical, Lake Magadi/aluminium/physiology contexts, balanced equations, four real salts, five-sector research and a community project; the pilot deliberately narrows these to a fictional store case and smaller card/practical set. The source does not establish either allocation. Compare outcome evidence and required preparation, not eight versus ten labels or raw page/finding counts.

### B1 — High: incorrect hydrogen gas test plus contradictory ignition instructions

Location: generators/data/gensci_2_4_data.js L4 Observe (lines 248–249); baseline guide PDF p27; summary L4 p2; assessment key part 2 p1. Quote: “No flames. I will bring the glowing splint to each group.” Also: “observe the squeaky pop confirming hydrogen gas.”

Evidence: a lighted splint is the conventional pop test for hydrogen; a glowing splint is the oxygen-test distinction. An ember is still an ignition source, conflicting with the declared no-ignition approach and leaving risk controls unclear. [RSC gas-test matching](https://www.rsc.org/cpd/teachers/Content/FileRepository/CMP/00/007/144/teachingOrder.html).

Correction: remove ignition testing and infer the product from known reactants/other appropriate evidence, or replace with a fully specified teacher risk-assessed gas-test protocol. Do not merely substitute “lighted” while retaining the conflicting safety instructions. Dependency: L4 procedure, formative checks, summary, teacher key and all exports.

### B2 — Medium: damp litmus claimed to confirm CO2

Location: same L4 Observe, line 248, baseline guide p27. Quote: “collect the gas by holding damp blue litmus paper at the mouth of the flask … (confirming CO2…)”.

Evidence: holding paper is not gas collection; acidic gases/aerosols can redden litmus. This observation is not a specific CO2 identification. The standard school confirmation uses a suitable limewater test. [RSC gas-test reference](https://www.rsc.org/cpd/teachers/Content/FileRepository/CMP/00/007/144/teachingOrder.html).

Correction: say gas evolution/acidic response is an observation and identify predicted CO2 from named reaction chemistry, or specify an approved limewater procedure with apparatus and safety. Dependency: L4 procedure/checks and summary; assess observation versus inference consistently.

### B3 — High: central referenced cards, images and “real” numerical data are not supplied in the baseline set

Location: L1 overview/framework asks for two photographs and twelve laminated cards; L3 Observe line 187 asks for three ~200-word reading cards with diagrams; L6 Observe requests Research Brief cards; L8 Observe line 487 names “From Fertiliser Bag to Floating Weed: How Salts Are Choking Lake Victoria” and a seasonal nitrate table; L8 summary line 516 claims “real seasonal nitrate concentration data”. Baseline guide pp53–54/58 and summary p4 contain the latter claims; assessment part 4/key p2 depends on the data trend.

Evidence: the four baseline output types contain instructions/descriptions, not the promised standalone texts, diagram assets, photographs or nitrate values/source. The guide DOCX has zero word/media images. Filename search found no matching named cards/case-study assets in data. An ARES search link is not a supplied case-study source. A separate installation might hold resources, but its contents were not accessible/verified here. Therefore the “real” data claim cannot be substantiated, Q2’s trend cannot be recomputed, and the task cannot be delivered from this export set alone.

Correction: supply exact teacher/student assets, source citations and a complete numerical table; label invented data illustrative. Confirm any ARES resource by direct identifier and matching content. Dependency: lesson activities, assessment, keys, summary and offline package. Do not invent baseline nitrate results during correction.

### B4 — Medium: schedule is internally inconsistent and contains a provable within-phase arithmetic error

Location: UNIT.totalDuration line 26; lesson entries; L3 Observe line 187: “Reading Stations (20 min)” with three cards “8 minutes each” and “a 1-minute transition bell”.

Evidence: entry durations total 480, not 320 minutes. Three readings require 24 minutes; two 1-minute transitions require 26, exceeding the labelled 20 before the demonstration. This is a numerical inconsistency independent of classroom pace.

Correction: set the intended total honestly and rebuild the lesson timetable; explicitly split double periods and allocate setup/cleanup/assessment. Dependency: metadata, overview, teacher-facing timing and comparison claims.

### B5 — Medium: universal base definition misrepresents the carbonate examples

Location: L2 knowledge line 109, Explain line 134, summary lines 158/609; guide p11 and summary pp1–2. Quote: “bases as substances that release OH⁻ ions in solution”; explanation says trona “releases hydroxide ions”.

Evidence/recomputation: trona/carbonate do not contain hydroxide to dissociate. Carbonate raises OH− through reaction with water: CO3²− + H2O ⇌ HCO3− + OH−. A hydroxide-only dissociation definition excludes bases such as carbonate and ammonia used in introductory teaching. This is not cured by correctly associating higher aqueous pH with greater OH− activity.

Correction: limit the dissociation description to soluble hydroxides; introduce the broader proton-accepting/base-with-water model as appropriate, showing the carbonate equilibrium if teaching mechanism. Dependency: L2 models, particle drawings, summaries, final-key parts 1/5; avoid diagrams with unbalanced charges or treating a solution as only H+/OH−. [RSC ammonia/water and acid-base demonstration notes](https://edu.rsc.org/experiments/indicators-and-dry-ice-demonstration/703.article).

### B6 — Medium: hygroscopy and deliquescence treated as mutually exclusive classes

Location: L5 Explain and summary lines 338/629; baseline summary p3. Quote: “A hygroscopic salt absorbs moisture from the air without dissolving. A deliquescent salt … dissolves completely.”

Evidence: hygroscopic describes moisture uptake; deliquescence is the dissolution outcome of sufficient uptake. A deliquescent solid is also hygroscopic. Calcium chloride’s manufacturer explicitly describes both behaviours together. Complete disappearance of every remaining crystal is not needed to observe the onset of deliquescence. [OxyChem calcium chloride](https://www.oxycalciumchloride.com/siteassets/documents/product-info-sheets/granulated_prodinfosheet.pdf), [IUPAC deliquescence](https://goldbook.iupac.org/terms/view/D01582/pdf).

Correction: teach the nested relation and distinguish observed state from permanent exclusive category; condition results on temperature/humidity. Dependency: L5 definitions/checks, drawings, summary and assessment key part 3. Do not mandate a pre-written class observation when actual samples show no change.

### B7 — Medium: fertiliser ion identities conflated

Location: L6 summary lines 398/637, baseline guide p44/45, summary p3; final key part 4 p2. Quote: “CAN and DAP release ammonium and nitrate ions”. L8 Q4 marking also says “nitrate/phosphate ions from CAN”.

Evidence: DAP is (NH4)2HPO4: ammonium and hydrogen phosphate, not nitrate; CAN does not supply phosphate just because DAP is discussed alongside it. The broader statement that both supply plant nutrients is sound. [FAO/JECFA DAP specification](https://www.fao.org/fileadmin/user_upload/jecfa_additives/docs/Monograph1/Additive-150-m1-corr.pdf).

Correction: distinguish each fertiliser’s supplied ions; if discussing later nitrification, name the soil transformation rather than claiming nitrate is directly released from DAP. Dependency: application and runoff model, summary and marking criteria. Avoid marking a chemically accurate distinction wrong.

### B8 — Medium: ordinary ice called an ionic lattice

Location: L6 summary lines 398/637; guide p45; summary p3. Quote: “NaCl gritting … lowers the freezing point of water by disrupting the ionic lattice of ice”.

Evidence: ordinary ice is a molecular hydrogen-bonded solid, not an ionic solid. Salt’s freezing-point effect must not be explained through a nonexistent ionic ice lattice. [Primary neutron-scattering research on hydrogen bonding in ice](https://www.nature.com/articles/365327a0).

Correction: use a suitable dissolution/freezing-point description and reserve ionic-lattice language for crystalline salts. Dependency: L6 summary and exports; road use remains an optional example.

### B9 — Medium: Lake Naivasha misclassified

Location: L8 DQB formative assessment, line 504; guide p56. Quote: “Why does trona form at Lake Magadi but not at Lake Naivasha, even though both are soda lakes?” is presented as a high-quality chemistry question.

Evidence: Lake Naivasha is a freshwater lake, so the premise is false. [Official Ramsar site information sheet](https://rsis.ramsar.org/RISapp/files/RISrep/KE724RISformer_161121.pdf).

Correction: make the contrast itself the question, or use an appropriately sourced alkaline-lake comparison. Dependency: L8 example and export only.

### B10 — Medium: acid-food safety is overgeneralised in the core question/key

Location: L3 Predict teacher moves; final assessment part 2 and key pp1–2. Quote: lemon juice “never hurt your mouth”; question asks why the same juice “does not damage your body”.

Evidence: ordinary dietary use differs from corrosion of bare metal, but acidic citrus exposure can erode enamel. Stomach mucus does not protect the mouth or justify an unconditional harmlessness claim. [American Dental Association dental erosion](https://www.ada.org/resources/ada-library/oral-health-topics/dental-erosion).

Correction: explain that effect depends on tissue, concentration, exposure and biological protections; remove “never”/“does not damage” and avoid tasting demonstrations or individual health prescriptions. Dependency: anchoring question, L3 discussion and final assessment/key. This correction does not imply citrus foods are generally forbidden or that classroom learners need clinical advice.

## Comparison limits, unresolved questions and disposition

The baseline has strong descriptive teacher prompts, local contexts and a more detailed intended research/community sequence, but many required assets are described rather than delivered. The pilot provides G1–G10 and labelled fallbacks, yet omits or reduces several baseline contexts and does not show all source competencies in every setting. Neither fewer findings nor shorter text establishes educational superiority. No cost-saving conclusion follows from this review.

Baseline numeric tasks: the aluminium equation 2Al + 6HCl → 2AlCl3 + 3H2 balances correctly. HCl/NaOH, H2SO4/CaCO3 and Mg/HCl product identities are correct; calcium sulfate coating can limit the marble/sulfuric-acid demonstration, so a teacher should rehearse it and avoid guaranteeing vigorous sustained reaction. No numerical nitrate table was available to solve. A five-mark rubric and four 4-mark classroom questions are separate assessment structures, not an arithmetic total conflict by themselves. The exported student assessment has five extended sections while L8 describes a different four-question paper: reconcile which instrument is administered and how much time it receives. That alignment concern is separate from the confirmed science errors above.

Baseline safety/preparation additionally needs school review: unspecified “safe” concentrations in L2; unspecific antacid tablet/HCl quantity in L3; blanket drain-disposal instruction in L3 despite multiple possible solutions; prompts about smelling observations in L4; no general practical fallback, and absent resource cards. These are unresolved operational dependencies, not invented evidence that an accident occurred. The baseline’s universal 0–14 pH endpoints should be qualified as the common dilute-aqueous teaching range, and its simplified limescale explanation should include precipitation on heating rather than attributing all CaCO3 scale only to evaporation. [USGS carbonate-hardness chemistry](https://pubs.usgs.gov/of/1950/0069/report.pdf). The exact hydration/weathering behaviour claimed for Magadi trona and the tea-seedling wood-ash anecdote remain unsourced contextual claims; no empirical validation of those anecdotes is claimed. They should be labelled scenarios or independently documented before public factual use.

An early baseline checkpoint called Mg(OH)2 a categorical salt error. That is withdrawn as a standalone finding: broad ionic-compound nomenclature and school acid/base/salt classifications can differ. The useful correction is to state the adopted classroom classification consistently, especially because L6 teacher guidance itself distinguishes Mg(OH)2 base from MgCl2 reaction salt. It is not counted as an additional confirmed error.

Release disposition: correct P1–P5 and settle classroom assessment administration, prerequisites, practical approval and offline materials. Recheck the regenerated documents. For the baseline, address B1/B3 before trying the central practical/data sequence; fix the linked science/marking misconceptions and schedule before reuse. Human chemistry/laboratory and Grade 10 classroom judgment remains required. Review completion means the specified desk review has been delivered, not that either package is certified safe, comprehensive or classroom-tested.

## Independent source access notes

Primary references were accessed on 2026-11-12. WHO/FAO/Bristol pages were retrieved directly. RSC practical/gas-test pages and some IUPAC pages blocked direct opening (405/403 or bot check); relevant indexed primary-source text/PDF retrieval was used and this limitation is retained. IUPAC’s washing-soda efflorescence example, RSC’s small-quantity/goggles/HCl–Mg procedure, OxyChem’s moisture/deliquescence description, CDC’s no-cleaner-mixing rule and WHO’s general sodium statements support the checks above; they do not replace a school-specific practical assessment. The reference list supplied by the author was itself read and was not treated as proof without checking.

<details>
<summary>Progress checkpoints preserved for interruption recovery</summary>

# Independent review: General Science 2.4

Status: IN PROGRESS. Fresh review begun after reading REVIEW_BRIEF.md. Author internal_review.json and REPORT.md have not been read.

Reviewer model: inherited Codex settings; exact model identifier is not exposed here and is not guessed.

Scope: source fidelity, science, numeric tasks, supplied materials, pedagogy, safety and rendered documents; baseline comparison follows initial findings.

## Checkpoint 1: initial review evidence

Read source JSON and visually inspected source crop; read blueprint, material cards G1–G10, manuscript including all ten lessons and five assessment sections, and module opening/schema. Seven PDF types extracted with Poppler and seven DOCX bodies extracted from XML. No author evaluation read.

Confirmed issue pending full report: Lesson 10 pairs an explicit independent assessment with inherited paired/group/shared-model strategy instructions. Source competency transcription also appears incomplete (checking enlarged source). Numeric mass changes independently recomputed: G7 +0.30 g, +1.20 g, −0.80 g; G10 +0.80 g, −0.50 g; keys match. Named chemical products match standard equations.

Sources checked independently so far: WHO sodium reduction; RSC acid–metal microscale experiment through search retrieval (direct open 405); IUPAC efflorescence through current PDF/search (direct term page 403); Bristol bleach article. Printed-reference readiness and full rendered layout remain under review.

## Checkpoint 2: fresh findings fixed before baseline access

Enlarged source competencies match the transcription; the suspected omission was a low-resolution reading error, not a source defect. Six outcomes, both inquiry questions, competencies, values and PCIs were checked against the crop; no transcription correction confirmed.

Confirmed fresh findings to document fully: (1) Lesson 10 independent/group contradiction; (2) SummaryTable claims expected responses but supplies generic placeholders for observations and task directions for explanations; (3) G9 offline fallback names a printed teacher reference not actually included as a learner source; (4) generated standard/assessment/summary attribution says AI (Claude, Anthropic), conflicting with pilot OpenAI-only labelling. Scientific equations and five mass calculations checked so far are sound within stated assumptions. A separate concern is assessment novelty: all pH values and all three named reactions repeat teaching examples; only salt masses change. This limits the explicit “fresh/new evidence” claim and transfer evidence, rather than invalidating every recall assessment.

PDF visual inspection completed for at least one page of each of seven types with pdftoppm and view_image (fitz absent); standard guide pp39–40 confirms unrelated optional Carboxylic acid naming resource repeated in independent assessment. Full PDF and DOCX text checking remains ongoing. Baseline has not yet been opened at this checkpoint.

## Checkpoint 3: baseline comparison evidence

Baseline inspected only after fresh findings were recorded. Generator is 8 entries labelled “8 × 40 = 320 minutes”; actual entry durations are 40,80,80,40,40,80,40,80 = 480 minutes (12 forty-minute periods). Pilot is 10 × 40 = 400. Therefore eight versus ten entries cannot be used as a time comparison. Baseline contains additional real-world contexts, balanced equations, 12-sample practical, physiology, five-sector research and community project demands; pilot narrows examples and replaces several activities with optional safe evidence cards.

Baseline confirmed science/safety issues: hydrogen uses a glowing splint and contradicts no-ignition instruction; litmus colour alone claimed to confirm CO2; DAP and CAN ion identities conflated; ice called an ionic lattice; Mg(OH)2 called a salt; universal base definition “releases OH−” wrong for carbonate examples; hygroscopy defined to exclude dissolution. Claimed real seasonal nitrate data/card is referenced but neither numerical table nor a source is supplied in baseline exports read so far. Baseline PDF/DOCX four types extracted; visual sampling and exact page mapping underway.

</details>
