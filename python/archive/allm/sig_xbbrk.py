"""XB break signals by kind (Oct 30 2026), opposite-side XB engine (x 4.0 default), x zone engine for the kind:
CDLx / CDSx = the XB break close is also a zone-engine flip · LDx / SDx = also a continuation ·
small cdlx / cdsx = internal break against the engine trend · ldx / sdx = internal, with the trend.
Zone for the grid = the new FVA: bear break -> first NBC body bottom .. XB high · bull -> XB low .. first NBC body top.
Also the foundational break stats (BCs before the first opposite BC / first NBC, points after the break)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/xb')
from xbzone2 import blocks
from sig_edge import zone
from mdata import bars, SPEC

MK = ['NQ', 'MNQ', 'MES', 'MGC', 'MCL']
TFS = ['5m', '15m', '1h', '4h']

def kinds(o, h, l, c):
    Z = zone(o, h, l, c)
    out = []
    for B in blocks(o, h, l, c, True):
        e = B['end']
        if e < 0: continue
        s = B['brk']; fn = B['fn']
        prev = Z['side'][e - 1]
        if Z['ev'][e] != 0 and Z['evd'][e] == s:
            k = 'CDLx/CDSx' if Z['ev'][e] == 1 else 'LDx/SDx'
        else:
            k = ('ldx' if prev == 1 else 'cdlx') if s == 1 else ('sdx' if prev == -1 else 'cdsx')
            k = 'ldx/sdx (internal)' if k in ('ldx', 'sdx') else 'cdlx/cdsx (internal)'
        if s == -1: zt, zb = B['H'], min(o[fn], c[fn])
        else: zt, zb = max(o[fn], c[fn]), B['L']
        out.append((e, s, k, zt, zb, B['H'], B['L']))
    return out

def after(o, h, l, c, e, s, cap=200):
    """BCs in the break direction after the break before the first opposite BC / before the first NBC,
    and points moved: MFE until the first opposite BC, close-to-close after 1, 3, 5, 10 candles."""
    n = len(c); same = 0; firstNBC = None; oppAt = None; mfe = 0.0
    for j in range(e + 1, min(e + 1 + cap, n)):
        bu = c[j] > h[j-1]; be = c[j] < l[j-1]
        mfe = max(mfe, (h[j] - c[e]) if s == 1 else (c[e] - l[j]))
        if (s == 1 and be) or (s == -1 and bu): oppAt = j; break
        if (s == 1 and bu) or (s == -1 and be):
            if firstNBC is None: same += 1
        elif firstNBC is None: firstNBC = j
    bcs_before_nbc = same
    bcs_before_opp = 0
    for j in range(e + 1, (oppAt or min(e + 1 + cap, n))):
        if (s == 1 and c[j] > h[j-1]) or (s == -1 and c[j] < l[j-1]): bcs_before_opp += 1
    mv = [s * (c[min(e + k, n - 1)] - c[e]) for k in (1, 3, 5, 10)]
    return bcs_before_opp, bcs_before_nbc, mfe, (oppAt - e) if oppAt else np.nan, *mv

rows, desc = [], []
for m in MK:
    tick = SPEC[m]['tick']
    for tf in TFS:
        try: d = bars(m, tf)
        except Exception as ex: print('skip', m, tf, ex); continue
        o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
        for e, s, k, zt, zb, XH, XL in kinds(o, h, l, c):
            if e + 2 >= len(c) or zt <= zb: continue
            far = zt if s == -1 else zb
            for strat in (k, 'all XB breaks'):
                rows.append(dict(m=m, strat=f'XB {strat} {tf}', tf=tf, i=e, t=d.index[e], side=s, ztop=zt, zbot=zb, ntype='mkt', npx=c[e],
                                 nsl=far + (2 * tick if s == -1 else -2 * tick), nrr=np.nan, nwait=10, note=k))
            a = after(o, h, l, c, e, s)
            desc.append((m, tf, k, d.index[e], s, h[e] - l[e], zt - zb) + a)
        print(m, tf, len(rows), flush=True)
S = pd.DataFrame(rows)
for m in MK:
    S[S.m == m].drop(columns='m').reset_index(drop=True).to_parquet(f'sig_xbbrk_{m}.parquet')
pd.DataFrame(desc, columns=['m', 'tf', 'kind', 'time', 'side', 'brkRange', 'fvaH', 'bcsBeforeOpp', 'bcsBeforeNBC', 'mfeToOpp', 'candlesToOpp', 'pts1', 'pts3', 'pts5', 'pts10']).to_parquet('xbbrk_desc.parquet')
print(S.groupby(['m','strat']).size().to_string())
