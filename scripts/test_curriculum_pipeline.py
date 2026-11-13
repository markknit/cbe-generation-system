"""Mutation tests against isolated reviewed records; no network or model calls."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from curriculum.validation import validate
from curriculum.fixtures import prepare
from curriculum_pipeline import acceptance, content_fingerprint, cached

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / 'data/codex_pilot_2026-11'
NAME = 'essmath_2_8'


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference_directory = tempfile.TemporaryDirectory(prefix='cbe-test-reference-')
        cls.reference = Path(cls.reference_directory.name)
        prepare(cls.reference)

    @classmethod
    def tearDownClass(cls):
        cls.reference_directory.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='cbe-mutation-')
        self.base = Path(self.temporary.name)
        for area in ('sources', 'manuscripts', 'materials', 'blueprints'):
            (self.base / area).mkdir()
            shutil.copyfile(self.reference / area / (NAME + '.json'), self.base / area / (NAME + '.json'))
        shutil.copyfile(self.reference / 'sources' / (NAME + '.verification.json'), self.base / 'sources' / (NAME + '.verification.json'))
        shutil.copyfile(self.reference / 'sources' / (NAME + '_source.png'), self.base / 'sources' / (NAME + '_source.png'))

    def tearDown(self):
        self.temporary.cleanup()

    def change(self, area, callback):
        path = self.base / area / (NAME + '.json')
        data = json.loads(path.read_text())
        callback(data)
        path.write_text(json.dumps(data))

    def errors(self):
        return '; '.join(validate(self.base, NAME)['errors'])

    def test_reference_passes(self):
        self.assertEqual(self.errors(), '')

    def test_missing_card_is_rejected(self):
        self.change('manuscripts', lambda d: d['lessons'][0]['materials'].append('E99'))
        self.assertIn('missing listed materials', self.errors())

    def test_missing_declared_asset_is_rejected(self):
        self.change('materials', lambda d: d['items'][0].__setitem__('assets', ['missing_figure.png']))
        self.assertIn('missing asset', self.errors())

    def test_independent_assessment_group_work_is_rejected(self):
        self.change('manuscripts', lambda d: d['lessons'][-1]['phases'][1].__setitem__(2, 'Evidence-first group work'))
        self.assertIn('collaborative strategies', self.errors())

    def test_bad_arithmetic_is_rejected(self):
        self.change('materials', lambda d: d['calculations'][0].__setitem__('expected', 1))
        self.assertIn('disagrees with expected answer', self.errors())

    def test_invalid_formula_never_executes_code(self):
        self.change('materials', lambda d: d['calculations'][0].__setitem__('expression', '__import__("os").getcwd()'))
        self.assertIn('invalid', self.errors())

    def test_phase_overrun_is_rejected(self):
        self.change('manuscripts', lambda d: d['lessons'][0]['minutes'].__setitem__(0, 99))
        self.assertIn('total 40 minutes', self.errors())

    def test_official_allocation_is_respected(self):
        self.change('sources', lambda d: d.__setitem__('official_lesson_allocation', 12))
        self.assertIn('official lesson allocation differs', self.errors())

    def test_source_drift_is_rejected(self):
        self.change('manuscripts', lambda d: d['unit'].__setitem__('values', 'Invented source wording'))
        self.assertIn('verbatim source values differs', self.errors())

    def test_changed_source_invalidates_verification(self):
        self.change('sources', lambda d: d.__setitem__('values', 'Changed source text'))
        self.assertIn('verification does not match', self.errors())

    def test_missing_source_pixels_are_rejected(self):
        (self.base / 'sources' / (NAME + '_source.png')).unlink()
        self.assertIn('crop missing', self.errors())

    def test_inventory_blocker_prevents_authoring(self):
        (self.base / 'inventory').mkdir()
        (self.base / 'inventory' / (NAME + '.json')).write_text(json.dumps({'source_status':'blocked_pdf_capture'}))
        self.assertIn('unresolved source', self.errors())

    def test_rubric_overclaim_is_rejected(self):
        self.change('blueprints', lambda d: d['rubric_links'][0].__setitem__('required_skills', ['unelicited_loss_comparison']))
        self.assertIn('skill absent', self.errors())

    def test_stale_review_is_rejected(self):
        target = self.base / 'reviews' / NAME;target.mkdir(parents=True)
        (target / 'content_acceptance.json').write_text(json.dumps({'content_fingerprint': 'old'}))
        with self.assertRaisesRegex(ValueError, 'stale'):
            acceptance(self.base, NAME, content_fingerprint(self.base, NAME), False)

    def test_fixture_mode_cannot_accept_modified_content(self):
        self.change('manuscripts', lambda d: d['lessons'][0].__setitem__('title', 'Changed lesson'))
        self.assertIn('unchanged reviewed pilot', '; '.join(validate(self.base, NAME, True)['errors']))

    def test_missing_or_modified_outputs_invalidate_cache(self):
        p=self.base/'artifact.txt';p.write_text('accepted')
        state={'stage':{'input':'input1','files':{'artifact.txt':hashlib.sha256(p.read_bytes()).hexdigest()}}}
        self.assertTrue(cached(state,'stage','input1',self.base))
        p.write_text('changed');self.assertFalse(cached(state,'stage','input1',self.base))
        p.unlink();self.assertFalse(cached(state,'stage','input1',self.base))

    def test_final_only_data_is_withheld_from_teaching_pack(self):
        from curriculum import compiler
        import zipfile
        self.change('blueprints', lambda d: d.__setitem__('isolate_final_materials', True))
        shutil.copyfile(self.reference/'attribution.yaml', self.base/'attribution.yaml')
        previous = compiler.BASE
        try:
            compiler.BASE = self.base
            compiler.build(NAME)
        finally:
            compiler.BASE = previous
        manuscript=json.loads((self.base/'manuscripts'/f'{NAME}.json').read_text())
        bank=json.loads((self.base/'materials'/f'{NAME}.json').read_text())
        final_id=manuscript['lessons'][-1]['materials'][0]
        title=next(c['title'] for c in bank['items'] if c['id']==final_id)
        def body(suffix):
            path=next((self.base/'outputs').rglob(manuscript['prefix']+'_'+suffix+'.docx'))
            with zipfile.ZipFile(path) as archive:
                return archive.read('word/document.xml').decode()
        self.assertNotIn(title, body('StudentMaterials'))
        self.assertIn(title, body('AssessmentMaterials'))
        self.assertIn(title, body('MaterialsTeacherKey'))

    def test_resource_curation_is_scoped_and_final_stays_independent(self):
        from curriculum.resource_policy import exclusion_reason
        policy={'module_allowed_titles': {'gensci_1_1': []}, 'excluded_title_phrases':['carboxylic acid naming']}
        self.assertIsNotNone(exclusion_reason(policy,'gensci_1_1','Power series intro'))
        self.assertIsNone(exclusion_reason(policy,'coremath_2_6','Area of a sector'))
        self.assertIsNotNone(exclusion_reason(policy,'coremath_2_6','Area of a sector',True))
        self.assertIsNotNone(exclusion_reason(policy,'gensci_2_4','Carboxylic acid naming'))


if __name__ == '__main__':
    unittest.main()
