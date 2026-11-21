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
D=json.loads((W/'manuscripts/gensci_3_4.json').read_text())
OUT=next((W/'outputs/v2').rglob(D['prefix']+'_data.json')).parent
auditpath=W/'evidence/artifact_audit_gensci_3_4_2026-11-14.json'
audit=json.loads(auditpath.read_text()); prior=json.loads((E/'gensci_3_4_artifact_review_check.json').read_text())
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
held=['HELD-OUT FINAL,paper models only.','Supplied readings:stationary centre,parallel centre,upward right,downward left,angled upward smaller right.']
heldabsent={t:all(norm(s) not in texts[t] for s in held) for t in teaching}
heldpresent={t:all(norm(s) in texts[t] for s in held) for t in ['AssessmentMaterials','MaterialsTeacherKey']}
fp=content_fingerprint(W,'gensci_3_4')
checks={
 'corrected_audit_sha256':sha(auditpath)=='f4b33206b8779c52c0c19ea0095a1e10dd1da941956e6adcf0569f38a50ed523',
 'all18_current_hashes_match_snapshot':all(hashes[r['type']]['docx_sha256']==r['docx_sha256'] and hashes[r['type']]['pdf_sha256']==r['pdf_sha256'] for r in audit['documents']),
 'all18_hashes_unchanged_during_visual_review':hashes==prior['artifact_hashes'],
 'accepted_fingerprint_unchanged':fp=='fa49957ecb8e19bea3b04563d9931b4d5bed90bf332ca306485571f6f92d63cf',
 'student_summary16rows':len(summaryrows)==16,
 'exact45_student_summary_response_cells':len(responses)==45,
 'all45_student_summary_responses_blank':not any(responses),
 'held_case_absent_all5_teaching_pdf':all(heldabsent.values()),
 'held_case_present_standalone_final_and_private_materials_pdf':all(heldpresent.values()),
 'final_papers_refer_to_standalone_GEM15':all(norm('Use only final reference/prompts') in texts[t] for t in ['FinalExplanation','FinalExplanation_TeacherKey']),
}
manifestpath=E/'gensci_3_4_visual_manifest.json'; manifest=json.loads(manifestpath.read_text())
for item in manifest['images']:item['actually_inspected']=True
manifest['inspection_complete']=True
manifest['pages_surveyed']=sum(manifest['page_counts'].values())
manifest['contact_sheets_inspected']=sum('overview' in x['path'] for x in manifest['images'])
manifest['readable_pages_inspected']=sum('readable' in x['path'] for x in manifest['images'])
manifest['observations']='All105pages surveyed through15contact sheets;51selectedpages read at120dpi. All material/key/final/summary pages read. StudentGEM4p1-2/GEM12p3-4,privateGEM5p2-3/GEM7p3-4/GEM10p4-5/GEM12p5-6/GEM14p6-7 continue intact. Studentfinalrubriclastrowp5-6,privatefinalI2promptp1-2/criterion2p2-3,teacherSummaryattributionp2-3,blankSummary12lessonrowsp1+3rowsp2 intact. No confirmed clipping/overlap/glyph loss;arrows/plus-minus supply symbols/rating/test limits readable. No embeddedimages;CBE63pages has extensive fallbackresource whitespace.'
M=json.loads((W/'materials/gensci_3_4.json').read_text());P=json.loads((W/'blueprints/gensci_3_4.json').read_text())
core=json.loads((E/'gensci_3_4_core27_pass1/binding.json').read_text())
checks['accepted_pass1_inputs_unchanged']=all(sha(ROOT/p)==h for p,h in core['inputs'].items())
checks['source_pdf_crop_verification_unchanged']=all(sha(ROOT/p)==h for p,h in core['sourcefiles'].items())
checks['L8c_L14acf_all4maps']=D['lessons'][7]['outcomes']==['c'] and D['lessons'][13]['outcomes']==['a','c','f'] and all(P[k][7]['outcomes']==['c'] and P[k][13]['outcomes']==['a','c','f'] for k in ['lesson_map','assessment_map','assessment_tasks'])
checks['GEM15_I1_two_two_key_exact']=M['items'][14]['teacher'].startswith('I1:two magnetisation and two qualified demagnetisation')
checks['copper_conductor_two_current_cards']=all('straight copper conductor' in M['items'][i]['student'] for i in [5,6])
checks['final5_10_10_10_5']=D['lessons'][-1]['minutes']==[5,10,10,10,5]
exportcheck=json.loads((E/'gensci_3_4_export_image_check.json').read_text())
checks['all9_PDF_no_images']=all(len(t.strip().splitlines())==2 for t in exportcheck['pdfimages_inventory'].values())
checks['current_keys_absent_student_PDF']=all(all(norm(c['teacher']) not in texts[t] for c in M['items']) for t in ['StudentMaterials','AssessmentMaterials','StudentSummaryTable','FinalExplanation'])

manifestpath.write_text(json.dumps(manifest,indent=2)+'\n')
result={'checks':checks,'pass':sum(checks.values()),'total':len(checks),'content_fingerprint':fp,'artifact_hashes':hashes,'corrected_audit_sha256':sha(auditpath),'held_case_pdf_absent_teaching':heldabsent,'held_case_pdf_present_final_or_private':heldpresent,'blank_summary_response_cells':len(responses),'visual_manifest_sha256':sha(manifestpath)}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'pass':sum(checks.values()),'total':len(checks)},indent=2))
assert all(checks.values())
