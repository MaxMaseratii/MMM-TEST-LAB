import pandas as pd, numpy as np
pd.set_option('display.width',320); pd.set_option('display.max_rows',400); pd.set_option('display.max_colwidth',70)
OUT='/home/claude/rt/out'
m=pd.read_parquet(f'{OUT}/ALL_merged.parquet')
T=['tf','family','signal','side','session','entry']
mm=m[(m.trades_o>=50)&(m.trades_f>=20)]
th=mm.groupby(T).agg(cells=('avgR_o','size'),n_o=('trades_o','median'),n_f=('trades_f','median'),
    med_o=('avgR_o','median'),med_f=('avgR_f','median'),pos_o=('avgR_o',lambda x:(x>0).mean()),pos_f=('avgR_f',lambda x:(x>0).mean())).reset_index()
th['minmed']=np.minimum(th.med_o,th.med_f)
th.to_parquet(f'{OUT}/THEMES.parquet')
# baseline: every candle of a side (RANDOM-like) = all MMCB signals pooled, entry C
c=pd.read_parquet(f'{OUT}/ALL_sess.parquet')
b=c[(c.family=='MMCB')&(c.entry=='C')]
num=['trades','_w','_s','_s2','_gw','_gl']
bb=b.groupby(['period','tf','side','session','stop','target','exit'])[num].sum().reset_index()
bb['avgR']=bb._s/bb.trades
base=bb.groupby(['period','tf','side','session']).avgR.median().unstack('period')
print('BASELINE every candle at its close (median over stop x target x exit)'); print(base.round(3).to_string())
good=th[(th.med_o>0)&(th.med_f>0)&(th.cells>=50)].sort_values('minmed',ascending=False)
print(len(th),'themes; positive both',len(good))
print(good.head(60).round(3).to_string(index=False))
