from pathlib import Path
from fractions import Fraction as F
import ast,json,math,operator,itertools
E=Path(__file__).parent;B=E.parents[3];M=json.loads((B/'materials/coremath_2_3.json').read_text());checks={};details={};panels=[]
def eq(k,a,w):checks[k]=a==w;details[k]={'actual':str(a),'expected':str(w)}
def near(k,a,w):checks[k]=math.isclose(float(a),float(w),rel_tol=1e-11,abs_tol=1e-11)
def turn(p,o,deg):
 x,y=(F(p[i])-F(o[i]) for i in range(2));t=(deg//90)%4;x,y=[(x,y),(-y,x),(-x,-y),(y,-x)][t];return x+F(o[0]),y+F(o[1])
def d2(p,q):return sum((F(x)-F(y))**2 for x,y in zip(p,q))
def area(t):return F((t[1][0]-t[0][0])*(t[2][1]-t[0][1])-(t[1][1]-t[0][1])*(t[2][0]-t[0][0]),2)
cases=[('CRT2ccw',(0,0),90,[(1,1),(3,1),(1,2)],[(-1,1),(-1,3),(-2,1)]),('CRT2cw',(0,0),-90,[(1,1),(3,1),(1,2)],[(1,-1),(1,-3),(2,-1)]),('CRT3half',(0,0),180,[(1,2),(-2,3),(0,-1)],[(-1,-2),(2,-3),(0,1)]),('CRT4',(1,1),90,[(2,1),(4,1),(2,3)],[(1,2),(1,4),(-1,2)]),('CRT5',(1,1),90,[(2,1),(3,1),(2,2)],[(1,2),(1,3),(0,2)]),('CRT6',(3,3),180,[(1,2),(2,5),(0,3)],[(5,4),(4,1),(6,3)]),('CRT10',(0,0),90,[(0,0),(3,0),(1,2)],[(0,0),(0,3),(-2,1)]),('CRT11',(0,0),-90,[(1,0),(3,0),(1,2)],[(0,-1),(0,-3),(2,-1)]),('finalI1',(0,0),-90,[(1,0),(3,0),(1,2)],[(0,-1),(0,-3),(2,-1)]),('finalI2',(1,2),90,[(1,0),(2,1)],[(3,2),(2,3)])]
for label,o,ang,pts,w in cases:
 out=[turn(p,o,ang) for p in pts];eq(label+'_all_images',out,w)
 for i,(p,q) in enumerate(zip(pts,out)):eq(label+f'_radius2_{i}',d2(p,o),d2(q,o));eq(label+f'_inverse_{i}',turn(q,o,-ang),p)
 for i in range(len(pts)):
  for j in range(i):eq(label+f'_side2_{i}_{j}',d2(pts[i],pts[j]),d2(out[i],out[j]))
 if len(pts)==3:eq(label+'_labelled_orientation',area(out),area(pts))
 panels.append({'label':label,'centre':o,'angle':ang,'points':pts,'images':[[float(x),float(y)] for x,y in out]})
for ang in [0,360,720]:eq('identity_'+str(ang),turn((1,2),(4,5),ang),(F(1),F(2)))
eq('450_equals90',turn((1,2),(0,0),450),turn((1,2),(0,0),90));eq('270_equalsCW90',turn((1,2),(0,0),270),turn((1,2),(0,0),-90));checks['90_differs270_noncentre']=turn((1,2),(0,0),90)!=turn((1,2),(0,0),270)
def bisector(p,q):a,b=(F(q[i])-F(p[i]) for i in range(2));c=(sum(F(x)**2 for x in q)-sum(F(x)**2 for x in p))/2;return a,b,c
def intersection(l,m):a,b,c=l;d,e,f=m;det=a*e-b*d;return ((c*e-b*f)/det,(a*f-c*d)/det)
for lab,pts,out,indices,w in [('CRT5',[(2,1),(3,1),(2,2)],[(1,2),(1,3),(0,2)],(0,2),(F(1),F(1))),('finalI2',[(1,0),(2,1)],[(3,2),(2,3)],(0,1),(F(1),F(2)))]:
 lines=[bisector(p,q) for p,q in zip(pts,out)];o=intersection(lines[indices[0]],lines[indices[1]]);eq(lab+'_derived_centre',o,w)
 for i,(p,q,L) in enumerate(zip(pts,out,lines)):
  eq(lab+f'_bisector_centre_check_{i}',L[0]*o[0]+L[1]*o[1],L[2]);u=[F(p[j])-o[j] for j in range(2)];v=[F(q[j])-o[j] for j in range(2)];near(lab+f'_derived_directed_angle_{i}',math.degrees(math.atan2(u[0]*v[1]-u[1]*v[0],u[0]*v[0]+u[1]*v[1]))%360,90)
for i,(p,q) in enumerate(zip([(1,2),(2,5),(0,3)],[(5,4),(4,1),(6,3)])):eq('CRT6_midpoint_'+str(i),tuple((F(x)+F(y))/2 for x,y in zip(p,q)),(F(3),F(3)))
for n,deg in [(2,60),(4,120)]:near('clock_angle_'+str(n),n*360/12,deg);near('clock_radius_'+str(n),math.sin(math.radians(deg))**2+math.cos(math.radians(deg))**2,1)
# Finite plane orders as vertex-set permutations, with the full turn counted once.
def rot2(p,deg):a=math.radians(deg);return(p[0]*math.cos(a)-p[1]*math.sin(a),p[0]*math.sin(a)+p[1]*math.cos(a))
def rounded(v):return tuple(round(float(x),8) for x in v)
def invariant(points,deg):return {rounded(rot2(p,deg)) for p in points}=={rounded(p) for p in points}
plane={'rectangle':[(-3,-2),(3,-2),(3,2),(-3,2)],'square':[(-1,-1),(1,-1),(1,1),(-1,1)]}
for n,lab in [(3,'equilateral'),(5,'pentagon'),(6,'hexagon')]:plane[lab]=[(math.cos(2*math.pi*j/n),math.sin(2*math.pi*j/n)) for j in range(n)]
for lab,n in [('rectangle',2),('square',4),('equilateral',3),('pentagon',5),('hexagon',6)]:checks[lab+'_matching_minimum']=invariant(plane[lab],360/n);checks[lab+'_half_minimum_not_matching']=not invariant(plane[lab],180/n)
eq('scalene_unequal_side_squares',{d2((0,0),(4,0)),d2((4,0),(1,2)),d2((1,2),(0,0))},{F(16),F(5),F(13)})
# Independent3D Rodrigues rotations permute vertices;permutation cycle lcm gives exact finite order.
def rotate3(v,axis,deg):
 length=math.sqrt(sum(x*x for x in axis));a=[x/length for x in axis];co,si=math.cos(math.radians(deg)),math.sin(math.radians(deg));dot=sum(x*y for x,y in zip(a,v));cross=(a[1]*v[2]-a[2]*v[1],a[2]*v[0]-a[0]*v[2],a[0]*v[1]-a[1]*v[0]);return tuple(v[i]*co+cross[i]*si+a[i]*dot*(1-co) for i in range(3))
def perm_order(pts,axis,deg):
 idx={rounded(p):i for i,p in enumerate(pts)};perm=[idx[rounded(rotate3(p,axis,deg))] for p in pts];visited=set();lengths=[]
 for i in range(len(pts)):
  if i in visited:continue
  j=i;c=0
  while j not in visited:visited.add(j);c+=1;j=perm[j]
  lengths.append(c)
 return math.lcm(*lengths),perm
cube=list(itertools.product([-1,1],repeat=3));tetra=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)];pyr=[(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0),(0,0,2)];prism=[(math.cos(2*math.pi*j/3),math.sin(2*math.pi*j/3),z) for z in [-1,1] for j in range(3)];solidchecks={}
for lab,pts,axis,n in [('cube_face',cube,(0,0,1),4),('cube_vertex',cube,(1,1,1),3),('cube_edge',cube,(1,1,0),2),('tetra_vertex_face',tetra,(1,1,1),3),('tetra_opposite_edge',tetra,(1,0,0),2),('pyramid',pyr,(0,0,1),4),('triangular_prism',prism,(0,0,1),3)]:
 order,perm=perm_order(pts,axis,360/n);eq(lab+'_vertex_permutation_order',order,n);solidchecks[lab]={'axis':axis,'angle':360/n,'permutation':perm,'order':order}
eq('cube_face_axis_count',6//2,3);eq('cube_vertex_axis_count',len(cube)//2,4);edges=[(a,b) for i,a in enumerate(cube) for b in cube[i+1:] if sum((x-y)**2 for x,y in zip(a,b))==4];eq('cube_edge_axis_count',len(edges)//2,6)
base=[(0,0),(3,0),(1,2)];reflection=[(0,0),(-3,0),(-1,2)];eq('reflected_opposite_orientation',area(reflection),-area(base));eq('final_SAS_sides',[d2((1,0),(3,0)),d2((1,0),(1,2))],[F(4),F(4)]);eq('final_SAS_perpendicular',(3-1)*(1-1)+(0-0)*(2-0),0)

def calc(n):
 if isinstance(n,ast.Expression):return calc(n.body)
 if isinstance(n,ast.Constant):return F(str(n.value))
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calc(n.operand)
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](calc(n.left),calc(n.right))
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt':return math.sqrt(calc(n.args[0]))
 raise ValueError(ast.dump(n))
for row in M['calculations']:near('registry_'+row['id'],calc(ast.parse(row['expression'],mode='eval')),row['expected'])
r={'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'checks':checks,'details':details,'panels':panels,'solid_permutations':solidchecks,'note':'Circle/cone continuous symmetry proved by radius-equation invariance in solutions.md;not inferred from finite sampled turns. Plane scalene/least-angle proofs also reasoned separately.'};(E/'independent_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['passed','total','failed']},indent=2))
