"""Group C (+ later groups) Chart Fanatics strategies: Andrea Cimitan, Carmine Rosato, Forrest Knight, Rajan Dhall, Anthony Crudele.
Same output format as cf/cfstrat.py. register(EXTRA) adds their jobs to cfrun2.py."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/mmmlab'); sys.path.insert(0, '/home/claude/cf'); sys.path.insert(0, '/home/claude/cf2')
from mmmlab import data as D, levels as LV
from mmmlab.candles import atr_rma
from cfstrat import base, out, endbar, swings, NQSTOP, leg_lvn
from cfstrat2 import ema, fractals, prev_daily_dir

BIN = {'NQ': 5.0, 'ES': 1.0, 'GC': 1.0}


def rth_prev(sym):
    """previous NY session (09:30-16:00) high / low per trading day"""
    f = D.fine(sym); mn = f.index.hour * 60 + f.index.minute; r = f[(mn >= 570) & (mn < 960)]
    g = r.groupby(D.sday(r.index)); H = g.high.max(); L = g.low.min()
    return H.shift(1), L.shift(1)


def on_range(sym):
    f = D.fine(sym); mn = f.index.hour * 60 + f.index.minute; r = f[(mn >= 1080) | (mn < 570)]
    g = r.groupby(D.sday(r.index)); return g.high.max(), g.low.min()


# ---------------------------------------------------------------- Andrea Cimitan - Auction Market Theory (5m)
def cimitan(d, m, DL):
    """Levels = previous NY session profile VAH / VAL / POC (70%).
    FAILED AUCTION long: a 5m bar trades below VAL (09:30-12:00), then within 3 bars a 5m close back above VAL = long at that close.
      Tag 'absorbed' if a bar below VAL had volume >= 1.5x its 20-bar average and a lower wick >= 50% of its range (his absorption,
      proxy). Stop below the excursion low. Target = POC. Short mirrors at VAH.
    BREAKOUT WITH ACCEPTANCE: opening range 09:30-09:45; a 5m close outside it with body >= 60% of the bar (acceptance in the body)
      = trade the break; stop = other side of the opening range; target 2R (his '1:2 is more than enough')."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']
    va = pd.Series(v).rolling(20, min_periods=5).mean().shift(1).values
    rows = []
    for k, ix in days.items():
        if k not in DL.index: continue
        r = DL.loc[k]; win = ix[(mn[ix] >= 570) & (mn[ix] < 720)]
        if len(win) < 6 or not (r.pVAL == r.pVAL): continue
        e = endbar(ix, mn, 960)
        for s, edge in ((1, r.pVAL), (-1, r.pVAH)):
            state = None
            for i in win:
                if state is None:
                    if (s == 1 and l[i] < edge) or (s == -1 and h[i] > edge): state = dict(k=i, ext=l[i] if s == 1 else h[i], ab=False)
                    else: continue
                st = state
                st['ext'] = min(st['ext'], l[i]) if s == 1 else max(st['ext'], h[i])
                rng = h[i] - l[i]
                if rng > 0 and va[i] == va[i] and v[i] >= 1.5 * va[i]:
                    wick = (min(o[i], c[i]) - l[i]) if s == 1 else (h[i] - max(o[i], c[i]))
                    if wick >= .5 * rng: st['ab'] = True
                if i > st['k'] and ((s == 1 and c[i] > edge) or (s == -1 and c[i] < edge)):
                    if i - st['k'] <= 3:
                        rows.append((i, s, st['ext'] - tick if s == 1 else st['ext'] + tick, r.pPOC, np.nan, e, win[0], e, 'Failed auction' + (' absorbed' if st['ab'] else ' plain')))
                    break
                if i - st['k'] > 3: break
        orb = ix[(mn[ix] >= 570) & (mn[ix] < 585)]
        if len(orb) < 2: continue
        H, L = h[orb].max(), l[orb].min()
        for i in win:
            if mn[i] < 585: continue
            rng = h[i] - l[i]
            if rng <= 0 or abs(c[i] - o[i]) < .6 * rng: continue
            if c[i] > H and c[i] > o[i]: rows.append((i, 1, L - tick, np.nan, np.nan, e, win[0], e, 'Breakout acceptance')); break
            if c[i] < L and c[i] < o[i]: rows.append((i, -1, H + tick, np.nan, np.nan, e, win[0], e, 'Breakout acceptance')); break
    return out(rows)


# ---------------------------------------------------------------- Carmine Rosato - Low Volume Node + PDL stop-run (1m)
def rosato(d, m, sym):
    """LVN (09:30-12:00): on 5m, a base (>= 3 overlapping candles, total range <= 1 ATR) then an impulse of >= 2x the base range within
      6 candles. LVN = lowest-volume price in the middle of the impulse leg (1m profile). First 1m candle that touches the LVN and
      closes back on the impulse side with volume >= 1.2x its 20-bar average = entry. Stop past the LVN zone (+-1 bin, 2 ticks).
      Target = high / low of day at entry (skip if < 1R).
    STOP RUN: a 1m candle trades below the previous NY low with volume >= 2x average (his 'heavy negative delta' proxy), and a 1m close
      back above it within 3 candles = long; stop below the flush low; target 2R. Mirror at the previous NY high."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; b = BIN[m]
    va = pd.Series(v).rolling(20, min_periods=5).mean().shift(1).values
    d5 = D.bars(sym, 5); o5, h5, l5, c5 = (d5[k].values for k in ('open', 'high', 'low', 'close'))
    a5 = atr_rma(h5, l5, c5, 14); t5 = d5.index.values; t1 = d.index.values; sd5 = D.sday(d5.index).values; mn5 = d5.index.hour * 60 + d5.index.minute
    PH, PL = rth_prev(sym)
    rows = []
    for k, ix in days.items():
        e = endbar(ix, mn, 960); win = ix[(mn[ix] >= 570) & (mn[ix] < 720)]
        if len(win) < 10: continue
        # ---- stop run of the previous NY low / high
        pl, ph = PL.get(k, np.nan), PH.get(k, np.nan)
        for s, L in ((1, pl), (-1, ph)):
            if L != L: continue
            for i in win:
                if ((s == 1 and l[i] < L) or (s == -1 and h[i] > L)) and va[i] == va[i] and v[i] >= 2 * va[i]:
                    ext = l[i] if s == 1 else h[i]
                    for j in range(i, min(i + 4, win[-1] + 1)):
                        ext = min(ext, l[j]) if s == 1 else max(ext, h[j])
                        if (s == 1 and c[j] > L) or (s == -1 and c[j] < L):
                            rows.append((j, s, ext - tick if s == 1 else ext + tick, np.nan, np.nan, e, win[0], e, 'Stop-run reclaim')); break
                    break
        # ---- LVN pullback
        q5 = np.where((sd5 == k) & (mn5 >= 570) & (mn5 < 720))[0]
        done = False
        for qi in range(len(q5) - 3):
            if done: break
            q = q5[qi]
            bh, bl = h5[q:q + 3].max(), l5[q:q + 3].min()
            if not (a5[q + 2] == a5[q + 2]) or bh - bl > a5[q + 2] or min(h5[q:q + 3]) < max(l5[q:q + 3]): continue
            br = bh - bl
            for z in range(q + 3, min(q + 9, len(c5))):
                if sd5[z] != k: break
                s = 1 if h5[z] - bl >= 3 * br else -1 if bh - l5[z] >= 3 * br else 0      # traveled 2x the base range beyond it
                if not s: continue
                a1 = int(np.searchsorted(t1, t5[q])); b1 = int(np.searchsorted(t1, t5[z] + np.timedelta64(5, 'm'))) - 1
                if b1 - a1 < 5: break
                lvn = leg_lvn(h, l, v, a1, b1, b)
                if lvn != lvn: break
                lo_z, hi_z = lvn - b, lvn + b
                for i in range(b1 + 1, min(b1 + 120, e)):
                    if mn[i] >= 720: break
                    if (s == 1 and l[i] < lo_z - 2 * tick) and c[i] < lo_z: break                   # zone failed
                    if (s == -1 and h[i] > hi_z + 2 * tick) and c[i] > hi_z: break
                    touch = (l[i] <= hi_z and c[i] > hi_z) if s == 1 else (h[i] >= lo_z and c[i] < lo_z)
                    if touch and va[i] == va[i] and v[i] >= 1.2 * va[i]:
                        stop = lo_z - 2 * tick if s == 1 else hi_z + 2 * tick
                        day_ = ix[ix <= i]; tp = h[day_[mn[day_] >= 570]].max() if s == 1 else l[day_[mn[day_] >= 570]].min()
                        if s * (tp - c[i]) >= s * (c[i] - stop):
                            rows.append((i, s, stop, tp, np.nan, e, win[0], e, 'LVN pullback'))
                        done = True; break
                break
    return out(rows)


# ---------------------------------------------------------------- Forrest Knight - Volume Profile edges (1H)
def profile_edges(lo, hi, vol, b):
    if len(lo) == 0: return []
    p0 = np.floor(lo.min() / b) * b; nb = int((hi.max() - p0) / b) + 1; hs = np.zeros(nb + 1)
    for x, y, w in zip(lo, hi, vol):
        i0 = int((x - p0) / b); i1 = int((y - p0) / b); hs[i0] += w / (i1 - i0 + 1); hs[i1 + 1] -= w / (i1 - i0 + 1)
    hs = np.convolve(np.cumsum(hs)[:nb], np.ones(3) / 3, 'same'); mx = hs.max(); E = []
    for k in range(nb):
        if hs[k] >= .5 * mx:
            if k + 3 < nb and (hs[k + 1:k + 4] <= .2 * mx).any(): E.append(p0 + (k + 1) * b)
            if k - 3 >= 0 and (hs[k - 3:k] <= .2 * mx).any(): E.append(p0 + k * b)
    return E


def knight(d, m, sym):
    """Profile = previous NY session (ASSUME; he uses session + visible range). Edge = where volume drops from >= 50% of the POC row to
    <= 20% within 3 rows (a 'shelf'). A setup needs all three: a level (overnight high / low, previous day high / low) that sits within
    0.25 ATR of a profile edge; a 1H candle that touches it with volume >= 1.5x its 20-bar average, a wick on the level side >= 40% of
    its range and a close back in the trade direction (colour) = entry at the close. Stop beyond the wick. Target = the opposite level."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; b = BIN[m]
    atr = atr_rma(h, l, c, 14); va = pd.Series(v).rolling(20, min_periods=5).mean().shift(1).values
    f = D.fine(sym); fm = f.index.hour * 60 + f.index.minute; fsd = D.sday(f.index)
    rth = f[(fm >= 570) & (fm < 960)]; G = {k: x for k, x in rth.groupby(D.sday(rth.index))}
    ONH, ONL = on_range(sym)
    dd = D.daily(sym); PDH = dd.high.shift(1); PDL = dd.low.shift(1)
    keys = sorted(G); prevk = {keys[q]: keys[q - 1] for q in range(1, len(keys))}
    rows = []; cache = {}
    for k, ix in days.items():
        if k not in prevk: continue
        pk = prevk[k]
        if pk not in cache:
            x = G[pk]; cache[pk] = profile_edges(x.low.values, x.high.values, x.volume.values.astype(float), b)
        E = cache[pk]
        lv = [x for x in (ONH.get(k, np.nan), ONL.get(k, np.nan), PDH.get(k, np.nan), PDL.get(k, np.nan)) if x == x]
        win = ix[(mn[ix] >= 540) & (mn[ix] < 960)]
        e = endbar(ix, mn, 960) if ix[-1] > 0 else ix[-1]
        e = ix[-1]
        used = set()
        for i in win:
            a = atr[i]
            if not (a == a and a > 0) or not (va[i] == va[i]) or v[i] < 1.5 * va[i]: continue
            rng = h[i] - l[i]
            if rng <= 0: continue
            for L in lv:
                if L in used or not any(abs(L - x) <= .25 * a for x in E): continue
                if l[i] <= L <= h[i] or abs(l[i] - L) <= .1 * a or abs(h[i] - L) <= .1 * a:
                    up_w = h[i] - max(o[i], c[i]); dn_w = min(o[i], c[i]) - l[i]
                    if c[i] < L and c[i] < o[i] and up_w >= .4 * rng and h[i] >= L: s = -1
                    elif c[i] > L and c[i] > o[i] and dn_w >= .4 * rng and l[i] <= L: s = 1
                    else: continue
                    tg = [x for x in lv if s * (x - c[i]) > 0]
                    tp = (min(tg) if s == 1 else max(tg)) if tg else np.nan
                    rows.append((i, s, l[i] - 2 * tick if s == 1 else h[i] + 2 * tick, tp, np.nan, min(len(c) - 1, i + 48), max(1, i - 24), min(len(c) - 1, i + 24), 'Edge + level + signal candle'))
                    used.add(L)
    return out(rows)


# ---------------------------------------------------------------- Rajan Dhall - Market Auction Theory (5m)
def dhall(d, m, sym):
    """Bias: previous daily candle closes in its bottom 25% and red = short (mirror long). Trend: close below EMA21 and EMA50 on the daily
    and on 5m. 45-degree trend: daily EMA21 moved >= 1 daily ATR over 10 days in the bias direction (ASSUME).
    Auction zone = first 3 straight 5m candles after 09:30 with total range <= 2 ATR(5m) (ASSUME; 1.2 ATR almost never happens at the open). A 5m close beyond the zone in the bias
    direction, then a retest: a candle reaches the zone edge, closes back beyond it in colour with a wick >= 40% = entry at the close.
    Stop beyond that candle. Target 2R (his minimum). New entries until 11:00 (his first hour + 30 min, ASSUME), max 2 a day."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; atr = atr_rma(h, l, c, 14)
    e21, e50 = ema(c, 21), ema(c, 50)
    dd = D.daily(sym); de21 = dd.close.ewm(span=21, adjust=False).mean(); de50 = dd.close.ewm(span=50, adjust=False).mean()
    dtr = pd.concat([dd.high - dd.low, (dd.high - dd.close.shift()).abs(), (dd.low - dd.close.shift()).abs()], axis=1).max(axis=1).rolling(14).mean()
    pos = (dd.close - dd.low) / (dd.high - dd.low)
    bias = pd.Series(0, index=dd.index); strict = pd.Series(False, index=dd.index)
    bias[(dd.close < dd.open) & (dd.close < de21) & (dd.close < de50)] = -1
    bias[(dd.close > dd.open) & (dd.close > de21) & (dd.close > de50)] = 1
    strict[((bias == -1) & (pos <= .25) & (de21 - de21.shift(10) <= -dtr)) | ((bias == 1) & (pos >= .75) & (de21 - de21.shift(10) >= dtr))] = True
    bias = bias.shift(1); strict = strict.shift(1).fillna(False)
    rows = []
    for k, ix in days.items():
        s = bias.get(k, 0)
        if not s or s != s: continue
        win = ix[(mn[ix] >= 570) & (mn[ix] < 660)]
        if len(win) < 6: continue
        e = endbar(ix, mn, 960); zone = None
        for q in range(len(win) - 2):
            a = win[q:q + 3]
            if atr[a[-1]] == atr[a[-1]] and h[a].max() - l[a].min() <= 2.0 * atr[a[-1]]: zone = (h[a].max(), l[a].min(), a[-1]); break
        if zone is None: continue
        ZH, ZL, z = zone; broke = False; n_ = 0
        for i in win:
            if i <= z: continue
            if not broke:
                if (s == -1 and c[i] < ZL) or (s == 1 and c[i] > ZH): broke = True
                continue
            rng = h[i] - l[i]
            if rng <= 0: continue
            if s == -1 and h[i] >= ZL and c[i] < ZL and c[i] < o[i] and (h[i] - max(o[i], c[i])) >= .4 * rng and c[i] < e21[i] and c[i] < e50[i]:
                rows.append((i, -1, h[i] + tick, np.nan, np.nan, e, win[0], e, 'Auction zone retest' + (' strict' if strict.get(k, False) else ' loose'))); n_ += 1
            if s == 1 and l[i] <= ZH and c[i] > ZH and c[i] > o[i] and (min(o[i], c[i]) - l[i]) >= .4 * rng and c[i] > e21[i] and c[i] > e50[i]:
                rows.append((i, 1, l[i] - tick, np.nan, np.nan, e, win[0], e, 'Auction zone retest' + (' strict' if strict.get(k, False) else ' loose'))); n_ += 1
            if n_ >= 2: break
    return out(rows)


# ---------------------------------------------------------------- Anthony Crudele - Bollinger 'Beacon' (daily)
def crudele(dd, m):
    """Daily Bollinger 20 / 3 SD. Beacon = Fib from the latest upper-band peak to the latest lower-band trough (3-bar pivots, confirmed).
    MEAN REVERSION short: after the expansion stalls, a daily close below the 30% line = short (target the 50% line); invalid on a close back
      above 30% (stop = 30% line + 0.5 ATR, ASSUME); 5-day time stop. Long mirrors (close above the 70% line, target 50%).
    EXPANSION long: bandwidth rising 3 days and a high at the upper band in the last 3 days, then a close above the 20-day high = long;
      stop 2 ATR; target = the previous upper-band peak (if above); 5-day time stop. Short mirrors."""
    o, h, l, c = (dd[k].values for k in ('open', 'high', 'low', 'close')); n = len(c)
    mid = pd.Series(c).rolling(20).mean().values; sdv = pd.Series(c).rolling(20).std(ddof=0).values
    ub, lb = mid + 3 * sdv, mid - 3 * sdv; bw = (ub - lb) / mid
    atr = atr_rma(h, l, c, 14)
    rows = []; Hpk = Lpk = None; prevPk = None
    for i in range(25, n - 1):
        j = i - 1
        if ub[j] > ub[j - 1] and ub[j] >= ub[i]: prevPk, Hpk = Hpk, ub[j]
        if lb[j] < lb[j - 1] and lb[j] <= lb[i]: Lpk = lb[j]
        a = atr[i]
        if Hpk is None or Lpk is None or not (a == a): continue
        H, L = Hpk, Lpk
        if H <= L: continue
        L30 = H - .3 * (H - L); L50 = H - .5 * (H - L); L70 = H - .7 * (H - L)
        e = min(n - 1, i + 5)
        if c[i] < L30 and c[i - 1] >= L30: rows.append((i, -1, L30 + .5 * a, L50, np.nan, e, max(1, i - 20), min(n - 1, i + 20), 'Mean reversion'))
        if c[i] > L70 and c[i - 1] <= L70: rows.append((i, 1, L70 - .5 * a, L50, np.nan, e, max(1, i - 20), min(n - 1, i + 20), 'Mean reversion'))
        rising = bw[i] > bw[i - 1] > bw[i - 2] > bw[i - 3]
        if rising and (h[i - 2:i + 1] >= ub[i - 2:i + 1]).any() and c[i] > h[i - 20:i].max():
            tp = prevPk if prevPk is not None and prevPk > c[i] else np.nan
            rows.append((i, 1, c[i] - 2 * a, tp, np.nan, e, max(1, i - 20), min(n - 1, i + 20), 'Expansion'))
        if rising and (l[i - 2:i + 1] <= lb[i - 2:i + 1]).any() and c[i] < l[i - 20:i].min():
            rows.append((i, -1, c[i] + 2 * a, np.nan, np.nan, e, max(1, i - 20), min(n - 1, i + 20), 'Expansion'))
    return out(rows)


def daily_series(m):
    out_ = []
    for s in D.MK[m]:
        try: dd = D.daily(s).copy()
        except FileNotFoundError: continue
        dd.index = pd.DatetimeIndex(dd.index)
        if m == 'NQ': dd['per'] = 'P1' if s == 'NQ' else 'P2'
        else:
            days = np.sort(dd.index.unique()); cut = days[len(days) // 2]; dd['per'] = np.where(dd.index < cut, 'P1', 'P2')
        dd['src'] = s; out_.append(dd)
    return out_


def register(EXTRA):
    import cfstrat as CS
    def cim():
        for m in ('NQ', 'ES'):
            for d in D.series(m, 5):
                src = d.src.iloc[0]; DL = CS.extra_levels(src, m)
                yield 'Andrea Cimitan', m, 5, src, d, cimitan(d, m, DL), dict(entries=['market'], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), 1, 2, 3], exits=['stop/target']), None
    def ros():
        for m in ('NQ', 'ES'):
            for d in D.series(m, 1):
                src = d.src.iloc[0]
                yield 'Carmine Rosato', m, 1, src, d, rosato(d, m, src), dict(entries=['market'], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), 2, 3], exits=['stop/target']), None
    def kni():
        for m in ('NQ', 'ES', 'GC'):
            for d in D.series(m, 60):
                src = d.src.iloc[0]
                yield 'Forrest Knight', m, 60, src, d, knight(d, m, src), dict(entries=['market'], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), 2, 3], exits=['stop/target']), None
    def dha():
        for m in ('NQ', 'ES'):
            for d in D.series(m, 5):
                src = d.src.iloc[0]
                yield 'Rajan Dhall', m, 5, src, d, dhall(d, m, src), dict(entries=['market'], stops=[('col', 'wk'), 'fixed'], targets=[2, 3], exits=['stop/target']), None
    def cru():
        for m in ('NQ', 'ES', 'GC'):
            for dd in daily_series(m):
                yield 'Anthony Crudele', m, 1440, dd.src.iloc[0], dd, crudele(dd, m), dict(entries=['market'], stops=[('col', 'wk'), 'fixed', ('atr', 2.0)], targets=[('col', 'tp'), 1, 2, None], exits=['stop/target']), None
    EXTRA.update(Cimitan=cim, Rosato=ros, Knight=kni, Dhall=dha, Crudele=cru)
