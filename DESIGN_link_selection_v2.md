# DESIGN — Resource-Link Selection v2

*Drafted 2026-09-29, Phase 1 of `handoff_bundle_2026-09-29/HANDOFF_bounded_project_v2_2026-09-29.md`.*
*Status: approved by Mark 2026-09-29; implemented in Phase 2 — see §7 for where the implementation differs from §4.*

---

## 1. Summary

The matcher in `src/ares_recommender.py` does not rank by relevance at all.
It gathers every item that matches **any one** of ~15–40 single-word queries,
many of which are curriculum boilerplate ("sub", "strand", "anchoring",
"phenomenon", "predict"). It then sorts that pool by channel quality, and
the first high-quality video that any stray word pulled in wins.
Answer keys win the same way because a Kenyan exam-prep channel is in the
top quality tier and nothing excludes answer material.

The fix below changes all four stages: build the query, retrieve candidates,
gate them, then rank them. It also adds a checker, sharing one config file
with the matcher, that runs inside `generate.js` and fails the sub-strand
when a bad match gets through.

## 2. Diagnosis

### 2.1 Baseline (reproduced exactly)

| Scope | Tier 1 (answer key) | Tier 2 (wrong domain) | Tier 3 (high repeat) | Slots checked |
|---|---|---|---|---|
| Handoff audit — **predict phase only** | **34** | **25** | **174** | 1,456 |
| Same rules, **all 5 phases** | 170 | 125 | (1,685 — not comparable¹) | 7,280 |

Tier 1 and Tier 2 are exactly 5× across all phases: the same bad pick is
repeated in every phase of an affected lesson, because the phase makes almost
no difference to what wins (see RC1).

¹ Tier 3's "reused 6+ times" rule inflates when all phases are counted: one
title used across a single lesson's 5 phases already counts as 5.

**Audit coverage gap:** `audit_resource_links.py` checks only `predict`, 20% of
the links that ship. The new checker (§4.7) checks all phases.

**Fill rate:** 7,280 / 7,280 slots contain a direct link and **0 are null**.
The matcher has never declined to match, so every weak match is currently
presented as a real recommendation.

### 2.2 Traced cases

Traced with the live DB (`data/ares_index/ares_content.db`, 1.57M rows)
using the production `_keywords()` / `_search()` code.

| Case | Shipped | Keyword that pulled it in | Where it came from | Better match in the same pool |
|---|---|---|---|---|
| Physics 2.1 L1 (Waves), predict video | "Anatomy of a skeletal muscle cell" | `anchoring` | "Anchoring Phenomenon" in `aresKeywords` (a pedagogy label); the video transcript mentions myosin *anchoring* | "Doppler effect introduction" — ranked **#2**, lost on a tie |
| Core Maths 2.9 L2 (Linear Motion), predict video | "Genetics vocabulary" | `strand` | The literal label "Sub-Strand 2.9" — present in **every** lesson (DNA *strands*) | bm25 top: motion/acceleration videos |
| Physics 3.3 L4 (Semiconductors), predict video | "The periodic table - classification of elements" | `semiconductor` (1 of 36 keywords) | A real but single-word hit (metalloids are semiconductors) | "05 Doping A Semiconductor" matches 5+ keywords; bm25 ranks it #1 |
| Physics 3.4 L2 (Electrostatics), predict reading — **Tier 1** | "topical-test-form-3-physics-electrostatics-2-answers" | `electrostatics` | Genuinely on-topic; channel "Kenya Curriculum Tools 2025" is in the tier-0 list; subject matched; PDF preferred | "Balloons and Static Electricity" (bm25 #1) |

"Genetics vocabulary" appearing in 14 lessons, mostly Maths, is explained by
RC2 below: every lesson's query contains `strand`.

### 2.3 Root causes

Tier 1 and Tier 2 have **different** root causes:

- **Tier 1 (answer keys)** is caused by RC4 alone. The answer key was a
  topically relevant document that should never have been eligible.
- **Tier 2 (wrong domain)** is caused by RC1, RC2 and RC3 acting together.
  An irrelevant item gets into the candidate pool, and nothing ranks it
  below the relevant ones.

| # | Root cause | Evidence |
|---|---|---|
| **RC1** | **Relevance plays no part in ranking.** The sort key is `(tier, is_storage, has_direct_url, subject_match, type, -hit_count)`. The one relevance term is last, and it is **broken**: `hit_counts` is keyed by row id (`rid`) but looked up by `r.kolibri_id`, so it is always 0. Among tier-0 Kolibri-storage videos the winner is whichever the earliest keyword happened to return. | `ares_recommender.py` `_search()` sort; the traces above |
| **RC2** | **Query pollution.** Each word of `topic + substrand + phase-boost` becomes its own OR query. That includes structural labels (`sub`, `strand`), pedagogy vocabulary (`anchoring`, `phenomenon`, `predict`, `phase`, `driving`, `question`, `board`, `model`, `ngss`, `cbe`), place names (`kabete`, `nakuru`), and phase boosts (`prior`, `knowledge`, `initial`). Any of these can bring in an item. | Physics 2.1 L1: 42 keywords, most not about waves |
| **RC3** | **Unordered retrieval.** Each keyword query is `LIMIT 150` with no `ORDER BY`, so for common words the rows that enter the pool are an arbitrary slice in rowid order, not the best 150. | `properties` has 3,259 matches; 150 arbitrary ones are taken |
| **RC4** | **No content exclusion.** Nothing filters answer keys or exam papers. The Kenyan exam channel is tier 0. `image` rows (1.43M) are not excluded from the reading pool. | Tier 1 trace |
| **RC5** | **No subject guard.** `subject_match` is only a late tiebreak. It also **can never be true** for General Science, Core Mathematics or Essential Mathematics, because it substring-matches `META.subject` ("Core Mathematics") against DB subjects ("Mathematics"). **97% of DB rows have subject "General"**, so the DB subject column alone can't be the guard. | DB `GROUP BY subject` |
| **RC6** | **No relevance floor.** `recommend_pair()` always returns `videos[0]` / `readings[0]` if the pool is non-empty. | 0 null slots in 7,280 |

## 3. Goals and constraints

- Stop answer keys and wrong-subject results from shipping. Prevent the same
  class of defect from coming back after future regenerations.
- When nothing is a confident match, say so clearly and give the ARES search
  link. Don't show a weak link as if it were a good one.
- Stay within `ares-contract.schema.json`, which is strict
  (`additionalProperties: false` everywhere). A resource record may be `null`
  (already allowed). **No new fields** such as confidence scores go into
  `_data.json`.
- Nothing is keyed to a grade. Word lists live in config and are keyed by
  subject family, so a new grade or a non-STEM subject needs no code change.
- No API cost. Matching stays a local SQLite FTS5 lookup, and re-rendering
  makes no API calls (verified: nothing under `generators/` calls the API).

## 4. Design

### 4.1 One config file shared by the matcher and the checker

New file: `config/link_matching.yaml`. Both `ares_recommender.py` and the
checker read it, so the rule that produces a link and the rule that checks it
can't drift apart. (That drift is the "fixed on symptoms, then re-fired"
pattern in STATUS.md.) It holds:

- `query_stopwords` — boilerplate/pedagogy/structure terms (`sub`, `strand`,
  `anchoring`, `phenomenon`, `predict`, `phase`, `driving`, `question`,
  `board`, `ngss`, `cbe`, `kenya`, `grade`, `lesson`, `final`, `explanation`, …)
- `exclude_patterns` — answer/exam material (§4.3)
- `subject_families` — which DB subjects each lesson subject may draw on (§4.5)
- `foreign_vocab` — subject-exclusive vocabulary (moved from the audit script)
- `thresholds` — relevance gate parameters (§4.4), tuned in Phase 2

### 4.2 Query construction (fixes RC2)

Build the query from what the lesson is **about**, weighted by where each
term comes from:

1. **Core terms**: the sub-strand name with its "Sub-Strand N.N:" prefix
   removed (e.g. "Properties of Waves"), plus content words from the lesson
   title.
2. **Detail terms**: phrases from `aresKeywords`, split on commas and kept
   together as phrases (`"doppler effect"`, `"p-n junction"`).
3. Remove `query_stopwords`, words under 3 letters, and terms with zero DB hits.
4. **Phase boosts leave the query.** The phase becomes a small tiebreak
   between candidates that already passed the gate (§4.6), not a search term.

### 4.3 Retrieval, and excluding answer/exam material (fixes RC3, RC4)

- **One** FTS5 query (`core OR detail` terms) ordered by
  `bm25(content_fts, title=10, description=3, extracted_text=1, transcript=1, keywords=5)`,
  taking the top 200. This replaces 15–40 unordered `LIMIT 150` queries and is
  cheaper as well as correct.
- **Content types allowed, filtered in SQL:** video slot = `video`; reading
  slot = `html, html5, pdf, exercise, h5p`. `image`, `audio`, `zim` and
  `topic` are never eligible.
- **Hard exclusion** on title, filename and path, from config:
  `answers?\b|marking[ _-]?scheme|topical[ _-]?test|kcse[ _-]?\d{4}|past[ _-]?papers?|\bexams?\b|\bmock\b`.
  **The handoff's bare `exam` must not be used as written.** Of ~1,900
  non-image DB titles containing "exam", ~1,830 contain it only because they
  say "example" or "examine". A bare `exam` would throw out good worked
  examples. Word boundaries fix this.

### 4.4 Relevance gate — the minimum threshold (fixes RC6)

bm25 scores aren't comparable across queries, so the gate uses term coverage,
which is:

- A candidate **passes** only if (a) at least one **core** term appears in its
  title, keywords or description (a hit only inside a long transcript is not
  enough — this rule alone rejects the muscle-cell and genetics cases), **and**
  (b) its weighted coverage of core + detail terms is at or above
  `thresholds.min_coverage`.
- If no candidate passes, the slot is `null` (§4.8).
- The thresholds are tuned in Phase 2 against the Grade 10 corpus. I will
  report the per-subject fill rate alongside the Tier counts, so the trade-off
  is visible, not assumed.

### 4.5 Subject/domain guard (fixes RC5)

This is layered, because the DB subject column is unreliable (97% "General")
and some genuinely right answers carry a neighbouring subject's tag. For
example, the best semiconductor-doping video is tagged Chemistry, and the
best linear-motion videos are tagged Physics.

1. **Subject family map** (config): Biology → {Biology, General};
   Physics → {Physics, General}; General Science → {Biology, Chemistry,
   Physics, General}; Mathematics / Core Mathematics / Essential Mathematics →
   {Mathematics, Physics², General}; any subject not listed → {its own name,
   General}.
   A DB subject outside the family is a **ranking penalty, not a rejection**.
2. **Hard reject** if the title contains `foreign_vocab` from a subject
   outside the family **and** has no core-term overlap. This is the audit's
   Tier 2 rule, moved into the matcher.
3. Fix the name comparison so "Core Mathematics" matches DB "Mathematics"
   (family lookup, not substring).

² Physics is included for Maths because KICD's Linear Motion and Vectors
sub-strands share content with it. Trivial to remove in config if you disagree.

### 4.6 Ranking among candidates that passed the gate

Order: **relevance first** (bm25), then subject-family match, then link
reliability (Kolibri-storage ID, has direct URL), then channel tier, then a
phase tiebreak. Channel tier moves from first to fourth place. It is still
useful for choosing between two equally relevant items, but it can no longer
lift an irrelevant one.

**Diversity within a lesson:** the 5 phases prefer distinct resources when
more than one passes the gate. Today a lesson often shows the same video in
all five phases. This is also the main driver of Tier 3 repeats.

### 4.7 Preventing recurrence — a gate inside the pipeline

New `scripts/check_resource_links.py`. It replaces the handoff audit script
(which stays as the historical baseline tool):

- **Scope:** all 5 phases, both slots. It walks both the flat Grade 10 tree
  and `v2/Grade{N}/` trees, the same way `generate_teacher_index.js` does.
- **Hard failures** (non-zero exit): an exclusion-pattern hit (Tier 1); foreign
  vocabulary with no core overlap (Tier 2); a `direct_url` whose Kolibri ID is
  missing from the content DB (dead link); a record failing the contract
  `resourceRecordOrNull` shape.
- **Warnings:** the same resource repeated across ≥3 phases of one lesson;
  a title reused ≥ N times corpus-wide (Tier 3 heuristic); Kolibri IDs found
  only in channel metadata, not storage (unverified — see §6); per-subject
  fill rate below a floor (a signal of a content-library gap rather than a bug).
- **Wiring:** `generate.js` runs it on every sub-strand it renders and exits
  non-zero on a hard failure, so `--all` cannot finish "successfully" with a
  bad link. `WORKFLOW.md` gets it as a required pre-ship step next to
  `validate_corpus.js`.
- **Defence in depth:** the matcher applies the same exclusion and
  foreign-vocab rules itself (§4.3, §4.5), so the checker should never fire.
  If it does, a matcher change has regressed.

### 4.8 How "no confident match" is stored and rendered

- **Data:** `video: null` and/or `reading: null`, with `fallback_search_url`
  always present. This is the shape the contract already allows, so nothing
  changes for the partner.
- **docx:** the null branch already exists in `aresResources.js` (it prints
  "🔍 Search ARES for videos"). It will be made explicit:
  > 📹 VIDEO: *No closely matching video in the ARES library for this activity.*
  > 🔍 Search ARES: `<search terms>` — with the full search URL printed
  > visibly, since printed copies lose hyperlinks.
- **Diagnostics** (scores, gate reasons, runner-up candidates) are written to
  a sidecar file, `logs/link_matching/<filePrefix>.json`, **not** the
  contract JSON. This makes every choice traceable afterwards without the
  kind of DB re-tracing done for this document.

### 4.9 Works for any grade and subject

- Matching inputs are lesson text plus `META.subject`. Grade plays no part in
  matching, only in output paths, and those paths already follow the
  grade-aware convention.
- A subject missing from `subject_families` falls back to {own name, General}.
  An empty `foreign_vocab` for a new subject just means the guard relies on
  the relevance gate. Non-STEM subjects (English, History) therefore need no
  code change, only optional config entries.
- Nothing in the new code names Grade 10, a specific subject, or STEM.

## 5. Phase 2 plan (once this design is approved)

1. Implement §4.1–4.8, then re-render only the Tier 1/2 sub-strands first.
2. Re-run the handoff audit script (predict only, comparable to 34/25/174),
   plus the new checker across all phases. Report both, plus the per-subject
   fill rate.
3. Hand-check 10 Tier 3 rows and report how many were real problems.
4. Link functionality: every shipped Kolibri ID exists in the content DB.
   Report storage vs channel-metadata-only IDs (see §6).
5. Stop and report. The full re-render of all 85 sub-strands (no API cost,
   ~minutes) is done in Phase 5 together with attribution, or earlier if you
   prefer.

## 6. Open items / risks

- **Live link verification isn't possible from jhm-spark.** No Kolibri
  answers on `ares.local:8069` or `localhost:8069` here. Of the 542 distinct
  Kolibri IDs shipped today, **280 are Kolibri-storage IDs** (recorded as
  confirmed correct) and **262 exist only in channel metadata**, which the
  code's own comment says "may differ on live server". I can prove existence
  in the DB, not that the link opens on a school box. **Question: is there a
  server (e.g. tsavo3) I can check these against?** If so, I'll probe each
  distinct ID once (~550 HTTP requests) in Phase 2.
- **Fill rate will drop, and that is intended.** Some sub-strands (probably
  parts of Maths, which the Kolibri library covers mostly through US-curriculum
  content) may end up with many "search ARES" cells. That will be reported per
  sub-strand as a **content-library gap**, not hidden. The handoff's step 4
  asks for exactly this list.
- **Threshold tuning is a judgment call.** I'll pick values that bring
  Tier 1/2 to 0 while keeping the fill rate as high as possible, and show
  both numbers so you can move the dial.
- **Partner impact:** none expected. Nulls are already legal, and no fields
  are added.

## 7. Implementation notes (Phase 2, 2026-09-29): where the build differs from §4

Each change below came from testing against real lessons. The measured
reason is given for each.

- **Web-module sources are eligible, not just Kolibri (§4.3).** The best
  semiconductor material is SeaVuria's own science videos and the PhET
  simulations, which are indexed as `web`. Neither the old matcher nor the
  Kolibri-only draft could pick them. Web items are eligible **only if their
  file exists** under the reference image's `/var/www/modules` (26,927 of
  27,410 do). Kiwix stays ineligible because its article links can't be
  verified. SeaVuria was added to channel tier 0.
- **Link verification uses the ARES disk image (§6 resolved).** jhm-spark has
  an ARES system disk mounted. Its Kolibri `db.sqlite3` (the instance on port
  8069, 75,324 nodes) and its web-modules tree are the reference: a Kolibri
  link must be a node with `available=1`, and a web link must be an existing
  file. This found **7 dead Kolibri IDs (45 slots)** in the old corpus: nodes
  whose content was never downloaded. All 542 old IDs were real node IDs; the
  "262 unverified" worry in §6 was unfounded.
- **The exclusion list is wider than the handoff regex (§4.3).** It adds
  `kcse`, `knec`, `pp1–3`, `paper 1–3` and a trailing `Ms`, plus the whole
  `kcse/` web folder (past papers and marking schemes). The handoff regex
  missed `biology-question-paper-1-kcse-2012`.
- **The gate uses whole phrases and position weights (§4.4).** Counting
  single words let "Service in the United States" through (`state` +
  `definition`). Instead:
  - Each `aresKeywords` phrase counts only if all its words are present.
  - Phrases are weighted by position (the lesson's first keywords are its
    main topic).
  - A multi-word sub-strand topic ("linear motion") must match whole.
  - A topic match also needs at least one lesson-specific term.
  - A partial-topic credit was tried and **reverted**: it let "Comparing
    animal and plant cells" into a mouthparts lesson.
- **Variety across phases has a floor (§4.6).** Forcing a different resource
  in every phase pushed later phases into weak matches. Variety now only
  chooses among candidates scoring ≥60% of the best; otherwise the best is
  reused.
- **Search terms are printed instead of the search URL (§4.8).** The ARES
  search URL is ~600 characters, so a no-match cell prints the search terms,
  which a teacher can type into ARES search, next to the hyperlinked search
  label.
- **Two more silent fallbacks were removed** (same class as RC6):
  - `aresResources.js` swallowed recommender errors and returned empty
    resources with `fallback_search_url: ''`, which is a contract violation.
  - `sections.js` replaced a failed module load with `() => ({})`.
  Both now fail the render. Re-rendering an edited JSON on a machine without
  the ARES DB keeps the existing `resourceLinks` and prints a warning.
