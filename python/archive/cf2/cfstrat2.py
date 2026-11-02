"""More Chart Fanatics strategies coded from their pages / episode summaries (Nov 2 2026). Same output format as cf/cfstrat.py:
i, s, wk (structure stop), tp (trader's own target or nan), lim (limit price or nan), endb, w0, w1, tag.
Every gap in the trader's rules is filled with ONE stated assumption (ASSUME)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/mmmlab'); sys.path.insert(0, '/home/claude/cf')
from mmmlab import data as D
from mmmlab.candles import atr_rma
from cfstrat import base, out, endbar, swings, NQSTOP


def ema(c, n): return pd.Series(c).ewm(span=n, adjust=False).mean().values


def fractals(h, l, k):
    n = len(h); sh = np.zeros(n, bool); sl = np.zeros(n, bool)
    for j in range(k, n - k):
        if h[j] >= h[j - k:j + k + 1].max(): sh[j] = True
        if l[j] <= l[j - k:j + k + 1].min(): sl[j] = True
    return sh, sl


def prev_daily_dir(d, sym):
    """direction of the previous completed session candle (18:00-17:00) for each bar"""
    dd = D.daily(sym); dirn = np.sign(dd.close - dd.open).shift(1)
    return dirn.reindex(D.sday(d.index)).values


# ---------------------------------------------------------------- TG Capital - Trident (30m, London kill zone)
def tg_capital(d, m, sym):
    """EMA 5>9>13>21 stacked + price beyond EMA200 + previous daily candle in the trade direction (ASSUME for his strength indicator).
    A 30m FVG completes 02:30-04:00 NY. A small doji (body <= 30% of range, ASSUME) wicks into the FVG's 50% (CE) and closes back
    inside / beyond the gap, then the next candle closes beyond the doji's high (long) = entry (ASSUME the logical direction).
    Entries 03:00-06:30. Stop: low of the first FVG candle. Exit: first close where the EMA stack breaks (his 'ride the trend')."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; n = len(c)
    e5, e9, e13, e21, e200 = ema(c, 5), ema(c, 9), ema(c, 13), ema(c, 21), ema(c, 200)
    up = (e5 > e9) & (e9 > e13) & (e13 > e21) & (c > e200); dn = (e5 < e9) & (e9 < e13) & (e13 < e21) & (c < e200)
    pdir = prev_daily_dir(d, sym)
    rows = []
    for k_, ix in days.items():
        fz = [q for q in ix if 150 <= mn[q] < 240 and q >= 2]
        done = {1: False, -1: False}
        for q in fz:
            for s in (1, -1):
                if done[s]: continue
                gap = (l[q] > h[q - 2]) if s == 1 else (h[q] < l[q - 2])
                if not gap: continue
                top, bot = (l[q], h[q - 2]) if s == 1 else (l[q - 2], h[q])
                ce = (top + bot) / 2
                for j in range(q + 1, min(q + 8, n - 1)):
                    if mn[j] > 390 or sd[j] != k_: break
                    rng = h[j] - l[j]
                    if rng <= 0 or abs(c[j] - o[j]) > .3 * rng: continue
                    if s == 1 and not (l[j] <= ce and c[j] >= bot): continue
                    if s == -1 and not (h[j] >= ce and c[j] <= top): continue
                    i = j + 1
                    if not (180 <= mn[i] <= 390) or sd[i] != k_: break
                    trig = c[i] > h[j] if s == 1 else c[i] < l[j]
                    ok = (up[i] if s == 1 else dn[i]) and pdir[i] == s
                    if trig and ok:
                        wk = l[q - 2] - tick if s == 1 else h[q - 2] + tick
                        rows.append((i, s, wk, np.nan, ce, min(n - 1, i + 960), max(1, i - 48), min(n - 1, i + 48), 'Trident'))
                        done[s] = True
                    break
    S = out(rows)
    flip = {1: ~up, -1: ~dn}
    return S, flip


# ---------------------------------------------------------------- Tori Trades - trendline bounce / break (4H)
def tori(d, m):
    """Pivots = 4H fractals (3 / 3). A trendline needs 2 pivots at least 42 4H candles apart (about one week, ASSUME) with no close
    through the line between them; each new pivot redraws the line from the best earlier anchor. Touches = pivots on the line.
    BOUNCE: price comes back to the live line (low within 0.25 ATR) and closes on the right side = trade with the line;
      stop = line -/+ 0.5 ATR (her Safety Line = the trendline).
    BREAK: a 4H close through the live opposite line, with a live Safety Line (the other line) no more than 2 ATR away;
      stop just beyond the Safety Line. Tag = 2-touch or 3+ touch line. She trails and has no target: exits = R targets or the
      exit at the first 4H close back through the sloped line (her trail along the line), max 2000 candles."""
    o, h, l, c, v, mn, sd, days = base(d); n = len(c)
    atr = atr_rma(h, l, c, 14); sh, sl = fractals(h, l, 3)
    PL, PH = [], []; up = dn = None; rows = []
    def mk(P, val, s):
        b_ = P[-1]
        for a_ in reversed(P[:-1]):
            if b_ - a_ < 42: continue
            if (s == 1 and val[a_] >= val[b_]) or (s == -1 and val[a_] <= val[b_]): continue
            sl_ = (val[b_] - val[a_]) / (b_ - a_); xs = np.arange(a_, b_ + 1); ln = val[a_] + sl_ * (xs - a_)
            if (s == 1 and (c[a_:b_ + 1] < ln - 1e-9).any()) or (s == -1 and (c[a_:b_ + 1] > ln + 1e-9).any()): continue
            tch = sum(1 for p in P if a_ <= p <= b_ and abs(val[p] - (val[a_] + sl_ * (p - a_))) <= .25 * atr[p] if atr[p] == atr[p])
            return dict(a=a_, b=b_, y=val[a_], m=sl_, t=max(tch, 2), used=False)
        return None
    lv = lambda L, x: L['y'] + L['m'] * (x - L['a'])
    def xbar(L, s, i):      # her exit: the first 4H close through the (sloped) line she trails along
        for j in range(i + 1, min(n, i + 2000)):
            if (s == 1 and c[j] < lv(L, j)) or (s == -1 and c[j] > lv(L, j)): return j
        return min(n - 1, i + 2000)
    for i in range(60, n):
        j = i - 3
        if sl[j]: PL.append(j); up = mk(PL, l, 1) or up
        if sh[j]: PH.append(j); dn = mk(PH, h, -1) or dn
        a_ = atr[i]
        if not (a_ == a_ and a_ > 0): continue
        e = min(n - 1, i + 2000); w0, w1 = max(1, i - 100), min(n - 1, i + 100)
        if up is not None and c[i] < lv(up, i):
            if dn is not None and lv(dn, i) - c[i] <= 2 * a_ and c[i] < lv(dn, i) and c[i - 1] >= lv(up, i - 1):
                rows.append((i, -1, lv(dn, i) + .25 * a_, np.nan, np.nan, xbar(dn, -1, i), w0, w1, f'Break {"3+" if up["t"] >= 3 else "2"}-touch'))
            up = None
        if dn is not None and c[i] > lv(dn, i):
            if up is not None and c[i] - lv(up, i) <= 2 * a_ and c[i] > lv(up, i) and c[i - 1] <= lv(dn, i - 1):
                rows.append((i, 1, lv(up, i) - .25 * a_, np.nan, np.nan, xbar(up, 1, i), w0, w1, f'Break {"3+" if dn["t"] >= 3 else "2"}-touch'))
            dn = None
        if up is not None and not up['used'] and i > up['b'] + 3 and l[i] <= lv(up, i) + .25 * a_ and c[i] > lv(up, i):
            rows.append((i, 1, lv(up, i) - .5 * a_, np.nan, np.nan, xbar(up, 1, i), w0, w1, f'Bounce {"3+" if up["t"] >= 3 else "2"}-touch')); up['used'] = True
        if dn is not None and not dn['used'] and i > dn['b'] + 3 and h[i] >= lv(dn, i) - .25 * a_ and c[i] < lv(dn, i):
            rows.append((i, -1, lv(dn, i) + .5 * a_, np.nan, np.nan, xbar(dn, -1, i), w0, w1, f'Bounce {"3+" if dn["t"] >= 3 else "2"}-touch')); dn['used'] = True
    return out(rows)


# ---------------------------------------------------------------- Jade Cap - Intraday Liquidity & Volatility (NY 9:30-11:30)
def jadecap(d, m, sym, DL):
    """Bias = previous daily candle (ASSUME). Levels: previous day H / L, Asia 20:00-00:00, London 02:00-05:00 (ASSUME hours).
    Bearish bias: a high level is raided 09:30-11:30; the first bearish FVG after the raid = entry (limit at its near edge, or market
    at the FVG candle close). Stop above the raid high. Target = nearest unswept opposite level. Flat 12:15. One trade a day."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']
    pdir = prev_daily_dir(d, sym)
    f = D.fine(sym); fm = f.index.hour * 60 + f.index.minute; fs = D.sday(f.index)
    asia = f[(fm >= 1200)]; lon = f[(fm >= 120) & (fm < 300)]
    AH = asia.high.groupby(D.sday(asia.index)).max(); AL = asia.low.groupby(D.sday(asia.index)).min()
    LH = lon.high.groupby(D.sday(lon.index)).max(); LL = lon.low.groupby(D.sday(lon.index)).min()
    rows = []
    for k, ix in days.items():
        if k not in DL.index: continue
        win = ix[(mn[ix] >= 570) & (mn[ix] < 690)]
        if len(win) < 5: continue
        s = -1 if pdir[win[0]] == -1 else 1 if pdir[win[0]] == 1 else 0
        if not s: continue
        r = DL.loc[k]
        hiL = [x for x in (r.pH, AH.get(k, np.nan), LH.get(k, np.nan)) if x == x]
        loL = [x for x in (r.pL, AL.get(k, np.nan), LL.get(k, np.nan)) if x == x]
        lv = hiL if s == -1 else loL
        e = endbar(ix, mn, 735)
        took = False
        for i0 in win:
            if took: break
            hit = [L for L in lv if (s == -1 and h[i0] > L and h[i0 - 1] <= L) or (s == 1 and l[i0] < L and l[i0 - 1] >= L)]
            if not hit: continue
            ext = h[i0] if s == -1 else l[i0]
            for q in range(i0 + 1, min(i0 + 25, win[-1] + 1)):
                ext = max(ext, h[q]) if s == -1 else min(ext, l[q])
                gap = (h[q] < l[q - 2]) if s == -1 else (l[q] > h[q - 2])
                if gap and q - 2 >= i0:
                    near = h[q] if s == -1 else l[q]
                    tg = [x for x in (loL if s == -1 else hiL) if s * (x - c[q]) > 0]
                    tp = (max(tg) if s == -1 else min(tg)) if tg else np.nan
                    rows.append((q, s, ext + tick if s == -1 else ext - tick, tp, near, e, win[0], e, 'Raid + FVG')); took = True; break
            break
    return out(rows)


# ---------------------------------------------------------------- Trader Kane - SMT divergence + PO3 (needs NQ and ES together)
def kane(dn, de, m_trade='NQ'):
    """dn / de = NQ and ES bars on the same chart (aligned by time). Reference high = max(previous day high, overnight 18:00-09:30 high)
    per market (ASSUME). 09:30-11:00: bearish SMT = one market trades above its reference high while the other has not (since 9:30).
    Then the latest bullish FVG of the push (last 20 candles) breaks: a close below its bottom = entry (market; limit = retest of it).
    Stop above the SMT high. Target = 50% of the impulse (09:30 low to the SMT high). Longs mirror. One trade a day."""
    J = dn.join(de, how='inner', lsuffix='', rsuffix='_e')
    o, h, l, c = (J[k].values for k in ('open', 'high', 'low', 'close')); he, le = J.high_e.values, J.low_e.values
    mn = J.index.hour.values * 60 + J.index.minute.values; sd = D.sday(J.index).values
    tick = .25; rows = []
    days = {k: x.values for k, x in pd.Series(np.arange(len(J))).groupby(sd)}
    keys = sorted(days)
    for di, k in enumerate(keys):
        if di == 0: continue
        prev = days[keys[di - 1]]; ix = days[k]
        on = ix[(mn[ix] >= 1080) | (mn[ix] < 570)]; win = ix[(mn[ix] >= 570) & (mn[ix] < 660)]
        if len(win) < 10 or not len(on): continue
        refH = max(h[prev].max(), h[on].max()); refL = min(l[prev].min(), l[on].min())
        refHe = max(he[prev].max(), he[on].max()); refLe = min(le[prev].min(), le[on].min())
        e = endbar(ix, mn, 960); took = False
        nqH = esH = nqL = esL = False; armed = 0; xH = -np.inf; xL = np.inf; b0 = win[0]
        for i in win:
            if took: break
            nqH |= h[i] > refH; esH |= he[i] > refHe; nqL |= l[i] < refL; esL |= le[i] < refLe
            if armed == 0:
                if nqH != esH: armed = -1
                elif nqL != esL: armed = 1
            if armed == -1:
                xH = max(xH, h[i])
                for q in range(i - 1, max(i - 20, b0), -1):
                    if l[q] > h[q - 2]: bot = h[q - 2]; break
                else: continue
                if c[i] < bot and c[i - 1] >= bot:
                    lo = l[b0:i + 1].min(); tp = (xH + lo) / 2
                    rows.append((i, -1, xH + tick, tp, bot, e, b0, e, 'SMT short')); took = True
            elif armed == 1:
                xL = min(xL, l[i])
                for q in range(i - 1, max(i - 20, b0), -1):
                    if h[q] < l[q - 2]: top = l[q - 2]; break
                else: continue
                if c[i] > top and c[i - 1] <= top:
                    hi = h[b0:i + 1].max(); tp = (xL + hi) / 2
                    rows.append((i, 1, xL - tick, tp, top, e, b0, e, 'SMT long')); took = True
    S = out(rows)
    return S, J[['open', 'high', 'low', 'close', 'volume']]


# ---------------------------------------------------------------- Tanja Trades - AMD (accumulation 06:00-08:30)
def tanja(d, m, news_days=None):
    """Accumulation = 06:00-08:30 range (ASSUME). Manipulation = a sweep beyond one side 08:30-10:30 (no trade on the sweep).
    Displacement = a 5m close beyond the latest opposite 2/2 fractal swing with a 3-candle FVG in the move; entry = limit at the FVG's
    near edge until 11:10 (never chase). Stop beyond the sweep extreme. Target = the other side of the range. news_days = set of
    session days (her news filter); None = every day."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']
    sh, sl = swings(h, l, 2)
    rows = []
    for k, ix in days.items():
        acc = ix[(mn[ix] >= 360) & (mn[ix] < 510)]; win = ix[(mn[ix] >= 510) & (mn[ix] < 630)]
        if len(acc) < 3 or len(win) < 5: continue
        RH, RL = h[acc].max(), l[acc].min(); e = endbar(ix, mn, 670)
        tag = 'news day' if news_days is not None and k in news_days else 'other day'
        for s in (-1, 1):                    # s = trade side; short after a sweep of the high
            sw = [i for i in win if (s == -1 and h[i] > RH) or (s == 1 and l[i] < RL)]
            if not sw: continue
            i0 = sw[0]; ext = h[i0] if s == -1 else l[i0]
            lastS = np.nan; took = False
            for i in range(i0, min(i0 + 30, ix[-1])):
                if mn[i] >= 670 or sd[i] != k: break
                ext = max(ext, h[i]) if s == -1 else min(ext, l[i])
                j = i - 2
                if s == -1 and sl[j]: lastS = l[j]
                if s == 1 and sh[j]: lastS = h[j]
                if lastS != lastS: continue
                brk = (c[i] < lastS) if s == -1 else (c[i] > lastS)
                gap = any((h[q] < l[q - 2]) if s == -1 else (l[q] > h[q - 2]) for q in range(i - 2, i + 1))
                if brk and gap:
                    for q in range(i, i - 3, -1):
                        if (s == -1 and h[q] < l[q - 2]) or (s == 1 and l[q] > h[q - 2]): near = h[q] if s == -1 else l[q]; break
                    tp = RL if s == -1 else RH
                    if s * (tp - c[i]) > 0:
                        rows.append((i, s, ext + tick if s == -1 else ext - tick, tp, near, e, win[0], e, tag)); took = True
                    break
            if took: break
    return out(rows)
