from pathlib import Path
import json,ast,operator,re,math
O=Path(__file__).resolve().parent;B=O.parents[3];bank=json.loads((B/'materials/gensci_2_1.json').read_text());ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}
def calc(n):
 if isinstance(n,ast.Constant):return n.value
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calc(n.operand)
 if isinstance(n,ast.BinOp):return ops[type(n.op)](calc(n.left),calc(n.right))
 raise ValueError(n)
expected={'PT_NA_N':12,'PT_O_N':8,'PT_CA_N':20,'PT_MGF_CHARGE':0,'PT_CA_PHOS_CHARGE':0,'PT_AL_SULPH_CHARGE':0,'PT_FINAL_MG_N':12,'PT_FINAL_F_N':10,'PT_FINAL_AR_N':22,'PT_FINAL_PHOS_CHARGE':0,'PT_FINAL_NH3_H':0,'PT_FINAL_NH3_O':0};ar=[]
for c in bank['calculations']:
 v=calc(ast.parse(c['expression'],mode='eval').body);ar.append({**c,'evaluated':v,'independently_derived':expected[c['id']],'pass':v==c['expected']==expected[c['id']]})
assert len(ar)==12 and all(x['pass'] for x in ar)
def atoms(f):
 ts=re.findall(r'[A-Z][a-z]?|\d+|[()]',f);stack=[{}];j=0
 while j<len(ts):
  t=ts[j]
  if t=='(':stack.append({});j+=1;continue
  if t==')':d=stack.pop();j+=1
  else:d={t:1};j+=1
  k=int(ts[j]) if j<len(ts) and ts[j].isdigit() else 1
  if j<len(ts) and ts[j].isdigit():j+=1
  for a,n in d.items():stack[-1][a]=stack[-1].get(a,0)+n*k
 assert len(stack)==1;return stack[0]
def total(side):
 d={}
 for coeff,f in side:
  for a,n in atoms(f).items():d[a]=d.get(a,0)+coeff*n
 return d
raw=[('PT10_Mg',[(2,'Mg'),(1,'O2')],[(2,'MgO')]),('PT10_water',[(2,'H2'),(1,'O2')],[(2,'H2O')]),('PT10_salt',[(2,'Na'),(1,'Cl2')],[(2,'NaCl')]),('PT10_ammonia',[(1,'N2'),(3,'H2')],[(2,'NH3')]),('PT11_carbonate',[(1,'CaCO3')],[(1,'CaO'),(1,'CO2')]),('PT11_neutralisation',[(1,'HCl'),(1,'NaOH')],[(1,'NaCl'),(1,'H2O')]),('PT11_alumina',[(4,'Al'),(3,'O2')],[(2,'Al2O3')]),('PT11_hydroxide',[(1,'Ca(OH)2'),(2,'HCl')],[(1,'CaCl2'),(2,'H2O')]),('final_Ca',[(2,'Ca'),(1,'O2')],[(2,'CaO')]),('final_ammonia',[(4,'NH3'),(3,'O2')],[(2,'N2'),(6,'H2O')])]
eq=[]
for name,left,right in raw:
 coeffs=[c for c,f in left+right];x={'task':name,'left':left,'right':right,'left_atoms':total(left),'right_atoms':total(right),'balanced':total(left)==total(right),'coefficient_gcd':math.gcd(*coeffs)};assert x['balanced'] and x['coefficient_gcd']==1;eq.append(x)
ions=[]
for symbol,z,q in [('Na',11,1),('Mg',12,2),('Al',13,3),('F',9,-1),('O',8,-2),('Cl',17,-1),('K',19,1),('Ca',20,2)]:
 n=z-q;ions.append({'symbol':symbol,'protons':z,'charge':q,'electrons':n,'electron_change':-q,'shells':[2,8] if n==10 else [2,8,8]});assert n in [10,18]
r={'registered_arithmetic':ar,'independently_balanced_equations':eq,'ion_electron_conservation':ions,'all_pass':True};(O/'fixed_checks.json').write_text(json.dumps(r,indent=2)+'\n');print('12 arithmetic checks;10 equation conservation/GCD checks;8 ion-count checks PASS')
