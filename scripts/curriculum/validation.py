"""Cheap structural/evidence checks before independent content review.

Passing this module does not establish factual correctness or classroom pacing.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


def validate(base, name, fixture=False):
    from .compiler import calc
    errors, warnings = [], []
    records = {}
    for area in ('sources', 'manuscripts', 'materials', 'blueprints'):
        path = base / area / (name + '.json')
        try:
            records[area] = json.loads(path.read_text())
        except (OSError, ValueError):
            errors.append(f'{area}: missing or invalid JSON')
    if len(records) != 4:
        return {'module': name, 'errors': errors, 'warnings': warnings}
    source, manuscript, bank, blueprint = (records[k] for k in ('sources', 'manuscripts', 'materials', 'blueprints'))
    inventory_file = base / 'inventory' / (name + '.json')
    if inventory_file.exists() and json.loads(inventory_file.read_text()).get('source_status') not in ('verified', 'reviewed_pilot'):
        errors.append('source inventory has an unresolved source/transcription blocker')
    if fixture:
        pilot = ROOT / 'data/codex_pilot_2026-11'
        for area in ('sources', 'manuscripts', 'materials'):
            reference = pilot / area / (name + '.json')
            if not reference.is_file() or records[area] != json.loads(reference.read_text()):
                errors.append('fixture mode requires unchanged reviewed pilot records: ' + area)
        old_blueprint = pilot / 'blueprints' / (name + '.json')
        if old_blueprint.is_file():
            original = json.loads(old_blueprint.read_text())
            if any(blueprint.get(k) != v for k, v in original.items()):
                errors.append('fixture mode changed original blueprint fields')
    for key in ('outcomes', 'inquiry_questions', 'coreCompetencies', 'values', 'pcis'):
        if not source.get(key):
            errors.append(f'source: required field {key} empty')
    try:
        verification = json.loads((base / 'sources' / (name + '.verification.json')).read_text())
        if verification.get('source_record_sha256') != sha(base / 'sources' / (name + '.json')):
            errors.append('source verification does not match the current record')
        if verification.get('status') != 'verified' or not verification.get('evidence'):
            errors.append('source visual/transcription verification incomplete')
        evidence_file = ROOT / verification.get('evidence', '')
        if not evidence_file.is_file() or sha(evidence_file) != verification.get('evidence_sha256'):
            errors.append('source verification evidence missing/changed')
        crop = base / 'sources' / (name + '_source.png')
        if not crop.is_file() or sha(crop) != verification.get('crop_sha256'):
            errors.append('source crop missing/changed')
    except (OSError, ValueError):
        errors.append('source verification record missing')
    source_pdf = ROOT / source.get('pdf', '')
    if not source_pdf.is_file() or sha(source_pdf) != source.get('pdf_sha256'):
        errors.append('source PDF missing or its hash changed')
    outcomes = {x.get('id') for x in source.get('outcomes', [])}
    if not outcomes or None in outcomes or len(outcomes) != len(source.get('outcomes', [])):
        errors.append('source outcome IDs empty/duplicate')
    items = bank.get('items', [])
    cards = {c.get('id'): c for c in items}
    if None in cards or len(cards) != len(items):
        errors.append('material IDs missing/duplicate')
    for card_id, card in cards.items():
        if not all(card.get(k) for k in ('title', 'student', 'teacher')):
            errors.append(f'{card_id}: missing student task, title or teacher preparation/key')
        for relative in card.get('assets', []):
            if not (base / 'materials' / relative).is_file():
                errors.append(f'{card_id}: missing asset {relative}')
        if re.search(r'(?i)(Teacher key and preparation|Exemplar answer\s*:)', card.get('student', '')):
            errors.append(f'{card_id}: teacher-key marker in student material')
    prefixes = {re.match(r'([A-Za-z]+)\d+$', k)[1] for k in cards if isinstance(k, str) and re.match(r'([A-Za-z]+)\d+$', k)}
    reference_re = re.compile(r'\b(?:' + '|'.join(re.escape(p) for p in prefixes) + r')\d+\b') if prefixes else None
    if reference_re:
        for text in strings([manuscript, items]):
            for match in reference_re.finditer(text):
                ref = match.group()
                if ref not in cards:
                    # A legacy key has "C24 m²" for shape C's answer, not
                    # card C24. Do not rewrite or reject that reviewed input.
                    if re.match(r'\s*(?:m|cm|mm|km|KES|USD)(?:[²³]|\b)', text[match.end():]):
                        warnings.append(f'ambiguous numeric/shape label {ref}; reviewer checks context')
                    else:
                        errors.append(f'unsupplied card reference {ref}')
    checks = bank.get('calculations', [])
    values = {}
    for check in checks:
        key = check.get('id')
        if not key or key in values:
            errors.append('calculation ID empty/duplicate')
            continue
        try:
            import math
            value = calc(check['expression'])
            if not math.isclose(value, check['expected'], rel_tol=check.get('relative_tolerance', 1e-8), abs_tol=check.get('absolute_tolerance', 1e-8)):
                errors.append(f'calculation {key} disagrees with expected answer')
            values[key] = value
        except (KeyError, TypeError, ValueError, ZeroDivisionError, OverflowError):
            errors.append(f'calculation {key} invalid')
    for text in strings([manuscript, items]):
        for key in re.findall(r'\{\{([^}:]+):[^}]+\}\}', text):
            if key not in values:
                errors.append(f'unresolved calculation reference {key}')
    lessons = manuscript.get('lessons', [])
    if not lessons or len(lessons) != blueprint.get('lesson_count'):
        errors.append('lesson count missing or differs from blueprint')
    allocation = source.get('official_lesson_allocation')
    if allocation is not None and len(lessons) != allocation and not blueprint.get('allocation_override_evidence'):
        errors.append('official lesson allocation differs; documented user override evidence required')
    taught = set()
    for number, lesson in enumerate(lessons, 1):
        if lesson.get('number') != number:
            errors.append(f'lesson {number}: numbering mismatch')
        times = lesson.get('minutes', [])
        if len(times) != 5 or any(not isinstance(n, (int, float)) or isinstance(n, bool) or n <= 0 for n in times) or sum(times) != 40:
            errors.append(f'lesson {number}: five positive phases must total 40 minutes')
        phases = lesson.get('phases', [])
        if len(phases) != 5 or any(len(p) != 4 or any(not isinstance(x, str) or not x.strip() for x in p) for p in phases):
            errors.append(f'lesson {number}: incomplete phase cells')
        refs = set(lesson.get('materials', []))
        if not refs <= cards.keys():
            errors.append(f'lesson {number}: missing listed materials')
        taught.update(lesson.get('outcomes', []))
        if not set(lesson.get('outcomes', [])) <= outcomes:
            errors.append(f'lesson {number}: unknown outcome')
    if taught != outcomes:
        errors.append('source teaching coverage mismatch')
    if blueprint.get('lesson_map') != [dict(lesson=l.get('number'), title=l.get('title'), outcomes=l.get('outcomes'), materials=l.get('materials')) for l in lessons]:
        errors.append('blueprint lesson map differs from manuscript')
    final = manuscript.get('assessment', {})
    sections = final.get('sections', [])
    if not sections or any(not all(s.get(k) for k in ('title', 'prompt', 'exemplar')) for s in sections):
        errors.append('assessment section missing prompt/key')
    if lessons:
        forbidden = ('then paired comparison', 'Evidence-first group work', 'Revise a shared model')
        strategies = ' '.join(p[2] for p in lessons[-1].get('phases', []) if len(p) == 4)
        if any(s in strategies for s in forbidden):
            errors.append('independent final contains collaborative strategies')
    evidence = blueprint.get('assessment_tasks', [])
    if not evidence:
        errors.append('explicit assessment_tasks missing (formative/final scope required)')
    evidence_ids = {t.get('id'): t for t in evidence}
    if None in evidence_ids or len(evidence_ids) != len(evidence):
        errors.append('assessment task IDs missing/duplicate')
    assessed = set()
    for task in evidence:
        if not task.get('skills'):
            errors.append('assessment task needs declared skill evidence')
        assessed.update(task.get('outcomes', []))
        if not set(task.get('outcomes', [])) <= outcomes:
            errors.append('assessment task has unknown outcome')
        if not set(task.get('materials', [])) <= cards.keys():
            errors.append('assessment task references missing material')
        if task.get('kind') not in ('formative', 'independent_final'):
            errors.append('assessment task must declare formative or independent_final')
        if task.get('kind') == 'independent_final' and not 1 <= task.get('section', 0) <= len(sections):
            errors.append('final assessment task has invalid section reference')
    if assessed != outcomes:
        errors.append('observable assessment coverage mismatch')
    links = blueprint.get('rubric_links', [])
    if {x.get('criterion') for x in links} != set(range(1, len(final.get('rubric', [])) + 1)):
        errors.append('each final rubric criterion needs explicit task evidence')
    for link in links:
        if not link.get('required_skills'):
            errors.append('rubric criterion needs declared required skills')
        tasks = [evidence_ids.get(key) for key in link.get('tasks', [])]
        if not tasks or any(t is None or t.get('kind') != 'independent_final' for t in tasks):
            errors.append('final rubric cites absent/non-final task evidence')
        skills = {skill for t in tasks if t for skill in t.get('skills', [])}
        if not set(link.get('required_skills', [])) <= skills:
            errors.append('rubric criterion requires a skill absent from its linked tasks')
    for key in ('coreCompetencies', 'values', 'pcis'):
        if manuscript.get('unit', {}).get(key) != source.get(key):
            errors.append(f'verbatim source {key} differs in manuscript')
    if not blueprint.get('rationale') or not blueprint.get('allocation_status'):
        errors.append('lesson allocation requires a rationale and source/design status')
    for text in strings([manuscript, bank]):
        if re.search(r'\b(?:TODO|FILL|TBD|undefined|NaN)\b', text):
            errors.append('unresolved drafting placeholder')
    if fixture:
        warnings.append('Reviewed reference fixture; this does not certify new lesson content')
    warnings.append('Numeric setup, units, substantive coverage, rubric/task meaning, science/safety and classroom pacing require independent review')
    return {'module': name, 'lessons': len(lessons), 'calculations': len(checks),
            'errors': sorted(set(errors)), 'warnings': warnings}
