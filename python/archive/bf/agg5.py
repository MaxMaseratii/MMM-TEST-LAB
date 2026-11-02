import numpy as np, pandas as pd, bfgrid2 as G
pd.set_option('display.width',250); pd.set_option('display.max_rows',500)
A=pd.concat([pd.read_parquet(f'grid2_{m}.parquet') for m in ['NQ','ES','GC','CL']],ignore_index=True)
A['ok']=(A.n1>=30)&(A.n2>=20); A['pass']=A.ok&(A.t1>=2)&(A.t2>=2); A['mt']=np.minimum(A.t1,A.t2)
# A per market x tf
g=A[A.ok].groupby(['m','tf','kind']).agg(combos=('pass','size'),passes=('pass','sum'),pos=('r1',lambda s:0)).reset_index()
pos=A[A.ok].assign(p=lambda d:(d.r1>0)&(d.r2>0)).groupby(['m','tf','kind']).p.mean().reset_index()
g=g.drop(columns='pos').merge(pos,on=['m','tf','kind'])
print(g.pivot_table(index=['m','tf'],columns='kind',values=['passes','p']).round(3).to_string())
# B reference trade per tf x stop: market C2, 1:2, stop/target only, both, all hours
q=A[(A.kind=='CDS/CDL')&(A.side=='both')&(A.slot=='all hours')&(A.w==0)&(A.e==0)&(A.t==0)&(A.x==0)&(A.m=='NQ')]
q=q.assign(stop=[G.SN[i] for i in q.st])
print(q[['tf','stop','n1','wr1','r1','pf1','t1','n2','wr2','r2','pf2','t2']].round(2).to_string(index=False))
