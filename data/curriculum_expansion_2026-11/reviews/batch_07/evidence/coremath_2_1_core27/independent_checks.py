from pathlib import Path
from fractions import Fraction as F
from collections import deque
import ast,json,math,operator
E=Path(__file__).parent;B=E.parents[3];M=json.loads((B/'materials/coremath_2_1.json').read_text());checks={};detail={}
def eq(k,a,w):checks[k]=a==w;detail[k]={'actual':str(a),'expected':str(w)}
def image(p,o,k):return tuple(F(o[i])+F(k)*(F(p[i])-F(o[i])) for i in range(2))
def signed_area(t):return F((t[1][0]-t[0][0])*(t[2][1]-t[0][1])-(t[1][1]-t[0][1])*(t[2][0]-t[0][0]),2)
def dist2(p,q):return sum((F(x)-F(y))**2 for x,y in zip(p,q))
constructions=[]
for label,o,k,pts,want in [('positive',(0,0),F(2),[(1,1),(3,1),(1,2)],[(2,2),(6,2),(2,4)]),('reduction',(2,1),F(1,2),[(4,3),(8,3),(4,7)],[(3,2),(5,2),(3,4)]),('negative',(0,0),F(-2),[(1,1),(3,1),(1,2)],[(-2,-2),(-6,-2),(-2,-4)]),('final_reduction',(0,0),F(1,2),[(2,2),(6,2),(2,4)],[(1,1),(3,1),(1,2)])]:
 out=[image(p,o,k) for p in pts];eq(label+'_all_image_coordinates',out,want)
 for j,(p,q) in enumerate(zip(pts,out)):
  eq(label+f'_directed_displacement_{j}',tuple(F(q[i])-o[i] for i in range(2)),tuple(k*(F(p[i])-o[i]) for i in range(2)))
  eq(label+f'_centre_distance_square_{j}',dist2(q,o),k*k*dist2(p,o))
 eq(label+'_side_distance_squared',dist2(out[0],out[1]),k*k*dist2(pts[0],pts[1]));eq(label+'_signed_area',signed_area(out),k*k*signed_area(pts));constructions.append({'label':label,'centre':o,'factor':str(k),'points':pts,'images':[[float(x),float(y)] for x,y in out]})
def line(p,q):a=F(q[1]-p[1]);b=F(p[0]-q[0]);return a,b,a*p[0]+b*p[1]
def cross(l,m):a,b,c=l;d,e,f=m;det=a*e-b*d;return((c*e-b*f)/det,(a*f-c*d)/det)
for label,pts,out,pairs in [('centre',[(2,1),(4,1),(2,3)],[(3,1),(7,1),(3,5)],(0,2)),('final_centre',[(2,1),(2,3)],[(3,1),(3,5)],(0,1))]:
 o=cross(line(pts[pairs[0]],out[pairs[0]]),line(pts[pairs[1]],out[pairs[1]]));eq(label+'_derived_intersection',o,(F(1),F(1)))
 for j,(p,q) in enumerate(zip(pts,out)):eq(label+f'_all_pairs_factor2_{j}',image(p,o,2),q)
 eq(label+'_side_length_squared_factor',dist2(out[0],out[1])/dist2(pts[0],pts[1]),F(4));constructions.append({'label':label,'centre':[float(x) for x in o],'factor':'2','points':pts,'images':out})
eq('CSE4_teacher_naive_halving_claim',tuple(F(x)/2 for x in (4,3)),(F(2),F(1)))
eq('factor_zero_collapses',image((3,5),(1,1),0),(F(1),F(1)));eq('factor_one_identity',image((3,5),(8,9),1),(F(3),F(5)));eq('translation_not_dilation',(3+2,1+2),(5,3))
for k,sizes in [('similar_triangles',[(3,4,5),(6,8,10)]),('similar_rectangles',[(2,3),(4,6)]),('nonsimilar_rectangles',[(2,3),(4,5)]),('equalvolume_nonsimilar',[(2,2,2),(1,2,4)])]:
 ratios=[F(y,x) for x,y in zip(*sizes)];eq(k+'_ratios_equal',len(set(ratios))==1,k.startswith('similar_'))
eq('rectangles_areas',[3*2,9*6],[6,54]);eq('rectangles_ratio',F(54,6),F(3)**2);eq('triangle_areas',[F(4*3,2),F(8*6,2)],[F(6),F(24)]);eq('triangle_ratio',F(24,6),F(2)**2)
for s,S,V in [(2,24,8),(4,96,64),(6,216,216)]:eq(f'cube_{s}_surface',6*s*s,S);eq(f'cube_{s}_volume',s**3,V)
for dims,V,S in [((2,3,4),24,52),((6,9,12),648,468),((4,6,8),192,208),((1,2,4),8,28)]:a,b,c=dims;eq(f'cuboid_{dims}_volume',a*b*c,V);eq(f'cuboid_{dims}_surface',2*(a*b+a*c+b*c),S)
for label,k,ar,vr in [('k3',F(3),F(9),F(27)),('reverse3',F(1,3),F(1,9),F(1,27)),('recover',F(5,2),F(25,4),F(125,8)),('project',F(2),F(4),F(8)),('final_area',F(5),F(25),F(125)),('final_volume',F(3,2),F(9,4),F(27,8))]:eq(label+'_area',k*k,ar);eq(label+'_volume',k*k*k,vr)
eq('negative_physical_length',abs(-2),2);eq('negative_physical_area',abs(-2)**2,4);eq('negative_physical_volume',abs(-2)**3,8)
eq('model_actual_dimensions_cm',(4*50,6*50),(200,300));eq('model_actual_dimensions_m',(F(200,100),F(300,100)),(F(2),F(3)));eq('model_area_cm2',4*6,24);eq('actual_area_cm2',200*300,60000);eq('actual_area_m2',F(60000,10000),F(6));eq('matching_unit_area_ratio',F(60000,24),F(2500));eq('wrong_single_factor',24*50,1200)
# Discrete90degree folding of the exact six-square net;all six face normals must differ.
cells={(0,1),(1,0),(1,1),(1,2),(2,1),(3,1)};neg=lambda v:tuple(-x for x in v);start=(1,1);frames={start:((1,0,0),(0,1,0),(0,0,1))};todo=deque([start])
while todo:
 r,c=todo.popleft();R,D,N=frames[r,c]
 for dr,dc,frame in [(0,1,(neg(N),D,R)),(0,-1,(N,D,neg(R))),(1,0,(R,neg(N),D)),(-1,0,(R,N,neg(D)))]:
  p=(r+dr,c+dc)
  if p in cells and p not in frames:frames[p]=frame;todo.append(p)
eq('net_all_faces_connected',len(frames),6);eq('net_six_unique_normals',len({v[2] for v in frames.values()}),6);eq('net_normals_complete',{v[2] for v in frames.values()},{(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)});eq('large_net_face_extent_cm',(3*4,4*4),(12,16));checks['net_fits_A4_before_tabs']=12<21 and 16<29.7

def calc(n):
 if isinstance(n,ast.Expression):return calc(n.body)
 if isinstance(n,ast.Constant):return F(str(n.value))
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -calc(n.operand)
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}[type(n.op)](calc(n.left),calc(n.right))
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt':return math.sqrt(calc(n.args[0]))
 raise ValueError(ast.dump(n))
for row in M['calculations']:checks['registry_'+row['id']]=math.isclose(float(calc(ast.parse(row['expression'],mode='eval'))),row['expected'],rel_tol=1e-12,abs_tol=1e-13)
r={'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'checks':checks,'detail':detail,'constructions':constructions,'folded_face_normals':{str(k):v[2] for k,v in frames.items()}};(E/'independent_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['passed','total','failed']},indent=2))
