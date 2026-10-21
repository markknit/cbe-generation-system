# Overrides to the SeaVuria Build Manual

`BUILD_MANUAL.md` (v1.0, Oct 2026) is the teachers' design spec. Where it
conflicts with the repo's binding rules (CLAUDE.md "Branch Policy —
presentations"), **these overrides win**. DRAFT: confirm with Mark and the
teacher review before treating as final.

| Manual says | Override |
|---|---|
| Footer text "© 2026 SeaVuria & ARES Education · CC BY-NC 4.0 …" (Sections 4, 13) | Render attribution only from `config/attribution.yaml` (SeaVuria credited as developer) via `generators/lib/attribution.js`. Never hardcode. Lesson/subject/number parts of the footer are generated; the credit text is not. |
| ARES links only on the hidden "Lesson at a glance" slide, never on student slides (Section 10) | OPEN CONFLICT. Hidden slides do not show in Slide Show, so links there are not clickable while projecting. Project rule: links must be clickable while projecting; only ares.local links. Needs Mark / teacher decision. |
| Placeholder `http://ares.local/REPLACE-WITH-REAL-ARES-LINK` (Section 10) | Use the real links in `_data.json`. Links go through `scripts/check_resource_links.py`; a failing link blocks the build. No placeholders. |
| Builder corrects clear science errors and outdated terms in the deck (Section 12) | Do not diverge from the lesson plan. Flag in the build log; lesson-plan content is changed only on `main`, never from this branch. |
| Builder inserts "Formative check to be added" placeholder slides (Section 8) | Allowed, but list in the build log. Do not invent assessment content. |
| Grade 10 science only; file names `Subject_G10_…` (Section 4) | Scope beyond Grade 10 science, and Maths, is undecided. Do not extend the rules to other grades or subjects without a decision. |
| AI builds one deck at a time with a teacher check (Section 2) | Generator design waits on teacher review of the 4 example decks. Do not build until then. |
