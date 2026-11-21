"""Read-only Core3.1 draft propagation, isolation, grid and independent data checks."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET,re
from fractions import Fraction as F
from collections import Counter
from itertools import accumulate
from PIL import Image
ROOT=Path(__file__).resolve().parents[5]; B=ROOT/'data/curriculum_expansion_2026-11';E=Path(__file__).resolve().parent
M=json.loads((B/'materials/coremath_3_1.json').read_text());N=json.loads((B/'manuscripts/coremath_3_1.json').read_text());S=json.loads((B/'sources/coremath_3_1.json').read_text())
W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'};D=B/'outputs/v2/Core_Mathematics/SS3.1_Statistics_I';T={};X={};Z={}
for p in D.glob('*.docx'):
 k=p.stem.removeprefix(N['prefix']+'_')
 with zipfile.ZipFile(p) as z:
  x=ET.fromstring(z.read('word/document.xml'));X[k]=x;T[k]='\n'.join(''.join(t.text or '' for t in q.findall('.//w:t',W)) for q in x.findall('.//w:p',W));Z[k]={i:hashlib.sha256(z.read(i)).hexdigest() for i in z.namelist() if i.startswith('word/media/')}
norm=lambda s:re.sub(r'\s+','',s);checks=[]
def ck(k,v):checks.append({'check':k,'pass':bool(v)})
for c in M['items']:
 for key in ['student','teacher']:ck(c['id']+' key '+key,norm(c[key]) in norm(T['MaterialsTeacherKey']))
 ck(c['id']+' student propagation',norm(c['student']) in norm(T['AssessmentMaterials' if c['id']=='SI16' else 'StudentMaterials']))
for l in N['lessons']:
 for key in ['title','purpose','knowledge','safety','reflection']:ck(f"L{l['number']} guide {key}",norm(l[key]) in norm(T['CompactTeacherGuide']))
 for i,ph in enumerate(l['phases']):
  for j,s in enumerate(ph):ck(f"L{l['number']}phase{i+1}cell{j+1}",norm(s) in norm(T['CompactTeacherGuide']))
 ck(f"L{l['number']}40min",sum(l['minutes'])==40)
ck('16officiallessons',S['official_lesson_allocation']==len(N['lessons'])==16)
ck('finalSI16absentteaching','SI16' not in T['StudentMaterials'])
ck('finalSI16presentassessment','SI16' in T['AssessmentMaterials'])
ck('assessmentonlySI16',not any(re.search(r'\bSI'+str(i)+r'\b',T['AssessmentMaterials']) for i in range(1,16)))
ck('noteachersolutionassessment',all(norm(c['teacher']) not in norm(T['AssessmentMaterials']) for c in M['items']))
ck('finaldatasetabsentguide',norm(M['items'][-1]['student']) not in norm(T['CompactTeacherGuide']))
rows=X['StudentSummaryTable'].findall('.//w:tr',W);ck('summary16rows',len(rows)==17)
for i,r in enumerate(rows[1:],1):
 cs=r.findall('w:tc',W);ck(f'summary{i}threeblank',len(cs)==4 and all(not ''.join(t.text or '' for t in c.findall('.//w:t',W)).strip() for c in cs[1:]))
for k,ids in [('StudentMaterials',['SI10','SI11','SI12']),('MaterialsTeacherKey',['SI10','SI11','SI12','SI16']),('AssessmentMaterials',['SI16'])]:
 ck(k+'imagecount',len(Z[k])==len(ids))
 for card,ex in zip(ids,X[k].findall('.//wp:extent',W)):
  p=B/'materials/diagrams'/f'{card}.png';w,h=Image.open(p).size
  ck(k+'embed'+card,hashlib.sha256(p.read_bytes()).hexdigest() in Z[k].values());ck(k+'aspect'+card,int(ex.get('cx'))*h==int(ex.get('cy'))*w)
ck('finalgridabsentteaching',hashlib.sha256((B/'materials/diagrams/SI16.png').read_bytes()).hexdigest() not in Z['StudentMaterials'].values())

# Independently derive numeric results from raw lists and declared class tables,
# without evaluating the author's registered expressions.
def raw(a):
 a=sorted(a);c=Counter(a);n=len(a);top=max(c.values());return {'sorted':a,'frequency':dict(sorted(c.items())),'N':n,'sum':sum(a),'mean':str(F(sum(a),n)),'median':str(F(a[n//2]) if n%2 else F(a[n//2-1]+a[n//2],2)),'modes':[x for x,f in sorted(c.items()) if f==top]}
def grouped(bounds,f):
 widths=[F(v-u) for u,v in zip(bounds,bounds[1:])];mid=[F(u+v,2) for u,v in zip(bounds,bounds[1:])];fx=[x*n for x,n in zip(mid,f)];return {'widths':list(map(str,widths)),'midpoints':list(map(str,mid)),'frequencies':f,'cum':list(accumulate(f)),'fx':list(map(str,fx)),'sumfx':str(sum(fx)),'N':sum(f),'meanestimate':str(sum(fx)/sum(f)),'densities':[str(F(n)/h) for n,h in zip(f,widths)]}
p=raw([2,4,3,2,5,4,4,6,2,3]);changed=raw([2,4,3,2,5,4,4,26,2,3]);rr=raw([10,12,14,16,18,20,22,24,26,28,30,34]);fa=raw([2,3,3,5,7,10]);g=grouped([10,20,30,40],[5,5,2]);g8=grouped([0,10,20,30],[4,8,4]);unequal=grouped([0,10,20,40],[4,6,10]);fb=grouped([10,20,30,40],[3,5,4]);fc=grouped([0,5,15,20],[5,10,10])
# Label every interpolation parameter from class evidence.
g8median=F(10)+(F(g8['N'],2)-g8['cum'][0])/g8['frequencies'][1]*10;g8mode=F(10)+F(8-4,2*8-4-4)*10
fbmedian=F(20)+(F(fb['N'],2)-fb['cum'][0])/fb['frequencies'][1]*10;fbmode=F(20)+F(5-3,2*5-3-4)*10
computed=[p['sum'],float(F(p['mean'])),float(F(changed['mean'])),float(F(p['median'])),rr['sum'],float(F(rr['mean'])),float(F(g['meanestimate'])),float(g8median),float(g8mode),*[float(F(z)) for z in unequal['densities']],float(F(fa['mean'])),float(F(fa['median'])),float(F(fb['meanestimate'])),float(fbmedian),float(fbmode),*[float(F(z)) for z in fb['densities']],*[float(F(z)) for z in fc['densities']]]
ck('registered23count',len(computed)==len(M['calculations'])==23)
for c,v in zip(M['calculations'],computed):ck('registered independent '+c['id'],abs(c['expected']-v)<1e-10)
ck('SI3table',list(p['frequency'].values())==[3,2,3,1,1] and p['modes']==[2,4])
ck('SI4grouping', [sum(a<=x<c for x in rr['sorted']) for a,c in [(10,20),(20,30),(30,40)]]==g['frequencies'])
ck('SI6oddmedian',raw([2,3,5,8,9])['median']=='5')
ck('SI6alluniqueequalfrequency',len(set(Counter([1,2,3,4]).values()))==1)
ck('finalAmode',fa['modes']==[3])
ck('SI11peakdistinction',unequal['frequencies'].index(max(unequal['frequencies']))==2 and [F(x) for x in unequal['densities']].index(max(F(x) for x in unequal['densities']))==1)
ck('finalCfrequencytie',fc['frequencies']==[5,10,10] and fc['densities']==['1','1','2'])

# Blank-panel usability:22x11 equal50px cells; an example valid choice of
# scale is2.5cm/cell horizontally,0.1density/cell or1frequency/cell vertically.
grid={}
for card in ['SI10','SI11','SI12','SI16']:
 im=Image.open(B/'materials/diagrams'/f'{card}.png').convert('RGB');pix=im.load();panels=2 if card=='SI16' else 1
 ck(card+'dimensions',im.size==(1280,720*panels));grid[card]={'pixels':im.size,'panels':panels,'cell_pixels':[50,50],'panel_plot_bounds':[]}
 for panel in range(panels):
  off=720*panel;grid[card]['panel_plot_bounds'].append([100,80+off,1200,630+off])
  ck(f'{card}axes{panel+1}',all(pix[x,y]==(0,0,0) for x,y in [(100,100+off),(100,500+off),(300,630+off),(1000,630+off)]))
  ck(f'{card}grid50{panel+1}',len({pix[x,200+off] for x in [150,200,250,300]})==1 and pix[175,200+off] != pix[150,200+off])
# Every teaching/final rectangle edge, polygon point and optional5/45zero endpoint fits.
construct={}
for name,bounds,f in [('SI10',[10,20,30,40],[5,5,2]),('SI11',[0,10,20,40],[4,6,10]),('SI16hist',[10,20,30,40],[3,5,4])]:
 data=grouped(bounds,f);rects=[[100+20*u,630-500*float(F(h)),100+20*v,630] for u,v,h in zip(bounds,bounds[1:],data['densities'])];construct[name]=rects;ck(name+'fitsblank',all(100<=x1<x2<=1200 and 80<=yt<=630 for x1,yt,x2,yb in rects))
for name,points in [('SI12',[(5,0),(15,5),(25,5),(35,2),(45,0)]),('SI16polygon',[(5,0),(15,3),(25,5),(35,4),(45,0)])]:
 coords=[[100+20*x,630-50*y] for x,y in points];construct[name]=coords;ck(name+'fitsblank',all(100<=x<=1200 and 80<=y<=630 for x,y in coords))
res={'passed':sum(x['pass'] for x in checks),'total':len(checks),'failed':[x for x in checks if not x['pass']],'checks':checks,'independent_data':{'practice':p,'changed':changed,'raw_lengths':rr,'practice_grouped':g,'SI8':g8,'unequal':unequal,'finalA':fa,'finalB':fb,'finalC':fc,'SI8_median_estimate':str(g8median),'SI8_mode_estimate':str(g8mode),'finalB_median_estimate':str(fbmedian),'finalB_mode_estimate':str(fbmode)},'blank_grid_geometry':grid,'independent_example_construction_pixels':construct,'construction_note':'One valid chosen scale,not a required pupil scale;SI16polygon y positions relative to its own panel. Optional zero closures are conventions,not observed data. No figures/content rendered or modified.'}
(E/'coremath_3_1_initial_checks.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['passed','total','failed']},indent=2))
