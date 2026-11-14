# Core Mathematics geometry — independent source transcription review

**HOLD for coremath_2_1; PASS for exact source transcription of coremath_2_2,coremath_2_3,coremath_2_4. One confirmed wording defect.** Reviewer:essential_source_review; date:2026-11-14. This report covers four current source JSON records against the newly supplied PDF/PNG, printed10–22, and does not accept generated lessons or output artifacts.

## Confirmed finding CMG-S1

`data/curriculum_expansion_2026-11/sources/coremath_2_1.json` → **learning_experiences[4]** has “ratio of the **areas** of similar plane figures”. Printed11 in **both** the PDF and rawPNG says “ratio of the **area** of similar plane figures”. Restore singular **area**; the exact-source policy retains source grammar rather than editing it into preferred mathematical prose. The discrepancy is one added s, not an unreadable source ambiguity. All remaining text in this activity matches.

Evidence: `evidence/core_geometry_source_transcription/similarity_activity_area_word_pdf_detail.png` and `similarity_activity_area_word_raw_detail.png`. The enlarged PDF detail is derived from150dpi rectangle[680,17050,935,17350]; the native rawPNG detail is its proportional region. The exact current pre-correction JSON is frozen separately. Root was notified before any correction request was finalized.

## Comparison scope and results

I compared every outcome, content item, inquiry, learning experience, competency/value/PCI line and both Project blocks against the actual full-resolution PDF and rawPNG regions, including all page-spanning continuations. Whitespace/line breaks and bullet presentation are normalized as declared by each record; words, grammatical forms, capitalization and punctuation were checked as printed. I did not use OCR as authority, author a substitute transcription, or silently repair the source.

| Record | Printed scope | Outcomes | Activities | Source sections checked | Verdict |
|---|---|---:|---:|---|---|
| coremath_2_1 Similarity and Enlargement |10–12|6|8|4 content,1 inquiry,2 competencies,2 values,2 PCIs,Project|HOLD:CMG-S1 only|
| coremath_2_2 Reflection and Congruence |13–15|6|10|4 content,2 inquiries,2 competencies,2 values,2 PCIs|PASS|
| coremath_2_3 Rotation |16–18|7|9|4 content,1 inquiry,2 competencies,2 values,1 PCI|PASS|
| coremath_2_4 Trigonometry1 |19–22|6|10|4 content,2 inquiries,3 competencies,2 values,2 PCIs,Project|PASS|

Similarity’s long area/volume-scale activity, digital-resource continuation and solids-model Project are present; the area-word mismatch above is the only confirmed omission/addition/case/punctuation defect found. Reflection/congruence retains both Cartesian/plain-paper work, all triangle-test alternatives and the final digital activity, with complete competencies/values/PCIs. Rotation retains source grammar such as the missing connector in its second activity and the separate final PCI page; no editorial correction is required in the source record. Trigonometry retains its table/calculator instructions, complementary/special-angle wording, tangent plural where printed, long research continuation, clinometer Project and complete final PCI page. Singular material in its competency versus plural materials in its Project is correctly retained. Source punctuation, including absent terminal punctuation in some bullets, is preserved apart from CMG-S1’s added s.

Source rows provide the recorded title capitalization; headings may use different case. All four records correctly use the new localPDF path/hash, physicalPDFpage1,150dpi crop bounds and printed source-page ranges. No explicit official lesson count is present in these tables, so null official_lesson_allocation is appropriate. The long PDF has one physical capture page; printed labels are internal page labels. The previously excluded footers18 and22 were additionally inspected in adjacent source margins in this review, confirming those printed page labels directly; no unit text is missing from the source crops.

Source-specific mathematical qualifications in notes are separate from quoted requirements. In particular, the printed90° using triangles wording is preserved rather than silently rewritten; teaching treatment of the limiting/nondegenerate-triangle/tangent issue remains a subsequent content-review responsibility. This source review does not endorse an unqualified finite tan90° or perform a lesson review.

## Exact binding

NewPDF SHA256: `700b55379210dda0ee24561d43a872f965eba9568ec8092b6e9116d7f3609b2c`.

New rawPNG SHA256: `ec00ae54ca37365d9a8a0aa1b6edafb3a18deda56565abb9983be5d64a4dd017`.

Prior capture-readability report SHA256: `77b768133d2cdedd067270e188123e3cbce6c4f85311cf46d7fc64f3e972730c`. That report’s seven independent PDF crops match the provided source crops byte-for-byte. Full PDF/nativePNG evidence for these four records remains in the adjacent `new_core_capture_readability/` folder. This report adds exact current source snapshots, detailed finding images and footer contexts.

| Source JSON | Current/pre-correction SHA256 | Crop SHA256 |
|---|---|---|
| coremath_2_1 | `8e7444e71dec4da95091f2ed8385faaecc96290a488337b67b01f0b164f3c983` | `63b40e071f6b598587562536c8a4c25b2895e12ef6e6748741ffe22948d843fa` |
| coremath_2_2 | `c3ce02da1922f635038ce0adcdfd0411ec4d9a4ff50c480644c22d775a07a2e2` | `395a1866d28bad439c1cc0164f0f4c2f62f4891f00d8a0557f229792f392af79` |
| coremath_2_3 | `84a560bf889ba176aec8c53beca1bc1c50af84174a783acc0411d5ff9e8a757d` | `5b75ad748bbaeb4cb84527ec60df9852e2a8edfb96a5708fb8ab9ee18bc1a9bb` |
| coremath_2_4 | `561bb9423c0207aaec22dcbb916e31e54d05b4fd46f5eed3452275fc3acffea4` | `91d81f93c0da638926744683d5c70855c2171f9a6a9266c5ba97a038349ba3c3` |

All four source files matched the frozen snapshots when this report was saved. `evidence/core_geometry_source_transcription/binding.json` records exact hashes/counts/current-byte checks/metadata checks and finding path. No source, crop, pipeline, manuscript or acceptance state was edited. **Ready for a narrow correction of CMG-S1 and focused recheck; the other three records have no confirmed source-transcription defect.**
