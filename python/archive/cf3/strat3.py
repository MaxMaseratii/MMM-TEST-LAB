"""Re-check from the full transcripts (Nov 2 2026): Trader Kane (Chart Fanatics ep. 1), Okala (8020 episode), Fabio Valentini (IQ Capital,
"Nasdaq Effort / machine gun 1:1"). Every rule is quoted from the transcript; every gap is ONE stated assumption (ASSUME).
Signal frame columns: i, s, wk (structure stop), lim (limit price), tp / tp2 (trader target prices), endb, w0, w1, tag."""
import sys, numpy as np, pandas as pd
from numba import njit
sys.path.insert(0, '/home/claude/mmmlab'); sys.path.insert(0, '/home/claude/cf')
from mmmlab import data as D
from mmmlab.candles import atr_rma
from cfstrat import base, endbar, swings

COLS = ['i', 's', 'wk', 'lim', 'tp', 'tp2', 'endb', 'w0', 'w1', 'tag']
def out(rows): return pd.DataFrame(rows, columns=COLS) if rows else pd.DataFrame(columns=COLS)


# ------------------------------------------------------------------ bars
def bars200(d1):
    """Okala's 200-second chart cannot be built from 1-minute data; ASSUME the closest proxy: each 10-minute block split 3+3+4 minutes
    (so three bars = one 10-minute candle, like his 200 s = 1/3 of 10 min)."""
    mn = d1.index.minute.values % 10
    part = np.where(mn < 3, 0, np.where(mn < 6, 3, 6))
    key = d1.index.floor('10min') + pd.to_timedelta(part, unit='m')
    g = d1.groupby(key)
    B = pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(), 'volume': g.volume.sum(),
                      'delta': g.delta.sum(), 'per': g.per.first(), 'src': g.src.first()})
    B['last'] = pd.Series(d1.index, index=d1.index).groupby(key).max()
    return B


def resample(d1, tf):
    key = d1.index.floor(f'{tf}min'); g = d1.groupby(key)
    B = pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(), 'volume': g.volume.sum(),
                      'delta': g.delta.sum(), 'per': g.per.first(), 'src': g.src.first()})
    B['last'] = pd.Series(d1.index, index=d1.index).groupby(key).max()
    return B


def to_1m(B, S, d1):
    """execute candle signals on the 1-minute bars: signal at the candle's last minute; end / window mapped the same way."""
    if not len(S): return S
    pos = d1.index.get_indexer(B['last'].values)
    S = S.copy()
    for col in ('i', 'endb', 'w0', 'w1'): S[col] = pos[S[col].values.astype(int)]
    return S[(S.i >= 0) & (S.endb > S.i)].reset_index(drop=True)


# ------------------------------------------------------------------ OKALA 8020
def lvls(p, tol, want=(20, 80)):
    base_ = np.floor(p / 100) * 100
    return [L for L in (base_ + x for x in (-80, -20, 20, 80, 120, 180)) if round(L % 100) in want and abs(L - p) <= tol]


def next_level(p, s, gap=15.0):
    """next 20 / 80 level at least `gap` points away in the trade direction."""
    base_ = np.floor(p / 100) * 100
    cand = sorted(base_ + x for x in (-180, -120, -80, -20, 20, 80, 120, 180, 220, 280))
    cand = [L for L in cand if s * (L - p) >= gap]
    return (min(cand) if s == 1 else max(cand)) if cand else np.nan


def okala2(d, m='NQ', t0=570, t1=690, tend=720):
    """Window: NY open (09:30) to 11:30, runners out by 12:00 ("avoid the lunch hour"; ASSUME exact times).
    Levels = prices ending in 20 / 80. His risk: 10 pt stop always; TP1 +15 to cover risk; then break-even; runner to a magnet.
    Magnets ("repair") = a candle that opens with NO wick on its open side (red: open = high; green: open = low) - untouched opens are
      targets. tp = nearest untouched repair beyond +15 (else the next 20/80 level), tp2 = next 20/80 level beyond +15.
    LEVEL TAP: limit at a 20/80 level when price is coming into it from the other side (within 8 pts, level untouched for 6 bars).
    FORK long (and mirror): strong move down (high of the 6 bars before minus the low >= 1.5 ATR, ASSUME), initiation candle with a long
      lower wick (>= 50% of its range) and small body (<= 35%), next candle tests that low (within 4 pts) without breaking it -> entry at
      its close if it closes >= 2 pts above the low (his example: low 23, entry 27, 10 pt stop).
    H (continuation, either side): a move lower (10-bar high to price >= 1.5 ATR), a bounce candle reaches a 20/80 level with a wick, the
      next candle rolls over (closes below the bounce candle's low) -> limit at the level retest. Mirror for longs.
    CROSS-SECTION: two strong same-colour candles in a row (bodies >= 60% of range, together >= 1 ATR); the cross = where the first closes
      and the second opens. When price comes back within 8 pts of an untested cross -> limit at the cross (continuation side).
    Tags say if a 20/80 level sits within 3 pts of the entry (his best entries stack level + structure)."""
    o, h, l, c, v, mn, sd, days = base(d); tick = D.SPEC[m]['tick']
    atr = atr_rma(h, l, c, 14); n = len(c)
    rng = h - l; body = np.abs(c - o)
    rows = []
    for k, ix in days.items():
        win = ix[(mn[ix] >= t0) & (mn[ix] < t1)]
        if len(win) < 6: continue
        e = endbar(ix, mn, tend); w0 = win[0]
        reps = []                     # [price, side it pulls: +1 above (target for longs) / -1 below, alive]
        crosses = []                  # [price, side to trade, alive, bar]
        ix0 = ix[(mn[ix] >= 480) & (mn[ix] < t1)]
        for i in ix0:
            if i < 14: continue
            # update magnets touched
            for r in reps:
                if r[2] and l[i] <= r[0] <= h[i]: r[2] = False
            if mn[i] >= t0:
                def tgts(px, s):
                    mags = [r[0] for r in reps if r[2] and s * (r[0] - px) >= 15]
                    t2 = next_level(px, s)
                    t1_ = (min(mags) if s == 1 else max(mags)) if mags else t2
                    return t1_, t2
                lv = lambda px: 'level' if lvls(px, 3.0) else 'no level'
                # LEVEL TAP
                for L in lvls(c[i], 8.0):
                    s = 1 if c[i] > L else -1
                    if abs(c[i] - L) < 1: continue
                    if (l[max(0, i - 6):i + 1].min() <= L <= h[max(0, i - 6):i + 1].max()): continue
                    if s * (c[i] - c[i - 3]) >= 0: continue          # must be coming INTO the level
                    a, b = tgts(L, s); rows.append((i, s, L - s * 10, L, a, b, e, w0, e, f'Level tap {"long" if s == 1 else "short"} {int(round(L % 100))}'))
                # FORK + reverse fork
                kk = i - 1; a_ = atr[kk]
                if a_ == a_ and a_ > 0 and rng[kk] > 0:
                    lw = min(o[kk], c[kk]) - l[kk]; uw = h[kk] - max(o[kk], c[kk])
                    if h[kk - 6:kk].max() - l[kk] >= 1.5 * a_ and lw >= .5 * rng[kk] and body[kk] <= .35 * rng[kk] \
                            and l[kk] <= l[i] <= l[kk] + 4 and c[i] >= l[kk] + 2:
                        a, b = tgts(c[i], 1); rows.append((i, 1, l[kk] - tick, np.nan, a, b, e, w0, e, f'Fork long | {lv(l[kk])}'))
                    if h[kk] - l[kk - 6:kk].min() >= 1.5 * a_ and uw >= .5 * rng[kk] and body[kk] <= .35 * rng[kk] \
                            and h[kk] - 4 <= h[i] <= h[kk] and c[i] <= h[kk] - 2:
                        a, b = tgts(c[i], -1); rows.append((i, -1, h[kk] + tick, np.nan, a, b, e, w0, e, f'Fork short | {lv(h[kk])}'))
                # H continuation
                j = i - 1; a_ = atr[j]
                if a_ == a_ and a_ > 0:
                    Ls = lvls(h[j], 3.0)
                    if Ls and h[i - 11:i - 1].max() - c[i] >= 1.5 * a_ and h[j] >= h[j - 1] and c[i] < l[j] and c[i] < o[i]:
                        a, b = tgts(Ls[0], -1); rows.append((i, -1, Ls[0] + 10, Ls[0], a, b, e, w0, e, f'H short {int(round(Ls[0] % 100))}'))
                    Ls = lvls(l[j], 3.0)
                    if Ls and c[i] - l[i - 11:i - 1].min() >= 1.5 * a_ and l[j] <= l[j - 1] and c[i] > h[j] and c[i] > o[i]:
                        a, b = tgts(Ls[0], 1); rows.append((i, 1, Ls[0] - 10, Ls[0], a, b, e, w0, e, f'H long {int(round(Ls[0] % 100))}'))
                # CROSS-SECTION retest
                for x in crosses:
                    px, s, alive, b0 = x
                    if not alive or i - b0 < 2: continue
                    if l[i] <= px <= h[i]: x[2] = False; continue
                    dist = (px - c[i]) if s == -1 else (c[i] - px)      # short cross sits above price, long cross below
                    if 0 < dist <= 8 and i - b0 >= 2:
                        a, b = tgts(px, s); rows.append((i, s, px - s * 10, px, a, b, e, w0, e, f'Cross-section {"long" if s == 1 else "short"} | {lv(px)}'))
                        x[2] = False
            # new magnets / crosses born at this bar's close
            if h[i] - o[i] < tick / 2 and c[i] < o[i]: reps.append([o[i], 1, True])
            if o[i] - l[i] < tick / 2 and c[i] > o[i]: reps.append([o[i], -1, True])
            a_ = atr[i]
            if a_ == a_ and a_ > 0 and rng[i] > 0 and rng[i - 1] > 0 and body[i] >= .6 * rng[i] and body[i - 1] >= .6 * rng[i - 1]:
                if c[i] < o[i] and c[i - 1] < o[i - 1] and o[i - 1] - c[i] >= a_: crosses.append([(c[i - 1] + o[i]) / 2, -1, True, i])
                if c[i] > o[i] and c[i - 1] > o[i - 1] and c[i] - o[i - 1] >= a_: crosses.append([(c[i - 1] + o[i]) / 2, 1, True, i])
    S = out(rows)
    return S.drop_duplicates(['i', 's', 'tag']).reset_index(drop=True)


# ------------------------------------------------------------------ TRADER KANE
def kane2(J, has_es=True):
    """J = NQ bars (+ high_e / low_e = ES bars, same times). Rules from the episode:
    - Trades NQ only, 09:15-11:30 ET (10 AM is the key manipulation). ASSUME entries 09:40-11:30 (he avoids entering around the open).
    - Power of three on H1 + H4 (+ daily): the current hour trades above the previous hour's high (10 AM sweeps the 9 AM high) and the
      current 4-hour candle (blocks from 18:00) is above the previous 4-hour high -> look short. Daily swept PDH = tag only (his own
      example did not need it). Longs mirror.
    - Premium / discount: short only above 50% of the dealing range (ASSUME: the last 3 sessions' high to the lowest low since it).
    - SMT: one of NQ / ES took its previous-hour high and the other did not (a "crack in correlation").
    - Entry: NQ closes below the latest bullish FVG of the push (the inversion) -> sell stop (= market at that close); or limit on a
      retap of the inverted gap. Stop: above the divergence high. TP: 50% of the range (the swept high to the session low since 18:00).
    - Break-even when the next hourly candle flips in the trade direction (handled by the simulator, bemode 1).
    At most 2 tries per side per day ("I would always take two")."""
    o, h, l, c = (J[k].values.astype(float) for k in ('open', 'high', 'low', 'close'))
    he = J.high_e.values if has_es else h; le = J.low_e.values if has_es else l
    idx = J.index; mn = idx.hour.values * 60 + idx.minute.values; sd = D.sday(idx).values; tick = .25; n = len(c)
    hid = pd.Series(idx.floor('h')).values
    h4 = ((idx.hour.values - 18) % 24) // 4
    h4id = pd.Series(sd.astype('datetime64[ns]')).values.astype('int64') // 10 ** 9 // 86400 * 10 + h4
    def prev_ext(key, arr, f):
        s = pd.Series(arr).groupby(key).agg(f); ks = s.index.values
        pos = np.searchsorted(ks, key) - 1
        return np.where(pos >= 0, s.values[np.maximum(pos, 0)], np.nan)
    pHH, pHL = prev_ext(hid, h, 'max'), prev_ext(hid, l, 'min')
    pHHe, pHLe = prev_ext(hid, he, 'max'), prev_ext(hid, le, 'min')
    p4H, p4L = prev_ext(h4id, h, 'max'), prev_ext(h4id, l, 'min')
    run = lambda key, arr, f: pd.Series(arr).groupby(key).transform(f).values
    hH = run(hid, h, 'cummax'); hL = run(hid, l, 'cummin'); hHe = run(hid, he, 'cummax'); hLe = run(hid, le, 'cummin')
    c4H = run(h4id, h, 'cummax'); c4L = run(h4id, l, 'cummin')
    dH = run(sd, h, 'cummax'); dL = run(sd, l, 'cummin')
    day = pd.DataFrame({'h': h, 'l': l, 'sd': sd}).groupby('sd').agg(H=('h', 'max'), L=('l', 'min'))
    keys = list(day.index); kpos = {k: q for q, k in enumerate(keys)}
    days = {k: x.values for k, x in pd.Series(np.arange(n)).groupby(sd)}
    shN, slN = swings(h, l, 2)
    def smt_swing(i, s):
        # classic SMT at the last two confirmed NQ swing points (last 30 bars): NQ makes a higher high and ES a lower high, or the reverse
        js = [j for j in range(i - 2, max(i - 30, 2), -1) if (shN[j] if s == -1 else slN[j])][:2]
        if len(js) < 2: return False
        j2, j1 = js
        if s == -1:
            a = h[j2] > h[j1]; b = he[max(j2 - 2, 0):j2 + 3].max() > he[max(j1 - 2, 0):j1 + 3].max()
        else:
            a = l[j2] < l[j1]; b = le[max(j2 - 2, 0):j2 + 3].min() < le[max(j1 - 2, 0):j1 + 3].min()
        return a != b
    rows = []
    for k, ix in days.items():
        q = kpos[k]
        if q < 3: continue
        PDH, PDL = day.H.iloc[q - 1], day.L.iloc[q - 1]
        R3H = day.H.iloc[q - 3:q].max(); R3L = day.L.iloc[q - 3:q].min()
        win = ix[(mn[ix] >= 580) & (mn[ix] < 690)]
        if len(win) < 5: continue
        e = endbar(ix, mn, 960); w0 = ix[mn[ix] >= 555][0] if (mn[ix] >= 555).any() else win[0]
        tries = {1: 0, -1: 0}
        for i in win:
            for s in (-1, 1):
                if tries[s] >= 2: continue
                if s == -1:
                    swN, swE = hH[i] > pHH[i], hHe[i] > pHHe[i]; h4ok = c4H[i] > p4H[i]
                    eq = (max(R3H, dH[i]) + min(R3L, dL[i])) / 2; prem = c[i] > eq or hH[i] > eq
                else:
                    swN, swE = hL[i] < pHL[i], hLe[i] < pHLe[i]; h4ok = c4L[i] < p4L[i]
                    eq = (max(R3H, dH[i]) + min(R3L, dL[i])) / 2; prem = c[i] < eq or hL[i] < eq
                if not (swN or swE) or not h4ok: continue
                smt_h = swN != swE; smt_s = has_es and smt_swing(i, s)
                if has_es and not (smt_h or smt_s): continue
                # inversion of the latest FVG of the push (within the current hour and the bar before)
                b0 = max(i - 12, ix[0] + 2); lvl = np.nan; top = np.nan
                for qq in range(i - 1, b0, -1):
                    if s == -1 and l[qq] > h[qq - 2]: lvl, top = h[qq - 2], l[qq]; break
                    if s == 1 and h[qq] < l[qq - 2]: lvl, top = l[qq - 2], h[qq]; break
                if lvl != lvl: continue
                if not (s * (lvl - c[i]) > 0 and s * (lvl - c[i - 1]) <= 0): continue
                ext = hH[i] if s == -1 else hL[i]
                lo = dL[i] if s == -1 else dH[i]
                tp = (ext + lo) / 2
                if s * (tp - c[i]) <= 0: continue
                dly = 'PD swept' if (s == -1 and dH[i] > PDH) or (s == 1 and dL[i] < PDL) else 'PD not swept'
                dow = idx[i].dayofweek
                tag = f'{"short" if s == -1 else "long"} | {"premium" if prem else "wrong side of 50%"} | {dly} | {"Tue-Thu" if dow in (1, 2, 3) else "Mon/Fri"}'
                if not has_es: tag += ' | no ES'
                else: tag += ' | SMT ' + ('hour' if smt_h else 'swing')
                rows.append((i, s, ext + tick if s == -1 else ext - tick, lvl, tp, np.nan, e, w0, e, tag))
                tries[s] += 1
    return out(rows)


# ------------------------------------------------------------------ FABIO (IQ Capital episode): per-candle value migration
@njit(cache=True)
def _cand_profile(gid, lo, hi, vol, ng, bin_):
    """per candle (group id) POC / VAH / VAL (70%) from 1m bars, each 1m bar's volume spread evenly over its range."""
    poc = np.full(ng, np.nan); vah = np.full(ng, np.nan); val = np.full(ng, np.nan)
    n = len(gid); a = 0
    while a < n:
        g = gid[a]; b = a
        while b < n and gid[b] == g: b += 1
        L = lo[a:b].min(); H = hi[a:b].max(); p0 = np.floor(L / bin_) * bin_
        nb = int((H - p0) / bin_) + 1; hs = np.zeros(nb + 1)
        for j in range(a, b):
            i0 = int((lo[j] - p0) / bin_); i1 = int((hi[j] - p0) / bin_)
            w = vol[j] / (i1 - i0 + 1)
            for q in range(i0, min(i1, nb - 1) + 1): hs[q] += w
        hs = hs[:nb]; tot = hs.sum()
        if tot > 0:
            k = int(np.argmax(hs)); up = k; dn = k; acc = hs[k]
            while acc < .7 * tot and (up < nb - 1 or dn > 0):
                a1 = hs[up + 1] if up < nb - 1 else -1.0; b1 = hs[dn - 1] if dn > 0 else -1.0
                if a1 >= b1: up += 1; acc += a1
                else: dn -= 1; acc += b1
            poc[g] = p0 + (k + .5) * bin_; vah[g] = p0 + (up + 1) * bin_; val[g] = p0 + dn * bin_
        a = b
    return poc, vah, val


def candles_with_value(d1, tf, bin_=1.0):
    B = resample(d1, tf)
    key = d1.index.floor(f'{tf}min'); gid = B.index.get_indexer(key).astype(np.int64)
    poc, vah, val = _cand_profile(gid, d1.low.values.astype(float), d1.high.values.astype(float), d1.volume.values.astype(float), len(B), bin_)
    B['poc'], B['vah'], B['val'] = poc, vah, val
    return B


def fabio_mg(B, m='NQ'):
    """'Machine gun 1:1': each candle has its own value area. Value switching / migrating higher (this candle's POC above the last one's)
    with a green candle and buyers dominating (candle delta > 0, real bid/ask delta from the data) -> long; mirror for shorts.
    His entry: "put my position at the value area, covering below" -> limit at the candle's POC (ASSUME), stop 1 tick beyond the candle's
    value area (VAL for longs), target 1:1. Every qualifying candle is a new trade.
    Tags: switch (value had been migrating the other way) vs continue; with the day (price on the trade side of the session VWAP from
    09:30, ASSUME for his 'main direction of the day'); effort (range per contract above its 20-candle median = 'thin book' side, ASSUME
    proxy for his Nasdaq Effort boxes). NY 09:30-15:30, out by 16:00."""
    o, h, l, c, v, mn, sd, days = base(B); tick = D.SPEC[m]['tick']
    poc, vah, val, dl = B.poc.values, B.vah.values, B.val.values, B.delta.values.astype(float)
    tp_ = (h + l + c) / 3
    eff = (h - l) / np.maximum(v, 1); effm = pd.Series(eff).rolling(20, min_periods=10).median().shift(1).values
    rows = []
    for k, ix in days.items():
        ny = ix[(mn[ix] >= 570) & (mn[ix] < 930)]
        if len(ny) < 6: continue
        e = endbar(ix, mn, 960)
        cv = np.cumsum(tp_[ny] * v[ny]); cw = np.cumsum(v[ny]); vw = cv / np.maximum(cw, 1)
        for q in range(2, len(ny)):
            i = ny[q]
            for s in (1, -1):
                if not (s * (poc[i] - poc[i - 1]) > 0 and s * (c[i] - o[i]) > 0 and s * dl[i] > 0): continue
                wk = val[i] - tick if s == 1 else vah[i] + tick
                if s * (poc[i] - wk) <= 0: continue
                sw = 'switch' if s * (poc[i - 1] - poc[i - 2]) < 0 else 'continue'
                withday = 'with VWAP' if s * (c[i] - vw[q]) > 0 else 'against VWAP'
                ef = 'effort yes' if effm[i] == effm[i] and eff[i] > effm[i] else 'effort no'
                rows.append((i, s, wk, poc[i], np.nan, np.nan, e, ny[0], e, f'{sw} | {withday} | {ef}'))
    return out(rows)


def aggression_trail(d, m='NQ'):
    """Fabio trails "below the last aggression": exit a long at a close under the low of the latest aggressive buy candle
    (full body >= 60% of range, volume >= 1.5x the 30-candle median, closes up); shorts mirror. Returns {1: arr, -1: arr}."""
    o, h, l, c, v = (d[k].values.astype(float) for k in ('open', 'high', 'low', 'close', 'volume'))
    vmed = pd.Series(v).rolling(30, min_periods=10).median().shift(1).values
    rng = h - l; body = np.abs(c - o)
    ag = (rng > 0) & (body >= .6 * rng) & (v >= 1.5 * vmed)
    up = pd.Series(np.where(ag & (c > o), l, np.nan)).ffill().values
    dn = pd.Series(np.where(ag & (c < o), h, np.nan)).ffill().values
    return {1: np.nan_to_num(c < up, nan=False).astype(np.bool_), -1: np.nan_to_num(c > dn, nan=False).astype(np.bool_)}
