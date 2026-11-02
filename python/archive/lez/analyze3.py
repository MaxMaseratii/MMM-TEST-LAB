import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from sim2 import cfg_names2
from analyze import GROUPS
from analyze2 import sess
from summ import groups_from, summarize
CN=cfg_names2()
STD={'max':CN.index(('Sbox','+box exit','RUN','BE2')),'tp2':CN.index(('Sbox','+box exit','TP2','')),'fix50':CN.index(('S50','','TP2','')),'tp3o':CN.index(('Sbox','+box exit','TP3','trailOpp'))}
SEQ={1:'S1 touch → BC',2:'S2 touch → NBC → BC',3:'S3 touch → NBC → opp → BC',4:'S4 touch → opp → BC'}
INS={0:'touch only',1:'close inside'}
AREA={1:'A1 next open',2:'A2 limit 50% of entry BC',3:'A3 limit at entry BC open',4:'A4 limit at the high/low the BC broke',5:'A5 limit at box edge',6:'A6 GMC gap limit'}
VAL={0:'1 BC (break only)',1:'2 BCs (validated) then retest'}
def explode(E):
    E=E.reset_index(drop=True).copy(); E['row']=np.arange(len(E))
    lv_un=E.lvl.unique(); gmap={l:[l]+[g for g,f in GROUPS.items() if f(l)] for l in lv_un}
    s=sess(E.t)
    E['L']=E.lvl.map(gmap)
    E['S']=[['all seq',SEQ[a],SEQ[a]+' · '+INS[b],INS[b]] for a,b in zip(E.seq.values,E.inside.values)]
    E['H']=[['any','held'] if x==0 else ['any'] for x in E.lv.values]
    E['F']=[['all',x] for x in s]
    X=E[['row','e','d','L','S','H','F']].copy()
    X['A']=E.area.map(AREA).values; X['V']=E.valid2.map(VAL).values
    for c in ('L','S','H','F'): X=X.explode(c)
    X['key']=(X.L+'|'+X.V+'|'+X.S+'|'+X.A+'|'+X.H+'|'+X.F).astype('category')
    return X[['key','row','e','d']]
if __name__=='__main__':
    t0=time.time(); out=[]
    for tf in ('1m','5m','15m'):
        G={};RR={}
        for per in ('old','fresh'):
            E,R=pickle.load(open(f'res2_{per}_{tf}.pkl','rb'))
            X=explode(E); G[per]=groups_from(X); RR[per]=R; del X
            print(tf,per,len(G[per]),round(time.time()-t0),flush=True)
        S=summarize(G['old'],G['fresh'],RR['old'],RR['fresh'],CN,STD,min_o=60,min_f=10)
        S['ltf']=tf; out.append(S); pickle.dump(G,open(f'G3_{tf}.pkl','wb'))
        print(tf,'groups',len(S),round(time.time()-t0),flush=True)
    S=pd.concat(out,ignore_index=True)
    k=S.key.str.split('|',expand=True); k.columns=['level','valid','seq','area','held','filter']
    S=pd.concat([S,k],axis=1); S.to_parquet('table3.parquet'); print(len(S))
