from pathlib import Path
import json,hashlib,zipfile,sys,collections,re
R=Path.cwd();B=R/'data/curriculum_expansion_2026-11';P=R/'data/codex_pilot_2026-11';O=B/'reviews/batch_07/evidence/final_delivery_index_review';sys.path.insert(0,str(R/'scripts'));from curriculum_pipeline import content_fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();idx=json.loads((B/'FINAL_DELIVERY_INDEX.json').read_text());integrity=json.loads((B/'evidence/final_checkpoint_integrity_2026-11-15.json').read_text());checks=[]
def ck(n,b):checks.append({'check':n,'pass':bool(b)})
ck('43 unit rows',len(idx['unit_index'])==43);ck('43 distinct unit identifiers',len({u['module']for u in idx['unit_index']})==43);ck('38 distinct current archives',len(idx['current_archives'])==len({a['path']for a in idx['current_archives']})==38)
subjects=collections.defaultdict(lambda:{'units':0,'lessons':0});totals=collections.Counter();archives=[];covered=[];unitpaths={};alllive=[]
for u in idx['unit_index']:
 base=B if u['origin']=='expansion'else P;mod=u['module'];m=json.loads((base/'manuscripts'/f'{mod}.json').read_text());ck(mod+' metadata+lesson count',all(u[k]==m[k]for k in ['subject','topic'])and u['lessons']==len(m['lessons']));subjects[m['subject']]['units']+=1;subjects[m['subject']]['lessons']+=len(m['lessons']);unitpaths[mod]=(base,m['prefix']);
 if base==B:ck(mod+' current content fingerprint',u['content_fingerprint']==content_fingerprint(B,mod)==integrity['modules'][mod]['fingerprint']);ck(mod+' acceptance exists',Path(u['content_acceptance']).is_file())
 else:ck(mod+' frozen review report exists',Path(u['review_report']).is_file())
for a in idx['current_archives']:
 path=R/a['path'];ck(path.name+' SHA256',sha(path)==a['sha256']);row={'path':a['path'],'sha256':sha(path),'modules':a['modules'],'primary_members':{},'raw_file_counts':{}};covered+=a['modules']
 with zipfile.ZipFile(path)as z:
  ck(path.name+' ZIP CRC',z.testzip()is None);names=z.namelist();raw=collections.Counter(Path(n).suffix for n in names);row['raw_file_counts']={k:raw[k]for k in ['.docx','.pdf','.json']};primary=[n for n in names if n.startswith('outputs/')and(n.endswith(('.docx','.pdf'))or n.endswith('_data.json'))];row['primary_members']={'docx':sum(n.endswith('.docx')for n in primary),'pdf':sum(n.endswith('.pdf')for n in primary),'exports':sum(n.endswith('_data.json')for n in primary)}
  for k,v in row['primary_members'].items():totals[k]+=v
  row['live_member_compared']=0;row['primary_hashes']={}
  base=P if path.is_relative_to(P)else B
  for n in primary:
   f=base/n;ck(path.name+' primary current '+n,f.is_file()and hashlib.sha256(z.read(n)).hexdigest()==sha(f));row['primary_hashes'][n]=hashlib.sha256(z.read(n)).hexdigest();row['live_member_compared']+=1;alllive.append({'path':str(f.relative_to(R)),'sha256':sha(f)})
  for mod in a['modules']:
   base,pre=unitpaths[mod];members=[n for n in primary if Path(n).name.startswith(pre+'_')];d=[n for n in members if n.endswith('.docx')];p=[n for n in members if n.endswith('.pdf')];e=[n for n in members if n.endswith('_data.json')];ck(mod+' packaged9Word9PDF1export',len(d)==9 and len(p)==9 and len(e)==1);ck(mod+' paired type stems',{Path(n).stem for n in d}=={Path(n).stem for n in p});u=next(u for u in idx['unit_index']if u['module']==mod);ck(mod+' correct archive row',u['archive']==str(path.relative_to(R)));export=json.loads(z.read(e[0]));ck(mod+' exported lessons',len(export['LESSONS'])==u['lessons'])
  # All frozen pilot154members checked to current files as claimed.
  if path.is_relative_to(P):
   files=[n for n in names if not n.endswith('/')];ck('frozen pilot154files',len(files)==154)
   for n in files:ck('pilot current member '+n,(P/n).is_file()and z.read(n)==(P/n).read_bytes())
 archives.append(row)
ck('each unit exactly once current archives',collections.Counter(covered)==collections.Counter(u['module']for u in idx['unit_index']));ck('actual current primary counts',dict(totals)=={'docx':387,'pdf':387,'exports':43});ck('index primary counts',idx['docx']==totals['docx']and idx['pdf']==totals['pdf']and idx['structured_exports']==totals['exports']);ck('subject totals',dict(subjects)==idx['by_subject']);ck('total514lessons',sum(v['lessons']for v in subjects.values())==idx['lessons']==514)
historical=[]
for a in idx['superseded_historical_archives']:
 path=B/a['archive'];receipt=Path(a['receipt_path']);r=json.loads(receipt.read_text());ck(a['module']+' old SHA unchanged',sha(path)==a['sha256']);ck(a['module']+' historical receipt corrected',receipt==Path(a['snapshot_directory'])/'original_receipt.json'and r['archive']==a['archive']and r['sha256']==a['sha256']);ck(a['module']+' superseded not current',str(path.relative_to(R))not in [a['path']for a in idx['current_archives']]);ck(a['module']+' current receipt explicitly labelled',Path(a['current_receipt_path']).is_file());historical.append({'path':str(path.relative_to(R)),'sha256':sha(path),'receipt_path':str(receipt),'receipt_sha256':sha(receipt),'replacement_receipt_sha256':sha(Path(a['current_receipt_path']))})
ck('two historical archives',len(historical)==2);ck('integrity40/483/37 zeroerrors',integrity['expansion_units']==40 and integrity['expansion_lessons']==483 and len(integrity['archives'])==37 and integrity['errors']==[]and integrity['blocked_source_modules']==[])
canonical=json.loads((B/'evidence/final_canonical_validation.json').read_text());ck('canonical40unitszeroerrors',canonical['units']==40 and canonical['errors']==0 and len(canonical['results'])==40 and all(not x['errors']for x in canonical['results']));pilot=json.loads((B/'evidence/final_frozen_pilot_integrity.json').read_text());ck('pilot integrity noerrors154',not pilot['errors']and pilot['members']==154)
partner=json.loads((B/'evidence/final_partner_export_scope.json').read_text());logp=R/partner['log'];log=logp.read_text();ck('partner log hash',sha(logp)==partner['log_sha256']);ck('partner scoped43/514andknownfail',partner['units']==43 and partner['lessons']==514 and partner['exit_code']==1 and len(partner['exports'])==43)
for e in partner['exports']:ck('partner current export '+e['path'],sha(Path(e['path']))==e['sha256'])
for text in ['0/43 file(s) conform · 213 total drift issue(s)','43 bundle(s) generated, previewed and grouped','CONTRACT GATE: 16 passed, 0 failed','24 passed, 1 failed','GATE: 3/7 adapter/fidelity checks passed']:ck('partner log '+text,text in log)
status=(B/'FINAL_CURRICULUM_STATUS.md').read_text();ck('statusdisclosespartnerfailure','Overall partner integration remains failing'in status and'0/43 conform; 213 drift findings'in status and'3/7'in status and'24/25'in status);ck('statusdisclosesclassroomlimits','Teacher classroom, practical, access, and pacing acceptance remain pending'in status);ck('statussayslocalkeys/historical','teacher-review packages containing answer keys'in status and'superseded are historical evidence'in status)
# Check all Markdown links resolve locally; no remote links in index expected.
links=re.findall(r'\]\(([^)]+)\)',status)
for link in links:ck('status link '+link,(B/link).resolve().is_file())
# Exact postfinding correction: only both historical receipt_paths plus explicit current_receipt_path.
initial=json.loads((O/'initial_FINAL_DELIVERY_INDEX.json').read_text());a=json.loads(json.dumps(idx))
for row in a['superseded_historical_archives']:row['receipt_path']=row.pop('current_receipt_path')
ck('FDI1 exact index-only path correction',a==initial);ck('FDI1 statusunchanged',(B/'FINAL_CURRICULUM_STATUS.md').read_bytes()==(O/'initial_FINAL_CURRICULUM_STATUS.md').read_bytes())
r={'verdict':'PASS'if all(x['pass']for x in checks)else'HOLD','checks':checks,'passed':sum(x['pass']for x in checks),'total':len(checks),'subjects':dict(subjects),'actual_primary_counts':dict(totals),'archives':archives,'historical':historical,'unit_live_primary_files':alllive,'index_status_and_evidence_hashes':{str(p.relative_to(R)):sha(p)for p in [B/'FINAL_DELIVERY_INDEX.json',B/'FINAL_CURRICULUM_STATUS.md',B/'evidence/final_checkpoint_integrity_2026-11-15.json',B/'evidence/final_canonical_validation.json',B/'evidence/final_frozen_pilot_integrity.json',B/'evidence/final_partner_export_scope.json',logp,B/'evidence/final_superseded_archive_integrity.json',B/'evidence/superseded_packages_2026-11-15/superseded_originals.json']}}
(O/'final_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(r['verdict'],r['passed'],r['total']);print('FAILURES',[c for c in checks if not c['pass']]);print('counts',r['actual_primary_counts']);print('rawarchiveddocxPDF',sum(a['raw_file_counts']['.docx']for a in archives),sum(a['raw_file_counts']['.pdf']for a in archives))
