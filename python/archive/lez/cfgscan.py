import numpy as np,pickle,sys
from sim2 import cfg_names2
CN=cfg_names2()
def scan(tf,key,top=8):
    G=pickle.load(open(f'G7_{tf}.pkl','rb')); out={}
    for per in ('old','fresh'):
        E,Rm,*_=pickle.load(open(f'res4_{per}_{tf}.pkl','rb')); idx=G[per][key]; R=Rm[idx]
        raw=np.abs(E.px.values[idx]-E.edge.values[idx])+0.25
        D=np.stack([np.full(len(idx),float(c[0][1:])) if c[0][1:].isdigit() else (np.clip(raw,20,50) if c[0]=='Sbox' else np.maximum(raw,10)) for c in CN],1)
        out[per]=(np.nanmean(R,0),np.nansum(R*D,0)*2,np.nanmean(R>0,0))
    o,f=out['old'],out['fresh']; ok=[i for i in range(len(CN)) if CN[i][0]!='Szone' and o[0][i]>0 and f[0][i]>0 and f[1][i]>0 and o[1][i]>0]
    print(key,len(ok))
    for i in sorted(ok,key=lambda i:-(o[0][i]+f[0][i]/3))[:top]: print('  ',CN[i],round(o[0][i],3),round(f[0][i],3),round(o[1][i]),round(f[1][i]),round(o[2][i],2),round(f[2][i],2))
for tf,k in [('15m','ALL UPG gaps|all|wick touch only|all|A1 next open|held'),('15m','M15 UPG|all|wick touch only|all|A4 limit at high/low the BC broke|held')]: scan(tf,k)
