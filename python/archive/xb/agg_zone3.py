import pandas as pd, numpy as np
T = pd.read_parquet('zone3_trades.parquet'); X = pd.read_parquet('zone3_react.parquet')
T = T[T.kind == 'A inside XB']; X = X[X.kind == 'A inside XB']
T['with'] = np.where(T.side == T.xbdir, 'WITH box', 'AGAINST box'); X['with'] = np.where(X.entry.str.startswith('SELL'), -1, 1)
X['with'] = np.where(X['with'] == X.xbdir, 'WITH box', 'AGAINST box')
# entry position from the side of the trade: where in the block you enter
POS = {'SELL XB high': '1 XB edge (far)', 'SELL XBB middle': '2 outer zone middle', 'SELL XBB bottom (balanced top)': '3 outer zone edge = Balanced edge',
       'SELL balanced middle (no-trade zone)': '4 Balanced middle', 'SELL XBS top (wrong zone)': '5 Balanced far edge', 'SELL XBS middle': '6 far zone middle',
       'BUY XB low': '1 XB edge (far)', 'BUY XBS middle': '2 outer zone middle', 'BUY XBS top (balanced bottom)': '3 outer zone edge = Balanced edge',
       'BUY balanced middle (no-trade zone)': '4 Balanced middle', 'BUY XBB bottom (wrong zone)': '5 Balanced far edge', 'BUY XBB middle': '6 far zone middle'}
T['pos'] = T.entry.map(POS); X['pos'] = X.entry.map(POS)
T['box'] = np.where(T.xbdir == -1, 'BEARISH XB', 'BULLISH XB'); X['box'] = np.where(X.xbdir == -1, 'BEARISH XB', 'BULLISH XB')
def st(r):
    r = np.asarray(r, float); n = len(r)
    if n < 3: return (n, np.nan, np.nan, np.nan, np.nan)
    w = r[r > 0].sum(); lo = -r[r < 0].sum(); sd = r.std(ddof=1)
    return (n, 100 * (r > 0).mean(), w / lo if lo > 0 else np.nan, r.mean(), r.mean() / sd * np.sqrt(n) if sd > 0 else np.nan)
# A. 50 pt 1:2 stop/target
S = T[(T.stop == 'S50') & (T.tgt == 2.0) & (T.exit == 'stop/target')]
rows = []
for (box, w, tf, pos, ent), g in S.groupby(['box', 'with', 'tf', 'pos', 'entry']):
    o = st(g[g.period == 'old'].R); f = st(g[g.period == 'fresh'].R)
    rows.append(dict(box=box, w=w, tf=tf, pos=pos, entry=ent, n1=o[0], n2=f[0], wr1=o[1], wr2=f[1], pf1=o[2], pf2=f[2], av1=o[3], av2=f[3], t1=o[4], t2=f[4]))
A = pd.DataFrame(rows); A.to_parquet('zone3_s50.parquet')
# B. all pairings: mean avg RR, share positive in both, passes
G = T.groupby(['box', 'with', 'tf', 'pos', 'entry', 'stop', 'tgt', 'exit', 'period']).R.agg(['size', 'mean', 'std']).reset_index()
G['t'] = G['mean'] / G['std'] * np.sqrt(G['size'])
W = G.pivot_table(index=['box', 'with', 'tf', 'pos', 'entry', 'stop', 'tgt', 'exit'], columns='period', values=['size', 'mean', 't']).reset_index()
W.columns = ['_'.join([c for c in col if c]) for col in W.columns]
W['pass'] = (W.t_old >= 2) & (W.t_fresh >= 2) & (W.size_old >= 30) & (W.size_fresh >= 20)
W['bp'] = (W.mean_old > 0) & (W.mean_fresh > 0)
W.to_parquet('zone3_grid.parquet')
B = W.groupby(['box', 'with', 'pos']).agg(pairs=('pass', 'size'), passes=('pass', 'sum'), both_pos=('bp', 'mean'), m1=('mean_old', 'mean'), m2=('mean_fresh', 'mean')).reset_index()
B.to_parquet('zone3_fam.parquet')
# C. coin flip
C = X[X.X == 50].groupby(['box', 'with', 'tf', 'pos', 'entry', 'period']).win.agg(['mean', 'size']).reset_index()
C.to_parquet('zone3_react_tab.parquet')
CA = X[X.X == 50].groupby(['box', 'with', 'pos', 'period']).win.agg(['mean', 'size']).unstack('period').round(3)
pd.set_option('display.width', 250)
print(B.round(3).to_string())
print(CA.to_string())
print(A[A.w == 'WITH box'].sort_values(['box', 'tf', 'pos']).round(3)[['box', 'tf', 'pos', 'n1', 'n2', 'wr1', 'wr2', 'av1', 'av2', 't1', 't2']].to_string(index=False))
print('PASSES', W[W['pass']][['box', 'with', 'tf', 'entry', 'stop', 'tgt', 'exit', 'size_old', 'size_fresh', 'mean_old', 'mean_fresh', 't_old', 't_fresh']].round(3).to_string())
