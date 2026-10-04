# Teacher / author review list — lesson content issues not auto-fixed

Updated 2026-10-04 after the verification pass. Cross-reference and dataset contradictions were fixed automatically (audit trail: `logs/lesson_repairs/<module>.cc.json`). Every item below was checked against the lesson text by a Claude Code agent and judged real:
- **science**: lessons explain an idea differently, or a lesson contains a science/maths error.
- **structural**: duplicated lessons, wrong order, a lesson relying on an activity no lesson contains, or a dataset that differs throughout (fix = rewrite or regenerate the lesson).

**207 items across 83 sub-strands**, most items first.

## gensci_2_2 — General Science: Chemical Families (6)
- **[structural]** 0 lesson order Group 1/Group 2 and sodium demo references — Group 2 is taught twice (L3, L6) and Group 1 comes after Group 2 although L3 says alkali metals were Lesson 2. Fixed only the sodium-in-water demo references (L6 'Lesson 3', L7 'Lesson 2' -> Lesson 4); the L3 ordering issue needs restructuring.
- **[structural]** 1 halogens never taught — Real: L3, L5, L7, L8 refer to a halogen lesson (chlorine bleaching hibiscus, iodine) that does not exist in the sequence; needs a design decision.
- **[science]** 3 sodium lamp mechanism and sodium flame colour — Real science error in L5 ('loses its single outer electron to produce the orange glow') vs L4's correct excitation account - not edited. The sodium 'violet flame' in L8 contradicted L4's observation (potassium lilac, sodium none) and was aligned as a dataset fix.
- **[science]** 4 Group 2 vs Group 1 reactivity explanation; Mg with cold water — Explanations are complementary; faint film vs 'no noticeable reaction' for Mg in cold water is a minor descriptive difference.
- **[science]** 6 calcium in CAN fertiliser — Minor: L3 says Ca and Mg are in CAN; CAN is calcium ammonium nitrate (Mg only in some blends).
- **[science]** 9 iron rusting equation — Both are valid representations (anhydrous vs hydrated oxide); not a real contradiction.

## gensci_3_2 — General Science: Linear Motion (6)
- **[structural]** Mkokoteni acceleration 2 (L2), 2.5 (L3), 9.8/10 (L4, L5, L7), ~3 slope component (L8) — Real: each lesson builds its calculations on a different acceleration and L4/L5/L7 model the cart as in free fall, which L8 rejects. Changing values would cascade through every worked answer; needs a decision on one cart acceleration. Only removed L3's false claim that 2.5 came from the previous lesson.
- **[structural]** Cart speed/distance after 8 s: 16 m/s (L2) vs 20 m/s, 80 m (L3) vs 24 m/s (L8) — Follows from the different accelerations above; each lesson's arithmetic is internally correct.
- **[science]** Definition of acceleration (L1 vs L2) — L2's 'constant change in velocity' is loose wording, not a real contradiction with L1.
- **[science]** Whether the cart on the slope accelerates at g — Real contradiction: L4/L5/L7 use g for the rolling cart, L8 says only a slope component (~3 m/s^2) acts. Same root as the structural acceleration issue.
- **[science]** Three vs four equations of linear motion — L5/L6 list the three used for free fall; not strictly contradictory but inconsistent count.
- **[structural]** Drop heights: exactly 2 m (L4) vs 0.5-2.0 m class table (L5); g ~9.8 vs ~10 — L5 relies on a multi-height Lesson 4 table L4 never produced; g 9.8 vs 'roughly 10' is a rounding difference (false positive part).

## math_1_1 — Mathematics: Real Numbers (6)
- **[structural]** Source of the √2/2 ≈ 0.7071 slice (arc vs radius fraction vs chord vs fraction of pizza) — Pizza B's irrational slice is defined loosely and differently across lessons; needs a single definition, not a word swap
- **[structural]** Cumulative model name / DQB column labels; L3 booklet 'begun in Lesson 1' — Artefact naming drifts lesson to lesson (map, booklet, model); not a single-word fix
- **[structural]** L3 cites rational/irrational and number line as already taught (Lesson 2 / last lesson), but L4 teaches them — L3 and L4 appear written in swapped order; references are consistent with that other order, so needs a re-sequencing decision
- **[structural]** Reciprocals taught fully in L3 then 'introduced' as new in L5 — Real duplication of content between L3 and L5
- **[science]** √4 described as having an irrational reciprocal in L6 — Real error in L6 (√4 = 2, reciprocal 1/2 is rational)
- **[science]** Whether 1/3 is 'messy' (L1) or a 'neat' rational slice (L7) — Mild framing tension; both treat 1/3 as rational

## bio_2_2 — Biology: Plant Transport (5)
- **[science]** Direction of phloem transport — L2 simplified 'downward' first model refined to bidirectional/mainly downward in L3/L5; progressive refinement, not a real contradiction.
- **[science]** Xylem energy / driver — Passive xylem (L3) and transpiration pull (L6-7) are compatible; the osmosis-from-Lesson-2 part was a cross-reference, fixed in L3.
- **[science]** Position of xylem and phloem in stem — L3 gives no position; L5 detail (monocot vs dicot) is additive; not a real contradiction.
- **[science]** Cause of irreversible wilting — Different contributing causes across lessons; complementary rather than contradictory.
- **[science]** Stomata in shade/heat — Mild wording differences on stomatal opening; not a real contradiction.

## coremath_3_1 — Core Mathematics: Statistics I (5)
- **[structural]** 40-price maize dataset changes between lessons — Dataset differs throughout (earlier unresolved conflict 1/2 in logs/lesson_repairs/coremath_3_1.json: each lesson 4-7 built on a different 40-price dataset; needs dataset rework).
- **[structural]** L4 frequency table mean 105.10 vs L1/L2 list and L8 Rift Valley spike — L4 arithmetic is internally correct (4204/40=105.1); mismatch is the differing dataset (earlier unresolved conflict 1/2 in logs/lesson_repairs/coremath_3_1.json: each lesson 4-7 built on a different 40-price dataset; needs dataset rework).
- **[structural]** Distribution shape / cause of mean>median (L4, L5, L8) — Follows from different datasets in L4/L5/L8 (earlier unresolved conflict 1/2 in logs/lesson_repairs/coremath_3_1.json: each lesson 4-7 built on a different 40-price dataset; needs dataset rework).
- **[structural]** Modal class / mode (L4 98, L5 100-109, L6 50-59, L7 70-74) — Each from a different dataset (earlier unresolved conflict 1/2 in logs/lesson_repairs/coremath_3_1.json: each lesson 4-7 built on a different 40-price dataset; needs dataset rework).
- **[structural]** Mean/median L7 (72.7/73.2) vs L8 (105.10/103) — Different datasets (earlier unresolved conflict 1/2 in logs/lesson_repairs/coremath_3_1.json: each lesson 4-7 built on a different 40-price dataset; needs dataset rework).

## g11_bio_2_2 — Biology: Growth and Development in Plants (5)
- **[structural]** hormones question loops L6->L7->L8->L9 — Real sequencing loop: L7 and L9 both teach hormones; L8 re-raises the hormone question. Not edited.
- **[structural]** measuring growth in L6 and again L8 — L6 and L8 both measure growth and plot curves; duplicate content.
- **[structural]** maize/bean growth data L6 vs L8 — L6's figures are an 'e.g.' of student data, L8's a back-up table; follows from the L6/L8 duplication. Not edited.
- **[science]** definition of growth (L2 vs L10) — L10 is a shorter paraphrase; not a real contradiction.
- **[science]** hormone list with/without ethylene — L10 lists four hormones, L7/L9 add ethylene; incomplete list, not a contradiction.

## phys_3_3 — Physics: Introduction to Electronics (5)
- **[science]** Mechanism by which heat reduces output — Real contradiction: L3 (mobility/lattice scattering lowering voltage), L5 (thermal pairs lowering Voc), L6 (mobility/current), L7 (recombination) give incompatible primary mechanisms; needs content review.
- **[science]** Silicon conduction band occupancy at room temperature — 'Mostly empty with a few electrons' (L2) and 'partially filled, not empty' (L3) are compatible; not a real contradiction.
- **[science]** Role of band gap / light vs heat / darkness conduction — Partly real: L2 ties conduction to light, L3 to thermal promotion, L7 says the gap blocks flow in darkness while L1 shows dim conduction without light emphasis; needs review.
- **[structural]** Turkana case study and superconductors in L6 — L6 uses a separate Turkana case study and groups superconductors with semiconductors; case-study design choice, not edited.
- **[structural]** Lesson where p-n junction explains temperature effect — L3 already offers a full temperature mechanism before L4/L5 defer it; sequencing issue, not edited.

## bio_2_3 — Biology: Plant Gaseous Exchange and Respiration (4)
- **[science]** Identity of gas in sukuma wiki bubbles (L4,8,9,11,12) — Real contradiction: lessons attribute the bubbles variously to O2 (photosynthesis), CO2 (respiration) or both; needs an author decision, not a text patch.
- **[science]** Ethanol vs lactic acid in anaerobic plant cells (L4,5,9,12) — Real but minor: L5 says waterlogged roots make lactic acid; L4/L12 say ethanol+CO2 (ethanol is the textbook answer for plants).
- **[structural]** Project investigation tracks (L9 anaerobic vs L10 plant gas exchange vs L11 anaerobic) — Real: L10 executes a different project from the one L9 plans and L11 presents; needs regeneration of L10, not a patch.
- **[science]** Warm water: stomatal opening vs enzyme rates (L2,3 vs L4-12) — Partly real: early lessons frame temperature via stomata, later via enzymes; compatible but not reconciled.

## chem_1_1 — Chemistry: Introduction to Chemistry (4)
- **[structural]** Which lesson covers states of matter / physical vs chemical change / properties — Fixed L4's wrong 'Lesson 3' pointer to Lesson 1 (PhET). Remaining: L6/L9/L10 recaps claim physical vs chemical change and properties of matter were taught, but only L1 touches them. Real gap, left for review.
- **[structural]** Concept map vs model format across lessons — Real but minor: L1 builds a before/after drawing, later lessons call it a concept map, L5 a class model. Left.
- **[structural]** Drug/prescription/dosage introduced in L4 and again in L7; DQB statements at start of unit — L4 exit task and L7 overlap (duplication, left). L8 'from Lesson 7' is accurate. Fixed L4's claim that DQB statements were posted at the start of the unit.
- **[science]** L5: nuclear energy attributed to Olkaria geothermal; fission called a chemical change like chapati — Within-L5 science errors (Olkaria is geothermal; fission is nuclear, not chemical change); not a cross-lesson dataset fix.

## chem_2_1 — Chemistry: Introduction to Salts (4)
- **[science]** CAN identity: NH4NO3 vs Ca(NO3)2/NH4NO3 mixture; CaCl2 hygroscopic link in L4/L6 — Real inconsistency in how CAN is described (and real CAN is NH4NO3 + CaCO3); pervasive simplification, needs a content decision
- **[science]** How CAN is made (neutralisation vs acid reactions vs CaCl2 from carbonate) — Mostly loose wording; L4 linking CAN clumping to CaCl2 is a real conceptual slip
- **[science]** Efflorescence product of washing soda: anhydrous (L6, L7) vs monohydrate (L8) — Real contradiction; monohydrate (L8) is chemically more accurate
- **[science]** Hygroscopic vs deliquescent definitions L6 vs L8 — Mild real contradiction: L6 lumps CaCl2 as deliquescent/hygroscopic, L8 separates them and hedges CAN

## coremath_1_3 — Core Mathematics: Quadratic Expressions and Equations (4)
- **[structural]** shot put height model differs across lessons — L1 uses h=-0.1x^2+1.2x+1.5 (lands ~12 m), L2 other data, L3/5/7/8 use -x^2+6x, L6 (-x+6)(x-1), L5 predict x^2+5x+6. L1 and L8 (both authoritative) disagree, so needs a module-level decision; not edited.
- **[structural]** max height 9 m for -x^2+6x / L6 roots 1 and 6 — Consequence of the simplified dataset; unrealistic but internally correct arithmetic. Part of the dataset decision above.
- **[structural]** factorisation introduced in both L3 and L5; L6 expansion placed after factorisation — Real duplication/out-of-order sequence (L6 still says factorising comes in L7). Not edited.
- **[science]** L4 difference of squares vs shot put eq; L7 formula/roots — L4 only uses the shot-put zeros as an analogy before x^2-16; not a real contradiction.

## essmath_2_1 — Essential Mathematics: Similarity and Enlargement (4)
- **[structural]** 0 water fill counts 4/9 vs 8/27 — Real and serious: the anchoring phenomenon (L1, L8) has 4 and 9 small cups filling the k=2 and k=3 cups, which is physically wrong for volume (should be 8 and 27); L5-L7 and FE teach k^3 correctly; L8 rationalises 9 as cross-section area. Needs author redesign of the phenomenon, not a text patch.
- **[structural]** 1 driving question 'eight times' vs observed 4 fills — Same root cause as 0: DQ (8x) is correct maths, the L1 observation (4 fills) is not.
- **[structural]** 2 what 9x refers to (label vs fills vs cross-section) — Same root cause as 0; L4 label/area 9x is correct, the 9 water fills is not.
- **[science]** 3 doubling gives 4x surface vs cross-section area — Both 4x statements are correct for area; contradiction only arises from the fill-count framing in 0.

## essmath_3_1 — Essential Mathematics: Statistics 1 (4)
- **[structural]** Median of the five-day ugali data (57 in phenomenon/L7/L8/FE vs 59 in L3, 58 in L6) — Authoritative summary (mean 58, mode 60, median 57 over 5 days) is mathematically impossible: sum 290 with two 60s forces the two lowest values to total 113 while both are below 57. The dataset L3 and FE Part 3 use (54,60,57,60,59) gives median 59. Fixed only L3's internal 58->59; L7/L8/FE 'median 57' needs a human decision on the dataset.
- **[structural]** Total orders 150 (L5, ugali 37%) vs 120 (ugali 47%) — Real contradiction; L5's whole graphing activity (5 frequencies, pie angles e.g. 134 deg, 37%, '150 portions') is built on the 150 table; fixing needs new invented frequencies for 4 meals, so left for regeneration.
- **[structural]** Mean/mode/median taught in L3 and re-taught as new in L6/L7 — Real duplication: L3 covers all three, L6 (mean/mode) and L7 (median) present them as new.
- **[structural]** L3 cites a Lesson 2 frequency distribution table; L2 built none (L4 does) — Ordering problem: frequency tables are built in L4, after L3; not fixable by renumbering.

## gensci_1_7 — General Science: Microorganisms (4)
- **[science]** Patch organisms: fungal moulds (L1,2,8) vs fungi and bacteria (L5) — Mild: L5 adds bacteria as co-colonisers; not strictly contradictory but blurs the 'moulds' conclusion.
- **[science]** Drying/salting said to reduce temperature (L7) — Real error within L7 (drying and salting reduce water availability, not temperature); needs author fix.
- **[science]** Transmission route categories (L3,4,5) — Different groupings of the same routes; not a real contradiction.
- **[science]** Patch fungi in 'same broad group' as yoghurt Lactobacillus (L2 vs L6) — Real but framed loosely: 'microorganisms' as the broad group is defensible; the prompt is posed as a true/false discussion.

## gensci_3_1 — General Science: Turning Effect of Force (4)
- **[science]** location of the jembe pivot — All lessons and the FE treat the blade/soil contact as pivot P; L5/FE friction 0.1 m from P is a modelling detail. Not a real contradiction.
- **[science]** two-handed grip as couple (L4) vs single force about pivot — Real conceptual tension: L4 calls the grip a pure couple while other lessons use a pivot model. Needs content review.
- **[science]** couple definition wording / tau vs M — Notation/wording inconsistency only; not a factual contradiction.
- **[science]** L2 200 g at 30 cm balanced by 100 g (needs 60 cm) — Real internal error in L2 (balance point off the half-metre rule), not a cross-lesson conflict; not edited.

## gensci_3_4 — General Science: Magnetism and Electromagnetic Induction (4)
- **[science]** Induction-method magnet called permanent yet soft iron easily demagnetised (L1,2) — Minor real imprecision within L1; L2 does not contradict it.
- **[science]** Stopping the generator = demagnetisation (L2) vs no relative motion (L4,5,6,8) — Real and serious: L2's explanation is physically wrong and contradicts L4-L8; needs author rewrite of L2 phenomenon link.
- **[science]** Bell make-and-break = generator switching mechanism (L7,8) — Real: L7/L8 claim the bell's switching is the generator mechanism, contradicting L4-L6 induction explanation.
- **[science]** Field strength 'maximises force on conductor' (L3) vs rate of flux cutting (L4,5) — Minor framing difference; not a hard contradiction.

## phys_1_4 — Physics: Energy, Work, Power and Machines (4)
- **[science]** Whether the nut moved / work done and source of heat (L3 vs L4) — Real tension: L3 says d = 0 so W = 0 yet attributes heat to friction work; L4 invokes microscopic slip. Not edited.
- **[structural]** Spanner MA / force figures (L3, L6, L7, L8) — Each lesson uses its own lever numbers (L3 handle 0.15 vs 0.45 m, L6 'about 4 times longer' with 50 N -> 200 N, L7 MA 4 vs 2, L8 'e.g. MA = 3.5'). Aligning would cascade through dependent calculations in L6 and L7.
- **[science]** Spanner energy as gravitational PE (L1-2) vs lever work (L3-8) — Real conceptual mismatch: L1 bridges the spanner arm to PE from its raised position; later lessons model it as applied-force lever work from chemical energy.
- **[science]** Power vs strength; Kipchoge 1,000 W — L8 equates stronger with more powerful; 1,000 W claim is high. Minor science quality issues, not edited.

## phys_4_1 — Physics: Greenhouse Effect and Climate Change (4)
- **[structural]** when the ozone layer was taught (L5 vs L6) — L3 briefly distinguishes ozone (UV) from GHGs while correcting a misconception, L5 assumes ozone was covered, L6 introduces it as new. Sequencing overlap; not edited. Fixed only L5's IR-trapping lesson pointers.
- **[science]** greenhouse gas lists differ — Different subsets listed; not a contradiction.
- **[science]** moisture source for long rains — Complementary emphases (Lake Victoria/Indian Ocean vs ITCZ); not contradictory.
- **[science]** L6 'UV rising' framing vs UV-B data declining after late 1990s — Possibly a real internal tension in L6's framing; needs content review.

## bio_1_2 — Biology: Chemicals of Life (3)
- **[science]** Number and identity of the six chemicals of life — Real: L1 lists vitamins and mineral salts separately with no nucleic acids; L2/L6/FE list nucleic acids and combine vitamins/minerals. Classification choice, left for review.
- **[structural]** Which lesson the food tests (iodine, Biuret) were performed in — Real and serious: no lesson performs iodine, Biuret or DCPIP tests (L3 does lipid tests only, L4 is structure/modelling), yet L5, L6, L1 reflection and FE Part 2/4 cite their results 'from Lesson 4'. Needs a content decision (add tests or rewrite L5/L6/FE evidence); only the clear-cut L5 storyline and L6 references were repointed.
- **[science]** Marasmus definition vs missing-chemical framing — Not a real contradiction: marasmus as overall energy/protein deficiency is correct; framing is just loose.

## bio_1_3 — Biology: Cell Biology (3)
- **[structural]** structure of Lesson 4 cumulative model — L4 builds two 2D diagrams; L5 describes it as a 3-column chart. Real mismatch but needs rework of L5's model activity.
- **[science]** animal cell vacuoles and centrioles — Not a real contradiction: small vacuoles and centrioles are both correct for animal cells; just different lists.
- **[science]** universal features 3 vs 4 — Mild real inconsistency (some lessons add ribosomes); both are defensible.

## bio_3_1 — Biology: Animal Nutrition (3)
- **[science]** Mosquito bypasses all digestion (L7) vs bypasses mechanical only (L9) — Real but mild contradiction; L9 is the more accurate version
- **[science]** Function of mosquito saliva (anticoagulant vs enzymes) — Mild; L8 implies a digestive role for saliva that L3 does not; not a hard contradiction
- **[structural]** L4 title mentions flamingo, content covers fish eagle/vulture/hornbill — Title/content mismatch; flamingo is covered in L5

## bio_3_3 — Biology: Animal Gaseous Exchange and Respiration (3)
- **[science]** Cause of burning sensation (L8 fuel switch vs lactic acid) — Real contradiction: L8 attributes burning/extra O2 demand to a carbohydrate-to-fat switch, contrary to L7/L10-12 lactic acid explanation; needs content review.
- **[science]** L9 warmth/burning vs L10 lactic acid — Mostly complementary (L9 is about heat/warmth); minor overlap, not a clear contradiction.
- **[science]** Stimulus for faster breathing (L6 vs L12) — Complementary levels of explanation (cell demand vs CO2/O2 chemoreception); not a real contradiction.

## chem_1_3 — Chemistry: The Periodic Table (3)
- **[structural]** Group numbering Roman (I, VII, VIII/0) in L3 vs Arabic (1, 17, 18) in L4+ — Real notation inconsistency across lessons, never reconciled; needs a deliberate choice, not a fact edit.
- **[science]** H placed in Group I (L3) vs alkali metals Li/Na/K (L4) — Not a real contradiction: H sits in the Group I column but is not an alkali metal; could be stated explicitly.
- **[structural]** L2 says Lesson 1 sketch arranged a subset of 10 cards; L1 sorts 20 — Minor mismatch built into L2's revision activity (re-sort their 10 cards); left.

## chem_1_4 — Chemistry: Chemical Bonding (3)
- **[structural]** Whether graphite conductivity data was collected (L8 vs L9) — L9 is written around four substances and hedges on whether graphite was tested, while L8 tests graphite; would need rewriting L9's activity, not a small edit.
- **[science]** Graphite delocalised electron location — Real minor inaccuracy: L9/L11/L13 say electrons delocalised 'between layers'; correct model (L4/L6) is within/along each layer.
- **[science]** Na+ empty outer shell wording — Wording ambiguity in L3 dot-and-cross instructions; not a real contradiction.

## chem_1_5 — Chemistry: Periodicity (3)
- **[science]** Period 3 first IE trend and Al dip (L5,6,7) — Real: L5/L6 data show Al IE < Mg, but L6/L7 explain reactivity as steadily rising IE across Na-Mg-Al.
- **[science]** Test for hydrogen gas (L2,3,6) — Real error: L2 (and L6 prompt) say hydrogen relights a glowing splint; correct test is the squeaky pop with a lighted splint (L3,L6 result). Needs author fix.
- **[science]** Group VII reactivity explained by electron affinity (L4) vs electronegativity/oxidising power (L7); argon as end of an electron-gain trend (L4) — Different but compatible explanatory framings (EA vs electronegativity); Cl does have the highest EA of Cl/Br/I; L4's argon remark is a loose preview, not a factual clash. No edit.

## chem_3_1 — Chemistry: Acids and Bases (3)
- **[structural]** 1 L4 seven-liquid set and 'three commercial indicators' — L4 deliberately uses a different seven-liquid set (vinegar in, Stoney/Jik out); 'three indicators' = litmus (red+blue paper), phenolphthalein, methyl orange, so the count is fine.
- **[structural]** 3 Kericho liming agent CaCO3 (L6) vs Ca(OH)2 (L9, L10) — Both are real agricultural limes; L6 is built throughout on the limestone + acid -> CO2 reaction, so aligning it to Ca(OH)2 would break the lesson. Needs author decision.
- **[science]** 4 Jik composition NaOH (L9) vs sodium hypochlorite (L7) — Real inaccuracy in L9: Jik is sodium hypochlorite (alkaline), not NaOH; not edited per rules.

## coremath_2_2 — Core Mathematics: Reflection and Congruence (3)
- **[structural]** When reflection properties were first discovered — L3 overview and slo already state the equidistance/perpendicular properties that L4 frames as first discovery; overlapping content, not a small edit.
- **[science]** Congruence lessons / direct vs opposite copy — L7 'sometimes a direct copy, sometimes mirror-flipped' refers to congruence tests generally vs reflection always opposite; not a real contradiction. L6 'next two lessons' is loose but acceptable.
- **[science]** Mirror line as guarantor of congruence (L2) vs congruence as open puzzle (L1/L7) — L2 frames congruent halves via line-of-symmetry definition, later lessons prove congruence from distance preservation; a difference of explanation, not editable by small edits.

## coremath_2_4 — Core Mathematics: Trigonometry 1 (3)
- **[science]** Angle of depression at mast top 40° (L3) vs equals elevation 50° (L7) — Real error in L3: the depression angle is 50° (alternate angles); 40° is the angle at the mast. Needs content fix
- **[structural]** Lake Victoria lighthouse angles: overview 32°/25° vs explain 120 m, 38°/22° in L8 — Overview and task disagree, and the task itself is geometrically impossible (elevation and depression between the same two points must be equal; mark scheme flounders). Needs rewrite, not a value swap
- **[science]** Mast geometry labelling / hawk depression at 40° in L3 — Same as the L3 depression-angle error above

## gensci_1_2 — General Science: The Cell (3)
- **[structural]** Plant cell EM in Lesson 2 / plant ultrastructure before L4 — L3 compares the animal cell with 'the plant cell from Lesson 2' though plant ultrastructure is taught in L4; fixed the explicit overclaims in L3 slo/sensemaking, the comparison framing in L3 overview remains (structural).
- **[science]** Number of organelles / lysosomes in plant cells — L5 includes lysosomes among plant organelles while L3/L4 treat them as animal-only; a real inconsistency (plant lysosomes are debated), not edited.
- **[science]** L3 absent structures vs L5 master diagram — Same lysosome issue as above; not edited.

## gensci_1_5 — General Science: Respiration (3)
- **[science]** Which organisms/acid cause the uji's sourness — Real contradiction: L1/L7/L8 attribute sourness to lactic acid bacteria, L4 to carbonic acid from yeast CO2 plus 'other organic acids', L6 to yeast producing 'lactic/acetic acid' (yeast do not make lactic acid). Needs content review.
- **[science]** Why fresh uji does not ferment: no organisms (L1, L4) vs lower substrate concentration (L6) — Real inconsistency in L6's summaryTablePrompt.explained; reviewer-worthy but science explanation, not edited.
- **[science]** Oxygen 'limited' vs absent for yeast anaerobic respiration — Wording difference (limited vs no oxygen); not a real contradiction.

## gensci_2_1 — General Science: The Periodic Table (3)
- **[science]** Group numbering 1-18 (L2) vs 1-8 (L3, L4) — Real inconsistency in notation; needs one convention chosen across the unit
- **[science]** Phosphate valency in DAP: PO4 3- vs HPO4 2- (L5, L6, L8) — Real contradiction; L5's DAP explanation should use HPO4 2- (valency 2)
- **[science]** (NH4)3PO4 'related to DAP' in L7 vs DAP = (NH4)2HPO4 — Real conceptual muddle in L7; equation does not produce DAP

## gensci_2_3 — General Science: Chemical Bonding (3)
- **[science]** Location of graphite's delocalised electrons (within vs between layers) — Real contradiction: L5 (pre-practical prediction, results sentence, model sketch, summary) says electrons are/move between layers, while L4, L7, L8 and FE say within/along layers. L5 is wrong and should be reviewed.
- **[science]** Graphite terminology (giant covalent vs giant atomic; six bond types vs four structural types) — Terminology varies but is not strictly contradictory (bond types vs structure types); minor.
- **[structural]** Lesson placement of metallic and giant covalent structures — L4 already teaches metallic bonding and graphite, but L6 defers them to L7 as still unexplained; sequencing issue, not edited.

## gensci_2_5 — General Science: Rates of Reactions (3)
- **[structural]** Which lesson investigated temperature — Real: no lesson runs a temperature investigation (only the L1 phenomenon demo). Repointed L4/L5/L6 'temperature (Lesson 3)' references to Lesson 1; L8 Station 2 'Rate vs Temperature graph (Lesson 3 class data)' cites data no lesson produces, left for review.
- **[structural]** Lessons 3 and 4 duplicate the concentration investigation — Real duplication (same four dilutions). Left.
- **[structural]** Catalysts and light covered in both L6 and L7; L8 counts four factors — Real duplication; L8's four-factor model omits light. Left.

## math_2_1 — Mathematics: Similarity and Enlargement (3)
- **[structural]** LSF/similarity introduced repeatedly (L2-L6) — Real duplication: L3 and L4 both discover similarity conditions, L5 and L6 both define LSF. Not edited.
- **[structural]** LSF first named in L1 vs L2 vs L5 — Part of the same duplication.
- **[structural]** No volume lesson: L7 and L8 both teach area scale factor; L7 promises VSF in L8; L11 assumes VSF = LSF^3 established — L7 and L8 duplicate ASF and no lesson investigates VSF; cannot be fixed by repointing references. Separate from the earlier LSF-duplication item (L2-L6).

## phys_1_2 — Physics: Mechanical Properties of Materials (3)
- **[science]** Sisal twine elastic behaviour (L1 vs L2); elastic limit 'formally introduced' in L6 — Slightly different thresholds for borderline sisal behaviour across two separate trials; L6 'formally introduces' a term already used - wording, not a real contradiction.
- **[structural]** Sequence of content: L3 uses Hooke's law and Ep = ½kx² before L4 introduces Hooke's law/k; L6 'formally introduces' elastic limit and Ep — Lessons 3 and 4 are effectively out of order (L3 applies k and the elastic limit that L4 introduces); not fixable by small edits. L5's 'Lessons 1-4' summary is consistent.
- **[science]** Cause of rope failure: L5 fracture stress / Young's modulus vs L6 low k beyond elastic limit; 3.73 m extension — Two different explanations of failure (stress exceeding fracture stress vs extension beyond elastic limit) and an unrealistic 3.73 m rope extension (784/210 is arithmetically right); content review, not edited.

## bio_2_1 — Biology: Plant Nutrition (2)
- **[structural]** Lesson 5 anchored on Elodea bubble data from Lesson 4 (Elodea is actually done in Lesson 7) — L5 is built throughout on bubble-count data learners have not yet collected (L4 is the starch test, Elodea is L7); cannot be fixed by renumbering since L7 is later. Needs lesson redesign or reorder.
- **[science]** Cause of wilting / stomata opening explained differently — Complementary explanations (light opens stomata; light+temperature raise transpiration); not a real contradiction.

## bio_3_2 — Biology: Animal Transport (2)
- **[science]** 0 fish heart chambers / efficiency meter ordering — Fish 2-chamber description consistent across lessons; L5 efficiency meter ranking fish above frog/lizard is a questionable pedagogical device, not a cross-lesson contradiction.
- **[science]** 14 grasshopper ~60% oxygen-delivery efficiency vs haemolymph carries no oxygen — Real tension: L5 meter assigns an oxygen-delivery efficiency to an animal whose blood L3 says carries no oxygen; needs author judgement, not edited.

## chem_1_2 — Chemistry: The Atom (2)
- **[science]** chlorine isotopes 'glow green (copper-like)' — Real error in L5: chlorine has no characteristic green flame colour; L4 makes no such claim. Needs a content fix, not edited here.
- **[science]** H in Group 1 with similar flame colours — Placing H with ns1 elements is a common simplification; 'similar but distinct colours' is loose wording, not a cross-lesson contradiction.

## coremath_1_1 — Core Mathematics: Real Numbers (2)
- **[science]** Number system hierarchy (whole numbers included or not) — L2 Venn omits Whole numbers while L4/L8 include them; a real inconsistency in presentation, not edited.
- **[structural]** Kericho temperature dataset L4 vs L8 — Different Kericho datasets in L4 and L8; not edited.

## coremath_2_3 — Core Mathematics: Rotation (2)
- **[science]** Rotation: direct vs opposite congruence (L7 vs L8) — Real and serious: L7 teaches rotation gives OPPOSITE congruence (incorrect); L8 correctly says direct. L7 needs an author rewrite.
- **[science]** Clock rotational symmetry order 12 vs infinite (L6 vs L8) — Not really contradictory: marked 12-hour face (order 12) vs plain circle (infinite); could confuse learners.

## coremath_2_7 — Core Mathematics: Surface Area and Volume of Solids (2)
- **[structural]** Lesson numbering of composite solids / cylinder volume derivation — L6 uses V = πr²h without deriving it although L5 promised a derivation; L6 forward refs to L7 composites are correct. Minor, left.
- **[structural]** Composite solids covered in both L4 and L7 — Real overlap (L4 does composite surface area, L7 surface area and volume). Left.

## essmath_1_1 — Essential Mathematics: Real Numbers (2)
- **[science]** Hierarchy of number sets (L8 nested ovals) — Real error: L8 Reference Map template nests the Irrational oval between Q and R, contradicting L6 and L8's own slo/assessment; not edited per rules.
- **[science]** Rational/irrational boundary under operations — L6 overstates that the boundary is preserved under all operations (e.g. sqrt2 x sqrt2 = 2); real but minor overclaim; not edited.

## essmath_2_3 — Essential Mathematics: Trigonometry (2)
- **[structural]** Which lesson discovered the constant ratio / named tangent — Fixed L3's 'Lesson 2' references to Lesson 1 (L1 did the ratio measurement). L4 re-runs the constant-ratio discovery as new after L3 already derived sin/cos/tan: real duplication, left. Also L4 claims 35° at 6 m and 10 m give the same height (they give 4.2 m and 7.0 m): real maths error, not edited.
- **[science]** Complementary angles and the two students' agreement (L5 vs L6) — Real conceptual problem: complementary angles do not explain why two observers agree (L1 data 38°/22° are not complementary); L6's claim about the top angle is correct geometry but different. Left.

## essmath_2_7 — Essential Mathematics: Volume and Capacity (2)
- **[structural]** container dimensions/capacities (L1 d=20 cm, 9.4/3.1/6.5 L vs L4/L8 d=28 cm, 18.47/6.16 L; L2 r=21,h=42) — L1 and L8 (both authoritative) disagree; L1 is internally consistent on d=20, L4/L8 on d=28, L2 on its own r=21/h=42 cone. Needs a module-level choice; not edited. Only L6's stray '141 litres in Lesson 4' was fixed to 18.5 L (L4's 18.47 L).
- **[structural]** opening diameter 20 vs 42 vs 28 cm — Same issue as above.

## essmath_3_2 — Essential Mathematics: Probability I (2)
- **[science]** Gor Mahia match probability (1/3 vs 0.5 vs 0.6) — Real conceptual tension: L1 asks whether a match is equally likely, L4 and the FE assume W/D/L = 1/3 each; L7 (0.5) and L8 (0.6) are explicitly stated simplifying assumptions. Not edited.
- **[science]** Why the 'win AND draw' advert is misleading (L4 vs L5) / P(A and B)=0 — P(A and B)=0 for mutually exclusive events is stated consistently in L4 and L8; L4 and L5 just emphasise different reasons the advert misleads. Not a factual conflict.

## g11_bio_1_2 — Biology: Ecology (2)
- **[science]** L1 rules out old age / lack of food; L7 lists food competition and predation as contributing factors — Mild tension, not a hard contradiction: L1 says these alone cannot explain the decline, L7 says they act together with nutrient enrichment
- **[science]** Algae as producers (L1) vs grouped with hydrophytes (L2) — Minor real inaccuracy in L2 (algae are not hydrophyte plants); no cross-lesson factual clash

## g11_bio_1_3 — Biology: Taxonomy II (2)
- **[science]** 0 moss true stems/leaves — Lessons agree bryophytes lack true roots, stems and leaves; 'stem-like/leaf-like' wording is standard, not a real contradiction.
- **[structural]** 4 which lesson introduces animal dichotomous keys — L6 already has learners write an animal key before L7 'introduces' it; overlap of content between lessons. Only L7's wrong 'last lesson' grouping reference edited.

## g11_bio_3_1 — Biology: Reproduction in Animals (2)
- **[science]** Fish fertilisation (L1 vs L3/L7) — L1 correctly separates externally spawning tilapia from internally fertilising sharks/guppies; L7's 'frogs and fish (external)' is a simplification. Not a real contradiction.
- **[science]** Hen fertilisation type / L7 category mixing — L7 lists fertilisation site and development type together; wording looseness, not a real contradiction of L1.

## gensci_1_3 — General Science: Nutrition in Animals (2)
- **[science]** Stomach enzymes (rennin in L3 only) — Minor real inaccuracy: rennin is negligible in human adults; not a contradiction between lessons. Left.
- **[science]** How the body 'knows' which chemical to release: glands/regions (L3), sphincters (L6), genetic programming (L7), hormonal and neural signals (L8) — Lessons give different partial explanations of digestive control that are never reconciled into one account (L8's hormonal/neural one is the accepted mechanism). No edit.

## gensci_1_6 — General Science: Plant Growth and Development (2)
- **[science]** Why the stored seeds failed to germinate — Real contradiction: L3 attributes failure to lack of water (Cup B), but the phenomenon (L2) says the seeds were planted with water and warmth and L2/L6 attribute it to dormancy/ABA. Needs rewording of L3's question and explanation, not done.
- **[science]** Auxin / apical dominance / etiolation — L6 attributes maize's unbranched habit to apical dominance vs branching beans; L8 links etiolation to auxin. Loose but not a clear contradiction.

## gensci_3_3 — General Science: Waves (2)
- **[science]** Why water waves reach the sheltered cove (L8 refraction vs L4/L5 diffraction) — Real contradiction: L8 Explained says refraction steers energy into the protected cove; L4 and L5 say refraction cannot explain the cove and diffraction does. Not edited.
- **[science]** Cats-eye reflectors reflection vs refraction — Within-L6 wording looseness; not a real between-lesson contradiction.

## math_2_2 — Mathematics: Area of Polygons (2)
- **[structural]** Shamba dimensions: L1 (48,35,52,40,37), L2 AB=120/AC=95/68 deg, L4 sub-plot 40/55/63, L7 (42,38,45,30,50) — Real: L1's sides are given 'e.g.' and later lessons (and FE Part 2) each use their own numbers with full worked calculations; reconciling needs one designed dataset, not spot edits.
- **[science]** Height expression in the sine-formula derivation (c sin A, b sin theta, a sin C) — Labelling differences depending on which sides are named; not a real contradiction.

## math_2_4 — Mathematics: Surface Area and Volume of Solids (2)
- **[science]** Base included in SA (L5) vs excluded (L10) — Different modelling conventions for different tasks; minor, could confuse but each lesson is self-consistent.
- **[structural]** Frustum volume never reaches 5,000 L (L3 ≈1.3 m³, L7 ≈3.3 m³) — Real: no lesson's frustum dimensions give 5,000 L, while L1/L9/L10/FE assert both tanks hold 5,000 L; L3's comparison sentence also needs the composite SA before L5 computes it. Needs a dataset redesign.

## math_3_4 — Mathematics: Linear Motion (2)
- **[science]** Meaning of negative acceleration (L3 vs L7) — Minor real imprecision: L7 says negative may mean a change of direction; L3 says slowing while moving forward. Left.
- **[structural]** L10 overtaking uses s = ut + ½at², not taught earlier — Real gap: the equation is not taught in L1–L9. Left.

## phys_1_3 — Physics: Temperature and Thermal Expansion (2)
- **[science]** Temperature at which water starts expanding: 0 °C freezing vs below 4 °C (L1, 2, 4, 6) — Anomalous expansion below 4 °C plus the 9% freezing expansion are both true; L6's 'lattice forms from 4 to 0 °C' wording is a science imprecision for teacher review.
- **[science]** Whether the 9% freezing expansion is covered by ΔV = γV₀ΔT (L4, 6) — L4 summaryTablePrompt.explained ends 'The volumetric expansion can be quantified using ΔV = γV₀ΔT', contradicting L4 Q2/L6/FE (phase change beyond the formula); science wording for teacher review.

## phys_1_5 — Physics: Moments of Equilibrium (2)
- **[science]** Toppling: 'no opposing moment' (L1) vs stool weight gives stabilising moment (L4) — Real: L1's explanation omits the stool's own weight, which L4 correctly treats as the opposing moment; L1 wording needs author attention.
- **[science]** Stability condition and equilibrium type (L4, L6) — Compatible framings (moment comparison vs stable equilibrium); the misattributed recap lesson numbers were fixed above.

## phys_2_1 — Physics: Properties of Waves (2)
- **[science]** Mechanism of FM fade: diffraction vs interference vs TIR (L10 model building) — Lessons explain the fade with different mechanisms; L10 model-building still has FM undergoing TIR at the tunnel wall, which needs rewriting, not a small edit.
- **[structural]** Duplicate v=fλ lessons (L3 and L5); unit model start L1 vs L2 — L3 and L5 both teach v=fλ (duplicated lessons). Model start refs are defensible: L1 Initial Wave Model, L2 starts the Running Wave Model.

## phys_3_1 — Physics: Radioactivity and Stability of Isotopes (2)
- **[science]** Beta-minus decay 'horizontal' on N vs Z plot (L2) vs arrows toward belt (L5) — Real error inside L2: Z+1, N-1 is a diagonal move; L5 not contradictory
- **[science]** C-14 dating sites (Olorgesailie, Fort Jesus, Koobi Fora Homo habilis) — Different sites are fine; C-14 for a ~1.8 Myr fossil would be wrong if L7 presents it as valid (likely a method-choice comparison)

## phys_3_2 — Physics: Current Electricity (2)
- **[structural]** 4 L9 'Lesson 6 data tables' with power column — L6 parallel-circuit V/I data can take a P = VI column, but L9's claim about higher-resistance components at the same current does not fit parallel data; minor, not edited.
- **[science]** 5 cause of dim lights at power restoration — Real contradiction in the phenomenon's explanation: L2/L8/L12 blame supply internal resistance (surge current, Ir drop) while L11 calls it a brownout (supply below 240 V). Needs author decision.

## phys_3_4 — Physics: Electrostatics (2)
- **[structural]** Coulomb's Law taught in both L3 and L5; Q-V attributed to L5/6 — Real duplication (L3 and L5 both introduce Coulomb's Law; L7 and L8 both cover capacitor energy). Fixed L8's Lesson 5 pointers to Lessons 6–7. Also L6/L9 cite 'electric field (Lesson 4)' and 'potential difference (Lesson 5)', which no lesson teaches as such; left.
- **[science]** Why traders' hairs stood up (L1 hairs repel each other vs L2 attracted toward the cloud) and roof charge (L2 conduction vs L4/L5/L9 induction) — Hair: L1 explains by mutual repulsion of like-charged hairs, L2 by attraction of opposite charges toward the cloud - different explanations for teachers. Roof: conduction path and induced positive charge (L9 'deficit') are complementary, as judged earlier.

## phys_4_2 — Physics: Introduction to Space Physics (2)
- **[science]** First galaxies ~1 billion years after Big Bang (L2) vs JWST galaxies at ~300 million years (L7/L8) — Real but mild inconsistency; L2's figure is outdated relative to JWST statements.
- **[science]** Geomagnetic storm tidal anomaly in Mombasa (L9) vs Moon-driven tides (L6) — Storm-surge anomaly vs astronomical tide are different effects; questionable science in L9 but not a direct contradiction.

## bio_1_1 — Biology: Cell Structure (1)
- **[structural]** Cells involved in wound healing — L8 teaches a different five-cell set (incl. sperm, acknowledged as not involved) from L1/L10/L12's healing cells; curriculum-driven, not edited.

## coremath_2_1 — Core Mathematics: Similarity and Enlargement (1)
- **[science]** Direction of L.S.F 1:200 (plan as image, L.S.F = 1/200) vs L5 real-to-plan area ratio 200^2 — Presentation inconsistency: L2/L3 distinguish L.S.F 1/200 (real->plan) from 200 (plan->real), L5 writes 'L.S.F = 1:200' and asks for real/plan area ratio without stating the inversion; answer 40 000 is correct. Author should state direction explicitly.

## coremath_2_5 — Core Mathematics: Area of Polygons (1)
- **[structural]** 4 triangle heights measured directly (L4) vs hidden (L3) — L3 motivates the sine formula with an unmeasurable height but L4 measures all heights directly; design tension, not edited. L1 estimate vs L2 'numerical areas later' is not a contradiction.

## coremath_2_6 — Core Mathematics: Area of a Part of a Circle (1)
- **[structural]** Radius of the Laikipia running diagram — Each lesson uses different pivot dimensions (L1 120/80, L2 40, L3 21, L4 70/40); no single dataset to align to, and dependent arithmetic throughout; not edited.

## coremath_2_8 — Core Mathematics: Vectors (1)
- **[structural]** L4 vector d = (2,1) as Kencom-to-Westlands '8 km vector' — L4 is built throughout on d=(2,1) (3d, half d, -d); changing it would rewrite the lesson. Not edited.

## coremath_3_2 — Core Mathematics: Probability I (1)
- **[structural]** L4 uses 'the Lesson 1 dice-rolling experiment results'; L1 only had a coin-toss experiment — No lesson in the module runs a two-dice rolling experiment (L1 coins, L3 dice grid only), so there is no lesson to repoint the reference to; L4 Task 1 needs rewording or a dice experiment added.

## essmath_1_2 — Essential Mathematics: Indices (1)
- **[science]** Zero-index treatment (L4,6,7) — Different framings of a⁰ = 1, not contradictory in substance.

## essmath_2_2 — Essential Mathematics: Reflection (1)
- **[science]** L4 models side mirror as y-axis and rear-view mirror as x-axis reflection vs same plane-mirror principle elsewhere — Earlier logged false_positive (same geometry); the only real issue is L4's loose modelling of a rear-view mirror as an x-axis ('floor') reflection, which is physically odd. Teacher note, not edited.

## essmath_2_5 — Essential Mathematics: Area of Part of a Circle (1)
- **[science]** L7 treats the customer's piece as a segment (90 deg, r=21: 346.4-220.5=125.9 cm2) while L1/L2 treat it as a sector wedge — Arithmetic is correct throughout; the difference is a modelling reframe (wedge = sector vs chord cut = segment) that the lessons do not reconcile. No edit.

## essmath_2_6 — Essential Mathematics: Surface Area of Solids (1)
- **[structural]** Which lesson covers cylinder/sphere/hemisphere/frustum; cylinder never taught (L1-L5) — No lesson teaches the cylinder surface area although the cylinder bucket is used in L3, L6 and L8 (and L3/L4 both derive the hemisphere). Wrong lesson pointers fixed as cross_reference: L1 placeholders and reflection, L3 storyline and reflection, L5 'Lessons 6-7'.

## g11_bio_1_1 — Biology: Taxonomy I (1)
- **[structural]** Next-lesson questions regress (L6 asks about larger categories after L3-4 hierarchy) — Real but mild sequencing issue; L6's 'larger categories' lead-in to L7 kingdoms echoes the KICD key inquiry question. Not patched.

## g11_bio_1_4 — Biology: Cell Division (1)
- **[science]** Interphase counted as a mitosis stage — L7 lists interphase as stage 1 of five while L3 teaches four stages plus cytokinesis; mild real inconsistency in presentation, not edited.

## g11_bio_2_3 — Biology: Excretion in Plants (1)
- **[structural]** Guttation experiment set up in L2 (POE, bell jar, read Day 2) and set up again in L3 — L1->L2 reference is correct. L3 repeats a POE guttation setup (labelled an 'extension') and repeats L2's guttation-vs-transpiration exit ticket; real duplication, needs a design decision rather than a fact edit.

## g11_bio_3_2 — Biology: Growth and Development in Animals (1)
- **[science]** Role of JH in incomplete metamorphosis and final moult (L4,5,6) — Not a real contradiction: 'absent' (L4) vs 'falling' (L5) are compatible descriptions of JH decline before the adult moult.

## g11_bio_3_3 — Biology: Excretion and Homeostasis in Animals (1)
- **[science]** Nitrogenous waste of marine fish (urea, L1) vs fish as ammonia (L7) — Not a real contradiction: L1 specifies urea for marine cartilaginous fish; L7's 'fish = ammonia' is a simplification for bony fish

## gensci_1_4 — General Science: Transport in Plants (1)
- **[science]** main force driving xylem water (root pressure L3 vs transpiration pull L7/L8) — Partly real: L3 presents root pressure as why the dye rose, but L3 itself flags it as insufficient for tall plants and L7/L8 complete the picture; progressive, not contradictory.

## gensci_2_4 — General Science: Acids, Bases and Salts (1)
- **[science]** Hygroscopic/efflorescent definitions and trona 'not by efflorescence' (L5, L6) — L5 says trona crusts gain/lose water with humidity but form by crystallisation, not efflorescence; a nuance of explanation, not a cross-lesson data conflict.

## math_1_4 — Mathematics: Congruence (1)
- **[science]** Waterline position / mirror line always y = mx + c — Real error: L5 and L8 say a mirror line can always be written y = mx + c, which excludes the vertical lines x = 3 and x = -1 taught in L3. The waterline moving (y = 0, y = k, hidden) across lessons is deliberate variation, not a contradiction. Not edited.

## math_2_3 — Mathematics: Area of Part of a Circle (1)
- **[structural]** When the sector area formula is taught: L1 Explain names and writes A = (θ/360°)πr², L2 formalises it, L3/L4 treat it as derived new in L4 — L1's Explain and model phases already name and apply the sector area formula although its overview says no formula is taught, and L4 derives it as new; sequencing issue, not edited (earlier pass missed L1's Explain phase).

## math_3_1 — Mathematics: Trigonometry I (1)
- **[structural]** Special angles derived in L7 then re-derived as new in L8 — Real L7/L8 overlap; fixed only L8's wrong 'last lesson' reference

## math_3_2 — Mathematics: Rotation (1)
- **[science]** 1 P(4,2) images; -240 rotation in L10 — L3 images are correct. Separate real error found in L10: B(4,0) rotated by -240 (= +120) is (-2, 2*sqrt3), not B'(0,4) as the L10 teacherReflection states; also uses a non-90 multiple never taught. Not edited (single-lesson maths error).

## math_3_3 — Mathematics: Vectors I (1)
- **[structural]** Scale of L1 rough ferry model — L1's first rough model uses arrow lengths (4 and 2 squares) that do not match the scale it states; a naive first model, not edited.
