"""Pullback map: for every MMCB candle, does the next candle(s) take its target (bull: the high)?
For the ones that DO, how deep was the pullback first, and which entry level (ladder / POC / VA) was touched?
And when a level fills, how often is the target still taken (before the candle's protected extreme breaks)?"""
import sys, numpy as np, pandas as pd, numba as nb
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
import data as D
OUT = '/home/claude/rt/out'

@nb.njit(cache=True)
def pmap(rO, rH, rL, sLast, js, side, tgt, prot, close, levels, M, tick):
    n = len(js); NL = levels.shape[1]
    took = np.zeros(n, np.bool_); protFirst = np.zeros(n, np.bool_)
    deep = np.full(n, np.nan)
    lvTouchB4 = np.zeros((n, NL), np.bool_)    # level filled (1 tick through) before the target was taken
    lvFill = np.zeros((n, NL), np.bool_)       # level filled inside the window
    lvWin = np.zeros((n, NL), np.bool_)        # after the fill: target taken before the protected extreme
    for r in range(n):
        j = js[r]; s = side[r]
        a = sLast[j] + 1; b = sLast[min(j + M, len(sLast) - 1)]
        mn = close[r] if s == 1 else close[r]
        ti = -1; pi = -1
        fillI = np.full(NL, -1)
        for i in range(a, b + 1):
            if s == 1:
                for k in range(NL):
                    L = levels[r, k]
                    if fillI[k] < 0 and not np.isnan(L) and rL[i] <= L - tick:
                        fillI[k] = i
                if pi < 0 and rL[i] < prot[r]:
                    pi = i
                if ti < 0 and rH[i] > tgt[r]:
                    ti = i
                if ti < 0:
                    mn = min(mn, rL[i])
            else:
                for k in range(NL):
                    L = levels[r, k]
                    if fillI[k] < 0 and not np.isnan(L) and rH[i] >= L + tick:
                        fillI[k] = i
                if pi < 0 and rH[i] > prot[r]:
                    pi = i
                if ti < 0 and rL[i] < tgt[r]:
                    ti = i
                if ti < 0:
                    mn = max(mn, rH[i])
        took[r] = ti >= 0 and (pi < 0 or pi > ti)
        protFirst[r] = pi >= 0 and (ti < 0 or pi <= ti)
        deep[r] = mn
        for k in range(NL):
            f = fillI[k]
            if f >= 0:
                lvFill[r, k] = True
                if ti >= 0 and f < ti:
                    lvTouchB4[r, k] = True
                # after the fill (next replay bar on): target before the protected extreme
                win = False
                for i in range(f + 1, b + 1):
                    if s == 1:
                        if rL[i] < prot[r]: break
                        if rH[i] > tgt[r]: win = True; break
                    else:
                        if rH[i] > prot[r]: break
                        if rL[i] < tgt[r]: win = True; break
                lvWin[r, k] = win
    return took, protFirst, deep, lvTouchB4, lvFill, lvWin

LVN = ['P 87.5', 'MP 75', 'BAL 50', 'MD 25', 'D 12.5', 'O open', 'POC', 'VA near edge', 'VA far edge']

def run(period):
    recs = []
    if period == 'old':
        m1, bars = D.old(); tfs = ['5m', '15m', '1h', '4h', 'D']; fpd = {}
    else:
        m1, m5, bars, fpd, dd = D.fresh(); tfs = ['5m', '10m', '15m', '1h', '4h', 'D']
    for tf in tfs:
        sig = bars[tf]; rep = m1
        if period == 'fresh':
            if tf == '5m':
                sig = sig[(sig.index >= m1.index[0]) & (sig.index <= m1.index[-1])]
            else:
                rep = m5
        o, h, l, c = sig.open.values, sig.high.values, sig.low.values, sig.close.values
        ty, pos, *_ = mmcb(sig)
        js = np.where(ty >= 0)[0]; js = js[(js > 20) & (js < len(c) - 4)]
        s = TSIDE[ty[js]]
        rg = (h - l)[js]
        lo, hi = l[js], h[js]
        lev = []
        for f in (.875, .75, .5, .25, .125):
            lev.append(np.where(s == 1, lo + f * rg, hi - f * rg))
        lev.append(o[js])
        if tf in fpd:
            poc, vah, val, _ = D.fp_levels(sig, fpd[tf])
            lev += [poc[js], np.where(s == 1, vah[js], val[js]), np.where(s == 1, val[js], vah[js])]
        else:
            lev += [np.full(len(js), np.nan)] * 3
        lev = np.array(lev).T
        # only levels beyond the close count as pullback levels
        lev = np.where((s[:, None] * (c[js][:, None] - lev)) > 0, lev, np.nan)
        sF, sL, r2s = map_replay(sig, rep)
        sess = session(sig.index)[js] if tf not in ('4h', 'D') else np.full(len(js), 3)
        for M in (1, 3):
            took, pf, deep, b4, fill, win = pmap(rep.open.values, rep.high.values, rep.low.values, sL, js, s,
                                                 np.where(s == 1, hi, lo), np.where(s == 1, lo, hi), c[js], lev, M, TICK)
            depth = np.where(s == 1, (deep - lo) / rg, (hi - deep) / rg)   # 1 = at the extreme, 0 = at the protected end
            closepos = np.where(s == 1, (c[js] - lo) / rg, (hi - c[js]) / rg)
            for t in range(16):
                for ss, sn in ((None, 'All'), (0, 'Asia'), (1, 'NY AM')):
                    m = ty[js] == t
                    if ss is not None:
                        m &= sess == ss
                    if m.sum() < 20:
                        continue
                    tk = m & took
                    rec = dict(period=period, tf=tf, candle=TYPES[t], side='long' if TSIDE[t] == 1 else 'short',
                               session=sn, window=f'next {M} candle' + ('s' if M > 1 else ''), candles=int(m.sum()),
                               target_taken=tk.sum() / m.sum(), protected_broken_first=(m & pf).sum() / m.sum())
                    if tk.sum() > 0:
                        dp = depth[tk]
                        cp = closepos[tk]
                        rec['takers_no_pullback_below_close'] = np.mean(dp >= cp - 1e-9)
                        rec['takers_median_depth_%'] = np.median(dp) * 100
                        for k, nm in enumerate(LVN):
                            has = ~np.isnan(lev[tk, k])
                            rec[f'takers: {nm} filled first'] = b4[tk, k][has].mean() if has.sum() > 10 else np.nan
                    for k, nm in enumerate(LVN):
                        has = m & ~np.isnan(lev[:, k])
                        fl = has & fill[:, k]
                        rec[f'{nm}: fill %'] = fl.sum() / has.sum() if has.sum() > 10 else np.nan
                        rec[f'{nm}: target after fill %'] = win[fl, k].mean() if fl.sum() > 10 else np.nan
                    recs.append(rec)
        print(period, tf, flush=True)
    df = pd.DataFrame(recs)
    df.to_parquet(f'{OUT}/P_pullback_{period}.parquet')
    return df

if __name__ == '__main__':
    run(sys.argv[1])
