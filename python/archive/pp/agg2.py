import numpy as np, pandas as pd, engine
from agg import table
A = pd.read_parquet('all_trades.parquet')
B = A[A.run == 'base']
out = {}
out['base'] = table(B, ['m', 'tf', 'setup'])
out['side'] = table(B, ['m', 'tf', 'setup', 'side'])
out['winsplit'] = table(B, ['m', 'tf', 'setup', 'win'])
W = A[A.run == 'win']
w1 = table(W, ['m', 'tf', 'setup', 'win']); w2 = table(W.assign(win=9), ['m', 'tf', 'setup', 'win'])
out['winrun'] = pd.concat([w1, w2], ignore_index=True)
out['flip'] = table(A[A.run == 'flip'], ['m', 'tf', 'setup'])
out['fst'] = table(A[A.run == 'fst'], ['m', 'tf', 'setup'])
out['t2R'] = table(B, ['m', 'tf', 'setup'], 'pl2R', 'rr2R')
out['t3R'] = table(B, ['m', 'tf', 'setup'], 'pl3R', 'rr3R')
for k in ('vside', 'vcol', 'stack', 'htf'):
    out[k] = table(B, ['m', 'tf', 'setup', k])
    out[k + '_win'] = table(W.assign(win=9), ['m', 'tf', 'setup', k])
pd.to_pickle(out, 'tables.pkl')
print('cells and verdicts per family (setups 0-10 vs random controls 11-12):')
for k, T in out.items():
    s = T[T.setup <= 10].v.value_counts(); r = T[T.setup >= 11].v.value_counts()
    print(f"{k:10s} cells {len(T[T.setup<=10]):5d}  HOLDS {s.get('HOLDS',0):3d} watch {s.get('watch',0):4d} | controls cells {len(T[T.setup>=11]):4d} HOLDS {r.get('HOLDS',0):2d} watch {r.get('watch',0):3d}")
for k, T in out.items():
    h = T[T.v == 'HOLDS']
    if len(h):
        h = h.copy(); h['s'] = h.setup.map(lambda i: engine.SETUPS[i][:28])
        cols = [c for c in h.columns if c in ('m','tf','s','side','win','vside','vcol','stack','htf')] + ['P1_n','P1_pts','P1_rr','P1_t','P2_n','P2_pts','P2_rr','P2_t','ALL_wr','ALL_pf']
        print('==', k); print(h[cols].round(3).to_string())
