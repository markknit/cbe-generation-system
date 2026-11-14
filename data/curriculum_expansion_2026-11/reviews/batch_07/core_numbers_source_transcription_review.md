# Core Numbers source transcription — independent review

**Initial verdict: HOLD for the three-record batch.** `coremath_1_1` passes; `coremath_1_2` and `coremath_1_3` each have two confirmed exact-transcription defects requiring a focused recheck. No author/source/pipeline or acceptance mutation was performed.

## Scope and authority

Compared every transcribed outcome, inquiry question, content bullet, suggested experience, competency, value and PCI against all three complete source crops and corresponding regions of the original user-provided PNG. Independently rasterised the supplied PDF physical page1 at150dpi using each declared rectangle: all three fresh crops are **pixel-identical** to canonical source crops. Cover/title/publication pixels were also inspected. This is local-source transcription review; no official-site download, independent publication authenticity certification or lesson-content review is claimed.

The supplied PDF is a FireShot/Google Drive capture with one very tall physical page (595.44×21691pt); printed curriculum pages1–6 are distinct embedded displayed pages. `physical_pdf_page:1` is therefore correct. PDF hash, Grade10/Core Mathematics/title metadata and printed page ranges match. `render_dpi:150` and rectangles refer to the1241px-wide PDF raster, not the1799px-wide original PNG. Original PNG dimensions are1799×65535. The cover says Core Mathematics Grade10,2025 and visibly retains DRAFT; current notes retain that caveat.

## Confirmed finding paths

| Finding | Record/path | Source pixels | Current JSON | Required correction |
|---|---|---|---|---|
| NUM-SRC-1 | `coremath_1_2.json /learning_experiences/0`, printed3 | `...share them with peers.` | `...share them with peers,` | Restore full stop. |
| NUM-SRC-2 | `coremath_1_2.json /learning_experiences/3`, printed3 | `...logarithm notation to base 10` with no terminal punctuation | Ends `base 10,` | Remove added comma. |
| NUM-SRC-3 | `coremath_1_3.json /coreCompetencies`, first label, printed6 | `Critical thinking and problem solving:` | `Critical thinking and problem-solving:` | Remove added hyphen. |
| NUM-SRC-4 | `coremath_1_3.json /coreCompetencies`, second line, printed6 | `the learner discusses with peers and comes up with quadratic identities.` | Uses `come up` | Restore `comes up`. |

These are transcription defects under the standing rule to normalise only bullets/line breaks. They are not requests to improve source grammar. Complete source/native-PNG regions and detail images are preserved in review evidence. Findings are also in `evidence/core_numbers_source_findings.json`.

## All-field and boundary observations

- **1.1 Real Numbers, printed1–2: PASS.** All6 outcomes (including f on the continuation page),1 inquiry,2 content bullets,8 complete experiences (including the last continuation),3 competencies,2 values and1 PCI match. No mismatch found. Source wording about categorising whole numbers as rational/irrational is retained, despite its pedagogical qualification needs; this review does not silently repair source content. Crop `[0,9900,1241,11200]` includes full strand/unit header, first-page table, second-page continuation and all lower boxes/page numbers.
- **1.2 Indices and Logarithms, printed3–4: HOLD for NUM-SRC-1/2 only.** All7 outcomes,1 inquiry,3 content bullets,7 complete experiences,2 competencies,2 values and1 PCI were read. Remaining wording/case/punctuation match. Outcome d has no terminal punctuation in pixels and correctly has none in JSON. The final experience continues onto printed4 and is complete. Crop `[0,11300,1241,12600]` includes both entire relevant page regions and lower boxes.
- **1.3 Quadratic Expressions and Equations, printed5–6: HOLD for NUM-SRC-3/4 only.** All8 outcomes including g/h continuation,1 inquiry,6 content bullets,7 experiences including page-spanning factorisation wording,2 competencies,2 values and1 PCI were read. Remaining fields match. The experience itself says `come up`, while the separate competency says `comes up`; preserve that source distinction. Retain source `roots, statement and real-life cases`, `real life` in outcomes g/h, and `real-life` in corresponding content/competency/value/PCI where printed. Crop `[0,12700,1241,14000]` includes the full unit table and continuation/lower boxes.

No explicit lesson allocation appears in any of these three tables: all three `official_lesson_allocation:null` values are correct. No next-unit content is mistaken for the reviewed unit; no continuation is truncated. The existing `verified_by` caveat says independent review pending; this report does not itself change that status. A focused recheck after the four corrections is required before accepting the batch.

## Exact reviewed inputs

Shared supplied originals:

- `CBE_Curriculums/Grade 10/STEM/Grade10_CoreMath.pdf` — `700b55379210dda0ee24561d43a872f965eba9568ec8092b6e9116d7f3609b2c`.
- `CBE_Curriculums/Grade 10/STEM/Grade10_CoreMath.png` — `ec00ae54ca37365d9a8a0aa1b6edafb3a18deda56565abb9983be5d64a4dd017`.

| Reviewed canonical input | SHA-256 |
|---|---|
| `data/curriculum_expansion_2026-11/sources/coremath_1_1.json` | `3f6b0e7f72ab8d9039a8cdaafa9a291e7d05939e917256f27023672adb160fcb` |
| `data/curriculum_expansion_2026-11/sources/coremath_1_1_source.png` | `f53737b3a5115509af7aa5f47b678dd1cf628a0fb00dd3724fef34d831b906de` |
| `data/curriculum_expansion_2026-11/sources/coremath_1_2.json` | `6ca36e978fc914bb1040bb0b8cf2f0c2ce1838940c05fdd155a2129638aab8fe` |
| `data/curriculum_expansion_2026-11/sources/coremath_1_2_source.png` | `dd0269249f57784269456348c9c5b3db5a3308fe00776879af3cdbae8cca1559` |
| `data/curriculum_expansion_2026-11/sources/coremath_1_3.json` | `6f84ac6a37c78c4242598a3c9e242a51fcfb64521ea0f4648b90e3f0caeb3512` |
| `data/curriculum_expansion_2026-11/sources/coremath_1_3_source.png` | `15fec579e6ced6194a209fc26d477228356eea111023fea791b62e2ea807f8a8` |

Evidence binding: `evidence/core_numbers_source_initial_binding.json`, SHA-256 `4914a1958b18eba198eebc0e4d86b8a08563b3adc217a9067a41ef8415cf2555`. It includes exact input records, hashes and crop equality results. Exact initial JSON snapshots are `evidence/coremath_1_{1,2,3}_source_initial.json`; independent PDF crops, original-PNG regions, detail evidence and original title view are alongside them. The existing OCR files were not used as visual authority.

No online source was needed or substituted. The user supplied local captures are the authorised source for this review; original-download restrictions remain unchanged.
