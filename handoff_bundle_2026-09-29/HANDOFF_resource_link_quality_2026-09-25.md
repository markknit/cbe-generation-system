# Handoff — ares_recommender.py Resource-Matching Quality Bug
*Prepared 2026-09-25, for the Claude Code session on jhm-spark*

## Why this exists

A teacher flagged that Physics Sub-Strand 2.1 ("Properties of Waves"), Lesson 1,
had a video resource about muscle anatomy — totally unrelated to sound waves
and the Doppler effect. An audit of the full generated corpus (all 85
sub-strands, `data/outputs/v2/`, the `resourceLinks` field written by
`ares_recommender.py` / `aresResources.js`) confirms this is not an isolated
incident. It's a real, quantifiable defect with two distinct failure modes.

**Do not just patch the one Physics example.** Both failure modes below
recur across many sub-strands and need root-cause fixes, not spot patches.

## Evidence

`audit_resource_links.py` (attached) walks every `*_data.json` under
`data/outputs/v2/`, reads `LESSONS[*].resourceLinks.predict.{video,reading}.title`,
and classifies each into three tiers. Run it yourself from the repo root:

```bash
cd /home/markk/ares/cbe-generation-system
python3 audit_resource_links.py
```

Current corpus state (1,456 resource links checked, across every lesson):

| Tier | Count | What it means |
|---|---|---|
| **Tier 1 — Answer key surfaced as a resource** | 34 | A KCSE/topical-test answer document is returned as the lesson's "reading." Unambiguous bug, no judgment call needed. |
| **Tier 2 — Wrong-domain vocabulary** | 25 | The matched title contains vocabulary specific to a different, incompatible subject (e.g. "Genetics vocabulary" landing in 8 different Mathematics lessons; "Anatomy of a skeletal muscle cell" in a Physics waves lesson and a Chemistry intro lesson). Very high confidence. |
| **Tier 3 — High repeat, no topical overlap** | 174 | Same title reused 6+ times corpus-wide with no keyword overlap to any of those lessons. Lower confidence — some of these may be genuinely broad, legitimate matches. Worth a look, not a fire drill. |

`resource_link_priority_targets.csv` (attached) has all three tiers as
concrete rows: subject, sub-strand, lesson number/title, which resource slot
(video/reading), the offending title, and why it was flagged.

**Named recurring offenders** worth checking first, since they show up
across many unrelated lessons (evidence the matcher is returning them as
some kind of default/fallback rather than a genuine best match):
- `"Genetics vocabulary"` — 14 occurrences corpus-wide
- `"Watch Me"` — 20 occurrences
- `"Video: Bending Light"` — 25 occurrences
- `"Anatomy of a skeletal muscle cell"` — appears in Chemistry Intro, Chemistry
  Chemical Bonding, AND Physics Properties of Waves — three unrelated subjects
- `"topical-test-form-3-physics-electrostatics-2-answers"` — reused across
  3 different Electrostatics lessons

## What to do, in order

### 1. Diagnose before touching code
Read the actual matching/scoring logic in `ares_recommender.py` (and
whatever in `aresResources.js` calls it). For at least 3 of the Tier 2
examples above, trace and report:
- What search query string was actually constructed for that lesson?
- What did the ARES content DB (FTS5) return, and in what rank order?
- Why did a wrong-subject result outrank (or stand in for) a right-subject one?

Write this up before changing anything — the answer-key leakage and the
generic-title-reuse pattern may have different root causes (e.g. a missing
content-type filter vs. a broken relevance threshold vs. overly generic
search-term construction), and they may need different fixes.

### 2. Required fixes
- **Hard exclude answer/exam material** from ever filling a video or reading
  slot — regex on title/filename (`answer|topical-test|kcse\s?\d{4}|exam`),
  or a proper content-type filter if the index has one.
- **Minimum relevance threshold.** If nothing in the search results clears
  it, return no direct match and fall back to the generic ARES search link
  only — do not force the top-ranked result through when it's a bad fit.
  This is the fix most likely to address the recurring-generic-title problem.
- **A build-time regression gate.** Add a step to the generation pipeline
  (or at minimum, a required pre-ship check) that re-runs
  `audit_resource_links.py` and fails/warns if Tier 1 or Tier 2 counts go
  above zero (or above their current baseline, if zero isn't immediately
  achievable). This is what prevents the next version of this bug from
  shipping silently for months before a teacher catches it again.

### 3. Verify, don't just assert "fixed"
After the fix, regenerate `resourceLinks` for at least the sub-strands
listed in Tier 1 and Tier 2 of the CSV, then re-run
`audit_resource_links.py` against the regenerated output. Report the new
Tier 1/2/3 counts against the baseline above (34 / 25 / 174). "It looks
better" is not sufficient — give the actual before/after numbers.

### 4. Stop-and-report gate
Before regenerating content for all 85 sub-strands, stop and report:
- The root-cause diagnosis from step 1
- What the fix actually changed (paste the diff or describe it precisely)
- Before/after Tier 1/2/3 counts from step 3
- Any sub-strands where a good local match genuinely doesn't exist in the
  content library (i.e. the fallback-to-search-link behavior will be the
  permanent state, not a bug) — flag these explicitly so they're a known
  gap, not a silent one.

## Files in this handoff
- `audit_resource_links.py` — the audit script, run it as-is from the repo root
- `resource_link_priority_targets.csv` — 233 flagged rows (Tier 1+2+3), with reasons
