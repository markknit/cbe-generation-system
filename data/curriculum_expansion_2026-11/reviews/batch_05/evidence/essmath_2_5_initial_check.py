"""Read-only independent sector geometry / actual draft propagation binding."""
from pathlib import Path
import json,hashlib,zipfile,re,math,xml.etree.ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'data/curriculum_expansion_2026-11';E=Path(__file__).resolve().parent
M=json.loads((B/'materials/essmath_2_5.json').read_text());N=json.loads((B/'manuscripts/essmath_2_5.json').read_text());S=json.loads((B/'sources/essmath_2_5.json').read_text());V=json.loads((B/'sources/essmath_2_5.verification.json').read_text());W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
D=B/'outputs/v2/Essential_Mathematics/SS2.5_Area_of_a_Part_of_a_Circle';T={};X={};XML={};checks=[];docs={}
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
  (E/f'essmath_2_5_{k}_review_text.txt').write_text(T[k])
ck('actualfivecompanions',len(T)==5)
for c in M['items']:
 for key in ['student','teacher']:ck(c['id']+'key'+key,norm(c[key]) in norm(T['MaterialsTeacherKey']))
 ck(c['id']+'studentpropagation',norm(c['student']) in norm(T['AssessmentMaterials' if c['id']=='CP10' else 'StudentMaterials']))
for l in N['lessons']:
 for key in ['title','purpose','knowledge','safety','reflection']:ck(f"L{l['number']}guide{key}",norm(l[key]) in norm(T['CompactTeacherGuide']))
 for i,phase in enumerate(l['phases']):
  for j,s in enumerate(phase):ck(f"L{l['number']}phase{i+1}cell{j+1}",norm(s) in norm(T['CompactTeacherGuide']))
 ck(f"L{l['number']}40min",sum(l['minutes'])==40)
for outcome in S['outcomes']:ck('guide source outcome'+outcome['id'],norm(outcome['text']) in norm(T['CompactTeacherGuide']))
ck('10designlessons',len(N['lessons'])==10)
ck('CP10absentteaching','CP10' not in T['StudentMaterials']);ck('CP10presentassessment','CP10' in T['AssessmentMaterials'])
ck('assessmentonlyCP10',not any(re.search(r'\bCP'+str(i)+r'\b',T['AssessmentMaterials']) for i in range(1,10)))
ck('noteachersolutionsassessment',all(norm(c['teacher']) not in norm(T['AssessmentMaterials']) for c in M['items']))
ck('finaldatasetabsentguide',norm(M['items'][-1]['student']) not in norm(T['CompactTeacherGuide']))
ck('finalanswerabsentteaching',norm(M['items'][-1]['teacher']) not in norm(T['StudentMaterials']))
rows=X['StudentSummaryTable'].findall('.//w:tr',W);ck('summary10rows',len(rows)==11)
for i,r in enumerate(rows[1:],1):
 cs=r.findall('w:tc',W);ck(f'summary{i}threeblank',len(cs)==4 and all(not ''.join(t.text or '' for t in c.findall('.//w:t',W)).strip() for c in cs[1:]))
for k,s in XML.items():
 for word in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']:ck(k+'attribution'+word,word in s)
# Derive all sectors from full circle fraction and triangles from chord/height;
# do not evaluate any author's expression strings. Projection coordinates also
# yield the appropriate acute central triangle directly.
def geometry(r,angle):
 t=math.radians(angle);sector=math.pi*r*r*(angle/360)
 chord=2*r*math.sin(t/2);height=r*math.cos(t/2);triangle=chord*height/2
 return {'r':r,'angle':angle,'sector':sector,'chord':chord,'height':height,'triangle':triangle,'minor':sector-triangle,'major':math.pi*r*r-(sector-triangle)}
g6=geometry(6,60);g10=geometry(10,90);gf=geometry(4,60)
computed=[math.pi*7**2/4,g6['sector'],math.pi*4**2*3/4,g6['triangle'],g6['minor'],g10['minor'],g10['major'],math.pi*.8**2/4,g6['major'],math.pi*8**2*135/360,gf['minor'],gf['major'],math.pi*1.2**2/4]
ck('13registrylength',len(computed)==len(M['calculations'])==13)
for c,value in zip(M['calculations'],computed):ck('independentregistry'+c['id'],abs(value-c['expected'])<1e-10)
for label,g in [('CP4',g6),('CP5',g10),('CP10B',gf)]:
 ck(label+'positivecap',0<g['minor']<g['sector']);ck(label+'complement',abs(g['minor']+g['major']-math.pi*g['r']**2)<1e-10)
ck('fixedanglesquaredscaling',abs(geometry(12,60)['minor']/g6['minor']-4)<1e-10)
ck('CP4equilateraltriangle',abs(g6['triangle']-9*math.sqrt(3))<1e-10)
ck('finaltiming',N['lessons'][-1]['minutes']==[4,12,16,4,4])
asset=B/'materials/diagrams/CP1.png';im=Image.open(asset)
ck('nativeCP1dimensions',im.size==(1400,700))
for k in ['StudentMaterials','MaterialsTeacherKey']:
 ck(k+'exactCP1embedded',sha(asset) in docs[k]['embedded_media'].values())
 ck(k+'CP1aspect',len(docs[k]['image_extents'])==1 and abs(docs[k]['image_extents'][0]['cx']/docs[k]['image_extents'][0]['cy']-2)<.001)
paths=[B/p/'essmath_2_5.json' for p in ['sources','blueprints','materials','manuscripts']]+[B/'sources/essmath_2_5.verification.json',asset]
hashes={str(p.relative_to(B)):sha(p) for p in sorted(set(paths))}
fp=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
sourcepaths=[ROOT/'CBE_Curriculums/Grade 10/STEM/Essential Mathematics Grade 10 - July 2025.pdf',B/'sources/essmath_2_5_source.png',ROOT/V['evidence']]
sh={str(p.relative_to(ROOT)):sha(p) for p in sourcepaths}
sourcechecks={'pdf':sha(sourcepaths[0])==S.get('source_pdf_sha256',S.get('pdf_sha256')),'source_record':sha(B/'sources/essmath_2_5.json')==V['source_record_sha256'],'crop':sha(sourcepaths[1])==V['crop_sha256'],'evidence':sha(sourcepaths[2])==V['evidence_sha256']}
# source PDF hash may be nested in record; record exact actual digest regardless.
binding={'content_fingerprint':fp,'canonical_hashes':hashes,'source_related_hashes':sh,'source_binding_checks':sourcechecks,'draft_documents':docs,'native_asset':{'path':str(asset.relative_to(B)),'sha256':sha(asset),'pixels':im.size}}
(E/'essmath_2_5_review_binding.json').write_text(json.dumps(binding,indent=2)+'\n')
res={'passed':sum(x['pass'] for x in checks),'total':len(checks),'failed':[x for x in checks if not x['pass']],'checks':checks,'independent_models':{'CP4':g6,'CP5':g10,'CP10B':gf,'registry_values':dict(zip([c['id'] for c in M['calculations']],computed))},'note':'Independent full-circle fractions and chord/height triangles; actual CP3/CP6 measurement/model tasks have no universal numeric answer.'}
(E/'essmath_2_5_initial_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'fingerprint':fp,'passed':res['passed'],'total':res['total'],'failed':res['failed'],'sourcechecks':sourcechecks,'docs':docs,'source_schema':list(S)},indent=2))
