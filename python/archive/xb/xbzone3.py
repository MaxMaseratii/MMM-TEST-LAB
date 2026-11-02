"""Do the XB zones work as Max predicts? (Oct 30 2026)
Prediction while the XB lives: BUY in XBS (XB low -> balanced bottom), SELL in XBB (balanced top -> XB high),
never trade inside the Balanced Zone. After the break: SELL the BeFVA (first NBC body bottom -> XB high),
BUY the BuFVA (first NBC body top -> XB low); the FVA dies on a close through it.
Two engines: ALL (every BC + NBC = XB, 4.0 logic) and OPP (XB only from a BC against the last BC).
Every entry x every stop x every target x every exit. Graded on the finest bars, stop wins ties, 1 pt cost.
A limit fills only on a TRUE touch: the 1m bar opens on the predicted side and trades through the level."""
import sys, time, numpy as np, pandas as pd
from numba import njit
import core
from core import raw, Fine, bars, TICK, COST
core.TFM['D'] = 1440

HOLD = 100        # structure candles a trade may live
FLIFE = 100       # structure candles an FVA order may wait
TG = np.array([1.0, 2.0, 3.0])
XN = ['stop/target', 'violation close', 'next session open']

def blocks(o, h, l, c, opp):
    n = len(c); out = []
    wait = live = False; last = 0
    exH = exL = 0.0; exI = -1; exD = 0; B = None
    for i in range(1, n):
        bu = c[i] > h[i-1]; be = c[i] < l[i-1]; bc = bu or be; dr = 1 if bu else -1
        xo = bc and (not opp or last == 0 or dr != last)
        if live:
            if c[i] > B['H'] or c[i] < B['L']:
                B['end'] = i; B['brk'] = 1 if c[i] > B['H'] else -1
                out.append(B); live = False; wait = xo
                if xo: exH, exL, exI, exD = h[i], l[i], i, dr
            else:
                B['H'] = max(B['H'], h[i]); B['L'] = min(B['L'], l[i])
                B['bt'] = max(B['bt'], o[i], c[i]); B['bb'] = min(B['bb'], o[i], c[i])
                B['hist'].append((i, B['H'], B['L'], B['bt'], B['bb']))
        elif wait:
            if bc: exH, exL, exI, exD = h[i], l[i], i, dr
            else:
                live = True; wait = False
                B = dict(bc=exI, dir=exD, fn=i, H=max(exH, h[i]), L=min(exL, l[i]),
                         bt=max(o[i], c[i]), bb=min(o[i], c[i]), end=-1, brk=0)
                B['hist'] = [(i, B['H'], B['L'], B['bt'], B['bb'])]
        elif xo:
            wait = True; exH, exL, exI, exD = h[i], l[i], i, dr
        if bc: last = dr
    return out

def next_open(t_ns):
    """first fine bar at or after the next session open: 02:00, 08:00, 09:30 New York (data is NY time)."""
    t = pd.to_datetime(t_ns); m = (t.hour * 60 + t.minute).values; day = t.normalize()
    nxt = np.full(len(m), 120 + 1440)
    for op in (570, 480, 120):
        nxt = np.where(m < op, op, nxt)
    tg = day.values + (nxt * 60 * 1_000_000_000).astype('timedelta64[ns]')
    return np.searchsorted(t_ns, tg.astype(np.int64), 'left')

@njit(cache=True)
def trade(fo, fh, fl, fc, nxt, ks, ke, lv, side, stp, kv, pv, kmax, tg, out):
    """limit, level lv[k-ks] per fine bar; fills on a TRUE touch (bar opens on the right side and trades through).
    stp[k-ks] = stop distance at that bar. kv / pv = violation exit bar and price (-1 = none).
    out[t, x] = R after cost for target t and exit x. returns 1 if filled."""
    n = len(fh); kf = -1
    for k in range(ks, min(ke + 1, n)):
        x = lv[k - ks]
        if x != x: continue
        if side == 1 and fo[k] > x and fl[k] <= x: kf = k; break
        if side == -1 and fo[k] < x and fh[k] >= x: kf = k; break
    if kf < 0: return 0
    ep = lv[kf - ks]; risk = stp[kf - ks]
    if not (risk > 0): return 0
    sl = ep - side * risk; cost = COST / risk
    ks2 = nxt[kf]
    for t in range(len(tg)):
        tp = ep + side * risk * tg[t]
        kS = -1; kT = -1; kend = -1
        for j in range(kf, n):
            if j > kmax: kend = j; break
            if (side == 1 and fl[j] <= sl) or (side == -1 and fh[j] >= sl): kS = j; break
            if j > kf and ((side == 1 and fh[j] >= tp) or (side == -1 and fl[j] <= tp)): kT = j; break
        if kS < 0 and kT < 0 and kend < 0: kend = n - 1
        for x in range(3):
            best = 1 << 60; r = 0.0
            if kS >= 0: best = kS; r = -1.0
            if kT >= 0: best = kT; r = tg[t]
            if x == 1 and kv >= kf and kv < best: best = kv; r = side * (pv - ep) / risk
            if x == 2 and ks2 > kf and ks2 < n and ks2 <= best: best = ks2; r = side * (fo[ks2] - ep) / risk
            if best == (1 << 60): r = side * (fc[kend - 1] - ep) / risk
            out[t, x] = r - cost
    return 1

@njit(cache=True)
def react(fo, fh, fl, fc, ks, ke, lv, side, X, kmax):
    """first TRUE touch of the level, then which comes first: +X in the predicted side (1) or -X (0). -1 = no touch / neither."""
    n = len(fh); kf = -1
    for k in range(ks, min(ke + 1, n)):
        x = lv[k - ks]
        if x != x: continue
        if side == 1 and fo[k] > x and fl[k] <= x: kf = k; break
        if side == -1 and fo[k] < x and fh[k] >= x: kf = k; break
    if kf < 0: return -1
    ep = lv[kf - ks]
    for j in range(kf + 1, min(kmax + 1, n)):
        up = fh[j] >= ep + X; dn = fl[j] <= ep - X
        if side == 1:
            if dn: return 0
            if up: return 1
        else:
            if up: return 0
            if dn: return 1
    return -1

def run(period, tf, opp):
    d1 = raw()['fresh5' if (period == 'fresh' and tf == '5m') else period]; F = Fine(d1)
    d = bars(d1, tf)
    o, h, l, c, atr = d.open.values, d.high.values, d.low.values, d.close.values, d.atr.values
    n = len(d)
    ke = np.searchsorted(F.t, d.tend.values.astype('datetime64[ns]').astype(np.int64), 'left')
    nxt = next_open(F.t)
    X50 = 50.0
    rows = []; rx = []
    XD = 0
    def put(kind, ent, sd, stn, lvA, stA, ks_, ke_, kv, pv, kmax, t_):
        out = np.zeros((3, 3))
        if trade(F.o, F.h, F.l, F.c, nxt, ks_, ke_, lvA, sd, stA, kv, pv, kmax, TG, out):
            for ti in range(3):
                for xi in range(3):
                    rows.append((period, tf, opp, kind, ent, sd, stn, TG[ti], XN[xi], t_, out[ti, xi], XD))
    for B in blocks(o, h, l, c, opp):
        e = B['end']
        if e < 0 or e + 2 >= n: continue
        s = B['brk']; fn = B['fn']; tE = d.index[e]; XD = B['dir']
        Hh = B['hist']
        # ---------- A. while the XB lives (orders from the first NBC close to the break candle) ----------
        k_s = ke[Hh[0][0]]; k_e = ke[e] - 1; m = k_e - k_s + 1
        if m > 0:
            idx = np.searchsorted(ke[[x[0] for x in Hh]], np.arange(k_s, k_e + 1), 'right') - 1
            arr = np.array([x[1:] for x in Hh])[idx]
            XH, XL, bt, bb = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
            kmax = ke[min(e + HOLD, n - 1)] - 1
            a = atr[e] if atr[e] == atr[e] else 50.0
            ent = {   # name: side, level, far edge for the 'XB edge' stop
                'BUY XBS top (balanced bottom)': (1, bb, XL),
                'BUY XBS middle': (1, (bb + XL) / 2, XL),
                'BUY XB low': (1, XL, None),
                'BUY balanced middle (no-trade zone)': (1, (bt + bb) / 2, XL),
                'BUY XBB bottom (wrong zone)': (1, bt, XL),
                'SELL XBB bottom (balanced top)': (-1, bt, XH),
                'SELL XBB middle': (-1, (bt + XH) / 2, XH),
                'SELL XB high': (-1, XH, None),
                'SELL balanced middle (no-trade zone)': (-1, (bt + bb) / 2, XH),
                'SELL XBS top (wrong zone)': (-1, bb, XH),
                'SELL XBS middle': (-1, (bb + XL) / 2, XH),
                'BUY XBB middle': (1, (bt + XH) / 2, XL),
            }
            for en, (sd, lv, far) in ent.items():
                lv = lv.astype(float)
                # violation = the XB breaks against the trade (a close past the far side), at the break candle close
                kv = ke[e] - 1 if s == -sd else -1
                pv = c[e]
                stops = {'S50': np.full(m, 50.0), 'ATR 1.5x': np.full(m, max(1.5 * a, 4.0))}
                if far is not None: stops['past XB edge'] = np.maximum(np.abs(lv - far) + 2 * TICK, 4.0)
                for stn, stA in stops.items():
                    put('A inside XB', en, sd, stn, lv, stA.astype(float), k_s, k_e, kv, pv, kmax, tE)
                for X in (25.0, 50.0):
                    r = react(F.o, F.h, F.l, F.c, k_s, k_e, lv, sd, X, kmax)
                    if r >= 0: rx.append((period, tf, opp, 'A inside XB', en, X, r, XD))
        # ---------- B. after the break: FVA ----------
        if s == -1: near, far = min(o[fn], c[fn]), B['H']     # BeFVA: first NBC body bottom -> XB high
        else: near, far = max(o[fn], c[fn]), B['L']           # BuFVA: first NBC body top -> XB low
        if (far - near) * (-s) <= 0: continue
        died = -1
        for j in range(e + 1, min(e + 1 + FLIFE, n)):
            if (s == -1 and c[j] > far) or (s == 1 and c[j] < far): died = j; break
        kl = ke[died] - 1 if died >= 0 else ke[min(e + FLIFE, n - 1)] - 1
        ks_ = ke[e]; mm = kl - ks_ + 1
        if mm <= 0: continue
        kv = kl if died >= 0 else -1; pv = c[died] if died >= 0 else 0.0
        kmax = ke[min(e + HOLD, n - 1)] - 1
        a = atr[e] if atr[e] == atr[e] else 50.0
        nm = 'BeFVA' if s == -1 else 'BuFVA'
        sideW = 'SELL' if s == -1 else 'BUY'
        mid = (near + far) / 2
        for en, lvv in ((f'{sideW} {nm} near edge (NBC body)', near), (f'{sideW} {nm} middle', mid), (f'{sideW} {nm} far edge (XB {"high" if s == -1 else "low"})', far)):
            stops = {'S50': 50.0, 'ATR 1.5x': max(1.5 * a, 4.0)}
            if abs(lvv - far) > 0.01: stops['past FVA far edge'] = max(abs(lvv - far) + 2 * TICK, 4.0)
            for stn, sp in stops.items():
                put('B FVA after break', en, s, stn, np.full(mm, lvv), np.full(mm, sp), ks_, kl, kv, pv, kmax, tE)
            for X in (25.0, 50.0):
                r = react(F.o, F.h, F.l, F.c, ks_, kl, np.full(mm, lvv), s, X, kmax)
                if r >= 0: rx.append((period, tf, opp, 'B FVA after break', en, X, r, XD))
    T = pd.DataFrame(rows, columns=['period', 'tf', 'opp', 'kind', 'entry', 'side', 'stop', 'tgt', 'exit', 'time', 'R', 'xbdir'])
    X = pd.DataFrame(rx, columns=['period', 'tf', 'opp', 'kind', 'entry', 'X', 'win', 'xbdir'])
    return T, X

if __name__ == '__main__':
    Ts, Xs = [], []
    for opp in (True,):
        for period in ('old', 'fresh'):
            for tf in ('5m', '15m', '1h', '4h', 'D'):
                t0 = time.time(); T, X = run(period, tf, opp)
                Ts.append(T); Xs.append(X)
                print('OPP' if opp else 'ALL', period, tf, len(T), len(X), round(time.time() - t0), 's', flush=True)
    pd.concat(Ts).to_parquet('zone3_trades.parquet'); pd.concat(Xs).to_parquet('zone3_react.parquet')
