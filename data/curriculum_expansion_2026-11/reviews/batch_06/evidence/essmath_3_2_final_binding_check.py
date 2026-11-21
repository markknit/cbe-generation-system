"""Read-only exact accepted input/audit/Word/PDF metadata binding."""
from pathlib import Path
import json,hashlib,subprocess,zipfile,xml.etree.ElementTree as ET,re
E=Path(__file__).resolve().parent;R=E.parents[4];B=R/'data/curriculum_expansion_2026-11';O=E/'essmath_3_2_layout';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((E/'essmath_3_2_artifact_review_check.json').read_text());old=json.loads((E/'essmath_3_2_recheck_pass_2/binding.json').read_text());init=json.loads((E/'essmath_3_2_initial/binding.json').read_text());auditp=B/'evidence/artifact_audit_essmath_3_2_2026-11-14.json';audit=json.loads(auditp.read_text());accp=B/'reviews/essmath_3_2/content_acceptance.json';acc=json.loads(accp.read_text());n=json.loads((B/'manuscripts/essmath_3_2.json').read_text());P=n['prefix'];OUT=next((B/'outputs/v2').rglob(P+'_data.json')).parent;checks={};details={};ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','x':'http://www.w3.org/1999/xhtml'}
checks['accepted_fingerprint']=a['content_fingerprint']==acc['content_fingerprint']=='7340b23168e2832985c6ba588d8635c6a6d95eabb7657ac6a138ba1331786e43'
checks['audit_snapshot_sha']=sha(auditp)=='335ab4a571e33df1ea833271c22584797e55a8d8ade24a312c29a0eb15c84287'
checks['nine_module_IDs']=len(audit['documents'])==9 and all(r['module']=='essmath_3_2' for r in audit['documents'])
for p,h in old['inputs'].items():checks['canonical_'+p]=sha(R/p)==h
for entry in acc['evidence']:checks['accepted_report_'+entry['path']]=sha(R/entry['path'])==entry['sha256']
verp=B/'sources/essmath_3_2.verification.json';ver=json.loads(verp.read_text());sourcep=B/'sources/essmath_3_2.json';source=json.loads(sourcep.read_text())
sourcefiles={source['pdf']:source['pdf_sha256'],'data/curriculum_expansion_2026-11/sources/essmath_3_2_source.png':ver['crop_sha256'],ver['evidence']:ver['evidence_sha256'],'data/curriculum_expansion_2026-11/sources/essmath_3_2.verification.json':init['verification_sha256']}
checks['verified_source_record']=sha(sourcep)==ver['source_record_sha256']
for p,h in sourcefiles.items():checks['source_'+p]=sha(R/p)==h
for row in audit['documents']:
 typ=row['type'];doc=OUT/f'{P}_{typ}.docx';pdf=B/'outputs/PDF'/f'{P}_{typ}.pdf'
 for ext,p in [('docx',doc),('pdf',pdf)]:checks[typ+'_'+ext+'_frozen_hash']=sha(p)==row[ext+'_sha256']==a['artifact_hashes'][typ][ext+'_sha256']
 with zipfile.ZipFile(doc) as zz:
  x=ET.fromstring(zz.read('word/document.xml'));xml=' '.join(zz.read(q).decode() for q in zz.namelist() if q.startswith('word/') and q.endswith('.xml'));media=[q for q in zz.namelist() if q.startswith('word/media/')];text='\n'.join(''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in x.findall('.//w:p',ns));(O/f'{typ}_Word.txt').write_text(text)
  embedded=[q for q in zz.namelist() if q.startswith(('word/charts/','word/embeddings/'))];sects=[{q.tag.split('}')[-1]:q.attrib for q in sec if q.tag.endswith(('pgSz','pgMar'))} for sec in x.findall('.//w:sectPr',ns)]
 checks[typ+'_noWordmedia']=not media and not embedded
 if typ in old['actual_words']:
  prior=(E/f'essmath_3_2_initial/{typ}.txt').read_text();checks[typ+'_accepted_text_same']=re.sub(r'\s+','',prior)==re.sub(r'\s+','',text)
 pdftxt=(O/f'{typ}.txt').read_text()
 for token in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']:checks[typ+'_attribution_'+token]=token in xml and token in pdftxt
 listing=subprocess.check_output(['pdfimages','-list',str(pdf)],text=True);checks[typ+'_noPDFimages']=len(listing.strip().splitlines())==2
 bbox=ET.fromstring(subprocess.check_output(['pdftotext','-bbox-layout',str(pdf),'-']));pages=bbox.findall('.//x:page',ns);sizes=[];outside=[];wc=0
 for i,page in enumerate(pages,1):
  width=float(page.attrib['width']);height=float(page.attrib['height']);sizes.append([width,height])
  for w in page.findall('.//x:word',ns):
   wc+=1
   if min(float(w.attrib['xMin']),float(w.attrib['yMin']))<-.5 or float(w.attrib['xMax'])>width+.5 or float(w.attrib['yMax'])>height+.5:outside.append({'page':i,'word':w.text,'bbox':w.attrib})
 checks[typ+'_page_bbox_within_media']=not outside;details[typ]={'Word_media':media,'Word_chart_embeddings':embedded,'Word_sections':sects,'PDF_image_listing':listing,'PDF_page_sizes':sizes,'PDF_word_boxes_checked':wc,'PDF_word_boxes_outside_page':outside,'current_word_text_sha':sha(O/f'{typ}_Word.txt')}
with zipfile.ZipFile(OUT/f'{P}_StudentSummaryTable.docx') as zz:summaryx=ET.fromstring(zz.read('word/document.xml'))
summaryrows=summaryx.findall('.//w:tbl/w:tr',ns);blankcount=sum(not ''.join(t.text or '' for t in c.findall('.//w:t',ns)).strip() for r in summaryrows[1:] for c in r.findall('w:tc',ns)[1:]);checks['ten_student_summary_rows']=len(summaryrows)==11;checks['thirty_blank_student_cells']=blankcount==30
exportp=OUT/f'{P}_data.json';export=json.loads(exportp.read_text());slots=[v[k] for l in export['LESSONS'] for v in l['resourceLinks'].values() for k in ['video','reading']];checks['all100slotsnull']=len(slots)==100 and all(v is None for v in slots)
checks['final10slotsnull']=a['final_slots_null'];checks['no_selected_resources']=not a['selected_resources']
visp=E/'essmath_3_2_visual_manifest.json';vis=json.loads(visp.read_text());files=[auditp,accp,verp,exportp,B/'resource_policy.json',E/'essmath_3_2_artifact_review_check.json',visp]+[R/p for d in vis['documents'] for key in ['contacts','readable_images'] for p in d[key]]
res={'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'checks':checks,'accepted_fingerprint':a['content_fingerprint'],'content_acceptance':acc,'accepted_canonical_hashes':old['inputs'],'source_hashes':sourcefiles,'artifact_hashes':a['artifact_hashes'],'artifact_details':details,'all_resource_slots':{'total':len(slots),'null':slots.count(None)},'policy_note':'No module-specific essmath_3_2 entry exists in current resource policy; actual export selects zero resources. This review certifies actual metadata, not an invented allowlist or external media preview.','evidence_hashes':{str(p.relative_to(R)):sha(p) for p in files}}
(E/'essmath_3_2_final_binding_check.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':res['passed'],'total':res['total'],'failed':res['failed'],'PDF_words':sum(d['PDF_word_boxes_checked'] for d in details.values())},indent=2));assert all(checks.values())
