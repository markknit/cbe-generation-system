from pathlib import Path
import sys,json,hashlib,tempfile,subprocess,zipfile,shutil
from lxml import etree
from PIL import Image
ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT/'scripts'))
from curriculum import compiler
BASE=ROOT/'data/curriculum_expansion_2026-11'
OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
bank=BASE/'materials/gensci_1_2.json'
cards={x['id']:x for x in json.loads(bank.read_text())['items']}
compiler.BASE=BASE
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
rows=[]
with tempfile.TemporaryDirectory(prefix='cell-frame-independent-') as temporary:
 tmp=Path(temporary)
 for key in ['CL3','CL4','CL5','CL6','CL13']:
  card=cards[key];path=tmp/(key+'.docx')
  compiler.write_doc(path,'Technical crop-frame proof',[card])
  source=BASE/'materials'/card['diagram'];w,h=Image.open(source).size
  l,t,r,b=card.get('diagram_crop',[0,0,w,h])
  with zipfile.ZipFile(path) as z:
   media=[z.read(n) for n in z.namelist() if n.startswith('word/media/')]
   tree=etree.fromstring(z.read('word/document.xml'))
  assert media==[source.read_bytes()]
  extent=tree.find('.//wp:extent',ns);crop=tree.find('.//a:srcRect',ns)
  cx,cy=int(extent.get('cx')),int(extent.get('cy'))
  assert abs(cx/cy-(r-l)/(b-t))<1e-6
  assert cx<=6.3*914400 and cy<=6.5*914400
  row={'card':key,'source':str(source.relative_to(ROOT)),'source_sha256':sha(source),'source_pixels':[w,h],'crop_pixels':[l,t,r,b],'srcRect':dict(crop.attrib) if crop is not None else None,'extent_emu':[cx,cy],'embedded_original_bytes_equal':True}
  target=OUT/path.name;shutil.copy2(path,target)
  row['docx_sha256']=sha(target);rows.append(row)
 profile=(tmp/'lo_profile').as_uri()
 result=subprocess.run(['soffice','-env:UserInstallation='+profile,'--headless','--convert-to','pdf','--outdir',str(tmp),*[str(tmp/(k+'.docx')) for k in ['CL3','CL4','CL5','CL6','CL13']]],capture_output=True,text=True,timeout=120)
 assert result.returncode==0,result.stderr
 for row in rows:
  key=row['card'];pdf=tmp/(key+'.pdf');assert pdf.is_file();shutil.copy2(pdf,OUT/pdf.name)
  row['pdf_sha256']=sha(OUT/pdf.name)
  row['pdf_info']=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
  subprocess.run(['pdftoppm','-scale-to','1500','-png',str(pdf),str(OUT/key)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
result={'scope':'Technical proof, not Cell content or final-artifact acceptance','canonical_materials_sha256':sha(bank),'compiler_sha256':sha(ROOT/'scripts/curriculum/compiler.py'),'validation_sha256':sha(ROOT/'scripts/curriculum/validation.py'),'pipeline_sha256':sha(ROOT/'scripts/curriculum_pipeline.py'),'tests_sha256':sha(ROOT/'scripts/test_curriculum_pipeline.py'),'soffice_version':subprocess.check_output(['soffice','--version'],text=True).strip(),'cards':rows,'evidence_hashes':{p.name:sha(p) for p in sorted(OUT.iterdir()) if p.suffix in ['.png','.pdf','.docx']}}
(OUT/'binding.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps([{'card':r['card'],'crop':r['crop_pixels'],'extent':r['extent_emu'],'embedded_original_bytes_equal':True} for r in rows],indent=2))
