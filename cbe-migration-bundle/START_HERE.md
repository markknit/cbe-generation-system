# START HERE — Kenya CBE Lesson Plan Generation System
## Migration Bundle, New Non-Profit Business Account, April 2026

> Read this first. This bundle exists to restart the project under a new
> Anthropic non-profit business account. The project itself is unchanged —
> same goal, same server, same KICD curriculum. Only the account is new.

---

## Bundle contents

```
cbe-migration-bundle/
├── START_HERE.md                      ← you are here
├── HANDOFF_PROMPT.md                  ← user's verbatim instructions for the new session
├── CLAUDE.md                          ← operational standards (auto-read by Claude Code)
├── PROJECT_CONTEXT.md                 ← full project history & design principles
├── session-handoff-2026-04-26.md      ← detailed handoff from final session before migration
├── generated-content/                 ← all .docx/.html/.md outputs to date
│   ├── Grade 10 Bio/
│   │   ├── Bio 1.1/                   (Introduction to Biology)
│   │   ├── Bio 1.3/                   (Cell Structure and Specialisation)
│   │   ├── Bio 1.4/                   (Chemicals of Life — the EXEMPLAR; see below)
│   │   └── Bio 2.1 Plant Nutrition/   (L1–12)
│   └── Grade 10 Math/                 (2.2 Reflection & Congruence, 2.3 Rotation,
│                                       2.4 Trigonometry 1 — multi-format)
└── training-and-templates/            ← reference docs from Project_update_040726
    ├── Overview to Claude.docx        ← READ FIRST after START_HERE — central new instructions
    ├── ! CBE Scheme of Work Template for AI.docx    ← new template structure
    ├── CBE SoW Biology Grade 10.docx                ← official KICD curriculum
    ├── Chem of Life CBE Outline.docx                ← KICD outline for sub-strand 1.4
    ├── Sensemaking .docx                            ← sensemaking strategies reference
    ├── Values, Competencies and Skills and .docx    ← CBE values/competencies reference
    └── Appendix F  Science and Engineering Practices in the NGSS - FINAL 060513.docx
                                                    ← NGSS SEPs reference (the 8 practices)
```

**Reading order:**
1. `START_HERE.md` (this file)
2. `HANDOFF_PROMPT.md` — the user's intent for the migration in their own words
3. `training-and-templates/Overview to Claude.docx` — the central new instructions
4. `training-and-templates/! CBE Scheme of Work Template for AI.docx` — new structure
5. `generated-content/Grade 10 Bio/Bio 1.4/` — the exemplar to model output on
6. `CLAUDE.md` — current operational standards (to be reconciled)
7. `PROJECT_CONTEXT.md` and `session-handoff-2026-04-26.md` — for in-flight threads

---

## The exemplar: Bio 1.4 Chemicals of Life

Per `Overview to Claude.docx`, the **Chemicals of Life** lesson sequence in
`generated-content/Grade 10 Bio/Bio 1.4/` is the user's exemplar — the gold
standard for the desired output. It includes the user's three intended
deliverables per sub-strand:

- `Biology_Chemicals_of_Life_CBE_LessonSequence 2_COMPLETE (1).docx`
- `FINAL_EXPLANATION_Chemicals_of_Life.docx`
- `SUMMARY_TABLE_Chemicals_of_Life.docx`

The phenomenon used is a **blood glucose graph** (rise after eating, gradual
return to baseline) over a 6-lesson sequence.

> Note: The session-handoff-2026-04-26.md describes a different Bio 1.4
> (Kipchoge marathon, 5 lessons) generated in today's claude.ai sandbox. That
> output was a separate exercise that pre-dated the user supplying the
> exemplar. The exemplar in this bundle is canonical; the Kipchoge version
> should be considered superseded unless the user says otherwise.

### The exemplar's structure — what to model new sub-strands on

**Top-level sections (per sub-strand):**

| Section | Content |
|---|---|
| A | Sub-Strand Overview |
| B | Lesson Sequence |
| C | Sample Summary Table Template |
| D | Sample Final Explanation Template |
| E | Differentiation and Inclusion |

**Section A (Sub-Strand Overview) sub-rows:**

Basic Information · Learning Outcomes · Core Competencies Developed · Values
Promoted · Pertinent and Contemporary Issues (PCIs) · **Career Connections** ·
**Focus for Lessons** · Anchoring Phenomenon · Storyline Thread · Key Inquiry
Questions / Driving Questions

**Per-lesson structure (within Section B):**

| Section | Content |
|---|---|
| A | Specific Learning Outcomes (Knowledge / Skills / Attitudes) |
| B | Overview |
| C | Lesson Implementation Framework |
| D | Teacher Reflection |
| E | Summary Table Prompt (3 structured questions) |

The Summary Table Prompt asks students:
1. *What did I observe?*
2. *What did I learn?*
3. *How does this explain the phenomenon?*

— with embedded notes like *DQB Started, Initial Model Created* and *Model Revised*.

---

## What's new (vs. the structure documented in CLAUDE.md)

The exemplar and `Overview to Claude.docx` together introduce these elements
that aren't currently in `CLAUDE.md`'s template description:

**New top-level sections per sub-strand:**
- Section C — Sample Summary Table Template (student-facing tool)
- Section D — Sample Final Explanation Template (teacher cheat sheet)
- Section E — Differentiation and Inclusion (modifications for diverse learners)

**New rows in the Sub-Strand Overview:**
- Career Connections
- Focus for Lessons

**New per-lesson elements:**
- Section D — **Teacher Reflection** (replaces what CLAUDE.md describes as
  "Reflection Questions — Exactly 8 numbered questions" for students;
  these are now teacher-facing, prompting reflection on practice)
- Section E — **Summary Table Prompt** with the three structured questions
  above (replaces the more open-ended "italic summary paragraph")

**Reinforced (already in spirit, now explicit):**
- NGSS Science and Engineering Practices embedded in lesson activities
  (the 8 SEPs from Appendix F: asking questions, developing/using models,
  planning investigations, analysing data, math/computational thinking,
  constructing explanations, argument from evidence, communicating information)
- Sensemaking strategies as explicit teacher prompts (Sensemaking .docx is the
  reference for strategy options)
- Initial model drawing in lesson 1, revised across the sequence

---

## Settled: Section C is 5 columns

The user has confirmed (April 2026, prior to bundle finalisation) that the
per-lesson **Lesson Implementation Framework (Section C) is 5 columns**:

> Learner Experience · Resource Link · Teacher Moves · Sensemaking Strategy · Formative Assessment

This matches the exemplar (`generated-content/Grade 10 Bio/Bio 1.4/`) and the
new template (`! CBE Scheme of Work Template for AI.docx`).

**This supersedes** the 6-column version (with phase-label first column) used
in the most recent claude.ai sandbox generation of Biology 1.3. CLAUDE.md and
the generator scripts that produced the 6-column output need to be updated to
match. Specifically:

- Remove the `labelColW = 900` first column.
- Restore the 5-column width array (e.g., `[1872, 1872, 1872, 1872, 1872]`
  DXA — total 9360 = full content width at 0.75" margins on US Letter), or
  whatever balanced split the user prefers.
- Remove the phase-label cell logic and per-row phase colour coding tied to
  that column.
- Phase identification (Predict / Observe / Explain / DQB / Model Building),
  if retained at all, lives inside the Learner Experience cell content
  rather than as a structural column. Confirm with the user whether phase
  labels remain visible at all — the exemplar does not appear to surface
  them as explicit row markers.

The user explicitly invited follow-up questions in the handoff:
*"If there are any inconsistencies that you discover between the previous
and the new instructions, or any missing instructions or data required —
please do not hesitate to ask me for guidance."*

---

## Reality vs prior documentation

The session-handoff document under-tracked what actually exists. Update
`CLAUDE.md`'s curriculum coverage table to match:

| Sub-strand | Per CLAUDE.md | Reality in `generated-content/` |
|---|---|---|
| Biology 1.1 Introduction to Biology | Not started | Full lesson sequence + companion docs |
| Biology 1.3 Cell Structure and Specialisation | L1–3 of 20 | Full lesson sequence + companion docs |
| Biology 1.4 Chemicals of Life | L1–5 of 24 | Exemplar (6 lessons, blood glucose) — full + companion docs |
| Biology 2.1 Plant Nutrition | Not started | L1–12 + companion docs |
| Math 2.2 Reflection and Congruence | Not started | 6 lessons (multi-format: docx + html + md) + companion docs |
| Math 2.3 Rotation | Not started | Full sequence (multi-format) + companion docs |
| Math 2.4 Trigonometry 1 | Not started | Full sequence (multi-format) + companion docs |

Reconciliation actions for the new account session:
1. Update `CLAUDE.md` "Curriculum Coverage Plan" table with the actual state.
2. Update `CLAUDE.md` "Lesson Plan Template Structure" section to add the new
   top-level sections (C/D/E) and per-lesson sections (D Teacher Reflection,
   E Summary Table Prompt) per the exemplar.
3. Document the multi-format outputs (`.html`, `.md`) for Math sub-strands.
4. Add Career Connections and Focus for Lessons rows to the documented
   Sub-Strand Overview structure.

---

## Account migration checklist

- [ ] **API key.** Replace the old account's key in `.env` on jhm-spark.
      Check for hardcoded references:
      ```bash
      grep -rn "sk-ant" /home/markk/ares/cbe-generation-system/
      ```
- [ ] **Claude Code authentication.** Log out and re-authenticate on both the
      Windows machine and jhm-spark using the new account credentials.
- [ ] **Claude.ai project.** Recreate the project in the new account and upload
      `START_HERE.md`, `HANDOFF_PROMPT.md`, `CLAUDE.md`, `PROJECT_CONTEXT.md`,
      and `Overview to Claude.docx` as project knowledge. Add the new template
      and the Biology SoW too.
- [ ] **Anthropic non-profit programs.** If the new account qualifies for
      non-profit pricing or credits, make sure that's applied before any bulk
      generation run.
- [ ] **Token budget.** The previous account hit a Pro plan token limit
      mid-generation. Confirm the new account's plan is sized for the
      ~2,000-lesson target, or split generation across many sessions with
      `/compact` between them.

---

## Recommended first actions under the new account

1. Recreate the claude.ai project; upload the documents listed in the
   checklist as project knowledge.
2. Work through the account migration checklist.
3. Read `Overview to Claude.docx` and study the Bio 1.4 exemplar.
4. Reconcile `CLAUDE.md` against the exemplar:
   - Add new sub-strand-overview rows (Career Connections, Focus for Lessons).
   - Add new top-level sections (C Sample Summary Table Template, D Sample
     Final Explanation Template, E Differentiation and Inclusion).
   - Update per-lesson structure (D → Teacher Reflection, E → Summary Table
     Prompt with the three structured questions).
   - Update curriculum coverage table to reality.
   - Settle Section C as 5 columns (already decided — see "Settled" section
     above): update the generators to match the exemplar.
5. Inventory `data/outputs/docx/` and `generators/` on the Windows working
   copy to confirm the generator scripts that produced the existing outputs.
6. Resume content work — outstanding sub-strands per the updated CLAUDE.md
   coverage tracker (Biology 1.2, 2.2, 2.3, 3.x; remaining Math; Physics;
   Chemistry).

---

## Restoration prompt for the first new-account session

Paste this into the first chat under the new account, after uploading the
bundle's `.md` files and `Overview to Claude.docx` as project knowledge:

```
I'm restarting the Kenya CBE Lesson Plan Generation System under a new
Anthropic non-profit business account. The project itself is unchanged —
server jhm-spark, user markk, path /home/markk/ares/cbe-generation-system.

Read the following in order:
1. START_HERE.md
2. HANDOFF_PROMPT.md
3. Overview to Claude.docx
4. The Bio 1.4 exemplar (generated-content/Grade 10 Bio/Bio 1.4/)
5. CLAUDE.md

The exemplar shows the target structure including new sections (Teacher
Reflection, Summary Table Prompt, Differentiation and Inclusion, Career
Connections, Focus for Lessons) that aren't yet documented in CLAUDE.md.
Section C is confirmed as 5 columns (see START_HERE.md "Settled" section)
— the existing 6-column generator code needs to be updated to match.
Reconcile CLAUDE.md before generating any new content.

Don't begin bulk generation until reconciliation is complete.
```

---

## What changed and what didn't

The account is new. There are new content sections to add per the exemplar
and `Overview to Claude.docx`. Everything else is unchanged.

KICD curriculum, the salamander phenomenon for 1.3, the 5-phase pedagogical
framework, colour assignments, file naming conventions, the model string
(`claude-sonnet-4-6`), the server, the user, the directory layout — all
unchanged. The new instructions are explicitly described by the user as
enhancing rather than replacing. The Section C 5-column decision *does*
revert one structural choice the most recent test generation took (6-column
phase-labeled), but the rest of the formatting carries forward.

Don't re-litigate decisions documented in `CLAUDE.md` or `PROJECT_CONTEXT.md`
unless `Overview to Claude.docx` or the exemplar explicitly directs that
change.
