"""Max's read of the XB zones: SELL in discount (XBS, price drops into it) · BUY in premium (XBB, price rises into it).
Stop-entry orders live from the first NBC close until the break. Compared with the old read (buy XBS / sell XBB limits). 50 pt stop, 1:2."""
import numpy as np, pandas as pd
from numba import njit
from core import *
from xbeng import blocks
HOLD = 100

@njit(cache=True)
def stopentry(fo, fh, fl, fc, ks, ke, lv, side, risk, rr, kmax, cost):
    n = len(fh); kf = -1; ep = 0.0
    for k in range(ks, min(ke + 1, n)):
        x = lv[k - ks]
        if x != x: continue
        if side == -1 and fl[k] <= x: kf = k; ep = min(x, fo[k]); break
        if side == 1 and fh[k] >= x: kf = k; ep = max(x, fo[k]); break
    if kf < 0: return 0.0, 0
    sl = ep - side * risk; tp = ep + side * risk * rr
    for j in range(kf, n):
        if j > kmax: return side * (fc[j - 1] - ep) / risk - cost / risk, 1
        slh = fl[j] <= sl if side == 1 else fh[j] >= sl
        tph = fh[j] >= tp if side == 1 else fl[j] <= tp
        if slh: return -1.0 - cost / risk, 1
        if tph and j > kf: return rr - cost / risk, 1
    return 0.0, 0

rows = []
R0 = raw()
for period in ('old', 'fresh'):
    for tf in ('5m', '15m', '1h', '4h'):
        d1 = R0['fresh5' if (period == 'fresh' and tf == '5m') else period]; F = Fine(d1)
        d = bars(d1, tf); o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values; n = len(d)
        ke = np.searchsorted(F.t, d.tend.values.astype('datetime64[ns]').astype(np.int64), 'left')
        last = 0; lastbc = np.zeros(n, int)   # direction of the last BC before bar i
        for i in range(1, n):
            lastbc[i] = last
            if c[i] > h[i-1]: last = 1
            elif c[i] < l[i-1]: last = -1
        for blk in blocks(o, h, l, c):
            e = blk['end']
            if e < 0 or e + 2 >= n: continue
            H = blk['hist']; k_s = ke[H[0][0]]; k_e = ke[e] - 1; m = k_e - k_s + 1
            if m <= 0: continue
            # opposite-side XB? (its BC goes against the BC before it)
            b0 = blk.get('bc', None)
            idx = np.searchsorted(ke[[x[0] for x in H]], np.arange(k_s, k_e + 1), 'right') - 1
            arr = np.array([x[1:] for x in H])[idx]; Hh, Ll, bt, bb = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
            kmax = ke[min(e + HOLD, n - 1)] - 1
            Z = {'MAX: SELL stop at XBS top (balanced bottom)': (-1, bb), 'MAX: SELL stop at XBS mid': (-1, (bb + Ll) / 2),
                 'MAX: BUY stop at XBB bottom (balanced top)': (1, bt), 'MAX: BUY stop at XBB mid': (1, (bt + Hh) / 2)}
            for zn, (sd, lv) in Z.items():
                R, f = stopentry(F.o, F.h, F.l, F.c, k_s, k_e, lv.astype(np.float64), sd, 50.0, 2.0, kmax, COST)
                if f: rows.append((period, tf, blk['dir'], zn, R, d.index[e]))
D = pd.DataFrame(rows, columns=['period', 'tf', 'xbdir', 'entry', 'R', 't'])
D.to_parquet('maxread.parquet')
def st(r):
    r = np.asarray(r); g = r[r > 0].sum(); L = -r[r < 0].sum()
    return f"n {len(r)} · WR {100*(r>0).mean():.0f}% · avg {r.mean():+.3f} · PF {g/L if L else 0:.2f} · t {r.mean()/r.std(ddof=1)*np.sqrt(len(r)):.1f}"
for (tf, en), g in D.groupby(['tf', 'entry'], sort=False):
    print(tf, '|', en, '|', st(g[g.period=='old'].R), '||', st(g[g.period=='fresh'].R))
