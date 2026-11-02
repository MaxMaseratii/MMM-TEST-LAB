"""MMM Data Library loader.
load('NQ', '1m')            -> every 1m bar of NQ in the library (all month files), indexed by bar OPEN time, New York.
load('MNQ', '5m', resample_from='1m') -> 5m bars built from the 1m data.
src column: T = tested NQ 2022-25 (back-adjusted), R = nq-es-trader repo 2026 (real futures),
            U = uploaded ES daily 2013-23, Y = Yahoo front month (raw).
Back-adjusted (T) and raw (R / Y) prices differ by the roll gap, so never mix them inside one test window."""
import glob, os, pandas as pd

def load(symbol, tf, root='lib', resample_from=None, start=None, end=None):
    if resample_from:
        d = load(symbol, resample_from, root, start=start, end=end)
        rule = {'2m': '2min', '3m': '3min', '5m': '5min', '15m': '15min', '30m': '30min', '1h': '60min'}[tf]
        g = d.groupby(d.index.floor(rule))
        return pd.DataFrame({'open': g.open.first(), 'high': g.high.max(), 'low': g.low.min(), 'close': g.close.last(),
                             'volume': g.volume.sum(), 'src': g.src.last()})
    files = sorted(glob.glob(os.path.join(root, 'data', symbol, tf, '*.csv')))
    if not files:
        raise FileNotFoundError(f'no files for {symbol} {tf} under {root}/data')
    d = pd.concat([pd.read_csv(f) for f in files])
    d.index = pd.to_datetime(d.pop('time'))
    d = d[~d.index.duplicated(keep='last')].sort_index()
    if start: d = d[d.index >= pd.Timestamp(start)]
    if end: d = d[d.index <= pd.Timestamp(end)]
    return d
