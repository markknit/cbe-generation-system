"""Old/current preparation code run only against temporary tiny PDF fixtures."""
from pathlib import Path
import contextlib,copy,hashlib,io,json,subprocess,sys,tempfile
from unittest.mock import patch
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[6];E=Path(__file__).parent
sys.path.insert(0,str(R/'scripts'));from curriculum_pipeline import content_fingerprint
old=subprocess.run(['git','show','HEAD:scripts/prepare_curriculum_sources.py'],cwd=R,text=True,capture_output=True,check=True).stdout
new=(R/'scripts/prepare_curriculum_sources.py').read_text()
(E/'old_prepare.py').write_text(old);(E/'reviewed_prepare.py').write_text(new)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();results=[]
for case in ['fresh','reuse','negative_start','end_beyond_image','replacement_wrong_width']:
 with tempfile.TemporaryDirectory(prefix='source_override_review_') as tmp:
  root=Path(tmp);b=root/'data/curriculum_expansion_2026-11'
  def put(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d))
  def pdf(name,color,width=80):
   im=Image.new('RGB',(width,200),color);dr=ImageDraw.Draw(im);dr.rectangle((0,80,width-1,139),fill='yellow');p=root/name;p.parent.mkdir(parents=True,exist_ok=True);im.save(p,'PDF',resolution=72)
  pdf('old.pdf','blue');pdf('new.pdf','red',81 if case=='replacement_wrong_width' else 80)
  for x in ['sources','materials','blueprints','manuscripts','inventory']:(b/x).mkdir(parents=True,exist_ok=True)
  units=[{'module':m,'subject':'Fixture','title':m} for m in ['coremath_1_1','coremath_1_2','coremath_2_6','coremath_2_7','gensci_1_1']]
  config={'render_dpi':72,'pixel_width':80,'subjects':{'coremath':{'pdf':'old.pdf','sections':{'2_6':[0,60],'2_7':[60,80]}},'gensci':{'pdf':'old.pdf','sections':{'1_1':[0,60]}}}}
  put(b/'inventory/baseline_units.json',units)
  for c in ['coremath','gensci']:put(b/f'inventory/{c}_ocr_lines.json',[{'y':0,'text':'old start'},{'y':59,'text':'old included'},{'y':60,'text':'old boundary'}])
  put(b/'inventory/new_lines.json',[{'y':79,'text':'before'},{'y':80,'text':'replacement start'},{'y':139,'text':'replacement last'},{'y':140,'text':'after'}]);put(root/'config/curriculum_source_sections.json',config)
  def run(src,reuse=False):
   ns={'__name__':'fixture_module','__file__':str(root/'scripts/prepare_curriculum_sources.py')};exec(compile(src,'fixture','exec'),ns);calls=[];actual=subprocess.run
   def tracked(cmd,*a,**kw):calls.append(cmd);return actual(cmd,*a,**kw)
   argv=['fixture']+(['--reuse-render-dir',str(root/'reuse')] if reuse else [])
   with patch.object(sys,'argv',argv),patch.object(ns['subprocess'],'run',side_effect=tracked),contextlib.redirect_stdout(io.StringIO()):ns['main']()
   return calls
  run(old)
  accepted=['coremath_2_6','coremath_2_7','gensci_1_1']
  for m in accepted:
   src={'pdf_sha256':h(root/'old.pdf'),'official_lesson_allocation':7};put(b/f'sources/{m}.json',src);ev=root/f'evidence/{m}.md';ev.parent.mkdir(exist_ok=True);ev.write_text('fixture visual acceptance')
   put(b/f'sources/{m}.verification.json',{'status':'verified','source_record_sha256':h(b/f'sources/{m}.json'),'crop_sha256':h(b/f'sources/{m}_source.png'),'evidence':str(ev.relative_to(root)),'evidence_sha256':h(ev)})
   for area,d in [('materials',{'items':[]}),('blueprints',{}),('manuscripts',{})]:put(b/f'{area}/{m}.json',d)
  run(old)
  protected=[p for area in ['sources','materials','blueprints','manuscripts'] for p in (b/area).glob('*')]+[b/f'inventory/{m}.json' for m in accepted]
  before={str(p.relative_to(b)):h(p) for p in protected};fps={m:content_fingerprint(b,m) for m in accepted}
  config['source_overrides']={m:{'pdf':'new.pdf','section':[80,140],'ocr_lines':'data/curriculum_expansion_2026-11/inventory/new_lines.json'} for m in ['coremath_1_1','coremath_1_2']}
  if case=='negative_start':config['source_overrides']['coremath_1_1']['section']=[-1,40]
  if case=='end_beyond_image':config['source_overrides']['coremath_1_1']['section']=[80,201]
  put(root/'config/curriculum_source_sections.json',config)
  if case=='reuse':
   (root/'reuse').mkdir()
   for c in ['coremath','gensci']:subprocess.run(['pdftoppm','-f','1','-l','1','-r','72','-singlefile','-png',str(root/'old.pdf'),str(root/f'reuse/cbe-prep-{c}')],check=True,capture_output=True)
  try:
   calls=run(new,case=='reuse');err=None
  except ValueError as x:calls=[];err=str(x)
  checks={}
  if case in ['fresh','reuse']:
   checks['protected_bytes_identical']=all(h(b/p)==v for p,v in before.items());checks['accepted_fingerprints_identical']=all(content_fingerprint(b,m)==v for m,v in fps.items());checks['all_accepted_remain_verified']=all(json.loads((b/f'inventory/{m}.json').read_text())['source_status']=='verified' for m in accepted)
   checks['renderer_calls_exact']=len(calls)==(1 if case=='reuse' else 3);checks['replacement_render_cached']=sum(str(root/'new.pdf') in x for x in calls)==1
   for m in ['coremath_1_1','coremath_1_2']:
    row=json.loads((b/f'inventory/{m}.json').read_text());ocr=(b/row['ocr']).read_text();im=Image.open(b/row['crop']);checks[m+'_replacement_record']=row['pdf']=='new.pdf' and row['pdf_sha256']==h(root/'new.pdf') and row['crop_pixels']==[0,80,80,140] and im.size==(80,60)
    checks[m+'_ocr_bounds_and_source']='replacement start\nreplacement last\n' in ocr and 'before' not in ocr and 'after' not in ocr and 'old start' not in ocr
    checks[m+'_not_autoaccepted']=row['source_status']=='located_requires_transcription_check' and not row['authoring_ready']
  else:checks['expected_geometry_or_bounds_rejection']=err is not None and ('geometry' in err if case=='replacement_wrong_width' else 'outside captured image' in err)
  results.append({'case':case,'checks':checks,'error':err,'pass':all(checks.values())})
(E/'fixture_results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
