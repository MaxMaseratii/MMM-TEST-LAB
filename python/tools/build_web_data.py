"""Build the web page's candle files (data/<SYM>.bin.gz) from the Python data pack (python/data/fine/<SYM>.parquet).
Run after adding new data:  python python/tools/build_web_data.py
Format (little-endian Int32 columns, gzip): [n, tick*1e6, ...] then dt (minutes since 1970, NY time, first value absolute),
open-prevclose, high-open, low-open, close-open (in ticks), volume, res (bar minutes)."""
import os, gzip, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
TICK = {'NQ': .25, 'MNQ': .25, 'MES': .25, 'MGC': .1, 'MCL': .01}
for sym, tick in TICK.items():
    p = os.path.join(ROOT, 'python', 'data', 'fine', f'{sym}.parquet')
    if not os.path.exists(p): continue
    f = pd.read_parquet(p)
    if sym == 'NQ': f = f[f.index < pd.Timestamp('2025-11-30 18:00')]
    t = (f.index.values.astype('datetime64[m]').astype(np.int64)).astype(np.int64)
    q = lambda x: np.round(x / tick).astype(np.int64)
    O, H, L, C = q(f.open.values), q(f.high.values), q(f.low.values), q(f.close.values)
    dt = np.diff(t, prepend=0); do = O - np.r_[0, C[:-1]]
    cols = [dt, do, H - O, L - O, C - O, np.round(f.volume.values).astype(np.int64), f.res.values.astype(np.int64)]
    n = len(t)
    arr = np.concatenate([np.array([n, int(round(tick * 1e6))], np.int64)] + cols).astype('<i4')
    assert np.abs(np.concatenate(cols[1:5])).max() < 2**31
    out = os.path.join(ROOT, 'data', f'{sym}.bin.gz')
    with gzip.open(out, 'wb', compresslevel=9) as g: g.write(arr.tobytes())
    print(sym, n, os.path.getsize(out) // 1024, 'KB')
