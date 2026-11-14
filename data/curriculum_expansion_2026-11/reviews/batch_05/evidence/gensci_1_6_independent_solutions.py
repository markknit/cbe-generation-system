"""Independent solutions transcribed from task inputs; no registry-expression evaluation."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
B=Path(__file__).resolve().parents[3];M=json.loads((B/'materials/gensci_1_6.json').read_text());D=json.loads((B/'manuscripts/gensci_1_6.json').read_text());P=json.loads((B/'blueprints/gensci_1_6.json').read_text());S=json.loads((B/'sources/gensci_1_6.json').read_text())
values={};extra={}
for label,counts,key in [('A',[8,9,7],'Apercent'),('B',[0,1,0],'Bpercent'),('C',[3,4,2],'Cpercent')]:
 per=[F(x*100,10) for x in counts];total=F(sum(counts)*100,30);values[key]=total
 extra[label]={'counts':counts,'total_germinated':sum(counts),'tray_percentages':[float(x) for x in per],'mean_percentage':float(sum(per)/3),'total_percentage':float(total),'tray_range_percentage_points':float(max(per)-min(per)),'n_independent_trays':3}
lengths=[0,0,1,3,5,6];days=[0,2,4,6,8,10]
for i in range(5):values['rate'+str(i)]=F(lengths[i+1]-lengths[i],days[i+1]-days[i])
values['rateall']=F(lengths[-1]-lengths[0],days[-1]-days[0]);values['finalM']=F((7+9+8)*100,30);values['finalD']=F((0+0+1)*100,30)
checks=[{'id':r['id'],'independent_fraction':str(values[r['id']]),'independent_value':float(values[r['id']]),'registry_expected':r['expected'],'pass':abs(float(values[r['id']])-r['expected'])<1e-12} for r in M['calculations']]
extra['unregistered']={'seeds_per_condition':30,'total_seeds':90,'total_replicate_environments':9,'A_minus_B_percentage_points':float(values['Apercent']-values['Bpercent']),'A_minus_C_percentage_points':float(values['Apercent']-values['Cpercent']),'FinalM_minus_D_percentage_points':float(values['finalM']-values['finalD']),'FinalM_tray_percentages':[70,90,80],'FinalD_tray_percentages':[0,0,10],'units':'Percentages use original ten-seed denominator per tray; length-change rates cm/day, not biomass rates. Equal seed counts make mean tray percentage equal pooled percentage; general unequal-count means require care.'}
structural={
'all_12_lessons_40_minutes':all(sum(l['minutes'])==40 for l in D['lessons']),
'all_8_source_outcomes':len(S['outcomes'])==8 and {o['id'] for o in S['outcomes']}==set('abcdefgh'),
'no_official_lesson_allocation':S['official_lesson_allocation'] is None,
'lesson_map_matches_manuscript':all(l['number']==p['lesson'] and l['title']==p['title'] and l['outcomes']==p['outcomes'] and l['materials']==p['materials'] for l,p in zip(D['lessons'],P['lesson_map'])),
'source_competencies_value_pci_verbatim_in_unit':all(S[k]==D['unit'][k] for k in ['coreCompetencies','values','pcis']),
'final_40_minute_sequence':D['lessons'][-1]['minutes']==[4,16,12,4,4],
'all_lesson_shared_safety_reflection_story_overview_identical':all(len({l[k] for l in D['lessons']})==1 for k in ['safety','reflection','story','overview','attitudes','aresKeywords'])}
solutions={
'GD1':'Water imbibition can swell a seed without new tissue. Irreversible division/expansion versus differentiation/maturity; elongation can coexist with reserve respiration and declining entire-seedling dry mass. Length does not establish health or biomass.',
'GD2':'Viable intrinsic dormant block versus viable quiescence because external conditions lack versus nonviability. Impermeable coat/conceptual scarification, physiological dormancy/species-appropriate stratification or after-ripening, immature embryo/maturation are qualified cases. Seven days without emergence does not distinguish them. No pupil treatments.',
'GD3':'A/B water comparison; A/C recorded temperature comparison with matched moisture; same lot/random allocation/three independent trays of ten each. Ventilation is shared, no isolated oxygen trial; light held comparable, not tested. Radicle >=2 mm is a declared local criterion, not every species universal definition. Teacher packet window and daily observations, not fixed predicted temperature outcome.',
'GD4':'Nine actual labelled replicate trays/90 seeds and actual daily raw record with temperature, moisture/water addition, new and cumulative counts, missingness and observer. Adult between-lesson oversight and mould isolation/disposal; learner named actions require observation, not a group plan.',
'GD5':'A 80/90/70%, pooled and mean80%; B0/10/0%, pooled and mean10/3%; C30/40/20%, pooled and mean30%. A-B=230/3 percentage points, A-C50. Three tray replicates per condition; seeds are nested. Small B count is not proof water unnecessary. Actual results cannot be manufactured from these fictional values.',
'GD6':'Phaseolus vulgaris usually epigeal: hypocotyl raises cotyledonary node above marked soil; Pisum sativum hypogeal: epicotyl extends with cotyledons below. Cotyledons are seed leaves distinct from first true leaves. Dates/stages/actual visible landmarks required; unresolved marked not seen. A supplied model is not performed observation.',
'GD7':'Apical primary extension/new primary tissues; lateral secondary girth. Typical woody vascular cambium secondary xylem inward/phloem outward; cork cambium protective periderm. Primary and secondary coexist in different regions/stages. Typical many eudicots/gymnosperms, not universal stems/plants; seasonal rings need suitable context.',
'GD8':'Interval cm/day rates0,0.5,1,1,0.5; overall0.6. Water/oxygen/suitable temperature and species-specific light for germination; reserves initially supply resources; later photosynthesis/light and external mineral supply matter. Longer etiolated shoot is not higher biomass/health. No universal more heat/fertilizer benefit.',
'GD9':'Auxin shoot elongation/tropism, gibberellins suitable germination/stem elongation, cytokinins division/shoot context, ABA dormancy/stomatal closure, ethylene ripening/abscission. These are representative roles with dose/tissue/species/stage/interacting-hormone qualifications, not one-to-one universal accelerators; no application.',
'GD10':'Require all three distinct growth/development, species-specific dormancy, hormone claims with evidence/limits, followed by one useful qualified benefit. Print evidence is reasoning, observed digital search/view/save separately documented. No personal upload/login/download/contact.',
'GD11':'All eight claims are false: swelling != new tissue; nonemergence != dormancy; waterlogging confounded; bean species differ; primary+secondary coexist; seed reserves/species light; hormones context dependent; reading != performed action. Useful establishment/monitoring decision must state a mechanism and limit.',
'GD12_I1_I2':'FinalM70/90/80%=80%; FinalD0/0/10%=10/3%; difference230/3 percentage points. Matched lot/count/tray/light/time/room temperature, replicate/raw daily checks; no cooler group and no independent temperature/light/oxygen conclusion. Bean/pea classifications and regions as GD6; supplied descriptions cannot certify actual comparison.',
'I3':'Typical apical length versus lateral girth and xylem inward/phloem outward; at least two stage-qualified resource/environment factors; all five hormones with roles and interaction/context limit.',
'I4':'Specific species-aware establishment/timing/monitoring benefit with condition/measurement limit; actual named setup/count/moisture/temp/record/check plus multi-day logs F4/F5, actual dated specimen/sketch/check F6. Written data/long shoot alone insufficient; appreciation response does not prove lasting disposition.'}
r={'scope':'Independent numerical and case solutions; inputs read from student prompts, values calculated independently without evaluating registry expressions','registry_checks':checks,'registry_total':len(checks),'registry_pass':sum(c['pass'] for c in checks),'additional_calculations':extra,'structural_checks':structural,'task_solutions':solutions}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'registry_total':len(checks),'registry_pass':sum(c['pass'] for c in checks),'structural_checks':structural,'evidence_sha256':hashlib.sha256(Path(__file__).with_suffix('.json').read_bytes()).hexdigest()},indent=2))
assert all(c['pass'] for c in checks) and all(structural.values())
