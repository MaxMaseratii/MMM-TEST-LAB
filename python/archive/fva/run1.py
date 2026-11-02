import sys, time, pickle, numpy as np, pandas as pd
sys.path.insert(0,'/home/claude/rt/eng'); sys.path.insert(0,'.')
from core import load, resample
from replica import run, category
from sim import ind_sim
t0=time.time()
m15 = load('MNQ','15m'); m15=m15[m15.index>='2025-11-30 18:00']
tr = run(m15, pv=2.0); print('MNQ 15m bars',len(m15),'trades',len(tr), round(time.time()-t0,1),'s')
h,l,c = m15.high.values, m15.low.values, m15.close.values
rows=[]
for t in tr:
    r,how,j = ind_sim(t,h,l,c)
    rows.append(dict(cat=category(t['etype']), t=t['t'], R=r, how=how, same=(j==t['i'])))
d=pd.DataFrame(rows); d=d[d.R.notna()]
print('indicator math: N',len(d),'WR',round((d.R>0).mean()*100,1),'avgRR',round(d.R.mean(),3), 'same-bar resolved %', round(d.same.mean()*100,1))
print(d.groupby('cat').apply(lambda x: pd.Series(dict(N=len(x),WR=round((x.R>0).mean()*100,1),same=round(x.same.mean()*100,1)))))
# last week like the screenshot (Oct 12-16)
w=d[d.t>='2026-10-11 18:00']; print('Oct 12-16: N',len(w),'WR',round((w.R>0).mean()*100,1))
print(w.groupby('cat').apply(lambda x: f"{(x.R>0).sum()}/{(x.R<=0).sum()} ({(x.R>0).mean()*100:.0f}%)"))
pickle.dump(tr,open('tr_mnq15.pkl','wb'))
