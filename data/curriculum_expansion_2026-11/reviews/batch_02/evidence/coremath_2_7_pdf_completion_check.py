"""Read-only scoped artifact check; writes only its JSON evidence beside this file."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
from curriculum_pipeline import content_fingerprint
W = ROOT / 'data/curriculum_expansion_2026-11'
D = json.loads((W / 'manuscripts/coremath_2_7.json').read_text())
PREFIX = D['prefix']
OUT = next((W / 'outputs/v2').rglob(PREFIX + '_data.json')).parent
NS = {'x': 'http://www.w3.org/1999/xhtml'}
TYPES = ['CBE_LessonSequence', 'FinalExplanation', 'FinalExplanation_TeacherKey', 'SummaryTable']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def norm(s):
    # Keep actual hyphens, joining only the line-break whitespace after them.
    return re.sub(r'(?<=-)\s+(?=\w)', '', re.sub(r'\s+', ' ', s)).strip()

blocks = {}
plain = {}
hashes = {}
for typ in TYPES:
    pdf = W / 'outputs/PDF' / (PREFIX + '_' + typ + '.pdf')
    docx = OUT / (PREFIX + '_' + typ + '.docx')
    hashes[typ] = {'docx_sha256': sha(docx), 'pdf_sha256': sha(pdf)}
    plain[typ] = subprocess.check_output(['pdftotext', str(pdf), '-'], text=True)
    xml = ET.fromstring(subprocess.check_output(['pdftotext', '-bbox-layout', str(pdf), '-']))
    blocks[typ] = []
    for page_number, page in enumerate(xml.findall('.//x:page', NS), 1):
        for b in page.findall('.//x:block', NS):
            blocks[typ].append({'page': page_number, 'x': float(b.attrib['xMin']), 'y': float(b.attrib['yMin']),
                                'text': ' '.join(word.text or '' for word in b.findall('.//x:word', NS))})

def region(typ, regions):
    return ' '.join(b['text'] for b in blocks[typ] if any(b['page'] == p and xmin <= b['x'] < xmax and ymin <= b['y'] < ymax
                    for p, xmin, xmax, ymin, ymax in regions))

rows = []
def check(label, expected, typ, regions=None):
    actual = region(typ, regions) if regions else ' '.join(b['text'] for b in blocks[typ])
    rows.append({'field': label, 'document': typ, 'pass': norm(expected) in norm(actual),
                 'method': 'bbox cell continuation' if regions else 'bbox text blocks',
                 **({'regions': regions} if regions else {})})

for typ in ['FinalExplanation', 'FinalExplanation_TeacherKey']:
    check('assessment.instructions', D['assessment']['instructions'], typ)
    for i, section in enumerate(D['assessment']['sections'], 1):
        # The capacity prompt and key continue across p1/p2 in the key table.
        rr = [(1, 60, 200, 537, 549), (2, 60, 200, 57, 121)] if typ.endswith('TeacherKey') and i == 3 else None
        check(f'assessment.section{i}.prompt', section['prompt'], typ, rr)
    cols = [(60, 200), (210, 335), (343, 470), (477, 603), (610, 730)]
    for i, rubric in enumerate(D['assessment']['rubric'], 1):
        for (key, expected), (xmin, xmax) in zip(rubric.items(), cols):
            rr = None
            if i == 3:
                rr = ([(5, xmin, xmax, 538, 550), (6, xmin, xmax, 57, 121)] if typ == 'FinalExplanation'
                      else [(2, xmin, xmax, 509, 552), (3, xmin, xmax, 57, 90)])
            check(f'assessment.rubric{i}.{key}', expected, typ, rr)
for i, section in enumerate(D['assessment']['sections'], 1):
    rr = [(1, 210, 731, 537, 549), (2, 210, 731, 57, 70)] if i == 3 else None
    check(f'assessment.section{i}.exemplar', section['exemplar'], 'FinalExplanation_TeacherKey', rr)
    rows.append({'field': f'assessment.section{i}.exemplar_absent', 'document': 'FinalExplanation',
                 'pass': norm(section['exemplar']) not in norm(plain['FinalExplanation']), 'method': 'student exemplar exclusion'})
for i, lesson in enumerate(D['lessons'], 1):
    for key, value in lesson['summary'].items():
        check(f'lesson{i}.summary.{key}', value, 'SummaryTable')
for i, phase in enumerate(D['lessons'][-1]['phases'], 1):
    for j, value in enumerate(phase, 1):
        check(f'lesson14.phase{i}.{j}', value, 'CBE_LessonSequence')
data = json.loads((OUT / (PREFIX + '_data.json')).read_text())
resources = data['LESSONS'][-1]['resourceLinks']
slots = {phase: {k: value[k] for k in ('video', 'reading')} for phase, value in resources.items()}
fingerprint = content_fingerprint(W, 'coremath_2_7')
result = {'content_fingerprint': fingerprint, 'fingerprint_matches_accepted': fingerprint == '261cfa07c19ffbd3eb912f3e18573dde71de2328970b3c276b3224a3478b6378',
          'artifact_hashes': hashes, 'checks': rows, 'checks_total': len(rows), 'checks_pass': sum(r['pass'] for r in rows),
          'final_resource_slots': slots, 'final_slots_null': all(v is None for phase in slots.values() for v in phase.values()),
          'normalization': 'Whitespace collapsed; whitespace immediately after a retained hyphen is removed. No glyphs or words discarded.',
          'scope': 'PDF canonical propagation, exact four-artifact hashes, accepted fingerprint and final null slots. Visual evidence and limits in completion report.'}
result['reproduced_layout_failures'] = []
for typ, label, expected in [
    ('SummaryTable', 'lesson1.summary.learned', D['lessons'][0]['summary']['learned']),
    ('FinalExplanation', 'assessment.rubric1.criterion', D['assessment']['rubric'][0]['criterion']),
    ('CBE_LessonSequence', 'lesson14.phase1.1', D['lessons'][-1]['phases'][0][0]),
]:
    pdf = W / 'outputs/PDF' / (PREFIX + '_' + typ + '.pdf')
    layout = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
    result['reproduced_layout_failures'].append({'document': typ, 'field': label, 'expected': expected,
        'naive_layout_substring_found': norm(expected) in norm(layout),
        'bbox_pass': next(r['pass'] for r in rows if r['document'] == typ and r['field'] == label)})
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'checks': result['checks_total'], 'passed': result['checks_pass'], 'fingerprint_matches': result['fingerprint_matches_accepted'], 'final_null': result['final_slots_null'],
                  'failures': [r for r in rows if not r['pass']]}, indent=2))
if result['checks_total'] != result['checks_pass'] or not result['fingerprint_matches_accepted'] or not result['final_slots_null']:
    raise SystemExit(1)
