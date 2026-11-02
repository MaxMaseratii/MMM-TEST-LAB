import numpy as np, pandas as pd, bfgrid3 as G
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
D=pd.read_parquet('grid3_all.parquet')
D['ok']=(D.n1>=30)&(D.n2>=20); D['pass']=D.ok&(D.t1>=2)&(D.t2>=2)
print(D[D.ok].groupby(['m','kind'],observed=True).agg(c=('pass','size'),p=('pass','sum')))
print(D[D.ok&D['pass']].groupby(['m','tf','kind'],observed=True).size())
B=D[(D.seq==0)&(D.slot==0)]
for col,names in (('b',G.BN),('c',G.CN)):
    g=B.groupby(['m','kind',col],observed=True)[['r1','r2']].mean().unstack('kind'); print(g.round(3))
# per tf NQ rule table: market, PO4 last & fixed 50, 1:2, stop/target
q=B[(B.m=='NQ')&(B.kind=='cds')&(B.e==0)&(B.t==0)&(B.x==0)&(B.st.isin([0,8]))]
print(q.pivot_table(index=['st','tf'],columns=['b','c'],values='r1').round(2).iloc[:, :10])
