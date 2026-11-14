"""Independent qualitative solutions and mathematical geometry cross-check; reviewer evidence only."""
from pathlib import Path
import json, math
E=Path(__file__).parent;B=E.parents[2]
D=json.loads((B/'manuscripts/gensci_3_4.json').read_text());M=json.loads((B/'materials/gensci_3_4.json').read_text());P=json.loads((B/'blueprints/gensci_3_4.json').read_text());S=json.loads((B/'sources/gensci_3_4.json').read_text())
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
# Coordinates: right+x, up+y, out-of-page+z; conductor line along z.
field=(1,0,0);wire=(0,0,1)
vel={'stationary':(0,0,0),'parallel':(1,0,0),'up':(0,1,0),'down':(0,-1,0),'angled':(math.sqrt(.5),math.sqrt(.5),0)}
geom={k:dot(cross(v,field),wire) for k,v in vel.items()}
checks={
'zero_registry_intentional':len(M['calculations'])==0,
'15_distinct_GEM_cards': [c['id'] for c in M['items']]==[f'GEM{i}' for i in range(1,16)],
'15_lessons_numbered': [l['number'] for l in D['lessons']]==list(range(1,16)),
'all_40min':all(sum(l['minutes'])==40 for l in D['lessons']),
'final_5_10_10_10_5':D['lessons'][-1]['minutes']==[5,10,10,10,5],
'zero_stationary_parallel':geom['stationary']==geom['parallel']==0,
'up_down_reversal':geom['up']==-geom['down'],
'angled_smaller_nonzero':0<abs(geom['angled'])<abs(geom['up']),
'field_reversal_flips':dot(cross(vel['up'],(-1,0,0)),wire)==-geom['up'],
'double_reversal_restores':dot(cross(vel['down'],(-1,0,0)),wire)==geom['up'],
'd_only_lesson7': [l['number'] for l in D['lessons'] if 'd' in l['outcomes']]==[7],
'd_only_F7': [t['id'] for t in P['assessment_tasks'] if 'd' in t['outcomes']]==['F7'],
'final_4_sections_4_criteria':len(D['assessment']['sections'])==len(D['assessment']['rubric'])==4,
'final_excludes_d':set(D['lessons'][-1]['outcomes'])==set('abcef'),
'all_source_outcomes_mapped':set().union(*(set(l['outcomes']) for l in D['lessons']))=={o['id'] for o in S['outcomes']},
'blueprint_maps_consistent':all(p['lesson']==l['number'] and p['title']==l['title'] and p['outcomes']==l['outcomes'] and p['materials']==l['materials'] for p,l in zip(P['lesson_map'],D['lessons'])),
'rubric_links_complete':all(r['tasks']==[f'I{i}'] and r['criterion']==i for i,r in enumerate(P['rubric_links'],1)),
'provenance_unit_exact':all(D['unit'][k]==S[k] for k in ['coreCompetencies','values','pcis']),
'no_official_allocation':S['official_lesson_allocation'] is None,
}
solutions={
'GEM1':'Draw existing aligned-within-domain regions with mixed net directions before;field favours domain growth/reorientation;soft iron loses much magnetisation after removal but residual effects depend history. Model is not microscopy.',
'GEM2':'DC coil or nearby magnet aligns/responds to applied field;consistent pole/direction stroking provides directed magnetising influence;mechanical disturbance in a field can assist. No reliable polarity from unspecified hammering,or universal most suitable method;use control/material/retention criteria. Magnetic induction of iron differs from voltage induction.',
'GEM3':'Alternating diminishing field cycles toward low net remanence;appropriate heat or disturbance with external-field conditions can reduce order. Tapping in an aligning field can have opposite effect. No live methods provided;unperformed until separately approved.',
'GEM4':'Draw labelled N/S,noncrossing closed lines external N-to-S/internal S-to-N and tangent compass north end. Density qualitative under consistent convention. Optional real directions must be recorded at marked positions;Earth field can matter.',
'GEM5':'A unchanged configuration no induced emf;B changing linked flux yes;C appropriate moving open rod can separate charges/voltage without closed current;D changing separate-coil current can induce in stationary loop. Emf energy per charge,not mechanical force;input energy required.',
'GEM6':'Explicit vector calculation above:stationary/parallel zero,up/down equal opposite signs,angled smaller nonzero at equal speed. Active wire aligned with v-cross-B. Wiring maps physical polarity to meter-right arbitrarily.',
'GEM7':'Actual school no-external-power circuit,zero/sensitivity/geometry precheck,actual setup drawing,all4 movements,baseline/reversal/repeats,roles/date/directions/readings or undetectable results required. A supplied table does not count as outcome d. Return-lead movement can contribute;control it.',
'GEM8':'Given upward-right convention:field reversal alone left;both field/motion reversals restore right. This is a relative sign,not universal wiring. Moving lead contributes motional/flux change;fix return leads outside gap and compare controlled motion.',
'GEM9':'Greater relevant perpendicular speed,B,proper active length increase motional magnitude if other conditions fixed;additional linked turns affect separate coil model with same change per turn. Arbitrary length/turns insufficient. Qualitative data do not independently establish exact ratios,even when an ideal law predicts them.',
'GEM10':'Generator mechanical work converts to electrical energy through linked change;transformer changing electrical input transfers energy via changing field;induction heating uses induced dissipative currents. Steady primary current gives no continuing ideal secondary induction after transients. Bell primarily electromagnetic attraction plus feedback;switching self-induction does not make it a generator.',
'GEM11':'A domains already exist;B presence alone insufficient;C vector geometry matters;D energy must enter;E battery bell not generation. For each,uncertainty/qualification is material remanence,field/loop/circuit change,wire/lead geometry,input/losses,or contact/core/current details respectively. Generator with mechanical input or transformer with changing primary is valid daily example.',
'GEM12':'Series path supply-switch-contact-coil-return,mechanical armature-contact linkage opens when attracted,spring recloses as field falls. Soft core low retention aids release. Need both circuit AND mechanical drawings. Rated current-limited supply with compatible coil,insulation/stability/contacts approved before power;design alone no making evidence.',
'GEM13':'Approved disconnected assembly,teacher inspection,brief test ≤5s or shorter rating,disconnect/check before adjustment,record actual role/date/product/failure or cycle,power-off correction and approved retest. Correct diagnosis may be contact not opening/reclosing,insufficient permitted pull,wrong spacing or residual retention;never bypass safety to fix. No resources means plan-only status.',
'GEM14':'All4 claims fail:table not actual GEM7;drawing not actual GEM13;stationary magnet not energy source;hammering depends field/material/history and soft iron not reliably permanent. Two uses generator/transformer need mechanical/changing electrical inputs. New evidence opportunities require school approval.',
'GEM15_I1':'Two valid magnetisation and two conditional demagnetisation descriptions suffice as prompt asks;not all methods mandatory. Domain reasoning,low relative retention,hammering qualifications and complete field/compass model required.',
'GEM15_I2':'Four movement predictions/reversals as above,closed current path versus open voltage,actual GEM7 observation missing. Supplied meter responses not fabricated experimental records.',
'GEM15_I3':'All4 listed factors with appropriate straight-wire/coil distinction,held controls and orientation;given qualitative records do not show exact multipliers.',
'GEM15_I4':'One generator OR transformer explained with energy/change;bell core/current/feedback contrast;none of actual practical/project/digital actions established by writing.'}
result={'scope':'Independent full qualitative task/key solutions;no numerical curriculum registry or emf derivation required. Vector arithmetic is reviewer verification only.','geometry_coordinates':'B along+x;v in xy;active wire alongz;dot(v cross B,wire) verifies relative motional effect,not universal meter sign.','geometry_relative_coefficients':geom,'checks':checks,'pass':sum(checks.values()),'total':len(checks),'solutions':solutions,'teacher_judgments':['actual GEM7 circuit sensitivity/clearance/lead control and role throughput','rated coil/current limiting and contact/mechanical bell provision','actual source magnetisation/demagnetisation methods remain unperformed','digital resource navigation/action evidence absent until observed','sufficient additional setup/build time and accessible response modes']}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'pass':sum(checks.values()),'total':len(checks)},indent=2));assert all(checks.values())
