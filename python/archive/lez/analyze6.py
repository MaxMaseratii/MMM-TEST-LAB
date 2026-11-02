import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim3 import cfg3
from summ import summarize
CN=cfg3()
STD={'max1':CN.index(('Sbox','RUN','BE+fees after 1 BC','no re-entry')),'max1r':CN.index(('Sbox','RUN','BE+fees after 1 BC','3 re-entries')),
     'opp3':CN.index(('Sbox','TP3','BE+fees after opp candle → BC','3 re-entries')),'fix':CN.index(('S50','TP2','no BE','no re-entry'))}
out=[]
for tf in ('1m','5m','15m'):
    G=pickle.load(open(f'G3_{tf}.pkl','rb'))
    keep=lambda g:{k:v for k,v in g.items() if '|A1 next open|' in k}
    Go,Gf=keep(G['old']),keep(G['fresh'])
    Ro=pickle.load(open(f'res3_old_{tf}.pkl','rb'))[0]; Rf=pickle.load(open(f'res3_fresh_{tf}.pkl','rb'))[0]
    S=summarize(Go,Gf,Ro,Rf,CN,STD,min_o=60,min_f=10); S['ltf']=tf; out.append(S); print(tf,len(S),flush=True)
S=pd.concat(out,ignore_index=True); k=S.key.str.split('|',expand=True); k.columns=['level','valid','seq','area','held','filter']
S=pd.concat([S,k],axis=1); S.to_parquet('table6.parquet')
# management comparison: per tf, median over ALL groups of avg R per setup for each config
rows=[]
for tf in ('1m','5m','15m'):
    G=pickle.load(open(f'G3_{tf}.pkl','rb'))
    for per in ('old','fresh'):
        R,NT,_=pickle.load(open(f'res3_{per}_{tf}.pkl','rb'))
        for k,idx in G[per].items():
            if '|A1 next open|' in k and k.startswith('ALL') and k.endswith('|any|all') and '|all seq|' in k:
                r=np.nan_to_num(R[idx]); nt=NT[idx]
                for c in range(len(CN)):
                    rows.append((tf,per,k.split('|')[0],k.split('|')[1],*CN[c],len(idx),r[:,c].mean(),(r[:,c]>=-0.001).mean(),nt[:,c].mean()))
M=pd.DataFrame(rows,columns=['ltf','per','level','valid','stop','target','mgmt','reentry','n','avg_setup','no_loss','trades_per_setup'])
M.to_parquet('mgmt.parquet')
g=M.groupby(['ltf','mgmt','reentry','per']).avg_setup.median().unstack('per').round(3)
print(g.to_string())
