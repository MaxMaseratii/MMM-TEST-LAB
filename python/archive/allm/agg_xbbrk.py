"""Aggregate the grid accumulators into tables."""
import sys, pickle, json, os, numpy as np, pandas as pd
import grid
FILES = sys.argv[1].split(',')
strats_all, acc_all, counts = [], {}, {}
for f in FILES:
    P = pickle.load(open(f, 'rb'))
    for mk, a in P['acc'].items():
        for k, s in enumerate(P['strats']):
            acc_all[(mk, s)] = a[k]
    counts.update(P['counts'])
def st(a):
    n, s1, s2, w, gw, gl = [a[..., k] for k in range(6)]
    with np.errstate(all='ignore'):
        m = s1 / n; var = np.maximum(s2 / n - m * m, 1e-12) * n / np.maximum(n - 1, 1)
        return n, 100 * w / n, np.where(gl > 0, gw / gl, np.nan), m, m / np.sqrt(var) * np.sqrt(n)
rows = []
for (mk, s), a in acc_all.items():
    if a[..., 0].sum() == 0: continue
    for sd in (0, 1):
        A1 = a[sd, 0]; A2 = a[sd, 1]
        n1, w1, p1, m1, t1 = st(A1); n2, w2, p2, m2, t2 = st(A2)
        idx = np.indices(A1.shape[:-1]).reshape(4, -1).T
        df = pd.DataFrame({'market': mk, 'strat': s, 'side': sd, 'e': idx[:, 0], 'st': idx[:, 1], 't': idx[:, 2], 'x': idx[:, 3],
                           'n1': n1.ravel(), 'wr1': w1.ravel(), 'pf1': p1.ravel(), 'avg1': m1.ravel(), 't1': t1.ravel(),
                           'n2': n2.ravel(), 'wr2': w2.ravel(), 'pf2': p2.ravel(), 'avg2': m2.ravel(), 't2': t2.ravel()})
        rows.append(df[(df.n1 > 0) | (df.n2 > 0)])
D = pd.concat(rows, ignore_index=True)
D.to_parquet('grid_xbbrk.parquet')
print('rows', len(D))
