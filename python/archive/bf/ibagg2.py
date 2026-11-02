import numpy as np, pandas as pd, sys
def st(x):
    x=x.dropna(); n=len(x)
    if n<2: return dict(n=n)
    pos=x[x>0].sum(); neg=-x[x<=0].sum()
    return dict(n=n,wr=(x>0).mean(),avg=x.mean(),pf=pos/neg if neg>0 else np.nan,t=x.mean()/x.std(ddof=1)*np.sqrt(n))
pd.set_option('display.width',250)
D=pd.read_parquet('ibtest.parquet')
D=D[~((D.variant=='IBc')&(D.kind=='TC'))]
def show(df,label):
    a=[]
    for p in ('P1','P2'):
        x=df[df.per==p]; s=st(x.r); a.append(f"{p}: n {s.get('n',0):.0f} WR {s.get('wr',np.nan):.0%} avgRR {s.get('avg',np.nan):+.2f} PF {s.get('pf',np.nan):.2f} t {s.get('t',np.nan):.1f} | rand {x.rr.mean():+.2f}")
    print(f"{label:70s} " + ' || '.join(a))
N=D[(D.m=='NQ')&(D.stop=='structure (swing)')]
for tf in (1,5):
    print('--- NQ',tf,'m')
    b=N[(N.tf==tf)&(N.variant=='IB')]
    show(b[(b.kind=='TC')&(b.target=='her target')],'TC her target (IB edge)')
    show(b[(b.kind=='TC')&(b.target=='her target')&b.vwOK],'TC her target + VWAP at IB mid')
    show(b[(b.kind=='FA')&(b.target=='her target')],'FA her target (IB mid)')
    show(b[(b.kind=='FA')&(b.target=='her target')&b.aligned],'FA her target, with the IB trend')
    show(b[(b.kind=='FA')&(b.target=='her target')&~b.aligned],'FA her target, against the IB trend')
    show(b[(b.kind=='FA')&(b.target=='1R')],'FA 1R (best win-rate shape)')
    c=N[(N.tf==tf)&(N.variant=='ASIA')]
    show(c[(c.kind=='AF')&(c.target=='3R')],'Asia sweep-fade 3R')
    show(c[(c.kind=='AB')&(c.target=='3R')],'Asia breakout-retest 3R')
