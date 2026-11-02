"""A. Entry location: MMCB candle types, every entry x stop x target x exit.
usage: python3 exp_a.py old|fresh"""
import sys, numpy as np, pandas as pd, time
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
import data as D

OUT = '/home/claude/rt/out'
import os; os.makedirs(OUT, exist_ok=True)

LAD = [('C', None), ('P 87.5', .875), ('MP 75', .75), ('BAL 50', .5), ('MD 25', .25), ('D 12.5', .125), ('XD 0', 0.0), ('O open', 'O')]
FPE = [('POC', 'poc'), ('VA near edge', 'vnear'), ('VA far edge', 'vfar')]
STOPS = ['S0 fixed 50', 'S1 candle extreme', 'S6 ATR x1', 'S6 ATR x1.5', 'S7 daily ATR x0.15']
RK = np.array([1., 2., 3., 4., 6.])

def datr_prev_map(sig_index, daily_df, keyed_by_session_start):
    a = pd.Series(atr(daily_df), index=daily_df.index).shift(1)
    if keyed_by_session_start:
        a.index = (a.index + pd.Timedelta(hours=6)).normalize()
    else:
        a.index = a.index.normalize()
    endd = (sig_index + pd.Timedelta(hours=6)).normalize()
    return a.reindex(endd).values

def build_rows(sig, types_, side_of, fp=None, datr=None, sess=None, extra_filter=None, fixed=50.0):
    o, h, l, c = sig.open.values, sig.high.values, sig.low.values, sig.close.values
    a = atr(sig)
    ents = LAD + (FPE if fp is not None else [])
    n = len(c)
    J = np.arange(n)
    s = side_of.astype(float)
    rg = h - l
    base = (types_ >= 0) & (rg > 0) & ~np.isnan(a) & (J >= 20) & (J < n - 1)
    if extra_filter is not None:
        base &= extra_filter
    tgt = np.where(s == 1, h, l)
    out = []
    for ei, (en, f) in enumerate(ents):
        if f is None:
            L = np.full(n, np.nan)
        elif f == 'O':
            L = o.copy()
        elif isinstance(f, str):
            poc, vah, val = fp
            L = poc if f == 'poc' else np.where((f == 'vnear') == (s == 1), vah, val)
        else:
            L = np.where(s == 1, l + f * rg, h - f * rg)
        m = base.copy()
        if f is not None:
            m &= ~np.isnan(L) & (s * (c - L) > 0)   # a pullback limit must sit beyond the close
        e0 = np.where(np.isnan(L), c, L)
        for si in range(5):
            if si == 0:
                stp = e0 - s * fixed
            elif si == 1:
                stp = np.where(s == 1, l - TICK, h + TICK)
            elif si == 2:
                stp = e0 - s * a
            elif si == 3:
                stp = e0 - s * 1.5 * a
            else:
                stp = e0 - s * 0.15 * (datr if datr is not None else np.full(n, np.nan))
            mm = m & ~np.isnan(stp)
            jj = J[mm]
            out.append(np.c_[jj, s[mm], L[mm], stp[mm], tgt[mm], types_[mm], sess[mm], np.full(len(jj), ei), np.full(len(jj), si)])
    R = np.concatenate(out).astype(float)
    return R, [e[0] for e in ents]

def run(period):
    t0 = time.time()
    if period == 'old':
        m1, bars = D.old()
        rep = m1
        tfs = ['5m', '15m', '1h', '4h', 'D']
        daily = bars['D']; dkeyed = True
        fpd = {}
    elif period == 'fresh10':
        rep, bars, dd = D.fresh10(); tfs = ['1h', '4h', 'D']; daily = dd; dkeyed = False; fpd = {}
    else:
        m1, m5, bars, fpd, dd = D.fresh()
        tfs = ['5m', '10m', '15m', '1h', '4h', 'D']
        daily = dd; dkeyed = False
    allst = []
    for tf in tfs:
        sig = bars[tf]
        if period == 'fresh':
            if tf == '5m':
                rep = m1
                sig = sig[(sig.index >= m1.index[0]) & (sig.index <= m1.index[-1])]
            else:
                rep = m5
        types_, pos, isBuX, isBeX, nbc = mmcb(sig)
        side_of = np.where(types_ >= 0, TSIDE[np.clip(types_, 0, 15)], 0)
        sess = session(sig.index) if tf not in ('4h', 'D') else np.full(len(sig), 3)
        fp = None
        if tf in fpd:
            poc, vah, val, _ = D.fp_levels(sig, fpd[tf])
            fp = (poc, vah, val)
        datr = datr_prev_map(sig.index, daily, dkeyed)
        rows, enames = build_rows(sig, types_, side_of, fp, datr, sess)
        nE = len(enames)
        grp = ((rows[:, 5] * 4 + rows[:, 6]) * nE + rows[:, 7]) * 5 + rows[:, 8]
        nG = 16 * 4 * nE * 5
        sF, sL, r2s = map_replay(sig, rep)
        evN = exit_events(sig)
        acc, cnt, _ = simulate(rep.open.values, rep.high.values, rep.low.values, rep.close.values,
                               sF, sL, r2s, sig.close.values, len(sig),
                               rows[:, 0].astype(np.int64), rows[:, 1].astype(np.int64), rows[:, 2], rows[:, 3], rows[:, 4],
                               grp.astype(np.int64), nG, RK, evN, EXIT_MO, 5, 100, 1.0, 2.0, TICK, -1, -1)
        labels = []
        SN = ['Asia', 'NY AM', 'Other', 'All (4H/D)']
        for ty in range(16):
            for ss in range(4):
                for ei in range(nE):
                    for si in range(5):
                        labels.append(dict(period=period, tf=tf, family='MMCB', signal=TYPES[ty],
                                           side='long' if TSIDE[ty] == 1 else 'short', session=SN[ss],
                                           entry=enames[ei], stop=STOPS[si]))
        st = stats_frame(acc, cnt, labels, RK)
        st.to_parquet(f'{OUT}/A_mmcb_{period}_{tf}.parquet')
        allst.append(st)
        print(period, tf, len(sig), 'rows', len(rows), 'cells', len(st), f'{time.time() - t0:.0f}s', flush=True)
    return allst

if __name__ == '__main__':
    run(sys.argv[1])
