# Three-criteria check of Round 2 changes (2026-11-10)

Independent strict review (claude-sonnet-5-5, one pass per module, about $8 of the $20 cap) of 690 Round 2 edit/set records in
Biology, Chemistry, Physics and Mathematics. Criteria: matches the teacher decisions, matches KICD, scientifically correct and consistent
with the lessons. The mechanical four-level rubric records (197) were not re-checked. Per-record results: data/revised_2026-10_full/verification/<module>.json.
Limits: one reviewer pass (not two); it reads the lessons as they are NOW.

Result: 636 of 690 passed. 54 raised a concern. After reading each concern against the current text:

## Not real (45 records, no action)
- math_2_9 (36 records, r2-069..124): written before the lesson split, so their lesson numbers differ from the current numbering; the text is in the right place. math_2_9-r2-144 ("8 lessons = 320 min") is superseded; the lessons now read 13 x 40 = 520 min.
- phys_1_3 (6 records, les-auto-002..007): the 17 degrees C rise was reverted later; the current lesson uses 15 degrees C / 1.65 mm.
- math_2_5-r2-094: the reviewer checked the apothem figures and found them correct.

## Real, small, for a person to look at (9 items)
1. math_1_2-r2-fe-002/003: Final Explanation asks "nearest thousand" (answer Ksh 85,000); Lesson 7 says Ksh 84,800 "nearest hundred". The maths is correct but the FE differs from the lesson (the lesson is the arbiter).
2. bio_1_3-r2-fe-001/002: part (e) was removed from the FE because the lessons then did not teach field-of-view size estimation; the lessons now teach it (Lessons 4, 6), so KICD outcomes (a) and (b) are not assessed. Consider restoring (e).
3. phys_4_1-r2-fe-004: exemplar names "James Muriithi"; the teacher decision asks that a person like this be labelled fictional.
4. bio_3_2-r2-les-tri-001: "a low-pressure open system cannot direct oxygen-carrying fluid" is loose for the grasshopper (haemolymph does not carry oxygen).
5. chem_1_2-r2-fe-004: "Bohr proposed fixed energy levels because Rutherford could not explain flame colours" is a simplification (Bohr's evidence was the hydrogen line spectrum).
6. chem_1_5-r2-fe-auto-001: the prompt states the cause (more electron shells), so it partly gives away the answer (style point, not an error).
7. phys_3_1-r2-les-tri-001/002: alpha-decay wording in the Explain phase may still conflict with an adjacent sentence ("toward the belt").
8. phys_1_2-r2-fe-001: the exemplar sentence reads awkwardly (limits mixed); the numbers match the lesson (850 N/m x 1.5 m = 1275 N).

None of these is a clear scientific error that would mislead a learner. They are not fixed; nothing was changed by this check.

## Fixed afterwards (2026-11-10)
All 9 items were corrected (records `<module>-r2-vfix-NNN`, group R2-VERIFY-FIX, in the journals): math_1_2 FE back to 'nearest hundred' (Ksh 84,800, calculator 84,794); bio_1_3 cell-size question restored as part (f) with the lesson's own example; phys_4_1 'fictional' added at the exemplar; bio_3_2 'oxygen-carrying' removed; chem_1_2 Bohr clause reworded; chem_1_5 cause removed from the prompt; phys_3_1 awkward parenthetical removed. phys_1_2 needed no change (the sentence is already correct and clear). FE loop re-run on the 7 touched modules: all CONVERGED, no further edits. Rebuilt and validated (70 modules, PASS); journals and this folder refreshed.

## Journals in this package (updated 2026-11-10)
`Journals/` holds the four Round 2 journals (Round2_Journal_<Subject>.docx): only the changes teachers have not yet answered (Round 2 lesson and Final Explanation changes, built-in answers, the nine verification fixes, and Round 2 flags). The cumulative history of every change (including items teachers already answered) is Journal_<Subject>.docx in data/revised_2026-10_full/journal/. Round2_Lesson_Check_Review.docx (38 closest-review items + optional list, now including the nine fixes) sits beside this report.
