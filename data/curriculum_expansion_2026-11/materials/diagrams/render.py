# Recreate committed mathematical figures with Python3 and matplotlib; no model calls.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Wedge,Polygon
from pathlib import Path
from math import sqrt,sin,cos,radians
out=Path(__file__).resolve().parent
def setup(title):
 f,a=plt.subplots(figsize=(8,5));a.set_aspect('equal');a.axis('off');a.set_title(title,fontsize=12);return f,a
def save(f,a,name):a.relim();a.autoscale_view();a.margins(.18);f.savefig(out/(name+'.png'),dpi=150,bbox_inches='tight');plt.close(f)
def line(a,p,q,label=None,offset=(0,0)):
 a.plot([p[0],q[0]],[p[1],q[1]],'k-',lw=1)
 if label:a.text((p[0]+q[0])/2+offset[0],(p[1]+q[1])/2+offset[1],label,fontsize=10,ha='center')
f,a=setup('CM21: concentric circles — not to scale');a.add_patch(Circle((0,0),7,fc='#deebff',ec='navy'));a.add_patch(Circle((0,0),4,fc='white',ec='navy'));line(a,(0,0),(7,0),'7 cm',(0,.3));line(a,(0,0),(0,-4),'4 cm',(-1,0));a.text(-.5,.3,'O');save(f,a,'CM21')
f,a=setup('CM23: minor sector AOB — not to scale');a.add_patch(Wedge((0,0),6,0,120,fc='#deebff',ec='navy'));line(a,(0,0),(6,0),'6 cm',(0,-.5));line(a,(0,0),(-3,3*sqrt(3)));a.text(.5,.6,'120°');a.text(-.5,-.5,'O');a.text(6.2,0,'A');a.text(-3,5.5,'B');save(f,a,'CM23')
f,a=setup('CM25: annular sector, common centre O — not to scale');a.add_patch(Wedge((0,0),10,0,72,width=4,fc='#deebff',ec='navy'));line(a,(0,0),(10,0),'R = 10 cm',(0,-.8));line(a,(0,0),(6*cos(radians(72)),6*sin(radians(72))),'r = 6 cm',(-1,.2));a.text(1.3,.7,'72°');a.text(-.5,-.5,'O');save(f,a,'CM25')
f,a=setup('CM26: chord AB subtends 90° at O; shade is minor segment');a.add_patch(Circle((0,0),8,fill=False,ec='navy'));a.add_patch(Wedge((0,0),8,0,90,fc='#deebff',ec='navy'));a.add_patch(Polygon([(0,0),(8,0),(0,8)],fc='white',ec='black'));line(a,(0,0),(8,0),'8 cm',(0,-.8));line(a,(0,0),(0,8),'8 cm',(-1,0));a.text(.8,.7,'90°');a.text(-.6,-.6,'O');a.text(8.2,0,'A');a.text(0,8.3,'B');save(f,a,'CM26')
def overlap(name,r1,r2,d,title,anglelabels,distance_label):
 f,a=setup(title);x=(r1*r1-r2*r2+d*d)/(2*d);h=sqrt(r1*r1-x*x)
 a.add_patch(Circle((0,0),r1,fc='#deebff',ec='navy',alpha=.5));a.add_patch(Circle((d,0),r2,fc='#ffe5c2',ec='#904e00',alpha=.5))
 P=(x,h);Q=(x,-h);line(a,(0,0),(d,0),'centre distance = '+distance_label+' cm',(0,-.8));line(a,P,Q)
 for c,r,label in [((0,0),r1,'O1'),((d,0),r2,'O2')]:
  line(a,c,P,str(r)+' cm',(-.4,.3));line(a,c,Q);a.text(c[0]-.3,-.4,label)
 a.text(x,h+.3,'P');a.text(x,-h-.6,'Q');a.text(d/2, -max(r1,r2)-1.3, anglelabels[0]+'; '+anglelabels[1], fontsize=11, ha='center')
 save(f,a,name)
overlap('CM28',5,5,sqrt(50),'CM28: overlap is bounded by the two minor arcs PQ',['angle P O1 Q = 90°','angle P O2 Q = 90°'],'5√2')
overlap('CM29',3,4,5,'CM29: P and Q are intersections\nTriangles O1 P O2 / O1 Q O2 are right at P / Q',['angle P O1 Q ≈ 106.260°','angle P O2 Q ≈ 73.740°'],'5')
overlap('CM212',6,6,6*sqrt(3),'CM212: independent task — overlap bounded by two minor arcs PQ',['angle P O1 Q = 60°','angle P O2 Q = 60°'],'6√3')
