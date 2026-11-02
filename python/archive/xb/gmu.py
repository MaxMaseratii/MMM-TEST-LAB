"""GMU ladder test: 3 approaches x 7 levels x C3 shape, per TF and period."""
import sys, numpy as np, pandas as pd, pickle, time
from core import *

LV = [('XD', 0.0), ('D', .125), ('MD', .25), ('BAL', .5), ('MP', .75), ('P', .875), ('XP', 1.0)]
APP = ['C3', 'GMU3', 'C1']
WAIT = 10      # candles a limit stays live
HOLD = 100     # max candles in a trade

def gmus(d):
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    out = []
    for i in range(2, len(d)):
        a, b = i - 2, i - 1          # c1, c2, c3 = a, b, i
        if c[b] > h[a] and l[i] - h[a] >= 2 * TICK:
            s = 1
        elif c[b] < l[a] and l[a] - h[i] >= 2 * TICK:
            s = -1
        else:
            continue
        ty = ctype(o[i], h[i], l[i], c[i], h[b], l[b])
        out.append((i, s, ty))
    return out

def run(period, tf, seed=1):
    d1 = raw()['fresh5' if (period == 'fresh' and tf == '5m') else period]; F = Fine(d1)
    d = bars(d1, tf)
    t0 = d.index.values.astype('datetime64[ns]').astype(np.int64)
    k0s = np.searchsorted(F.t, d.tend.values.astype('datetime64[ns]').astype(np.int64), 'left')
    n = len(d)
    h, l, c, atr = d.high.values, d.low.values, d.close.values, d.atr.values
    rows = []
    G = gmus(d)
    for (i, s, ty) in G:
        if i + 1 >= n: continue
        k0 = k0s[i]
        kexp = k0s[min(i + WAIT, n - 1)] - 1
        kmax = k0s[min(i + HOLD, n - 1)] - 1
        rng = {'C3': (l[i], h[i]), 'GMU3': (min(l[i-2:i+1]), max(h[i-2:i+1])), 'C1': (l[i-2], h[i-2])}
        fam = family(ty); ln = 'with' if (lean(ty) == 'bull') == (s == 1) else 'against'
        for ap in APP:
            lo, hi = rng[ap]
            for nm, p in LV:
                lv = lo + p * (hi - lo)
                mk = 1 if (s == 1 and lv >= c[i]) or (s == -1 and lv <= c[i]) else 0
                if mk: lv = c[i]
                for sname, sp in (('S50', 50.0), ('ATR', max(1.5 * atr[i], 2.0) if atr[i] == atr[i] else 50.0)):
                    for rr in (1.0, 2.0, 3.0):
                        R, f, kf, ex = grade(F.t, F.h, F.l, F.c, k0, kexp, kmax, s, lv, mk, sp, rr)
                        rows.append((period, tf, d.index[i], s, ty, fam, ln, ap, nm, mk, sname, rr, f, R))
    # random baseline: every 10th candle, random side, market at close
    rng_ = np.random.default_rng(seed)
    for i in range(20, n - 1, 7):
        s = 1 if rng_.random() < .5 else -1
        k0 = k0s[i]; kmax = k0s[min(i + HOLD, n - 1)] - 1
        for rr in (1.0, 2.0, 3.0):
            R, f, kf, ex = grade(F.t, F.h, F.l, F.c, k0, k0, kmax, s, c[i], 1, 50.0, rr)
            rows.append((period, tf, d.index[i], s, 'RANDOM', 'RANDOM', '-', 'RANDOM', '-', 1, 'S50', rr, f, R))
    df = pd.DataFrame(rows, columns=['period', 'tf', 'time', 'side', 'c3', 'fam', 'lean', 'app', 'lvl', 'mkt', 'stop', 'rr', 'filled', 'R'])
    return df, len(G), n

if __name__ == '__main__':
    out = []
    for period in ('old', 'fresh'):
        for tf in ('5m', '15m', '1h', '4h'):
            t = time.time()
            df, ng, nb = run(period, tf)
            out.append(df)
            print(period, tf, 'bars', nb, 'GMU', ng, 'rows', len(df), round(time.time() - t), 's', flush=True)
    pd.concat(out).to_parquet('gmu_trades.parquet')
