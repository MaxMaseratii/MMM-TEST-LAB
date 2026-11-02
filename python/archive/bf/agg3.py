import sys, numpy as np, pandas as pd
import bfgrid2 as G
ms = sys.argv[1:] or ['NQ','ES','GC','CL']
D = pd.concat([pd.read_parquet(f'grid2_{m}.parquet') for m in ms], ignore_index=True)
D['pass'] = (D.t1 >= 2) & (D.t2 >= 2) & (D.n1 >= 30) & (D.n2 >= 20)
print(D.groupby(['m','kind']).agg(rows=('pass','size'), passes=('pass','sum')).assign(rate=lambda x: x.passes/x.rows))
def nm(r): return f"{r.m} {r.tf}m {r.side} {r.slot} | {G.WN[r.w]} | {G.EN[r.e]} | {G.SN[r.st]} | {G.TN[r.t]} | {G.XN[r.x]}"
P = D[D.pass_ if False else D['pass'] & (D.kind=='CDS/CDL')].copy()
P['tmin'] = P[['t1','t2']].min(1)
for _, r in P.sort_values('tmin', ascending=False).head(25).iterrows():
    print(f"{nm(r)} | n {r.n1:.0f}/{r.n2:.0f} wr {r.wr1:.2f}/{r.wr2:.2f} avgRR {r.r1:+.3f}/{r.r2:+.3f} pf {r.pf1:.2f}/{r.pf2:.2f} t {r.t1:.1f}/{r.t2:.1f}")
