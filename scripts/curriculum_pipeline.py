#!/usr/bin/env python3
"""Stage canonical curriculum records, then build only changed outputs.

No model endpoint is called. New content requires independent review before
final rendering. The original reviewed pilot workspace is read-only here.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = ('CBE_LessonSequence', 'CompactTeacherGuide', 'StudentMaterials',
            'MaterialsTeacherKey', 'FinalExplanation', 'FinalExplanation_TeacherKey',
            'SummaryTable', 'StudentSummaryTable', 'AssessmentMaterials')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def content_fingerprint(base, name):
    paths = [base / a / (name + '.json') for a in ('sources', 'blueprints', 'materials', 'manuscripts')]
    paths.append(base / 'sources' / (name + '.verification.json'))
    bank = load(base / 'materials' / (name + '.json'))
    for card in bank['items']:
        picture = base / 'materials/diagrams' / (card['id'] + '.png')
        if picture.exists():
            paths.append(picture)
        paths += [base / 'materials' / a for a in card.get('assets', [])]
    return hashlib.sha256(json.dumps({str(p.relative_to(base)): sha(p) for p in sorted(set(paths))}, sort_keys=True).encode()).hexdigest()


def signature(paths, extra=''):
    return hashlib.sha256((extra + json.dumps({str(p): sha(p) for p in sorted(set(paths))}, sort_keys=True)).encode()).hexdigest()


def content_signature(base, name):
    from curriculum import compiler
    return signature([Path(compiler.__file__), Path(__file__), base / 'attribution.yaml'], content_fingerprint(base, name))


def standard_signature(base, name):
    code = list((ROOT / 'generators/lib').glob('*.js')) + [ROOT / 'generators/aresResources.js', ROOT / 'generators/generate.js', ROOT / 'src/ares_recommender.py', ROOT / 'config/link_matching.yaml', ROOT / 'scripts/curriculum/resource_recommender.py', ROOT / 'scripts/curriculum/resource_policy.py', Path(__file__)]
    db = ROOT / 'data/ares_index/ares_content.db'
    db_version = str((db.stat().st_size, db.stat().st_mtime_ns))
    return signature([base / 'attribution.yaml', base / 'resource_policy.json'] + code, content_fingerprint(base, name) + db_version)


def cached(state, key, fingerprint, base):
    record = state.get(key, {})
    files = record.get('files', {})
    return record.get('input') == fingerprint and bool(files) and all((base / p).is_file() and sha(base / p) == h for p, h in files.items())


def remember(state, key, fingerprint, files, base):
    state[key] = {'input': fingerprint, 'files': {str(p.relative_to(base)): sha(p) for p in files}}


def preflight(base, name, fixture):
    from curriculum.validation import validate
    result = validate(base, name, fixture)
    save(base / 'evidence/preflight' / (name + '.json'), result)
    if result['errors']:
        raise ValueError(f'{name}: ' + '; '.join(result['errors']))
    return result


def acceptance(base, name, fingerprint, fixture):
    record = load(base / 'reviews' / name / 'content_acceptance.json')
    if record.get('content_fingerprint') != fingerprint:
        raise ValueError('Content review is stale for ' + name)
    if record.get('kind') == 'regression_fixture':
        if not fixture:
            raise ValueError('Fixture evidence cannot accept new lesson content')
    elif record.get('verdict') != 'accepted' or record.get('unresolved_confirmed_errors', 1) != 0:
        raise ValueError('Independent content review has not accepted ' + name)
    evidence = record.get('evidence', [])
    if not evidence or any(not (ROOT / r['path']).is_file() or sha(ROOT / r['path']) != r['sha256'] for r in evidence):
        raise ValueError('Independent review evidence missing/changed for ' + name)


def build(base, names, fixture):
    from curriculum import compiler
    compiler.BASE = base
    state_path = base / 'evidence/build_state.json'
    state = load(state_path) if state_path.exists() else {}
    for name in names:
        report = preflight(base, name, fixture)
        fp = content_signature(base, name)
        key = name + ':content'
        if cached(state, key, fp, base):
            print(name, 'content build unchanged; skipped')
            continue
        result = compiler.build(name)
        manuscript = load(base / 'manuscripts' / (name + '.json'))
        module = json.loads((base / 'modules' / (name + '_data.js')).read_text().split('module.exports = ', 1)[1].rstrip().removesuffix(';'))
        directory = base / 'outputs' / module['META']['outputDir']
        files = [base / 'modules' / (name + '_data.js'), base / 'evidence' / (name + '_checks.json')]
        files += [directory / (manuscript['prefix'] + '_' + suffix + '.docx') for suffix in ('CompactTeacherGuide', 'StudentMaterials', 'MaterialsTeacherKey', 'StudentSummaryTable', 'AssessmentMaterials')]
        remember(state, key, fp, files, base)
        save(state_path, state)
        print(name, 'content built:', result['lessons'], 'lessons;', report['calculations'], 'calculation checks')


def render(base, names, fixture):
    build(base, names, fixture)
    state_path = base / 'evidence/build_state.json'
    state = load(state_path)
    for name in names:
        fingerprint = content_fingerprint(base, name)
        acceptance(base, name, fingerprint, fixture)
        fp = standard_signature(base, name)
        key = name + ':standard'
        if cached(state, key, fp, base):
            print(name, 'standard documents unchanged; skipped')
            continue
        manuscript = load(base / 'manuscripts' / (name + '.json'))
        environment = {**os.environ, 'CBE_WORKSPACE': str(base), 'CBE_MODULE_NAME': name, 'CBE_DATA_DIR': str(base / 'modules'),
                       'CBE_OUTPUT_ROOT': str(base / 'outputs'), 'CBE_FE_ISSUES_DIR': str(base / 'reviews/fe_issues'),
                       'ATTRIBUTION_YAML': str(base / 'attribution.yaml'),
                       'ARES_RECOMMENDER_SCRIPT': str(ROOT / 'scripts/curriculum/resource_recommender.py'),
                       'CBE_INDEPENDENT_LESSON_TITLES': json.dumps([manuscript['lessons'][-1]['title']])}
        log = base / 'evidence' / (name + '_render.log')
        with log.open('w') as stream:
            subprocess.run(['node', str(ROOT / 'generators/generate.js'), name], env=environment, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)
        output = next((base / 'outputs/v2').rglob(manuscript['prefix'] + '_data.json'))
        directory = output.parent
        files = [output] + [directory / (manuscript['prefix'] + '_' + suffix + '.docx') for suffix in ('CBE_LessonSequence', 'FinalExplanation', 'FinalExplanation_TeacherKey', 'SummaryTable')]
        remember(state, key, fp, files, base)
        save(state_path, state)
        print(name, 'standard documents built; local link/consistency gates passed')


def pdf(base, names):
    state_path = base / 'evidence/build_state.json'
    state = load(state_path) if state_path.exists() else {}
    version = subprocess.check_output(['soffice', '--version'], text=True).strip() + sha(Path(__file__))
    selected = []
    for name in names:
        prefix = load(base / 'manuscripts' / (name + '.json'))['prefix']
        for path in sorted((base / 'outputs/v2').rglob(prefix + '_*.docx')):
            target = base / 'outputs/PDF' / (path.stem + '.pdf')
            fp = signature([path], version)
            key = str(path.relative_to(base)) + ':pdf'
            if cached(state, key, fp, base):
                continue
            selected.append((path, target, fp, key))
    if not selected:
        print('PDF conversion unchanged; skipped')
        return
    with tempfile.TemporaryDirectory(prefix='cbe-convert-') as temporary:
        temporary = Path(temporary)
        result = subprocess.run(['soffice', '-env:UserInstallation=' + (temporary / 'profile').as_uri(), '--headless', '--convert-to', 'pdf', '--outdir', str(temporary), *[str(p) for p, _, _, _ in selected]], capture_output=True, text=True, timeout=240)
        if result.returncode:
            raise RuntimeError('LibreOffice failed; no successful conversion claimed')
        if any(not (temporary / target.name).is_file() for _, target, _, _ in selected):
            raise RuntimeError('LibreOffice omitted a PDF; old PDFs are not accepted as fresh conversions')
        for _, target, fp, key in selected:
            target.parent.mkdir(parents=True, exist_ok=True)
            (temporary / target.name).replace(target)
            remember(state, key, fp, [target], base)
    save(state_path, state)
    print('PDFs converted:', len(selected))


def audit(base, names, fixture=False):
    import jsonschema
    validator = jsonschema.Draft202012Validator(load(ROOT / 'ares-contract.schema.json'))
    rows = []
    state = load(base / 'evidence/build_state.json')
    version = subprocess.check_output(['soffice', '--version'], text=True).strip() + sha(Path(__file__))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for name in names:
        preflight(base, name, fixture)
        acceptance(base, name, content_fingerprint(base, name), fixture)
        if not cached(state, name + ':content', content_signature(base, name), base) or not cached(state, name + ':standard', standard_signature(base, name), base):
            raise ValueError(name + ': stale/missing content or standard build; final audit cannot pass old exports')
        manuscript = load(base / 'manuscripts' / (name + '.json'))
        prefix = manuscript['prefix']
        data_path = next((base / 'outputs/v2').rglob(prefix + '_data.json'))
        data = load(data_path)
        errors = list(validator.iter_errors(data))
        if errors:
            raise ValueError(name + ': R1 schema errors: ' + '; '.join(e.message for e in errors))
        allowed = load(base / 'resource_policy.json').get('module_allowed_titles', {}).get(name)
        if allowed is not None:
            for lesson in data['LESSONS']:
                for resources in lesson['resourceLinks'].values():
                    for kind in ('video', 'reading'):
                        if resources[kind] is not None and resources[kind]['title'] not in allowed:
                            raise ValueError(name + ': selected resource has not been independently vetted')
        for suffix in SUFFIXES:
            docx = data_path.parent / (prefix + '_' + suffix + '.docx')
            pdf_path = base / 'outputs/PDF' / (prefix + '_' + suffix + '.pdf')
            if not docx.is_file() or not pdf_path.is_file():
                raise ValueError(name + ': incomplete nine-type document inventory')
            if not cached(state, str(docx.relative_to(base)) + ':pdf', signature([docx], version), base):
                raise ValueError('PDF is stale or changed: ' + pdf_path.name)
            with zipfile.ZipFile(docx) as archive:
                body = archive.read('word/document.xml').decode()
                xml = ' '.join(archive.read(p).decode() for p in archive.namelist() if p.startswith('word/') and p.endswith('.xml'))
                if 'ChatGPT/Codex' not in xml or 'OpenAI' not in xml or any(s in xml for s in ('Claude, Anthropic', 'AI assistance from Claude')):
                    raise ValueError('Incorrect attribution in ' + docx.name)
                if suffix in ('FinalExplanation', 'StudentMaterials', 'AssessmentMaterials') and any(s in body for s in ('Teacher key and preparation', 'Teacher Key: Exemplar Answers', 'Exemplar answer:')):
                    raise ValueError('Teacher exemplar marker in student file ' + docx.name)
                if suffix == 'StudentSummaryTable':
                    tree = ET.fromstring(body)
                    for row in tree.findall('.//w:tbl/w:tr', ns)[1:]:
                        if any(''.join(c.itertext()).strip() for c in row.findall('w:tc', ns)[1:]):
                            raise ValueError('Student summary is not blank')
            text = subprocess.check_output(['pdftotext', '-layout', str(pdf_path), '-'], text=True)
            if any(token in text for token in ('{{', 'undefined', 'NaN', 'FILL', '\ufffd')):
                raise ValueError('Unresolved placeholder in ' + pdf_path.name)
            rows.append({'module': name, 'type': suffix, 'docx_sha256': sha(docx), 'pdf_sha256': sha(pdf_path), 'text_characters': len(text)})
        if any(resources[k] is not None for resources in data['LESSONS'][-1]['resourceLinks'].values() for k in ('video', 'reading')):
            raise ValueError('Independent assessment contains selected external resources')
    save(base / 'evidence/artifact_audit.json', {'documents': rows, 'scope': 'Automated structural/text checks; content review and visual layout inspection remain separate requirements.'})
    print('Artifact audit passed:', len(rows), 'Word/PDF pairs')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=ROOT / 'data/curriculum_expansion_2026-11')
    parser.add_argument('--fixture', action='store_true', help='Validate explicitly attested reviewed reference copies; never accepts new content')
    parser.add_argument('command', choices=('check', 'build', 'render', 'pdf', 'audit'))
    parser.add_argument('modules', nargs='*')
    args = parser.parse_args()
    base = args.workspace.resolve()
    if base == ROOT / 'data/codex_pilot_2026-11':
        parser.error('The reviewed pilot is frozen. Use a separate workspace.')
    os.environ['CBE_WORKSPACE'] = str(base)
    names = args.modules or sorted(p.stem for p in (base / 'manuscripts').glob('*.json'))
    if not names:
        parser.error('No authored modules selected')
    if args.command in ('build', 'render'):
        subprocess.run(['python3', str(ROOT / 'scripts/check_codex_usage.py')], check=True, stdout=subprocess.DEVNULL)
    if args.command == 'check':
        for name in names:
            print(json.dumps(preflight(base, name, args.fixture)))
    elif args.command == 'build':
        build(base, names, args.fixture)
    elif args.command == 'render':
        render(base, names, args.fixture)
    elif args.command == 'pdf':
        pdf(base, names)
    else:
        audit(base, names, args.fixture)


if __name__ == '__main__':
    main()
