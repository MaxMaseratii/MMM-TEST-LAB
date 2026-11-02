import numpy as np, pandas as pd, json, sys
sys.path.insert(0,'.'); import bfprop
def r(v,d=3):
    try:
        v=float(v); return None if not np.isfinite(v) else round(v,d)
    except: return None
def st(x):
    x=x.dropna(); n=len(x)
    if n<2: return [n,None,None,None,None]
    pos=x[x>0].sum(); neg=-x[x<=0].sum()
    return [n,r((x>0).mean()),r(x.mean()),r(pos/neg if neg>0 else np.nan,2),r(x.mean()/x.std(ddof=1)*np.sqrt(n),2)]
D=pd.read_parquet('ibtest.parquet'); D=D[~((D.variant=='IBc')&(D.kind=='TC'))]
S={}
rows=[]
for (m,tf,var,kind,stop,tg),g in D.groupby(['m','tf','variant','kind','stop','target']):
    a=st(g[g.per=='P1'].r); b=st(g[g.per=='P2'].r)
    rows.append([m,int(tf),var,kind,stop,tg]+a+[r(g[g.per=='P1'].rr.mean())]+b+[r(g[g.per=='P2'].rr.mean())])
S['all']=rows
# filters
F=[]
N=D[(D.stop=='structure (swing)')&(D.variant=='IB')]
for m in ['NQ','ES','GC']:
    for tf in sorted(N[N.m==m].tf.unique()):
        b=N[(N.m==m)&(N.tf==tf)]
        for lab,x in (('TC to IB edge (her rule)',b[(b.kind=='TC')&(b.target=='her target')]),('TC to IB edge + VWAP at IB mid',b[(b.kind=='TC')&(b.target=='her target')&b.vwOK]),
                      ('FA back to IB mid (her rule)',b[(b.kind=='FA')&(b.target=='her target')]),('FA with the IB trend',b[(b.kind=='FA')&(b.target=='her target')&b.aligned]),('FA against the IB trend',b[(b.kind=='FA')&(b.target=='her target')&~b.aligned])):
            F.append([m,int(tf),lab]+st(x[x.per=='P1'].r)+[r(x[x.per=='P1'].rr.mean())]+st(x[x.per=='P2'].r)+[r(x[x.per=='P2'].rr.mean())])
S['filters']=F
# money
M=[]
for m in ['NQ','ES','GC']:
    for tf in sorted(D[D.m==m].tf.unique()):
        b=D[(D.m==m)&(D.tf==tf)&(D.variant=='IB')&(D.stop=='structure (swing)')&(D.target=='her target')&D.kind.isin(['FA','TC'])].copy()
        if len(b)==0: continue
        b['t']=pd.to_datetime(b.day)+pd.to_timedelta(b.mn,unit='m'); b=b.sort_values('t')
        keep=[]; los={}
        for k,(dd,rr) in enumerate(zip(b.day,b.r)):
            if los.get(dd,0)>=2: continue
            keep.append(k)
            if rr<=0: los[dd]=los.get(dd,0)+1
        b=b.iloc[keep]
        for p in ('P1','P2'):
            x=b[b.per==p]
            if len(x)<5: continue
            mo=x.t.dt.to_period('M'); months=mo.nunique(); usd=x.r*200; pm=usd.groupby(mo).sum()
            T=pd.DataFrame({'t':x.t,'r':x.r,'risk':200.0}).reset_index(drop=True)
            pr=bfprop.prop(T,pv=1.0,risk_usd=200.0)
            M.append([m,int(tf),p,len(x),r(len(x)/months,1),r((x.r>0).mean()),r(x.r.mean()),r(usd.sum()/months,0),r(pm.max(),0),r(pm.min(),0),r((pm>0).mean()),len(pr),r(pr.count('pass')/len(pr),2)])
S['money']=M
json.dump(S,open('site6/summary.json','w'),separators=(',',':'))
print(len(json.dumps(S))//1024,'KB'); print(M)
