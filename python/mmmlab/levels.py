"""LEVELS: her "boring levels" toolkit, reusable for any test (Nov 2 2026).
vp(lo, hi, vol, row)        volume profile -> (POC, VAH, VAL) at 70% value area; each bar's volume spread over its range.
day_levels(sym, market)     per trading day: H, L, POC / VAH / VAL (NY 9:30-16:00 session; gold = full session), London H / L (02-08 ET),
                            previous week POC / VAH / VAL (wPOC ...), and the previous day's values (pH, pL, pPOC, pVAH, pVAL).
zones(sym, market, tf)      supply / demand zones: displacement candle body >= 1 ATR closing beyond the prior candle (strict = 1.5 ATR out
                            of a tight 3-candle range); zone = the candle to the left, body high to low; tA = live from, tD = dead at.
vwap_anchor(d, mask)        running VWAP restarting where mask is True (NY 9:30, session 18:00, week).
react(o, h, l, c, ks, L, s, eps)   touch-and-reject finder at a level: returns {'close': (bar, swing, touch bar), 'aggr': ...}.
Lv(lines, zones, vwaps, tol)       level set: .near(lo, hi, bar, own) = families stacked nearby, .target(ep, s, risk, bar) = next level.
The full test that uses these: archive/bf/lvtest.py (IB + Tokyo + level reactions)."""
import numpy as np, pandas as pd
from . import data as D

BIN = {'NQ': 2.0, 'ES': 0.5, 'GC': 0.5, 'CL': 0.01}


def vp(lo, hi, vol, b):
    if len(lo) == 0 or np.nansum(vol) <= 0: return (np.nan,) * 3
    p0 = np.floor(lo.min() / b) * b
    nb = int((hi.max() - p0) / b) + 1
    i0 = np.clip(((lo - p0) / b).astype(np.int64), 0, nb - 1); i1 = np.clip(((hi - p0) / b).astype(np.int64), 0, nb - 1)
    w = vol / (i1 - i0 + 1)
    df = np.zeros(nb + 1); np.add.at(df, i0, w); np.add.at(df, i1 + 1, -w)
    hs = np.cumsum(df)[:nb]
    pc = int(np.argmax(hs)); tot = hs.sum(); a = b_ = pc; acc = hs[pc]
    while acc < 0.7 * tot and (a > 0 or b_ < nb - 1):
        up = hs[b_ + 1] if b_ < nb - 1 else -1; dn = hs[a - 1] if a > 0 else -1
        if up >= dn: b_ += 1; acc += up
        else: a -= 1; acc += dn
    return p0 + (pc + 0.5) * b, p0 + (b_ + 1) * b, p0 + a * b       # POC, VAH, VAL


def day_levels(src, m):
    f = D.fine(src)
    sd = D.sday(f.index); mn = f.index.hour * 60 + f.index.minute
    lo, hi, v = f.low.values, f.high.values, f.volume.values.astype(float)
    b = BIN[m]
    days = np.sort(sd.unique())
    rows = {}
    g = pd.Series(np.arange(len(f))).groupby(sd.values)
    for dd, ix in g:
        ix = ix.values
        mm = mn[ix]
        ny = ix[(mm >= 570) & (mm < 960)]
        lon = ix[(mm >= 120) & (mm < 480)]
        sess = ix if m == 'GC' else ny
        P = vp(lo[sess], hi[sess], v[sess], b)
        rows[dd] = dict(H=hi[ix].max(), L=lo[ix].min(), POC=P[0], VAH=P[1], VAL=P[2],
                        lonH=hi[lon].max() if len(lon) else np.nan, lonL=lo[lon].min() if len(lon) else np.nan)
    DL = pd.DataFrame(rows).T.astype(float); DL.index = pd.DatetimeIndex(DL.index); DL = DL.sort_index()
    wk = pd.DatetimeIndex(sd).to_period('W-FRI')
    W = {}
    for k, ix in pd.Series(np.arange(len(f))).groupby(wk.values):
        ix = ix.values; W[k] = vp(lo[ix], hi[ix], v[ix], b)
    DL['wk'] = pd.DatetimeIndex(DL.index).to_period('W-FRI')
    prevW = {k: W.get(k - 1, (np.nan,) * 3) for k in DL.wk.unique()}
    DL['wPOC'] = [prevW[k][0] for k in DL.wk]; DL['wVAH'] = [prevW[k][1] for k in DL.wk]; DL['wVAL'] = [prevW[k][2] for k in DL.wk]
    for col in ('H', 'L', 'POC', 'VAH', 'VAL'):
        DL['p' + col] = DL[col].shift(1)
    return DL


def zones(src, m, tf):
    z = D.bars(src, tf)
    o, h, l, c = (z[k].values for k in ('open', 'high', 'low', 'close'))
    cp = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.c_[h - l, np.abs(h - cp), np.abs(l - cp)], axis=1)
    atr = pd.Series(tr).rolling(14).mean().values
    tick = D.SPEC[m]['tick']
    sd = D.sday(z.index); dpos = pd.Series(np.arange(len(sd.unique())), index=np.sort(sd.unique()))[sd].values
    out = []
    n = len(c)
    for j in range(4, n):
        a = atr[j - 1]
        if not np.isfinite(a) or a <= 0: continue
        body = c[j] - o[j]
        for s in (1, -1):
            if s * body < 1.0 * a: continue
            if not ((s == 1 and c[j] > h[j - 1]) or (s == -1 and c[j] < l[j - 1])): continue
            strict = s * body >= 1.5 * a and (h[j - 3:j].max() - l[j - 3:j].min()) <= 2.0 * a
            top = max(o[j - 1], c[j - 1]); bot = min(o[j - 1], c[j - 1])
            if top - bot < 2 * tick: top, bot = h[j - 1], l[j - 1]
            # dead: first close beyond the far side on this chart, max 20 trading days
            kmax = min(n, j + 1 + 20 * (1440 // tf))
            seg = c[j + 1:kmax]
            br = np.where(seg < bot)[0] if s == 1 else np.where(seg > top)[0]
            kd = j + 1 + br[0] if len(br) else kmax - 1
            kd = min(kd, int(np.searchsorted(dpos, dpos[j] + 20)) if dpos[j] + 20 <= dpos[-1] else n - 1)
            out.append((z.index[j] + pd.Timedelta(minutes=tf), z.index[min(kd, n - 1)] + pd.Timedelta(minutes=tf), top, bot, s, tf, strict))
    return pd.DataFrame(out, columns=['tA', 'tD', 'top', 'bot', 's', 'tf', 'strict'])


def vwap_anchor(d, anchor_mask):
    """running VWAP that restarts at each True in anchor_mask"""
    tp = ((d.high + d.low + d.close) / 3).values; v = d.volume.values.astype(float)
    grp = np.cumsum(anchor_mask)
    pv = pd.Series(tp * v).groupby(grp).cumsum().values; vv = pd.Series(v).groupby(grp).cumsum().values
    return np.where(vv > 0, pv / np.maximum(vv, 1e-9), tp)


def react(o, h, l, c, ks, L, s, eps, far=None, maxw=12):
    """ks: consecutive window bar indices. Long at support L (s=1): touch = low <= L+eps with the prior close above L (approach from above).
    Episode = up to maxw candles from the touch. Trigger 'close' = a candle in trade color closing back beyond L; 'aggr' = also beyond the
    prior candle's high / low. Returns {trig: (j, swing extreme, touch bar)}, first of each. A zone dies on a close beyond its far side."""
    if s == 1: cand = np.where((l[ks] <= L + eps) & (c[ks - 1] > L))[0]
    else: cand = np.where((h[ks] >= L - eps) & (c[ks - 1] < L))[0]
    res = {}; pn = 0
    for p in cand:
        if p < pn: continue
        k0 = ks[p]; ex = l[k0] if s == 1 else h[k0]; endp = min(len(ks), p + maxw); q = p
        while q < endp:
            j = ks[q]
            ex = min(ex, l[j]) if s == 1 else max(ex, h[j])
            if far is not None and ((s == 1 and c[j] < far) or (s == -1 and c[j] > far)): return res
            if ((s == 1 and c[j] > o[j] and c[j] > L) or (s == -1 and c[j] < o[j] and c[j] < L)):
                if 'close' not in res: res['close'] = (j, ex, k0)
                if 'aggr' not in res and ((s == 1 and c[j] > h[j - 1]) or (s == -1 and c[j] < l[j - 1])): res['aggr'] = (j, ex, k0)
                if len(res) == 2: return res
            q += 1
        pn = q
    return res


class Lv:
    """level set for one day / window: static lines + zones + dynamic VWAPs"""
    def __init__(self, lines, zs, vws, tol):
        self.lines = lines          # list of (name, fam, price)
        self.zs = zs                # DataFrame rows of active zones with kA, kD
        self.vws = vws              # list of (name, array)
        self.tol = tol

    def near(self, lo, hi, j, own):
        """families with a level within tol of [lo, hi] at bar j (own family excluded)"""
        t = self.tol; f = set()
        for nm, fam, p in self.lines:
            if fam != own and np.isfinite(p) and p >= lo - t and p <= hi + t: f.add(fam)
        for r in self.zs.itertuples():
            fam = f'Z{r.tf}'
            if fam != own and r.kA <= j < r.kD and r.top >= lo - t and r.bot <= hi + t: f.add(fam)
        for nm, arr in self.vws:
            if nm != own and np.isfinite(arr[j]) and lo - t <= arr[j] <= hi + t: f.add(nm)
        return f

    def target(self, ep, s, risk, j):
        ps = [p for _, _, p in self.lines if np.isfinite(p)]
        for r in self.zs.itertuples():
            if r.kA <= j < r.kD: ps += [r.top, r.bot]
        ps = np.array(ps)
        ok = ps[s * (ps - ep) >= risk] if len(ps) else ps
        if len(ok) == 0: return None
        return float(ok[np.argmin(np.abs(ok - ep))])
