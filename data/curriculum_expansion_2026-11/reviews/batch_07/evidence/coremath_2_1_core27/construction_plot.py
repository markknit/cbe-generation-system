from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
E=Path(__file__).parent;data=json.loads((E/'independent_checks.json').read_text())['constructions'];im=Image.new('RGB',(1500,1000),'white');d=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14);title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for j,c in enumerate(data):
 ox=(j%3)*500;oy=(j//3)*500;pts=c['points'];out=c['images'];o=c['centre'];allp=pts+out+[o,(0,0)];xmin=math.floor(min(p[0] for p in allp))-1;xmax=math.ceil(max(p[0] for p in allp))+1;ymin=math.floor(min(p[1] for p in allp))-1;ymax=math.ceil(max(p[1] for p in allp))+1;scale=min(380/(xmax-xmin),370/(ymax-ymin));left=ox+70;top=oy+65
 def at(p):return(left+(p[0]-xmin)*scale,top+(ymax-p[1])*scale)
 d.text((ox+20,oy+15),f"{c['label']}   O={tuple(o)}   k={c['factor']}",font=title,fill='black')
 for x in range(xmin,xmax+1):
  a,b=at((x,ymin)),at((x,ymax));d.line([a,b],fill='#dddddd');d.text((a[0]-5,a[1]+5),str(x),font=font,fill='black')
 for y in range(ymin,ymax+1):
  a,b=at((xmin,y)),at((xmax,y));d.line([a,b],fill='#dddddd');d.text((a[0]-27,a[1]-6),str(y),font=font,fill='black')
 for p,q in zip(pts,out):d.line([at(o),at(p),at(q)],fill='#888888',width=1)
 for group,col,tag in [(pts,'#1965b0','object'),(out,'#c43c39','image')]:
  xy=[at(p) for p in group]
  if len(xy)>2:d.line(xy+[xy[0]],fill=col,width=2)
  else:d.line(xy,fill=col,width=2)
  for i,p in enumerate(group):
   a=at(p);d.ellipse((a[0]-3,a[1]-3,a[0]+3,a[1]+3),fill=col);d.text((a[0]+5,a[1]+(4 if tag=='image' else -17)),chr(65+i)+("'" if tag=='image' else ''),font=font,fill=col)
 a=at(o);d.ellipse((a[0]-4,a[1]-4,a[0]+4,a[1]+4),outline='black',width=2);d.text((a[0]-16,a[1]+5),'O',font=font,fill='black');d.text((ox+20,oy+465),'Blue: object; red: calculated image; equal x/y scale',font=font,fill='black')
im.save(E/'independent_constructions.png')
