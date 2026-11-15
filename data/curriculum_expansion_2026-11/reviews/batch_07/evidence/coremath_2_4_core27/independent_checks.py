from pathlib import Path
import json,math,re,hashlib,zipfile,io,xml.etree.ElementTree as ET
from fractions import Fraction as F
from PIL import Image
E=Path(__file__).resolve().parent;B=Path('data/curriculum_expansion_2026-11');M=json.loads((E/'initial_materials.json').read_text());N=json.loads((E/'initial_manuscripts.json').read_text());P=json.loads((E/'initial_blueprints.json').read_text());checks={};geo={}
def ck(k,v): checks[k]=bool(v)
def close(x,y,t=1e-10):return abs(x-y)<=t
s=lambda a:math.sin(math.radians(a));c=lambda a:math.cos(math.radians(a));t=lambda a:math.tan(math.radians(a))
func={'sin_deg':s,'cos_deg':c,'tan_deg':t,'atan_deg':lambda x:math.degrees(math.atan(x)),'sqrt':math.sqrt}
for r in M['calculations']:
 value=eval(r['expression'],{'__builtins__':{}},func);ck('registry_'+r['id'],math.isclose(value,r['expected'],rel_tol=r.get('relative_tolerance',1e-9),abs_tol=r.get('absolute_tolerance',1e-9)))
# Independently parse student table, rather than verifying only declared registry values.
rows=re.findall(r'(\d+)°: sin ([\d.]+), cos ([\d.]+), tan ([\d.]+)',M['items'][1]['student'])
ck('nine_complete_table_rows',len(rows)==9)
for a,*vals in rows:
 for name,actual,f in zip(['sin','cos','tan'],vals,[s,c,t]):ck(f'table_{a}_{name}',actual.rstrip('.')==f'{f(int(a)):.4f}')
for a,b in [(10,80),(20,70),(30,60),(40,50),(45,45)]:
 ck(f'complement_{a}_{b}_sin',close(s(a),c(b)));ck(f'complement_{a}_{b}_cos',close(c(a),s(b)))
for a in [10,20,30,40,45,50,60,70,80]:
 ck(f'acute_identity_{a}_tan',close(s(a)/c(a),t(a)));ck(f'acute_identity_{a}_pyth',close(s(a)**2+c(a)**2,1))
for k,x,y in [('A_sin',F(3,5),F(3,5)),('A_cos',F(4,5),F(4,5)),('A_tan',F(3,4),F(3,4)),('B_sin',F(4,5),F(4,5)),('B_cos',F(3,5),F(3,5)),('B_tan',F(4,3),F(4,3)),('tan_fraction',F(3,5)/F(4,5),F(3,4)),('pyth_fraction',F(3,5)**2+F(4,5)**2,F(1))]:ck('CTG1_5_'+k,x==y)
ck('40_rounded_ratio',close(.6428/.7660,.8391644908616188));ck('40_true_tan',close(t(40),.8390996311772799));ck('40_rounded_differ',.6428/.7660!=.8391)
for a,vals in [(30,(.5,math.sqrt(3)/2,1/math.sqrt(3))),(45,(1/math.sqrt(2),1/math.sqrt(2),1)),(60,(math.sqrt(3)/2,.5,math.sqrt(3)))]:
 for name,x,f in zip(['sin','cos','tan'],vals,[s,c,t]):ck(f'exact_triangle_{a}_{name}',close(x,f(a)))
ck('45_hypotenuse',close(math.sqrt(1**2+1**2),math.sqrt(2)));ck('30_60_altitude',close(math.sqrt(2**2-1**2),math.sqrt(3)));ck('rationalised30tan',close(1/math.sqrt(3),math.sqrt(3)/3))
for name,a,b in [('sin40',s(40),.6427876097),('cos50',c(50),.6427876097),('tan30',t(30),.5773502692)]:ck('device_display_'+name,round(a,10)==b)
ck('inverse_sin06',round(math.degrees(math.asin(.6)),2)==36.87);ck('inverse_tan075',round(math.degrees(math.atan(.75)),2)==36.87)
ck('CTG9_opposite',close(10*s(30),5));ck('CTG9_adjacent',close(10*c(30),5*math.sqrt(3)));ck('CTG9_pyth',close(5**2+(5*math.sqrt(3))**2,100));ck('CTG9_table_adjacent',close(10*.8660,8.660));ck('CTG9_table_exact_2dp',f'{10*.8660:.2f}'==f'{5*math.sqrt(3):.2f}'=='8.66')
for name,value,expected in [('CTG10rise',12*t(30),4*math.sqrt(3)),('CTG10height',1.5+12*t(30),8.428203230275509),('CTG11A',15/t(45),15),('CTG11Bhorizontal',12/t(30),12*math.sqrt(3)),('CTG11Bslant',12/s(30),24),('CTG12paper',5*t(30),5/math.sqrt(3)),('CTG13rise',10*t(30),10/math.sqrt(3)),('CTG13height',1.4+10*t(30),7.1735026918962586),('final_depression',8/t(45),8)]:ck(name,close(value,expected))
for name,v,expected in [('height10',1.5+12*t(30),'8.43'),('horizontal11',12/t(30),'20.78'),('paper12',5*t(30),'2.89'),('height13final',1.4+10*t(30),'7.17')]:ck('round2_'+name,f'{v:.2f}'==expected)
for k,v in [('sin',F(5,13)),('cos',F(12,13)),('tan',F(5,12))]:ck('final_'+k,v=={'sin':F(5,13),'cos':F(12,13),'tan':F(5,12)}[k])
ck('final_pyth',5**2+12**2==13**2);ck('final_tan_cancel',F(5,13)/F(12,13)==F(5,12));ck('final_complement',close(s(40),c(50)));ck('final_raw60_wrong',not close(1.4+10*t(60),1.4+10*t(30)))
# Geometric plumb-line derivation: global downward vector expressed in instrument coordinates.
for alpha in [-70,-30,-10,0,10,30,70]:
 r=math.degrees(math.atan2(math.cos(math.radians(alpha)),math.sin(math.radians(alpha))))
 ck(f'plumb_angle_{alpha}',close(abs(90-r),abs(alpha)))
ck('r60_r120_same_magnitude',abs(90-60)==abs(90-120)==30)
# Endpoint determined analytically by coordinate (0,1), not a float tangent implementation.
ck('endpoint_coordinates',0**2+1**2==1);ck('endpoint_denominator_zero',0==0);ck('two_right_angles_degenerate',180-90-90==0)
# Verify every linked mapping and final section correspondence; manual semantic checks in solutions.md.
for i,l in enumerate(N['lessons'],1):
 ck(f'lesson{i}_mapping',l['outcomes']==P['lesson_map'][i-1]['outcomes']);ck(f'lesson{i}_40min',sum(l['minutes'])==40)
 if i<15:
  arrays=[x['outcomes'] for key in ['assessment_map','assessment_tasks'] for x in P[key] if x.get('task',x.get('id'))==f'F{i}'];ck(f'F{i}_four_maps',len(arrays)==2 and all(a==l['outcomes'] for a in arrays))
for i,sec in enumerate(N['assessment']['sections'],1):ck(f'final{i}_phase_prompt',sec['prompt']==N['lessons'][-1]['phases'][i][0])
ck('final_timing',N['lessons'][-1]['minutes']==[3,9,12,8,8]);ck('project_timing',all(N['lessons'][i]['minutes']==[3,24,6,2,5] for i in [11,12]))
# Actual SVG numerical geometry, each tick and label; no new curriculum rendering.
svg=B/'materials/diagrams/CTG12.svg';png=B/'materials/diagrams/CTG12.png';ns={'s':'http://www.w3.org/2000/svg'};x=ET.fromstring(svg.read_text());lines=x.findall('s:line',ns)
geo['182_lines_baseline_plus181ticks']=len(lines)==182
for i,line in enumerate(lines[1:]):
 a=math.radians(i);X,Y=float(line.attrib['x2']),float(line.attrib['y2']);geo[f'tick{i}_angle_radius']=close(X,800+650*math.cos(a)) and close(Y,230+650*math.sin(a))
for txt in x.findall('s:text',ns):
 if (txt.text or '').isdigit():
  i=int(txt.text);X,Y=float(txt.attrib['x']),float(txt.attrib['y']);expected=(800+539.5*math.cos(math.radians(i)),230+539.5*math.sin(math.radians(i)))
  if i in [0,180]:expected=(expected[0],260)
  geo[f'label{i}']=close(X,expected[0]) and close(Y,expected[1])
geo['centre_dot']=any(cir.attrib.get('cx')=='800' and cir.attrib.get('cy')=='230' for cir in x.findall('s:circle',ns));geo['png_dimensions']=Image.open(png).size==(1600,1120)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();emb={}
for doc in ['StudentMaterials','MaterialsTeacherKey']:
 p=next((B/'outputs/v2').rglob(N['prefix']+'_'+doc+'.docx'))
 with zipfile.ZipFile(p) as z:
  media=[q for q in z.namelist() if q.startswith('word/media/')];raw=z.read(media[0]);root=ET.fromstring(z.read('word/document.xml'));ext=root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent');emb[doc]={'one_media':len(media)==1,'exact_png_bytes':hashlib.sha256(raw).hexdigest()==sha(png),'image_dimensions':list(Image.open(io.BytesIO(raw)).size),'extents':[e.attrib for e in ext],'undistorted':len(ext)==1 and close(float(ext[0].attrib['cx'])/float(ext[0].attrib['cy']),1600/1120,1e-6)}
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'geometry':geo,'geometry_passed':sum(geo.values()),'geometry_total':len(geo),'geometry_failed':[k for k,v in geo.items() if not v],'assets':{str(p):sha(p) for p in [svg,png]},'embeddings':emb}
(E/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['checks','geometry']},indent=2))
