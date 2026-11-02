"""Port of the MMM Zone engine (x, Concepts Pro+) f_zoneEngine, gate off.
grow = G1 (inside wick pushes the edge), expMode True = EXPANDER box (born from the expander BC range),
expMode False = CONTRACTION box (born from the first inside candle range)."""
import numpy as np

def zone_engine(o, h, l, c, v, grow=True, expMode=False):
    n = len(c)
    ev_type = np.zeros(n, int); ev_dir = np.zeros(n, int); ev_tier = np.zeros(n, int)
    brk_p = np.full(n, np.nan); tn_new = np.full(n, np.nan)
    # live box info per bar (after processing the bar)
    z_live = np.zeros(n, bool); z_h = np.full(n, np.nan); z_l = np.full(n, np.nan); z_t0 = np.full(n, -1)
    # box that ENDED on this bar (closed outside)
    end_f = np.zeros(n, bool); end_h = np.full(n, np.nan); end_l = np.full(n, np.nan); end_t0 = np.full(n, -1)
    side_arr = np.zeros(n, int)
    zWait = False; exH = exL = np.nan; exT = -1
    zLive = False; bxH = bxL = np.nan; bxT = -1; bxId = 0
    side = 0; tier = 0; tnP = np.nan; tnT = -1
    pP = np.nan; pT = -1; pId = -1; pLive = False
    rP = np.nan; rT = -1; rId = -1; rLive = False
    legHi = legLo = np.nan; legHiT = legLoT = -1
    pbHi = pbLo = np.nan; pbHiT = pbLoT = -1
    for i in range(1, n):
        ph, pl = h[i - 1], l[i - 1]
        bu = c[i] > ph; be = c[i] < pl; bc = bu or be
        formed = False
        endF = False; endH = endL = np.nan; endT = -1
        if zLive:
            if c[i] > bxH or c[i] < bxL:
                endF = True; endH = bxH; endL = bxL; endT = bxT
                if bxId == pId: pLive = False
                if bxId == rId: rLive = False
                zLive = False; zWait = bc
                if bc:
                    exH, exL, exT = h[i], l[i], i
            else:
                if grow:
                    bxH = max(bxH, h[i]); bxL = min(bxL, l[i])
        elif zWait:
            if bc:
                exH, exL, exT = h[i], l[i], i
            else:
                zLive = True; zWait = False; formed = True; bxId += 1; bxT = exT
                if expMode:
                    bxH = max(exH, h[i]) if grow else exH
                    bxL = min(exL, l[i]) if grow else exL
                else:
                    bxH, bxL = h[i], l[i]
        elif bc:
            zWait = True; exH, exL, exT = h[i], l[i], i
        if zLive and bxId == pId:
            pP = bxH if side == 1 else bxL
        if zLive and bxId == rId:
            rP = bxL if side == 1 else bxH
        if side != 0:
            if np.isnan(legHi) or h[i] > legHi: legHi, legHiT = h[i], i
            if np.isnan(legLo) or l[i] < legLo: legLo, legLoT = l[i], i
        if not np.isnan(pP):
            if np.isnan(pbHi) or h[i] > pbHi: pbHi, pbHiT = h[i], i
            if np.isnan(pbLo) or l[i] < pbLo: pbLo, pbLoT = l[i], i
        evType = 0; evDir = 0; nTnP = np.nan; nTnT = -1; bp = np.nan
        if side == 1:
            if c[i] < tnP:
                evType, evDir, bp = 1, -1, tnP
                hasP = not np.isnan(pP)
                nTnP = pP if hasP else legHi; nTnT = pT if hasP else legHiT
            elif not np.isnan(pP) and c[i] > pP:
                evType, evDir, bp = 2, 1, pP
                hasR = not np.isnan(rP)
                nTnP = rP if hasR else pbLo; nTnT = rT if hasR else pbLoT
            elif not np.isnan(rP) and c[i] < rP:
                rP = np.nan; rT = -1; rId = -1; rLive = False
        elif side == -1:
            if c[i] > tnP:
                evType, evDir, bp = 1, 1, tnP
                hasP = not np.isnan(pP)
                nTnP = pP if hasP else legLo; nTnT = pT if hasP else legLoT
            elif not np.isnan(pP) and c[i] < pP:
                evType, evDir, bp = 2, -1, pP
                hasR = not np.isnan(rP)
                nTnP = rP if hasR else pbHi; nTnT = rT if hasR else pbHiT
            elif not np.isnan(rP) and c[i] > rP:
                rP = np.nan; rT = -1; rId = -1; rLive = False
        elif endF:
            evType = 1
            evDir = 1 if c[i] > endH else -1
            bp = endH if evDir == 1 else endL
            nTnP = endL if evDir == 1 else endH; nTnT = endT
        if evType != 0:
            side = evDir
            tier = 1 if evType == 1 else tier + 1
            tnP, tnT = nTnP, nTnT
            pP = np.nan; pT = -1; pId = -1; pLive = False
            rP = np.nan; rT = -1; rId = -1; rLive = False
            legHi, legHiT, legLo, legLoT = h[i], i, l[i], i
            pbHi = pbLo = np.nan
        if formed:
            if side != 0 and np.isnan(pP):
                pId = bxId; pLive = True; pP = bxH if side == 1 else bxL; pT = bxT
                pbHi, pbHiT, pbLo, pbLoT = bxH, bxT, bxL, bxT
            elif side != 0 and not pLive and np.isnan(rP):
                rId = bxId; rLive = True; rP = bxL if side == 1 else bxH; rT = bxT
        ev_type[i], ev_dir[i], ev_tier[i], brk_p[i] = evType, evDir, tier if evType else 0, bp
        if evType: tn_new[i] = tnP
        z_live[i], z_h[i], z_l[i], z_t0[i] = zLive, bxH, bxL, bxT
        end_f[i], end_h[i], end_l[i], end_t0[i] = endF, endH, endL, endT
        side_arr[i] = side
    return dict(ev_type=ev_type, ev_dir=ev_dir, ev_tier=ev_tier, brk_p=brk_p, tn_new=tn_new, z_live=z_live, z_h=z_h, z_l=z_l,
                z_t0=z_t0, end_f=end_f, end_h=end_h, end_l=end_l, end_t0=end_t0, side=side_arr)
