# Versioned package self-manifest — focused closure

**PASS: PSM-C27-1 closed.** Reviewer core27;frozen 2026-11-15T01:47:04.222950+00:00. Exact helper SHA `c03576bc9174873c43df04642ad56513236df1659a351d1dc82e6eecc6049a88`. Earlier CA guard findings remain closed. No production helper/package/acceptance/progress mutation or author edit occurred.

Compared with immutable self-manifest HOLD helper `b1c295311838b7c8d24720e61ff80de0eaecf8386f4e8fed5e1d7e84e580305a`:the only change defines `mp` before manifest construction,discards that exact path from `files`,and reuses it for the subsequent write. The manifest consequently covers all other ZIPmembers;the new manifest is added after construction without a self-hash. Archive/date/18artifact/CA/path guards and module evidence selection are unchanged.

Five isolated exact-helper scenarios pass. The four earlier negative guard cases were rerun (parent escape,symlink escape,badSHA,empty evidence),with every fixture file byte unchanged and no new archive. The positive case starts with an actual existing original ZIP and existing reviewed-manifest sentinel,then creates a distinct versioned ZIP using18synthetic artifact placeholders and valid legacy/new CA reports. Complete helper execution now succeeds. Independent assertions confirm original ZIP SHA unchanged,no self-entry,unique complete coverage of all other ZIPmembers,all member SHAchecks,CRC,actual-byte legacy report,newCAreport and legacy module evidence inclusion,absence of unrelated assets,and no absolute/parent member paths. This is an isolated integration proof,not curriculum artifact acceptance.

The current real Essential1.3CA now lists four reports (legacy batch03initial,corpus disclosure,focused correction recheck,root acceptance). Read-only checks confirm all four files resolve inside the base,exist,and match their recorded hashes. No current CA entry was invented or edited by this review.

Evidence:

| File | SHA-256 |
|---|---|
| `evidence/package_review_evidence_core27/manifest_closure_reviewed_helper.py` | `c03576bc9174873c43df04642ad56513236df1659a351d1dc82e6eecc6049a88` |
| `evidence/package_review_evidence_core27/manifest_closure_proof.py` | `aa2aaf6a5a37b056f08fb174b53da043320612ffbc4370f9e7d15ebfb869da00` |
| `evidence/package_review_evidence_core27/manifest_closure_proof.json` | `9fb1f56571b2f744c0fdeca72a0dc9e24d5d419befbf4d57a63c140ec5f77318` |
| `evidence/package_review_evidence_core27/manifest_closure_exact_delta.diff` | `5cc81258013a66f1b3400530ab0d0e5d2834f942be2fce83ff9e481983ef02df` |

Five cases are preserved in `evidence/package_review_evidence_core27/closure_fixtures_v3/`. Prior HOLD/closure reports and helper snapshots remain immutable. The helper is accepted within this narrow serial local-package scope;no whole-corpus production verifier/package run or classroom/partner acceptance is claimed.
