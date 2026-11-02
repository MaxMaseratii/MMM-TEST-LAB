"""DATA: every market's candles, ready for any test.

fine(sym)        finest bars per trading day (1m, else 5m, else 15m). NY time. Columns open high low close volume res.
bars(sym, tf)    candles on tf minutes (1, 2, 3, 5, 10, 15, 30, 60, 240) built from fine bars, only on days whose fine bars are <= tf.
                 240 (4h) is anchored at 18:00. Adds 'delta' (1m-style: +vol green sub-bar, -vol red sub-bar).
daily(sym), weekly(sym)   session candles (18:00 -> 17:00, week Sun 18:00 -> Fri 17:00).
series(market, tf)        list of frames to test, each with column 'per' = P1 / P2 (the two-period rule):
                 NQ: NQ Dec 2022 - Nov 2025 = P1, MNQ 2026 = P2 (run apart, no price seam).
                 ES / GC / CL: first half vs second half of that chart's own trading days.
SPEC[market]     stop = fixed 1:2 test stop (NQ 50 / ES 20 / GC 12 / CL 0.50), cost per trade in points, tick, $ per point (micro).
sday(index)      trading day of each bar (18:00 starts the next day).

Data lives in <package>/data/fine/*.parquet, or set env MMMLAB_DATA to another folder.
Add new data: data.add_csv(sym, path) merges a TradingView / Yahoo CSV (time, open, high, low, close, volume) into the pack."""
import os, numpy as np, pandas as pd

ROOT = os.environ.get('MMMLAB_DATA', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'))
END = pd.Timestamp('2099-01-01')
NQCUT = pd.Timestamp('2025-11-30 18:00')
MK = {'NQ': ['NQ', 'MNQ'], 'ES': ['MES'], 'GC': ['MGC'], 'CL': ['MCL']}
SYM2M = {'NQ': 'NQ', 'MNQ': 'NQ', 'MES': 'ES', 'ES': 'ES', 'MGC': 'GC', 'GC': 'GC', 'MCL': 'CL', 'CL': 'CL'}
SPEC = {'NQ': dict(stop=50.0, cost=1.0, tick=0.25, pv=2.0),
        'ES': dict(stop=20.0, cost=0.5, tick=0.25, pv=5.0),
        'GC': dict(stop=12.0, cost=0.2, tick=0.1, pv=10.0),
        'CL': dict(stop=0.50, cost=0.02, tick=0.01, pv=100.0)}
_C = {}


def sday(ix):
    return (ix + pd.Timedelta(hours=6)).normalize()


def fine(sym, cut=True):
    """cut=True: NQ stops at Nov 30 2025 (MNQ 2026 is the second period, no overlap)."""
    k = ('fine', sym, cut)
    if k not in _C:
        f = pd.read_parquet(os.path.join(ROOT, 'fine', f'{sym}.parquet'))
        if cut and sym == 'NQ': f = f[f.index < NQCUT]
        _C[k] = f
    return _C[k]


def bars(sym, tf):
    key_ = (sym, tf)
    if key_ in _C: return _C[key_]
    f = fine(sym)
    f = f[f.res <= tf]
    key = f.index.floor(f'{tf}min') if tf <= 60 else (f.index - pd.Timedelta(hours=18)).floor(f'{tf}min') + pd.Timedelta(hours=18)
    f = f.assign(dl=np.sign(f.close.values - f.open.values) * f.volume.values)
    g = f.groupby(key)
    d = pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(),
                      'volume': g.volume.sum(), 'delta': g.dl.sum()})
    d['src'] = sym
    _C[key_] = d
    return d


def daily(sym):
    f = fine(sym); g = f.groupby(sday(f.index))
    return pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(), 'volume': g.volume.sum()})


def weekly(sym):
    d = daily(sym); g = d.groupby(pd.DatetimeIndex(d.index).to_period('W-FRI'))
    return pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(), 'volume': g.volume.sum()})


def series(m, tf):
    out = []
    for s in MK[m]:
        try: d = bars(s, tf).copy()
        except FileNotFoundError: continue
        if len(d) < 300: continue
        if m == 'NQ':
            d['per'] = 'P1' if s == 'NQ' else 'P2'
        else:
            sd = sday(d.index); days = np.sort(sd.unique()); cut = days[len(days) // 2]
            d['per'] = np.where(sd < cut, 'P1', 'P2')
        out.append(d)
    return out


def add_csv(sym, path, res=None):
    """merge new bars (csv with time,open,high,low,close,volume in NY time) into the data pack; finer bars win per day."""
    n = pd.read_csv(path); n.index = pd.to_datetime(n.pop('time')); n = n[['open', 'high', 'low', 'close', 'volume']].astype(float)
    if res is None: res = int(pd.Series(n.index).diff().dt.total_seconds().div(60).mode().iloc[0])
    n['res'] = res
    p = os.path.join(ROOT, 'fine', f'{sym}.parquet')
    old = pd.read_parquet(p) if os.path.exists(p) else n.iloc[:0]
    allb = pd.concat([old, n]); allb['sd'] = sday(allb.index)
    best = allb.groupby('sd').res.min()
    allb = allb[allb.res.values == best.reindex(allb.sd).values].drop(columns='sd')
    allb = allb[~allb.index.duplicated(keep='last')].sort_index()
    allb.index.name = 'time'; allb.to_parquet(p, compression='zstd'); _C.clear()
    return len(allb)
