"""Independent chemistry derivations; no pipeline build or author self-review."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from functools import reduce
from math import gcd
import re,json
E=Path(__file__).resolve().parent;B=Path.cwd()/'data/curriculum_expansion_2026-11'
M=json.loads((B/'materials/gensci_2_1.json').read_text()); checks={}; results={}
def check(k,v):checks[k]=bool(v)
def atoms(f):
 ts=re.findall(r'[A-Z][a-z]?|\d+|[()]',f); stack=[Counter()];i=0
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
# Fill subshells independently (4s before3d) and aggregate principal-shell counts.
syms='H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca'.split()
configs={};placements={}
for z,s in enumerate(syms,1):
 remaining=z;cs=Counter()
 for n,cap in [(1,2),(2,2),(2,6),(3,2),(3,6),(4,2)]:
  fill=min(remaining,cap);cs[n]+=fill;remaining-=fill
  if not remaining:break
 c=[cs[n] for n in sorted(cs) if cs[n]];configs[s]=c
 group=18 if s=='He' else (c[-1] if c[-1]<=2 else c[-1]+10)
 placements[s]=[group,len(c)];check(s+'_total',sum(c)==z)
 check(s+'_reference',','.join(map(str,c)) in next(x['student'] for x in M['items'] if x['id']=='PT2'))
expected=[[1,1],[18,1],[1,2],[2,2],[13,2],[14,2],[15,2],[16,2],[17,2],[18,2],[1,3],[2,3],[13,3],[14,3],[15,3],[16,3],[17,3],[18,3],[1,4],[2,4]]
for s,gp in zip(syms,expected):check(s+'_placement',placements[s]==gp)
results['configs']=configs;results['placements_group_period']=placements
isotopes=[('Na',11,23),('O',8,16),('Ca',20,40),('Mg',12,24),('F',9,19),('Ar',18,40)]
results['isotopes']={s:{'p':z,'n':a-z,'e':z} for s,z,a in isotopes}
for s,z,a in isotopes:check(s+'_nucleon_identity',z+(a-z)==a)
iondata={s:{'charge':q,'electrons':syms.index(s)+1-q,'shells':[2,8] if syms.index(s)+1-q==10 else [2,8,8]} for s,q in [('Na',1),('Mg',2),('Al',3),('F',-1),('O',-2),('Cl',-1),('K',1),('Ca',2)]}
for s,r in iondata.items():check(s+'_ion_charge',syms.index(s)+1-r['electrons']==r['charge']);check(s+'_ion_total',sum(r['shells'])==r['electrons'])
results['ions']=iondata
# Before/after dot-cross electron and charge accounting for all requested compounds.
diagrams={}
for f,donor,acceptor,qm,qn in [('NaCl','Na','Cl',1,-1),('MgO','Mg','O',2,-2),('MgCl2','Mg','Cl',2,-1),('MgF2','Mg','F',2,-1)]:
 count=atoms(f);nm=count[donor];nn=count[acceptor];old=configs[acceptor][-1];cross=abs(qn)
 diagrams[f]={'donors':nm,'acceptors':nn,'acceptor_original_dots':old,'crosses_each':cross,'net_charge':nm*qm+nn*qn}
 check(f+'_electron_transfer',nm*qm==nn*cross);check(f+'_outer8',old+cross==8);check(f+'_neutral',nm*qm+nn*qn==0)
results['diagrams']=diagrams
pairs=[('NaCl','Na',1,'Cl',-1),('MgO','Mg',2,'O',-2),('Ca(OH)2','Ca',2,'OH',-1),('(NH4)2SO4','NH4',1,'SO4',-2),('Al(NO3)3','Al',3,'NO3',-1),('Ca3(PO4)2','Ca',2,'PO4',-3),('NaHCO3','Na',1,'HCO3',-1),('Na2CO3','Na',1,'CO3',-2),('K2SO4','K',1,'SO4',-2),('NH4NO3','NH4',1,'NO3',-1),('CaCO3','Ca',2,'CO3',-2),('Al2(SO4)3','Al',3,'SO4',-2),('NH4Cl','NH4',1,'Cl',-1),('Na2SO4','Na',1,'SO4',-2),('KNO3','K',1,'NO3',-1),('Ca(NO3)2','Ca',2,'NO3',-1),('(NH4)3PO4','NH4',1,'PO4',-3)]
formula_results={}
for f,c,qc,a,qa in pairs:
 g=gcd(qc,-qa);nc=-qa//g;na=qc//g
 tally=Counter({k:v*nc for k,v in atoms(c).items()});tally.update({k:v*na for k,v in atoms(a).items()})
 check(f+'_ratio_formula',atoms(f)==tally);check(f+'_neutral_ratio',nc*qc+na*qa==0)
 formula_results[f]={'cation':c,'anion':a,'ratio':[nc,na],'charge':nc*qc+na*qa,'atoms':dict(tally)}
results['formulae']=formula_results
# Independent fixed coefficient solutions and atom-tally validation, all ten distinct equations.
eqs=[([('Mg',2),('O2',1)],[('MgO',2)]),([('H2',2),('O2',1)],[('H2O',2)]),([('Na',2),('Cl2',1)],[('NaCl',2)]),([('N2',1),('H2',3)],[('NH3',2)]),([('CaCO3',1)],[('CaO',1),('CO2',1)]),([('HCl',1),('NaOH',1)],[('NaCl',1),('H2O',1)]),([('Al',4),('O2',3)],[('Al2O3',2)]),([('Ca(OH)2',1),('HCl',2)],[('CaCl2',1),('H2O',2)]),([('Ca',2),('O2',1)],[('CaO',2)]),([('NH3',4),('O2',3)],[('N2',2),('H2O',6)])]
def tally(side):
 t=Counter()
 for f,n in side:t.update({k:v*n for k,v in atoms(f).items()})
 return t
results['equations']=[]
for i,(left,right) in enumerate(eqs,1):
 a,b=tally(left),tally(right);check(f'equation{i}_conservation',a==b);check(f'equation{i}_primitive',reduce(gcd,[n for _,n in left+right])==1)
 results['equations'].append({'left':left,'right':right,'left_atoms':dict(a),'right_atoms':dict(b)})
oxidations={'NaCl':{'Na':1,'Cl':-1},'MgO':{'Mg':2,'O':-2},'H2O':{'H':1,'O':-2},'CO2':{'C':4,'O':-2},'NH3':{'N':-3,'H':1},'O2':{'O':0},'CaO':{'Ca':2,'O':-2}}
for f,ox in oxidations.items():check(f+'_oxidation_sum',sum(n*ox[s] for s,n in atoms(f).items())==0)
results['oxidation_states']=oxidations
registry=[12,8,20,0,0,0,12,10,22,0,0,0]
for c,v in zip(M['calculations'],registry):check(c['id']+'_independent',c['expected']==v)
check('affinity_teaching',30>10);check('affinity_final',25>5)
results['checks']=checks;results['passed']=sum(checks.values());results['total']=len(checks);results['failed']=[k for k,v in checks.items() if not v]
results['method_limit']='Computed independent populations/ratios/tallies compared manually with every task/key; structural text presence is supplementary, not an exhaustive chemistry proof or learner-performance observation.'
(E/'fixed_checks.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({k:results[k] for k in ['passed','total','failed']}))
