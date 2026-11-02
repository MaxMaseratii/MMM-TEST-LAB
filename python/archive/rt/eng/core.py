"""MMM research engine (Oct 2026 test).
Data: bar OPEN time, New York (naive). Signals on CLOSED candles only.
"""
import numpy as np, pandas as pd, numba as nb, glob, os

LIB = '/home/claude/rt/lib/data'
TICK = 0.25

# ───────────────────────── data ─────────────────────────
def load(sym, tf, months=None):
    fs = sorted(glob.glob(f'{LIB}/{sym}/{tf}/*.csv'))
    if months:
        fs = [f for f in fs if os.path.basename(f)[:-4] in months]
    d = pd.concat([pd.read_csv(f) for f in fs])
    d.index = pd.to_datetime(d.pop('time'))
    d = d[~d.index.duplicated(keep='last')].sort_index()
    return d[['open', 'high', 'low', 'close', 'volume']].astype(float)

def resample(d, tf):
    """tf in 5m,10m,15m,1h,4h,D. 4h anchored at 18:00, D = 18:00 session."""
    if tf in ('5m', '10m', '15m', '1h', '2m', '30m'):
        rule = {'2m': '2min', '5m': '5min', '10m': '10min', '15m': '15min', '30m': '30min', '1h': '60min'}[tf]
        key = d.index.floor(rule)
    elif tf == '4h':
        key = (d.index - pd.Timedelta(hours=18)).floor('4h') + pd.Timedelta(hours=18)
    elif tf == 'D':
        key = (d.index + pd.Timedelta(hours=6)).floor('D') - pd.Timedelta(hours=6)
    g = d.groupby(key)
    return pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(),
                         'close': g.close.last(), 'volume': g.volume.sum()})

def atr(d, n=14):
    h, l, c = d.high.values, d.low.values, d.close.values
    pc = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.c_[h - l, np.abs(h - pc), np.abs(l - pc)], axis=1)
    out = np.full(len(tr), np.nan)
    if len(tr) > n:
        out[n - 1] = tr[:n].mean()
        a = 1.0 / n
        for i in range(n, len(tr)):
            out[i] = out[i - 1] + a * (tr[i] - out[i - 1])
    return out

def daily_atr_prev(sig, daily):
    """yesterday's daily ATR(14), mapped to each signal bar."""
    da = pd.Series(atr(daily), index=daily.index).shift(1)
    sess = (sig.index + pd.Timedelta(hours=6)).floor('D') - pd.Timedelta(hours=6)
    return da.reindex(sess).values

def session(idx):
    m = idx.hour * 60 + idx.minute
    asia = (m >= 1080) | (m < 120)
    am = (m >= 570) & (m < 810)
    s = np.where(asia, 0, np.where(am, 1, 2))
    return s  # 0 Asia, 1 NY AM, 2 other

# ───────────────────────── MMCB ─────────────────────────
TYPES = ['BuBC+', 'BuBC-', 'BuC2+', 'BuC2-', 'BuAFs+', 'BuAFs-', 'CI•BuAF', 'S&D•BuAF',
         'BeBC+', 'BeBC-', 'BeC2+', 'BeC2-', 'BeAFs+', 'BeAFs-', 'CI•BeAF', 'S&D•BeAF']
# trade side of each type (its lean)
TSIDE = np.array([1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1])

def mmcb(d):
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    ph, pl = np.r_[np.nan, h[:-1]], np.r_[np.nan, l[:-1]]
    rg = h - l
    pos = np.where(rg > 0, (c - l) / np.where(rg > 0, rg, 1), 0.5)
    tH, tL = h > ph, l < pl
    t = np.full(len(c), -1)
    bu, be = c > ph, c < pl
    ins = ~bu & ~be
    t[bu & ~tL & (pos >= .75)] = 0
    t[bu & ~tL & (pos < .75)] = 1
    t[bu & tL & (pos >= .75)] = 2
    t[bu & tL & (pos < .75)] = 3
    t[ins & tL & ~tH & (pos >= .5)] = 4
    t[ins & tL & ~tH & (pos < .5)] = 5
    t[ins & ~tL & ~tH & (pos >= .5)] = 6
    t[ins & tL & tH & (pos >= .5)] = 7
    t[be & ~tH & (pos <= .25)] = 8
    t[be & ~tH & (pos > .25)] = 9
    t[be & tH & (pos <= .25)] = 10
    t[be & tH & (pos > .25)] = 11
    t[ins & tH & ~tL & (pos <= .5)] = 12
    t[ins & tH & ~tL & (pos > .5)] = 13
    t[ins & ~tL & ~tH & (pos < .5)] = 14
    t[ins & tL & tH & (pos < .5)] = 15
    t[0] = -1
    # structure BC (open rule, as in the Pine engines)
    isBuX = (c > ph) | ((o > ph) & ~(c < pl))
    isBeX = (c < pl) | ((o < pl) & ~(c > ph))
    nbc = ~isBuX & ~isBeX
    nbc[0] = False
    return t, pos, isBuX, isBeX, nbc

# ───────────────────────── SuperTrend 14 × 2 stall engine (MMM PRO PLUS) ─────────────────────────
def supertrend_stall(d, exit_bc_only=False, st_bc_only=False):
    """returns per bar: dir (1 bull, -1 bear), flipUp, flipDn, exitLong, exitShort (EXIT labels)."""
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    a = atr(d, 14)
    n = len(c)
    ph, pl = np.r_[np.nan, h[:-1]], np.r_[np.nan, l[:-1]]
    isBuX = (c > ph) | ((o > ph) & ~(c < pl))
    isBeX = (c < pl) | ((o < pl) & ~(c > ph))
    ub = lb = np.nan
    sdir = 1  # 1 = bear (upper band), -1 = bull
    dirs = np.zeros(n, int); st = np.full(n, np.nan)
    fu = np.zeros(n, bool); fd = np.zeros(n, bool); xl = np.zeros(n, bool); xs = np.zeros(n, bool)
    z = None  # [op, ext, side]
    prev_st = np.nan; prev_dir = 1
    for i in range(n):
        if np.isnan(a[i]):
            dirs[i] = 1; continue
        hl2 = (h[i] + l[i]) / 2
        rub, rlb = hl2 + 2 * a[i], hl2 - 2 * a[i]
        pub, plb, pdir = ub, lb, sdir
        nub = rub if (np.isnan(pub) or rub < pub or (c[i - 1] > pub and pdir == -1)) else pub
        nlb = rlb if (np.isnan(plb) or rlb > plb or (c[i - 1] < plb and pdir == 1)) else plb
        if np.isnan(a[i - 1]) if i > 0 else True:
            ndir = 1
        elif pdir == 1:
            ndir = -1 if (c[i] > nub and (not st_bc_only or isBuX[i])) else 1
        else:
            ndir = 1 if (c[i] < nlb and (not st_bc_only or isBeX[i])) else -1
        ub, lb, sdir = nub, nlb, ndir
        s = lb if sdir == -1 else ub
        st[i] = s
        up = sdir < 0
        dirs[i] = 1 if up else -1
        flip = (i > 0) and (sdir != prev_dir) and not np.isnan(prev_st)
        step = (not flip) and (not np.isnan(prev_st)) and (s > prev_st if up else s < prev_st)
        fu[i] = flip and up
        fd[i] = flip and not up
        # live zone check (made on an earlier stair candle)
        if z is not None:
            op, ext, zs = z
            if zs == -1:  # bear stall
                if c[i] < ext:
                    z = None
                elif c[i] > op and (not exit_bc_only or isBuX[i]):
                    xs[i] = True; z = None
            else:
                if c[i] > ext:
                    z = None
                elif c[i] < op and (not exit_bc_only or isBeX[i]):
                    xl[i] = True; z = None
        if flip or step:
            sd = 1 if up else -1
            z = [min(o[i], c[i]) if sd == 1 else max(o[i], c[i]), h[i] if sd == 1 else l[i], sd]
        prev_st, prev_dir = s, sdir
    return dirs, fu, fd, xl, xs

# ───────────────────────── exit event arrays ─────────────────────────
EXITS = ['X0 none', 'XO opp BC', 'XN2 2 NBC', 'XN3 3 NBC', 'XN4 4 NBC',
         'XN2A 2 NBC, one leans against', 'XN2W 2 NBC, all lean with', 'XN2R 2 NBC with a rejection wick against',
         'XSA stall EXIT any close or flip', 'XSB stall EXIT body close or flip', 'XSF SuperTrend flip only']
EXIT_MO = np.array([0, 0, 1, 2, 3, 1, 1, 1, 0, 0, 0])

def next_true(ev):
    """nxt[j] = first index >= j where ev is True (n if none)."""
    n = len(ev)
    nxt = np.full(n + 1, n, np.int64)
    for j in range(n - 1, -1, -1):
        nxt[j] = j if ev[j] else nxt[j + 1]
    return nxt

def exit_events(d):
    """returns nxt arrays shape (2 sides, X, n+1): side 0 = long, 1 = short."""
    t, pos, isBuX, isBeX, nbc = mmcb(d)
    h, l = d.high.values, d.low.values
    ph, pl = np.r_[np.nan, h[:-1]], np.r_[np.nan, l[:-1]]
    n = len(nbc)
    run = np.zeros(n, int)
    for j in range(n):
        run[j] = run[j - 1] + 1 if (nbc[j] and j > 0) else (1 if nbc[j] else 0)
    _, _, _, xlA, xsA = supertrend_stall(d, False)
    dirB, fuB, fdB, xlB, xsB = supertrend_stall(d, True)
    dirA, fuA, fdA, _, _ = supertrend_stall(d, False)
    out = np.zeros((2, len(EXITS), n + 1), np.int64)
    for s, side in enumerate((1, -1)):
        against = (pos < .5) if side == 1 else (pos > .5)
        rejA = ((h > ph) & (pos < .5)) if side == 1 else ((l < pl) & (pos > .5))
        prevA = np.r_[False, against[:-1]]
        prevR = np.r_[False, rejA[:-1]]
        two = run >= 2
        evs = [np.zeros(n, bool),
               isBeX if side == 1 else isBuX,
               run >= 2, run >= 3, run >= 4,
               two & (against | prevA),
               two & ~(against | prevA),
               two & (rejA | prevR),
               (xlA | fdA) if side == 1 else (xsA | fuA),
               (xlB | fdA) if side == 1 else (xsB | fuA),
               fdA if side == 1 else fuA]
        for x, ev in enumerate(evs):
            out[s, x] = next_true(ev)
    return out

# ───────────────────────── replay mapping ─────────────────────────
def map_replay(sig, rep, sig_tf_minutes=None):
    """for each signal bar j: first and last replay index inside it (by open time).
    sig bars start at sig.index[j]; next start = sig.index[j+1]."""
    st = sig.index.values
    rt = rep.index.values
    first = np.searchsorted(rt, st, 'left')
    nxt = np.r_[st[1:], np.datetime64('2100-01-01')]
    last = np.searchsorted(rt, nxt, 'left') - 1
    # replay bar -> signal bar
    r2s = np.searchsorted(st, rt, 'right') - 1
    return first.astype(np.int64), last.astype(np.int64), r2s.astype(np.int64)

# ───────────────────────── trade simulator ─────────────────────────
@nb.njit(cache=True)
def simulate(rO, rH, rL, rC, sFirst, sLast, r2s, sigClose, nSig,
             rows_j, rows_side, rows_L, rows_stp, rows_tgt, rows_grp, nGrp,
             RK, evN, exit_mo, W, Hmax, cost, dmin, tick, store_k, store_x):
    """rows: one per (signal, entry, stop). L = entry level (nan = market at the signal close).
    stp = absolute stop price. tgt = absolute candle TGT (nan if none) -> extra target column.
    RK = R multiples (inf = no target). Targets k: 0..len(RK)-1 = RK, len(RK) = TGT.
    evN[side, x, j] = first signal bar >= j with exit event x.
    Accumulates per (grp, k, x): n, wins, sumR, sumR2, gw, gl.  Also per grp: rows, fills."""
    K = len(RK) + 1
    X = evN.shape[1]
    acc = np.zeros((nGrp, K, X, 6))
    cnt = np.zeros((nGrp, 3))
    nR = len(rows_j)
    keep = np.full(nR, np.nan)   # stored R for (store_k, store_x)
    nRep = len(rO)
    for r in range(nR):
        j = rows_j[r]; side = rows_side[r]; L = rows_L[r]; stp = rows_stp[r]; g = rows_grp[r]
        sgn = 1.0 if side == 1 else -1.0
        cnt[g, 0] += 1
        start = sLast[j] + 1
        if start >= nRep:
            continue
        market = np.isnan(L)
        if market:
            e = sigClose[j]
            fi = sLast[j]          # filled at the close of the signal bar
            gsig = j + 1
        else:
            d0 = sgn * (L - stp)
            if d0 < dmin:
                continue
            canc = L + sgn * 2.0 * d0
            endSig = j + W
            fi = -1
            i = start
            while i < nRep and r2s[i] <= endSig:
                if side == 1:
                    if rL[i] <= L - tick:
                        e = min(L, rO[i]); fi = i; break
                    if rH[i] >= canc:
                        break
                else:
                    if rH[i] >= L + tick:
                        e = max(L, rO[i]); fi = i; break
                    if rL[i] <= canc:
                        break
                i += 1
            if fi < 0:
                continue
            gsig = r2s[fi]
        d = sgn * (e - stp)
        if d < dmin:
            continue
        cnt[g, 1] += 1
        # scan after the fill: stop index, target indices, max replay index
        endSig2 = gsig + Hmax - 1
        if endSig2 >= nSig:
            endSig2 = nSig - 1
        lastRep = sLast[endSig2]
        # stop on the fill bar (limit fills only)
        stopI = -1; stopPx = 0.0
        tI = np.full(K, -1, np.int64)
        tP = np.empty(K)
        for k in range(K - 1):
            tP[k] = e + sgn * RK[k] * d
        tg = rows_tgt[r]
        tP[K - 1] = tg if (not np.isnan(tg) and sgn * (tg - e) > 0) else np.inf * sgn
        if not market:
            if (side == 1 and rL[fi] <= stp) or (side == -1 and rH[fi] >= stp):
                stopI = fi; stopPx = stp
        i = fi + 1
        remaining = K
        while stopI < 0 and i <= lastRep and i < nRep:
            if side == 1:
                if rL[i] <= stp:
                    stopI = i; stopPx = min(rO[i], stp); break
                for k in range(K):
                    if tI[k] < 0 and rH[i] >= tP[k]:
                        tI[k] = i
            else:
                if rH[i] >= stp:
                    stopI = i; stopPx = max(rO[i], stp); break
                for k in range(K):
                    if tI[k] < 0 and rL[i] <= tP[k]:
                        tI[k] = i
            i += 1
        # outcome per target and exit
        for x in range(X):
            ej = evN[0 if side == 1 else 1, x, min(gsig + exit_mo[x], nSig)]
            if ej > endSig2:
                ej = endSig2   # time exit
            exI = sLast[ej]
            exPx = sigClose[ej]
            for k in range(K):
                if k == K - 1 and np.isinf(tP[k]):
                    continue
                endI = exI; px = exPx
                tk = tI[k]
                if tk >= 0 and tk <= endI:
                    endI = tk; px = tP[k]
                if stopI >= 0 and stopI <= endI:
                    px = stopPx
                R = sgn * (px - e) / d - cost / d
                a = acc[g, k, x]
                a[0] += 1; a[2] += R; a[3] += R * R
                if R > 0:
                    a[1] += 1; a[4] += R
                else:
                    a[5] -= R
                if k == store_k and x == store_x:
                    keep[r] = R
    return acc, cnt, keep

def stats_frame(acc, cnt, grp_labels, RK, min_n=30):
    """flatten the accumulator into a DataFrame."""
    K = acc.shape[1]; X = acc.shape[2]
    tn = [f'1:{int(v) if v == int(v) else v}' if np.isfinite(v) else 'no target' for v in RK] + ['TGT']
    recs = []
    for g in range(acc.shape[0]):
        for k in range(K):
            for x in range(X):
                n, w, s, s2, gw, gl = acc[g, k, x]
                if n < 1:
                    continue
                avg = s / n
                sd = np.sqrt(max((s2 - n * avg * avg) / (n - 1), 0)) if n > 1 else np.nan
                recs.append(dict(**grp_labels[g], target=tn[k], exit=EXITS[x], signals=int(cnt[g, 0]),
                                 trades=int(n), fill=cnt[g, 1] / max(cnt[g, 0], 1),
                                 WR=w / n, PF=gw / gl if gl > 0 else np.nan, avgR=avg,
                                 t=avg / sd * np.sqrt(n) if sd and sd > 0 else np.nan,
                                 _w=w, _s=s, _s2=s2, _gw=gw, _gl=gl, _sig=cnt[g, 0], _fill=cnt[g, 1]))
    return pd.DataFrame(recs)
