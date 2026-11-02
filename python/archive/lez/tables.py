import pandas as pd, numpy as np, pickle, json, sys
sys.path.insert(0,'/home/claude/lez')
T=pd.read_parquet('table.parquet')      # all 200 configs, filter = all
T2=pd.read_parquet('table2.parquet')    # 70 configs, with filters
F=pd.read_parquet('families.parquet')
out={}
r2=lambda x: None if pd.isna(x) else round(float(x),3)
# 1. entry models compared, on all levels together (union of groups → use 'ALL' groups median)
A=T[(T.held=='any')&(T.level.str.startswith('ALL'))&(T.o_n>=80)&(T.f_n>=15)]
g=A.groupby(['ltf','entry']).apply(lambda d: pd.Series({'level groups':d.level.nunique(),'median avg RR 2022–25':d.o_avg.median(),'median avg RR 2026':d.f_avg.median(),
   '% settings + in both':((d.o_avg>0)&(d.f_avg>0)).mean()*100,'best avg RR 2022–25':d.o_avg.max()})).reset_index()
out['entries']=g.round(3).to_dict('records')
# 2. level ranking (individual levels + groups), filter all, held any
L=F[(F['filter']=='all')&(F.held=='any')]
L=L.sort_values('both',ascending=False)
out['levels']=L[['ltf','level','entry','n_o','n_f','both','o_med','f_med','o_best']].assign(both=lambda d:(d.both*100).round(0)).round(3).to_dict('records')
# 3. filters (sessions / trend) for the 2 main families
Q=F[F.level.isin(['ALL UPG gaps','ALL PRO f boxes M15','ALL PRO f boxes H1','ALL session / range H-L','ALL break boxes CDL/CDS/LD/SD','ALL LEZ (any TF)'])&F.entry.isin(['M1 all','M3 · limit at box edge'])&(F.held=='any')]
out['filters']=Q[['ltf','level','entry','filter','n_o','n_f','both','o_med','f_med']].assign(both=lambda d:(d.both*100).round(0)).round(3).to_dict('records')
# 4. stops / exits: M1 all + M3, all PRO f + UPG + sessions groups, 5m and 1m, average over level groups
S=T[(T.held=='any')&(T.level.str.startswith('ALL'))&(T.entry.isin(['M1 all','M3 · limit at box edge']))&(T.o_n>=80)]
sx=S.groupby(['ltf','entry','stop','boxexit','target','trail']).agg(o=('o_avg','mean'),f=('f_avg','mean'),wr_o=('o_wr','mean')).reset_index()
out['exits']=sx.round(3).to_dict('records')
# 5. your model per level: M1 all, held, Sbox + box exit, RUN BE2 / TP5 / TP3 trailOpp
Y=T[(T.entry=='M1 all')&(T.held=='held')&(T.stop=='Sbox')&(T.boxexit=='+box exit')&(((T.target=='RUN')&(T.trail.isin(['BE2','trailOpp'])))|((T.target=='TP5')&(T.trail==''))|((T.target=='TP2')&(T.trail=='')))]
out['yours']=Y[['ltf','level','target','trail','o_n','o_wr','o_avg','o_pf','o_t','f_n','f_wr','f_avg','f_t']].round(3).to_dict('records')
# 6. retest types
RT=T[(T.held=='any')&(T.level.str.startswith('ALL'))&(T.entry.str.startswith('M1'))&(T.o_n>=60)]
rt=RT.groupby(['ltf','entry']).agg(n_o=('o_n','median'),o_med=('o_avg','median'),f_med=('f_avg','median'),both=('o_avg',lambda s:((s>0)&(RT.loc[s.index,'f_avg']>0)).mean()*100)).reset_index()
out['retest']=rt.round(3).to_dict('records')
# 7. foundations
out['found']=pd.read_parquet('found.parquet').round(2).to_dict('records')
# 8. strategies
S2=pd.read_parquet('strats.parquet'); out['strats']=S2.replace([np.inf],999).round(3).to_dict('records')
# runner distribution for M1 RUN trailOpp on all levels
json.dump(out,open('sheet.json','w'),default=str)
print({k:len(v) for k,v in out.items()})
