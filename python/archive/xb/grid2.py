"""GMU entry map: bull and bear SEPARATE. Ladder names from each range's LOW (Max's convention, no mirroring).
Entries: GMU3 / C1 / C2 / C3 ladders (XD 0 .. XP 100) + c1/c2/c3 open & close + gap 50%.
Stops x targets x exits, groups: ALL, c3 BC, c3 NBC, c3 family x lean."""
import sys, time, numpy as np, pandas as pd
from numba import njit
from core import raw, Fine, bars, TICK
from grid import next_open_index
sys.path.insert(0, '/home/claude/ten'); from common import ctype, family, lean

LADDER = [('XD', 0.0), ('D', .125), ('MD', .25), ('BAL', .5), ('MP', .75), ('P', .875), ('XP', 1.0)]
RANGES = ['GMU3', 'C1', 'C2', 'C3']
ENAME = [f'{r} {n}' for r in RANGES for n, _ in LADDER] + ['c1 open', 'c1 close', 'c2 open', 'c2 close', 'c3 open', 'c3 close', 'gap 50%']
NE = len(ENAME)
SNAME = ['S50 fixed 50', 'ATR 1.5x', 'past GMU3 low/high', 'past c1 low/high', 'past gap edge (c1 H/L)', 'past c2 open (GMU open)',
         'past c2 low/high', 'past c3 low/high', 'past c3 open', 'past own range end', 'past GMU3 BAL']
NS = len(SNAME)
TGT = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 6.0]); NT = 6
XNAME = ['stop / target only', 'close through GMU open', 'gap filled (close through c1)', 'next session open']; NX = 4
FAM = ['BC+', 'BC-', 'C2', 'AFs', 'CI', 'S&D']
GNAME = ['ALL', 'c3 BC (with)', 'c3 NBC'] + [f'{f} {w}' for f in FAM for w in ('with', 'against')]
NG = len(GNAME)
WAIT, HOLD = 10, 100

@njit(cache=True)
def run_all(gi, gs, gg1, gg2, EL, SL, atr, tc, ke, ci, fo, fh, fl, fc, nxt, c2o, c1e, acc, nbar):
    nf = len(fh)
    for q in range(len(gi)):
        i = gi[q]; s = gs[q]; side = 0 if s == 1 else 1
        k0 = ke[i]
        if k0 >= nf: continue
        kexp = ke[min(i + WAIT, nbar - 1)] - 1
        for e in range(EL.shape[1]):
            lv = EL[q, e]
            if lv != lv: continue
            mk = (s == 1 and lv >= tc[i]) or (s == -1 and lv <= tc[i])
            if mk: lv = tc[i]
            kf = -1
            if mk: kf = k0
            else:
                for k in range(k0, min(kexp + 1, nf)):
                    if (s == 1 and fl[k] <= lv) or (s == -1 and fh[k] >= lv):
                        kf = k; break
            if kf < 0: continue
            ep = lv; cf = ci[kf]
            kmax = ke[min(cf + HOLD, nbar - 1)] - 1
            kv1 = -1; pv1 = 0.0; kv2 = -1; pv2 = 0.0
            for j in range(cf, min(cf + HOLD, nbar)):
                if kv1 < 0 and ((s == 1 and tc[j] < c2o[q]) or (s == -1 and tc[j] > c2o[q])):
                    kv1 = ke[j]; pv1 = tc[j]
                if kv2 < 0 and ((s == 1 and tc[j] < c1e[q]) or (s == -1 and tc[j] > c1e[q])):
                    kv2 = ke[j]; pv2 = tc[j]
                if kv1 >= 0 and kv2 >= 0: break
            ksx = nxt[kf]; psx = fo[ksx] if ksx < nf else fc[nf - 1]
            for st in range(SL.shape[2]):
                if st == 0: sl = ep - s * 50.0
                elif st == 1: sl = ep - s * 1.5 * atr[i]
                else: sl = SL[q, e, st]
                if sl != sl: continue
                risk = s * (ep - sl)
                if not (risk >= 4.0): continue
                ks = -1; kt = np.full(6, -1); left = 6; kend = -1; pend = 0.0
                for j in range(kf, nf):
                    if j > kmax:
                        kend = j; pend = fc[j - 1]; break
                    if (s == 1 and fl[j] <= sl) or (s == -1 and fh[j] >= sl):
                        ks = j; break
                    if j > kf or mk:
                        for t in range(6):
                            if kt[t] < 0:
                                tp = ep + s * risk * TGT_[t]
                                if (s == 1 and fh[j] >= tp) or (s == -1 and fl[j] <= tp):
                                    kt[t] = j; left -= 1
                    if left == 0 and j >= max(kv1, kv2, ksx): break
                if ks < 0 and kend < 0:
                    kend = min(kmax + 1, nf - 1); pend = fc[kend - 1]
                cost = 1.0 / risk
                for t in range(6):
                    for x in range(4):
                        best = 1 << 60; r = 0.0
                        if ks >= 0: best = ks; r = -1.0
                        if kt[t] >= 0 and kt[t] < best: best = kt[t]; r = TGT_[t]
                        if x == 1 and kv1 >= 0 and kv1 <= best: best = kv1; r = s * (pv1 - ep) / risk
                        if x == 2 and kv2 >= 0 and kv2 <= best: best = kv2; r = s * (pv2 - ep) / risk
                        if x == 3 and ksx < nf and ksx <= best and ksx > kf: best = ksx; r = s * (psx - ep) / risk
                        if best == (1 << 60): r = s * (pend - ep) / risk
                        r -= cost
                        for g in (0, gg1[q], gg2[q]):
                            if g < 0: continue
                            a = acc[g, side, e, st, t, x]
                            a[0] += 1; a[1] += r; a[2] += r * r
                            if r > 0: a[3] += 1; a[4] += r
                            else: a[5] -= r
TGT_ = TGT

def run(period, tf):
    d1 = raw()['fresh5' if (period == 'fresh' and tf == '5m') else period]; F = Fine(d1)
    d = bars(d1, tf)
    o, h, l, c, atr = d.open.values, d.high.values, d.low.values, d.close.values, np.nan_to_num(d.atr.values)
    n = len(d)
    ke = np.searchsorted(F.t, d.tend.values.astype('datetime64[ns]').astype(np.int64), 'left')
    ks0 = np.searchsorted(F.t, d.index.values.astype('datetime64[ns]').astype(np.int64), 'left')
    ci = np.searchsorted(ks0, np.arange(len(F.t)), 'right') - 1
    nxt = next_open_index(F.t)
    rows = []
    for i in range(16, n - 1):
        a, b = i - 2, i - 1
        if c[b] > h[a] and l[i] - h[a] >= 2 * TICK: s = 1
        elif c[b] < l[a] and l[a] - h[i] >= 2 * TICK: s = -1
        else: continue
        ty = ctype(o[i], h[i], l[i], c[i], h[b], l[b])
        bc3 = (s == 1 and c[i] > h[b]) or (s == -1 and c[i] < l[b])
        nbc3 = not (c[i] > h[b] or c[i] < l[b])
        g1 = 1 if bc3 else (2 if nbc3 else -1)
        g2 = 3 + FAM.index(family(ty)) * 2 + (0 if (lean(ty) == 'bull') == (s == 1) else 1)
        rng = {'GMU3': (min(l[a:i+1]), max(h[a:i+1])), 'C1': (l[a], h[a]), 'C2': (l[b], h[b]), 'C3': (l[i], h[i])}
        el = []; own = []
        for r in RANGES:
            lo, hi = rng[r]
            for _, p in LADDER:
                el.append(lo + p * (hi - lo)); own.append(lo if s == 1 else hi)
        gap_lo, gap_hi = (h[a], l[i]) if s == 1 else (h[i], l[a])
        pts = [o[a], c[a], o[b], c[b], o[i], c[i], (gap_lo + gap_hi) / 2]
        el += pts; own += [np.nan] * len(pts)
        g3lo, g3hi = rng['GMU3']
        far = lambda lo_, hi_: lo_ - 0.5 if s == 1 else hi_ + 0.5
        base = [np.nan, np.nan, far(g3lo, g3hi), far(l[a], h[a]), (h[a] - 0.5) if s == 1 else (l[a] + 0.5), o[b] - s * 0.5,
                far(l[b], h[b]), far(l[i], h[i]), o[i] - s * 0.5, np.nan, (g3lo + g3hi) / 2 - s * 0.5]
        sl = np.array([base[:9] + [ow - s * 0.5 if ow == ow else np.nan, base[10]] for ow in own])
        rows.append((i, s, g1, g2, el, sl, o[b], h[a] if s == 1 else l[a]))
    gi = np.array([r[0] for r in rows]); gs = np.array([r[1] for r in rows])
    gg1 = np.array([r[2] for r in rows]); gg2 = np.array([r[3] for r in rows])
    EL = np.array([r[4] for r in rows], dtype=float); SL = np.array([r[5] for r in rows], dtype=float)
    c2o = np.array([r[6] for r in rows], dtype=float); c1e = np.array([r[7] for r in rows], dtype=float)
    acc = np.zeros((NG, 2, NE, NS, NT, NX, 6))
    run_all(gi, gs, gg1, gg2, EL, SL, atr, c, ke, ci, F.o, F.h, F.l, F.c, nxt, c2o, c1e, acc, n)
    cnt = np.array([[np.sum(gs == sd) if g == 0 else np.sum((gs == sd) & ((gg1 == g) | (gg2 == g))) for sd in (1, -1)] for g in range(NG)])
    # random baseline per side: market at the close of every 7th candle, 50 pt, 1:2, stop/target only
    from core import grade
    rnd = []
    for sd in (1, -1):
        R = []
        for i in range(20, n - 1, 7):
            k = ke[i]; km = ke[min(i + HOLD, n - 1)] - 1
            if k >= len(F.t): continue
            r, f, _, _ = grade(F.t, F.h, F.l, F.c, k, k, km, sd, c[i], 1, 50.0, 2.0)
            if f: R.append(r)
        rnd.append(R)
    return acc, cnt, rnd

if __name__ == '__main__':
    import pickle
    out = {}
    for period in ('old', 'fresh'):
        for tf in ('5m', '15m', '1h', '4h'):
            t = time.time(); acc, cnt, rnd = run(period, tf); out[(period, tf)] = (acc, cnt, rnd)
            print(period, tf, cnt[0], round(time.time() - t), 's', flush=True)
    pickle.dump(out, open('grid2.pkl', 'wb'))
