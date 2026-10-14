# Full Grade 10 revision run: queue (update as agents finish)
Folder: data/revised_2026-10_full (CBE_REVISED_DIR). Brief: REVIEWER_BRIEF.md (v3). Pilot sub-strands done: gensci_3_1 coremath_2_4 math_2_4 bio_2_3.
Order: bio, chem, phys, math, coremath, essmath, gensci. Concurrency: 6 agents. Status of a module = has change_records/<m>.json.
Per subject when complete: revise_build.py MODULES, build_revision_journal.js, run_lesson3_checks (LESSON3_OUT_DIR=outputs/v2), commit+push, short report.
Prompt template: "Revise sub-strand <m> (Grade 10 <Subject>). First read $F/REVIEWER_BRIEF.md completely (incl. 'Changes in this round' and 'Lessons from the pilot') and GUIDELINES_14.md. Scratch: <scratchpad>/full_<m>/. Report per brief."
