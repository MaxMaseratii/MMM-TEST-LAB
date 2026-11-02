import numpy as np,pandas as pd,pickle,sys
sys.path.insert(0,'/home/claude/lez')
from data import rs
from eng4 import run
R=pickle.load(open('raw.pkl','rb')); out={}
for per in ('old','fresh'):
    m1=R[per]
    for tf in ('15m','1h'):
        d=rs(m1,tf); run(d,snap=False); side=np.array(run.SIDE)
        # known after the candle closes: close time = next candle start (or +dur)
        dur=pd.Timedelta(minutes=15 if tf=='15m' else 60)
        out[(per,tf)]=(d.index.values+dur.to_timedelta64(), side)
        print(per,tf,len(d),np.bincount(side+1))
pickle.dump(out,open('trend.pkl','wb'))
