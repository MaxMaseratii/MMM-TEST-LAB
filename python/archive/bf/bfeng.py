"""MMM Body Flip Trend engine, mirrored from the Pine (Nov 2 2026), numba.
BuBC = green close above the prior high. BeBC = red close below the prior low. Everything else = NBC.
C1 = 1st opposite body close (sets boundary + size to beat). C2 = next same-side body close with body >= c2pct% of C1
(+ delta check if on) = CDS / CDL. A too-small one becomes the new C1. A close beyond the boundary cancels (✕).
Trend line: starts at C1 at the flip; a body close in the trend direction with body >= step% of the candle before
moves the line to that candle (only tighter). ATR stop line = trend-line candle wick +/- k * ATR."""
import numpy as np
from numba import njit


@njit(cache=True)
def atr_rma(h, l, c, n):
    m = len(c); a = np.full(m, np.nan)
    if m < n: return a
    tr = np.empty(m); tr[0] = h[0] - l[0]
    for i in range(1, m):
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
    s = 0.0
    for i in range(n): s += tr[i]
    a[n - 1] = s / n
    for i in range(n, m):
        a[i] = (a[i - 1] * (n - 1) + tr[i]) / n
    return a


@njit(cache=True)
def run(o, h, l, c, dl, atr, c2pct, bndWick, maxWait, dOn, dPct, stepPct, stepBC, lvlWick, cap):
    n = len(c)
    trend = np.zeros(n, np.int8)
    lnB = np.full(n, np.nan); lnW = np.full(n, np.nan); lnA = np.full(n, np.nan)
    # flip events
    fI = np.full(n, -1, np.int64); fS = np.zeros(n, np.int8); fC1 = np.full(n, -1, np.int64)
    fB1 = np.zeros(n); fB2 = np.zeros(n); fD1 = np.full(n, np.nan); fD2 = np.full(n, np.nan)
    fW1 = np.zeros(n); fL1 = np.zeros(n); fSW = np.zeros(n); fSL = np.zeros(n); fSB = np.zeros(n); fSI = np.zeros(n, np.int64); fLine = np.full(n, np.nan); fRes = np.zeros(n, np.int64); fBig = np.zeros(n, np.int8)
    nf = 0
    # cancel events
    xI = np.full(n, -1, np.int64); xS = np.zeros(n, np.int8); nx = 0
    # C1 registry per side (biggest not beaten)
    rb = np.zeros((2, cap)); ri = np.zeros((2, cap), np.int64); rd = np.full((2, cap), np.nan); rn = np.zeros(2, np.int64)
    tr = 0; setOn = False; setSide = 0; setBody = 0.0; setD = np.nan; setBnd = 0.0; setLB = 0.0; setLW = 0.0; setA = np.nan; setBar = 0
    resets = 0
    stB = 0.0; stW = 0.0; stL = 0.0; stI = 0
    lB = np.nan; lW = np.nan; lA = np.nan
    lastBuxO = np.nan; lastBexO = np.nan
    for i in range(1, n):
        buX = c[i] > h[i - 1] and c[i] > o[i]
        beX = c[i] < l[i - 1] and c[i] < o[i]
        body = abs(c[i] - o[i]); bTop = max(o[i], c[i]); bBot = min(o[i], c[i])
        d = dl[i]
        # biggest unbeaten C1 per side, before this candle beats any
        bigB = np.zeros(2)
        for sd in range(2):
            mx = 0.0
            for k in range(rn[sd]):
                if rb[sd, k] > mx: mx = rb[sd, k]
            bigB[sd] = mx
        # beat registry
        for sd in range(2):
            side = -1 if sd == 0 else 1
            bc = beX if side == -1 else buX
            if bc and rn[sd] > 0:
                k = 0
                while k < rn[sd]:
                    dref = rd[sd, k]
                    dgood = (not dOn) or d != d or dref != dref or (d * side > 0 and abs(d) >= abs(dref) * dPct / 100.0)
                    if ri[sd, k] < i and body >= rb[sd, k] * c2pct / 100.0 and dgood:
                        for q in range(k, rn[sd] - 1):
                            rb[sd, q] = rb[sd, q + 1]; ri[sd, q] = ri[sd, q + 1]; rd[sd, q] = rd[sd, q + 1]
                        rn[sd] -= 1
                    else:
                        k += 1
        ev = 0
        if tr == 0:
            if buX or beX:
                tr = 1 if buX else -1
                lB = bBot if buX else bTop
                lW = l[i] if buX else h[i]
                lA = atr[i]
        else:
            flipped = False
            if setOn:
                cancel = c[i] > setBnd if setSide == -1 else c[i] < setBnd
                same = beX if setSide == -1 else buX
                dok = (not dOn) or d != d or setD != setD or (d * setSide > 0 and abs(d) >= abs(setD) * dPct / 100.0)
                if cancel:
                    setOn = False; ev = 3
                    xI[nx] = i; xS[nx] = setSide; nx += 1
                elif same and body >= setBody * c2pct / 100.0 and dok:
                    sdi = 0 if setSide == -1 else 1
                    fI[nf] = i; fS[nf] = setSide; fC1[nf] = setBar; fB1[nf] = setBody; fB2[nf] = body
                    fD1[nf] = setD; fD2[nf] = d; fW1[nf] = setLW; fL1[nf] = setLB
                    fLine[nf] = lastBuxO if setSide == -1 else lastBexO
                    fRes[nf] = resets
                    fSW[nf] = stW; fSL[nf] = stL; fSB[nf] = stB; fSI[nf] = stI
                    fBig[nf] = 1 if (bigB[sdi] > setBody and body >= bigB[sdi] * c2pct / 100.0) else 0
                    nf += 1
                    tr = setSide; lB = setLB; lW = setLW; lA = setA
                    setOn = False; flipped = True; ev = 2
                elif maxWait > 0 and i - setBar >= maxWait:
                    setOn = False; ev = 4
                elif same:
                    setOn = False; ev = 5
            if (not flipped) and lB == lB:
                if stepBC:
                    dirOk = buX if tr == 1 else beX
                else:
                    dirOk = c[i] > o[i] if tr == 1 else c[i] < o[i]
                pb = abs(c[i - 1] - o[i - 1])
                if dirOk and body > 0 and body >= pb * stepPct / 100.0:
                    cB = min(o[i - 1], c[i - 1]) if tr == 1 else max(o[i - 1], c[i - 1])
                    cW = l[i - 1] if tr == 1 else h[i - 1]
                    # tighter by the shown level (wick by default: compare wicks)
                    cur = lW if lvlWick else lB
                    cand = cW if lvlWick else cB
                    if (tr == 1 and cand > cur) or (tr == -1 and cand < cur):
                        lB = cB; lW = cW; lA = atr[i - 1]
            opp = beX if tr == 1 else buX
            if (not setOn) and (not flipped) and ev != 3 and opp:
                if ev == 5: resets += 1
                else: resets = 0
                setOn = True; setSide = -tr; setBody = body; setD = d
                if setSide == -1:
                    setBnd = h[i] if bndWick else bTop
                    setLB = bTop; setLW = h[i]
                else:
                    setBnd = l[i] if bndWick else bBot
                    setLB = bBot; setLW = l[i]
                setA = atr[i]; setBar = i
                # strongest C1 of the chain (biggest body among C1s that replaced each other)
                if ev != 5 or body > stB:
                    stB = body; stW = setLW; stL = setLB; stI = i
                sd = 0 if setSide == -1 else 1
                if rn[sd] >= cap:
                    for q in range(cap - 1):
                        rb[sd, q] = rb[sd, q + 1]; ri[sd, q] = ri[sd, q + 1]; rd[sd, q] = rd[sd, q + 1]
                    rn[sd] -= 1
                rb[sd, rn[sd]] = body; ri[sd, rn[sd]] = i; rd[sd, rn[sd]] = d; rn[sd] += 1
        if buX: lastBuxO = o[i]
        if beX: lastBexO = o[i]
        trend[i] = tr; lnB[i] = lB; lnW[i] = lW; lnA[i] = lA
    return (trend, lnB, lnW, lnA, fI[:nf], fS[:nf], fC1[:nf], fB1[:nf], fB2[:nf], fD1[:nf], fD2[:nf], fW1[:nf], fL1[:nf],
            fLine[:nf], fRes[:nf], fBig[:nf], xI[:nx], xS[:nx], fSW[:nf], fSL[:nf], fSB[:nf], fSI[:nf])


def signals(df, c2pct=50.0, bndWick=False, maxWait=0, dOn=False, dPct=50.0, stepPct=100.0, stepBC=True, atrLen=14, lvlWick=True):
    o = df.open.values.astype(np.float64); h = df.high.values.astype(np.float64)
    l = df.low.values.astype(np.float64); c = df.close.values.astype(np.float64)
    dl = df.delta.values.astype(np.float64)
    atr = atr_rma(h, l, c, atrLen)
    r = run(o, h, l, c, dl, atr, float(c2pct), bool(bndWick), int(maxWait), bool(dOn), float(dPct), float(stepPct), bool(stepBC), bool(lvlWick), 150)
    keys = ['trend', 'lnB', 'lnW', 'lnA', 'fI', 'fS', 'fC1', 'fB1', 'fB2', 'fD1', 'fD2', 'fW1', 'fL1', 'fLine', 'fRes', 'fBig', 'xI', 'xS', 'fSW', 'fSL', 'fSB', 'fSI']
    S = dict(zip(keys, r))
    S.update(o=o, h=h, l=l, c=c, atr=atr, dl=dl)
    return S
