# Content-acceptance evidence bundling — narrow code review

**Verdict: HOLD for two confirmed new-guard issues.** Reviewer: core27. Frozen 2026-11-15T01:41:15.103856+00:00. Exact reviewed helper SHA `ea16845449fc2d858780af782bf6b66539bb6cf857a8f47221e88830c14183f4`;prior immutable version-guard helper SHA `cd65aa16966638bea2d22d3f1208bdbd3b7d4a585618e9cc660fd011401aa4a1`. No production helper execution,packaging,acceptance/progress/receipt mutation or author edits.

Reversing only the new four-line evidence collection/validation block and added parent-list expression reconstructs the frozen prior helper byte-for-byte. Thus archive basename/no-overwrite guard,latest dated audit selection,nine-row/module assertion,all18actual Word/PDF hash checks,report/fingerprint guards and other prior packaging code are unchanged. The review covers this delta,not successful production packaging.

**PRE-C27-1: containment check is lexical.** `Path.is_relative_to(b)` does not normalise `..` or resolve symlinks. Read-only path counterexample `data/curriculum_expansion_2026-11/../outside.md` passes the new lexical check while its resolved path is outside the resolved base. If a CA entry points to such an existing file with its matching SHA,the new guard admits it. The later lexical `relative_to(b)` yields a parent path for the ZIP member. No file was created or helper executed for this proof. Resolve both paths,check actual containment,and normalise verified paths back to the base-relative representation used by the archive. Do not claim this guard ensures real containment as written.

**PRE-C27-2: validation runs after acceptance-state write.** The existing `artifact_acceptance.json` write precedes the new CA evidence checks. A missing file,wrong SHA or failed containment check therefore aborts after the helper has already recorded a new accepted artifact state. New evidence validation must complete before the first mutation. This is demonstrated by exact statement order,not a production invocation.

The actual legacy Essential1.3 CA has one report entry: `reviews/batch_03/essmath_1_3_initial.md` under the workspace base. It exists,resolves inside the base and matches SHA `becca2020de6292767ff7410167da1ea970b6c7ad902c04806ddee53b87c09db`. Its parent and parent/evidence are correctly added. Read-only enumeration selects37files:the batch03initial/layout reports and35module-prefixed evidence files. All37resolve inside the base and all are Essential1.3prefixed;no other-module evidence/assets were selected by these added parents. Every explicit CA evidence report is directly included in the set even if its basename is not module-prefixed;set semantics deduplicate repeated paths.

Consequently the added selection logic addresses the real missing legacy-parent issue. It collects all explicitly declared CA reports and the module-prefixed evidence under their parents/evidence directories. It does not recursively interpret arbitrary report links or promise inclusion of non-prefixed transitive references. A future batch07closure entry will add its own parent/evidence directory when actually present in CA;this review does not invent that pending acceptance entry or claim its SHA was checked already. The currently accepted legacy CA fingerprint is from the old revision and is not an authorisation to package the newly corrected content.

Evidence:

| File | SHA-256 |
|---|---|
| `evidence/package_review_evidence_core27/reviewed_package_helper.py` | `ea16845449fc2d858780af782bf6b66539bb6cf857a8f47221e88830c14183f4` |
| `evidence/package_review_evidence_core27/proof.json` | `9a8c65311d888de9a1810667f801ea816178817e983a419c5231adc31883c996` |

The proof records the exact diff,reverse-delta equality,legacyCAhash/report checks,all37selected hashes and the lexical counterexample. Existing frozen archives/receipts were not altered. Await focused closure after the two guard corrections;no broad curriculum/source/math review is required.
