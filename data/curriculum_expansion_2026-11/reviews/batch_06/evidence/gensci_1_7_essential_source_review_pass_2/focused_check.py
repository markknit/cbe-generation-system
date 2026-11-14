from pathlib import Path
import json,hashlib
b=Path('data/curriculum_expansion_2026-11');r=b/'reviews/batch_06';o=Path(__file__).resolve().parent;p1=r/'evidence/gensci_1_7_essential_source_review_pass_1';c=json.loads((o/'binding.json').read_text());i=json.loads((p1/'binding.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();diff=[]
def walk(a,z,p):
 if type(a)!=type(z):diff.append(p);return
 if isinstance(a,dict):
  for k in set(a)|set(z):
   if k not in a or k not in z:diff.append(p+'.'+k)
   else:walk(a[k],z[k],p+'.'+k)
 elif isinstance(a,list):
  if len(a)!=len(z):diff.append(p+'.length')
  for k,(x,y) in enumerate(zip(a,z)):walk(x,y,p+'['+str(k)+']')
 elif a!=z:diff.append(p)
for k in ['sources','materials','blueprints','manuscripts']:
 old=json.loads((p1/(k+'_snapshot.json')).read_text());new=json.loads((b/k/'gensci_1_7.json').read_text());walk(old,new,k)
 if k!='manuscripts':assert c['inputs'][str(b/k/'gensci_1_7.json')]==i['inputs'][str(b/k/'gensci_1_7.json')]
assert diff and all(p.startswith(('manuscripts.lessons[11].minutes[','manuscripts.lessons[11].phases[','manuscripts.lessons[11].story')) for p in diff),diff
for f in ['source_pdf_sha256','source_crop_sha256','source_verification_sha256']:assert c[f]==i[f]
assert c['passed']==c['total']==445
same_text={k:(o/(k+'.txt')).read_bytes()==(p1/(k+'.txt')).read_bytes() for k in c['words'] if k!='CompactTeacherGuide'};assert all(same_text.values())
m=json.loads((b/'manuscripts/gensci_1_7.json').read_text());assert m['lessons'][11]['minutes']==[5,10,10,10,5];assert sum(m['lessons'][11]['minutes'])==40
prior=r/'gensci_1_7_review_essential_source_review_pass_1.md';assert sha(prior)=='5b6886fb6c5208813e83378e5820d03c20e04e4b4f7646377ec5f04718cdd378';initial=r/'gensci_1_7_review_essential_source_review.md';assert sha(initial)=='33db31f5c3713993b262f7b19e866a8c59c4a1feecc3a8d936dad0f0457792ba'
c['verdict']='PASS / ACCEPTED for content';c['semantic_content_acceptance']=True;c['unresolved_confirmed_errors']=0;(o/'binding.json').write_text(json.dumps(c,indent=2)+'\n')
z={'content_fingerprint':c['reviewed_content_fingerprint'],'changed_semantic_paths':sorted(diff),'source_materials_blueprint_unchanged':True,'all_other_manuscript_fields_unchanged':True,'unaffected_four_companion_body_texts_equal_pass1':same_text,'rebuilt_all5_Word_hashes_in_binding':True,'final_minutes':[5,10,10,10,5],'old_reports_unchanged':{str(p):sha(p) for p in [initial,prior]},'finding_closed':'GS17-C4','verdict':'PASS'};(o/'focused_diff.json').write_text(json.dumps(z,indent=2)+'\n');print(c['reviewed_content_fingerprint']);print('changed semantic fields',len(diff));print(''.join((o/'CompactTeacherGuide.txt').read_text().split('Lesson 12:',1)[1:]))
