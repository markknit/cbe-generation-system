from pathlib import Path
import math,json,hashlib,zipfile
from lxml import etree
from PIL import Image
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';O=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bank=json.loads((B/'materials/coremath_2_4.json').read_text()); checks=[]
def ck(n,a,b,tol=1e-11):
 ok=math.isclose(a,b,rel_tol=tol,abs_tol=tol);checks.append(dict(check=n,actual=a,expected=b,pass_=ok))
env={'sqrt':math.sqrt,'sin_deg':lambda x:math.sin(math.radians(x)),'cos_deg':lambda x:math.cos(math.radians(x)),'tan_deg':lambda x:math.tan(math.radians(x)),'atan_deg':lambda x:math.degrees(math.atan(x))}
for c in bank['calculations']:
 a=eval(c['expression'],{'__builtins__':{}},env);tol=c.get('absolute_tolerance',1e-11);ck('registry '+c['id'],a,c['expected'],tol)
 if c['id'].startswith(('sin_','cos_','tan_')):ck('strict four-decimal rounding '+c['id'],float(format(a,'.4f')),c['expected'])
for n,a,b in [('B sine',4/5,.8),('B cosine',3/5,.6),('B tangent',4/3,1.3333333333333333),('inverse sine degrees',math.degrees(math.asin(.6)),36.86989764584402),('unit isosceles Pythagoras',1+1,math.sqrt(2)**2),('equilateral split Pythagoras',1+math.sqrt(3)**2,4),('side-case Pythagoras',5**2+(5*math.sqrt(3))**2,100),('final Pythagoras',5**2+12**2,13**2),('calibration level',abs(90-90),0),('calibration left',abs(90-60),30),('calibration right',abs(90-120),30),('final exact tangent',5/12,(5/13)/(12/13)),('elevation total rounded',round(1.5+12/math.sqrt(3),2),8.43),('depression horizontal rounded',round(12*math.sqrt(3),2),20.78),('calibration rise rounded',round(5/math.sqrt(3),2),2.89),('field/final height rounded',round(1.4+10/math.sqrt(3),2),7.17),('final horizontal',8/math.tan(math.pi/4),8)]:ck(n,a,b)
for a,b in [(10,80),(20,70),(30,60),(40,50),(45,45)]:
 ck(f'sine cosine complement {a}/{b}',math.sin(math.radians(a)),math.cos(math.radians(b)))
 ck(f'cosine sine complement {a}/{b}',math.cos(math.radians(a)),math.sin(math.radians(b)))
for t in (30,45,60):
 sn,cs={30:(.5,math.sqrt(3)/2),45:(math.sqrt(2)/2,math.sqrt(2)/2),60:(math.sqrt(3)/2,.5)}[t]
 ck(f'exact sine {t}',math.sin(math.radians(t)),sn);ck(f'exact cosine {t}',math.cos(math.radians(t)),cs);ck(f'exact tangent {t}',math.tan(math.radians(t)),sn/cs)
# SVG native-coordinate geometry: one baseline,181 degree radial ticks,19 numbered labels.
svg=B/'materials/diagrams/CTG12.svg';png=B/'materials/diagrams/CTG12.png';root=etree.parse(str(svg));ns={'s':'http://www.w3.org/2000/svg'};lines=root.findall('.//s:line',ns);ticks=[]
for e in lines:
 x1,y1,x2,y2=[float(e.get(a)) for a in ('x1','y1','x2','y2')];d2=math.hypot(x2-800,y2-230)
 if abs(d2-650)<1e-6 and math.hypot(x2-x1,y2-y1)<100:
  ang=math.degrees(math.atan2(y2-230,x2-800));ticks.append(ang)
  ck('tick radial collinearity '+str(round(ang)),(x1-800)*(y2-230)-(y1-230)*(x2-800),0,1e-7)
ck('181 angular ticks',len(ticks),181)
for i,a in enumerate(sorted(ticks)):ck('tick angle '+str(i),a,i,1e-9)
labels=[]
for e in root.findall('.//s:text',ns):
 t=''.join(e.itertext())
 if t.isdigit():
  ang=int(t);x,y=float(e.get('x')),float(e.get('y'));labels.append(ang)
  if ang in (0,180):ck('endpoint label legibility offset '+t,y,260)
  else:ck('degree label position '+t,math.degrees(math.atan2(y-230,x-800)),ang,1e-9)
ck('19 labelled angles',len(labels),19)
baselines=[e for e in lines if e.get('x1')=='150' and e.get('x2')=='1450' and e.get('y1')=='230' and e.get('y2')=='230'];ck('diameter baseline',len(baselines),1)
# Centre dot may float lexical format; inspect geometry numerically.
circles=root.findall('.//s:circle',ns);ck('centre dot at pivot',sum(float(e.get('cx'))==800 and float(e.get('cy'))==230 for e in circles),1)
media=[];wns={'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
for p in sorted((B/'outputs/v2/Core_Mathematics/SS2.4_Trigonometry_1').glob('*.docx')):
 with zipfile.ZipFile(p) as z:
  names=[n for n in z.namelist() if n.startswith('word/media/')];tree=etree.fromstring(z.read('word/document.xml'))
  expect=p.stem.endswith(('_StudentMaterials','_MaterialsTeacherKey'));ck(p.name+' expected image count',len(names),int(expect))
  for n in names:
   b=z.read(n);original=hashlib.sha256(b).hexdigest()==sha(png);ck(p.name+' original image bytes',int(original),1)
   out=O/(p.stem+'_'+Path(n).name);out.write_bytes(b)
   for extent in tree.findall('.//wp:extent',wns):ck(p.name+' embedded equal aspect',int(extent.get('cx'))/int(extent.get('cy')),1600/1120,1e-6)
   ck(p.name+' no Word crop',len(tree.findall('.//a:srcRect',wns)),0)
   media.append(dict(word=p.name,media=n,sha256=hashlib.sha256(b).hexdigest(),original_png=original))
r=dict(checks=checks,passed=sum(q['pass_'] for q in checks),total=len(checks),assets={str(p.relative_to(R)):sha(p) for p in [svg,png]},png_size=Image.open(png).size,tick_angles=ticks,labels=labels,media=media)
(O/'math_media_results.json').write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['total']);print([q for q in checks if not q['pass_']])
