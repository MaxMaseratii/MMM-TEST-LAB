"""Drop-in replacement for the old allm/mdata.py, reading the mmmlab data pack.
Lets the archived engines (sig_edge, sig_fva, sig_misc, grid, ...) run unchanged: put this folder first on sys.path."""
import numpy as np, pandas as pd
from mmmlab import data as _D
SPEC = {'NQ': dict(s50=50.0, cost=1.0, tick=0.25, pv=2.0), 'MNQ': dict(s50=50.0, cost=1.0, tick=0.25, pv=2.0),
        'MES': dict(s50=20.0, cost=0.5, tick=0.25, pv=5.0), 'MGC': dict(s50=12.0, cost=0.2, tick=0.1, pv=10.0),
        'MCL': dict(s50=0.50, cost=0.02, tick=0.01, pv=100.0)}
TFM = {'1m': 1, '5m': 5, '15m': 15, '1h': 60, '4h': 240, 'D': 1440, 'W': 10080}
_C = {}
sday = _D.sday


def fine(m):
    return _D.fine(m, cut=False)


def _key(ix, tf):
    if tf in ('1m', '5m', '15m', '1h'):
        return ix.floor({'1m': '1min', '5m': '5min', '15m': '15min', '1h': '60min'}[tf])
    if tf == '4h': return (ix - pd.Timedelta(hours=18)).floor('4h') + pd.Timedelta(hours=18)
    if tf == 'D': return sday(ix) - pd.Timedelta(hours=6)
    if tf == 'W':
        s = sday(ix); wk = s - pd.to_timedelta(s.weekday, unit='D'); return wk - pd.Timedelta(hours=6)
    raise ValueError(tf)


def bars(m, tf):
    k = (m, tf)
    if k in _C: return _C[k]
    f = fine(m)
    if tf in ('1m', '5m', '15m'): f = f[f.res <= TFM[tf]]
    g = f.groupby(_key(f.index, tf))
    d = pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(), 'volume': g.volume.sum()})
    d['tend'] = d.index + pd.Timedelta(minutes=min(TFM[tf], 1440 if tf != 'W' else 10080))
    if tf == 'D': d['tend'] = d.index + pd.Timedelta(hours=23)
    if tf == 'W': d['tend'] = d.index + pd.Timedelta(days=5, hours=23)
    _C[k] = d
    return d


def period(m, t):
    t = pd.DatetimeIndex(t)
    if m == 'NQ': return np.array(['P1'] * len(t))
    if m == 'MNQ': return np.array(['P2'] * len(t))
    return np.where(t < pd.Timestamp('2026-06-01'), 'P1', 'P2')
