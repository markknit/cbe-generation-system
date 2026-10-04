#!/usr/bin/env python3
"""
generate_substrand.py — CBE Lesson Plan Content Generator
==========================================================
Generates a complete sub-strand data module for the universal generator
by calling the Claude API with KICD curriculum content and teacher templates.

Usage:
    python3 src/generate_substrand.py \\
        --subject biology \\
        --substrand 1.4 \\
        --output bio_1_4 \\
        --lessons 6 \\
        [--template "data/raw/CBE LESSON TEMPLATES/Biology 10.1.4 ...docx"] \\
        [--run]

Outputs: generators/data/<output>_data.js
Then optionally runs: node generators/generate.js <output>
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# ── Bootstrap ────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / '.env')
except ImportError:
    pass

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not found. Run: pip install anthropic")
    sys.exit(1)

MODEL = os.environ.get('CLAUDE_MODEL', 'claude-sonnet-5-5')
EFFORT = os.environ.get('CLAUDE_EFFORT', 'high')   # output_config.effort; same as config/quiz_generation.yaml
CLIENT = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

# ── Per-run cost tracking (added 2026-07-30) ─────────────────────────────────
# WORKFLOW.md's cost estimates turned out to be far off actual spend on the
# 2026-07-30 General Science run — partly because repair passes (live-mode
# calls fixing stub lessons found after the fact) aren't in the original
# estimate at all. This tracks real usage per run so future estimates can be
# checked against actual spend instead of a generic per-lesson table.
PRICE_PER_MTOK = {
    'sync':  {'input': 2.0,  'output': 10.0},   # live/--run calls (call_claude) — claude-sonnet-5-5
    'batch': {'input': 1.0,  'output': 5.0},    # Message Batches API
}
_USAGE = {
    'sync_input': 0, 'sync_output': 0, 'sync_calls': 0,
    'batch_input': 0, 'batch_output': 0, 'batch_requests': 0,
}


def _track_sync_usage(response) -> None:
    """Record token usage from a live (call_claude) API response."""
    usage = getattr(response, 'usage', None)
    if usage is None:
        return
    _USAGE['sync_input']  += getattr(usage, 'input_tokens', 0) or 0
    _USAGE['sync_output'] += getattr(usage, 'output_tokens', 0) or 0
    _USAGE['sync_calls']  += 1


def _track_batch_usage(message) -> None:
    """Record token usage from one successful Message Batches API result."""
    usage = getattr(message, 'usage', None)
    if usage is None:
        return
    _USAGE['batch_input']    += getattr(usage, 'input_tokens', 0) or 0
    _USAGE['batch_output']   += getattr(usage, 'output_tokens', 0) or 0
    _USAGE['batch_requests'] += 1


def _estimate_cost() -> float:
    sync_cost  = (_USAGE['sync_input']  / 1_000_000) * PRICE_PER_MTOK['sync']['input']
    sync_cost += (_USAGE['sync_output'] / 1_000_000) * PRICE_PER_MTOK['sync']['output']
    batch_cost  = (_USAGE['batch_input']  / 1_000_000) * PRICE_PER_MTOK['batch']['input']
    batch_cost += (_USAGE['batch_output'] / 1_000_000) * PRICE_PER_MTOK['batch']['output']
    return sync_cost + batch_cost


def log_run_cost(output_name: str, mode: str) -> None:
    """Append this run's token usage and estimated cost to logs/api_cost_log.md.

    `mode` is a short label for what kind of run this was (e.g. 'run',
    'batch-submit', 'collect', 'repair') so the log can be skimmed for
    which activity actually drove spend.
    """
    import datetime
    log_path = PROJECT_ROOT / 'logs' / 'api_cost_log.md'
    log_path.parent.mkdir(exist_ok=True)

    cost = _estimate_cost()
    if _USAGE['sync_calls'] == 0 and _USAGE['batch_requests'] == 0:
        return  # nothing to log (e.g. batch submitted but not yet collected)

    if not log_path.exists():
        log_path.write_text(
            "# API cost log\n\n"
            "Actual per-run token usage and estimated cost, logged automatically by "
            "`generate_substrand.py`. Cross-check against WORKFLOW.md's Model and "
            "Cost Reference table periodically — if actual spend consistently runs "
            "above the documented contingency, the estimate needs revising.\n\n"
            "| Timestamp (UTC) | Output | Mode | Sync in/out tokens | Batch in/out tokens | Est. cost |\n"
            "|---|---|---|---|---|---|\n"
        )

    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    with open(log_path, 'a') as f:
        f.write(
            f"| {timestamp} | {output_name} | {mode} "
            f"| {_USAGE['sync_input']:,}/{_USAGE['sync_output']:,} "
            f"| {_USAGE['batch_input']:,}/{_USAGE['batch_output']:,} "
            f"| ${cost:.4f} |\n"
        )
    print(f"  Logged run cost to {log_path} (${cost:.4f} estimated)")

# ── Curriculum extraction ─────────────────────────────────────────────────────

def slice_curriculum_text(text: str, substrand_id: str) -> str:
    """Cut one sub-strand's section out of a whole-curriculum OCR text file.

    In the KICD design tables each sub-strand's section opens with a line that
    holds its number and "By the end of the sub strand"; the section runs to the
    next such line for a different sub-strand. Returns '' if not found, so the
    caller can fall back to the full text and say so.
    """
    lines = text.split('\n')
    starts = []
    for i, l in enumerate(lines):
        if re.search(r'By the end of the sub', l, re.I):
            # The line also carries the strand number ("2.0 Anatomy 2.1 ..."); the
            # sub-strand is the first number that isn't a strand (X.0).
            # No \b after the number: OCR often drops the space ("1.1The Mole").
            ids = [n for n in re.findall(r'(?<![\d.])\d{1,2}\.\d{1,2}(?!\d)', l) if not n.endswith('.0')]
            if ids:
                starts.append((i, ids[0]))
    # Duplicated OCR page slices repeat a section opener (seen for 3.2); the
    # first occurrence starts the section, the next *different* id ends it.
    begin = next((i for i, sid in starts if sid == substrand_id), None)
    if begin is None:
        return ''
    end = next((i for i, sid in starts if i > begin and sid != substrand_id), len(lines))
    # KICD groups a whole strand's assessment rubrics after its last sub-strand
    # (all four Grade 11 subjects checked), followed by the next STRAND heading
    # or the appendices. Stop there, or the last sub-strand of each strand
    # carries every sibling's rubric (Core Maths 1.7: 13k chars, 80% rubric).
    # Case-sensitive on purpose: the repeated per-page column header reads
    # "Strand Sub Strand Specific Learning ...", which must NOT end a section.
    stop = re.compile(r'[Aa]ssessment [Rr]ubric|^\s*STRAND\b|^\s*APPENDIX\b')
    end = next((i for i in range(begin + 1, end) if stop.search(lines[i])), end)
    # Keep the table's column-header line, which sits just above the opener.
    if begin > 0 and 'Specific Learning' in lines[begin - 1]:
        begin -= 1
    return '\n'.join(lines[begin:end]).strip()


def extract_curriculum_pdf(pdf_path: str, substrand_id: str) -> str:
    """Extract sub-strand section from KICD curriculum PDF."""
    try:
        import pdfminer.high_level as pdfminer
        text = pdfminer.extract_text(pdf_path)
    except Exception as e:
        print(f"  WARNING: Could not extract PDF: {e}")
        return ""

    # Search for sub-strand section using various patterns
    subject_num = substrand_id.split('.')[0]
    sub_num     = substrand_id.split('.')[1] if '.' in substrand_id else ''

    # Try to find the section
    patterns = [
        f"{subject_num}.{sub_num} ",
        f"Sub Strand {subject_num}.{sub_num}",
        f"SUB STRAND {subject_num}.{sub_num}",
    ]

    start_idx = -1
    for pattern in patterns:
        idx = text.find(pattern, 20000)   # skip past table of contents
        if idx > 0:
            # Verify it's the content section (not TOC) by checking for SLO language
            snippet = text[idx:idx+500]
            if any(kw in snippet for kw in ['learner should', 'Learner should', 'Learning Outcomes', 'By the end']):
                start_idx = idx
                break
            elif start_idx == -1:
                start_idx = idx   # use first hit as fallback

    if start_idx == -1:
        print(f"  WARNING: Sub-strand {substrand_id} not found in curriculum PDF")
        return ""

    # Extract ~4000 chars which should cover the full sub-strand entry
    raw = text[start_idx:start_idx + 4500]
    # Clean up the fragmented PDF text
    raw = re.sub(r'  +', ' ', raw)        # collapse multiple spaces
    raw = re.sub(r'\n +\n', '\n\n', raw)  # clean blank lines
    return raw.strip()


# Label prefixes in the "CBE PHENOMENON-DRIVEN LESSON SEQUENCE — Teacher
# Planning Template" form (Grade 11 templates, 2026-09-30). Matched against the
# first line of the label cell, lower-cased; the value is the next cell.
_FORM_FIELDS = [
    ('number of lessons', 'lesson_count_text'),
    ('periods per lesson', 'periods'),
    ('kicd learning outcomes', 'learning_outcomes'),
    ('kicd key inquiry', 'key_inquiry'),
    ('key concepts', 'key_concepts'),
    ('the anchoring phenomenon', 'phenomenon'),
    ('the driving question', 'driving_question'),
    ('why this will grab', 'hook'),
    ('how students show their first thinking', 'first_thinking'),
    ('prior knowledge', 'prior_knowledge'),
    ('sense-making strategies', 'sensemaking'),
    ('formative assessment', 'formative'),
    ('final product', 'final_product'),
    ('practical constraints', 'constraints'),
    ('core competencies', 'competencies'),
    ('core values', 'values'),
    ('pertinent', 'pcis'),
    ('career', 'careers'),
]


def _parse_planning_form(rows: list) -> dict:
    """Parse the Teacher Planning Template form (Parts 1-8) from table rows.

    The Grade 10 scheme-of-work templates keep their content in paragraphs;
    this form keeps almost all of it in tables, including the Part 4 lesson
    spine ("the part AI cannot invent"). Returns {} for anything that is not
    this form, so Grade 10 templates are unaffected.
    """
    def first_line(c):
        return c.split('\n', 1)[0].strip().lower()
    if not any(r and 'LESSON SPINE' in r[0].upper() for r in rows):
        return {}

    form, spine, part = {}, [], ''
    spine_cols = []
    for r in rows:
        head = r[0].strip()
        if head.upper().startswith('PART '):
            part = head.split('·')[0].strip().upper()      # e.g. 'PART 4', 'PART 6B'
            continue
        if part == 'PART 4':
            if first_line(head) == 'lesson' and len(r) > 1:
                spine_cols = [first_line(c) for c in r[1:]]
                continue
            if head.lower().startswith('e.g') or head.lower().startswith('one row per lesson') or len(r) < 2:
                continue
            cols = spine_cols or [f'col{i}' for i in range(1, len(r))]
            # Teachers fill the Lesson cell three ways: "4"; "2. Kingdom
            # Plantae" (number + title); or blank/garbled (e.g. "1123" from
            # Word list numbering), where the row's cells shift left because
            # empty cells are dropped. Number those rows in order.
            m = re.match(r'(\d{1,2})(?!\d)\.?\s*(.*)', head, re.S)
            if len(r) == len(cols) + 1 and m:
                number, title, cells = int(m.group(1)), m.group(2).strip(), r[1:]
            elif len(r) == len(cols) + 1:
                number, title, cells = len(spine) + 1, '' if re.fullmatch(r'\d+', head) else head, r[1:]
            else:
                number, title, cells = len(spine) + 1, '', r
            row = {'number': number, 'cells': dict(zip(cols, cells))}
            if title:
                row['cells'] = {'lesson title': title, **row['cells']}
            spine.append(row)
            continue
        if part == 'PART 6':
            if len(r) == 1 and not head.lower().startswith('write out'):
                form['final_explanation'] = (form.get('final_explanation', '') + '\n' + head).strip()
            continue
        if part == 'PART 8':
            if len(r) == 1:
                form['anything_else'] = (form.get('anything_else', '') + '\n' + head).strip()
            continue
        if len(r) >= 2:
            label = first_line(head)
            for prefix, key in _FORM_FIELDS:
                if label.startswith(prefix) and key not in form:
                    form[key] = r[1].strip()
                    break
    m = re.search(r'\d{1,2}', form.get('lesson_count_text', ''))
    if m:
        form['lesson_count'] = int(m.group(0))
    elif spine:
        form['lesson_count'] = len(spine)   # "Number of lessons" left blank: the spine is the plan
    form['spine'] = spine
    return form


def _spine_row_text(row: dict) -> str:
    return '\n'.join(f'- {k.rstrip("?:")}: {v}' for k, v in row['cells'].items())


def template_unit_context(template: dict) -> str:
    """Extra UNIT-prompt sections from a planning-form template ('' otherwise)."""
    f = template.get('form') if template else None
    if not f:
        return ''
    parts = []
    for key, title in [('driving_question', "DRIVING QUESTION (the teacher's; keep its meaning)"),
                       ('key_inquiry', 'KICD KEY INQUIRY QUESTIONS (as entered by the teacher)'),
                       ('key_concepts', 'KEY CONCEPTS STUDENTS MUST END UP UNDERSTANDING'),
                       ('hook', 'WHY THIS PHENOMENON WILL GRAB THESE STUDENTS'),
                       ('prior_knowledge', 'PRIOR KNOWLEDGE AND MISCONCEPTIONS'),
                       ('competencies', 'WHERE CORE COMPETENCIES HAPPEN (teacher notes)'),
                       ('values', 'WHERE CORE VALUES HAPPEN (teacher notes)'),
                       ('pcis', 'PERTINENT AND CONTEMPORARY ISSUES (teacher notes)'),
                       ('careers', 'CAREER CONNECTIONS'),
                       ('constraints', 'PRACTICAL CONSTRAINTS TO RESPECT')]:
        if f.get(key):
            parts.append(f'TEACHER TEMPLATE — {title}:\n{f[key]}')
    if f.get('spine'):
        parts.append("TEACHER TEMPLATE — LESSON SPINE (storylineThread MUST follow this, "
                     "one line per lesson, same order):\n" +
                     '\n'.join(f"Lesson {r['number']}: " + ' | '.join(r['cells'].values()) for r in f['spine']))
    return '\n\n'.join(parts)


def template_lesson_context(template: dict, num: int) -> str:
    """The lesson prompt's template section. Planning-form templates give this
    lesson's own spine row; older templates keep the generic evidence text."""
    f = template.get('form') if template else None
    if not f:
        return f"TEACHER TEMPLATE — EVIDENCE ACTIVITIES:\n{template.get('evidence_activities', '') if template else ''}"
    parts = []
    row = next((r for r in f.get('spine', []) if r['number'] == num), None)
    if row:
        parts.append("TEACHER'S PLAN FOR THIS LESSON (build the lesson around this; "
                     "keep its evidence activity and resources):\n" + _spine_row_text(row))
    for key, title in [('sensemaking', 'SENSE-MAKING STRATEGIES THE TEACHER WANTS USED'),
                       ('formative', 'FORMATIVE ASSESSMENT THE TEACHER WANTS USED'),
                       ('constraints', 'PRACTICAL CONSTRAINTS TO RESPECT'),
                       ('anything_else', 'OTHER TEACHER NOTES')]:
        if f.get(key):
            parts.append(f'{title}:\n{f[key]}')
    if num == 1 and f.get('first_thinking'):
        parts.append(f"HOW STUDENTS SHOW THEIR FIRST THINKING:\n{f['first_thinking']}")
    return '\n\n'.join(parts)


def template_fe_context(template: dict) -> str:
    """The teacher's own model final explanation, from a planning-form template."""
    f = template.get('form') if template else None
    if not f or not f.get('final_explanation'):
        return ''
    out = ("\nTEACHER'S MODEL FINAL EXPLANATION (scientifically authoritative; base the "
           "exemplars on it, in student-accessible language):\n" + f['final_explanation'])
    if f.get('final_product'):
        out += f"\n\nFINAL PRODUCT STUDENTS WILL PRODUCE:\n{f['final_product']}"
    return out + '\n'


def extract_template_docx(docx_path: str) -> dict:
    """Extract content from teacher-authored SoW template docx."""
    try:
        from docx import Document
        doc = Document(docx_path)
    except Exception as e:
        print(f"  WARNING: Could not read template: {e}")
        return {}

    result = {
        'paragraphs': [],
        'table_content': [],
        'phenomenon': '',
        'lesson_sequence': '',
        'learning_outcomes': '',
        'core_competencies': [],
        'core_values': [],
        'evidence_activities': '',
        'final_explanation_notes': '',
    }

    # Extract paragraphs
    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            result['paragraphs'].append(text)
            # Capture specific fields
            if 'Learning Outcomes' in text and len(text) > 50:
                result['learning_outcomes'] = text
            if 'Student-facing objective' in text:
                result['student_objective'] = text

    # Detect competencies and values from paragraphs
    capture_comp = False
    capture_val  = False
    for p in doc.paragraphs:
        text = p.text.strip()
        if 'CORE COMPETENCIES' in text:
            capture_comp = True
            capture_val  = False
            continue
        if 'CORE VALUES' in text:
            capture_val  = True
            capture_comp = False
            continue
        if capture_comp and text and ':' in text:
            result['core_competencies'].append(text.split(':')[0].strip())
        if capture_val and text and len(text) > 5:
            result['core_values'].append(text)

    # Extract table content
    for table in doc.tables:
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                ct = cell.text.strip()
                if ct:
                    row_data.append(ct)
            if row_data:
                result['table_content'].append(row_data)

    # Find phenomenon (usually in row with "PHENOMENON")
    for row in result['table_content']:
        for i, cell in enumerate(row):
            if 'PHENOMENON' in cell.upper() and i + 1 < len(row):
                result['phenomenon'] = row[i + 1][:500]
                break

    # Find lesson sequence
    for row in result['table_content']:
        for i, cell in enumerate(row):
            if 'LESSON SEQUENCE' in cell.upper() and i + 1 < len(row):
                result['lesson_sequence'] = row[i + 1][:800]
                break

    # Find evidence activities
    for row in result['table_content']:
        for i, cell in enumerate(row):
            if 'EVIDENCE GATHERED' in cell.upper() and i + 1 < len(row):
                result['evidence_activities'] = row[i + 1][:800]
                break

    # Find final explanation notes
    for row in result['table_content']:
        for i, cell in enumerate(row):
            if 'FINAL EXPLANATION' in cell.upper() and i + 1 < len(row):
                result['final_explanation_notes'] = row[i + 1][:400]
                break

    form = _parse_planning_form(result['table_content'])
    if form:
        result['form'] = form
        result['phenomenon'] = form.get('phenomenon', result['phenomenon'])
        result['learning_outcomes'] = form.get('learning_outcomes', '')
        result['lesson_sequence'] = '\n'.join(
            f"Lesson {r['number']}: {next(iter(r['cells'].values()), '')}" for r in form['spine'])
        result['final_explanation_notes'] = form.get('final_explanation', '')[:400]

    return result


# ── System prompt ─────────────────────────────────────────────────────────────

def build_system_prompt(grade: int) -> str:
    return f"""You are an expert curriculum designer for Kenya's Grade {grade} CBE (Competency-Based Curriculum).
You generate structured lesson plan content for the ARES Education offline learning platform.

YOUR OUTPUTS:
- Always respond with valid JSON only — no markdown fences, no explanations, no preamble
- Follow the exact JSON schema provided in each request
- Use Kenya-relevant contexts, examples, scientists, food items, and place names throughout
- Embed NGSS Science and Engineering Practices where indicated
- All KICD-mandated text (learning outcomes, competencies, values, PCIs) must be used verbatim
- Write teacher actions as specific, actionable instructions (include WAIT TIME, cold-call counts, specific questions)
- Connect every lesson phase back to the anchoring phenomenon

LESSON STRUCTURE (5 phases):
1. Predict Phase — students predict before instruction
2. Observe Phase — evidence gathering (experiment, video, reading, simulation)
3. Explain Phase — sensemaking, applying knowledge
4. Driving Question Board (DQB) Creation — tracking growing understanding
5. Model Building Phase — cumulative model revision

KENYA CONTEXT RULES:
- Use Kenyan food examples (ugali, sukuma wiki, nyama choma, githeri, mandazi, maize, beans)
- Reference Kenyan scientists, athletes, farmers where relevant
- Use Kenyan place names (Nairobi, Mombasa, Kisumu, Kericho, Rift Valley, Lake Victoria)
- Prefer local Kenyan contexts over Western examples
"""

# Module-level default (Grade 10) so anything that imports this module and
# references SYSTEM_PROMPT before main() runs (tests, --collect mode, a
# future REPL/import use) still gets a valid string. main() overwrites this
# with the real target grade as its first act — see "grade" below.
SYSTEM_PROMPT = build_system_prompt(10)

# ── Claude API call ───────────────────────────────────────────────────────────

# ── Output schemas for structured generation ──────────────────────────────────
# Generating via structured outputs (rather than free-text JSON) guarantees well-formed
# output and biases the model to the ares-contract shape. additionalProperties
# is False so stray keys (e.g. legacy 'storyline', top-level 'safetyNotes')
# cannot appear; required sets mirror docs/SCHEMA.md / ares-contract.schema.json.

def _s(desc: str = "") -> dict:
    return {"type": "string", "description": desc} if desc else {"type": "string"}

UNIT_TOOL_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "gradeLevel": _s(), "subject": _s(), "strand": _s(), "substrand": _s(),
        "totalDuration": _s(),
        "content": _s("KICD sub-strand content; bullet list, one topic per line prefixed with •"),
        "learningOutcomes": _s(), "coreCompetencies": _s(), "values": _s(),
        "sep": _s(), "pcis": _s(), "careers": _s(), "focus": _s(),
        "phenomenon": _s(), "supportingPhenomena": _s(),
        "drivingQuestion": _s(), "storylineThread": _s(),
    },
    "required": ["gradeLevel", "subject", "strand", "substrand", "totalDuration",
                 "content", "learningOutcomes", "coreCompetencies",
                 "phenomenon", "drivingQuestion", "storylineThread"],
}

CANONICAL_PHASES = ["Predict Phase", "Observe Phase", "Explain Phase",
                    "Driving Question Board (DQB) Creation", "Model Building Phase"]

LESSON_TOOL_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "number": {"type": "integer"},
        "title": _s(), "duration": _s(), "substrand": _s(), "aresKeywords": _s(),
        "slo": {
            "type": "object", "additionalProperties": False,
            "properties": {"purpose": _s(), "knowledge": _s(), "skills": _s(),
                           "attitudes": _s(), "keyInquiry": _s(),
                           "purposeInStoryline": _s(), "safetyNotes": _s()},
            "required": ["purpose", "knowledge", "skills", "attitudes",
                         "keyInquiry", "purposeInStoryline", "safetyNotes"],
        },
        "overview": _s(),
        "framework": {
            "type": "array",
            "items": {
                "type": "object", "additionalProperties": False,
                # enum, not free text: on 2026-09-30 both Sonnet 5.5 and 4.6 decorated
                # labels ("Phase 1: Predict (about 15 minutes)"), which fails the
                # contract and the link gate. Structured outputs enforces the enum.
                "properties": {"phase": {"type": "string", "enum": CANONICAL_PHASES},
                               "learnerExperience": _s(),
                               "teacherMoves": _s(), "sensemakingStrategy": _s(),
                               "formativeAssessment": _s()},
                "required": ["phase", "learnerExperience", "teacherMoves",
                             "sensemakingStrategy", "formativeAssessment"],
            },
        },
        "teacherReflection": _s(),
        "summaryTablePrompt": {
            "type": "object", "additionalProperties": False,
            "properties": {"observed": _s(), "learned": _s(), "explained": _s()},
            "required": ["observed", "learned", "explained"],
        },
    },
    "required": ["number", "title", "duration", "substrand", "slo", "overview",
                 "framework", "teacherReflection", "summaryTablePrompt"],
}

FE_TOOL_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "subjectLabel": _s(), "instructions": _s(),
        "sections": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"title": _s(), "prompt": _s(), "exemplar": _s()},
            "required": ["title", "prompt", "exemplar"]}},
        "rubric": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"criterion": _s(), "excellent": _s(),
                           "proficient": _s(), "developing": _s()},
            "required": ["criterion", "excellent", "proficient", "developing"]}},
    },
    "required": ["subjectLabel", "instructions", "sections"],
}

ST_TOOL_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "subStrand": _s(), "drivingQuestion": _s(),
        "lessons": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"number": {"type": "integer"}, "title": _s(),
                           "observed": _s(), "learned": _s(), "explained": _s()},
            "required": ["number", "title", "observed", "learned", "explained"]}},
    },
    "required": ["subStrand", "drivingQuestion", "lessons"],
}


def _schema_violations(obj, schema, path: str = "") -> list:
    """Dependency-free structural check against the (simple) tool schemas above.
    Catches what crashes the docx layer or breaks the contract: a field declared
    array/object arriving as a string, or a missing/empty required field."""
    t = schema.get("type")
    types = t if isinstance(t, list) else ([t] if t else [])

    def kind(v):
        if isinstance(v, bool):  return "boolean"
        if isinstance(v, str):   return "string"
        if isinstance(v, int):   return "integer"
        if isinstance(v, float): return "number"
        if isinstance(v, list):  return "array"
        if isinstance(v, dict):  return "object"
        if v is None:            return "null"
        return "unknown"

    k = kind(obj)
    if types and k not in types and not (k == "integer" and "number" in types):
        return [f"{path or 'root'}: expected {types}, got {k}"]

    errs = []
    if "object" in types and isinstance(obj, dict):
        for r in schema.get("required", []):
            if r not in obj or obj[r] in (None, ""):
                errs.append(f"{path}{r}: missing/empty required field")
        for key, sub in schema.get("properties", {}).items():
            if key in obj and obj[key] is not None:
                errs += _schema_violations(obj[key], sub, f"{path}{key}.")
    if "array" in types and isinstance(obj, list):
        item = schema.get("items")
        if item:
            for i, el in enumerate(obj):
                errs += _schema_violations(el, item, f"{path}[{i}].")
    return errs


def _structured_params(schema: dict) -> dict:
    """Request fields for schema-constrained JSON output.

    Sonnet 5.5 rejects forced tool_choice (the pre-2026-09-30 mechanism), so the
    schema goes in output_config.format instead. The API then guarantees the
    text block is JSON matching the schema. Thinking is adaptive (Sonnet 5.5
    cannot disable it) and counts against max_tokens, hence the 16000 budgets.
    """
    return {
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": EFFORT,
                          "format": {"type": "json_schema", "schema": schema}},
    }


def _text_of(content) -> str:
    """First text block — content[0] may be a thinking block on Sonnet 5.5."""
    return next((b.text for b in content if getattr(b, "type", None) == "text"), "")


def call_claude(user_prompt: str, max_tokens: int = 16000, retries: int = 3,
                schema: dict | None = None) -> dict | None:
    """Call Claude and return a dict.

    If `schema` (a JSON Schema) is given, output is constrained to it via
    structured outputs, so malformed-JSON failures (unescaped quotes, missing
    delimiters, fence noise) cannot occur. Without a schema, falls back to
    free-text JSON parsing.
    """
    for attempt in range(retries):
        try:
            kwargs = dict(
                model=MODEL,
                max_tokens=max_tokens,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
            if schema is not None:
                kwargs.update(_structured_params(schema))

            response = CLIENT.messages.create(**kwargs)
            _track_sync_usage(response)  # count tokens even on truncated/retried attempts - they're billed regardless

            # Explicit truncation detection (previously surfaced only as a parse error)
            if getattr(response, "stop_reason", None) == "max_tokens":
                print(f"    Truncated (stop_reason=max_tokens, max_tokens={max_tokens}, attempt {attempt+1})")
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                return None

            if getattr(response, "stop_reason", None) == "refusal":
                print(f"    Refused (stop_details={getattr(response, 'stop_details', None)}, attempt {attempt+1})")
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                return None

            if schema is not None:
                text = _text_of(response.content)
                data = json.loads(text) if text else None
                if data is None:
                    print(f"    No text block returned (attempt {attempt+1})")
                    if attempt < retries - 1:
                        time.sleep(2)
                        continue
                    return None
                violations = _schema_violations(data, schema)
                if violations:
                    # e.g. model stuffed an array field into a string — re-roll
                    print(f"    Tool output off-schema (attempt {attempt+1}): {violations[:3]}")
                    if attempt < retries - 1:
                        time.sleep(2)
                        continue
                    return None
                return data

            raw = _text_of(response.content).strip()
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)
            raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw)
            return json.loads(raw)

        except json.JSONDecodeError as e:
            print(f"    JSON parse error (attempt {attempt+1}): {e}")
            if attempt < retries - 1:
                time.sleep(2)
        except anthropic.APIError as e:
            print(f"    API error (attempt {attempt+1}): {e}")
            if attempt < retries - 1:
                time.sleep(5)
        except Exception as e:
            print(f"    Unexpected error (attempt {attempt+1}): {e}")
            if attempt < retries - 1:
                time.sleep(2)

    return None


# ── Unit generation ───────────────────────────────────────────────────────────

def generate_unit(curriculum_text: str, template: dict, args) -> dict | None:
    """Generate the UNIT sub-strand overview data."""
    print("  Generating UNIT data...")

    prompt = f"""Generate the sub-strand overview (UNIT) data for:
Subject: {_subject_display(args.subject)}
Grade: {args.grade}
Sub-strand: {args.substrand} — {args.substrand_name}
Number of lessons: {args.lessons}

KICD CURRICULUM CONTENT (use verbatim for SLOs, competencies, values, PCIs):
{curriculum_text}

TEACHER TEMPLATE — PHENOMENON:
{template.get('phenomenon', '')}

TEACHER TEMPLATE — LESSON SEQUENCE OUTLINE:
{template.get('lesson_sequence', '')}

TEACHER TEMPLATE — LEARNING OUTCOMES:
{template.get('learning_outcomes', '')}

{template_unit_context(template)}

Return ONLY this JSON structure (no other text):
{{
  "gradeLevel": "{args.grade}",
  "subject": "{_subject_display(args.subject)}",
  "strand": "Strand {args.substrand.split('.')[0]}.0: [official KICD strand name]",
  "substrand": "Sub-Strand {args.substrand}: {args.substrand_name}",
  "totalDuration": "{args.lessons} lessons × 40 minutes = {args.lessons * 40} minutes total",
  "content": "bullet list of sub-strand content topics, one per line prefixed with •",
  "learningOutcomes": "By the end of the sub-strand, the learner should be able to:\\na) ...\\nb) ...\\nc) ...\\nd) ...\\ne) ...",
  "coreCompetencies": "• Competency name: description of how developed in this sub-strand\\n• ...",
  "values": "• Value name: description\\n• ...",
  "sep": "• SEP name: how embedded\\n• ...",
  "pcis": "• PCI: description\\n• ...",
  "careers": "• Career: how this sub-strand connects\\n• ...",
  "focus": "2-3 sentence overview of the unit focus and approach",
  "totalDuration": "{args.lessons} lessons (approximately {args.lessons * 2} periods × 40 minutes = {args.lessons * 80} minutes)",
  "phenomenon": "Full description of the anchoring phenomenon including what students observe and why it is puzzling",
  "supportingPhenomena": "• 2-4 additional supporting phenomena\\n• ...",
  "drivingQuestion": "DRIVING QUESTION: [the main driving question]\\n\\nKICD KEY INQUIRY QUESTIONS:\\n1. [verbatim from KICD]\\n2. [verbatim from KICD]",
  "storylineThread": "Lesson 1: [brief description]\\nLesson 2: ...\\n[continue for all {args.lessons} lessons]"
}}"""

    return call_claude(prompt, schema=UNIT_TOOL_SCHEMA)


# ── Lesson generation ─────────────────────────────────────────────────────────

LESSON_SCHEMA = {
    "number": 0,
    "title": "Lesson title — subtitle",
    "duration": "40 minutes",
    "substrand": "Sub-Strand X.Y: Name",
    "aresKeywords": "4-5 specific biology content keywords for ARES search",
    "slo": {
        "purpose": "One sentence describing lesson purpose in storyline",
        "knowledge": "• bullet 1\\n• bullet 2\\n• bullet 3",
        "skills": "• bullet 1\\n• bullet 2",
        "attitudes": "• bullet 1\\n• bullet 2",
        "keyInquiry": "The key question this lesson addresses",
        "purposeInStoryline": "How this lesson advances the storyline",
        "safetyNotes": "Safety considerations or 'No specific hazards.'"
    },
    "overview": "2-3 paragraph prose overview of the lesson...",
    "framework": [
        {
            "phase": "Predict Phase",
            "learnerExperience": "What students do (2-4 sentences)",
            "teacherMoves": "Specific teacher actions with exact quotes, WAIT TIME notes, cold-call counts",
            "sensemakingStrategy": "Name and description of strategy used",
            "formativeAssessment": "What teacher looks for and how to assess"
        },
        {"phase": "Observe Phase", "learnerExperience": "...", "teacherMoves": "...", "sensemakingStrategy": "...", "formativeAssessment": "..."},
        {"phase": "Explain Phase", "learnerExperience": "...", "teacherMoves": "...", "sensemakingStrategy": "...", "formativeAssessment": "..."},
        {"phase": "Driving Question Board (DQB) Creation", "learnerExperience": "...", "teacherMoves": "...", "sensemakingStrategy": "...", "formativeAssessment": "..."},
        {"phase": "Model Building Phase", "learnerExperience": "...", "teacherMoves": "...", "sensemakingStrategy": "...", "formativeAssessment": "..."}
    ],
    "teacherReflection": "3-5 numbered reflection questions for teacher after teaching",
    "summaryTablePrompt": {
        "observed": "What students observed in this lesson",
        "learned": "Key learning from this lesson",
        "explained": "How this explains the phenomenon"
    }
}


def generate_lesson(num: int, curriculum_text: str, template: dict,
                    unit: dict, prev_summaries: list, args, fact_sheet: dict | None = None) -> dict | None:
    """Generate a single lesson."""
    print(f"  Generating Lesson {num}/{args.lessons}...")

    # Build context from previous lessons
    prev_context = ""
    if prev_summaries:
        prev_context = "PREVIOUS LESSONS (for storyline continuity):\n"
        for s in prev_summaries:
            prev_context += f"  Lesson {s['number']}: {s['title']} — {s.get('summary', '')}\n"

    lesson_pos = "opening lesson that launches the phenomenon" if num == 1 else \
                 "final lesson with Final Explanation" if num == args.lessons else \
                 f"lesson {num} of {args.lessons} in the evidence-gathering sequence"

    prompt = f"""Generate Lesson {num} ({lesson_pos}) for:
Subject: {_subject_display(args.subject)} Grade {args.grade}
Sub-strand: {args.substrand} {args.substrand_name}
Driving question: {unit.get('drivingQuestion', '')}
Phenomenon: {unit.get('phenomenon', '')}
Storyline thread for this lesson: {_get_lesson_storyline(unit, num)}

KICD CURRICULUM CONTENT:
{curriculum_text}

{template_lesson_context(template, num)}

{_lesson_fs(fact_sheet, num)}
{prev_context}

RULES:
- All learner experiences must connect back to the phenomenon
- Teacher moves must include specific quoted phrases, WAIT TIME (10-15 seconds minimum), cold-call counts
- Sensemaking strategies: name the strategy and explain how it builds understanding
- Formative assessment: specific, observable indicators
- Kenya-relevant contexts throughout (local food examples, Kenyan scientists, local contexts)
- Lesson {num} should {"introduce the phenomenon and open the DQB" if num == 1 else "build on previous evidence and advance the driving question"}
{"- Final lesson: focus on Final Explanation, model comparison L1 vs final, DQB completion" if num == args.lessons else ""}

Return the lesson as JSON matching the provided schema, with rich, real content in every field.
Field structure for reference (do NOT return any field as a stringified blob):
{json.dumps(LESSON_SCHEMA, indent=2)}

"framework" MUST be an array of 5 separate phase objects (Predict, Observe, Explain,
DQB/Driving Question Board, Model Building) — each an object with phase, learnerExperience,
teacherMoves, sensemakingStrategy, formativeAssessment. Never return framework as a string.
Set "number" to {num}.
Set "substrand" to "Sub-Strand {args.substrand}: {args.substrand_name}".
"""

    result = call_claude(prompt, schema=LESSON_TOOL_SCHEMA)
    if result and 'lesson' in result:
        return result['lesson']
    return result   # in case Claude returns the lesson directly


def _lesson_fs(fact_sheet: dict | None, num: int) -> str:
    if not fact_sheet:
        return ""
    import lesson_consistency as lc
    return lc.fact_sheet_block(fact_sheet, num)


def _get_lesson_storyline(unit: dict, num: int) -> str:
    """Extract this lesson's storyline description from unit data."""
    storyline = unit.get('storylineThread') or unit.get('storyline', '')
    if not storyline:
        return ''
    lines = [l for l in storyline.split('\n') if l.strip()]
    for line in lines:
        if line.strip().startswith(f'Lesson {num}:'):
            return line.strip()
    return lines[num - 1] if num <= len(lines) else ''


# ── Final Explanation & Summary Table generation ──────────────────────────────

VERIFY_TOOL_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "issues": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "properties": {"where": _s(), "problem": _s(),
                           "kind": {"type": "string", "enum": ["final_explanation", "lesson_sequence"]}},
            "required": ["where", "problem", "kind"]}},
    },
    "required": ["issues"],
}


def _log_json(kind: str, name: str, data) -> None:
    d = PROJECT_ROOT / 'logs' / kind
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))


def make_fact_sheet(curriculum_text: str, unit: dict, template: dict, args) -> dict | None:
    """Shared facts + lesson map, generated BEFORE any lesson (src/lesson_consistency.py)."""
    import lesson_consistency as lc
    print("  Generating fact sheet (shared data + lesson map)...")
    fs = lc.generate_fact_sheet(call_claude, _subject_display(args.subject), args.grade,
                                f"{args.substrand} {args.substrand_name}", args.lessons, unit,
                                curriculum_text, (template or {}).get('lesson_sequence', ''))
    if fs:
        _log_json('fact_sheets', args.output, fs)
    else:
        print("  WARNING: fact sheet generation failed — lessons will be generated without it")
    return fs


def consistency_pass(unit: dict, lessons: list, args, fact_sheet: dict | None, name: str) -> None:
    """After the lessons exist: review contradictions between them, repair majors
    with exact edits, keep the best version. Logged to logs/lesson_drift/ and
    logs/lesson_repairs/. Mutates `lessons`."""
    import lesson_consistency as lc
    print("  Checking lessons agree with each other (and the fact sheet)...")
    r = lc.check_and_repair(call_claude, _subject_display(args.subject), args.grade,
                            f"{args.substrand} {args.substrand_name}", unit, lessons, fact_sheet)
    if r["status"] != "ok":
        print("  WARNING: consistency review failed — run scripts/review_lesson_consistency.py later")
        return
    _log_json('lesson_drift', name, {"name": name, "subject": _subject_display(args.subject),
                                     "substrand": args.substrand_name, "lessons": len(lessons),
                                     "conflicts": r["conflicts"]})
    _log_json('lesson_repairs', name, {"module": name, "history": r["history"]})
    print(f"  Lesson consistency: {r['majors']} major contradiction(s) left after repair "
          f"(see logs/lesson_drift/{name}.json)")


def lesson_digest(lessons: list, unit: dict) -> str:
    """What the lessons actually taught: the facts the Final Explanation must
    agree with. Titles alone (the old input) let the model invent its own
    dataset, characters and numbers."""
    out = []
    ph = (unit or {}).get('phenomenon', '')
    if ph:
        out.append(f"PHENOMENON AND ANCHOR DATA:\n{ph}\n")
    for l in lessons:
        stp = l.get('summaryTablePrompt') or {}
        out.append(
            f"LESSON {l.get('number')}: {l.get('title', '')}\n"
            f"  Overview: {l.get('overview', '')}\n"
            f"  What learners observed: {stp.get('observed', '')}\n"
            f"  What learners learned: {stp.get('learned', '')}\n"
            f"  How it explains the phenomenon: {stp.get('explained', '')}\n")
    return "\n".join(out)


FE_RULES = """HARD RULES (a validator and a second reviewer will check every one):
1. GROUNDED IN THE LESSONS. Use the same phenomenon, characters, places and data the
   lessons above used. If the lessons give numbers (times, distances, masses...),
   reuse those exact numbers. Do not invent a second, different dataset.
   The lessons were written separately and may disagree with EACH OTHER about a
   detail. Where they do, treat LESSON 1 (the anchor) and the LAST lesson as
   authoritative, and keep this document consistent with itself. Do not try to
   satisfy every lesson; do not state a contested detail more precisely than the
   authoritative lessons do.
2. If you give the student a data table, it must be internally consistent: check
   every cumulative value, every difference, every "who is ahead / which is larger"
   statement and every crossing point against the table BEFORE you write the
   exemplar. Prompts must never state something the table contradicts.
3. Prompts ask questions; they must NOT contain the answers. Exemplars hold the answers.
4. Exemplars are finished model answers. No scratch work, no "[Re-calculation]",
   no "wait", no self-corrections.
5. Use only ideas, terms and methods taught in the lesson sequence above.
6. Tables use well-formed markdown rows ("| a | b |" with one separator row).
7. Use scalar/vector, distance/displacement, and similar paired terms exactly as the
   lessons did, and consistently within the document.
"""


def _fs_block(args) -> str:
    fs = getattr(args, 'fact_sheet', None)
    if not fs:
        return ""
    import lesson_consistency as lc
    return ("\nWhere lessons disagree, the FACT SHEET below is authoritative (it overrides "
            "rule 1's Lesson 1 / last-lesson default):\n" + lc.fact_sheet_block(fs))


def _fe_prompt(unit: dict, lessons: list, args, fe_template, lesson_template,
               feedback: list | None, prev_fe: dict | None = None) -> str:
    fe_template_section = ""
    if fe_template and fe_template.get('paragraphs'):
        fe_template_section = (
            "\nTEACHER TEMPLATE — FINAL EXPLANATION REFERENCE "
            "(use as structural and content guidance; improve quality where possible):\n"
            + "\n".join(fe_template['paragraphs'][:40]))
    fix = ""
    if feedback:
        fix = ("\nA REVIEWER FOUND THESE PROBLEMS IN YOUR PREVIOUS ATTEMPT. "
               "Fix every one:\n"
               + "\n".join(f"- [{i['where']}] {i['problem']}" for i in feedback) + "\n")
        if prev_fe:
            fix += ("\nYOUR PREVIOUS ATTEMPT (JSON). Return the SAME document with the minimum "
                    "edits needed to fix the problems above. Do not rewrite, reorder or re-number "
                    "anything that was not flagged; keep every other number, name and sentence "
                    "exactly as it is:\n" + json.dumps(prev_fe, ensure_ascii=False, indent=1) + "\n")
    return f"""AUDIENCE: This Final Explanation document is for STUDENTS to answer (the prompts) and for TEACHERS to mark against (the exemplars). Use clear, student-accessible language. Write in second person when appropriate.

Generate a Final Explanation assessment document for:
Subject: {_subject_display(args.subject)} Grade {args.grade}
Sub-strand: {args.substrand} {args.substrand_name}
Driving question: {unit.get('drivingQuestion', '')}

THE LESSON SEQUENCE AS ACTUALLY TAUGHT (the Final Explanation must agree with this):
{lesson_digest(lessons, unit)}
{_fs_block(args)}
{fe_template_section}{template_fe_context(lesson_template)}
{FE_RULES}{fix}
Fields: "instructions" are given to the students (they will write in a blank space under each prompt, so do not say the answers are printed). "sections": 4-5 sections, each with a "prompt" (student-facing, no answers) and an "exemplar" (the model answer). "rubric": 4-5 criteria.
"""


def verify_final_explanation(unit: dict, lessons: list, fe: dict, args) -> list | None:
    """Independent consistency review. Returns the list of issues ([] = clean),
    or None if the reviewer call itself failed."""
    prompt = f"""You are a meticulous reviewer of a Kenyan CBE Grade {args.grade} {_subject_display(args.subject)} assessment. Find ONLY real defects; do not comment on style.

THE LESSON SEQUENCE AS TAUGHT:
{lesson_digest(lessons, unit)}

THE FINAL EXPLANATION UNDER REVIEW (JSON):
{json.dumps(fe, ensure_ascii=False, indent=1)}

Check, working through the numbers yourself:
1. Every data table: recompute cumulative values, differences, averages and the claimed winner/leader/crossing point. Report any statement in a prompt or exemplar that the data contradicts, or any exemplar calculation that is wrong.
2. Two passages of the document that disagree with each other (different numbers for the same fact, different outcomes).
3. Disagreement with the lessons: different characters, places, datasets or key numbers for the same phenomenon, or a method/term the lessons never taught.
4. Prompts that contain their own answer.
5. Scratch work or self-correction text left in an exemplar ("[Re-calculation]", "wait", "actually").
6. A scientific or mathematical error, or a term used inconsistently (e.g. distance vs displacement).
7. CROSS-PART NUMBERS: list every numeric fact the document states about each named person, object or situation (a speed, a time, a mass, a distance, a rate) and compare them across ALL parts, prompts and exemplars. Flag any entity given two different values for the same moment or phase (e.g. 'about 19 km/h, nearly constant' in one part and 21 km/h in another) unless the text explains the change.
CLASSIFY every issue with "kind":
- "final_explanation": a defect that the Final Explanation's author can fix (cases 1, 2, 4, 5, 6 above, and a disagreement with LESSON 1 or the LAST lesson).
- "lesson_sequence": the LESSONS contradict EACH OTHER or contain an impossible/unrealistic figure, so no Final Explanation could agree with all of them. Report these once each, naming the lessons involved, but do NOT also report them against the Final Explanation.
Return {{"issues": []}} if you find none. Otherwise one entry per defect, "where" naming the section/part or lessons, "problem" stating exactly what is wrong and what the right value is."""
    r = call_claude(prompt, schema=VERIFY_TOOL_SCHEMA)
    if r is None:
        return None
    return r.get('issues', [])


def generate_final_explanation(curriculum_text: str, unit: dict,
                               lessons: list, args,
                               fe_template: dict | None = None,
                               lesson_template: dict | None = None,
                               max_rounds: int = 4,
                               log_name: str | None = None) -> dict | None:
    """Generate the Final Explanation FROM THE FINISHED LESSONS, then have a
    second call check it for contradictions; regenerate with the reviewer's
    findings until clean (up to max_rounds). If issues remain, the unresolved
    list is written to logs/final_explanation_issues/<name>.json, which the
    cross-document validator treats as a hard failure."""
    print("  Generating Final Explanation (from lesson content)...")
    feedback, best, best_issues, lesson_conflicts = None, None, None, []
    for rnd in range(1, max_rounds + 1):
        fe = call_claude(_fe_prompt(unit, lessons, args, fe_template, lesson_template, feedback,
                                     prev_fe=best if feedback else None),
                         schema=FE_TOOL_SCHEMA)
        if fe is None:
            print(f"    FE generation failed (round {rnd})")
            continue
        issues = verify_final_explanation(unit, lessons, fe, args)
        if issues is None:
            print(f"    FE review call failed (round {rnd}); treating as unverified")
            continue
        mine = [i for i in issues if i.get('kind') != 'lesson_sequence']
        lesson_conflicts = [i for i in issues if i.get('kind') == 'lesson_sequence'] or lesson_conflicts
        print(f"    FE review round {rnd}: {len(mine)} Final Explanation issue(s), "
              f"{len(issues) - len(mine)} lesson-sequence conflict(s)")
        if best is None or len(mine) < len(best_issues):
            best, best_issues = fe, mine          # keep the best attempt, not the last
        if not mine:
            break
        feedback = mine
    name = log_name or getattr(args, 'output', None) or f"{args.subject}_{args.substrand}"
    root = Path(__file__).resolve().parent.parent / 'logs'
    # Contradictions BETWEEN LESSONS are a different class of problem: they cannot
    # be fixed here and must not block the Final Explanation. Recorded for review.
    lc_path = root / 'lesson_conflicts' / f"{name}.json"
    if lesson_conflicts:
        lc_path.parent.mkdir(parents=True, exist_ok=True)
        lc_path.write_text(json.dumps({"name": name, "conflicts": lesson_conflicts},
                                      indent=2, ensure_ascii=False))
    elif lc_path.exists():
        lc_path.unlink()
    log_path = root / 'final_explanation_issues' / f"{name}.json"
    if best is not None and best_issues == []:
        if log_path.exists():
            log_path.unlink()
        return best
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps({"name": name, "status": "needs_review",
                                    "unresolved": best_issues,
                                    "verified": best_issues is not None},
                                   indent=2, ensure_ascii=False))
    print(f"    WARNING: best attempt has {len(best_issues or [])} unresolved finding(s): "
          f"written, but flagged for human review — see {log_path}")
    return best


def generate_summary_table(unit: dict, lessons: list, args,
                           st_template: dict | None = None) -> dict | None:
    """Summary Table, DERIVED from the lessons — no API call.

    It used to be a separate model call that was shown the lesson titles and
    free to rewrite them; in 73 of 85 sub-strands it did, so the teacher
    reference described a different lesson sequence from the one taught
    (partner validator, 2026-10-03). Each lesson already carries its own
    summaryTablePrompt {observed, learned, explained}; the table is those
    rows, with the lesson's own title. Drift is impossible by construction."""
    print("  Building Summary Table from lessons...")
    return derive_summary_table(unit, lessons, args.substrand, args.substrand_name)


def derive_summary_table(unit: dict, lessons: list, substrand_id: str, substrand_name: str) -> dict:
    dq = (unit or {}).get("drivingQuestion", "").split("\n")[0]
    return {
        "subStrand": f"Sub-Strand {substrand_id}: {substrand_name}",
        "drivingQuestion": dq,
        "lessons": [
            {
                "number": l["number"],
                "title": l["title"],
                "observed": (l.get("summaryTablePrompt") or {}).get("observed", ""),
                "learned": (l.get("summaryTablePrompt") or {}).get("learned", ""),
                "explained": (l.get("summaryTablePrompt") or {}).get("explained", ""),
            }
            for l in lessons
        ],
    }


# ── Data file writer ──────────────────────────────────────────────────────────

# Version of ares-contract.schema.json that generated files declare conformance to.
SCHEMA_VERSION = '1.0.0'


def write_data_file(output_name: str, meta: dict, unit: dict,
                    lessons: list, fe: dict | None, st: dict | None):
    """Write the assembled data file to generators/data/."""
    output_path = PROJECT_ROOT / 'generators' / 'data' / f'{output_name}_data.js'

    # ── Normalise to ares-contract canonical shape (defensive: covers model
    #    wobble and applies to both sync and batch-collect callers) ──────────
    if 'storyline' in unit and not unit.get('storylineThread'):
        unit['storylineThread'] = unit.pop('storyline')
    else:
        unit.pop('storyline', None)
    if not meta.get('substrand_id') or not meta.get('substrand_name'):
        _sm = re.match(r'\s*Sub-Strand\s+([\d.]+):\s*(.+)', unit.get('substrand', ''))
        if _sm:
            meta.setdefault('substrand_id', _sm.group(1))
            meta.setdefault('substrand_name', _sm.group(2).strip())
    def _coerce_int(v):
        """Contract types lesson 'number' as integer; coerce stringified ints."""
        if isinstance(v, bool):
            return v
        if isinstance(v, str) and v.strip().lstrip('-').isdigit():
            return int(v.strip())
        return v
    for _lesson in lessons:
        if isinstance(_lesson, dict) and 'safetyNotes' in _lesson:
            _sn = _lesson.pop('safetyNotes')
            _slo = _lesson.get('slo')
            if isinstance(_slo, dict) and not _slo.get('safetyNotes'):
                _slo['safetyNotes'] = _sn
        if isinstance(_lesson, dict) and 'number' in _lesson:
            _lesson['number'] = _coerce_int(_lesson['number'])
    if isinstance(st, dict) and isinstance(st.get('lessons'), list):
        for _stl in st['lessons']:
            if isinstance(_stl, dict) and 'number' in _stl:
                _stl['number'] = _coerce_int(_stl['number'])

    def js_val(obj):
        """Convert Python object to JS-compatible string."""
        return json.dumps(obj, indent=2, ensure_ascii=False)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"'use strict';\n")
        f.write(f"/**\n")
        f.write(f" * {output_name}_data.js\n")
        f.write(f" * Generated by generate_substrand.py\n")
        f.write(f" * Run: node generators/generate.js {output_name}\n")
        f.write(f" */\n\n")

        # META
        f.write(f"const META = {js_val(meta)};\n\n")

        # UNIT
        f.write(f"const UNIT = {js_val(unit)};\n\n")

        # LESSONS
        f.write(f"const LESSONS = {js_val(lessons)};\n\n")

        # FINAL_EXPLANATION
        if fe:
            f.write(f"const FINAL_EXPLANATION = {js_val(fe)};\n\n")
        else:
            f.write(f"const FINAL_EXPLANATION = null;\n\n")

        # SUMMARY_TABLE
        if st:
            f.write(f"const SUMMARY_TABLE = {js_val(st)};\n\n")
        else:
            f.write(f"const SUMMARY_TABLE = null;\n\n")

        f.write(f"const schemaVersion = '{SCHEMA_VERSION}';\n\n")
        f.write(f"module.exports = {{ schemaVersion, META, UNIT, LESSONS, FINAL_EXPLANATION, SUMMARY_TABLE }};\n")

    print(f"  Written: {output_path}")
    return output_path


# ── Subject/substrand lookup ──────────────────────────────────────────────────

# Nested by grade FIRST, subject second. This is the fix for the highest-
# severity finding in this handoff: Grade 11 reuses Grade 10's strand/
# sub-strand numbering (confirmed against the KICD sources — e.g. Biology
# '2.1' is "Plant Nutrition" at Grade 10 but "Reproduction in Plants" at
# Grade 11). Before this change, SUBSTRAND_NAMES was flat (subject -> id),
# so a Grade 11 lookup for biology '2.1' would have silently returned
# "Plant Nutrition" — the right-shaped, wrong-grade answer — and that name
# would have gone straight into the content-generation prompt. Do not
# flatten this back.
SUBSTRAND_NAMES = {
    10: {
        'biology': {
            '1.1': 'Cell Structure',
            '1.2': 'Chemicals of Life',
            '1.3': 'Cell Biology',
            '2.1': 'Plant Nutrition',
            '2.2': 'Plant Transport',
            '2.3': 'Plant Gaseous Exchange and Respiration',
            '3.1': 'Animal Nutrition',
            '3.2': 'Animal Transport',
            '3.3': 'Animal Gaseous Exchange and Respiration',
        },
        'chemistry': {
            '1.1': 'Introduction to Chemistry',
            '1.2': 'The Atom',
            '1.3': 'The Periodic Table',
            '1.4': 'Chemical Bonding',
            '1.5': 'Periodicity',
            '2.1': 'Introduction to Salts',
            '3.1': 'Acids and Bases',
        },
        'physics': {
            '1.1': 'Pressure',
            '1.2': 'Mechanical Properties of Materials',
            '1.3': 'Temperature and Thermal Expansion',
            '1.4': 'Energy, Work, Power and Machines',
            '1.5': 'Moments of Equilibrium',
            '2.1': 'Properties of Waves',
            '3.1': 'Radioactivity and Stability of Isotopes',
            '3.2': 'Current Electricity',
            '3.3': 'Introduction to Electronics',
            '3.4': 'Electrostatics',
            '4.1': 'Greenhouse Effect and Climate Change',
            '4.2': 'Introduction to Space Physics',
        },
        'mathematics': {
            '1.1': 'Real Numbers',
            '1.2': 'Indices',
            '1.3': 'Quadratic Equations',
            '1.4': 'Congruence',
            '2.1': 'Similarity and Enlargement',
            '2.2': 'Area of Polygons',
            '2.3': 'Area of Part of a Circle',
            '2.4': 'Surface Area and Volume of Solids',
            '3.1': 'Trigonometry I',
            '3.2': 'Rotation',
            '3.3': 'Vectors I',
            '3.4': 'Linear Motion',
            '4.1': 'Statistics I',
            '4.2': 'Probability I',
        },
        'general_science': {
            '1.1': 'Introduction to General Science',
            '1.2': 'The Cell',
            '1.3': 'Nutrition in Animals',
            '1.4': 'Transport in Plants',
            '1.5': 'Respiration',
            '1.6': 'Plant Growth and Development',
            '1.7': 'Microorganisms',
            '2.1': 'The Periodic Table',
            '2.2': 'Chemical Families',
            '2.3': 'Chemical Bonding',
            '2.4': 'Acids, Bases and Salts',
            '2.5': 'Rates of Reactions',
            '3.1': 'Turning Effect of Force',
            '3.2': 'Linear Motion',
            '3.3': 'Waves',
            '3.4': 'Magnetism and Electromagnetic Induction',
        },
        'core_mathematics': {
            '1.1': 'Real Numbers',
            '1.2': 'Indices and Logarithms',
            '1.3': 'Quadratic Expressions and Equations',
            '2.1': 'Similarity and Enlargement',
            '2.2': 'Reflection and Congruence',
            '2.3': 'Rotation',
            '2.4': 'Trigonometry 1',
            '2.5': 'Area of Polygons',
            '2.6': 'Area of a Part of a Circle',
            '2.7': 'Surface Area and Volume of Solids',
            '2.8': 'Vectors',
            '2.9': 'Linear Motion',
            '3.1': 'Statistics I',
            '3.2': 'Probability I',
        },
        'essential_mathematics': {
            '1.1': 'Real Numbers',
            '1.2': 'Indices',
            '1.3': 'Quadratic Equations',
            '2.1': 'Similarity and Enlargement',
            '2.2': 'Reflection',
            '2.3': 'Trigonometry',
            '2.4': 'Area of Polygons',
            '2.5': 'Area of Part of a Circle',
            '2.6': 'Surface Area of Solids',
            '2.7': 'Volume and Capacity',
            '2.8': 'Commercial Arithmetic 1',
            '3.1': 'Statistics 1',
            '3.2': 'Probability I',
        },
    },
    11: {
        # Biology: COMPLETE and hand-verified 2026-09-19 against the rendered
        # "SUMMARY STRANDS AND SUB STRANDS" table on page ix of
        # 'Biology Grade 11 - October 2025.pdf', read as an image at 200 dpi —
        # NOT from OCR text (§6.5 of HANDOFF_new_stem_subjects_2026-07-28.md:
        # OCR flattens these tables and is not authoritative for names).
        # The document was also checked to its end: it closes after 3.3 and the
        # appendix, so there is no strand beyond 3.0 to miss.
        #
        # Every one of these differs from the Grade 10 sub-strand at the same
        # number, which is exactly why this dict is keyed by grade. Grade 11
        # also has 10 sub-strands to Grade 10's 9 — strand 1.0 gained a fourth.
        'biology': {
            '1.1': 'Taxonomy I',
            '1.2': 'Ecology',
            '1.3': 'Taxonomy II',
            '1.4': 'Cell Division',
            '2.1': 'Reproduction in Plants',
            '2.2': 'Growth and Development in Plants',
            '2.3': 'Excretion in Plants',
            '3.1': 'Reproduction in Animals',
            '3.2': 'Growth and Development in Animals',
            '3.3': 'Excretion and Homeostasis in Animals',
        },
        # Chemistry, Physics, Core Mathematics: hand-verified 2026-10-01 the
        # same way, against each PDF's rendered "SUMMARY OF STRANDS AND SUB
        # STRANDS" table (embedded image, viewed directly). Names follow the
        # table; capitalisation normalised to Title Case.
        'chemistry': {
            '1.1': 'The Mole',
            '1.2': 'Non-metals',
            '2.1': 'Salts',
            '2.2': 'Gas Laws',
            '2.3': 'Reaction Rates',
            '3.1': 'Hydrocarbons',
        },
        'physics': {
            '1.1': 'Fluid Flow',
            '1.2': 'Linear Motion',
            '1.3': 'Projectile Motion',
            '1.4': 'Dimensional Analysis',
            '1.5': 'Heat Transmission',
            '2.1': 'Refraction of Light',
            '2.2': 'Electromagnetic Waves',
            '2.3': 'Thermionic Emission and its Applications',
            '3.1': 'Capacitors',
            '3.2': 'Magnetic Effect of Electric Current',
            '3.3': 'Diodes',
            '4.1': 'Physics of Wind Formation',
            '4.2': 'Introduction to Rockets',
        },
        # Strand 4.0 Calculus is new at Grade 11 (no Grade 10 equivalent).
        'core_mathematics': {
            '1.1': 'Quadratic Expressions and Equations',
            '1.2': 'Irrational Numbers',
            '1.3': 'Linear Inequalities',
            '1.4': 'Logarithms II',
            '1.5': 'Formulae and Variations',
            '1.6': 'Sequences and Series',
            '1.7': 'Matrices I',
            '2.1': 'Approximation and Errors',
            '2.2': 'Angle Properties of a Circle',
            '2.3': 'Commercial Arithmetic',
            '2.4': 'Circles, Chords and Tangents',
            '2.5': 'Trigonometry II',
            '2.6': 'Graphical Methods',
            '3.1': 'Permutations and Combinations',
            '3.2': 'Probability II',
            '4.1': 'Functions',
            '4.2': 'Differentiation I',
        },
        # NOT ADDED: general_science and essential_mathematics. Their Grade 11
        # source PDFs (October 2025) are broken screen captures that repeat the
        # front-matter "National Goals of Education" pages and never reach the
        # curriculum tables (checked 2026-10-01 by viewing the images). A
        # replacement source is needed before either can be added.
    },
}

# Native-text (pdfminer-extractable) curriculum PDFs, nested by grade so a
# Grade 11+ entry is added alongside — never in place of — a Grade 10 one.
# NOTE: as of this handoff, every Grade 11 STEM source in
# CBE_Curriculums/Grade 11/STEM/ is a screenshot with NO text layer (verified
# via pdffonts). None belong in this map yet — they go in CURRICULUM_TEXT_MAP
# below, after OCR extraction (Phase 4 of the handoff doc).
CURRICULUM_PDF_MAP = {
    10: {
        'biology':     'data/raw/curriculum_pdfs/Grade10_Biology_CBE_Curriculum.pdf',
        'chemistry':   'data/raw/curriculum_pdfs/Grade10_Chemistry_CBE_Curriculum.pdf',
        'physics':     'data/raw/curriculum_pdfs/Grade10_Physics_CBE_Curriculum.pdf',
        'mathematics': 'data/raw/curriculum_pdfs/Grade10_Mathematics_Curriculum.pdf',
    },
    11: {
        # TODO Phase 4: populate once a native-text (or OCR'd) Grade 11 source
        # is confirmed for each subject. See HANDOFF_grade_aware_pipeline.md.
    },
}

# Subjects whose source PDFs have no text layer (OCR image-only scans) use a
# pre-extracted, deduped plain-text file instead of extract_curriculum_pdf().
# See HANDOFF_new_stem_subjects_2026-07-28.md §6.
# Pre-extracted, deduped plain text for subjects whose source PDFs have no
# text layer (OCR image-only scans) — see HANDOFF_new_stem_subjects_2026-07-28.md
# §6 for the extraction method. Nested by grade for the same reason as
# CURRICULUM_PDF_MAP above.
CURRICULUM_TEXT_MAP = {
    10: {
        'general_science':       'data/raw/curriculum_text/general_science.txt',
        'core_mathematics':      'data/raw/curriculum_text/core_mathematics.txt',
        'essential_mathematics': 'data/raw/curriculum_text/essential_mathematics.txt',
    },
    11: {
        # OCR-extracted 2026-09-19 with scripts/extract_curriculum_ocr.py
        # (17 slices @ 200 dpi, tesseract --psm 4). All 10 sub-strands verified
        # findable by both name and number; no dedup was needed.
        'biology': 'data/raw/curriculum_text/grade11_biology.txt',
        # OCR'd 2026-10-01 (same script and settings); 0 duplicate blocks removed.
        'chemistry':        'data/raw/curriculum_text/grade11_chemistry.txt',
        'physics':          'data/raw/curriculum_text/grade11_physics.txt',
        'core_mathematics': 'data/raw/curriculum_text/grade11_core_mathematics.txt',
        # general_science / essential_mathematics: OCR output exists but the
        # source PDFs contain no curriculum (see SUBSTRAND_NAMES[11]); not mapped.
    },
}

# Nested by grade for the same reason as SUBSTRAND_NAMES above: Grade 11
# Biology '2.1' (Reproduction in Plants) has no established lesson count of
# its own and must not silently inherit Grade 10 '2.1's count of 12.
LESSON_COUNTS = {
    10: {
        'biology': {'1.1': 6, '1.2': 14, '1.3': 20, '1.4': 24,
                    '2.1': 12, '2.2': 22, '2.3': 22,
                    '3.1': 12, '3.2': 24, '3.3': 24},
    },
    11: {
        # TODO Phase 4: populate once Grade 11 lesson counts are confirmed
        # (KICD's own suggested counts are guidelines, not requirements —
        # see WORKFLOW.md; a uniform --lessons N is an acceptable default
        # the way it already is for chemistry/physics/mathematics at Grade 10).
    },
}


# ── v2 template lookup ────────────────────────────────────────────────────────

V2_TEMPLATE_DIR = PROJECT_ROOT / 'data' / 'raw' / 'CBE LESSON TEMPLATES' / 'v2_owner_inventory'

_SUBJECT_FOLDER = {
    'biology': 'Biology', 'chemistry': 'Chemistry',
    'physics': 'Physics', 'mathematics': 'Maths',
    'general_science': 'General_Science',
    'core_mathematics': 'Core_Mathematics',
    'essential_mathematics': 'Essential_Mathematics',
}

# Human-readable subject label for docx headers/labels. Multi-word subjects need
# an explicit entry — args.subject.capitalize() mangles 'general_science' into
# 'General_science' (only the first character is capitalized, underscore kept).
_SUBJECT_DISPLAY = {
    'general_science': 'General Science',
    'core_mathematics': 'Core Mathematics',
    'essential_mathematics': 'Essential Mathematics',
}


def _subject_display(subject: str) -> str:
    return _SUBJECT_DISPLAY.get(subject, subject.capitalize())


def _v2_output_dir(grade: int, subject: str, substrand_id: str, substrand_name: str) -> str:
    """Return the outputDir path segment for v2 output, e.g.
    'v2/Grade11/Biology/SS2.1_Reproduction_in_Plants'.

    GRADE 10 IS DELIBERATELY FLAT: 'v2/<Subject>/...', with no Grade10 segment.

    Why: all 85 Grade 10 sub-strands were generated before the grade segment
    existed, and their data modules hardcode the flat outputDir. Migrating that
    tree was considered and explicitly deferred on 2026-09-19 (Mark's call) —
    the files are stable, and moving them churns teacher-visible Google Drive
    paths for no present benefit. Revisit at the next full-corpus regeneration
    (the pending Kenyan-terminology pass is the likely trigger), so the Drive
    re-sync is paid once rather than twice. See STATUS.md Active Threads.

    This is the ONE place that exception lives. Keep it here: path *construction*
    is the single chokepoint, so consumers that walk the tree only ever have to
    cope with two shapes, never invent a third.
    """
    subj_folder = _SUBJECT_FOLDER.get(subject, subject.capitalize())
    ss_folder = f"SS{substrand_id}_{substrand_name.replace(' ', '_')}"
    if grade == 10:
        return f"v2/{subj_folder}/{ss_folder}"
    # Grade 11+: lesson plans and quizzes in two parallel trees (Mark,
    # 2026-10-01), so each is easy to find and review on its own:
    #   v2/Grade11/Biology/Lesson_Plans/SS2.1_.../   (docx + _data.json + _quiz.json)
    #   v2/Grade11/Biology/Quizzes/SS2.1_.../        (build_quiz.js output)
    # Consumers that walk the tree: generate_teacher_index.js (reads
    # Lesson_Plans/), build_quiz.js (maps Lesson_Plans -> Quizzes).
    return f"v2/Grade{grade}/{subj_folder}/Lesson_Plans/{ss_folder}"


def find_v2_templates(grade: int, subject: str, substrand_id: str) -> dict:
    """Find up to three template docx files for this sub-strand from v2_owner_inventory.
    Returns {'lesson': Path|None, 'fe': Path|None, 'st': Path|None}.

    Grade-segmented the same way as _v2_output_dir(): Grade 10 templates stay
    flat at v2_owner_inventory/<Subject>/SS…, every other grade lives under
    v2_owner_inventory/Grade<N>/<Subject>/SS….

    This MUST be keyed by grade. Grades reuse the same strand/sub-strand
    numbering with different topics, so a flat lookup of 'biology' + '2.1'
    would hand a Grade 11 run Grade 10's SS2.1_Plant_Nutrition template while
    generating Reproduction in Plants — the same silent wrong-content failure
    that SUBSTRAND_NAMES had. Missing templates are safe (generation falls
    back to curriculum text); a wrong-grade template is not.
    """
    subject_folder = _SUBJECT_FOLDER.get(subject, subject.capitalize())
    if grade == 10:
        subject_dir = V2_TEMPLATE_DIR / subject_folder
    else:
        subject_dir = V2_TEMPLATE_DIR / f'Grade{grade}' / subject_folder
    matches = list(subject_dir.glob(f'SS{substrand_id}_*'))
    if not matches:
        return {'lesson': None, 'fe': None, 'st': None}

    found = {'lesson': None, 'fe': None, 'st': None}
    for f in matches[0].glob('*.docx'):
        fname = f.name.lower().replace('_', '').replace('-', '').replace(' ', '')
        if 'resourceguide' in fname:
            continue
        if 'finalexplanation' in fname:
            found['fe'] = f
        elif 'summarytable' in fname or 'answerkey' in fname:
            found['st'] = f
        else:
            found['lesson'] = f
    return found


def determine_lesson_count(curriculum_text: str, lesson_template: dict,
                            substrand_id: str, subject: str, grade: int) -> tuple:
    """Return (count, source); source is 'template_form'|'template_regex'|'pre_pass'|'default'.
    Clamps result to [6, 14].
    """
    # 0. Planning-form templates state it explicitly ("Number of lessons").
    #    Checked first because the form's printed instructions say "Most
    #    sub-strands run 5 to 8 lessons", which the regex below would read as 8.
    #    The teacher's figure wins even outside 6-14 (it follows KICD time
    #    allocation), with a warning.
    form_count = (lesson_template or {}).get('form', {}).get('lesson_count')
    if form_count:
        if not 6 <= form_count <= 14:
            print(f"  NOTE: template asks for {form_count} lessons, outside the usual 6-14; using it.")
        return (form_count, 'template_form')

    # 1. Regex on template paragraph text
    if lesson_template:
        all_text = ' '.join(lesson_template.get('paragraphs', []))
        m = (re.search(r'\b(1[0-4]|[6-9])\s+lessons?\b', all_text, re.IGNORECASE) or
             re.search(r'\b(1[0-4]|[6-9])\s+periods?\b', all_text, re.IGNORECASE))
        if m:
            return (int(m.group(1)), 'template_regex')

    # 2. Pre-pass API call — small, cached in batch checkpoint
    COUNT_SCHEMA = {
        'type': 'object', 'additionalProperties': False,
        'properties': {
            'lesson_count': {'type': 'integer'},   # 6-14, clamped below (structured outputs rejects minimum/maximum)
        },
        'required': ['lesson_count'],
    }
    excerpt = curriculum_text[:2000] if curriculum_text else ''
    template_excerpt = ' '.join(lesson_template.get('paragraphs', [])[:10]) if lesson_template else ''
    prompt = (
        f"How many lessons (6–14) should Sub-Strand {substrand_id} of Grade {grade} "
        f"{subject.capitalize()} have?\n\n"
        f"CURRICULUM EXCERPT:\n{excerpt}\n\n"
        f"TEMPLATE EXCERPT:\n{template_excerpt}\n\n"
        f"Consider topic complexity, number of learning outcomes, and any KICD guidance. "
        f"Target range 6–14, average 8–10."
    )
    result = call_claude(prompt, max_tokens=4000, retries=2, schema=COUNT_SCHEMA)
    if result and isinstance(result.get('lesson_count'), int):
        return (max(6, min(14, result['lesson_count'])), 'pre_pass')

    return (8, 'default')


# ── Main ──────────────────────────────────────────────────────────────────────

def _checkpoint_path(output_name: str) -> Path:
    return PROJECT_ROOT / 'generators' / 'data' / f'.{output_name}_checkpoint.json'

def _save_checkpoint(output_name: str, lessons: list):
    path = _checkpoint_path(output_name)
    with open(path, 'w') as f:
        json.dump(lessons, f, ensure_ascii=False)

def _load_checkpoint(output_name: str) -> list | None:
    path = _checkpoint_path(output_name)
    if path.exists():
        try:
            with open(path) as f:
                data = json.load(f)
            print(f"  Found checkpoint with {len(data)} lesson(s)")
            return data
        except Exception:
            return None
    return None



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
              end='\r', flush=True)
        if batch.processing_status == 'ended':
            print()  # newline after \r
            return batch
        time.sleep(poll_interval)


def collect_batch_results(batch_id: str) -> dict:
    """Retrieve all results from a completed batch.
    Returns dict mapping custom_id → parsed dict (or None on error).
    Handles structured-output JSON (current), tool_use (batches submitted
    before 2026-09-30) and free-text JSON responses.
    """
    results = {}
    for result in CLIENT.beta.messages.batches.results(batch_id):
        cid = result.custom_id
        if result.result.type != 'succeeded':
            print(f"  WARNING: {cid} failed: {result.result.type}")
            results[cid] = None
            continue

        _track_batch_usage(result.result.message)
        content = result.result.message.content

        # Legacy tool_use block (batches submitted with forced tool_choice)
        tool_data = None
        for block in content:
            if getattr(block, 'type', None) == 'tool_use':
                tool_data = block.input
                break
        # Structured outputs: the text block is schema-constrained JSON
        if tool_data is None and result.result.message.stop_reason == 'end_turn':
            try:
                tool_data = json.loads(_text_of(content))
            except json.JSONDecodeError:
                tool_data = None

        if tool_data is not None:
            schema = LESSON_TOOL_SCHEMA if cid.startswith('lesson_') else FE_TOOL_SCHEMA
            violations = _schema_violations(tool_data, schema)
            if violations:
                print(f"  WARNING: Schema violations for {cid}: {violations[:3]}")
                results[cid] = None
            else:
                results[cid] = tool_data
        else:
            # Fallback: free-text JSON (legacy batches submitted without tool_use)
            raw = _text_of(content).strip()
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)
            raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw)
            try:
                results[cid] = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"  WARNING: JSON parse failed for {cid}: {e}")
                results[cid] = None
    return results


def build_batch_requests(curriculum_text: str, lesson_template: dict,
                          unit: dict, args,
                          fe_template: dict | None = None) -> list:
    """Build all lesson requests for batch submission (the Final Explanation is
    generated afterwards, from the collected lessons — see run_collect).
    Note: prev_summaries context is omitted in batch mode since all
    requests are submitted simultaneously. The unit storyline thread
    provides sufficient continuity.
    """
    requests = []

    for lesson_num in range(1, args.lessons + 1):
        lesson_pos = "opening lesson that launches the phenomenon" if lesson_num == 1 else \
                     "final lesson with Final Explanation" if lesson_num == args.lessons else \
                     f"lesson {lesson_num} of {args.lessons} in the evidence-gathering sequence"

        prompt = (
            f"Generate Lesson {lesson_num} ({lesson_pos}) for:\n"
            f"Subject: {_subject_display(args.subject)} Grade {args.grade}\n"
            f"Sub-strand: {args.substrand} {args.substrand_name}\n"
            f"Driving question: {unit.get('drivingQuestion', '')}\n"
            f"Phenomenon: {unit.get('phenomenon', '')}\n"
            f"Storyline thread for this lesson: {_get_lesson_storyline(unit, lesson_num)}\n\n"
            f"KICD CURRICULUM CONTENT:\n{curriculum_text}\n\n"
            f"{template_lesson_context(lesson_template, lesson_num)}\n\n"
            f"{_lesson_fs(getattr(args, 'fact_sheet', None), lesson_num)}\n"
            f"RULES:\n"
            f"- All learner experiences must connect back to the phenomenon\n"
            f"- Teacher moves must include specific quoted phrases, WAIT TIME (10-15 seconds), cold-call counts\n"
            f"- Sensemaking strategies: name the strategy and explain how it builds understanding\n"
            f"- Formative assessment: specific, observable indicators\n"
            f"- Kenya-relevant contexts throughout\n"
            f"- Lesson {lesson_num} should "
            f"{'introduce the phenomenon and open the DQB' if lesson_num == 1 else 'build on previous evidence and advance the driving question'}\n"
            f"{'- Final lesson: focus on Final Explanation, model comparison L1 vs final, DQB completion' if lesson_num == args.lessons else ''}\n\n"
            f"Return the lesson as JSON matching the provided schema. Set number to {lesson_num}. "
            f"Set substrand to 'Sub-Strand {args.substrand}: {args.substrand_name}'."
        )

        requests.append({
            "custom_id": f"lesson_{lesson_num}",
            "params": {
                "model": MODEL,
                "max_tokens": 16000,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}],
                **_structured_params(LESSON_TOOL_SCHEMA),
            },
        })

    # No Final Explanation request here: it is generated AFTER the lessons are
    # collected (run_collect), from their actual content. Requested alongside
    # them it could only see the driving question, so it invented its own
    # dataset and contradicted the lessons (Core Mathematics 2.9, 2026-10-03).

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

    # Lessons must agree with each other before the Final Explanation is written.
    class _CArgs:
        pass
    c_args = _CArgs()
    c_args.subject, c_args.grade = meta.get('subject', 'Biology').lower(), meta['grade']
    c_args.substrand, c_args.substrand_name = meta.get('substrand_id', ''), meta.get('substrand_name', '')
    fact_sheet = batch_meta.get('fact_sheet')
    consistency_pass(unit, lessons, c_args, fact_sheet, output_name)

    # Final Explanation: generated now, from the collected lessons (not in the
    # batch), then reviewed for contradictions.
    class _FeArgs:
        pass
    fe_args = _FeArgs()
    fe_args.grade          = meta['grade']
    fe_args.subject        = meta.get('subject', 'Biology').lower()
    fe_args.substrand      = meta.get('substrand_id', '')
    fe_args.substrand_name = meta.get('substrand_name', '')
    fe_args.lessons        = n_lessons
    fe_args.output         = output_name
    fe_args.fact_sheet     = fact_sheet
    _v2 = find_v2_templates(fe_args.grade, fe_args.subject, fe_args.substrand)
    _fe_path = _v2.get('fe')
    fe_template = extract_template_docx(str(_fe_path)) if _fe_path else None
    _lt_path = _v2.get('lesson')
    lesson_template = extract_template_docx(str(_lt_path)) if _lt_path else {}
    fe = generate_final_explanation('', unit, lessons, fe_args, fe_template=fe_template,
                                    lesson_template=lesson_template, log_name=output_name)
    if not fe:
        print("  WARNING: Final Explanation missing or failed")

    # Generate Summary Table synchronously (needs real lesson data)
    print("  Generating Summary Table (synchronous — needs lesson data)...")

    # Build args-like namespace for generate_summary_table
    class _Args:
        pass
    st_args = _Args()
    # From META, not a default: this path runs on collect, long after the
    # original --grade was parsed, and a wrong grade here silently selects
    # another grade's template.
    st_args.grade       = meta['grade']
    st_args.subject     = meta.get('subject', 'Biology').lower()
    st_args.substrand   = meta.get('substrand_id', '')
    st_args.substrand_name = meta.get('substrand_name', '')
    st_args.lessons     = n_lessons

    # Re-load ST template (needed for audience-aware generation)
    _st_path = find_v2_templates(st_args.grade, st_args.subject, st_args.substrand).get('st')
    st_template = extract_template_docx(str(_st_path)) if _st_path else None

    st = generate_summary_table(unit, lessons, st_args, st_template=st_template)
    if st:
        print("  Summary Table generated ✓")

    # Write data file
    print("\n  Writing data file...")
    output_path = write_data_file(output_name, meta, unit, lessons, fe, st)

    # Optionally run generator
    if hasattr(args, 'run') and args.run:
        print("\n  Running generator...")
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

    log_run_cost(output_name, 'collect')
    print(f"\n✓ Done! Data file: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate CBE sub-strand content via Claude API')
    parser.add_argument('--subject',   required=False, default=None,
                        choices=['biology', 'chemistry', 'physics', 'mathematics',
                                 'general_science', 'core_mathematics', 'essential_mathematics'])
    parser.add_argument('--grade',     type=int, default=None,
                        help='Target grade level, e.g. 10, 11, 12. Required for all modes '
                             'except --collect (the grade was already fixed at submit time). '
                             'No default on purpose: a silent default is how this pipeline '
                             'ended up hardcoded to Grade 10 everywhere in the first place.')
    parser.add_argument('--substrand', required=False, default=None,
                        help='Sub-strand number e.g. 1.4')
    parser.add_argument('--output',    required=False, default=None,
                        help='Output name e.g. bio_1_4')
    parser.add_argument('--lessons',   type=int, default=None,
                        help='Number of lessons (default: from KICD curriculum)')
    parser.add_argument('--template',  default=None,
                        help='Path to teacher template docx (auto-detected if omitted)')
    parser.add_argument('--batch',     action='store_true',
                        help='Submit all content as a Message Batches API job (50%% cheaper)')
    parser.add_argument('--collect',   default=None, metavar='NAME',
                        help='Collect results from a previously submitted batch')
    parser.add_argument('--wait',      action='store_true',
                        help='With --collect: poll until batch is complete')
    parser.add_argument('--resume',    action='store_true',
                        help='Resume from checkpoint if interrupted')
    parser.add_argument('--run',       action='store_true',
                        help='Run node generators/generate.js after creating data file')
    parser.add_argument('--unit-only', action='store_true',
                        help='Generate UNIT only (for testing)')
    args = parser.parse_args()

    # Validate required args when not in collect mode
    if not args.collect:
        missing = [f for f, v in [('--subject', args.subject),
                                   ('--substrand', args.substrand),
                                   ('--output', args.output),
                                   ('--grade', args.grade)] if v is None]
        if missing:
            parser.error(f"the following arguments are required: {', '.join(missing)}")

    # ── Batch collect mode ────────────────────────────────────────────────────
    if args.collect:
        run_collect(args.collect, args)
        return

    # Grade is known and validated past this point (required unless --collect).
    # Rebuild SYSTEM_PROMPT for the actual target grade before any API call.
    global SYSTEM_PROMPT
    SYSTEM_PROMPT = build_system_prompt(args.grade)

    # Resolve substrand name — keyed by GRADE first, then subject. Getting
    # this order wrong is exactly how a Grade 11 run could silently generate
    # content titled after a Grade 10 sub-strand of the same number; see the
    # comment on SUBSTRAND_NAMES's definition.
    args.substrand_name = SUBSTRAND_NAMES.get(args.grade, {}).get(args.subject, {}).get(
        args.substrand, f'Sub-Strand {args.substrand}'
    )
    if args.substrand not in SUBSTRAND_NAMES.get(args.grade, {}).get(args.subject, {}):
        print(f"  WARNING: no registered name for grade {args.grade} {args.subject} "
              f"'{args.substrand}' — using generic placeholder '{args.substrand_name}'. "
              f"Add a real entry to SUBSTRAND_NAMES[{args.grade}]['{args.subject}'] first "
              f"unless a generic name is genuinely intended.")

    # ── Extract source content + templates ───────────────────────────────────

    print("\n1. Extracting source content...")
    if args.subject in CURRICULUM_TEXT_MAP.get(args.grade, {}):
        curriculum_text = (PROJECT_ROOT / CURRICULUM_TEXT_MAP[args.grade][args.subject]).read_text(
            encoding='utf-8', errors='replace')
        # Grade 11+: send only this sub-strand's section (the whole Grade 11
        # Biology file is 53k chars across 10 sub-strands, which invites SLOs
        # from the wrong one). Grade 10's text-source subjects were generated
        # from the full text and are left that way.
        if args.grade != 10:
            _section = slice_curriculum_text(curriculum_text, args.substrand)
            if _section:
                curriculum_text = _section
            else:
                print(f"  WARNING: sub-strand {args.substrand} section not found in curriculum "
                      f"text; sending the full text")
    else:
        _pdf_rel = CURRICULUM_PDF_MAP.get(args.grade, {}).get(args.subject)
        if not _pdf_rel:
            # Without this, an unregistered grade/subject falls through as an
            # empty path, resolves to PROJECT_ROOT, and fails inside the PDF
            # extractor with an error that looks like a broken parser rather
            # than missing configuration. Fail here, saying what to add.
            sys.exit(
                f"ERROR: no curriculum source registered for grade {args.grade} "
                f"'{args.subject}'.\n"
                f"  Add an entry to CURRICULUM_TEXT_MAP[{args.grade}]['{args.subject}'] "
                f"(OCR-extracted text, preferred) or "
                f"CURRICULUM_PDF_MAP[{args.grade}]['{args.subject}'] (native-text PDF).\n"
                f"  Screenshot PDFs with no text layer must be OCR-extracted first — "
                f"registering one under CURRICULUM_PDF_MAP yields empty text, not an error."
            )
        curriculum_pdf  = str(PROJECT_ROOT / _pdf_rel)
        curriculum_text = extract_curriculum_pdf(curriculum_pdf, args.substrand)
    print(f"  Curriculum text: {len(curriculum_text)} chars")

    # Find v2 templates (lesson + FE + ST); --template CLI arg overrides lesson only
    _v2 = find_v2_templates(args.grade, args.subject, args.substrand)
    lesson_template_path = Path(args.template) if args.template else _v2['lesson']
    fe_template_path     = _v2['fe']
    st_template_path     = _v2['st']

    lesson_template = extract_template_docx(str(lesson_template_path)) if lesson_template_path else {}
    fe_template     = extract_template_docx(str(fe_template_path)) if fe_template_path else None
    st_template     = extract_template_docx(str(st_template_path)) if st_template_path else None

    if lesson_template_path:
        print(f"  Lesson template: {lesson_template_path.name} "
              f"({len(lesson_template.get('paragraphs', []))} paragraphs)")
    if fe_template_path:
        print(f"  FE template:     {fe_template_path.name}")
    if st_template_path:
        print(f"  ST template:     {st_template_path.name}")

    # Resolve lesson count (CLI --lessons wins; otherwise probe template/curriculum)
    lesson_count_source = 'cli'
    if args.lessons is None:
        args.lessons, lesson_count_source = determine_lesson_count(
            curriculum_text, lesson_template, args.substrand, args.subject, args.grade)
        print(f"  Lesson count: {args.lessons} (source: {lesson_count_source})")

    print(f"\nGenerating: {_subject_display(args.subject)} Grade {args.grade} Sub-Strand {args.substrand}: {args.substrand_name}")
    print(f"  Lessons: {args.lessons}")
    print(f"  Output:  generators/data/{args.output}_data.js")
    print(f"  Model:   {MODEL}")

    # ── Generate content via Claude API ──────────────────────────────────────

    print("\n2. Generating content via Claude API...")

    # UNIT
    unit = generate_unit(curriculum_text, lesson_template, args)
    if not unit:
        print("ERROR: Failed to generate UNIT data")
        sys.exit(1)
    print(f"  UNIT generated ✓")

    if args.unit_only:
        print("\n[unit-only mode — stopping here]")
        print(json.dumps(unit, indent=2))
        log_run_cost(args.output, 'unit-only')
        return

    # Shared facts + lesson map, before any lesson (both modes).
    args.fact_sheet = make_fact_sheet(curriculum_text, unit, lesson_template, args)

    # ── Batch submit mode ─────────────────────────────────────────────────────
    if args.batch:
        print("\n2b. Building batch requests...")
        requests = build_batch_requests(curriculum_text, lesson_template, unit, args,
                                         fe_template=fe_template)
        print(f"  Built {len(requests)} requests "
              f"({args.lessons} lessons + 1 Final Explanation)")

        batch_id = submit_batch(requests)

        # Save batch ID and metadata for later collection
        id_path = _batch_id_path(args.output)
        id_path.write_text(batch_id)
        meta_path = id_path.with_suffix('.json')
        _subj_cap = _subject_display(args.subject)
        _subj_file = _SUBJECT_FOLDER.get(args.subject, _subj_cap)
        meta_path.write_text(json.dumps({
            "unit": unit,
            "meta": {
                "subject":        _subj_cap,
                "grade":          args.grade,
                "substrand_id":   args.substrand,
                "substrand_name": args.substrand_name,
                "outputDir":      _v2_output_dir(args.grade, args.subject, args.substrand, args.substrand_name),
                "filePrefix":     f"{_subj_file}_{args.substrand_name.replace(' ', '_')}",
                "titleDoc":       f"{_subj_cap.upper()} GRADE {args.grade}: {args.substrand_name.upper()}",
                "subtitleDoc":    f"CBE Phenomenon-Driven Lesson Sequence — Sub-Strand {args.substrand} ({args.lessons} Lessons)",
                "col3Label":      "Teacher Moves",
                "col5Label":      "Formative Assessment Strategy",
            },
            "lessons": args.lessons,
            "fact_sheet": args.fact_sheet,
            "lesson_count_source": lesson_count_source,
        }, ensure_ascii=False, indent=2))

        print(f"\n✓ Batch submitted!")
        print(f"  Batch ID saved to: {id_path}")
        print(f"  Collect results when ready:")
        print(f"    python3 src/generate_substrand.py --collect {args.output} --run")
        print(f"  Or poll automatically:")
        print(f"    python3 src/generate_substrand.py --collect {args.output} --wait --run")
        return

    # LESSONS — with checkpoint resume support
    lessons        = []
    prev_summaries = []
    start_lesson   = 1

    if args.resume:
        saved = _load_checkpoint(args.output)
        if saved:
            lessons        = saved
            prev_summaries = [{"number": l["number"], "title": l["title"],
                                "summary": l.get("summaryTablePrompt", {}).get("learned", "")[:150]}
                               for l in lessons]
            start_lesson   = len(lessons) + 1
            print(f"  Resuming from lesson {start_lesson} ({len(lessons)} already done)")

    for lesson_num in range(start_lesson, args.lessons + 1):
        lesson = generate_lesson(lesson_num, curriculum_text, lesson_template,
                                  unit, prev_summaries, args, fact_sheet=args.fact_sheet)
        if not lesson:
            print(f"  WARNING: Failed to generate Lesson {lesson_num} — using stub")
            lesson = {
                "number": lesson_num,
                "title": f"Lesson {lesson_num}",
                "duration": "40 minutes",
                "substrand": f"Sub-Strand {args.substrand}: {args.substrand_name}",
                "aresKeywords": args.substrand_name.lower(),
                "slo": {"purpose": "", "knowledge": "", "skills": "", "attitudes": "",
                        "keyInquiry": "", "purposeInStoryline": "", "safetyNotes": ""},
                "overview": "",
                "framework": [
                    {"phase": ph, "learnerExperience": "", "teacherMoves": "",
                     "sensemakingStrategy": "", "formativeAssessment": ""}
                    for ph in ["Predict Phase", "Observe Phase", "Explain Phase",
                                "Driving Question Board (DQB) Creation", "Model Building Phase"]
                ],
                "teacherReflection": "",
                "summaryTablePrompt": {"observed": "", "learned": "", "explained": ""},
            }
        lessons.append(lesson)

        # Save checkpoint after each lesson so we can resume if interrupted
        _save_checkpoint(args.output, lessons)

        # Track lesson summary for next lesson's context
        prev_summaries.append({
            "number": lesson_num,
            "title": lesson.get("title", f"Lesson {lesson_num}"),
            "summary": lesson.get("summaryTablePrompt", {}).get("learned", "")[:150],
        })

        # Brief pause to avoid rate limits
        time.sleep(1)

    # Lessons must agree with each other before the Final Explanation is written.
    consistency_pass(unit, lessons, args, args.fact_sheet, args.output)

    # FINAL EXPLANATION
    fe = generate_final_explanation(curriculum_text, unit, lessons, args,
                                     fe_template=fe_template,
                                     lesson_template=lesson_template,
                                     log_name=args.output)
    if fe:
        print("  Final Explanation generated ✓")
    else:
        print("  WARNING: Final Explanation generation failed — using null")

    # SUMMARY TABLE
    st = generate_summary_table(unit, lessons, args, st_template=st_template)
    if st:
        print("  Summary Table generated ✓")
    else:
        print("  WARNING: Summary Table generation failed — using null")

    # ── Build META ─────────────────────────────────────────────────────────────

    subject_cap = _subject_display(args.subject)
    subject_file = _SUBJECT_FOLDER.get(args.subject, subject_cap)

    meta = {
        "subject":     subject_cap,
        "grade":       args.grade,
        "substrand_id":   args.substrand,
        "substrand_name": args.substrand_name,
        "outputDir":   _v2_output_dir(args.grade, args.subject, args.substrand, args.substrand_name),
        "filePrefix":  f"{subject_file}_{args.substrand_name.replace(' ', '_')}",
        "titleDoc":    f"{subject_cap.upper()} GRADE {args.grade}: {args.substrand_name.upper()}",
        "subtitleDoc": f"CBE Phenomenon-Driven Lesson Sequence — Sub-Strand {args.substrand} ({args.lessons} Lessons)",
        "col3Label":   "Teacher Moves",
        "col5Label":   "Formative Assessment Strategy",
    }

    # ── Write data file ─────────────────────────────────────────────────────

    print("\n3. Writing data file...")
    output_path = write_data_file(args.output, meta, unit, lessons, fe, st)

    # ── Optionally run generator ─────────────────────────────────────────────

    if args.run:
        print(f"\n4. Running generator...")
        import subprocess
        result = subprocess.run(
            ['node', 'generators/generate.js', args.output],
            cwd=PROJECT_ROOT,
            capture_output=True, text=True,
        )
        print(result.stdout)
        if result.returncode != 0:
            print("Generator errors:", result.stderr)

    log_run_cost(args.output, 'run')
    print(f"\n✓ Done!")
    print(f"  Data file: {output_path}")
    print(f"  To generate docx: node generators/generate.js {args.output}")


if __name__ == '__main__':
    main()
