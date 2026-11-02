import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from sim import bc_arrays
from sim3 import simulate3
from run import sid_of
from data import rs
R0=pickle.load(open('raw.pkl','rb')); W={'1m':120,'5m':48,'15m':24}
for per in ('old','fresh'):
    for tf in ('1m','5m','15m'):
        t0=time.time(); E,_=pickle.load(open(f'res2_{per}_{tf}.pkl','rb'))
        d=R0[per] if tf=='1m' else rs(R0[per],tf)
        O,H,L,C=[d[k].values.astype(np.float64) for k in ('open','high','low','close')]
        bu,be,nn=bc_arrays(H,L,C); sid=sid_of(d.index)
        e=np.where(E.area.values==1,E.e.values,-1).astype(np.float64)
        R,NT,PT=simulate3(O,H,L,C,bu,be,sid,e,E.px.values,E.d.values.astype(np.float64),E.top.values,E.bot.values,1.0,W[tf])
        pickle.dump((R,NT,PT),open(f'res3_{per}_{tf}.pkl','wb'))
        print(per,tf,R.shape,round(time.time()-t0,1),flush=True)
