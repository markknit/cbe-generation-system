# Independent Cell image-frame code review

**Disposition: ACCEPTED for the current five PNG/JPEG Cell image references and their declared crop frames, with one confirmed nonblocking general-format validation gap.** This is technical support verification, not Cell source/content acceptance or final-artifact acceptance.

## Bound inputs and evidence

Reviewed `image_spec` and `add_material_image` in `scripts/curriculum/compiler.py`, diagram validation in `scripts/curriculum/validation.py`, the three new tests in `scripts/test_curriculum_pipeline.py`, and declared-asset/canonical-input hashing in `scripts/curriculum_pipeline.py`.

| Input | SHA-256 |
|---|---|
| compiler.py | `3ee5bb4481f380f1fb7a01fcccbe75102af4a0b5764237005b188a750450ad0a` |
| validation.py | `2afa410f9bdb0d2ed9a500a554fb4e75ab91d0409f8fbb991a7b3c57ec7d32ba` |
| test_curriculum_pipeline.py | `c29cc1f484cb237bcaea223f10cee9bace527a4c7252c7b485da8e2b4be75c0c` |
| curriculum_pipeline.py | `9a604072f3382fd165d60f9917d7c15b8978086c8473e9332863c4a1dd092eaa` |
| Current Cell materials JSON | `be3c308103306e18c6295deaad722ef8826ff23b2dfdabfe5c466978d79cb896` |

[Technical proof binding](evidence/cell_image_frame_proof/binding.json) binds all five source images, their dimensions/crops, embedded-media equality, Word geometry, proof Word/PDF hashes, renderer version and page-image hashes. [Independent mutation evidence](evidence/cell_image_frame_proof/independent_mutations.json) records extra boundary/fingerprint/format checks. [Test log](evidence/cell_image_frame_proof/tests.log) records the independent 21/21 pipeline test pass. [Reproducer](evidence/cell_image_frame_proof/reproduce.py) renders isolated technical proofs under a temporary LibreOffice profile and saves evidence in this review directory only. No production/canonical/code files were edited and no previously reviewed unit was rebuilt.

## Confirmed implementation behavior

1. An explicit diagram must also appear in the card's `assets`. Resolved paths must remain within `materials`, including resolution of parent segments and symlinks. Missing declared diagrams fail. The older implicit `materials/diagrams/{id}.png` convention remains available.
2. A crop is a four-integer, nonempty, in-bounds pixel rectangle. Boolean and float coordinates, zero-sized rectangles, negative/out-of-range bounds, wrong-length boxes and explicit null crops are rejected. Independent mutation checks confirmed these cases and an escaping path rejection.
3. The source file is supplied directly to python-docx. Its five resulting Word media entries individually equal the corresponding original source file **byte for byte**. No bitmap cropping, scientific retouching or source-image synthesis occurs in this path.
4. The frame uses DrawingML `a:srcRect`, with fractions calculated against full source dimensions. Visible crop aspect controls both frame dimensions; width is at most 6.3 inches and height at most 6.5 inches. Percentage rounding to 1/100000 and Word EMU integer sizing can introduce tiny coordinate rounding, not intentional image-content modification. All current boxes were checked against source dimensions.
5. Full canonical materials JSON is fingerprinted, so changing `diagram` or `diagram_crop` changes content acceptance inputs. Declared `assets` contribute their file bytes; implicit conventional diagram files are also hashed. Independent mutation checks confirmed that changing image bytes and changing crop coordinates independently change `content_fingerprint`. Content cache additionally includes compiler code, and PDF cache includes exact Word bytes and renderer version.
6. This is local input binding, not proof that a file came from the credited remote scientific source. Source provenance, licence and specimen/calibration metadata still need content-review verification against the original records. The code also does not itself validate whether a crop is pedagogically appropriate or keeps a scale bar.

## Actual LibreOffice proof

I inspected all five original images, then rendered each selected card through the actual `compiler.write_doc` path. Conversion used an isolated temporary profile and the current installed LibreOffice version recorded in the binding. Each proof is one PDF page. I visually inspected all five page renders, with no observed clipping, gross distortion or missing selected bar/label.

| Card | Frame and actual proof result |
|---|---|
| CL3 | Full 1280 × 1024 source; original onion-root field visible. No invented calibration bar was added. |
| CL4 | `[0,2084,1397,3125]` selects the bottom cheek-cell panel of the three-panel composite, with its original white scale bar. Upper views are absent from the visible frame. The bar's numerical 15 µm meaning comes from metadata/caption, not a printed number in these pixels; verifying that value remains a content-review task. |
| CL5 | `[1037,0,1985,538]` selects Figure 3B. B, N, Ch, V and the original 2 µm scale bar remain visible. Other panels are not visible. |
| CL6 | Full 1805 × 1711 source and original 2 µm bar remain visible; no complete-cell outline was fabricated. |
| CL13 | `[688,0,1332,925]` selects Figure 1B. B, N and original 1 µm scale bar remain visible. Portrait frame fits at 6.5-inch height with correct visible aspect. |

Proofs: [CL3](evidence/cell_image_frame_proof/CL3.pdf), [CL4](evidence/cell_image_frame_proof/CL4.pdf), [CL5](evidence/cell_image_frame_proof/CL5.pdf), [CL6](evidence/cell_image_frame_proof/CL6.pdf), [CL13](evidence/cell_image_frame_proof/CL13.pdf). These are technical evidence, not student release files.

## Confirmed general-format validation gap

**CIF-1 — Preflight accepts an unsupported image format; build then fails.** A valid WebP declared in `assets` and `diagram`, with a valid crop, produces no validation errors because PIL opens it. `add_material_image` subsequently raises `docx.image.exceptions.UnrecognizedImageError` because python-docx cannot embed that format. This was independently reproduced in a temporary fixture; see mutation evidence. None of the present Cell assets is WebP, so this does not block their current PNG/JPEG support. If arbitrary image formats are intended, validation should test python-docx support or restrict/document supported formats and include a corresponding negative test. This is a failure-reporting gap rather than silent image corruption.

The three new automated tests use a uniform PNG and inspect XML/media rather than conversion. They meaningfully cover binding, bounds, crop fractions, aspect and portrait height. They do not by themselves test visible panel selection, calibration-bar retention, actual renderer handling, unsupported formats or fingerprint mutation. The independent checks above supply evidence for the present five images and two fingerprint mutations, without claiming universal image-format or renderer coverage.

## Residual checks for actual Cell documents

- Native crop frames are **not redaction**. The complete source composite is embedded and can be recovered or uncropped. Student/key/final isolation must inspect the entire embedded source, not only visible panels. Current proof images are scientific composites rather than teacher-answer pages, but final-only isolation of CL13 and its entire source asset must be checked in the actual student/teaching ZIPs and PDFs.
- A 6.5-inch image cap does not guarantee its caption and the image stay together on a densely populated actual page. The five standalone proofs fit; the complete Student Materials, Teacher Key and Assessment Materials documents still require page-by-page layout review.
- Actual final Word/PDF media hashes, crop rectangles, visible labels/bars and readability must be verified after build. No native Microsoft Word rendering was run; the successful actual conversion evidence is for the recorded LibreOffice installation.
- Scientific image provenance/licensing, bar calibration, caption/method accuracy, what the images support biologically, task answers, performance evidence and assessment isolation remain the forthcoming independent content/artifact review. Code tests cannot accept them.
