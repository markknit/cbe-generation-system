"""Reproduce isolated regression fixtures from the frozen reviewed pilot."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
PILOT = ROOT / 'data/codex_pilot_2026-11'
OUTCOMES = {'essmath_2_8': [['a','b'],['c'],['d'],['e'],['f']],
            'coremath_2_5': [['a','b'],['c'],['d'],['e'],['f','g']],
            'gensci_2_4': [['a'],['b'],['c'],['d'],['e','f']]}
LINKS = {'essmath_2_8': [[1],[2,3],[4],[5]], 'coremath_2_5': [[1],[2,3],[4],[5]], 'gensci_2_4': [[1],[2,3],[4],[5]]}


def prepare(base):
    if base.resolve() == PILOT.resolve():
        raise ValueError('Cannot overwrite frozen pilot')
    for area in ('sources', 'manuscripts', 'materials', 'blueprints', 'modules', 'evidence', 'reviews'):
        (base / area).mkdir(parents=True, exist_ok=True)
    for filename in ('attribution.yaml', 'resource_policy.json'):
        shutil.copyfile(PILOT / filename, base / filename)
    shutil.copytree(PILOT / 'materials/diagrams', base / 'materials/diagrams', dirs_exist_ok=True)
    for name, outcomes in OUTCOMES.items():
        for area in ('sources', 'manuscripts', 'materials', 'blueprints'):
            shutil.copyfile(PILOT / area / (name + '.json'), base / area / (name + '.json'))
        shutil.copyfile(PILOT / 'sources' / (name + '_source.png'), base / 'sources' / (name + '_source.png'))
        record = base / 'sources' / (name + '.json')
        source_evidence = PILOT / 'reviews/independent' / (name + '_recheck.md')
        verification = {'status': 'verified', 'source_record_sha256': hashlib.sha256(record.read_bytes()).hexdigest(),
                        'evidence': str(source_evidence.relative_to(ROOT)),
                        'evidence_sha256': hashlib.sha256(source_evidence.read_bytes()).hexdigest(),
                        'crop_sha256': hashlib.sha256((base / 'sources' / (name + '_source.png')).read_bytes()).hexdigest(),
                        'kind': 'reviewed_reference_fixture'}
        (base / 'sources' / (name + '.verification.json')).write_text(json.dumps(verification, indent=2))
        manuscript = json.loads((base / 'manuscripts' / (name + '.json')).read_text())
        path = base / 'blueprints' / (name + '.json')
        blueprint = json.loads(path.read_text())
        tasks = [{'id': f'formative_{l["number"]}', 'kind': 'formative', 'outcomes': l['outcomes'],
                  'materials': l['materials'], 'skills': ['outcome_' + o for o in l['outcomes']]} for l in manuscript['lessons'][:-1]]
        tasks += [{'id': f'final_{i}', 'kind': 'independent_final', 'section': i, 'outcomes': o,
                   'materials': manuscript['lessons'][-1]['materials'], 'skills': ['outcome_' + x for x in o]} for i, o in enumerate(outcomes, 1)]
        blueprint['assessment_tasks'] = tasks
        blueprint['rubric_links'] = [{'criterion': i, 'tasks': ['final_' + str(t) for t in indices],
                                     'required_skills': sorted({'outcome_' + o for t in indices for o in outcomes[t-1]})} for i, indices in enumerate(LINKS[name], 1)]
        path.write_text(json.dumps(blueprint, ensure_ascii=False, indent=2))
        from curriculum_pipeline import content_fingerprint
        evidence = PILOT / 'reviews/independent' / (name + '_recheck.md')
        acceptance = {'kind': 'regression_fixture', 'content_fingerprint': content_fingerprint(base, name),
                      'evidence': [{'path': str(evidence.relative_to(ROOT)), 'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()}]}
        target = base / 'reviews' / name / 'content_acceptance.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(acceptance, indent=2))
