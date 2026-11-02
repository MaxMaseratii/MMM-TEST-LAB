import numpy as np, pandas as pd, sys
pd.set_option('display.width', 260); pd.set_option('display.max_rows', 400)
D = pd.read_parquet('lvtest.parquet')
D['cb'] = np.where(D.conf.fillna(0) >= 2, '3+ levels', np.where(D.conf.fillna(0) >= 1, '2 levels', '1 level'))


def st(x):
    x = x.dropna(); n = len(x)
    if n < 2: return dict(n=n, wr=np.nan, avg=np.nan, pf=np.nan, t=np.nan)
    pos = x[x > 0].sum(); neg = -x[x <= 0].sum()
    return dict(n=n, wr=(x > 0).mean(), avg=x.mean(), pf=pos / neg if neg > 0 else np.nan, t=x.mean() / x.std(ddof=1) * np.sqrt(n))


def line(df, label):
    a = []
    for p in ('P1', 'P2'):
        x = df[df.per == p]; s = st(x.r); rs = st(x.rr)
        a.append(f"{p}: n {s['n']:5.0f} WR {s['wr']:4.0%} avgRR {s['avg']:+.2f} PF {s['pf']:.2f} t {s['t']:+.1f} | rand {rs['avg']:+.2f}")
    print(f"{label:60s} " + ' || '.join(a))


def grid(df, by):
    out = []
    for k, g in df.groupby(by):
        row = dict(zip(by, k if isinstance(k, tuple) else (k,)))
        for p in ('P1', 'P2'):
            x = g[g.per == p]; s = st(x.r); rs = st(x.rr)
            row.update({f'{a}{p[1]}': b for a, b in s.items()}); row[f'rand{p[1]}'] = rs['avg']; row[f'rt{p[1]}'] = rs['t']
        out.append(row)
    return pd.DataFrame(out)


if __name__ == '__main__':
    L = D[D.variant == 'LEVELS']
    G = grid(L, ['m', 'tf', 'kind', 'grp', 'trig', 'cb', 'stop', 'target'])
    ok = (G.n1 >= 30) & (G.n2 >= 30)
    pas = ok & (G.t1 >= 2) & (G.t2 >= 2); rpas = ok & (G.rt1 >= 2) & (G.rt2 >= 2)
    print('LEVEL combos with 30+ trades in both periods:', ok.sum(), 'pass', pas.sum(), 'random pass', rpas.sum())
    print(G[pas].sort_values('t2', ascending=False).round(2).head(60).to_string())
