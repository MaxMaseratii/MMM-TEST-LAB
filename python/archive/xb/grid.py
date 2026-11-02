"""GMU full grid: every ladder entry x every stop x every target x every exit, accumulated in numba.
Bull side shown; bear is mirrored. Depth names: XD = deepest pullback (bull 0%, bear 100%)."""
import sys, time, numpy as np, pandas as pd
from numba import njit
from core import raw, Fine, bars, TICK
sys.path.insert(0, '/home/claude/ten'); from common import ctype, family, lean

DEP = np.array([0.0, .125, .25, .5, .75, .875, 1.0])          # bull fractions from the low: XD D MD BAL MP P XP
DNAME = ['XD', 'D', 'MD', 'BAL', 'MP', 'P', 'XP']
SNAME = ['S50 fixed 50', 'ATR 1.5x', 'past XD', 'past D', 'past MD', 'past BAL', 'past MP', 'past P', 'past XD +12.5%',
         'past GMU open (c2 open)', 'past gap edge (c1 H/L)', 'past GMU low/high (3 candles)', 'past c3 low/high']
TGT = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 6.0])
XNAME = ['stop / target only', 'close through GMU open', 'gap filled (close through c1)', 'next session open']
FAM = ['BC+', 'BC-', 'C2', 'AFs', 'CI', 'S&D']
WAIT, HOLD, MINR, COST = 10, 100, 4.0, 1.0
NS, NT, NX = len(SNAME), len(TGT), len(XNAME)

@njit(cache=True)
def run_all(gi, gs, gsh, rlo, rhi, c2o, c1e, g3e, c3e, atr, tc, ke, ci, fo, fh, fl, fc, nxt, acc, nbar):
    nf = len(fh)
    for q in range(len(gi)):
        i = gi[q]; s = gs[q]; sh = gsh[q]
        k0 = ke[i]
        if k0 >= nf: continue
        kexp = ke[min(i + WAIT, nbar - 1)] - 1
        for ap in range(3):
            lo = rlo[q, ap]; hi = rhi[q, ap]; rg = hi - lo
            for d in range(7):
                frac = DEP_[d] if s == 1 else 1.0 - DEP_[d]
                lv = lo + frac * rg
                mk = (s == 1 and lv >= tc[i]) or (s == -1 and lv <= tc[i])
                if mk: lv = tc[i]
                # fill (cancel if a TF close goes through the GMU open first)
                kf = -1
                if mk:
                    kf = k0
                else:
                    for k in range(k0, min(kexp + 1, nf)):
                        if (s == 1 and fl[k] <= lv) or (s == -1 and fh[k] >= lv):
                            kf = k; break
                        # TF close check at the last fine bar of a TF candle
                        j = ci[k]
                        if k == ke[j] - 1:
                            if (s == 1 and tc[j] < c2o[q]) or (s == -1 and tc[j] > c2o[q]):
                                break
                if kf < 0: continue
                ep = lv
                cf = ci[kf]
                kmax = ke[min(cf + HOLD, nbar - 1)] - 1
                # violation exits (TF closes from the fill candle on)
                kv1 = -1; pv1 = 0.0; kv2 = -1; pv2 = 0.0
                for j in range(cf, min(cf + HOLD, nbar)):
                    if kv1 < 0 and ((s == 1 and tc[j] < c2o[q]) or (s == -1 and tc[j] > c2o[q])):
                        kv1 = ke[j]; pv1 = tc[j]
                    if kv2 < 0 and ((s == 1 and tc[j] < c1e[q]) or (s == -1 and tc[j] > c1e[q])):
                        kv2 = ke[j]; pv2 = tc[j]
                    if kv1 >= 0 and kv2 >= 0: break
                ksx = nxt[kf]; psx = fo[ksx] if ksx < nf else fc[nf - 1]
                for st in range(13):
                    if st == 0: sl = ep - s * 50.0
                    elif st == 1: sl = ep - s * 1.5 * atr[i]
                    elif st <= 7:
                        f2 = DEP_[st - 2] if s == 1 else 1.0 - DEP_[st - 2]
                        sl = lo + f2 * rg - s * 2 * 0.25
                    elif st == 8:
                        sl = (lo - 0.125 * rg - 0.5) if s == 1 else (hi + 0.125 * rg + 0.5)
                    elif st == 9: sl = c2o[q] - s * 0.5
                    elif st == 10: sl = c1e[q] - s * 0.5
                    elif st == 11: sl = g3e[q] - s * 0.5
                    else: sl = c3e[q] - s * 0.5
                    risk = s * (ep - sl)
                    if not (risk >= 4.0) or risk != risk: continue
                    # walk: stop index and first hit index of each target
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
                    cost = COST_ / risk
                    for t in range(6):
                        for x in range(4):
                            # earliest event
                            best = 1 << 60; r = 0.0
                            if ks >= 0: best = ks; r = -1.0
                            if kt[t] >= 0 and kt[t] < best: best = kt[t]; r = TGT_[t]
                            if x == 1 and kv1 >= 0 and kv1 <= best: best = kv1; r = s * (pv1 - ep) / risk
                            if x == 2 and kv2 >= 0 and kv2 <= best: best = kv2; r = s * (pv2 - ep) / risk
                            if x == 3 and ksx < nf and ksx <= best and ksx > kf: best = ksx; r = s * (psx - ep) / risk
                            if best == (1 << 60): r = s * (pend - ep) / risk
                            r -= cost
                            a = acc[sh, ap, d, st, t, x]
                            a[0] += 1; a[1] += r; a[2] += r * r
                            if r > 0: a[3] += 1; a[4] += r
                            else: a[5] -= r

DEP_ = DEP; TGT_ = TGT; COST_ = COST

def next_open_index(t_ns):
    t = pd.to_datetime(t_ns)
    m = (t.hour * 60 + t.minute).values
    day = t.normalize()
    opens = np.array([120, 480, 570])
    nxtm = np.full(len(m), 120 + 1440)
    for o in opens[::-1]:
        nxtm = np.where(m < o, o, nxtm)
    tgt = day.values + (nxtm * 60 * 1_000_000_000).astype('timedelta64[ns]')
    return np.searchsorted(t_ns, tgt.astype(np.int64), 'left')

def run(period, tf):
    d1 = raw()['fresh5' if (period == 'fresh' and tf == '5m') else period]; F = Fine(d1)
    d = bars(d1, tf)
    o, h, l, c, atr = d.open.values, d.high.values, d.low.values, d.close.values, d.atr.values
    n = len(d)
    ke = np.searchsorted(F.t, d.tend.values.astype('datetime64[ns]').astype(np.int64), 'left')
    ks0 = np.searchsorted(F.t, d.index.values.astype('datetime64[ns]').astype(np.int64), 'left')
    ci = np.searchsorted(ks0, np.arange(len(F.t)), 'right') - 1
    nxt = next_open_index(F.t)
    G = []
    for i in range(16, n - 1):
        a, b = i - 2, i - 1
        if c[b] > h[a] and l[i] - h[a] >= 2 * TICK: s = 1
        elif c[b] < l[a] and l[a] - h[i] >= 2 * TICK: s = -1
        else: continue
        ty = ctype(o[i], h[i], l[i], c[i], h[b], l[b])
        sh = FAM.index(family(ty)) * 2 + (0 if (lean(ty) == 'bull') == (s == 1) else 1)
        rl = [l[i], min(l[a:i+1]), l[a]]; rh = [h[i], max(h[a:i+1]), h[a]]
        G.append((i, s, sh, rl, rh, o[b], h[a] if s == 1 else l[a], min(l[a:i+1]) if s == 1 else max(h[a:i+1]), l[i] if s == 1 else h[i]))
    gi = np.array([x[0] for x in G]); gs = np.array([x[1] for x in G]); gsh = np.array([x[2] for x in G])
    rlo = np.array([x[3] for x in G]); rhi = np.array([x[4] for x in G])
    c2o = np.array([x[5] for x in G]); c1e = np.array([x[6] for x in G]); g3e = np.array([x[7] for x in G]); c3e = np.array([x[8] for x in G])
    acc = np.zeros((12, 3, 7, NS, NT, NX, 6))
    atr = np.nan_to_num(atr, nan=0.0)
    run_all(gi, gs, gsh, rlo, rhi, c2o, c1e, g3e, c3e, atr, c, ke, ci, F.o, F.h, F.l, F.c, nxt, acc, n)
    return acc, len(G)

if __name__ == '__main__':
    out = {}
    for period in ('old', 'fresh'):
        for tf in ('5m', '15m', '1h', '4h'):
            t = time.time(); acc, ng = run(period, tf); out[(period, tf)] = acc
            print(period, tf, ng, 'GMUs', round(time.time() - t), 's', flush=True)
    np.save('grid_acc.npy', np.stack([out[(p, tf)] for p in ('old', 'fresh') for tf in ('5m', '15m', '1h', '4h')]))
