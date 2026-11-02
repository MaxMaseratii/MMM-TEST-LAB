"""MMM PRO PLUS points test (Table 3 / Table 4) mirrored in Python from the Pine script (Nov 2 2026).
Pass 1 (signals): SuperTrend 14 x 2, stall zones / EXIT labels / REJ, after-EXIT tests (50% line, ST rejection,
resumption BC, GMC, box break), flips, VWAP + urgency state. Same order of operations as the Pine.
Pass 2 (trades): the 11 setups, limit fills 1 tick through, stop by wick (gap = exit at open), exit on the EXIT label
in your direction or a SuperTrend flip, fill candle counts only the move against you, cost per trade,
optional 2-hour windows (A-E, forced flat) and daily rules (per setup and window: max 3 trades, stop after 2 losses)."""
import numpy as np, pandas as pd

SETUPS = ['FLIP market at close', 'FLIP limit at old ST line', 'BC FLIP limit at PG', 'NBC FLIP limit at PG',
          'STALL REJ1 market', 'AFTER EXIT limit at 50%', 'AFTER EXIT ST rejection', 'AFTER EXIT 50% + resumption BC',
          'AFTER EXIT 50% + GMC', 'AFTER EXIT box break close', 'BOX BREAK retest limit',
          'RANDOM with trend (control)', 'RANDOM side (control)']
NS = len(SETUPS)
WIN = ['outside', 'A NY open', 'B London', 'C News', 'D Afternoon', 'E Reopen']
ST_LEN, ST_MULT, GMC_MIN, REJ_ATR, VOL_LEN, VOL_MULT, VW_BAND, CVD_LOOK = 14, 2.0, 0.1, 0.1, 20, 1.5, 0.25, 5


def rma_atr(h, l, c, n=ST_LEN):
    tr = np.empty(len(c)); tr[0] = h[0] - l[0]
    tr[1:] = np.maximum(h[1:] - l[1:], np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))
    a = np.full(len(c), np.nan)
    if len(c) < n: return a
    a[n - 1] = tr[:n].mean()
    for i in range(n, len(c)):
        a[i] = (a[i - 1] * (n - 1) + tr[i]) / n
    return a


def supertrend(o, h, l, c, atr, pine_custom=True):
    """returns st, dir (dir -1 = bull / lower band, 1 = bear) exactly as the PRO PLUS code (pine_custom) or ta.supertrend."""
    n = len(c); st = np.full(n, np.nan); dr = np.ones(n, dtype=np.int8)
    ub = lb = np.nan; d = 1
    for i in range(n):
        hl2 = (h[i] + l[i]) / 2
        rU = hl2 + ST_MULT * atr[i]; rL = hl2 - ST_MULT * atr[i]
        pU, pL, pD = ub, lb, d
        c1 = c[i - 1] if i > 0 else np.nan
        if pine_custom:
            nU = rU if (pU != pU or rU < pU or (c1 > pU and pD == -1)) else pU
            nL = rL if (pL != pL or rL > pL or (c1 < pL and pD == 1)) else pL
        else:
            nU = rU if (pU != pU or rU < pU or c1 > pU) else pU
            nL = rL if (pL != pL or rL > pL or c1 < pL) else pL
        if i == 0 or atr[i - 1] != atr[i - 1]:
            nD = 1
        elif pD == 1:
            nD = -1 if c[i] > nU else 1
        else:
            nD = 1 if c[i] < nL else -1
        ub, lb, d = nU, nL, nD
        st[i] = lb if d == -1 else ub
        dr[i] = d
    return st, dr


def signals(df):
    """pass 1. df: open high low close volume delta, NY-time index. returns dict of arrays."""
    o = df.open.values; h = df.high.values; l = df.low.values; c = df.close.values
    v = df.volume.values.astype(float); dl = df.delta.values.astype(float)
    n = len(c)
    atr = rma_atr(h, l, c)
    st, dr = supertrend(o, h, l, c, atr)
    stUp = dr < 0
    hp = np.r_[np.nan, h[:-1]]; lp = np.r_[np.nan, l[:-1]]
    buX = (c > hp) | ((o > hp) & ~(c < lp))
    beX = (c < lp) | ((o < lp) & ~(c > hp))
    h2 = np.r_[np.nan, np.nan, h[:-2]]; l2 = np.r_[np.nan, np.nan, l[:-2]]
    gmin = np.nan_to_num(atr) * GMC_MIN
    buG = ((l - h2) >= gmin) & (l > h2)
    beG = ((l2 - h) >= gmin) & (h < l2)
    fUp = np.r_[False, (dr[1:] < 0) & (dr[:-1] > 0)]
    fDn = np.r_[False, (dr[1:] > 0) & (dr[:-1] < 0)]
    # VWAP (session from 18:00 NY) + urgency state
    sday = (df.index + pd.Timedelta(hours=6)).normalize().values
    newd = np.r_[True, sday[1:] != sday[:-1]]
    hlc3 = (h + l + c) / 3
    vw = np.empty(n); cvd = np.empty(n); spv = sv = cv = 0.0
    for i in range(n):
        if newd[i]: spv = sv = 0.0; cv = 0.0
        spv += hlc3[i] * v[i]; sv += v[i]; cv += dl[i]
        vw[i] = spv / sv if sv > 0 else c[i]; cvd[i] = cv
    vavg = pd.Series(v).rolling(VOL_LEN).mean().values
    rel = np.where(vavg > 0, v / np.where(vavg > 0, vavg, 1), 0.0)
    cvd5 = np.r_[np.full(CVD_LOOK, np.nan), cvd[:-CVD_LOOK]]
    urgB = (rel >= VOL_MULT) & (dl > 0) & (cvd > cvd5)
    urgS = (rel >= VOL_MULT) & (dl < 0) & (cvd < cvd5)
    vband = np.nan_to_num(atr) * VW_BAND
    vws = np.zeros(n, dtype=np.int8); s = 0
    for i in range(n):
        if abs(c[i] - vw[i]) <= vband[i]: s = 0
        elif c[i] > vw[i]: s = 1 if urgB[i] else (1 if s == 1 else 0)
        else: s = -1 if urgS[i] else (-1 if s == -1 else 0)
        vws[i] = s

    exL = np.zeros(n, bool); exS = np.zeros(n, bool)
    rejS = np.zeros(n, np.int8); t50S = np.zeros(n, np.int8); t50P = np.full(n, np.nan); t50I = np.full(n, -1, np.int64)
    pxRej = np.zeros(n, np.int8); rsm = np.zeros(n, np.int8); gmc = np.zeros(n, np.int8)
    brk = np.zeros(n, np.int8); brkP = np.full(n, np.nan)
    stBu = np.full(n, np.nan); stBe = np.full(n, np.nan)
    fsBu = fsBe = np.nan
    live = None   # [side, op, ext, bar0, rej, prevTouch]
    px = {}       # side -> [ext, mid, t50, stRej, rsm, gmc]
    for i in range(1, n):
        if fDn[i] and st[i] == st[i]: fsBe = st[i]
        if fUp[i] and st[i] == st[i]: fsBu = st[i]
        stBu[i] = fsBu; stBe[i] = fsBe
        if st[i] != st[i] or st[i - 1] != st[i - 1]:
            continue
        flip = dr[i] != dr[i - 1]
        step = (not flip) and ((st[i] > st[i - 1]) if stUp[i] else (st[i] < st[i - 1]))
        stPrev = st[i - 1]
        for sd in list(px.keys()):
            if flip:
                del px[sd]; continue
            x = px[sd]; bull = sd == 1
            bk = c[i] > x[0] if bull else c[i] < x[0]
            hit = l[i] <= x[1] if bull else h[i] >= x[1]
            if hit and not x[2]:
                t50S[i] = sd; t50P[i] = x[1]; t50I[i] = x[6]
            if hit: x[2] = True
            if (l[i] <= st[i] and c[i] > st[i]) if bull else (h[i] >= st[i] and c[i] < st[i]):
                if not x[3]: pxRej[i] = sd
                x[3] = True
            if x[2] and not bk and not x[4] and (buX[i] if bull else beX[i]):
                x[4] = True; rsm[i] = sd
            if x[2] and not bk and not x[5] and (buG[i] if bull else beG[i]):
                x[5] = True; gmc[i] = sd
            if bk:
                brk[i] = sd; brkP[i] = x[0]; del px[sd]
        if live is not None:
            sd, op, ext, b0, rj, pt = live
            bear = sd == -1
            beyond = c[i] > op if bear else c[i] < op
            touch = False; status = 0
            if (c[i] < ext) if bear else (c[i] > ext):
                status = 2
            elif beyond:
                status = 1
            else:
                a = atr[i] if atr[i] == atr[i] else 0.0
                touch = (h[i] >= op - REJ_ATR * a and c[i] < op) if bear else (l[i] <= op + REJ_ATR * a and c[i] > op)
                if touch and not pt:
                    rj += 1
                    if rj == 1: rejS[i] = sd
            live = [sd, op, ext, b0, rj, touch]
            if status == 1:
                if bear: exS[i] = True
                else: exL[i] = True
                if sd not in px and not flip:
                    px[sd] = [ext, (ext + stPrev) / 2, False, False, False, False, i]
                live = None
            elif status == 2:
                live = None
        if flip or step:
            sd = 1 if stUp[i] else -1
            live = [sd, min(o[i], c[i]) if sd == 1 else max(o[i], c[i]), h[i] if sd == 1 else l[i], i, 0, False]
    return dict(o=o, h=h, l=l, c=c, st=st, dr=dr, atr=atr, buX=buX, beX=beX, fUp=fUp, fDn=fDn, vw=vw, vws=vws,
                exL=exL, exS=exS, rejS=rejS, t50S=t50S, t50P=t50P, t50I=t50I, pxRej=pxRej, rsm=rsm, gmc=gmc, brk=brk, brkP=brkP,
                stBu=stBu, stBe=stBe)


def windows(idx):
    m = idx.hour.values * 60 + idx.minute.values
    def w(a, b): return (m >= a) & (m < b)
    tA = w(585, 660); tB = w(210, 315); tC = w(515, 585); tD = w(860, 945); tE = w(1110, 1185)
    hA = tA; hB = w(210, 330); hC = w(515, 600); hD = w(860, 960); hE = w(1110, 1200)
    now = np.where(tA, 1, np.where(tB, 2, np.where(tC, 3, np.where(tD, 4, np.where(tE, 5, 0))))).astype(np.int8)
    T = np.vstack([np.ones(len(m), bool), tA, tB, tC, tD, tE])
    H = np.vstack([np.ones(len(m), bool), hA, hB, hC, hD, hE])
    return now, T, H


def trades(S, idx, stop, cost, tick, win_on=False, day_on=False, use_exit=True, stop_mode='fixed', maxstop=None,
           day_max=3, day_loss=2):
    """pass 2. returns (trade log DataFrame, missed counts, skipped counts)."""
    o, h, l, c, st = S['o'], S['h'], S['l'], S['c'], S['st']
    fUp, fDn, exL, exS = S['fUp'], S['fDn'], S['exL'], S['exS']
    n = len(c); thru = tick * 1.0
    wnow, T, H = windows(idx)
    dom = idx.day.values
    dayT = {}; dayL = {}
    missed = np.zeros(NS, int); skipped = np.zeros(NS, int)
    rng = np.random.default_rng(12345); rnd = rng.random(n) < 0.02; rside = np.where(rng.random(n) < 0.5, 1, -1)
    log = []
    open_ = []   # [setup, side, lvl, filled, entry, risk, mfe, mae, favPre, bar0, win, stopPx, isig, ifill]
    maxstop = stop if maxstop is None else maxstop

    def dok(s, w):
        return (not day_on) or (dayT.get((s, w), 0) < day_max and dayL.get((s, w), 0) < day_loss)

    def okn(s, sd, i):
        return sd != 0 and ((not win_on) or wnow[i] > 0) and dok(s, wnow[i])

    def stop_px(entry, sd, i):
        if stop_mode == 'flipst':
            return S['stBu'][i] if sd == 1 else S['stBe'][i]
        return entry - sd * stop

    def popen(t, px, i):
        sp = stop_px(px, t[1], i)
        if sp != sp: skipped[t[0]] += 1; return False
        d = (px - sp) * t[1]
        if not (d > 0 and (stop_mode == 'fixed' or d <= maxstop)):
            skipped[t[0]] += 1; return False
        t[3] = True; t[4] = px; t[11] = sp; t[5] = d; t[9] = i; t[13] = i
        k = (t[0], t[10]); dayT[k] = dayT.get(k, 0) + 1
        return True

    def pclose(t, plraw, i, why):
        pl = plraw - cost
        if pl <= 0:
            k = (t[0], t[10]); dayL[k] = dayL.get(k, 0) + 1
        log.append((t[0], t[1], t[10], t[12], t[13], i, pl, t[5], t[8], t[6], t[7], why, t[14]))

    def pfirst(t, i, xs):
        sd = t[1]
        t[7] = max(0.0, t[4] - l[i] if sd == 1 else h[i] - t[4])
        if (l[i] <= t[11]) if sd == 1 else (h[i] >= t[11]):
            pclose(t, (t[11] - t[4]) * sd, i, 'stop'); return True
        if xs:
            pclose(t, (c[i] - t[4]) * sd, i, 'exit'); return True
        return False

    i0 = int(np.argmax(~np.isnan(st)))
    for i in range(i0, n):
        if i > 0 and dom[i] != dom[i - 1]:
            dayT.clear(); dayL.clear()
        if win_on and open_:
            keep = []
            for t in open_:
                w = t[10]
                end = w > 0 and ((not H[w, i]) if t[3] else (not T[w, i]))
                if end:
                    if t[3]: pclose(t, (o[i] - t[4]) * t[1], i, 'window')
                    else: missed[t[0]] += 1
                else:
                    keep.append(t)
            open_ = keep
        if open_:
            keep = []
            for t in open_:
                if i <= t[9]:
                    keep.append(t); continue
                sd = t[1]
                xs = ((use_exit and exL[i]) or fDn[i]) if sd == 1 else ((use_exit and exS[i]) or fUp[i])
                if not t[3]:
                    touch = (l[i] <= t[2] - thru) if sd == 1 else (h[i] >= t[2] + thru)
                    if touch:
                        if not dok(t[0], t[10]):
                            missed[t[0]] += 1; continue
                        if not popen(t, min(o[i], t[2]) if sd == 1 else max(o[i], t[2]), i):
                            continue
                        if pfirst(t, i, xs): continue
                        keep.append(t)
                    elif xs:
                        missed[t[0]] += 1
                    else:
                        keep.append(t)
                else:
                    fav = h[i] - t[4] if sd == 1 else t[4] - l[i]
                    adv = t[4] - l[i] if sd == 1 else h[i] - t[4]
                    t[7] = max(t[7], adv); t[6] = max(t[6], fav)
                    if (l[i] <= t[11]) if sd == 1 else (h[i] >= t[11]):
                        xp = min(o[i], t[11]) if sd == 1 else max(o[i], t[11])
                        pclose(t, (xp - t[4]) * sd, i, 'stop')
                    elif xs:
                        pclose(t, (c[i] - t[4]) * sd, i, 'exit')
                    else:
                        t[8] = max(t[8], fav); keep.append(t)
            open_ = keep
        if st[i] != st[i]:
            continue

        def market(s, sd, px):
            if okn(s, sd, i):
                t = [s, sd, np.nan, False, np.nan, np.nan, 0.0, 0.0, 0.0, i, int(wnow[i]), np.nan, i, -1, i]
                if popen(t, px, i): open_.append(t)

        def limit(s, sd, lv):
            if okn(s, sd, i) and lv == lv:
                open_.append([s, sd, lv, False, np.nan, np.nan, 0.0, 0.0, 0.0, i, int(wnow[i]), np.nan, i, -1, i])

        if fUp[i] or fDn[i]:
            sd = 1 if fUp[i] else -1
            bc = S['buX'][i] if fUp[i] else S['beX'][i]
            market(0, sd, c[i])
            limit(1, sd, st[i - 1])
            limit(2 if bc else 3, sd, o[i])
        if S['rejS'][i]:
            market(4, int(S['rejS'][i]), c[i])
        sd5 = int(S['t50S'][i]); p5 = S['t50P'][i]
        if okn(5, sd5, i) and p5 == p5:
            t = [5, sd5, p5, False, np.nan, np.nan, 0.0, 0.0, 0.0, i, int(wnow[i]), np.nan, i, -1, int(S['t50I'][i])]
            th = (l[i] <= p5 - thru) if sd5 == 1 else (h[i] >= p5 + thru)
            if th:
                if popen(t, min(o[i], p5) if sd5 == 1 else max(o[i], p5), i):
                    if not pfirst(t, i, False): open_.append(t)
            else:
                open_.append(t)
        if S['pxRej'][i]: market(6, int(S['pxRej'][i]), c[i])
        if S['rsm'][i]: market(7, int(S['rsm'][i]), c[i])
        if S['gmc'][i]: market(8, int(S['gmc'][i]), c[i])
        if S['brk'][i]:
            sd = int(S['brk'][i])
            market(9, sd, c[i])
            limit(10, sd, S['brkP'][i])
            keep = []
            for t in open_:
                if t[0] == 5 and not t[3] and t[1] == sd: missed[5] += 1
                else: keep.append(t)
            open_ = keep
        if rnd[i]:
            market(11, 1 if S['dr'][i] < 0 else -1, c[i])
            market(12, int(rside[i]), c[i])
    cols = ['setup', 'side', 'win', 'isig', 'ifill', 'iexit', 'pl', 'risk', 'favpre', 'mfe', 'mae', 'why', 'itag']
    return pd.DataFrame(log, columns=cols), missed, skipped
