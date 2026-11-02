import time, ppdata, engine, numpy as np, pandas as pd
t0=time.time()
L=ppdata.series('NQ',5); print('load',time.time()-t0,[len(d) for d in L])
d=L[0]
t0=time.time(); S=engine.signals(d); print('sig',time.time()-t0)
print('flips',S['fUp'].sum()+S['fDn'].sum(),'exits',S['exL'].sum()+S['exS'].sum(),'t50',(S['t50S']!=0).sum(),'brk',(S['brk']!=0).sum(),'rej1',(S['rejS']!=0).sum(),'gmc',(S['gmc']!=0).sum())
sp=ppdata.SPEC['NQ']
t0=time.time(); T,mi,sk=engine.trades(S,d.index,sp['stop'],sp['cost'],sp['tick']); print('trades',time.time()-t0,len(T))
g=T.groupby('setup').pl.agg(['count','mean','std'])
g['t']=g['mean']/g['std']*np.sqrt(g['count']); g['wr']=T.groupby('setup').pl.apply(lambda x:(x>0).mean())
g.index=[engine.SETUPS[i] for i in g.index]; print(g.round(2)); print('missed',mi,'skipped',sk)
print(T.why.value_counts())
