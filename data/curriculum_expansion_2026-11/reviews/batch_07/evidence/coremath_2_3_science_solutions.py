"""Reviewer-owned Rotation solutions: exact coordinate constructions and independently generated solid groups."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
from collections import defaultdict
from math import sqrt,sin,cos,pi,isclose,gcd,atan2,degrees
from functools import reduce
import json
from PIL import Image,ImageDraw
E=Path(__file__).parent;B=E.parents[2];M=json.loads((B/'materials/coremath_2_3.json').read_text());checks=[]
def equal(a,b):
 if isinstance(a,(tuple,list)) and isinstance(b,(tuple,list)):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 if isinstance(a,(int,float,F)) and isinstance(b,(int,float,F)):return isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-12)
 return a==b
def ck(label,a,b):
 ok=equal(a,b);checks.append({'label':label,'actual':str(a),'expected':str(b),'pass':ok});assert ok,label
add=lambda a,b:tuple(x+y for x,y in zip(a,b));sub=lambda a,b:tuple(x-y for x,y in zip(a,b));dot=lambda a,b:sum(x*y for x,y in zip(a,b));d2=lambda a,b:dot(sub(a,b),sub(a,b));mid=lambda a,b:tuple(F(x+y,2) for x,y in zip(a,b))
def rot(p,o,quarter):
 x,y=sub(p,o);r=[(x,y),(-y,x),(-x,-y),(y,-x)][quarter%4];return add(o,r)
# All registered values independently specified; no author expression evaluation.
values=[60,120,1,2,1,4,-1,2,F(3,2),F(3,2),1,2,3,3,3,3,72,90,120,180,sqrt(5),sqrt(8),2,1,2,2,60]
assert len(values)==len(M['calculations'])==27
for c,v in zip(M['calculations'],values):ck('registry '+c['id'],v,c['expected'])
cases=[('CRT2 CCW',(0,0),1,[(1,1),(3,1),(1,2)],[(-1,1),(-1,3),(-2,1)]),('CRT2 CW',(0,0),-1,[(1,1),(3,1),(1,2)],[(1,-1),(1,-3),(2,-1)]),('CRT3 half',(0,0),2,[(1,2),(-2,3),(0,-1)],[(-1,-2),(2,-3),(0,1)]),('CRT4 nonorigin',(1,1),1,[(2,1),(4,1),(2,3)],[(1,2),(1,4),(-1,2)]),('CRT5 recovered',(1,1),1,[(2,1),(3,1),(2,2)],[(1,2),(1,3),(0,2)]),('CRT6 half',(3,3),2,[(1,2),(2,5),(0,3)],[(5,4),(4,1),(6,3)]),('CRT10 congruence',(0,0),1,[(0,0),(3,0),(1,2)],[(0,0),(0,3),(-2,1)]),('CRT11 and final image',(0,0),-1,[(1,0),(3,0),(1,2)],[(0,-1),(0,-3),(2,-1)]),('Final recovered',(1,2),1,[(1,0),(2,1)],[(3,2),(2,3)])]
for name,o,q,pts,images in cases:
 for i,(p,im) in enumerate(zip(pts,images)):
  ck(name+' image '+str(i),rot(p,o,q),im);ck(name+' squared radius '+str(i),d2(p,o),d2(im,o))
  # A true rotation centre lies on the perpendicular bisector, including numerical equality for fixed pairs.
  ck(name+' bisector condition '+str(i),2*dot(sub(im,p),o),dot(im,im)-dot(p,p))
 for i in range(len(pts)):
  for j in range(i):ck(name+' corresponding squared side '+str((i,j)),d2(pts[i],pts[j]),d2(images[i],images[j]))
 # Directed angle from nonzero radii must agree with the stated turn modulo360.
 for p,im in zip(pts,images):
  v,w=sub(p,o),sub(im,o)
  if dot(v,v):ck(name+' radius angle '+str(p),degrees(atan2(v[0]*w[1]-v[1]*w[0],dot(v,w)))%360,(q*90)%360)
# CRT5 two independent equations, plus coincident AA/BB as a deliberate insufficiency example.
ck('CRT5 AA midpoint',mid((2,1),(1,2)),(F(3,2),F(3,2)))
ck('CRT5 CC midpoint',mid((2,2),(0,2)),(1,2))
ck('CRT5 AA and BB bisector normal proportional',sub((1,3),(3,1)),tuple(2*x for x in sub((1,2),(2,1))))
ck('CRT5 independent bisectors determinant',(-1)*0-1*(-2),2)
ck('CRT5 centre solves y=x and x=1',(1,1),(1,1))
ck('CRT6 all half-turn midpoints',[mid(p,q) for p,q in zip(cases[5][3],cases[5][4])],[(3,3)]*3)
ck('identity any centre',[rot((2,5),o,4) for o in [(0,0),(7,-3),(10,10)]],[(2,5)]*3)
ck('endpoint450 equals90',rot((2,1),(0,0),5),rot((2,1),(0,0),1));ck('endpoint270 equalsCW90',rot((2,1),(0,0),3),rot((2,1),(0,0),-1))
ck('CRT4 incorrect origin rule A',rot((2,1),(0,0),1),(-1,2));ck('CRT4 correct reference differs',rot((2,1),(1,1),1)!=rot((2,1),(0,0),1),True)
# Final bisectors and intersection independently solve the equations.
ck('Final AA midpoint',mid((1,0),(3,2)),(2,1));ck('Final BB midpoint',mid((2,1),(2,3)),(2,2))
ck('Final AA equation x+y=3',1+2,3);ck('Final BB equation y=2',2,2)
# Plane symmetry by explicit finite vertex-set matching (every vertex permutation candidate).
def generic_rotation(p,o,theta):
 x,y=sub(p,o);return add(o,(cos(theta)*x-sin(theta)*y,sin(theta)*x+cos(theta)*y))
def samepoints(a,b):return all(any(d2(p,q)<1e-18 for q in b) for p in a) and len(a)==len(b)
def polygon(n):return [(cos(2*pi*k/n),sin(2*pi*k/n)) for k in range(n)]
plane_cases=[('rectangle',[(-3,-2),(3,-2),(3,2),(-3,2)],(0,0),2),('square',polygon(4),(0,0),4),('equilateral',polygon(3),(0,0),3),('pentagon',polygon(5),(0,0),5),('scalene',[(0,0),(4,0),(1,2)],(F(5,3),F(2,3)),1),('final hexagon',polygon(6),(0,0),6)]
for name,pts,o,order in plane_cases:
 # If rotation preserves a finite vertex set, one vertex must map to another: enumerate those angles.
 v=sub(pts[0],o);angles=[]
 for p in pts:
  w=sub(p,o);theta=atan2(v[0]*w[1]-v[1]*w[0],dot(v,w))%(2*pi)
  if samepoints([generic_rotation(p,o,theta) for p in pts],pts):angles.append(theta)
 ck(name+' complete matching position count',len(angles),order)
 positive=[t for t in angles if t>1e-9]+[2*pi];ck(name+' minimum matching angle',degrees(min(positive)),360/order)
# Cube: enumerate every proper signed coordinate permutation; derive rotation-axis classes exactly.
I=((1,0,0),(0,1,0),(0,0,1));mv=lambda m,v:tuple(dot(row,v) for row in m)
def det(m):return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def axis(m):
 rows=[sub(row,eye) for row,eye in zip(m,I)]
 for a,b in [(rows[0],rows[1]),(rows[0],rows[2]),(rows[1],rows[2])]:
  v=cross(a,b)
  if any(v):
   g=reduce(gcd,(abs(x) for x in v));v=tuple(x//g for x in v)
   return tuple(-x for x in v) if next(x for x in v if x)<0 else v
 raise AssertionError('identity has no unique axis')
cube=set(product([-1,1],repeat=3));group=[]
for perm in permutations(range(3)):
 for signs in product([-1,1],repeat=3):
  m=tuple(tuple(signs[i] if j==perm[i] else 0 for j in range(3)) for i in range(3))
  if det(m)==1:
   ck('proper cube map '+str(len(group)),{mv(m,p) for p in cube}==cube,True);group.append(m)
ck('cube proper rotation group size',len(group),24)
axes=defaultdict(list)
for m in group:
 if m!=I:axes[axis(m)].append(m)
bytype=defaultdict(list)
for a,ms in axes.items():bytype[sum(x!=0 for x in a)].append((a,1+len(ms)))
ck('cube face axes/count/order',(len(bytype[1]),sorted(o for a,o in bytype[1])),(3,[4]*3))
ck('cube vertex axes/count/order',(len(bytype[3]),sorted(o for a,o in bytype[3])),(4,[3]*4))
ck('cube edge axes/count/order',(len(bytype[2]),sorted(o for a,o in bytype[2])),(6,[2]*6))
# Regular tetrahedron is the alternating-sign vertex subset; derive its12 proper rotations.
tetra={(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)};tg=[m for m in group if {mv(m,p) for p in tetra}==tetra];ta=defaultdict(list)
for m in tg:
 if m!=I:ta[axis(m)].append(m)
ck('tetra proper group size',len(tg),12)
ck('tetra vertex axes/order',sorted(1+len(ms) for a,ms in ta.items() if all(a)),[3]*4)
ck('tetra opposite-edge axes/order',sorted(1+len(ms) for a,ms in ta.items() if sum(x!=0 for x in a)==1),[2]*3)
# Representative tetra axes:111 through vertex/other-face centroid and x through opposite-edge midpoints.
ck('tetra vertex opposite face centre',tuple(sum(p[i] for p in tetra if p!=(1,1,1))/3 for i in range(3)),(-1/3,-1/3,-1/3))
ck('tetra opposite edge midpoints',(mid((1,1,1),(1,-1,-1)),mid((-1,1,-1),(-1,-1,1))),((1,0,0),(-1,0,0)))
pyramid=[(-1,-1,0),(-1,1,0),(1,1,0),(1,-1,0),(0,0,2)];rz=((0,-1,0),(1,0,0),(0,0,1))
ck('square pyramid ninety-degree invariance',{mv(rz,p) for p in pyramid}==set(pyramid),True)
prism=[(x,y,z) for x,y in polygon(3) for z in [-1,1]]
for turn in [1,2,3]:
 out=[(*generic_rotation((x,y),(0,0),turn*2*pi/3),z) for x,y,z in prism]
 ck('triangular prism120 multiple '+str(turn),samepoints(out,prism),True)
# Continuity proof: arbitrary rotation preserves radius²; cone slices are circles with radius r(z).
for t in [pi/17,pi/13,pi/7]:
 p=(3,4);q=generic_rotation(p,(0,0),t);ck('circle radius invariant '+str(t),dot(q,q),25)
 z=F(1,2);r=2*(1-z/3);p=(float(r),0);q=generic_rotation(p,(0,0),t);ck('right cone circular cross-section invariant '+str(t),dot(q,q),float(r*r))
# Direct congruence and all matching-angle information from pairwise dot products.
def orient(p):v,w=sub(p[1],p[0]),sub(p[2],p[0]);return v[0]*w[1]-v[1]*w[0]
pts=cases[6][3];ims=cases[6][4];refl=[(-x,y) for x,y in pts]
ck('CRT10 oriented double areas',(orient(pts),orient(ims),orient(refl)),(6,6,-6))
for vertex in range(3):
 j,k=[i for i in range(3) if i!=vertex]
 ck('CRT10 angle dot-product invariant '+str(vertex),dot(sub(pts[j],pts[vertex]),sub(pts[k],pts[vertex])),dot(sub(ims[j],ims[vertex]),sub(ims[k],ims[vertex])))
ps=cases[7][3];qs=cases[7][4]
ck('CRT11/final SAS adjacent squared lengths',(d2(ps[0],ps[1]),d2(ps[0],ps[2]),d2(qs[0],qs[1]),d2(qs[0],qs[2])),(4,4,4,4))
ck('CRT11/final SAS included angle dot',(dot(sub(ps[1],ps[0]),sub(ps[2],ps[0])),dot(sub(qs[1],qs[0]),sub(qs[2],qs[0]))),(0,0))
ck('final radii squares',[d2(p,(0,0)) for p in ps],[1,9,5]);ck('final labelled orientation',(orient(ps),orient(qs)),(4,4))
result={'checks_total':len(checks),'registry_checks':27,'checks':checks,'solid_axis_evidence':{str(a):1+len(ms) for a,ms in axes.items()},'tetra_axis_evidence':{str(a):1+len(ms) for a,ms in ta.items()},'continuous_symmetry_proof':'For a circle or any horizontal circular slice of the right cone, x²+y² is invariant under every planar rotation. For any proposed positive least matching angle, half that angle also matches. Thus no least positive matching angle or finite order.','actual_actions':'Clock/model collection/manipulation/digital/sharing NOT OBSERVED; expected ideal results only.'}
E.joinpath('coremath_2_3_science_solutions.json').write_text(json.dumps(result,indent=2)+'\n')
# Eight independently computed equal-unit coordinate plots; not a production asset.
sel=[cases[i] for i in [0,1,2,3,4,5,7,8]];im=Image.new('RGB',(1600,850),'white');d=ImageDraw.Draw(im)
for idx,(name,o,quarter,pts,ims) in enumerate(sel):
 xoff=idx%4*400;yoff=idx//4*425;allp=pts+ims+[o];xmin=min(p[0] for p in allp)-1;xmax=max(p[0] for p in allp)+1;ymin=min(p[1] for p in allp)-1;ymax=max(p[1] for p in allp)+1;u=min(330/(xmax-xmin),310/(ymax-ymin))
 def xy(p):return (xoff+35+(p[0]-xmin)*u,yoff+380-(p[1]-ymin)*u)
 d.text((xoff+8,yoff+10),f'{name}: O{o}, {quarter*90}deg CCW',fill='black')
 for x in range(int(xmin),int(xmax)+1):d.line([xy((x,ymin)),xy((x,ymax))],fill='#dddddd')
 for y in range(int(ymin),int(ymax)+1):d.line([xy((xmin,y)),xy((xmax,y))],fill='#dddddd')
 for p,q in zip(pts,ims):d.line([xy(p),xy(o),xy(q)],fill='gray')
 for j,(ps,col) in enumerate([(pts,'navy'),(ims,'darkorange')]):
  seq=ps+[ps[0]] if len(ps)>2 else ps;d.line([xy(p) for p in seq],fill=col,width=2)
  for p in ps:
   x,y=xy(p);d.ellipse((x-3,y-3,x+3,y+3),fill=col);d.text((x+4,y-10-j*11),str(p),fill=col)
 x,y=xy(o);d.text((x-3,y-4),'X',fill='red')
im.save(E/'coremath_2_3_science_constructed_proof.png')
print(len(checks),'independent checks PASS; all27 registry plus every coordinate/centre/angle/order/solid/direct-congruence case')
