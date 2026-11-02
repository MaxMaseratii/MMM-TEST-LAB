"""IDEA GRID: honest close-decided FVA events through the MMM engine.
Types: FlipBC, BrkBC, Rej FVA, Rej Zone, G3 FVA, G3 Zone, Sig FVA, Sig Zone, FailC, FailC RT, Fail+C, Fail+C RT, RANDOM.
6 stops x 8 targets (1:0.5 .. 1:6 + TGT) x 12 exits x side x session. 5m / 15m / 1h / 4h, NQ 2023-25 then MNQ 2026."""
import sys, os, time, pickle; sys.path.insert(0, '/home/claude/fva'); sys.path.insert(0, '/home/claude/rt/eng')
import numpy as np, pandas as pd
import fva_grid as G, replica4
from core import atr, TICK, load, resample

IDEAS = ['FlipBC', 'BrkBC', 'Rej FVA', 'Rej Zone', 'G3 FVA', 'G3 Zone', 'Sig FVA', 'Sig Zone', 'FailC', 'FailC RT', 'Fail+C', 'Fail+C RT']
G.TYPES = IDEAS + ['RANDOM']
G.ENTS = ['market at close', 'limit retest 5']
G.NG = len(G.TYPES) * 2 * 4 * 2 * 6
G.RK = np.array([0.5, 1., 1.5, 2., 3., 4., 6.])
G.TN = ['1:0.5', '1:1', '1:1.5', '1:2', '1:3', '1:4', '1:6', 'TGT']
G.replica_run = lambda sig: [t for t in replica4.run(sig) if t['etype'] in IDEAS]
G.OUT = '/home/claude/fva/grid_i'
os.makedirs(G.OUT, exist_ok=True)

def make_rows(sig, setups, datr, seed):
    o, h, l, c = sig.open.values, sig.high.values, sig.low.values, sig.close.values
    n = len(c); a = atr(sig); sess = G.sess_of(sig.index)
    T, O = [], []
    pos = {t: k for k, t in enumerate(sig.index)}
    for s in setups:
        i = pos.get(pd.Timestamp(s['t']))
        if i is None or i < 20 or i >= n - 1 or np.isnan(a[i]):
            continue
        ti = G.TYPES.index(s['etype']); sd = 1.0 if s['long'] else -1.0; si_ = 0 if s['long'] else 1; se = sess[i]
        if s['mkt']:
            en, L, e0 = 0, np.nan, c[i]
        else:
            if not (sd * (c[i] - s['ep']) > 0):
                continue
            en, L, e0 = 1, s['ep'], s['ep']
        stops = [e0 - sd * 50.0, s['sl'], s['swing'], e0 - sd * a[i], e0 - sd * 1.5 * a[i], e0 - sd * 0.15 * datr[i]]
        for st, sp in enumerate(stops):
            if sp is None or np.isnan(sp):
                continue
            row = [i, sd, L, sp, s['tgt'] if s['tgt'] is not None else np.nan, G.gidx(ti, si_, se, en, st)]
            (T if en == 0 else O).append(row)
    rng = np.random.default_rng(seed)
    rsl, rsh = G.swings(h, l)
    J = rng.choice(np.arange(20, n - 1), size=min(n // 4, 20000), replace=False)
    ti = G.TYPES.index('RANDOM')
    for j in J:
        if np.isnan(a[j]): continue
        sd = 1.0 if rng.random() < .5 else -1.0; si_ = 0 if sd > 0 else 1
        e0 = c[j]
        stops = [e0 - sd * 50.0, (l[j] - 4 * TICK) if sd > 0 else (h[j] + 4 * TICK), (rsl[j] - 4 * TICK) if sd > 0 else (rsh[j] + 4 * TICK),
                 e0 - sd * a[j], e0 - sd * 1.5 * a[j], e0 - sd * 0.15 * datr[j]]
        for st, sp in enumerate(stops):
            if np.isnan(sp): continue
            T.append([j, sd, np.nan, sp, np.nan, G.gidx(ti, si_, sess[j], 0, st)])
    return np.array(T, float).reshape(-1, 6), np.array(O, float).reshape(-1, 6)

G.make_rows = make_rows

def run(which, tfs):
    t0 = time.time()
    if which == 'old':
        m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
        for tf in tfs:
            mins = {'5m': 5, '15m': 15, '1h': 60, '4h': 240}[tf]
            sig = bars[tf]; setups = G.replica_run(sig)
            acc, cnt = G.segment(sig, setups, m1, bars['D'], True, mins, 7, sig.index[0], sig.index[-1])
            G.flatten(acc, cnt, ('old', tf)).to_parquet(f'{G.OUT}/old_{tf}.parquet')
            print('old', tf, len(setups), f'{time.time() - t0:.0f}s', flush=True)
    else:
        m15 = load('MNQ', '15m'); m15 = m15[m15.index >= '2025-11-30 18:00']
        m1 = load('MNQ', '1m'); m5 = load('MNQ', '5m'); dd = load('MNQ', '1d')
        k1 = m1.index.floor('5min').unique()
        rep = pd.concat([m1, m5[~m5.index.isin(k1)]]).sort_index(); rep = rep[~rep.index.duplicated()]
        segs = [('2026-03-04 19:00', '2026-05-01 16:59'), ('2026-07-02 18:00', '2026-10-16 16:59')]
        for tf in tfs:
            mins = {'5m': 5, '15m': 15, '1h': 60, '4h': 240}[tf]
            if tf == '5m':
                sig = m5; st = [('2026-09-01 00:00', '2026-10-16 16:59')]
            else:
                sig = m15 if tf == '15m' else resample(m15, tf); st = segs
            setups = G.replica_run(sig)
            acc = cnt = 0
            for a_, b_ in st:
                A_, C_ = G.segment(sig, setups, rep, dd, False, mins, 11, pd.Timestamp(a_), pd.Timestamp(b_))
                acc = acc + A_; cnt = cnt + C_
            G.flatten(acc, cnt, ('new', tf)).to_parquet(f'{G.OUT}/new_{tf}.parquet')
            print('new', tf, len(setups), f'{time.time() - t0:.0f}s', flush=True)

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2].split(','))
