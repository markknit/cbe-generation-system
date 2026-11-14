from pathlib import Path
from fractions import Fraction as F
import ast,json,math,operator
E=Path(__file__).parent;B=E.parents[3];M=json.loads((B/'materials/coremath_1_1.json').read_text());checks={};details={}
def record(k,actual,expected):checks[k]=actual==expected;details[k]={'actual':str(actual),'expected':str(expected)}
for task,values,parity,kind in [('CRN1',[0,1,2,3,4,9,11,15,21],['even','odd','even','odd','even','odd','odd','odd','odd'],['neither','neither','prime','prime','composite','composite','prime','composite','composite']),('I1',[0,1,2,9,17,25],['even','odd','even','odd','odd','odd'],['neither','neither','prime','composite','prime','composite'])]:
 for n,p,k in zip(values,parity,kind):
  factors=[x for x in range(1,n+1) if n%x==0];record(f'{task}_{n}_parity','even' if n%2==0 else 'odd',p);record(f'{task}_{n}_divisors','neither' if n<2 else ('prime' if len(factors)==2 else 'composite'),k)
for n,want in [(9,[(1,9),(3,3)]),(15,[(1,15),(3,5)])]:record(f'CRN1_{n}_pairs',[(x,n//x) for x in range(1,math.isqrt(n)+1) if n%x==0],want)
for s,want in [('3.0','0.3333'),('3.1','0.3226'),('3.2','0.3125'),('3.3','0.3030'),('3.4','0.2941'),('3.5','0.2857'),('3.6','0.2778'),('3.7','0.2703'),('3.8','0.2632'),('3.9','0.2564'),('4.0','0.2500'),('4.2','0.2381'),('4.8','0.2083')]:record('table_'+s,format(float(1/F(s)),'#.4g'),want)
recips=[('C3_4',F(4),F(1,4)),('C3_neg5',F(-5),F(-1,5)),('C3_2thirds',F(2,3),F(3,2)),('C4_mixed',F(3,2),F(2,3)),('C4_negmixed',F(-5,2),F(-2,5)),('C4_quarter',F(1,4),F(4)),('C4_negdecimal',F(-2,5),F(-5,2)),('C4_ninth',F(1,9),F(9)),('C6_3point6',F(18,5),F(5,18)),('C6_neg2point5',F(-5,2),F(-2,5)),('C6_2thirds',F(2,3),F(3,2)),('I2_negmixed',F(-7,4),F(-4,7)),('I2_3fifths',F(3,5),F(5,3))]
for k,x,w in recips:record(k+'_reciprocal',1/x,w);record(k+'_product',x*w,F(1))
for n,w in [(2,'0.7071'),(5,'0.4472')]:record('root_'+str(n)+'_4sf',format(1/math.sqrt(n),'.4g'),w);checks['root_'+str(n)+'_product']=math.isclose(math.sqrt(n)*(1/math.sqrt(n)),1,rel_tol=1e-15)
try:1/F(0);checks['zero_no_reciprocal']=False
except ZeroDivisionError:checks['zero_no_reciprocal']=True
for s,w in [('32',F(1,32)),('.32',F(25,8)),('.036',F(250,9)),('.42',F(50,21))]:record('scaling_'+s,1/F(s),w)
for k,a,d,w in [('portions',F(9,2),F(3,4),F(6)),('strip',F(12,5),F(3,10),F(8)),('signeddivision',F(-3,5),F(2,7),F(-21,10)),('finalportions',F(7,2),F(7,8),F(4))]:record(k,a/d,w);record(k+'_reverse',w*d,a)
def calc(node):
 if isinstance(node,ast.Expression):return calc(node.body)
 if isinstance(node,ast.Constant):return F(str(node.value))
 if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -calc(node.operand)
 if isinstance(node,ast.BinOp):return {ast.Div:operator.truediv,ast.Mult:operator.mul,ast.Add:operator.add,ast.Sub:operator.sub}[type(node.op)](calc(node.left),calc(node.right))
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='sqrt' and len(node.args)==1:return math.sqrt(calc(node.args[0]))
 raise ValueError(ast.dump(node))
for row in M['calculations']:
 actual=float(calc(ast.parse(row['expression'],mode='eval')));checks['registry_'+row['id']]=math.isclose(actual,row['expected'],rel_tol=1e-13,abs_tol=1e-14)
result={'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'checks':checks,'details':details,'note':'Rational/irrational classifications and all explanation/advice/model tasks are independently reasoned in solutions.md, not inferred from numerical registry.'};(E/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['passed','total','failed']},indent=2))
