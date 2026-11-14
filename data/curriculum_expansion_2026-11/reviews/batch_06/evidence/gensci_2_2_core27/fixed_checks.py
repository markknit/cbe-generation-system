from pathlib import Path
from collections import Counter
from functools import reduce
from math import gcd
import json,re
E=Path(__file__).resolve().parent;B=Path.cwd()/'data/curriculum_expansion_2026-11';M=json.loads((B/'materials/gensci_2_2.json').read_text());N=json.loads((B/'manuscripts/gensci_2_2.json').read_text());P=json.loads((B/'blueprints/gensci_2_2.json').read_text());C={};R={}
def ck(k,v):C[k]=bool(v)
def atoms(f):
 ts=re.findall(r'[A-Z][a-z]?|\d+|[()]',f);stack=[Counter()];i=0
 while i<len(ts):
  t=ts[i];i+=1
  if t=='(':stack.append(Counter());continue
  if t==')':q=stack.pop()
  else:q=Counter({t:1})
  n=1
  if i<len(ts) and ts[i].isdigit():n=int(ts[i]);i+=1
  stack[-1].update({k:v*n for k,v in q.items()})
 assert len(stack)==1
 return stack[0]
# Independent periodic group classification, including exceptions and residual set.
syms='H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca'.split();groups=[1,18,1,2,13,14,15,16,17,18,1,2,13,14,15,16,17,18,1,2];bins={k:[] for k in ['alkali','alkaline_earth','halogen','noble','other']}
for s,g in zip(syms,groups):
 family=({1:'alkali',2:'alkaline_earth',17:'halogen',18:'noble'}).get(g,'other') if s!='H' else 'other';bins[family].append(s)
expected={'alkali':['Li','Na','K'],'alkaline_earth':['Be','Mg','Ca'],'halogen':['F','Cl'],'noble':['He','Ne','Ar'],'other':['H','B','C','N','O','Al','Si','P','S']}
for k in bins:ck(k+'_exact_members',bins[k]==expected[k])
ck('all_twenty_once',Counter(sum(bins.values(),[]))==Counter(syms));ck('no_first20_transition',all(g not in range(3,13) for g in groups));R['family_sort']=bins
for s,g,block,trans in [('Fe',8,'d',True),('Cu',11,'d',True),('Zn',12,'d',False),('Pb',14,'p',False)]:R[s]={'group':g,'block':block,'transition_under_stated_atom_common_cation_criterion':trans}
# Complete atom counts for every distinct fixed equation, both teaching and held-out final.
eqs=[('Na_water',[('Na',2),('H2O',2)],[('NaOH',2),('H2',1)]),('Na_oxygen_rich',[('Na',2),('O2',1)],[('Na2O2',1)]),('Mg_oxygen',[('Mg',2),('O2',1)],[('MgO',2)]),('Mg_steam',[('Mg',1),('H2O',1)],[('MgO',1),('H2',1)]),('Mg_HCl',[('Mg',1),('HCl',2)],[('MgCl2',1),('H2',1)]),('Cl_water_equilibrium',[('Cl2',1),('H2O',1)],[('HCl',1),('HClO',1)])]
def tally(side):
 t=Counter()
 for f,n in side:t.update({k:v*n for k,v in atoms(f).items()})
 return t
R['equations']={}
for name,left,right in eqs:
 a,b=tally(left),tally(right);ck(name+'_all_atoms_conserved',a==b);ck(name+'_primitive',reduce(gcd,[n for _,n in left+right])==1);R['equations'][name]={'left':left,'right':right,'left_atoms':dict(a),'right_atoms':dict(b)}
for x in M['calculations']:ck(x['id']+'_independent_zero',x['expected']==0)
for l in N['lessons']:
 ck('L'+str(l['number'])+'_mapping_agrees',l['outcomes']==P['lesson_map'][l['number']-1]['outcomes'])
 for id in l['outcomes']:ck('L'+str(l['number'])+'_known_outcome_'+id,id in 'abcde')
ck('final_timing_5_8_8_12_7',N['lessons'][-1]['minutes']==[5,8,8,12,7]);ck('rubric_links_1to4',[q['tasks'] for q in P['rubric_links']]==[['I1'],['I2'],['I3'],['I4']]);ck('source_performance_scope_explicit','unperformed' in P['performance_evidence']['chemical']);ck('final_no_performance_claim','not certified' in N['assessment']['instructions'])
R['checks']=C;R['passed']=sum(C.values());R['total']=len(C);R['failed']=[k for k,v in C.items() if not v];R['method_limit']='Supplementary fixed classification/tally/structure checks; conditions,uses,safety,open explanations and partial-outcome scope independently reviewed in report. No practical performance observed.'
(E/'fixed_checks.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps({k:R[k] for k in ['passed','total','failed']}))
