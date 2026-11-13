"""Draw geometry schematics from the same explicit dimensions used by the cards."""
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[2]/'data/codex_pilot_2026-11/materials/diagrams';B.mkdir(exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
def panel(draw,origin,title,points,labels,lines=()):
 ox,oy=origin;draw.text((ox+20,oy+10),title,fill='black',font=font)
 def p(v):return (ox+70+v[0]*40,oy+380-v[1]*40)
 draw.polygon([p(v) for v in points],outline='#174b6b',width=4)
 for a,b in lines:draw.line([p(a),p(b)],fill='#777777',width=2)
 for x,y,t in labels:draw.text(p((x,y)),t,fill='black',font=small)

def sheet(name,panels):
 rows=(len(panels)+1)//2;im=Image.new('RGB',(1300,rows*500+80),'white');d=ImageDraw.Draw(im)
 for i,p in enumerate(panels):panel(d,((i%2)*650,(i//2)*500),*p)
 d.text((30,rows*500+20),'Schematic: use stated dimensions; measure only when the task requests a scale drawing.',font=small,fill='black')
 im.save(B/(name+'.png'))

h=8*math.sin(math.radians(30));x=8*math.cos(math.radians(30))
sheet('C1',[('C1: triangle ABC',[(0,0),(10,0),(x,h)],[(-.5,-.5,'A'),(10,-.5,'B'),(x,h+.5,'C'),(4,-.8,'10 m'),(2,2,'8 m'),(.5,.7,'30°'),(x+.2,1.8,'h')],[((x,0),(x,h))])])
sheet('C5',[('C5(a): parallelogram',[(0,0),(12,0),(14,5),(2,5)],[(5,-.8,'12 m'),(2.2,2,'5 m')],[((2,0),(2,5))]),('C5(b): trapezium',[(0,0),(14,0),(11,4),(3,4)],[(5,-.8,'14 m'),(5,4.3,'8 m'),(3.2,1.7,'4 m')],[((3,0),(3,4))])])
sheet('C9',[('C9: missing top-right corner',[(0,0),(10,0),(10,5),(6,5),(6,8),(0,8)],[(3,-.8,'10 m'),(-1.5,3,'8 m'),(7,5.3,'4 m'),(6.2,6.5,'3 m')])])
sheet('C10',[('C10: ordered coordinate plan',[(0,0),(8,0),(8,3),(5,3),(5,6),(0,6)],[(-1,-.8,'(0,0)'),(7,-.8,'(8,0)'),(8.1,2.7,'(8,3)'),(4.4,2.2,'(5,3)'),(5,6.4,'(5,6)'),(-1.3,6.4,'(0,6)')])])
# The assessment diagrams supply exactly the stated dimensions, not derived heights/areas.
a=6*math.cos(math.radians(30));b=6*math.sin(math.radians(30))
sheet('C12',[('C12 A',[(0,0),(8,0),(a,b)],[(3,-.8,'8 m'),(1,2,'6 m'),(.8,.8,'30°')]),('C12 B',[(0,0),(6,0),(3,4)],[(2,-.8,'6 m'),(.2,2,'5 m'),(4.5,2,'5 m')]),('C12 C',[(0,0),(10,0),(8,3),(2,3)],[(4,-.8,'10 m'),(4,3.4,'6 m'),(2.2,1.4,'3 m')],[((2,0),(2,3))]),('C12 E: missing top-right corner',[(0,0),(9,0),(9,5),(6,5),(6,7),(0,7)],[(3,-.8,'9 m'),(-1.5,3,'7 m'),(7,5.3,'3 m'),(6.2,6,'2 m')])])
print('Wrote',len(list(B.glob('*.png'))),'geometry sheets')
