from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import json,math
P=Path(__file__).resolve().parent;m=json.loads((P/'materials_snapshot.json').read_text());checks=[]
def ck(n,v,e):checks.append({'id':n,'independent_value':v,'expected':e,'pass':v==e})
for c in m['calculations']:
 v=eval(c['expression'],{'__builtins__':{}},{'sqrt':math.sqrt});checks.append({'id':c['id'],'independent_value':v,'expected':c['expected'],'pass':math.isclose(v,c['expected'],rel_tol=1e-12,abs_tol=1e-12)})
def rotate(p,o,q):
 x,y=[F(a)-F(b) for a,b in zip(p,o)]
 for _ in range(q%4):x,y=-y,x
 return x+o[0],y+o[1]
cases=[('quarterCCW',(0,0),1,[(1,1),(3,1),(1,2)],[(-1,1),(-1,3),(-2,1)]),('quarterCW',(0,0),-1,[(1,1),(3,1),(1,2)],[(1,-1),(1,-3),(2,-1)]),('half',(0,0),2,[(1,2),(-2,3),(0,-1)],[(-1,-2),(2,-3),(0,1)]),('nonorigin',(1,1),1,[(2,1),(4,1),(2,3)],[(1,2),(1,4),(-1,2)]),('recover',(1,1),1,[(2,1),(3,1),(2,2)],[(1,2),(1,3),(0,2)]),('halfcentre',(3,3),2,[(1,2),(2,5),(0,3)],[(5,4),(4,1),(6,3)]),('congruence',(0,0),1,[(0,0),(3,0),(1,2)],[(0,0),(0,3),(-2,1)]),('application',(0,0),-1,[(1,0),(3,0),(1,2)],[(0,-1),(0,-3),(2,-1)]),('finalimage',(0,0),-1,[(1,0),(3,0),(1,2)],[(0,-1),(0,-3),(2,-1)]),('finalcentre',(1,2),1,[(1,0),(2,1)],[(3,2),(2,3)])]
for name,o,q,ps,es in cases:
 for j,(p,e) in enumerate(zip(ps,es)):
  v=rotate(p,o,q);ck(name+str(j),list(map(str,v)),list(map(str,e)))
  ck(name+' radius'+str(j),sum((a-b)**2 for a,b in zip(p,o)),sum((a-b)**2 for a,b in zip(v,o)))
for q,e in [(4,(1,2)),(5,(-2,1)),(1,(-2,1)),(3,(2,-1)),(-1,(2,-1))]:ck('endpoint quarter multiples'+str(q),list(map(str,rotate((1,2),(0,0),q))),list(map(str,e)))
def locus(p,q):return[2*(F(b)-F(a)) for a,b in zip(p,q)]+[sum(F(x)**2 for x in q)-sum(F(x)**2 for x in p)]
def intersect(l,k):
 a,b,c=l;d,e,f=k;det=a*e-b*d;return((c*e-b*f)/det,(a*f-c*d)/det)
for name,p,q,r,s,e in [('centreCRT5',(2,1),(1,2),(2,2),(0,2),(1,1)),('centreFinal',(1,0),(3,2),(2,1),(2,3),(1,2))]:ck(name,list(map(str,intersect(locus(p,q),locus(r,s)))),list(map(str,e)))
# Proper rotations map each vertex set onto itself; powers test least order.
def apply(A,v):return tuple(sum(a*b for a,b in zip(row,v)) for row in A)
I=((1,0,0),(0,1,0),(0,0,1));Z90=((0,-1,0),(1,0,0),(0,0,1));cycle=((0,0,1),(1,0,0),(0,1,0));edge180=((0,1,0),(1,0,0),(0,0,-1));X180=((1,0,0),(0,-1,0),(0,0,-1))
cube=set(product((-1,1),repeat=3));tetra={(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)};pyramid={(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0),(0,0,2)}
for name,verts,A,order in [('cubeFace',cube,Z90,4),('cubeVertex',cube,cycle,3),('cubeEdge',cube,edge180,2),('tetraVertex',tetra,cycle,3),('tetraEdge',tetra,X180,2),('pyramidAxis',pyramid,Z90,4)]:
 ck(name+' vertex bijection',sorted(apply(A,v) for v in verts),sorted(verts))
 for power in range(1,order+1):
  cur={v:v for v in verts}
  for _ in range(power):cur={v:apply(A,w) for v,w in cur.items()}
  ck(name+' least order step'+str(power),all(v==w for v,w in cur.items()),power==order)
ck('cube axis line counts',[6//2,8//2,12//2],[3,4,6]);ck('tetra all edge squares',sorted(sum((a-b)**2 for a,b in zip(x,y)) for x,y in combinations(tetra,2)),[8]*6)
# Equilateral-base right prism: rotation120 degrees maps both bases cyclically.
prism=[(math.cos(2*math.pi*j/3),math.sin(2*math.pi*j/3),z) for z in [-1,1] for j in range(3)]
for j,v in enumerate(prism):
 a=2*math.pi/3;w=(math.cos(a)*v[0]-math.sin(a)*v[1],math.sin(a)*v[0]+math.cos(a)*v[1],v[2]);ck('prism axial120 vertex'+str(j),min(sum((x-y)**2 for x,y in zip(w,t)) for t in prism)<1e-20,True)
def area2(t):return sum(t[i][0]*t[(i+1)%3][1]-t[(i+1)%3][0]*t[i][1] for i in range(3))
ck('CRT10 original orientation',area2([(0,0),(3,0),(1,2)]),6);ck('CRT10 rotation orientation',area2([(0,0),(0,3),(-2,1)]),6);ck('CRT10 reflection orientation',area2([(0,0),(-3,0),(-1,2)]),-6);ck('final orientation',area2([(0,-1),(0,-3),(2,-1)]),4)
r={'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks,'solid_rotation_matrices':{'cube_face90':Z90,'cube_vertex120':cycle,'cube_edge180':edge180,'tetra_edge180':X180},'cube_vertices':sorted(cube),'tetra_vertices':sorted(tetra),'pyramid_vertices':sorted(pyramid)};(P/'independent_checks.json').write_text(json.dumps(r,indent=2,default=str)+'\n');assert all(c['pass'] for c in checks);print(len(checks),'independent registered/coordinate/bisector/solid-symmetry/orientation checks PASS')
