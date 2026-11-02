"""Honest CONFIRMATION entries on the flip zones: the touch candle must CLOSE and hold the box
(not close through it). Then: entry 0 = market at that close · entry 1 = limit back at the level for the next 5 candles.
Same engine, same 6 stops x 7 targets x 12 exits x sides x sessions, RANDOM = luck."""
import sys; sys.path.insert(0, '/home/claude/fva')
import numpy as np, pandas as pd, os
import fva_grid as G, replica2
from core import atr, TICK

G.TYPES = ['PES/PEL+ hold', 'CDL/CDS+ hold', 'RANDOM']
G.ENTS = ['market at hold close', 'limit next 5']
G.NG = len(G.TYPES) * 2 * 4 * 2 * 6
MAP = {'② PES/PEL+': 'PES/PEL+ hold', '④ CDL/CDS+': 'CDL/CDS+ hold'}
G.replica_run = lambda sig: [t for t in replica2.run(sig) if t['etype'] in MAP]
G.OUT = '/home/claude/fva/grid_c'
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
        ti = G.TYPES.index(MAP[s['etype']]); sd = 1.0 if s['long'] else -1.0; si_ = 0 if s['long'] else 1; se = sess[i]
        for en in (0, 1):
            if en == 0:
                L = np.nan; e0 = c[i]
            else:
                if not (sd * (c[i] - s['ep']) > 0):
                    continue
                L = s['ep']; e0 = L
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
G.run(sys.argv[1])
