"""Signals (setups) for the 18 MMM EDGE PRO strategies (X.M1-X.M5, C.M1-C.M8, XCS.M1-XCS.M5).

Port of the MMM EDGE PRO Pine (15m core: zone engine x expander + contraction, candle engine c, swing engine s,
GMC / AFs / BC+ patterns, daily + 1h filters, Asia / NY AM windows, XCS combos, XCS.M5 iBlocks) plus the
book rules for the strategies that only live in the Oct 28 build (X.M3 5m iBlock, XCS.M3/M4 4H GMC AFs filter,
C.M6/C.M7 1m level retest, C.M8 09:30 opening candle).
Old -> new codes: EP.M1 = X.M4 · EP.M4 = X.M5 · EP.M2 = C.M3 · EP.M3 = C.M4 · EP.M5 = C.M5 · LR.M1/M2 = C.M6/C.M7 · OC.M1 = C.M8.

signals(m) -> one row per setup (filters applied, no one-at-a-time, no sizing).
Columns: strat tf i t side ztop zbot ntype npx nsl nrr nwait note."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/allm')
from mdata import bars, fine, SPEC

NAN = float('nan')
COLS = ['strat', 'tf', 'i', 't', 'side', 'ztop', 'zbot', 'ntype', 'npx', 'nsl', 'nrr', 'nwait', 'note']


def _row(strat, tf, i, t, side, zt, zb, ntype, npx, nsl, nrr, nwait, note):
    return (strat, tf, int(i), t, int(side), float(max(zt, zb)), float(min(zt, zb)), ntype, float(npx), float(nsl),
            float(nrr), int(nwait), note)


# ─────────────────────────────── helpers ───────────────────────────────
def atr_rma(h, l, c, n=14):
    """Pine ta.atr: RMA of the true range, seeded with the SMA of the first n."""
    pc = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    tr[0] = h[0] - l[0]
    out = np.full(len(c), np.nan)
    if len(c) < n:
        return out
    out[n - 1] = tr[:n].mean()
    for k in range(n, len(c)):
        out[k] = (out[k - 1] * (n - 1) + tr[k]) / n
    return out


def mins(ix):
    return (ix.hour * 60 + ix.minute).values


def hit_open(md):
    """Pine f_hitT for the session opens 18:00, 02:00, 08:00, 09:30 (bar whose open first reaches the time)."""
    mdp = np.r_[-1, md[:-1]]
    r = np.zeros(len(md), bool)
    for tm in (1080, 120, 480, 570):
        up = (md > mdp) & (tm > mdp) & (tm <= md)
        wr = (md < mdp) & ((tm > mdp) | (tm <= md))
        r |= (mdp >= 0) & (up | wr)
    return r


def day_dir(d, m):
    """yesterday's CME daily candle direction (sign close - open) for each candle of d (closed D candle only)."""
    D = bars(m, 'D')
    dk = (d.index + pd.Timedelta(hours=6)).normalize() - pd.Timedelta(hours=6)
    pos = np.searchsorted(D.index.values, dk.values, 'left') - 1     # the D candle before the current one
    sg = np.sign(D.close.values - D.open.values)
    out = np.where(pos >= 0, sg[np.clip(pos, 0, None)], 0)
    # the previous D candle must have ended before this candle starts
    ok = (pos >= 0) & (D.tend.values[np.clip(pos, 0, None)] <= d.index.values + np.timedelta64(1, 'm'))
    return np.where(ok, out, 0).astype(int)


def htf_state(d, H, arr):
    """value of arr (per HTF candle, after it closed) at the close of each candle of d."""
    p = np.searchsorted(H.tend.values, d.tend.values, 'right') - 1
    v = np.where(p >= 0, arr[np.clip(p, 0, None)], 0)
    return v


# ─────────────────────────────── zone engine (x) ───────────────────────────────
def zone(o, h, l, c, grow=True, exp=True):
    """Port of f_zoneEngine (gate off). Per candle (after the candle): side, tier, tnP, ev (1 flip / 2 continuation),
    evd, evn (old tier on a continuation), new PO4 ntn and its origin box noh / nol, the broken P# box boh / bol."""
    n = len(c)
    SIDE = np.zeros(n, int); TIER = np.zeros(n, int); TN = np.full(n, NAN)
    EV = np.zeros(n, int); EVD = np.zeros(n, int); EVN = np.zeros(n, int)
    NTN = np.full(n, NAN); NOH = np.full(n, NAN); NOL = np.full(n, NAN); BOH = np.full(n, NAN); BOL = np.full(n, NAN)
    zWait = False; exH = exL = NAN; zLive = False; bxH = bxL = NAN; bxId = 0
    side = 0; tier = 0; tnP = NAN
    pP = NAN; pId = -1; pLive = False; pOH = pOL = NAN
    rP = NAN; rId = -1; rLive = False; rOH = rOL = NAN
    legHi = legHiL = legLo = legLoH = NAN
    pbHi = pbHiL = pbLo = pbLoH = NAN
    isn = np.isnan
    for i in range(1, n):
        hi, lo, cl = h[i], l[i], c[i]
        ph, pl = h[i - 1], l[i - 1]
        bu = cl > ph; be = cl < pl; bc = bu or be
        formed = False; endF = False; endH = endL = NAN
        if zLive:
            if cl > bxH or cl < bxL:
                endF = True; endH = bxH; endL = bxL
                if bxId == pId: pLive = False
                if bxId == rId: rLive = False
                zLive = False; zWait = bc
                if bc: exH = hi; exL = lo
            elif grow:
                bxH = max(bxH, hi); bxL = min(bxL, lo)
        elif zWait:
            if bc:
                exH = hi; exL = lo
            else:
                zLive = True; zWait = False; formed = True; bxId += 1
                if exp:
                    bxH = max(exH, hi) if grow else exH; bxL = min(exL, lo) if grow else exL
                else:
                    bxH = hi; bxL = lo
        elif bc:
            zWait = True; exH = hi; exL = lo
        if zLive and bxId == pId:
            pP = bxH if side == 1 else bxL; pOH = bxH; pOL = bxL
        if zLive and bxId == rId:
            rP = bxL if side == 1 else bxH; rOH = bxH; rOL = bxL
        if side != 0:
            if isn(legHi) or hi > legHi: legHi = hi; legHiL = lo
            if isn(legLo) or lo < legLo: legLo = lo; legLoH = hi
        if not isn(pP):
            if isn(pbHi) or hi > pbHi: pbHi = hi; pbHiL = lo
            if isn(pbLo) or lo < pbLo: pbLo = lo; pbLoH = hi
        ev = 0; evd = 0; evn = 0; ntn = noh = nol = NAN
        if side == 1:
            if cl < tnP:
                ev = 1; evd = -1; hasP = not isn(pP)
                ntn = pP if hasP else legHi; noh = pOH if hasP else legHi; nol = pOL if hasP else legHiL
            elif not isn(pP) and cl > pP:
                ev = 2; evd = 1; evn = tier; BOH[i] = pOH; BOL[i] = pOL; hasR = not isn(rP)
                ntn = rP if hasR else pbLo; noh = rOH if hasR else pbLoH; nol = rOL if hasR else pbLo
            elif not isn(rP) and cl < rP:
                rP = NAN; rId = -1; rLive = False
        elif side == -1:
            if cl > tnP:
                ev = 1; evd = 1; hasP = not isn(pP)
                ntn = pP if hasP else legLo; noh = pOH if hasP else legLoH; nol = pOL if hasP else legLo
            elif not isn(pP) and cl < pP:
                ev = 2; evd = -1; evn = tier; BOH[i] = pOH; BOL[i] = pOL; hasR = not isn(rP)
                ntn = rP if hasR else pbHi; noh = rOH if hasR else pbHi; nol = rOL if hasR else pbHiL
            elif not isn(rP) and cl > rP:
                rP = NAN; rId = -1; rLive = False
        elif endF:
            ev = 1; evd = 1 if cl > endH else -1
            ntn = endL if evd == 1 else endH; noh = endH; nol = endL
        if ev != 0:
            side = evd; tier = 1 if ev == 1 else tier + 1; tnP = ntn
            pP = NAN; pId = -1; pLive = False; rP = NAN; rId = -1; rLive = False
            legHi = hi; legHiL = lo; legLo = lo; legLoH = hi; pbHi = NAN; pbLo = NAN
        if formed:
            if side != 0 and isn(pP):
                pId = bxId; pLive = True; pP = bxH if side == 1 else bxL; pOH = bxH; pOL = bxL
                pbHi = bxH; pbHiL = bxL; pbLo = bxL; pbLoH = bxH
            elif side != 0 and not pLive and isn(rP):
                rId = bxId; rLive = True; rP = bxL if side == 1 else bxH; rOH = bxH; rOL = bxL
        SIDE[i] = side; TIER[i] = tier; TN[i] = tnP; EV[i] = ev; EVD[i] = evd; EVN[i] = evn
        NTN[i] = ntn; NOH[i] = noh; NOL[i] = nol
    return dict(side=SIDE, tier=TIER, tn=TN, ev=EV, evd=EVD, evn=EVN, ntn=NTN, noh=NOH, nol=NOL, boh=BOH, bol=BOL)


# ─────────────────────────────── candle engine (c) ───────────────────────────────
def cengine(o, h, l, c):
    """Port of f_xsCandle. Per candle: ev, side, tier, tn (PO4), origin box oh / ol, pb, plus for a flip the old PO4
    (break line, brk) and the candle index of the new PO4 (pbi: the first opposite-BC candle, or the flip candle)."""
    n = len(c)
    EV = np.zeros(n, int); SD = np.zeros(n, int); TR = np.zeros(n, int); TN = np.full(n, NAN)
    OH = np.full(n, NAN); OL = np.full(n, NAN); PB = np.full(n, NAN); BRK = np.full(n, NAN); PBI = np.full(n, -1)
    side = 0; tier = 0; tn = NAN; pb = NAN; pbH = pbL = NAN; pbI = -1; rs = NAN; rsH = rsL = NAN
    isn = np.isnan
    for i in range(1, n):
        op, hi, lo, cl = o[i], h[i], l[i], c[i]
        bu = cl > h[i - 1]; be = cl < l[i - 1]
        done = False; ev = 0
        if side == 1:
            if cl < tn:
                BRK[i] = tn; side = -1
                OH[i] = hi if isn(pb) else pbH; OL[i] = lo if isn(pb) else pbL
                PBI[i] = i if isn(pb) else pbI
                tn = op if isn(pb) else pb; pb = NAN; rs = NAN; tier = 1; ev = 1; done = True
            elif not isn(pb) and cl > pb:
                OH[i] = hi if isn(rs) else rsH; OL[i] = lo if isn(rs) else rsL
                tn = op if isn(rs) else rs; pb = NAN; rs = NAN; tier += 1; ev = 2; done = True
        elif side == -1:
            if cl > tn:
                BRK[i] = tn; side = 1
                OH[i] = hi if isn(pb) else pbH; OL[i] = lo if isn(pb) else pbL
                PBI[i] = i if isn(pb) else pbI
                tn = op if isn(pb) else pb; pb = NAN; rs = NAN; tier = 1; ev = 1; done = True
            elif not isn(pb) and cl < pb:
                OH[i] = hi if isn(rs) else rsH; OL[i] = lo if isn(rs) else rsL
                tn = op if isn(rs) else rs; pb = NAN; rs = NAN; tier += 1; ev = 2; done = True
        else:
            if bu or be:
                side = 1 if bu else -1; tn = op; tier = 1; done = True
        if not done:
            if side == 1:
                if not isn(rs) and cl < rs: rs = NAN
                if be and isn(pb):
                    pb = op; pbH = hi; pbL = lo; pbI = i
                elif bu and not isn(pb) and isn(rs):
                    rs = op; rsH = hi; rsL = lo
            elif side == -1:
                if not isn(rs) and cl > rs: rs = NAN
                if bu and isn(pb):
                    pb = op; pbH = hi; pbL = lo; pbI = i
                elif be and not isn(pb) and isn(rs):
                    rs = op; rsH = hi; rsL = lo
        EV[i] = ev; SD[i] = side; TR[i] = tier; TN[i] = tn; PB[i] = pb
    return dict(ev=EV, side=SD, tier=TR, tn=TN, oh=OH, ol=OL, pb=PB, brk=BRK, pbi=PBI)


# ─────────────────────────────── swing engine (s) ───────────────────────────────
def sengine(h, l, c):
    """Port of f_xsSwing. Per candle: ev, evs (side of the event), evt (tier), po, oh, ol, sig (trend side)."""
    n = len(c)
    EV = np.zeros(n, int); ES = np.zeros(n, int); ET = np.zeros(n, int); PO = np.full(n, NAN)
    OH = np.full(n, NAN); OL = np.full(n, NAN); SG = np.zeros(n, int)
    tH = h[0]; tHlo = l[0]; tL = l[0]; tLhi = h[0]; tSt = 0; sig = 0; tier = 0; cdlB = -1; cdsB = -1
    lHi = lHiLo = lLo = lLoHi = NAN
    hs = []; ls = []          # [price, bar]
    for i in range(1, n):
        hi, lo, cl = h[i], l[i], c[i]
        bu = cl > h[i - 1]; be = cl < l[i - 1]
        if tSt == 0:
            if hi > tH: tH = hi; tHlo = lo
            if lo < tL: tL = lo; tLhi = hi
        if tSt == 1 and hi >= tH: tH = hi; tHlo = lo
        if tSt == -1 and lo <= tL: tL = lo; tLhi = hi
        if be and tSt >= 0:
            hs.append([tH, i]); lHi = tH; lHiLo = tHlo; tSt = -1; tL = lo; tLhi = hi
        elif bu and tSt <= 0:
            ls.append([tL, i]); lLo = tL; lLoHi = tLhi; tSt = 1; tH = hi; tHlo = lo
        ev = 0; evS = 0; evT = 0; po = oh = ol = NAN
        lowDone = False
        for k in range(len(ls) - 1, -1, -1):
            p, b = ls[k]
            if b < i and cl < p:
                if not lowDone:
                    flip = sig != -1
                    if flip or b > cdsB:
                        lowDone = True
                        if flip:
                            cdsB = i; tier = 1
                        else:
                            tier += 1
                        ev = 1 if flip else 2; evS = -1; evT = tier; po = lHi; oh = lHi; ol = lHiLo; sig = -1
                del ls[k]
        highDone = False
        for k in range(len(hs) - 1, -1, -1):
            p, b = hs[k]
            if b < i and cl > p:
                if not highDone:
                    flip = sig != 1
                    if flip or b > cdlB:
                        highDone = True
                        if flip:
                            cdlB = i; tier = 1
                        else:
                            tier += 1
                        ev = 1 if flip else 2; evS = 1; evT = tier; po = lLo; oh = lLoHi; ol = lLo; sig = 1
                del hs[k]
        while len(ls) > 20: ls.pop(0)
        while len(hs) > 20: hs.pop(0)
        EV[i] = ev; ES[i] = evS; ET[i] = evT; PO[i] = po; OH[i] = oh; OL[i] = ol; SG[i] = sig
    return dict(ev=EV, evs=ES, evt=ET, po=PO, oh=OH, ol=OL, sig=SG)


def react(s, h, l, c, ph, pl):
    """f_xsReact: 0 BC+ · 1 BC- · 2 AFs+ · 3 AFs- · -1 none (for side s)."""
    rg = h - l
    pos = (c - l) / rg if rg > 0 else 0.5
    if s == 1:
        if c > ph: return 0 if pos >= 0.75 else 1
        if l < pl and c > pl and c <= ph and not (h > ph): return 2 if pos >= 0.5 else 3
    else:
        if c < pl: return 0 if pos <= 0.25 else 1
        if h > ph and c < ph and c >= pl and not (l < pl): return 2 if pos <= 0.5 else 3
    return -1


# ─────────────────────────────── the 15m core (Pine f_core) ───────────────────────────────
def core15(m):
    tf = '15m'
    d = bars(m, tf); sp = SPEC[m]; s50 = sp['s50']; tick = sp['tick']; k = s50 / 50.0
    o, h, l, c = (d[x].values.astype(float) for x in ('open', 'high', 'low', 'close'))
    n = len(d); T = d.index
    md = mins(T)
    toHit = hit_open(md)
    inAsia = (md >= 1080) | (md < 120)
    inAM = (md >= 570) & (md < 810)
    okSes = inAsia | inAM
    okX = (inAsia & ~(md < 120)) | inAM
    dDir = day_dir(d, m)
    H1 = bars(m, '1h')
    zh = zone(*(H1[x].values.astype(float) for x in ('open', 'high', 'low', 'close')))
    h1S = htf_state(d, H1, zh['side'])
    atr = atr_rma(h, l, c)
    Z = zone(o, h, l, c, True, True)          # x engine (expander, G1)
    C = zone(o, h, l, c, True, False)         # contraction engine
    X = cengine(o, h, l, c)                   # candle engine c
    S = sengine(h, l, c)                      # swing engine s
    h1_, h2_ = np.r_[NAN, h[:-1]], np.r_[NAN, NAN, h[:-2]]
    l1_, l2_ = np.r_[NAN, l[:-1]], np.r_[NAN, NAN, l[:-2]]
    c1_ = np.r_[NAN, c[:-1]]; o1_ = np.r_[NAN, o[:-1]]
    gL = (c1_ > h2_) & (l > h2_)
    gS = (c1_ < l2_) & (h < l2_)
    afL = (h > h1_) & (l >= l1_) & (c <= h1_) & (c >= l1_)
    afS = (l < l1_) & (h <= h1_) & (c >= l1_) & (c <= h1_)
    bcP = (c > h1_) & (l >= l1_) & (c > (h + l) / 2)
    rows = []
    minr = 1.0 * k

    def lim_wait(i, s, lv, d0, dead, contr_cut=True):
        """bars a C / X.M2 limit stays live (Pine f_trades): 20 candles, next session open, next contraction
        continuation break, the 1:2 level printing, a close past the break candle."""
        tgC = lv + s * 2.0 * d0
        w = 20
        for j in range(i + 1, min(i + 21, n)):
            if toHit[j]:
                return j - i - 1
            if (s == 1 and h[j] >= tgC) or (s == -1 and l[j] <= tgC):
                return j - i
            if s * (c[j] - dead) < 0:
                return j - i
            if contr_cut and C['ev'][j] == 2:
                return j - i
        return min(w, n - 1 - i)

    for i in range(4, n):
        t = T[i]
        zEv, zDir, zNum = Z['ev'][i], Z['evd'][i], Z['evn'][i]
        cEv, cDir, cNum = C['ev'][i], C['evd'][i], C['evn'][i]
        if okSes[i]:
            # X.M4 (EP.M1 · Z): T3+ break, daily filter, skip 00-02, 1.5 ATR, ½ at +0.5R, runner 1:6 / opposite break
            if okX[i] and zEv == 2 and zNum >= 2 and dDir[i] == zDir and atr[i] == atr[i]:
                sl = c[i] - zDir * 1.5 * atr[i]
                if zDir * (c[i] - sl) >= minr:
                    rows.append(_row('X.M4', tf, i, t, zDir, Z['boh'][i], Z['bol'][i], 'mkt', c[i], sl, 6.0, 0, f'T{zNum + 1} LDx' if zDir == 1 else f'T{zNum + 1} SDx'))
            # C.M3 (EP.M2 · G): bull GMC, daily green, 1 ATR, ½ at +0.75R, runner 1:3
            if okX[i] and gL[i] and dDir[i] == 1 and atr[i] == atr[i]:
                sl = c[i] - atr[i]
                if c[i] - sl >= minr:
                    rows.append(_row('C.M3', tf, i, t, 1, max(h[i - 2:i + 1]), min(l[i - 2:i + 1]), 'mkt', c[i], sl, 3.0, 0, 'GMC long c3 close'))
            # C.M4 (EP.M3 · B): bull GMC + c3 AFs against, daily green + 1h trend up, 1 ATR, runner 1:6
            if okX[i] and gL[i] and afL[i] and dDir[i] == 1 and h1S[i] == 1 and atr[i] == atr[i]:
                sl = c[i] - atr[i]
                if c[i] - sl >= minr:
                    rows.append(_row('C.M4', tf, i, t, 1, max(h[i - 2:i + 1]), min(l[i - 2:i + 1]), 'mkt', c[i], sl, 6.0, 0, 'GMC c3 AFs long'))
            # X.M5 (EP.M4 · C): contraction LDx (any), buy limit at 75% of the break candle, fills in Asia only
            if inAsia[i] and cEv == 2 and cNum >= 1 and cDir == 1:
                lv = l[i] + (h[i] - l[i]) * 0.75
                if lv < c[i]:
                    w = lim_wait(i, 1, lv, s50, l[i])
                    if w > 0:
                        rows.append(_row('X.M5', tf, i, t, 1, C['boh'][i], C['bol'][i], 'lmt', lv, lv - s50, 2.0, w, f'contraction LDx{cNum} MP limit'))
            # C.M5 (EP.M5 · M): BC+ bull, daily green + 1h up, fixed 50, ½ at +0.5R, runner 1:2
            if okX[i] and bcP[i] and dDir[i] == 1 and h1S[i] == 1:
                rows.append(_row('C.M5', tf, i, t, 1, h[i], l[i], 'mkt', c[i], c[i] - s50, 2.0, 0, 'BC+ long'))
            # X.M1: T3+ break, no daily filter, 1.5 ATR, 1:6 or opposite break
            if zEv == 2 and zNum >= 2 and atr[i] == atr[i]:
                sl = c[i] - zDir * 1.5 * atr[i]
                if zDir * (c[i] - sl) >= minr:
                    rows.append(_row('X.M1', tf, i, t, zDir, Z['boh'][i], Z['bol'][i], 'mkt', c[i], sl, 6.0, 0, f'T{zNum + 1} {"LDx" if zDir == 1 else "SDx"}'))
            # X.M2: contraction T3+ break, limit at 75% (MP bull / MD bear), fixed 50, 1:2
            if cEv == 2 and cNum >= 2:
                lv7 = l[i] + (h[i] - l[i]) * 0.75 if cDir == 1 else h[i] - (h[i] - l[i]) * 0.75
                if cDir * (c[i] - lv7) > 0:
                    dead = l[i] if cDir == 1 else h[i]
                    w = lim_wait(i, cDir, lv7, s50, dead)
                    if w > 0:
                        rows.append(_row('X.M2', tf, i, t, cDir, C['boh'][i], C['bol'][i], 'lmt', lv7, lv7 - cDir * s50, 2.0, w, f'contraction T{cNum + 1} {"MP" if cDir == 1 else "MD"} limit'))
            # C.M1: GMC c3 AFs against, long and short, 1 ATR, 1:6
            if ((gL[i] and afL[i]) or (gS[i] and afS[i])) and atr[i] == atr[i]:
                s8 = 1 if (gL[i] and afL[i]) else -1
                sl = c[i] - s8 * atr[i]
                if s8 * (c[i] - sl) >= minr:
                    rows.append(_row('C.M1', tf, i, t, s8, max(h[i - 2:i + 1]), min(l[i - 2:i + 1]), 'mkt', c[i], sl, 6.0, 0, 'GMC c3 AFs against'))
            # C.M2: every bull GMC, fixed 50, 1:2 (+ gap-candle-open exit)
            if gL[i]:
                rows.append(_row('C.M2', tf, i, t, 1, max(h[i - 2:i + 1]), min(l[i - 2:i + 1]), 'mkt', c[i], c[i] - s50, 2.0, 0, 'GMC long c3 close'))
    # ── XCS.M1 / M2 (all hours) and XCS.M5 (pre-market iBlock AFs+) ──
    blocks = []      # [top, bot, po4, side, born, touch]
    for i in range(1, n):
        t = T[i]
        zEv, zDir = Z['ev'][i], Z['evd'][i]
        xe, xs, xt = X['ev'][i], X['side'][i], X['tier'][i]
        we, ws, wt = S['ev'][i], S['evs'][i], S['evt'][i]
        m5 = {1: None, -1: None}
        pre = 480 <= md[i] < 570
        for q in range(len(blocks) - 1, -1, -1):
            qt, qb, qk, qs, qn, qh = blocks[q]
            qd = False
            if qh < 0:
                if (qs == 1 and l[i] <= qt) or (qs == -1 and h[i] >= qb):
                    qh = i; blocks[q][5] = i
                    if not pre: qd = True
            if not qd and qh >= 0:
                if i - qh > 10:
                    qd = True
                elif (qs == 1 and c[i] > qk) or (qs == -1 and c[i] < qk):
                    r = react(qs, h[i], l[i], c[i], h[i - 1], l[i - 1])
                    if r >= 0:
                        qd = True
                        if r == 2 and m5[qs] is None:
                            m5[qs] = (qt, qb)
            if not qd and ((qs == 1 and c[i] < qk) or (qs == -1 and c[i] > qk)): qd = True
            if not qd and i - qn >= 300: qd = True
            if qd: del blocks[q]
        for e in range(3):
            qe = (zEv, xe, we)[e]; qs = (zDir, xs, ws)[e]
            qa = (Z['noh'][i], X['oh'][i], S['oh'][i])[e]; qb = (Z['nol'][i], X['ol'][i], S['ol'][i])[e]
            qp = (Z['ntn'][i], X['tn'][i], S['po'][i])[e]
            if qe == 2 and qa == qa and qb == qb:
                qt_, qm_ = max(qa, qb), min(qa, qb)
                dup = any(b[4] == i and b[3] == qs and b[0] == qt_ and b[1] == qm_ for b in blocks)
                if qt_ > qm_ and not dup:
                    pk = qp if qp == qp else (qm_ if qs == 1 else qt_)
                    blocks.append([qt_, qm_, min(max(pk, qm_), qt_), qs, i, -1])
        while len(blocks) > 120: blocks.pop(0)
        if i <= 3: continue
        m1 = {1: False, -1: False}; m2 = {1: False, -1: False}; nt = {1: [], -1: []}
        for ev_, sd_, tr_, nm in ((zEv, zDir, Z['tier'][i], 'x'), (xe, xs, xt, 'c'), (we, ws, wt, 's')):
            if ev_ == 2:
                m2[sd_] = True; nt[sd_].append(f'{nm}T{tr_}')
                if tr_ >= 6: m1[sd_] = True
        for s in (1, -1):
            if m1[s]:
                rows.append(_row('XCS.M1', tf, i, t, s, h[i], l[i], 'mkt', c[i], c[i] - s * s50, 2.0, 0, 'P5+ break ' + ','.join(x for x in nt[s] if int(x[2:]) >= 6)))
            if m2[s]:
                rows.append(_row('XCS.M2', tf, i, t, s, h[i], l[i], 'mkt', c[i], c[i] - s * s50, 2.0, 0, 'break ' + ','.join(nt[s])))
            if m5[s] is not None:
                sl = l[i] - tick if s == 1 else h[i] + tick
                if s * (c[i] - sl) >= tick:
                    rows.append(_row('XCS.M5', tf, i, t, s, m5[s][0], m5[s][1], 'mkt', c[i], sl, 2.0, 0, 'pre-market iBlock AFs+'))
    return rows, dict(d=d, Z=Z, X=X, S=S, md=md, okAN=inAsia | inAM)


# ─────────────────────────────── XCS.M3 / XCS.M4 (4H GMC AFs filter → 15m pullback BC) ───────────────────────────────
def xcs34(m, ctx):
    d = ctx['d']; Z, X, S = ctx['Z'], ctx['X'], ctx['S']; okAN = ctx['okAN']
    s50 = SPEC[m]['s50']
    o, h, l, c = (d[x].values.astype(float) for x in ('open', 'high', 'low', 'close'))
    H4 = bars(m, '4h')
    ho, hh, hl, hc = (H4[x].values.astype(float) for x in ('open', 'high', 'low', 'close'))
    nH = len(H4)
    # 1) filters on 4H: [side, start 4H index (AFs candle), afs extreme]
    filt = []
    gm = []   # live GMCs: [side, edge (c1 high / low), gopen (c2 open), touch idx]
    for j in range(2, nH):
        # update live GMCs with candle j. A GMC lives until a 4H close through its open; each touch of the gap
        # edge opens a 4-candle window (the touch candle + 3) for a bullish (bearish) AFs = the filter.
        keep = []
        for g in gm:
            sd, edge, gop, tch = g
            if sd * (hc[j] - gop) < 0:          # 4H close through the GMC open → dead
                continue
            if tch < 0 and ((sd == 1 and hl[j] <= edge) or (sd == -1 and hh[j] >= edge)):
                tch = j; g[3] = j
            if tch >= 0 and j - tch <= 3:
                r = react(sd, hh[j], hl[j], hc[j], hh[j - 1], hl[j - 1])
                if r in (2, 3):                  # BuAFs (+ or -) / BeAFs mirror
                    filt.append((sd, j, hl[j] if sd == 1 else hh[j]))
                    g[3] = -1                    # re-arm: the next touch can give a new filter
            elif tch >= 0:
                g[3] = -1                        # window over without an AFs → wait for a new touch
            keep.append(g)
        gm = keep
        # new GMC on candle j (c1 = j-2, c2 = j-1, c3 = j)
        if hc[j - 1] > hh[j - 2] and hl[j] > hh[j - 2]:
            gm.append([1, hh[j - 2], ho[j - 1], -1])
        if hc[j - 1] < hl[j - 2] and hh[j] < hl[j - 2]:
            gm.append([-1, hl[j - 2], ho[j - 1], -1])
    # 2) 15m entries inside each filter window
    t15 = d.tend.values; T = d.index
    rows = []; seen = set()
    for sd, a, ext in filt:
        if a + 1 >= nH: continue
        endj = min(a + 6, nH - 1)
        # the filter dies at the close of a 4H candle closing past the AFs extreme
        for j in range(a + 1, endj + 1):
            if sd * (hc[j] - ext) < 0:
                endj = j; break
        t0 = H4.tend.values[a]; t1 = H4.tend.values[endj]
        i0 = np.searchsorted(t15, t0, 'right'); i1 = np.searchsorted(t15, t1, 'right')
        pull = False
        for i in range(max(i0, 1), min(i1, len(d))):
            trend = (Z['side'][i] == sd) or (X['side'][i] == sd) or (S['sig'][i] == sd)
            opp = c[i] < l[i - 1] if sd == 1 else c[i] > h[i - 1]
            withbc = c[i] > h[i - 1] if sd == 1 else c[i] < l[i - 1]
            if not pull:
                if opp and trend: pull = True
                continue
            if withbc:
                if okAN[i] and (i, sd) not in seen:
                    seen.add((i, sd))
                    for code in (('XCS.M3', 'XCS.M4') if sd == 1 else ('XCS.M3',)):
                        rows.append(_row(code, '15m', i, T[i], sd, h[i], l[i], 'mkt', c[i], c[i] - sd * s50, 2.0, 0, '4H GMC AFs → 15m pullback BC'))
                break
    return rows


# ─────────────────────────────── X.M3 (5m iBlock T4+ long, limit at the top) ───────────────────────────────
def xm3(m):
    tf = '5m'
    d = bars(m, tf)
    if len(d) < 50: return []
    s50 = SPEC[m]['s50']
    o, h, l, c = (d[x].values.astype(float) for x in ('open', 'high', 'low', 'close'))
    Z = zone(o, h, l, c, True, True)
    n = len(d); rows = []
    for i in np.where((Z['ev'] == 2) & (Z['evd'] == 1) & (Z['evn'] >= 3))[0]:
        top, bot, po = max(Z['noh'][i], Z['nol'][i]), min(Z['noh'][i], Z['nol'][i]), Z['ntn'][i]
        if not (top > bot): continue       # a top at / above the close fills at once (marketable limit)
        # the block lives with its PO4: dead on a close below the PO4 (cap 300 candles)
        w = 300
        below = np.where(c[i + 1:min(i + 301, n)] < po)[0]
        if len(below): w = int(below[0]) + 1
        w = min(w, n - 1 - i)
        if w <= 0: continue
        rows.append(_row('X.M3', tf, i, d.index[i], 1, top, bot, 'lmt', top, top - s50, 2.0, w, f'iBlock T{Z["evn"][i] + 1} XP limit'))
    return rows


# ─────────────────────────────── C.M8 (09:30 15m BuBC above the pre-open high) ───────────────────────────────
def cm8(m):
    tf = '15m'
    d = bars(m, tf); s50 = SPEC[m]['s50']
    h, l, c = d.high.values, d.low.values, d.close.values
    md = mins(d.index); rows = []
    day = d.index.normalize()
    for i in np.where(md == 570)[0]:
        if i < 6: continue
        if not (c[i] > h[i - 1]): continue
        w = (day == day[i]) & (md >= 480) & (md < 570)
        pre = h[w]
        if len(pre) == 0 or not (c[i] > pre.max()): continue
        rows.append(_row('C.M8', tf, i, d.index[i], 1, h[i], l[i], 'mkt', c[i], c[i] - s50, 3.0, 0, '09:30 BuBC > pre-open high'))
    return rows


# ─────────────────────────────── C.M6 / C.M7 (1m level retest, NY AM longs) ───────────────────────────────
def htf_gmc_levels(m, tf):
    """newest live GMC level (c2 open) after each closed tf candle; dies on a tf close through it."""
    H = bars(m, tf)
    o, h, l, c = (H[x].values.astype(float) for x in ('open', 'high', 'low', 'close'))
    live = []; out = np.full(len(H), NAN)
    for j in range(len(H)):
        live = [g for g in live if g[0] * (c[j] - g[1]) >= 0]
        if j >= 2:
            if c[j - 1] > h[j - 2] and l[j] > h[j - 2]: live.append((1, o[j - 1]))
            if c[j - 1] < l[j - 2] and h[j] < l[j - 2]: live.append((-1, o[j - 1]))
        if live: out[j] = live[-1][1]
    return H.tend.values, out


def lr(m):
    tf = '1m'
    d = bars(m, tf)
    if len(d) < 1000: return []
    s50 = SPEC[m]['s50']; k = s50 / 50.0
    o, h, l, c = (d[x].values.astype(float) for x in ('open', 'high', 'low', 'close'))
    n = len(d); T = d.index; md = mins(T); tend = d.tend.values
    X = cengine(o, h, l, c)
    # 15m trend (candle engine on 15m, last closed 15m candle)
    D15 = bars(m, '15m')
    x15 = cengine(*(D15[x].values.astype(float) for x in ('open', 'high', 'low', 'close')))
    p15 = np.searchsorted(D15.tend.values, tend, 'right') - 1
    tr15 = np.where(p15 >= 0, x15['side'][np.clip(p15, 0, None)], 0)
    # HTF GMC levels
    g1t, g1v = htf_gmc_levels(m, '1h'); g4t, g4v = htf_gmc_levels(m, '4h')
    # day levels from the 1m candles (CME day = 18:00 -> 17:00)
    F = fine(m); F = F[F.res <= 1]
    fk = (F.index + pd.Timedelta(hours=6)).normalize()
    fmd = mins(F.index)
    gF = F.groupby(fk)
    DO = gF.open.first(); DH = gF.high.max(); DL = gF.low.min()
    asia = F[(fmd >= 1080) | (fmd < 120)].groupby(fk[(fmd >= 1080) | (fmd < 120)])
    on = F[(fmd >= 1080) | (fmd < 570)].groupby(fk[(fmd >= 1080) | (fmd < 570)])
    rtho = F[fmd == 570].groupby(fk[fmd == 570]).open.first()
    prc = F[(fmd < 960) & (fmd >= 570)].groupby(fk[(fmd < 960) & (fmd >= 570)]).close.last()
    ASH, ASL, ONH, ONL = asia.high.max(), asia.low.min(), on.high.max(), on.low.min()
    days = DO.index
    dpos = {dd: q for q, dd in enumerate(days)}
    dk = (T + pd.Timedelta(hours=6)).normalize()
    rows = []
    cand = np.where((X['ev'] == 1) & (X['side'] == 1) & (md >= 570) & (md < 720))[0]
    for i in cand:
        if tr15[i] != 1: continue
        t1 = X['tn'][i]; brk = X['brk'][i]; pbi = X['pbi'][i]
        if not (t1 == t1) or not (brk == brk): continue
        dd = dk[i]; q = dpos.get(dd)
        lv = []
        if q is not None:
            lv += [DO.iloc[q]]
            if q > 0 and (days[q] - days[q - 1]) <= pd.Timedelta(days=4):
                pdd = days[q - 1]
                lv += [DH.iloc[q - 1], DL.iloc[q - 1]]
                if pdd in prc.index: lv.append(prc[pdd])
        for ser in (ASH, ASL, ONH, ONL, rtho):
            if dd in ser.index: lv.append(ser[dd])
        p1 = np.searchsorted(g1t, tend[i], 'right') - 1; p4 = np.searchsorted(g4t, tend[i], 'right') - 1
        if p1 >= 0: lv.append(g1v[p1])
        if p4 >= 0: lv.append(g4v[p4])
        lv = np.array([x for x in lv if x == x])
        if not len(lv): continue
        dist = np.abs(lv - t1)
        if dist.min() > 15 * k: continue
        level = lv[np.argmin(dist)]
        # no bull GMC between the PO4 T1 candle and the CDL candle with its level (c2 open) inside T1 .. break line
        lo_, hi_ = min(t1, brk), max(t1, brk); gap = False
        for kk in range(max(pbi + 2, 2), i + 1):
            if c[kk - 1] > h[kk - 2] and l[kk] > h[kk - 2] and lo_ <= o[kk - 1] <= hi_:
                gap = True; break
        if gap: continue
        if not (t1 < c[i]): continue
        for code, stp in (('C.M6', 40.0), ('C.M7', 35.0)):
            sl = t1 - stp * k
            cx = t1 + 2 * stp * k
            w = 60
            up = np.where(h[i + 1:min(i + 61, n)] >= cx)[0]
            if len(up): w = int(up[0]) + 1
            w = min(w, n - 1 - i)
            if w <= 0: continue
            rows.append(_row(code, tf, i, T[i], 1, brk, min(t1, level), 'lmt', t1, sl, 5.0, w, f'CDL PO4 T1 retest · level {level:.2f}'))
    return rows


def signals(m: str) -> pd.DataFrame:
    rows, ctx = core15(m)
    rows += xcs34(m, ctx)
    rows += xm3(m)
    rows += cm8(m)
    rows += lr(m)
    S = pd.DataFrame(rows, columns=COLS)
    S['nrr'] = S.nrr.astype(float)
    return S.sort_values(['t', 'strat']).reset_index(drop=True)


if __name__ == '__main__':
    import time
    for m in (sys.argv[1:] or ['NQ', 'MNQ', 'MES', 'MGC', 'MCL']):
        t0 = time.time()
        S = signals(m)
        S.to_parquet(f'/home/claude/allm/sig_edge_{m}.parquet')
        print(m, len(S), round(time.time() - t0, 1), 's', S.groupby('strat').size().to_dict(), flush=True)
