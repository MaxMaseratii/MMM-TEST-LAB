import pickle, glob, pandas as pd, numpy as np
L='/home/claude/data5/MNQ/'
def ld(tf):
    fs=sorted(glob.glob(L+tf+'/*.csv')); d=pd.concat([pd.read_csv(f) for f in fs]); d.index=pd.to_datetime(d.pop('time'))
    d=d[~d.index.duplicated(keep='last')].sort_index(); return d[['open','high','low','close','volume']].astype(float)
r=pickle.load(open('/home/claude/lez/raw.pkl','rb'))
m1=r['fresh']; m5=ld('5m'); m15=ld('15m')
sday=lambda ix: (ix+pd.Timedelta(hours=6)).normalize()
d1=set(sday(m1.index)); d5=set(sday(m5.index))
p5=m5[~sday(m5.index).isin(d1)]
p15=m15[~sday(m15.index).isin(d1|d5)]
f_all=pd.concat([m1,p5,p15]).sort_index(); f_all=f_all[~f_all.index.duplicated(keep='first')]
f_5=pd.concat([m1,p5]).sort_index(); f_5=f_5[~f_5.index.duplicated(keep='first')]
print(len(m1),len(p5),len(p15), f_all.index[0], f_all.index[-1])
pickle.dump({'old':r['old'],'fresh':f_all,'fresh5':f_5},open('/home/claude/xb/raw2.pkl','wb'))
