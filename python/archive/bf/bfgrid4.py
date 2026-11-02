"""Test 4: Max's trade management (Nov 2 2026). Always: one trade at a time + exit at the close of the next opposite flip (new C2).
MODES  0 no BE · then BE = entry + 1 fee or + 2 fees, set when a body close in our direction closes past that level, then trail:
       none / Body Flip trend line / wick of each new BC / open of each new BC   -> 1 + 2 x 4 = 9 modes
OLD DOC BELOW (test 3) for the rest.
Test 3: trade-management rules on the Body Flip CDS / CDL retest (Nov 2 2026).
RULES TESTED
  BE    move the stop to entry + cost (no loss) once the trade is in profit by 0.25R / 0.5R / 1R  (or never)
  ONE   one trade at a time: a new signal is skipped while a trade is open (always on in this test)
  CX    exit at the close if a candle closes back beyond: C2 open · C2 wick · C1 open · C1 wick (PO4)  (or never)
ENTRIES 0 market C2 close · 1-7 last C1 range 0/12.5/25/50/75/87.5/100% · 8-14 C2 range (same). Limits live 10 candles.
STOPS   0 PO4 last C1 wick · 1 PO4 strongest C1 wick · 2-5 ATR trailing x0.5/1/1.5/2 · 6-9 fixed NQ 20/40/50/60 (scaled on other markets)
TARGETS 1:2 1:3 1:4 1:5 1:6 none   EXITS 0 stop/target only · 1 also at the next opposite flip
Graded on chart candles, stop first on a tie, BE starts the candle after it is earned, limits fill 1 tick through,
cost per trade, 100-candle limit. Sequences: side both / long only / short only x window all hours / 09:45-12:00 (6 traders)."""
import numpy as np
from numba import njit

LEV = np.array([0.0, 0.125, 0.25, 0.5, 0.75, 0.875, 1.0])
KST = np.array([0.5, 1.0, 1.5, 2.0])
KFX = np.array([0.4, 0.8, 1.0, 1.2])
TGT = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 1e9])
NE, NST, NT, NB, NC = 15, 10, 6, 9, 5
NX = 1
NV = NT * NB * NC
NK = 6   # exit kinds: 0 stop at a loss, 1 stop at 0 or better (BE / trail), 2 target, 3 next flip, 4 close exit, 5 time limit
LN = ['0%', '12.5%', '25%', '50%', '75%', '87.5%', '100%']
EN = ['market C2 close'] + [f'limit last C1 range {x}' for x in LN] + [f'limit C2 range {x}' for x in LN]
SN = ['PO4 last C1 wick', 'PO4 strongest C1 wick', 'ATR x0.5 trailing', 'ATR x1 trailing', 'ATR x1.5 trailing', 'ATR x2 trailing',
      'fixed 20 pts', 'fixed 40 pts', 'fixed 50 pts', 'fixed 60 pts']
TN = ['1:2', '1:3', '1:4', '1:5', '1:6', 'no target']
BN = ['no BE'] + [f'BE +{k} fee{"s" if k > 1 else ""}, {tr}' for k in (1, 2) for tr in ('no trail', 'trail trend line', 'trail BC wick', 'trail BC open')]
KN = ['stop at a loss', 'stop at 0 or better', 'target', 'next flip', 'close exit', 'time limit']
CN = ['no close exit', 'close past C2 open', 'close past C2 wick', 'close past C1 open', 'close past C1 wick']
SEQ = ['both', 'long', 'short']


@njit(cache=True)
def _line(trend, lnW, atr, j, s, k):
    if j < 0 or trend[j] != s or lnW[j] != lnW[j] or atr[j] != atr[j]: return np.nan
    return lnW[j] - s * k * atr[j]


@njit(cache=True)
def grade(o, h, l, c, trend, lnW, atr, flipUp, flipDn, buX, beX,
          sI, sS, sC1, sPO, sSPO, sMask, sPer, s50, cost, tick, HOLD, WAIT, acc, busy):
    """acc[seq(3), per, slot(2), e, st, v(NV), 6 + 2 * NK] (exit-kind counts, then exit-kind R sums). v = (ti * NB + bi) * NC + ci. busy[seq, slot, e, st, v] = exit candle of the open trade."""
    n = len(c)
    minr = 0.08 * s50
    tT = np.empty(NT, np.int64)
    stK = np.empty(NB); tS = np.empty(NB, np.int64); pS = np.empty(NB); trig = np.zeros(NB, np.bool_)
    tC = np.empty(NC - 1, np.int64); LC = np.empty(NC - 1)
    exB = np.empty(NV, np.int64); rv = np.empty(NV); kv = np.empty(NV, np.int64)
    for q in range(len(sI)):
        i = sI[q]; s = sS[q]; per = sPer[q]; mask = sMask[q]
        if i + 2 >= n: continue
        sq2 = 1 if s == 1 else 2
        b1 = sC1[q]
        if s == 1:
            LC[0] = o[i]; LC[1] = l[i]; LC[2] = o[b1]; LC[3] = l[b1]
        else:
            LC[0] = o[i]; LC[1] = h[i]; LC[2] = o[b1]; LC[3] = h[b1]
        for e in range(NE):
            if e == 0:
                px = c[i]
            else:
                g = (e - 1) // 7; f = LEV[(e - 1) % 7]
                b = b1 if g == 0 else i
                if s == 1: px = h[b] - f * (h[b] - l[b])
                else: px = l[b] + f * (h[b] - l[b])
                px = np.round(px / tick) * tick
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
                free = False
                for sqm in range(3):
                    if sqm != 0 and sqm != sq2: continue
                    for sl in range(2):
                        if not ((mask >> sl) & 1): continue
                        for v in range(NV):
                            bz = busy[sqm, sl, e, st, v]
                            if kf > bz or (e == 0 and kf >= bz):
                                free = True; break
                        if free: break
                    if free: break
                if not free: continue
                if st == 0: stop = sPO[q]
                elif st == 1: stop = sSPO[q]
                elif st >= 6: stop = ep - s * KFX[st - 6] * s50
                else: stop = _line(trend, lnW, atr, kf if e == 0 else kf - 1, s, KST[st - 2])
                if stop != stop: continue
                risk = s * (ep - stop)
                if not (risk >= minr): continue
                lim = min(kf + HOLD, n - 1)
                base = stop
                for k in range(NB):
                    stK[k] = stop; tS[k] = -1; pS[k] = 0.0; trig[k] = False
                for k in range(NT): tT[k] = -1
                for k in range(NC - 1): tC[k] = -1
                tF = -1; pF = 0.0
                nst = 0
                if e > 0:
                    if (s == 1 and l[kf] <= stop) or (s == -1 and h[kf] >= stop):
                        for k in range(NB):
                            tS[k] = kf; pS[k] = stop
                        nst = NB
                    else:
                        for k in range(NC - 1):
                            if s * (c[kf] - LC[k]) < 0: tC[k] = kf
                        if (s == 1 and flipDn[kf]) or (s == -1 and flipUp[kf]):
                            tF = kf; pF = c[kf]
                if nst < NB:
                    for j in range(kf + 1, lim + 1):
                        if st >= 2 and st <= 5:
                            ln = _line(trend, lnW, atr, j - 1, s, KST[st - 2])
                            if ln == ln:
                                base = max(base, ln) if s == 1 else min(base, ln)
                        # stop check with the stop known before this candle
                        for k in range(NB):
                            if tS[k] >= 0: continue
                            sk = base
                            if k > 0 and trig[k]:
                                sk = max(stK[k], base) if s == 1 else min(stK[k], base)
                            stK[k] = sk
                            if (s == 1 and l[j] <= sk) or (s == -1 and h[j] >= sk):
                                tS[k] = j; pS[k] = min(o[j], sk) if s == 1 else max(o[j], sk); nst += 1
                        if nst >= NB: break
                        fav = h[j] - ep if s == 1 else ep - l[j]
                        for k in range(NT - 1):
                            if tT[k] < 0 and fav >= TGT[k] * risk: tT[k] = j
                        if tF < 0 and ((s == 1 and flipDn[j]) or (s == -1 and flipUp[j])):
                            tF = j; pF = c[j]
                        for k in range(NC - 1):
                            if tC[k] < 0 and s * (c[j] - LC[k]) < 0: tC[k] = j
                        # at the close: BE set by a body close in our direction past entry + fees, then trail (used from the next candle)
                        bcUs = buX[j] if s == 1 else beX[j]
                        for k in range(1, NB):
                            if tS[k] >= 0: continue
                            fees = 1.0 if k <= 4 else 2.0
                            tr = (k - 1) % 4
                            bel = ep + s * fees * max(cost, tick)
                            if not trig[k]:
                                if bcUs and s * (c[j] - bel) > 0:
                                    trig[k] = True
                                    stK[k] = max(stK[k], bel) if s == 1 else min(stK[k], bel)
                                else:
                                    continue
                            # trail (also on the BE candle itself)
                            if tr == 1:
                                if trend[j] == s and lnW[j] == lnW[j]:
                                    stK[k] = max(stK[k], lnW[j]) if s == 1 else min(stK[k], lnW[j])
                            elif tr == 2 and bcUs:
                                stK[k] = max(stK[k], l[j]) if s == 1 else min(stK[k], h[j])
                            elif tr == 3 and bcUs:
                                stK[k] = max(stK[k], o[j]) if s == 1 else min(stK[k], o[j])
                # resolve every variant (flip exit always on)
                v = 0
                for ti in range(NT):
                    for bi in range(NB):
                        for ci in range(NC):
                            jE = tS[bi] if tS[bi] >= 0 else lim
                            best = (jE + 1) * 4 + 3; bp = c[jE]; kd = 5
                            if tS[bi] >= 0:
                                best = tS[bi] * 4 + 1; bp = pS[bi]; kd = 0
                            if ti < NT - 1 and tT[ti] >= 0 and tT[ti] * 4 + 2 < best:
                                best = tT[ti] * 4 + 2; bp = ep + s * TGT[ti] * risk; kd = 2
                            if tF >= 0 and tF * 4 + 3 < best:
                                best = tF * 4 + 3; bp = pF; kd = 3
                            if ci > 0 and tC[ci - 1] >= 0 and tC[ci - 1] * 4 + 3 < best:
                                best = tC[ci - 1] * 4 + 3; bp = c[tC[ci - 1]]; kd = 4
                            xb = best // 4
                            if xb > lim: xb = lim
                            exB[v] = xb
                            rv[v] = (s * (bp - ep) - cost) / risk
                            if kd == 0 and rv[v] >= -1e-9: kd = 1
                            kv[v] = kd
                            v += 1
                for sqm in range(3):
                    if sqm != 0 and sqm != sq2: continue
                    for sl in range(2):
                        if not ((mask >> sl) & 1): continue
                        for v in range(NV):
                            bz = busy[sqm, sl, e, st, v]
                            if kf > bz or (e == 0 and kf >= bz):
                                busy[sqm, sl, e, st, v] = exB[v]
                                x = rv[v]
                                a = acc[sqm, per, sl, e, st, v]
                                a[0] += 1.0; a[2] += x; a[3] += x * x
                                if x > 0:
                                    a[1] += 1.0; a[4] += x
                                else:
                                    a[5] -= x
                                a[6 + kv[v]] += 1.0
                                a[6 + NK + kv[v]] += x
    return 0
