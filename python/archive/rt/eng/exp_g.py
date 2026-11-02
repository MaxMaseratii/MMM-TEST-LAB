"""GMC (3 candles with a gap) on every timeframe: entries XU / c3 close / c3 low / gap 50% / c1 high / c2 ladder / POC,
split by the type of candle 3. usage: python3 exp_g.py old|fresh"""
import sys, numpy as np, pandas as pd, time
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
from rows import *
import data as D

OUT = '/home/claude/rt/out'
GRP = ['c3 BC+ with the gap', 'c3 BC- with the gap', 'c3 CI (inside)', 'c3 AFs against (swept c2 far side, closed back in)',
       'c3 AFs with (swept c2 near side)', 'c3 other']
CATN = ['GMC LONG · ' + g for g in GRP] + ['GMC SHORT · ' + g for g in GRP]
CATS = ['long'] * 6 + ['short'] * 6

def c3group(ty, bull):
    # ty = MMCB type of c3 vs c2
    if bull:
        m = {0: 0, 2: 0, 1: 1, 3: 1, 6: 2, 14: 2, 12: 3, 13: 3, 4: 4, 5: 4}
    else:
        m = {8: 0, 10: 0, 9: 1, 11: 1, 6: 2, 14: 2, 4: 3, 5: 3, 12: 4, 13: 4}
    return m.get(int(ty), 5)

def gmc_rows(sig, sess, datr, fp=None):
    o, h, l, c = sig.open.values, sig.high.values, sig.low.values, sig.close.values
    n = len(c)
    ty, pos, *_ = mmcb(sig)
    h1, l1, o1, c1 = [np.r_[np.nan, x[:-1]] for x in (h, l, o, c)]
    h2, l2 = [np.r_[np.nan, np.nan, x[:-2]] for x in (h, l)]
    bull = (c1 > h2) & (l > h2)
    bear = (c1 < l2) & (h < l2)
    side = np.where(bull, 1, np.where(bear, -1, 0))
    cat = np.array([c3group(ty[j], side[j] == 1) + (0 if side[j] == 1 else 6) if side[j] != 0 else -1 for j in range(n)])
    s = side.astype(float)
    r2 = h1 - l1
    ents = [('c3 close', None),
            ('XU c2 open', o1),
            ('c3 low/high = gap edge', np.where(s == 1, l, h)),
            ('gap 50%', np.where(s == 1, (l + h2) / 2, (h + l2) / 2)),
            ('c1 high/low = gap filled', np.where(s == 1, h2, l2)),
            ('c2 P 87.5', np.where(s == 1, l1 + .875 * r2, h1 - .875 * r2)),
            ('c2 MP 75', np.where(s == 1, l1 + .75 * r2, h1 - .75 * r2)),
            ('c2 BAL 50', np.where(s == 1, l1 + .5 * r2, h1 - .5 * r2)),
            ('c2 D 12.5', np.where(s == 1, l1 + .125 * r2, h1 - .125 * r2))]
    if fp is not None:
        poc = fp[0]
        ents += [('c3 POC', poc), ('c2 POC', np.r_[np.nan, poc[:-1]])]
    s1 = np.where(s == 1, l1 - TICK, h1 + TICK)       # below c2 (the gap candle)
    tgt = np.where(s == 1, h, l)                        # c3 extreme
    rows = build(sig, side != 0, side, cat, sess, ents, s1, tgt, datr)
    return rows, [e[0] for e in ents]

def run(period):
    t0 = time.time()
    if period == 'old':
        m1, bars = D.old(); rep = m1
        tfs = ['5m', '15m', '1h', '4h', 'D']; daily = bars['D']; dk = True; fpd = {}
    elif period == 'fresh10':
        rep, bars, dd = D.fresh10(); tfs = ['1h', '4h', 'D']; daily = dd; dk = False; fpd = {}
    else:
        m1, m5, bars, fpd, dd = D.fresh()
        tfs = ['5m', '10m', '15m', '1h', '4h', 'D']; daily = dd; dk = False
    for tf in tfs:
        sig = bars[tf]
        if period == 'fresh':
            if tf == '5m':
                rep = m1; sig = sig[(sig.index >= m1.index[0]) & (sig.index <= m1.index[-1])]
            else:
                rep = m5
        sess = session(sig.index) if tf not in ('4h', 'D') else np.full(len(sig), 3)
        fp = D.fp_levels(sig, fpd[tf])[:3] if tf in fpd else None
        datr = datr_prev_map(sig.index, daily, dk)
        rows, en = gmc_rows(sig, sess, datr, fp)
        acc, cnt, _ = run_rows(sig, rep, rows, 12, len(en))
        st = stats_frame(acc, cnt, labels(dict(period=period, tf=tf, family='GMC'), CATN, CATS, en), RK)
        st.to_parquet(f'{OUT}/G_gmc_{period}_{tf}.parquet')
        print(period, tf, 'rows', len(rows), f'{time.time() - t0:.0f}s', flush=True)

if __name__ == '__main__':
    run(sys.argv[1])
