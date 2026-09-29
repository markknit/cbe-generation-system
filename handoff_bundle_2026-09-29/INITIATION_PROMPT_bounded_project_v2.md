# Initiation Prompt — Bounded Project v2
*Copy the bundle to jhm-spark, then paste the fenced prompt as the first
message of the Claude Code session.*

## 1. Copy the bundle to jhm-spark

From the folder where you downloaded `handoff_bundle_2026-09-29`:

```bash
scp -r handoff_bundle_2026-09-29 markk@jhm-spark:/home/markk/ares/cbe-generation-system/
ssh markk@jhm-spark
cd /home/markk/ares/cbe-generation-system
claude
```

## 2. Paste this prompt

```
This is a bounded project with fixed goals on this repo
(/home/markk/ares/cbe-generation-system). All handoff materials are in
handoff_bundle_2026-09-29/. Read, in order:
1. handoff_bundle_2026-09-29/README.md
2. handoff_bundle_2026-09-29/HANDOFF_bounded_project_v2_2026-09-29.md
   (the authoritative spec; it supersedes any earlier presentation or quiz
   handoff that may be in the repo root)
3. STATUS.md and CLAUDE.md, fresh from the repo

Goals:
- Fix the resource-link selection process so it stops returning exam
  answer keys and wrong-subject matches, with an automated check that
  prevents recurrence.
- Add a per-lesson Quick Check quiz (5-10 multiple-choice questions) as a
  .pptx/.pdf deck, plus a teacher answer key (.html/.pdf).
- Add the attribution and licensing text from
  handoff_bundle_2026-09-29/config/attribution.yaml to every sub-strand
  document, after every lesson, and on every quiz deck and answer key.
- Leave the pipeline ready for Grade 11, which starts right after this.

Hard constraints:
- Do NOT regenerate lesson plan content. Only re-run link matching, generate
  quiz content, and re-render documents.
- Presentations are deferred. Do not build a presentation generator;
  presentation_examples_deferred/ is reference only.
- All new code is parameterized by grade and subject (use the existing
  required --grade mechanism). Test on Grade 10 only.
- Keep additions compatible with ares-contract.schema.json; document any
  unavoidable impact.
- Attribution text comes only from config/attribution.yaml, with {YEAR}
  replaced by the current year.

Work phase by phase. Start with PHASE 0 (report the current state,
including anything earlier sessions already did on the link fix) and stop.
There are stop-and-report gates after Phases 0, 1, 2, 3, 4, 6 and 8. Do not
continue past a gate without my confirmation. Get a cost estimate
confirmed before any full-corpus run.

If anything is unclear or contradicts what you find in the repo, ask me
rather than guessing.
```

## Notes for you (not part of the prompt)

- **Phase 0 matters** because an earlier link-fix handoff may already be
  partly done on the server. Phase 0 makes Claude Code report that before
  touching anything.
- **Phase 1's design doc** is the gate that decides whether the link fix is
  a real process change or just another patch. Worth reading closely.
- **Attribution wording** (revised 2026-09-29): SeaVuria is credited as
  developer of the content and pedagogy. ARES is credited for technical
  implementation, with AI assistance (Claude) disclosed on the Production
  line and in the footer. There is no longer a claim that every lesson was
  reviewed, so the text stays accurate while teacher review is ongoing.
