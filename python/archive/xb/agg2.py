import pickle, numpy as np, pandas as pd
from grid2 import ENAME, SNAME, TGT, XNAME, GNAME
from core import stats
O = pickle.load(open('grid2.pkl', 'rb'))
TFS = ['5m','15m','1h','4h']; SIDES = ['BULL','BEAR']
def st(a):
    n, s1, s2, w, gw, gl = a.T
    with np.errstate(all='ignore'):
        m = s1 / n; var = np.maximum(s2 / n - m * m, 1e-12) * n / np.maximum(n - 1, 1)
        return n, 100 * w / n, np.where(gl > 0, gw / gl, np.nan), m, m / np.sqrt(var) * np.sqrt(n)
recs = []
for tf in TFS:
    ao = O[('old', tf)][0]; af = O[('fresh', tf)][0]
    G, S, E, Sx, T, X, _ = ao.shape
    idx = np.indices((G, S, E, Sx, T, X)).reshape(6, -1).T
    no, wo, po, mo, to = st(ao.reshape(-1, 6)); nf, wf, pf, mf, tf_ = st(af.reshape(-1, 6))
    df = pd.DataFrame({'tf': tf, 'grp': idx[:, 0], 'side': idx[:, 1], 'entry': idx[:, 2], 'stop': idx[:, 3], 'target': idx[:, 4], 'exit': idx[:, 5],
                       'n_old': no, 'wr_old': wo, 'pf_old': po, 'avg_old': mo, 't_old': to, 'n_26': nf, 'wr_26': wf, 'pf_26': pf, 'avg_26': mf, 't_26': tf_})
    recs.append(df[(df.n_old >= 30) & (df.n_26 >= 10)])
D = pd.concat(recs, ignore_index=True)
D.to_parquet('grid2_table.parquet'); print('rows', len(D))
# fill counts per GMU (for fill %)
for tf in TFS:
    print(tf, 'GMUs old', O[('old', tf)][1][0], '2026', O[('fresh', tf)][1][0])
# random baseline per side
for tf in TFS:
    print(tf, 'RANDOM long/short 50pt 1:2:', [ (stats(O[(p, tf)][2][0])['avg'], stats(O[(p, tf)][2][1])['avg']) for p in ('old','fresh')])
