import numpy as np, pandas as pd, json
from grid import DNAME, SNAME, TGT, XNAME, FAM
A = np.load('grid_acc.npy')   # [8, 12 shapes, 3 ap, 7 d, 13 st, 6 t, 4 x, 6 stats]
TFS = ['5m','15m','1h','4h']; APS = ['C3','GMU3','C1']
SH = [f'{f} {w}' for f in FAM for w in ('with','against')]
def st(a):
    n, s1, s2, w, gw, gl = a
    if n < 2: return n, np.nan, np.nan, np.nan, np.nan
    m = s1 / n; var = max(s2 / n - m * m, 1e-12) * n / (n - 1)
    return int(n), round(100 * w / n, 1), round(gw / gl, 2) if gl > 0 else np.nan, round(m, 3), round(m / np.sqrt(var) * np.sqrt(n), 2)
rows = []
for ti, tf in enumerate(TFS):
    o = A[ti]; f = A[4 + ti]
    for shi in range(13):
        so = o.sum(axis=0) if shi == 12 else o[shi]; sf = f.sum(axis=0) if shi == 12 else f[shi]
        shn = 'ALL' if shi == 12 else SH[shi]
        for ap in range(3):
            for d in range(7):
                for s_ in range(13):
                    for t in range(6):
                        for x in range(4):
                            a = so[ap, d, s_, t, x]; b = sf[ap, d, s_, t, x]
                            if a[0] < 30: continue
                            no, wo, po, mo, to = st(a); nf, wf, pf, mf, tf_ = st(b)
                            rows.append((tf, shn, APS[ap], DNAME[d], SNAME[s_], f'1:{TGT[t]:g}', XNAME[x], no, wo, po, mo, to, nf, wf, pf, mf, tf_))
D = pd.DataFrame(rows, columns=['tf','c3','range','entry','stop','target','exit','n_old','wr_old','pf_old','avg_old','t_old','n_26','wr_26','pf_26','avg_26','t_26'])
D.to_parquet('grid_table.parquet')
print('rows', len(D))
P = D[(D.n_old >= 100) & (D.n_26 >= 40)]
both = P[(P.t_old >= 2) & (P.t_26 >= 2)]
loose = P[(P.t_old >= 2) & (P.avg_26 > 0) & (P.t_26 >= 1)]
print('tested (n ok):', len(P), ' pass t>=2 both:', len(both), ' loose:', len(loose))
print(both.groupby(['tf','c3']).size())
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
print(both.sort_values('t_26', ascending=False).head(60).to_string())
# ALL shapes: best by tf
for tf in TFS:
    q = P[(P.tf == tf) & (P.c3 == 'ALL')].copy(); q['tmin'] = q[['t_old','t_26']].min(axis=1)
    print('\n== ALL shapes best min-t', tf); print(q.sort_values('tmin', ascending=False).head(8).to_string())
