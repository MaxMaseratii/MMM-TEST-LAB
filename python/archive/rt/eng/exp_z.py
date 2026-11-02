"""Zone x box breaks (CONTRACTION G1 and EXPANDER G1): entries at close / break-candle ladder / broken level / box 50% / POC."""
import sys, numpy as np, pandas as pd, time
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
from rows import *
from zone import zone_engine
import data as D
OUT = '/home/claude/rt/out'
CATN = ['x LONG · CDLx flip T1', 'x LONG · LDx T2', 'x LONG · LDx T3+', 'x SHORT · CDSx flip T1', 'x SHORT · SDx T2', 'x SHORT · SDx T3+']
CATS = ['long'] * 3 + ['short'] * 3

def zrows(sig, sess, datr, fp, expMode):
    o, h, l, c, v = [sig[k].values for k in ('open', 'high', 'low', 'close', 'volume')]
    z = zone_engine(o, h, l, c, v, True, expMode)
    side = z['ev_dir']
    tier = z['ev_tier']
    cat = np.where(side == 0, -1, np.where(tier <= 1, 0, np.where(tier == 2, 1, 2)) + np.where(side == 1, 0, 3))
    s = side.astype(float); rg = h - l
    boxmid = np.where(z['end_f'], (z['end_h'] + z['end_l']) / 2, np.nan)
    ents = [('close', None),
            ('break candle P 87.5', np.where(s == 1, l + .875 * rg, h - .875 * rg)),
            ('break candle MP 75', np.where(s == 1, l + .75 * rg, h - .75 * rg)),
            ('break candle BAL 50', np.where(s == 1, l + .5 * rg, h - .5 * rg)),
            ('broken level retest', z['brk_p']),
            ('broken box 50%', boxmid)]
    if fp is not None:
        ents += [('break candle POC', fp[0])]
    s1 = np.where(s == 1, z['tn_new'] - TICK, z['tn_new'] + TICK)   # the protected level (new T#)
    tgt = np.where(s == 1, h, l)
    return build(sig, side != 0, side, cat, sess, ents, s1, tgt, datr), [e[0] for e in ents]

def run(period):
    t0 = time.time()
    if period == 'old':
        m1, bars = D.old(); rep = m1; tfs = ['5m', '15m', '1h', '4h']; daily = bars['D']; dk = True; fpd = {}
    elif period == 'fresh10':
        rep, bars, dd = D.fresh10(); tfs = ['1h', '4h']; daily = dd; dk = False; fpd = {}
    else:
        m1, m5, bars, fpd, dd = D.fresh(); tfs = ['5m', '10m', '15m', '1h', '4h']; daily = dd; dk = False
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
        evN = exit_events(sig)
        for mode, em in (('CONTRACTION G1', False), ('EXPANDER G1', True)):
            rows, en = zrows(sig, sess, datr, fp, em)
            acc, cnt, _ = run_rows(sig, rep, rows, 6, len(en), evN=evN)
            st = stats_frame(acc, cnt, labels(dict(period=period, tf=tf, family='Zone x ' + mode), CATN, CATS, en), RK)
            st.to_parquet(f'{OUT}/Z_{mode[:3]}_{period}_{tf}.parquet')
            print(period, tf, mode, 'rows', len(rows), f'{time.time() - t0:.0f}s', flush=True)

if __name__ == '__main__':
    run(sys.argv[1])
