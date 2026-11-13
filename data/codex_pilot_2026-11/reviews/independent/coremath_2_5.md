# Independent review: Core Mathematics 2.5 — Area of Polygons

Status: COMPLETE — corrections required before release.

Reviewer: Codex, with inherited agent settings. The exact runtime model identifier is not exposed to this reviewer; no exact model name is inferred. Review date: 2026-11-12. No paid API calls were made. Only this review file and scratch files under `/tmp` were written.

## Scope and independence

Read `reviews/REVIEW_BRIEF.md` first. Fresh pilot review used `sources/coremath_2_5.json`, the visually inspected `sources/coremath_2_5_source.png` (including enlarged competencies/values/PCI crop), `blueprints/coremath_2_5.json`, `materials/coremath_2_5.json`, all five supplied Core diagrams C1/C5/C9/C10/C12, `manuscripts/coremath_2_5.json`, `modules/coremath_2_5_data.js`, and all seven pilot DOCX types and their PDFs. Initial evidence was saved before baseline comparison. The author’s `internal_review.json`, `REPORT.md`, and other author evaluation/check files were not read at any stage.

Pilot output prefix below is `Codex_Core_Mathematics_Area_of_Polygons_`; DOCX files are in `outputs/v2/Core_Mathematics/SS2.5_Area_of_Polygons/` and PDFs in `outputs/PDF/`, relative to `data/codex_pilot_2026-11/`. Baseline is the current `generators/data/coremath_2_5_data.js`, compared after fresh pilot inspection, with four corresponding DOCX/data exports in repository `data/outputs/v2/Core_Mathematics/SS2.5_Area_of_Polygons/` and four PDFs in `data/outputs/v2/PDF/Core_Mathematics/SS2.5_Area_of_Polygons/`. This is sub-strand 2.5, not the older API pilot’s 2.4.

DOCX paragraphs/tables and PDF text were extracted locally. PyMuPDF/fitz was unavailable in the available Python environments, so equivalent local `pdftoppm` raster rendering and `view_image` inspection were used. Visually inspected pilot PDF pages: CBE Lesson Sequence 1, 3, 4, 49, 51; Compact Teacher Guide 2, 13; Student Materials 3, 4; Final Explanation 1, 2, 6; Final Explanation Teacher Key 1; Materials Teacher Key 6; Summary Table 2. Visually inspected baseline pages: CBE Lesson Sequence 1, 25; Final Explanation 6, 7; Final Explanation Teacher Key 1; Summary Table 1. Other PDF pages were text/structure checks, not a page-by-page visual proof. All source and material diagrams were viewed independently of these PDF samples. No visual clipping was confirmed in sampled pages; standard-guide row splitting and repeated resource blocks make it considerably longer than the compact guide. This sampling cannot certify every rendered page.

Severity: high = blocks reliable teaching/assessment or omits a required source outcome; medium = materially misleading wording, administration or evidence; low = provenance, packaging or presentation correction.

## Pilot findings

### P1 — Medium: the declared verbatim source transcription changes competencies and values

**Location/quote:** `sources/coremath_2_5.json`, `coreCompetencies`, `values`, `pcis`, and `transcription_policy`: “source wording retained, including apparent grammatical errors.” The same altered text appears in manuscript `unit`, generated module `UNIT`, and standard guide overview (PDF p. 1). Examples: “shapes ... that have the shapes of polygons”; “the learner researches and discuss the use of polygons”; “takes care when calculating”.

**Evidence:** The crop’s wording is different, including a substantive restriction to **regular** polygons, explicit use of **area**, plural “learners”, and Responsibility referring to identifying objects for calculation rather than merely taking care. Outcomes a–g and inquiry wording agree substantively with the crop; the source crop does not provide an official lesson allocation, correctly acknowledged by the pilot.

**Exact replacement transcription** (normalised line breaks only; apparent source grammar retained):

> Critical Thinking and Problem Solving: the learner uses trigonometric ratios to generate the formula for a triangle given two sides and an included angle.
>
> Creativity and Imagination: the learner identifies from the immediate environment objects in the shape of regular polygons and calculates their area.
>
> Learning to Learn: the learners research and discuss the use of the area of polygons in real-life situations.
>
> Patriotism: the learner uses the objects from the environment and takes care of the environment.
>
> Responsibility: the learner identifies objects from the immediate environment to use in calculating the area of regular polygons.
>
> Peace: the learner harmoniously discusses in groups and uses trigonometric ratios to generate the formula for the area of a triangle given two sides and an included angle.
>
> Environmental Education: the learner collects objects from the immediate environment to be used as learning materials for area of polygons.

**Correction/dependencies:** Correct the source JSON first, then manuscript unit metadata, generated JS/data and standard DOCX/PDF. If an edited pedagogical paraphrase is wanted, label it as a paraphrase alongside the exact source rather than claiming verbatim retention. No numeric answers change.

### P2 — Medium: C4 conflates a mixed-unit conversion coefficient with a dimensionless scale factor

**Location/quote:** Materials C4 teacher: “Linear scale 5 gives area scale 25, agreeing with 84×25.” Manuscript Lesson 4 Explain: “Explain why 5 times the side lengths produces 25 times the area.” This appears in Materials Teacher Key PDF p. 2 and both guides’ Lesson 4. The actual plan is “1 cm to 5 m”.

**Evidence/calculation:** The drawing sides 13, 14, 15 **cm** correspond to 65, 70, 75 **m**. In common units the linear factor is 500, so the area factor is 250,000: 84 cm² × 250,000 = 21,000,000 cm² = 2100 m². Alternatively the useful mixed-unit conversion is **25 m² per cm²**, not an unqualified dimensionless area factor 25. The numeric final area is correct; the scale explanation is not unit-safe as written.

**Correction/dependencies:** Say “each 1 cm² on the plan represents 25 m² on the plot; the dimensionless scale is 1:500.” Update C4 teacher explanation, Lesson 4 Explain and any corresponding summary wording in both guides and keys. Retain 13/14/15 cm and 2100 m². This is a conceptual units correction, not a failed numeric calculation.

### P3 — Medium: the independent assessment lesson gives conflicting collaboration instructions

**Location/quote:** Manuscript Lesson 12 Predict sensemaking: “Individual prediction, then paired comparison”; Observe sensemaking: “Evidence-first group work”; Model Building sensemaking: “Revise a shared model”. The adjacent instructions say “Complete the five assessment sections independently”, “keep the collected answers unchanged”, and “individual written transfer”. See Compact Teacher Guide PDF p. 13 and standard-guide Lesson 12 (including p. 49); generated JS `LESSONS[11].framework` carries all three contradictions.

**Evidence:** A teacher following the sensemaking column may allow peers to compare approaches immediately before or during a task whose claimed evidence is independent. These are substantive administration contradictions, not merely the conventional phase titles.

**Correction/dependencies:** Replace Lesson 12’s sensemaking strategies with individual reading, private working and individual transfer checks. State when, after collection, peer discussion is allowed. Change manuscript, generated module/data and both teacher guides. Preserve student dimensions and numeric keys.

### P4 — Medium: assessment resources and outcome claims need explicit limits

**Location/quote:** Lesson 12 Predict teacher moves: “Give only the Student Materials and student Final Explanation”; Lesson 12 inquiry: “Can I justify a method without being told its name?”; assessment section 1 supplies `A=ab sinθ/2`, section 4 supplies the congruent-triangle method, and section 5 requires subtraction and decomposition. Student Materials includes C1–C11 as well as C12: C3 supplies Heron’s formula, C7 supplies `A=nsr/2`, and C9/C10 explicitly scaffold the matching L-region methods.

**Evidence:** The seven-file package contains no C12-only handout. Giving the named full Student Materials makes this an individual, scaffolded/open-resource exercise. It can assess calculation and explanation, but cannot uniformly support an unprompted method-selection claim. In addition, assessment B (5,5,6) can validly be solved using Pythagoras: height √(25−9)=4, area 6×4/2=12 m², without demonstrating Heron; yet the rubric says “Apply Heron’s formula”. C3/C4 provide formative Heron evidence, so this is a limit on the final assessment evidence, not absence of teaching for outcome c.

**Correction/dependencies:** Make the resource policy explicit. Supply a C12-only sheet if unscaffolded selection is intended, or describe the assessment as individual explanation/application with permitted formulas. Require Heron working in section 2 if that specific technique must be established by the final assessment, while accepting alternative valid mathematics where the prompt permits it. Align the blueprint assessment claims, manuscript rubric/purpose and both guides. Merely changing numerical dimensions does not remove scaffolded-method cues. No teacher answer text was found in the pilot student Final Explanation or Student Materials.

### P5 — Medium: the source-linked environmental competencies are asserted but have no corresponding learner activity

**Location/quote:** Manuscript/unit PCI says learners “collect[] objects from the immediate environment”; competencies say learners identify local polygonal objects and research real-life uses. All lessons’ preparation is “Use paper tasks and calculators”; C1 is expressly an “Illustrative school-garden plan, not a surveyed site”, and C11 is a fictional garden. C7/C8 are supplied abstract regular polygons.

**Evidence:** The source crop suggests identifying regular polygon objects, using irregular polygon objects from the immediate environment, and research/discussion of uses. The pilot supplies substantial geometric tasks and a credible fictional cost model, but no task asks learners to identify/collect local polygon objects, calculate a selected object’s area or research a use. Reproducing the competency/PCI text in overview metadata does not create evidence for those behaviours. This does not invalidate the seven mathematical outcome activities.

**Correction/dependencies:** Add a modest, accessible local-object identification/measurement or supplied-object alternative, plus a short evidence-backed real-use research/discussion task; specify an observable product and safe collection constraints. Alternatively acknowledge the paper-model adaptation and limit claims of demonstrated competencies/PCI. Update blueprint lesson map, manuscript, materials and teacher guidance; recalculate pacing if activities are added. Local teachers should decide whether object collection itself is appropriate.

### P6 — Low: the Summary Table refers to an absent student version

**Location/quote:** `..._SummaryTable.docx`, instructions table 2 row 2 / PDF p. 1: “The student version has blank cells for students to complete after each lesson.” The supplied file is clearly “Teacher Reference (Pre-filled)”.

**Evidence:** Neither the seven pilot output types nor Student Materials contains a blank twelve-lesson student Summary Table. The prefilled file contains worked numeric answers and should not be substituted as the blank learner record.

**Correction/dependencies:** Supply a blank version, or change instructions to have learners draw/copy a blank four-column record in their books. Update packaging/instructions; no content mathematics changes. This is an availability finding, not a claim that a separate worksheet is always pedagogically necessary.

### P7 — Low: standard outputs contradict the pilot’s production provenance

**Location/quote:** Standard guide, Final Explanation, Final Explanation Teacher Key and Summary Table attribution: “lesson drafting and compilation assisted by AI (Claude, Anthropic)”; standard-guide footers also say “with AI assistance from Claude”. The standard-guide subtitle says “OpenAI-only evaluation”, and compact/material files say “OpenAI-only pilot”. Visual examples: standard guide p. 1/attribution, Final Explanation p. 6, Summary Table p. 2.

**Evidence:** The generated files make inconsistent authorship/tool claims. This appears to be inherited export boilerplate. The review cannot independently verify all historical drafting lineage, so the correction must describe the actual pilot/template roles accurately rather than inventing a model identity.

**Correction/dependencies:** Correct production attribution in pilot export configuration/template usage and rerender all affected DOCX/PDF; retain accurate template/framework credit. No manuscript mathematical edits are required. This finding does not establish which exact model produced the content.

## Pilot independent solution and coverage ledger

These recomputations include every exercise, not just the registered calculation array.

| Task | Independent result and condition |
|---|---|
| C1 | h = 8 sin30° = 4 m; A = 10×4/2 = 20 m². 40 m² incorrectly uses AC as perpendicular height. |
| C2 | sinθ=h/a ⇒ h=a sinθ ⇒ A=ab sinθ/2; 12×7 sin60°/2 = 21√3 = 36.37306696 cm². |
| C3 | 13+14>15, 13+15>14, 14+15>13; s=21 m; √(21×8×7×6)=84 m². For 3,4,8, 3+4<8: impossible, no triangular area. |
| C4 | Drawing sides 13,14,15 cm, s=21 cm, area84 cm²; plot s=105 m, √(105×40×35×30)=2100 m². Rounded field inputs imply an estimate; see P2 for scale units. |
| C5(a,b) | Parallelogram12×5=60 m²; trapezium(8+14)×4/2=44 m². Stated heights perpendicular; diagram labels match. |
| C6(a,b,c) | Rhombus four triangles each(5×4/2)=10 cm² ⇒40 cm²; kite12×7/2=42 cm²; general quadrilateral10×3/2+10×4/2=15+20=35 m². Two heights are on opposite sides, so add nonoverlapping triangle areas. |
| C7 | n triangles each sr/2 ⇒ nsr/2; hexagon6×4×2√3/2=24√3=41.56921938 cm². Given apothem agrees with regular hexagon side4. |
| C8 | Half-centre angles180/7=25.71428571° and22.5°; full centre angles51.42857143° and45°. r=(s/2)/tan(180°/n). Heptagon r=4.153042793 m, area58.142599104→58.1 m²; octagon r=4.828427125 m, area77.254833996→77.3 m². |
| C9 | 10×8−4×3=68 m²; decomposition10×5+6×3=68. Diagram missing corner dimensions agree; unlabelled top6 m and right5 m; perimeter would be36 m, a length rather than area. |
| C10 | Ordered coordinate region area8×3+5×3=39 m²; bounding8×6−3×3=39 m². Missing top-right3×3 region and all coordinate labels agree with diagram. |
| C11 | Separate beds20+68=88 m²; 88 m²×150 KES/m²=13,200 KES. Waste, measurement error, pack size and delivery are justified real-order limits; no percentage is specified. Resolved generated output correctly replaces the manuscript cost placeholder. |
| C12 / final1 | Using8 m base, h=6 sin30°=3 m; area12 m²; derivation as C2. Diagram6/8/30° agrees. |
| C12 / final2 | 5,5,6 satisfy triangle inequalities; s=8 m; √(8×3×3×2)=12 m². Alternative height4 m also gives12 m² (assessment limitation P4). |
| C12 / final3 | (6+10)×3/2=24 m², with perpendicular distance between parallel sides. Diagram agrees. |
| C12 / final4 | Printed apothems give heptagon7×2×2.076521/2=14.535647→14.5 m²; octagon8×2×2.414214/2=19.313712→19.3 m². They approximate correct side2 regular-polygon apothems2.076521397 and2.414213562. |
| C12 / final5 | 9×7−3×2=57 m²; decomposition9×5+6×2=57 m². Diagram missing corner3×2 agrees; derived boundary lengths6 and5 m. Real-order limits as C11. |

No incorrect pilot numeric answer or inconsistent diagram dimension was identified. Acute-angle scope is explicitly stated in C2 and in its teacher key; no obtuse-angle extension is supplied. Teacher judgement is needed on whether additional generality/practice is necessary for this class.

| Source outcome | Substantive pilot teaching | Observable evidence |
|---|---|---|
| a derive sine area rule | C2 altitude/sine substitution, L2 | Labelled derivation; final1 |
| b apply sine area rule | C1/C2, L1/L2; reused C11 | Height/area reasoning; final1 |
| c Heron | C3 triangle validity and Heron; C4 scale application | C3/C4 working; final2 subject to P4 |
| d quadrilaterals | C5 parallelogram/trapezium; C6 rhombus/kite/general quadrilateral | Diagrams/decomposition and three computed areas; final3 samples trapezium only |
| e regular heptagon/octagon | C7 regular-polygon centre decomposition; C8 apothem relation and both polygons | C8 working; final4 both polygons |
| f irregular polygons | C9 dimensional L-region; C10 coordinate L-region | Two decompositions; final5 |
| g real-life area uses | C1/C4 model limits; C11 cover-area/cost recommendation | Recommendation and limits; final5/transfer |

Cards C1–C12 all exist. C11’s dependencies C1 and C9 are supplied and explicitly separate; C12 plus the student Final Explanation supply all assessment data. Five diagrams are present and embedded in both materials DOCX files; C12 has diagrams A/B/C/E and textual D data, sufficient for learners to draw regular polygons. The teacher key is separate. Local paper, squared paper, ruler/set square/geometry tools for labelled/scale drawings, calculator or printed apothems, notebooks and two colours are needed; these ordinary consumables/tools are not downloadable artifacts. A concise consolidated preparation list would help, especially a compass or construction support for the13/14/15 cm scale triangle. No physical garden measurements are falsely claimed. No dangerous practical work is required by the pilot.

Standard export resource blocks contain local ARES search/resource hyperlinks. They are clearly marked “No closely matching...” or “Related topic: not an exact match”; essential local cards do not depend on those optional links. DOCX relationships were inspected; runtime access to `ares.local`, suitability of linked full content and ARES server installation were not tested. Thus external-resource availability is not certified. No absent essential C-card was found.

All twelve phase allocations sum to40 minutes; total480 minutes. Lessons1–11 each use4+16+10+4+6; final lesson4+30+2+1+3. The fixed8-minute individual work interval covers from one triangle to multi-shape derivation/plotting tasks; a classroom timing trial is still needed. The30-minute final requires six area results, derivation/explanations and sketches, so read/write pace and adjustments matter. This is not evidence of a proven impossible schedule.

## Baseline comparison — same rubric, reviewed after pilot

### B1 — High: source outcome coverage is missing

**Location/quote:** Baseline `UNIT.learningOutcomes` rewrites the seven source outcomes into six different outcomes. Heron’s formula is absent from the entire module. Lesson4 is “Heptagons — Decomposing the Kericho Land Plot” and uses an **irregular** heptagon. Lesson8 assigns a poster section for “regular polygons (heptagon, octagon)” without a worked regular-heptagon task.

**Evidence:** Source outcome c explicitly requires determining triangle area using Heron. Source e explicitly requires regular heptagon and octagon. Irregular heptagon triangulation does not establish regular-heptagon apothem/centre reasoning or provide practice in its area. Baseline teaches sine derivation/application, quadrilaterals, regular octagon, irregular/composite regions and application; it does not substantively teach or assess Heron or calculate a regular heptagon.

**Correction/dependencies:** Restore exact source outcomes with separately labelled author additions, add Heron and regular-heptagon activities/tasks/keys, and map evidence. Revise lesson plan, materials, final assessment, summary and all exports; recalculate actual teaching duration. Baseline competencies/values also differ substantially from source (e.g. Integrity/Respect/Unity replace Patriotism/Peace), so label additions and preserve the official source wording separately.

### B2 — High: essential diagrams/worksheets and two final-test tasks are not supplied

**Location/quote:** L1 Predict requires a printed scaled Kericho heptagon “scale1 cm:5 m”, labelled pegs, north arrow and scale bar; L1 Observe gives boundary sides18,22,15,20,25,17,19 m and refers to interior angles without giving them. L4/L7 repeatedly need the same scaled outline. L6 requires the Nakuru scale pentagon worksheet; L3 needs a derivation worksheet with tables “on the back”. L8 Model Building assessment Q4: “a scale diagram is provided”; Q5 asks a non-solar area without supplying any rectangle/parallelogram dimensions.

**Evidence:** All four baseline DOCX files have zero inline images; the module output directory contains only four DOCX and one data JSON, and its PDF folder four PDFs. No companion diagram/card/worksheet set was found in this module package. Seven side lengths alone do not uniquely determine a heptagon’s area; the unspecified interior angles cannot fix it. The pentagon can be reconstructed from later coordinates but is not supplied as the promised scale worksheet. L8 Q4 has no vertices/dimensions, and Q5 no dimensions, so neither numeric task can be solved from supplied data. The five-section Final Explanation export is a different assessment from the five questions described in L8 (B8).

**Correction/dependencies:** Supply validated, printable scale diagrams and reference answers/measurement tolerances for the actual shapes, or supply enough coordinates/dimensions and clear teacher preparation instructions. Supply Q4/Q5 data, mathematical tables if retained and blank tables/alternative notebook instructions. Recompute dependent areas, shares and assessment keys. A teacher-generated replacement outline is new design work, not a faithful recovery of the absent original shape.

### B3 — High: the generic sine derivation drops an altitude from a point already on the base

**Location/quote:** Baseline L3 Observe learnerExperience (generator line188): generic ABC with “a (opposite A), b (opposite B), c (opposite C)” then “draw the perpendicular height h from vertex A down to side b”.

**Evidence:** Under those labels b=AC. A lies on AC, so its perpendicular distance to that base is zero. For base b=AC and included angle C, drop from **B** to AC; in that right triangle h=a sinC, correctly yielding A=ab sinC/2. The numeric solar-panel answer14.84 m² remains correct.

**Correction/dependencies:** Change the altitude vertex to B and consistently show/label its foot in the promised worksheet. Update module, standard guide and any diagram/derivation key. This is not resolved by changing only the final formula, which is already correct.

### B4 — High: pentagon formative check instructs teachers to reject the correct two diagonals

**Location/quote:** Baseline L6 Observe formativeAssessment (generator line370; CBE PDF p.38): “exactly3 ... diagonals from vertex A — if a group draws only2 diagonals, their polygon is not fully triangulated; intervene immediately.”

**Evidence:** The task correctly asks for AC and AD in pentagon ABCDE: **two** diagonals, giving **three** triangles. From one vertex of a convex n-gon there are n−3 internal fan diagonals and n−2 triangles. Three diagonals from A to non-adjacent vertices of this pentagon are impossible without counting a boundary edge or drawing an invalid segment.

**Correction/dependencies:** Change to “two diagonals producing three nonoverlapping triangles” and update guide/checks; retain correct task and triangle count. Dependent learner diagnosis/remediation must not mark a correct construction wrong.

### B5 — High: Lesson7 composite-shape answer cues conflict with the specified dimensions

**Location/quote:** Baseline L7 Observe teacherMoves (line428; CBE PDF p.44): “156 m² for the L-shape and147 m² for the garden”. FormativeAssessment (line430; PDF p.45) first says156, then includes an editorial note computing174.

**Evidence/calculation:** Outer18×12 minus6×7 notch =216−42=**174 m²**. For a top-right notch, two decompositions are18×5+12×7=174 and12×12+6×5=174. Garden15×10 +5×4/2 −3×4 =150+10−12=**148 m²**. Neither156 nor147 matches the stated tasks. The note “correct value depends on ... worksheet dimensions” does not resolve dimensions already fixed in learner instructions.

**Correction/dependencies:** Replace incorrect cues with174/148 everywhere, remove unresolved editorial note, and validate any subsequently supplied diagrams against the specified dimensions. Correct module, guide, worksheets and dependent student feedback. If dimensions are intentionally changed, recompute both decompositions and keys together.

### B6 — High: baseline student assessment contains its own numeric answers

**Location/quote:** Baseline Final Explanation DOCX rubric table8, “Use of formulae and calculation accuracy” excellent cell; PDF p.6: “calculates14.84 m²,43.46 m² and48 m²”.

**Evidence:** Those are the exact numeric results requested in final sections2c,3b and3d. They appear in the **student** document as well as the teacher key. Visual inspection confirms the leak, not merely data-field presence. An open formula poster does not justify printing assessed numeric answers beside the questions.

**Correction/dependencies:** Keep answers in the teacher key only; use student rubric language describing working, accuracy, units and reasoning without results. Regenerate the student DOCX/PDF and any distributable copies. The pilot’s generic student rubric does not contain this particular numeric leakage.

### B7 — Medium: unrestricted fan triangulation claim is false for concave polygons

**Location/quote:** Baseline Summary L6 learned: “Any irregular polygon ... by drawing diagonals from one reference vertex to all non-adjacent vertices”; final section5 exemplar/rubric repeats the fan rule for any polygon; L4/other lessons make similar universal claims.

**Evidence/counterexample:** The simple concave L-hexagon (0,0),(4,0),(4,1),(1,1),(1,4),(0,4) has area7. The segment from vertex(4,0) to non-adjacent(1,4) passes through(2.5,2), outside that polygon. A fan from an arbitrary vertex therefore can cross exterior space. The theorem that a simple polygon admits n−2 triangles is distinct from the claim that every vertex supplies such a fan.

**Correction/dependencies:** Restrict one-vertex fan statements/examples to convex polygons (or a verified visible-from-that-vertex configuration); teach valid interior diagonals/ear triangulation or rectangle decomposition for concave polygons. Update source-independent claims in lessons, summary, key and rubric. Supplied drawings must be checked once provided. Pilot’s concave L-regions use valid rectangle decompositions and avoid this error.

### B8 — Medium: delivered final assessment differs from the lesson’s planned assessment and rubric exports are stale

**Location/quote:** L8 Model Building describes Q1 base48/height35 triangle; Q2 trapezium22/14/height9; Q3 octagon6/apothem7.24; Q4 hexagon split between2 owners; Q5 rectangular non-solar region. The exported Final Explanation instead asks five sections about Kericho explanations, the familiar5/7/58° panel, side3 octagon and a3 cm²→48 m² conversion. Baseline exported data has schema1.0.0 and lacks the four `belowExpectations` entries present in current generator schema1.1.0; DOCX rubric has Excellent/Proficient/Developing(1–2), not the generator’s four descriptors.

**Evidence:** These are different questions/benchmarks and different rubric structures, not merely rendering variations. L8’s numeric benchmarks840/162/130.32 cannot mark the delivered final paper. The current generator and delivered JSON differ in schema, resourceLinks additions and missing belowExpectations keys; instructional content otherwise agrees.

**Correction/dependencies:** Choose the intended assessment, align L8 tasks, supplied data, final student paper, teacher key and benchmarks; regenerate all baseline exports using the corrected current schema. Retain an explicitly stated resource policy (baseline permits the Toolkit poster). Recheck B2 and B6 during reconciliation. Do not silently treat the old exports as a proof of the current renderer.

### B9 — Medium: baseline duration metadata understates the lesson records

**Location/quote:** `UNIT.totalDuration`: “8 lessons ×40 minutes =320 minutes total”, CBE PDF p.1. Lesson durations are80,80,40,80,80,80,80,80 minutes.

**Evidence/calculation:** Actual sum=7×80+40=**600 minutes**, i.e.15 forty-minute periods. Pilot=12×40=480 minutes. Lesson record counts8 vs12 do not measure available teaching time. The source crop states no official count, so neither author’s allocation is an official KICD requirement.

**Correction/dependencies:** Fix unit metadata and explicitly name double periods/split points; reconcile phase/presentation time with class group count. Update outputs and any pilot comparison/cost denominator. No cost or quality superiority follows solely from duration differences.

### B10 — Medium: rhombus/kite explanation gives the wrong reason for their shared area rule

**Location/quote:** L2 Explain learnerExperience: rhombus “each diagonal halves the other ... and kite (same logic as rhombus)”; baseline final2 exemplar and Summary L2 learned: the shapes share a formula “because each is fixed by its two diagonals” / “fully determined by their two diagonals”.

**Evidence:** In a general kite only its symmetry diagonal bisects the other; the two diagonals need not bisect each other. Fixed lengths do not determine a unique kite: vertices(0,2),(3,0),(0,−8),(−3,0) and(0,3),(3,0),(0,−7),(−3,0) have the same diagonal lengths10 and6 but different shapes. Both have area30 because the diagonals are perpendicular. Summing the four right-triangle areas yields half the diagonal product without requiring mutual bisection.

**Correction/dependencies:** State perpendicular diagonals as the shared condition and show the kite’s unequal diagonal segments if needed. Correct L2 derivation, final teacher exemplar and Summary Table. Numeric diagonal-product answers remain correct.

### B11 — Low: numerical rounding and lesson-forward references are inconsistent

**Location/quote:** L5 Explain says `A=2(1+1.414)×9=...43.45 m²`, and repeated L5 checkpoints/model cite43.45; final3 exemplar instead43.46 to2 decimal places. L3 DQB teacherMoves says “Lessons4 and5 — the Sine Rule and Cosine Rule”; those lessons are heptagon and octagon decomposition. L2 DQB previews Lesson3 as irregular hexagons/heptagons, whereas L3 is sine area.

**Evidence:** Exact side3 octagon area18(1+√2)=43.45584412, correctly rounding to43.46. Using truncated√2=1.414 produces43.452, which rounds43.45, so precision was lost before final rounding. The forward references contradict the module’s own lesson titles/tasks.

**Correction/dependencies:** Retain calculator precision through final rounding or explicitly identify the rough approximation; unify numeric exemplars. Replace the forward references with actual next-lesson content. Module and guide/model wording need revision; the766-tile/65,110 KES result can remain under its stated round-up-then-add10% convention. The “always add10%” construction claim should instead be an explicit problem assumption unless supported for the actual ordering context; no universal Kenya construction rule was established by this review.

## Baseline independent solution ledger and unresolved data

| Task | Independent result / limit |
|---|---|
| L1 triangle cut-outs | 8×6/2=24 cm²;10×5/2=25 cm². Heptagon area and actual equal-share boundary cannot be solved from seven side lengths alone or absent outline. |
| L2 rank/areas | A parallelogram8×5=40 cm²; B rhombus10×6/2=30; C trapezium(9+5)×4/2=28; D kite10×6/2=30. Rank A > B=D > C. |
| L2 applications | Pen24×15=360 m²; terrace(3.6+2.2)×1.4/2=4.06 m². |
| L3 solar | 5×7 sin58°/2=14.84084168→14.84 m²; four-decimal table sin58°=.8480 gives14.8400, same2dp. Correct altitude from B if base b=AC. |
| L3 maize/interior | 12×9 sin72°/2=51.35705188→51.36 m²;8.4×11.2 sin65°/2=42.63271830→42.63 m². These provided answers agree. |
| L4 triangles/scales/shares | Heptagon n−2=5 triangles via valid triangulation; convex fan needs4 diagonals. 1 cm:5 m implies1 cm²:25 m². Hypothetical1380/3=460 and1420/3=473⅓ m²; estimate1400/3=466⅔ m². Actual drawing/area unavailable. |
| L5 centre pattern | Triangle/square/hexagon/octagon centre fans have3/4/6/8 triangles and angles120°/90°/60°/45°. Octagon side3 true apothem3.621320344 m; each triangle5.431980515 m²; total43.45584412→43.46 m². Measured3.62 gives5.43 per triangle and43.44 total, reasonably approximate43.5 to1dp. |
| L5 tiling/cost | Tile area.25×.25=.0625 m². True area/.0625=695.29350596; base count ceil=696. Stated convention adds10% to696:765.6 then ceil=766; cost766×85=65,110 KES. Adding allowance before a single final round-up would instead giveceil764.82285656=765; conventions must be explicit, not conflated. Scale drawing side3/.5=6 cm, overall octagon span6(1+√2)=14.4853 cm. |
| L6 coordinate extension | A(0,0),B(3,0),C(5,2),D(4,5),E(1,4). Fan ABC/ACD/ADE areas3,8.5,5.5 cm²; total17 cm². Shoelace forward47, reverse13 ⇒(47−13)/2=17 cm²;×16=272 m².1 cm:4 m gives area coefficient16 m²/cm²; scale ratio1:400. |
| L6 further estimate | Five triangle areas averaging280 m² imply1400 m². Hypothetical ruler correction3.8→3.2 cm has no named triangle/base and cannot be validated against unspecified worksheet; do not hard-code actual group data. |
| L7 composite | L=174 m², garden=148 m² as B5. Kericho total/share geometry remains underdetermined. A hypothetical1416 total would give472 m² per family. |
| L8 in-lesson Q1–Q3 | 48×35/2=840 m²; (22+14)×9/2=162 m²;8×6×7.24/2=173.76 m² — **the stated Q3 benchmark130.32 m² is wrong** (additional finding below). |
| L8 Q4–Q5 | Hexagon data/diagram absent; non-solar rectangle/parallelogram dimensions absent. Cannot compute justified numeric answers. |
| Exported final sections1–5 | Valid triangulation explanation subject to concavity condition; quadrilateral rules subject to B10; solar14.84 m²; octagon43.46 m²;3 cm²×16=48 m²; each-family share=actual total/3, but no supplied actual total. Familiar examples are reused rather than novel assessment dimensions. |

### B12 — High: final in-lesson octagon benchmark is arithmetically wrong

**Location/quote:** Baseline L8 Model Building learnerExperience: “regular octagon with side6 m and apothem7.24 m”; formativeAssessment: “Q3≈130.32 m²”.

**Evidence/calculation:** A=nsr/2=8×6×7.24/2=**173.76 m²**.130.32 is6×6×7.24/2, apparently using six triangles for an octagon. True side6 apothem is7.242640687 m, consistent with rounded7.24; the supplied dimensions are not the problem.

**Correction/dependencies:** Replace benchmark with173.76 m² for supplied apothem, or≈173.82 m² only if learners derive and retain the true apothem. Update module, guide and intended final key after B8 assessment reconciliation. This task is not present in the delivered five-section final export; do not use its benchmark to mark that different paper.

## Comparison and classroom judgement

The pilot provides all seven named outcome areas with concrete local cards and independent numeric keys; its numeric examples and five diagrams checked out. It still needs the source transcription, scale explanation, assessment administration/evidence, competency-activity alignment and packaging/provenance corrections above. The baseline contains richer scripted contextual dialogue and planned physical measurement/dissection, but cannot be taught as a complete supplied package without its missing diagrams and needs substantial content/key corrections. This is a scoped content review, not evidence that one authoring system is universally better or cheaper.

The baseline’s actual600 minutes include physical cut-out work, presentations and more extended community-land framing; the pilot’s480 minutes use paper models and shorter fixed routines. The baseline’s displayed320-minute allocation is erroneous. Both source coverage and task form differ. Fewer findings, fewer pages, fewer lesson records or different minutes alone cannot establish learning effectiveness, production cost or savings.

Classroom judgement remains required for prerequisite sine/tangent and scale knowledge, drawing-tool access, scientific-calculator availability, support for language/reading/writing needs, the30-minute pilot final assessment, how many groups can present within available time, and whether a local-object/research activity is needed to substantiate competency/PCI claims. The paper pilot has straightforward safety needs; baseline scissors require ordinary safe handling and measurement/dissection supervision. Assertions about actual Kenyan organisations, historical family narratives, standard construction wastage, KNEC table requirements or actual local sites were not established from supplied primary evidence; use clearly fictional teaching scenarios and explicit assumptions, or verify those claims before publication. No claim of school validation or complete external-link verification is made.
