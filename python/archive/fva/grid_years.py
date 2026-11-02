import sys, pickle, pandas as pd, numpy as np
sys.path.insert(0,'/home/claude/fva')
from fva_grid import segment, flatten, replica_run, OUT
m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl','rb'))
out=[]
for tf, mins in (('15m',15),('1h',60)):
    sig=bars[tf]; setups=replica_run(sig)
    for y in (2023,2024,2025):
        a,c=segment(sig,setups,m1,bars['D'],True,mins,7,pd.Timestamp(f'{y-1}-12-31 18:00'),pd.Timestamp(f'{y}-12-31 17:00'))
        df=flatten(a,c,(f'old{y}',tf)); df=df[df.type.isin(['PES/PEL+','CDL/CDS+','Fail+','Fail','BuX/BeX'])]
        out.append(df); print(tf,y,len(df),flush=True)
pd.concat(out).to_parquet(f'{OUT}/years.parquet')
