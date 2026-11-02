"""Generic row builder + runner: every entry x every stop for a set of signal bars."""
import numpy as np, pandas as pd
from core import *

STOPS = ['S0 fixed 50', 'S1 structure', 'S6 ATR x1', 'S6 ATR x1.5', 'S7 daily ATR x0.15']
RK = np.array([1., 2., 3., 4., 6.])

def datr_prev_map(sig_index, daily_df, keyed_by_session_start):
    a = pd.Series(atr(daily_df), index=daily_df.index).shift(1)
    if keyed_by_session_start:
        a.index = (a.index + pd.Timedelta(hours=6)).normalize()
    else:
        a.index = a.index.normalize()
    endd = (sig_index + pd.Timedelta(hours=6)).normalize()
    return a.reindex(endd).values

def build(sig, mask, side, cat, sess, entries, s1, tgt, datr, fixed=50.0):
    """mask: signal bars. side: +1/-1 array. cat: int category per bar.
    entries: list of (name, L array) with L = nan for market. s1: structure stop price array.
    returns rows [j, side, L, stp, tgt, cat, sess, ei, si]"""
    c = sig.close.values
    a = atr(sig)
    n = len(c)
    J = np.arange(n)
    s = side.astype(float)
    base = mask & ~np.isnan(a) & (J >= 20) & (J < n - 1)
    out = []
    for ei, (en, L) in enumerate(entries):
        m = base.copy()
        if L is None:
            L = np.full(n, np.nan)
        else:
            m &= ~np.isnan(L) & (s * (c - L) > 0)
        e0 = np.where(np.isnan(L), c, L)
        for si in range(5):
            if si == 0:
                stp = e0 - s * fixed
            elif si == 1:
                stp = s1
            elif si == 2:
                stp = e0 - s * a
            elif si == 3:
                stp = e0 - s * 1.5 * a
            else:
                stp = e0 - s * 0.15 * datr
            mm = m & ~np.isnan(stp)
            jj = J[mm]
            out.append(np.c_[jj, s[mm], L[mm], stp[mm], tgt[mm], cat[mm], sess[mm], np.full(len(jj), ei), np.full(len(jj), si)])
    return np.concatenate(out).astype(float)

def run_rows(sig, rep, rows, ncat, nent, evN=None, RKs=RK, W=5, Hmax=100, cost=1.0, store=(-1, -1)):
    nG = ncat * 4 * nent * 5
    grp = ((rows[:, 5] * 4 + rows[:, 6]) * nent + rows[:, 7]) * 5 + rows[:, 8]
    sF, sL, r2s = map_replay(sig, rep)
    if evN is None:
        evN = exit_events(sig)
    acc, cnt, keep = simulate(rep.open.values, rep.high.values, rep.low.values, rep.close.values,
                              sF, sL, r2s, sig.close.values, len(sig),
                              rows[:, 0].astype(np.int64), rows[:, 1].astype(np.int64), rows[:, 2], rows[:, 3], rows[:, 4],
                              grp.astype(np.int64), nG, RKs, evN, EXIT_MO, W, Hmax, cost, 2.0, TICK, store[0], store[1])
    return acc, cnt, keep

def labels(meta, catnames, catside, entnames):
    SN = ['Asia', 'NY AM', 'Other', 'All (4H/D)']
    out = []
    for ci in range(len(catnames)):
        for ss in range(4):
            for ei in range(len(entnames)):
                for si in range(5):
                    out.append(dict(**meta, signal=catnames[ci], side=catside[ci], session=SN[ss],
                                    entry=entnames[ei], stop=STOPS[si]))
    return out
