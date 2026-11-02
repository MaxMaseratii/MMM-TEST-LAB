"""XB range trades (Max, Oct 30 2026): enter at a zone of a LIVE Xpander Block, target the other side.
SELL at XBB (balanced top / XBB middle / XB high) -> targets: balanced middle, balanced bottom (other side of the
balanced zone), XBS middle, XB low.  BUY at XBS mirrors it.  Reference: enter at the balanced middle.
Odds measured from the first TRUE touch (1m bar opens on the right side and trades through the level):
 - each target hit before the VIOLATION (a structure candle closes beyond the XB edge against the trade)
 - drawdown (MAE, pts and % of the XB height) until the target or the violation
 - trades: exit at target or at the violation close · or a hard stop 2 ticks past the XB edge · or a 50 pt stop.
XB engine: opposite side only (x 4.0 default). NQ 1m 2022-25 (P1) -> MNQ 2026 (P2). Timeframes 15m, 1h, 4h, D."""
import time, numpy as np, pandas as pd
from numba import njit
import core
from core import raw, Fine, bars, TICK, COST
from xbzone2 import blocks
core.TFM['D'] = 1440

ENT = ['XBB bottom (balanced top)', 'XBB middle', 'XB high (far edge)', 'Balanced middle (reference)']
TGT = ['balanced middle', 'balanced far side', 'far zone middle', 'XB far edge']

@njit(cache=True)
def walk(fo, fh, fl, fc, ks, ke, lv, side, kend, tg, edge, out):
    """first true touch of lv[k-ks] in ks..ke. Then walk to kend (last 1m bar of the block) and record:
    out[0] fill bar, out[1] entry, out[2+j] bar where target j (price tg[j] at touch) is hit (-1),
    out[6+j] MAE (pts) until target j or kend, out[10] bar where the hard stop (edge + 2 ticks) is hit (-1),
    out[11] bar where a 50 pt stop is hit (-1), out[12] overall MAE to kend. returns 1 if touched."""
    n = len(fh); kf = -1
    for k in range(ks, min(ke + 1, n)):
        x = lv[k - ks]
        if x != x: continue
        if side == 1 and fo[k] > x and fl[k] <= x: kf = k; break
        if side == -1 and fo[k] < x and fh[k] >= x: kf = k; break
    if kf < 0: return 0
    ep = lv[kf - ks]; ix = kf - ks
    out[0] = kf; out[1] = ep
    hs = edge[ix] - side * 2 * TICK
    for j in range(4): out[2 + j] = -1
    out[10] = -1; out[11] = -1
    mae = 0.0
    for k in range(kf, min(kend + 1, n)):
        adv = (fh[k] - ep) if side == -1 else (ep - fl[k])
        if adv > mae: mae = adv
        # the fill bar: only adverse moves after the fill count for stops; targets need a later bar
        if out[10] < 0 and ((side == -1 and fh[k] >= hs) or (side == 1 and fl[k] <= hs)): out[10] = k
        if out[11] < 0 and ((side == -1 and fh[k] >= ep + 50) or (side == 1 and fl[k] <= ep - 50)): out[11] = k
        for j in range(4):
            if out[2 + j] < 0:
                t = tg[j, ix]
                if (side == -1 and t < ep) or (side == 1 and t > ep):
                    if k > kf and ((side == -1 and fl[k] <= t) or (side == 1 and fh[k] >= t)):
                        out[2 + j] = k; out[6 + j] = mae
    for j in range(4):
        if out[2 + j] < 0: out[6 + j] = mae
    out[12] = mae
    return 1

def run(period, tf):
    d1 = raw()['fresh5' if (period == 'fresh' and tf == '5m') else period]; F = Fine(d1)
    d = bars(d1, tf)
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    n = len(d)
    ke = np.searchsorted(F.t, d.tend.values.astype('datetime64[ns]').astype(np.int64), 'left')
    rows = []
    for B in blocks(o, h, l, c, True):
        e = B['end']
        if e < 0 or e + 1 >= n: continue
        Hh = B['hist']
        k_s = ke[Hh[0][0]]; k_e = ke[e] - 1; m = k_e - k_s + 1
        if m <= 0: continue
        idx = np.searchsorted(ke[[x[0] for x in Hh]], np.arange(k_s, k_e + 1), 'right') - 1
        arr = np.array([x[1:] for x in Hh])[idx]
        XH, XL, bt, bb = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
        bm = (bt + bb) / 2
        for side in (-1, 1):
            if side == -1:
                lvls = [bt, (bt + XH) / 2, XH, bm]
                tg = np.vstack([bm, bb, (bb + XL) / 2, XL]); edge = XH
            else:
                lvls = [bb, (bb + XL) / 2, XL, bm]
                tg = np.vstack([bm, bt, (bt + XH) / 2, XH]); edge = XL
            viol = B['brk'] == -side         # the block broke against the trade
            for ei, lv in enumerate(lvls):
                out = np.zeros(13)
                if not walk(F.o, F.h, F.l, F.c, k_s, k_e, lv.astype(float), side, k_e, tg.astype(float), edge.astype(float), out): continue
                kf = int(out[0]); ix = kf - k_s; ep = out[1]
                height = XH[ix] - XL[ix]
                rec = dict(xbdir=B['dir'], period=period, tf=tf, side='SELL' if side == -1 else 'BUY', entry=ENT[ei], viol=viol,
                           height=height, ep=ep, edge=edge[ix], vclose=c[e], kv=k_e, kfill=kf,
                           hs=out[10], s50=out[11], mae=out[12], time=d.index[e])
                for j in range(4):
                    t = tg[j, ix]
                    ok = (side == -1 and t < ep) or (side == 1 and t > ep)
                    rec[f'tg{j}'] = t if ok else np.nan
                    rec[f'hit{j}'] = out[2 + j] if ok else np.nan
                    rec[f'mae{j}'] = out[6 + j]
                rows.append(rec)
    return pd.DataFrame(rows)

if __name__ == '__main__':
    R = []
    for period in ('old', 'fresh'):
        for tf in ('5m', '15m', '1h', '4h', 'D'):
            t0 = time.time(); X = run(period, tf); R.append(X)
            print(period, tf, len(X), round(time.time() - t0), 's', flush=True)
    pd.concat(R).to_parquet('xbrange3.parquet')
