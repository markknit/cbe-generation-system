"""Independent read-only geometry, raster tick and actual Word frame verification."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json,math,hashlib,zipfile
from PIL import Image
E=Path(__file__).parent;B=E.parents[2];svg=B/'materials/diagrams/CTG12.svg';png=B/'materials/diagrams/CTG12.png';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();S={'s':'http://www.w3.org/2000/svg'};r=ET.parse(svg).getroot();checks=[]
def ck(label,a,b,tol=1e-8):
 if isinstance(a,(tuple,list)) and isinstance(b,(tuple,list)):ok=len(a)==len(b) and all(math.isclose(float(x),float(y),abs_tol=tol,rel_tol=0) for x,y in zip(a,b))
 elif isinstance(a,(float,int)) and isinstance(b,(float,int)):ok=math.isclose(a,b,abs_tol=tol,rel_tol=0)
 else:ok=a==b
 checks.append({'label':label,'actual':str(a),'expected':str(b),'pass':ok});assert ok,label
ck('SVG viewBox',r.attrib['viewBox'],'0 0 1600 1120');im=Image.open(png).convert('RGB');ck('PNG dimensions',im.size,(1600,1120))
center=r.find('s:circle',S);ck('pivot centre',(float(center.attrib['cx']),float(center.attrib['cy'])),(800,230))
lines=r.findall('s:line',S);ck('baseline plus181degree ticks',len(lines),182)
base=lines[0];ck('baseline endpoints',[float(base.attrib[k]) for k in ['x1','y1','x2','y2']],[150,230,1450,230])
arc=r.find('s:polyline',S);pts=[tuple(map(float,p.split(','))) for p in arc.attrib['points'].split()];ck('semicircle vertex count',len(pts),181)
for degree,(tick,point) in enumerate(zip(lines[1:],pts)):
 angle=math.radians(degree);expected=(800+650*math.cos(angle),230+650*math.sin(angle));ck(f'SVG arc{degree}',point,expected)
 a=tuple(float(tick.attrib[k]) for k in ['x1','y1']);b=tuple(float(tick.attrib[k]) for k in ['x2','y2']);ck(f'SVG outertick{degree}',b,expected)
 length=58.5 if degree%10==0 else 32.5 if degree%5==0 else 16.25
 inner=(800+(650-length)*math.cos(angle),230+(650-length)*math.sin(angle));ck(f'SVG innertick{degree}',a,inner)
 # The actual supplied PNG has a visible dark radial tick at radius642 for every degree.
 x=800+642*math.cos(angle);y=230+642*math.sin(angle);ix,iy=round(x),round(y)
 dark=any(max(im.getpixel((xx,yy)))<80 for xx in range(ix-2,ix+3) for yy in range(iy-2,iy+3))
 ck(f'PNG visible tick{degree}',dark,True)
texts=r.findall('s:text',S);labels={int(t.text):t for t in texts if (t.text or '').isdigit()};ck('numeric degree labels',sorted(labels),list(range(0,181,10)))
for degree,t in labels.items():
 a=math.radians(degree);x=800+539.5*math.cos(a);y=230+539.5*math.sin(a)+(30 if degree in [0,180] else 0)
 ck(f'SVG numeral position{degree}',(float(t.attrib['x']),float(t.attrib['y'])),(x,y))
ck('SVG90 directly below pivot',float(labels[90].attrib['x']),800)
required=['Attach sight edge along baseline; attach string at centre dot.','Level sight: string reads 90°. Angle magnitude = |90° − reading|.','Record UP or DOWN separately. Uniform resizing preserves angles.']
for s in required:ck('SVG instruction '+s,any(t.text==s for t in texts),True)
# Actual Word embedded bytes and effective picture frame preserve angle geometry.
D=json.loads((B/'manuscripts/coremath_2_4.json').read_text());O=B/'outputs/v2/Core_Mathematics/SS2.4_Trigonometry_1';N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','a':'http://schemas.openxmlformats.org/drawingml/2006/main','pic':'http://schemas.openxmlformats.org/drawingml/2006/picture','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'};word={}
for typ in ['CompactTeacherGuide','StudentMaterials','MaterialsTeacherKey','StudentSummaryTable','AssessmentMaterials']:
 p=O/(D['prefix']+'_'+typ+'.docx')
 with zipfile.ZipFile(p) as z:
  rt=ET.fromstring(z.read('word/document.xml'));media={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')};frames=[]
  for frame in rt.findall('.//wp:inline',N)+rt.findall('.//wp:anchor',N):
   ext=frame.find('wp:extent',N);crop=frame.find('.//a:srcRect',N);inner=frame.find('.//a:xfrm/a:ext',N)
   if ext is not None:
    a={k:int(v) for k,v in ext.attrib.items()};frames.append({'extent':a,'crop':crop.attrib if crop is not None else None,'inner_extent':inner.attrib if inner is not None else None});ck(typ+' physical frame aspect',a['cx']/a['cy'],1600/1120,1e-6);ck(typ+' no crop',crop is None,True)
  ck(typ+' expected media hash set',set(media.values()),{sha(png)} if typ in ['StudentMaterials','MaterialsTeacherKey'] else set())
  ck(typ+' picture count',len(frames),1 if typ in ['StudentMaterials','MaterialsTeacherKey'] else 0)
  word[typ]={'docx_sha256':sha(p),'media':media,'frames':frames}
result={'checks_total':len(checks),'checks':checks,'asset_hashes':{'CTG12.png':sha(png),'CTG12.svg':sha(svg)},'word_frames':word,'scope':'All original SVGdegree positions,visible PNGticks and actual five-Word media bytes/frames;no production rendering or physical instrument observation. Uniform framing preserves aspect;actual physical alignment/free-plumb/vertical-plane/level calibration remains teacher observed.'}
E.joinpath('coremath_2_4_clinometer_geometry.json').write_text(json.dumps(result,indent=2)+'\n');print(len(checks),'clinometer geometry/raster/actual Word frame checks PASS')
