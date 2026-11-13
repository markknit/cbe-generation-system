# Reviewed pilot checkpoint

**Independent review and corrections completed on 2026-11-12 after Mark explicitly resumed the task.** Read [INDEPENDENT_REPORT.md](INDEPENDENT_REPORT.md) for the current results and [Review_Package_Reviewed.zip](Review_Package_Reviewed.zip) for corrected artifacts. Three complete initial reviews remain unchanged; separate focused rechecks confirm all 18 original finding instances plus two minor Science follow-ups were addressed. Teacher/classroom confirmation, partner R1 ingestion support and usage/correction-cost measurement remain open.

A second server restart interrupted the first three reviewer attempts before they saved reports. Three fresh subject reviewers then completed the task using progressive on-disk checkpoints. Do not rerun those reviews simply because the session is new. The reviewed deliverables are 27 DOCX and 27 PDF across 31 lessons; the original 21/21 ZIP is a pre-review snapshot. Changes are local/unpushed; derive the current commit/ahead state from git.

The following is the **historical reboot resumption plan, now completed**. Wider generation, promotion and publication require the next user decision; they are not implied by resuming this checkpoint.

After reboot:

1. Run the repository’s `/restart` verification in `/home/markk/ares/cbe-generation-system` on `main`. Do not regenerate the existing drafts simply because the session is new.
2. Follow Mark’s explicit resume instruction: **“Resume the pilot and run the three independent review agents.”** Keep all AI work in ChatGPT/Codex; do not resume the old paid API pilot.
3. Use one fresh Codex reviewer per module: `essmath_2_8` (9 lessons), `coremath_2_5` (12 lessons), `gensci_2_4` (10 lessons). Use the inherited model/settings unless Mark requests otherwise. Give each reviewer `reviews/REVIEW_BRIEF.md`, its source JSON/crop, blueprint, materials, module and rendered documents. They should inspect these before the author’s internal review or REPORT.md. Each writes only its own findings file, for example `reviews/independent/<module>.md`; no concurrent edits to manuscripts or shared code.
4. Independently solve numeric tasks, verify substantive outcome coverage and source wording, trace references, inspect assessment answers and review scientific accuracy, practical safety, prerequisites and pacing. Record unread sources or incomplete review as pending, not clean. Compare older baseline modules only after the new manuscript review and disclose different teaching durations.
5. Triage findings, preserve the original verdicts and record corrections. Rebuild affected artifacts and rerun the relevant local gates. Use at most two correction passes before reporting unresolved teacher judgements. Return a pilot quality/cost report before any wider generation or promotion.

Verified at this checkpoint: 3 modules, 31 lessons, 21 DOCX, 21 PDF, 47 registered calculations. Existing local contract/R1 schema/link/consistency checks passed in the build. Partner rendering worked, but ingestion failed because the installed partner schema is R0 (`1.0.0`), rejecting R1 (`1.1.0`) and `belowExpectations`. This known delivery dependency is not a reason to downgrade the pilot schema or edit the partner checkout unasked.

Use the canonical directories here: `sources/`, `blueprints/`, `materials/`, `manuscripts/`, `modules/`, `outputs/` and `reviews/`. `Review_Package.zip` and REPORT.md are the original build snapshot. The untracked `Review_Package/` directory is an extracted copy: all 68 files matched the committed ZIP before reboot. Preserve it; do not stage duplicate files or use it as the editing source.

Before this checkpoint commit, `main` had two local/unpushed commits, `9d8bb00f` and `4e433620`. Re-derive current ahead/behind state after reboot. No push, promotion or Drive publication is authorized by this pause checkpoint. Actual subscription usage and teacher correction effort remain unmeasured; no numerical cost saving or independent quality advantage has been established.
