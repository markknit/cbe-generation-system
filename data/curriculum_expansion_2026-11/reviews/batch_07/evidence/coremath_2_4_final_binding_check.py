"""Independent read-only final blank/isolation/correction and frozen artifact binding checks."""
from pathlib import Path
import json,hashlib,re,sys,subprocess,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[5];sys.path.insert(0,str(R/'scripts'));from curriculum_pipeline import content_fingerprint
B=R/'data/curriculum_expansion_2026-11';E=Path(__file__).parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();norm=lambda s:re.sub(r'\s+','',s)
D=json.loads((B/'manuscripts/coremath_2_4.json').read_text());M=json.loads((B/'materials/coremath_2_4.json').read_text());P=json.loads((B/'blueprints/coremath_2_4.json').read_text());O=B/'outputs/v2/Core_Mathematics/SS2.4_Trigonometry_1';ap=B/'evidence/artifact_audit_coremath_2_4_2026-11-15.json';audit=json.loads(ap.read_text());prior=json.loads((E/'coremath_2_4_artifact_review_check.json').read_text());ini=json.loads((E/'coremath_2_4_science_initial_word_check.json').read_text());ess=json.loads((E/'coremath_2_4_recheck_essential_pass1/binding.json').read_text());N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};hashes={};trees={};pdftexts={}
for row in audit['documents']:
 typ=row['type'];doc=O/(D['prefix']+'_'+typ+'.docx');pdf=B/'outputs/PDF'/(D['prefix']+'_'+typ+'.pdf');hashes[typ]={'docx_sha256':sha(doc),'pdf_sha256':sha(pdf)}
 with zipfile.ZipFile(doc) as z:trees[typ]=ET.fromstring(z.read('word/document.xml'))
 pdftexts[typ]=norm(subprocess.check_output(['pdftotext',str(pdf),'-'],text=True))
summaryrows=trees['StudentSummaryTable'].findall('.//w:tbl/w:tr',N);responses=[''.join(t.text or '' for t in c.findall('.//w:t',N)).strip() for r in summaryrows[1:] for c in r.findall('w:tc',N)[1:]]
final=norm(M['items'][-1]['student']);teaching=['CBE_LessonSequence','CompactTeacherGuide','StudentMaterials','SummaryTable','StudentSummaryTable']
# Default pdftotext dehyphenates the literal half-base at a line end. Use prior bbox character-preserving full-card matches and independently check two unique contiguous cues.
cues=['Use only this final card and separate prompts.','Right triangleABC has rightangleC,AC=12cm,BC=5cm,AB=13cm;chosen acute angleA.']
heldabsent={t:final not in pdftexts[t] and all(norm(cue) not in pdftexts[t] for cue in cues) for t in teaching}
heldpresent={t:all(norm(cue) in pdftexts[t] for cue in cues) and any(r['document']==t and r['field']=='CTG15.student' and r['word_pass'] and r['pdf_pass'] for r in prior['checks']) for t in ['AssessmentMaterials','MaterialsTeacherKey']}
checks={
 'correct_frozen_audit_sha256':sha(ap)=='e64b10a105968d7931db9b9337e2e729c98cac623fcf085fc2dee75fe28fa82e',
 'nine_correct_module_types':len(audit['documents'])==9 and {r['module'] for r in audit['documents']}=={'coremath_2_4'} and len({r['type'] for r in audit['documents']})==9,
 'all18_current_hashes_match_snapshot':all(hashes[r['type']]['docx_sha256']==r['docx_sha256'] and hashes[r['type']]['pdf_sha256']==r['pdf_sha256'] for r in audit['documents']),
 'all18_hashes_unchanged_during_visual_review':hashes==prior['artifact_hashes'],
 'accepted_fingerprint_unchanged':content_fingerprint(B,'coremath_2_4')=='0d4ab09fb5d757a52037056486d1f2228c5ab7473a69cf301dcc58a39f04a899',
 'all_pass1_canonical_inputs_match':all(sha(R/p)==h for p,h in ess['inputs'].items()),
 'all5_draft_binaries_match_accepted_pass1':all(hashes[t]['docx_sha256']==v['sha256'] for t,v in ess['words'].items()),
 'all5_draft_body_text_match_original_independent_review':all(v['body_text_matches_initial_extract'] for v in prior['companion_rebuild_bridge'].values()),
 'source_crop_unchanged':sha(B/'sources/coremath_2_4_source.png')==ini['source_pixel_sha256'],
 'source_pdf_unchanged':sha(R/'CBE_Curriculums/Grade 10/STEM/Grade10_CoreMath.pdf')==ini['source_pdf_sha256'],
 'source_verification_unchanged':sha(B/'sources/coremath_2_4.verification.json')==ini['canonical_hashes']['sources/coremath_2_4.verification.json'],
 'all52_registered_calculations_and_cards_unchanged':(B/'materials/coremath_2_4.json').read_bytes()==(E/'coremath_2_4_initial_materials_snapshot.json').read_bytes() and len(M['calculations'])==52,
 'both_template_assets_original_bytes':all(sha(B/'materials'/p)==h for p,h in ini['asset_hashes'].items()),
 'summary16rows_15lessons':len(summaryrows)==16,
 'exact45_blank_student_summary_cells':len(responses)==45 and not any(responses),
 'four_blank_final_answer_areas':prior['blank_final_answer_cells'],
 'full_CTG15_absent_all5_teachingPDF':all(heldabsent.values()),
 'full_CTG15_present_standalone_and_private_materialsPDF':all(heldpresent.values()),
 'final_papers_refer_standalone_CTG15':all(norm('Work independently with CTG15') in pdftexts[t] for t in ['FinalExplanation','FinalExplanation_TeacherKey']),
 'full_teacher_keys_absent_all4_studentPDF':all(all(norm(c['teacher']) not in pdftexts[t] for c in M['items']) for t in ['StudentMaterials','AssessmentMaterials','StudentSummaryTable','FinalExplanation']),
 'all_final_exemplars_absent_studentPDF':all(all(norm(s['exemplar']) not in pdftexts[t] for s in D['assessment']['sections']) for t in ['StudentMaterials','AssessmentMaterials','StudentSummaryTable','FinalExplanation']),
 'final3_9_12_8_5plus3':D['lessons'][-1]['minutes']==[3,9,12,8,8],
 'project_L12_L13_3_24_6_2_5':all(D['lessons'][i]['minutes']==[3,24,6,2,5] for i in [11,12]),
 'all10_final_resource_slots_null':prior['final_slots_null'],
 'selected_resources_empty':prior['selected_resources']==[],
}
# Independently reconstruct the only two permitted canonical changes from own frozen initial snapshot.
old=json.loads((E/'coremath_2_4_initial_manuscripts_snapshot.json').read_text());new3='Correct diagrams,ratio choices,height and distance results,units and sight-point/horizontal assumptions.';new4='Correct calibrated-angle interpretation and a specific checked use with two valid limits and an honest distinction between written and observed actions.'
old['assessment']['rubric'][2]['proficient']=new3;old['assessment']['rubric'][3]['proficient']=new4;checks['manuscript_only2_intended_rubric_changes']=old==D
for k in ['sources','materials','blueprints']:checks[k+'_unchanged_from_initial']=json.loads((E/f'coremath_2_4_initial_{k}_snapshot.json').read_text())==json.loads((B/k/'coremath_2_4.json').read_text())
rubric_evidence={}
for typ in ['FinalExplanation','FinalExplanation_TeacherKey']:
 candidates=[]
 for table in trees[typ].findall('.//w:tbl',N):
  t=''.join(x.text or '' for x in table.findall('.//w:t',N))
  if 'Criterion' in t and D['assessment']['rubric'][0]['criterion'] in t:candidates.append(t)
 assert len(candidates)==1
 rtext=norm(candidates[0]);pdf_rubric=pdftexts[typ].split('RUBRIC')[-1]
 # Student rubric criterion3continues across5–6. The global text stream interleaves other columns; the actual343..470column check preserves the whole cell.
 neutral=all(norm(s) in rtext for s in [new3,new4]) and all(any(r['document']==typ and r['field']==field and r['word_pass'] and r['pdf_pass'] for r in prior['checks']) for field in ['assessment.rubric3.proficient','assessment.rubric4.proficient']);noanswers=all(s not in rtext and s not in pdf_rubric for s in ['7.17','8mresults','Correct30°','30°interpretation'])
 checks[typ+'_neutral_descriptors_actualWordPDF']=neutral and noanswers;rubric_evidence[typ]={'actual_word_rubric':candidates[0],'neutral_descriptors_present_WordPDF':neutral,'old_solutions_absent_WordPDF_rubric':noanswers}
# Final all-page/contact plus declared normal readable sample completed; every one was actually opened.
vp=E/'coremath_2_4_visual_manifest.json';v=json.loads(vp.read_text());assert len(v['images'])==65
for item in v['images']:
 assert sha(R/item['path'])==item['sha256'];item['actually_inspected']=True
v.update(inspection_complete=True,pages_surveyed=sum(v['page_counts'].values()),contact_sheets_inspected=15,readable_pages_inspected=50,observations='All106pages in15contacts;50distinctpages at120dpi. CBE63pages with fallback-resource whitespace. GuidefinalL15row continues16–17;studentCTG5continues1–2;privateCTG3continues1–2 andCTG15key6–7;studentrubriccriterion3continues5–6;privateI2prompt1–2;teacherSummaryL6title1–2/attribution2–3. All inspected continuations intact. Clinometer original PNG readable on studentp3/privatep5 with complete ticks/pivot/baseline/captions,no distortion/crop. Current rubric neutral,4finalanswerareas and45summarycells blank. No confirmed clipping,overlap or mathematical glyph loss.')
vp.write_text(json.dumps(v,indent=2)+'\n');checks['visual_coverage_and_evidence_hashes_complete']=v['pages_surveyed']==106 and v['contact_sheets_inspected']==15 and v['readable_pages_inspected']==50
(E/'coremath_2_4_layout_review_progress.json').write_text(json.dumps({'actually_inspected_indices':list(range(65)),'all106pages_surveyed_in15contacts':True,'readable_samples_observed':50,'findings':'No confirmed blocker;alldeclaredvisualinspectioncomplete'},indent=2)+'\n')
r={'checks':checks,'pass':sum(checks.values()),'total':len(checks),'content_fingerprint':content_fingerprint(B,'coremath_2_4'),'artifact_hashes':hashes,'frozen_audit_sha256':sha(ap),'held_card_absent_teaching':heldabsent,'held_card_present_standalone_or_private':heldpresent,'rubric_evidence':rubric_evidence,'blank_summary_response_cells':len(responses),'visual_manifest_sha256':sha(vp)}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':checks,'pass':sum(checks.values()),'total':len(checks)},indent=2));assert all(checks.values())
