"""Grader for test 5 (new Body Flip logic): every event type x entry x stop x target x exit, independent trades.
ENTRIES 0 market at the signal close · 1 limit at the event level (touched / broken line, PO4, or the CDS / CDL line for a flip)
        · 2 limit at 50% of the signal candle. A limit must be on the pullback side of the close; it lives 10 candles; an opposite flip cancels it.
STOPS   0 structure (the signal candle wick beyond the level, or the PO4 for a flip) · 1-4 fixed NQ 20 / 40 / 50 / 60 (scaled)
        · 5 PO4 of the trade side (latest alive) · 6 ATR line (only when the trend is on the trade side) · 7 trend line (same)
TARGETS 1:1 1:2 1:3 1:4 1:6 none
EXITS   0 stop / target only · 1 also at the next opposite flip · 2 also at a close beyond the trade-side trend line (or the opposite flip)
        · 3 Max management: stop to entry + 1 fee once a body close in the trade direction closes past that, and out at the next opposite flip
Chart candles, stop first on a tie, limits fill 1 tick through, cost per trade, 100-candle limit, risk under 8% of the 50-pt stop skipped."""
import numpy as np
from numba import njit

KFX = np.array([0.4, 0.8, 1.0, 1.2])
TGT = np.array([1.0, 2.0, 3.0, 4.0, 6.0, 1e9])
NE, NST, NT, NX = 3, 8, 6, 4
EN = ['market at signal close', 'limit at the event level', 'limit at 50% of signal candle']
SN = ['structure (wick / PO4)', 'fixed 20 pts', 'fixed 40 pts', 'fixed 50 pts', 'fixed 60 pts', 'PO4 of trade side', 'ATR line', 'trend line']
TN = ['1:1', '1:2', '1:3', '1:4', '1:6', 'no target']
XN = ['stop/target only', 'out at next flip', 'out at close past trend line', 'BE +1 fee on BC, out at next flip']


@njit(cache=True)
def grade(o, h, l, c, trend, tl, at, poBu, poBe, flipUp, flipDn, buX, beX,
          sI, sS, sRef, sStr, sMask, sPer, nslot, s50, cost, tick, HOLD, WAIT, acc):
    n = len(c)
    minr = 0.08 * s50
    tT = np.empty(NT, np.int64)
    res = np.zeros((NT, NX))
    for q in range(len(sI)):
        i = sI[q]; s = sS[q]; sd = 0 if s == -1 else 1; per = sPer[q]; mask = sMask[q]
        if i + 2 >= n: continue
        for e in range(NE):
            if e == 0: px = c[i]
            elif e == 1: px = sRef[q]
            else: px = np.round((h[i] + l[i]) / 2 / tick) * tick
            if px != px: continue
            kf = -1; ep = px
            if e == 0:
                kf = i
            else:
                if s * (c[i] - px) <= 0: continue
                for j in range(i + 1, min(i + WAIT + 1, n)):
                    if (s == 1 and l[j] <= px - tick) or (s == -1 and h[j] >= px + tick):
                        kf = j; ep = min(o[j], px) if s == 1 else max(o[j], px); break
                    if (s == 1 and flipDn[j]) or (s == -1 and flipUp[j]): break
                if kf < 0: continue
            for st in range(NST):
                if st == 0: stop = sStr[q]
                elif st <= 4: stop = ep - s * KFX[st - 1] * s50
                elif st == 5: stop = poBu[i] if s == 1 else poBe[i]
                elif st == 6: stop = at[i] if trend[i] == s else np.nan
                else: stop = tl[i] if trend[i] == s else np.nan
                if stop != stop: continue
                risk = s * (ep - stop)
                if not (risk >= minr): continue
                lim = min(kf + HOLD, n - 1)
                be = ep + s * max(cost, tick)
                # path: plain stop, BE stop (x3)
                tS = -1; pS = 0.0; tB = -1; pB = 0.0; trig = False
                for k in range(NT): tT[k] = -1
                tF = -1; pF = 0.0; tL = -1; pL = 0.0
                if e > 0 and ((s == 1 and l[kf] <= stop) or (s == -1 and h[kf] >= stop)):
                    tS = kf; pS = stop; tB = kf; pB = stop
                else:
                    for j in range(kf + 1, lim + 1):
                        if tS < 0 and ((s == 1 and l[j] <= stop) or (s == -1 and h[j] >= stop)):
                            tS = j; pS = min(o[j], stop) if s == 1 else max(o[j], stop)
                        if tB < 0:
                            sb = stop
                            if trig: sb = max(stop, be) if s == 1 else min(stop, be)
                            if (s == 1 and l[j] <= sb) or (s == -1 and h[j] >= sb):
                                tB = j; pB = min(o[j], sb) if s == 1 else max(o[j], sb)
                        if tS >= 0 and tB >= 0: break
                        fav = h[j] - ep if s == 1 else ep - l[j]
                        if tS < 0:
                            for k in range(NT - 1):
                                if tT[k] < 0 and fav >= TGT[k] * risk: tT[k] = j
                        opp = flipDn[j] if s == 1 else flipUp[j]
                        if tF < 0 and opp:
                            tF = j; pF = c[j]
                        if tL < 0:
                            lv = tl[j - 1] if trend[j - 1] == s else np.nan
                            if opp or (lv == lv and s * (c[j] - lv) < 0):
                                tL = j; pL = c[j]
                        if not trig and ((s == 1 and buX[j]) or (s == -1 and beX[j])) and s * (c[j] - be) > 0:
                            trig = True
                for ti in range(NT):
                    for xi in range(NX):
                        if xi == 3:
                            best = (lim + 1) * 4 + 3; bp = c[lim]
                            if tB >= 0:
                                best = tB * 4 + 1; bp = pB
                            # targets are not tracked for the BE path beyond the plain-stop window; use them only if hit before the BE stop
                            if ti < NT - 1 and tT[ti] >= 0 and tT[ti] * 4 + 2 < best:
                                best = tT[ti] * 4 + 2; bp = ep + s * TGT[ti] * risk
                            if tF >= 0 and tF * 4 + 3 < best:
                                best = tF * 4 + 3; bp = pF
                        else:
                            best = (lim + 1) * 4 + 3; bp = c[lim]
                            if tS >= 0:
                                best = tS * 4 + 1; bp = pS
                            if ti < NT - 1 and tT[ti] >= 0 and tT[ti] * 4 + 2 < best:
                                best = tT[ti] * 4 + 2; bp = ep + s * TGT[ti] * risk
                            if xi == 1 and tF >= 0 and tF * 4 + 3 < best:
                                best = tF * 4 + 3; bp = pF
                            if xi == 2 and tL >= 0 and tL * 4 + 3 < best:
                                best = tL * 4 + 3; bp = pL
                        res[ti, xi] = (s * (bp - ep) - cost) / risk
                for sl in range(nslot):
                    if (mask >> sl) & 1:
                        for ti in range(NT):
                            for xi in range(NX):
                                v = res[ti, xi]
                                a = acc[sd, per, sl, e, st, ti, xi]
                                a[0] += 1.0; a[2] += v; a[3] += v * v
                                if v > 0:
                                    a[1] += 1.0; a[4] += v
                                else:
                                    a[5] -= v
    return 0


@njit(cache=True)
def found(o, h, l, c, buX, beX, sI, sS, sPer, sMask, out):
    """foundation stats: out[side, per, slot, 9] = n, sum BCs before opposite BC, sum BCs before first NBC, sum pts +1, +5, +10, sum sq +5, n(+10 avail), hits +5>0"""
    n = len(c)
    for q in range(len(sI)):
        i = sI[q]; s = sS[q]; sd = 0 if s == -1 else 1
        if i + 11 >= n: continue
        k1 = 0
        for j in range(i + 1, min(i + 200, n)):
            if (s == 1 and beX[j]) or (s == -1 and buX[j]): break
            if (s == 1 and buX[j]) or (s == -1 and beX[j]): k1 += 1
        k2 = 0
        for j in range(i + 1, min(i + 200, n)):
            if (s == 1 and buX[j]) or (s == -1 and beX[j]): k2 += 1
            else: break
        p1 = s * (c[i + 1] - c[i]); p5 = s * (c[i + 5] - c[i]); p10 = s * (c[i + 10] - c[i])
        for sl in range(2):
            if (sMask[q] >> sl) & 1:
                a = out[sd, sPer[q], sl]
                a[0] += 1; a[1] += k1; a[2] += k2; a[3] += p1; a[4] += p5; a[5] += p10; a[6] += p5 * p5; a[7] += p10 * p10; a[8] += 1.0 if p5 > 0 else 0.0
    return 0
