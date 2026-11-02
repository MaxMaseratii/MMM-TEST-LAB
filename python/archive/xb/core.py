"""Core for the GMU ladder + new Xpander Block (XB) tests.
Bars are built from 1m data (raw.pkl: old = NQ 1m Dec 2022-Dec 2025, fresh = MNQ 1m 2026 days).
All trades are graded on 1m bars: stop wins ties, target only from the 1m bar after the fill, 1 pt cost."""
import sys, pickle, numpy as np, pandas as pd
from numba import njit
sys.path.insert(0, '/home/claude/lez'); sys.path.insert(0, '/home/claude/ten')
from data import rs
from common import ctype, family, lean

TICK = 0.25
TFM = {'5m': 5, '15m': 15, '1h': 60, '4h': 240}
COST = 1.0
_R = None
def raw():
    global _R
    if _R is None:
        _R = pickle.load(open('/home/claude/xb/raw2.pkl', 'rb'))
    return _R

class Fine:
    def __init__(self, d1):
        self.t = d1.index.values.astype('datetime64[ns]').astype(np.int64)
        self.o = d1.open.values.astype(np.float64); self.h = d1.high.values.astype(np.float64)
        self.l = d1.low.values.astype(np.float64); self.c = d1.close.values.astype(np.float64)

def bars(d1, tf):
    d = rs(d1, tf)
    d['tend'] = d.index + pd.Timedelta(minutes=TFM[tf])
    tr = pd.concat([d.high - d.low, (d.high - d.close.shift()).abs(), (d.low - d.close.shift()).abs()], axis=1).max(axis=1)
    d['atr'] = tr.rolling(14).mean()
    return d

def rs_key(d, tf):
    if tf in ('5m', '15m', '1h'):
        return d.index.floor({'5m': '5min', '15m': '15min', '1h': '60min'}[tf])
    if tf == '4h':
        return (d.index - pd.Timedelta(hours=18)).floor('4h') + pd.Timedelta(hours=18)
    raise ValueError(tf)

@njit(cache=True)
def grade(ft, fh, fl, fc, k0, kexp, kmax, side, lvl, market, stop_pts, rr):
    """side 1 long / -1 short. market: fill at lvl at bar k0 (price = signal close).
    limit: fill when price trades through lvl between k0 and kexp; cancelled if target level is hit first.
    returns (R after cost, filled flag, fill index, exit code: 1 tp, -1 sl, 0 time)."""
    n = len(fh)
    risk = stop_pts
    ep = lvl
    sl = ep - side * risk
    tp = ep + side * risk * rr
    k = k0
    kf = -1
    if market == 1:
        kf = k0
    else:
        while k < n and k <= kexp:
            if side == 1:
                if fl[k] <= ep:
                    kf = k; break
                if fh[k] >= tp:
                    return 0.0, 0, -1, 0
            else:
                if fh[k] >= ep:
                    kf = k; break
                if fl[k] <= tp:
                    return 0.0, 0, -1, 0
            k += 1
        if kf < 0:
            return 0.0, 0, -1, 0
    cost = COST / risk
    for j in range(kf, n):
        if j > kmax:
            x = fc[j - 1]
            return side * (x - ep) / risk - cost, 1, kf, 0
        if side == 1:
            slh = fl[j] <= sl
            tph = fh[j] >= tp
        else:
            slh = fh[j] >= sl
            tph = fl[j] <= tp
        if slh:
            return -1.0 - cost, 1, kf, -1
        if tph and (j > kf or market == 1):
            return rr - cost, 1, kf, 1
    return 0.0, 0, -1, 0

def stats(R):
    R = np.asarray(R, dtype=float)
    n = len(R)
    if n == 0:
        return dict(n=0, wr=None, pf=None, avg=None, t=None)
    w = R[R > 0].sum(); l = -R[R < 0].sum()
    sd = R.std(ddof=1) if n > 1 else 0
    return dict(n=n, wr=round(100 * (R > 0).mean(), 1), pf=round(w / l, 2) if l > 0 else None,
                avg=round(R.mean(), 3), t=round(R.mean() / sd * np.sqrt(n), 2) if sd > 0 else None)

@njit(cache=True)
def grade_path(ft, fh, fl, fc, ks, ke, lv, sp, side, rr, kmax):
    """limit whose level (lv[k-ks]) and stop distance (sp[k-ks]) can change per 1m bar, live ks..ke.
    returns (R, filled, kfill)."""
    n = len(fh)
    kf = -1
    for k in range(ks, min(ke + 1, n)):
        x = lv[k - ks]
        if x != x:
            continue
        if (side == 1 and fl[k] <= x) or (side == -1 and fh[k] >= x):
            kf = k; break
    if kf < 0:
        return 0.0, 0, -1
    ep = lv[kf - ks]; risk = sp[kf - ks]
    sl = ep - side * risk; tp = ep + side * risk * rr
    cost = COST / risk
    for j in range(kf, n):
        if j > kmax:
            return side * (fc[j - 1] - ep) / risk - cost, 1, kf
        if side == 1:
            slh = fl[j] <= sl; tph = fh[j] >= tp
        else:
            slh = fh[j] >= sl; tph = fl[j] <= tp
        if slh:
            return -1.0 - cost, 1, kf
        if tph and j > kf:
            return rr - cost, 1, kf
    return 0.0, 0, -1
