import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim2 import cfg_names2
from analyze2 import sess
from summ import groups_from, summarize
CN=cfg_names2()
STD={'max':CN.index(('Szone','+box exit','RUN','BE2')),'tp2':CN.index(('Szone','+box exit','TP2','')),'fix50':CN.index(('S50','','TP2','')),'tp3o':CN.index(('Szone','+box exit','TP3','trailOpp'))}
MOD={51:'O5 no close back inside for 1 candle → enter',52:'O5 no close back inside for 2 candles → enter',53:'O5 no close back inside for 3 candles → enter',55:'O5 no close back inside for 5 candles → enter',
     61:'O6 closed back inside (1st candle) → enter on the next BC out',62:'O6 closed back inside (≤2 candles) → next BC out',63:'O6 closed back inside (≤3 candles) → next BC out',65:'O6 closed back inside (≤5 candles) → next BC out'}
ALL=pickle.load(open('ofk_res.pkl','rb')); out=[]
for tf in ('1m','5m','15m','1h'):
    G={};RR={}
    for per in ('old','fresh'):
        E,R=ALL[(per,tf)]; E=E.reset_index(drop=True); E['row']=np.arange(len(E))
        grp={'CDL':['CDL','flips CDL/CDS','all breaks'],'CDS':['CDS','flips CDL/CDS','all breaks'],'LD':['LD','continuations LD/SD','all breaks'],'SD':['SD','continuations LD/SD','all breaks']}
        E['T']=E.typ.map(grp); E['F']=[['all',s] for s in sess(E.t)]
        X=E[['row','e','d','T','F']].copy(); X['M']=E.model.map(MOD).values
        for c in ('T','F'): X=X.explode(c)
        X['key']=(X['T']+'|'+X.M+'|all|'+X.F).astype('category')
        G[per]=groups_from(X[['key','row','e','d']]); RR[per]=R
    S=summarize(G['old'],G['fresh'],RR['old'],RR['fresh'],CN,STD,min_o=40,min_f=8); S['tf']=tf; out.append(S)
    pickle.dump(G,open(f'G5_{tf}.pkl','wb'))
S=pd.concat(out,ignore_index=True); k=S.key.str.split('|',expand=True); k.columns=['break','entry','backin','filter']
S=pd.concat([S,k],axis=1); S.to_parquet('table5.parquet')
pd.set_option('display.width',300); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',50)
c=['tf','break','entry','n_o','n_f','both','o_med','f_med','best_cfg','best_o_wr','best_o_avg','best_o_t','best_f_avg','best_f_t']
a=S[S['filter']=='all']
print(a[a['break']=='all breaks'][c].round(2).to_string())
print(a.sort_values('both',ascending=False)[c].head(25).round(2).to_string())
