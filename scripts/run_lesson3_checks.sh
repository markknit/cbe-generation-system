#!/usr/bin/env bash
# run_lesson3_checks.sh — run the partner's (Lesson3 editor) DB-free checks against OUR output.
#
# Run after every regeneration / renderer change, before telling the partner anything is ready.
# The partner's full suite (test:unit/int/http/e2e) tests HIS application; the checks below are the
# ones that consume OUR files, and they need no database or Docker:
#   1 contract-drift        every *_data.json against the contract (report; non-zero only if unreadable)
#   2 corpus-resource-check contract + resourceLinks survive ingest -> adapter exactly (counts enforced)
#   3 corpus-check          renders all 4 documents per sub-strand through HIS vendored generator; fails on
#                           raw markdown tables, malformed JSON, generation/preview errors
#   4 ingest-extract-check, contract-check   his own gates for the ingest code (sanity that his checkout works)
#   5 adapter-fidelity      his rendering vs OUR docx for 3 sub-strands (needs his vendored generator pinned
#                           to our current commit: see app/src/generator/vendor/PROVENANCE.md)
#
#   scripts/run_lesson3_checks.sh [--update] [--unit]
#     --update  git pull his repo first (default: use the checkout as is)
#     --unit    also run his `npm run test:unit` (offline vitest)
# Environment: LESSON3_DIR (default ~/ares/Lesson3, a clone of https://github.com/james-beep-boop/Lesson3
# with `cd app && npm ci` done; his AGENTS.md pins Node 24.21.0).
# Exit 0 only if every check passes; a summary is written to logs/lesson3_checks.log.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
L3="${LESSON3_DIR:-$HOME/ares/Lesson3}"
N24="$(ls -d "$HOME"/ares/tools/node-v24.21.0-*/bin 2>/dev/null | head -1)"; [ -n "$N24" ] && export PATH="$N24:$PATH"   # his repo pins Node 24.21.0
LOG="$ROOT/logs/lesson3_checks.log"
UPDATE=0; UNIT=0
for a in "$@"; do case "$a" in --update) UPDATE=1;; --unit) UNIT=1;; esac; done

[ -d "$L3/app" ] || { echo "No Lesson3 checkout at $L3 (set LESSON3_DIR; git clone https://github.com/james-beep-boop/Lesson3 && cd Lesson3/app && npm ci)"; exit 2; }
[ -d "$L3/app/node_modules" ] || { echo "Run 'cd $L3/app && npm ci' first (his repo pins Node 24.21.0)"; exit 2; }
[ "$UPDATE" = 1 ] && git -C "$L3" pull --ff-only -q

# flat staging dir of COPIES (his scripts do not recurse and ignore symlinks)
STAGE="$(mktemp -d)"; trap 'rm -rf "$STAGE"' EXIT
FILES=0; LESSONS=0
while IFS= read -r f; do
  cp "$f" "$STAGE/$(basename "$f")"; FILES=$((FILES+1))
done < <(find "$ROOT/data/outputs/v2" -name '*_data.json' -not -path '*/PDF/*' | sort)
LESSONS=$(python3 - "$STAGE" <<'EOF'
import glob, json, sys
print(sum(len(json.load(open(f))["LESSONS"]) for f in glob.glob(sys.argv[1] + "/*_data.json")))
EOF
)

mkdir -p "$ROOT/logs"
{ echo "== lesson3 checks $(date -Is)  ours=$(git -C "$ROOT" rev-parse --short HEAD)  his=$(git -C "$L3" rev-parse --short HEAD)  files=$FILES lessons=$LESSONS"
  grep -m1 'Pinned commit' "$L3/app/src/generator/vendor/PROVENANCE.md"; } | tee "$LOG"

# his extractor-parity gate hardcodes a sample named bio_1_4_data.js (that sub-strand was renumbered away): feed it a current module under that name
DEMO="$STAGE/demo"; mkdir -p "$DEMO"; cp "$ROOT/generators/data/bio_1_3_data.js" "$DEMO/bio_1_4_data.js"
FAILED=()
run() {  # name, command...
  local name="$1"; shift
  echo "--- $name" | tee -a "$LOG"
  if (cd "$L3/app" && "$@") >>"$LOG" 2>&1; then echo "    PASS" | tee -a "$LOG"; else echo "    FAIL (details in $LOG)" | tee -a "$LOG"; FAILED+=("$name"); fi
}

run "contract-drift"          npx tsx scripts/contract-drift.ts -- "$STAGE"
run "corpus-resource-check"   env ARES_JSON_CORPUS_DIR="$STAGE" ARES_JSON_EXPECTED_FILES="$FILES" ARES_JSON_EXPECTED_LESSONS="$LESSONS" npx tsx scripts/corpus-resource-check.ts
run "corpus-check"            env ARES_CORPUS_DIR="$STAGE" npx tsx scripts/corpus-check.ts
# Informational only: tests HIS extractor against a sample module, not our output. Known benign diff as of
# 2026-10-08: the extractor stamps schemaVersion on a .js module that lacks it (our JSON exports carry it).
echo "--- ingest-extract-check (informational)" | tee -a "$LOG"
(cd "$L3/app" && env ARES_DEMO_PATH="$DEMO" npx tsx scripts/ingest-extract-check.ts) >>"$LOG" 2>&1 \
  && echo "    PASS" | tee -a "$LOG" || echo "    not clean (his gate; see log, not counted)" | tee -a "$LOG"
run "contract-check"          npx tsx scripts/contract-check.ts
for d in Physics/SS4.1_Greenhouse_Effect_and_Climate_Change Essential_Mathematics/SS1.2_Indices Maths/SS3.1_Trigonometry_I; do
  dir="$(find "$ROOT/data/outputs/v2" -type d -path "*/$d" -not -path '*/PDF/*' | head -1)"
  if [ -z "$dir" ]; then dir="$(find "$ROOT/data/outputs/v2" -type d -name "$(basename "$d")" -not -path '*/PDF/*' | head -1)"; fi
  [ -n "$dir" ] && run "adapter-fidelity $(basename "$d")" env ARES_FIDELITY_SUBSTRAND_DIR="$dir" npx tsx scripts/adapter-fidelity.ts \
    || { echo "--- adapter-fidelity $d: directory not found" | tee -a "$LOG"; FAILED+=("adapter-fidelity $d (missing)"); }
done
[ "$UNIT" = 1 ] && run "test:unit" npm run test:unit

echo | tee -a "$LOG"
if [ ${#FAILED[@]} -eq 0 ]; then echo "ALL LESSON3 CHECKS PASSED" | tee -a "$LOG"; exit 0; fi
echo "FAILED: ${FAILED[*]}" | tee -a "$LOG"; exit 1
