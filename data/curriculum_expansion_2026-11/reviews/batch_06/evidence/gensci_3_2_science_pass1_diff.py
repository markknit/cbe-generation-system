"""Focused immutable-initial to current namespace correction verification."""
from pathlib import Path
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'scripts'))
from curriculum_pipeline import content_fingerprint
B=ROOT/'data/curriculum_expansion_2026-11';E=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
norm=lambda s:re.sub(r'\s+',' ',s).strip()
reverse=lambda s:re.sub(r'GSLM(?=\d)','LM',s)
initial=json.loads((E/'gensci_3_2_science_initial_word_check.json').read_text());current=json.loads((E/'gensci_3_2_science_pass1_word_check.json').read_text())
checks={};diffs=[];bindings={}
def diff(a,b,path=''):
 if type(a)!=type(b):diffs.append({'path':path,'type_change':True});return
 if isinstance(a,dict):
  if a.keys()!=b.keys():diffs.append({'path':path,'key_change':True});return
  for k in a:diff(a[k],b[k],path+'.'+k)
 elif isinstance(a,list):
  if len(a)!=len(b):diffs.append({'path':path,'length_change':True});return
  for i,(x,y) in enumerate(zip(a,b)):diff(x,y,path+f'[{i}]')
 elif a!=b:diffs.append({'path':path,'before':a,'after':b,'namespace_only':isinstance(a,str) and isinstance(b,str) and reverse(b)==a})
for kind in ['sources','materials','manuscripts','blueprints']:
 oldpath=E/f'gensci_3_2_initial_{kind}_snapshot.json';newpath=B/kind/'gensci_3_2.json'
 old=json.loads(oldpath.read_text());new=json.loads(newpath.read_text())
 checks[kind+'_reverse_namespace_restores_entire_initial_json']=json.loads(reverse(json.dumps(new,ensure_ascii=False)))==old
 if kind=='sources':checks['source_exact_bytes_unchanged']=sha(newpath)==sha(oldpath)
 if kind=='materials':checks['all22calculation_records_and_ids_unchanged']=old['calculations']==new['calculations'] and len(new['calculations'])==22;checks['all13_unique_new_cardids']=[c['id'] for c in new['items']]==['GSLM'+str(i) for i in range(1,14)]
 if kind=='manuscripts':checks['same_final_minutes']=new['lessons'][-1]['minutes']==old['lessons'][-1]['minutes']==[4,8,12,10,6]
 diff(old,new,kind)
 q=E/f'gensci_3_2_pass1_{kind}_snapshot.json';q.write_bytes(newpath.read_bytes());bindings[kind]={'initial_sha256':sha(oldpath),'current_sha256':sha(newpath),'current_snapshot':str(q.relative_to(ROOT))}
checks['every_actual_scalar_change_namespace_only']=bool(diffs) and all(d.get('namespace_only',False) for d in diffs)
checks['exactly3canonical_documents_changed']={x.split('.')[0] for x in [d['path'] for d in diffs]}=={'materials','manuscripts','blueprints'}
checks['source_verification_bytes_unchanged']=sha(B/'sources/gensci_3_2.verification.json')==initial['canonical_hashes']['sources/gensci_3_2.verification.json']
checks['sourcecrop_unchanged']=sha(B/'sources/gensci_3_2_source.png')=='f368a4b4ce0c0c8b06f816a5c77f13b420510b7328759b94922090480b248172'
legacy={'LM5':'0abc74762b0987c5e805a89b3699d2606f5d6a3b7a243956bd1359de59bc3e06','LM8':'8a953fdb52665bfa85db27ab70e0775bc51261cbd082df55f9e759874b097af7'}
checks['old_legacy_graph_bytes_unchanged']=all(sha(B/'materials/diagrams'/(k+'.png'))==h for k,h in legacy.items())
checks['no_new_GSLM_graph_file_exists']=not any((B/'materials/diagrams').glob('GSLM*'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
o=B/'outputs/v2/General_Science/SS3.2_Linear_Motion';wordbridge={}
for typ,h in current['draft_word_hashes'].items():
 p=o/('Codex_General_Science_Linear_Motion_'+typ+'.docx')
 with zipfile.ZipFile(p) as z:
  root=ET.fromstring(z.read('word/document.xml'));raw='\n'.join(''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in root.findall('.//w:p',ns));media=[q for q in z.namelist() if q.startswith('word/media/')];blips=root.findall('.//a:blip',ns)
  checks[typ+'_no_media_or_drawing_references']=not media and not blips
  old=(E/f'gensci_3_2_{typ}_science_initial_review_text.txt').read_text()
  checks[typ+'_reverse_namespace_restores_body_text']=norm(reverse(raw))==norm(old)
  checks[typ+'_no_old_numeric_card_reference']=not re.search(r'(?<!GS)LM\d+',raw)
  checks[typ+'_current_hash_matches_word_reader']=sha(p)==h
  if typ=='StudentSummaryTable':
   rs=root.findall('.//w:tbl/w:tr',ns);cells=[''.join(t.text or '' for t in c.findall('.//w:t',ns)).strip() for row in rs[1:] for c in row.findall('w:tc',ns)[1:]]
   checks['current_exact39_blank_response_cells']=len(rs)==14 and len(cells)==39 and not any(cells)
  wordbridge[typ]={'initial_sha256':initial['draft_word_hashes'][typ],'current_sha256':h,'initial_body_text_sha256':sha(E/f'gensci_3_2_{typ}_science_initial_review_text.txt'),'current_body_text_sha256':sha(E/f'gensci_3_2_{typ}_science_pass1_review_text.txt'),'media_count':len(media),'drawing_reference_count':len(blips)}
checks['current_fingerprint_matches_word_reader']=content_fingerprint(B,'gensci_3_2')==current['content_fingerprint']
checks['all_actual_word_structural_protections_pass']=all(current['student_exemplars_absent'].values()) and all(current['teacher_keys_absent'].values()) and current['blank_student_summary_13_rows'] and current['final_card_text_absent_teaching'] and all(current['attribution'].values())
r={'scope':'Namespace-only focused correction,not a repeated physics review','initial_report_sha256':sha(B/'reviews/batch_06/gensci_3_2_initial_science.md'),'initial_fingerprint':initial['content_fingerprint'],'current_fingerprint':current['content_fingerprint'],'canonical_bindings':bindings,'scalar_changes':diffs,'scalar_change_count':len(diffs),'checks':checks,'checks_pass':sum(checks.values()),'checks_total':len(checks),'word_bridge':wordbridge}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'scalar_changes':len(diffs),'checks_pass':sum(checks.values()),'checks_total':len(checks),'failures':[k for k,v in checks.items() if not v]},indent=2));assert all(checks.values())
