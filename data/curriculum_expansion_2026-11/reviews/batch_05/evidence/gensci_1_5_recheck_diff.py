from pathlib import Path
import json,hashlib,sys,zipfile,xml.etree.ElementTree as E
B=Path('data/curriculum_expansion_2026-11');V=B/'reviews/batch_05/evidence';initial=json.loads((V/'gensci_1_5_initial_check.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();changes=[{'file':'manuscripts/gensci_1_5.json','field':'unit.focus','old':'RQwithundefinedlimits','new':'RQ with zero-denominator limits'},{'file':'manuscripts/gensci_1_5.json','field':'lessons[10].phases[2][0]','old':'Check undefinedquotient,products/ATP,temperature and no-tasting/performed-evidence limits.','new':'Check cases with no defined quotient,products/ATP,temperature and no-tasting/performed-evidence limits.'},{'file':'materials/gensci_1_5.json','field':'RS11.teacher','old':'zeroO2RQundefinedandnotsubstrateidentifier','new':'With zero oxygen consumption,RQ has no defined finite value and cannot identify a substrate'}]
canonical=[]
for rel,oldsha in initial['canonical_hashes'].items():
 p=B/rel;new=p.read_text();reconstructed=new
 for c in changes:
  if c['file']==rel:
   assert reconstructed.count(c['new'])==1
   reconstructed=reconstructed.replace(c['new'],c['old'])
 canonical.append({'path':rel,'initial_sha256':oldsha,'current_sha256':sha(p),'reverse_reconstruction_sha256':hashlib.sha256(reconstructed.encode()).hexdigest(),'pass':hashlib.sha256(reconstructed.encode()).hexdigest()==oldsha})
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};out=B/'outputs/v2/General_Science/SS1.5_Respiration';words=[]
for typ,oldsha in initial['draft_word_hashes'].items():
 p=out/('Codex_General_Science_Respiration_'+typ+'.docx')
 with zipfile.ZipFile(p) as z:
  root=E.fromstring(z.read('word/document.xml'));new='\n'.join(''.join(t.text or '' for t in x.findall('.//w:t',N)) for x in root.findall('.//w:p',N))
 old=(V/('gensci_1_5_'+typ+'_review_text.txt')).read_text();expected=old
 applicable=[]
 for c in changes:
  if c['old'] in expected:expected=expected.replace(c['old'],c['new']);applicable.append(c['field'])
 words.append({'type':typ,'initial_sha256':oldsha,'current_sha256':sha(p),'binary_same':sha(p)==oldsha,'expected_body_changes':applicable,'body_exactly_initial_with_only_applicable_replacements':new==expected})
primary=V/'respiration_primary/WSU_FS173E_independent.pdf';sol=V/'gensci_1_5_independent_solutions.json';r={'changes':changes,'canonical_reverse_reconstruction':canonical,'word_body_diff_bridge':words,'no_placeholder_substring_in_bank_manuscript':all('undefined' not in (B/p).read_text().lower() for p in ['materials/gensci_1_5.json','manuscripts/gensci_1_5.json']),'initial_report_unchanged':sha(B/'reviews/batch_05/gensci_1_5_initial.md')=='fad8e05d41dcd8b0591580a55b05c7c0e6fef77f6ba42103802b9e2fbcae81ab','primary_original_unchanged':sha(primary)=='d064e2e41b7ec8d5a6114678afd6933b710deecb3dc71c03aec6fce9ce3f802d','independent_solutions_unchanged':sha(sol)=='36e38c57cf917a5b16f785da48c72aa4b4b60769337599d75927f1b141b4d103','removed_wrong_audit_not_used':not (B/'evidence/batch_05_gensci_1_5_artifact_audit.json').exists()}
(V/'gensci_1_5_recheck_diff.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
assert all(x['pass'] for x in canonical) and all(x['body_exactly_initial_with_only_applicable_replacements'] for x in words) and r['no_placeholder_substring_in_bank_manuscript'] and r['initial_report_unchanged'] and r['primary_original_unchanged'] and r['independent_solutions_unchanged']
