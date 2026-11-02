import pandas as pd, numpy as np
pd.set_option('display.width',320); pd.set_option('display.max_rows',400); pd.set_option('display.max_colwidth',60)
OUT='/home/claude/rt/out'
c=pd.read_parquet(f'{OUT}/ALL_sess.parquet')
K=['tf','family','signal','side','session','entry','stop','target','exit']
o=c[c.period=='old']
f=c[((c.period=='fresh')&c.tf.isin(['5m','10m','15m']))|((c.period=='fresh10')&c.tf.isin(['1h','4h','D']))]
m=o.merge(f,on=K,suffixes=('_o','_f'))
m['minR']=np.minimum(m.avgR_o,m.avgR_f)
m.to_parquet(f'{OUT}/ALL_merged.parquet')
surv=m[(m.trades_o>=100)&(m.avgR_o>0)&(m.t_o>=2.5)&(m.trades_f>=30)&(m.avgR_f>0)]
print('cells',len(m),'survivors',len(surv))
print(surv.groupby(['family','tf']).size())
cols=K+['trades_o','WR_o','PF_o','avgR_o','t_o','trades_f','WR_f','PF_f','avgR_f','t_f']
print(surv.sort_values('minR',ascending=False).groupby(['family','tf']).head(4)[cols].round(2).to_string(index=False))
