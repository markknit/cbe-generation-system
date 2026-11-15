from pathlib import Path
from fractions import Fraction as F
import json,math
P=Path(__file__).resolve().parent
m=json.loads((P/'materials_snapshot.json').read_text());checks=[]
for c in m['calculations']:
 v=eval(c['expression'],{'__builtins__':{}},{})
 checks.append({'kind':'registered','id':c['id'],'independent_value':v,'expected':c['expected'],'pass':math.isclose(v,c['expected'],rel_tol=1e-12,abs_tol=1e-12)})
def multiply(p,q):
 r=[F(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):r[i+j]+=a*b
 return r
# Independently obtained factors; coefficients are ordered constant,x,x².
factors=[('common1',[0,3],[3,2],[0,9,6]),('common2',[0,1],[-5,1],[0,-5,1]),('common3',[0,-2],[-4,1],[0,8,-2]),('monic1',[2,1],[3,1],[6,5,1]),('monic2',[-3,1],[2,1],[-6,-1,1]),('squares',[-3,1],[3,1],[-9,0,1]),('repeated',[3,1],[3,1],[9,6,1]),('nonmonic1',[1,2],[3,1],[3,7,2]),('nonmonic2',[-2,3],[1,2],[-2,-1,6]),('formation1',[-2,1],[3,1],[-6,1,1]),('formationRepeated',[-3,1],[-3,1],[9,-6,1]),('rectangle15',[5,1],[-3,1],[-15,2,1]),('solve1',[-2,1],[-3,1],[6,-5,1]),('solveZero',[0,2],[-3,1],[0,-6,2]),('solveSquare',[-5,1],[5,1],[-25,0,1]),('solveRepeated',[2,1],[2,1],[4,4,1]),('rectangle36',[9,1],[-4,1],[-36,5,1]),('array20',[5,1],[-4,1],[-20,1,1]),('auditZero',[0,1],[-4,1],[0,-4,1]),('finalFactor',[-1,2],[3,1],[-3,5,2]),('finalFormation',[2,1],[-5,1],[-10,-3,1]),('finalSolve',[1,2],[-3,1],[-3,-5,2]),('final28',[7,1],[-4,1],[-28,3,1]),('final40',[8,1],[-5,1],[-40,3,1])]
for name,p,q,e in factors:
 v=multiply(p,q);checks.append({'kind':'coefficient_expansion','id':name,'independent_coefficients':list(map(str,v)),'expected_coefficients':e,'pass':v==list(map(F,e))})
# Both signs, zero, and repeated roots checked against original equations.
rootcases=[('CQE9A',[6,-5,1],[2,3]),('CQE9B',[0,-6,2],[0,3]),('CQE10A',[3,7,2],[F(-1,2),-3]),('CQE10B',[-25,0,1],[-5,5]),('CQE10C',[-15,2,1],[-5,3]),('CQE10D',[4,4,1],[-2]),('CQE11A',[-36,5,1],[-9,4]),('CQE11B',[-20,1,1],[-5,4]),('CQE12A',[-49,0,1],[-7,7]),('CQE12variation',[-64,0,1],[-8,8]),('CQE13B',[0,-4,1],[0,4]),('finalEquation',[-3,-5,2],[F(-1,2),3]),('final28',[-28,3,1],[-7,4]),('final40',[-40,3,1],[-8,5])]
for name,p,roots in rootcases:
 for r in roots:
  r=F(r);v=sum(F(c)*r**i for i,c in enumerate(p));checks.append({'kind':'root_substitution','id':name,'root':str(r),'residual':str(v),'pass':v==0})
(P/'independent_checks.json').write_text(json.dumps({'checks':checks,'passed':sum(c['pass'] for c in checks),'total':len(checks)},indent=2)+'\n')
assert all(c['pass'] for c in checks)
print(len(checks),'independent registered/coefficient/root checks PASS')
