# Final delivery index — initial scoped HOLD

**HOLD — FDI-1.** The initial final index has two historical archive rows whose `receipt_path` resolves to the new replacement archive receipt rather than that row’s old historical receipt. Both original archive hashes themselves are correct.

The concrete correction is to point each historical `receipt_path` to its preserved `snapshot_directory/original_receipt.json`;the former live path can remain under explicit `current_receipt_path`. This preserves current versus historical evidence meaning.

Initial FINAL_DELIVERY_INDEX.json SHA256:`49a949ebe70e65f5e4922160ba25b95b21156c449939d9dc4f4648db81b9e555`. Unchanged status SHA256:`bf9740fbb535d83ecf938c40aead4ec4d9de3d8f29490cc00d6b0a1ac1f1b588`. Exact initial index/status snapshots and finding JSON are preserved in `evidence/final_delivery_index_review/`. This is only the initial link finding;all final count/archive checks and correction closure are reported separately. No author/index/archive changes were made by this reviewer.
