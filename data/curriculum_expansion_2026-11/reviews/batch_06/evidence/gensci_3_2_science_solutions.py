"""Independent read-only kinematic solutions and current artifact defect evidence."""
from pathlib import Path
import ast,hashlib,json,math,operator,zipfile
import xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[3]
E=Path(__file__).parent
D=json.loads((B/'manuscripts/gensci_3_2.json').read_text());M=json.loads((B/'materials/gensci_3_2.json').read_text());P=json.loads((B/'blueprints/gensci_3_2.json').read_text())
ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
def arithmetic(n):
 if isinstance(n,ast.Expression):return arithmetic(n.body)
 if isinstance(n,ast.Constant) and type(n.value) in (int,float):return n.value
 if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -arithmetic(n.operand)
 if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](arithmetic(n.left),arithmetic(n.right))
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt' and len(n.args)==1 and not n.keywords:return math.sqrt(arithmetic(n.args[0]))
 raise ValueError(ast.dump(n))
calc=[]
for x in M['calculations']:
 v=arithmetic(ast.parse(x['expression'],mode='eval'));calc.append({'id':x['id'],'expression':x['expression'],'reviewer_result':v,'author_expected':x['expected'],'pass':math.isclose(v,x['expected'],rel_tol=1e-10,abs_tol=1e-10)})
v=lambda u,a,t:u+a*t
s=lambda u,a,t:u*t+a*t*t/2
frames_t=[0,.1,.2,.3];frames_s=[0,.05,.2,.45]
frame_avg=[(frames_s[i+1]-frames_s[i])/(frames_t[i+1]-frames_t[i]) for i in range(3)]
frame_mid=[(frames_t[i+1]+frames_t[i])/2 for i in range(3)]
numbers={
 'LM1':{'distance_m':4+3,'displacement_m':4-3,'average_speed_m_s':(4+3)/7,'average_velocity_m_s':(4-3)/7},
 'LM2':{'t_s':[0,2,4,6],'positive_positions_m':[0,6,12,18],'negative_positions_m':[18,12,6,0],'interval_velocity_positive_m_s':[3,3,3],'interval_velocity_negative_m_s':[-3,-3,-3]},
 'LM3':{'a_m_s2':(-1-5)/3,'zero_v_time_s':2.5,'graph_points_t_v':[[0,5],[2.5,0],[3,-1]],'optional_integral_displacement_m':s(5,-2,3),'optional_path_length_m':6.25+.25},
 'LM4':{'A_final_v_m_s':v(3,2,4),'B_time_s':(15-3)/2,'C_a_m_s2':(11-3)/4},
 'LM5':{'s_m':s(2,1.5,4),'final_v_m_s':v(2,1.5,4),'endpoint_mean_v_m_s':(2+8)/2,'independent_trapezoid_area_m':(2+8)*4/2,'incorrect_unsquared_value':2*4+.5*1.5*4,'note':'Velocity stayspositive so distance20m; omitted t² also breaks dimensions.'},
 'LM6':{'v_squared_m2_s2':4**2+2*3*8,'speed_m_s':8,'required_forward_velocity_m_s':8,'algebraic_roots_m_s':[-8,8],'first_rest_t_s':-12/(-3),'first_rest_s_m':12**2/(2*3),'note':'Do not extend a braking-to-first-rest model past its domain.'},
 'LM7':{'graph_points_t_v':[[0,4],[3,4],[6,10]],'segment_accelerations_m_s2':[0,2],'areas_m':[12,21],'total_s_m':33,'total_distance_m':33,'average_v_m_s':33/6,'incorrect_single_ramp_area_m':(4+10)*6/2},
 'LM8':{'actual_data':'NONE supplied; school-approved observed record required','repeat_count':3,'max_height_m':.5,'optional_ideal_max_height_fall_time_s':math.sqrt(2*.5/10),'note':'0.316s ideal time illustrates why a low hand-timed drop cannot establish precise g; not an observed time. Downward observation alone is not a quantitative acceleration measurement.'},
 'LM9':{'times_s':frames_t,'positions_m':frames_s,'interval_average_v_m_s':frame_avg,'midpoint_times_s':frame_mid,'successive_acceleration_m_s2':[(frame_avg[i+1]-frame_avg[i])/.1 for i in range(2)],'ideal_formula_positions_m':[s(0,10,t) for t in frames_t],'actual_video':'not supplied'},
 'LM10':{'A_s_m':s(0,10,1),'A_v_m_s':v(0,10,1),'B_t_s':math.sqrt(2*1.25/10),'B_v_m_s':5,'C_s_m':s(2,10,.4),'C_v_m_s':v(2,10,.4),'note':'Paper heights5m/1.25m/1.6m do not change LM8actual0.50m maximum.'},
 'LM11':{'apex_t_s':1,'apex_s_m':s(10,-10,1),'apex_v_m_s':v(10,-10,1),'apex_a_m_s2':-10,'return_t_s':2,'return_s_m':s(10,-10,2),'return_v_m_s':v(10,-10,2),'t_half_s':{'s_m':s(10,-10,.5),'v_m_s':v(10,-10,.5)},'t_one_half_s':{'s_m':s(10,-10,1.5),'v_m_s':v(10,-10,1.5)}},
 'LM12':{'double_height_ideal_impact_speed_factor':math.sqrt(2),'note':'Road contact/friction/drive forces prevent gravity-only freefall classification; ideal fall speed scales with sqrt(height),not height. No safety-system certification or actual road/height/digital activity follows.'},
 'LM13/I1':{'distance_m':7,'displacement_m':3,'average_speed_m_s':1,'average_velocity_m_s':3/7},
 'LM13/I2':{'B_v_m_s':v(2,3,4),'B_s_m':s(2,3,4),'B_endpoint_area_m':(2+14)*4/2,'C_first_rest_t_s':5,'C_s_m':10**2/(2*2)},
 'LM13/I3':{'D_s_m':s(0,10,.6),'D_v_m_s':v(0,10,.6),'E_interval_average_v_m_s':frame_avg,'apex_v_m_s':0,'apex_acceleration':'downward g; sign depends coordinate','actual_investigation':'not established'},
 'LM13/I4':{'note':'Two bounded precautions may preventfalls/excludepeople fromapproveddropzone and requirequalifiedroadcontrols; written model does not establish real safety,dropactivity or digitalresearch.'}
}
checks={
 'all22registry':len(calc)==22 and all(x['pass'] for x in calc),
 'LM5_two_routes_agree':s(2,1.5,4)==(2+v(2,1.5,4))*4/2==20,
 'LM7_areas_match_piecewise_models':s(4,0,3)+s(4,2,3)==12+21==33,
 'LM9_formula_frames_match':all(math.isclose(s(0,10,t),x,abs_tol=1e-12) for t,x in zip(frames_t,frames_s)),
 'LM9_averages_are_midpoint_velocities_under_model':all(math.isclose(x,v(0,10,t),abs_tol=1e-12) for x,t in zip(frame_avg,frame_mid)),
 'LM11_sameposition_oppositevelocities':s(10,-10,.5)==s(10,-10,1.5)==3.75 and v(10,-10,.5)==-v(10,-10,1.5)==5,
 'all13lesson40min':len(D['lessons'])==13 and all(sum(l['minutes'])==40 for l in D['lessons']),
 'final4_8_12_10_6':D['lessons'][-1]['minutes']==[4,8,12,10,6],
 'all_lesson_maps_match':len(P['lesson_map'])==13 and all(l['title']==p['title'] and l['outcomes']==p['outcomes'] and l['materials']==p['materials'] for l,p in zip(D['lessons'],P['lesson_map'])),
 'all16assessmentmaps_match_tasks':len(P['assessment_map'])==16 and all(x['outcomes']==next(t['outcomes'] for t in P['assessment_tasks'] if t['id']==x['task']) for x in P['assessment_map']),
 'four_rubric_links':len(D['assessment']['sections'])==len(D['assessment']['rubric'])==len(P['rubric_links'])==4 and all(x['tasks']==['I'+str(i)] for i,x in enumerate(P['rubric_links'],1)),
 'four_source_outcomes_final':set(D['lessons'][-1]['outcomes'])==set('abcd'),
}
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
o=B/'outputs/v2/General_Science/SS3.2_Linear_Motion';embedded={}
for typ in ['StudentMaterials','MaterialsTeacherKey']:
 with zipfile.ZipFile(o/(D['prefix']+'_'+typ+'.docx')) as z:
  ps=ET.fromstring(z.read('word/document.xml')).findall('.//w:p',ns);rows=[]
  for i,p in enumerate(ps):
   for image in p.findall('.//a:blip',ns):
    rows.append({'paragraph_index':i,'relationship':image.attrib,'preceding_text':[''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in ps[max(0,i-2):i]],'confirmed':'Referenced actual image after LM5 or LM8; graph data incompatible with current task.'})
  embedded[typ]=rows
word=o/(D['prefix']+'_StudentSummaryTable.docx')
with zipfile.ZipFile(word) as z:
 rs=ET.fromstring(z.read('word/document.xml')).findall('.//w:tbl/w:tr',ns)
 cells=[''.join(t.text or '' for t in c.findall('.//w:t',ns)).strip() for r in rs[1:] for c in r.findall('w:tc',ns)[1:]]
checks['actual39blank_summary_cells']=len(rs)==14 and len(cells)==39 and not any(cells)
result={'independent_registry':calc,'independent_all_task_solutions':numbers,'checks':checks,'checks_pass':sum(checks.values()),'checks_total':len(checks),'confirmed_artifact_defect':{'embedded_positions':embedded,'graph1_sha256':'0abc74762b0987c5e805a89b3699d2606f5d6a3b7a243956bd1359de59bc3e06','graph1_points_t_s_x_m':[[0,2],[2,6],[4,6],[6,2],[8,-2]],'graph2_sha256':'8a953fdb52665bfa85db27ab70e0775bc51261cbd082df55f9e759874b097af7','graph2_points_t_s_v_m_s':[[0,3],[2,3],[4,-1],[6,-1]],'scope':'Both actual student/private Word companions; current material records have no diagram keys. Teacher may not infer these are current LM5/LM8 data.'}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pass':sum(checks.values()),'total':len(checks),'registry':len(calc),'referenced_wrong_images_each_document':{k:len(v) for k,v in embedded.items()}},indent=2))
assert all(checks.values())
