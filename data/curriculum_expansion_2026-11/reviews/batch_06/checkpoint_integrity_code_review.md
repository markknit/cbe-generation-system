# Checkpoint integrity utility — independent code review

Verdict: **HOLD for the advertised reviewed-checkpoint integrity gate**. Review of `evidence/procedures/verify_reviewed_checkpoint.py` SHA256 `d2dda724767f05e985762fa7b233c0c719293548d439c84212e6c2ea365a6c19`. No production full-script run, acceptance, build, render or production-data edits were performed.

## Confirmed false-PASS paths

1. **Artifact-review acceptance and its evidence are unchecked** (lines46–54). Only content_acceptance is loaded. A present artifact_acceptance with verdict HOLD and a current layout report changed from its bound hash both produce exit0/errors[] in the isolated fixture. This breaks the intended chain from actual delivered artifacts to independent final review. Require accepted artifact verdict/current fingerprint,nonempty evidence and correct current report hashes; require its exact artifact path/hash set to match current and archived delivery files. Also require nonempty content evidence rather than accepting an empty evidence list.
2. **Suffix counts do not verify the required nine document types/pairs** (lines55–63). Nine `Demo_WrongType0…8.docx` and nine matching wrong-type PDFs plus data.json pass. Missing FinalExplanation/teacher key or other required types can therefore be hidden by substitute names. Compare exact expected9×2+1 path/type sets,not only totals,then compare each hash against both archive and artifact acceptance. Exact relative paths also prevent alternate directories from satisfying counts.
3. **Packaged canonical bytes are not bound to the claimed packaged fingerprint** (lines44–51). Fingerprint is calculated only from current local canonical inputs and compared to acceptance/manifest strings. An archive containing a different manuscript with a matching internal member hash still passes if its manifest claims the current accepted fingerprint. Fixture demonstrates this. Verify packaged fingerprint-input paths/bytes against current bound inputs,or recompute the fingerprint from archived canonical inputs/assets using the same algorithm. Merely copying a fingerprint string into the manifest does not attest archived source/material/lesson bytes.
4. **Manifest coverage is not enforced** (lines31–40). `files:[]` passes,reporting zero verified manifest entries while all other checks succeed. Missing or duplicate manifest rows are not rejected; nonartifact members can be absent from the member-hash list. Require each expected archived nondirectory member exactly once,with a documented exception for the delivery manifest itself (which cannot self-hash); reject duplicate paths. The trusted whole-ZIP receipt SHA still protects frozen bytes,so this is a member-manifest completeness/packaging-validation gap,not a claim that ZIP corruption defeats SHA256.

## Reporting and operational limits

- `manifest_entries_verified` increments even for mismatching/missing entries (line40). Rename to checked or increment only after success; the errors/exit status currently still reject those failures. This is misleading count reporting rather than a false overall pass.
- Script writes `evidence/checkpoint_integrity_2026-11-14.json` (lines85–86),so “read-only” means no source/output regeneration or acceptance changes,not zero filesystem writes.
- Missing files/malformed schemas raise rather than producing a structured failure receipt. This fails closed via nonzero exit but may leave an older integrity JSON behind. A caller must require successful completion/current run metadata and never treat a preexisting report as fresh success.
- Receipt byte/entry counts and manifest lesson counts are not compared. Totals are recalculated from current manuscripts; those numbers do not independently validate manifest metadata. No fixed33-unit check is needed if authored-set coverage is the intended criterion,provided the authored inventory is the agreed scope.
- Valid CRC,receipt SHA,listed-member SHA,local-content fingerprints,content-report hashes and duplicate module coverage checks are sound in their stated narrow role. This review does not repeat semantic/layout/classroom acceptance or audit every real archive. No confirmed corruption of an existing package is alleged.

## Isolated verification evidence

Executed the unchanged utility via subprocess in seven temporary fixture roots. A minimal fake `curriculum_pipeline.content_fingerprint` returning a known accepted fixture fingerprint isolates utility control flow without importing/writing production pipeline state. Minimal delivery bytes test naming/hash logic,not valid Word/PDF parsing (which this utility does not implement).

Baseline: exit0. Four defect fixtures above: exit0/errors[] (unexpected for the intended gate). Bad receipt-SHA and bad member-SHA controls: exit1 with the correct respective error. All temporary roots were removed; only review evidence files remain.

Reproducible fixture runner: `reviews/batch_06/evidence/checkpoint_integrity_core27/fixture_checks.py`; exact outputs: `fixture_results.json`. No production verification utility execution occurred. Recommendations are scoped to verification; no author/pipeline/utility edits were made.
