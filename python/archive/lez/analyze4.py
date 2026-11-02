import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim2 import cfg_names2
from analyze2 import sess
from summ import groups_from, summarize
CN=cfg_names2()
STD={'max':CN.index(('Szone','+box exit','RUN','BE2')),'tp2':CN.index(('Szone','+box exit','TP2','')),'fix50':CN.index(('S50','','TP2','')),'tp3o':CN.index(('Szone','+box exit','TP3','trailOpp'))}
MOD={1:'O1 break close → next open',2:'O2 retest of the broken box (limit)',3:'O3 retest of the new T# (limit)',4:'O4 retest of the LEZ (limit)',
     12:'O2v broken box, after a 2nd BC',13:'O3v new T#, after a 2nd BC',14:'O4v LEZ, after a 2nd BC'}
ALL=pickle.load(open('of_res.pkl','rb')); out=[]
for tf in ('1m','5m','15m','1h'):
    G={};RR={}
    for per in ('old','fresh'):
        E,R=ALL[(per,tf)]; E=E.reset_index(drop=True); E['row']=np.arange(len(E))
        grp={'CDL':['CDL','flips CDL/CDS','all breaks'],'CDS':['CDS','flips CDL/CDS','all breaks'],'LD':['LD','continuations LD/SD','all breaks'],'SD':['SD','continuations LD/SD','all breaks']}
        E['T']=E.typ.map(grp)
        E['B']=[['all','no close back inside before entry' if b==0 else 'closed back inside before entry'] for b in E.backin.values]
        E['F']=[['all',s] for s in sess(E.t)]
        X=E[['row','e','d','T','B','F']].copy(); X['M']=E.model.map(MOD).values
        for c in ('T','B','F'): X=X.explode(c)
        X['key']=(X['T']+'|'+X.M+'|'+X.B+'|'+X.F).astype('category')
        G[per]=groups_from(X[['key','row','e','d']]); RR[per]=R
    S=summarize(G['old'],G['fresh'],RR['old'],RR['fresh'],CN,STD,min_o=40,min_f=8); S['tf']=tf; out.append(S)
    pickle.dump(G,open(f'G4_{tf}.pkl','wb')); print(tf,len(S),flush=True)
S=pd.concat(out,ignore_index=True); k=S.key.str.split('|',expand=True); k.columns=['break','entry','backin','filter']
S=pd.concat([S,k],axis=1); S.to_parquet('table4.parquet')
