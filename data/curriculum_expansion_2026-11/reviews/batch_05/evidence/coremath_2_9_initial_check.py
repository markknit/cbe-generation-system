"""Read-only independent draft propagation/isolation and motion-model review checks."""
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as ET,re
from fractions import Fraction as F
from PIL import Image
ROOT=Path(__file__).resolve().parents[5]
B=ROOT/'data/curriculum_expansion_2026-11'; E=Path(__file__).resolve().parent
M=json.loads((B/'materials/coremath_2_9.json').read_text()); N=json.loads((B/'manuscripts/coremath_2_9.json').read_text())
W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
D=B/'outputs/v2/Core_Mathematics/SS2.9_Linear_Motion'; T={};X={};Z={}
for p in D.glob('*.docx'):
 k=p.stem.removeprefix(N['prefix']+'_')
 with zipfile.ZipFile(p) as z:
  x=ET.fromstring(z.read('word/document.xml'));X[k]=x
  T[k]='\n'.join(''.join(t.text or '' for t in q.findall('.//w:t',W)) for q in x.findall('.//w:p',W))
  Z[k]={i:hashlib.sha256(z.read(i)).hexdigest() for i in z.namelist() if i.startswith('word/media/')}
norm=lambda s:re.sub(r'\s+','',s)
checks=[]
def check(label,value):checks.append({'check':label,'pass':bool(value)})
for c in M['items']:
 for key in ['student','teacher']:check(c['id']+' key '+key,norm(c[key]) in norm(T['MaterialsTeacherKey']))
 if c['id']!='LM12':check(c['id']+' teaching student',norm(c['student']) in norm(T['StudentMaterials']))
 else:check('LM12 assessment student',norm(c['student']) in norm(T['AssessmentMaterials']))
for l in N['lessons']:
 for key in ['title','purpose','knowledge','safety']:check(f"L{l['number']} guide {key}",norm(l[key]) in norm(T['CompactTeacherGuide']))
 for i,ph in enumerate(l['phases']):
  for j,s in enumerate(ph):check(f"L{l['number']} phase{i+1} cell{j+1}",norm(s) in norm(T['CompactTeacherGuide']))
 check(f"L{l['number']}40minutes",sum(l['minutes'])==40)
check('final card absent teaching','LM12' not in T['StudentMaterials'])
check('final card present assessment','LM12' in T['AssessmentMaterials'])
check('assessment only LM12',not any(re.search(r'\bLM'+str(i)+r'\b',T['AssessmentMaterials']) for i in range(1,12)))
check('no teacher solution in assessment',not any(norm(c['teacher']) in norm(T['AssessmentMaterials']) for c in M['items']))
check('no final solution in teaching',norm(M['items'][-1]['teacher']) not in norm(T['StudentMaterials']))
check('no final dataset in guide',norm(M['items'][-1]['student']) not in norm(T['CompactTeacherGuide']))
rows=X['StudentSummaryTable'].findall('.//w:tr',W)
check('summary12rows',len(rows)==13)
for i,r in enumerate(rows[1:],1):
 cells=r.findall('w:tc',W);check(f'summary{i}threeblankcells',len(cells)==4 and all(not ''.join(t.text or '' for t in c.findall('.//w:t',W)).strip() for c in cells[1:]))
for k in ['StudentMaterials','MaterialsTeacherKey']:
 for card in ['LM5','LM8']:
  p=B/'materials/diagrams'/f'{card}.png';sha=hashlib.sha256(p.read_bytes()).hexdigest()
  check(k+' embed '+card,sha in Z[k].values())
 for i,extent in enumerate(X[k].findall('.//wp:extent',W)):
  check(f'{k} aspect{i+1}',int(extent.get('cx'))*960==int(extent.get('cy'))*1400)

# Independently integrate each specified piecewise-linear velocity model;
# split at zero for distance rather than taking abs of the net trapezium.
def vm(points):
 points=[(F(t),F(v)) for t,v in points];areas=[];distance=F(0);zeros=[];slopes=[]
 for (t,v),(u,w) in zip(points,points[1:]):
  dt=u-t;slopes.append((w-v)/dt);areas.append((v+w)*dt/2)
  if v*w<0:
   z=t-v*dt/(w-v);zeros.append(z);distance+=(abs(v)*(z-t)+abs(w)*(u-z))/2
  else:distance+=(abs(v)+abs(w))*dt/2
 return {'accelerations':list(map(str,slopes)),'signed_areas':list(map(str,areas)),'displacement':str(sum(areas)),'distance':str(distance),'interior_zero_crossings':list(map(str,zeros))}
models={'LM7':vm([(0,0),(2,4),(4,4),(6,0)]),'LM8':vm([(0,3),(2,3),(4,-1),(6,-1)]),'finalV':vm([(0,-2),(2,2),(4,2),(6,0)])}
check('LM7 independent area',models['LM7']['displacement']=='16' and models['LM7']['distance']=='16')
check('LM8 independent split area',models['LM8']['displacement']=='6' and models['LM8']['distance']=='21/2' and models['LM8']['interior_zero_crossings']==['7/2'])
check('finalV independent split area',models['finalV']['displacement']=='6' and models['finalV']['distance']=='8' and models['finalV']['interior_zero_crossings']==['1'])
# Actual raster positions: orange curve/marker nearest the independently mapped nodes.
geometry={}
for card,points,xmax,ymin,ymax in [('LM5',[(0,2),(2,6),(4,6),(6,2),(8,-2)],8,-4,8),('LM8',[(0,3),(2,3),(4,-1),(6,-1)],6,-2,4)]:
 im=Image.open(B/'materials/diagrams'/f'{card}.png').convert('RGB');pix=im.load();nodes=[]
 for t,v in points:
  x=120+1140*t/xmax;y=130+650*(ymax-v)/(ymax-ymin)
  hits=[]
  for a in range(round(x)-3,round(x)+4):
   for b in range(round(y)-3,round(y)+4):
    r,g,bl=pix[a,b]
    if r>120 and 30<g<150 and bl<65 and r>g*1.3:hits.append([a,b])
  check(f'{card} orange node{t},{v}',bool(hits));nodes.append({'data':[t,v],'expected_pixel':[x,y],'orange_hit':bool(hits)})
 geometry[card]={'image_size':im.size,'axes_plot_bounds':[120,130,1260,780],'time_range':[0,xmax],'ordinate_range':[ymin,ymax],'nodes':nodes,'note':'Ranges/tick labels read visually; node pixels checked against independent axis mapping. Different physical dimensions on axes do not require square numerical units.'}
result={'checks':checks,'passed':sum(c['pass'] for c in checks),'total':len(checks),'failed':[c for c in checks if not c['pass']],'independent_velocity_models':models,'graph_geometry':geometry}
(E/'coremath_2_9_initial_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['passed','total','failed','independent_velocity_models']},indent=2))
