import numpy as np, pandas as pd, glob, os, pickle
LIB='/home/claude/rt/lib/data'
def load(sym, months=None):
    fs=sorted(glob.glob(f'{LIB}/{sym}/1m/*.csv'))
    if months: fs=[f for f in fs if os.path.basename(f)[:-4] in months]
    d=pd.concat([pd.read_csv(f) for f in fs]); d.index=pd.to_datetime(d.pop('time'))
    d=d[~d.index.duplicated(keep='last')].sort_index()
    return d[['open','high','low','close','volume']].astype(float)
def rs(d, tf):
    if tf in ('5m','15m','1h'):
        key=d.index.floor({'5m':'5min','15m':'15min','1h':'60min'}[tf])
    elif tf=='4h': key=(d.index-pd.Timedelta(hours=18)).floor('4h')+pd.Timedelta(hours=18)
    elif tf=='D': key=(d.index+pd.Timedelta(hours=6)).floor('D')-pd.Timedelta(hours=6)
    elif tf=='W':
        s=(d.index+pd.Timedelta(hours=6)).floor('D')-pd.Timedelta(hours=6)   # session day start 18:00
        sd=(s+pd.Timedelta(hours=6)).normalize()                              # calendar trading date
        wk=sd-pd.to_timedelta(sd.weekday,unit='D')                            # monday
        key=wk-pd.Timedelta(hours=6)                                          # sunday 18:00
    g=d.groupby(key)
    o=pd.DataFrame({'open':g.open.first(),'high':g.high.max(),'low':g.low.min(),'close':g.close.last()})
    return o
if __name__=='__main__':
    old=load('NQ',[f'{y}-{m:02d}' for y in (2022,2023,2024,2025) for m in range(1,13)])
    old=old[old.index<'2026-01-01']
    fresh=load('MNQ')
    print(old.index[0],old.index[-1],len(old)); print(fresh.index[0],fresh.index[-1],len(fresh))
    pickle.dump({'old':old,'fresh':fresh},open('raw.pkl','wb'))
