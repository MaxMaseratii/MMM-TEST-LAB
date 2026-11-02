import time, bfrun, numpy as np
t0=time.time()
bfrun.run_market('NQ', tag='test', tfs=[15])
print('total', time.time()-t0)
import pandas as pd
R=pd.read_parquet('grid_test_NQ.parquet')
x=R[(R.kind=='CDS/CDL')&(R.slot=='all hours')&(R.side=='both')&(R.e==0)&(R.st==0)&(R.t==2)&(R.h==0)]
print(x[['x','n1','wr1','r1','t1','n2','wr2','r2','t2']].round(3).to_string())
