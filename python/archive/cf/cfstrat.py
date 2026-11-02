"""Chart Fanatics / TradeZella strategies coded for futures (Nov 2 2026). Every rule comes from the trader's page or transcript;
every gap in their rules is filled with ONE stated assumption (marked ASSUME) so it can be tested.
Each signal function takes a bars frame d (index NY time, open high low close volume, per) plus context and returns a DataFrame:
  i (signal bar), s (+1 long / -1 short), wk (structure stop price), tp (the trader's own target price or nan), lim (limit entry price or nan),
  endb (last bar the trade may live), w0 / w1 (window for the random twin), tag."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..'))
from mmmlab import data as D, levels as LV
from mmmlab.candles import atr_rma

NQSTOP = {'NQ': 1.0, 'ES': 0.4, 'GC': 0.24, 'CL': 0.01}      # scale NQ points to the market (NQ 50 = ES 20 = GC 12)


def base(d):
    o, h, l, c, v = (d[k].values.astype(float) for k in ('open', 'high', 'low', 'close', 'volume'))
    mn = d.index.hour.values * 60 + d.index.minute.values
    sd = D.sday(d.index).values
    days = {}
    for k, x in pd.Series(np.arange(len(c))).groupby(sd): days[k] = x.values
    return o, h, l, c, v, mn, sd, days


def out(rows):
    cols = ['i', 's', 'wk', 'tp', 'lim', 'endb', 'w0', 'w1', 'tag']
    return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)


def endbar(ix, mn, tmax):
    k = ix[mn[ix] < tmax] if tmax > 0 else ix
    return int(k[-1]) if len(k) else int(ix[-1])


def extra_levels(sym, m):
    """day levels + Asia evening range (18:00-23:59), previous week / month high-low."""
    DL = LV.day_levels(sym, m)
    f = D.fine(sym); sd = D.sday(f.index); mn = f.index.hour * 60 + f.index.minute
    ev = f[mn >= 1080]; g = ev.groupby(D.sday(ev.index))
    DL['as2H'] = g.high.max().reindex(DL.index); DL['as2L'] = g.low.min().reindex(DL.index)
    dd = D.daily(sym); wk = pd.DatetimeIndex(dd.index).to_period('W-FRI'); mo = pd.DatetimeIndex(dd.index).to_period('M')
    WH = dd.high.groupby(wk).max(); WL = dd.low.groupby(wk).min(); MH = dd.high.groupby(mo).max(); ML = dd.low.groupby(mo).min()
    w = pd.DatetimeIndex(DL.index).to_period('W-FRI'); m_ = pd.DatetimeIndex(DL.index).to_period('M')
    DL['pwH'] = WH.reindex(w - 1).values; DL['pwL'] = WL.reindex(w - 1).values
    DL['pmH'] = MH.reindex(m_ - 1).values; DL['pmL'] = ML.reindex(m_ - 1).values
    return DL


def swings(h, l, k=1):
    """confirmed swing highs / lows: bar j is a swing high if h[j] > the k bars each side; known at bar j+k."""
    n = len(h); sh = np.zeros(n, bool); sl = np.zeros(n, bool)
    for j in range(k, n - k):
        if h[j] > h[j - k:j].max() and h[j] > h[j + 1:j + k + 1].max(): sh[j] = True
        if l[j] < l[j - k:j].min() and l[j] < l[j + 1:j + k + 1].min(): sl[j] = True
    return sh, sl


# ---------------------------------------------------------------- 1. JJ Simon - Fair Pricing Theory (NQ 1m)
def jj_simon(d, m, ext_nq=25.0):
    """Fair price = 9:30 open. HTF bias = 9:29 close vs the close 9 hours before (ASSUME: 9h, the middle of his 6-12h).
    Displacement = body > previous body, close beyond the previous wick, previous candle the opposite color.
    BOS = close through the last 3-candle swing high / low (wick higher than the candle before and after).
    CONT: 9:30-9:34, first displacement or BOS away from fair price in the bias direction (first trade of the session).
    REV: 9:30-11:00, price at least 25 NQ pts from fair price (ASSUME), then a displacement or BOS back toward it. Target = fair price."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; ext = ext_nq * NQSTOP[m]
    sh, sl = swings(h, l, 1)
    rows = []
    for k, ix in days.items():
        o930 = ix[mn[ix] == 570]
        if not len(o930): continue
        b0 = o930[0]; FP = o[b0]
        pre = ix[(mn[ix] < 570) & (mn[ix] >= 0)]
        ref = ix[(mn[ix] == 30)]
        if not len(pre) or not len(ref): continue
        bias = 1 if c[pre[-1]] > c[ref[0]] else -1
        win = ix[(mn[ix] >= 570) & (mn[ix] < 660)]
        e16 = endbar(ix, mn, 960)
        lastH = lastL = np.nan; cont_done = False
        for i in range(max(ix[0] + 2, b0 - 120), win[-1] + 1 if len(win) else b0):
            j = i - 1                                       # swing at j-1 is confirmed at j
            if sh[j - 1]: lastH = h[j - 1]
            if sl[j - 1]: lastL = l[j - 1]
            if mn[i] < 570 or mn[i] >= 660 or sd[i] != k: continue
            body, pbody = abs(c[i] - o[i]), abs(c[i - 1] - o[i - 1])
            dU = c[i] > o[i] and c[i - 1] < o[i - 1] and body > pbody and c[i] > h[i - 1]
            dD = c[i] < o[i] and c[i - 1] > o[i - 1] and body > pbody and c[i] < l[i - 1]
            bU = lastH == lastH and c[i] > lastH and c[i - 1] <= lastH
            bD = lastL == lastL and c[i] < lastL and c[i - 1] >= lastL
            for s, disp, bos in ((1, dU, bU), (-1, dD, bD)):
                if not (disp or bos): continue
                trig = 'BOS' if bos else 'displacement'
                wk = l[i] - tick if s == 1 else h[i] + tick
                if not cont_done and mn[i] < 575 and s == bias and s * (c[i] - FP) > 0:
                    rows.append((i, s, wk, np.nan, np.nan, e16, b0, e16, 'CONT ' + trig)); cont_done = True
                if s * (FP - c[i]) >= ext:
                    rows.append((i, s, wk, FP, np.nan, e16, b0, e16, 'REV ' + trig))
            if mn[i] >= 575: cont_done = True
    return out(rows)


# ---------------------------------------------------------------- 2. Candace Lau - NQ liquidity sweep + IFVG (1m)
def candace(d, m, DL):
    """Liquidity: previous day H / L, Asia H / L (18:00-23:59), London H / L (02:00-08:00, NY only).
    Windows: London 02:00-05:00, New York 09:30-11:30 (ASSUME for 'the open').
    Sweep = trade beyond the level. Then a bearish (for longs) 1m FVG formed before / during the sweep is inverted:
    a candle BODY closes above its top within 20 candles of the sweep (ASSUME 20). Entry: retrace into the IFVG (limit at its top),
    or market at the inversion close. Stop beyond the sweep extreme. Her target = opposing liquidity (nearest level the other way)."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']
    rows = []
    for k, ix in days.items():
        if k not in DL.index: continue
        r = DL.loc[k]
        for wname, t0, t1, tend, extra in (('London', 120, 300, 480, False), ('NY', 570, 690, 960, True)):
            win = ix[(mn[ix] >= t0) & (mn[ix] < t1)]
            if len(win) < 10: continue
            e = endbar(ix, mn, tend)
            lv = [('prev day', r.pH, r.pL), ('Asia', r.as2H, r.as2L)] + ([('London', r.lonH, r.lonL)] if extra else [])
            highs = [x[1] for x in lv if x[1] == x[1]]; lows = [x[2] for x in lv if x[2] == x[2]]
            for name, LH, LL in lv:
                for s, Lv in ((1, LL), (-1, LH)):
                    if Lv != Lv: continue
                    sw = [i for i in win if (s == 1 and l[i] < Lv) or (s == -1 and h[i] > Lv)]
                    if not sw: continue
                    i0 = sw[0]
                    if (s == 1 and c[i0 - 1] < Lv) or (s == -1 and c[i0 - 1] > Lv): continue    # must come from the other side
                    ext = l[i0] if s == 1 else h[i0]
                    done = False
                    for j in range(i0, min(i0 + 20, win[-1] + 1)):
                        ext = min(ext, l[j]) if s == 1 else max(ext, h[j])
                        # latest opposite FVG formed in the 30 candles before j (bearish gap for a long: h[q] < l[q-2])
                        top = np.nan
                        for q in range(j - 1, max(j - 30, ix[0] + 2), -1):
                            if s == 1 and h[q] < l[q - 2]: top, bot = l[q - 2], h[q]; break
                            if s == -1 and l[q] > h[q - 2]: top, bot = h[q - 2], l[q]; break
                        if top != top: continue
                        if (s == 1 and c[j] > top and o[j] < c[j]) or (s == -1 and c[j] < top and o[j] > c[j]):
                            tgts = [x for x in (highs if s == 1 else lows) if s * (x - c[j]) > 0]
                            tp = (min(tgts) if s == 1 else max(tgts)) if tgts else np.nan
                            rows.append((j, s, ext - tick if s == 1 else ext + tick, tp, top, e, win[0], e, f'{wname} {name}'))
                            done = True; break
                    if done: continue
    return out(rows)


# ---------------------------------------------------------------- 3. Dhesi - Liquidity Inversion Model (15m sweep + inversion, 1m entry)
def dhesi(d, m, DL, d15):
    """Liquidity: previous month / week / day high-low, Asia (18:00-23:59) and London (02-08) high-low.
    15m: a candle sweeps the level, then within 3 candles (sweep candle included) the latest opposite 15m FVG inverts (close through it).
    1m: after that, price retraces and makes a 1m FVG against the trade, then a 1m candle closes through it = entry (LTF inversion).
    Window: from 10:00 (he waits for the 10:00 4H candle) to 15:00. Stop beyond the sweep extreme (the structural high / low).
    Target: first technical target = nearest opposing level (ASSUME), half off there, stop to break-even, runner."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']
    o5, h5, l5, c5 = (d15[k].values for k in ('open', 'high', 'low', 'close')); t15 = d15.index; sd15 = D.sday(t15).values; mn15 = t15.hour * 60 + t15.minute
    rows = []
    pos1 = pd.Series(np.arange(len(d)), index=d.index)
    for k, ix in days.items():
        if k not in DL.index: continue
        r = DL.loc[k]
        q = np.where((sd15 == k) & (mn15 >= 600) & (mn15 < 900))[0]
        if len(q) < 3: continue
        e = endbar(ix, mn, 960)
        lv = [('month', r.pmH, r.pmL), ('week', r.pwH, r.pwL), ('day', r.pH, r.pL), ('Asia', r.as2H, r.as2L), ('London', r.lonH, r.lonL)]
        highs = [x[1] for x in lv if x[1] == x[1]]; lows = [x[2] for x in lv if x[2] == x[2]]
        used = set()
        for name, LH, LL in lv:
            for s, Lv in ((-1, LH), (1, LL)):
                if Lv != Lv or (name, s) in used: continue
                sw = [j for j in q if (s == -1 and h5[j] > Lv) or (s == 1 and l5[j] < Lv)]
                if not sw: continue
                j0 = sw[0]; ext = h5[j0] if s == -1 else l5[j0]; armed = None
                for j in range(j0, min(j0 + 3, len(c5))):
                    ext = max(ext, h5[j]) if s == -1 else min(ext, l5[j])
                    for qq in range(j0 - 1, max(j0 - 20, 2), -1):            # latest 15m FVG on the swept side, formed before the sweep
                        if s == -1 and l5[qq] > h5[qq - 2]: edge = h5[qq - 2]; break
                        if s == 1 and h5[qq] < l5[qq - 2]: edge = l5[qq - 2]; break
                    else: edge = np.nan
                    if edge == edge and ((s == -1 and c5[j] < edge) or (s == 1 and c5[j] > edge)):
                        armed = t15[j] + pd.Timedelta(minutes=15); break
                if armed is None: continue
                a = int(np.searchsorted(d.index.values, armed.to_datetime64()))
                for i in range(a + 2, min(a + 90, e)):
                    if mn[i] >= 900 or sd[i] != k: break
                    if (s == -1 and h[i] > ext) or (s == 1 and l[i] < ext): break                       # idea invalid
                    # last 1m FVG against the trade (bullish gap for a short) in the last 15 candles, then a close through it
                    for qq in range(i - 1, max(i - 15, a), -1):
                        if s == -1 and l[qq] > h[qq - 2]: edge = h[qq - 2]; break
                        if s == 1 and h[qq] < l[qq - 2]: edge = l[qq - 2]; break
                    else: continue
                    if (s == -1 and c[i] < edge and c[i - 1] >= edge) or (s == 1 and c[i] > edge and c[i - 1] <= edge):
                        tg = [x for x in (lows if s == -1 else highs) if s * (x - c[i]) > 0]
                        tp = (max(tg) if s == -1 else min(tg)) if tg else np.nan
                        rows.append((i, s, ext + tick if s == -1 else ext - tick, tp, np.nan, e, ix[mn[ix] >= 600][0], e, f'{name} sweep'))
                        used.add((name, s)); break
    return out(rows)


# ---------------------------------------------------------------- 4. Okala - 80/20 Nasdaq
def okala(d, m, tol=3.0):
    """Levels = prices ending in 20 or 80. Window 9:30-11:30 (NY open, no lunch).
    FORK (long): sharp drop (the 5 candles before fell >= 1.5 ATR, ASSUME), rejection candle with a long lower wick
      (wick >= 2x body and >= half the range, ASSUME) whose low is within 3 pts of a 20 / 80 level, next candle tests the low
      (within 3 pts) but does not break it, then a candle closes above that candle's high = long.
    H (short): in a move lower (10-candle high minus price >= 1.5 ATR), a bounce reaches an 80 level (high within 3 pts), then a candle
      closes below the bounce candle's low = short; limit option = retest of the 80 level.
    Okala's risk: fixed 10 pt stop, first scale at +15, then break-even."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']
    atr = atr_rma(h, l, c, 14)
    lvl = lambda p, want: [L for L in (np.floor(p / 100) * 100 + x for x in (-80, -20, 20, 80, 120, 180)) if round(L % 100) in want and abs(L - p) <= tol]
    rows = []
    for k, ix in days.items():
        win = ix[(mn[ix] >= 570) & (mn[ix] < 690)]
        if len(win) < 5: continue
        e = endbar(ix, mn, 960)
        for i in win:
            if i < 12: continue
            kk = i - 2; a = atr[kk]
            if a == a and a > 0:
                body = abs(c[kk] - o[kk]); rng = h[kk] - l[kk]; lw = min(o[kk], c[kk]) - l[kk]
                drop = h[kk - 5:kk].max() - l[kk]
                if rng > 0 and drop >= 1.5 * a and lw >= 2 * body and lw >= .5 * rng and lvl(l[kk], (20, 80)):
                    if l[kk] <= l[kk + 1] <= l[kk] + tol and c[i] > h[kk + 1]:
                        rows.append((i, 1, l[kk] - tick, np.nan, np.nan, e, win[0], e, 'Fork long'))
            a = atr[i - 1]
            if a == a and a > 0:
                j = i - 1
                L80 = lvl(h[j], (80,))
                if L80 and h[i - 11:i - 1].max() - c[i] >= 1.5 * a and h[j] >= h[j - 1] and c[i] < l[j] and c[i] < o[i]:
                    rows.append((i, -1, h[j] + tick, np.nan, L80[0], e, win[0], e, 'H short'))
    return out(rows)


# ---------------------------------------------------------------- 5. Marci Silfrain - Measured Move ("Little RZY")
def marci(d, m, k=3):
    """Trend: EMA20 above EMA50 (long) / below (short) (ASSUME). Swings: k=3 fractals.
    Long: two rising swing lows draw the trendline, a swing high forms after the second, price pulls back to the line
    (low within 0.25 ATR of it, close above it, green candle) = long. Target = swing high + (swing high - line under it).
    Stop: below the line (0.25 ATR) or the candle low, whichever is lower. Short = mirror. One trade per structure.
    Tag = structure number in the trend (1st / 2nd = her best)."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; n = len(c)
    atr = atr_rma(h, l, c, 14)
    e20 = pd.Series(c).ewm(span=20, adjust=False).mean().values; e50 = pd.Series(c).ewm(span=50, adjust=False).mean().values
    sh, sl = swings(h, l, k)
    rows = []
    LO = []; HI = []; used = set(); cnt = {1: 0, -1: 0}; tr_prev = 0
    for i in range(60, n):
        j = i - k
        if sh[j]: HI.append(j)
        if sl[j]: LO.append(j)
        tr = 1 if e20[i] > e50[i] else -1
        if tr != tr_prev: cnt = {1: 0, -1: 0}; tr_prev = tr
        a = atr[i]
        if not (a == a and a > 0): continue
        for s in (1, -1):
            if s != tr: continue
            P = LO if s == 1 else HI; X = HI if s == 1 else LO
            if len(P) < 2: continue
            p1, p2 = P[-2], P[-1]
            y1 = l[p1] if s == 1 else h[p1]; y2 = l[p2] if s == 1 else h[p2]
            if not ((s == 1 and y2 > y1) or (s == -1 and y2 < y1)): continue
            ext = [x for x in X if x > p2]
            if not ext: continue
            e_ = ext[-1]; ye = h[e_] if s == 1 else l[e_]
            slope = (y2 - y1) / (p2 - p1)
            line = lambda x: y2 + slope * (x - p2)
            key = (p1, p2, s)
            if key in used or i <= e_: continue
            seg = slice(e_ + 1, i)
            if s == 1 and (c[seg] < line(np.arange(e_ + 1, i))).any(): used.add(key); continue
            if s == -1 and (c[seg] > line(np.arange(e_ + 1, i))).any(): used.add(key); continue
            Li = line(i)
            if s == 1 and l[i] <= Li + .25 * a and c[i] > Li and c[i] > o[i]:
                dist = ye - line(e_); tp = ye + dist
                stop = min(Li - .25 * a, l[i] - tick)
            elif s == -1 and h[i] >= Li - .25 * a and c[i] < Li and c[i] < o[i]:
                dist = line(e_) - ye; tp = ye - dist
                stop = max(Li + .25 * a, h[i] + tick)
            else: continue
            used.add(key); cnt[s] += 1
            if dist <= 0: continue
            rows.append((i, s, stop, tp, np.nan, min(n - 1, i + 2000), max(1, i - 200), min(n - 1, i + 200), f'structure {min(cnt[s], 3)}{"+" if cnt[s] >= 3 else ""}'))
    return out(rows)


# ---------------------------------------------------------------- 6. Fabio Valentini - Auction Market (trend + mean reversion)
def leg_lvn(h, l, v, a, b, bin_):
    """lowest-volume price between 25% and 75% of the leg a..b (volume spread over each candle's range)."""
    lo = l[a:b + 1].min(); hi = h[a:b + 1].max()
    if hi - lo < 4 * bin_: return np.nan
    p0 = np.floor(lo / bin_) * bin_; nb = int((hi - p0) / bin_) + 1; hs = np.zeros(nb + 1)
    for j in range(a, b + 1):
        i0 = int((l[j] - p0) / bin_); i1 = int((h[j] - p0) / bin_); w = v[j] / (i1 - i0 + 1); hs[i0] += w; hs[i1 + 1] -= w
    hs = np.cumsum(hs)[:nb]
    q0 = int(.25 * nb); q1 = max(q0 + 1, int(.75 * nb))
    k = q0 + int(np.argmin(hs[q0:q1]))
    return p0 + (k + .5) * bin_


def fabio(d, m, DL):
    """Balance reference = previous NY session volume profile (his 'stupid simple' daily profile; POC / VAH / VAL at 70%).
    Aggression proxy (no footprint): a full-body candle (body >= 60% of range) closing in the trade direction with volume >= 2x the
    median of the last 30 candles (ASSUME - he uses 20-40 lot bubbles we cannot see).
    TREND (NY 09:45-13:30, out of balance): price trades above the previous VAH (long state) / below VAL (short). Impulse leg = session
      low (high) since 9:30 to the newest high (low). Pullback into the leg's low-volume node (LVN) without breaking the leg start,
      then an aggression candle closing back beyond the LVN = entry. Stop 2 ticks beyond that candle. His target: previous day high
      (long) / low (short) when it is ahead, else none (trail / R targets).
    MEAN REVERSION (London 02:00-08:00, out by 08:00; also NY 09:45-13:30): price breaks below VAL (above VAH), then closes back inside
      (the reclaim). Do not take the first move: wait for a pullback toward the reclaim leg's LVN / middle, then an aggression candle back
      in = entry. Stop 2 ticks beyond the aggression candle. Target = previous POC."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; bin_ = {'NQ': 2.0, 'ES': .5, 'GC': .5, 'CL': .01}[m]
    vmed = pd.Series(v).rolling(30, min_periods=10).median().shift(1).values
    rng = h - l; body = np.abs(c - o)
    agg = lambda i, s: rng[i] > 0 and body[i] >= .6 * rng[i] and s * (c[i] - o[i]) > 0 and vmed[i] == vmed[i] and v[i] >= 1.5 * vmed[i]
    vtag = lambda i: ' | vol 2x+' if v[i] >= 2 * vmed[i] else ' | vol 1.5-2x'
    rows = []
    for k, ix in days.items():
        if k not in DL.index: continue
        r = DL.loc[k]
        if not (r.pVAH == r.pVAH): continue
        VAH, VAL, POC = r.pVAH, r.pVAL, r.pPOC
        e16 = endbar(ix, mn, 960)
        ny = ix[(mn[ix] >= 570) & (mn[ix] < 810)]
        # ---- trend model
        if len(ny) > 20:
            b0 = ny[0]
            for s in (1, -1):
                start = b0; ext_bar = b0; taken = False
                for i in ny:
                    if mn[i] < 585:
                        if (s == 1 and h[i] >= h[ext_bar]) or (s == -1 and l[i] <= l[ext_bar]): ext_bar = i
                        if (s == 1 and l[i] <= l[start]) or (s == -1 and h[i] >= h[start]): start = i
                        continue
                    if taken: break
                    outside = (s == 1 and c[i - 1] > VAH) or (s == -1 and c[i - 1] < VAL)
                    if (s == 1 and l[i] < l[start]) or (s == -1 and h[i] > h[start]): start = i; ext_bar = i; continue
                    if (s == 1 and h[i] >= h[ext_bar]) or (s == -1 and l[i] <= l[ext_bar]): ext_bar = i; continue
                    if not outside or ext_bar - start < 5: continue
                    lvn = leg_lvn(h, l, v, start, ext_bar, bin_)
                    if lvn != lvn: continue
                    if (s == 1 and l[i] <= lvn + 2 * tick and c[i] > lvn) or (s == -1 and h[i] >= lvn - 2 * tick and c[i] < lvn):
                        if agg(i, s):
                            tp = r.pH if (s == 1 and r.pH == r.pH and r.pH > c[i]) else r.pL if (s == -1 and r.pL == r.pL and r.pL < c[i]) else np.nan
                            rows.append((i, s, l[i] - 2 * tick if s == 1 else h[i] + 2 * tick, tp, np.nan, e16, ny[0], e16, 'TREND NY' + vtag(i)))
                            taken = True
        # ---- mean reversion model
        for wname, t0, t1, tend in (('London', 120, 480, 480), ('NY', 585, 810, 960)):
            win = ix[(mn[ix] >= t0) & (mn[ix] < t1)]
            if len(win) < 20: continue
            e = endbar(ix, mn, tend)
            for s in (1, -1):
                edge = VAL if s == 1 else VAH
                state = 0; exb = None; rec = None; top = None; took = False
                for i in win:
                    if took: break
                    if state == 0:
                        if (s == 1 and l[i] < edge) or (s == -1 and h[i] > edge): state = 1; exb = i
                    elif state == 1:
                        if (s == 1 and l[i] < l[exb]) or (s == -1 and h[i] > h[exb]): exb = i
                        if (s == 1 and c[i] > edge) or (s == -1 and c[i] < edge): state = 2; rec = i; top = i
                    elif state == 2:
                        if (s == 1 and l[i] < l[exb]) or (s == -1 and h[i] > h[exb]): state = 1; exb = i; continue   # broke the low again
                        if (s == 1 and h[i] >= h[top]) or (s == -1 and l[i] <= l[top]): top = i; continue
                        if top - exb < 2: continue
                        lvn = leg_lvn(h, l, v, exb, top, bin_)
                        mid = (h[top] + l[exb]) / 2
                        zone = lvn if lvn == lvn else mid
                        if ((s == 1 and l[i] <= zone and c[i] > zone) or (s == -1 and h[i] >= zone and c[i] < zone)) and agg(i, s) and s * (POC - c[i]) > 0:
                            rows.append((i, s, l[i] - 2 * tick if s == 1 else h[i] + 2 * tick, POC, np.nan, e, win[0], e, f'MEAN REV {wname}' + vtag(i)))
                            took = True
    return out(rows)
