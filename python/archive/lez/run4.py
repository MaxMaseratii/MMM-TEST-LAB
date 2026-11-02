import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from sim import bc_arrays
from sim4 import turn_boxes2, find_entries3
from sim2 import simulate2
from sim3 import simulate3
from run import sid_of
from data import rs
R0=pickle.load(open('raw.pkl','rb')); EV=pickle.load(open('events.pkl','rb'))
WIN={'1m':(60,60,10),'5m':(12,12,6),'15m':(8,16,4)}; W3={'1m':120,'5m':48,'15m':24}
for per in ('old','fresh'):
    m1=R0[per]; ev=EV[per].reset_index(drop=True)
    for tf in ('1m','5m','15m'):
        t0=time.time(); d=m1 if tf=='1m' else rs(m1,tf)
        O,H,L,C=[d[k].values.astype(np.float64) for k in ('open','high','low','close')]
        bu,be,nn=bc_arrays(H,L,C); BJ,BP,BT,BB,BK=turn_boxes2(O,H,L,C,bu,be,nn)
        ei=ev.i.values.astype(np.int64) if tf=='1m' else np.searchsorted(d.index.values,ev.t.dt.floor({'5m':'5min','15m':'15min'}[tf]).values).astype(np.int64)
        sid=sid_of(d.index); w1,w2,w3=WIN[tf]
        ent,bxs=find_entries3(O,H,L,C,bu,be,nn,ei,ev.d.values.astype(np.int64),ev.top.values,ev.bot.values,BJ,BP,BT,BB,BK,w1,w2,w3)
        E=pd.DataFrame(ent,columns=['ev','area','e','px','d','edge','top','bot','lim','pre','touch','first','boxtype','lv','boxj','k','post','nxt'])
        for c in ('ev','area','e','d','lim','pre','touch','first','boxtype','lv','boxj','k','post','nxt'): E[c]=E[c].astype(np.int64)
        X=pd.DataFrame(bxs,columns=['ev','d','boxtype','first','second','retested','bars','lv','outc','post','nxt','inside']); X['lvl']=ev.lvl.values[X.ev.values.astype(int)]
        Rm=simulate2(O,H,L,C,bu,be,sid,E.e.values.astype(np.float64),E.px.values,E.d.values.astype(np.float64),E.edge.values,E.lim.values.astype(np.float64),1.0)
        e1=np.where(E.area.values==1,E.e.values,-1).astype(np.float64)
        R3,NT,PT=simulate3(O,H,L,C,bu,be,sid,e1,E.px.values,E.d.values.astype(np.float64),E.top.values,E.bot.values,1.0,W3[tf])
        E['lvl']=ev.lvl.values[E.ev.values]; E['t']=d.index[E.e.values.clip(0,len(d)-1)]
        pickle.dump((E,Rm,R3,NT,PT,X),open(f'res4_{per}_{tf}.pkl','wb'))
        print(per,tf,len(E),len(X),round(time.time()-t0,1),flush=True)
