# Independent focused recheck — Cell image frames, correction pass 1

**ACCEPTED: CIF-1 CLOSED. No newly caused issue confirmed in this scoped recheck.** Current PNG/JPEG source-image and crop-frame support remains technically accepted. Full Cell scientific content and actual complete-artifact review remain separate.

The immutable initial report is [cell_image_frame_code_review.md](cell_image_frame_code_review.md), SHA-256 `7f555024c1330e4964c7590ba92d46ee63ae7121c99a4d58ad1b8c80e8b7564e`. It preserves the original WebP preflight/build discrepancy and five-image LibreOffice proof. I did not alter that report or its evidence.

## Correction and independent checks

`image_spec` now uses the same python-docx `Image.from_file` decoder used by the document-writing path before accepting an image. Unsupported/corrupt stream exceptions from that decoder are translated to `ValueError`, which existing preflight catches and records. Thus Pillow recognition alone no longer establishes renderer compatibility. The added test creates a real Pillow-readable WebP rather than mocking the decoder.

I independently reran the entire pipeline suite: **22/22 tests PASS**. I also recreated the original failure independently in a temporary fixture. Pillow fully loaded the WebP, while `image_spec` rejected it with `ValueError`, caused by `UnrecognizedImageError`; preflight reported `E1: invalid or unbound diagram/crop` before any document build. This closes the specific confirmed finding.

I then revalidated CL3, CL4, CL5, CL6 and CL13 through current `compiler.write_doc`, writing only temporary proof files. All five current source images and the canonical materials record are unchanged from the initial bound proof. Every embedded media entry still equals its original source bytes exactly. More strongly, each new `word/document.xml` is byte-identical to its corresponding initially rendered and visually inspected proof. This confirms unchanged crop percentages, extents, aspect, text and panel placement for those proof inputs. No additional LibreOffice conversion was necessary for this decoder-only correction; the existing successful five-image conversion evidence remains applicable to identical document XML and media. No production outputs or reviewed units were rebuilt.

## Bound revision

| Input | SHA-256 |
|---|---|
| compiler.py | `d25bd88ddd005f306ccc7a5628f6dd7afdf8eb57a641adb0dff17f59c4c09d92` |
| validation.py | `2afa410f9bdb0d2ed9a500a554fb4e75ab91d0409f8fbb991a7b3c57ec7d32ba` |
| test_curriculum_pipeline.py | `569134904edf04507253f726dbb6237f925dfe936383535f5c710ef531f43f29` |
| curriculum_pipeline.py | `9a604072f3382fd165d60f9917d7c15b8978086c8473e9332863c4a1dd092eaa` |
| Cell materials JSON | `be3c308103306e18c6295deaad722ef8826ff23b2dfdabfe5c466978d79cb896` |

[Focused binding evidence](evidence/cell_image_frame_recheck/binding.json) records these hashes, the independent WebP rejection and all five current source/embedded/XML comparisons. [22-test log](evidence/cell_image_frame_recheck/tests.log) records the full independent test run.

## Limits retained

Crop frames preserve complete source files and are not redaction. Actual Cell teaching exports must omit the complete final-only Figure 1 source file, not merely hide its selected panel. The different taught Figure 3 source and explicitly reused animal image require their own intended-isolation checks. Scientific provenance/licences, numerical scale-bar metadata, supported biological claims, tasks/answers, page layout and actual nine Word/PDF-pair propagation remain forthcoming content/artifact checks. This focused recheck does not accept those artifacts or assert universal decoding/rendering compatibility for every conceivable image.
