#!/usr/bin/env python3
"""Create exact-pixel source packs and a readiness inventory, without authoring.

Crops/located evidence are distinct from accepted verbatim transcriptions.
No old lesson prose is used as a requirement source.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/curriculum_expansion_2026-11'
PILOTS = {'gensci_2_4', 'essmath_2_8', 'coremath_2_5'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-render-dir', type=Path, help='Reuse the exact 150dpi cbe-prep-<subject>.png renders from this preparation run')
    args = parser.parse_args()
    config = json.loads((ROOT / 'config/curriculum_source_sections.json').read_text())
    units = json.loads((BASE / 'inventory/baseline_units.json').read_text())
    rows = []
    with tempfile.TemporaryDirectory(prefix='cbe-source-render-') as temporary:
        for code, spec in config['subjects'].items():
            pdf = ROOT / spec['pdf']
            image_path = (args.reuse_render_dir / ('cbe-prep-' + code + '.png')) if args.reuse_render_dir else Path(temporary) / (code + '.png')
            if not args.reuse_render_dir:
                subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-r', str(config['render_dpi']), '-singlefile', '-png', str(pdf), str(image_path.with_suffix(''))], check=True, capture_output=True)
            image = Image.open(image_path)
            if image.width != config['pixel_width']:
                raise ValueError('Unexpected source-render geometry')
            lines = json.loads((BASE / 'inventory' / (code + '_ocr_lines.json')).read_text())
            for unit in sorted((u for u in units if u['module'].startswith(code + '_')), key=lambda u: u['module']):
                suffix = unit['module'].removeprefix(code + '_')
                record = {**unit, 'pdf': spec['pdf'], 'pdf_sha256': sha(pdf), 'physical_pdf_page': 1,
                          'official_lesson_allocation': None, 'allocation_status': 'Not inferred from baseline; decide against verified curriculum requirements.',
                          'reviewed_pilot': unit['module'] in PILOTS, 'new_lesson_count': None}
                if suffix not in spec['sections']:
                    record.update(source_status='blocked_pdf_capture', authoring_ready=False,
                                  blocker='Current Core PDF repeats contents-page material in the requirements region; older OCR cannot establish current-source fidelity.',
                                  replacement_needed='Readable authoritative requirements and competency/value/PCI pages for this unit.')
                else:
                    start, end = spec['sections'][suffix]
                    crop = BASE / 'sources' / (unit['module'] + '_source.png')
                    image.crop((0, start, image.width, end)).save(crop)
                    text = '\n'.join(r['text'] for r in lines if start <= r['y'] < end)
                    ocr = BASE / 'sources' / (unit['module'] + '_ocr.txt')
                    ocr.write_text('# OCR CANDIDATE — pixels are authority; not an accepted verbatim transcription.\n' + text + '\n')
                    record.update(source_status='located_requires_transcription_check', authoring_ready=False,
                                  crop=str(crop.relative_to(BASE)), crop_sha256=sha(crop),
                                  crop_pixels=[0, start, image.width, end], render_dpi=config['render_dpi'],
                                  ocr=str(ocr.relative_to(BASE)), ocr_sha256=sha(ocr),
                                  next_action='Visually verify the full requirements and exact transcription before source acceptance. Compiler requires a matching verification record.')
                    if unit['module'] in PILOTS:
                        record.update(source_status='reviewed_pilot', next_action='Keep the reviewed pilot and its recheck; no re-authoring.')
                    else:
                        source_path = BASE / 'sources' / (unit['module'] + '.json')
                        verification_path = BASE / 'sources' / (unit['module'] + '.verification.json')
                        if source_path.is_file() and verification_path.is_file():
                            source = json.loads(source_path.read_text())
                            verified = json.loads(verification_path.read_text())
                            evidence = ROOT / verified.get('evidence', '')
                            if (verified.get('status') == 'verified'
                                    and verified.get('source_record_sha256') == sha(source_path)
                                    and verified.get('crop_sha256') == sha(crop)
                                    and source.get('pdf_sha256') == sha(pdf)
                                    and evidence.is_file()
                                    and verified.get('evidence_sha256') == sha(evidence)):
                                record.update(source_status='verified', authoring_ready=True,
                                              official_lesson_allocation=source.get('official_lesson_allocation'),
                                              allocation_status='Read from verified source; null means not stated in this table.',
                                              next_action='Prepare materials/solutions and blueprint; independent content review remains mandatory.')
                    if unit['module'] == 'essmath_3_2':
                        record['source_identifier_note'] = 'Requirements table prints 4.2 Probability I; existing internal inventory uses3.2. Preserve this discrepancy for verification, not an automatic rename.'
                out = BASE / 'inventory' / (unit['module'] + '.json')
                out.write_text(json.dumps(record, indent=2) + '\n')
                rows.append(record)
    summary = {'units_total': len(rows), 'reviewed_pilot_units': sum(r['reviewed_pilot'] for r in rows),
               'remaining_units': sum(not r['reviewed_pilot'] for r in rows),
               'remaining_with_located_pixel_packs': sum(not r['reviewed_pilot'] and r['source_status'] != 'blocked_pdf_capture' for r in rows),
               'remaining_verified_source_packs': sum(not r['reviewed_pilot'] and r['source_status'] == 'verified' for r in rows),
               'remaining_blocked_current_pdf': [r['module'] for r in rows if r['source_status'] == 'blocked_pdf_capture'],
               'readiness_limit': 'Located pixel packs and OCR candidates are not accepted verbatim transcriptions; final source acceptance is mandatory before authoring/build.',
               'units': rows}
    (BASE / 'inventory/source_inventory.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'units'}, indent=2))


if __name__ == '__main__':
    main()
