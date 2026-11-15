from pathlib import Path
from io import BytesIO
import json,hashlib,sys,zipfile
from lxml import etree
from docx import Document
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';sys.path.insert(0,str(R/'scripts'));from curriculum_pipeline import content_fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();bh=lambda b:hashlib.sha256(b).hexdigest();ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
indexp=B/'evidence/superseded_packages_2026-11-15/superseded_originals.json';index=json.loads(indexp.read_text());results={}
def diff(a,b,p=''):
 if type(a)!=type(b):return[(p,a,b)]
 if isinstance(a,dict):return sum([diff(a.get(k),b.get(k),p+'/'+k)for k in sorted(set(a)|set(b))],[])
 if isinstance(a,list):
  if len(a)!=len(b):return[(p,a,b)]
  return sum([diff(x,y,p+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))],[])
 return[]if a==b else[(p,a,b)]
expectedfps={'coremath_1_1':'78e0ecd0344157c601f8d94ba6c52571865ec8cfd62c098c9a5ba13e4aaffe5f','essmath_1_3':'994ab2b3e64f219e8943d9a490f020eb78d2019c27260b96c1ca15003f2ef3e1'}
for entry in index:
 mod=entry['module'];old=R/entry['snapshot_directory'];out=B/f'reviews/batch_07/evidence/{mod}_rubric_correction_recheck';out.mkdir(exist_ok=True);checks=[]
 def ck(n,b):checks.append({'check':n,'pass':bool(b)})
 diffs={};inputs={}
 for k in ['sources','materials','blueprints','manuscripts']:
  p=B/k/f'{mod}.json';raw=p.read_bytes();out.joinpath('current_'+k+'.json').write_bytes(raw);a=json.loads((old/('original_'+k+'.json')).read_text());b=json.loads(raw);diffs[k]=diff(a,b);inputs[k]={'old':sha(old/('original_'+k+'.json')),'current':bh(raw)}
  if k!='manuscripts':ck(k+' original exact bytes',inputs[k]['old']==inputs[k]['current'])
 ck('exact requested diff paths',[d[0]for d in diffs['manuscripts']]==(['/assessment/rubric/3/proficient']if mod=='coremath_1_1'else['/assessment/rubric/1/excellent','/assessment/rubric/1/proficient']))
 m=json.loads((B/'manuscripts'/f'{mod}.json').read_text());s=json.loads((B/'sources'/f'{mod}.json').read_text());bank=json.loads((B/'materials'/f'{mod}.json').read_text());archive=B/entry['archive'];ck('old archive unchanged SHA',sha(archive)==entry['sha256']);receipt=json.loads((old/'original_receipt.json').read_text());ck('old archive receipt SHA matches',receipt['sha256']==sha(archive));ck('current fingerprint',content_fingerprint(B,mod)==expectedfps[mod]);words={};assets={}
 for c in bank['items']:
  for a in c.get('assets',[]):assets[a]=sha(B/'materials'/a)
 with zipfile.ZipFile(archive)as originalzip:
  for k in ['sources','materials','blueprints','manuscripts']:
   matches=[n for n in originalzip.namelist()if n==f'{k}/{mod}.json'];ck(k+' snapshot matches original ZIP canonical',len(matches)==1 and bh(originalzip.read(matches[0]))==inputs[k]['old'])
  for typ in ['AssessmentMaterials','CompactTeacherGuide','MaterialsTeacherKey','StudentMaterials','StudentSummaryTable']:
   candidates=[n for n in originalzip.namelist()if n.endswith('_'+typ+'.docx')];ck(typ+' one old actual ZIP member',len(candidates)==1);member=candidates[0];current=B/member;oldbytes=originalzip.read(member)
   def data(b):
    with zipfile.ZipFile(BytesIO(b))as z:
     tree=etree.fromstring(z.read('word/document.xml'));text='\n'.join(t.text or''for t in tree.findall('.//w:t',ns));media={n:bh(z.read(n))for n in z.namelist()if n.startswith('word/media/')};allxml=' '.join(z.read(n).decode()for n in z.namelist()if n.startswith('word/')and n.endswith('.xml'))
     return text,media,allxml,z.read('word/document.xml')
   ot,om,ox,ob=data(oldbytes);ct,cm,cx,cb=data(current.read_bytes());words[typ]={'member':member,'old_docx_sha256':bh(oldbytes),'current_path':str(current.relative_to(R)),'current_docx_sha256':sha(current),'old_media':om,'current_media':cm,'old_body_sha256':bh(ob),'current_body_sha256':bh(cb),'text_unchanged':ot==ct};out.joinpath(typ+'_current.txt').write_text(ct);ck(typ+' body text unchanged',ot==ct);ck(typ+' media unchanged',om==cm);ck(typ+' no undeclared images',not cm and not assets);ck(typ+' attribution','ChatGPT/Codex'in cx and'OpenAI'in cx);words[typ]['_text']=ct
 final=bank['items'][-1]['id']
 for c in bank['items']:
  for k in ['title','student','teacher']:ck('key '+c['id']+' '+k,c[k]in words['MaterialsTeacherKey']['_text'])
  typ='AssessmentMaterials'if c['id']==final else'StudentMaterials'
  for k in ['title','student']:ck(typ+' '+c['id']+' '+k,c[k]in words[typ]['_text'])
  ck('student no full teacher key '+c['id'],c['teacher']not in words[typ]['_text'])
  if c['id']==final:ck('full final excluded teaching',c['student']not in words['StudentMaterials']['_text'])
 for o in s['outcomes']:ck('guide source '+o['id'],o['text']in words['CompactTeacherGuide']['_text'])
 for l in m['lessons']:
  for k in ['title','purpose','knowledge','safety','reflection']:ck('guide L'+str(l['number'])+' '+k,l[k]in words['CompactTeacherGuide']['_text'])
  for j,p in enumerate(l['phases']):
   for q,t in enumerate(p):ck('guide phase '+str(l['number'])+'/'+str(j)+'/'+str(q),t in words['CompactTeacherGuide']['_text'])
  ck('minutes L'+str(l['number']),sum(l['minutes'])==40)
 doc=Document(B/words['StudentSummaryTable']['member']);rows=doc.tables[0].rows;ck('summary row count',len(rows)==len(m['lessons'])+1)
 for l,row in zip(m['lessons'],rows[1:]):
  ck('summary label '+str(l['number']),row.cells[0].text==str(l['number'])+'. '+l['title'])
  for j in range(1,4):ck('summary blank '+str(l['number'])+'/'+str(j),not row.cells[j].text)
 for w in words.values():w.pop('_text')
 ck('archive unchanged at end',sha(archive)==entry['sha256']);result={'module':mod,'verdict':'PASS'if all(c['pass']for c in checks)else'HOLD','original_content_fingerprint':entry['original_content_fingerprint'],'current_content_fingerprint':content_fingerprint(B,mod),'archive':str(archive.relative_to(R)),'archive_sha256':sha(archive),'index_sha256':sha(indexp),'inputs':inputs,'diff':diffs,'assets':assets,'words':words,'checks':checks,'passed':sum(c['pass']for c in checks),'total':len(checks),'preserved_original_files':{str(p.relative_to(R)):sha(p)for p in sorted(old.glob('*'))if p.is_file()}};(out/'binding.json').write_text(json.dumps(result,indent=2)+'\n');print(mod,result['verdict'],result['passed'],result['total']);print('FAILURES',[c for c in checks if not c['pass']]);print('diff',diffs['manuscripts']);results[mod]=result
