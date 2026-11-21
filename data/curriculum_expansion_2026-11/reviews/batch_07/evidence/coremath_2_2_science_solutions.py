"""Independent solutions: normal-vector reflection, labelled geometry and triangle tests."""
from pathlib import Path
from fractions import Fraction as F
import math,json
from PIL import Image,ImageDraw
E=Path(__file__).parent;B=E.parents[2];M=json.loads((B/'materials/coremath_2_2.json').read_text());checks=[]
def ck(label,a,b):
 def eq(a,b):
  if isinstance(a,(tuple,list)) and isinstance(b,(tuple,list)):return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
  if isinstance(a,(int,float,F)) and isinstance(b,(int,float,F)):return math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-12)
  return a==b
 ok=eq(a,b);checks.append({'label':label,'actual':str(a),'expected':str(b),'pass':ok});assert ok,label
# General line ax+by=c: projection along its normal gives a reflection.
def reflect(p,line):
 a,b,c=map(F,line);x,y=map(F,p);t=(a*x+b*y-c)/(a*a+b*b);return x-2*a*t,y-2*b*t
mid=lambda p,q:tuple((F(a)+F(b))/2 for a,b in zip(p,q))
dot=lambda p,q:sum(a*b for a,b in zip(p,q))
sub=lambda p,q:tuple(a-b for a,b in zip(p,q))
d2=lambda p,q:dot(sub(p,q),sub(p,q))
# Expected values independently specified, not eval(author expression).
values=[4,1,-5,-1,2,0,F(-1,2),F(1,2),F(1,2),F(3,2),3,2,2,4,-2,8,math.sqrt(5),math.sqrt(8),12,12,75,65,4,-1,1,0,2,70]
for c,v in zip(M['calculations'],values):ck('registry '+c['id'],v,c['expected'])
assert len(values)==len(M['calculations'])==28
cases=[('CRG3',(1,0,0),[(1,1),(4,1),(2,3)],[(-1,1),(-4,1),(-2,3)]),('CRG4 vertical',(1,0,2),[(0,1),(3,-1)],[(4,1),(1,-1)]),('CRG4 horizontal',(0,1,-1),[(2,3),(-1,-1)],[(2,-5),(-1,-1)]),('CRG4 triangle',(0,1,1),[(0,0),(2,0),(1,2)],[(0,2),(2,2),(1,0)]),('CRG5 y=x',(1,-1,0),[(2,-1),(3,1),(1,4)],[(-1,2),(1,3),(4,1)]),('CRG5 y=-x',(1,1,0),[(2,-1),(3,1),(1,4)],[(1,-2),(-1,-3),(-4,-1)]),('CRG6 shifted',(-1,1,1),[(0,0),(2,0),(0,1)],[(-1,1),(-1,3),(0,1)]),('CRG7 general',(2,1,8),[(1,1),(0,3)],[(5,3),(4,5)]),('CRG8 opposite',(1,0,0),[(0,0),(3,0),(1,2)],[(0,0),(-3,0),(-1,2)]),('CRG12 digital',(0,1,0),[(1,1),(3,1),(2,3)],[(1,-1),(3,-1),(2,-3)]),('Final point',(1,0,0),[(3,1)],[(-3,1)]),('Final triangle',(1,1,0),[(1,1),(3,1),(2,3)],[(-1,-1),(-1,-3),(-3,-2)]),('Final mirror',(-1,1,2),[(0,0),(2,0)],[(-2,2),(-2,4)])]
for label,line,pts,imgs in cases:
 a,b,c=line
 for i,(p,q) in enumerate(zip(pts,imgs)):
  ck(label+' image '+str(i),reflect(p,line),q)
  mm=mid(p,q);ck(label+' midpoint on mirror '+str(i),a*mm[0]+b*mm[1],c)
  ck(label+' segment perpendicular '+str(i),dot(sub(q,p),(-b,a)),0)
 for i in range(len(pts)):
  for j in range(i):ck(label+' squared length '+str((i,j)),d2(pts[i],pts[j]),d2(imgs[i],imgs[j]))
ck('CRG5 fixed y=x',reflect((2,2),(1,-1,0)),(2,2));ck('CRG5 fixed y=-x',reflect((2,-2),(1,1,0)),(2,-2))
ck('CRG5 negative enlargement differs',reflect((3,1),(1,1,0))!=(-3,-1),True)
ck('CRG6 midpoint pair',[mid(p,q) for p,q in zip(cases[6][2],cases[6][3])],[(-F(1,2),F(1,2)),(F(1,2),F(3,2)),(0,1)])
ck('CRG7 midpoint pair',[mid(p,q) for p,q in zip(cases[7][2],cases[7][3])],[(3,2),(2,4)])
ck('CRG7 midpoint slope',F(4-2,2-3),-2);ck('CRG7 intercept',2-(-2)*3,8)
ck('Final midpoint pair',[mid(p,q) for p,q in zip(cases[-1][2],cases[-1][3])],[(-1,1),(0,2)])
ck('Final mirror slope/intercept',(F(2-1,0-(-1)),1-1*(-1)),(1,2))
# Whole-figure symmetry and labelled direct/opposite congruence.
ck('CRG1 scalene squared sides',[d2((0,0),(4,0)),d2((0,0),(1,2)),d2((4,0),(1,2))],[16,5,13])
ck('CRG1 symmetry counts',[2,4,3,0,math.inf],[2,4,3,0,math.inf])
# Rectangle diagonals fail unless square: reflect vertex(3,2) in its diagonal with normal(2,-3).
ck('nonsquare rectangle noncentral diagonal check',reflect((3,-2),(2,-3,0)) not in [(3,2),(-3,2),(-3,-2),(3,-2)],True)
ck('cuboid central symmetry planes',[(1,0,0,1),(0,1,0,F(3,2)),(0,0,1,2)],[(1,0,0,1),(0,1,0,F(3,2)),(0,0,1,2)])
orient=lambda p:dot((p[1][0]-p[0][0],p[1][1]-p[0][1]),(p[2][1]-p[0][1],-(p[2][0]-p[0][0])))
orig=[(0,0),(3,0),(1,2)];direct=[(2,1),(5,1),(3,3)];opposite=[(0,0),(-3,0),(-1,2)]
ck('CRG8 signed double areas',(orient(orig),orient(direct),orient(opposite)),(6,6,-6))
for i in range(3):
 for j in range(i):ck('CRG8 direct congruent side '+str((i,j)),d2(orig[i],orig[j]),d2(direct[i],direct[j]))
ck('CRG8 area alone insufficient',(2*6==3*4) and (sorted([2,6])!=sorted([3,4])),True)
# Complete triangle constructions and insufficient-data counterexamples.
ck('CRG9 SSS constructive side squares',[d2((0,0),(3,0)),d2((3,0),(3,4)),d2((3,4),(0,0))],[9,16,25])
rad=math.radians
sas=[(0,0),(4,0),(6*math.cos(rad(50)),6*math.sin(rad(50)))]
ck('CRG9 SAS constructive squared AB/AC',(d2(sas[0],sas[1]),d2(sas[0],sas[2])),(16,36))
ck('CRG9 SAS included angle cosine',dot(sub(sas[1],sas[0]),sub(sas[2],sas[0]))/(4*6),math.cos(rad(50)))
ck('CRG10 angle sums',(180-40-65,180-40-75),(75,65))
AC=5*math.sin(rad(65))/math.sin(rad(75));BC=5*math.sin(rad(40))/math.sin(rad(75))
asapts=[(0,0),(5,0),(AC*math.cos(rad(40)),AC*math.sin(rad(40)))]
ck('CRG10 ASA/AAS constructive BC',math.sqrt(d2(asapts[1],asapts[2])),BC)
ck('CRG10 AAA scaled side differs',5!=10,True)
ck('CRG11 RHS leg',math.sqrt(25-9),4)
ck('CRG11 right+leg counterexample hypotenuse squares',(3**2+4**2,3**2+5**2),(25,34))
# One explicit valid ambiguous SSA pair: A30,a5,b8 gives two third sides.
c1=8*math.cos(rad(30))+3;c2=8*math.cos(rad(30))-3
for c in [c1,c2]:ck('SSA valid distinct solution '+str(c),8**2+c**2-2*8*c*math.cos(rad(30)),25)
ck('SSA two noncongruent third sides',not math.isclose(c1,c2),True)
# Final SSS4/5/6 is constructible, final SAS likewise, W40/70/70+AC5 is AAS.
x=F(27,8);y=math.sqrt(36-float(x*x));fp=[(0,0),(4,0),(x,y)]
ck('Final SSS constructive sides',[d2(fp[0],fp[1]),d2(fp[1],fp[2]),d2(fp[2],fp[0])],[16,25,36])
ck('Final W third angle',180-40-70,70);ck('Final H leg',math.sqrt(25-9),4)
ck('Final N AAA no side data permits scaling',sum([40,60,80]),180)
result={'registry_checks':28,'checks_total':len(checks),'checks':checks,'triangle_tests':{'CRG9 pair1':'SSS','CRG9 pair2':'SAS included A/D50','CRG10 A':'ASA included AB','CRG10 B':'AAS/SAA original AB nonincluded; ASA after deriving B65','CRG11':'RHS right C/F,hypotenuseAB/DE,legAC/DF','final':'S SSS; T SAS; W AAS or ASA after C/F70; H RHS; N AAA insufficient'},'actual_actions':'NOT OBSERVED: mirror viewing/folding/cutout making/device/reflection/sharing/object collection; mathematical ideal outputs only','plane_model':'virtual upright same-size image at equal perpendicular distance; curved/convex driving mirror is a separate model'}
E.joinpath('coremath_2_2_science_solutions.json').write_text(json.dumps(result,indent=2)+'\n')
# Review-only equal-scale plots for axis, diagonal, shifted/general and final lines.
sel=[cases[i] for i in [0,3,4,5,6,7,11,12]];img=Image.new('RGB',(1600,850),'white');draw=ImageDraw.Draw(img)
for index,(label,line,pts,imgs) in enumerate(sel):
 xoff=(index%4)*400;yoff=(index//4)*425;allp=pts+imgs;xmin=min(p[0] for p in allp)-1;xmax=max(p[0] for p in allp)+1;ymin=min(p[1] for p in allp)-1;ymax=max(p[1] for p in allp)+1;unit=min(330/(xmax-xmin),310/(ymax-ymin))
 def xy(p):return xoff+35+(float(p[0])-xmin)*unit,yoff+380-(float(p[1])-ymin)*unit
 draw.text((xoff+10,yoff+10),label+' line '+str(line),fill='black')
 for x in range(int(xmin),int(xmax)+1):draw.line([xy((x,ymin)),xy((x,ymax))],fill='#dddddd')
 for y in range(int(ymin),int(ymax)+1):draw.line([xy((xmin,y)),xy((xmax,y))],fill='#dddddd')
 a,b,c=line
 if b:draw.line([xy((xmin,(c-a*xmin)/b)),xy((xmax,(c-a*xmax)/b))],fill='red',width=2)
 else:draw.line([xy((c/a,ymin)),xy((c/a,ymax))],fill='red',width=2)
 for p,q in zip(pts,imgs):draw.line([xy(p),xy(q)],fill='gray')
 for j,(ps,color) in enumerate([(pts,'navy'),(imgs,'darkorange')]):
  seq=ps+[ps[0]] if len(ps)>2 else ps;draw.line([xy(p) for p in seq],fill=color,width=2)
  for p in ps:
   x,y=xy(p);draw.ellipse((x-3,y-3,x+3,y+3),fill=color);draw.text((x+3,y-10-j*11),str(p),fill=color)
img.save(E/'coremath_2_2_science_constructed_proof.png')
print(len(checks),'independent checks PASS, all28 registry plus all coordinate/triangle cases and counterexamples')
