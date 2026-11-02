"""Trade simulator for the re-check (Nov 2 2026): scale-outs (e.g. Okala 2 of 3 off at +15), break-even rules,
trailing exits, and a random twin for every trade (same side, same stop size, same targets in points, random bar).
Same-candle stop and target = stop wins. Cost per trade from SPEC (NQ 1 pt)."""
import sys, numpy as np, pandas as pd
from numba import njit
sys.path.insert(0, '/home/claude/mmmlab')
from mmmlab import data as D
from mmmlab.grade import fill_limit


@njit(cache=True)
def sim_scale(o, h, l, c, i, s, ep, stop, lpx, lfr, be_first, tgt, jEnd, cost, flip, bemode, hid, hop):
    """legs: prices lpx with fractions lfr (in order). After the first leg fills the stop goes to break-even if be_first.
    The rest runs to tgt (nan = none) / flip close / jEnd close.
    bemode 1: stop to break-even at a close in profit once a NEW hour has started and price is past that hour's open (Kane).
    returns (R, exit bar)."""
    risk = s * (ep - stop)
    if risk <= 0: return np.nan, i
    left = 1.0; got = 0.0; k = 0; nl = len(lpx); sl = stop; h0 = hid[i]
    for j in range(i + 1, jEnd + 1):
        if (s == 1 and l[j] <= sl) or (s == -1 and h[j] >= sl):
            px = min(o[j], sl) if s == 1 else max(o[j], sl)
            return (got + left * s * (px - ep) - cost) / risk, j
        while k < nl and ((s == 1 and h[j] >= lpx[k]) or (s == -1 and l[j] <= lpx[k])):
            f = min(lfr[k], left); got += f * s * (lpx[k] - ep); left -= f; k += 1
            if be_first: sl = ep
        if left <= 1e-9: return (got - cost) / risk, j
        if tgt == tgt and ((s == 1 and h[j] >= tgt) or (s == -1 and l[j] <= tgt)):
            return (got + left * s * (tgt - ep) - cost) / risk, j
        if flip[j]:
            return (got + left * s * (c[j] - ep) - cost) / risk, j
        if bemode == 1 and hid[j] != h0 and s * (c[j] - hop[j]) > 0 and s * (c[j] - ep) > 0:
            sl = ep
    return (got + left * s * (c[jEnd] - ep) - cost) / risk, jEnd


def trades(d, sig, market, entries, stops, targets, exits, end, window, fill=10, seed=7):
    """entries: 'market' | ('limit', col).   stops: 'fixed' (Max 50 pt NQ / 20 ES) | ('pts', x) | ('col', name).
    targets: ('R', x) | ('pts', x) | ('col', name) | None.  Runner target after the legs.
    exits: dicts  {name, legs: [(kind, x, frac)] kind 'pts' or 'R', be: bool, flip: {1: arr, -1: arr} or None, bemode: 0/1}."""
    sp = D.SPEC[market]
    o, h, l, c = (d[k].values.astype(np.float64) for k in ('open', 'high', 'low', 'close'))
    n = len(c); idx = d.index
    hid = (idx.dayofyear.values * 24 + idx.hour.values).astype(np.int64)
    hop = pd.Series(o).groupby(hid).transform('first').values.astype(np.float64)
    I = sig.i.values.astype(np.int64); S = sig.s.values.astype(np.int64)
    E = np.asarray(end, np.int64); W0 = np.asarray(window[0], np.int64); W1 = np.asarray(window[1], np.int64)
    rng = np.random.default_rng(seed); nofl = np.zeros(n, np.bool_)
    tags = [k for k in ('tag',) if k in sig.columns]
    rows = []
    for k in range(len(I)):
        i, s, jE = I[k], S[k], E[k]
        if i >= n - 2 or jE <= i: continue
        rj = int(rng.integers(W0[k], max(W0[k] + 1, W1[k] - 5)))
        rE = max(rj + 1, min(n - 1, rj + (jE - i)))
        for en in entries:
            if en == 'market': fi, ep = i, c[i]
            else:
                px = float(sig[en[1]].values[k])
                if not np.isfinite(px): continue
                fi = fill_limit(h, l, i, s, px, fill)
                if fi < 0 or fi >= jE: continue
                ep = px if not ((s == 1 and o[fi] < px) or (s == -1 and o[fi] > px)) else o[fi]
            for st in stops:
                if st == 'fixed': sl = ep - s * sp['stop']
                elif st[0] == 'pts': sl = ep - s * st[1]
                else: sl = float(sig[st[1]].values[k])
                risk = s * (ep - sl)
                if not np.isfinite(risk) or risk <= 0.04 * sp['stop']: continue
                for tg in targets:
                    if tg is None: tp = np.nan
                    elif tg[0] == 'R': tp = ep + s * tg[1] * risk
                    elif tg[0] == 'pts': tp = ep + s * tg[1]
                    else: tp = float(sig[tg[1]].values[k])
                    if np.isfinite(tp) and s * (tp - ep) <= 0: continue
                    for ex in exits:
                        lp = []; lf = []
                        for kind, x, fr in ex.get('legs', []):
                            dist = x if kind == 'pts' else x * risk
                            lp.append(dist); lf.append(fr)
                        lp = np.array(lp, np.float64); lf = np.array(lf, np.float64)
                        if np.isfinite(tp) and len(lp) and s * (tp - ep) <= lp[0]: continue   # target closer than the first scale
                        fl = ex['flip'][s] if ex.get('flip') else nofl
                        bm = ex.get('bemode', 0); bf = ex.get('be', True)
                        if en != 'market' and ((s == 1 and l[fi] <= sl) or (s == -1 and h[fi] >= sl)):
                            r, jx = (-risk - sp['cost']) / risk, fi          # limit filled and stop touched in the same bar: count the loss
                        else:
                            r, jx = sim_scale(o, h, l, c, fi, s, ep, sl, ep + s * lp, lf, bf, tp, jE, sp['cost'], fl, bm, hid, hop)
                        e2 = c[rj]; rtp = np.nan if not np.isfinite(tp) else e2 + (tp - ep)
                        rr, _ = sim_scale(o, h, l, c, rj, s, e2, e2 - s * risk, e2 + s * lp, lf, bf, rtp, rE, sp['cost'], fl, bm, hid, hop)
                        row = dict(te=idx[fi], tx=idx[jx], s=s, entry=en if isinstance(en, str) else f'limit {en[1]}',
                                   stop=st if isinstance(st, str) else f'{st[0]} {st[1]}', target='none' if tg is None else f'{tg[0]} {tg[1]}',
                                   exit=ex['name'], r=r, r_rand=rr, risk=risk)
                        for t in tags: row[t] = sig[t].values[k]
                        rows.append(row)
    T = pd.DataFrame(rows)
    if len(T): T['per'] = d.per.reindex(T.te).values if 'per' in d.columns else 'P1'
    return T


def st(x):
    x = pd.Series(x).dropna(); n = len(x)
    if n < 2: return dict(n=n, wr=np.nan, avg=np.nan, pf=np.nan, t=np.nan)
    pos = x[x > 0].sum(); neg = -x[x <= 0].sum()
    return dict(n=n, wr=(x > 0).mean(), avg=x.mean(), pf=pos / neg if neg > 0 else np.nan, t=x.mean() / x.std(ddof=1) * np.sqrt(n) if x.std() > 0 else np.nan)
