# Core Numbers source transcription — focused correction recheck

**PASS for the current three source records.** All four initial transcription findings are closed; no other change was found. This is source-only verification, not lesson/material/content acceptance. Root source acceptance remains a separate action.

Initial HOLD remains immutable: `core_numbers_source_transcription_review.md`, SHA-256 `f1a21a10265271290802ee039aa628aa9d6ceab3e6dd6135a40a500840c77294`.

## Exact correction closure

Compared each current source JSON recursively against its frozen initial snapshot, and re-read the original-PNG finding details against the corrected strings:

- NUM-SRC-1: `coremath_1_2 /learning_experiences/0` now ends `peers.` as printed.
- NUM-SRC-2: `coremath_1_2 /learning_experiences/3` now ends `base 10` with no terminal punctuation, as printed.
- NUM-SRC-3: `coremath_1_3 /coreCompetencies`, first label now reads `Critical thinking and problem solving:` without the added hyphen.
- NUM-SRC-4: the second competency now reads `the learner discusses with peers and comes up with quadratic identities.` as printed. The separate experience's `come up` remains unchanged.

Precisely four textual corrections were made across **three JSON scalar paths in two JSON files**: both competency corrections occupy the same multiline `coreCompetencies` scalar. Thus four changed scalar paths would be an inaccurate count. Exact before/after values are recorded in the recheck evidence.

All10/10 focused checks pass. `coremath_1_1.json` is byte-identical to its initial reviewed input. Restoring the two1.2 experience strings and the single1.3 competency scalar recovers the complete original records. No additional wording, outcome, inquiry, content, experience, competency/value/PCI, note or metadata change occurred.

## Preserved source and crop binding

Original supplied PDF/PNG bytes and all three canonical crop bytes are unchanged. Their declared physical page1,150dpi,rectangles and printed page ranges remain unchanged. The prior independently rasterised PDF crops remain pixel-identical to those unchanged canonical crops. All continuations and lower competency/value/PCI boxes previously inspected still apply. No explicit unit lesson count appears; all three allocation fields remain null. DRAFT/publication/capture caveats are preserved.

Originals:

- `CBE_Curriculums/Grade 10/STEM/Grade10_CoreMath.pdf`: `700b55379210dda0ee24561d43a872f965eba9568ec8092b6e9116d7f3609b2c`.
- `CBE_Curriculums/Grade 10/STEM/Grade10_CoreMath.png`: `ec00ae54ca37365d9a8a0aa1b6edafb3a18deda56565abb9983be5d64a4dd017`.

| Current source JSON | SHA-256 |
|---|---|
| `coremath_1_1.json` | `3f6b0e7f72ab8d9039a8cdaafa9a291e7d05939e917256f27023672adb160fcb` |
| `coremath_1_2.json` | `533a4d3973b7a1aec806e47a85fe2f05be0c1606f5de0c83274f504294fc028d` |
| `coremath_1_3.json` | `a3724a092451ef06963c46a4a4f65161e6618b8ac5b0303c7e94e809dcbec207` |

| Unchanged canonical crop | SHA-256 |
|---|---|
| `data/curriculum_expansion_2026-11/sources/coremath_1_1_source.png` | `f53737b3a5115509af7aa5f47b678dd1cf628a0fb00dd3724fef34d831b906de` |
| `data/curriculum_expansion_2026-11/sources/coremath_1_2_source.png` | `dd0269249f57784269456348c9c5b3db5a3308fe00776879af3cdbae8cca1559` |
| `data/curriculum_expansion_2026-11/sources/coremath_1_3_source.png` | `15fec579e6ced6194a209fc26d477228356eea111023fea791b62e2ea807f8a8` |

## Evidence and limits

`evidence/core_numbers_source_recheck_binding.json`, SHA-256 `3b3f25fe5a894ddc447763ff968be6fd0be252b51cc32ec3ef97da73276cf978`, preserves current full records, hashes, exact recursive differences and all10 check results. Current immutable snapshots are `evidence/coremath_1_{1,2,3}_source_recheck_snapshot.json`. The initial binding/evidence and finding detail images remain preserved.

No repeated full-source review is claimed: the initial complete printed1–6 comparison carries forward through the exact limited diff and unchanged image bindings. No author/source/pipeline/acceptance/output mutation was performed. Review evidence only was written. No online download or bypass was attempted; the authorised local captures remain the reviewed source.
