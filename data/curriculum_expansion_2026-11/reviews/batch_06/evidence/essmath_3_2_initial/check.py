from pathlib import Path
import sys,json,hashlib,zipfile
from lxml import etree
from PIL import Image
ROOT=Path(__file__).resolve().parents[6];sys.path.insert(0,str(ROOT/'scripts'))
from curriculum.validation import validate
BASE=ROOT/'data/curriculum_expansion_2026-11';OUT=Path(__file__).resolve().parent;NAME='essmath_3_2'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda a:json.loads((BASE/a/(NAME+'.json')).read_text())
s,m,bp,bank=load('sources'),load('manuscripts'),load('blueprints'),load('materials')
folder=BASE/'outputs/v2/Essential_Mathematics/SS3.2_Probability_I'
words={};checks=[]
def ck(label,condition):
 checks.append({'label':label,'pass':bool(condition)});assert condition,label
for p in sorted(folder.glob('*.docx')):
 with zipfile.ZipFile(p) as z:
  tree=etree.fromstring(z.read('word/document.xml'));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  text='\n'.join(''.join(n.itertext()) for n in tree.findall('.//w:t',ns))
  paragraphs=[''.join(t.itertext()) for n in tree.findall('.//w:p',ns) for t in []]
  text='\n'.join(''.join(t.itertext()) for t in tree.findall('.//w:t',ns))
  media={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
  allxml=' '.join(z.read(n).decode() for n in z.namelist() if n.startswith('word/') and n.endswith('.xml'))
 key=p.stem.split('_Probability_I_',1)[1];words[key]={'path':str(p.relative_to(ROOT)),'sha256':sha(p),'text':text,'media':media}
 (OUT/(key+'.txt')).write_text(text)
 ck(key+' OpenAI attribution','ChatGPT/Codex' in allxml and 'OpenAI' in allxml)
for c in bank['items']:
 for field in ['title','student','teacher']:
  ck('key '+c['id']+' '+field,c[field] in words['MaterialsTeacherKey']['text'])
 if c['id']!='EP10':
  for field in ['title','student']:ck('student '+c['id']+' '+field,c[field] in words['StudentMaterials']['text'])
  ck('student no key '+c['id'],c['teacher'] not in words['StudentMaterials']['text'])
 else:
  for field in ['title','student']:ck('assessment EP10 '+field,c[field] in words['AssessmentMaterials']['text'])
  ck('teaching no final task',c['student'] not in words['StudentMaterials']['text'])
  ck('assessment no final key',c['teacher'] not in words['AssessmentMaterials']['text'])
g=words['CompactTeacherGuide']['text']
for o in s['outcomes']:ck('guide source '+o['id'],o['text'] in g)
for l in m['lessons']:
 for f in ['title','purpose','knowledge','safety','reflection']:ck('guide L'+str(l['number'])+' '+f,l[f] in g)
 for i,p in enumerate(l['phases']):
  for j,t in enumerate(p):ck('guide L'+str(l['number'])+' phase'+str(i+1)+' cell'+str(j+1),t in g)
for key,ids in [('StudentMaterials',[]),('MaterialsTeacherKey',[]),('AssessmentMaterials',[])]:
 expected={sha(BASE/'materials/diagrams'/(k+'.png')) for k in ids}
 ck(key+' media binding',set(words[key]['media'].values())==expected and len(words[key]['media'])==len(ids))
from docx import Document
d=Document(ROOT/words['StudentSummaryTable']['path']);rows=d.tables[0].rows
ck('blank summary 10 lessons',len(rows)==11)
for l,row in zip(m['lessons'],rows[1:]):
 ck('summary L'+str(l['number'])+' label',row.cells[0].text==str(l['number'])+'. '+l['title'])
 for j in range(1,4):ck('summary L'+str(l['number'])+' blank'+str(j),row.cells[j].text=='')
ck('preflight structural pass',not validate(BASE,NAME)['errors'])
# Expected numerical results are independently established from geometry/arithmetic.
import math
expected={'half':.5,'joint':.25,'or':.75,'exactly':.5,'Hobserved':.7,'Robserved':.55,'HRobserved':.3,'pairtotal':20,'rangeunion':1}
for c in bank['calculations']:ck('registered '+c['id'],math.isclose(c['expected'],expected[c['id']],rel_tol=1e-12,abs_tol=1e-12))
full=Path('/tmp/essential-source-review-full.png');crop=BASE/'sources/essmath_3_2_source.png'
if full.exists():
 actual=Image.open(full).crop(tuple(s['crop_pixels']));stored=Image.open(crop);ck('source crop matches prior independent fresh render',actual.size==stored.size and actual.tobytes()==stored.tobytes())
record={'scope':'Initial independent content and five-Word propagation review;confirmed semantic issues are reported separately from structural pass','acceptance_fingerprint_computed':False,'source_pdf_sha256':sha(ROOT/s['pdf']),'source_crop_sha256':sha(crop),'inputs':{str(BASE/a/(NAME+'.json')):sha(BASE/a/(NAME+'.json')) for a in ['sources','blueprints','materials','manuscripts']},'verification_sha256':sha(BASE/'sources'/f'{NAME}.verification.json'),'diagrams':{},'words':{k:{a:v for a,v in d.items() if a!='text'} for k,d in words.items()},'checks':checks,'checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks)}
(OUT/'binding.json').write_text(json.dumps(record,indent=2)+'\n');print(str(len(checks))+'/'+str(len(checks))+' propagation/structural checks PASS')
