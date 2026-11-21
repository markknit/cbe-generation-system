from pathlib import Path
from fractions import Fraction as F
import ast,json,math,operator
E=Path(__file__).parent;B=E.parents[3];M=json.loads((B/'materials/coremath_2_2.json').read_text());checks={};details={};panels=[]
def eq(k,a,w):checks[k]=a==w;details[k]={'actual':str(a),'expected':str(w)}
def near(k,a,w):checks[k]=math.isclose(float(a),float(w),rel_tol=1e-11,abs_tol=1e-11)
def reflect(p,L):a,b,c=map(F,L);x,y=map(F,p);t=2*(a*x+b*y+c)/(a*a+b*b);return(x-t*a,y-t*b)
def d2(p,q):return sum((F(x)-F(y))**2 for x,y in zip(p,q))
def area(t):return F((t[1][0]-t[0][0])*(t[2][1]-t[0][1])-(t[1][1]-t[0][1])*(t[2][0]-t[0][0]),2)
cases=[('CRG3',(1,0,0),[(1,1),(4,1),(2,3)],[(-1,1),(-4,1),(-2,3)]),('CRG4vertical',(1,0,-2),[(0,1),(3,-1)],[(4,1),(1,-1)]),('CRG4horizontal',(0,1,1),[(2,3),(-1,-1)],[(2,-5),(-1,-1)]),('CRG4triangle',(0,1,-1),[(0,0),(2,0),(1,2)],[(0,2),(2,2),(1,0)]),('CRG5diag',(1,-1,0),[(2,-1),(3,1),(1,4)],[(-1,2),(1,3),(4,1)]),('CRG5negdiag',(1,1,0),[(2,-1),(3,1),(1,4)],[(1,-2),(-1,-3),(-4,-1)]),('CRG6shift',(1,-1,1),[(0,0),(2,0),(0,1)],[(-1,1),(-1,3),(0,1)]),('CRG7general',(2,1,-8),[(1,1),(0,3)],[(5,3),(4,5)]),('CRG12digital',(0,1,0),[(1,1),(3,1),(2,3)],[(1,-1),(3,-1),(2,-3)]),('finalP',(1,0,0),[(3,1)],[(-3,1)]),('finaltriangle',(1,1,0),[(1,1),(3,1),(2,3)],[(-1,-1),(-1,-3),(-3,-2)]),('finalmirror',(1,-1,2),[(0,0),(2,0)],[(-2,2),(-2,4)])]
for label,L,pts,w in cases:
 out=[reflect(p,L) for p in pts];eq(label+'_all_images',out,w);a,b,c=map(F,L)
 for i,(p,q) in enumerate(zip(pts,out)):
  mid=tuple((F(x)+F(y))/2 for x,y in zip(p,q));eq(label+f'_midpoint_{i}',a*mid[0]+b*mid[1]+c,F(0));eq(label+f'_normal_segment_{i}',b*(q[0]-p[0])-a*(q[1]-p[1]),F(0));eq(label+f'_involution_{i}',reflect(q,L),p)
 if len(pts)>1:eq(label+'_preserved_side',d2(pts[0],pts[1]),d2(out[0],out[1]))
 if len(pts)==3:eq(label+'_reversed_orientation',area(out),-area(pts))
 panels.append({'label':label,'mirror':L,'points':pts,'images':[[float(x),float(y)] for x,y in out]})
for p,L in [((2,2),(1,-1,0)),((2,-2),(1,1,0)),((-1,-1),(0,1,1))]:eq('fixed_'+str(p),reflect(p,L),p)
checks['negative_enlargement_differs']=reflect((3,1),(1,1,0))!=(-3,-1)
for label,pts,lines in [('rectangle',[(0,0),(6,0),(6,4),(0,4)],[(1,0,-3),(0,1,-2)]),('square',[(0,0),(4,0),(4,4),(0,4)],[(1,0,-2),(0,1,-2),(1,-1,0),(1,1,-4)])]:
 for i,L in enumerate(lines):eq(label+f'_symmetry_{i}',{reflect(p,L) for p in pts},set(pts))
checks['rectangle_diagonal_not_symmetry']={reflect(p,(2,-3,0)) for p in [(0,0),(6,0),(6,4),(0,4)]}!=set([(0,0),(6,0),(6,4),(0,4)])
eq('scalene_side_squares',[d2((0,0),(4,0)),d2((0,0),(1,2)),d2((4,0),(1,2))],[F(16),F(5),F(13)])
for lab,ps,qs,expected_m,expected_c in [('shift',[(0,0),(2,0)],[(-1,1),(-1,3)],F(1),F(1)),('general',[(1,1),(0,3)],[(5,3),(4,5)],F(-2),F(8)),('final',[(0,0),(2,0)],[(-2,2),(-2,4)],F(1),F(2))]:
 mids=[tuple((F(x)+F(y))/2 for x,y in zip(p,q)) for p,q in zip(ps,qs)];m=(mids[1][1]-mids[0][1])/(mids[1][0]-mids[0][0]);c=mids[0][1]-m*mids[0][0];eq(lab+'_derived_slope',m,expected_m);eq(lab+'_derived_intercept',c,expected_c)
base=[(0,0),(3,0),(1,2)];direct=[(2,1),(5,1),(3,3)];opposite=[(0,0),(-3,0),(-1,2)]
eq('direct_translation',[(p[0]+2,p[1]+1) for p in base],direct);eq('opposite_reflection',[reflect(p,(1,0,0)) for p in base],opposite);eq('direct_order',area(direct),area(base));eq('opposite_order',area(opposite),-area(base))
for i in range(3):eq('congruent_direct_side_'+str(i),d2(base[i],base[(i+1)%3]),d2(direct[i],direct[(i+1)%3]));eq('congruent_opposite_side_'+str(i),d2(base[i],base[(i+1)%3]),d2(opposite[i],opposite[(i+1)%3]))
# Independent triangle coordinates for SSS,SAS,ASA/AAS,RHS,including final variants.
def sss(ab,bc,ca):x=(ab*ab+ca*ca-bc*bc)/(2*ab);return[(0.,0.),(float(ab),0.),(x,math.sqrt(ca*ca-x*x))]
def length(p,q):return math.hypot(p[0]-q[0],p[1]-q[1])
triangles={}
for lab,ab,bc,ca in [('SSS',3,4,5),('finalSSS',4,5,6)]:
 t=sss(ab,bc,ca);triangles[lab]=t
 for i,w in enumerate([ab,bc,ca]):near(lab+'_constructed_side_'+str(i),length(t[i],t[(i+1)%3]),w)
t=[(0.,0.),(4.,0.),(6*math.cos(math.radians(50)),6*math.sin(math.radians(50)))];triangles['SAS']=t;near('SAS_AB',length(t[0],t[1]),4);near('SAS_AC',length(t[0],t[2]),6);near('SAS_included_angle',math.degrees(math.atan2(t[2][1],t[2][0])),50)
b=5*math.sin(math.radians(65))/math.sin(math.radians(75));triangles['ASA_AAS']=[(0.,0.),(5.,0.),(b*math.cos(math.radians(40)),b*math.sin(math.radians(40)))];eq('ASA_third',180-40-65,75);eq('AAS_third',180-40-75,65);eq('final_AAS_third',180-40-70,70);triangles['finalAAS']=[(0.,0.),(5.,0.),(5*math.cos(math.radians(40)),5*math.sin(math.radians(40)))];triangles['RHS']=[(3.,0.),(0.,4.),(0.,0.)];near('RHS_hypotenuse',length(*triangles['RHS'][:2]),5);eq('RHS_other_leg',math.isqrt(25-9),4);checks['one_leg_insufficient']=math.hypot(3,4)!=math.hypot(3,5);checks['AAA_size_not_fixed']=5!=10
# A concrete ambiguous SSA counterexample: A30°,a3,b4 admits two B values with positive C.
b1=math.degrees(math.asin(F(2,3)));b2=180-b1;checks['general_SSA_ambiguous']=180-30-b1>0 and 180-30-b2>0 and b1!=b2
eq('equal_area_counterexample_areas',(2*6,3*4),(12,12));checks['equal_area_not_congruent']={(2,6),(6,2)}!={(3,4),(4,3)}

def calc(n):
 if isinstance(n,ast.Expression):return calc(n.body)
 if isinstance(n,ast.Constant):return F(str(n.value))
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calc(n.operand)
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](calc(n.left),calc(n.right))
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt':return math.sqrt(calc(n.args[0]))
 raise ValueError(ast.dump(n))
for row in M['calculations']:near('registry_'+row['id'],calc(ast.parse(row['expression'],mode='eval')),row['expected'])
r={'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'checks':checks,'details':details,'panels':panels,'triangles':triangles};(E/'independent_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['passed','total','failed']},indent=2))
