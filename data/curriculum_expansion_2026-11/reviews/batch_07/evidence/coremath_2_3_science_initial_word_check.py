"""Independent read-only binding and draft propagation checks; writes review evidence only."""
from pathlib import Path
import json, hashlib, re, zipfile, sys
import xml.etree.ElementTree as E
from PIL import Image
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts'))
from curriculum_pipeline import content_fingerprint
B=ROOT/'data/curriculum_expansion_2026-11'; name='coremath_2_3'
D=json.loads((B/'manuscripts'/f'{name}.json').read_text())
M=json.loads((B/'materials'/f'{name}.json').read_text())
S=json.loads((B/'sources'/f'{name}.json').read_text())
O=B/'outputs/v2/Core_Mathematics/SS2.3_Rotation'
types=['CompactTeacherGuide','StudentMaterials','MaterialsTeacherKey','StudentSummaryTable','AssessmentMaterials']
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','pic':'http://schemas.openxmlformats.org/drawingml/2006/picture','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','p':'http://schemas.openxmlformats.org/package/2006/relationships'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
norm=lambda s:re.sub(r'\s+',' ',s).strip()
trees={};texts={};hashes={};media={};frames={};attrs={}
for typ in types:
 p=O/(D['prefix']+'_'+typ+'.docx');hashes[typ]=sha(p)
 with zipfile.ZipFile(p) as z:
  root=E.fromstring(z.read('word/document.xml'));trees[typ]=root
  texts[typ]=norm('\n'.join(''.join(t.text or '' for t in x.findall('.//w:t',N)) for x in root.findall('.//w:p',N)))
  media[typ]={m:hashlib.sha256(z.read(m)).hexdigest() for m in z.namelist() if m.startswith('word/media/')}
  rels={x.attrib['Id']:x.attrib['Target'] for x in E.fromstring(z.read('word/_rels/document.xml.rels'))}
  frames[typ]=[]
  for pic in root.findall('.//pic:blipFill',N):
   blip=pic.find('a:blip',N)
   if blip is None:continue
   target='word/'+rels[blip.attrib['{'+N['r']+'}embed']]
   crop=pic.find('a:srcRect',N)
   frames[typ].append({'media_sha256':hashlib.sha256(z.read(target)).hexdigest(),'crop':crop.attrib if crop is not None else None})
  xml=' '.join(z.read(q).decode() for q in z.namelist() if q.startswith('word/') and q.endswith('.xml'))
  attrs[typ]=all(s in xml for s in ['ChatGPT/Codex','OpenAI'])
checks=[]
def ck(typ,label,t):
 exact=norm(t) in texts[typ]; compact=re.sub(r'\s+','',t) in re.sub(r'\s+','',texts[typ]);checks.append({'document':typ,'field':label,'pass':exact or compact,'match_method':'collapsed whitespace' if exact else 'nonspace characters;Word w:br boundaries omit spaces in w:t extraction'})
for l in D['lessons']:
 for k in ['title','purpose','knowledge','safety','reflection']:ck('CompactTeacherGuide',f"L{l['number']}.{k}",l[k])
 for i,p in enumerate(l['phases'],1):
  for j,t in enumerate(p,1):ck('CompactTeacherGuide',f"L{l['number']}.phase{i}.{j}",t)
for c in M['items']:
 target='AssessmentMaterials' if c['id'] in ['CRT12'] else 'StudentMaterials'
 ck(target,c['id']+'.student',c['student'])
 ck('MaterialsTeacherKey',c['id']+'.student',c['student']);ck('MaterialsTeacherKey',c['id']+'.teacher',c['teacher'])
for i,o in enumerate(S['outcomes']):
 ck('CompactTeacherGuide',f'outcome{i}',o['text'] if isinstance(o,dict) else o)
summary_rows=trees['StudentSummaryTable'].findall('.//w:tbl/w:tr',N)[1:]
blank=len(summary_rows)==12 and all(not ''.join(t.text or '' for t in c.findall('.//w:t',N)).strip() for r in summary_rows for c in r.findall('w:tc',N)[1:])
student_types=['StudentMaterials','AssessmentMaterials','StudentSummaryTable']
exemplars_absent={typ:all(norm(s['exemplar']) not in texts[typ] for s in D['assessment']['sections']) for typ in student_types}
keys_absent={typ:all(norm(c['teacher']) not in texts[typ] for c in M['items']) for typ in student_types}
final_card_text_absent=all(norm(c['student']) not in texts['StudentMaterials'] and c['title'] not in texts['StudentMaterials'] for c in M['items'] if c['id'] in ['CRT12'])
assets={}
isolation={typ:not media[typ] for typ in types}
final_present={}
reuse={}
crop_checks=[]
for typ in ['StudentMaterials','MaterialsTeacherKey','AssessmentMaterials']:
 for c in M['items']:
  if 'diagram' not in c or (typ=='StudentMaterials' and c['id'] in ['CRT12']) or (typ=='AssessmentMaterials' and c['id'] not in ['CRT12']):continue
  p=B/'materials'/c['diagram'];h=sha(p);candidates=[f for f in frames[typ] if f['media_sha256']==h]
  expected=None
  if c.get('diagram_crop'):
   w,hh=Image.open(p).size;l,t,r,b=c['diagram_crop'];expected={k:str(round(v*100000)) for k,v in {'l':l/w,'t':t/hh,'r':(w-r)/w,'b':(hh-b)/hh}.items()}
  crop_checks.append({'document':typ,'card':c['id'],'original_bytes_present':h in media[typ].values(),'expected_crop':expected,'actual':candidates,'pass':bool(candidates) and any(f['crop']==expected for f in candidates)})
canonical={str(p.relative_to(B)):sha(p) for p in [B/k/(name+'.json') for k in ['sources','materials','manuscripts','blueprints']]+[B/'sources'/(name+'.verification.json')]}
result={'scope':'Full initial content review plus five actual draft Word bindings;no rendering or final page-layout acceptance','content_fingerprint':content_fingerprint(B,name),'canonical_hashes':canonical,'source_pixel_sha256':sha(B/'sources'/(name+'_source.png')),'source_pdf_sha256':sha(ROOT/S['pdf']),'asset_hashes':assets,'draft_word_hashes':hashes,'checks':checks,'checks_total':len(checks),'checks_pass':sum(c['pass'] for c in checks),'blank_student_summary_12_rows':blank,'student_exemplars_absent':exemplars_absent,'teacher_keys_absent':keys_absent,'final_card_text_absent_teaching':final_card_text_absent,'no_unexpected_embedded_media':isolation,'media_hashes':media,'image_frame_checks':crop_checks,'attribution':attrs,'lesson_minutes':[sum(l['minutes']) for l in D['lessons']]}
# Preserve actual current Word body text for later final-artifact bridges.
for typ in types:
 with zipfile.ZipFile(O/(D['prefix']+'_'+typ+'.docx')) as z:
  root=E.fromstring(z.read('word/document.xml'))
  raw='\n'.join(''.join(t.text or '' for t in p.findall('.//w:t',N)) for p in root.findall('.//w:p',N))
  (Path(__file__).parent/('coremath_2_3_'+typ+'_science_initial_review_text.txt')).write_text(raw)

for kind in ['sources','materials','manuscripts','blueprints']:
 (Path(__file__).parent/(name+'_initial_'+kind+'_snapshot.json')).write_bytes((B/kind/(name+'.json')).read_bytes())
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','media_hashes','asset_hashes','image_frame_checks']},indent=2));print('CROP FAILURES',json.dumps([c for c in crop_checks if not c['pass']]))
if not all(c['pass'] for c in checks) or not all(c['pass'] for c in crop_checks):raise SystemExit(1)
