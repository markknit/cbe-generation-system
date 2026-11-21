from pathlib import Path
import math,json
from PIL import Image,ImageDraw,ImageFont
E=Path(__file__).parent;r=json.loads((E/'independent_checks.json').read_text());panels=r['panels']+[{'label':k,'points':v,'images':[],'mirror':None} for k,v in r['triangles'].items()];im=Image.new('RGB',(1600,2000),'white');d=ImageDraw.Draw(im);f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
for j,p in enumerate(panels):
 ox=j%4*400;oy=j//4*400;pts=p['points'];out=p['images'];allp=pts+out;lo=[math.floor(min(v[i] for v in allp))-1 for i in range(2)];hi=[math.ceil(max(v[i] for v in allp))+1 for i in range(2)];s=min(310/(hi[0]-lo[0]),300/(hi[1]-lo[1]));at=lambda v:(ox+45+(v[0]-lo[0])*s,oy+45+(hi[1]-v[1])*s);d.text((ox+10,oy+10),p['label'],font=ft,fill='black')
 for x in range(lo[0],hi[0]+1):
  a,b=at((x,lo[1])),at((x,hi[1]));d.line([a,b],fill='#dddddd');d.text((a[0]-4,a[1]+4),str(x),font=f,fill='black')
 for y in range(lo[1],hi[1]+1):
  a,b=at((lo[0],y)),at((hi[0],y));d.line([a,b],fill='#dddddd');d.text((a[0]-25,a[1]-6),str(y),font=f,fill='black')
 if p['mirror']:
  a,b,c=p['mirror'];hits=[]
  if b:
   for x in [lo[0],hi[0]]:
    y=-(a*x+c)/b
    if lo[1]<=y<=hi[1]:hits.append(at((x,y)))
  if a:
   for y in [lo[1],hi[1]]:
    x=-(b*y+c)/a
    if lo[0]<=x<=hi[0]:hits.append(at((x,y)))
  if len(hits)>1:d.line(hits[:2],fill='black',width=2)
  for a,b in zip(pts,out):d.line([at(a),at(b)],fill='#aaaaaa')
 for group,col,prime in [(pts,'#1965b0',False),(out,'#c43c39',True)]:
  if not group:continue
  xy=[at(v) for v in group]
  if len(xy)>1:d.line(xy+([xy[0]] if len(xy)>2 else []),fill=col,width=2)
  for i,v in enumerate(group):
   x,y=at(v);d.ellipse((x-3,y-3,x+3,y+3),fill=col);d.text((x+4,y+(4 if prime else -17)),chr(65+i)+("'" if prime else ''),font=f,fill=col)
 d.text((ox+10,oy+375),'Equal x/y scale; blue object, red reflection',font=f,fill='black')
im.save(E/'independent_constructions.png')
