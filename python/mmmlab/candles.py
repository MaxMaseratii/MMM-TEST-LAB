"""CANDLES: the MMM candle rules and the foundation stats.

bc(o, h, l, c)       +1 BuBC (green close above the prior high), -1 BeBC (red close below the prior low), 0 NBC.
atr_rma(h, l, c, n)  Pine ta.atr (RMA).   atr_sma(...) simple average ATR (used for zones).
foundation(o, h, l, c, I, s)   for events at bars I with side s (+1 / -1), the foundation numbers Max always wants:
     bc_before_opp = same-side BCs after the event before the first opposite BC
     bc_before_nbc = same-side BCs in a row right after the event before the first NBC
     p1 / p5 / p10 = points moved in the event direction after 1 / 5 / 10 candles, up5 = share up after 5."""
import numpy as np
from numba import njit


def bc(o, h, l, c):
    hp = np.r_[np.nan, h[:-1]]; lp = np.r_[np.nan, l[:-1]]
    return np.where((c > hp) & (c > o), 1, np.where((c < lp) & (c < o), -1, 0)).astype(np.int64)


@njit(cache=True)
def atr_rma(h, l, c, n=14):
    m = len(c); a = np.full(m, np.nan)
    if m < n: return a
    tr = np.empty(m); tr[0] = h[0] - l[0]
    for i in range(1, m): tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
    s = 0.0
    for i in range(n): s += tr[i]
    a[n - 1] = s / n
    for i in range(n, m): a[i] = (a[i - 1] * (n - 1) + tr[i]) / n
    return a


def atr_sma(h, l, c, n=14):
    cp = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.c_[h - l, np.abs(h - cp), np.abs(l - cp)], axis=1)
    return np.convolve(tr, np.ones(n) / n, 'full')[:len(tr)] * np.where(np.arange(len(tr)) >= n - 1, 1, np.nan)


@njit(cache=True)
def _found(c, b, I, s):
    n = len(c); out = np.full((len(I), 5), np.nan)
    for k in range(len(I)):
        i = I[k]; sd = s[k]
        a = 0
        for j in range(i + 1, min(n, i + 500)):
            if b[j] == -sd: break
            if b[j] == sd: a += 1
        z = 0
        for j in range(i + 1, min(n, i + 500)):
            if b[j] == sd: z += 1
            else: break
        out[k, 0] = a; out[k, 1] = z
        for q, w in ((2, 1), (3, 5), (4, 10)):
            if i + w < n: out[k, q] = sd * (c[i + w] - c[i])
    return out


def foundation(o, h, l, c, I, s):
    F = _found(c.astype(np.float64), bc(o, h, l, c), np.asarray(I, np.int64), np.asarray(s, np.int64))
    return dict(n=len(I), bc_before_opp=np.nanmean(F[:, 0]), bc_before_nbc=np.nanmean(F[:, 1]),
                p1=np.nanmean(F[:, 2]), p5=np.nanmean(F[:, 3]), p10=np.nanmean(F[:, 4]), up5=np.nanmean(F[:, 3] > 0))
