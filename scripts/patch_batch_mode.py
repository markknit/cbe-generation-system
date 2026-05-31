#!/usr/bin/env python3
"""
patch_batch_mode.py
====================
Adds Message Batches API support to generate_substrand.py.
Adds --batch flag (submit) and --collect flag (retrieve results).

Run from project root:
    python3 scripts/patch_batch_mode.py
"""
import re

path = 'src/generate_substrand.py'
with open(path) as f:
    src = f.read()

# ── 1. Add batch helper functions before main() ───────────────────────────────

BATCH_FUNCTIONS = '''
# ── Message Batches API ───────────────────────────────────────────────────────

def _batch_id_path(output_name: str) -> Path:
    return PROJECT_ROOT / 'generators' / 'data' / f'.{output_name}_batch_id.txt'


def submit_batch(requests: list) -> str:
    """Submit all requests as a single Message Batches API job.
    Returns the batch_id for later collection.
    """
    print(f"  Submitting batch of {len(requests)} requests...")
    batch = CLIENT.beta.messages.batches.create(
        requests=requests,
        betas=["output-300k-2026-03-24"],   # 300K output tokens per request
    )
    print(f"  Batch ID: {batch.id}")
    print(f"  Status:   {batch.processing_status}")
    return batch.id


def poll_batch(batch_id: str, poll_interval: int = 60) -> object:
    """Poll until the batch is complete. Returns the finished batch object."""
    import sys
    print(f"  Polling batch {batch_id} (checking every {poll_interval}s)...")
    while True:
        batch = CLIENT.beta.messages.batches.retrieve(batch_id)
        counts = batch.request_counts
        done   = counts.succeeded + counts.errored + counts.expired
        total  = counts.processing + done
        print(f"    {batch.processing_status}: {done}/{total} done "
              f"({counts.succeeded} succeeded, {counts.errored} errored)",
              end='\\r', flush=True)
        if batch.processing_status == 'ended':
            print()  # newline after \\r
            return batch
        time.sleep(poll_interval)


def collect_batch_results(batch_id: str) -> dict:
    """Retrieve all results from a completed batch.
    Returns dict mapping custom_id → parsed JSON (or None on error).
    """
    results = {}
    for result in CLIENT.beta.messages.batches.results(batch_id):
        cid = result.custom_id
        if result.result.type == 'succeeded':
            raw = result.result.message.content[0].text.strip()
            raw = re.sub(r'^```(?:json)?\\s*', '', raw)
            raw = re.sub(r'\\s*```$', '', raw)
            raw = re.sub(r'[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', '', raw)
            try:
                results[cid] = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"  WARNING: JSON parse failed for {cid}: {e}")
                results[cid] = None
        else:
            print(f"  WARNING: {cid} failed: {result.result.type}")
            results[cid] = None
    return results


def build_batch_requests(curriculum_text: str, template: dict,
                          unit: dict, args) -> list:
    """Build all lesson + FE requests for batch submission.
    Note: prev_summaries context is omitted in batch mode since all
    requests are submitted simultaneously. The unit storyline thread
    provides sufficient continuity.
    """
    requests = []

    for lesson_num in range(1, args.lessons + 1):
        lesson_pos = "opening lesson that launches the phenomenon" if lesson_num == 1 else \\
                     "final lesson with Final Explanation" if lesson_num == args.lessons else \\
                     f"lesson {lesson_num} of {args.lessons} in the evidence-gathering sequence"

        prompt = (
            f"Generate Lesson {lesson_num} ({lesson_pos}) for:\\n"
            f"Subject: {args.subject.capitalize()} Grade 10\\n"
            f"Sub-strand: {args.substrand} {args.substrand_name}\\n"
            f"Driving question: {unit.get('drivingQuestion', '')}\\n"
            f"Phenomenon: {unit.get('phenomenon', '')}\\n"
            f"Storyline thread for this lesson: {_get_lesson_storyline(unit, lesson_num)}\\n\\n"
            f"KICD CURRICULUM CONTENT:\\n{curriculum_text}\\n\\n"
            f"TEACHER TEMPLATE — EVIDENCE ACTIVITIES:\\n"
            f"{template.get('evidence_activities', '')}\\n\\n"
            f"RULES:\\n"
            f"- All learner experiences must connect back to the phenomenon\\n"
            f"- Teacher moves must include specific quoted phrases, WAIT TIME (10-15 seconds), cold-call counts\\n"
            f"- Sensemaking strategies: name the strategy and explain how it builds understanding\\n"
            f"- Formative assessment: specific, observable indicators\\n"
            f"- Kenya-relevant contexts throughout\\n"
            f"- Lesson {lesson_num} should "
            f"{'introduce the phenomenon and open the DQB' if lesson_num == 1 else 'build on previous evidence and advance the driving question'}\\n"
            f"{'- Final lesson: focus on Final Explanation, model comparison L1 vs final, DQB completion' if lesson_num == args.lessons else ''}\\n\\n"
            f"Return ONLY this JSON (no other text):\\n"
            f"{json.dumps({'lesson': LESSON_SCHEMA}, indent=2)}\\n\\n"
            f"Replace all placeholder values with real content for Lesson {lesson_num}.\\n"
            f"Set number to {lesson_num}. Set substrand to "
            f"'Sub-Strand {args.substrand}: {args.substrand_name}'."
        )

        requests.append({
            "custom_id": f"lesson_{lesson_num}",
            "params": {
                "model": MODEL,
                "max_tokens": 8192,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}],
            },
        })

    # Final Explanation request
    lesson_titles = "\\n".join(
        f"  Lesson {i+1}: [will be filled from lesson content]"
        for i in range(args.lessons)
    )
    fe_prompt = (
        f"Generate a Final Explanation assessment document for:\\n"
        f"Subject: {args.subject.capitalize()} Grade 10\\n"
        f"Sub-strand: {args.substrand} {args.substrand_name}\\n"
        f"Driving question: {unit.get('drivingQuestion', '')}\\n"
        f"Phenomenon: {unit.get('phenomenon', '')}\\n"
        f"Number of lessons in sequence: {args.lessons}\\n\\n"
        f"Return ONLY this JSON:\\n"
        '{\\n'
        '  "subjectLabel": "SUBJECT LABEL IN CAPS",\\n'
        '  "instructions": "Multi-sentence instructions for students...",\\n'
        '  "sections": [\\n'
        '    {\\n'
        '      "title": "SECTION 1: TITLE IN CAPS",\\n'
        '      "prompt": "Specific prompt for this section",\\n'
        '      "exemplar": "2-3 paragraph model answer with Kenyan contexts"\\n'
        '    }\\n'
        '  ],\\n'
        '  "rubric": [\\n'
        '    {\\n'
        '      "criterion": "Criterion name",\\n'
        '      "excellent": "Excellent (4) descriptor",\\n'
        '      "proficient": "Proficient (3) descriptor",\\n'
        '      "developing": "Developing (1-2) descriptor"\\n'
        '    }\\n'
        '  ]\\n'
        '}\\n\\n'
        f"Include 4-5 sections and 4-5 rubric criteria."
    )

    requests.append({
        "custom_id": "final_explanation",
        "params": {
            "model": MODEL,
            "max_tokens": 5000,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": fe_prompt}],
        },
    })

    return requests


def run_collect(output_name: str, args):
    """Collect results from a previously submitted batch and assemble data file."""
    id_path = _batch_id_path(output_name)
    if not id_path.exists():
        print(f"ERROR: No batch ID found for '{output_name}'")
        print(f"  Expected: {id_path}")
        print(f"  Submit a batch first with: --batch")
        sys.exit(1)

    batch_id = id_path.read_text().strip()
    batch_meta_path = id_path.with_suffix('.json')
    batch_meta = json.loads(batch_meta_path.read_text()) if batch_meta_path.exists() else {}

    print(f"Collecting batch: {batch_id}")

    # Check status
    batch = CLIENT.beta.messages.batches.retrieve(batch_id)
    print(f"  Status: {batch.processing_status}")

    if batch.processing_status != 'ended':
        if args.wait:
            batch = poll_batch(batch_id)
        else:
            counts = batch.request_counts
            print(f"  Not ready yet ({counts.processing} still processing)")
            print(f"  Run again with --wait to poll, or check back later")
            return

    # Collect results
    print("  Collecting results...")
    results = collect_batch_results(batch_id)
    print(f"  Got {len(results)} results ({sum(1 for v in results.values() if v)} succeeded)")

    # Reconstruct unit from saved metadata
    unit = batch_meta.get('unit', {})
    meta = batch_meta.get('meta', {})
    n_lessons = batch_meta.get('lessons', args.lessons if hasattr(args, 'lessons') else 6)

    # Extract lessons
    lessons = []
    for i in range(1, n_lessons + 1):
        cid  = f"lesson_{i}"
        data = results.get(cid)
        if data:
            lesson = data.get('lesson', data)   # handle both {lesson: {...}} and {...}
            lessons.append(lesson)
        else:
            print(f"  WARNING: Lesson {i} missing or failed — using stub")
            lessons.append({
                "number": i, "title": f"Lesson {i}",
                "duration": "40 minutes",
                "substrand": f"Sub-Strand {meta.get('substrand_id', '')}: {meta.get('substrand_name', '')}",
                "aresKeywords": "",
                "slo": {"purpose":"","knowledge":"","skills":"","attitudes":"",
                        "keyInquiry":"","purposeInStoryline":"","safetyNotes":""},
                "overview": "",
                "framework": [
                    {"phase": ph, "learnerExperience":"","teacherMoves":"",
                     "sensemakingStrategy":"","formativeAssessment":""}
                    for ph in ["Predict Phase","Observe Phase","Explain Phase",
                               "Driving Question Board (DQB) Creation","Model Building Phase"]
                ],
                "teacherReflection": "",
                "summaryTablePrompt": {"observed":"","learned":"","explained":""},
            })

    # Extract FE
    fe = results.get('final_explanation')
    if not fe:
        print("  WARNING: Final Explanation missing or failed")

    # Generate Summary Table synchronously (needs real lesson data)
    print("  Generating Summary Table (synchronous — needs lesson data)...")

    # Build args-like namespace for generate_summary_table
    class _Args:
        pass
    st_args = _Args()
    st_args.subject     = meta.get('subject', 'Biology').lower()
    st_args.substrand   = meta.get('substrand_id', '')
    st_args.substrand_name = meta.get('substrand_name', '')
    st_args.lessons     = n_lessons

    st = generate_summary_table(unit, lessons, st_args)
    if st:
        print("  Summary Table generated ✓")

    # Write data file
    print("\\n  Writing data file...")
    output_path = write_data_file(output_name, meta, unit, lessons, fe, st)

    # Optionally run generator
    if hasattr(args, 'run') and args.run:
        print("\\n  Running generator...")
        import subprocess
        result = subprocess.run(
            ['node', 'generators/generate.js', output_name],
            cwd=PROJECT_ROOT, capture_output=True, text=True,
        )
        print(result.stdout)
        if result.returncode != 0:
            print("Generator errors:", result.stderr)

    # Clean up batch ID file
    id_path.unlink(missing_ok=True)
    batch_meta_path.unlink(missing_ok=True)

    print(f"\\n✓ Done! Data file: {output_path}")

'''

# Insert before def main():
src = src.replace('def main():', BATCH_FUNCTIONS + 'def main():', 1)
print("✓ Batch helper functions inserted")

# ── 2. Add --batch, --collect, --wait flags to argparse ──────────────────────

old_flags = "    parser.add_argument('--resume',    action='store_true',"
new_flags = """    parser.add_argument('--batch',     action='store_true',
                        help='Submit all content as a Message Batches API job (50%% cheaper)')
    parser.add_argument('--collect',   default=None, metavar='NAME',
                        help='Collect results from a previously submitted batch')
    parser.add_argument('--wait',      action='store_true',
                        help='With --collect: poll until batch is complete')
    parser.add_argument('--resume',    action='store_true',"""

src = src.replace(old_flags, new_flags, 1)
print("✓ --batch, --collect, --wait flags added")

# ── 3. Add batch dispatch at the start of main() body ────────────────────────

# Find where args = parser.parse_args() is, then insert dispatch after it
old_parse = "    args = parser.parse_args()\n\n    # Resolve substrand name"
new_parse = """    args = parser.parse_args()

    # ── Batch collect mode ────────────────────────────────────────────────────
    if args.collect:
        run_collect(args.collect, args)
        return

    # Resolve substrand name"""

src = src.replace(old_parse, new_parse, 1)
print("✓ --collect dispatch added to main()")

# ── 4. Add batch submit logic after UNIT generation ──────────────────────────

old_unit_check = """    if args.unit_only:
        print("\\n[unit-only mode — stopping here]")
        print(json.dumps(unit, indent=2))
        return

    # LESSONS — with checkpoint resume support"""

new_unit_check = """    if args.unit_only:
        print("\\n[unit-only mode — stopping here]")
        print(json.dumps(unit, indent=2))
        return

    # ── Batch submit mode ─────────────────────────────────────────────────────
    if args.batch:
        print("\\n2b. Building batch requests...")
        requests = build_batch_requests(curriculum_text, template, unit, args)
        print(f"  Built {len(requests)} requests "
              f"({args.lessons} lessons + 1 Final Explanation)")

        batch_id = submit_batch(requests)

        # Save batch ID and metadata for later collection
        id_path = _batch_id_path(args.output)
        id_path.write_text(batch_id)
        meta_path = id_path.with_suffix('.json')
        meta_path.write_text(json.dumps({
            "unit": unit,
            "meta": {
                "subject":        args.subject.capitalize(),
                "substrand_id":   args.substrand,
                "substrand_name": args.substrand_name,
                **meta,
            },
            "lessons": args.lessons,
        }, ensure_ascii=False, indent=2))

        print(f"\\n✓ Batch submitted!")
        print(f"  Batch ID saved to: {id_path}")
        print(f"  Collect results when ready:")
        print(f"    python3 src/generate_substrand.py --collect {args.output} --run")
        print(f"  Or poll automatically:")
        print(f"    python3 src/generate_substrand.py --collect {args.output} --wait --run")
        return

    # LESSONS — with checkpoint resume support"""

src = src.replace(old_unit_check, new_unit_check, 1)
print("✓ Batch submit logic added after UNIT generation")

# ── 5. Write patched file ─────────────────────────────────────────────────────

with open(path, 'w') as f:
    f.write(src)

print(f"\n✓ Patched {path}")
print(f"  Total lines: {src.count(chr(10))}")
print("""
New usage:
  # Submit batch (generates UNIT synchronously, everything else via batch API)
  python3 src/generate_substrand.py --subject biology --substrand 1.4 --output bio_1_4 --lessons 6 --batch

  # Collect results later
  python3 src/generate_substrand.py --collect bio_1_4 --run

  # Collect with automatic polling (blocks until done)
  python3 src/generate_substrand.py --collect bio_1_4 --wait --run
""")
