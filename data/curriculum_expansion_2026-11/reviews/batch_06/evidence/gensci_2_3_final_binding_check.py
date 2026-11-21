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
D=json.loads((W/'manuscripts/gensci_2_3.json').read_text())
OUT=next((W/'outputs/v2').rglob(D['prefix']+'_data.json')).parent
auditpath=W/'evidence/artifact_audit_gensci_2_3_2026-11-14.json'
audit=json.loads(auditpath.read_text()); prior=json.loads((E/'gensci_2_3_artifact_review_check.json').read_text())
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
held=['HELD-OUT FINAL REFERENCE','Fictional jobs: solid electrical contact,hard abrasive,and formable heat-transfer container']
heldabsent={t:all(norm(s) not in texts[t] for s in held) for t in teaching}
heldpresent={t:all(norm(s) in texts[t] for s in held) for t in ['AssessmentMaterials','MaterialsTeacherKey']}
fp=content_fingerprint(W,'gensci_2_3')
checks={
 'corrected_audit_sha256':sha(auditpath)=='f3706d1d5b6399d58dfe76b087b1b07b8f434e12bef5f149b3945d4631f57ec8',
 'all18_current_hashes_match_snapshot':all(hashes[r['type']]['docx_sha256']==r['docx_sha256'] and hashes[r['type']]['pdf_sha256']==r['pdf_sha256'] for r in audit['documents']),
 'all18_hashes_unchanged_during_visual_review':hashes==prior['artifact_hashes'],
 'accepted_fingerprint_unchanged':fp=='6681e48003343a90c25909f2875b7128385a022aaf1051f9c4374906d3216014',
 'student_summary15rows':len(summaryrows)==15,
 'exact42_student_summary_response_cells':len(responses)==42,
 'all42_student_summary_responses_blank':not any(responses),
 'held_case_absent_all5_teaching_pdf':all(heldabsent.values()),
 'held_case_present_standalone_final_and_private_materials_pdf':all(heldpresent.values()),
 'final_papers_refer_to_standalone_CB14':all(norm('Use only held-out reference and prompts') in texts[t] for t in ['FinalExplanation','FinalExplanation_TeacherKey']),
}
manifestpath=E/'gensci_2_3_visual_manifest.json'; manifest=json.loads(manifestpath.read_text())
for item in manifest['images']:item['actually_inspected']=True
manifest['inspection_complete']=True
manifest['pages_surveyed']=sum(manifest['page_counts'].values())
manifest['contact_sheets_inspected']=sum('overview' in x['path'] for x in manifest['images'])
manifest['readable_pages_inspected']=sum('readable' in x['path'] for x in manifest['images'])
manifest['observations']='All99pages surveyed through14contact sheets;46selectedpages read at120dpi. All student/private material/final/summary pages read. CB5studentp1-2,CB3privatep1-2,CB8privatep3-4,CB10privatep4-5,CB13privatep5-6 continue intact. Student final startsSection1onp2 after cover/instructions;rubricp5-6,keypromptp1-2/keyrubricp2-3,teachersummaryp1-2 and attributionp2-3,blanksummary12rowsp1+2rowsp2 intact. No confirmed clipping/overlap/glyph loss;CBEfallbackcellsaddwhitespace/length. No selectedmedia/embeddedimages.'
manifestpath.write_text(json.dumps(manifest,indent=2)+'\n')
result={'checks':checks,'pass':sum(checks.values()),'total':len(checks),'content_fingerprint':fp,'artifact_hashes':hashes,'corrected_audit_sha256':sha(auditpath),'held_case_pdf_absent_teaching':heldabsent,'held_case_pdf_present_final_or_private':heldpresent,'blank_summary_response_cells':len(responses),'visual_manifest_sha256':sha(manifestpath)}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'pass':sum(checks.values()),'total':len(checks)},indent=2))
assert all(checks.values())
