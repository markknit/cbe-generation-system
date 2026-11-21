from pathlib import Path
import json,hashlib,zipfile,subprocess,re,xml.etree.ElementTree as ET
B=Path('data/curriculum_expansion_2026-11');E=B/'reviews/batch_06/evidence';N=json.loads((B/'manuscripts/gensci_2_1.json').read_text());S=json.loads((B/'sources/gensci_2_1.json').read_text());M=json.loads((B/'materials/gensci_2_1.json').read_text());P=next((B/'outputs/v2').rglob(N['prefix']+'_data.json'));D=json.loads(P.read_text());J=json.loads((E/'gensci_2_1_artifact_review_check.json').read_text());checks={};media={};geometry={};flat=lambda x:re.sub(r'\s+','',x);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','x':'http://www.w3.org/1999/xhtml'}
def ck(k,v):checks[k]=bool(v)
for k,v in N['unit'].items():
 if k not in ['keyInquiryQuestions','teacherConfirmationRequired']:ck('unit_'+k,D['UNIT'][k]==v)
ck('source_outcomes',D['UNIT']['learningOutcomes']=='\n'.join(x['text'] for x in S['outcomes']));ck('author_unit_fields_absent',all(k not in D['UNIT'] for k in ['keyInquiryQuestions','teacherConfirmationRequired']))
for i,(l,d) in enumerate(zip(N['lessons'],D['LESSONS']),1):
 for k in ['number','title','aresKeywords']:ck(f'L{i}_{k}',d[k]==l[k])
 for a,b in [('purpose','purpose'),('knowledge','knowledge'),('skills','skills'),('attitudes','attitudes'),('inquiry','keyInquiry'),('story','purposeInStoryline'),('safety','safetyNotes')]:ck(f'L{i}_slo_{a}',d['slo'][b]==l[a])
 ck(f'L{i}_overview',d['overview'].startswith(l['overview']));ck(f'L{i}_reflection',d['teacherReflection']==l['reflection']);ck(f'L{i}_summary',d['summaryTablePrompt']==l['summary'])
 for j,(p,q) in enumerate(zip(l['phases'],d['framework'])):
  for k,a in enumerate(['learnerExperience','teacherMoves','sensemakingStrategy','formativeAssessment']):ck(f'L{i}_phase{j}_{a}',q[a]==(str(l['minutes'][j])+' minutes. ' if k==1 else '')+p[k])
final={**N['assessment'],'sections':[{k:v for k,v in s.items() if k!='marks'} for s in N['assessment']['sections']]};ck('final_exact_projection',D['FINAL_EXPLANATION']==final)
ck('summary_exact',D['SUMMARY_TABLE']['lessons']==[{'number':l['number'],'title':l['title'],**l['summary']} for l in N['lessons']])
policy=B/'resource_policy.json';(E/'gensci_2_1_resource_policy_review_snapshot.json').write_bytes(policy.read_bytes());allowed=json.loads(policy.read_text())['module_allowed_titles']['gensci_2_1'];ck('allowlist_empty',allowed==[]);ck('selected_resources_zero',not J['selected_resources']);ck('all150slots_null',all(v[k] is None for l in D['LESSONS'] for v in l['resourceLinks'].values() for k in ['video','reading']))
for t in J['artifact_hashes']:
 doc=P.parent/(N['prefix']+'_'+t+'.docx');pdf=B/'outputs/PDF'/(N['prefix']+'_'+t+'.pdf')
 with zipfile.ZipFile(doc) as z:
  tree=ET.fromstring(z.read('word/document.xml'));text=' '.join(e.text or '' for e in tree.findall('.//w:t',ns));xml=' '.join(z.read(x).decode() for x in z.namelist() if x.startswith('word/') and x.endswith('.xml'));m=[x for x in z.namelist() if x.startswith(('word/media/','word/embeddings/'))]
 ptext=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
 if t in ['CBE_LessonSequence','CompactTeacherGuide','StudentMaterials','SummaryTable','StudentSummaryTable']:
  ck(t+'_held_reference_absent_Word',flat(M['items'][-1]['student']) not in flat(text));ck(t+'_held_reference_absent_PDF',flat(M['items'][-1]['student']) not in flat(ptext))
 ck(t+'_attribution',all(s in xml and s in ptext for s in ['SeaVuria','ARES','ChatGPT/Codex','OpenAI','BY-NC','4.0']));ck(t+'_no_unresolved',not any(s in ptext for s in ['{{','undefined','NaN','FILL','\ufffd']));ck(t+'_no_media',not m)
 pi=subprocess.check_output(['pdfimages','-list',str(pdf)],text=True).splitlines();media[t]={'word_media':m,'pdf_image_rows':pi[2:]};ck(t+'_pdf_no_raster_images',len(pi)==2)
 bbox=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-']));outside=[];sizes=[];nwords=0
 for i,page in enumerate(bbox.findall('.//x:page',ns),1):
  w,h=float(page.attrib['width']),float(page.attrib['height']);sizes.append([w,h])
  for q in page.findall('.//x:word',ns):
   nwords+=1
   if float(q.attrib['xMin'])<0 or float(q.attrib['yMin'])<0 or float(q.attrib['xMax'])>w or float(q.attrib['yMax'])>h:outside.append({'page':i,'word':q.text,'box':q.attrib})
 geometry[t]={'page_sizes_points':sorted(set(tuple(x) for x in sizes)),'word_count':nwords,'outside_page':outside};ck(t+'_text_within_page',not outside)
 if t=='StudentSummaryTable':
  rows=tree.findall('.//w:tbl/w:tr',ns);cells=[c for r in rows[1:] for c in r.findall('w:tc',ns)[1:]];ck('exact45empty_summarycells',len(cells)==45 and all(not ''.join(x.text or '' for x in c.findall('.//w:t',ns)).strip() for c in cells))
audit=B/'evidence/artifact_audit_gensci_2_1_2026-11-14.json';ck('frozen_audit_sha',sha(audit)=='d65c1e00fc05a0894f6989e644d89910d007e6065a8e4bdb3d1a3d4d8df958ba')
R={'export_sha256':sha(P),'resource_policy_snapshot_sha256':sha(E/'gensci_2_1_resource_policy_review_snapshot.json'),'checks':checks,'passed':sum(checks.values()),'total':len(checks),'failed':[k for k,v in checks.items() if not v],'media':media,'geometry':geometry};(E/'gensci_2_1_export_media_check.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps({k:R[k] for k in ['passed','total','failed','export_sha256']}))
