# Source preparation selected-module preservation recheck

Verdict: **PASS for a refresh explicitly restricted with `--modules` to the seven new Core units**. No confirmed blocker remains for that scoped invocation. The default unfiltered refresh retains its pre-existing inventory-reconstruction behavior and is not approved here as a way to preserve customised inventories.

Current preparation script SHA256 `7ce647ea18785ee65e9b309bdcf7cc8c38ed4b7ab65fe106ca6b85c35fb49bbc`;config SHA256 `c837d322e5203f2d7976960a7172af1afb6f9575c30f1100fe82a156d8628360` (unchanged from the initial override review). The initial report `source_override_code_review.md` remains immutable,SHA256 `bab2103cc580d2eb17b47135e927defcde8b4a67f253ec12ffabae5a3e9e7d4a`.

## Scope and exact diff

Parent's production guard found20 old inventory metadata resets from the general refresh's reconstructed next_action/count/allocation fields and reported restoring exact baseline bytes. Source/crop/OCR/canonical/artifacts were reported unchanged. The first review tested source override selection and preservation of inventories produced by the prior preparation code;it did not exercise existing custom metadata. Its fixture byte-identity result must not be generalised to arbitrary current inventory metadata. This follow-up explicitly covers that gap. I did not independently rerun production or perform recovery.

Compared current code with the exact initially reviewed script snapshot. The only change is the new `--modules` nargs+ option,set/known-ID prevalidation,preflight existence checks for every unselected inventory,and an early per-unit append-existing-row/continue branch. No source rendering,override,hash,OCR,crop,verification or config code changed. Unknown IDs and missing preserved inventory are rejected by parser.error before the temporary render context or any file mutation. For valid selections the unselected row is read for the aggregate and its original file is never rewritten;its crop/OCR is never touched.

## Independent fixture results

Five isolated scenarios,**39/39 assertions pass**,using the actual43 module IDs and real pdftoppm/Pillow on tiny PDFs. Each existing inventory has deliberately customised next_action,new_lesson_count,official allocation/prose and nested metadata,plus sentinel source crops/OCR. Every unselected unit also has canonical records and a content fingerprint.

- Selected seven,normal rendering:all36 unselected inventory files retain exact original bytes;their72 crop/OCR files and36 fingerprints are unchanged. All43 canonical source/materials/blueprint/manuscript records are byte-identical. Seven selected rows refresh from the replacement PDF and remain unaccepted;no unsupported source acceptance is inferred.
- Selected seven with `--reuse-render-dir`:same preservation and aggregate checks pass. Only the cached shared replacement render runs;normal mode renders the three base PDFs and one replacement.
- Unknown module:exit2,specific error,zero renderer calls and byte-identical complete before/after temporary tree.
- Missing one unselected inventory:exit2,specific error,zero renderer calls and byte-identical complete temporary tree;no partial update.
- Missing a selected inventory:refresh succeeds,all36 unselected rows remain exact and the complete43-unit aggregate is restored.

Every successful aggregate contains exactly43 unique original IDs,with the36 preserved rows semantically equal to their originals and seven newly located rows. Fixture totals are3 pilots,40 nonpilot units,40 located nonpilot packs,33 verified nonpilot packs and no still-blocked target. The custom count/allocation/next-action values in unselected rows survive in the aggregate as well as on disk.

## Operational boundary

Use the explicit seven-ID `--modules` invocation for the pending refresh. Without that flag the script intentionally retains its older all-unit reconstruction path. Base subject PDFs/renders/OCR are still opened even if all that subject's units are unselected;they remain read-only but must be available. Invalid crop/render/JSON encountered after selected processing starts can still cause a partial selected refresh;this change is a selection/preservation guard,not a transaction. The existing production before/after checksum guard remains valuable and should be retained.

No production preparation run,accepted source edits,author/pipeline mutation,rendered curriculum output changes or new acceptance occurred in this review. All fixture roots were temporary and removed. Source-content transcription verification and independent lesson review remain separate.

Evidence: `reviews/batch_07/evidence/source_override_scoped_core27/fixture_checks.py`, `fixture_results.json`, `reviewed_prepare.py`, `exact_diff.patch`, `binding.json`. Exact script bytes remain saved for the next production guard/recheck.
