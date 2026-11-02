"""Retest grid for Body Flip CDS / CDL (Nov 2 2026, test 2).
Entries are limits placed back inside the C1 or C2 candle range after the flip (C2 close), plus market at C2 close.
Depth is measured from the side price is on: long -> 0% = top of the range, 100% = bottom; short -> 0% = bottom, 100% = top.
So 100% of the C1 range is the C1 wick = the PO4 line.
ENTRIES 0 market C2 close · 1-7 last C1 range 0/12.5/25/50/75/87.5/100% · 8-14 strongest C1 range (same) · 15-21 C2 range (same)
STOPS   0 PO4 = last C1 wick · 1 PO4 = strongest C1 wick · 2-5 ATR line trailing x0.5 / 1 / 1.5 / 2 · 6-9 fixed points: NQ 20 / 40 / 50 / 60 (ES 8 / 16 / 20 / 24, gold 4.8 / 9.6 / 12 / 14.4, crude 0.20 / 0.40 / 0.50 / 0.60)
TARGETS 1:2 1:3 1:4 1:5 1:6 none
EXITS   0 stop / target only · 1 also exit at the close of the next opposite flip (opposite CDS / CDL)
WAIT    limit order lives 10 or 30 candles; an opposite flip cancels it.
Graded on the chart candles, stop first on a tie, limits fill 1 tick through, cost per trade, 100-candle limit,
risk under 8% of the fixed stop skipped. Fill candle: only the move against you counts."""
import numpy as np
from numba import njit

LEV = np.array([0.0, 0.125, 0.25, 0.5, 0.75, 0.875, 1.0])
KST = np.array([0.5, 1.0, 1.5, 2.0])
KFX = np.array([0.4, 0.8, 1.0, 1.2])   # x the market's base stop (NQ 50) -> NQ 20 / 40 / 50 / 60
TGT = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 1e9])
WAITS = np.array([10, 30], np.int64)
NE, NST, NT, NX, NW = 22, 10, 6, 2, 2
LN = ['0%', '12.5%', '25%', '50%', '75%', '87.5%', '100%']
EN = ['market C2 close'] + [f'limit last C1 range {x}' for x in LN] + [f'limit strongest C1 range {x}' for x in LN] + [f'limit C2 range {x}' for x in LN]
SN = ['PO4 last C1 wick', 'PO4 strongest C1 wick', 'ATR x0.5 trailing', 'ATR x1 trailing', 'ATR x1.5 trailing', 'ATR x2 trailing', 'fixed 20 pts', 'fixed 40 pts', 'fixed 50 pts', 'fixed 60 pts']
TN = ['1:2', '1:3', '1:4', '1:5', '1:6', 'no target']
XN = ['stop/target only', 'exit at next flip']
WN = ['wait 10', 'wait 30']


@njit(cache=True)
def _line(trend, lnW, atr, j, s, k):
    if j < 0 or trend[j] != s or lnW[j] != lnW[j] or atr[j] != atr[j]: return np.nan
    return lnW[j] - s * k * atr[j]


@njit(cache=True)
def grade(o, h, l, c, trend, lnW, atr, flipUp, flipDn,
          sI, sS, sC1, sSC1, sPO, sSPO, sMask, sPer, nslot, s50, cost, tick, HOLD, acc):
    """acc[side, per, slot, w, e, st, t, x, 6 stats]. sC1 / sSC1 = bar of last / strongest C1, sPO / sSPO = their wick (PO4)."""
    n = len(c)
    minr = 0.08 * s50
    res = np.zeros((NT, NX))
    tT = np.empty(NT, np.int64)
    for q in range(len(sI)):
        i = sI[q]; s = sS[q]; sd = 0 if s == -1 else 1; per = sPer[q]; mask = sMask[q]
        if i + 2 >= n: continue
        for w in range(NW):
            WAIT = WAITS[w]
            for e in range(NE):
                if e == 0:
                    px = c[i]
                else:
                    g = (e - 1) // 7; f = LEV[(e - 1) % 7]
                    b = sC1[q] if g == 0 else (sSC1[q] if g == 1 else i)
                    if s == 1: px = h[b] - f * (h[b] - l[b])
                    else: px = l[b] + f * (h[b] - l[b])
                    px = np.round(px / tick) * tick
                kf = -1; ep = px
                if e == 0:
                    kf = i
                else:
                    if s * (c[i] - px) <= 0: continue          # limit must sit on the pullback side of the C2 close
                    for j in range(i + 1, min(i + WAIT + 1, n)):
                        if (s == 1 and l[j] <= px - tick) or (s == -1 and h[j] >= px + tick):
                            kf = j; ep = min(o[j], px) if s == 1 else max(o[j], px); break
                        if (s == 1 and flipDn[j]) or (s == -1 and flipUp[j]): break   # flip known at the close: cancels after the candle
                    if kf < 0: continue
                for st in range(NST):
                    if st == 0: stop = sPO[q]
                    elif st == 1: stop = sSPO[q]
                    elif st >= 6: stop = ep - s * KFX[st - 6] * s50
                    else: stop = _line(trend, lnW, atr, kf if e == 0 else kf - 1, s, KST[st - 2])
                    if stop != stop: continue
                    risk = s * (ep - stop)
                    if not (risk >= minr): continue
                    lim = min(kf + HOLD, n - 1)
                    tStop = -1; pStop = 0.0; tF = -1; pF = 0.0
                    for k in range(NT): tT[k] = -1
                    if e > 0 and ((s == 1 and l[kf] <= stop) or (s == -1 and h[kf] >= stop)):
                        tStop = kf; pStop = stop
                    jEnd = lim
                    if tStop < 0:
                        for j in range(kf + 1, lim + 1):
                            if st >= 2 and st <= 5:
                                ln = _line(trend, lnW, atr, j - 1, s, KST[st - 2])
                                if ln == ln:
                                    stop = max(stop, ln) if s == 1 else min(stop, ln)
                            if (s == 1 and l[j] <= stop) or (s == -1 and h[j] >= stop):
                                tStop = j; pStop = min(o[j], stop) if s == 1 else max(o[j], stop); jEnd = j
                                break
                            fav = h[j] - ep if s == 1 else ep - l[j]
                            for k in range(NT - 1):
                                if tT[k] < 0 and fav >= TGT[k] * risk: tT[k] = j
                            if tF < 0 and ((s == 1 and flipDn[j]) or (s == -1 and flipUp[j])):
                                tF = j; pF = c[j]
                    for ti in range(NT):
                        for xi in range(NX):
                            best = (jEnd + 1) * 4 + 3; bp = c[jEnd]
                            if tStop >= 0:
                                best = tStop * 4 + 1; bp = pStop
                            if ti < NT - 1 and tT[ti] >= 0 and tT[ti] * 4 + 2 < best:
                                best = tT[ti] * 4 + 2; bp = ep + s * TGT[ti] * risk
                            if xi == 1 and tF >= 0 and tF * 4 + 3 < best:
                                best = tF * 4 + 3; bp = pF
                            res[ti, xi] = (s * (bp - ep) - cost) / risk
                    for sl in range(nslot):
                        if (mask >> sl) & 1:
                            for ti in range(NT):
                                for xi in range(NX):
                                    v = res[ti, xi]
                                    a = acc[sd, per, sl, w, e, st, ti, xi]
                                    a[0] += 1.0; a[2] += v; a[3] += v * v
                                    if v > 0:
                                        a[1] += 1.0; a[4] += v
                                    else:
                                        a[5] -= v
    return 0
