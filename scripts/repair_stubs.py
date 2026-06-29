#!/usr/bin/env python3
"""
repair_stubs.py
===============
Repairs stub lessons and missing Final Explanations across Biology sub-strands.
Run from project root with venv activated.

Usage:
    python3 scripts/repair_stubs.py
"""
import json, os, re, subprocess, sys, time
from pathlib import Path

os.chdir('/home/markk/ares/cbe-generation-system')
sys.path.insert(0, 'src')

from dotenv import load_dotenv
load_dotenv('.env')
import anthropic

CLIENT = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
MODEL  = 'claude-sonnet-4-6'

SYSTEM = ("You are an expert CBE curriculum designer for Kenya Grade 10. "
          "Respond with valid JSON only. No markdown fences, no preamble. "
          "Never use apostrophes inside JSON string values — rephrase instead.")

# ── What needs fixing ─────────────────────────────────────────────────────────

REPAIRS = {
    'bio_1_1': {'stubs': [1, 3, 11], 'fe': False, 'subject': 'Biology', 'substrand': '1.1', 'name': 'Cell Structure'},
    'bio_1_2': {'stubs': [5, 6], 'fe': False, 'subject': 'Biology', 'substrand': '1.2', 'name': 'Chemicals of Life'},
    'bio_1_3': {'stubs': [2, 8], 'fe': False, 'subject': 'Biology', 'substrand': '1.3', 'name': 'Cell Biology'},
    'bio_2_1': {'stubs': [1, 3, 4, 10], 'fe': False, 'subject': 'Biology', 'substrand': '2.1', 'name': 'Plant Nutrition'},
    'bio_2_3': {'stubs': [3, 6, 11], 'fe': False, 'subject': 'Biology', 'substrand': '2.3', 'name': 'Plant Gaseous Exchange and Respiration'},
    'bio_3_1': {'stubs': [2, 4, 8, 9], 'fe': False, 'subject': 'Biology', 'substrand': '3.1', 'name': 'Animal Nutrition'},
    'bio_3_2': {'stubs': [1, 6, 11], 'fe': False, 'subject': 'Biology', 'substrand': '3.2', 'name': 'Animal Transport'},
    'bio_3_3': {'stubs': [11], 'fe': False, 'subject': 'Biology', 'substrand': '3.3', 'name': 'Animal Gaseous Exchange and Respiration'},
    'chem_1_2': {'stubs': [1], 'fe': False, 'subject': 'Chemistry', 'substrand': '1.2', 'name': 'The Atom'},
    'chem_1_3': {'stubs': [5, 7, 8, 9], 'fe': False, 'subject': 'Chemistry', 'substrand': '1.3', 'name': 'The Periodic Table'},
    'chem_1_4': {'stubs': [6, 9, 13], 'fe': False, 'subject': 'Chemistry', 'substrand': '1.4', 'name': 'Chemical Bonding'},
    'chem_1_5': {'stubs': [2, 6], 'fe': False, 'subject': 'Chemistry', 'substrand': '1.5', 'name': 'Periodicity'},
    'chem_3_1': {'stubs': [3, 8, 9], 'fe': False, 'subject': 'Chemistry', 'substrand': '3.1', 'name': 'Acids and Bases'},
    'phys_1_1': {'stubs': [3, 9], 'fe': False, 'subject': 'Physics', 'substrand': '1.1', 'name': 'Pressure'},
    'phys_1_2': {'stubs': [1, 3], 'fe': False, 'subject': 'Physics', 'substrand': '1.2', 'name': 'Mechanical Properties of Materials'},
    'phys_1_3': {'stubs': [5], 'fe': False, 'subject': 'Physics', 'substrand': '1.3', 'name': 'Temperature and Thermal Expansion'},
    'phys_1_5': {'stubs': [5, 6], 'fe': False, 'subject': 'Physics', 'substrand': '1.5', 'name': 'Moments of Equilibrium'},
    'phys_2_1': {'stubs': [3, 6, 7, 8], 'fe': False, 'subject': 'Physics', 'substrand': '2.1', 'name': 'Properties of Waves'},
    'phys_3_1': {'stubs': [4], 'fe': False, 'subject': 'Physics', 'substrand': '3.1', 'name': 'Radioactivity and Stability of Isotopes'},
    'phys_3_2': {'stubs': [1, 2, 7, 8, 10], 'fe': False, 'subject': 'Physics', 'substrand': '3.2', 'name': 'Current Electricity'},
    'phys_3_3': {'stubs': [2, 5], 'fe': False, 'subject': 'Physics', 'substrand': '3.3', 'name': 'Introduction to Electronics'},
    'phys_3_4': {'stubs': [3, 6, 8, 9], 'fe': False, 'subject': 'Physics', 'substrand': '3.4', 'name': 'Electrostatics'},
    'phys_4_1': {'stubs': [2, 4, 7], 'fe': False, 'subject': 'Physics', 'substrand': '4.1', 'name': 'Greenhouse Effect and Climate Change'},
    'phys_4_2': {'stubs': [4, 6, 7, 9], 'fe': False, 'subject': 'Physics', 'substrand': '4.2', 'name': 'Introduction to Space Physics'},
    'math_1_1': {'stubs': [6], 'fe': False, 'subject': 'Mathematics', 'substrand': '1.1', 'name': 'Real Numbers'},
    'math_1_2': {'stubs': [1, 5, 6], 'fe': False, 'subject': 'Mathematics', 'substrand': '1.2', 'name': 'Indices'},
    'math_1_3': {'stubs': [2, 4, 7], 'fe': False, 'subject': 'Mathematics', 'substrand': '1.3', 'name': 'Quadratic Equations'},
    'math_2_1': {'stubs': [1, 9, 10], 'fe': False, 'subject': 'Mathematics', 'substrand': '2.1', 'name': 'Similarity and Enlargement'},
    'math_2_3': {'stubs': [3, 5, 10], 'fe': False, 'subject': 'Mathematics', 'substrand': '2.3', 'name': 'Area of Part of a Circle'},
    'math_3_1': {'stubs': [1, 3, 9], 'fe': False, 'subject': 'Mathematics', 'substrand': '3.1', 'name': 'Trigonometry I'},
    'math_3_2': {'stubs': [7], 'fe': False, 'subject': 'Mathematics', 'substrand': '3.2', 'name': 'Rotation'},
    'math_3_3': {'stubs': [1, 4], 'fe': False, 'subject': 'Mathematics', 'substrand': '3.3', 'name': 'Vectors I'},
    'math_3_4': {'stubs': [1, 2], 'fe': False, 'subject': 'Mathematics', 'substrand': '3.4', 'name': 'Linear Motion'},
    'math_4_1': {'stubs': [4, 6], 'fe': False, 'subject': 'Mathematics', 'substrand': '4.1', 'name': 'Statistics I'},
    'math_4_2': {'stubs': [3], 'fe': False, 'subject': 'Mathematics', 'substrand': '4.2', 'name': 'Probability I'},
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_unit(output_name):
    """Extract UNIT data from existing data file via node."""
    result = subprocess.check_output(['node', '-e', f"""
var d = require('./generators/data/{output_name}_data.js');
console.log(JSON.stringify({{
  phenomenon:      d.UNIT.phenomenon      || d.UNIT.anchoringPhenomenon || '',
  drivingQuestion: d.UNIT.drivingQuestion || d.UNIT.drivingQuestion     || '',
  storyline:       d.UNIT.storyline       || d.UNIT.storylineThread     || '',
  substrand:       d.UNIT.substrand       || '',
  strand:          d.UNIT.strand          || '',
  lessons_count:   d.LESSONS.length
}}, null, 2));
"""], text=True)
    return json.loads(result)


def get_lesson_context(output_name, lesson_num):
    """Get neighbouring lessons for context."""
    result = subprocess.check_output(['node', '-e', f"""
var d = require('./generators/data/{output_name}_data.js');
var prev = d.LESSONS.filter(function(l) {{ return l.number < {lesson_num} && l.overview && l.overview.length > 50; }});
var last = prev.length ? prev[prev.length-1] : null;
console.log(JSON.stringify({{
  prev_title:   last ? last.title : '',
  prev_summary: last ? (last.summaryTablePrompt ? last.summaryTablePrompt.learned : '') : '',
  total:        d.LESSONS.length
}}));
"""], text=True)
    return json.loads(result)


def get_lessons_for_fe(output_name):
    """Get lesson titles for FE generation context."""
    result = subprocess.check_output(['node', '-e', f"""
var d = require('./generators/data/{output_name}_data.js');
var titles = d.LESSONS.map(function(l) {{ return 'Lesson ' + l.number + ': ' + l.title; }});
console.log(titles.join('\\n'));
"""], text=True)
    return result.strip()


def call_claude(prompt, max_tokens=8192):
    """Call Claude and parse JSON response with retries."""
    for attempt in range(3):
        try:
            response = CLIENT.messages.create(
                model=MODEL, max_tokens=max_tokens,
                system=SYSTEM,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.content[0].text.strip()
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)
            raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw)
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"    JSON error attempt {attempt+1}: {e}")
            if attempt < 2:
                time.sleep(3)
    return None


def patch_lesson(output_name, lesson_num, lesson_data):
    """Replace stub lesson in data file with real content via patch_lesson.js."""
    tmp_path = f'/tmp/{output_name}_lesson{lesson_num}.json'
    with open(tmp_path, 'w') as f:
        json.dump(lesson_data, f, ensure_ascii=False, indent=2)
    result = subprocess.run(
        ['node', 'scripts/patch_lesson.js', output_name, str(lesson_num), tmp_path],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"    {result.stdout.strip()}")
        return True
    print(f"    patch_lesson.js error: {result.stderr[:200]}")
    return False


def patch_fe(output_name, fe_data):
    """Replace null FINAL_EXPLANATION with real content."""
    path = f'generators/data/{output_name}_data.js'
    with open(path) as f:
        js = f.read()

    fe_json = json.dumps(fe_data, indent=2, ensure_ascii=False)
    new_js = re.sub(
        r'const FINAL_EXPLANATION = null;',
        f'const FINAL_EXPLANATION = {fe_json};',
        js
    )

    if new_js != js:
        with open(path, 'w') as f:
            f.write(new_js)
        return True
    return False


# ── Lesson generation prompt ──────────────────────────────────────────────────

LESSON_SCHEMA = ('{"lesson": {"number": N, "title": "FILL", "duration": "40 minutes", '
                 '"substrand": "FILL", "aresKeywords": "FILL", '
                 '"slo": {"purpose": "FILL", "knowledge": "FILL", "skills": "FILL", '
                 '"attitudes": "FILL", "keyInquiry": "FILL", "purposeInStoryline": "FILL", '
                 '"safetyNotes": "FILL"}, "overview": "FILL", '
                 '"framework": ['
                 '{"phase": "Predict Phase", "learnerExperience": "FILL", "teacherMoves": "FILL", "sensemakingStrategy": "FILL", "formativeAssessment": "FILL"},'
                 '{"phase": "Observe Phase", "learnerExperience": "FILL", "teacherMoves": "FILL", "sensemakingStrategy": "FILL", "formativeAssessment": "FILL"},'
                 '{"phase": "Explain Phase", "learnerExperience": "FILL", "teacherMoves": "FILL", "sensemakingStrategy": "FILL", "formativeAssessment": "FILL"},'
                 '{"phase": "Driving Question Board (DQB) Creation", "learnerExperience": "FILL", "teacherMoves": "FILL", "sensemakingStrategy": "FILL", "formativeAssessment": "FILL"},'
                 '{"phase": "Model Building Phase", "learnerExperience": "FILL", "teacherMoves": "FILL", "sensemakingStrategy": "FILL", "formativeAssessment": "FILL"}'
                 '], "teacherReflection": "FILL", '
                 '"summaryTablePrompt": {"observed": "FILL", "learned": "FILL", "explained": "FILL"}}}')


def generate_lesson(output_name, lesson_num, repair):
    unit    = get_unit(output_name)
    context = get_lesson_context(output_name, lesson_num)
    total   = context['total']

    pos = ('opening lesson launching the phenomenon' if lesson_num == 1
           else 'final consolidation lesson' if lesson_num == total
           else f'lesson {lesson_num} of {total} in the evidence-gathering sequence')

    prompt = (
        f"Generate Lesson {lesson_num} ({pos}) for:\n"
        f"Subject: {repair['subject']} Grade 10\n"
        f"Sub-strand: {repair['substrand']} {repair['name']}\n"
        f"Driving question: {unit['drivingQuestion']}\n"
        f"Phenomenon: {unit['phenomenon']}\n"
        f"Storyline: {unit['storyline']}\n\n"
        f"Previous lesson: {context['prev_title']}\n"
        f"Previous learning: {context['prev_summary']}\n\n"
        f"Requirements:\n"
        f"- Connect all phases back to the phenomenon\n"
        f"- Kenya-relevant contexts (local food, places, scientists)\n"
        f"- Teacher moves with specific quotes and WAIT TIME instructions\n"
        f"- {'Introduce phenomenon and open DQB' if lesson_num == 1 else 'Advance the driving question with new evidence'}\n\n"
        f"Return ONLY this JSON with all FILL values replaced:\n"
        f"{LESSON_SCHEMA.replace('N', str(lesson_num))}"
    )

    result = call_claude(prompt)
    if result:
        return result.get('lesson', result)
    return None


# ── FE generation ─────────────────────────────────────────────────────────────

FE_SCHEMA = ('{"subjectLabel": "FILL IN CAPS", '
             '"instructions": "FILL - multi-sentence student instructions", '
             '"sections": ['
             '{"title": "SECTION 1: TITLE IN CAPS", "prompt": "FILL", "exemplar": "FILL - 2-3 paragraphs with Kenyan examples"}'
             '], '
             '"rubric": ['
             '{"criterion": "FILL", "excellent": "FILL", "proficient": "FILL", "developing": "FILL"}'
             ']}')


def generate_fe(output_name, repair):
    unit   = get_unit(output_name)
    titles = get_lessons_for_fe(output_name)

    prompt = (
        f"Generate a Final Explanation assessment document for:\n"
        f"Subject: Biology Grade 10\n"
        f"Sub-strand: {repair['substrand']} {repair['name']}\n"
        f"Driving question: {unit['drivingQuestion']}\n"
        f"Phenomenon: {unit['phenomenon']}\n\n"
        f"Lessons completed:\n{titles}\n\n"
        f"Include 4-5 sections covering the main content areas.\n"
        f"Include 4-5 rubric criteria.\n"
        f"Exemplar answers must use Kenyan contexts.\n\n"
        f"Return ONLY this JSON with all FILL values replaced:\n"
        f"{FE_SCHEMA}"
    )

    return call_claude(prompt, max_tokens=5000)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    total_fixed = 0

    for output_name, repair in REPAIRS.items():
        stubs = repair['stubs']
        need_fe = repair['fe']

        if not stubs and not need_fe:
            print(f"{output_name}: nothing to repair")
            continue

        print(f"\n{'='*50}")
        print(f"Repairing {output_name} ({repair['name']})")

        # Fix stub lessons
        for lesson_num in stubs:
            print(f"  Generating Lesson {lesson_num}...")
            lesson = generate_lesson(output_name, lesson_num, repair)
            if lesson:
                if patch_lesson(output_name, lesson_num, lesson):
                    print(f"  Lesson {lesson_num} patched")
                    total_fixed += 1
                else:
                    print(f"  WARNING: Could not patch Lesson {lesson_num} — saving to /tmp/{output_name}_lesson{lesson_num}.json")
                    with open(f'/tmp/{output_name}_lesson{lesson_num}.json', 'w') as f:
                        json.dump(lesson, f, indent=2, ensure_ascii=False)
            else:
                print(f"  ERROR: Failed to generate Lesson {lesson_num}")
            time.sleep(1)

        # Fix missing FE
        if need_fe:
            print(f"  Generating Final Explanation...")
            fe = generate_fe(output_name, repair)
            if fe:
                if patch_fe(output_name, fe):
                    print(f"  Final Explanation patched")
                    total_fixed += 1
                else:
                    print(f"  WARNING: Could not patch FE — saving to /tmp/{output_name}_fe.json")
                    with open(f'/tmp/{output_name}_fe.json', 'w') as f:
                        json.dump(fe, f, indent=2, ensure_ascii=False)
            else:
                print(f"  ERROR: Failed to generate Final Explanation")

        # Regenerate docx for this sub-strand
        print(f"  Regenerating docx...")
        result = subprocess.run(
            ['node', 'generators/generate.js', output_name],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  {result.stdout.strip().split(chr(10))[-1]}")
        else:
            print(f"  Generator error: {result.stderr[:200]}")

    print(f"\n{'='*50}")
    print(f"Repairs complete. {total_fixed} items fixed.")
    print("Run the check script again to verify.")


if __name__ == '__main__':
    main()
