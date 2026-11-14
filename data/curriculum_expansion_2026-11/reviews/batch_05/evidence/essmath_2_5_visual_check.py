from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageDraw
import subprocess,json,hashlib
E=Path(__file__).resolve().parent;R=E.parents[4];B=R/'data/curriculum_expansion_2026-11';O=E/'essmath_2_5_layout';O.mkdir(exist_ok=True)
PRE='Codex_Essential_Mathematics_Area_of_a_Part_of_a_Circle';P=json.loads((E/'essmath_2_5_artifact_review_check.json').read_text())['pdf_pages']
plan={'CBE_LessonSequence':[1,12,20,24,39,40,43],'CompactTeacherGuide':[4,7,11],'StudentMaterials':[1,2],'MaterialsTeacherKey':[1,2,3,4],'FinalExplanation':[1,3,4,5],'FinalExplanation_TeacherKey':[1,2,3],'SummaryTable':[1,2],'StudentSummaryTable':[1],'AssessmentMaterials':[1]}
def render(typ):
 tmp=Path('/tmp/circle-parts-independent-review')/typ;tmp.mkdir(parents=True,exist_ok=True);pdf=B/'outputs/PDF'/f'{PRE}_{typ}.pdf'
 subprocess.run(['pdftoppm','-r','70','-png',str(pdf),str(tmp/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 pages=sorted(tmp.glob('page-*.png'),key=lambda p:int(p.stem.rsplit('-',1)[1]));sheets=[]
 for start in range(0,len(pages),12):
  sheet=Image.new('RGB',(1440,1335),'#ddd');draw=ImageDraw.Draw(sheet)
  for j,p in enumerate(pages[start:start+12]):
   im=Image.open(p).convert('RGB');im.thumbnail((350,410));x=j%4*360+(360-im.width)//2;y=j//4*445+25;sheet.paste(im,(x,y));draw.text((j%4*360+5,j//4*445+5),f'{typ} p{start+j+1}',fill='black')
  target=O/f'{typ}_contact_{start+1}.jpg';sheet.save(target,quality=90);sheets.append(str(target.relative_to(R)))
 readable=[]
 for page in plan[typ]:
  target=O/f'{typ}_readable_{page}'
  subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-r','130','-singlefile','-png',str(pdf),str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  readable.append(str(target.with_suffix('.png').relative_to(R)))
 text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);(O/f'{typ}.txt').write_text(text)
 return {'type':typ,'pages':len(pages),'contacts':sheets,'readable_pages':plan[typ],'readable_images':readable}
with ThreadPoolExecutor(max_workers=3) as pool:inventory=list(pool.map(render,P))
manifest={'total_pages':sum(x['pages'] for x in inventory),'contact_sheets':sum(len(x['contacts']) for x in inventory),'readable_pages':sum(len(x['readable_pages']) for x in inventory),'documents':inventory}
(E/'essmath_2_5_visual_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
