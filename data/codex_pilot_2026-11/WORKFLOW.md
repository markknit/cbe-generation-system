# Pilot production and acceptance workflow

This is the OpenAI-only evaluation authorized by Mark on 2026-11-12. Work is authored in the Codex session. Scripts below are deterministic authoring records, exporters and checks; they do not call any model endpoint. Existing ARES matching runs against the local database.

## Source and lesson decisions

Read each `sources/<module>.json` and its PDF crop. Treat original PDF pixels as authority over OCR. Requirements and source provenance are preserved separately from lesson prose. The Core 2.4 table is missing/obscured in the available PDF; Core 2.5 was selected instead. No claim about the identity of March/July mathematics sources is needed for this pilot.

The blueprints allocate 9 Essential, 12 Core and 10 General Science 40-minute lessons. These are reasoned teaching designs, not official allocations. A source table without a count is not evidence for an eight-lesson allocation. New and old units have different lengths, so comparisons must be qualified.

## Rebuild

From the repository root, with the existing venv:

```bash
venv/bin/python scripts/codex_pilot/complete_source_records.py
venv/bin/python scripts/codex_pilot/author_essential.py
venv/bin/python scripts/codex_pilot/author_core.py
venv/bin/python scripts/codex_pilot/author_science.py
venv/bin/python scripts/codex_pilot/diagrams.py
venv/bin/python scripts/codex_pilot/build.py essmath_2_8 coremath_2_5 gensci_2_4
CBE_DATA_DIR="$PWD/data/codex_pilot_2026-11/modules" node scripts/validate_corpus.js
ARES_RECOMMENDER_SCRIPT="$PWD/scripts/codex_pilot/resource_recommender.py" ATTRIBUTION_YAML="$PWD/data/codex_pilot_2026-11/attribution.yaml" CBE_DATA_DIR="$PWD/data/codex_pilot_2026-11/modules" CBE_OUTPUT_ROOT="$PWD/data/codex_pilot_2026-11/outputs" CBE_FE_ISSUES_DIR="$PWD/data/codex_pilot_2026-11/reviews/fe_issues" node generators/generate.js --all
venv/bin/python scripts/codex_pilot/render_pdfs.py
```

Use the pilot-only `ATTRIBUTION_YAML` override so this Codex-authored evaluation does not inherit Claude/Anthropic drafting credit. Companion documents read the same pilot configuration. The pilot resource wrapper applies `resource_policy.json`: no selected recommendations during independent assessment, and no out-of-scope carboxylic-acid naming suggestions. Contract-required search fallbacks remain for later teacher preparation; do not use them during assessment.

`CBE_DATA_DIR` must be absolute for the renderer’s require(). The pilot FE issue directory avoids inheriting findings attached to older content with the same curriculum identifiers. Its use does not certify the new content: the separate review record states which reviews have actually occurred. Do not clear or delete original review logs.

## Review standard

The writer’s record is not an independent verdict. A fresh reviewer should receive the source requirements, crops, companion materials, modules and assessment keys, but not the writer’s self-evaluation. Review all outcomes, solve every exercise independently, check calculations not registered in code, trace all card/table references, and inspect feasibility, safety and rendered documents. Return exact locations, evidence, severity and proposed correction; do not invent issues to meet a quota. Preserve the initial findings and the later disposition.

Use at most two correction passes before recording unresolved judgement calls for a teacher. Recheck affected calculations, materials, assessment and rendered output after a correction. A failed call, unread source or incomplete review is pending/failed, never clean. Same-family model reviews can share errors. Teacher classroom confirmation remains separate from model review.

## Acceptance boundaries

- Structural/contract, resource-link and cross-document gates pass.
- Every declared outcome maps to an observable task; reviewer checks the mapping’s substance.
- No unresolved confirmed mathematical/scientific error is accepted for release.
- Hypothetical data are labelled; published facts have attributable sources.
- Practical fallbacks disclose whether hands-on skill was actually observed.
- Student assessment contains no teacher exemplar answers.
- DOCX/PDF files are inspected and source/output hashes recorded.
- Pilot report distinguishes actual evidence from estimates and missing evidence.

Bulk generation, promotion, Drive publication and partner delivery require the later pilot checkpoint. The original API pilot is a separate experiment and its 7.65 USD ledger is not this pilot’s cost. Subscription usage and human review time are real costs; exact plan-credit consumption is not exposed to this session. No claim of zero total cost or numeric 43-module cost saving is justified yet.

## Reviewed-pilot checks and packaging

Run `venv/bin/python scripts/codex_pilot/audit_outputs.py` after rendering to verify the full nine-type document inventory, student blanks, attribution and final-resource policy and refresh artifact hashes. `render_pdfs.py` accepts optional module names (for example `gensci_2_4`) to limit conversions after a focused correction. Initial and correction review records remain separate; the correction limit is two passes.

`Review_Package_Reviewed.zip` is the corrected teacher-review snapshot. The original `Review_Package.zip`, extracted copy and `REPORT.md` preserve the initial draft. Current conclusions are in `INDEPENDENT_REPORT.md`.
