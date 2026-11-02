import numpy as np, pandas as pd, bfgrid5 as G
pd.set_option('display.width',250); pd.set_option('display.max_rows',300)
A=pd.concat([pd.read_parquet(f'grid5_{m}.parquet') for m in ['NQ','ES','GC','CL']],ignore_index=True)
A['ok']=(A.n1>=30)&(A.n2>=20); A['pass']=A.ok&(A.t1>=2)&(A.t2>=2)
g=A[A.ok].assign(p=lambda d:(d.r1>0)&(d.r2>0)).groupby(['kind']).agg(c=('pass','size'),ps=('pass','sum'),pos=('p','mean'))
g['rate']=g.ps/g.c; print(g)
print(A[A['pass']].groupby(['m','kind']).size())
P=A[A['pass']&~A.kind.str.startswith('RANDOM')].assign(mt=lambda d:np.minimum(d.t1,d.t2)).sort_values('mt',ascending=False)
for _,r in P.head(40).iterrows(): print(f"{r.m} {r.tf}m {r.kind} | {r.side} {['all','0945-12'][r.slot]} | {G.EN[r.e]} | {G.SN[r.st]} | {G.TN[r.t]} | {G.XN[r.x]} | n {r.n1:.0f}/{r.n2:.0f} wr {r.wr1:.2f}/{r.wr2:.2f} RR {r.r1:+.2f}/{r.r2:+.2f} pf {r.pf1:.2f}/{r.pf2:.2f} t {r.t1:.1f}/{r.t2:.1f}")
