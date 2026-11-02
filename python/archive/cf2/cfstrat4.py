"""Group B Chart Fanatics strategies: Trader Mayne, Marco Trades, Vincent Desiano, Abraham Perez (proxy), Trader Yush (proxy)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/mmmlab'); sys.path.insert(0, '/home/claude/cf'); sys.path.insert(0, '/home/claude/cf2')
from mmmlab import data as D
from mmmlab.candles import atr_rma
from cfstrat import base, out, endbar, swings, NQSTOP
from cfstrat3 import rth_prev, on_range


def out2(rows):
    cols = ['i', 's', 'wk', 'tp', 'lim', 'endb', 'w0', 'w1', 'tag', 'tp2']
    return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)


# ---------------------------------------------------------------- Trader Mayne - Structure + OTE (H4 range, M15 entry)
def mayne(d15, m, sym):
    """H4: 3-candle swings; a close beyond the last opposite swing = market structure break (MSB). Range = the swing low before the break
    to the highest high after it (long). OTE = 62-79% retracement (ASSUME; he states only 'discount below 50%').
    M15 inside the OTE: a candle takes out the latest M15 swing low (stop run), then a close above the latest M15 swing high (LTF MSB).
    Entry = limit at the high of the last up-close candle before the swept low (the breaker), valid 10 candles. Stop below the swept low.
    Target = the range high (HTF external liquidity). Skip if under 2:1. One trade per range. Shorts mirror."""
    o, h, l, c, v, mn, sd, days = base(d15); tick = D.SPEC[m]['tick']; n = len(c)
    d4 = D.bars(sym, 240); o4, h4, l4, c4 = (d4[k].values for k in ('open', 'high', 'low', 'close')); t4 = d4.index.values
    s4h, s4l = swings(h4, l4, 1); s1h, s1l = swings(h, l, 1)
    t15 = d15.index.values
    # H4 ranges
    R = []; lastH = lastL = None; lastHi = lastLi = None
    for i in range(2, len(c4)):
        if s4h[i - 1]: lastH, lastHi = h4[i - 1], i - 1
        if s4l[i - 1]: lastL, lastLi = l4[i - 1], i - 1
        if lastH is not None and lastL is not None:
            if c4[i] > lastH and c4[i - 1] <= lastH: R.append((1, i, lastL))
            if c4[i] < lastL and c4[i - 1] >= lastL: R.append((-1, i, lastH))
    rows = []
    for s, i4, anchor in R:
        # extreme after the MSB until the next opposite swing confirms (max 30 H4 bars)
        j_end = min(len(c4) - 1, i4 + 30); ext = h4[i4] if s == 1 else l4[i4]; k4 = i4
        for j in range(i4 + 1, j_end + 1):
            if (s == 1 and h4[j] > ext) or (s == -1 and l4[j] < ext): ext = h4[j] if s == 1 else l4[j]; k4 = j
            if (s == 1 and s4l[j - 1] and j - 1 > i4) or (s == -1 and s4h[j - 1] and j - 1 > i4): break
        H, L = (ext, anchor) if s == 1 else (anchor, ext)
        if H - L <= 0: continue
        z_lo, z_hi = (H - .79 * (H - L), H - .62 * (H - L)) if s == 1 else (L + .62 * (H - L), L + .79 * (H - L))
        start = int(np.searchsorted(t15, t4[k4] + np.timedelta64(240, 'm'))); stop_t = start + 30 * 96
        lastSL = lastSH = None; swept = None; done = False
        for i in range(max(start, 3), min(n - 1, stop_t)):
            if (s == 1 and c[i] < L) or (s == -1 and c[i] > H): break                     # range broken
            if s1h[i - 2]: lastSH = (h[i - 2], i - 2)
            if s1l[i - 2]: lastSL = (l[i - 2], i - 2)
            inz = (l[i] <= z_hi and h[i] >= z_lo)
            if swept is None and inz:
                if s == 1 and lastSL and l[i] < lastSL[0]: swept = (l[i], i)
                if s == -1 and lastSH and h[i] > lastSH[0]: swept = (h[i], i)
            elif swept is not None:
                swept = (min(swept[0], l[i]), swept[1]) if s == 1 else (max(swept[0], h[i]), swept[1])
                if (s == 1 and lastSH and c[i] > lastSH[0] and lastSH[1] < swept[1] + 5) or (s == -1 and lastSL and c[i] < lastSL[0] and lastSL[1] < swept[1] + 5):
                    q = swept[1] - 1
                    while q > swept[1] - 15 and not ((s == 1 and c[q] > o[q]) or (s == -1 and c[q] < o[q])): q -= 1
                    lim = h[q] if s == 1 else l[q]
                    stp = swept[0] - tick if s == 1 else swept[0] + tick
                    tp = H if s == 1 else L
                    if s * (tp - lim) >= 2 * s * (lim - stp) and s * (lim - stp) > 0:
                        rows.append((i, s, stp, tp, lim, min(n - 1, i + 960), max(1, i - 96), min(n - 1, i + 96), 'OTE breaker', np.nan))
                    done = True; break
        if done: continue
    return out2(rows)


# ---------------------------------------------------------------- Marco Trades - Liquidity trap (5m NY open)
def marco(d, m, sym):
    """Respected levels = 5m 3-candle swing highs / lows from 07:30-09:30 and the previous NY session, that price later moved >= 1 ATR
    away from (ASSUME). 09:30-11:00: a candle trades above a respected high and that candle or the next closes back below it = short at
    that close (buy below lows, sell above highs, after the trap). Stop 2 ticks past the sweep. Target = nearest opposing respected level
    (his 1:3+ minimum is a grid option). One trade a session."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; atr = atr_rma(h, l, c, 14)
    sh, sl = swings(h, l, 1)
    keys = sorted(days); rows = []
    for di, k in enumerate(keys):
        if di == 0: continue
        ix = days[k]; pv = days[keys[di - 1]]
        pre = np.r_[pv[(mn[pv] >= 570) & (mn[pv] < 960)], ix[(mn[ix] >= 450) & (mn[ix] < 570)]]
        win = ix[(mn[ix] >= 570) & (mn[ix] < 660)]
        if len(pre) < 10 or len(win) < 5: continue
        e = endbar(ix, mn, 960)
        HL = []
        for j in pre:
            if j < 1 or j >= len(c) - 1: continue
            a = atr[j] if atr[j] == atr[j] else 0
            after = pre[pre > j]
            if not len(after) or a <= 0: continue
            if sh[j] and h[j] - l[after].min() >= a: HL.append((1, h[j]))
            if sl[j] and h[after].max() - l[j] >= a: HL.append((-1, l[j]))
        highs = sorted(x for t, x in HL if t == 1); lows = sorted(x for t, x in HL if t == -1)
        took = False
        for i in win:
            if took: break
            for s, lv_list in ((-1, highs), (1, lows)):
                hit = [L for L in lv_list if (s == -1 and h[i] > L and h[i - 1] <= L) or (s == 1 and l[i] < L and l[i - 1] >= L)]
                if not hit: continue
                L = hit[0]
                for j in (i, i + 1):
                    if j >= len(c) or mn[j] >= 660: break
                    if (s == -1 and c[j] < L) or (s == 1 and c[j] > L):
                        ext = max(h[i], h[j]) if s == -1 else min(l[i], l[j])
                        opp = [x for x in (lows if s == -1 else highs) if s * (x - c[j]) > 0]
                        tp = (max(opp) if s == -1 else min(opp)) if opp else np.nan
                        rows.append((j, s, ext + 2 * tick if s == -1 else ext - 2 * tick, tp, np.nan, e, win[0], e, 'Liquidity trap', np.nan))
                        took = True; break
                if took: break
    return out2(rows)


# ---------------------------------------------------------------- Vincent Desiano - Break & Retest (2m, 10:00-12:00)
def desiano(d, m, sym):
    """Levels = previous NY session high / low and overnight (pre-market) high / low. No Trade Zone = between the nearest levels around
    the 9:30 open (ASSUME). 10:00-12:00 (he skips the first 30 minutes): a 2m close beyond a level outside the NTZ = break (no entry);
    then a candle wicks back into the level and closes in the break direction = entry at the close. A close back through the level before
    that cancels it. Stop past the retest low / high. TP1 = the next level / day extreme (half off there in his management)."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']
    PH, PL = rth_prev(sym); ONH, ONL = on_range(sym)
    rows = []
    for k, ix in days.items():
        lv = [x for x in (PH.get(k, np.nan), PL.get(k, np.nan), ONH.get(k, np.nan), ONL.get(k, np.nan)) if x == x]
        o930 = ix[mn[ix] == 570]
        if len(lv) < 2 or not len(o930): continue
        op = o[o930[0]]
        above = [x for x in lv if x > op]; below = [x for x in lv if x < op]
        nt_lo = max(below) if below else -np.inf; nt_hi = min(above) if above else np.inf
        win = ix[(mn[ix] >= 600) & (mn[ix] < 720)]
        e = endbar(ix, mn, 955)
        for L in sorted(set(lv)):
            for s in (1, -1):
                if s == 1 and L < nt_hi: continue        # long breaks only at / above the top of the NTZ
                if s == -1 and L > nt_lo: continue
                broke = False; rl = None
                for i in win:
                    if not broke:
                        if (s == 1 and c[i] > L) or (s == -1 and c[i] < L): broke = True
                        continue
                    if (s == 1 and c[i] < L) or (s == -1 and c[i] > L): break
                    if (s == 1 and l[i] <= L) or (s == -1 and h[i] >= L):
                        rl = l[i] if s == 1 else h[i]
                        if (s == 1 and c[i] > L and c[i] > o[i]) or (s == -1 and c[i] < L and c[i] < o[i]):
                            day_ = ix[(ix <= i) & (mn[ix] >= 570)]
                            nxt = [x for x in lv if s * (x - c[i]) > 0] + [h[day_].max() if s == 1 else l[day_].min()]
                            nxt = [x for x in nxt if s * (x - c[i]) > 0]
                            tp = (min(nxt) if s == 1 else max(nxt)) if nxt else np.nan
                            rows.append((i, s, rl - tick if s == 1 else rl + tick, tp, np.nan, e, win[0], e, 'Break and retest', np.nan)); break
    return out2(rows)


# ---------------------------------------------------------------- Abraham Perez - ICT + order flow, IFVG model (proxy, 1m)
def perez(d, m, sym):
    """PROXY (his Bookmap / tape confirmation can't be seen). Bias = direction of the last 4H swing break. Windows: Asia 20:00-23:00
    (swept level = previous NY high / low) and NY 09:30-11:30 (swept level = overnight high / low). A sweep against the bias, then within
    15 candles a 1m body closes through the latest opposite 1m FVG of the leg (IFVG) with volume >= 1.5x average and a body >= 1 ATR
    ('displacement with intent'), on the right side of the session VWAP = entry at the close. Stop 2 ticks past the sweep. Target 1:2
    (his choppy-day target) or the next session level."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; atr = atr_rma(h, l, c, 14)
    va = pd.Series(v).rolling(20, min_periods=5).mean().shift(1).values
    tp_ = (h + l + c) / 3; grp = pd.Series(sd).ne(pd.Series(sd).shift()).cumsum().values
    vw = pd.Series(tp_ * v).groupby(grp).cumsum().values / np.maximum(pd.Series(v).groupby(grp).cumsum().values, 1e-9)
    d4 = D.bars(sym, 240); h4, l4, c4 = d4.high.values, d4.low.values, d4.close.values; s4h, s4l = swings(h4, l4, 1)
    bias4 = np.zeros(len(c4)); lh = ll = None; b = 0
    for i in range(2, len(c4)):
        if s4h[i - 1]: lh = h4[i - 1]
        if s4l[i - 1]: ll = l4[i - 1]
        if lh is not None and c4[i] > lh: b = 1
        if ll is not None and c4[i] < ll: b = -1
        bias4[i] = b
    bi = np.searchsorted(d4.index.values + np.timedelta64(240, 'm'), d.index.values, side='right') - 1
    B = np.where(bi >= 0, bias4[np.clip(bi, 0, None)], 0)
    PH, PL = rth_prev(sym); ONH, ONL = on_range(sym)
    rows = []
    for k, ix in days.items():
        for wname, t0, t1, LH, LL, tend in (('Asia', 1200, 1380, PH.get(k, np.nan), PL.get(k, np.nan), 120), ('NY', 570, 690, ONH.get(k, np.nan), ONL.get(k, np.nan), 960)):
            win = ix[(mn[ix] >= t0) & (mn[ix] < t1)]
            if len(win) < 10: continue
            e = endbar(ix, mn, tend) if wname == 'NY' else ix[(mn[ix] >= 1200) | (mn[ix] < 120)][-1]
            s = int(B[win[0]])                         # bearish bias -> a high is swept -> short
            if s == 0: continue
            L = LH if s == -1 else LL
            if L != L: continue
            sw = [i for i in win if (s == -1 and h[i] > L) or (s == 1 and l[i] < L)]
            if not sw: continue
            i0 = sw[0]; ext = h[i0] if s == -1 else l[i0]
            for i in range(i0, min(i0 + 15, win[-1] + 1)):
                ext = max(ext, h[i]) if s == -1 else min(ext, l[i])
                edge = np.nan
                for q in range(i - 1, max(i - 30, ix[0] + 2), -1):
                    if s == -1 and l[q] > h[q - 2]: edge = h[q - 2]; break
                    if s == 1 and h[q] < l[q - 2]: edge = l[q - 2]; break
                if edge != edge: continue
                body = abs(c[i] - o[i])
                if ((s == -1 and c[i] < edge and c[i] < o[i] and c[i] < vw[i]) or (s == 1 and c[i] > edge and c[i] > o[i] and c[i] > vw[i])) \
                        and va[i] == va[i] and v[i] >= 1.5 * va[i] and atr[i] == atr[i] and body >= atr[i]:
                    tp = LL if s == -1 else LH
                    rows.append((i, s, ext + 2 * tick if s == -1 else ext - 2 * tick, tp if s * (tp - c[i]) > 0 else np.nan, np.nan, e, win[0], e, f'IFVG {wname}', np.nan)); break
    return out2(rows)


# ---------------------------------------------------------------- Trader Yush - Order flow range model (proxy, 5m)
def yush(d, m, DL, sym):
    """PROXY (his big-lot prints, delta and DOM can't be seen). Value = previous NY session profile (VAH / VAL / POC). Area of interest =
    VAH or VAL with a market level (previous day H / L / close, overnight H / L) within 5 NQ pts (2 ES) = 2 of his 4 tools. Range day =
    the 10:00 price is inside value. 09:30-12:00: a 5m candle trades above VAH and closes back inside (failed breakout) = short at the
    close; stop 2 ticks above the high. His T1 = middle of value (half off, break-even), T2 = VAL. Longs mirror at VAL."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']; tol = 5 * NQSTOP[m] / 1.0 if m == 'NQ' else 2.0
    ONH, ONL = on_range(sym); dd = D.daily(sym); PDH, PDL, PDC = dd.high.shift(1), dd.low.shift(1), dd.close.shift(1)
    rows = []
    for k, ix in days.items():
        if k not in DL.index: continue
        r = DL.loc[k]
        if not (r.pVAH == r.pVAH): continue
        VAH, VAL = r.pVAH, r.pVAL; MID = (VAH + VAL) / 2
        mk = [x for x in (PDH.get(k, np.nan), PDL.get(k, np.nan), PDC.get(k, np.nan), ONH.get(k, np.nan), ONL.get(k, np.nan)) if x == x]
        b10 = ix[mn[ix] == 600]
        rng_day = bool(len(b10) and VAL <= c[b10[0]] <= VAH)
        win = ix[(mn[ix] >= 570) & (mn[ix] < 720)]; e = endbar(ix, mn, 960)
        for s, edge, tp in ((-1, VAH, VAL), (1, VAL, VAH)):
            if not any(abs(x - edge) <= tol for x in mk): continue
            for i in win:
                if (s == -1 and h[i] > edge and c[i] < edge) or (s == 1 and l[i] < edge and c[i] > edge):
                    rows.append((i, s, h[i] + 2 * tick if s == -1 else l[i] - 2 * tick, tp, np.nan, e, win[0], e, 'Range day' if rng_day else 'Trend day', MID)); break
    return out2(rows)


def register(EXTRA):
    import cfstrat as CS
    def may():
        for m in ('NQ', 'ES', 'GC'):
            for d in D.series(m, 15):
                src = d.src.iloc[0]
                yield 'Trader Mayne', m, 15, src, d, mayne(d, m, src), dict(entries=[('limit', 'lim'), 'market'], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), 2, 3], exits=['stop/target']), None
    def mar():
        for m in ('NQ', 'ES'):
            for d in D.series(m, 5):
                src = d.src.iloc[0]
                yield 'Marco Trades', m, 5, src, d, marco(d, m, src), dict(entries=['market'], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), 2, 3, 5], exits=['stop/target']), None
    def des():
        for m in ('NQ', 'ES'):
            for d in D.series(m, 2):
                src = d.src.iloc[0]
                yield 'Vincent Desiano', m, 2, src, d, desiano(d, m, src), dict(entries=['market'], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), 2, None], exits=['stop/target', ('half', 1)]), None
    def per():
        for m in ('NQ', 'ES'):
            for d in D.series(m, 1):
                src = d.src.iloc[0]
                yield 'Abraham Perez', m, 1, src, d, perez(d, m, src), dict(entries=['market'], stops=[('col', 'wk'), 'fixed'], targets=[2, ('col', 'tp')], exits=['stop/target']), None
    def yus():
        for m in ('NQ', 'ES'):
            for d in D.series(m, 5):
                src = d.src.iloc[0]; DL = CS.extra_levels(src, m)
                yield 'Trader Yush', m, 5, src, d, yush(d, m, DL, src), dict(entries=['market'], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), ('col', 'tp2'), 2], exits=['stop/target']), None
    EXTRA.update(Mayne=may, Marco=mar, Desiano=des, Perez=per, Yush=yus)
