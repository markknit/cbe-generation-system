# Package version guard — narrow independent review

**Verdict: PASS for the optional archive-name/preflight guard delta.** Current helper SHA256 `cd65aa16966638bea2d22d3f1208bdbd3b7d4a585618e9cc660fd011401aa4a1`. No production helper execution,packaging,acceptance/manifest/progress mutation or author edits occurred. The runtime proof uses an exact copied helper in an isolated reviewer fixture with a stub pipeline import and disabled bytecode writes.

Compared current bytes against the immutable helper retained by `package_audit_date_review.md`,SHA256 `5ad6ba255cd0d6dcf5c5271181a1d919422c70d98d797b465ffd7837f46cf7db`. Reversing exactly the six new preflight lines and restoring the former late `zp` assignment reconstructs that prior helper byte-for-byte. Consequently the per-module latest dated audit selection,report hash guard,accepted-content fingerprint guard,nine-row/module assertion,all18actual Word/PDF hash guards,manifest integrity checks and remaining packaging behavior are unchanged. This review does not repeat or broaden the earlier audit-date review.

The fifth optional command argument is used as the archive basename;omitting it preserves `{module}_Reviewed.zip`. `Path(name).name == name` and suffix `.zip` reject parent/absolute path forms and other suffixes on the current POSIX host. The archive path is now constructed before report selection/hash reads and all packaging writes. An existing destination raises `FileExistsError` with an explicit new-version instruction. There is no later hardcoded assignment to discard the caller’s version name. Version numbering is explicitly caller-selected,not automatically inferred.

Five isolated scenarios passed:

| Scenario | Observed result | Write proof |
|---|---|---|
| Omitted optional argument,existing default archive | `FileExistsError` before report guard | All fixture bytes unchanged |
| Explicit existing frozen version | `FileExistsError` before report guard | All fixture bytes unchanged |
| Invalid `../escape.zip` | basename `ValueError` | All fixture bytes unchanged |
| Invalid `.txt`suffix | suffix `ValueError` | All fixture bytes unchanged |
| New explicit `isolated_unit_Reviewed_v2.zip` | Passes new preflight,then fails the existing report-hash assertion as deliberately arranged | All fixture bytes unchanged;no new archive created |

The fixture contains real existing ZIP files and sentinels for report,artifact acceptance,reviewed manifest,package receipt and inventory progress. Every file’s SHA256 before/after each invocation agrees,including both frozen ZIPs. The stub canonical-fingerprint function is never called. Thus these are direct fail-before-write observations rather than inference from an exception alone. The original production helper remained byte-identical to the reviewed copy throughout.

Evidence under `reviews/batch_07/evidence/`:

- `package_version_guard_science_proof.py` — SHA256 `efe43418ef46893e1e8a1f86494a722690b94a367b4af013c4c85ac47f8e4921`.
- `package_version_guard_science_proof.json` — SHA256 `e90da0f24d2f077a5a21588abff5f7e89ca1d67347e399809871882b5ea3bda5`;contains exact diff,current/prior helper hashes,all fixture hashes and individual tracebacks/results.
- `package_version_guard_science_fixture/` — exact reviewed helper,isolated import stub and unchanged fixture files retained.

Scope is this preflight/version argument under the serialized packaging workflow. No successful production package or broader acceptance decision is claimed. Earlier review limits and teacher/partner acceptance remain separate.
