"""Offline compiler boundary regression. Isolated copies only; all Word writers stubbed."""
from pathlib import Path
import copy,hashlib,json,subprocess,tempfile,types,sys
import jsonschema
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'data/curriculum_expansion_2026-11';E=Path(__file__).parent;CODE=ROOT/'scripts/curriculum/compiler.py';sys.path.insert(0,str(ROOT/'scripts'))
from curriculum_pipeline import content_fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
current=CODE.read_text();previous=subprocess.check_output(['git','show','HEAD:scripts/curriculum/compiler.py'],cwd=ROOT,text=True)
schema=json.loads((ROOT/'ares-contract.schema.json').read_text());validator=jsonschema.Draft202012Validator(schema);rows=[];details={};writes=[]
def ck(label,value):
 rows.append({'check':label,'pass':bool(value)})
 if not value:raise AssertionError(label)
def load_compiler(text,base):
 mod=types.ModuleType('compiler_review');mod.__file__=str(CODE);exec(compile(text,str(CODE),'exec'),mod.__dict__);mod.BASE=base
 def stub(*args,**kwargs):writes.append(str(args[0]));return None
 mod.write_doc=stub;mod.write_guide=stub;mod.write_student_summary=stub
 return mod
def export(text,base,name):
 mod=load_compiler(text,base);mod.build(name)
 p=base/'modules'/(name+'_data.js');out=json.loads(p.read_text().split('module.exports = ',1)[1].rsplit(';',1)[0]);return out

def contract_errors(bundle):
 value=copy.deepcopy(bundle)
 # Production's later resource stage supplies this map. No recommender is run.
 for lesson in value['LESSONS']:lesson['resourceLinks']={p:{'video':None,'reading':None,'fallback_search_url':'https://example.invalid/search'} for p in ['predict','observe','explain','dqb','model']}
 return [{'path':'/'.join(map(str,x.absolute_path)),'message':x.message} for x in validator.iter_errors(value)]

names=['gensci_1_7','gensci_1_6','essmath_2_7','coremath_3_2'];production_paths=[B/k/(name+'.json') for name in names for k in ['sources','blueprints','materials','manuscripts']]+[B/'sources'/(name+'.verification.json') for name in names]
production_paths+=sorted((B/'outputs/v2/General_Science/SS1.7_Microorganisms').glob('*.docx'));before={str(p.relative_to(ROOT)):sha(p) for p in production_paths}
with tempfile.TemporaryDirectory(prefix='compiler-author-metadata-review-') as temporary:
 base=Path(temporary)
 for name in names:
  for k in ['sources','blueprints','materials','manuscripts']:
   target=base/k/(name+'.json');target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((B/k/(name+'.json')).read_bytes())
  (base/'sources'/(name+'.verification.json')).write_bytes((B/'sources'/(name+'.verification.json')).read_bytes())
 for name in names:
  canonical=[base/k/(name+'.json') for k in ['sources','blueprints','materials','manuscripts']]+[base/'sources'/(name+'.verification.json')];pre={str(p.relative_to(base)):sha(p) for p in canonical};fp=content_fingerprint(base,name)
  old=export(previous,base,name);new=export(current,base,name);d=json.loads((base/'manuscripts'/(name+'.json')).read_text());s=json.loads((base/'sources'/(name+'.json')).read_text());p=json.loads((base/'blueprints'/(name+'.json')).read_text())
  expected=copy.deepcopy(old)
  for key in ['keyInquiryQuestions','teacherConfirmationRequired']:expected['UNIT'].pop(key,None)
  for section in expected['FINAL_EXPLANATION']['sections']:section.pop('marks',None)
  ck(name+': exact named omissions only',new==expected)
  ck(name+': all lessons unchanged',new['LESSONS']==old['LESSONS'])
  ck(name+': metadata and summary unchanged',new['META']==old['META'] and new['SUMMARY_TABLE']==old['SUMMARY_TABLE'])
  ck(name+': final prose/rubric unchanged',all(new['FINAL_EXPLANATION'][k]==old['FINAL_EXPLANATION'][k] for k in old['FINAL_EXPLANATION'] if k!='sections') and all({k:v for k,v in x.items() if k!='marks'}==y for x,y in zip(old['FINAL_EXPLANATION']['sections'],new['FINAL_EXPLANATION']['sections'])))
  ck(name+': source outcomes preserved',new['UNIT']['learningOutcomes']=='\n'.join(x['text'] for x in s['outcomes']))
  ck(name+': canonical files and content fingerprint unchanged',all(sha(base/k)==h for k,h in pre.items()) and content_fingerprint(base,name)==fp)
  if name!='gensci_1_7':ck(name+': entire old/new bundle identical',new==old)
  errors=contract_errors(new)
  if errors:print('SCHEMA DIAGNOSTIC',name,errors[:3])
  ck(name+': new R1 validates after isolated null-resource map',not errors)
  details[name]={'old_schema_errors':contract_errors(old),'new_schema_errors':errors,'fingerprint':fp,'canonical_hashes':pre}
  if name=='gensci_1_7':
   baseline=new;manuscript=copy.deepcopy(d)
   ck('GS1.7 old gate rejects exactly author notes/section marks',len(details[name]['old_schema_errors'])==4 and all('Additional properties' in x['message'] for x in details[name]['old_schema_errors']))
   ck('GS1.7 all named notes/marks remain canonical','keyInquiryQuestions' in d['unit'] and 'teacherConfirmationRequired' in d['unit'] and all('marks' in x for x in d['assessment']['sections']))
   ck('GS1.7 inquiry remains in exported authoritative driver',all(q in new['UNIT']['drivingQuestion'] for q in d['unit']['keyInquiryQuestions']) and new['UNIT']['drivingQuestion']==d['unit']['drivingQuestion'])
   ck('GS1.7 teacher confirmations retained in blueprint',bool(p['teacher_confirmation_required']) and json.loads((base/'blueprints'/(name+'.json')).read_text())==p)
 # Unknown keys must still reach R1, not disappear through a broad allowlist.
 name='gensci_1_7';path=base/'manuscripts'/(name+'.json')
 for label,mutate in [
  ('unknown UNIT key',lambda d:d['unit'].__setitem__('unexpectedAuthorNote','must fail')),
  ('unknown section key',lambda d:d['assessment']['sections'][0].__setitem__('unexpectedSectionNote','must fail')),
  ('unknown final key',lambda d:d['assessment'].__setitem__('unexpectedFinalNote','must fail')),
  ('named UNIT-only note at section level',lambda d:d['assessment']['sections'][0].__setitem__('teacherConfirmationRequired','must fail'))]:
  case=copy.deepcopy(manuscript);mutate(case);path.write_text(json.dumps(case,ensure_ascii=False,indent=2)+'\n');value=export(current,base,name);errors=contract_errors(value);ck(label+': preserved and rejected by R1',len(errors)==1 and 'Additional properties' in errors[0]['message']);details[label]=errors
 # Each excluded field still participates in canonical fingerprinting.
 for label,mutate in [
  ('inquiry author note',lambda d:d['unit']['keyInquiryQuestions'].append('Isolated sentinel')),
  ('confirmation author note',lambda d:d['unit'].__setitem__('teacherConfirmationRequired',d['unit']['teacherConfirmationRequired']+' Isolated sentinel')),
  ('section marks',lambda d:d['assessment']['sections'][0].__setitem__('marks',99))]:
  path.write_text(json.dumps(manuscript,ensure_ascii=False,indent=2)+'\n');fp=content_fingerprint(base,name);case=copy.deepcopy(manuscript);mutate(case);path.write_text(json.dumps(case,ensure_ascii=False,indent=2)+'\n');ck(label+': fingerprint changes despite same export',content_fingerprint(base,name)!=fp and export(current,base,name)==baseline)
 ck('no Word/PDF files rendered',not list(base.rglob('*.docx')) and not list(base.rglob('*.pdf')))
 ck('all writer stub paths remain isolated',all(Path(p).is_relative_to(base) for p in writes))
ck('production canonical and existing GS1.7 Word hashes unchanged',all(sha(ROOT/k)==h for k,h in before.items()))
ck('compiler and contract unchanged by review',sha(CODE)==hashlib.sha256(current.encode()).hexdigest())
result={'compiler_path':str(CODE.relative_to(ROOT)),'compiler_sha256':sha(CODE),'previous_HEAD_sha256':hashlib.sha256(previous.encode()).hexdigest(),'contract_sha256':sha(ROOT/'ares-contract.schema.json'),'checks_total':len(rows),'checks_pass':sum(r['pass'] for r in rows),'checks':rows,'details':details,'production_bindings_unchanged':before,'scope':'Old/new isolated module builds with all three Word writer functions stubbed; R1 validation uses a test-only all-null resource map. No production rebuild/render, acceptance, pipeline/cache/audit command or network request.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['compiler_sha256','previous_HEAD_sha256','contract_sha256','checks_total','checks_pass']},indent=2))
