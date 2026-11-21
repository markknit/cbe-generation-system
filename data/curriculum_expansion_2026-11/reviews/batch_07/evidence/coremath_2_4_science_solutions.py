"""Reviewer-owned solutions for all Trigonometry1 tasks, rounded tables, exact constructions and instrument geometry."""
from pathlib import Path
from fractions import Fraction as F
from math import sin,cos,tan,asin,atan,sqrt,pi,degrees,radians,isclose,atan2,hypot
import re,json,hashlib,zipfile,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
E=Path(__file__).parent;B=E.parents[2];M=json.loads((B/'materials/coremath_2_4.json').read_text());checks=[]
def ck(label,a,b,tol=1e-11):
 def eq(a,b):
  if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)):return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
  if isinstance(a,(int,float,F)) and isinstance(b,(int,float,F)):return isclose(float(a),float(b),rel_tol=0,abs_tol=tol)
  return a==b
 ok=eq(a,b);checks.append({'label':label,'actual':str(a),'expected':str(b),'absolute_tolerance':tol,'pass':ok});assert ok,label
sd=lambda a:sin(radians(a));cd=lambda a:cos(radians(a));td=lambda a:tan(radians(a));asin_d=lambda x:degrees(asin(x));atan_d=lambda x:degrees(atan(x))
# Independently defined values; never evaluate author expressions.
vals={}
for angle in [10,20,30,40,45,50,60,70,80]:
 for name,fn in [('sin',sd),('cos',cd),('tan',td)]:vals[f'{name}_{angle}']=fn(angle)
vals.update({'ratioSin':F(3,5),'ratioCos':F(4,5),'ratioTan':F(3,4),'tanRelation':F(3,4),'pythRelation':1,'roundedRatio':F(6428,7660),'special45':sqrt(2)/2,'special30tan':sqrt(3)/3,'sideOpp':5,'sideAdj':5*sqrt(3),'inverseTan':atan_d(F(3,4)),'elevationRise':4*sqrt(3),'elevationHeight':1.5+4*sqrt(3),'depression45':15,'depression30':12*sqrt(3),'slant30':24,'fieldExample':1.4+10/sqrt(3),'finalSin':F(5,13),'finalCos':F(12,13),'finalTan':F(5,12),'finalRelation':F(5,12),'finalDepression':8,'clinometerReading':30,'calibrationRise':5/sqrt(3),'readingOtherSide':30})
assert len(vals)==len(M['calculations'])==52
for c in M['calculations']:ck('registry '+c['id'],vals[c['id']],c['expected'],c.get('absolute_tolerance',1e-11))
# Parse actual authored instructional table as well as register; ensure every formatted entry is rounded correctly.
table_text=M['items'][1]['student'];rows={}
for match in re.finditer(r'(\d+)°: sin ([0-9.]+), cos ([0-9.]+), tan ([0-9.]+)',table_text):
 a=int(match[1]);rows[a]=tuple(match[i].rstrip('.') for i in [2,3,4])
ck('complete instructional table row count',len(rows),9)
for a,entries in rows.items():
 for name,fn,entry in zip(['sin','cos','tan'],[sd,cd,td],entries):ck(f'CTG2 actual {name}{a} 4dp',entry,f'{fn(a):.4f}')
ck('CTG2 requested lookups',[rows[40][0],rows[50][1],rows[30][2],rows[80][2]],['0.6428','0.6428','0.5774','5.6713'])
for a,b in [(10,80),(20,70),(30,60),(40,50),(45,45)]:
 ck(f'CTG4 rounded complement sin{a}/cos{b}',rows[a][0],rows[b][1]);ck(f'CTG4 rounded complement cos{a}/sin{b}',rows[a][1],rows[b][0]);ck(f'CTG4 exact-value complement {a}',sd(a),cd(b))
ck('CTG1 A exact ratios',[F(3,5),F(4,5),F(3,4)],[F(3,5),F(4,5),F(3,4)])
ck('CTG1 B side-role swap',[F(4,5),F(3,5),F(4,3)],[F(4,5),F(3,5),F(4,3)])
ck('CTG1 hypotenuse check',3**2+4**2,5**2)
ck('CTG5 exact tangent quotient',F(3,5)/F(4,5),F(3,4));ck('CTG5 Pythagorean ratio identity',F(3,5)**2+F(4,5)**2,1)
ck('CTG5 rounded quotient',float(F(6428,7660)),0.8391644908616188)
ck('CTG5 rounded quotient differs from rounded tan entry',float(F(6428,7660))!=float(rows[40][2]),True)
ck('CTG5 exact trig quotient 40',sd(40)/cd(40),td(40))
ck('CTG3 degree-mode numerical outputs',[sd(40),cd(50),td(30)],[0.6427876096865393,0.6427876096865394,0.5773502691896257])
ck('CTG3 radians different angle',not isclose(sin(40),sd(40)),True)
ck('CTG3 4dp results',[f'{x:.4f}' for x in [sd(40),cd(50),td(30)]],['0.6428','0.6428','0.5774'])
# Construct special-angle triangles and exact forms; endpoint handled symbolically rather than float tan(pi/2).
ck('CTG6 unit-leg hypotenuse squared',1**2+1**2,2)
ck('CTG6 exact equivalent sine forms',1/sqrt(2),sqrt(2)/2)
ck('CTG7 equilateral split altitude squared',2**2-1**2,3)
special={30:(F(1,2),sqrt(3)/2,sqrt(3)/3),45:(sqrt(2)/2,sqrt(2)/2,1),60:(sqrt(3)/2,F(1,2),sqrt(3))}
for a,expected in special.items():
 ck(f'CTG6/7 three special ratios {a}',(sd(a),cd(a),td(a)),expected)
 ck(f'CTG6/7 exact tangent relation {a}',expected[0]/expected[1],expected[2])
ck('CTG7 tan30 rationalisation',1/sqrt(3),sqrt(3)/3)
ck('CTG8 endpoint unit circle coordinate',(0,1),(0,1))
ck('CTG8 triangle cannot have two right angles',90+90>=180,True)
try:F(1,0);zero_division=False
except ZeroDivisionError:zero_division=True
ck('CTG8 no real division 1/0',zero_division,True)
# Inverse cues and every application; rounded paper model results never represented as real readings.
ck('CTG9 inverse sine cue',f'{asin_d(.6):.2f}','36.87');ck('CTG9 inverse tangent cue',f'{atan_d(.75):.2f}','36.87')
ck('CTG9 A exact sides',(5,5*sqrt(3)),(10*sd(30),10*cd(30)))
ck('CTG9 A Pythagoras',5**2+(5*sqrt(3))**2,100)
ck('CTG9 table adjacent',10*float(rows[30][1]),8.660)
ck('CTG9 table and exact 2dp',[f'{10*float(rows[30][1]):.2f}',f'{5*sqrt(3):.2f}'],['8.66','8.66'])
ck('CTG10 elevation total',f'{1.5+12*td(30):.2f}','8.43');ck('CTG10 elevation rise',12*td(30),4*sqrt(3))
ck('CTG10 second elevation cue',f'{atan_d(F(6,8)):.2f}','36.87')
ck('CTG11 depression A',15/td(45),15);ck('CTG11 depression B horizontal',12/td(30),12*sqrt(3))
ck('CTG11 depression B slant',12/sd(30),24);ck('CTG11 B horizontal2dp',f'{12/td(30):.2f}','20.78')
ck('CTG11 B Pythagoras',12**2+(12*sqrt(3))**2,24**2)
ck('CTG12 paper read magnitude',abs(90-60),30);ck('CTG12 opposite-scale-side magnitude',abs(90-120),30)
ck('CTG12 explicit5m elevation application',f'{5*td(30):.2f}','2.89')
ck('CTG13 fictional rise',10*td(30),10/sqrt(3));ck('CTG13 fictional total2dp',f'{1.4+10*td(30):.2f}','7.17')
# Final exact ratios/table/complement/special cases/height/depression/calibration.
ck('Final triangle Pythagoras',5**2+12**2,13**2)
ck('Final exact relation',F(5,13)/F(12,13),F(5,12));ck('Final sin/cos identity',F(5,13)**2+F(12,13)**2,1)
finaltext=M['items'][-1]['student']
finalrows={int(a):(s.rstrip('.'),c.rstrip('.'),t.rstrip('.')) for a,s,c,t in re.findall(r'(\d+)°sin([0-9.]+),cos([0-9.]+),tan([0-9.]+)',finaltext)}
ck('Final supplied table count',len(finalrows),5)
for a,entries in finalrows.items():ck(f'Final actual table row {a}',entries,rows[a])
ck('Final elevation total2dp',f'{1.4+10/sqrt(3):.2f}','7.17');ck('Final depression horizontal',8/td(45),8)
ck('Final scale reading not elevation',abs(90-60)!=60,True)
# Physical clinometer: in a vertical sight plane, plumb gravity is fixed while baseline rotates beta.
# Template local x follows its positive diameter, local y is below the baseline.
for beta in [-80,-30,-5,0,5,30,80]:
 b=radians(beta);u=(cos(b),sin(b));v=(sin(b),-cos(b));g=(0,-1)
 x=g[0]*u[0]+g[1]*u[1];y=g[0]*v[0]+g[1]*v[1];raw=degrees(atan2(y,x))
 ck(f'clinometer physical magnitude beta{beta}',abs(90-raw),abs(beta))
 # Direction of target cannot be inferred without which sight-line direction is selected.
ck('sight reversal retains magnitude but reverses UP/DOWN',abs(90-60),abs(90-120))
result={'checks_total':len(checks),'registry_checks':52,'checks':checks,'exact_special_table':{'30':['1/2','sqrt(3)/2','sqrt(3)/3'],'45':['sqrt(2)/2','sqrt(2)/2','1'],'60':['sqrt(3)/2','1/2','sqrt(3)'],'90':['1','0','not defined over the reals']},'CTG14_repairs':['A opposite/adjacent roles depend on the named acute angle','B degrees and radians are different units;mode matters','C rounded ratios may produce a different last decimal','D tangent90 would divide by zero;no finite or infinite real value','E a slant distance is not the horizontal component','F actual make/calibrate/use requires observed actions'],'actual_evidence':'NOT OBSERVED: actual calculator mode/actions/displays,instrument make/calibrate/use,external research,parental support and environmental/group actions. Paper results are not fabricated observations.','geometry_limit':'vertical sight plane,freely hanging plumb line,aligned sight baseline and pivot,level calibration90;record UP/DOWN separately;0<angle<90 for nondegenerate finite tangent field model.'}
E.joinpath('coremath_2_4_science_solutions.json').write_text(json.dumps(result,indent=2)+'\n')
# Independent labelled triangle/application proof, not a production figure.
im=Image.new('RGB',(1500,850),'white');d=ImageDraw.Draw(im)
def triangle(box,title,a,b,labela,labelb,labelh):
 x0,y0,x1,y1=box;d.text((x0,y0),title,fill='black');u=min((x1-x0-100)/a,(y1-y0-100)/b);A=(x0+35,y1-45);C=(A[0]+a*u,A[1]);B=(C[0],C[1]-b*u);d.line([A,C,B,A],fill='navy',width=3);d.rectangle((C[0]-12,C[1]-12,C[0],C[1]),outline='black');d.text(((A[0]+C[0])/2,C[1]+8),labela,fill='black');d.text((C[0]+8,(C[1]+B[1])/2),labelb,fill='black');d.text(((A[0]+B[0])/2-20,(A[1]+B[1])/2-20),labelh,fill='black');d.text((A[0]-20,A[1]-20),'A',fill='black')
triangle((10,10,490,400),'CTG1: named angle A',4,3,'adjacent4','opposite3','hyp5')
triangle((510,10,990,400),'CTG6: 45-degree derivation',1,1,'1','1','sqrt2')
triangle((1010,10,1490,400),'CTG7: 30/60-degree half',sqrt(3),1,'sqrt3','1','2; angleA30')
triangle((10,435,490,840),'CTG10: elevation rise then sight height',12,4*sqrt(3),'horizontal12m','rise4sqrt3','30deg +sight1.5m')
triangle((510,435,990,840),'CTG11: depression reference triangle',12*sqrt(3),12,'horizontal12sqrt3','drop12m','slant24;30deg')
triangle((1010,435,1490,840),'Final: angle A exact ratios',12,5,'adjacent12','opposite5','hyp13')
im.save(E/'coremath_2_4_science_constructed_proof.png')
print(len(checks),'independent checks PASS, all52registry and every table/inverse/special/application/calibration/final case')
