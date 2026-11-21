from pathlib import Path
import json,hashlib,re,sys,datetime,zipfile
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';P=R/'data/codex_pilot_2026-11';E=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'scripts'));from curriculum_pipeline import content_fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();digit=[];word=[];allrows=[];inputs=[];nc=0
numberwords=re.compile(r'(?i)\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|hundred|half|quarter|third)\b')
def classify(mod,idx,key,text,is_digit):
 if mod=='coremath_1_1' and idx==4:return 'CONFIRMED_ANSWER_DISCLOSURE','4portions supplies I4 result;7/2 divided by7/8=4.'
 if mod=='coremath_2_4' and idx in [3,4] and is_digit:return 'CONFIRMED_ANSWER_DISCLOSURE_INITIAL','Initial7.17m/8m results and30°interpretation supply requested unknowns;current root correction recorded separately.'
 if mod=='essmath_1_3' and idx==2 and key in ['excellent','proficient']:return 'CONFIRMED_PARTIAL_ANSWER_DISCLOSURE','lost-zero/zero-root names0 as one requested root of y²=4y;not merely a generic zero-product-law reference.'
 if is_digit:
  if mod=='coremath_1_1' and idx==1:return 'GENERAL_INCLUSION_IDENTITY','0 and1 are supplied classification cases;0/1 read as fraction is generic representation of zero,not one of the six requested exact-value fraction answers. Slight wording ambiguity,not a concrete unknown answer.'
  if mod in ['coremath_1_1','coremath_1_2']:return 'DECLARED_PRECISION','Significant-figure requirement already in prompt;no numerical result disclosed.'
  if mod=='coremath_1_3':return 'GIVEN_INPUT','99² is the expression explicitly supplied to evaluate;9801 is not supplied.'
  if mod=='coremath_2_4':return 'GIVEN_DOMAIN_CASE','90° is the expressly requested endpoint;sin/cos/tan values are not printed by this descriptor.'
  return 'GENERAL_INVARIANT_DEFINITION','Total probability1 or reciprocal product1 is the governing invariant/definition,not the sought event probabilities/reciprocal value.'
 if mod=='coremath_2_8' and 'one another' in text:return 'IDIOM','one another is reciprocal-language idiom,not a number.'
 if 'zero-product' in text:return 'GENERAL_RULE','Zero-product is the named general algebraic condition;does not give a particular solution.'
 if mod=='coremath_2_2':return 'ORDINAL_TARGET','Third angle labels the requested unknown;does not give its size.'
 if mod=='coremath_2_8':return 'GIVEN_CONSTRUCTION_RELATION','Half-displacement is expressly supplied A+(1/2)AB;midpoint coordinate remains unknown.'
 if mod=='coremath_2_9':return 'DEFINED_TARGET','Zero crossing is already the requested target;crossing time/areas remain unknown.'
 if mod=='coremath_1_1' or mod=='essmath_1_1':return 'GIVEN_ZERO_EXCEPTION','Zero is explicitly supplied in prompt for reciprocal exception;no reciprocal numeric answer is supplied.'
 if mod in ['coremath_2_7','gensci_1_5']:return 'GIVEN_MODEL_DOMAIN','Zero-thickness/zero-denominator names an explicitly supplied model/input condition;does not supply a sought result.'
 return 'RESPONSE_OR_MODEL_COMPONENT_COUNT','Counts requested responses/components or partial-credit breadth,or restates model decomposition;does not supply a sought numerical value.'
for base in [B,P]:
 for p in sorted((base/'manuscripts').glob('*.json')):
  n=json.loads(p.read_text());mod=p.stem;a=n['assessment'];inputs.append({'module':mod,'workspace':str(base.relative_to(R)),'path':str(p.relative_to(R)),'sha256':sha(p),'content_fingerprint':content_fingerprint(base,mod) if base==B else None,'pilot_note':None if base==B else 'Legacy pilot lacks per-source verification JSON; exact manuscript hash binds this rubric scan without inventing a current expansion fingerprint','criteria':len(a['rubric'])})
  for idx,r in enumerate(a['rubric'],1):
   nc+=1
   for key,text in r.items():
    # Preserve complete rubric and related assessment,including nonnumeric descriptors.
    row={'module':mod,'criterion':idx,'level':key,'text':text};allrows.append(row)
    if re.search(r'\d',text) or numberwords.search(text):
     kind,reason=classify(mod,idx,key,text,bool(re.search(r'\d',text)));entry={**row,'classification':kind,'reason':reason,'assessment_sections':a['sections']};
     if re.search(r'\d',text):digit.append(entry)
     if numberwords.search(text):word.append(entry)
# Preserve initial Trig descriptors from frozen reviewer snapshot;current manuscript is already a correction.
old=B/'reviews/batch_07/evidence/coremath_2_4_core27/initial_manuscripts.json';n=json.loads(old.read_text());initial=[]
for idx,r in enumerate(n['assessment']['rubric'],1):
 for key,text in r.items():
  if re.search(r'\d',text):
   kind,reason=classify('coremath_2_4',idx,key,text,True);initial.append({'module':'coremath_2_4','criterion':idx,'level':key,'text':text,'classification':kind,'reason':reason,'assessment_sections':n['assessment']['sections']})
for mod in ['coremath_1_1','essmath_1_3']:
 p=B/'manuscripts'/f'{mod}.json';(E/f'frozen_{mod}_manuscript.json').write_bytes(p.read_bytes())
art=[]
for p in sorted((B/'outputs/v2/Core_Mathematics/SS1.1_Real_Numbers').glob('*.docx')):
 art.append({'path':str(p.relative_to(R)),'sha256':sha(p)})
 pdf=B/'outputs/PDF'/p.with_suffix('.pdf').name
 if pdf.exists():art.append({'path':str(pdf.relative_to(R)),'sha256':sha(pdf)})
for p in (B/'outputs/v2/Essential_Mathematics/SS1.3_Quadratic_Equations_I').glob('*_FinalExplanation.docx'):
 for q in [p,B/'outputs/PDF'/p.with_suffix('.pdf').name]:art.append({'path':str(q.relative_to(R)),'sha256':sha(q)})
zp=B/'coremath_1_1_Reviewed.zip';archive={'path':str(zp.relative_to(R)),'sha256':sha(zp),'checked_members':[]}
with zipfile.ZipFile(zp) as z:
 for path in ['manuscripts/coremath_1_1.json','materials/coremath_1_1.json']+[str(Path(x['path']).relative_to(B.relative_to(R))) for x in art if x['path'].endswith(('_FinalExplanation.docx','_FinalExplanation.pdf')) and 'Core_Mathematics' in x['path']]:
  raw=z.read(path);current=B/path;archive['checked_members'].append({'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'current_equal':raw==current.read_bytes()})
result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Numeric rubric disclosure only;40 expansion plus3 frozen pilots;no broad content/layout redo.','modules':inputs,'module_count':len(inputs),'criterion_count':nc,'rubric_string_count':len(allrows),'all_rubric_strings':allrows,'current_digit_candidate_count':len(digit),'current_digit_candidates':digit,'word_candidate_count':len(word),'word_candidates':word,'initial_trig_binding':{'path':str(old.relative_to(R)),'sha256':sha(old),'accepted_initial_fp':'66b147720950899a52238f801fb1f94e56d716e96427e64434b1ce4d9dce2897','candidates':initial},'actual_artifacts':art,'old_archive':archive,'caveat':'Core2.4changed during review;initial descriptors bound to preserved initial manuscript. No correction verdict here.'}
(E/'candidate_ledger.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print({k:v for k,v in result.items() if k.endswith('_count')});print('archive',archive)
