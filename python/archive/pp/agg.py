"""Aggregate PRO PLUS trades into stat rows. Every row: P1, P2 and both together, with a verdict."""
import numpy as np, pandas as pd, engine

def load():
    A = pd.concat([pd.read_parquet('trades_NQ.parquet'), pd.read_parquet('trades_ES_GC_CL.parquet')], ignore_index=True)
    return A.sort_values('t', kind='stable').reset_index(drop=True)

def st(pl, rr):
    n = len(pl)
    if n == 0: return dict(n=0)
    pos = pl[pl > 0].sum(); neg = -pl[pl <= 0].sum()
    sd = rr.std(ddof=1) if n > 1 else np.nan
    eq = np.cumsum(rr); dd = (np.maximum.accumulate(np.r_[0, eq])[1:] - eq).max()
    los = (pl <= 0).astype(int); mx = 0; cur = 0
    for x in los:
        cur = cur + 1 if x else 0; mx = max(mx, cur)
    return dict(n=n, wr=float((pl > 0).mean()), pts=float(pl.mean()), rr=float(rr.mean()),
                pf=float(pos / neg) if neg > 0 else np.nan, t=float(rr.mean() / sd * np.sqrt(n)) if sd and sd > 0 else np.nan,
                dd=float(dd), ml=int(mx))

def verdict(a, b):
    n1, n2 = a.get('n', 0), b.get('n', 0)
    if n1 < 30 or n2 < 20: return 'few trades'
    if a['rr'] > 0 and b['rr'] > 0 and a['t'] >= 2 and b['t'] >= 2: return 'HOLDS'
    if a['rr'] > 0 and b['rr'] > 0: return 'watch'
    if a['rr'] > 0 or b['rr'] > 0: return 'weak'
    return 'no edge'

def row(g, plc='pl', rrc='rr'):
    out = {}
    for p in ('P1', 'P2'):
        x = g[g.per == p]
        out[p] = st(x[plc].values, x[rrc].values)
    out['ALL'] = st(g[plc].values, g[rrc].values)
    out['v'] = verdict(out['P1'], out['P2'])
    return out

def table(A, keys, plc='pl', rrc='rr'):
    rows = []
    for k, g in A.groupby(keys, sort=False):
        k = k if isinstance(k, tuple) else (k,)
        r = row(g, plc, rrc)
        d = dict(zip(keys, k))
        for p in ('P1', 'P2', 'ALL'):
            for f, v in r[p].items(): d[f'{p}_{f}'] = v
        d['v'] = r['v']; rows.append(d)
    return pd.DataFrame(rows)

if __name__ == '__main__':
    A = load()
    stop = A.m.map({'NQ': 50.0, 'ES': 20.0, 'GC': 12.0, 'CL': 0.5}); cost = A.m.map({'NQ': 1.0, 'ES': 0.5, 'GC': 0.2, 'CL': 0.02})
    for k in (2, 3):
        hit = A.favpre >= k * A.risk
        A[f'pl{k}R'] = np.where(hit, k * A.risk - cost, A.pl); A[f'rr{k}R'] = A[f'pl{k}R'] / stop
    A.to_parquet('all_trades.parquet')
    B = A[A.run == 'base']
    T = table(B, ['m', 'tf', 'setup']); T.to_parquet('t_base.parquet')
    pd.set_option('display.width', 250)
    v = T[['m', 'tf', 'setup', 'P1_n', 'P1_rr', 'P1_t', 'P2_n', 'P2_rr', 'P2_t', 'v']].copy()
    v['setup'] = v.setup.map(lambda i: engine.SETUPS[i][:28])
    print(v.round(3).to_string())
