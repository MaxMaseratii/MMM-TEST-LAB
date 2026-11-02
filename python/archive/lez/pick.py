import pandas as pd, numpy as np, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim import cfg_names, STOPS
from analyze2 import SUB
pd.set_option('display.width',300); pd.set_option('display.max_columns',50); pd.set_option('display.max_colwidth',30)
CN=cfg_names()
T=pd.read_parquet('table2.parquet'); F=pd.read_parquet('families.parquet')
fam=F[(F.both>=0.84)&(F.n_o>=150)&(F.n_f>=20)]
key=['ltf','level','entry','held','filter']
P=T.merge(fam[key+['both','o_med','f_med']],on=key)
P=P[(P.o_t>=2)&(P.f_avg>0)]
best=P.sort_values('b_t',ascending=False).groupby(key).head(1)
print(best[key+['stop','boxexit','target','trail','both','o_n','o_wr','o_avg','o_t','f_n','f_wr','f_avg','f_t','b_t']].round(2).to_string())
best.to_parquet('best.parquet')
