from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET,subprocess
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';E=Path(__file__).resolve().parent;C=json.loads((E/'check.json').read_text());D=json.loads((B/'manuscripts/coremath_1_1.json').read_text());OUT=next((B/'outputs/v2').rglob(D['prefix']+'_data.json')).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};oldstr='Correct reciprocal model,4portions,units,assumption/product check and concrete evidence-based written advice.';newstr='Correct reciprocal model,portion count,units,assumption/product check and concrete evidence-based written advice.'
def delta(a,b,path=''):
 if type(a)!=type(b):return [{'path':path,'old':a,'new':b}]
 if isinstance(a,dict):return sum([delta(a.get(k),b.get(k),path+'/'+str(k)) for k in sorted(set(a)|set(b))],[])
 if isinstance(a,list):return sum([delta(x,y,path+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))],[]) if len(a)==len(b) else [{'path':path,'old':a,'new':b}]
 return [] if a==b else [{'path':path,'old':a,'new':b}]
zp=B/'coremath_1_1_Reviewed.zip';bridge={};canon={};export_delta=[]
with zipfile.ZipFile(zp) as z:
 for area in ['sources','materials','blueprints','manuscripts']:
  p=f'{area}/coremath_1_1.json';canon[area]=delta(json.loads(z.read(p)),json.loads((B/p).read_text()))
 for typ in C['pdf_pages']:
  p=OUT/(D['prefix']+'_'+typ+'.docx');rel=str(p.relative_to(B));oldbytes=z.read(rel)
  import io
  with zipfile.ZipFile(io.BytesIO(oldbytes)) as old,zipfile.ZipFile(p) as new:
   def text(q):root=ET.fromstring(q.read('word/document.xml'));return '\n'.join(''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in root.findall('.//w:p',ns))
   a,b=text(old),text(new);bridge[typ]={'old_docx_sha256':hashlib.sha256(oldbytes).hexdigest(),'new_docx_sha256':sha(p),'body_text_same':a==b,'only_neutral_descriptor_change':a.replace(oldstr,newstr)==b,'old_disclosure_occurrences':a.count(oldstr),'new_disclosure_occurrences':b.count(oldstr),'new_neutral_occurrences':b.count(newstr)}
  pdf=B/'outputs/PDF'/(D['prefix']+'_'+typ+'.pdf');oldpdf=z.read(str(pdf.relative_to(B)));pold=E/('archived_'+typ+'.pdf');pold.write_bytes(oldpdf);a=subprocess.check_output(['pdftotext','-layout',str(pold),'-'],text=True);b=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);norm=lambda s:''.join(s.split());bridge[typ]['pdf_nonspace_same']=norm(a)==norm(b);bridge[typ]['pdf_only_neutral_change']=norm(a).replace(norm(oldstr),norm(newstr))==norm(b)
 data=OUT/(D['prefix']+'_data.json');export_delta=delta(json.loads(z.read(str(data.relative_to(B)))),json.loads(data.read_text()))
# Review actual exported canonical structure, timings,resource slots,geometries.
export=json.loads(data.read_text());slots=[v[k] for l in export['LESSONS'] for v in l['resourceLinks'].values() for k in ['video','reading']];geometry={}
for typ in C['pdf_pages']:
 pdf=B/'outputs/PDF'/(D['prefix']+'_'+typ+'.pdf');x=ET.fromstring(subprocess.check_output(['pdftotext','-bbox-layout',str(pdf),'-']));nsx={'x':'http://www.w3.org/1999/xhtml'};pages=x.findall('.//x:page',nsx);geometry[typ]=[]
 for i,p in enumerate(pages,1):
  w,h=float(p.attrib['width']),float(p.attrib['height']);words=p.findall('.//x:word',nsx);outside=[t.text for t in words if float(t.attrib['xMin'])<0 or float(t.attrib['yMin'])<0 or float(t.attrib['xMax'])>w+.1 or float(t.attrib['yMax'])>h+.1];geometry[typ].append({'page':i,'width':w,'height':h,'out_of_page_words':outside})
result={'old_archive_sha256':sha(zp),'canonical_deltas':canon,'body_bridge':bridge,'structured_export_delta':export_delta,'slots':len(slots),'all_slots_null':all(v is None for v in slots),'final_minutes':D['lessons'][-1]['minutes'],'all40min':all(sum(l['minutes'])==40 for l in D['lessons']),'geometry':geometry,'all_text_in_page':all(not p['out_of_page_words'] for rows in geometry.values() for p in rows)};(E/'bridge.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='geometry'},indent=2))
