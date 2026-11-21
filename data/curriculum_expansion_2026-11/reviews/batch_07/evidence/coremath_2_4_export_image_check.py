from pathlib import Path
import json,hashlib,zipfile,subprocess,xml.etree.ElementTree as E
from PIL import Image
B=Path('data/curriculum_expansion_2026-11');V=B/'reviews/batch_07/evidence';O=B/'outputs/v2/Core_Mathematics/SS2.4_Trigonometry_1';P=B/'outputs/PDF';D=json.loads((B/'manuscripts/coremath_2_4.json').read_text());S=json.loads((B/'sources/coremath_2_4.json').read_text());M=json.loads((B/'materials/coremath_2_4.json').read_text());X=json.loads((O/(D['prefix']+'_data.json')).read_text());A=json.loads((V/'coremath_2_4_artifact_review_check.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
def ck(label,val):rows.append({'field':label,'pass':bool(val)})
for k,v in D['unit'].items():
 if k not in ['keyInquiryQuestions','teacherConfirmationRequired']:ck('UNIT.'+k,X['UNIT'][k]==v)
ck('UNIT.source_outcomes',X['UNIT']['learningOutcomes']=='\n'.join(o['text'] for o in S['outcomes']))
ck('lesson_count',len(X['LESSONS'])==len(D['lessons'])==15)
for l,out in zip(D['lessons'],X['LESSONS']):
 pre='L'+str(l['number'])+'.';ck(pre+'number/title',(l['number'],l['title'])==(out['number'],out['title']))
 for k,t in {'purpose':'purpose','knowledge':'knowledge','skills':'skills','attitudes':'attitudes','inquiry':'keyInquiry','story':'purposeInStoryline','safety':'safetyNotes'}.items():ck(pre+k,out['slo'][t]==l[k])
 ck(pre+'reflection',out['teacherReflection']==l['reflection'])
 for i,(p,o) in enumerate(zip(l['phases'],out['framework'])):
  for j,k in enumerate(['learnerExperience','teacherMoves','sensemakingStrategy','formativeAssessment']):ck(pre+f'phase{i}.{k}',o[k]==(str(l['minutes'][i])+' minutes. '+p[j] if j==1 else p[j]))
 ck(pre+'summary',X['SUMMARY_TABLE']['lessons'][l['number']-1]=={'number':l['number'],'title':l['title'],**l['summary']})
expected_assessment={**D['assessment'],'sections':[{k:v for k,v in s.items() if k!='marks'} for s in D['assessment']['sections']]}
ck('FINAL_EXPLANATION',X['FINAL_EXPLANATION']==expected_assessment)
selected=[(l['number'],p,k,v[k]) for l in X['LESSONS'] for p,v in l['resourceLinks'].items() for k in ['video','reading'] if v[k] is not None]
ck('selected_resources_empty',selected==[])
policy=V/'coremath_2_4_resource_policy_review_snapshot.json';ck('snapshot_module_allowlist_empty',json.loads(policy.read_text())['module_allowed_titles']['coremath_2_4']==[])
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','a':'http://schemas.openxmlformats.org/drawingml/2006/main','pic':'http://schemas.openxmlformats.org/drawingml/2006/picture','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
assets={sha(B/'materials'/c['diagram']):B/'materials'/c['diagram'] for c in M['items'] if 'diagram' in c};media={};aspect=[];pdfimages={}
for typ in A['artifact_hashes']:
 with zipfile.ZipFile(O/(D['prefix']+'_'+typ+'.docx')) as z:
  r=E.fromstring(z.read('word/document.xml'));rels={x.attrib['Id']:x.attrib['Target'] for x in E.fromstring(z.read('word/_rels/document.xml.rels'))};media[typ]={q:hashlib.sha256(z.read(q)).hexdigest() for q in z.namelist() if q.startswith('word/media/')}
  for inline in r.findall('.//wp:inline',N):
   blip=inline.find('.//a:blip',N)
   if blip is None:continue
   h=hashlib.sha256(z.read('word/'+rels[blip.attrib['{'+N['r']+'}embed']])).hexdigest();ck(typ+'.embedded_original_known',h in assets)
   w,hh=Image.open(assets[h]).size;crop=inline.find('.//a:srcRect',N);c={k:int(crop.get(k,'0'))/100000 if crop is not None else 0 for k in ['l','r','t','b']};ext=inline.find('wp:extent',N);ratio=int(ext.get('cx'))/int(ext.get('cy'));expected=w*(1-c['l']-c['r'])/(hh*(1-c['t']-c['b']));err=abs(ratio/expected-1);aspect.append({'document':typ,'image':assets[h].name,'relative_aspect_error':err,'pass':err<0.001})
 pdfimages[typ]=subprocess.check_output(['pdfimages','-list',str(P/(D['prefix']+'_'+typ+'.pdf'))],text=True)
 for line in pdfimages[typ].splitlines()[2:]:
  parts=line.split()
  if len(parts)>13:
   xp,yp=float(parts[12]),float(parts[13]);ck(typ+'.pdf_image_xy_sampling',abs(xp/yp-1)<0.02)
finalcard=next(c for c in M['items'] if c['id']=='CTG15')
for typ in ['CBE_LessonSequence','CompactTeacherGuide','StudentMaterials','SummaryTable','StudentSummaryTable']:
 with zipfile.ZipFile(O/(D['prefix']+'_'+typ+'.docx')) as z:
  text=''.join(t.text or '' for t in E.fromstring(z.read('word/document.xml')).findall('.//w:t',N))
  ck(typ+'.full_final_card_data_absent',finalcard['student'] not in text)
for typ in media:ck(typ+'.no_unexpected_embedded_images',set(media[typ].values())==({sha(B/'materials/diagrams/CTG12.png')} if typ in ['StudentMaterials','MaterialsTeacherKey'] else set()))
# Explicit comparison of all 18 current files with frozen audit done in artifact_review_check.
result={'export_sha256':sha(O/(D['prefix']+'_data.json')),'resource_policy_snapshot_sha256':sha(policy),'checks':rows,'total':len(rows),'pass':sum(r['pass'] for r in rows),'aspect_checks':aspect,'media_sha256':media,'pdfimages_inventory':pdfimages,'selected_resources':selected}
(V/'coremath_2_4_export_image_check.json').write_text(json.dumps(result,indent=2)+'\n');print('checks',len(rows),'pass',result['pass'],'aspect',len(aspect),'pass',sum(a['pass'] for a in aspect));print('FAILURES',[r for r in rows if not r['pass']])
if not all(r['pass'] for r in rows) or not all(a['pass'] for a in aspect):raise SystemExit(1)
