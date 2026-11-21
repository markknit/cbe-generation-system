from fractions import Fraction as Q
from pathlib import Path
import json,math
E=Path(__file__).resolve().parent;M=json.loads((Path.cwd()/'data/curriculum_expansion_2026-11/materials/gensci_3_1.json').read_text());C={};R={}
q=lambda x:Q(str(x))
def ck(k,v):C[k]=bool(v)
def moment(forces,pivot=(0,0)):
 px,py=map(q,pivot);return sum((q(x)-px)*q(fy)-(q(y)-py)*q(fx) for x,y,fx,fy in forces)
def resultant(forces):return [sum(q(r[i]) for r in forces) for i in [2,3]]
def record(forces,pivot=(0,0)):return {'forces_xy_FxFy':forces,'pivot':pivot,'moment_exact_Nm':str(moment(forces,pivot)),'moment_Nm':float(moment(forces,pivot)),'resultant_N':[float(x) for x in resultant(forces)]}
R['TF1']={'down':record([[.30,0,0,-10]]),'line_through_pivot':record([[.30,0,10,0]]),'slant_magnitude_Nm':float(q(10)*q(.18)),'slant_turning_sense':'undetermined without force-arrow direction'}
ck('TF1_down',moment([[.30,0,0,-10]])==-3);ck('TF1_linezero',moment([[.30,0,10,0]])==0);ck('TF1_slant',q(10)*q(.18)==q(1.8));ck('TF1_slant_geometry_feasible',0<q(.18)<=q(.30))
R['TF2']={'A_Nm':float(12*q(25)/100),'B_N':float(q(2.4)/q(.4)),'C_m':float(q(1.8)/6)}
for k,x,y in [('A',12*q(25)/100,3),('B',q(2.4)/q(.4),6),('C',q(1.8)/6,q(.3))]:ck('TF2_'+k,x==y)
forces={'A':[.2,0,0,-4],'B':[-.2,0,0,-4],'C':[.4,0,0,3],'D':[-.4,0,0,3]};R['TF3']={k:record([v]) for k,v in forces.items()};R['TF3']['ABC']=record([forces[k] for k in 'ABC'])
for k,v in zip('ABCD',[-.8,.8,1.2,-1.2]):ck('TF3_'+k,moment([forces[k]])==q(v))
ck('TF3_ABC_moment',moment([forces[k] for k in 'ABC'])==q(1.2));ck('TF3_ABC_resultant',resultant([forces[k] for k in 'ABC'])==[0,-5])
# Determine downward unknown using algebraic moment balance, then all-force reaction.
for name,left,xright,weight in [('TF4_weightless',[-.3,0,0,-2],.2,None),('TF4_weighted',[-.3,0,0,-2],.2,[.1,0,0,-1]),('TF12_D',[-.25,0,0,-2],.1,None)]:
 known=[left]+([weight] if weight else []);F=moment(known)/q(xright);reaction=F-resultant(known)[1];allforces=known+[[xright,0,0,float(-F)],[0,0,0,float(reaction)]];R[name]={**record(allforces),'unknown_downward_N':float(F),'upward_reaction_N':float(reaction)}
 ck(name+'_momentzero',moment(allforces)==0);ck(name+'_forcezero',resultant(allforces)==[0,0])
for name,f,r in [('TF4_weightless',3,5),('TF4_weighted',2.5,5.5),('TF12_D',5,7)]:ck(name+'_F',R[name]['unknown_downward_N']==f);ck(name+'_reaction',R[name]['upward_reaction_N']==r)
R['TF5']={'first_predicted_1N_distance_m':float(q(.5)*q(.2)/1),'first_each_magnitude_Nm':float(q(.5)*q(.2)),'second_each_magnitude_Nm':float(q(.5)*q(.15))};ck('TF5_distance',R['TF5']['first_predicted_1N_distance_m']==.1);ck('TF5_firstmoment',R['TF5']['first_each_magnitude_Nm']==.1);ck('TF5_secondmoment',R['TF5']['second_each_magnitude_Nm']==.075)
for name,fs,want in [('TF6_T1',[[-.2,0,0,-.5],[.1,0,0,-1]],0),('TF6_T2',[[-.15,0,0,-.5],[.16,0,0,-.5]],-.005)]:
 R[name]=record(fs);R[name]['separate_moments_Nm']=[float(moment([r])) for r in fs];ck(name+'_sum',moment(fs)==q(want))
# Compute signed contributions about both pivots and explicitly derive translation law.
pairs=[('TF7',[[-.2,0,0,-6],[.2,0,0,6]],2.4,2.4,0),('TF8',[[-.2,0,0,-4],[.2,0,0,6]],2,3,2),('TF12_B',[[-.3,0,0,-5],[.1,0,0,5]],2,2,0),('TF12_C',[[-.2,0,0,-3],[.1,0,0,5]],1.1,2.1,2)]
for name,fs,mo,mp,fy in pairs:
 R[name]={'O':record(fs),'P':record(fs,(-.5,0)),'separate_O':[float(moment([r])) for r in fs],'separate_P':[float(moment([r],(-.5,0))) for r in fs]}
 ck(name+'_O',moment(fs)==q(mo));ck(name+'_P',moment(fs,(-.5,0))==q(mp));ck(name+'_resultant',resultant(fs)==[0,q(fy)])
 for p in [-2,-.5,0,.25,1]:ck(name+'_translation_'+str(p),moment(fs,(p,0))==moment(fs)-q(p)*resultant(fs)[1])
 if fy==0:ck(name+'_couple_Fseparation',moment(fs)==q(fs[1][3])*(q(fs[1][0])-q(fs[0][0])))
 else:ck(name+'_pivot_dependence',moment(fs)!=moment(fs,(-.5,0)))
R['TF9']={'door_short_N':float(8/q(.2)),'door_long_N':float(8/q(.8)),'wrench_N':float(6/q(.3))}
for k,w in [('door_short_N',40),('door_long_N',10),('wrench_N',20)]:ck('TF9_'+k,R['TF9'][k]==w)
R['TF12_A']={'down':record([[.24,0,0,-10]]),'line_through_pivot_moment':0,'slant_magnitude_Nm':float(12*q(.15)),'slant_turning_sense':'undetermined'};ck('TF12_A_down',moment([[.24,0,0,-10]])==q(-2.4));ck('TF12_A_slant',12*q(.15)==q(1.8));R['TF12_door_N']=float(6/q(.75));ck('TF12_door',R['TF12_door_N']==8)
expected=[3,1.8,3,6,3,2.5,-.005,2.4,2.4,2,3,40,10,-2.4,2,2,1.1,5,8];ck('exact19registry',len(M['calculations'])==len(expected))
for r,x in zip(M['calculations'],expected):ck(r['id']+'_independent',math.isclose(r['expected'],x,rel_tol=1e-12,abs_tol=1e-12))
R['checks']=C;R['passed']=sum(C.values());R['total']=len(C);R['failed']=[k for k,v in C.items() if not v];R['method_limit']='Independent r_xF_y-r_yF_x signed sums using exact rational arithmetic, actual record data, force balance and pivot-translation identity; no actual demonstration, tool operation or supplied diagram asset exists. Written keys checked manually against these derivations.'
(E/'fixed_checks.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps({k:R[k] for k in ['passed','total','failed']}))
