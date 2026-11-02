"""Tests of the new Xpander Block: inside zones (before the break) and FVA entries (after the break)."""
import sys, time, numpy as np, pandas as pd
from core import *
from xbeng import blocks

LIFE = 50; HOLD = 100; CONF = 10

def gmu_c2(o, h, l, c):
    """side of the GMU whose c2 is bar b (gap confirmed by bar b+1); 0 if none."""
    n = len(c); g = np.zeros(n, int)
    for b in range(1, n - 1):
        a, i = b - 1, b + 1
        if c[b] > h[a] and l[i] - h[a] >= 2 * TICK: g[b] = 1
        elif c[b] < l[a] and l[a] - h[i] >= 2 * TICK: g[b] = -1
    return g

def run(period, tf):
    d1 = raw()['fresh5' if (period == 'fresh' and tf == '5m') else period]; F = Fine(d1)
    d = bars(d1, tf)
    o, h, l, c, atr = d.open.values, d.high.values, d.low.values, d.close.values, d.atr.values
    n = len(d)
    ks = np.searchsorted(F.t, d.index.values.astype('datetime64[ns]').astype(np.int64), 'left')   # first 1m of bar i
    ke = np.searchsorted(F.t, d.tend.values.astype('datetime64[ns]').astype(np.int64), 'left')    # first 1m after bar i
    g = gmu_c2(o, h, l, c)
    B = blocks(o, h, l, c)
    zrows, frows, brows = [], [], []
    last_g = {1: None, -1: None}   # last GMU c2 index per side
    gb = 0
    for blk in B:
        e = blk['end']
        if e < 0 or e + 2 >= n: continue
        s = blk['brk']; fn = blk['fn']
        # ---------- A. inside the block: limits live from the first NBC close to the break candle ----------
        H = blk['hist']    # (i, H, L, bt, bb) known at close of i
        k_s = ke[H[0][0]]; k_e = ke[e] - 1       # live during candles fn+1 .. e
        m = k_e - k_s + 1
        if m > 0:
            idx = np.searchsorted(ke[[x[0] for x in H]], np.arange(k_s, k_e + 1), 'right') - 1
            arr = np.array([x[1:] for x in H])[idx]    # H L bt bb per 1m bar
            Hh, Ll, bt, bb = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
            kmax = ke[min(e + HOLD, n - 1)] - 1
            zones = {
                'BUY XBS top (bal. bottom)': (1, bb, bb - Ll),
                'BUY XBS mid': (1, (bb + Ll) / 2, (bb + Ll) / 2 - Ll),
                'BUY XB low (XD)': (1, Ll, None),
                'SELL XBB bottom (bal. top)': (-1, bt, Hh - bt),
                'SELL XBB mid': (-1, (bt + Hh) / 2, Hh - (bt + Hh) / 2),
                'SELL XB high (XP)': (-1, Hh, None),
                'BUY balanced mid': (1, (bt + bb) / 2, None),
                'SELL balanced mid': (-1, (bt + bb) / 2, None),
            }
            for zn, (sd, lv, dist) in zones.items():
                for stn in ('S50', 'XB'):
                    if stn == 'XB':
                        if dist is None: continue
                        sp = np.maximum(dist + 2 * TICK, 4.0)
                    else:
                        sp = np.full(m, 50.0)
                    R, f, kf = grade_path(F.t, F.h, F.l, F.c, k_s, k_e, lv.astype(float), sp.astype(float), sd, 2.0, kmax)
                    if f:
                        zrows.append((period, tf, d.index[e], blk['dir'], s, zn, stn, R))
        # ---------- B. after the break ----------
        if s == -1: fb, ft_ = min(o[fn], c[fn]), h[fn]; near, far = fb, ft_
        else: fb, ft_ = l[fn], max(o[fn], c[fn]); near, far = ft_, fb
        mid = (fb + ft_) / 2
        # FVA life and touch
        tch = -1; died = -1
        for j in range(e + 1, min(e + 1 + LIFE, n)):
            if tch < 0 and ((s == -1 and h[j] >= near) or (s == 1 and l[j] <= near)): tch = j
            if (s == -1 and c[j] > far) or (s == 1 and c[j] < far): died = j; break
        endlife = died if died >= 0 else min(e + LIFE, n - 1)
        # GMU relation
        brkG = g[e] == s
        og = last_g[-s]; oppState = 'none'
        if og is not None:
            op = o[og]
            killed = [j for j in range(og + 2, e + 1) if (s == -1 and c[j] < op) or (s == 1 and c[j] > op)]
            oppState = 'broken by this break' if killed and killed[0] == e else ('broken before' if killed else 'still alive')
        rel = 'cont' if s == blk['dir'] else 'rev'
        tcl = 'no touch'
        if tch >= 0:
            if (s == -1 and c[tch] > far) or (s == 1 and c[tch] < far): tcl = 'closed through'
            elif (s == -1 and c[tch] >= near) or (s == 1 and c[tch] <= near): tcl = 'closed inside'
            else: tcl = 'closed back out'
        # deeper: after the touch, did price close inside later / break the FVA within 20 candles?
        broke20 = died >= 0 and tch >= 0 and died - tch <= 20
        # MFE / MAE (pts) from the near edge after touch, 20 candles
        mfe = mae = np.nan
        if tch >= 0:
            j2 = min(tch + 20, n - 1)
            if s == -1:
                mfe = near - l[tch:j2 + 1].min(); mae = h[tch:j2 + 1].max() - near
            else:
                mfe = h[tch:j2 + 1].max() - near; mae = near - l[tch:j2 + 1].min()
        brows.append((period, tf, d.index[e], blk['dir'], s, rel, brkG, oppState, tch - e if tch >= 0 else -1, tcl, died >= 0,
                      broke20, mfe, mae, ft_ - fb, h[e] - l[e]))
        tags = (rel, brkG, oppState, tcl)
        kmax = ke[min(e + HOLD, n - 1)] - 1
        fsp = max(abs(far - near) + 2 * TICK, 4.0)
        def add(en, stn, R, f):
            if f: frows.append((period, tf, d.index[e], s) + tags + (en, stn, R))
        # E0 market at the break close
        for stn, sp in (('S50', 50.0), ('ATR', max(1.5 * atr[e], 2.0) if atr[e] == atr[e] else 50.0)):
            R, f, kf, ex = grade(F.t, F.h, F.l, F.c, ke[e], ke[e], kmax, s, c[e], 1, sp, 2.0); add('E0 market at break close', stn, R, f)
        # E1/E2/E3 limits live while the FVA lives
        kl = ke[endlife] - 1 if died < 0 else ks[died] + 0   # stop working when the killing candle starts... (kept to its open)
        kl = ke[endlife] - 1
        for en, lv in (('E1 limit FVA near edge', near), ('E2 limit FVA mid', mid), ('E3 limit FVA far edge', far)):
            for stn, sp in (('S50', 50.0), ('FVA', fsp if en != 'E3 limit FVA far edge' else None)):
                if sp is None: continue
                if en == 'E2 limit FVA mid' and stn == 'FVA': sp = max(abs(far - mid) + 2 * TICK, 4.0)
                mm = kl - ke[e] + 1
                if mm <= 0: continue
                R, f, kf = grade_path(F.t, F.h, F.l, F.c, ke[e], kl, np.full(mm, lv), np.full(mm, sp), s, 2.0, kmax)
                add(en, stn, R, f)
        # E4 touch, then first BC in the break direction (FVA alive) within CONF candles -> market at its close
        if tch >= 0:
            for j in range(tch, min(tch + CONF + 1, n - 1)):
                if died >= 0 and j >= died: break
                if (s == -1 and c[j] < l[j-1]) or (s == 1 and c[j] > h[j-1]):
                    for stn, sp in (('S50', 50.0), ('FVA', max(abs(far - c[j]) + 2 * TICK, 4.0))):
                        R, f, kf, ex = grade(F.t, F.h, F.l, F.c, ke[j], ke[j], kmax, s, c[j], 1, sp, 2.0); add('E4 touch then BC (close)', stn, R, f)
                    break
            # E5 touch candle closes back out (rejection) -> market at its close
            if tcl == 'closed back out':
                for stn, sp in (('S50', 50.0), ('FVA', max(abs(far - c[tch]) + 2 * TICK, 4.0))):
                    R, f, kf, ex = grade(F.t, F.h, F.l, F.c, ke[tch], ke[tch], kmax, s, c[tch], 1, sp, 2.0); add('E5 touch, close back out (close)', stn, R, f)
        # E6/E7 honest GMU versions: the break candle is c2 of a GMU, known at the close of c3 (= e+1)
        if brkG and e + 1 < n - 1:
            c3 = e + 1
            for stn, sp in (('S50', 50.0), ('ATR', max(1.5 * atr[e], 2.0) if atr[e] == atr[e] else 50.0)):
                R, f, kf, ex = grade(F.t, F.h, F.l, F.c, ke[c3], ke[c3], kmax, s, c[c3], 1, sp, 2.0); add('E6 break is GMU: market at c3 close', stn, R, f)
            alive = died < 0 or died > c3
            if alive and kl > ke[c3]:
                mm = kl - ke[c3] + 1
                for stn, sp in (('S50', 50.0), ('FVA', fsp)):
                    R, f, kf = grade_path(F.t, F.h, F.l, F.c, ke[c3], kl, np.full(mm, near), np.full(mm, sp), s, 2.0, kmax)
                    add('E7 break is GMU: limit FVA near edge after c3', stn, R, f)
        # update GMU memory up to e (c2 at index b confirmed at b+1 <= e)
        while gb < e:
            if g[gb] != 0: last_g[g[gb]] = gb
            gb += 1
    Z = pd.DataFrame(zrows, columns=['period', 'tf', 'time', 'xbdir', 'brk', 'zone', 'stop', 'R'])
    Fd = pd.DataFrame(frows, columns=['period', 'tf', 'time', 'side', 'rel', 'brkGMU', 'oppGMU', 'touchClose', 'entry', 'stop', 'R'])
    Bd = pd.DataFrame(brows, columns=['period', 'tf', 'time', 'xbdir', 'brk', 'rel', 'brkGMU', 'oppGMU', 'touchAfter', 'touchClose', 'fvaDied', 'broke20', 'mfe', 'mae', 'fvaH', 'brkRange'])
    return Z, Fd, Bd, len(B)

if __name__ == '__main__':
    Zs, Fs, Bs = [], [], []
    for period in ('old', 'fresh'):
        for tf in ('5m', '15m', '1h', '4h'):
            t = time.time()
            Z, Fd, Bd, nb = run(period, tf)
            Zs.append(Z); Fs.append(Fd); Bs.append(Bd)
            print(period, tf, 'blocks', nb, len(Z), len(Fd), round(time.time() - t), 's', flush=True)
    pd.concat(Zs).to_parquet('xb_zone.parquet'); pd.concat(Fs).to_parquet('xb_fva.parquet'); pd.concat(Bs).to_parquet('xb_brk.parquet')
