"""Read-only checksum/coverage verification; does not rerender or accept content."""
import collections
import datetime
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.path.insert(0, 'scripts')
from curriculum_pipeline import content_fingerprint

base = Path('data/curriculum_expansion_2026-11')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
errors, archives, covered = [], [], {}
for receipt_path in sorted((base / 'evidence').glob('*_package.json')):
    receipt = load(receipt_path)
    path = base / receipt['archive']
    row = {'archive': path.name, 'sha256': sha(path), 'manifest_entries_verified': 0, 'modules': []}
    if row['sha256'] != receipt['sha256']:
        errors.append(f'{path.name}: receipt SHA mismatch')
    with zipfile.ZipFile(path) as bundle:
        names = bundle.namelist()
        if len(set(names)) != len(names) or bundle.testzip() is not None:
            errors.append(f'{path.name}: duplicate member or ZIP corruption')
        manifests = []
        for name in names:
            if not name.startswith('evidence/') or not name.endswith('manifest.json'):
                continue
            data = json.loads(bundle.read(name))
            if isinstance(data.get('files'), list) and ('units' in data or 'module' in data):
                manifests.append((name, data))
        if len(manifests) != 1:
            errors.append(f'{path.name}: expected one delivery manifest, got {len(manifests)}')
            continue
        manifest_name, manifest = manifests[0]
        listed = [item['path'] for item in manifest['files']]
        if len(set(listed)) != len(listed) or set(listed) != set(names) - {manifest_name}:
            errors.append(f'{path.name}: manifest must uniquely cover every member except itself')
        for item in manifest['files']:
            if item['path'] not in names or hashlib.sha256(bundle.read(item['path'])).hexdigest() != item['sha256']:
                errors.append(f'{path.name}: member SHA mismatch: {item["path"]}')
            row['manifest_entries_verified'] += 1
            if item['path'].startswith('reviews/'):
                live = base / item['path']
                if not live.is_file() or sha(live) != item['sha256']:
                    errors.append(f'{path.name}: archived review file changed: {item["path"]}')
        units = manifest.get('units', [manifest])
        for unit in units:
            module = unit['module']
            manuscript = load(base / 'manuscripts' / (module + '.json'))
            prefix = manuscript['prefix']
            acceptance = load(base / 'reviews' / module / 'content_acceptance.json')
            current = content_fingerprint(base, module)
            if acceptance['verdict'] != 'accepted' or acceptance.get('unresolved_confirmed_errors', 1) != 0:
                errors.append(f'{module}: no accepted content verdict')
            if acceptance['content_fingerprint'] != current or unit['content_fingerprint'] != current:
                errors.append(f'{module}: current/accepted/packaged fingerprint mismatch')
            if not acceptance.get('evidence'):
                errors.append(f'{module}: missing content review evidence')
            for evidence in acceptance.get('evidence', []):
                if sha(evidence['path']) != evidence['sha256']:
                    errors.append(f'{module}: content report hash changed: {evidence["path"]}')
            # Recompute the archived fingerprint from actual canonical member bytes,
            # including any implicit legacy image and declared material assets.
            canonical = [f'{area}/{module}.json' for area in ('sources', 'blueprints', 'materials', 'manuscripts')]
            canonical.append(f'sources/{module}.verification.json')
            bank_path = f'materials/{module}.json'
            if bank_path in names:
                bank = json.loads(bundle.read(bank_path))
                for card in bank['items']:
                    implicit = f'materials/diagrams/{card["id"]}.png'
                    if implicit in names or (base / implicit).exists():
                        canonical.append(implicit)
                    canonical.extend('materials/' + asset for asset in card.get('assets', []))
            if any(name not in names for name in canonical):
                errors.append(f'{module}: missing archived fingerprint input')
            else:
                archived_fp = hashlib.sha256(json.dumps({name: hashlib.sha256(bundle.read(name)).hexdigest()
                    for name in sorted(set(canonical))}, sort_keys=True).encode()).hexdigest()
                if archived_fp != current:
                    errors.append(f'{module}: archived canonical fingerprint differs from accepted/current')
            files = [name for name in names if name.startswith('outputs/') and Path(name).name.startswith(prefix + '_')]
            counts = {suffix: sum(name.endswith(suffix) for name in files) for suffix in ('.docx', '.pdf', '_data.json')}
            if counts != {'.docx': 9, '.pdf': 9, '_data.json': 1}:
                errors.append(f'{module}: wrong delivery counts {counts}')
            types = ('CBE_LessonSequence', 'CompactTeacherGuide', 'FinalExplanation', 'FinalExplanation_TeacherKey',
                     'SummaryTable', 'StudentSummaryTable', 'StudentMaterials', 'MaterialsTeacherKey', 'AssessmentMaterials')
            expected_basenames = {prefix + '_' + typ + suffix for typ in types for suffix in ('.docx', '.pdf')}
            expected_basenames.add(prefix + '_data.json')
            if {Path(name).name for name in files} != expected_basenames or len(files) != 19:
                errors.append(f'{module}: exact delivery document types mismatch')
            artifact_path = base / 'reviews' / module / 'artifact_acceptance.json'
            artifact_mode = 'legacy_frozen_manifest_and_review_hashes'
            if artifact_path.exists():
                artifact_mode = 'explicit_artifact_acceptance'
                ar = load(artifact_path)
                if ar.get('verdict') != 'accepted' or ar.get('content_fingerprint') != current:
                    errors.append(f'{module}: artifact acceptance verdict/fingerprint mismatch')
                ar_files = [item['path'] for item in ar.get('artifacts', [])]
                if len(set(ar_files)) != len(ar_files) or set(ar_files) != set(files):
                    errors.append(f'{module}: artifact acceptance coverage mismatch')
                for item in ar.get('artifacts', []):
                    live = base / item['path']
                    if not live.is_file() or sha(live) != item['sha256']:
                        errors.append(f'{module}: artifact acceptance SHA mismatch: {item["path"]}')
                if not ar.get('evidence'):
                    errors.append(f'{module}: missing artifact review evidence')
                for evidence in ar.get('evidence', []):
                    live = Path(evidence['path'])
                    if not live.is_file() or sha(live) != evidence['sha256']:
                        errors.append(f'{module}: artifact report hash changed: {evidence["path"]}')
            elif unit.get('artifact_verdict') != 'scoped_review_pass':
                errors.append(f'{module}: no accepted frozen artifact verdict')
            for name in files:
                if name.endswith(('.docx', '.pdf', '_data.json')):
                    current_path = base / name
                    if not current_path.is_file() or sha(current_path) != hashlib.sha256(bundle.read(name)).hexdigest():
                        errors.append(f'{module}: current artifact differs from frozen archive: {name}')
            entry = {'archive': path.name, 'lessons': len(manuscript['lessons']), 'fingerprint': current, 'counts': counts, 'artifact_acceptance_mode': artifact_mode}
            if module in covered:
                errors.append(f'{module}: duplicate archive coverage')
            covered[module] = entry
            row['modules'].append(module)
    archives.append(row)

authored = {p.stem for p in (base / 'manuscripts').glob('*.json')}
if authored != set(covered):
    errors.append('Authored/package coverage mismatch: ' + str(sorted(authored ^ set(covered))))
subject_totals = collections.defaultdict(lambda: {'units': 0, 'lessons': 0})
for module, entry in covered.items():
    subject = load(base / 'manuscripts' / (module + '.json'))['subject']
    subject_totals[subject]['units'] += 1
    subject_totals[subject]['lessons'] += entry['lessons']
progress = load(base / 'inventory/progress.json')
blocked = [u['module'] for u in progress['units'] if u.get('source_status') == 'blocked_pdf_capture']
result = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'scope': 'Frozen archive checksums, current artifacts/content fingerprints and delivery coverage only. Does not repeat independent semantic/layout or classroom review.',
          'archives': archives, 'modules': covered, 'expansion_units': len(covered),
          'expansion_lessons': sum(x['lessons'] for x in covered.values()),
          'by_subject_expansion_only': dict(subject_totals), 'blocked_source_modules': blocked, 'errors': errors}
target = base / 'evidence/checkpoint_integrity_2026-11-14.json'
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ('expansion_units', 'expansion_lessons', 'by_subject_expansion_only', 'blocked_source_modules', 'errors')}, indent=2))
sys.exit(bool(errors))
