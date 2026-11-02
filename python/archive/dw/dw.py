import pandas as pd, numpy as np, glob, json, pickle, sys
sys.path.insert(0,'/home/claude/ten')
from common import ctype, lean, TYPES
L='/home/claude/data5/NQ/'
d=pd.concat([pd.read_csv(f) for f in sorted(glob.glob(L+'1d/*.csv'))]); d.index=pd.to_datetime(d.pop('time')); d=d[~d.index.duplicated(keep='last')].sort_index()
bad=(d.low>d[['open','close']].min(axis=1)+1e-6)|(d.high<d[['open','close']].max(axis=1)-1e-6)|(d.high<=d.low)
print('daily bars',len(d),'bad',bad.sum()); d=d[~bad]
def wk(x):
    g=x.groupby(x.index.to_period('W-FRI'))
    w=pd.DataFrame({'open':g.open.first(),'high':g.high.max(),'low':g.low.min(),'close':g.close.last(),'n':g.open.size()}); w.index=w.index.to_timestamp(); return w
def stats_bars(b):
    """next-candle odds from bars only (no intraday order)"""
    o,h,l,c=b.open.values,b.high.values,b.low.values,b.close.values
    ty=[None]+[ctype(o[i],h[i],l[i],c[i],h[i-1],l[i-1]) for i in range(1,len(b))]
    R={}
    for T in TYPES:
        dl=1 if lean(T)=='bull' else -1
        idx=[i for i in range(1,len(b)-1) if ty[i]==T]
        if not idx: continue
        tg=[(h[i] if dl==1 else l[i]) for i in idx]; pr=[(l[i] if dl==1 else h[i]) for i in idx]
        ht=np.array([(h[i+1]>=t) if dl==1 else (l[i+1]<=t) for i,t in zip(idx,tg)])
        hp=np.array([(l[i+1]<=p) if dl==1 else (h[i+1]>=p) for i,p in zip(idx,pr)])
        bw=np.array([(c[i+1]>h[i]) if dl==1 else (c[i+1]<l[i]) for i in idx]); ba=np.array([(c[i+1]<l[i]) if dl==1 else (c[i+1]>h[i]) for i in idx])
        n=len(idx); R[T]=dict(n=n,tgt=100*ht.mean(),prot=100*hp.mean(),both=100*(ht&hp).mean(),bcw=100*bw.mean(),bca=100*ba.mean(),nbc=100*(1-bw.mean()-ba.mean()))
    return R
def sessions(m, kind):
    """build daily (18:00-17:00, labelled by close date) or weekly sessions from intraday bars; return bars + list of intraday slices"""
    t=m.index
    if kind=='D': key=(t+pd.Timedelta(hours=6)).normalize()   # 18:00 -> next day
    else: key=(t+pd.Timedelta(hours=6)).to_period('W-FRI').to_timestamp()
    g=m.groupby(key)
    b=pd.DataFrame({'open':g.open.first(),'high':g.high.max(),'low':g.low.min(),'close':g.close.last(),'cnt':g.open.size()})
    b=b[b.index.dayofweek<5] if kind=='D' else b
    return b, key
def order_stats(m,kind,minc):
    b,key=sessions(m,kind); b=b[b.cnt>=minc]
    H=m.high.values; Lw=m.low.values; kv=key.values
    starts={}; 
    for k,i in zip(*np.unique(kv,return_index=True)): starts[k]=i
    ends={}
    for k,i in zip(*np.unique(kv[::-1],return_index=True)): ends[k]=len(kv)-1-i
    o,h,l,c=b.open.values,b.high.values,b.low.values,b.close.values; ix=b.index.values
    R={}
    for i in range(1,len(b)-1):
        T=ctype(o[i],h[i],l[i],c[i],h[i-1],l[i-1]); dl=1 if lean(T)=='bull' else -1
        tg=h[i] if dl==1 else l[i]; pr=l[i] if dl==1 else h[i]; mid=(h[i]+l[i])/2
        a=starts[ix[i+1]]; z=ends[ix[i+1]]+1; hh=H[a:z]; ll=Lw[a:z]
        it=np.flatnonzero(hh>=tg) if dl==1 else np.flatnonzero(ll<=tg)
        ip=np.flatnonzero(ll<=pr) if dl==1 else np.flatnonzero(hh>=pr)
        im=np.flatnonzero(ll<=mid) if dl==1 else np.flatnonzero(hh>=mid)
        r=R.setdefault(T,dict(n=0,first=0,mid=0,tgt=0,amb=0))
        if len(it) and len(ip) and it[0]==ip[0]: r['amb']+=1; continue
        r['n']+=1; r['tgt']+=len(it)>0
        r['first']+= len(it)>0 and (len(ip)==0 or it[0]<ip[0])
        r['mid']+= len(im)>0 and (len(it)==0 or im[0]<it[0])
    return {T:dict(n=v['n'],first=100*v['first']/v['n'] if v['n'] else None,mid=100*v['mid']/v['n'] if v['n'] else None,tgt=100*v['tgt']/v['n'] if v['n'] else None,amb=v['amb']) for T,v in R.items()}
old=d[d.index<'2026-01-01']; new=d[d.index>='2025-12-20']
A={'D':stats_bars(old),'W':stats_bars(wk(old))}
F={'D':stats_bars(new[new.index>='2025-12-31']),'W':stats_bars(wk(new[new.index>='2025-12-26']))}
raw=pickle.load(open('/home/claude/lez/raw.pkl','rb'))['old']
I={'D':order_stats(raw,'D',600),'W':order_stats(raw,'W',3000)}
h1=pd.concat([pd.read_csv(f) for f in sorted(glob.glob(L+'1h/2026.csv'))]); h1.index=pd.to_datetime(h1.pop('time')); h1=h1.sort_index()
I26={'D':order_stats(h1,'D',15),'W':order_stats(h1,'W',80)}
out={}
for tf in ('D','W'):
    out[tf]={}
    for T in TYPES:
        a=A[tf].get(T); 
        if not a: continue
        i=I[tf].get(T,{}); f=F[tf].get(T,{}); j=I26[tf].get(T,{})
        rr=lambda x: None if x is None else int(round(x))
        out[tf][T]=[a['n'],rr(a['tgt']),rr(i.get('first')),rr(a['prot']),rr(a['bcw']),rr(a['bca']),rr(a['nbc']),rr(i.get('mid')),f.get('n',0),rr(f.get('tgt')),rr(j.get('first')),i.get('n',0),j.get('n',0)]
    print(tf); [print(' ',T,v) for T,v in out[tf].items()]
json.dump(out,open('dw_odds.json','w'))
# sanity: compare 1m-built daily with Yahoo daily on overlapping dates
b,_=sessions(raw,'D'); b=b[b.cnt>=600]; j=b.join(d,rsuffix='_y',how='inner'); 
print('overlap',len(j),'close diff med',(j.close-j.close_y).abs().median(),'range ratio med',((j.high-j.low)/(j.high_y-j.low_y)).median())
# weekly TGT-first / 50% using the daily bars inside the next week (2000-2025); same-day hits = unknown, skipped
def weekly_order(x):
    w=wk(x); wk_id=x.index.to_period('W-FRI').to_timestamp()
    o,h,l,c=w.open.values,w.high.values,w.low.values,w.close.values; ix=w.index
    R={}
    for i in range(1,len(w)-1):
        T=ctype(o[i],h[i],l[i],c[i],h[i-1],l[i-1]); dl=1 if lean(T)=='bull' else -1
        tg=h[i] if dl==1 else l[i]; pr=l[i] if dl==1 else h[i]; mid=(h[i]+l[i])/2
        nx=x[wk_id==ix[i+1]]; hh=nx.high.values; ll=nx.low.values
        it=np.flatnonzero(hh>=tg) if dl==1 else np.flatnonzero(ll<=tg)
        ip=np.flatnonzero(ll<=pr) if dl==1 else np.flatnonzero(hh>=pr)
        im=np.flatnonzero(ll<=mid) if dl==1 else np.flatnonzero(hh>=mid)
        r=R.setdefault(T,dict(n=0,first=0,mid=0))
        if len(it) and len(ip) and it[0]==ip[0]: continue
        if len(it) and len(im) and it[0]==im[0] and not (len(ip) and ip[0]<it[0]): pass
        r['n']+=1; r['first']+= len(it)>0 and (len(ip)==0 or it[0]<ip[0])
        r['mid']+= len(im)>0 and (len(it)==0 or im[0]<it[0])
    return R
WO=weekly_order(old)
for T,v in out['W'].items():
    r=WO.get(T)
    if r and r['n']: v[2]=int(round(100*r['first']/r['n'])); v[7]=int(round(100*r['mid']/r['n'])); v[11]=r['n']
for tf in ('D','W'):
    for T,v in out[tf].items():
        if v[11]<10: v[2]=None; v[7]=None
        if v[8]<5: v[9]=None
        if v[12]<5: v[10]=None
print('W'); [print(' ',T,v) for T,v in out['W'].items()]
json.dump(out,open('dw_odds.json','w'))
