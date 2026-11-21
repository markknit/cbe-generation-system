# Checkpoint utility correction recheck

Verdict: **HOLD for one remaining content-evidence false-PASS**. Reviewed utility SHA256 `b86189b9ea656d92a35e028a9ec429ccdc74ee554e4106052752c467deec3c15`; exact reviewed bytes saved as `evidence/checkpoint_integrity_core27_recheck/reviewed_utility.py`. The initial HOLD report remains unchanged (SHA256 `4be67bb3a3c9315e3c22965f5874de866a8a978b9c9b1f3f2249b7319bae6bbb`). No production verifier run or production-data edits occurred.

## Closed defects

The corrected code now checks explicit artifact acceptance verdict/fingerprint/exact19artifact hashes/nonempty artifact evidence/current report hashes; legacy fallback is explicitly labelled and requires frozen scoped-review-pass plus equality of every archived review file to its current counterpart. It compares exact19 output basenames with total cardinality, rejects empty/duplicate/incomplete manifest coverage, and recomputes the actual archived canonical fingerprint including declared assets and implicit legacy images. UTC run time is recorded.

All original seven fixture scenarios have the intended result: baseline exit0; artifactHOLD/changed report,wrong nine types,empty member manifest,changed archived canonical,bad receipt SHA and bad member SHA exit1. Fixtures were rebuilt with complete canonical records and the **actual curriculum_pipeline.content_fingerprint implementation** (read-only copy in each temporary scripts directory), rather than the original constant stub, so the new archived-fingerprint comparison is meaningfully exercised.

Additional fixtures: valid legacy fallback passes with `legacy_frozen_manifest_and_review_hashes`; bad legacy verdict,changed archived review,missing implicit image,changed declared asset,duplicate manifest row and bad explicit artifact hash each fail for the expected reason. Both explicit and legacy successes record UTC/mode correctly. This closes the four principal initial defects.

## Remaining confirmed issue

**CPI-C27-R1 — empty content review evidence is accepted.** A content_acceptance record with accepted verdict,current fingerprint,zero unresolved errors and `evidence:[]` produces exit0/errors[] even though no independent content report hash is checked. This was explicitly recommended in initial finding1 and is the remaining asymmetry with the new nonempty artifact-evidence guard. Require a nonempty content evidence list before iterating it. Otherwise a missing content-report binding is invisible to the reviewed-checkpoint gate. The fixture changes only this evidence list from the valid baseline.

15 isolated scenarios were executed:14 match expected exits;the empty-content-evidence scenario is the sole unexpected pass. Full scenario/error/mode/time evidence: `evidence/checkpoint_integrity_core27_recheck/fixture_results.json`; runner: `fixture_checks.py`. No fixture roots remain.

## Retained limits

The verifier still hashes its designated listed reports rather than semantically rereviewing lessons/layout. Trusted receipt/acceptance metadata is not a security signature. This review does not assert any real package has empty content evidence or a corrupt artifact. The utility writes its own integrity report;“read-only” excludes author/output/acceptance regeneration. Missing/malformed inputs may raise and leave a previous integrity JSON,so callers must require the current successful process and fresh UTC. `manifest_entries_verified` still counts attempted entries even on mismatch;errors correctly fail the run,so this is a nonblocking report-label/count issue. All production archives and classroom performance remain outside this focused code recheck.
