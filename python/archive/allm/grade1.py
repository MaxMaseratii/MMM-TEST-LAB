"""Grade ONE rule per signal, trade by trade (same logic as grid.kernel). Returns a DataFrame of trades."""
import numpy as np, pandas as pd
from numba import njit
import grid
from mdata import SPEC

@njit(cache=True)
def one(si, sside, EL, EW, SL, tc, th, tl, ke, ci, fo, fh, fl, fc, nxt, nbar, tgt, xmode, cost, minr, HOLD, out):
    nf = len(fh)
    for q in range(len(si)):
        i = si[q]; s = sside[q]; k0 = ke[i]
        out[q, 0] = np.nan
        if k0 >= nf: continue
        lv = EL[q]
        if lv != lv: continue
        mk = EW[q] == 0 or (s == 1 and lv >= tc[i]) or (s == -1 and lv <= tc[i])
        if mk: lv = tc[i]
        kf = -1
        if mk: kf = k0
        else:
            kexp = ke[min(i + EW[q], nbar - 1)] - 1
            for k in range(k0, min(kexp + 1, nf)):
                if (s == 1 and fl[k] <= lv) or (s == -1 and fh[k] >= lv):
                    kf = k; break
        if kf < 0: continue
        ep = lv; cf = ci[kf]
        kmax = ke[min(cf + HOLD, nbar - 1)] - 1
        sl = SL[q]
        if sl != sl: continue
        risk = s * (ep - sl)
        if not (risk >= minr): continue
        ksx = nxt[kf]
        tp = ep + s * risk * tgt
        r = 0.0; kx = -1
        for j in range(kf, nf):
            if xmode == 2 and j == ksx and j > kf:
                r = s * (fo[j] - ep) / risk; kx = j; break
            if j > kmax:
                r = s * (fc[j - 1] - ep) / risk; kx = j; break
            if (s == 1 and fl[j] <= sl) or (s == -1 and fh[j] >= sl):
                r = -1.0; kx = j; break
            if j > kf or mk:
                if (s == 1 and fh[j] >= tp) or (s == -1 and fl[j] <= tp):
                    r = tgt; kx = j; break
        if kx < 0: continue
        out[q, 0] = r - cost / risk; out[q, 1] = risk; out[q, 2] = kf; out[q, 3] = kx; out[q, 4] = ep

def trades(m, tf, S, e, st, t, x):
    """e/st/x use the grid's numbering. Returns trades with time, R, risk pts."""
    sp = SPEC[m]
    S = S.reset_index(drop=True).copy(); S['sgid'] = 0
    P = grid.prepare(m, tf, S)
    EL = P['EL'][:, e].copy(); EW = P['EW'][:, e].copy()
    if st == 1: SL = EL.copy()   # filled below once the entry price is known (market = close)
    ep_guess = np.where((EW == 0) | ((S.side.values == 1) & (EL >= P['tc'][P['si']])) | ((S.side.values == -1) & (EL <= P['tc'][P['si']])), P['tc'][P['si']], EL)
    if st == 1: SL = ep_guess - S.side.values * sp['s50']
    elif st == 2: SL = ep_guess - S.side.values * 1.5 * P['atr'][P['si']]
    else: SL = P['SLF'][:, st].copy()
    out = np.full((len(S), 5), np.nan)
    one(P['si'], P['sside'], EL, EW.astype(np.int64), SL.astype(float), P['tc'], P['th'], P['tl'], P['ke'], P['ci'], P['fo'], P['fh'], P['fl'], P['fc'],
        P['nxt'], P['nbar'], float(grid.TGT[t]), x, sp['cost'], sp['s50'] * 0.08, grid.HOLD, out)
    T = S[['t', 'side']].copy(); T['R'] = out[:, 0]; T['risk'] = out[:, 1]; T['ep'] = out[:, 4]; T['per'] = P['sper']
    return T.dropna(subset=['R'])
