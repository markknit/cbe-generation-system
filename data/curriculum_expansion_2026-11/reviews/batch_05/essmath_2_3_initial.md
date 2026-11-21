# Independent initial content review — Essential Mathematics 2.3 Trigonometry

**HOLD — one confirmed outcome-traceability issue, EM23-C1.** No mathematical answer, source-scope, clinometer-rule or current five-Word propagation defect was confirmed. The hold is local to the Lesson 7/F7 mapping described below, not missing overall complementary-ratio coverage.

Current content fingerprint: `c360a40717d4d62dc4e9307f3ace2610405ee169b1867040d73ae5e64331d9b3`.

## Source/materials-first review and binding

I inspected actual printed pp14–15 pixels before reviewing all 12 material cards and independently solving their tasks. I then read all 12 lessons/phase cells and summaries, the complete blueprint and assessment/rubric links, four final sections/exemplars and four rubric criteria, and checked all five actual draft Word companions. No author self-review was used. No input, shared code, output or acceptance record was edited, and no pipeline/render operation was run.

All five outcomes, the inquiry question, competencies, Love value and Self-esteem PCI agree with the complete source continuation. The source crop exactly matches the same rectangle from the prior independent fresh 150 dpi PDF render. Source PDF SHA-256: `7459a495859a658a42704799f848e27400fc3b10083b42d7fe8e6364ebf82e73`; crop SHA-256: `c460b179d7f96af1cabbec503c8cf7ebb241aaaa6c27f49b17f7bd4f8fcbf569`.

The heading focuses on sine/cosine, but outcome b explicitly requires tangent: the draft correctly includes all three acute right-triangle ratios. The p15 project explicitly requires making and using a simple clinometer for elevation/depression; actual making/calibration and both-direction use are separately scheduled in F8/F9. Digital-resource experience is present in F10, with actual digital action distinguished from printed/source reasoning. No allocation is printed; 12 × 40 = 480 minutes is identified as teaching design, with all phase totals 40. No non-right-triangle rules or inverse-angle syllabus is introduced. Degree/radian distinction is only an input-mode caution.

[Binding/check evidence](evidence/essmath_2_3_initial/binding.json) contains canonical/source/verification hashes, the fingerprint, exact five Word hashes and their media inventories. [Geometry/semantic evidence](evidence/essmath_2_3_initial/geometry_and_semantics.json) records independent complement values, theoretical plumb examples, actual TR1 media/aspect checks and the current mapping issue. Full extracted actual Word text and the [reproducible checker](evidence/essmath_2_3_initial/check.py) are saved beside them.

## Confirmed issue EM23-C1

Lesson 7, its blueprint lesson-map entry, formative F7 and F7 assessment-map entry all claim outcome **c: relate sines and cosines of complementary angles**. TR7 and every Lesson 7 phase instead ask about equality of depression/elevation angles under parallel horizontals and solving horizontal/sightline lengths with tangent/sine. They do not ask learners to relate sine and cosine of complementary angles. Alternate-interior-angle equality is not itself the complementary sine/cosine relationship.

Either remove c consistently from these Lesson 7/F7 mappings, or explicitly elicit the complementary sine/cosine relation there. Outcome c remains properly taught in Lesson 4/TR4 and assessed in final I2, so narrowing this local claim does not remove required overall coverage. F10 permits checking a ratio or a complementary relation; that optional choice should not by itself certify that every learner has demonstrated c, which is separately assessed by I2.

## Independent solutions — every material and final task

| Task | Independently checked answer/reason |
|---|---|
| TR1 | Right angle at B; AC=5 cm is hypotenuse. Relative to A: opposite BC=3, adjacent leg AB=4. Relative to C: opposite AB=4, adjacent leg BC=3. The hypotenuse stays fixed; opposite/adjacent swap. |
| TR2 | A: sin=3/5=0.6, cos=4/5=0.8, tan=3/4=0.75. C: sin=4/5=0.8, cos=3/5=0.6, tan=4/3≈1.3333. Scaled 6–8–10 triangle gives the same six ratios; common scale and length units cancel. Tangent can exceed 1; acute sine/cosine lie strictly between 0 and 1. |
| TR3 | sin30°=cos60°=0.5000; cos30°=sin60°≈0.8660; tan45°=1.0000. With hypotenuse 10 cm, opposite=5 cm and adjacent=5√3≈8.6603 cm. The longest-side check holds. |
| TR4 | Complement table: (20°,70°) gives sin20=cos70≈0.3420 and cos20=sin70≈0.9397; (30°,60°) gives 0.5000/0.8660; (40°,50°) gives sin40=cos50≈0.6428 and cos40=sin50≈0.7660. Right-triangle angle sum gives A+C=90° and exchanged legs prove exact identities; rounded matches alone are not proof. Same-angle sin/cos equality is not general (within acute domain only at 45°). |
| TR5a | Opposite rise=12 tan30°=4√3≈6.93 m. |
| TR5b | Hypotenuse=6/sin60°=4√3≈6.93 m, greater than the 6 m opposite leg. |
| TR5c | Hypotenuse=5/cos45°=5√2≈7.07 m. |
| TR6 | Rise=12 tan30°=4√3≈6.9282 m; total=1.5+4√3≈8.4282→8.43 m. Requires a vertical pole, horizontal baseline and common ground datum; horizontal distance is not sightline length. |
| TR7 | Horizontal separation=9/tan30°=9√3≈15.59 m; sightline=9/sin30°=18 m. Depression equals target elevation by parallel horizontals/alternate interior angles. It is measured from horizontal, not vertical. |
| TR8 | With tube along baseline, plumb through protractor centre and baseline horizontal, p=90°. For acute up/down aim, either scale may read 90°−θ or 90°+θ; θ=abs(90°−p). At 30°, 60°/120° both give 30°. Direction must be recorded separately; the absolute magnitude cannot recover it. An incorrectly attached pivot/baseline is not cured by blindly applying the formula. |
| TR9 | Actual readings have no predetermined numeric answer. Each direction needs three actual raw plumb readings, up/down label, derived magnitude and repeat spread after calibration. For height estimates, rise/drop=d tanθ relative to a known sight datum; do not replace d with diagonal sightline distance or invent baseline/target data. Unperformed actions/readings remain NOT OBSERVED. |
| TR10 | A valid example is conditional indoor sight-height estimation using horizontal distance and a correct reference datum. Tilt, baseline uncertainty, parallax/plumb motion, scale reading and calibration can limit it. A checked source claim may use the exact TR1 side ratios or TR4 identities. Actual digital use and project action are separately evidenced. |
| TR11 | Hypotenuse fixed opposite right angle; tan=opposite/adjacent leg; sin20°=cos70°, not cos20°; d tanθ gives rise/drop from the sight horizontal under stated geometry, so total height needs the correct datum/eye-height adjustment. A safe implication must follow from these conditions rather than requiring hazardous access. |
| TR12 / final A | Right angle Y; hypotenuse XZ=13. X: opposite YZ=5, adjacent XY=12, ratios 5/13,12/13,5/12. Z: opposite XY=12, adjacent YZ=5, ratios 12/13,5/13,12/5=2.4. X+Z=90°, so sinX=cosZ and cosX=sinZ. Units cancel. |
| Final degree benchmarks | sin30°=cos60°=1/2; tan45°=1. Correct mode is required. Complement relation is exact geometrically, not proved solely by displayed decimal agreement. |
| TR12 / final B | Rise=8 tan45°=8 m; total pole height=8+1.4=9.4 m. Level-ground/vertical-pole/common-datum assumptions are relevant. |
| TR12 / final C | Horizontal separation=6/tan30°=6√3≈10.39 m; sightline=6/sin30°=12 m. Given 6 m is already vertical sight-to-target difference; do not add eye height again. Parallel horizontals justify depression/elevation equality. |
| Final application/project evidence | A useful application needs correct known quantities/reference and a limit. Calibration/magnitude/direction explanation matches TR8. Naming assembly/calibration and both-direction sight/read/record/check evidence is knowledge about performance verification; a written final answer does not itself certify making or use. |

All **23 registered checks** agree with independently established exact fractions/radicals/lengths: four A/C ratios, five degree benchmarks, two 10 cm legs, three TR5 lengths, pole height, two 9 m depression lengths, three final X ratios, final pole height and two final depression lengths. The check uses independent fraction/radical expectations rather than accepting the compiler's arithmetic result as semantic proof. Complement-table values and all nonregistered counterpart ratios are covered above.

## TR1 actual diagram and draft Word propagation

I visually inspected the actual 1200 × 650 PNG. A is left, B lower-right with the right-angle marker, C above B; AB is labelled 4 cm, BC 3 cm and AC 5 cm. Labels and mathematical-model caption are readable and unambiguous. The drawn legs are proportioned 4:3; no measured-object claim is made. Both Student Materials and Materials Teacher Key embed its exact original bytes at preserved 1200:650 aspect; Assessment Materials contains no diagram/answer image. TR1 SHA-256: `6f8a6f65e7cb834b815c50e391ada03ebfe24fb1b7d3fd27907dd1999680db00`.

All **460/460 actual five-Word propagation/structural checks PASS**. The compact guide includes all five source outcomes and all current lesson titles/purposes/knowledge/safety/reflection text and 240 phase cells. Student Materials includes TR1–TR11 tasks in full, without teacher keys or the actual final TR12 task/data. Materials Teacher Key includes all 12 tasks/keys and the original diagram. Assessment Materials contains final-only TR12 student data with its answer absent. Student Summary Table has 12 correct lesson labels and all 36 response cells blank. All five files carry ChatGPT/Codex/OpenAI attribution. Structural preflight passes but does not detect C1's unsupported local outcome tag.

This is actual Word-package text/table/media verification, not paginated final Word/PDF layout acceptance. No final rendering was run.

## Project honesty, assessment and classroom limits

F8 requires actual named assembly/calibration contributions, retained instrument and real calibration readings. F9 requires actual elevation **and** depression use, three readings each, named sight/read/record/check evidence, comparison of variation and explicit NOT OBSERVED treatment of missed actions. The source's collaborative project need not become an unsupported claim that every learner independently built a whole instrument. Individual scope must still be recorded honestly. Prepared accessible cuts/holes, short strings, blunt secured weights, stable clean instruments and fixed safe indoor targets support the plan. No sun/bright-light/people sighting, road/height access or movement while sighting is directed.

The final four rubric criteria align with side/ratio reasoning, complements/mode, paper elevation/depression models and explanation of applications/performance-evidence requirements. They must be interpreted with the explicit blueprint/key limitation that written responses do not establish actual making/use or digital action. Diagram, ratio, unit and assumption evidence is requested. Independent final conditions withhold teaching cards, peers, hints, media and keys. No engineering/field-certification or persistent self-esteem inference is supported by paper results.

Teacher confirmation remains necessary for target geometry, usable protractor scale/pivot/sightline alignment, horizontal/30° calibration reference, baseline/datum measurements, supervision, tool/target capacity, accessible action opportunities and 40-minute project/final pacing. These are disclosed classroom constraints rather than confirmed content defects. Actual action evidence is not yet available and is not fabricated by this review.

**Release remains HOLD pending correction and independent recheck of EM23-C1.** Preserve this exact initial report and fingerprint; a correction should receive separate scoped evidence.
