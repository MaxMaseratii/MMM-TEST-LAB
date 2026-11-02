"""Signals for FVA.A / FVA.B (FVA Break 4.x), the GMU (all charts), the new XB FVA (after the break) and the XB zones (XBS / XBB)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/fva'); sys.path.insert(0, '/home/claude/xb')
import replica4
from xbeng import blocks
from mdata import bars, SPEC

def _row(strat, tf, i, t, side, zt, zb, ntype, npx, nsl, nrr, nwait, note):
    return dict(strat=strat, tf=tf, i=int(i), t=t, side=int(side), ztop=float(zt), zbot=float(zb), ntype=ntype, npx=float(npx), nsl=float(nsl), nrr=nrr, nwait=nwait, note=note)

def fva_ab(m):
    d = bars(m, '1h'); s50 = SPEC[m]['s50']
    c, h, l = d.close.values, d.high.values, d.low.values
    tr = np.maximum(h - l, np.maximum(np.abs(h - np.r_[c[0], c[:-1]]), np.abs(l - np.r_[c[0], c[:-1]])))
    atr = pd.Series(tr).rolling(14).mean().bfill().values
    st = replica4.run(d)
    rt = {(x['i'], x['long'], x['etype']): x for x in st if x['etype'].endswith(' RT')}
    out = []
    for x in st:
        if x['etype'] not in ('FailC', 'Fail+C'): continue
        i = x['i']; sd = 1 if x['long'] else -1
        r = rt.get((i, x['long'], x['etype'] + ' RT'))
        if r is None: continue
        far = x['sl'] + sd * replica4.BUF       # the box side away from the trade
        zt, zb = (r['ep'], far) if sd == 1 else (far, r['ep'])
        if x['etype'] == 'FailC':
            out.append(_row('FVA.A', '1h', i, d.index[i], sd, zt, zb, 'mkt', c[i], c[i] - sd * atr[i], 6.0, 0, 'box fail'))
        else:
            hr = d.index[i].hour
            if hr >= 18 or hr <= 1:     # Asia: 1h candle opens 18:00-01:00
                out.append(_row('FVA.B', '1h', i, d.index[i], sd, zt, zb, 'mkt', c[i], c[i] - sd * s50, 1.5, 0, 'Asia flip-zone fail'))
    return out

def gmu(m, tf):
    d = bars(m, tf); s50 = SPEC[m]['s50']; tick = SPEC[m]['tick']
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    out = []
    for i in range(2, len(d) - 1):
        a, b = i - 2, i - 1
        if c[b] > h[a] and l[i] - h[a] >= 2 * tick: s = 1
        elif c[b] < l[a] and l[a] - h[i] >= 2 * tick: s = -1
        else: continue
        zt, zb = max(h[a:i + 1]), min(l[a:i + 1])
        out.append(_row('GMU ' + tf, tf, i, d.index[i], s, zt, zb, 'mkt', c[i], c[i] - s * s50, 2.0, 0, 'c3 close'))
    return out

def xb(m, tf):
    d = bars(m, tf); s50 = SPEC[m]['s50']
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    out = []
    for B in blocks(o, h, l, c):
        fn = B['fn']
        # XB zones at the block birth (first NBC close): BUY in XBS, SELL in XBB
        H0, L0, bt0, bb0 = B['hist'][0][1:]
        if bb0 > L0:
            out.append(_row('XB zone ' + tf, tf, fn, d.index[fn], 1, bb0, L0, 'lmt', bb0, bb0 - s50, 2.0, 10, 'XBS buy'))
        if H0 > bt0:
            out.append(_row('XB zone ' + tf, tf, fn, d.index[fn], -1, H0, bt0, 'lmt', bt0, bt0 + s50, 2.0, 10, 'XBB sell'))
        e = B['end']
        if e < 0 or e >= len(d) - 1: continue
        s = B['brk']
        if s == -1: zb, zt = min(o[fn], c[fn]), h[fn]; near = zb
        else: zb, zt = l[fn], max(o[fn], c[fn]); near = zt
        if zt <= zb: continue
        out.append(_row('XB FVA ' + tf, tf, e, d.index[e], s, zt, zb, 'lmt', near, near - s * s50, 2.0, 50, 'FVA after break'))
    return out

def signals(m):
    rows = fva_ab(m)
    for tf in ('5m', '15m', '1h', '4h'):
        rows += gmu(m, tf) + xb(m, tf)
    return pd.DataFrame(rows)

if __name__ == '__main__':
    for m in ('NQ', 'MNQ', 'MES', 'MGC', 'MCL'):
        S = signals(m); S.to_parquet(f'sig_misc_{m}.parquet')
        print(m, S.groupby('strat').size().to_dict(), flush=True)
