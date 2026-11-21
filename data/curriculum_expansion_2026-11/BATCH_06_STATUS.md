# Batch 06 — all source-ready units completed

Checked 2026-11-14 20:21 UTC. This batch completed 10 units / 129 lessons, including Essential Probability before the reset and nine Science units / 119 lessons after it. Each has accepted content, independently reviewed final artifacts and a frozen local teacher-review package.

Across the expansion, **33 units / 392 lessons** are reviewed and packaged in **30 archives** (early batches contain multiple units). The frozen pilot adds 3 units / 31 lessons: **36 of 43 units / 423 lessons complete locally**.

| Curriculum | Completed units, including pilot | Lessons | Remaining units |
|---|---:|---:|---:|
| General Science | 16/16 | 197 | 0 |
| Essential Mathematics | 13/13 | 135 | 0 |
| Core Mathematics | 7/14 | 91 | 7 |

## Batch packages

| Unit | Lessons | Archive SHA-256 |
|---|---:|---|
| essmath_3_2: Probability I | 10 | `915635b78aa6ea24e267088281fa2a0db2732e38d45f6df4e5200b2fb96f217a` |
| gensci_1_7: Microorganisms | 12 | `d2f5c038282f2363d6ed14bcf4d15a706689ec93e67673770a6ebb822c5896b6` |
| gensci_2_1: The Periodic Table | 15 | `f8c2b2f3f55747361af3a86135006ade773ade07c21f79cf20d99b3997835ca2` |
| gensci_2_2: Chemical Families | 12 | `6b4cfc9e8a30f8a18cc402e0f1ddfc540f4b0e9fa33e192359aaa25590347f64` |
| gensci_2_3: Chemical Bonding | 14 | `bcfaee4d6afea664c340370ed5102cf06df1e9800bbc2a7ff486a9a062f97ef7` |
| gensci_2_5: Rates of Reactions | 13 | `42bb9d71b76fdd4b53b012ff77694bf574c4398a2f4aa9bfe45e4a2ca38ba7d4` |
| gensci_3_1: Turning Effect of Force | 12 | `d898e07f567db63155adf3657fd8392764e966f4f4a5cf47ab91c1071236c389` |
| gensci_3_2: Linear Motion | 13 | `7d03d7897bcebefe6c1e1b71469df7b656c10ca5a51f7b71427c68079ffe3f96` |
| gensci_3_3: Waves | 13 | `7f0d1f868bfd2708f0c438f4058ec4006152f8187ee576633fb31f05c2d06d02` |
| gensci_3_4: Magnetism and Electromagnetic Induction | 15 | `e9b1bbede97c576f2c6faa8bf06db5cf6800762c5766425523153a2f8b982d7d` |

Receipts and member-level manifests are in `evidence/`. Independent initial findings and focused closures remain under `reviews/batch_06/`; prior reports and frozen archives were preserved. Each unit delivers nine DOCX/PDF pairs plus one structured R1 export. The new nine Science units add 81 pairs.

## Final verification

- `evidence/checkpoint_integrity_2026-11-14.json`: PASS, 30 archives, all 33 authored units / 392 lessons, zero errors. Receipt/ZIP CRC/member hashes, exact document types, archived canonical fingerprints, current artifact hashes, content evidence and artifact-review evidence verified. Six early units use their explicit frozen-manifest artifact verdict and current review-file hashes; the other 27 have artifact-acceptance records. This checksum check does not repeat semantic or classroom review.
- `evidence/batch_06_final_canonical_checks.json`: all 33 canonical sets pass with zero errors. The 33 routine warnings retain the requirement for independent semantic/classroom checks; content and artifact review records supply the independent desk reviews.
- The final Magnetism review passed 1,039 propagation checks per format, 482 export/media checks and 18 final binding checks. All 105 pages were surveyed; 51 distinct pages were read at 120 dpi. All eighteen artifact hashes match the frozen audit.
- The new integrity utility was independently corrected and closed against 15 isolated fixtures (two positive, thirteen negative). Reports: `reviews/batch_06/checkpoint_integrity_code_review.md`, `checkpoint_integrity_code_recheck.md`, `checkpoint_integrity_code_closure.md`.
- Staged whitespace check passes for code, JSON, Markdown and all other files except seven literal student-summary text captures with blank final rows. Those exact frozen, hash-bound evidence bytes are preserved; `evidence/batch_06_whitespace_evidence_exceptions.json` records the exceptions.
- Frozen pilot archive receipt SHA and ZIP CRC were rechecked; its three current exports contain 31 lessons. Its files were not regenerated.

## Remaining work and limits

The seven missing Core Mathematics units need readable authoritative July 2025 requirements, including competency/value/PCI continuation pages: 1.1 Real Numbers; 1.2 Indices and Logarithms; 1.3 Quadratic Expressions and Equations; 2.1 Similarity and Enlargement; 2.2 Reflection and Congruence; 2.3 Rotation; 2.4 Trigonometry 1. No lesson counts are inferred for them. Local current captures are unreadable/repeated. The connected Drive and official-link lookup did not supply a permitted readable replacement; bounded lookup findings are in `evidence/core_source_lookup_2026-11-14.json`. A source-path/link question remains unanswered. Do not substitute old OCR or generated lessons, or bypass a download restriction.

Current partner run (`evidence/batch_06_final_partner_verdict.json`, exact 33 export hashes): all 33 bundles render; contract tests 16/16 pass. Overall command exits 1: enforcing partner R0 ingestion rejects our R1 schema (0/33 conform, 163 drift findings). Informational extractor tests are 24/25. Indices adapter fidelity is 3/7: attribution and rubric wording differ in four documents. The directory is present; the shell prints a misleading missing-directory message after failure. Physics/Maths adapter fixtures are absent and skipped. No schema downgrade or partner edit was made.

Actual classroom practicals, equipment/rating/sensitivity checks, digital provision, projects, outreach, access and pacing remain teacher-verified. Written records/plans are not evidence that those actions occurred. Independent desk/layout review is complete for the deliverable scope. No paid model API, push, promotion or Drive publication was performed. The active allowance stop remains 2%; it was not reached.

Next action: obtain a readable permitted current Core source, visually verify and bind all seven source records, then continue the existing materials → blueprint/manuscript → independent review → final artifacts → package process. Preserve completed packages.
