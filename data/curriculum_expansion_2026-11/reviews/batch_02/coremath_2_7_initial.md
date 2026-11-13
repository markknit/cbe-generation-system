# Independent initial review — Core Mathematics2.7

Status: IN PROGRESS, incremental materials/source review only. Whole-unit acceptance withheld: manuscript/blueprint/final assessment/actual outputs pending. Root central usage18% at2026-11-13T09:23:09UTC exit0, no pause. No content edits, author self-review, baseline audit or paid calls.

## Incremental source/material findings checkpoint

Read full source JSON and supplied pixels (printed28–30), complete14-card bank/solutions and viewed all six supplied PNGs SV1/2/3/4/6/14. Original PDF crop independently re-rendered to `/tmp/core27_review/source_original.png`; original-PDF visual comparison and enlarged source checks continue. Registry is empty as expected, so independent task calculations were done first: all stated numeric answers agree, including similarity, contact-face subtraction, holes and capacities.

**C27-1 — Medium, confirmed geometric error: SV1 triangular-prism diagram is not a foldable net as labelled.**

- Location: `materials/diagrams/SV1.png`, right-hand “right-triangular prism net”; top rectangle10×3, middle10×4, bottom10×5. Both attached triangles have their3cm leg extending from the **bottom** end of the4cm attachment.
- Evidence: at the middle strip’s upper boundary, each triangle’s free incident edge is the5cm hypotenuse, but the neighbouring top panel has width3. At the lower boundary, each triangle’s free edge is3, but its neighbouring bottom panel has width5. When folded, end edges cannot join along equal lengths. All five face areas remain correct; a face inventory is acceptable, but the picture specifically claims to be a net.
- Correction: mirror both end triangles vertically so their3cm edges meet the top10×3 strip, or swap top/bottom rectangle widths and labels so5 meets5 and3 meets3. Retain middle10×4 and area132cm². Inspect revised PNG and later embedded/printed net in focused recheck.
- Dependencies: SV1 diagram and all later materials exports containing it; any model-construction/net evidence. Rectangular-prism net in the same PNG is valid and needs no mathematical change.

Whole-unit verdict remains withheld. Parent informed immediately so this can be corrected before rendering; preserve this initial finding even after correction.

## Independent solution ledger — materials-first stage

All14 card tasks have been independently solved before any calculation registry was available. Unless noted, lengths arecm, surface areacm² and volumecm³. No keyed numeric answer disagreed with recomputation; C27-1 concerns net topology, not face-area arithmetic.

| Card | Independent results and geometric checks |
|---|---|
| SV1 | Box faces2×40+2×24+2×15=158. Triangular end3×4/2=6 each; lateral10(3+4+5)=120, total132. Six rectangular-box faces form valid shown net. Triangular face inventory correct; attached edge order in PNG invalid as C27-1. |
| SV2 | Central triangle3–4–5 gives face altitude5. Four faces4×(6×5/2)=60 plus base36=96. Apex-to-corner edge√(4²+3²+3²)=√34≈5.831, not5. Shown square-plus-four-triangles net labels face altitude correctly. |
| SV3 | Cone curvedπ×3×5=15π≈47.124; total+9π=24π≈75.398. Cylinder curved2π×3×4=24π, total+18π=42π≈131.947. Cone net angle360×3/5=216°; arc216/360×2π5=6π matches base circumference, sector area15π. Cylinder side rectangle4 by6π. PNG geometry agrees. |
| SV4 | Similarity ratio removed/original2/5 gives original H20/3,removed8/3, difference4; slants25/3 and10/3,difference5. Frustum slant√(4²+(5−2)²)=5. Curvedπ[5×25/3−2×10/3]=35π≈109.956; ends29π;total64π≈201.062. Actual unrolled annular-sector radii25/3,10/3 and216° would give same35π; an ordinary trapezium is only the axial section. PNG correctly identifies axial section. |
| SV5 | Sphere r2 area16π≈50.265; hemisphere curved8π, closed total12π. r4 sphere64π≈201.062, area scale4. Orange-peel strips are approximate, not an exact distortion-free planar unfolding. No real sphere cutting required. |
| SV6 | Big box2(48+32+24)=208;small2(4+6+6)=32. Shared2×2 face area4 occurs twice in standalone surface sum:208+32−8=232 exposed. Cylinder/hemisphere:side24π+hemisphere18π+bottom9π=51π≈160.221; joining disks excluded. Through-hole cube (normal6cm hole length)216−2π+12π=216+10π≈247.416; new exposed wall12π. |
| SV7 | Triangular-prism volume6×10=60, not132 surface units. Internal box20×15×10=3000cm³=3L. Cylinder9π×4=36π≈113.097. External dimensions do not determine usable thick-wall capacity. |
| SV8 | Cone(1/3)9π×4=12π≈37.699 versus matching cylinder36π. Pyramid(1/3)36×4=48 versus matching prism144. Printed fallback75.3/25.1=3. The illustrative capacities are separate supplied comparison data, not claimed exact measurements of the earlier3/4cm cone. One comparison supports a model, not a universal proof. |
| SV9 | Original/removed cone volumes(π/3)25×20/3=500π/9 and(π/3)4×8/3=32π/9;difference468π/9=52π≈163.363. Formula(4π/3)(25+10+4)=52π. Cylinder bounds16π<52π<100π. Constant-annulus extrusion gives84π, wrong solid. |
| SV10 | Sphere r2 volume32π/3≈33.510; hemisphere16π/3≈16.755. r4 sphere256π/3≈268.083; volume factor8 versus surface factor4. Internal shell radius, not outer radius alone, governs capacity. |
| SV11 | Joined boxes192+12=204. Cylinder/hemisphere36π+18π=54π≈169.646. Cube minus full6cm cylindrical cavity216−6π≈197.150. Zero-thickness joining face has no3D volume to subtract. |
| SV12 | Open cylinder side80π+bottom16π=96π≈301.593. Capacity160π≈502.655cm³/mL≈0.503L. Model cost0.5×96π=48π≈150.796KES or150.80KES to2dp. Lid would add16π≈50.265cm² and8π≈25.133KES. Price is explicit fictional datum; no invented waste/market charge needed. |
| SV13 | AuditA false:cone slant5 gives curved15π, while12π is volume coefficient. B false:volume needs perpendicular height. C false:contact area does not subtract from volume when only touching. Chosen model has no universal key; enough dimensions plus stated internal/external/exposed assumptions are necessary. |
| SV14 F | h4,R−r3 imply s5. Similarity gives original H8/removed4, slants10/5. Curved45π plus end disks36π+9π=90π≈282.743; volume(4π/3)(36+18+9)=84π≈263.894. |
| SV14 G | Cylinder side24π + hemisphere8π + bottom4π=36π≈113.097 exposed; internal join disks excluded. Volume24π+16π/3=88π/3≈92.153. PNG agrees with r2 and cylinderh6. |
| SV14 H | Internal25×12×8=2400cm³=2.4L. External-only dimensions would not establish capacity; no unique real price/waste response is supplied or needed. |

## Source fidelity and current limits

Independently viewed original local PDF crop at150dpi including printed28–30, matching supplied source pixels. Mathematical outcomes a–e, two inquiry questions and literal competencies/values/PCI agree substantively with source JSON. The two nearly identical cone/cylinder competency bullets are present in the source and should not be “repaired” merely for duplication. No lesson count is printed; planned14 must remain explicitly an authoring decision, not an official source allocation.

The source suggests nets/models, composite components, matching cone/cylinder filling, appropriate local containers and digital resources. Current bank addresses nets/face inventories, correct internal/external surface distinctions, capacity, optional actual vessel filling, and safe local/drawn models. Sphere’s lack of an exact planar net is correctly acknowledged rather than falsely supplied. Paper/drawing fallback cannot establish physical making/measuring/filling, and keys explicitly require honest observed/not-observed records. Optional filling needs genuinely matching **internal** cone/cylinder base/height, watertight nonbreakable vessels, precheck/spill tray and no electricity exposure; the printed ratio is a safe access alternative, not empirical evidence.

Teacher judgement/pending full-unit review: feasibility of finding matching cone/cylinder vessels, access to tools/calculators and drawing alternatives, time for net construction/similarity reasoning, safe scissors/compass use and internal dimension measurement. SV6’s optional hole wording would benefit from saying its axis is perpendicular to the opposite faces (key assumes length6); SV11 explicitly supplies full6cm length. This is currently a clarity suggestion, not a separate confirmed wrong answer. Source digital-device experience should be either supplied or transparently adapted; printed analysis alone must not be credited as digital competence.

**Pending before whole-unit verdict:** full14-lesson manuscript, canonical final prompts/exemplars/rubric, blueprint coverage/pacing/isolation rules, generated module and actual draft DOCX/PDF; corrected SV1 image plus later embedded exports. No acceptance granted from this materials-only stage.

## Full-record review checkpoint

Resumed on root verified16% at09:30:56UTC. Read full14-lesson canonical manuscript and final4-section assessment/3-criterion rubric plus full blueprint maps. All14 phase totals40min,overall560min;14 explicitly labelled authoring-design choice with no source allocation claim. Source-required basic/composite surface/volume and real uses covered; source competencies/PCI literal fields carried. Actual practical versus printed/diagram evidence distinguished explicitly in L8/L13 and final instructions. No new content error identified at this stage.

39registered calculations now independently recomputed without discrepancy, confirming unchanged keys after earlier all-task solve. Current independently computed content fingerprint `261cfa07c19ffbd3eb912f3e18573dde71de2328970b3c276b3224a3478b6378`. All five draft DOCX/PDF types extracted. Corrected SV1 image hash is embedded exactly in StudentMaterials and MaterialsTeacherKey Word files; final-only SV14 appears only in AssessmentMaterials/full teacher key,not teaching StudentMaterials. PDF visual samples and final verdict in progress. Standard final files remain pending content acceptance.
