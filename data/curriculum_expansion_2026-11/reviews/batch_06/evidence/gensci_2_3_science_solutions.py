"""Independent reviewer solutions; no author/output/pipeline mutations."""
from pathlib import Path
import ast, hashlib, json, operator, zipfile
import xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[3]
M=json.loads((B/'materials/gensci_2_3.json').read_text())
D=json.loads((B/'manuscripts/gensci_2_3.json').read_text())
P=json.loads((B/'blueprints/gensci_2_3.json').read_text())
ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul}
def arithmetic(n):
 if isinstance(n,ast.Expression):return arithmetic(n.body)
 if isinstance(n,ast.Constant) and type(n.value) in (int,float):return n.value
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -arithmetic(n.operand)
 if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](arithmetic(n.left),arithmetic(n.right))
 raise ValueError(ast.dump(n))
calc=[{'id':x['id'],'expression':x['expression'],'independent_result':arithmetic(ast.parse(x['expression'],mode='eval')),'author_expected':x['expected'],'pass':arithmetic(ast.parse(x['expression'],mode='eval'))==x['expected']} for x in M['calculations']]
# The first atom contributes dots; a chemically identical second atom contributes crosses.
# Pairs denote origins, not distinct types of electron. In water/ammonia N or O dots, H crosses.
molecules={
 'H2':{'electron_total':2,'bond_pairs':['H(dot)-H(cross)'],'lone_pairs':{},'drawn_electrons':2},
 'H2O':{'electron_total':8,'bond_pairs':['O(dot)-H(cross)','O(dot)-H(cross)'],'lone_pairs':{'O':['dot,dot','dot,dot']},'drawn_electrons':8},
 'O2':{'electron_total':12,'bond_pairs':['O(dot)-O(cross)','O(dot)-O(cross)'],'lone_pairs':{'O1':['dot,dot','dot,dot'],'O2':['cross,cross','cross,cross']},'drawn_electrons':12},
 'N2':{'electron_total':10,'bond_pairs':['N(dot)-N(cross)']*3,'lone_pairs':{'N1':['dot,dot'],'N2':['cross,cross']},'drawn_electrons':10},
 'I2':{'electron_total':14,'bond_pairs':['I(dot)-I(cross)'],'lone_pairs':{'I1':['dot,dot']*3,'I2':['cross,cross']*3},'drawn_electrons':14},
 'NH3':{'electron_total':8,'bond_pairs':['N(dot)-H(cross)']*3,'lone_pairs':{'N':['dot,dot']},'drawn_electrons':8},
 'NH4+':{'electron_total':8,'bond_pairs':['N(dot)-H(cross)']*3+['N(dot)-H(dot) donated pair'],'lone_pairs':{},'drawn_electrons':8,'overall_charge':1,'final_bonds_equivalent':True}
}
ionic={
 'NaCl':{'before':{'Na':1,'Cl':7},'transfer':[1],'after':['[Na]+ (emptied represented3rd shell; inner Ne core omitted)','[Cl:7dots+1cross]−'],'formula_ratio':'1:1','net_charge':1-1},
 'MgO':{'before':{'Mg':2,'O':6},'transfer':[2],'after':['[Mg]2+ (emptied represented3rd shell; inner Ne core omitted)','[O:6dots+2crosses]2−'],'formula_ratio':'1:1','net_charge':2-2},
 'MgF2':{'before':{'Mg':2,'F1':7,'F2':7},'transfer':[1,1],'after':['[Mg]2+ (inner shells omitted)','[F:7dots+1cross]−','[F:7dots+1cross]−'],'formula_ratio':'1:2','net_charge':2+2*(-1)}
}
solutions={
 'CB1':'NaCl ionic attraction; H2 covalent sharing; Al metallic collective bonding; water-to-water hydrogen bonding. H2/O2/N2/I2/diamond/graphite/Al are elements; water/NaCl/MgO/MgF2 compounds. Diagram limit may be size,energy,3D arrangement or absence of actual testing.',
 'CB2':'Use ionic records. Alternating +/− fragment continues in3D; NaCl formula gives ratio,not molecule. Attractive interactions extend beyond one partner. Solid ions fixed; molten ions carry current. Net charges zero.',
 'CB3':'Use molecule records: shared pairs1,2,2,3,1; O/N/I lone pairs per atom2,1,3. O2 Lewis model does not explain its magnetic behaviour; this task is a declared Lewis model. Boiling keeps ordinary molecular connectivity and overcomes intermolecular cohesion.',
 'CB4':'NH3:5+3=8,three bonding/one lone pair. H+ contributes no electrons. N pair donation N→H+ yields bracketed NH4+,5+4−1=8,four bonding pairs,charge+1. Final N–H bonds equivalent. Formal N charge+1 is not oxidation state−3.',
 'CB5':'Two bent water molecules: Oδ−,Hδ+; internal solid O–H connections and lone pairs,intermolecular O(lone pair)···H–O dashed attraction. Two I–I molecules have dispersion between molecules. All molecular examples have dispersion; water-like hydrogen bonding requires suitable donor/acceptor. No universal relative-strength ranking. Iodine boiling/sublimation separates molecules without normally breaking I–I.',
 'CB6':'Extended positive cores/delocalised electrons; attraction is collective. Solid Al electrical current has electronic carriers; molten salt ionic carriers. Electrons plus lattice vibrations transfer heat. Nondirectional collective bonding permits plastic deformation; core3+/three-electron picture is limited bookkeeping.',
 'CB7':'NaCl ionic,I2 molecular,diamond/graphite covalent networks,Al metallic. Graphite mobile electrons along sheets; diamond ordinary electrical insulator but good thermal conductor. Network bonding defeats universal low-melting-covalent shortcut; high melting alone cannot diagnose ionic bonding. Carbon phase changes require pressure context if developed beyond this qualitative school model.',
 'CB8':'NaCl~801C,Al~660C,water~0/100C near101kPa are supplied references,not measurements. Fair solubility design controls water volume,temp,mixing,time and distinguishes dissolving rate from saturation amount; quantitative solubility needs measured solute and equilibrium/saturation. Electrical design controls voltage,contacts,geometry,temp and solution concentration; ionic solution conducts much more than pure water. Thermal design controls dimensions,mass,initial/boundary temps,time/insulation with approved sensors/protocol; heat transfer rate is not identical to conductivity. No permission to operate apparatus. Optional actual room-temp known salt requires approved amounts/equipment/record and no tasting.',
 'CB9':'Diamond4-neighbour3Dnetwork strong/hard→abrasive. Graphite3-neighbour sheets with delocalised electrons conduct and weaker intersheet cohesion permits marking/sliding. Both carbon; neither simple molecule. Grade/geometry/product limits remain.',
 'CB10':'Al conducts heat and forms easily; low mass stems from density not bond label alone. Oxide surface/alloy/coating/manufacturer matter. Reject all-hobs/all-coatings-safe/any-cleaner claims; ask compatibility,care,condition,permitted uses. No medical or universal safety verdict.',
 'CB11':'A Al or graphite electron carriers subject contact/geometry; B diamond3Dhard network; C graphite sliding layers; D Al heat transfer/forming/lightweight subject manual. Reflection example: covalent graphite can conduct,unlike a bond-label-only assumption. No prices/certificates supplied.',
 'CB12':'Actual H2O(two O–H,bent) or O2(double) molecular product AND actual alternating NaCl fragment,labels,key,continuation and revision. A boundary fragment can have unequal visible counts; bulk stoichiometry1:1. Paper plan not construction; digital title/link/action only when actually navigated. Scrap connectors/small parts/accessibility require preview.',
 'CB13':'Draft benefit: heat transfer/formability. Manufacturer questions: hob/coating compatibility and cleaning/use limits. Care limit: follow actual manual; do not abrade/clean experimentally. Label draft/not delivered. Actual approved audience/date/feedback only if delivered; no behaviour-change or permanent-disposition inference.',
 'CB14/I1':'Use MgF2/water/NH4+ independent representations above; show charges,all requested pairs/donation/intermolecular dotted connection; origin labels do not make final ammonium bond different.',
 'CB14/I2':'MgF2 giant ionic,H2O molecular,diamond/graphite giant covalent,Al metallic. Molten MgF2 mobile ions; solid ordinary ion transport absent. Al/graphite electrons mobile; diamond ordinary mobile-carrier absence. Network diamond contradicts low-melting covalent generalisation qualitatively; no ordinary-pressure carbon melting experiment asserted.',
 'CB14/I3':'Contact Al or graphite with electronic-carrier explanation; abrasive diamond with 3D hard-network explanation; formable heat container Al with delocalised-electron/lattice heat transfer and malleability. Every use requires grade/product/manual/geometry constraint; no numerical cost possible.',
 'CB14/I4':'Bond-type-only rejection of graphite contact changes with layered/delocalised-electron structure. Size/connectors/boundary/scale in ball-stick diagrams are schematic. Written work proves none of actual model/property/virtual-lab/outreach performances.'
}
word=B/'outputs/v2/General_Science/SS2.3_Chemical_Bonding'/(D['prefix']+'_StudentSummaryTable.docx')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(word) as z:
 rows=ET.fromstring(z.read('word/document.xml')).findall('.//w:tbl/w:tr',ns)
 responses=[''.join(t.text or '' for t in cell.findall('.//w:t',ns)).strip() for row in rows[1:] for cell in row.findall('w:tc',ns)[1:]]
checks={
 'five_registry_answers_correct':all(x['pass'] for x in calc) and len(calc)==5,
 'molecular_counts_equal_drawn_pairs':all(x['electron_total']==x['drawn_electrons']==2*(len(x['bond_pairs'])+sum(len(v) for v in x['lone_pairs'].values())) for x in molecules.values()),
 'all_three_ionic_formula_charges_neutral':all(x['net_charge']==0 for x in ionic.values()),
 'all14_lessons40min':len(D['lessons'])==14 and all(sum(x['minutes'])==40 for x in D['lessons']),
 'final_minutes4_14_8_8_6':D['lessons'][-1]['minutes']==[4,14,8,8,6],
 'all_lesson_maps_match':all(l['outcomes']==p['outcomes'] and l['materials']==p['materials'] and l['title']==p['title'] for l,p in zip(D['lessons'],P['lesson_map'])),
 'all_six_outcomes_in_final':set(D['lessons'][-1]['outcomes'])==set('abcdef'),
 'four_rubric_links_match_sections':len(D['assessment']['sections'])==len(D['assessment']['rubric'])==len(P['rubric_links'])==4 and all(x['tasks']==['I'+str(i)] for i,x in enumerate(P['rubric_links'],1)),
 'all17_assessment_map_task_records_agree':len(P['assessment_map'])==17 and all(x['outcomes']==next(t['outcomes'] for t in P['assessment_tasks'] if t['id']==x['task']) for x in P['assessment_map']),
 'actual42_summary_cells_blank':len(rows)==15 and len(responses)==42 and not any(responses),
}
r={'independent_registry':calc,'reviewer_molecular_pair_representations':molecules,'reviewer_ionic_representations':ionic,'independent_task_solutions':solutions,'checks':checks,'pass':sum(checks.values()),'total':len(checks),'scope':'All14cards and4final sections solved; unregistered numerical/electron/property conditions included. No actual classroom performance certified.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':checks,'pass':sum(checks.values()),'total':len(checks)},indent=2))
assert all(checks.values())
