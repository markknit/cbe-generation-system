from pathlib import Path
import math,json
from PIL import Image,ImageDraw,ImageFont
E=Path(__file__).parent;ps=json.loads((E/'independent_checks.json').read_text())['panels'];im=Image.new('RGB',(1500,1200),'white');d=ImageDraw.Draw(im);f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for j,p in enumerate(ps):
 ox=j%4*375;oy=j//4*400;pts=p['points'];out=p['images'];o=p['centre'];allp=pts+out+[o];lo=[math.floor(min(v[i] for v in allp))-1 for i in range(2)];hi=[math.ceil(max(v[i] for v in allp))+1 for i in range(2)];s=min(290/(hi[0]-lo[0]),295/(hi[1]-lo[1]));at=lambda v:(ox+40+(v[0]-lo[0])*s,oy+45+(hi[1]-v[1])*s);d.text((ox+8,oy+10),f"{p['label']} O={tuple(o)} {p['angle']}deg",font=ft,fill='black')
 for x in range(lo[0],hi[0]+1):
  a,b=at((x,lo[1])),at((x,hi[1]));d.line([a,b],fill='#ddd');d.text((a[0]-4,a[1]+4),str(x),font=f,fill='black')
 for y in range(lo[1],hi[1]+1):
  a,b=at((lo[0],y)),at((hi[0],y));d.line([a,b],fill='#ddd');d.text((a[0]-25,a[1]-6),str(y),font=f,fill='black')
 for a,b in zip(pts,out):d.line([at(a),at(o),at(b)],fill='#aaaaaa')
 for group,col,prime in [(pts,'#1965b0',False),(out,'#c43c39',True)]:
  xy=[at(v) for v in group];d.line(xy+([xy[0]] if len(xy)>2 else []),fill=col,width=2)
  for i,v in enumerate(group):
   x,y=at(v);d.ellipse((x-3,y-3,x+3,y+3),fill=col);d.text((x+4,y+(4 if prime else -17)),chr(65+i)+("'" if prime else ''),font=f,fill=col)
 x,y=at(o);d.ellipse((x-4,y-4,x+4,y+4),outline='black',width=2);d.text((x-14,y+5),'O',font=f,fill='black');d.text((ox+8,oy+375),'Equal axis scales; positive angle is CCW',font=f,fill='black')
im.save(E/'independent_constructions.png')
