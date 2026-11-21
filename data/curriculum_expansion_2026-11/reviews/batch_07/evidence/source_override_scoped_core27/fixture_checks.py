"""Selected preparation against temporary 43-unit inventories, never production."""
from pathlib import Path
import contextlib,copy,hashlib,io,json,subprocess,sys,tempfile
from unittest.mock import patch
from PIL import Image
R=Path(__file__).resolve().parents[6];E=Path(__file__).parent;src=(R/'scripts/prepare_curriculum_sources.py').read_text();(E/'reviewed_prepare.py').write_text(src)
sys.path.insert(0,str(R/'scripts'));from curriculum_pipeline import content_fingerprint
units=json.loads((R/'data/curriculum_expansion_2026-11/inventory/baseline_units.json').read_text());selected={'coremath_1_1','coremath_1_2','coremath_1_3','coremath_2_1','coremath_2_2','coremath_2_3','coremath_2_4'};pilots={'gensci_2_4','essmath_2_8','coremath_2_5'};h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();results=[]
for case in ['selected_fresh','selected_reuse','unknown_module','missing_preserved_inventory','missing_selected_inventory']:
 with tempfile.TemporaryDirectory(prefix='selected_sources_review_') as tmp:
  root=Path(tmp);b=root/'data/curriculum_expansion_2026-11'
  def put(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=1)+'\n')
  for d in ['inventory','sources','materials','blueprints','manuscripts']:(b/d).mkdir(parents=True,exist_ok=True)
  Image.new('RGB',(80,200),'blue').save(root/'old.pdf','PDF',resolution=72);Image.new('RGB',(80,200),'red').save(root/'new.pdf','PDF',resolution=72)
  config={'render_dpi':72,'pixel_width':80,'subjects':{c:{'pdf':'old.pdf','sections':{}} for c in ['coremath','essmath','gensci']},'source_overrides':{m:{'pdf':'new.pdf','section':[80,140],'ocr_lines':'data/curriculum_expansion_2026-11/inventory/new_ocr.json'} for m in selected}}
  put(root/'config/curriculum_source_sections.json',config);put(b/'inventory/baseline_units.json',units)
  for c in config['subjects']:put(b/f'inventory/{c}_ocr_lines.json',[])
  put(b/'inventory/new_ocr.json',[{'y':80,'text':'new replacement'}])
  originals={}
  for i,u in enumerate(units):
   m=u['module'];row={**u,'reviewed_pilot':m in pilots,'source_status':'blocked_pdf_capture' if m in selected else ('reviewed_pilot' if m in pilots else 'verified'),'new_lesson_count':i+10,'official_lesson_allocation':i+20,'allocation_status':'custom accepted allocation prose','next_action':'custom final-reviewed next action','authoring_ready':m not in selected,'custom_nested':{'preserve':['exact',i]}}
   originals[m]=copy.deepcopy(row);put(b/f'inventory/{m}.json',row)
   for area,d in [('sources',{'accepted_source':'immutable'}),('materials',{'items':[]}),('blueprints',{'accepted':'immutable'}),('manuscripts',{'accepted':'immutable'})]:put(b/f'{area}/{m}.json',d)
   put(b/f'sources/{m}.verification.json',{'status':'not_attempted_fixture'});(b/f'sources/{m}_source.png').write_bytes(b'frozen crop');(b/f'sources/{m}_ocr.txt').write_bytes(b'frozen OCR')
  put(b/'inventory/source_inventory.json',{'previous':'must stay on validation failure'})
  argv=['fixture','--modules',*sorted(selected)]
  if case=='unknown_module':argv+=['not_a_real_module']
  if case=='missing_preserved_inventory':(b/'inventory/gensci_1_1.json').unlink()
  if case=='missing_selected_inventory':(b/'inventory/coremath_1_1.json').unlink()
  if case=='selected_reuse':
   (root/'reuse').mkdir()
   for c in config['subjects']:subprocess.run(['pdftoppm','-f','1','-l','1','-r','72','-singlefile','-png',str(root/'old.pdf'),str(root/f'reuse/cbe-prep-{c}')],check=True,capture_output=True)
   argv+=['--reuse-render-dir',str(root/'reuse')]
  before={str(p.relative_to(root)):h(p) for p in root.rglob('*') if p.is_file()};fps={m:content_fingerprint(b,m) for m in originals if m not in selected};calls=[];actual=subprocess.run;ns={'__name__':'fixture_module','__file__':str(root/'scripts/prepare_curriculum_sources.py')};exec(compile(src,'fixture','exec'),ns)
  def track(cmd,*a,**kw):calls.append(cmd);return actual(cmd,*a,**kw)
  exit_code=0;stderr=io.StringIO()
  with patch.object(sys,'argv',argv),patch.object(ns['subprocess'],'run',side_effect=track),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(stderr):
   try:ns['main']()
   except SystemExit as x:exit_code=x.code
  after={str(p.relative_to(root)):h(p) for p in root.rglob('*') if p.is_file()};c={}
  if case in ['unknown_module','missing_preserved_inventory']:
   c['exit2_before_mutation']=exit_code==2 and before==after;c['no_renderer_calls']=len(calls)==0;c['specific_error']='Unknown module IDs' in stderr.getvalue() if case=='unknown_module' else 'Missing preserved inventory: gensci_1_1' in stderr.getvalue()
  else:
   c['success']=exit_code==0
   unselected=[m for m in originals if m not in selected];c['all36_inventories_byte_exact']=all(before[str((b/f'inventory/{m}.json').relative_to(root))]==h(b/f'inventory/{m}.json') for m in unselected)
   c['all36_crops_ocr_byte_exact']=all(before[str((b/f'sources/{m}{s}').relative_to(root))]==h(b/f'sources/{m}{s}') for m in unselected for s in ['_source.png','_ocr.txt'])
   c['all43_canonical_records_byte_exact']=all(before[str((b/f'{a}/{m}.json').relative_to(root))]==h(b/f'{a}/{m}.json') for m in originals for a in ['sources','materials','blueprints','manuscripts'])
   c['all36_fingerprints_unchanged']=all(content_fingerprint(b,m)==v for m,v in fps.items())
   summary=json.loads((b/'inventory/source_inventory.json').read_text());rows={r['module']:r for r in summary['units']}
   c['aggregate43unique']=summary['units_total']==43 and len(summary['units'])==43 and len(rows)==43 and set(rows)==set(originals)
   c['aggregate36_preserved_custom_rows']=all(rows[m]==originals[m] for m in unselected)
   c['aggregate7_refreshed_unaccepted']=all(rows[m]['pdf']=='new.pdf' and rows[m]['source_status']=='located_requires_transcription_check' and not rows[m]['authoring_ready'] for m in selected)
   c['aggregate_totals']=summary['reviewed_pilot_units']==3 and summary['remaining_units']==40 and summary['remaining_with_located_pixel_packs']==40 and summary['remaining_verified_source_packs']==33 and summary['remaining_blocked_current_pdf']==[]
   c['replacement_cached']=sum(str(root/'new.pdf') in cmd for cmd in calls)==1
   c['render_count']=len(calls)==(1 if case=='selected_reuse' else 4)
  results.append({'case':case,'checks':c,'pass':all(c.values()),'stderr':stderr.getvalue()})
(E/'fixture_results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
