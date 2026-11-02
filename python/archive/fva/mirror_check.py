"""Mirror of the Pine 4.0 trade manager (bar by bar, 1m intrabars) vs the test engine, old NQ 1h."""
import sys, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import map_replay, mmcb
from rows import datr_prev_map
import replica2
m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
sig = bars['1h']
ss = [s for s in replica2.run(sig) if s['etype'] == '⑦ Fail+' and s['long'] and not (s['ep'] < s['sl'] + 1.0)]
datr = datr_prev_map(sig.index, bars['D'], True)
pos = {t: k for k, t in enumerate(sig.index)}
o, h, l, c = sig.open.values, sig.high.values, sig.low.values, sig.close.values
t_, cp, isBuX, isBeX, nbc = mmcb(sig)
run = np.zeros(len(c), int)
for j in range(len(c)):
    run[j] = (run[j-1] + 1 if j > 0 else 1) if nbc[j] else 0
sF, sL, r2s = map_replay(sig, m1)
rO, rH, rL = m1.open.values, m1.high.values, m1.low.values
out = {}
for s in ss:
    j = pos.get(pd.Timestamp(s['t']))
    if j is None or j < 20 or j >= len(c) - 1 or j in out: continue
    e = c[j]; stp = e - 0.15 * datr[j]; d = e - stp
    if np.isnan(d) or d < 2: continue
    tp = e + 4 * d; px = None
    for k in range(j + 1, min(j + 101, len(c))):
        for i in range(sF[k], sL[k] + 1):
            if rL[i] <= stp: px = min(rO[i], stp); break
            if rH[i] >= tp: px = tp; break
        if px is None:
            if k >= j + 2 and run[k] >= 2 and cp[k] >= .5 and cp[k-1] >= .5: px = c[k]
            elif k >= j + 100: px = c[k]
        if px is not None: break
    if px is not None:
        out[j] = (px - e) / d - 1.0 / d
eng = pd.read_parquet('trades_M1_clean.parquet'); eng = eng[eng.period == 'old'].set_index('j').R
mir = pd.Series(out)
both = eng.index.intersection(mir.index)
diff = (eng[both] - mir[both]).abs()
print('engine', len(eng), 'mirror', len(mir), 'common', len(both), 'max diff', diff.max(), 'n diff>1e-6', (diff > 1e-6).sum())
print('engine avg', eng.mean().round(4), 'mirror avg', mir.mean().round(4))
