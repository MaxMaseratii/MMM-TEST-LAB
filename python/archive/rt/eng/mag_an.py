import pandas as pd, numpy as np, glob
pd.set_option('display.width',320); pd.set_option('display.max_rows',500)
from core import TYPES
OUT='/home/claude/rt/out'
LEV=['P 87.5','MP 75','BAL 50','MD 25','O open']; TRG=['T0 limit at the level','T1 LTF body close','T2 LTF rejection candle','T3 LTF GMC','T4 LTF flip (CDLc / CDSc)']
SMN=['trigger candle (T4: new LTF T1 PO4)','LTF swing since touch','HTF protected extreme','fixed 50']
d=pd.concat([pd.read_parquet(f) for f in glob.glob(f'{OUT}/M_*.parquet')],ignore_index=True)
d['type']=[TYPES[t] for t in d.ty]; d['level']=[LEV[i] for i in d.lev]; d['trigger']=[TRG[i] for i in d.trig]; d['stop']=[SMN[i] for i in d.smode]
d['window']=np.where(d.win==0,'next HTF candle','next 2 HTF candles')
t=d[d.stat==4].copy()
t['ge2']=t.rr0>=2
def agg(x):
    n=len(x)
    o=dict(trades=n, rr_to_target_median=x.rr0.median(), pct_target_ge_2R=x.ge2.mean(),
           WR_at_HTF_target=(x.R_tgt>0).mean(), avgR_at_HTF_target=x.R_tgt.mean(),
           WR_at_2R=(x.R_2R>0).mean(), avgR_at_2R=x.R_2R.mean(), WR_at_3R=(x.R_3R>0).mean(), avgR_at_3R=x.R_3R.mean())
    y=x[x.ge2]
    o.update(trades_if_ge2=len(y), WR_if_ge2_at_target=(y.R_tgt>0).mean() if len(y) else np.nan, avgR_if_ge2_at_target=y.R_tgt.mean() if len(y) else np.nan)
    return pd.Series(o)
g=t.groupby(['period','htf','ltf','window','trigger','stop']).apply(agg).reset_index()
g.to_parquet(f'{OUT}/MAG_summary.parquet')
gt=t.groupby(['period','htf','ltf','window','type','level','trigger','stop']).apply(agg).reset_index()
gt.to_parquet(f'{OUT}/MAG_detail.parquet')
# status funnel
f=d.groupby(['period','htf','ltf','window','trigger','stop']).stat.value_counts(normalize=True).unstack().fillna(0)
f.columns=[{0:'no touch',1:'target first (missed)',2:'protected broke first',3:'no trigger',4:'traded',5:'stop too small'}[c] for c in f.columns]
f.reset_index().to_parquet(f'{OUT}/MAG_funnel.parquet')
x=g[(g.window=='next HTF candle')]
print(x[['period','htf','ltf','trigger','stop','trades','rr_to_target_median','pct_target_ge_2R','WR_at_HTF_target','avgR_at_HTF_target','WR_at_2R','avgR_at_2R','trades_if_ge2','WR_if_ge2_at_target','avgR_if_ge2_at_target']].round(2).to_string(index=False))
