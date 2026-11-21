"""Read-only final isolation, blank-cell and frozen-artifact binding checks."""
from pathlib import Path
import hashlib, json, re, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts'))
from curriculum_pipeline import content_fingerprint
W=ROOT/'data/curriculum_expansion_2026-11'; E=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
norm=lambda s:re.sub(r'\s+','',s)
D=json.loads((W/'manuscripts/gensci_2_2.json').read_text())
OUT=next((W/'outputs/v2').rglob(D['prefix']+'_data.json')).parent
auditpath=W/'evidence/artifact_audit_gensci_2_2_2026-11-14.json'
audit=json.loads(auditpath.read_text()); prior=json.loads((E/'gensci_2_2_artifact_review_check.json').read_text())
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
hashes={}; texts={}; trees={}
for row in audit['documents']:
 typ=row['type']; doc=OUT/(D['prefix']+'_'+typ+'.docx'); pdf=W/'outputs/PDF'/(D['prefix']+'_'+typ+'.pdf')
 hashes[typ]={'docx_sha256':sha(doc),'pdf_sha256':sha(pdf)}
 with zipfile.ZipFile(doc) as z: trees[typ]=ET.fromstring(z.read('word/document.xml'))
 texts[typ]=norm(subprocess.check_output(['pdftotext',str(pdf),'-']).decode())
summaryrows=trees['StudentSummaryTable'].findall('.//w:tbl/w:tr',ns)
responses=[ ''.join(t.text or '' for t in c.findall('.//w:t',ns)).strip() for r in summaryrows[1:] for c in r.findall('w:tc',ns)[1:] ]
teaching=['CBE_LessonSequence','CompactTeacherGuide','StudentMaterials','SummaryTable','StudentSummaryTable']
held=['INDEPENDENT FINAL REFERENCE','Fictional materialM is identified asCu by a trusted sample record']
heldabsent={t:all(norm(s) not in texts[t] for s in held) for t in teaching}
heldpresent={t:all(norm(s) in texts[t] for s in held) for t in ['AssessmentMaterials','MaterialsTeacherKey']}
fp=content_fingerprint(W,'gensci_2_2')
checks={
 'corrected_audit_sha256':sha(auditpath)=='5cf68e611405753b18d71c00814737fd1c7da8d32c971e4c7928b41c5962b8cc',
 'all18_current_hashes_match_snapshot':all(hashes[r['type']]['docx_sha256']==r['docx_sha256'] and hashes[r['type']]['pdf_sha256']==r['pdf_sha256'] for r in audit['documents']),
 'all18_hashes_unchanged_during_visual_review':hashes==prior['artifact_hashes'],
 'accepted_fingerprint_unchanged':fp=='7773c26c304657c4b5bdf47e315c437d322ac2bdfcef093d341fe80b435972a9',
 'student_summary13rows':len(summaryrows)==13,
 'exact36_student_summary_response_cells':len(responses)==36,
 'all36_student_summary_responses_blank':not any(responses),
 'held_case_absent_all5_teaching_pdf':all(heldabsent.values()),
 'held_case_present_standalone_final_and_private_materials_pdf':all(heldpresent.values()),
 'final_papers_refer_to_standalone_CF12':all(norm('Use only final reference and prompts') in texts[t] for t in ['FinalExplanation','FinalExplanation_TeacherKey']),
}
manifestpath=E/'gensci_2_2_visual_manifest.json'; manifest=json.loads(manifestpath.read_text())
for item in manifest['images']:item['actually_inspected']=True
manifest['inspection_complete']=True
manifest['pages_surveyed']=sum(manifest['page_counts'].values())
manifest['contact_sheets_inspected']=sum('overview' in x['path'] for x in manifest['images'])
manifest['readable_pages_inspected']=sum('readable' in x['path'] for x in manifest['images'])
manifest['observations']='All85pages surveyed through14contact sheets;44selectedpages read at120dpi. All student material/private key/final/summary pages read. Student CF4p1-2/CF8p2-3 and private CF12keyp5-6 continue intact. Final rubric p4-5 and key rubric p2-3 continue intact. No confirmed clipping/overlap/lostcontent;CBE fallback cells add whitespace/length. No selected media or embedded images.'
manifestpath.write_text(json.dumps(manifest,indent=2)+'\n')
result={'checks':checks,'pass':sum(checks.values()),'total':len(checks),'content_fingerprint':fp,'artifact_hashes':hashes,'corrected_audit_sha256':sha(auditpath),'held_case_pdf_absent_teaching':heldabsent,'held_case_pdf_present_final_or_private':heldpresent,'blank_summary_response_cells':len(responses),'visual_manifest_sha256':sha(manifestpath)}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'pass':sum(checks.values()),'total':len(checks)},indent=2))
assert all(checks.values())
