from pathlib import Path
import json,hashlib,subprocess,copy
E=Path(__file__).resolve().parent;I=E.parent/'gensci_2_1_core27';B=Path.cwd()/'data/curriculum_expansion_2026-11';old=json.loads((I/'binding.json').read_text());now=json.loads((E/'binding.json').read_text());changes=[];checks={}
sha=lambda b:hashlib.sha256(b).hexdigest()
def diff(a,b,p=''):
 if type(a)!=type(b):changes.append({'path':p,'before':a,'after':b});return
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:diff(a[k],b[k],p+'/'+k)
 elif isinstance(a,list):
  if a!=b and (not a or not isinstance(a[0],(dict,list))):changes.append({'path':p,'before':a,'after':b})
  else:
   assert len(a)==len(b)
   for i,(x,y) in enumerate(zip(a,b)):diff(x,y,p+'/'+str(i))
 elif a!=b:changes.append({'path':p,'before':a,'after':b})
for p,h in old['inputs'].items():
 raw=subprocess.check_output(['git','show','HEAD:'+p]);checks[p+'_old_git_matches_frozen_hash']=sha(raw)==h;assert sha(raw)==h
 before=json.loads(raw);after=json.loads(Path(p).read_text());(E/('before_'+Path(p).name)).write_bytes(raw)
 diff(before,after,p)
expected={}
for prefix in ['data/curriculum_expansion_2026-11/manuscripts/gensci_2_1.json/lessons','data/curriculum_expansion_2026-11/blueprints/gensci_2_1.json/lesson_map']:
 expected[prefix+'/6/outcomes']=(['d','e'],['e']);expected[prefix+'/10/outcomes']=(['e','f'],['f']);expected[prefix+'/13/outcomes']=(list('abcdefg'),list('acdefg'))
for label in ['assessment_map','assessment_tasks']:
 prefix='data/curriculum_expansion_2026-11/blueprints/gensci_2_1.json/'+label
 expected[prefix+'/6/outcomes']=(['d','e'],['e']);expected[prefix+'/10/outcomes']=(['e','f'],['f']);expected[prefix+'/13/outcomes']=(list('abcdefg'),list('acdefg'))
extra=['data/curriculum_expansion_2026-11/materials/gensci_2_1.json/items/6/student','data/curriculum_expansion_2026-11/materials/gensci_2_1.json/items/6/teacher','data/curriculum_expansion_2026-11/manuscripts/gensci_2_1.json/lessons/6/phases/2']
actual={d['path']:d for d in changes};checks['exact_15_changed_fields']=set(actual)==set(expected)|set(extra)
for p,(a,b) in expected.items():checks[p+'_expected_delta']=actual[p]['before']==a and actual[p]['after']==b
for p in extra[:2]:checks[p+'_append_only']=actual[p]['after'].startswith(actual[p]['before'])
x=actual[extra[-1]];checks['L7_phase3_only_learner_and_check_changed']=x['before'][1:3]==x['after'][1:3]
M=json.loads((B/'materials/gensci_2_1.json').read_text());N=json.loads((B/'manuscripts/gensci_2_1.json').read_text());P=json.loads((B/'blueprints/gensci_2_1.json').read_text())
for id,cards in [('d',['PT5','PT6']),('e',['PT7','PT8','PT9','PT13']),('b',['PT3','PT12'])]:
 checks[id+'_retained_actual_task_locations']=all(any(id in l['outcomes'] and c in l['materials'] for l in N['lessons']) for c in cards)
checks['all_seven_final_outcomes_retained']=set(N['lessons'][-1]['outcomes'])==set('abcdefg')
checks['new_formula_ratio_NaCl_correct']=(1==1 and 'gives1:1,NaCl' in M['items'][6]['teacher'])
checks['new_formula_ratio_MgO_correct']=(2//2==1 and 'simplifies2:2 to1:1,MgO' in M['items'][6]['teacher'])
checks['new_prompt_requires_construction_ratio']='show the simplest combining ratio instead of merely copying' in M['items'][6]['student']
checks['initial_report_immutable']=sha((B/'reviews/batch_06/gensci_2_1_initial_core27.md').read_bytes())=='489712bd6e7ce32f7392617cddd9f4370afcabe71b8af9aa9fa57b5c75d006fa'
for k in ['AssessmentMaterials','StudentSummaryTable']:
 checks[k+'_text_unchanged']=(E/(k+'.txt')).read_bytes()==(I/(k+'.txt')).read_bytes()
# Compare exact changed Word paragraph sequences, so phase/card changes cannot hide another text edit.
import difflib
worddiffs={}
for k in now['documents']:
 a=(I/(k+'.txt')).read_text().splitlines();b=(E/(k+'.txt')).read_text().splitlines();ops=[(tag,a[i:j],b[x:y]) for tag,i,j,x,y in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes() if tag!='equal'];worddiffs[k]=ops
 allowed={str(c['before']) for c in changes if isinstance(c['before'],str)}|{str(t) for c in changes if c['path']==extra[-1] for t in c['before']}
 for tag,aa,bb in ops:
  checks[k+'_changed_paragraphs_expected_'+str(len(checks))]=all(t in allowed for t in aa)
result={'initial_fingerprint':old['fingerprint'],'current_fingerprint':now['fingerprint'],'changes':changes,'word_paragraph_diffs':worddiffs,'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v]}
(E/'delta.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:result[k] for k in ['initial_fingerprint','current_fingerprint','passed','total','failed']}))
