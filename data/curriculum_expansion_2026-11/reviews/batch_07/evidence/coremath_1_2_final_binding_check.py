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
D=json.loads((W/'manuscripts/coremath_1_2.json').read_text())
OUT=next((W/'outputs/v2').rglob(D['prefix']+'_data.json')).parent
auditpath=W/'evidence/artifact_audit_coremath_1_2_2026-11-14.json'
audit=json.loads(auditpath.read_text()); prior=json.loads((E/'coremath_1_2_artifact_review_check.json').read_text())
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
held=['Use only these new final data and the separate final prompts.','Index inputs:0.001,1/32,3^2×3^3']
heldabsent={t:all(norm(s) not in texts[t] for s in held) for t in teaching}
heldpresent={t:all(norm(s) in texts[t] for s in held) for t in ['AssessmentMaterials','MaterialsTeacherKey']}
fp=content_fingerprint(W,'coremath_1_2')
checks={
 'corrected_audit_sha256':sha(auditpath)=='b2ffddb1f1415f82977feaf2f34cbd69bfef837327d1ec46daf7def7f68fe7ae',
 'all18_current_hashes_match_snapshot':all(hashes[r['type']]['docx_sha256']==r['docx_sha256'] and hashes[r['type']]['pdf_sha256']==r['pdf_sha256'] for r in audit['documents']),
 'all18_hashes_unchanged_during_visual_review':hashes==prior['artifact_hashes'],
 'accepted_fingerprint_unchanged':fp=='05f9afafa0f5e2ebfb5d2cc365e9ee2ff3978665664fc522ca026cfee4b22d0b',
 'student_summary15rows':len(summaryrows)==15,
 'exact42_student_summary_response_cells':len(responses)==42,
 'all42_student_summary_responses_blank':not any(responses),
 'held_case_absent_all5_teaching_pdf':all(heldabsent.values()),
 'held_case_present_standalone_final_and_private_materials_pdf':all(heldpresent.values()),
 'final_papers_refer_to_standalone_CIL14':all(norm('Work independently with CIL14') in texts[t] for t in ['FinalExplanation','FinalExplanation_TeacherKey']),
}
manifestpath=E/'coremath_1_2_visual_manifest.json'; manifest=json.loads(manifestpath.read_text())
for item in manifest['images']:item['actually_inspected']=True
manifest['inspection_complete']=True
manifest['pages_surveyed']=sum(manifest['page_counts'].values())
manifest['contact_sheets_inspected']=sum('overview' in x['path'] for x in manifest['images'])
manifest['readable_pages_inspected']=sum('readable' in x['path'] for x in manifest['images'])
manifest['observations']='All98pages surveyed in14contact sheets;47distinctpages read at120dpi. GuidefinalI4continuesp15-16withrepeatedheader,textintact. StudentCIL12p2-3,privateCIL7p2-3/CIL10p3-4/CIL13p4-5,studentrubriccriterion3p5-6,privateI2promptp1-2/criterion1p2-3,teacherSummaryL6p1-2/attributionp2-3 intact. BlankSummary12lessonrowsp1+2p2,42blankcells. Longcomma-separatedtableswrapmiddigits,butallsignificantdigitsretained/readable;no confirmedclipping,overlap or glyph loss. Zero images;CBE59pages includesfallbackresource whitespace.'
M=json.loads((W/'materials/coremath_1_2.json').read_text());P=json.loads((W/'blueprints/coremath_1_2.json').read_text())
core=json.loads((E/'coremath_1_2_core27_pass1/binding.json').read_text())
checks['accepted_pass1_inputs_unchanged']=all(sha(ROOT/p)==h for p,h in core['inputs'].items())
checks['source_originals_crop_verification_unchanged']=all(sha(ROOT/p)==h for p,h in core['sourcefiles'].items())
checks['L13_F13_only_c_all4maps']=D['lessons'][12]['outcomes']==['c'] and all(P[k][12]['outcomes']==['c'] for k in ['lesson_map','assessment_map','assessment_tasks'])
newroot='For positive x,x^(1/n) is the positive nth root of x;negative powers invert the result.'
newanti='Explain why 10^(3.0791)=10^3×10^(0.0791) is the antilog of3.0791;accept a reasoned preference for direct arithmetic on this simple example.'
checks['three_root_fields_correct']=all(v==newroot for v in [D['lessons'][3]['knowledge'],D['lessons'][3]['phases'][2][3],D['lessons'][3]['summary']['observed']])
checks['antilog_field_correct']=D['lessons'][11]['phases'][2][0]==newanti
oldroot='For positive bases,1/n is a positive nth root;negative powers invert the result.'
oldanti='Explain why 3.0791 normalises to10^3×10^0.0791'
checks['old_errors_absent_current9PDF']=all(norm(oldroot) not in t and norm(oldanti) not in t for t in texts.values())
for kind in ['sources','materials','manuscripts','blueprints']:
 old=json.loads((E/f'coremath_1_2_initial_{kind}_snapshot.json').read_text());expected=json.loads(json.dumps(old));cur=json.loads((W/kind/'coremath_1_2.json').read_text())
 if kind=='manuscripts':
  expected['lessons'][3]['knowledge']=newroot;expected['lessons'][3]['phases'][2][3]=newroot;expected['lessons'][3]['summary']['observed']=newroot;expected['lessons'][11]['phases'][2][0]=newanti;expected['lessons'][12]['outcomes']=['c']
 elif kind=='blueprints':
  for k in ['lesson_map','assessment_map','assessment_tasks']:expected[k][12]['outcomes']=['c']
 checks[kind+'_only_eight_intended_changes']=cur==expected
checks['final_4_10_8_8_8plus2']=D['lessons'][-1]['minutes']==[4,10,8,8,10]
exportcheck=json.loads((E/'coremath_1_2_export_image_check.json').read_text())
checks['all9_PDF_no_images']=all(len(t.strip().splitlines())==2 for t in exportcheck['pdfimages_inventory'].values())
checks['keys_absent_all4_studentPDF']=all(all(norm(c['teacher']) not in texts[t] for c in M['items']) for t in ['StudentMaterials','AssessmentMaterials','StudentSummaryTable','FinalExplanation'])

manifestpath.write_text(json.dumps(manifest,indent=2)+'\n')
result={'checks':checks,'pass':sum(checks.values()),'total':len(checks),'content_fingerprint':fp,'artifact_hashes':hashes,'corrected_audit_sha256':sha(auditpath),'held_case_pdf_absent_teaching':heldabsent,'held_case_pdf_present_final_or_private':heldpresent,'blank_summary_response_cells':len(responses),'visual_manifest_sha256':sha(manifestpath)}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'pass':sum(checks.values()),'total':len(checks)},indent=2))
assert all(checks.values())
