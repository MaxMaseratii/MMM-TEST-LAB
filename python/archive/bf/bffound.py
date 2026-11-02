"""A: foundation stats for every CDS / CDL (and failed setups ✕), with a random control.
Per event (break candle = C2, side s):
  BCs in the new direction after the break before the first opposite BC, and before the first NBC
  points after 1, 3, 5, 10 candles (close to close, in the break direction) and in ATR
  protected C1: does a close go back beyond C1 (wick) before price travels 1R / 2R / 3R (R = fixed stop: NQ 50 ...)?
Failed setups (✕): the same forward points in the OLD trend direction, and a market trade at the ✕ close, fixed stop 1:2."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/pp')
import ppdata, bfeng, bfrun
from numba import njit

TFS = bfrun.TFS


@njit(cache=True)
def fwd(o, h, l, c, I, S, C1W, s50, cost):
    n = len(c); m = len(I)
    out = np.full((m, 16), np.nan)
    for q in range(m):
        i = I[q]; s = S[q]
        if i + 11 >= n: continue
        # BCs after the break
        same = 0; firstNBC = -1; bcNbc = 0; done = False
        for j in range(i + 1, min(i + 300, n)):
            bu = c[j] > h[j - 1] and c[j] > o[j]; be = c[j] < l[j - 1] and c[j] < o[j]
            if (s == 1 and be) or (s == -1 and bu): break
            if (s == 1 and bu) or (s == -1 and be):
                same += 1
                if firstNBC < 0: bcNbc += 1
            elif firstNBC < 0:
                firstNBC = j
        out[q, 0] = same; out[q, 1] = bcNbc
        for k, kk in enumerate((1, 3, 5, 10)):
            out[q, 2 + k] = s * (c[i + kk] - c[i])
        # C1 protected vs 1R / 2R / 3R (from the C2 close)
        ep = c[i]; w = C1W[q]
        hit = np.full(4, -1.0)   # 0 = C1 broken first, 1..3 = R reached first
        tC1 = -1; tR = np.full(3, -1)
        for j in range(i + 1, min(i + 500, n)):
            if tC1 < 0 and ((s == 1 and c[j] < w) or (s == -1 and c[j] > w)): tC1 = j
            fav = h[j] - ep if s == 1 else ep - l[j]
            for k in range(3):
                if tR[k] < 0 and fav >= (k + 1) * s50: tR[k] = j
            if tC1 >= 0 and tR[2] >= 0: break
        for k in range(3):
            # 1 = R reached before (or without) a close beyond C1
            if tR[k] >= 0 and (tC1 < 0 or tR[k] <= tC1): out[q, 6 + k] = 1.0
            else: out[q, 6 + k] = 0.0
        out[q, 9] = 1.0 if tC1 >= 0 else 0.0
        # fixed stop 1:2 market at the close (used for ✕ trades)
        stop = ep - s * s50; tp = ep + s * 2 * s50; r = np.nan
        for j in range(i + 1, min(i + 101, n)):
            if (s == 1 and l[j] <= stop) or (s == -1 and h[j] >= stop):
                r = (min(o[j], stop) if s == 1 else max(o[j], stop)); break
            if (s == 1 and h[j] >= tp) or (s == -1 and l[j] <= tp):
                r = tp; break
        if r != r: r = c[min(i + 100, n - 1)]
        out[q, 10] = (s * (r - ep) - cost) / s50
    return out


def run(markets=('NQ', 'ES', 'GC', 'CL'), kw=None, tag='base'):
    kw = kw or {}
    rows = []
    for m in markets:
        sp = ppdata.SPEC[m]
        for tf in TFS:
            for d in ppdata.series(m, tf):
                S = bfeng.signals(d, **kw)
                o, h, l, c = S['o'], S['h'], S['l'], S['c']; atr = S['atr']
                mk = bfrun.masks(d, S, tf, kw)
                per = np.where(d.per.values == 'P2', 'P2', 'P1')
                I = S['fI']; Sd = S['fS'].astype(np.int64)
                F = fwd(o, h, l, c, I, Sd, S['fW1'], sp['stop'], sp['cost'])
                ev = pd.DataFrame(F[:, :11], columns=['bc_opp', 'bc_nbc', 'p1', 'p3', 'p5', 'p10', 'r1', 'r2', 'r3', 'c1brk', 'fix12'])
                ev['kind'] = 'CDS/CDL'; ev['side'] = np.where(Sd == 1, 'long (CDL)', 'short (CDS)'); ev['mask'] = mk
                ev['atr'] = atr[I]; ev['per'] = per[I]
                # failed setups: old trend direction = opposite of the setup side
                X = S['xI']; XS = (-S['xS']).astype(np.int64)
                FX = fwd(o, h, l, c, X, XS, np.where(XS == 1, l[X], h[X]).astype(float), sp['stop'], sp['cost'])
                ex = pd.DataFrame(FX[:, :11], columns=ev.columns[:11])
                ex['kind'] = '✕ failed setup (old trend)'; ex['side'] = np.where(XS == 1, 'long', 'short'); ex['mask'] = 1 | (((d.index.hour.values[X] * 60 + d.index.minute.values[X] >= 585) & (d.index.hour.values[X] * 60 + d.index.minute.values[X] < 720)).astype(np.int64) << 1)
                ex['atr'] = atr[X]; ex['per'] = per[X]
                # random control: same count, random bars, random side
                rng = np.random.default_rng(11 + tf)
                R = np.sort(rng.choice(np.arange(20, len(d) - 12), size=min(len(I), len(d) - 40), replace=False)).astype(np.int64)
                RS = np.where(rng.random(len(R)) < 0.5, 1, -1).astype(np.int64)
                FR = fwd(o, h, l, c, R, RS, np.where(RS == 1, l[R - 1], h[R - 1]).astype(float), sp['stop'], sp['cost'])
                er = pd.DataFrame(FR[:, :11], columns=ev.columns[:11])
                er['kind'] = 'RANDOM'; er['side'] = np.where(RS == 1, 'long', 'short'); er['mask'] = 1 | (((d.index.hour.values[R] * 60 + d.index.minute.values[R] >= 585) & (d.index.hour.values[R] * 60 + d.index.minute.values[R] < 720)).astype(np.int64) << 1)
                er['atr'] = atr[R]; er['per'] = per[R]
                for e in (ev, ex, er):
                    e['m'] = m; e['tf'] = tf
                    rows.append(e.dropna(subset=['p10']))
                print('found', m, tf, d.src.iloc[0], len(I), len(X), flush=True)
    A = pd.concat(rows, ignore_index=True)
    A.to_parquet(f'found_{tag}.parquet')
    return A


if __name__ == '__main__':
    run()
