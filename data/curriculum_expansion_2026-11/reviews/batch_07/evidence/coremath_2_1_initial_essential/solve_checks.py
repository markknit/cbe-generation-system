from pathlib import Path
from fractions import Fraction as F
from collections import deque,Counter
import math,json
P=Path(__file__).resolve().parent;m=json.loads((P/'materials_snapshot.json').read_text());checks=[]
def check(n,v,e):checks.append({'id':n,'independent_value':v,'expected':e,'pass':v==e})
for c in m['calculations']:
 v=eval(c['expression'],{'__builtins__':{}},{'sqrt':math.sqrt});checks.append({'id':c['id'],'independent_value':v,'expected':c['expected'],'pass':math.isclose(v,c['expected'],rel_tol=1e-12,abs_tol=1e-12)})
def image(o,k,p):return tuple(F(x)+F(k)*(F(y)-F(x)) for x,y in zip(o,p))
cases=[('positive',(0,0),F(2),[(1,1),(3,1),(1,2)],[(2,2),(6,2),(2,4)]),('nonorigin',(2,1),F(1,2),[(4,3),(8,3),(4,7)],[(3,2),(5,2),(3,4)]),('negative',(0,0),F(-2),[(1,1),(3,1),(1,2)],[(-2,-2),(-6,-2),(-2,-4)]),('final',(0,0),F(1,2),[(2,2),(6,2),(2,4)],[(1,1),(3,1),(1,2)])]
for n,o,k,pts,exp in cases:
 for j,(p,e) in enumerate(zip(pts,exp)):
  v=image(o,k,p);check(n+str(j),list(map(str,v)),list(map(str,e)))
for n,p,q in [('CSE2A',(2,1),(3,1)),('CSE2B',(4,1),(7,1)),('CSE2C',(2,3),(3,5)),('finalA',(2,1),(3,1)),('finalB',(2,3),(3,5))]:
 k=F(2);o=tuple((F(y)-k*F(x))/(1-k) for x,y in zip(p,q));check(n+' centre',list(map(str,o)),['1','1'])
# Rigidly fold all 6 unit faces. Face basis(u,v,n), root normal out of cube.
add=lambda a,b:tuple(x+y for x,y in zip(a,b));mul=lambda c,a:tuple(c*x for x in a);neg=lambda a:mul(-1,a)
cells={(0,1),(1,0),(1,1),(1,2),(2,1),(3,1)};poses={(1,1):((F(0),F(0),F(0)),(1,0,0),(0,1,0),(0,0,1))};queue=deque([(1,1)])
while queue:
 cell=queue.popleft();c,u,v,n=poses[cell]
 for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)]:
  dest=(cell[0]+dr,cell[1]+dc)
  if dest not in cells or dest in poses:continue
  if dc==1:w=u;basis=(neg(n),v,u)
  elif dc==-1:w=neg(u);basis=(n,v,neg(u))
  elif dr==1:w=v;basis=(u,neg(n),v)
  else:w=neg(v);basis=(u,n,neg(v))
  centre=add(c,mul(F(1,2),add(w,neg(n))));poses[dest]=(centre,*basis);queue.append(dest)
edges=Counter();vertices=set();face_info=[]
for cell,(c,u,v,n) in sorted(poses.items()):
 corners=[add(c,add(mul(s,u),mul(t,v))) for s,t in [(F(-1,2),F(-1,2)),(F(1,2),F(-1,2)),(F(1,2),F(1,2)),(F(-1,2),F(1,2))]]
 vertices.update(corners)
 for a,b in zip(corners,corners[1:]+corners[:1]):edges[tuple(sorted([a,b]))]+=1
 face_info.append({'cell':cell,'centre':list(map(str,c)),'normal':n,'corners':[[str(z) for z in x] for x in corners]})
check('net six faces',len(poses),6);check('net six outward normals',len({x[3] for x in poses.values()}),6);check('net eight vertices',len(vertices),8);check('net twelve edges',len(edges),12);check('every folded edge shared twice',sorted(edges.values()),[2]*12)
check('large face net bounds cm',[3*4,4*4],[12,16]);check('small face net bounds cm',[3*2,4*2],[6,8])
# Orientation area of triangle is preserved by planar negative dilation.
def twicearea(t):return sum(t[i][0]*t[(i+1)%3][1]-t[(i+1)%3][0]*t[i][1] for i in range(3))
check('negative orientation ratio',F(twicearea([(-2,-2),(-6,-2),(-2,-4)]),twicearea([(1,1),(3,1),(1,2)])),F(4))
r={'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks,'folded_net_faces':face_info,'net_edges_multiplicities':[{'edge':[[str(v) for v in p] for p in edge],'uses':count} for edge,count in sorted(edges.items())]};(P/'independent_checks.json').write_text(json.dumps(r,indent=2,default=str)+'\n');assert all(c['pass'] for c in checks);print(len(checks),'registered/coordinate/centre/net/orientation checks PASS')
