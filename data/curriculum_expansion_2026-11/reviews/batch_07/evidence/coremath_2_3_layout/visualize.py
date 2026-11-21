from pathlib import Path
import json,subprocess,hashlib,tempfile
from PIL import Image,ImageDraw
from concurrent.futures import ThreadPoolExecutor
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[5];BASE=ROOT/'data/curriculum_expansion_2026-11';PRE='Codex_Core_Mathematics_Rotation'
TYPES=json.loads((OUT/'check.json').read_text())['pdf_pages']
def render(typ):
 folder=Path('/tmp/rotation-core-independent-layout')/typ;folder.mkdir(parents=True,exist_ok=True)
 pdf=BASE/'outputs/PDF'/(PRE+'_'+typ+'.pdf')
 subprocess.run(['pdftoppm','-r','90','-png',str(pdf),str(folder/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 pages=sorted(folder.glob('page-*.png'),key=lambda x:int(x.stem.rsplit('-',1)[1]));files=[]
 for start in range(0,len(pages),12):
  contact=Image.new('RGB',(1320,1365),'#dddddd');draw=ImageDraw.Draw(contact)
  for j,p in enumerate(pages[start:start+12]):
   im=Image.open(p).convert('RGB');im.thumbnail((322,420));x=(j%4)*330+(330-im.width)//2;y=(j//4)*455+25
   contact.paste(im,(x,y));draw.text(((j%4)*330+5,(j//4)*455+5),typ+' p'+str(start+j+1),fill='black')
  target=OUT/(typ+'_overview_'+str(start+1)+'.jpg');contact.save(target,quality=90);files.append(str(target.relative_to(ROOT)))
 return {'type':typ,'pages':len(pages),'overview_files':files}
with ThreadPoolExecutor(max_workers=3) as pool:inventory=list(pool.map(render,TYPES))
(OUT/'visual_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
for typ in TYPES:
 pdf=BASE/'outputs/PDF'/(PRE+'_'+typ+'.pdf');text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
 (OUT/(typ+'.txt')).write_text(text)
 pages=text.split('\f')
 terms={'CBE_LessonSequence':['Lesson 2','Lesson 3','Lesson 12','Lesson 14'],'CompactTeacherGuide':['Lesson 3','Lesson 12','Lesson 14','consult'],'StudentMaterials':['CQE2','CQE3','CQE7','CQE12'],'MaterialsTeacherKey':['CQE3','CQE10','CQE14'],'FinalExplanation':['Form an expression','Interpret and explore','Write your answer'],'FinalExplanation_TeacherKey':['9801','−1/2','40cm'],'SummaryTable':['Lesson'],'StudentSummaryTable':['Lesson'],'AssessmentMaterials':['CQE14']}.get(typ,[])
 print(typ,{term:[i+1 for i,t in enumerate(pages) if term.casefold() in t.casefold()] for term in terms})
