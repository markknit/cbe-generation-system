# Handoff Bundle — 2026-09-29

Start here. Everything Claude Code needs for the bounded project is in this folder.

## Read in this order
1. `INITIATION_PROMPT_bounded_project_v2.md`: how to copy this bundle to jhm-spark, and the prompt to paste into Claude Code
2. `HANDOFF_bounded_project_v2_2026-09-29.md`: the authoritative spec (Phases 0 to 8)
3. `HANDOFF_resource_link_quality_2026-09-25.md`: detail on the link-matching bug (still valid; referenced by Phase 1)

## Contents
| Path | Purpose |
|---|---|
| `config/attribution.yaml` | Single source of truth for attribution/licensing text; `{YEAR}` = current year |
| `audit_resource_links.py`, `resource_link_priority_targets.csv` | Link audit script and its flagged rows (baseline 34 / 25 / 174) |
| `samples/Attribution_Placement_Sample.docx` / `.pdf` | Where the header block and per-lesson footer go |
| `samples/quiz/` | Target quiz outputs for 4 lessons (Quick Check .pptx/.pdf, Answer Key .html/.pdf, source `_quiz.json`), plus the reference builder |
| `presentation_examples_deferred/` | Full presentation examples under teacher review. **Not in scope; do not build.** |

## Supersedes (ignore if found in the repo root)
- `HANDOFF_bounded_project_2026-09-26.md` and `INITIATION_PROMPT_bounded_project.md`
- `HANDOFF_grade10_regen_and_pipeline_2026-09-25.md` and `INITIATION_PROMPT_combined_regen.md`
- `INITIATION_PROMPT_resource_link_fix.md` (its scope is now Phases 1 and 2 here)
- `prototype/` (early process-oriented slide/quiz prototype)
