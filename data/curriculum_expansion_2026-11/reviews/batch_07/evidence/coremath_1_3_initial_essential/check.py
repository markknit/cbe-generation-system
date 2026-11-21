from pathlib import Path
import json,sys,hashlib,zipfile
from lxml import etree
from docx import Document
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';O=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'scripts'));from curriculum_pipeline import content_fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda k:json.loads((B/k/'coremath_1_3.json').read_text());m=load('manuscripts');bank=load('materials');s=load('sources');ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};f=B/'outputs/v2/Core_Mathematics/SS1.3_Quadratic_Expressions_and_Equations';words={};checks=[]
def ck(n,c):checks.append({'check':n,'pass':bool(c)})
for p in sorted(f.glob('*.docx')):
 key=p.stem.split('_Quadratic_Expressions_and_Equations_')[1]
 with zipfile.ZipFile(p) as z:
  tree=etree.fromstring(z.read('word/document.xml'));text='\n'.join(t.text or '' for t in tree.findall('.//w:t',ns));allxml=' '.join(z.read(n).decode() for n in z.namelist() if n.startswith('word/') and n.endswith('.xml'));media=[n for n in z.namelist() if n.startswith('word/media/')]
 words[key]={'path':str(p.relative_to(R)),'sha256':sha(p),'text':text,'media':media};(O/(key+'.txt')).write_text(text);ck(key+' attribution','ChatGPT/Codex' in allxml and 'OpenAI' in allxml)
for c in bank['items']:
 for k in ['title','student','teacher']:ck('key '+c['id']+' '+k,c[k] in words['MaterialsTeacherKey']['text'])
 typ='AssessmentMaterials' if c['id']=='CQE14' else 'StudentMaterials'
 for k in ['title','student']:ck(typ+' '+c['id']+' '+k,c[k] in words[typ]['text'])
 ck('student no teacher '+c['id'],c['teacher'] not in words[typ]['text'])
 if c['id']=='CQE14':ck('teaching no final CQE14',c['student'] not in words['StudentMaterials']['text'])
g=words['CompactTeacherGuide']['text']
for o in s['outcomes']:ck('source '+o['id'],o['text'] in g)
for l in m['lessons']:
 for k in ['title','purpose','knowledge','safety','reflection']:ck('L'+str(l['number'])+' '+k,l[k] in g)
 for j,phase in enumerate(l['phases']):
  for k,t in enumerate(phase):ck('L'+str(l['number'])+' phase'+str(j)+' cell'+str(k),t in g)
 ck('L'+str(l['number'])+' minutes',sum(l['minutes'])==40)
d=Document(R/words['StudentSummaryTable']['path']);rows=d.tables[0].rows;ck('summary14rows',len(rows)==15)
for l,row in zip(m['lessons'],rows[1:]):
 ck('summary L'+str(l['number'])+' label',row.cells[0].text==str(l['number'])+'. '+l['title'])
 for j in range(1,4):ck('summary L'+str(l['number'])+' blank'+str(j),not row.cells[j].text)
r={'reviewed_content_fingerprint':content_fingerprint(B,'coremath_1_3'),'verdict':'HOLD','inputs':{str((B/k/'coremath_1_3.json').relative_to(R)):sha(B/k/'coremath_1_3.json') for k in ['sources','materials','blueprints','manuscripts']},'source_pdf_sha256':sha(R/s['pdf']),'source_crop_sha256':sha(B/'sources/coremath_1_3_source.png'),'source_verification_sha256':sha(B/'sources/coremath_1_3.verification.json'),'words':{k:{a:v for a,v in d.items() if a!='text'} for k,d in words.items()},'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks),'semantic_content_acceptance':False};(O/'binding.json').write_text(json.dumps(r,indent=2)+'\n');print(r['reviewed_content_fingerprint']);print(r['passed'],r['total']);print('failures',[x for x in checks if not x['pass']])
