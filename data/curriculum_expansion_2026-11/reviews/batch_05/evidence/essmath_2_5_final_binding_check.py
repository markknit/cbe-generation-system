from pathlib import Path
import json,hashlib,subprocess,zipfile,xml.etree.ElementTree as ET
from PIL import Image,ImageChops
E=Path(__file__).resolve().parent;R=E.parents[4];B=R/'data/curriculum_expansion_2026-11';O=E/'essmath_2_5_layout';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((E/'essmath_2_5_artifact_review_check.json').read_text());old=json.loads((E/'essmath_2_5_review_binding.json').read_text());audit=json.loads((B/'evidence/batch_05_essmath_2_5_artifact_audit.json').read_text());acc=json.loads((B/'reviews/essmath_2_5/content_acceptance.json').read_text());P='Codex_Essential_Mathematics_Area_of_a_Part_of_a_Circle';OUT=next((B/'outputs/v2').rglob(P+'_data.json')).parent;checks={};images={};ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
checks['accepted_fingerprint']=a['content_fingerprint']=='75f60aa3258a3e6679ca81122364ee7d520b143579f80f7b2e4d2d6f4c93e770'
for p,h in old['canonical_hashes'].items():checks['canonical_'+p]=sha(B/p)==h
for p,h in old['source_related_hashes'].items():checks['source_'+p]=sha(R/p)==h
for row in audit['documents']:
 for ext in ['docx','pdf']:checks[row['type']+'_'+ext+'_audit_hash']=a['artifact_hashes'][row['type']][ext+'_sha256']==row[ext+'_sha256']
for k,v in old['draft_documents'].items():checks[k+'_contentaccepted_draft_hash']=sha(R/v['path'])==v['sha256']
checks['initial_report_immutable']=sha(B/'reviews/batch_05/essmath_2_5_initial.md')=='98eb42afc00d5c10fb39ed7dcfc6281eb92a7e3d1ebaf2750a2b7b2621d0aa57'
checks['recheck_immutable']=sha(B/'reviews/batch_05/essmath_2_5_recheck.md')=='995930a43937c99cc63502ead12239dd8e28e7e512e81a1c05c7a9efecab077a'
asset=B/'materials/diagrams/CP1.png';orig=Image.open(asset).convert('RGB')
for typ in ['StudentMaterials','MaterialsTeacherKey']:
 pdf=B/'outputs/PDF'/f'{P}_{typ}.pdf';pref=O/f'{typ}_extracted_image'
 subprocess.run(['pdfimages','-png',str(pdf),str(pref)],check=True)
 extracted=sorted(O.glob(f'{typ}_extracted_image-*.png'));checks[typ+'_onePDFimage']=len(extracted)==1
 im=Image.open(extracted[0]).convert('RGB');identical=im.size==orig.size and ImageChops.difference(im,orig).getbbox() is None;checks[typ+'_PDFpixelidentity']=identical
 with zipfile.ZipFile(OUT/f'{P}_{typ}.docx') as z:
  media={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')};x=ET.fromstring(z.read('word/document.xml'));extents=[e.attrib for e in x.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent')]
 checks[typ+'_Wordassetbytes']=sha(asset) in media.values();checks[typ+'_aspect2to1']=len(extents)==1 and int(extents[0]['cx'])==2*int(extents[0]['cy'])
 images[typ]={'PDF_extracted':str(extracted[0].relative_to(R)),'PDF_extracted_sha256':sha(extracted[0]),'native_RGB_pixel_identity':identical,'native_dimensions':im.size,'Word_media':media,'Word_extents':extents,'pdfimages_list':subprocess.check_output(['pdfimages','-list',str(pdf)],text=True)}
export=json.loads((OUT/f'{P}_data.json').read_text());slots=[v[k] for l in export['LESSONS'] for v in l['resourceLinks'].values() for k in ['video','reading']];checks['all100slotsnull']=len(slots)==100 and all(v is None for v in slots)
policy=json.loads((B/'evidence/essmath_2_5_resource_policy_snapshot.json').read_text());checks['scopedemptyallowlist']=policy['module_allowed_titles']['essmath_2_5']==[]
for typ in a['artifact_hashes']:
 with zipfile.ZipFile(OUT/f'{P}_{typ}.docx') as z:xml=' '.join(z.read(n).decode() for n in z.namelist() if n.startswith('word/') and n.endswith('.xml'))
 txt=(O/f'{typ}.txt').read_text()
 for token in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']:checks[typ+'_attribution_'+token]=token in xml and token in txt
visual=json.loads((E/'essmath_2_5_visual_manifest.json').read_text());files=[E/'essmath_2_5_artifact_review_check.json',E/'essmath_2_5_visual_manifest.json',B/'evidence/batch_05_essmath_2_5_artifact_audit.json',B/'evidence/essmath_2_5_resource_policy_snapshot.json',B/'reviews/essmath_2_5/content_acceptance.json',OUT/f'{P}_data.json']+[R/p for d in visual['documents'] for key in ['contacts','readable_images'] for p in d[key]]
res={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'content_acceptance':acc,'accepted_binding':old,'artifact_hashes':a['artifact_hashes'],'images':images,'all_resource_slots':{'total':len(slots),'null':slots.count(None)},'evidence_hashes':{str(p.relative_to(R)):sha(p) for p in files}}
(E/'essmath_2_5_final_binding_check.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':res['passed'],'total':res['total'],'failed':res['failed'],'acceptance':acc,'images':images},indent=2))
assert all(checks.values())
