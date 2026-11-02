"""MMM Body Flip Trend engine v2 (Nov 2 2026) - mirrors the CURRENT Pine logic (numba).
Candles: BuBC = green close above prior high, BeBC = red close below prior low, else NBC.
Flip (CDS / CDL): C1 = 1st opposite BC (boundary = body, no close past it or cancel). C2 = next same-side BC with body >= 50% of C1
  (smaller = new C1). OPEN CHECK: some candle from C1 on must CLOSE beyond the open of the last opposite BC (sticky);
  the flip comes when both happened (a qualified C2 waits = armed).
PO4: highest high (BePO4) / lowest low (BuPO4) from C1 to the flip candle. Touch (wick beyond, close inside) moves it to the wick,
  a close beyond deletes it. Keep 10 (a PO4 whose trend still has a live line is never dropped).
Trend line: starts at the same extreme. Step: a trend-direction BC with body >= the candle before moves it to that candle's wick (tighter only).
  Touch -> moves to the wick. Close beyond -> deleted (next step starts a new one).
ATR line: line candle wick -/+ 0.5 x live ATR(14); same touch / delete / restart rules.
Old lines: at a flip, the old trend's live lines stay (touch moves, close beyond deletes). Keep 20.
CDS / CDL line: TL break (or later ATR break) of the running trend -> the closest BC open beyond the broken line (pending);
  at the flip it becomes the CDS / CDL line; no break -> open of the last opposite BC.
EVENTS (per bar, after the close): flip, TL touch / break, ATR touch / break, PO4 touch / break, old-line touch / break."""
import numpy as np
from numba import njit

NPO = 64
NOLD = 20


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
def run(o, h, l, c, atr, c2pct, atrK, openChk, keepPo, keepOld):
    n = len(c)
    trendA = np.zeros(n, np.int8); tlA = np.full(n, np.nan); atA = np.full(n, np.nan)
    poBu = np.full(n, np.nan); poBe = np.full(n, np.nan)
    # events: kind codes 1 flip, 2 TL touch, 3 TL break, 4 ATR touch, 5 ATR break, 6 PO4 touch, 7 PO4 break, 8 old TL touch, 9 old ATR touch
    cap = n * 3 + 100
    eI = np.zeros(cap, np.int64); eK = np.zeros(cap, np.int8); eS = np.zeros(cap, np.int8)
    eRef = np.full(cap, np.nan); eWk = np.full(cap, np.nan); eX1 = np.full(cap, np.nan); eX2 = np.full(cap, np.nan)
    ne = 0
    # PO4 list
    pLv = np.zeros(NPO); pSd = np.zeros(NPO, np.int8); pTr = np.zeros(NPO, np.int64); pn = 0
    # old lines
    oLv = np.zeros(NOLD); oSd = np.zeros(NOLD, np.int8); oAt = np.zeros(NOLD, np.bool_); oTr = np.zeros(NOLD, np.int64); on_ = 0
    # body closes for the CDS line
    tr = 0; curTr = 0; trStart = 0
    setOn = False; setSide = 0; setBody = 0.0; setBnd = 0.0; setAtr = np.nan; setBar = 0
    armed = False; oppDone = False
    lnB = np.nan; lnW = np.nan
    tlOn = False; tlLv = np.nan
    atOn = False; atBase = np.nan; atAtr = np.nan; atTch = np.nan; atLvP = np.nan
    pbLv = np.nan; pbSd = 0; pbRk = 0
    lastBuxO = np.nan; lastBexO = np.nan
    for i in range(1, n):
        isBu = c[i] > h[i - 1] and c[i] > o[i]
        isBe = c[i] < l[i - 1] and c[i] < o[i]
        body = abs(c[i] - o[i]); bTop = max(o[i], c[i]); bBot = min(o[i], c[i])
        a = atr[i]
        # PO4 list: close beyond deletes, touch moves to the wick
        k = pn - 1
        while k >= 0:
            sd = pSd[k]
            if (sd == -1 and c[i] > pLv[k]) or (sd == 1 and c[i] < pLv[k]):
                if ne < cap:
                    eI[ne] = i; eK[ne] = 7; eS[ne] = -sd; eRef[ne] = pLv[k]; eWk[ne] = h[i] if sd == -1 else l[i]; ne += 1
                for m in range(k, pn - 1):
                    pLv[m] = pLv[m + 1]; pSd[m] = pSd[m + 1]; pTr[m] = pTr[m + 1]
                pn -= 1
            elif (sd == -1 and h[i] > pLv[k]) or (sd == 1 and l[i] < pLv[k]):
                if ne < cap:
                    eI[ne] = i; eK[ne] = 6; eS[ne] = sd; eRef[ne] = pLv[k]; eWk[ne] = h[i] if sd == -1 else l[i]; ne += 1
                pLv[k] = h[i] if sd == -1 else l[i]
            k -= 1
        flipped = False
        if tr == 0:
            if isBu or isBe:
                tr = 1 if isBu else -1
                trStart = i
                lnB = bBot if isBu else bTop; lnW = l[i] if isBu else h[i]
                tlLv = lnW; tlOn = True
                atBase = lnW; atAtr = a; atTch = np.nan; atOn = True
        else:
            # old lines
            k = on_ - 1
            while k >= 0:
                sd = oSd[k]
                if (sd == 1 and c[i] < oLv[k]) or (sd == -1 and c[i] > oLv[k]):
                    for m in range(k, on_ - 1):
                        oLv[m] = oLv[m + 1]; oSd[m] = oSd[m + 1]; oAt[m] = oAt[m + 1]; oTr[m] = oTr[m + 1]
                    on_ -= 1
                elif (sd == 1 and l[i] < oLv[k]) or (sd == -1 and h[i] > oLv[k]):
                    if ne < cap:
                        eI[ne] = i; eK[ne] = 9 if oAt[k] else 8; eS[ne] = sd; eRef[ne] = oLv[k]; eWk[ne] = l[i] if sd == 1 else h[i]; ne += 1
                    oLv[k] = l[i] if sd == 1 else h[i]
                k -= 1
            tlDel = False; atDel = False; tlBrk = np.nan; atBrk = np.nan
            if tlOn:
                if (tr == 1 and c[i] < tlLv) or (tr == -1 and c[i] > tlLv):
                    tlBrk = tlLv; tlOn = False; lnB = np.nan; lnW = np.nan; tlDel = True
                    if ne < cap:
                        eI[ne] = i; eK[ne] = 3; eS[ne] = -tr; eRef[ne] = tlBrk; eWk[ne] = h[i] if tr == 1 else l[i]; ne += 1
                elif (tr == 1 and l[i] < tlLv) or (tr == -1 and h[i] > tlLv):
                    if ne < cap:
                        eI[ne] = i; eK[ne] = 2; eS[ne] = tr; eRef[ne] = tlLv; eWk[ne] = l[i] if tr == 1 else h[i]; ne += 1
                    tlLv = l[i] if tr == 1 else h[i]
            if atOn and atLvP == atLvP:
                if (tr == 1 and c[i] < atLvP) or (tr == -1 and c[i] > atLvP):
                    atBrk = atLvP; atOn = False; atDel = True
                    if ne < cap:
                        eI[ne] = i; eK[ne] = 5; eS[ne] = -tr; eRef[ne] = atBrk; eWk[ne] = h[i] if tr == 1 else l[i]; ne += 1
                elif (tr == 1 and l[i] < atLvP) or (tr == -1 and h[i] > atLvP):
                    if ne < cap:
                        eI[ne] = i; eK[ne] = 4; eS[ne] = tr; eRef[ne] = atLvP; eWk[ne] = l[i] if tr == 1 else h[i]; ne += 1
                    atTch = l[i] if tr == 1 else h[i]
            # pending CDS / CDL line
            if pbLv == pbLv and ((pbSd == -1 and c[i] > pbLv) or (pbSd == 1 and c[i] < pbLv)):
                pbLv = np.nan; pbRk = 0
            if atDel or (tlDel and pbRk < 2):
                ref = atBrk if atDel else tlBrk
                side = -tr
                bv = np.nan
                lb = min(min(400, i - 1), max(i - trStart, 1))
                for kk in range(1, lb + 1):
                    j = i - kk
                    if j < 1: break
                    if side == -1:
                        isBc = c[j] > h[j - 1] and c[j] > o[j]
                    else:
                        isBc = c[j] < l[j - 1] and c[j] < o[j]
                    if isBc:
                        lv = o[j]
                        if (side == -1 and lv > ref and c[i] < lv) or (side == 1 and lv < ref and c[i] > lv):
                            if bv != bv or (side == -1 and lv < bv) or (side == 1 and lv > bv):
                                bv = lv
                if bv != bv: bv = ref
                pbLv = bv; pbSd = side; pbRk = 2 if atDel else 1
            cancelled = False; small = False
            if setOn:
                cancel = (setSide == -1 and c[i] > setBnd) or (setSide == 1 and c[i] < setBnd)
                same = isBe if setSide == -1 else isBu
                qual = same and body >= setBody * c2pct / 100.0
                oppO = lastBuxO if setSide == -1 else lastBexO
                if (not cancel) and (not oppDone) and oppO == oppO and ((setSide == -1 and c[i] < oppO) or (setSide == 1 and c[i] > oppO)):
                    oppDone = True
                beyond = (not openChk) or oppO != oppO or oppDone
                if cancel:
                    setOn = False; armed = False; oppDone = False; cancelled = True
                elif qual and (not beyond) and (not armed):
                    armed = True
                elif (qual or armed) and beyond:
                    wasArmed = armed and not qual
                    armed = False; oppDone = False
                    # keep the old trend's live lines
                    if tlOn:
                        if on_ == NOLD or on_ >= keepOld:
                            for m in range(0, on_ - 1):
                                oLv[m] = oLv[m + 1]; oSd[m] = oSd[m + 1]; oAt[m] = oAt[m + 1]; oTr[m] = oTr[m + 1]
                            on_ -= 1
                        oLv[on_] = tlLv; oSd[on_] = tr; oAt[on_] = False; oTr[on_] = curTr; on_ += 1
                    if atOn and atLvP == atLvP:
                        if on_ == NOLD or on_ >= keepOld:
                            for m in range(0, on_ - 1):
                                oLv[m] = oLv[m + 1]; oSd[m] = oSd[m + 1]; oAt[m] = oAt[m + 1]; oTr[m] = oTr[m + 1]
                            on_ -= 1
                        oLv[on_] = atLvP; oSd[on_] = tr; oAt[on_] = True; oTr[on_] = curTr; on_ += 1
                    tr = setSide; curTr += 1; trStart = setBar
                    exW = np.nan; exB = np.nan
                    for j in range(setBar, i + 1):
                        vw = h[j] if tr == -1 else l[j]
                        vb = max(o[j], c[j]) if tr == -1 else min(o[j], c[j])
                        if exW != exW or (tr == -1 and vw > exW) or (tr == 1 and vw < exW): exW = vw
                        if exB != exB or (tr == -1 and vb > exB) or (tr == 1 and vb < exB): exB = vb
                    lnB = exB; lnW = exW
                    tlLv = exW; tlOn = True
                    atBase = exW; atAtr = setAtr; atTch = np.nan; atOn = True
                    setOn = False; flipped = True
                    # CDS / CDL line level
                    if pbLv == pbLv and pbSd == tr:
                        cdsLv = pbLv
                    else:
                        cdsLv = lastBuxO if tr == -1 else lastBexO
                        if cdsLv != cdsLv: cdsLv = o[i]
                    pbLv = np.nan; pbRk = 0
                    # PO4 (wick extreme from C1 to here)
                    poPx = exW
                    if pn == NPO:
                        for m in range(0, pn - 1):
                            pLv[m] = pLv[m + 1]; pSd[m] = pSd[m + 1]; pTr[m] = pTr[m + 1]
                        pn -= 1
                    pLv[pn] = poPx; pSd[pn] = tr; pTr[pn] = curTr; pn += 1
                    while pn > keepPo:
                        drop = -1
                        for m in range(pn):
                            live = pTr[m] == curTr
                            if not live:
                                for q in range(on_):
                                    if oTr[q] == pTr[m]:
                                        live = True; break
                            if not live:
                                drop = m; break
                        if drop < 0: break
                        for m in range(drop, pn - 1):
                            pLv[m] = pLv[m + 1]; pSd[m] = pSd[m + 1]; pTr[m] = pTr[m + 1]
                        pn -= 1
                    if ne < cap:
                        eI[ne] = i; eK[ne] = 1; eS[ne] = tr; eRef[ne] = cdsLv; eWk[ne] = poPx; eX1[ne] = setBody; eX2[ne] = 1.0 if wasArmed else 0.0; ne += 1
                elif same and not armed:
                    setOn = False; small = True   # too small: becomes the new C1 below (keeps the open check)
            # step
            if not flipped:
                dirOk = isBu if tr == 1 else isBe
                bprev = abs(c[i - 1] - o[i - 1])
                if dirOk and body > 0 and body >= bprev:
                    candB = min(o[i - 1], c[i - 1]) if tr == 1 else max(o[i - 1], c[i - 1])
                    candW = l[i - 1] if tr == 1 else h[i - 1]
                    cur = lnW
                    if cur != cur or (tr == 1 and candW > cur) or (tr == -1 and candW < cur):
                        lnB = candB; lnW = candW
                        if not tlOn:
                            tlOn = True; tlLv = candW
                        elif (tr == 1 and candW > tlLv) or (tr == -1 and candW < tlLv):
                            tlLv = candW
                        nb = candW
                        nLv = nb - tr * a * atrK
                        curLv = np.nan
                        if atBase == atBase and a == a:
                            curLv = atBase - tr * a * atrK
                            if atTch == atTch:
                                curLv = min(curLv, atTch) if tr == 1 else max(curLv, atTch)
                        if not atOn:
                            atOn = True; atBase = nb; atAtr = atr[i - 1]; atTch = np.nan
                        elif curLv != curLv or (tr == 1 and nLv > curLv) or (tr == -1 and nLv < curLv):
                            atBase = nb; atAtr = atr[i - 1]; atTch = np.nan
            # new C1
            opp = isBe if tr == 1 else isBu
            if (not setOn) and (not flipped) and (not cancelled) and opp:
                oppC1 = lastBuxO if tr == 1 else lastBexO
                c1Brk = oppC1 == oppC1 and ((tr == 1 and c[i] < oppC1) or (tr == -1 and c[i] > oppC1))
                oppDone = (small and oppDone) or c1Brk
                setOn = True; setSide = -tr; setBody = body
                setBnd = bTop if setSide == -1 else bBot
                setAtr = a; setBar = i
        # ATR level after this candle
        if atOn and tr != 0:
            lv = np.nan
            if atBase == atBase and a == a:
                lv = atBase - tr * a * atrK
                if atTch == atTch:
                    lv = min(lv, atTch) if tr == 1 else max(lv, atTch)
            atLvP = lv
        else:
            atLvP = np.nan
        if isBu: lastBuxO = o[i]
        if isBe: lastBexO = o[i]
        trendA[i] = tr
        tlA[i] = tlLv if tlOn else np.nan
        atA[i] = atLvP
        for m in range(pn):
            if pSd[m] == 1: poBu[i] = pLv[m]
            else: poBe[i] = pLv[m]
    return trendA, tlA, atA, poBu, poBe, eI[:ne], eK[:ne], eS[:ne], eRef[:ne], eWk[:ne], eX1[:ne], eX2[:ne]


KN = {1: 'FLIP (CDS / CDL)', 2: 'TL touch-hold', 3: 'TL break', 4: 'ATR touch-hold', 5: 'ATR break', 6: 'PO4 touch-hold', 7: 'PO4 break',
      8: 'old TL touch-hold', 9: 'old ATR touch-hold'}


def signals(df, c2pct=50.0, atrK=0.5, openChk=True, atrLen=14):
    o = df.open.values.astype(np.float64); h = df.high.values.astype(np.float64)
    l = df.low.values.astype(np.float64); c = df.close.values.astype(np.float64)
    atr = atr_rma(h, l, c, atrLen)
    r = run(o, h, l, c, atr, float(c2pct), float(atrK), bool(openChk), 10, 20)
    keys = ['trend', 'tl', 'at', 'poBu', 'poBe', 'eI', 'eK', 'eS', 'eRef', 'eWk', 'eX1', 'eX2']
    S = dict(zip(keys, r)); S.update(o=o, h=h, l=l, c=c, atr=atr)
    return S
