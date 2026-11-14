"""Read-only independent sector geometry / actual draft propagation binding."""
from pathlib import Path
import json,hashlib,zipfile,re,math,xml.etree.ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'data/curriculum_expansion_2026-11';E=Path(__file__).resolve().parent
M=json.loads((B/'materials/essmath_3_1.json').read_text());N=json.loads((B/'manuscripts/essmath_3_1.json').read_text());S=json.loads((B/'sources/essmath_3_1.json').read_text());V=json.loads((B/'sources/essmath_3_1.verification.json').read_text());W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
D=B/'outputs/v2/Essential_Mathematics/SS3.1_Statistics_I';T={};X={};XML={};checks=[];docs={}
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
  (E/f'essmath_3_1_{k}_review_text.txt').write_text(T[k])
ck('actualfivecompanions',len(T)==5)
for c in M['items']:
 for key in ['student','teacher']:ck(c['id']+'key'+key,norm(c[key]) in norm(T['MaterialsTeacherKey']))
 ck(c['id']+'studentpropagation',norm(c['student']) in norm(T['AssessmentMaterials' if c['id'] in {'ES11','ES12','ES13','ES14'} else 'StudentMaterials']))
for l in N['lessons']:
 for key in ['title','purpose','knowledge','safety','reflection']:ck(f"L{l['number']}guide{key}",norm(l[key]) in norm(T['CompactTeacherGuide']))
 for i,phase in enumerate(l['phases']):
  for j,s in enumerate(phase):ck(f"L{l['number']}phase{i+1}cell{j+1}",norm(s) in norm(T['CompactTeacherGuide']))
 ck(f"L{l['number']}40min",sum(l['minutes'])==40)
for outcome in S['outcomes']:ck('guide source outcome'+outcome['id'],norm(outcome['text']) in norm(T['CompactTeacherGuide']))
ck('11designlessons',len(N['lessons'])==11)
ck('ES11absentteaching','ES11' not in T['StudentMaterials']);ck('ES11presentassessment','ES11' in T['AssessmentMaterials'])
ck('assessmentonlyES11',not any(re.search(r'\bCP'+str(i)+r'\b',T['AssessmentMaterials']) for i in range(1,11)))
ck('noteachersolutionsassessment',all(norm(c['teacher']) not in norm(T['AssessmentMaterials']) for c in M['items']))
ck('finaldatasetabsentguide',norm(M['items'][-1]['student']) not in norm(T['CompactTeacherGuide']))
ck('finalanswerabsentteaching',norm(M['items'][-1]['teacher']) not in norm(T['StudentMaterials']))
rows=X['StudentSummaryTable'].findall('.//w:tr',W);ck('summary11rows',len(rows)==12)
for i,r in enumerate(rows[1:],1):
 cs=r.findall('w:tc',W);ck(f'summary{i}threeblank',len(cs)==4 and all(not ''.join(t.text or '' for t in c.findall('.//w:t',W)).strip() for c in cs[1:]))
for k,s in XML.items():
 for word in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']:ck(k+'attribution'+word,word in s)
# Independent raw enumeration and weighted frequency summaries;
# no evaluation of author expression strings.
from collections import Counter
from fractions import Fraction as F
import statistics
raw=[1,2,2,3,4,6,6,8];freq=Counter(raw);changed=raw[:-1]+[24];final=[2,3,3,4,8];ff=Counter(final);cats={'red':8,'blue':5,'green':3};pie={'red':6,'blue':3,'green':3};fb={'red':10,'blue':6,'green':4}
angles={k:F(x,sum(pie.values()))*360 for k,x in pie.items()};fangles={k:F(x,sum(fb.values()))*360 for k,x in fb.items()}
computed=[sum(raw),F(sum(raw),len(raw)),F(sum(changed),len(changed)),statistics.median(raw),F(cats['red'],sum(cats.values())),24-10,angles['red'],angles['blue'],sum([180,120,120]),sum(final),F(sum(final),len(final)),fangles['red'],fangles['blue'],fangles['green'],20-12,F(20-12,20)*100]
ck('16registrylength',len(computed)==len(M['calculations'])==16)
for c,value in zip(M['calculations'],computed):ck('independentregistry'+c['id'],abs(float(value)-c['expected'])<1e-10)
ck('fullnumericfrequency',freq=={1:1,2:2,3:1,4:1,6:2,8:1});ck('weightedtotal',sum(x*f for x,f in freq.items())==32)
ck('tiedmodes2and6',set(statistics.multimode(raw))=={2,6});ck('oddmedian5',statistics.median([2,3,5,8,9])==5)
ck('equalfreqnodistinct',len(set(Counter([1,2,3,4]).values()))==1)
ck('colourcounts',Counter(['red','blue','red','green','red','blue'])=={'red':3,'blue':2,'green':1})
ck('barcomparisons',cats['red']-cats['blue']==3 and cats['blue']-cats['green']==2)
ck('teachingpiecomplete',sum(angles.values())==360 and sum(F(x,12)*100 for x in pie.values())==100)
ck('badbarratio',F(8,5)==F(16,10));ck('badpie420',sum([180,120,120])==420)
ck('finalfrequency',ff=={2:1,3:2,4:1,8:1});ck('finalmedianmode',statistics.median(final)==3 and statistics.multimode(final)==[3])
ck('finalpiecomplete',sum(fangles.values())==360);ck('finalshares',list(F(x,20)*100 for x in fb.values())==[50,30,20])
ck('finalredcomparison',fb['red']-fb['blue']==4 and F(fb['red'],20)==F(1,2))
ck('finaltiming',N['lessons'][-1]['minutes']==[4,16,12,4,4])
assets=[B/'materials/diagrams'/f'ES{x}.png' for x in [5,6,7,12,13,14]]
for asset in assets:
 im=Image.open(asset);ck(asset.stem+'native1100x800',im.size==(1100,800))
 destinations=['MaterialsTeacherKey','StudentMaterials' if asset.stem in {'ES5','ES6','ES7'} else 'AssessmentMaterials']
 for k in destinations:ck(k+asset.stem+'exactbytes',sha(asset) in docs[k]['embedded_media'].values())
for k in ['StudentMaterials','MaterialsTeacherKey','AssessmentMaterials']:
 ck(k+'allplotaspect',all(abs(v['cx']/v['cy']-1100/800)<.0001 for v in docs[k]['image_extents']))
for k,count in [('StudentMaterials',3),('MaterialsTeacherKey',6),('AssessmentMaterials',3)]:ck(k+'plotcount',len(docs[k]['embedded_media'])==count)
for i in range(11,15):ck('ES'+str(i)+'absentteaching','ES'+str(i) not in T['StudentMaterials'])
ck('ES11dataabsentguide',norm(M['items'][10]['student']) not in norm(T['CompactTeacherGuide']))
paths=[B/p/'essmath_3_1.json' for p in ['sources','blueprints','materials','manuscripts']]+[B/'sources/essmath_3_1.verification.json']+assets
hashes={str(p.relative_to(B)):sha(p) for p in sorted(set(paths))}
fp=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
sourcepaths=[ROOT/'CBE_Curriculums/Grade 10/STEM/Essential Mathematics Grade 10 - July 2025.pdf',B/'sources/essmath_3_1_source.png',ROOT/V['evidence']]
sh={str(p.relative_to(ROOT)):sha(p) for p in sourcepaths}
sourcechecks={'pdf':sha(sourcepaths[0])==S.get('source_pdf_sha256',S.get('pdf_sha256')),'source_record':sha(B/'sources/essmath_3_1.json')==V['source_record_sha256'],'crop':sha(sourcepaths[1])==V['crop_sha256'],'evidence':sha(sourcepaths[2])==V['evidence_sha256']}
# source PDF hash may be nested in record; record exact actual digest regardless.
binding={'content_fingerprint':fp,'canonical_hashes':hashes,'source_related_hashes':sh,'source_binding_checks':sourcechecks,'draft_documents':docs}
(E/'essmath_3_1_review_binding.json').write_text(json.dumps(binding,indent=2)+'\n')
res={'passed':sum(x['pass'] for x in checks),'total':len(checks),'failed':[x for x in checks if not x['pass']],'checks':checks,'independent_models':{'numeric_frequency':dict(freq),'raw_sorted':sorted(raw),'raw_modes':statistics.multimode(raw),'final_frequency':dict(ff),'pie_angles':{k:str(v) for k,v in angles.items()},'final_pie_angles':{k:str(v) for k,v in fangles.items()},'registry_values':dict(zip([c['id'] for c in M['calculations']],map(float,computed)))},'note':'Independent raw data enumeration/frequency-weighted totals and fractional shares; actual project/time observations/digital actions have no universal numeric answer.'}
(E/'essmath_3_1_initial_checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'fingerprint':fp,'passed':res['passed'],'total':res['total'],'failed':res['failed'],'sourcechecks':sourcechecks,'docs':docs,'source_schema':list(S)},indent=2))
