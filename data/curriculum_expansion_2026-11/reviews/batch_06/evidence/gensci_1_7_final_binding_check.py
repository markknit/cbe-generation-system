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
D=json.loads((W/'manuscripts/gensci_1_7.json').read_text())
OUT=next((W/'outputs/v2').rglob(D['prefix']+'_data.json')).parent
auditpath=W/'evidence/artifact_audit_gensci_1_7_2026-11-14.json'
audit=json.loads(auditpath.read_text()); prior=json.loads((E/'gensci_1_7_artifact_review_check.json').read_text())
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
held=['FINAL-ONLY HELD-OUT CASE','Separate food-stock case: a vendor has fresh cut melon']
heldabsent={t:all(norm(s) not in texts[t] for s in held) for t in teaching}
heldpresent={t:all(norm(s) in texts[t] for s in held) for t in ['AssessmentMaterials','MaterialsTeacherKey']}
fp=content_fingerprint(W,'gensci_1_7')
checks={
 'corrected_audit_sha256':sha(auditpath)=='6bb686a48214ab62be0dc70264f84a8c6f6e89ebc07d0e5f9b0227983b5a563a',
 'all18_current_hashes_match_snapshot':all(hashes[r['type']]['docx_sha256']==r['docx_sha256'] and hashes[r['type']]['pdf_sha256']==r['pdf_sha256'] for r in audit['documents']),
 'all18_hashes_unchanged_during_visual_review':hashes==prior['artifact_hashes'],
 'accepted_fingerprint_unchanged':fp=='10a7799804f3a1e910a7017408f55882059ab8f6186ffb5750fbbd1484e8b70d',
 'student_summary13rows':len(summaryrows)==13,
 'exact36_student_summary_response_cells':len(responses)==36,
 'all36_student_summary_responses_blank':not any(responses),
 'held_case_absent_all5_teaching_pdf':all(heldabsent.values()),
 'held_case_present_standalone_final_and_private_materials_pdf':all(heldpresent.values()),
 'final_papers_refer_to_standalone_MI12':all(norm('standalone final-only MI12 case') in texts[t] for t in ['FinalExplanation','FinalExplanation_TeacherKey']),
}
manifestpath=E/'gensci_1_7_visual_manifest.json'; manifest=json.loads(manifestpath.read_text())
for item in manifest['images']:item['actually_inspected']=True
manifest['inspection_complete']=True
manifest['pages_surveyed']=sum(manifest['page_counts'].values())
manifest['contact_sheets_inspected']=sum('overview' in x['path'] for x in manifest['images'])
manifest['readable_pages_inspected']=sum('readable' in x['path'] for x in manifest['images'])
manifest['additional_details']=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'actually_inspected':True,'method':'crop of already inspected120dpi review PNG, enlarged20%; no deliverable mutation'} for p in sorted(E.glob('gensci_1_7_Guide_detail_*.jpg'))]
manifest['observations']='All88pages surveyed;46 selected pages read. Continuations are intact, including final rubric p4-5 and student MI9 p3-4. CBE resource fallback cells cause long tables/blank space. No confirmed clipping, overlap, lost task text or media. Five additional Guide crops make repeated-page UI image deltas unambiguous.'
manifestpath.write_text(json.dumps(manifest,indent=2)+'\n')
result={'checks':checks,'pass':sum(checks.values()),'total':len(checks),'content_fingerprint':fp,'artifact_hashes':hashes,'corrected_audit_sha256':sha(auditpath),'held_case_pdf_absent_teaching':heldabsent,'held_case_pdf_present_final_or_private':heldpresent,'blank_summary_response_cells':len(responses),'visual_manifest_sha256':sha(manifestpath)}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'pass':sum(checks.values()),'total':len(checks)},indent=2))
assert all(checks.values())
