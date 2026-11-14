from pathlib import Path
import json,hashlib
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';O=Path(__file__).resolve().parent;I=B/'reviews/batch_06/evidence/gensci_2_5_initial_essential';oldbind=json.loads((I/'binding.json').read_text());curbind=json.loads((O/'binding.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();changes=[]
def walk(a,z,p):
 if type(a)!=type(z):changes.append({'path':p,'before':a,'after':z});return
 if isinstance(a,dict):
  for k in set(a)|set(z):
   if k not in a or k not in z:changes.append({'path':p+'.'+k,'before':a.get(k),'after':z.get(k)})
   else:walk(a[k],z[k],p+'.'+k)
 elif isinstance(a,list):
  if len(a)!=len(z):changes.append({'path':p+'.length','before':len(a),'after':len(z)})
  for j,(x,y) in enumerate(zip(a,z)):walk(x,y,p+'['+str(j)+']')
 elif a!=z:changes.append({'path':p,'before':a,'after':z})
old={};new={}
for k in ['sources','blueprints','materials','manuscripts']:
 p=B/k/'gensci_2_5.json';old[k]=json.loads((I/(k+'_snapshot.json')).read_text());new[k]=json.loads(p.read_text());walk(old[k],new[k],k);(O/(k+'_snapshot.json')).write_bytes(p.read_bytes())
allowed={'sources.suggested_learning_experiences[3]','sources.verified_by','materials.items[9].teacher','manuscripts.assessment.sections[1].exemplar'};assert {x['path'] for x in changes}==allowed
for f in ['source_pdf_sha256','source_crop_sha256']:assert curbind[f]==oldbind[f]
vpath=B/'sources/gensci_2_5.verification.json';v=json.loads(vpath.read_text());ep=R/v['evidence'];assert v['status']=='verified';assert v['source_record_sha256']==sha(B/'sources/gensci_2_5.json');assert v['crop_sha256']==sha(B/'sources/gensci_2_5_source.png');assert v['evidence_sha256']==sha(ep);assert new['sources']['pdf_sha256']==curbind['source_pdf_sha256']
assert 'biological, chemical and physical processes' in new['sources']['suggested_learning_experiences'][3]
unchanged={k:(O/(k+'.txt')).read_bytes()==(I/(k+'.txt')).read_bytes() for k in curbind['words'] if k!='MaterialsTeacherKey'};assert all(unchanged.values())
expected=(I/'MaterialsTeacherKey.txt').read_text().replace(old['materials']['items'][9]['teacher'],new['materials']['items'][9]['teacher']);assert expected==(O/'MaterialsTeacherKey.txt').read_text()
assert new['materials']['calculations']==old['materials']['calculations'];assert new['materials']['items'][2]==old['materials']['items'][2];assert new['blueprints']==old['blueprints'];assert curbind['passed']==curbind['total']==479
prior=B/'reviews/batch_06/gensci_2_5_initial_essential.md';assert sha(prior)=='a7609f5847abb494d0ff7d93e268a183b244607add325905fcef894405577375'
for k,w in curbind['words'].items():assert sha(R/w['path'])==w['sha256']
for p,h in curbind['inputs'].items():assert sha(R/p)==h
(O/'source_verification_snapshot.json').write_bytes(vpath.read_bytes());(O/'source_verification_evidence_snapshot.md').write_bytes(ep.read_bytes());curbind['verdict']='PASS / ACCEPTED for authored content';curbind['semantic_content_acceptance']=True;curbind['unresolved_confirmed_errors']=0;(O/'binding.json').write_text(json.dumps(curbind,indent=2)+'\n')
r={'verdict':'PASS','content_fingerprint':curbind['reviewed_content_fingerprint'],'closed':['GS25-C1','GS25-C2'],'semantic_changes':sorted(changes,key=lambda x:x['path']),'all_other_canonical_fields_unchanged':True,'source_pdf_and_crop_unchanged':True,'source_verification_current_record_crop_evidence_hashes_match':True,'verification_files':{str(vpath.relative_to(R)):sha(vpath),str(ep.relative_to(R)):sha(ep)},'unaffected_four_companion_body_texts_identical':unchanged,'key_body_text_change_exactly_RR10_teacher_replacement':True,'initial_report_sha256':sha(prior),'initial_numeric_evidence_sha256':sha(I/'fixed_checks.json'),'RR3_and_b_maps_performance_conditions_unchanged':True}
(O/'focused_diff.json').write_text(json.dumps(r,indent=2)+'\n');print(r['content_fingerprint']);print('4canonical field changes only;source verification bindings and5actualWord PASS')
