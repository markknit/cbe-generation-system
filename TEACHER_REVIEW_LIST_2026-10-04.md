# Teacher / author review list

Updated 2026-10-04 after: regeneration of the 8 worst sub-strands with the fact sheet, the science-fix pass, and an independent check of every science fix (0 reverted). Fixed items are removed; audit trail in `logs/lesson_repairs/<module>.cc.json`.

- **science — needs rewrite**: a real error whose fix changes an activity, dataset or worked answer.
- **structural**: duplicated lessons, wrong order, or reliance on an activity no lesson contains.
- **teaching choice**: two acceptable explanations; pick one (or accept both).
- **science (unclassified)**: not matched to a fix-pass verdict; check it.

**103 items in 57 sub-strands** (was 207): 26 needs-rewrite, 57 structural, 19 teaching choices, 0 unclassified. Removed: 46 fixed, 33 not real, 31 in regenerated sub-strands.

## gensci_3_2 — General Science: Linear Motion (6) (5)
- **[science — needs rewrite]** Whether the cart on the slope accelerates at g — A cart on a slope accelerates at g sin(theta) < g; fixing L4/L5/L7 means changing their worked calculations and the single cart acceleration used across lessons.
- **[structural]** Mkokoteni acceleration 2 (L2), 2.5 (L3), 9.8/10 (L4, L5, L7), ~3 slope component (L8) — Real: each lesson builds its calculations on a different acceleration and L4/L5/L7 model the cart as in free fall, which L8 rejects. Changing values would cascade through every worked answer; needs a decision on one cart acceleration. Only removed L3's false claim that 2.5 came from the previous les
- **[structural]** Cart speed/distance after 8 s: 16 m/s (L2) vs 20 m/s, 80 m (L3) vs 24 m/s (L8) — Follows from the different accelerations above; each lesson's arithmetic is internally correct.
- **[structural]** Drop heights: exactly 2 m (L4) vs 0.5-2.0 m class table (L5); g ~9.8 vs ~10 — L5 relies on a multi-height Lesson 4 table L4 never produced; g 9.8 vs 'roughly 10' is a rounding difference (false positive part).
- **[teaching choice]** Three vs four equations of linear motion — Four equations (incl. s = (u+v)t/2) or the three used for free fall are both standard; count wording is a teacher choice.

## math_1_1 — Mathematics: Real Numbers (6) (5)
- **[structural]** Source of the √2/2 ≈ 0.7071 slice (arc vs radius fraction vs chord vs fraction of pizza) — Pizza B's irrational slice is defined loosely and differently across lessons; needs a single definition, not a word swap
- **[structural]** Cumulative model name / DQB column labels; L3 booklet 'begun in Lesson 1' — Artefact naming drifts lesson to lesson (map, booklet, model); not a single-word fix
- **[structural]** L3 cites rational/irrational and number line as already taught (Lesson 2 / last lesson), but L4 teaches them — L3 and L4 appear written in swapped order; references are consistent with that other order, so needs a re-sequencing decision
- **[structural]** Reciprocals taught fully in L3 then 'introduced' as new in L5 — Real duplication of content between L3 and L5
- **[teaching choice]** Whether 1/3 is 'messy' (L1) or a 'neat' rational slice (L7) — Both lessons treat 1/3 as rational; "messy" (repeating decimal) vs "neat" (fraction) is framing only.

## phys_1_4 — Physics: Energy, Work, Power and Machines (4) (5)
- **[science — needs rewrite]** Whether the nut moved / work done and source of heat (L3 vs L4) — L3 sets d = 0 so W = 0 yet credits heat to friction work; resolving it means rewriting the L3/L4 worked reasoning about slip.
- **[science — needs rewrite]** Spanner energy as gravitational PE (L1-2) vs lever work (L3-8) — L1-2 model the spanner energy as gravitational PE, later lessons as lever work from chemical energy; fixing requires redesigning the L1-2 energy model.
- **[science — needs rewrite]** Power vs strength; Kipchoge 1,000 W — Power depends on rate of work, not strength; also L5 data (800 N x 5.85 m/s = 4,680 W) contradicts the L5 summary "roughly 1,000 W" and 800 N is unrealistic — needs the Kipchoge dataset reworked.
- **[science — needs rewrite]** L5 Kipchoge power: 800 N x 5.85 m/s = 4,680 W contradicts 'roughly 1,000 W'; 800 N is not a realistic running force — found by fixer
- **[structural]** Spanner MA / force figures (L3, L6, L7, L8) — Each lesson uses its own lever numbers (L3 handle 0.15 vs 0.45 m, L6 'about 4 times longer' with 50 N -> 200 N, L7 MA 4 vs 2, L8 'e.g. MA = 3.5'). Aligning would cascade through dependent calculations in L6 and L7.

## phys_3_3 — Physics: Introduction to Electronics (5) (4)
- **[science — needs rewrite]** Mechanism by which heat reduces output — Accepted mechanism: higher T raises intrinsic carrier concentration/recombination (dark saturation current), lowering Voc; Isc rises slightly. L3/L6's mobility-scattering chain is wrong as primary cause; fixing needs rewrites of L3, L6, L7 explanations.
- **[structural]** Turkana case study and superconductors in L6 — L6 uses a separate Turkana case study and groups superconductors with semiconductors; case-study design choice, not edited.
- **[structural]** Lesson where p-n junction explains temperature effect — L3 already offers a full temperature mechanism before L4/L5 defer it; sequencing issue, not edited.
- **[teaching choice]** Role of band gap / light vs heat / darkness conduction — 'Insulator-like in darkness' is a standard simplification (intrinsic Si conducts only slightly via thermal promotion); level of detail is a teacher choice.

## g11_bio_2_2 — Biology: Growth and Development in Plants (5) (3)
- **[structural]** hormones question loops L6->L7->L8->L9 — Real sequencing loop: L7 and L9 both teach hormones; L8 re-raises the hormone question. Not edited.
- **[structural]** measuring growth in L6 and again L8 — L6 and L8 both measure growth and plot curves; duplicate content.
- **[structural]** maize/bean growth data L6 vs L8 — L6's figures are an 'e.g.' of student data, L8's a back-up table; follows from the L6/L8 duplication. Not edited.

## bio_2_3 — Biology: Plant Gaseous Exchange and Respiration (4) (3)
- **[science — needs rewrite]** Identity of gas in sukuma wiki bubbles (L4,8,9,11,12) — Bubble gas identity (O2 vs CO2) is a storyline-level decision tied to the anchoring phenomenon and untested bubbles; not a text patch.
- **[structural]** Project investigation tracks (L9 anaerobic vs L10 plant gas exchange vs L11 anaerobic) — Real: L10 executes a different project from the one L9 plans and L11 presents; needs regeneration of L10, not a patch.
- **[teaching choice]** Warm water: stomatal opening vs enzyme rates (L2,3 vs L4-12) — Stomatal and enzyme framings of temperature are both valid and compatible; teacher can reconcile.

## chem_1_1 — Chemistry: Introduction to Chemistry (4) (3)
- **[structural]** Which lesson covers states of matter / physical vs chemical change / properties — Fixed L4's wrong 'Lesson 3' pointer to Lesson 1 (PhET). Remaining: L6/L9/L10 recaps claim physical vs chemical change and properties of matter were taught, but only L1 touches them. Real gap, left for review.
- **[structural]** Concept map vs model format across lessons — Real but minor: L1 builds a before/after drawing, later lessons call it a concept map, L5 a class model. Left.
- **[structural]** Drug/prescription/dosage introduced in L4 and again in L7; DQB statements at start of unit — L4 exit task and L7 overlap (duplication, left). L8 'from Lesson 7' is accurate. Fixed L4's claim that DQB statements were posted at the start of the unit.

## phys_4_1 — Physics: Greenhouse Effect and Climate Change (4) (3)
- **[science — needs rewrite]** L6 'UV rising' framing vs UV-B data declining after late 1990s — L6 anchoring question frames Nairobi UV as rising while the lesson dataset shows a decline after the late 1990s; reframing touches the anchoring phenomenon and dataset, and real tropical UV-B trends need checking.
- **[structural]** when the ozone layer was taught (L5 vs L6) — L3 briefly distinguishes ozone (UV) from GHGs while correcting a misconception, L5 assumes ozone was covered, L6 introduces it as new. Sequencing overlap; not edited. Fixed only L5's IR-trapping lesson pointers.
- **[teaching choice]** moisture source for long rains — Lake Victoria/Indian Ocean moisture and ITCZ are complementary emphases.

## gensci_2_1 — General Science: The Periodic Table (3) (3)
- **[science — needs rewrite]** (NH4)3PO4 'related to DAP' in L7 vs DAP = (NH4)2HPO4 — L7 worksheet balances 3NH4OH + H3PO4 -> (NH4)3PO4 while the lesson/gallery cards target (NH4)2HPO4 and the Predict Card annotates DAP with the (NH4)3PO4 ratio; needs the equation (e.g. 2NH3 + H3PO4 -> (NH4)2HPO4) and annotation redesigned. The false claim that DAP needs 3 ammonium was corrected unde
- **[science — needs rewrite]** L7 equation (3) 'Ca + 2HNO3 -> Ca(NO3)2 + H2': nitric acid generally does not give H2 with metals — found by checker
- **[teaching choice]** Group numbering 1-18 (L2) vs 1-8 (L3, L4) — Both IUPAC 1-18 and traditional I-VIII group numbering are valid; teacher should pick one convention for the unit.

## gensci_2_5 — General Science: Rates of Reactions (3) (3)
- **[structural]** Which lesson investigated temperature — Real: no lesson runs a temperature investigation (only the L1 phenomenon demo). Repointed L4/L5/L6 'temperature (Lesson 3)' references to Lesson 1; L8 Station 2 'Rate vs Temperature graph (Lesson 3 class data)' cites data no lesson produces, left for review.
- **[structural]** Lessons 3 and 4 duplicate the concentration investigation — Real duplication (same four dilutions). Left.
- **[structural]** Catalysts and light covered in both L6 and L7; L8 counts four factors — Real duplication; L8's four-factor model omits light. Left.

## essmath_2_3 — Essential Mathematics: Trigonometry (2) (3)
- **[science — needs rewrite]** Complementary angles and the two students' agreement (L5 vs L6) — The two observers agree because both triangles share the fixed height (h = d·tanθ); complementary-angle identity does not explain it. L5/L6 storyline framing, L6 attitudes (supplementary angles) and reflection problem would need redesign.
- **[science — needs rewrite]** L1/L6: the two observers' data give different tank heights (7.81 m vs 8.08 m; 14.3 m vs 12.6 m) — found by fixer
- **[structural]** Which lesson discovered the constant ratio / named tangent — Fixed L3's 'Lesson 2' references to Lesson 1 (L1 did the ratio measurement). L4 re-runs the constant-ratio discovery as new after L3 already derived sin/cos/tan: real duplication, left. Also L4 claims 35° at 6 m and 10 m give the same height (they give 4.2 m and 7.0 m): real maths error, not edited.

## gensci_1_7 — General Science: Microorganisms (4) (2)
- **[teaching choice]** Patch organisms: fungal moulds (L1,2,8) vs fungi and bacteria (L5) — Bacteria do co-colonise spoiled food alongside moulds; L5 adding bacteria is correct, only a level-of-detail difference.
- **[teaching choice]** Patch fungi in 'same broad group' as yoghurt Lactobacillus (L2 vs L6) — Moulds, yeast and Lactobacillus are all microorganisms, so the "same broad group" true/false prompt is defensible; it is a deliberate discussion prompt.

## gensci_3_1 — General Science: Turning Effect of Force (4) (2)
- **[science — needs rewrite]** two-handed grip as couple (L4) vs single force about pivot — Reconciling L4's pure-couple model of the two-handed grip with the single-pivot moment model used elsewhere requires redesigning L4's explanation.
- **[science — needs rewrite]** L2 200 g at 30 cm balanced by 100 g (needs 60 cm) — Correct: 2 N x 30 cm needs 1 N at 60 cm, beyond the 50 cm half-rule. Fix changes the L2 activity setup (e.g. place 200 g at 20 cm -> 100 g at 40 cm); left for author.

## gensci_3_4 — General Science: Magnetism and Electromagnetic Induction (4) (2)
- **[science — needs rewrite]** Stopping the generator = demagnetisation (L2) vs no relative motion (L4,5,6,8) — Correct science: the dynamo stops because there is no relative motion/flux change, not demagnetisation. L2's title, purpose, storyline link, overview, model check and summary are all built on the wrong analogy - needs author rewrite of L2's phenomenon link.
- **[science — needs rewrite]** Bell make-and-break = generator switching mechanism (L7,8) — Correct science: a generator's output and polarity reversal come from the rotating coil cutting a steady field (induction), not make-and-break switching or magnetisation/demagnetisation. The claim is built into L7's purpose, model-revision group tasks and comparison table, and L8's summary - needs r

## chem_1_3 — Chemistry: The Periodic Table (3) (2)
- **[structural]** Group numbering Roman (I, VII, VIII/0) in L3 vs Arabic (1, 17, 18) in L4+ — Real notation inconsistency across lessons, never reconciled; needs a deliberate choice, not a fact edit.
- **[structural]** L2 says Lesson 1 sketch arranged a subset of 10 cards; L1 sorts 20 — Minor mismatch built into L2's revision activity (re-sort their 10 cards); left.

## chem_1_4 — Chemistry: Chemical Bonding (3) (2)
- **[structural]** Whether graphite conductivity data was collected (L8 vs L9) — L9 is written around four substances and hedges on whether graphite was tested, while L8 tests graphite; would need rewriting L9's activity, not a small edit.
- **[teaching choice]** Na+ empty outer shell wording — Drawing Na+ with an empty third shell vs a full 2,8 shell are both accepted dot-and-cross conventions.

## chem_3_1 — Chemistry: Acids and Bases (3) (2)
- **[structural]** 1 L4 seven-liquid set and 'three commercial indicators' — L4 deliberately uses a different seven-liquid set (vinegar in, Stoney/Jik out); 'three indicators' = litmus (red+blue paper), phenolphthalein, methyl orange, so the count is fine.
- **[structural]** 3 Kericho liming agent CaCO3 (L6) vs Ca(OH)2 (L9, L10) — Both are real agricultural limes; L6 is built throughout on the limestone + acid -> CO2 reaction, so aligning it to Ca(OH)2 would break the lesson. Needs author decision.

## coremath_2_2 — Core Mathematics: Reflection and Congruence (3) (2)
- **[structural]** When reflection properties were first discovered — L3 overview and slo already state the equidistance/perpendicular properties that L4 frames as first discovery; overlapping content, not a small edit.
- **[teaching choice]** Mirror line as guarantor of congruence (L2) vs congruence as open puzzle (L1/L7) — Line-of-symmetry framing (L2) vs distance-preservation proof (L7) are two valid explanations at different depths.

## coremath_2_4 — Core Mathematics: Trigonometry 1 (3) (2)
- **[science — needs rewrite]** L8 lighthouse problem: 38° elevation and 22° depression along the same line of sight must be equal; L8 overview uses 32°/25° — found by checker
- **[structural]** Lake Victoria lighthouse angles: overview 32°/25° vs explain 120 m, 38°/22° in L8 — Overview and task disagree, and the task itself is geometrically impossible (elevation and depression between the same two points must be equal; mark scheme flounders). Needs rewrite, not a value swap

## gensci_2_3 — General Science: Chemical Bonding (3) (2)
- **[structural]** Lesson placement of metallic and giant covalent structures — L4 already teaches metallic bonding and graphite, but L6 defers them to L7 as still unexplained; sequencing issue, not edited.
- **[teaching choice]** Graphite terminology (giant covalent vs giant atomic; six bond types vs four structural types) — 'Giant covalent' and 'giant atomic' are both accepted names for graphite's structure; bond types vs structure types are different classifications, not a contradiction.

## phys_1_2 — Physics: Mechanical Properties of Materials (3) (2)
- **[science — needs rewrite]** Cause of rope failure: L5 fracture stress / Young's modulus vs L6 low k beyond elastic limit; 3.73 m extension — 3.73 m = 784/210 applies Hooke law beyond the 2.1 m elastic limit (invalid) and is embedded in the L6 data card, FE table and worked answers; failure explanations (fracture stress vs beyond elastic limit) are compatible but need content review.
- **[structural]** Sequence of content: L3 uses Hooke's law and Ep = ½kx² before L4 introduces Hooke's law/k; L6 'formally introduces' elastic limit and Ep — Lessons 3 and 4 are effectively out of order (L3 applies k and the elastic limit that L4 introduces); not fixable by small edits. L5's 'Lessons 1-4' summary is consistent.

## bio_3_2 — Biology: Animal Transport (2) (2)
- **[science — needs rewrite]** 0 fish heart chambers / efficiency meter ordering — Fish 2-chamber heart is consistent; the L5 Efficiency Meter values/ordering are a dataset design choice — changing them means changing the dataset.
- **[science — needs rewrite]** 14 grasshopper ~60% oxygen-delivery efficiency vs haemolymph carries no oxygen — Insect haemolymph does not carry O2 (tracheae do); L5 data table and meter assign grasshopper ~60% oxygenation — fixing requires redesigning the L5 dataset.

## coremath_1_1 — Core Mathematics: Real Numbers (2) (2)
- **[structural]** Kericho temperature dataset L4 vs L8 — Different Kericho datasets in L4 and L8; not edited.
- **[teaching choice]** Number system hierarchy (whole numbers included or not) — N ⊂ Z ⊂ Q ⊂ R is correct with or without a separate W region (N ⊂ W ⊂ Z); adding W to L2 Venn would change its five-region model activity, so teacher should pick one presentation.

## coremath_2_7 — Core Mathematics: Surface Area and Volume of Solids (2) (2)
- **[structural]** Lesson numbering of composite solids / cylinder volume derivation — L6 uses V = πr²h without deriving it although L5 promised a derivation; L6 forward refs to L7 composites are correct. Minor, left.
- **[structural]** Composite solids covered in both L4 and L7 — Real overlap (L4 does composite surface area, L7 surface area and volume). Left.

## essmath_2_7 — Essential Mathematics: Volume and Capacity (2) (2)
- **[structural]** container dimensions/capacities (L1 d=20 cm, 9.4/3.1/6.5 L vs L4/L8 d=28 cm, 18.47/6.16 L; L2 r=21,h=42) — L1 and L8 (both authoritative) disagree; L1 is internally consistent on d=20, L4/L8 on d=28, L2 on its own r=21/h=42 cone. Needs a module-level choice; not edited. Only L6's stray '141 litres in Lesson 4' was fixed to 18.5 L (L4's 18.47 L).
- **[structural]** opening diameter 20 vs 42 vs 28 cm — Same issue as above.

## gensci_1_3 — General Science: Nutrition in Animals (2) (2)
- **[science — needs rewrite]** How the body 'knows' which chemical to release: glands/regions (L3), sphincters (L6), genetic programming (L7), hormonal and neural signals (L8) — No single statement is wrong, but reconciling the partial explanations into the accepted hormonal + nervous control account needs new content across L3/L6/L7/L8.
- **[teaching choice]** Stomach enzymes (rennin in L3 only) — Rennin (milk-clotting, mainly in young mammals) is still listed in Kenyan syllabus gastric juice; whether to keep it for adults is a teacher's level-of-detail choice.

## math_2_4 — Mathematics: Surface Area and Volume of Solids (2) (2)
- **[structural]** Frustum volume never reaches 5,000 L (L3 ≈1.3 m³, L7 ≈3.3 m³) — Real: no lesson's frustum dimensions give 5,000 L, while L1/L9/L10/FE assert both tanks hold 5,000 L; L3's comparison sentence also needs the composite SA before L5 computes it. Needs a dataset redesign.
- **[teaching choice]** Base included in SA (L5) vs excluded (L10) — Including/excluding the base is a modelling choice stated per task (L10 tank sits on a platform); each lesson is self-consistent.

## phys_3_4 — Physics: Electrostatics (2) (2)
- **[structural]** Coulomb's Law taught in both L3 and L5; Q-V attributed to L5/6 — Real duplication (L3 and L5 both introduce Coulomb's Law; L7 and L8 both cover capacitor energy). Fixed L8's Lesson 5 pointers to Lessons 6–7. Also L6/L9 cite 'electric field (Lesson 4)' and 'potential difference (Lesson 5)', which no lesson teaches as such; left.
- **[teaching choice]** Why traders' hairs stood up (L1 hairs repel each other vs L2 attracted toward the cloud) and roof charge (L2 conduction vs L4/L5/L9 induction) — Hairs charged alike both repel each other and are attracted to the oppositely charged cloud; roof conduction vs induction are complementary. Teacher picks emphasis.

## bio_1_3 — Biology: Cell Biology (3) (1)
- **[structural]** structure of Lesson 4 cumulative model — L4 builds two 2D diagrams; L5 describes it as a 3-column chart. Real mismatch but needs rework of L5's model activity.

## bio_3_1 — Biology: Animal Nutrition (3) (1)
- **[structural]** L4 title mentions flamingo, content covers fish eagle/vulture/hornbill — Title/content mismatch; flamingo is covered in L5

## chem_1_5 — Chemistry: Periodicity (3) (1)
- **[teaching choice]** Group VII reactivity explained by electron affinity (L4) vs electronegativity/oxidising power (L7); argon as end of an electron-gain trend (L4) — Electron affinity vs electronegativity/oxidising power are compatible framings for Group VII reactivity; argon remark is a loose preview.

## gensci_1_2 — General Science: The Cell (3) (1)
- **[structural]** Plant cell EM in Lesson 2 / plant ultrastructure before L4 — L3 compares the animal cell with 'the plant cell from Lesson 2' though plant ultrastructure is taught in L4; fixed the explicit overclaims in L3 slo/sensemaking, the comparison framing in L3 overview remains (structural).

## gensci_1_5 — General Science: Respiration (3) (1)
- **[science — needs rewrite]** Which organisms/acid cause the uji's sourness — Correct fact: uji sourness is mainly lactic acid from lactic acid bacteria (yeast make ethanol + CO2, not lactic acid); but L4 claim sentence, pH activity and model are built on yeast as the souring agent, so fixing needs lesson redesign.

## bio_2_1 — Biology: Plant Nutrition (2) (1)
- **[structural]** Lesson 5 anchored on Elodea bubble data from Lesson 4 (Elodea is actually done in Lesson 7) — L5 is built throughout on bubble-count data learners have not yet collected (L4 is the starch test, Elodea is L7); cannot be fixed by renumbering since L7 is later. Needs lesson redesign or reorder.

## coremath_2_3 — Core Mathematics: Rotation (2) (1)
- **[science — needs rewrite]** Rotation: direct vs opposite congruence (L7 vs L8) — Correct fact: rotation produces DIRECT congruence (orientation preserved, image superimposable by sliding/turning in the plane). L7's whole activity, SLOs, chart and summary are built on 'rotation = opposite congruence'; needs author rewrite of L7.

## g11_bio_1_3 — Biology: Taxonomy II (2) (1)
- **[structural]** 4 which lesson introduces animal dichotomous keys — L6 already has learners write an animal key before L7 'introduces' it; overlap of content between lessons. Only L7's wrong 'last lesson' grouping reference edited.

## g11_bio_3_1 — Biology: Reproduction in Animals (2) (1)
- **[teaching choice]** Fish fertilisation (L1 vs L3/L7) — Most bony fish (e.g. tilapia) fertilise externally; L7 "frogs and fish (external)" is an acceptable simplification of L1, which notes shark/guppy exceptions.

## gensci_1_6 — General Science: Plant Growth and Development (2) (1)
- **[science — needs rewrite]** Why the stored seeds failed to germinate — L3 explain prompt (3), its formative-assessment target (gourd = No Water cup) and summary all attribute failure to lack of water, while the phenomenon says water and warmth were given; fixing requires redesigning the L3 prompt/assessment, not a wording swap.

## math_2_2 — Mathematics: Area of Polygons (2) (1)
- **[structural]** Shamba dimensions: L1 (48,35,52,40,37), L2 AB=120/AC=95/68 deg, L4 sub-plot 40/55/63, L7 (42,38,45,30,50) — Real: L1's sides are given 'e.g.' and later lessons (and FE Part 2) each use their own numbers with full worked calculations; reconciling needs one designed dataset, not spot edits.

## math_3_4 — Mathematics: Linear Motion (2) (1)
- **[structural]** L10 overtaking uses s = ut + ½at², not taught earlier — Real gap: the equation is not taught in L1–L9. Left.

## phys_3_2 — Physics: Current Electricity (2) (1)
- **[structural]** 4 L9 'Lesson 6 data tables' with power column — L6 parallel-circuit V/I data can take a P = VI column, but L9's claim about higher-resistance components at the same current does not fit parallel data; minor, not edited.

## phys_4_2 — Physics: Introduction to Space Physics (2) (1)
- **[science — needs rewrite]** Geomagnetic storm tidal anomaly in Mombasa (L9) vs Moon-driven tides (L6) — Geomagnetic storms do not raise tides; a sea-level anomaly would be meteorological storm surge, not astronomical tide. The 12 cm Mombasa anomaly is part of L9's case-study dataset and model choices, so removing it changes the activity.

## bio_1_1 — Biology: Cell Structure (1) (1)
- **[structural]** Cells involved in wound healing — L8 teaches a different five-cell set (incl. sperm, acknowledged as not involved) from L1/L10/L12's healing cells; curriculum-driven, not edited.

## coremath_2_5 — Core Mathematics: Area of Polygons (1) (1)
- **[structural]** 4 triangle heights measured directly (L4) vs hidden (L3) — L3 motivates the sine formula with an unmeasurable height but L4 measures all heights directly; design tension, not edited. L1 estimate vs L2 'numerical areas later' is not a contradiction.

## coremath_2_6 — Core Mathematics: Area of a Part of a Circle (1) (1)
- **[structural]** Radius of the Laikipia running diagram — Each lesson uses different pivot dimensions (L1 120/80, L2 40, L3 21, L4 70/40); no single dataset to align to, and dependent arithmetic throughout; not edited.

## coremath_2_8 — Core Mathematics: Vectors (1) (1)
- **[structural]** L4 vector d = (2,1) as Kencom-to-Westlands '8 km vector' — L4 is built throughout on d=(2,1) (3d, half d, -d); changing it would rewrite the lesson. Not edited.

## coremath_3_2 — Core Mathematics: Probability I (1) (1)
- **[structural]** L4 uses 'the Lesson 1 dice-rolling experiment results'; L1 only had a coin-toss experiment — No lesson in the module runs a two-dice rolling experiment (L1 coins, L3 dice grid only), so there is no lesson to repoint the reference to; L4 Task 1 needs rewording or a dice experiment added.

## essmath_2_2 — Essential Mathematics: Reflection (1) (1)
- **[science — needs rewrite]** L4 models side mirror as y-axis and rear-view mirror as x-axis reflection vs same plane-mirror principle elsewhere — Modelling the rear-view mirror as an x-axis (floor) reflection is physically odd but is the L4 activity design; changing it means changing the activity.

## essmath_2_6 — Essential Mathematics: Surface Area of Solids (1) (1)
- **[structural]** Which lesson covers cylinder/sphere/hemisphere/frustum; cylinder never taught (L1-L5) — No lesson teaches the cylinder surface area although the cylinder bucket is used in L3, L6 and L8 (and L3/L4 both derive the hemisphere). Wrong lesson pointers fixed as cross_reference: L1 placeholders and reflection, L3 storyline and reflection, L5 'Lessons 6-7'.

## g11_bio_1_1 — Biology: Taxonomy I (1) (1)
- **[structural]** Next-lesson questions regress (L6 asks about larger categories after L3-4 hierarchy) — Real but mild sequencing issue; L6's 'larger categories' lead-in to L7 kingdoms echoes the KICD key inquiry question. Not patched.

## g11_bio_2_3 — Biology: Excretion in Plants (1) (1)
- **[structural]** Guttation experiment set up in L2 (POE, bell jar, read Day 2) and set up again in L3 — L1->L2 reference is correct. L3 repeats a POE guttation setup (labelled an 'extension') and repeats L2's guttation-vs-transpiration exit ticket; real duplication, needs a design decision rather than a fact edit.

## gensci_1_4 — General Science: Transport in Plants (1) (1)
- **[teaching choice]** main force driving xylem water (root pressure L3 vs transpiration pull L7/L8) — Rooted seedling: root pressure contributes; L3 flags it as insufficient and L7/L8 add transpiration pull as main driver. Progressive model; teacher may foreground transpiration pull earlier.

## math_2_3 — Mathematics: Area of Part of a Circle (1) (1)
- **[structural]** When the sector area formula is taught: L1 Explain names and writes A = (θ/360°)πr², L2 formalises it, L3/L4 treat it as derived new in L4 — L1's Explain and model phases already name and apply the sector area formula although its overview says no formula is taught, and L4 derives it as new; sequencing issue, not edited (earlier pass missed L1's Explain phase).

## math_3_1 — Mathematics: Trigonometry I (1) (1)
- **[structural]** Special angles derived in L7 then re-derived as new in L8 — Real L7/L8 overlap; fixed only L8's wrong 'last lesson' reference

## math_3_3 — Mathematics: Vectors I (1) (1)
- **[structural]** Scale of L1 rough ferry model — L1's first rough model uses arrow lengths (4 and 2 squares) that do not match the scale it states; a naive first model, not edited.

## essmath_3_2 (1)
- **[science]** L7: 'compound probability of two independent events is always less than either' should be 'less than or equal to' — found by checker

## phys_1_5 (1)
- **[teaching choice]** L1 demo: a load on a corner within the stool's base should not tip it without a push — found by fixer
