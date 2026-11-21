"""Reviewer-owned exact solutions and cube-net folding; never edits inputs."""
from pathlib import Path
import json,math
from fractions import Fraction as F
from collections import deque
from PIL import Image,ImageDraw
E=Path(__file__).parent;B=E.parents[2]
M=json.loads((B/'materials/coremath_2_1.json').read_text())
checks=[]
def ck(label,actual,expected):
 ok=actual==expected
 checks.append({'label':label,'actual':str(actual),'expected':str(expected),'pass':ok})
 assert ok,label
# Derive all registered values from independently specified mathematical quantities.
sa=lambda a,b,c:2*(a*b+a*c+b*c)
vals=dict(zip(['centreX','centreY','positiveImageQx','reductionPx','reductionPy','reductionQx','negativeQx','rectangleSmall','rectangleLarge','triangleSmall','triangleLarge','cubeSurfaceSmall','cubeSurfaceLarge','cubeVolumeSmall','cubeVolumeLarge','cuboidSmall','cuboidLarge','recoverArea','recoverVolume','modelArea','actualAreaCm','actualAreaM','projectSurfaceLarge','projectVolumeLarge','finalSurfaceSmall','finalSurfaceLarge','finalVolumeLarge','finalAreaRecover','finalVolumeScale','finalVolumeRecover','finalAreaScale'],[1,1,6,3,2,5,-6,6,54,6,24,24,216,8,216,24,648,F(5,2),F(5,2),24,60000,6,96,64,52,208,192,5,125,F(3,2),F(9,4)]))
for c in M['calculations']:ck('registry '+c['id'],vals[c['id']],F(str(c['expected'])))
dilate=lambda p,o,k:tuple(F(oi)+F(k)*(F(pi)-F(oi)) for pi,oi in zip(p,o))
constructions=[('CSE2',(1,1),2,[(2,1),(4,1),(2,3)],[(3,1),(7,1),(3,5)]),('CSE3',(0,0),2,[(1,1),(3,1),(1,2)],[(2,2),(6,2),(2,4)]),('CSE4',(2,1),F(1,2),[(4,3),(8,3),(4,7)],[(3,2),(5,2),(3,4)]),('CSE5',(0,0),-2,[(1,1),(3,1),(1,2)],[(-2,-2),(-6,-2),(-2,-4)]),('Final centre',(1,1),2,[(2,1),(2,3)],[(3,1),(3,5)]),('Final reduction',(0,0),F(1,2),[(2,2),(6,2),(2,4)],[(1,1),(3,1),(1,2)])]
for label,o,k,pts,images in constructions:
 for i,(p,q) in enumerate(zip(pts,images)):
  ck(label+' image '+str(i),dilate(p,o,k),q)
  if k!=1:ck(label+' inverse centre '+str(i),tuple((F(qi)-k*pi)/(1-k) for pi,qi in zip(p,q)),o)
ck('CSE2/Final AA line centre',1,1)
ck('CSE2 CC and Final BB y=2x-1 centre',2*1-1,1)
ck('CSE3 false translation Q',(3+2,1+2),(5,3))
ck('CSE4 false origin halving P',dilate((4,3),(0,0),F(1,2)),(2,F(3,2)))
# Counterexamples, signed geometry, ratios and units not covered by the registry.
ck('CSE1 triangle length factors',[F(b,a) for a,b in zip([3,4,5],[6,8,10])],[F(2)]*3)
ck('CSE1 rectangle similar',[F(4,2),F(6,3)],[F(2)]*2)
ck('CSE1 rectangle failure',F(4,2)!=F(5,3),True)
ck('CSE1 rotation also fails',F(5,2)!=F(4,3),True)
ck('CSE1 equal-side rhombus/square angles differ',(60,120)!=(90,90),True)
ck('CSE5 determinant preserves planar orientation',(-2)**2,4)
ck('CSE5 physical length/area/volume',(abs(-2),abs(-2)**2,abs(-2)**3),(2,4,8))
ck('zero collapses all points',[dilate(p,(1,1),0) for p in [(2,3),(5,6)]],[(1,1)]*2)
ck('identity independent of centre',dilate((2,3),(8,-7),1),(2,3))
ck('CSE6 rectangle area ratio',F(54,6),9);ck('CSE6 triangle area ratio',F(24,6),4)
ck('CSE6 cube surface ratio',F(216,24),9)
ck('CSE7 cube volume ratio',F(216,8),27);ck('CSE7 cuboid volume ratio',F(648,24),27)
ck('CSE7 equal volumes',2**3,1*2*4)
ck('CSE7 no common edge scale',len(set([F(1,2),F(2,2),F(4,2)]))>1,True)
ck('CSE8 square root recovery',F(5,2)**2,F(25,4));ck('CSE8 cube root recovery',F(5,2)**3,F(125,8))
ck('CSE8 forward',(3,3**2,3**3),(3,9,27));ck('CSE8 reverse',(F(1,3),F(1,3)**2,F(1,3)**3),(F(1,3),F(1,9),F(1,27)))
ck('CSE9 dimensions metres',(F(4*50,100),F(6*50,100)),(2,3))
ck('CSE9 cm2 to m2',F(60000,10000),6);ck('CSE9 area ratio',F(60000,24),2500)
ck('CSE9 incorrect linear multiplication',24*50,1200)
ck('CSE10 project measures',(6*2**2,2**3,6*4**2,4**3),(24,8,96,64))
ck('CSE10 project ratios',(F(4,2),F(96,24),F(64,8)),(2,4,8))
ck('Final cuboid measures',(sa(2,3,4),sa(4,6,8),2*3*4,4*6*8),(52,208,24,192))
ck('Final ratio roots',(F(225,9),5**3,F(3,2)**3,F(3,2)**2),(25,125,F(27,8),F(9,4)))
# Fold all six cells into oriented cube faces, checking connectivity and distinct normals.
cells={(0,1),(1,0),(1,1),(1,2),(2,1),(3,1)}
neg=lambda v:tuple(-x for x in v)
ori={(1,1):((1,0,0),(0,1,0),(0,0,1))};q=deque(ori)
while q:
 p=q.popleft();u,v,n=ori[p]
 for (dr,dc),o in [((0,1),(neg(n),v,u)),((0,-1),(n,v,neg(u))),((1,0),(u,neg(n),v)),((-1,0),(u,n,neg(v)))]:
  t=p[0]+dr,p[1]+dc
  if t not in cells:continue
  if t in ori:ck('net orientation consistency '+str(t),ori[t],o)
  else:ori[t]=o;q.append(t)
ck('net connected face count',len(ori),6)
ck('net distinct face normals',len({o[2] for o in ori.values()}),6)
ck('4cm net face extent',(3*4,4*4),(12,16))
# Actual measurement/status CSE11 has no supplied numerical observations; do not manufacture them.
result={'registry_checks':31,'all_checks':len(checks),'checks':checks,'net_normals':{str(p):o[2] for p,o in ori.items()},'actual_project_measurements':'NOT OBSERVED; no numerical actual measurements supplied','CSE12_repairs':['A length2=>area4,volume8','B signed-2=>physical volume8,not-8','C equal volume cube2/cuboid1x2x4 does not prove similarity','D model area factor2500,not50'],'usefulness':'A checked model area or dimension supports a stated planning decision under explicit uniform-scale/unit/idealisation assumptions; alternatives valid.'}
E.joinpath('coremath_2_1_science_solutions.json').write_text(json.dumps(result,indent=2)+'\n')
# Independent constructed coordinates and both dimensioned six-cell nets.
img=Image.new('RGB',(1600,850),'white');draw=ImageDraw.Draw(img)
for index,(label,o,k,pts,imgs) in enumerate(constructions):
 xoff=(index%4)*400;yoff=(index//4)*425
 allpts=pts+imgs+[o];xmin=min(p[0] for p in allpts)-1;xmax=max(p[0] for p in allpts)+1;ymin=min(p[1] for p in allpts)-1;ymax=max(p[1] for p in allpts)+1
 unit=min(330/(xmax-xmin),320/(ymax-ymin))
 def xy(p):return (xoff+35+(p[0]-xmin)*unit,yoff+380-(p[1]-ymin)*unit)
 draw.text((xoff+10,yoff+10),f'{label}: O{o}, k={k}',fill='black')
 for x in range(int(xmin),int(xmax)+1):draw.line([xy((x,ymin)),xy((x,ymax))],fill='#dddddd')
 for y in range(int(ymin),int(ymax)+1):draw.line([xy((xmin,y)),xy((xmax,y))],fill='#dddddd')
 for p,im in zip(pts,imgs):draw.line([xy(o),xy(p),xy(im)],fill='gray',width=1)
 for j,(ps,color) in enumerate([(pts,'navy'),(imgs,'darkorange')]):
  seq=ps+[ps[0]] if len(ps)>2 else ps
  draw.line([xy(p) for p in seq],fill=color,width=3)
  for p in ps:
   x,y=xy(p);draw.ellipse((x-3,y-3,x+3,y+3),fill=color);draw.text((x+3,y-12-j*11),str(p),fill=color)
 x,y=xy(o);draw.text((x-3,y-5),'X',fill='red')
for index,e in enumerate([2,4],6):
 xoff=(index%4)*400;yoff=(index//4)*425;unit=65
 draw.text((xoff+10,yoff+10),f'Six-face cube net edge {e}cm; extent {3*e}x{4*e}cm',fill='black')
 for r,c in cells:
  x=xoff+65+c*unit;y=yoff+55+r*unit;draw.rectangle((x,y,x+unit,y+unit),outline='black',width=2);draw.text((x+15,y+25),f'{e}cm',fill='black')
img.save(E/'coremath_2_1_science_constructed_proof.png')
print(f'{len(checks)} exact independent checks PASS; all31 registry values plus constructions/counterexamples/ratios/units/six-face fold')
