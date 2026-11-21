from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,ROUND_HALF_UP
import ast,json,math,operator
E=Path(__file__).parent;B=E.parents[3];M=json.loads((B/'materials/coremath_1_2.json').read_text());checks={};detail={}
def eq(k,a,w):checks[k]=a==w;detail[k]={'actual':str(a),'expected':str(w)}
def near(k,a,w):checks[k]=math.isclose(float(a),float(w),rel_tol=1e-12,abs_tol=1e-13);detail[k]={'actual':str(a),'expected':str(w)}
for k,a,w in [('8',2**3,8),('27',3**3,27),('64base2',2**6,64),('64base4',4**3,64),('64base8',8**2,64),('1000',10**3,1000),('3pow4',3**4,81),('3times4',3*4,12),('C2product',2**3*2**2,32),('C2quotient',F(3**5,3**2),27),('C2nested',(2**3)**2,64),('C2powerproduct',(2*3)**2,36),('C2sum',2**2+2**3,12),('C3zeroquotient',F(3**2,3**2),1),('C3negquotient',F(2**2,2**5),F(1,8)),('C3zero',5**0,1),('C3negative',F(1,2**3),F(1,8)),('C3tenneg',F(1,10**2),F(1,100)),('C3fourneg',F(1,4),F(1,4)),('C5A',2**3*3**2,72),('C5B',2**3+2**2,12),('C5C',(2+3)**2,25),('C5D',(2**2)**3,64),('C5E',2**(2**3),256),('C5F',(-2)**2,4),('C5G',-(2**2),-4),('C5invalidsum',2**2+3**2,13),('I1decimal',F(1,10**3),F('.001')),('I1fraction',F(1,2**5),F(1,32)),('I1product',3**2*3**3,243),('I1quotient',F(3**5,3**2),27)]:eq(k,a,w)
for x,n,r,m,w in [(16,2,4,1,4),(27,3,3,2,9),(81,2,9,-1,F(1,9)),(32,5,2,2,4)]:eq(f'root_{x}_integer_check',r**n,x);eq(f'root_{x}_power',F(r)**m,w)
logs=[(1,'0'),(2,'0.3010'),(3,'0.4771'),(4,'0.6021'),(5,'0.6990'),(6,'0.7782'),(7,'0.8451'),(8,'0.9031'),(9,'0.9542'),(10,'1')]
for x,w in logs:near('logtable_'+str(x),float(f'{math.log10(x):.4f}'),D(w))
for x,w in [(2,'.3010'),(3,'.4771'),(5,'.6990'),(7,'.8451'),(8,'.9031')]:near('final_logtable_'+str(x),float(f'{math.log10(x):.4f}'),D(w))
for u,w in [('0.7781','5.999'),('0.3010','2.000'),('0.4771','3.000'),('0.6990','5.000'),('0.9030','7.998'),('0.2386','1.732'),('0.0791','1.200'),('0.5441','3.500'),('0.3979','2.500'),('0.9542','8.999'),('0.3495','2.236')]:eq('antilog_table_'+u,format(10**float(u),'#.4g'),w)
for x,u in [(1000,3),(1,0),(.01,-2),(math.sqrt(10),.5),(.1,-1)]:near('notation_'+str(x),math.log10(x),u);near('notation_inverse_'+str(x),10**u,x)
for x,u in [(0,None),(-1,None)]:
 try:math.log10(x);checks['log_domain_'+str(x)]=False
 except ValueError:checks['log_domain_'+str(x)]=True
for k,a,w in [('log70',D('.8451')+1,D('1.8451')),('logPoint007',D('.8451')-3,D('-2.1549')),('log200',D('.3010')+2,D('2.3010')),('logPoint02',D('.3010')-2,D('-1.6990')),('product',D('.3010')+D('.4771'),D('.7781')),('scaledproduct',D('1.3010')+D('2.4771'),D('3.7781')),('quotient',D('1.4771')-D('.6990'),D('.7781')),('negativequotient',D('2.4771')-D('-.3010'),D('2.7781')),('power',3*D('.3010'),D('.9030')),('root',D('.4771')/2,D('.23855')),('combined',D('1.3010')+D('2.4771')-D('.6990'),D('3.0791')),('finalproduct',D('.8451')+D('.6990'),D('1.5441')),('finalquotient',D('1.3010')-D('.9031'),D('.3979')),('finalpower',2*D('.4771'),D('.9542')),('finalroot',D('.6990')/2,D('.3495'))]:eq(k,a,w)
eq('root_intermediate_round',D('.23855').quantize(D('.0001'),rounding=ROUND_HALF_UP),D('.2386'));eq('cuberoot_log_round',(D('.9031')/3).quantize(D('.0001'),rounding=ROUND_HALF_UP),D('.3010'))
for k,x,w in [('C9product',5.999,'6.00'),('C9scaled',5999,'6.00e+03'),('C10quotient',5.999,'6.00'),('C10scaled',599.9,'600.'),('C11power',7.998,'8.00'),('C11sqrt',1.732,'1.73'),('C11cube',2.000,'2.00'),('C12combined',1200,'1.20e+03'),('I3product',35.00,'35.0'),('I3quotient',2.500,'2.50'),('I4power',8.999,'9.00'),('I4root',2.236,'2.24')]:eq(k+'_3sf',format(x,'#.3g'),w)
for x,y in [(2,3),(20,300),(30,5),(300,.5),(7,5),(20,8)]:near(f'actual_log_product_identity_{x}_{y}',math.log10(x*y),math.log10(x)+math.log10(y));near(f'actual_log_quotient_identity_{x}_{y}',math.log10(x/y),math.log10(x)-math.log10(y))
for x,r in [(2,3),(3,.5),(8,F(1,3)),(3,2),(5,.5)]:near(f'actual_log_power_root_identity_{x}_{r}',math.log10(x**r),float(r)*math.log10(x))
for x in [2,.02,7]:eq('actual_device_log_'+str(x),round(math.log10(x),10),{2:.3010299957,.02:-1.6989700043,7:.8450980400}[x])
near('actual_device_inverse',10**.3010,1.9998618696327441)
def calc(n):
 if isinstance(n,ast.Expression):return calc(n.body)
 if isinstance(n,ast.Constant):return F(str(n.value))
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calc(n.operand)
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](calc(n.left),calc(n.right))
 raise ValueError(ast.dump(n))
for row in M['calculations']:near('registry_'+row['id'],calc(ast.parse(row['expression'],mode='eval')),row['expected'])
r={'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'checks':checks,'detail':detail,'note':'Table logs checked by actual log10, inverse rows by10**u;exact factor/domain derivations and meaningful method-choice tasks separately worked in solutions.md.37registry arithmetic checks alone do not prove log setup.'};(E/'independent_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['passed','total','failed']},indent=2))
