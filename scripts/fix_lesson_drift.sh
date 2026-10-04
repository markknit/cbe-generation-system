#!/usr/bin/env bash
# fix_lesson_drift.sh MODULE [MODULE...]  — repair -> derive Summary Table -> re-review, up to 3 rounds
# per module, stopping early at 0 major contradictions. Then rebuild the Final Explanation.
# Residual contradictions stay in logs/lesson_drift/<module>.json for a human.
set -u
cd "$(dirname "$0")/.."
source venv/bin/activate
for M in "$@"; do
  echo "=== $M"
  for r in 1 2 3; do
    python3 scripts/repair_lesson_drift.py "$M" 2>&1 | grep -E "edits:|FAILED|no major"
    python3 scripts/rebuild_consistency.py --summary-tables --only "$M" >/dev/null
    out=$(python3 scripts/review_lesson_consistency.py --only "$M" 2>&1 | grep -E "^  $M")
    echo "  round $r: $out"
    case "$out" in *" 0 major"*) break;; esac
  done
  python3 scripts/rebuild_consistency.py --final-explanations --only "$M" 2>&1 | grep -E "^  (OK|REVIEW|FAILED)"
done
