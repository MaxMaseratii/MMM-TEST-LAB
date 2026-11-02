"""Market data for the all-strategy full-grid test.
fine(market): finest bars per day (1m, else 5m, else 15m), NY time index, columns open high low close volume, plus 'res' (bar minutes).
bars(market, tf): candles on tf built from fine bars ONLY on days whose finest bars are <= tf.
Markets: NQ (NQ 1m Dec 2022 - Dec 2025) · MNQ, MES, MGC, MCL (Dec 2025 - Oct 2026).
Periods: NQ = 'P1' (all) · MNQ = 'P2' (all) · MES/MGC/MCL: P1 = before 2026-06-01, P2 = from 2026-06-01."""
import pickle, glob, os, numpy as np, pandas as pd
LIB = '/home/claude/data5/'
LIB2 = '/home/claude/rt/lib/data/'
SPEC = {  # stop 50-pt equivalent, cost per trade, tick, $ per point (micro)
    'NQ': dict(s50=50.0, cost=1.0, tick=0.25, pv=2.0),
    'MNQ': dict(s50=50.0, cost=1.0, tick=0.25, pv=2.0),
    'MES': dict(s50=20.0, cost=0.5, tick=0.25, pv=5.0),
    'MGC': dict(s50=12.0, cost=0.2, tick=0.1, pv=10.0),
    'MCL': dict(s50=0.50, cost=0.02, tick=0.01, pv=100.0),
}
TFM = {'1m': 1, '5m': 5, '15m': 15, '1h': 60, '4h': 240, 'D': 1440, 'W': 10080}
_C = {}

def _ld(path_glob):
    fs = sorted(glob.glob(path_glob))
    if not fs: return None
    d = pd.concat([pd.read_csv(f) for f in fs]); d.index = pd.to_datetime(d.pop('time'))
    d = d[~d.index.duplicated(keep='last')].sort_index()
    return d[['open', 'high', 'low', 'close', 'volume']].astype(float)

def sday(ix):
    return (ix + pd.Timedelta(hours=6)).normalize()

def fine(m):
    if m in _C: return _C[m]
    if m == 'NQ':
        r = pickle.load(open('/home/claude/lez/raw.pkl', 'rb'))['old']; f = r.copy(); f['res'] = 1
    else:
        parts = []
        m1 = None
        if m == 'MNQ':
            m1 = pickle.load(open('/home/claude/lez/raw.pkl', 'rb'))['fresh']
        elif os.path.isdir(LIB2 + m + '/1m'):
            m1 = _ld(LIB2 + m + '/1m/*.csv')
        m5 = _ld(LIB + m + '/5m/*.csv'); m15 = _ld(LIB + m + '/15m/*.csv')
        used = set()
        for res, d in ((1, m1), (5, m5), (15, m15)):
            if d is None: continue
            sd = sday(d.index)
            keep = d[~sd.isin(used)].copy(); keep['res'] = res
            parts.append(keep); used |= set(sd.unique())
        f = pd.concat(parts).sort_index(); f = f[~f.index.duplicated(keep='first')]
    _C[m] = f
    return f

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
    if tf in ('1m', '5m', '15m'):
        f = f[f.res <= TFM[tf]]
    key = _key(f.index, tf)
    g = f.groupby(key)
    d = pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(), 'volume': g.volume.sum()})
    d['tend'] = d.index + pd.Timedelta(minutes=min(TFM[tf], 1440 if tf != 'W' else 10080))
    if tf == 'D': d['tend'] = d.index + pd.Timedelta(hours=23)
    if tf == 'W': d['tend'] = d.index + pd.Timedelta(days=5, hours=23)
    _C[k] = d
    return d

def period(m, t):
    """'P1' / 'P2' label per timestamp array"""
    t = pd.DatetimeIndex(t)
    if m == 'NQ': return np.array(['P1'] * len(t))
    if m == 'MNQ': return np.array(['P2'] * len(t))
    return np.where(t < pd.Timestamp('2026-06-01'), 'P1', 'P2')

if __name__ == '__main__':
    for m in ('NQ', 'MNQ', 'MES', 'MGC', 'MCL'):
        f = fine(m); print(m, f.index[0], f.index[-1], len(f), f.res.value_counts().to_dict())
        for tf in ('5m', '15m', '1h'):
            print('   ', tf, len(bars(m, tf)))
