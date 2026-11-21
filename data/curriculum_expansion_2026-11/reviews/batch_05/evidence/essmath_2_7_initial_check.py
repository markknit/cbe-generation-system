"""Read-only independent sector geometry / actual draft propagation binding."""
from pathlib import Path
import json,hashlib,zipfile,re,math,xml.etree.ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'data/curriculum_expansion_2026-11';E=Path(__file__).resolve().parent
M=json.loads((B/'materials/essmath_2_7.json').read_text());N=json.loads((B/'manuscripts/essmath_2_7.json').read_text());S=json.loads((B/'sources/essmath_2_7.json').read_text());V=json.loads((B/'sources/essmath_2_7.verification.json').read_text());W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
D=B/'outputs/v2/Essential_Mathematics/SS2.7_Volume_and_Capacity';T={};X={};XML={};checks=[];docs={}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ck(label,value):checks.append({'check':label,'pass':bool(value)})
norm=lambda s:re.sub(r'\s+','',s)
for p in sorted(D.glob('*.docx')):
 k=p.stem.removeprefix(N['prefix']+'_')
 with zipfile.ZipFile(p) as z:
  x=ET.fromstring(z.read('word/document.xml'));X[k]=x;T[k]='\n'.join(''.join(t.text or '' for t in q.findall('.//w:t',W)) for q in x.findall('.//w:p',W));XML[k]=' '.join(z.read(n).decode() for n in z.namelist() if n.startswith('word/') and n.endswith('.xml'))
  media={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
  extents=[{a:int(v) for a,v in e.attrib.items()} for e in x.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')]
  docs[k]={'path':str(p.relative_to(ROOT)),'sha256':sha(p),'embedded_media':media,'image_extents':extents}
  (E/f'essmath_2_7_{k}_review_text.txt').write_text(T[k])
ck('actualfivecompanions',len(T)==5)
for c in M['items']:
 for key in ['student','teacher']:ck(c['id']+'key'+key,norm(c[key]) in norm(T['MaterialsTeacherKey']))
 ck(c['id']+'studentpropagation',norm(c['student']) in norm(T['AssessmentMaterials' if c['id']=='VC12' else 'StudentMaterials']))
for l in N['lessons']:
 for key in ['title','purpose','knowledge','safety','reflection']:ck(f"L{l['number']}guide{key}",norm(l[key]) in norm(T['CompactTeacherGuide']))
 for i,phase in enumerate(l['phases']):
  for j,s in enumerate(phase):ck(f"L{l['number']}phase{i+1}cell{j+1}",norm(s) in norm(T['CompactTeacherGuide']))
 ck(f"L{l['number']}40min",sum(l['minutes'])==40)
for outcome in S['outcomes']:ck('guide source outcome'+outcome['id'],norm(outcome['text']) in norm(T['CompactTeacherGuide']))
ck('12designlessons',len(N['lessons'])==12)
ck('VC12absentteaching','VC12' not in T['StudentMaterials']);ck('VC12presentassessment','VC12' in T['AssessmentMaterials'])
ck('assessmentonlyVC12',not any(re.search(r'\bCP'+str(i)+r'\b',T['AssessmentMaterials']) for i in range(1,12)))
ck('noteachersolutionsassessment',all(norm(c['teacher']) not in norm(T['AssessmentMaterials']) for c in M['items']))
ck('finaldatasetabsentguide',norm(M['items'][-1]['student']) not in norm(T['CompactTeacherGuide']))
ck('finalanswerabsentteaching',norm(M['items'][-1]['teacher']) not in norm(T['StudentMaterials']))
rows=X['StudentSummaryTable'].findall('.//w:tr',W);ck('summary12rows',len(rows)==13)
for i,r in enumerate(rows[1:],1):
 cs=r.findall('w:tc',W);ck(f'summary{i}threeblank',len(cs)==4 and all(not ''.join(t.text or '' for t in c.findall('.//w:t',W)).strip() for c in cs[1:]))
for k,s in XML.items():
 for word in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']:ck(k+'attribution'+word,word in s)
# Independent model geometry from similarity and parent-solid subtraction;
# do not evaluate registered expressions.
cone=lambda r,h:math.pi*r*r*h/3
pyramid=lambda A,h:A*h/3
def conefrustum(R,r,h):
 ratio=r/R;H=h/(1-ratio);small=H-h
 return cone(R,H)-cone(r,small)
def pyramidfrustum(A,a,h):
 ratio=math.sqrt(a/A);H=h/(1-ratio);small=H-h
 return pyramid(A,H)-pyramid(a,small)
cf=conefrustum(5,3,4);cfpractice=conefrustum(5,3,12);pf=pyramidfrustum(16,4,3);rf=pyramidfrustum(24,6,5);cm=conefrustum(3,1.5,2);csmall=conefrustum(1.5,.75,1);psmall=pyramidfrustum(4,1,1.5);finalB=conefrustum(4,2,3);finalC=pyramidfrustum(25,9,6)
computed=[2500/1000,.002*1000,cone(3,4),math.pi*9*4,pyramid(16,3),pyramid(48,5),cf,cfpractice,pf,rf,cone(1.5,2),pyramid(4,1.5),cm,csmall,psmall,.9*cfpractice,.9*cfpractice/100,cone(3,6),pyramid(36,5),finalB,finalC,.8*finalB,.8*finalB/50]
ck('23registrylength',len(computed)==len(M['calculations'])==23)
for c,value in zip(M['calculations'],computed):ck('independentregistry'+c['id'],abs(value-c['expected'])<1e-9)
ck('litres075to750cm3',.75*1000==750);ck('m3cubedconversion',100**3==1000000);ck('m3to1000L',100**3/1000==1000)
ck('matchedconeone3ratio',abs(cone(3,4)/(math.pi*9*4)-1/3)<1e-12)
ck('cone345slant',math.hypot(3,4)==5);ck('conesector216',360*3/5==216)
ck('conesectorarc',abs(math.radians(216)*5-2*math.pi*3)<1e-12)
ck('halfconearc',abs(math.radians(216)*2.5-2*math.pi*1.5)<1e-12)
ck('pyramidfaceheight',abs(math.hypot(3,2)-math.sqrt(13))<1e-12);ck('pyramidedge',abs(math.sqrt(3**2+2**2+2**2)-math.sqrt(17))<1e-12)
ck('conefrustumslant',math.hypot(2,3-1.5)==2.5)
ck('annulusouterradius',2.5*3/(3-1.5)==5);ck('annulusinnerradius',5-2.5==2.5)
ck('annulusouterarc',abs(math.radians(216)*5-2*math.pi*3)<1e-12);ck('annulusinnerarc',abs(math.radians(216)*2.5-2*math.pi*1.5)<1e-12)
ck('pyramidfrustumface',abs(math.hypot(3,(4-2)/2)-math.sqrt(10))<1e-12);ck('pyramidfrustumcorner',abs(math.sqrt(3**2+2*((4-2)/2)**2)-math.sqrt(11))<1e-12)
ck('conecubicscale',abs(cone(1.5,2)/cone(3,4)-1/8)<1e-12);ck('pyramidcubicscale',pyramid(4,1.5)/pyramid(16,3)==1/8)
ck('cfmodelcubicscale',abs(csmall/cm-1/8)<1e-12);ck('pfmodelcubicscale',psmall/pf==1/8)
ck('squareparents6and3',abs(pyramid(16,6)-pyramid(4,3)-28)<1e-12)
ck('rectparents10and5',abs(pyramid(24,10)-pyramid(6,5)-70)<1e-12)
ck('finaltiming',N['lessons'][-1]['minutes']==[4,12,16,4,4])
for k in docs:ck(k+'noembeddedmedia',docs[k]['embedded_media']=={})
paths=[B/p/'essmath_2_7.json' for p in ['sources','blueprints','materials','manuscripts']]+[B/'sources/essmath_2_7.verification.json']
hashes={str(p.relative_to(B)):sha(p) for p in sorted(set(paths))}
fp=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
sourcepaths=[ROOT/'CBE_Curriculums/Grade 10/STEM/Essential Mathematics Grade 10 - July 2025.pdf',B/'sources/essmath_2_7_source.png',ROOT/V['evidence']]
sh={str(p.relative_to(ROOT)):sha(p) for p in sourcepaths}
sourcechecks={'pdf':sha(sourcepaths[0])==S.get('source_pdf_sha256',S.get('pdf_sha256')),'source_record':sha(B/'sources/essmath_2_7.json')==V['source_record_sha256'],'crop':sha(sourcepaths[1])==V['crop_sha256'],'evidence':sha(sourcepaths[2])==V['evidence_sha256']}
# source PDF hash may be nested in record; record exact actual digest regardless.
binding={'content_fingerprint':fp,'canonical_hashes':hashes,'source_related_hashes':sh,'source_binding_checks':sourcechecks,'draft_documents':docs}
(E/'essmath_2_7_review_binding.json').write_text(json.dumps(binding,indent=2)+'\n')
res={'passed':sum(x['pass'] for x in checks),'total':len(checks),'failed':[x for x in checks if not x['pass']],'checks':checks,'independent_models':{'cone_frustum_parent_difference':cf,'pyramid_frustum_parent_difference':pf,'registry_values':dict(zip([c['id'] for c in M['calculations']],computed))},'note':'Independent similar-parent subtraction, full cone/pyramid formulas and Pythagorean net checks; actual measurement/model/documentation tasks have no universal numerical answer.'}
(E/'essmath_2_7_initial_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'fingerprint':fp,'passed':res['passed'],'total':res['total'],'failed':res['failed'],'sourcechecks':sourcechecks,'docs':docs,'source_schema':list(S)},indent=2))
