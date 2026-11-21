from pathlib import Path
import json, subprocess, hashlib
from PIL import Image,ImageOps,ImageDraw
B=Path('data/curriculum_expansion_2026-11');E=B/'reviews/batch_05/evidence';P=B/'outputs/PDF';prefix='Codex_General_Science_Transport_in_Plants_';j=json.loads((E/'gensci_1_4_artifact_review_check.json').read_text());R=E/'gensci_1_4_pages';R.mkdir(exist_ok=True)
manifest={'render_method':'pdftoppm75dpi every current PDF page;4x3 labelled contact sheets;selected direct readable pages at120dpi','pdf_hashes':{k:v['pdf_sha256'] for k,v in j['artifact_hashes'].items()},'page_counts':j['pdf_pages'],'images':[]}
def register(p,scope):manifest['images'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':scope})
for typ,count in j['pdf_pages'].items():
 pdf=P/(prefix+typ+'.pdf');subprocess.run(['pdftoppm','-r','75','-jpeg',str(pdf),str(R/typ)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 paths=sorted(R.glob(typ+'-*.jpg'))
 assert len(paths)==count
 for start in range(0,count,12):
  sheet=Image.new('RGB',(1280,1290),'#e7e7e7');draw=ImageDraw.Draw(sheet)
  for n,p in enumerate(paths[start:start+12],start+1):
   im=Image.open(p);im.thumbnail((310,400));x=((n-start-1)%4)*320+(320-im.width)//2;y=((n-start-1)//4)*430+24;sheet.paste(im,(x,y));draw.text((((n-start-1)%4)*320+8,y-20),f'{typ} p{n}',fill='black')
  out=E/f'gensci_1_4_{typ}_overview_{start+1}.jpg';sheet.save(out,quality=90);register(out,f'all pages {start+1}–{min(start+12,count)} contact survey')
# Include every material/caption page and selected procedure/function/final/table pages.
selected={'CBE_LessonSequence':[1,2,27,28,30,31,32,34,40,47,48,49,50],'CompactTeacherGuide':[7,8,9,11,13],'StudentMaterials':[1,2,3],'MaterialsTeacherKey':[1,2,3,4,5],'FinalExplanation':[1,2,3,4,5,6],'FinalExplanation_TeacherKey':[1,2,3],'SummaryTable':[1,2],'StudentSummaryTable':[1],'AssessmentMaterials':[1]}
for typ,pages in selected.items():
 for n in pages:
  out=E/f'gensci_1_4_{typ}_readable_{n}';subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','120','-singlefile','-png',str(P/(prefix+typ+'.pdf')),str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE);register(out.with_suffix('.png'),f'direct readable {typ} p{n} at120dpi')
(E/'gensci_1_4_visual_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print({k:v for k,v in manifest.items() if k!='images'});print('saved',len(manifest['images']),'review images')
