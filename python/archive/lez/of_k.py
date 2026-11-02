import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from data import rs
from eng4 import run
from sim import bc_arrays
from sim2 import simulate2
from run import sid_of
R0=pickle.load(open('raw.pkl','rb')); ALL={}
for per in ('old','fresh'):
    for tf in ('1m','5m','15m','1h'):
        d=R0[per] if tf=='1m' else rs(R0[per],tf)
        O,H,L,C=[d[k].values.astype(np.float64) for k in ('open','high','low','close')]; n=len(C)
        bu,be,nn=bc_arrays(H,L,C); sid=sid_of(d.index)
        _,_,ev,_=run(d,snap=False); rows=[]
        for q,e in enumerate(ev):
            t,nm,dd,pend,bi,bt,bb=e[:7]; typ=nm[:3] if nm[:3] in ('CDL','CDS') else nm[:2]
            nxt=ev[q+1][4] if q+1<len(ev) else n-1
            near=bt if dd==1 else bb; far=bb if dd==1 else bt
            for K in (1,2,3,5):
                if bi+K+1>=n or bi+K>=nxt: continue
                seg=C[bi+1:bi+K+1]
                back=(seg<=near).any() if dd==1 else (seg>=near).any()
                # O5: no close back inside for K candles → enter in the break direction
                if not back: rows.append((q,typ,dd,50+K,bi+K+1,O[bi+K+1],far,0))
                # O6: it closed back inside within K candles → fade? no: enter WITH the break only after it closes back out (next BC with the break)
                else:
                    for k in range(bi+K+1,min(nxt,bi+K+60,n-1)):
                        if (dd==1 and C[k]<far) or (dd==-1 and C[k]>far): break
                        if (bu[k] if dd==1 else be[k]) and ((C[k]>near) if dd==1 else (C[k]<near)):
                            rows.append((q,typ,dd,60+K,k+1,O[k+1],far,0)); break
        E=pd.DataFrame(rows,columns=['ev','typ','d','model','e','px','edge','lim']); E['t']=d.index[E.e.values]
        Rm=simulate2(O,H,L,C,bu,be,sid,E.e.values.astype(np.float64),E.px.values,E.d.values.astype(np.float64),E.edge.values,E.lim.values.astype(np.float64),1.0)
        ALL[(per,tf)]=(E,Rm); print(per,tf,len(E),flush=True)
pickle.dump(ALL,open('ofk_res.pkl','wb'))
