from pathlib import Path
from fractions import Fraction as F
import json,math
P=Path(__file__).resolve().parent;m=json.loads((P/'materials_snapshot.json').read_text());checks=[]
def ck(n,v,e):checks.append({'id':n,'independent_value':v,'expected':e,'pass':v==e})
for c in m['calculations']:
 v=eval(c['expression'],{'__builtins__':{}},{'sqrt':math.sqrt});checks.append({'id':c['id'],'independent_value':v,'expected':c['expected'],'pass':math.isclose(v,c['expected'],rel_tol=1e-12,abs_tol=1e-12)})
def reflect(p,line):
 x,y=map(F,p);a,b,c=map(F,line);t=2*(a*x+b*y+c)/(a*a+b*b);return(x-t*a,y-t*b)
cases=[('CRG3',(1,0,0),[(1,1),(4,1),(2,3)],[(-1,1),(-4,1),(-2,3)]),('CRG4x',(1,0,-2),[(0,1),(3,-1)],[(4,1),(1,-1)]),('CRG4y',(0,1,1),[(2,3),(-1,-1)],[(2,-5),(-1,-1)]),('CRG4triangle',(0,1,-1),[(0,0),(2,0),(1,2)],[(0,2),(2,2),(1,0)]),('CRG5plus',(-1,1,0),[(2,-1),(3,1),(1,4)],[(-1,2),(1,3),(4,1)]),('CRG5minus',(1,1,0),[(2,-1),(3,1),(1,4)],[(1,-2),(-1,-3),(-4,-1)]),('CRG6',(-1,1,-1),[(0,0),(2,0),(0,1)],[(-1,1),(-1,3),(0,1)]),('CRG7',(2,1,-8),[(1,1),(0,3)],[(5,3),(4,5)]),('digital',(0,1,0),[(1,1),(3,1),(2,3)],[(1,-1),(3,-1),(2,-3)]),('finaltriangle',(1,1,0),[(1,1),(3,1),(2,3)],[(-1,-1),(-1,-3),(-3,-2)]),('finalmirror',(-1,1,-2),[(0,0),(2,0)],[(-2,2),(-2,4)]),('finalplane',(1,0,0),[(3,1)],[(-3,1)]),('fixedplus',(-1,1,0),[(2,2)],[(2,2)]),('fixedminus',(1,1,0),[(2,-2)],[(2,-2)])]
for name,line,ps,es in cases:
 for j,(p,e) in enumerate(zip(ps,es)):
  v=reflect(p,line);ck(name+str(j),list(map(str,v)),list(map(str,e)))
for name,p,q,e in [('midA',(0,0),(-1,1),(F(-1,2),F(1,2))),('midB',(2,0),(-1,3),(F(1,2),F(3,2))),('midP',(1,1),(5,3),(3,2)),('midQ',(0,3),(4,5),(2,4)),('midU',(0,0),(-2,2),(-1,1)),('midV',(2,0),(-2,4),(0,2))]:ck(name,[str((F(a)+F(b))/2) for a,b in zip(p,q)],list(map(str,e)))
def twicearea(t):return sum(t[i][0]*t[(i+1)%3][1]-t[(i+1)%3][0]*t[i][1] for i in range(3))
ck('direct orientation',twicearea([(2,1),(5,1),(3,3)]),6);ck('opposite orientation',twicearea([(0,0),(-3,0),(-1,2)]),-6);ck('original orientation',twicearea([(0,0),(3,0),(1,2)]),6)
ck('scalene squared sides',[4**2,1**2+2**2,3**2+2**2],[16,5,13]);ck('CRG8 squared sides',[3**2,1**2+2**2,2**2+2**2],[9,5,8]);ck('finalSSS triangle inequality',4+5>6,True)
ck('ASA third angle',180-40-65,75);ck('AAS remaining',180-40-75,65);ck('finalAAS third',180-40-70,70);ck('RHS leg square',25-9,16)
# Independent constructive SSA counterexample: AB8, BC5, angleA30°, AC r.
ssa=[]
for r in [4*math.sqrt(3)-3,4*math.sqrt(3)+3]:
 c=(r*math.cos(math.pi/6),r/2);bc=math.hypot(c[0]-8,c[1]);ssa.append({'AB':8,'BC':bc,'angle_A_deg':30,'AC':r,'C':c});checks.append({'id':'SSA counterexample '+str(r),'independent_value':bc,'expected':5,'pass':math.isclose(bc,5,rel_tol=1e-12)})
r={'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks,'independent_SSA_counterexample':ssa};(P/'independent_checks.json').write_text(json.dumps(r,indent=2)+'\n');assert all(c['pass'] for c in checks);print(len(checks),'independent registry/coordinate/midpoint/orientation/triangle checks PASS')
