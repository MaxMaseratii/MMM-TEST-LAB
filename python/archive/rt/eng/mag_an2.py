import pandas as pd, numpy as np, glob
OUT='/home/claude/rt/out'
TRG=['T0 limit at the level','T1 LTF body close','T2 LTF rejection candle','T3 LTF GMC','T4 LTF flip (CDLc / CDSc)']
SMN=['trigger candle (T4: new LTF T1 PO4)','LTF swing since touch','HTF protected extreme','fixed 50']
LEV=['P 87.5','MP 75','BAL 50','MD 25','O open']
from core import TYPES
S=[];F=[];DT=[]
cols=['period','htf','ltf','win','trig','smode','lev','ty','stat','R_tgt','R_2R','R_3R','rr0']
for f in glob.glob(f'{OUT}/M_*.parquet'):
    d=pd.read_parquet(f,columns=cols)
    fu=d.groupby(['period','htf','ltf','win','trig','smode']).stat.value_counts(normalize=True).unstack().fillna(0); F.append(fu.reset_index())
    t=d[d.stat==4].copy(); del d
    t['ge2']=t.rr0>=2; t['w_t']=t.R_tgt>0; t['w2']=t.R_2R>0; t['w3']=t.R_3R>0
    t['Rg']=np.where(t.ge2,t.R_tgt,np.nan); t['wg']=np.where(t.ge2,(t.R_tgt>0).astype(float),np.nan)
    agg=dict(trades=('R_tgt','size'),rr_to_target_median=('rr0','median'),pct_target_ge_2R=('ge2','mean'),WR_at_HTF_target=('w_t','mean'),avgR_at_HTF_target=('R_tgt','mean'),
             WR_at_2R=('w2','mean'),avgR_at_2R=('R_2R','mean'),WR_at_3R=('w3','mean'),avgR_at_3R=('R_3R','mean'),trades_if_ge2=('ge2','sum'),WR_if_ge2_at_target=('wg','mean'),avgR_if_ge2_at_target=('Rg','mean'))
    S.append(t.groupby(['period','htf','ltf','win','trig','smode']).agg(**agg).reset_index())
    DT.append(t.groupby(['period','htf','ltf','win','ty','lev','trig','smode']).agg(**agg).reset_index())
def lab(x):
    x['window']=np.where(x.win==0,'next HTF candle','next 2 HTF candles'); x['trigger']=[TRG[i] for i in x.trig]; x['stop']=[SMN[i] for i in x.smode]
    if 'ty' in x: x['type']=[TYPES[i] for i in x.ty]; x['level']=[LEV[i] for i in x.lev]
    return x.drop(columns=[c for c in ['win','trig','smode','ty','lev'] if c in x])
s=lab(pd.concat(S)); s=s[['period','htf','ltf','window','trigger','stop']+[c for c in s.columns if c not in ['period','htf','ltf','window','trigger','stop']]]
s.to_parquet(f'{OUT}/MAG_summary.parquet')
dt=lab(pd.concat(DT)); dt=dt[['period','htf','ltf','window','type','level','trigger','stop']+[c for c in dt.columns if c not in ['period','htf','ltf','window','type','level','trigger','stop']]]
dt.to_parquet(f'{OUT}/MAG_detail.parquet')
fu=lab(pd.concat(F)); fu=fu.rename(columns={0:'no touch',1:'target first (missed)',2:'protected broke first',3:'no trigger',4:'traded',5:'stop too small'})
fu.columns=[str(c) for c in fu.columns]; fu.to_parquet(f'{OUT}/MAG_funnel.parquet')
print('ok')
