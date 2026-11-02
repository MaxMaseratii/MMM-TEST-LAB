import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from sim import bc_arrays, turn_boxes
from sim2 import find_entries2, simulate2
from run import sid_of
from data import rs
R0=pickle.load(open('raw.pkl','rb')); EV=pickle.load(open('events.pkl','rb'))
WIN={'1m':(60,60,10),'5m':(12,12,6),'15m':(8,16,4)}
for per in ('old','fresh'):
    m1=R0[per]; ev=EV[per].reset_index(drop=True)
    for tf in ('1m','5m','15m'):
        t0=time.time()
        d=m1 if tf=='1m' else rs(m1,tf)
        O,H,L,C=[d[k].values.astype(np.float64) for k in ('open','high','low','close')]
        bu,be,nn=bc_arrays(H,L,C); BJ,BP,BT,BB=turn_boxes(O,H,L,C,bu,be,nn)
        ei=ev.i.values.astype(np.int64) if tf=='1m' else np.searchsorted(d.index.values,ev.t.dt.floor({'5m':'5min','15m':'15min'}[tf]).values).astype(np.int64)
        sid=sid_of(d.index); parts=[]
        for nv in (0,1):
            w1,w2,w3=WIN[tf]
            ent=find_entries2(O,H,L,C,bu,be,nn,ei,ev.d.values.astype(np.int64),ev.top.values,ev.bot.values,BJ,BP,BT,BB,w1,w2,w3,nv)
            E=pd.DataFrame(ent,columns=['ev','area','e','px','d','edge','top','bot','lim','seq','inside','ty','dirN','lv','boxj','k'])
            for c in ('ev','area','e','d','lim','seq','inside','ty','dirN','lv','boxj','k'): E[c]=E[c].astype(np.int64)
            E['valid2']=nv; parts.append(E)
        E=pd.concat(parts,ignore_index=True)
        Rm=simulate2(O,H,L,C,bu,be,sid,E.e.values.astype(np.float64),E.px.values,E.d.values.astype(np.float64),E.edge.values,E.lim.values.astype(np.float64),1.0)
        E['lvl']=ev.lvl.values[E.ev.values]; E['t']=d.index[E.e.values.clip(0,len(d)-1)]
        pickle.dump((E,Rm),open(f'res2_{per}_{tf}.pkl','wb'))
        print(per,tf,len(E),E.groupby(['valid2','area']).size().to_dict(),round(time.time()-t0,1),flush=True)
