from pathlib import Path
from fractions import Fraction as F
import ast,json,math,operator
E=Path(__file__).parent;B=E.parents[3];M=json.loads((B/'materials/coremath_1_3.json').read_text());checks={};detail={}
def eq(k,a,w):checks[k]=a==w;detail[k]={'actual':str(a),'expected':str(w)}
def mul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
for k,a,b,w in [('C1rectangle',[0,1],[4,1],[0,4,1]),('C1difference',[1,1],[-1,1],[-1,0,1]),('C5common',[0,3],[3,2],[0,9,6]),('C5zero',[0,1],[-5,1],[0,-5,1]),('C5negative',[0,-2],[-4,1],[0,8,-2]),('C6positive',[2,1],[3,1],[6,5,1]),('C6mixed',[-3,1],[2,1],[-6,-1,1]),('C6difference',[-3,1],[3,1],[-9,0,1]),('C6repeated',[3,1],[3,1],[9,6,1]),('C7nonmonic',[1,2],[3,1],[3,7,2]),('C7mixed',[-2,3],[1,2],[-2,-1,6]),('C7common2',[-4,2],[2,1],[-8,0,2]),('C8formation',[-2,1],[3,1],[-6,1,1]),('C8repeat',[-3,1],[-3,1],[9,-6,1]),('C9monic',[-2,1],[-3,1],[6,-5,1]),('C9zero',[0,2],[-3,1],[0,-6,2]),('C10squares',[-5,1],[5,1],[-25,0,1]),('C10rearrange',[5,1],[-3,1],[-15,2,1]),('C10repeat',[2,1],[2,1],[4,4,1]),('C11rectangle',[9,1],[-4,1],[-36,5,1]),('C11array',[5,1],[-4,1],[-20,1,1]),('C13correct',[3,1],[3,1],[9,6,1]),('C13false',[3,1],[-3,1],[-9,0,1]),('C13zero',[0,1],[-4,1],[0,-4,1]),('I2factor',[-1,2],[3,1],[-3,5,2]),('I3formation',[2,1],[-5,1],[-10,-3,1]),('I3solve',[1,2],[-3,1],[-3,-5,2]),('I4context',[7,1],[-4,1],[-28,3,1]),('I4changed',[8,1],[-5,1],[-40,3,1])]:eq(k+'_full_coefficients',mul(a,b),list(map(F,w)))
# Exact discriminant-based reviewer check independently confirms completeness;not a proposed teaching method.
def roots(c,b,a):
 d=F(b*b-4*a*c)
 if d<0:return set()
 rn,rd=math.isqrt(d.numerator),math.isqrt(d.denominator);assert rn*rn==d.numerator and rd*rd==d.denominator
 s=F(rn,rd);return {(-F(b)+s)/(2*a),(-F(b)-s)/(2*a)}
rootcases=[('C8roots',-6,1,1,{F(2),F(-3)}),('C8repeated',9,-6,1,{F(3)}),('C8rectangle',-15,2,1,{F(-5),F(3)}),('C9monic',6,-5,1,{F(2),F(3)}),('C9zero',0,-6,2,{F(0),F(3)}),('C10nonmonic',3,7,2,{F(-1,2),F(-3)}),('C10squares',-25,0,1,{F(-5),F(5)}),('C10rearrange',-15,2,1,{F(-5),F(3)}),('C10repeat',4,4,1,{F(-2)}),('C11rectangle',-36,5,1,{F(-9),F(4)}),('C11array',-20,1,1,{F(-5),F(4)}),('C12square',-49,0,1,{F(-7),F(7)}),('C12changed',-64,0,1,{F(-8),F(8)}),('C13zero',0,-4,1,{F(0),F(4)}),('I3formation',-10,-3,1,{F(-2),F(5)}),('I3solve',-3,-5,2,{F(-1,2),F(3)}),('I4context',-28,3,1,{F(-7),F(4)}),('I4changed',-40,3,1,{F(-8),F(5)}),('C7no_real',1,0,1,set())]
for k,c,b,a,w in rootcases:
 eq(k+'_complete_roots',roots(c,b,a),w)
 for r in w:eq(k+'_substitution_'+str(r),a*r*r+b*r+c,F(0))
# Coefficient expansion of two-variable area identities.
def pmul(a,b):
 o={}
 for (i,j),x in a.items():
  for (u,v),y in b.items():o[i+u,j+v]=o.get((i+u,j+v),0)+x*y
 return {k:v for k,v in o.items() if v}
eq('area_square_plus_symbolic',pmul({(1,0):1,(0,1):1},{(1,0):1,(0,1):1}),{(2,0):1,(1,1):2,(0,2):1})
eq('area_square_minus_symbolic',pmul({(1,0):1,(0,1):-1},{(1,0):1,(0,1):-1}),{(2,0):1,(1,1):-2,(0,2):1})
eq('area_difference_symbolic',pmul({(1,0):1,(0,1):1},{(1,0):1,(0,1):-1}),{(2,0):1,(0,2):-1})
outer=mul([2,1],[5,1]);inner=mul([0,1],[3,1]);eq('border_full_coefficient_difference',[x-y for x,y in zip(outer,inner)],[10,4,0]);eq('border_solution',F(30-10,4),F(5));eq('border_original_check',7*10-5*8,30)
for k,x,y,w in [('squareplus',4,2,36),('squareminus',5,-2,9),('numeric102',100,2,10404),('numeric98',100,-2,9604),('numeric2point5',F(2),F(1,2),F(25,4)),('final99',100,-1,9801)]:eq(k+'_cross_terms',x*x+2*x*y+y*y,w);eq(k+'_direct',(x+y)**2,w)
eq('difference51x49',51*49,2499);eq('missing_cross_counterexample',(1+1)**2-(1**2+1**2),2)
for k,rs in [('C11rectangle',{F(-9),F(4)}),('C11array',{F(-5),F(4)}),('I4context',{F(-7),F(4)}),('I4changed',{F(-8),F(5)})]:eq(k+'_positive_selection',{r for r in rs if r>0},{F(5) if k=='I4changed' else F(4)})
eq('rectangle_check',4*9,36);eq('array_check',4*5,20);eq('final_context_units_check',4*7,28);eq('final_changed_units_check',5*8,40);eq('nonzero_rhs_counterexample',(2-2)*(2+3),0);checks['nonzero_rhs_not_satisfied']=(2-2)*(2+3)!=7

def calc(n):
 if isinstance(n,ast.Expression):return calc(n.body)
 if isinstance(n,ast.Constant):return F(str(n.value))
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calc(n.operand)
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](calc(n.left),calc(n.right))
 raise ValueError(ast.dump(n))
for row in M['calculations']:checks['registry_'+row['id']]=math.isclose(float(calc(ast.parse(row['expression'],mode='eval'))),row['expected'],rel_tol=1e-13,abs_tol=1e-14)
r={'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'checks':checks,'detail':detail,'note':'Whole coefficient identities,complete exact root sets,area/model reasoning and28registry checked;geometric construction/domain/exploration tasks fully solved in solutions.md.'};(E/'independent_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['passed','total','failed']},indent=2))
