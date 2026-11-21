from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
P=Path(__file__).resolve().parent
im=Image.new('RGB',(1500,1000),'white');d=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
scenes=[('Centre recovery: O=(1,1), k=2',(1,1),[(2,1),(4,1),(2,3)],[(3,1),(7,1),(3,5)],(0,8,0,6)),('Origin k=2',(0,0),[(1,1),(3,1),(1,2)],[(2,2),(6,2),(2,4)],(-1,7,-1,5)),('Nonorigin k=1/2',(2,1),[(4,3),(8,3),(4,7)],[(3,2),(5,2),(3,4)],(0,9,0,8)),('Origin k=-2; physical length ratio2',(0,0),[(1,1),(3,1),(1,2)],[(-2,-2),(-6,-2),(-2,-4)],(-7,4,-5,3)),('Final origin k=1/2',(0,0),[(2,2),(6,2),(2,4)],[(1,1),(3,1),(1,2)],(-1,7,-1,5))]
for index,(title,o,orig,img,bounds) in enumerate(scenes):
 xoff=(index%3)*500;yoff=(index//3)*500;d.text((xoff+15,yoff+12),title,fill='black',font=font);xmin,xmax,ymin,ymax=bounds;scale=min(430/(xmax-xmin),390/(ymax-ymin));ox=xoff+40;oy=yoff+450
 def xy(p):return (ox+(p[0]-xmin)*scale,oy-(p[1]-ymin)*scale)
 for x in range(xmin,xmax+1):d.line([xy((x,ymin)),xy((x,ymax))],fill='#e0e0e0');d.text(xy((x,0)),str(x),fill='#666666',font=small)
 for y in range(ymin,ymax+1):d.line([xy((xmin,y)),xy((xmax,y))],fill='#e0e0e0');d.text(xy((0,y)),str(y),fill='#666666',font=small)
 d.line([xy((xmin,0)),xy((xmax,0))],fill='black');d.line([xy((0,ymin)),xy((0,ymax))],fill='black')
 for p,q in zip(orig,img):d.line([xy(o),xy(p),xy(q)],fill='#999999',width=1)
 for pts,color,tag in [(orig,'#1263a0',''),(img,'#c53a2a',"'")]:
  d.line([xy(p) for p in pts+[pts[0]]],fill=color,width=3)
  for name,p in zip('ABC',pts):
   x,y=xy(p);d.ellipse((x-3,y-3,x+3,y+3),fill=color);d.text((x+4,y-17),name+tag+str(p),fill=color,font=small)
 x,y=xy(o);d.ellipse((x-4,y-4,x+4,y+4),outline='black',width=2);d.text((x+5,y+5),'O'+str(o),fill='black',font=small)
xoff=1000;yoff=500;d.text((xoff+15,yoff+12),'Cube net: target edge2cm or4cm',fill='black',font=font)
for r,c in [(0,1),(1,0),(1,1),(1,2),(2,1),(3,1)]:
 x=xoff+90+c*85;y=yoff+75+r*85;d.rectangle((x,y,x+85,y+85),outline='black',width=2);d.text((x+9,y+33),str((r,c)),font=font,fill='#1263a0')
d.text((1015,940),'Fold proof: 6 faces, 8 vertices, 12 paired edges.',fill='black',font=font)
im.save(P/'independent_construction_proof.png')
