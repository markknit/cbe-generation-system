#!/usr/bin/env bash
# check_new_stem_subjects_status.sh
#
# Verifies how far Phase 0-2 of HANDOFF_new_stem_subjects_2026-07-08.md
# actually got, for General Science / Core Mathematics / Essential Mathematics.
#
# Run this ON jhm-spark, from the repo root:
#   cd /home/markk/ares/cbe-generation-system
#   bash check_new_stem_subjects_status.sh
#
# It does not modify anything - read-only checks only.

set -uo pipefail

REPO_ROOT="$(pwd)"
PASS="✅"
PARTIAL="🟡"
FAIL="❌"

echo "=================================================================="
echo "  Status check: General Science / Core Mathematics / Essential Math"
echo "  Repo: $REPO_ROOT"
echo "  Run at: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "=================================================================="
echo

# ------------------------------------------------------------------
# Sanity check: are we actually in the right repo?
# ------------------------------------------------------------------
if [ ! -d "generators" ] || [ ! -d "src" ]; then
  echo "$FAIL Doesn't look like the cbe-generation-system repo root."
  echo "   Expected to find 'generators/' and 'src/' here. Aborting."
  exit 1
fi

# ------------------------------------------------------------------
# 0. Git context first, since everything else is judged against this
# ------------------------------------------------------------------
echo "------------------------------------------------------------------"
echo "0. GIT CONTEXT"
echo "------------------------------------------------------------------"
CURRENT_BRANCH="$(git branch --show-current 2>/dev/null || echo 'UNKNOWN')"
echo "Current branch: $CURRENT_BRANCH"

echo
echo "Uncommitted changes (git status --short):"
GIT_STATUS="$(git status --short 2>/dev/null)"
if [ -z "$GIT_STATUS" ]; then
  echo "  (none - working tree clean)"
else
  echo "$GIT_STATUS" | sed 's/^/  /'
fi

echo
echo "Last 10 commits on this branch:"
git log --oneline -10 2>/dev/null | sed 's/^/  /'

echo
echo "Commits anywhere mentioning the new subjects (by message or path):"
GIT_HITS="$(git log --oneline --all \
  --grep="General Science" --grep="Core Mathematics" --grep="Essential Mathematics" \
  --grep="general_science" --grep="core_mathematics" --grep="essential_mathematics" \
  --regexp-ignore-case -- . 2>/dev/null)"
GIT_PATH_HITS="$(git log --oneline --all -- \
  '*general_science*' '*core_mathematics*' '*essential_mathematics*' \
  '*General Science*' '*Core Mathematics*' '*Essential Mathematics*' \
  '*HANDOFF_new_stem*' 2>/dev/null)"
if [ -z "$GIT_HITS" ] && [ -z "$GIT_PATH_HITS" ]; then
  echo "  (none found)"
else
  echo "$GIT_HITS" | sed 's/^/  [msg] /'
  echo "$GIT_PATH_HITS" | sed 's/^/  [path] /'
fi
echo

# ------------------------------------------------------------------
# PHASE 0 - extraction verified, numbering pinned
# ------------------------------------------------------------------
echo "------------------------------------------------------------------"
echo "PHASE 0 - Extraction method verified, strand/sub-strand numbering pinned"
echo "------------------------------------------------------------------"

PHASE0_SIGNALS=0

echo "-- Handoff document present on this machine?"
HANDOFF_FILES="$(find . -iname "*HANDOFF_new_stem*" -not -path "./.git/*" 2>/dev/null)"
if [ -n "$HANDOFF_FILES" ]; then
  echo "  $PASS Found:"
  echo "$HANDOFF_FILES" | sed 's/^/     /'
  PHASE0_SIGNALS=$((PHASE0_SIGNALS+1))
else
  echo "  $FAIL Not found anywhere under $REPO_ROOT"
fi

echo
echo "-- Cleaned/transcribed curriculum text (data/raw/curriculum_text/)?"
if [ -d "data/raw/curriculum_text" ]; then
  COUNT=$(find data/raw/curriculum_text -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "  $PASS Directory exists, $COUNT file(s):"
  find data/raw/curriculum_text -type f 2>/dev/null | sed 's/^/     /'
  PHASE0_SIGNALS=$((PHASE0_SIGNALS+1))
else
  echo "  $FAIL data/raw/curriculum_text/ does not exist"
fi

echo
echo "-- Source PDFs present and still unreadable-as-text (sanity re-check)?"
CURRIC_DIR="CBE_Curriculums/Grade 10/STEM"
if [ -d "$CURRIC_DIR" ]; then
  for f in "General Science Grade 10 - July 2025.pdf" \
           "Core Mathematics Grade 10 - July 2025.pdf" \
           "Essential Mathematics Grade 10 - July 2025.pdf"; do
    if [ -f "$CURRIC_DIR/$f" ]; then
      if command -v pdfinfo >/dev/null 2>&1; then
        PAGES=$(pdfinfo "$CURRIC_DIR/$f" 2>/dev/null | awk -F': *' '/^Pages/{print $2}')
        SIZE=$(pdfinfo "$CURRIC_DIR/$f" 2>/dev/null | awk -F': *' '/^Page size/{print $2}')
        echo "  found: $f  (Pages: $PAGES | Page size: $SIZE)"
      else
        echo "  found: $f  (pdfinfo not installed - can't check geometry)"
      fi
    else
      echo "  $FAIL missing: $f"
    fi
  done
else
  echo "  $FAIL Curriculum folder not found: $CURRIC_DIR"
fi

echo
if [ "$PHASE0_SIGNALS" -ge 2 ]; then
  echo "PHASE 0 VERDICT: $PASS Looks done (handoff + extracted text both present)"
elif [ "$PHASE0_SIGNALS" -eq 1 ]; then
  echo "PHASE 0 VERDICT: $PARTIAL Partial - one signal present, one missing (see above)"
else
  echo "PHASE 0 VERDICT: $FAIL Not started"
fi
echo

# ------------------------------------------------------------------
# PHASE 1 - wired into pipeline
# ------------------------------------------------------------------
echo "------------------------------------------------------------------"
echo "PHASE 1 - New subjects wired into the generation pipeline"
echo "------------------------------------------------------------------"

PHASE1_SIGNALS=0
PIPELINE_FILES="src/generate_substrand.py src/ares_recommender.py ares_scan_config.yaml"

for f in $PIPELINE_FILES; do
  if [ -f "$f" ]; then
    HITS=$(grep -inE "general_science|core_mathematics|essential_mathematics" "$f" 2>/dev/null)
    if [ -n "$HITS" ]; then
      echo "  $PASS $f references the new subjects:"
      echo "$HITS" | sed 's/^/     /' | head -5
      PHASE1_SIGNALS=$((PHASE1_SIGNALS+1))
    else
      echo "  $FAIL $f - no reference found"
    fi
  else
    echo "  $FAIL $f - file not found"
  fi
done

echo
TOTAL_PIPELINE_FILES=3
if [ "$PHASE1_SIGNALS" -eq "$TOTAL_PIPELINE_FILES" ]; then
  echo "PHASE 1 VERDICT: $PASS Fully wired (all $TOTAL_PIPELINE_FILES files reference new subjects)"
elif [ "$PHASE1_SIGNALS" -gt 0 ]; then
  echo "PHASE 1 VERDICT: $PARTIAL Partially wired ($PHASE1_SIGNALS of $TOTAL_PIPELINE_FILES files)"
else
  echo "PHASE 1 VERDICT: $FAIL Not started"
fi
echo

# ------------------------------------------------------------------
# PHASE 2 - one pilot sub-strand per subject
# ------------------------------------------------------------------
echo "------------------------------------------------------------------"
echo "PHASE 2 - Pilot sub-strand generated per subject"
echo "------------------------------------------------------------------"

echo "-- Data files (generators/data/):"
DATA_HITS="$(ls generators/data/ 2>/dev/null | grep -iE "gensci|general_science|core_math|essential_math")"
if [ -n "$DATA_HITS" ]; then
  echo "$DATA_HITS" | sed 's/^/  '"$PASS"' /'
else
  echo "  $FAIL none found"
fi

echo
echo "-- Output folders (data/outputs/v2/):"
for SUBJ in "General Science" "Core Mathematics" "Essential Mathematics"; do
  if [ -d "data/outputs/v2/$SUBJ" ]; then
    N=$(find "data/outputs/v2/$SUBJ" -iname "*.docx" 2>/dev/null | wc -l | tr -d ' ')
    echo "  $PASS data/outputs/v2/$SUBJ/  ($N docx file(s))"
  else
    echo "  $FAIL data/outputs/v2/$SUBJ/  not found"
  fi
done

PHASE2_COUNT=$(( $(echo "$DATA_HITS" | grep -c . 2>/dev/null || echo 0) ))
echo
if [ "$PHASE2_COUNT" -ge 3 ]; then
  echo "PHASE 2 VERDICT: $PASS At least one pilot data file per subject found"
elif [ "$PHASE2_COUNT" -gt 0 ]; then
  echo "PHASE 2 VERDICT: $PARTIAL Some pilot data found, not all 3 subjects"
else
  echo "PHASE 2 VERDICT: $FAIL Not started"
fi
echo

# ------------------------------------------------------------------
# STATUS.md cross-check
# ------------------------------------------------------------------
echo "------------------------------------------------------------------"
echo "STATUS.md - local copy vs. this thread"
echo "------------------------------------------------------------------"
if [ -f "STATUS.md" ] || [ -f "docs/STATUS.md" ]; then
  STATUS_FILE="STATUS.md"
  [ -f "docs/STATUS.md" ] && STATUS_FILE="docs/STATUS.md"
  if grep -qiE "general science|core mathematics|essential mathematics" "$STATUS_FILE" 2>/dev/null; then
    echo "  $PASS $STATUS_FILE mentions the new subjects - session log may have this thread"
    grep -inE "general science|core mathematics|essential mathematics" "$STATUS_FILE" | sed 's/^/     /'
  else
    echo "  $FAIL $STATUS_FILE does NOT mention the new subjects (matches what was seen on GitHub main)"
  fi
else
  echo "  $FAIL No STATUS.md found in repo root or docs/"
fi
echo

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------
echo "=================================================================="
echo "  SUMMARY"
echo "=================================================================="
echo "Phase 0 (extraction/numbering):  see verdict above"
echo "Phase 1 (pipeline wiring):       see verdict above"
echo "Phase 2 (pilot sub-strand):      see verdict above"
echo
echo "Next step: whichever phase shows FAIL first is where to resume."
echo "If Phase 0 is FAIL, start the handoff from the top."
echo "If Phase 0 is PASS but Phase 1 is FAIL, wiring didn't happen yet -"
echo "  re-run the Phase 1 steps from HANDOFF_new_stem_subjects_2026-07-08.md."
echo "If Phase 0-1 PASS but Phase 2 FAIL, run the one-substrand pilot."
echo "If Phase 0-2 all PASS, you're clear to move to Phase 3 (full batch)."
echo "=================================================================="
