# Core2.1 independent initial review — cross-review addendum

**Current verdict: HOLD for one confirmed teacher-key arithmetic error.** This supersedes the initial PASS verdict only; the initial report is preserved unchanged. Current fingerprint `92bc42e7dbbe057f0dd60204765af046bcb1deba60df16bd0f60fe6058aab7c9`.

After the full initial report was frozen, the parent relayed another independent reviewer's CSE4 finding. I then independently inspected `materials/coremath_2_1.json`, `items[id=CSE4].teacher`, and the actual current `MaterialsTeacherKey` Word body. Both say: “HalvingP’s coordinates would give(2,1),which isO rather than the correct image.”

P is(4,3), so origin-based halving is **(2,1.5)**, not(2,1). O is(2,1), and the correct reduction about O is **(3,2)**; the supplied genuine images P′(3,2),Q′(5,2),R′(3,4) are correct. Correct the false-method counterexample to(2,1.5) and remove the claim that it equals O. This requires no changes to the student task, intended images, source, final, rubric or lesson timing.

The reviewer-owned exact solution script already computed(2,1.5) correctly, but my initial review failed to flag its contradiction with the teacher-key sentence. This is a newly confirmed cross-review finding, not a changed author input or a newly invented task requirement. Propagation checks establish that the erroneous key reached the Word; they do not validate its arithmetic.

Immutable initial report: `coremath_2_1_initial_science.md`, SHA256 `1fdadc2d4f6dc89ef5dfd7016555fe4023a2262c1564c97f130c2a124a44e7e3`. Materials SHA256 `dd13f9f76d91ec3225c5a3a53816bc4a044c9377bbcccb1f575f353c6a1bed22`. Actual teacher-key Word SHA256 `a360bfd6745c417e3010a7e36dd276f1972add350a4558798ca58024b4599af1`. The expected fingerprint and material bytes remain unchanged from the initial binding. Evidence: `evidence/coremath_2_1_science_crossreview_finding.json`, SHA256 `628733230308c307fcba7c65dfda06a1f11ac33bafc1610f5390d33fb757f223`. No author/output/acceptance edits or builds were made. All other declared scope limits and evidence in the initial report remain applicable. A separately bound focused correction recheck is required before content PASS.
