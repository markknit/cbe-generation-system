# GS3.2 Linear Motion — independent initial content review

**Verdict: HOLD — one confirmed actual-Word artifact defect.** Reviewer: science_review. Date:2026-11-14. The canonical science/tasks/keys/alignment are otherwise acceptable within the explicit performance limits below. Preserve this initial report/binding before correcting outputs; no author self-review used.

Current fingerprint `316dbac1f77b599d35a755b661b21d12b61549e3945b00c0a39cd485af4046c4`.

## Confirmed defect and correction scope

Both actual **StudentMaterials** and **MaterialsTeacherKey** contain two referenced graph images unrelated to the current tasks,although canonical material records contain no diagram metadata:

- Immediately after **LM5**, image SHA256 `0abc74762b0987c5e805a89b3699d2606f5d6a3b7a243956bd1359de59bc3e06` shows displacement points(0,2),(2,6),(4,6),(6,2),(8,−2). Current LM5 specifies u2m/s,a1.5m/s²,t4s:displacement20m and positive increasing velocity. The graphic instead rests/reverses and is not this problem.
- Immediately after **LM8**, image SHA256 `8a953fdb52665bfa85db27ab70e0775bc51261cbd082df55f9e759874b097af7` shows east-positive velocity points(0,3),(2,3),(4,−1),(6,−1). It is not the current supervised downward low-drop record and supplies an unrelated measured-looking motion graph beside a task with no prefilled actual data.

I viewed both extracted images and inspected their actual document.xml drawing relationships/preceding task paragraphs. They are referenced visible content,not merely unused ZIP media. Their bytes exactly match workspace legacy `materials/diagrams/LM5.png` and `LM8.png`; a shared card-ID fallback collision is a reasoned explanation,not a required compiler diagnosis. Exact placements and images are saved in `evidence/gensci_3_2_science_solutions.json` and `gensci_3_2_StudentMaterials_image1.png`/`image2.png` (private-file copies also retained).

**Required:** remove this unintended legacy-image association while keeping current text/data/answers intact,then rebuild the five companions and independently recheck actual media/text/isolation/hash binding. Root's proposed unique GSLM card namespace is a plausible narrow resolution if every canonical cross-reference follows it and source wording remains unchanged. No new chemistry/physics content or production compiler change is requested by this finding.

## Complete source/content scope

Read actual source pixels printed35–37,canonical source,all13student cards/keys,complete blueprint,all13manuscript lessons/every phase and summary/reflection,four final sections/exemplars and four rubric rows. All four outcomes,content including **no derivations needed**,both inquiry questions,all suggested experiences,competencies,values and PCIs match the source. No official lesson count is printed;13×40minutes is teaching design. Source road/free-fall PCI wording remains verbatim while teaching explicitly separates road contact motion from gravity-only free fall.

Source JSON SHA256 `b9b6fe9eb9bbc6803c8eab78a26d4c333ce33694e71172bfe3b8a1a8261142b5`; crop `f368a4b4ce0c0c8b06f816a5c77f13b420510b7328759b94922090480b248172`; verification JSON `6e17a43f7bca1f69c28046a82829c4ab5bbf1691c8becb47f6c83157bc8e5dba`. Curriculum PDF SHA256 `ee989d27038d838096438ff16a02fe1be0abc81e7010168036fcb9a125d0d0fd`. Four exact canonical snapshots were saved before correction in `evidence/gensci_3_2_initial_*_snapshot.json`,indexed by `gensci_3_2_initial_canonical_snapshots.json`.

Independent solutions cover **all22registry expressions**,all unregistered values,graphs,controls,sign/root choices,real-life claims and final tasks. All22 pass;13separate conservation/cross-route/mapping/timing/actual-blank-cell checks pass. Key results:

- LM1:distance7m,displacement+1m,average speed1m/s,average velocity+1/7m/s. Return path can have zero displacement with nonzero distance. LM2 slopes±3m/s; straight interpolation is an assumption,not knowledge of every between-sample movement.
- LM3:a−2m/s²,v0 at2.5s; speed decreases then increases after reversal. Velocity-time endpoints(0,5),(3,−1). LM4:A11m/s,B6s,C2m/s². Changing acceleration requires interval-specific treatment.
- LM5:s20m,v8m/s,endpoint mean5m/s; the unsquared-time arithmetic gives11 rather than20 and has a dimension error. LM6:v²64,root+8m/s selected by forward context; algebra alone permits±8. First rest4s/24m; do not extrapolate the braking model past rest.
- LM7 graph(0,4),(3,4),(6,10),areas12+21=33m,average velocity5.5m/s,accelerations0then2m/s². No reversal,so distance33m. Whole-trip endpoint mean incorrectly gives42m.
- LM9 interval averages0.5,1.5,2.5m/s; differences per0.10s give10m/s² under the stated model. They equal midpoint velocities at0.05/0.15/0.25s under constant acceleration,not measured endpoint speeds. Formula positions0.05/0.20/0.45m agree.
- LM10:A5m/10m/s;B0.50s/5m/s;C1.6m/6m/s. All are paper models using stated g10. LM11:apex1s/5m,v0 buta−10m/s²;return2s/−10m/s. At0.5and1.5s position3.75m,velocities+5and−5m/s.
- LM12:road contact/friction/drive forces exclude ideal free fall; doubling rest-release height multiplies impact speed by√2,not2; calculations cannot certify protection; gravity persists at apex. Precautions remain conceptual and bounded.
- Final LM13:I1distance7m,displacement+3m,averages1and+3/7m/s;I2B14m/s/32m (cross-check8×4),C5s/25m;I3D1.8m/6m/s,E interval averages as above,apexv0/downwardg;I4proper road/free-fall and actual/safety evidence limits. No numerical answer defect found.

All lesson/task outcome maps agree; all four rubric links match their corresponding elicited final skills. c-tagged written/frame tasks are expressly conceptual,not actual-investigation evidence. Every lesson totals40minutes. Final and actual Guide agree **4read/8I1/12I2/10I3/6I4-check-submit**,with procedure-only support,no hints/guided correction and collection before feedback. No derivation is demanded.

## Actual five Word binding

**368/368 text propagation checks pass**,but this does not cure the confirmed image defect. All requested guide/card/key/source outcome text propagates. All39student-summary response cells are blank across13lesson rows. Held LM13 is absent teaching StudentMaterials and correctly present in standalone AssessmentMaterials; private keys/full exemplars are absent student files. All five retain OpenAI attribution. Exact current hashes:

| Companion | SHA256 |
|---|---|
| CompactTeacherGuide | `8ba71227573da05dcaecc4222ebdba7c48baeca055154615872163ba9a3cbb45` |
| StudentMaterials | `3b9f435f4415a3602ba9925a88b7d33b952d111c81b3420159b6e3642d18dbb9` |
| MaterialsTeacherKey | `e105b4898f381f67815b46054e24460334579e4bdf7df9021dc72053045a3df6` |
| StudentSummaryTable | `d682aaebec5ed9731d389f80f28760551b9f0736e230c165398bd46738397a55` |
| AssessmentMaterials | `cba3052c474608957194b2527110d2dcf061ffd25aa28ddca974f3603e679f52` |

## Safety,primary checks and teacher judgments

LM8 requires teacher-approved light soft ball,stable floor-level catch tray,clear exclusion zone,release without throw from≤0.50m,retrieval after rest and three actual records with height,object,release condition,roles/date. No climbing,stairs,windows,roads,hard/heavy loads or people below. Actual outcome c evidence requires observed approved releases; acceleration claims need suitable calibrated timed-position evidence. Looking alone or human stopwatch timing over this low drop cannot establish precise g. Supplied LM9 frames remain fictional conceptual records; missing provision must retain not-performed status.

Real drag,release/scale/frame uncertainty and local gravity differ from the ideal model. Paper heights/times do not authorise larger drops. No actual road test,launch or safety-system certification is supplied. Teacher confirms materials,exclusion/supervision,frame provision,accessibility,pacing,actual discussion/research actions and individual records. Written work cannot prove digital navigation,practical investigation or enduring peace/unity dispositions.

Independent primary checks used [OpenStax speed/velocity](https://openstax.org/books/physics/pages/2-2-speed-and-velocity),[constant-acceleration equations](https://openstax.org/books/physics/pages/3-2-representing-acceleration-with-equations-and-graphs) and [falling objects](https://openstax.org/books/college-physics-2e/pages/2-7-falling-objects). The latter supports signed upward/downward motion,negligible-drag idealisation and nonzero apex acceleration. External cliff/metal-ball/reaction-time exercises were not imported. Access/substitution limits are recorded in `evidence/gensci_3_2_primary_receipt.json`; no local original PDF is claimed.

Apart from the confirmed legacy images,no additional correction request. Practical timing/frame detectability and classroom final workload are teacher judgments. No actual-classroom or full page-layout acceptance is claimed.

Evidence SHA256: Word binding `69cf292162f4db509c7f43a799028356404c5c6922b9a0c09d114cdb5611aecf`; independent solutions/actual image placements `7babe6836dd078af6600527d302175b69707c0ea06fd7ee0a25742a5a3dea575`; canonical snapshot index `9eede2fcc760842912245cce388e030f6121332f4c3707f6f48e56e6f8ffa1f7`. All exact input hashes and initial actual Word text extracts are retained. No author/source/canonical/output/acceptance/pipeline state changed; no build/render ran.
