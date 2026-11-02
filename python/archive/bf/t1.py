import sys, time; sys.path.insert(0,'/home/claude/pp')
import ppdata, bfeng, numpy as np, pandas as pd
d=ppdata.series('NQ',15)[1]
t0=time.time(); S=bfeng.signals(d); print('t',time.time()-t0, 'flips',len(S['fI']),'cancels',len(S['xI']),'bars',len(d))
print('resets dist',np.bincount(S['fRes'])[:8],'big',S['fBig'].mean())
k=30; i=S['fI'][k]; c1=S['fC1'][k]
sub=d.iloc[c1-3:i+4][['open','high','low','close']].copy()
idx=np.arange(c1-3,i+4); sub['tr']=S['trend'][idx]; sub['lnW']=S['lnW'][idx]
print(S['fS'][k],S['fB1'][k],S['fB2'][k],S['fW1'][k],S['fLine'][k],S['fRes'][k]); print(sub.to_string())
d1=ppdata.series('NQ',1)[0]; t0=time.time(); S1=bfeng.signals(d1); print('1m t',time.time()-t0,len(S1['fI']),len(d1))
