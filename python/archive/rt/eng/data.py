"""Datasets. OLD = NQ 1m Dec 2022 - Dec 2025 (back-adjusted T). FRESH = MNQ Jul - Oct 2026 (raw V/Y)."""
import numpy as np, pandas as pd, os, pickle
from core import load, resample

CACHE = '/home/claude/rt/cache'
os.makedirs(CACHE, exist_ok=True)

def _c(name, fn):
    p = f'{CACHE}/{name}.pkl'
    if os.path.exists(p):
        return pickle.load(open(p, 'rb'))
    v = fn(); pickle.dump(v, open(p, 'wb')); return v

def old():
    def mk():
        m1 = load('NQ', '1m')
        m1 = m1[m1.index < '2025-12-12']
        bars = {tf: resample(m1, tf) for tf in ['5m', '15m', '1h', '4h', 'D']}
        return m1, bars
    return _c('old', mk)

def fresh():
    def mk():
        m5 = load('MNQ', '5m')
        m1 = load('MNQ', '1m', months=['2026-09', '2026-10'])
        b15 = load('MNQ', '15m'); b15 = b15[b15.index >= '2026-07-02 18:00']
        b10 = load('MNQ', '10m'); b10 = b10[b10.index >= '2026-07-02 18:00']
        bars = {'5m': m5, '10m': b10, '15m': b15}
        for tf in ['1h', '4h', 'D']:
            bars[tf] = resample(m5, tf)
        fp = {}
        for tf in ['5m', '10m', '15m']:
            f = pd.read_csv(f'/home/claude/rt/lib/data/MNQ/fp_{tf}/2026.csv')
            f.index = pd.to_datetime(f.pop('time'))
            fp[tf] = f
        # daily bars for the S7 stop (Yahoo daily, raw)
        dd = load('MNQ', '1d')
        return m1, m5, bars, fp, dd
    return _c('fresh', mk)

def fp_levels(bars, fp):
    """absolute POC / VAH / VAL on the bars (nan where no footprint). VA clipped to the bar."""
    j = bars.join(fp, how='left')
    poc = (j.close + j['POC-CLOSE']).clip(j.low, j.high)
    vah = (j.close + j['VAH-CLOSE']).clip(j.low, j.high)
    val = (j.close + j['VAL-CLOSE']).clip(j.low, j.high)
    return poc.values, vah.values, val.values, j

def fresh10():
    """MNQ Dec 2025 - Oct 2026 (raw V/Y), 15m bars as the replay; 1h / 4h / D built from them."""
    def mk():
        m15 = load('MNQ', '15m')
        m15 = m15[m15.index >= '2025-11-30 18:00']
        bars = {'15m': m15}
        for tf in ['1h', '4h', 'D']:
            bars[tf] = resample(m15, tf)
        dd = load('MNQ', '1d')
        return m15, bars, dd
    return _c('fresh10', mk)
