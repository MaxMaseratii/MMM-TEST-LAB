import pandas as pd, numpy as np, json
T = pd.read_parquet('zone2_trades.parquet'); X = pd.read_parquet('zone2_react.parquet')
def st(r):
    r = np.asarray(r, float); n = len(r)
    if n < 2: return dict(n=n, wr=None, pf=None, av=None, t=None)
    w = r[r > 0].sum(); lo = -r[r < 0].sum(); sd = r.std(ddof=1)
    return dict(n=n, wr=round(100*(r > 0).mean(), 1), pf=round(w/lo, 2) if lo > 0 else None, av=round(r.mean(), 3), t=round(r.mean()/sd*np.sqrt(n), 2) if sd > 0 else None)
G = T.groupby(['opp', 'tf', 'kind', 'entry', 'stop', 'tgt', 'exit', 'period']).R
A = G.agg(n='size', av='mean', sd='std', wr=lambda r: (r > 0).mean(), gw=lambda r: r[r > 0].sum(), gl=lambda r: -r[r < 0].sum()).reset_index()
A['t'] = A.av / A.sd * np.sqrt(A.n); A['pf'] = A.gw / A.gl
W = A.pivot_table(index=['opp', 'tf', 'kind', 'entry', 'stop', 'tgt', 'exit'], columns='period', values=['n', 'av', 't', 'wr', 'pf']).reset_index()
W.columns = ['_'.join([c for c in col if c]) if isinstance(col, tuple) else col for col in W.columns]
W['pass'] = (W.t_old >= 2) & (W.t_fresh >= 2) & (W.n_old >= 30) & (W.n_fresh >= 20)
W.to_parquet('zone2_grid.parquet')
print('pairings', len(W), 'PASS', int(W['pass'].sum()))
print(W[W['pass']].sort_values('t_fresh', ascending=False)[['opp','tf','entry','stop','tgt','exit','n_old','n_fresh','wr_old','wr_fresh','av_old','av_fresh','t_old','t_fresh']].head(40).to_string())
# family score: share of pairings positive in both periods, mean avg RR
def fam(e):
    if 'wrong zone' in e: return '3 wrong zone (control)'
    if 'balanced' in e: return '2 balanced (no-trade)'
    if 'FVA' in e: return '4 FVA after break'
    return '1 predicted zone'
W['fam'] = W.entry.map(fam)
print(W.groupby(['opp','fam']).agg(pairs=('av_old','size'), mean_old=('av_old','mean'), mean_fresh=('av_fresh','mean'), both_pos=('av_old', lambda s: 0), pas=('pass','sum')).round(3))
pos = W.assign(bp=(W.av_old > 0) & (W.av_fresh > 0)).groupby(['opp','fam']).bp.mean().round(3); print(pos)
# 50 pt 1:2 stop/target, OPP engine
S = W[(W.stop=='S50') & (W.tgt==2.0) & (W.exit=='stop/target')]
print(S[S.opp].sort_values(['tf','entry'])[['tf','entry','n_old','n_fresh','wr_old','wr_fresh','pf_old','pf_fresh','av_old','av_fresh','t_old','t_fresh']].round(3).to_string())
# reaction
R = X.groupby(['opp','tf','kind','entry','X','period']).win.agg(['mean','size']).reset_index()
R['z'] = (R['mean'] - 0.5) / np.sqrt(0.25 / R['size'])
RW = R.pivot_table(index=['opp','tf','kind','entry','X'], columns='period', values=['mean','size','z']).reset_index()
RW.columns = ['_'.join([c for c in col if c]) if isinstance(col, tuple) else col for col in RW.columns]
RW.to_parquet('zone2_react_tab.parquet')
print(RW[(RW.opp) & (RW.X == 50)].round(3).to_string())
# walk-forward: best pairing per entry/tf picked on old t, its fresh result
wf = W[(W.n_old >= 30) & (W.n_fresh >= 20)].sort_values('t_old', ascending=False).groupby(['opp','tf','entry']).head(1)
print(wf[wf.opp].groupby('fam')[['av_old','av_fresh']].mean().round(3))
print(wf[wf.opp].sort_values(['fam','tf'])[['tf','entry','stop','tgt','exit','av_old','av_fresh','t_old','t_fresh']].round(2).to_string())
