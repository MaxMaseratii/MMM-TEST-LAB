import sys, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import map_replay, mmcb
import fva_grid as G, replica4
m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
sig = bars['1h']; se = G.sess_of(sig.index)
ss = [s for s in replica4.run(sig) if s['etype'] == 'Fail+C']
pos = {t: k for k, t in enumerate(sig.index)}
o, h, l, c = sig.open.values, sig.high.values, sig.low.values, sig.close.values
t_, cp, isBuX, isBeX, nbc = mmcb(sig)
run = np.zeros(len(c), int)
for j in range(len(c)): run[j] = (run[j-1] + 1 if j > 0 else 1) if nbc[j] else 0
sF, sL, r2s = map_replay(sig, m1); rO, rH, rL = m1.open.values, m1.high.values, m1.low.values
for tag, stopk in (('A1', 'box'), ('A2', 'fix')):
    out = {}
    for s in ss:
        j = pos.get(pd.Timestamp(s['t']))
        if j is None or j < 20 or j >= len(c) - 1 or se[j] != 0: continue
        sd = 1 if s['long'] else -1
        if (j, sd) in out: continue
        e = c[j]; stp = s['sl'] if stopk == 'box' else e - sd * 50; d = sd * (e - stp)
        if d < 2: continue
        tp = e + sd * 1.5 * d; px = None
        for k in range(j + 1, min(j + 101, len(c))):
            for i in range(sF[k], sL[k] + 1):
                if (sd == 1 and rL[i] <= stp) or (sd == -1 and rH[i] >= stp): px = min(rO[i], stp) if sd == 1 else max(rO[i], stp); break
                if (sd == 1 and rH[i] >= tp) or (sd == -1 and rL[i] <= tp): px = tp; break
            if px is None and tag == 'A2' and k >= j + 2 and run[k] >= 2 and (cp[k] >= .5 if sd == 1 else cp[k] <= .5) and (cp[k-1] >= .5 if sd == 1 else cp[k-1] <= .5): px = c[k]
            if px is None and k >= j + 100: px = c[k]
            if px is not None: break
        if px is not None: out[(j, sd)] = sd * (px - e) / d - 1.0 / d
    eng = pd.read_parquet(f'pick_{tag}.parquet'); eng = eng[eng.period == 'old']
    eng = pd.Series(eng.R.values, index=list(zip(eng.j, eng.side.astype(int))))
    mir = pd.Series(out); com = eng.index.intersection(mir.index)
    print(tag, 'engine', len(eng), 'mirror', len(mir), 'common', len(com), 'max diff', (eng[com] - mir[com]).abs().max())
