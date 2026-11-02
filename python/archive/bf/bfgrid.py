"""Full trade grid for the Body Flip CDS / CDL signals (numba).
Every signal x 6 entries x 8 stops x 7 targets x 9 exits x 2 (half out or not), long and short apart, two periods,
up to 20 slots (time windows and filters). Graded on the chart candles, stop first on a tie, limit target from the
candle after the fill, 1 tick through for limits, cost per trade, 100-candle limit, risk under 8% of the fixed stop skipped.
ENTRIES 0 market at C2 close · 1 limit C2 open · 2 limit C2 50% · 3 limit C1 body (open) · 4 limit CDS/CDL line · 5 limit C1 wick
STOPS   0 fixed (NQ 50 / ES 20 / gold 12 / crude 0.50) · 1 C1 wick (protected PO4) · 2-7 ATR line trailing x 0.25 0.5 0.75 1 1.5 2
TARGETS 1 1.5 2 3 4 6 RR · ride (no target)
EXITS   0 stop / target only · 1 opposite CDS / CDL · 2 close beyond the trend line · 3/4 close beyond ATR line x0.5 / x1
        5/6 wick touch of ATR line x0.5 / x1 · 7 next session open (02:00 / 08:00 / 09:30) · 8 first opposite BC
HALF    0 none · 1 half off at +0.5R, rest stop to entry"""
import numpy as np
from numba import njit

KST = np.array([0.25, 0.5, 0.75, 1.0, 1.5, 2.0])
KEX = np.array([0.5, 1.0])
TGT = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 1e9])
NE, NST, NT, NX, NH = 6, 8, 7, 9, 2
EN = ['market C2 close', 'limit C2 open', 'limit C2 50%', 'limit C1 open', 'limit CDS/CDL line', 'limit C1 wick']
SN = ['fixed', 'C1 wick (PO4)', 'ATR x0.25', 'ATR x0.5', 'ATR x0.75', 'ATR x1', 'ATR x1.5', 'ATR x2']
TN = ['1:1', '1:1.5', '1:2', '1:3', '1:4', '1:6', 'ride']
XN = ['stop/target only', 'opposite CDS/CDL', 'close past trend line', 'close past ATR x0.5', 'close past ATR x1',
      'touch ATR x0.5', 'touch ATR x1', 'next session open', 'first opposite BC']
HN = ['full', 'half at +0.5R']


@njit(cache=True)
def _line(trend, lnW, atr, j, s, k):
    # ATR line of the trade side known after candle j (nan if the trend is not the trade side)
    if j < 0 or trend[j] != s or lnW[j] != lnW[j] or atr[j] != atr[j]: return np.nan
    return lnW[j] - s * k * atr[j]


@njit(cache=True)
def grade(o, h, l, c, trend, lnW, atr, flipUp, flipDn, buX, beX, sess,
          sI, sS, sC1W, sC1B, sLine, sMask, sPer, nslot, s50, cost, tick, HOLD, WAIT, KST, KEX, TGT, acc, keep, outK):
    """acc[side, per, slot, e, st, t, x, h, 6 stats]. keep: (e, st, t, x, h) combos whose single trades are written to outK."""
    n = len(c)
    minr = 0.08 * s50
    nk = keep.shape[0]
    res = np.zeros((NT, NX, NH))
    ok = np.zeros((NT, NX, NH), np.bool_)
    tT = np.empty(NT, np.int64)
    tX = np.empty(NX, np.int64); pX = np.empty(NX)
    tX4 = np.empty(2, np.int64); pX4 = np.empty(2)
    tX4H = np.empty(2, np.int64); pX4H = np.empty(2)
    nout = 0
    for q in range(len(sI)):
        i = sI[q]; s = sS[q]; sd = 0 if s == -1 else 1; per = sPer[q]; mask = sMask[q]
        if i + 2 >= n: continue
        for e in range(NE):
            if e == 0: px = c[i]
            elif e == 1: px = o[i]
            elif e == 2: px = (o[i] + c[i]) / 2
            elif e == 3: px = sC1B[q]
            elif e == 4: px = sLine[q]
            else: px = sC1W[q]
            if px != px: continue
            kf = -1; ep = px; start = 0
            if e == 0:
                kf = i; start = i + 1
            else:
                if s * (c[i] - px) <= 0: continue          # not a limit on the right side
                for j in range(i + 1, min(i + WAIT + 1, n)):
                    if (s == 1 and l[j] <= px - tick) or (s == -1 and h[j] >= px + tick):
                        kf = j; ep = min(o[j], px) if s == 1 else max(o[j], px); break
                    if (s == 1 and flipDn[j]) or (s == -1 and flipUp[j]): break
                if kf < 0: continue
                start = kf + 1
            for st in range(NST):
                if st == 0: stop = ep - s * s50
                elif st == 1: stop = sC1W[q]
                else:
                    stop = _line(trend, lnW, atr, kf if e == 0 else kf - 1, s, KST[st - 2])
                if stop != stop: continue
                risk = s * (ep - stop)
                if not (risk >= minr): continue
                lim = min(kf + HOLD, n - 1)
                # fill candle of a limit: only the move against you
                tStop = -1; pStop = 0.0
                if e > 0 and ((s == 1 and l[kf] <= stop) or (s == -1 and h[kf] >= stop)):
                    tStop = kf; pStop = stop
                for k in range(NT): tT[k] = -1
                for k in range(NX): tX[k] = -1
                for k in range(2):
                    tX4[k] = -1; tX4H[k] = -1
                tH = -1; tSH = -1; pSH = 0.0
                lvT = 0.0
                jEnd = lim
                if tStop < 0:
                    for k in range(2):
                        lv0 = _line(trend, lnW, atr, kf if e == 0 else kf - 1, s, KEX[k])
                        if e > 0 and lv0 == lv0 and ((s == 1 and l[kf] <= max(lv0, stop)) or (s == -1 and h[kf] >= min(lv0, stop))):
                            tX4[k] = kf; pX4[k] = max(lv0, stop) if s == 1 else min(lv0, stop)
                    for j in range(start, lim + 1):
                        # session open exit happens at the open
                        if tX[7] < 0 and sess[j]:
                            tX[7] = j; pX[7] = o[j]
                        # trail the ATR stop
                        if st >= 2:
                            ln = _line(trend, lnW, atr, j - 1, s, KST[st - 2])
                            if ln == ln:
                                if s == 1: stop = max(stop, ln)
                                else: stop = min(stop, ln)
                        # half-out stop (entry or better)
                        if tH >= 0 and tSH < 0:
                            sh = max(stop, ep) if s == 1 else min(stop, ep)
                            if (s == 1 and l[j] <= sh) or (s == -1 and h[j] >= sh):
                                tSH = j; pSH = min(o[j], sh) if s == 1 else max(o[j], sh)
                        for k in range(2):
                            lv = _line(trend, lnW, atr, j - 1, s, KEX[k])
                            if tX4[k] < 0:
                                eff = stop
                                if lv == lv: eff = max(stop, lv) if s == 1 else min(stop, lv)
                                if (s == 1 and l[j] <= eff) or (s == -1 and h[j] >= eff):
                                    tX4[k] = j; pX4[k] = min(o[j], eff) if s == 1 else max(o[j], eff)
                            if tH >= 0 and tX4H[k] < 0:
                                eff = max(stop, ep) if s == 1 else min(stop, ep)
                                if lv == lv: eff = max(eff, lv) if s == 1 else min(eff, lv)
                                if (s == 1 and l[j] <= eff) or (s == -1 and h[j] >= eff):
                                    tX4H[k] = j; pX4H[k] = min(o[j], eff) if s == 1 else max(o[j], eff)
                        stopNow = (s == 1 and l[j] <= stop) or (s == -1 and h[j] >= stop)
                        if stopNow:
                            tStop = j; pStop = min(o[j], stop) if s == 1 else max(o[j], stop)
                            jEnd = j
                            break
                        fav = h[j] - ep if s == 1 else ep - l[j]
                        if tH < 0 and fav >= 0.5 * risk: tH = j
                        for k in range(NT - 1):
                            if tT[k] < 0 and fav >= TGT[k] * risk: tT[k] = j
                        # close exits
                        opp = flipDn[j] if s == 1 else flipUp[j]
                        if tX[1] < 0 and opp:
                            tX[1] = j; pX[1] = c[j]
                        if tX[2] < 0:
                            lv2 = lnW[j - 1] if trend[j - 1] == s else np.nan
                            if opp or (lv2 == lv2 and s * (c[j] - lv2) < 0):
                                tX[2] = j; pX[2] = c[j]
                        for k in range(2):
                            if tX[3 + k] < 0:
                                lv = _line(trend, lnW, atr, j - 1, s, KEX[k])
                                if opp or (lv == lv and s * (c[j] - lv) < 0):
                                    tX[3 + k] = j; pX[3 + k] = c[j]
                        if tX[8] < 0 and ((s == 1 and beX[j]) or (s == -1 and buX[j])):
                            tX[8] = j; pX[8] = c[j]
                # resolve every variant
                for ti in range(NT):
                    for xi in range(NX):
                        for hi in range(NH):
                            # first event for the full position. code: time*4 + priority (0 open, 1 stop, 2 target, 3 close)
                            best = (jEnd + 1) * 4 + 3; bp = c[jEnd]; kind = 9
                            if tStop >= 0:
                                best = tStop * 4 + 1; bp = pStop; kind = 1
                            if xi == 5 or xi == 6:
                                k = xi - 5
                                if tX4[k] >= 0 and tX4[k] * 4 + 1 < best:
                                    best = tX4[k] * 4 + 1; bp = pX4[k]; kind = 1
                            if ti < NT - 1 and tT[ti] >= 0 and tT[ti] * 4 + 2 < best:
                                best = tT[ti] * 4 + 2; bp = ep + s * TGT[ti] * risk; kind = 2
                            if xi == 7 and tX[7] >= 0 and tX[7] * 4 < best:
                                best = tX[7] * 4; bp = pX[7]; kind = 0
                            if (xi == 1 or xi == 2 or xi == 3 or xi == 4 or xi == 8 or xi == 5 or xi == 6):
                                xc = xi if xi <= 4 or xi == 8 else 1     # touch exits also leave on the opposite CDS / CDL
                                if tX[xc] >= 0 and tX[xc] * 4 + 3 < best:
                                    best = tX[xc] * 4 + 3; bp = pX[xc]; kind = 3
                            r = s * (bp - ep)
                            if hi == 1 and tH >= 0 and tH * 4 + 1 < best and not (tH * 4 + 1 == best):
                                # half taken: the rest exits on the first of half-stop, target, exit, limit
                                best2 = (jEnd + 1) * 4 + 3; bp2 = c[jEnd]
                                if tStop >= 0:
                                    best2 = tStop * 4 + 1; bp2 = pStop
                                if tSH >= 0 and tSH * 4 + 1 < best2:
                                    best2 = tSH * 4 + 1; bp2 = pSH
                                if xi == 5 or xi == 6:
                                    k = xi - 5
                                    if tX4H[k] >= 0 and tX4H[k] * 4 + 1 < best2:
                                        best2 = tX4H[k] * 4 + 1; bp2 = pX4H[k]
                                if ti < NT - 1 and tT[ti] >= 0 and tT[ti] * 4 + 2 < best2:
                                    best2 = tT[ti] * 4 + 2; bp2 = ep + s * TGT[ti] * risk
                                if xi == 7 and tX[7] >= 0 and tX[7] * 4 < best2:
                                    best2 = tX[7] * 4; bp2 = pX[7]
                                if (xi >= 1 and xi <= 6) or xi == 8:
                                    xc = xi if xi <= 4 or xi == 8 else 1
                                    if tX[xc] >= 0 and tX[xc] * 4 + 3 < best2:
                                        best2 = tX[xc] * 4 + 3; bp2 = pX[xc]
                                r = 0.5 * 0.5 * risk + 0.5 * s * (bp2 - ep)
                            res[ti, xi, hi] = (r - cost) / risk
                # accumulate
                for sl in range(nslot):
                    if (mask >> sl) & 1:
                        for ti in range(NT):
                            for xi in range(NX):
                                for hi in range(NH):
                                    v = res[ti, xi, hi]
                                    a = acc[sd, per, sl, e, st, ti, xi, hi]
                                    a[0] += 1.0; a[2] += v; a[3] += v * v
                                    if v > 0:
                                        a[1] += 1.0; a[4] += v
                                    else:
                                        a[5] -= v
                for kk in range(nk):
                    if keep[kk, 0] == e and keep[kk, 1] == st and nout < outK.shape[0]:
                        outK[nout, 0] = kk; outK[nout, 1] = q; outK[nout, 2] = res[keep[kk, 2], keep[kk, 3], keep[kk, 4]]
                        outK[nout, 3] = risk; outK[nout, 4] = i
                        nout += 1
    return nout
