"""GRADE: turn signals into trades, stats and the pass test (Max's rules built in).

Signals table (pandas): one row per signal with columns
   i (bar index of the signal close), s (+1 long / -1 short), and any tag columns you want to split by.
trades(d, sig, market, entries, stops, targets, exits, end=...)  pairs EVERY entry x stop x target x exit (no hand picking).
   entries : 'market' (signal close) or ('limit', col) = limit at sig[col], must fill within `fill` bars.
   stops   : 'fixed' (SPEC stop: NQ 50 / ES 20 / GC 12) | ('col', name) price column in sig | ('atr', k) k x ATR | ('pts', x)
   targets : R multiples (1, 2, 3 ...), None = no target, or ('col', name) a price column.
   exits   : 'stop/target' | ('flip', arr) exit at the close of bar where arr is True (e.g. next flip) | ('time', minutes_of_day)
             | ('half', r1) half off at r1 x risk, stop to break-even on the rest, runner to the target (None = to the end)
             | ('half_time', r1, minute) the same, everything out at minute of day.
   Every trade gets a RANDOM twin: same side, same stop size, same target in R, random bar in the same window (r_rand).
   Same-candle stop and target = stop wins. Cost per trade from SPEC.
table(T, by)   stats per group and period: n, WR (win rate), avg RR, PF (profit factor), t-score, random avg RR.
passes(G)      PASS = t-score >= 2 in BOTH periods (and 30+ trades each); also counts random passes as the luck level."""
import numpy as np, pandas as pd
from numba import njit
from . import data as D
from .candles import atr_rma


@njit(cache=True)
def sim(o, h, l, c, i, s, ep, stop, tgt, jEnd, cost, flip):
    """entry price ep at bar i (filled), stop / target from the next bar, exit at a flip bar close or at jEnd close.
    returns (R, exit bar). tgt = nan for none. flip = bool array (exit at that bar's close)."""
    risk = s * (ep - stop)
    if risk <= 0: return np.nan, i
    for j in range(i + 1, jEnd + 1):
        if (s == 1 and l[j] <= stop) or (s == -1 and h[j] >= stop):
            px = min(o[j], stop) if s == 1 else max(o[j], stop)
            return (s * (px - ep) - cost) / risk, j
        if tgt == tgt and ((s == 1 and h[j] >= tgt) or (s == -1 and l[j] <= tgt)):
            return (s * (tgt - ep) - cost) / risk, j
        if flip[j]:
            return (s * (c[j] - ep) - cost) / risk, j
    return (s * (c[jEnd] - ep) - cost) / risk, jEnd


@njit(cache=True)
def sim_half(o, h, l, c, i, s, ep, stop, r1, tgt, jEnd, cost, flip):
    """half off at r1 x risk, stop to break-even on the other half, runner to tgt (nan = none) / flip / jEnd. returns (R, exit bar)."""
    risk = s * (ep - stop)
    if risk <= 0: return np.nan, i
    t1 = ep + s * r1 * risk
    for j in range(i + 1, jEnd + 1):
        if (s == 1 and l[j] <= stop) or (s == -1 and h[j] >= stop):
            px = min(o[j], stop) if s == 1 else max(o[j], stop)
            return (s * (px - ep) - cost) / risk, j
        if (s == 1 and h[j] >= t1) or (s == -1 and l[j] <= t1):
            if tgt == tgt and ((s == 1 and h[j] >= tgt) or (s == -1 and l[j] <= tgt)):
                return (0.5 * r1 * risk + 0.5 * s * (tgt - ep) - cost) / risk, j
            for k in range(j + 1, jEnd + 1):
                if (s == 1 and l[k] <= ep) or (s == -1 and h[k] >= ep):
                    px = min(o[k], ep) if s == 1 else max(o[k], ep)
                    return (0.5 * r1 * risk + 0.5 * s * (px - ep) - cost) / risk, k
                if tgt == tgt and ((s == 1 and h[k] >= tgt) or (s == -1 and l[k] <= tgt)):
                    return (0.5 * r1 * risk + 0.5 * s * (tgt - ep) - cost) / risk, k
                if flip[k]:
                    return (0.5 * r1 * risk + 0.5 * s * (c[k] - ep) - cost) / risk, k
            return (0.5 * r1 * risk + 0.5 * s * (c[jEnd] - ep) - cost) / risk, jEnd
        if flip[j]:
            return (s * (c[j] - ep) - cost) / risk, j
    return (s * (c[jEnd] - ep) - cost) / risk, jEnd


@njit(cache=True)
def fill_limit(h, l, i, s, px, nmax):
    for j in range(i + 1, min(len(h), i + 1 + nmax)):
        if (s == 1 and l[j] <= px) or (s == -1 and h[j] >= px): return j
    return -1


def _name(x):
    if isinstance(x, str): return x
    if isinstance(x, tuple): return f'{x[0]} {x[1]}' if isinstance(x[1], (str, int, float)) else x[0]
    return str(x)


def trades(d, sig, market, entries=('market',), stops=('fixed',), targets=(2,), exits=('stop/target',), end=None, fill=10, seed=1, window=None):
    """end: array of the last bar index allowed for each signal (e.g. session end), default = 2000 bars later.
    window: (start_bar_array, end_bar_array) to draw the random twin from (default = 200 bars before the signal .. end)."""
    sp = D.SPEC[market]
    o, h, l, c = (d[k].values.astype(np.float64) for k in ('open', 'high', 'low', 'close'))
    n = len(c); atr = atr_rma(h, l, c, 14)
    I = sig.i.values.astype(np.int64); S = sig.s.values.astype(np.int64)
    E = np.minimum(n - 1, I + 2000) if end is None else np.asarray(end, np.int64)
    W0 = np.maximum(1, I - 200) if window is None else np.asarray(window[0], np.int64)
    W1 = E if window is None else np.asarray(window[1], np.int64)
    rng = np.random.default_rng(seed)
    nofl = np.zeros(n, np.bool_)
    mn = d.index.hour.values * 60 + d.index.minute.values
    rows = []
    tags = [k for k in sig.columns if k not in ('i', 's')]
    for k in range(len(I)):
        i, s, jE = I[k], S[k], E[k]
        if i >= n - 1: continue
        rj = int(rng.integers(W0[k], max(W0[k] + 1, W1[k] - 5)))
        for en in entries:
            if en == 'market': fi, ep = i, c[i]
            else:
                px = float(sig[en[1]].values[k])
                if not np.isfinite(px): continue
                fi = fill_limit(h, l, i, s, px, fill)
                if fi < 0: continue
                ep = px if not ((s == 1 and o[fi] < px) or (s == -1 and o[fi] > px)) else o[fi]
            for st in stops:
                if st == 'fixed': sl = ep - s * sp['stop']
                elif st[0] == 'col': sl = float(sig[st[1]].values[k])
                elif st[0] == 'atr': sl = ep - s * st[1] * atr[i]
                elif st[0] == 'pts': sl = ep - s * st[1]
                risk = s * (ep - sl)
                if not np.isfinite(risk) or risk <= 0.04 * sp['stop']: continue
                for tg in targets:
                    if tg is None: tp = np.nan
                    elif isinstance(tg, tuple): tp = float(sig[tg[1]].values[k])
                    else: tp = ep + s * tg * risk
                    if np.isfinite(tp) and s * (tp - ep) <= 0: continue
                    for ex in exits:
                        fl = ex[1] if isinstance(ex, tuple) and ex[0] == 'flip' else nofl
                        tmin = ex[1] if isinstance(ex, tuple) and ex[0] == 'time' else ex[2] if isinstance(ex, tuple) and ex[0] == 'half_time' else None
                        def _end(a):
                            if tmin is None: return jE
                            later = np.where(mn[a + 1:jE + 1] >= tmin)[0] if mn[a] < tmin else np.where((mn[a + 1:jE + 1] >= tmin) & (mn[a + 1:jE + 1] < mn[a]))[0]
                            return a + 1 + later[0] if len(later) else jE
                        jEnd = _end(fi); rEnd = max(rj + 1, _end(rj))
                        rtp = np.nan if not np.isfinite(tp) else c[rj] + (tp - ep)
                        if isinstance(ex, tuple) and ex[0] in ('half', 'half_time'):
                            r, jx = sim_half(o, h, l, c, fi, s, ep, sl, float(ex[1]), tp, jEnd, sp['cost'], fl)
                            rr, _ = sim_half(o, h, l, c, rj, s, c[rj], c[rj] - s * risk, float(ex[1]), rtp, rEnd, sp['cost'], fl)
                        else:
                            r, jx = sim(o, h, l, c, fi, s, ep, sl, tp, jEnd, sp['cost'], fl)
                            rr, _ = sim(o, h, l, c, rj, s, c[rj], c[rj] - s * risk, rtp, rEnd, sp['cost'], fl)
                        row = dict(te=d.index[fi], tx=d.index[jx], s=s, entry=_name(en), stop=_name(st), target=_name(tg) if tg is not None else 'none',
                                   exit=_name(ex), r=r, r_rand=rr, risk=risk)
                        for t in tags: row[t] = sig[t].values[k]
                        rows.append(row)
    T = pd.DataFrame(rows)
    if 'per' in d.columns and len(T): T['per'] = d.per.reindex(T.te).values
    return T


def stats(x):
    x = pd.Series(x).dropna(); n = len(x)
    if n < 2: return dict(n=n, wr=np.nan, avg=np.nan, pf=np.nan, t=np.nan)
    pos = x[x > 0].sum(); neg = -x[x <= 0].sum()
    return dict(n=n, wr=(x > 0).mean(), avg=x.mean(), pf=pos / neg if neg > 0 else np.nan, t=x.mean() / x.std(ddof=1) * np.sqrt(n))


def table(T, by, per=('P1', 'P2')):
    out = []
    for k, g in T.groupby(by):
        row = dict(zip(by, k if isinstance(k, tuple) else (k,)))
        for p in per:
            x = g[g.per == p]; s = stats(x.r); rs = stats(x.r_rand)
            q = p[-1]
            row.update({f'n{q}': s['n'], f'WR{q}': s['wr'], f'avgRR{q}': s['avg'], f'PF{q}': s['pf'], f't{q}': s['t'], f'rand{q}': rs['avg'], f'rand_t{q}': rs['t']})
        out.append(row)
    return pd.DataFrame(out)


def passes(G, nmin=30):
    ok = (G.n1 >= nmin) & (G.n2 >= nmin)
    G = G.assign(PASS=ok & (G.t1 >= 2) & (G.t2 >= 2), RAND_PASS=ok & (G.rand_t1 >= 2) & (G.rand_t2 >= 2))
    print(f'combos with {nmin}+ trades in both periods: {int(ok.sum())} | PASS: {int(G.PASS.sum())} | random PASS (luck level): {int(G.RAND_PASS.sum())}')
    return G
