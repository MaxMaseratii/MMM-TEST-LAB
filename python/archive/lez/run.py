import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from sim import *
def sid_of(idx):
    m=idx.hour*60+idx.minute
    b=np.where((m>=1080)|(m<120),0,np.where(m<480,1,np.where(m<570,2,3)))
    ch=np.r_[0,(np.diff(b)!=0)|(np.diff(idx.values).astype('timedelta64[m]').astype(int)>120)]
    return np.cumsum(ch).astype(np.int64)
def ltf_arrays(m1,tf):
    if tf=='1m': d=m1
    else:
        g=m1.groupby(m1.index.floor('5min'))
        d=pd.DataFrame({'open':g.open.first(),'high':g.high.max(),'low':g.low.min(),'close':g.close.last()})
    return d
if __name__=='__main__':
    R0=pickle.load(open('raw.pkl','rb')); EV=pickle.load(open('events.pkl','rb'))
    for per in ('old','fresh'):
        m1=R0[per]; ev=EV[per].reset_index(drop=True)
        for tf,(w1,w2) in (('1m',(60,60)),('5m',(12,12))):
            t0=time.time()
            d=ltf_arrays(m1,tf); O,H,L,C=[d[k].values.astype(np.float64) for k in ('open','high','low','close')]
            bu,be,nn=bc_arrays(H,L,C)
            BJ,BP,BT,BB=turn_boxes(O,H,L,C,bu,be,nn)
            if tf=='1m': ei=ev.i.values.astype(np.int64)
            else: ei=np.searchsorted(d.index.values,ev.t.dt.floor('5min').values).astype(np.int64)
            ent=find_entries(O,H,L,C,bu,be,nn,ei,ev.d.values.astype(np.int64),ev.top.values,ev.bot.values,BJ,BP,BT,BB,w1,w2)
            E=pd.DataFrame(ent,columns=['ev','model','e','px','d','edge','top','bot','lim','rt','ty','boxj','ft','lv'])
            for c in ('ev','model','e','d','lim','rt','ty','boxj','ft','lv'): E[c]=E[c].astype(np.int64)
            sid=sid_of(d.index)
            Rm=simulate(O,H,L,C,bu,be,sid,E.e.values.astype(np.float64),E.px.values,E.d.values.astype(np.float64),E.edge.values,E.lim.values.astype(np.float64),1.0)
            E['lvl']=ev.lvl.values[E.ev.values]; E['t']=d.index[E.e.values.clip(0,len(d)-1)]
            E['ltf']=tf; E['per']=per
            pickle.dump((E,Rm),open(f'res_{per}_{tf}.pkl','wb'))
            print(per,tf,'boxes',len(BJ),'entries',len(E),'secs',round(time.time()-t0,1),flush=True)
            print(E.groupby('model').size().to_dict(),flush=True)
