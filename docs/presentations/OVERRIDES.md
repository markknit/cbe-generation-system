# Overrides to the SeaVuria Build Manual

`BUILD_MANUAL.md` (v1.0, Oct 2026) is the teachers' design spec. Where it
conflicts with the repo's binding rules (CLAUDE.md "Branch Policy —
presentations"), **these overrides win**. Decisions recorded 2026-10-21 (Mark); still subject to the
teacher review.

| Manual says | Override |
|---|---|
| Footer text "© 2026 SeaVuria & ARES Education · CC BY-NC 4.0 …" (Sections 4, 13) | **DECIDED: `config/attribution.yaml` is the guide.** Render attribution only from it via `generators/lib/attribution.js`; never hardcode. Differences today: the manual hardcodes "2026" (YAML: current year at generation), says "ARES Education" (YAML: "SeaVuria and ARES"), omits the visible licence URL, the KICD alignment line and the AI-assistance credit (the YAML has all four). The lesson/subject/number part of the footer is generated; the credit text is not. **Open detail:** the YAML `lesson_footer` is a full sentence, too long for every slide. Use it in full on the title slide and last slide; a short per-slide line needs a new `slide_footer` key added to the YAML **on `main`** (not here). Until it exists, show only the generated lesson/subject part plus the logos on other slides. |
| ARES links only on the hidden "Lesson at a glance" slide, never on student slides (Section 10) | **DECIDED: links go on the slides**, clickable in Slide Show, as an **icon** (e.g. a projector or resource image) carrying the hyperlink, so no long URL clutters the screen. Only ares.local links, taken from `_data.json`. Each icon needs alt text and a visible label, and the plain URL goes in the speaker notes so printed copies keep it. Icon artwork and exact placement are for the teacher review. |
| Placeholder `http://ares.local/REPLACE-WITH-REAL-ARES-LINK` (Section 10) | Use the real links in `_data.json`. Links go through `scripts/check_resource_links.py`; a failing link blocks the build. No placeholders. |
| Builder corrects clear science errors and outdated terms in the deck (Section 12) | **DECIDED: flag, do not fix in the deck.** Do not diverge from the lesson plan. List each suspected error in the build log; lesson-plan content is changed only on `main` and the deck is then rebuilt from it. Reason: prevents drift between decks and lesson plans. |
| Builder inserts "Formative check to be added" placeholder slides (Section 8) | Allowed, but list in the build log. Do not invent assessment content. |
| Grade 10 science only; file names `Subject_G10_…` (Section 4) | Scope beyond Grade 10 science is undecided. **Maths is processed last**; Mark expects it will not need a separate process once teacher review is done (undecided). Do not extend the rules to other grades or subjects without a decision. |
| AI builds one deck at a time with a teacher check (Section 2) | Generator design waits on teacher review of the 4 example decks. Do not build until then. |
