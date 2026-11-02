"""Two ways to score the replica's setups.

ind_sim   = exactly the indicator's Layer-3 math: the trade is checked on the SAME bar it is created,
            entry and target/stop all read from that bar's high/low, target checked first.
honest    = what a trader could really get:
            • touch entries ①②③④ (limit at a level known before the touch): filled at the first 1m bar
              that touches the level; a stop hit in that 1m bar = loss; the target only counts from the next 1m bar.
            • ⑤ BuX/BeX and ⑥ LQG (entry = OPEN of the signal candle, already in the past):
              'close'  = market order at the signal candle CLOSE, same stop, target re-drawn at 2R from the close
              'limit'  = limit order at the candle OPEN, working from the NEXT bar (missed if the target comes first)
            • 1m bar touching both stop and target = loss. No slippage. Expiry after 500 chart bars at the close.
"""
import numpy as np, pandas as pd, math
from replica import TICK, RR, RISK, category

TOUCH = ('①', '②', '③', '④')


def ind_sim(tr, h, l, c):
    i0 = tr['i']; ep, sl, tp, lg = tr['ep'], tr['sl'], tr['tp'], tr['long']
    act = False
    n = len(h)
    for j in range(i0, n):
        force = (j - i0) > 500
        if not act:
            if (l[j] <= ep) if lg else (h[j] >= ep):
                act = True
            else:
                if ((h[j] >= tp) or (l[j] <= sl)) if lg else ((l[j] <= tp) or (h[j] >= sl)):
                    return None, 'missed', j
        if act and not force:
            tph = (h[j] >= tp) if lg else (l[j] <= tp)
            slh = (l[j] <= sl) if lg else (h[j] >= sl)
            if tph or slh:
                x = tp if tph else sl
                return ((x - ep) if lg else (ep - x)) / abs(ep - sl), 'tp' if tph else 'sl', j
        if force:
            if act:
                return ((c[j] - ep) if lg else (ep - c[j])) / abs(ep - sl), 'exp', j
            return None, 'expired', j
    return None, 'open', n - 1


class Fine:
    """finest bars available, each tagged with its chart-bar index."""
    def __init__(self, fine_df, chart_index):
        self.t = fine_df.index.values
        self.o = fine_df.open.values; self.h = fine_df.high.values; self.l = fine_df.low.values; self.c = fine_df.close.values
        ci = np.searchsorted(chart_index.values, self.t, side='right') - 1
        self.ci = ci
        # first fine bar of each chart bar
        self.first = np.searchsorted(ci, np.arange(len(chart_index)), side='left')


def walk(F, k0, ep, sl, tp, lg, i0, skip_tp_first=True):
    """position open from fine bar k0 (filled inside k0). returns R, how."""
    h, l, c, ci = F.h, F.l, F.c, F.ci
    n = len(h)
    risk = abs(ep - sl)
    for k in range(k0, n):
        if ci[k] - i0 > 500:
            x = c[k - 1]
            return ((x - ep) if lg else (ep - x)) / risk, 'exp'
        slh = (l[k] <= sl) if lg else (h[k] >= sl)
        tph = (h[k] >= tp) if lg else (l[k] <= tp)
        if slh:
            return -1.0 * abs(sl - ep) / risk, 'sl'
        if tph and not (k == k0 and skip_tp_first):
            return abs(tp - ep) / risk, 'tp'
    return None, 'open'


def redraw(lg, ep, sl, pv):
    rp = math.floor(abs(ep - sl) / TICK + 0.5) * TICK
    if rp < 4 * TICK:
        rp = 4 * TICK; sl = ep - rp if lg else ep + rp
    if (lg and sl >= ep) or ((not lg) and sl <= ep):
        return None
    tp = ep + rp * RR if lg else ep - rp * RR
    ps = int(max(1, math.floor(RISK / max(rp * pv, TICK) + 0.5)))
    ar = rp * pv * ps
    if ar > RISK * 1.05:
        return None
    return sl, tp, ps, ar


def honest(tr, F, chart_c, pv, mode='close', fixed=None):
    """returns (R, how, ps, arisk) or None when no trade."""
    lg, ep, sl, tp, i0 = tr['long'], tr['ep'], tr['sl'], tr['tp'], tr['i']
    et = tr['etype']
    if any(k in et for k in TOUCH):
        k_lo = F.first[i0]; k_hi = F.first[i0 + 1] if i0 + 1 < len(F.first) else len(F.h)
        k0 = None
        for k in range(k_lo, k_hi):
            if (F.l[k] <= ep) if lg else (F.h[k] >= ep):
                k0 = k; break
        if k0 is None:
            k0 = k_lo
        if fixed:
            sl = ep - fixed if lg else ep + fixed; tp = ep + 2 * fixed if lg else ep - 2 * fixed
            ps = int(max(1, math.floor(RISK / (fixed * pv) + 0.5))); ar = fixed * pv * ps
        else:
            ps, ar = tr['ps'], tr['arisk']
        r, how = walk(F, k0, ep, sl, tp, lg, i0)
        return (r, how, ps, ar) if r is not None else None
    # ⑤ / ⑥ : entry was the candle OPEN
    if i0 + 1 >= len(F.first):
        return None
    k_next = F.first[i0 + 1]
    if mode == 'close':
        ep2 = chart_c[i0]
        if fixed:
            sl2 = ep2 - fixed if lg else ep2 + fixed; tp2 = ep2 + 2 * fixed if lg else ep2 - 2 * fixed
            ps = int(max(1, math.floor(RISK / (fixed * pv) + 0.5))); ar = fixed * pv * ps
        else:
            rd = redraw(lg, ep2, sl, pv)
            if rd is None:
                return None
            sl2, tp2, ps, ar = rd
        r, how = walk(F, k_next, ep2, sl2, tp2, lg, i0, skip_tp_first=False)
        return (r, how, ps, ar) if r is not None else None
    # limit at the open, from the next bar
    if fixed:
        sl = ep - fixed if lg else ep + fixed; tp = ep + 2 * fixed if lg else ep - 2 * fixed
        ps = int(max(1, math.floor(RISK / (fixed * pv) + 0.5))); ar = fixed * pv * ps
    else:
        ps, ar = tr['ps'], tr['arisk']
    n = len(F.h)
    for k in range(k_next, n):
        if F.ci[k] - i0 > 500:
            return None
        if (F.l[k] <= ep) if lg else (F.h[k] >= ep):
            r, how = walk(F, k, ep, sl, tp, lg, i0)
            return (r, how, ps, ar) if r is not None else None
        if (F.h[k] >= tp) if lg else (F.l[k] <= tp):
            return None  # target first = missed
    return None


def stats(R, fees=None):
    R = np.asarray(R, float)
    n = len(R)
    if n == 0:
        return dict(N=0)
    w = R[R > 0].sum(); ls = -R[R < 0].sum()
    sd = R.std(ddof=1) if n > 1 else np.nan
    d = dict(N=n, WR=(R > 0).mean() * 100, avgRR=R.mean(), PF=w / ls if ls > 0 else np.inf,
             t=R.mean() / (sd / math.sqrt(n)) if n > 1 and sd > 0 else np.nan)
    if fees is not None:
        Rn = R - np.asarray(fees)
        d['avgRR_net'] = Rn.mean()
        sdn = Rn.std(ddof=1) if n > 1 else np.nan
        d['t_net'] = Rn.mean() / (sdn / math.sqrt(n)) if n > 1 and sdn > 0 else np.nan
    return d
