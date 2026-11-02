"""New Xpander Block engine (Max, Oct 30 2026), closed candles, grow-with-wicks.
XB = expander BC + the candles that close back inside its high/low (high/low grow with wicks).
Balanced zone = highest / lowest open-close of the candles after the BC (the negotiation).
XBB (upper) = balanced top -> XB high (sell area) · XBS (lower) = XB low -> balanced bottom (buy area).
Break = a close above the XB high (bull) / below the XB low (bear).
BuFVA = first NBC low -> its body top · BeFVA = first NBC body bottom -> its high."""
import numpy as np

def blocks(o, h, l, c):
    n = len(c)
    out = []
    zWait = False; zLive = False
    exH = exL = 0.0; exI = -1; exD = 0
    for i in range(1, n):
        bu = c[i] > h[i-1]; be = c[i] < l[i-1]; bc = bu or be
        if zLive:
            if c[i] > B['H'] or c[i] < B['L']:
                B['end'] = i; B['brk'] = 1 if c[i] > B['H'] else -1
                out.append(B)
                zLive = False; zWait = bc
                if bc:
                    exH, exL, exI, exD = h[i], l[i], i, (1 if bu else -1)
            else:
                B['H'] = max(B['H'], h[i]); B['L'] = min(B['L'], l[i])
                B['bt'] = max(B['bt'], o[i], c[i]); B['bb'] = min(B['bb'], o[i], c[i])
                B['hist'].append((i, B['H'], B['L'], B['bt'], B['bb']))
        elif zWait:
            if bc:
                exH, exL, exI, exD = h[i], l[i], i, (1 if bu else -1)
            else:
                zLive = True; zWait = False
                B = dict(bc=exI, dir=exD, fn=i, H=max(exH, h[i]), L=min(exL, l[i]),
                         bt=max(o[i], c[i]), bb=min(o[i], c[i]), end=-1, brk=0)
                B['hist'] = [(i, B['H'], B['L'], B['bt'], B['bb'])]
        elif bc:
            zWait = True; exH, exL, exI, exD = h[i], l[i], i, (1 if bu else -1)
    return out
