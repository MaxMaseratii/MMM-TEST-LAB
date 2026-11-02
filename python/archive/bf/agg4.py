import numpy as np, pandas as pd, bfgrid2 as G
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
D = pd.concat([pd.read_parquet(f'grid2_{m}.parquet') for m in ['NQ','ES','GC','CL']], ignore_index=True)
D['R'] = (D.r1*D.n1 + D.r2*D.n2)/(D.n1+D.n2); D['N']=D.n1+D.n2
base = (D.side=='both')&(D.w==0)&(D.x==0)
# 1 entry ladder: NQ, all hours, PO4 last (st0) and ATR x1 (st3), 1:2 , avg RR P1/P2 per tf
for st in (0,3):
    q = D[base&(D.m=='NQ')&(D.slot=='all hours')&(D.st==st)&(D.t==0)&(D.kind=='CDS/CDL')]
    print('\nNQ all hours both, wait 10,', G.SN[st], '1:2 -> avgRR P1 / P2 (n P1)')
    t = q.pivot_table(index='e', columns='tf', values=['r1','r2'])
    t.index=[G.EN[i] for i in t.index]; print(t.round(2).to_string())
# 2 stops & exits: mean avg RR over all TF x entries per market (CDS vs random side)
q = D[(D.side=='both')&(D.w==0)&(D.slot=='all hours')]
print('\nmean avg RR (P1, P2) over every chart x entry, by stop and target/exit')
t = q.groupby(['m','kind','st']).agg(r1=('r1','mean'), r2=('r2','mean')).unstack('kind'); t.index=[(a,G.SN[b]) for a,b in t.index]; print(t.round(3).to_string())
t = q.groupby(['m','kind','t','x']).agg(r1=('r1','mean'), r2=('r2','mean')).unstack('kind'); t.index=[(a,G.TN[b],G.XN[c]) for a,b,c in t.index]; print(t.round(3).to_string())
# 3 share of combos with avgRR>0 both periods, n>=30/20
q = D[(D.n1>=30)&(D.n2>=20)]
print('\nshare of combos positive in both periods'); print(q.assign(pos=(q.r1>0)&(q.r2>0)).groupby(['m','kind']).pos.mean().unstack().round(3))
