"""Fill TGT-first and 50%-first for 1h / Daily / Weekly on NQ, ES, GC, CL from finer bars of the same source."""
import pandas as pd, numpy as np, glob, json, pickle, sys
sys.path.insert(0,'/home/claude/ten')
from common import ctype, lean
L='/home/claude/data5/'
def rd(sym,tf,years=None):
    fs=sorted(glob.glob(f'{L}{sym}/{tf}/*.csv'))
    d=pd.concat([pd.read_csv(f) for f in fs]); d.index=pd.to_datetime(d.pop('time')); d=d[~d.index.duplicated(keep='last')].sort_index()
    d=d[(d.high>=d[['open','close']].max(axis=1)-1e-9)&(d.low<=d[['open','close']].min(axis=1)+1e-9)&(d.high>d.low)]
    return d[['open','high','low','close']]
def parent(fine, kind):
    t=fine.index
    if kind=='1h': key=t.floor('h')
    elif kind=='D': key=(t+pd.Timedelta(hours=6)).normalize()
    else: key=t.to_period('W-FRI').to_timestamp()
    g=fine.groupby(key)
    b=pd.DataFrame({'open':g.open.first(),'high':g.high.max(),'low':g.low.min(),'close':g.close.last(),'cnt':g.open.size()})
    return b,key
def order(fine, kind, minc, maxgap):
    """rows: (date, type, first(bool), mid(bool)) for each candle whose NEXT candle is fully covered"""
    b,key=parent(fine,kind); kv=np.asarray(key); H=fine.high.values; Lo=fine.low.values
    u,first=np.unique(kv,return_index=True); last=np.r_[first[1:],len(kv)]
    pos={k:(a,z) for k,a,z in zip(u,first,last)}
    b=b[b.cnt>=minc]
    o,h,l,c=b.open.values,b.high.values,b.low.values,b.close.values; ix=b.index
    rows=[]
    for i in range(1,len(b)-1):
        if (ix[i]-ix[i-1])>maxgap or (ix[i+1]-ix[i])>maxgap: continue
        T=ctype(o[i],h[i],l[i],c[i],h[i-1],l[i-1]); dl=1 if lean(T)=='bull' else -1
        tg=h[i] if dl==1 else l[i]; pr=l[i] if dl==1 else h[i]; mid=(h[i]+l[i])/2
        a,z=pos[np.datetime64(ix[i+1])] if np.datetime64(ix[i+1]) in pos else pos[ix[i+1]]
        hh=H[a:z]; ll=Lo[a:z]
        it=np.flatnonzero(hh>=tg) if dl==1 else np.flatnonzero(ll<=tg)
        ip=np.flatnonzero(ll<=pr) if dl==1 else np.flatnonzero(hh>=pr)
        im=np.flatnonzero(ll<=mid) if dl==1 else np.flatnonzero(hh>=mid)
        if len(it) and len(ip) and it[0]==ip[0]: continue          # same fine bar: order unknown
        if len(it) and len(im) and it[0]==im[0]: mflag=None
        else: mflag= len(im)>0 and (len(it)==0 or im[0]<it[0])
        rows.append((ix[i],T, len(it)>0 and (len(ip)==0 or it[0]<ip[0]), mflag))
    return rows
M={'NQ':('NQ','MNQ'),'ES':('ES','MES'),'GC':('GC','MGC'),'CL':('CL','MCL')}
raw_old=pickle.load(open('/home/claude/lez/raw.pkl','rb'))['old'][['open','high','low','close']]
OUT={}; SRC={}
for m,(big,mic) in M.items():
    f15=rd(mic,'15m'); f5=rd(mic,'5m')
    cut5=f5.index.min()
    fine_h=pd.concat([f15[f15.index<cut5.floor('D')], f5])           # 15m before the 5m data starts, then 5m
    R={'1h':[], 'D':[], 'W':[]}
    R['1h']+=order(fine_h,'1h',3,pd.Timedelta(hours=1))
    R['D']+=order(f15,'D',60,pd.Timedelta(days=4))
    if m=='NQ':
        R['1h']+=order(raw_old,'1h',50,pd.Timedelta(hours=1))
        R['D']+=order(raw_old,'D',600,pd.Timedelta(days=4))
    d1=rd(big,'1d')
    if m=='GC': d1=d1[d1.index>='2020-01-01']
    R['W']+=order(d1,'W',3,pd.Timedelta(days=10))
    p2={'1h':pd.Timestamp('2026-06-01'),'D':pd.Timestamp('2026-06-01') if m!='NQ' else pd.Timestamp('2026-01-01'),'W':pd.Timestamp('2023-05-01') if m=='GC' else pd.Timestamp('2013-01-01')}
    OUT[m]={}
    for tf,rows in R.items():
        df=pd.DataFrame(rows,columns=['t','T','first','mid'])
        res={}
        for T,g in df.groupby('T'):
            g2=g[g.t>=p2[tf]]; gm=g[g.mid.notna()]
            res[T]=dict(n=len(g),first=round(100*g['first'].mean()) if len(g)>=10 else None,
                        mid=round(100*gm['mid'].astype(bool).mean()) if len(gm)>=10 else None,
                        n2=len(g2),first2=round(100*g2['first'].mean()) if len(g2)>=10 else None)
        OUT[m][tf]=res
        print(m,tf,len(df),{k:(v['n'],v['first'],v['mid']) for k,v in res.items() if k in ('BuBC+','BeBC+','BuBC-','BuC2+')})
json.dump(OUT,open('order4.json','w'))
