import numpy as np, pandas as pd, bfgrid5 as G
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
A=pd.concat([pd.read_parquet(f'grid5_{m}.parquet') for m in ['NQ','ES','GC','CL']],ignore_index=True)
key=['m','tf','side','slot','e','st','t','x']
R=A[A.kind=='RANDOM side'][key+['r1','r2','t1','t2']].rename(columns=lambda c: c if c in key else 'rs_'+c)
RT=A[A.kind=='RANDOM with trend'][key+['r1','r2','t1','t2']].rename(columns=lambda c: c if c in key else 'rt_'+c)
# the old TL touch-hold, market entry, fixed 50 (scaled), 1:2, out at next flip, all hours: every market x tf x side
q=A[(A.kind=='old TL touch-hold')&(A.slot==0)&(A.e==0)&(A.st==3)&(A.x==1)&(A.t==1)].merge(R,on=key,how='left').merge(RT,on=key,how='left')
print(q[['m','tf','side','n1','n2','wr1','wr2','r1','r2','t1','t2','rs_r1','rs_r2','rt_r1','rt_r2']].round(2).to_string(index=False))
