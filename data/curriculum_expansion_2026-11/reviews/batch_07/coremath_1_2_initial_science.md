# Core Mathematics1.2 Indices and Logarithms — independent initial content review

**HOLD.** All37 registered calculations and the numerical task/key answers are correct, but two manuscript notation defects and one task/outcome mapping gap require correction. Propagation success does not close these content findings.

Current reviewed fingerprint: `d94af2a1939d656839200f8c98cba4f3eda3e8811db5ac4028217f96f4ec822f`. This report freezes the initial full independent review before author corrections. No author/source/output/pipeline/acceptance changes or builds/renders were performed.

## Full scope and source continuity

Read accepted source record/its7 outcomes, all14 CIL cards and private keys, all37 registry expressions/answers, full14-lesson manuscript with70 phases/all summaries/reflections, complete blueprint/mappings/teacher confirmations, all4 independent final prompts/exemplars and all4 rubric criteria. Independently solved all tasks, including unregistered expressions, table/scaling/inverse work and every final demand. Opened all5 actual Word packages; full body texts and exact snapshots are preserved.

The complete source pixel review of printed3–4 carries forward from the accepted source recheck: outcomes/inquiry/content/experiences/competencies/values/PCI are unchanged. Source JSON `533a4d3973b7a1aec806e47a85fe2f05be0c1606f5de0c83274f504294fc028d`, crop `dd0269249f57784269456348c9c5b3db5a3308fe00776879af3cdbae8cca1559`, supplied capture PDF `700b55379210dda0ee24561d43a872f965eba9568ec8092b6e9116d7f3609b2c`. Source wording/case is retained; no official allocation appears.14×40minutes is explicitly teaching design. The user capture's DRAFT caveat remains; no new official download or publication-authenticity claim is made.

## Confirmed defects and required closure

**CIL-S1 — fractional exponent is called the root value.** In `manuscripts/coremath_1_2.json`, zero-based paths `/lessons/3/knowledge`, `/lessons/3/phases/2/3`, `/lessons/3/summary/observed` repeat:

> For positive bases,1/n is a positive nth root;negative powers invert the result.

The exponent1/n is not itself the root value: for x=16,n=2,the positive root is4 while1/n=1/2. State that **x^(1/n) is the positive nth root of x, for x>0 and positive integer n**, or equivalent exact notation. CIL4 student/key definitions already state the correct relationship. The erroneous knowledge/phase wording propagates into the actual CompactTeacherGuide; this is not an unused metadata note. All repeated manuscript occurrences and regenerated applicable artifacts must agree.

**CIL-S2 — logarithm is confused with its antilog in L12 instruction.** `/lessons/11/phases/2/0` says:

> Explain why 3.0791 normalises to10^3×10^0.0791;accept a reasoned preference for direct arithmetic on this simple example.

The RHS is10^3.0791,approximately1200,not3.0791. State **10^3.0791=10^3×10^0.0791**, or explicitly that the antilog of3.0791 is being normalised. The CIL12 key/log arithmetic is correct; the learner instruction and its actual CompactTeacherGuide occurrence are not precise enough to preserve the log/number distinction.

**CIL-S3 — L13/F13 overclaims b,d,g.** Current outcomes `[b,c,d,g]` appear at manuscript `/lessons/12/outcomes` and blueprint `/lesson_map/12/outcomes`, `/assessment_map/12/outcomes`, `/assessment_tasks/12/outcomes`.

CIL13/L13 ask six repair examples,a group chart update and an individual correction/calculation/domain condition. They do **not explicitly elicit** a factor-based derivation of an index law(b),a power-of10/log inverse-notation conversion(d),or an individual specific usefulness/limit or method-choice explanation(g). The phase asking pupils to respect a reasoned view does not request their own assessable usefulness evidence. Applying an existing law to repair an example supports c; it does not establish all three additional source outcomes. A group chart alone is expressly not each learner's derivation.

Close by limiting L13/F13 to the supported c in all four linked arrays,or by adding concrete individual elicitation and matching key/lesson evidence for every retained claim. The smaller mapping correction preserves the unchanged tasks: b remains covered in L2/L3/finalI1,d in L6/finalI2,g in L12/finalI4. No broader content expansion is required. This finding concerns explicit assessment evidence,not a demand to grade enthusiasm or infer a lasting attitude.

## Independent mathematical/task verification

All37 registry results agree with independent assigned exact/decimal values and separately evaluated arithmetic. All10 common-log rows and all11 unique antilog rows are correctly rounded (4decimal places and4significant figures respectively). Final table rows duplicate verified common-log entries. Ten arithmetic/structure consistency checks pass; these do not assert that the semantic mapping defects are closed.

| Task | Independently checked result/meaning |
|---|---|
| CIL1 |8=2³,27=3³,64=2⁶=4³=8²,1000=10³;3⁴=81 versus3×4=12.|
| CIL2 |32,27,64,36;factor expansion/cancellation validates product,quotient,nested/product-power laws;addition4+8=12 does not give32.|
| CIL3 |3²/3²=1;2²/2⁵=1/8;5⁰=1,2⁻³=1/8,10⁻²=1/100,4⁻¹=1/4;nonzero-base restriction.|
| CIL4 |4,9,1/9,4;root denominator/power numerator verified,including9³=27² and4⁵=32². Card/key correct despite CIL-S1.|
| CIL5 |A72,B12,C25,D64,E256,F4,G−4;parentheses/sign/tower/sum distinctions valid.|
| CIL6 |Logs3,0,−2,1/2 andlog0.1=−1;10^u always positive,so no real log0/negative input.|
| CIL7 |log70≈1.8451,log0.007≈−2.1549,log200≈2.3010,log0.02≈−1.6990. Signed exponent arithmetic and precision valid.|
| CIL8 |Logs2≈0.3010299957,0.02≈−1.6989700043,7≈0.8450980400;10^0.3010≈1.9998618696,not exact2. Actual display/action must be observed.|
| CIL9 |Log sum0.7781→antilog5.999→6.00(3SF),exact6;scaled sum3.7781→5999→6.00×10³,exact6000.|
| CIL10 |Differences0.7781 and2.7781→5.999 and599.9→6.00 and6.00×10²;exact6,600. Subtracting a negative handled correctly.|
| CIL11 |2³:0.9030→7.998→8.00,exact8. √3:0.23855→0.2386→1.732→1.73,exact√3. Cube-root8:0.301033…→0.3010→2.000→2.00,exact2.|
| CIL12 |Combined log3.0791;antilog10³×1.200→1.20×10³,exact1200. Benefit/precision/domain reflection actually requested here.|
| CIL13 |Repairs1/8,1,log5≈0.6990 rather thanlog6≈0.7781,−1.6990,finite-output approximation,16^(1/2)=4 rather than8. Mathematical repairs valid; mapping gap remains.|
| Final I1 |10⁻³,2⁻⁵;factor-derived3⁵=243 and3³=27;9,1/4,1 with domain conditions.|
| Final I2 |log0.01=−2,log1000=3;1.8451,−2.1549;actual log7→0.8451(4DP) or pending device component;positive-input proof.|
| Final I3 |7×5:1.5441→10×3.500→35.0(3SF),exact35.20÷8:0.3979→2.500→2.50,exact2.5.|
| Final I4 |3²:0.9542→8.999→9.00,exact9.√5:0.3495→2.236→2.24,exact√5;specific method benefit/limit with reasoned preference allowed.|

The identity versus rounded numerical representation distinction is otherwise correctly maintained. Positive real bases constrain rational indices;integer negative-base examples are explicitly grouped. Quotient laws/zero/negative exponents require nonzero bases;0^0 is outside the asserted cases. Common-log arguments stay positive even when outputs are negative. Bar-characteristic notation is not silently substituted for signed decimal logs. Tables are labelled teacher-prepared instructional data,not an official book. All requested inverse rows are supplied; table-based answers use3SF and retain exact direct comparisons separately.

Complete independent registry/table/task evidence is `evidence/coremath_1_2_science_solutions.json`; it is reviewer evidence,not an added student derivation requirement.

## Lessons, final assessment and actual-action boundaries

All14 lessons total40minutes; blueprint/manuscript maps are mechanically consistent,though CIL-S3 identifies substantive overmapping. All7 source outcomes have genuine routes elsewhere. All4 final prompts actually ask the linked skills and align with their4 rubric criteria: factor derivation/index forms;inverse notation/signed table/conditional calculator;products/quotients;power/root plus reasoned method choice. No final task requires enthusiasm. Accepting direct simple arithmetic as preferable under a valid argument is appropriate for source g.

Final timing is4procedure/10I1/8I2/8I3/8I4+2checking,matching `[4,10,8,8,10]`. No worked hints,teaching cards,peer consultation or exposed key are allowed; actual device action is observed without coaching. The typo `nopierrevision` in the final teacher sentence is understandable alongside the explicit independent conditions and is a minor copy-edit observation,not an additional mathematical HOLD.

CIL8 and finalI2 require model-specific common-log/inverse operation verification and actual entries/displays/individual observation,or NOT OBSERVED/pending if unprovided. Written key sequences/supplied approximations do not certify actual use. Group derivation/resource care remain observed individually where claimed; a chart does not prove every learner's reasoning. Teacher approval/access,prerequisites,individual device throughput,signed-log fluency and40-minute pacing remain classroom judgments.

## Actual Word propagation and separation

399/399 applicable actual Word text checks pass,covering14 lesson core fields and every phase cell,all14 full card/student/private strings and7 source outcomes. This includes confirming that CIL-S1/S2 erroneous strings are present in the actual Guide; propagation is not correctness. An additional15/15 binding/isolation checks confirm current source/canonical/Word hashes unchanged during review,42 blank learner-summary cells across14 rows,and absence of the full held-out CIL14 stimulus from teaching Guide/StudentMaterials/blank Summary.

Full final reference is supplied separately in AssessmentMaterials/private MaterialsTeacherKey. Complete private material keys and final exemplars are absent from student-facing documents. All5 Word packages contain zero embedded media and retain ChatGPT/Codex/OpenAI attribution. No legacy diagram collision occurs. Exact source metadata,signs,table values/root symbols propagate. This initial gate does not claim native Word pagination or final PDF layout/standard response-sheet inspection; no render/conversion was run.

## Evidence, alternatives and required next step

Confirmed HOLD findings are CIL-S1,S2,S3 above. Reasoned alternatives: repair semantic mappings by reducing claims or explicitly eliciting the missing skills; either is reviewable,while retaining genuine coverage elsewhere. Accept other mathematically valid input forms/device sequences only under the same domains/precision/observation limits. No additional confirmed numerical answer defect was found. Pending classroom/actions/access are not presented as completed or as additional authoring blockers.

Make a limited correction,then request focused recheck against these frozen inputs (standing maximum two correction passes). This report remains immutable. No external source was needed for stable elementary mathematics; the accepted local curriculum pixels remain source authority.

| Canonical input | SHA-256 |
|---|---|
| `sources/coremath_1_2.json` | `533a4d3973b7a1aec806e47a85fe2f05be0c1606f5de0c83274f504294fc028d` |
| `materials/coremath_1_2.json` | `8b76985b9c55ca167f0ee78d2feb36c8dd6e982bed042bf04b597f87e2739e1d` |
| `manuscripts/coremath_1_2.json` | `8ee5c67c880ed4c0198f1f3b296db24a58cada76464866f799dba84d64e3f731` |
| `blueprints/coremath_1_2.json` | `375811b10106261f68f6bef80972a7c143e888d93bbe348f34ef95d6f308b8cd` |
| `sources/coremath_1_2.verification.json` | `b95b951b0c81250ed9e32e1d0d61cf5f32df975d4781c119ff8fb35ed0f34675` |

| Actual Word companion | SHA-256 |
|---|---|
| CompactTeacherGuide | `46464efff26c6eb326335585ce693515d5214e6c34367872bf8b4865270bd4db` |
| StudentMaterials | `8d48cf2469cd0bd6b17be468c54214c92640a7b9e6e07effb1f72d6d7175460b` |
| MaterialsTeacherKey | `08c68ae5862ad356efd48b2752ccc1c7a20d2db239bb13ec86a71c4e82988c9e` |
| StudentSummaryTable | `f815bfa0d0c7d7eec7d5f93b1f7e6ab202c449a7d71939f63db9021ed71413a8` |
| AssessmentMaterials | `b87bc4af318ab5917d77413ecd09e1f525d9893dfe3fb23a4804f457f4d8aed5` |

| Reviewer evidence | SHA-256 |
|---|---|
| `evidence/coremath_1_2_science_initial_word_check.json` | `69eab3b89e9f5e1cf4e0712438da12415e68544dc74c54b854aabe9dbe7f6f02` |
| `evidence/coremath_1_2_science_solutions.json` | `d617274daa84310d9f07e67aa50a028b8dccd401ff8c00c7df345bfb0beada24` |
| `evidence/coremath_1_2_initial_final_binding.json` | `9abf893b5c8fe632a77056b83cb4b88b0211e5452e9d31878be4a3b908a5f734` |

Corresponding check/solver scripts,exact frozen four canonical JSON snapshots and5 actual Word extracts remain alongside evidence. No source,author/output/pipeline or acceptance mutation occurred.
