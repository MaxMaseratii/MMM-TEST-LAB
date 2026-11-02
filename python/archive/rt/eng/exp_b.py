"""Balance study (exit question) + BC flow per candle type.
1) Every time N NBCs in a row print after a body close run (N = 2, 3, 4): which body close comes next,
   with the run (continuation) or against it (flip)? Split by what the balance candles are.
   'move to next BC' = signed points (with the run = +) from the close of the Nth NBC to the close of the next BC.
2) BC flow after each MMCB type: same-side BCs before the first opposite BC, before the first NBC, and the points."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
import data as D
OUT = '/home/claude/rt/out'

def comp_label(tys, poss, hs, ls, phs, pls, d):
    """d = run direction. classify the balance candles."""
    lab = []
    rejA = rejW = lean_against = 0
    for t, p, h, l, ph, pl in zip(tys, poss, hs, ls, phs, pls):
        sweptHi, sweptLo = h > ph, l < pl
        if d == 1:
            if sweptHi and p < .5: rejA += 1          # took the high and closed in the bottom half = rejection against
            if sweptLo and p >= .5: rejW += 1         # took the low and closed in the top half = rejection with (AFs+)
            if p < .5: lean_against += 1
        else:
            if sweptLo and p > .5: rejA += 1
            if sweptHi and p <= .5: rejW += 1
            if p > .5: lean_against += 1
    if rejA and not rejW: return 'has a rejection AGAINST the run'
    if rejW and not rejA: return 'has a rejection WITH the run (AFs+)'
    if rejA and rejW: return 'rejections both ways'
    if lean_against == 0: return 'no sweep, all close in the run half'
    if lean_against == len(tys): return 'no sweep, all close in the against half'
    return 'no sweep, mixed closes'

def balance_study(sig, period, tf):
    o, h, l, c = [sig[k].values for k in ('open', 'high', 'low', 'close')]
    ty, pos, isBuX, isBeX, nbc = mmcb(sig)
    a = atr(sig)
    ph, pl = np.r_[np.nan, h[:-1]], np.r_[np.nan, l[:-1]]
    sess = session(sig.index)
    n = len(c)
    bcdir = np.where(isBuX & ~isBeX, 1, np.where(isBeX & ~isBuX, -1, 0))
    # next BC index after each bar
    nxt = np.full(n + 1, n)
    for j in range(n - 1, -1, -1):
        nxt[j] = j if bcdir[j] != 0 else nxt[j + 1]
    recs = []
    j = 1
    while j < n - 1:
        if nbc[j] and bcdir[j - 1] != 0:
            d = bcdir[j - 1]
            k = j
            while k < n and nbc[k]:
                k += 1
            run = k - j     # NBCs in a row
            nb_ = nxt[k] if k < n else n
            if nb_ >= n:
                break
            for N in (2, 3, 4):
                if run >= N:
                    e = j + N - 1
                    cont = bcdir[nb_] == d
                    mv = d * (c[nb_] - c[e])
                    first = 'balance starts with ' + TYPES[ty[j]] if ty[j] >= 0 else ''
                    recs.append(dict(period=period, tf=tf, N=N, run_dir='bull' if d == 1 else 'bear',
                                     session=['Asia', 'NY AM', 'Other'][sess[j]] if tf not in ('4h', 'D') else 'All',
                                     composition=comp_label(ty[j:e + 1], pos[j:e + 1], h[j:e + 1], l[j:e + 1], ph[j:e + 1], pl[j:e + 1], d),
                                     first_candle=TYPES[ty[j]] if ty[j] >= 0 else 'n/a',
                                     more_nbc=run > N, cont=cont, move_pts=mv, move_atr=mv / a[e] if a[e] > 0 else np.nan))
            j = k
        else:
            j += 1
    return pd.DataFrame(recs)

def bc_flow(sig, period, tf):
    o, h, l, c = [sig[k].values for k in ('open', 'high', 'low', 'close')]
    ty, pos, isBuX, isBeX, nbc = mmcb(sig)
    n = len(c)
    bcdir = np.where(isBuX & ~isBeX, 1, np.where(isBeX & ~isBuX, -1, 0))
    recs = []
    for j in range(20, n - 1):
        t = ty[j]
        if t < 0:
            continue
        s = TSIDE[t]
        k = j + 1; same = 0; same_b4_nbc = 0; hit_nbc = False; ext = c[j]
        while k < n and bcdir[k] != -s:
            if bcdir[k] == s:
                same += 1
                if not hit_nbc: same_b4_nbc += 1
            else:
                hit_nbc = True
            ext = max(ext, h[k]) if s == 1 else min(ext, l[k])
            k += 1
            if k - j > 300: break
        if k >= n:
            break
        recs.append((t, same, same_b4_nbc, s * (ext - c[j]), s * (c[k] - c[j])))
    df = pd.DataFrame(recs, columns=['t', 'same_bcs_before_opposite_bc', 'same_bcs_before_first_nbc', 'best_pts_before_opposite_bc', 'pts_at_opposite_bc_close'])
    g = df.groupby('t').agg(candles=('t', 'size'),
                            avg_same_bcs_before_opposite_bc=('same_bcs_before_opposite_bc', 'mean'),
                            avg_same_bcs_before_first_nbc=('same_bcs_before_first_nbc', 'mean'),
                            pct_no_follow_through=('same_bcs_before_opposite_bc', lambda x: (x == 0).mean()),
                            avg_best_pts=('best_pts_before_opposite_bc', 'mean'),
                            median_best_pts=('best_pts_before_opposite_bc', 'median'),
                            avg_pts_at_opposite_bc=('pts_at_opposite_bc_close', 'mean')).reset_index()
    g['candle'] = [TYPES[t] for t in g.t]
    g['side'] = ['long' if TSIDE[t] == 1 else 'short' for t in g.t]
    g['period'] = period; g['tf'] = tf
    return g.drop(columns='t')

if __name__ == '__main__':
    B, F = [], []
    m1, bars = D.old()
    for tf in ['5m', '15m', '1h', '4h', 'D']:
        B.append(balance_study(bars[tf], 'old', tf)); F.append(bc_flow(bars[tf], 'old', tf)); print('old', tf, flush=True)
    m1, m5, fb, fpd, dd = D.fresh()
    for tf in ['5m', '10m', '15m', '1h', '4h', 'D']:
        B.append(balance_study(fb[tf], 'fresh', tf)); F.append(bc_flow(fb[tf], 'fresh', tf)); print('fresh', tf, flush=True)
    pd.concat(B).to_parquet(f'{OUT}/B_balance.parquet')
    pd.concat(F).to_parquet(f'{OUT}/F_bcflow.parquet')
