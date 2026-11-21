"""Reproduce dimensioned solids/net schematics with Python3+matplotlib;no model calls."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Wedge,Circle,Arc
OUT=Path(__file__).resolve().parent

def finish(f,name):
 f.tight_layout();f.savefig(OUT/(name+'.png'),dpi=150,bbox_inches='tight');plt.close(f)
def axsetup(a,title):a.set_aspect('equal');a.axis('off');a.set_title(title,fontsize=11)
def line(a,x,y,style='k-'):a.plot(x,y,style,lw=1)
# Dimensioned face nets;not physical print-scale templates.
f,axes=plt.subplots(1,2,figsize=(10,6))
a=axes[0];axsetup(a,'SV1: rectangular prism net\nAll face dimensions cm;not to scale')
for x,y,w,h in [(0,0,8,5),(0,5,8,3),(0,-3,8,3),(-3,0,3,5),(8,0,3,5),(0,8,8,5)]:
 a.add_patch(Rectangle((x,y),w,h,fc='#e1efff',ec='navy'));a.text(x+w/2,y+h/2,f'{w} × {h}',ha='center',va='center',fontsize=11)
a.set_xlim(-5,13);a.set_ylim(-5,15)
a=axes[1];axsetup(a,'SV1: right-triangular prism net\nEnd triangles:legs3,4;hypotenuse5 cm')
for x,y,w,h in [(0,0,10,4),(0,4,10,3),(0,-5,10,5)]:
 a.add_patch(Rectangle((x,y),w,h,fc='#e1efff',ec='navy'));a.text(x+w/2,y+h/2,f'{w} × {h}',ha='center',va='center',fontsize=11)
for pts in [[(0,0),(0,4),(-3,4)],[(10,0),(10,4),(13,4)]]:a.add_patch(Polygon(pts,fc='#ffecd2',ec='black'))
a.text(-2,4.4,'3');a.text(12,4.4,'3');a.set_xlim(-5,15);a.set_ylim(-7,10);finish(f,'SV1')
f,a=plt.subplots(figsize=(7,7));axsetup(a,'SV2: right square-pyramid net\nBase edges6 cm;each face altitude5 cm;not to scale')
a.add_patch(Rectangle((0,0),6,6,fc='#e1efff',ec='navy'));a.text(3,3,'6 × 6 cm',ha='center')
for pts in [[(0,6),(6,6),(3,11)],[(0,0),(6,0),(3,-5)],[(0,0),(0,6),(-5,3)],[(6,0),(6,6),(11,3)]]:a.add_patch(Polygon(pts,fc='#ffecd2',ec='black'))
line(a,[3,3],[6,11],'k--');a.text(3.4,8.5,'5 cm\nface altitude',fontsize=10);a.set_xlim(-6,12);a.set_ylim(-6,12);finish(f,'SV2')
f,axes=plt.subplots(1,2,figsize=(10,4.7));a=axes[0];axsetup(a,'SV3: cone curved-surface sector\nNet radius=slant5 cm;angle216°')
a.add_patch(Wedge((0,0),5,0,216,fc='#e1efff',ec='navy'));a.text(.5,.5,'216°');line(a,[0,5],[0,0]);a.text(2.2,-.6,'5 cm');a.set_xlim(-6,6);a.set_ylim(-4,6)
a=axes[1];axsetup(a,'SV3: base disk\nRadius3 cm')
a.add_patch(Circle((0,0),3,fc='#ffecd2',ec='black'));line(a,[0,3],[0,0]);a.text(1.2,.3,'3 cm');a.set_xlim(-4,4);a.set_ylim(-4,4);finish(f,'SV3')
def frustum(a,R,r,h,s,title):
 axsetup(a,title+'\nAxial section;not to print scale')
 a.add_patch(Polygon([(-R,0),(R,0),(r,h),(-r,h)],fc='#e1efff',ec='navy'))
 line(a,[0,R],[0,0]);line(a,[0,r],[h,h]);line(a,[0,0],[0,h],'k--')
 a.text(R/2,-.8,f'R={R} cm',ha='center');a.text(0,h+.4,f'r={r} cm',ha='center')
 a.text(.3,h/2,f'h={h} cm');a.text((R+r)/2+.5,h/2,f's={s} cm')
 a.set_xlim(-R-2,R+4);a.set_ylim(-1.4,h+1.4)
def cap(a,r,h,title):
 axsetup(a,title+'\nAxial section;not to print scale')
 a.add_patch(Rectangle((-r,0),2*r,h,fc='#e1efff',ec='navy'))
 a.add_patch(Wedge((0,h),r,0,180,fc='#ffecd2',ec='navy'))
 line(a,[-r,r],[h,h],'k--');line(a,[0,r],[h,h]);line(a,[0,0],[0,h+r],'k--')
 a.text(r+.4,h/2,f'cylinder h={h} cm',fontsize=10);a.text(.1,h+.3,f'r={r} cm',fontsize=10)
 a.text(0,-.8,'closed bottom',ha='center',fontsize=10);a.set_xlim(-r-1,r+4.5);a.set_ylim(-1.4,h+r+1)
f,a=plt.subplots(figsize=(8,4.5));frustum(a,5,2,4,5,'SV4: right circular frustum');finish(f,'SV4')
f,a=plt.subplots(figsize=(8,5));cap(a,3,4,'SV6: cylinder+hemisphere\nDashed joining disk is internal');finish(f,'SV6')
f,axes=plt.subplots(1,2,figsize=(11,5));frustum(axes[0],6,3,4,5,'SV14 F: closed frustum');cap(axes[1],2,6,'SV14 G: cylinder+hemisphere');finish(f,'SV14')
