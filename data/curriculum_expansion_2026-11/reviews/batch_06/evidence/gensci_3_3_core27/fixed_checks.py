from pathlib import Path
from fractions import Fraction as F
import json,math
E=Path(__file__).resolve().parent;M=json.loads((Path.cwd()/'data/curriculum_expansion_2026-11/materials/gensci_3_3.json').read_text());C={};R={};q=lambda x:F(str(x))
def ck(k,v):C[k]=bool(v)
def periodic(tag,xs,ys,ts,amp,wantlambda,wantperiod):
 ds=[q(b)-q(a) for a,b in zip(xs,xs[1:])];dt=[q(b)-q(a) for a,b in zip(ts,ts[1:])];a=max(map(q,ys));lo=min(map(q,ys));lam=ds[0];T=dt[0];freq=1/T;v=lam/T
 R[tag]={'spatial_crests_m':xs,'displacement_extrema_m':ys,'temporal_crests_s':ts,'amplitude_m':float(a),'peak_to_peak_m':float(a-lo),'lambda_m':float(lam),'period_s':float(T),'frequency_Hz':float(freq),'derived_speed_m_s':float(v)}
 ck(tag+'_crest_intervals',all(d==q(wantlambda) for d in ds));ck(tag+'_time_intervals',all(t==q(wantperiod) for t in dt));ck(tag+'_amplitude',a==-lo==q(amp));ck(tag+'_peak_to_peak',a-lo==2*q(amp));ck(tag+'_equation',freq*lam==v)
periodic('GWV1',[.2,1,1.8],[.03,-.03],[0,.25,.50],.03,.8,.25);periodic('GWV13',[.1,.7,1.3],[.02,-.02],[0,.2,.4],.02,.6,.2)
for tag,v,f,lam in [('GWV2_initial',12,3,4),('GWV2_new',12,6,2),('GWV4_A',20,5,4),('GWV4_B',10,5,2),('GWV13_A',30,10,3),('GWV13_B',20,10,2)]:
 R[tag]={'speed_m_s':v,'frequency_Hz':f,'lambda_m':float(q(v)/q(f)),'period_s':float(1/q(f))};ck(tag+'_lambda',q(v)/q(f)==q(lam));ck(tag+'_period_frequency',1/q(f)*q(f)==1)
ck('GWV2_speed_fixed',R['GWV2_initial']['frequency_Hz']*R['GWV2_initial']['lambda_m']==R['GWV2_new']['frequency_Hz']*R['GWV2_new']['lambda_m']);ck('GWV4_frequency_period_fixed',R['GWV4_A']['frequency_Hz']==R['GWV4_B']['frequency_Hz'] and R['GWV4_A']['period_s']==R['GWV4_B']['period_s']);ck('GWV13_boundary_frequency_period_fixed',R['GWV13_A']['frequency_Hz']==R['GWV13_B']['frequency_Hz'] and R['GWV13_A']['period_s']==R['GWV13_B']['period_s'])
R['GWV3']={'speed_A_m_s':float(50*q(.4)),'frequency_B_Hz':float(q(340)/q(.85)),'wavelength_C_m':float(q(300)/(q(1.5)*1000)),'period_D_s':float(1/q(25)),'kHz_error_ratio':float((q(300)/q(1.5))/(q(300)/(q(1.5)*1000)))}
for k,w in [('speed_A_m_s',20),('frequency_B_Hz',400),('wavelength_C_m',.2),('period_D_s',.04),('kHz_error_ratio',1000)]:ck('GWV3_'+k,R['GWV3'][k]==w)
for tag,angle in [('GWV5',35),('GWV13',30)]:R[tag+'_reflection']={'incident_to_normal_deg':angle,'reflected_to_normal_deg':angle,'to_surface_deg':90-angle};ck(tag+'_normal_complement',R[tag+'_reflection']['reflected_to_normal_deg']+R[tag+'_reflection']['to_surface_deg']==90)
R['echoes']={'GWV6_oneway_m':float(q(340)*q(.4)/2),'GWV6_17m_roundtrip_s':float(2*q(17)/q(340)),'GWV13_oneway_m':float(q(340)*q(.3)/2)}
for k,w in [('GWV6_oneway_m',68),('GWV6_17m_roundtrip_s',.1),('GWV13_oneway_m',51)]:ck(k,R['echoes'][k]==w)
for name,lam,gap,w in [('GWV8_A',.85,.5,1.7),('GWV8_B',.085,.5,.17),('GWV13',.8,.4,2)]:R[name+'_ratio']=float(q(lam)/q(gap));ck(name+'_ratio',R[name+'_ratio']==w)
ck('GWV8_A_relative_spreading',R['GWV8_A_ratio']>R['GWV8_B_ratio']);R['conditional_refraction']={'D':'warmer/faster below;cooler/slower above;initial near-horizontal ray curves up','N':'cooler/slower below;warmer/faster above;initial near-horizontal ray curves down','limit':'temperature profiles supplied;no actual wind,weather,audibility measurement or clock-time universal law'}
expected=[4,.8,20,400,.2,.04,68,.1,1.7,.17,.6,5,3,3,2,51];ck('exact16registry',len(M['calculations'])==len(expected))
for c,w in zip(M['calculations'],expected):ck(c['id']+'_independent',math.isclose(c['expected'],w,rel_tol=1e-13,abs_tol=1e-13))
R['checks']=C;R['passed']=sum(C.values());R['total']=len(C);R['failed']=[k for k,v in C.items() if not v];R['method_limit']='Independent exact-rational quantities from raw spatial/time/boundary/echo/ratio records,not eval of registered expressions. Graphs/diagrams are learner-drawn tasks;no supplied graphic asset exists. Scientific explanations and actual-performance scope are reviewed separately.'
(E/'fixed_checks.json').write_text(json.dumps(R,indent=2)+'\n');print(json.dumps({k:R[k] for k in ['passed','total','failed']}))
