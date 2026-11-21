# CA evidence guard — focused closure

**Scoped PASS: PRE-C27-1 and PRE-C27-2 closed.** Reviewer core27;frozen 2026-11-15T01:46:01.812567+00:00. Helper SHA `b1c295311838b7c8d24720e61ff80de0eaecf8386f4e8fed5e1d7e84e580305a`. This is not an overall packaging PASS:an independently preserved self-manifest blocker is recorded separately in `package_self_manifest_review.md`.

Compared exact current bytes with the immutable initial HOLD helper. CA evidence validation now immediately follows accepted-content loading/fingerprint checks and precedes every mutation. The evidence list must be nonempty. Each entry resolves to an actual file within `b.resolve()` and must match its recorded SHA. The verified resolved path is normalised back to `b / relative_path` before collection. The previous late validation block is removed. Parent selection and prior archive/date/artifact guards are unchanged by this correction.

Four exact-helper executions in isolated fixtures passed the negative checks:resolved parent escape,symlink escape,bad report SHA,andempty evidence. Each raises before any write. Full before/after hashes of every fixture file match,including sentinels for artifact acceptance,reviewed manifest,receipt andprogress;no new archive exists in these cases. Bytecode writes were disabled. The copied production helper was not modified.

A positive isolated fixture uses synthetic18artifact placeholders plus a copied actual-byte batch03legacyreport and a separate synthetic batch07CAclosure. The legacy CA path includes an absolute `..`alias inside the base;normalisation succeeds. Its constructed ZIP contains both declared CA reports,the legacy layout report and module-prefixed evidence;the actual legacy report bytes match exactly. No absolute/parent ZIP paths or unrelated sentinel asset are included,andCRCpasses. These six CA-selection assertions pass. Complete manifest SHA verification then fails for the separately reported self-manifest issue;no successful complete package is claimed. No production helper was executed.

Evidence:

- `evidence/package_review_evidence_core27/closure_reviewed_helper.py` SHA `b1c295311838b7c8d24720e61ff80de0eaecf8386f4e8fed5e1d7e84e580305a`.
- `evidence/package_review_evidence_core27/closure_attempt_proof.json` SHA `b4b96d8d4560e7625ab8c541f8cc9e99a560686bbf323107cdae69f51185f619`;exactdelta,four negative before/after hash sets,six positive CAchecks and separate self-manifest mismatch.
- Isolated cases retained under `evidence/package_review_evidence_core27/closure_fixtures_v2/`. Synthetic output placeholders do not represent curriculum artifacts or final acceptance.

The initial helper HOLD/report and reviewed bytes remain immutable. No author,archive,production acceptance,receipt orprogress files were changed by this review. Final helper readiness awaits the separate manifest closure.
