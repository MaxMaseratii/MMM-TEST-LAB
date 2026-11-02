"""Candles for the MMM PRO PLUS points test (Nov 2 2026).
Same data as every other MMM market test (allm/mdata.fine): NQ 1m Dec 2022 - Dec 2025, MNQ / MES / MGC / MCL Dec 2025 - Oct 28 2026.
bars(m, tfm): tfm-minute candles built from the finest bars, only on days whose finest bars are <= tfm.
Each candle also gets 'delta' = sum over its finest sub-bars of (+vol if close>open, -vol if close<open) (Pine: 1m lower TF delta)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/allm')
import mdata

END = pd.Timestamp('2026-10-28 23:59')
MK = {'NQ': ['NQ', 'MNQ'], 'ES': ['MES'], 'GC': ['MGC'], 'CL': ['MCL']}
SPEC = {'NQ': dict(stop=50.0, cost=1.0, tick=0.25, pv=2.0),
        'ES': dict(stop=20.0, cost=0.5, tick=0.25, pv=5.0),
        'GC': dict(stop=12.0, cost=0.2, tick=0.1, pv=10.0),
        'CL': dict(stop=0.50, cost=0.02, tick=0.01, pv=100.0)}
_C = {}


def bars_one(src, tfm):
    f = mdata.fine(src)
    f = f[f.index <= END]
    f = f[f.res <= tfm]
    if tfm >= 1440:
        raise ValueError
    key = f.index.floor(f'{tfm}min') if tfm <= 60 else (f.index - pd.Timedelta(hours=18)).floor(f'{tfm}min') + pd.Timedelta(hours=18)
    sgn = np.sign(f.close.values - f.open.values)
    f = f.assign(dl=sgn * f.volume.values)
    g = f.groupby(key)
    d = pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(),
                      'volume': g.volume.sum(), 'delta': g.dl.sum()})
    d['src'] = src
    return d


def series(m, tfm):
    """list of candle frames to run the engine on (NQ and MNQ run apart: no price seam). Each has column 'per' = P1 / P2.
    NQ: NQ 2022-25 = P1, MNQ 2026 = P2. ES / gold / crude: first half vs second half of this chart's own trading days."""
    out = []
    for s in MK[m]:
        d = bars_one(s, tfm)
        if len(d) < 300: continue
        if m == 'NQ':
            d['per'] = 'P1' if s == 'NQ' else 'P2'
            if s == 'NQ': d = d[d.index < pd.Timestamp('2025-11-30 18:00')]
        else:
            sd = mdata.sday(d.index)
            days = np.sort(sd.unique())
            cut = days[len(days) // 2]
            d['per'] = np.where(sd < cut, 'P1', 'P2')
        out.append(d)
    return out
