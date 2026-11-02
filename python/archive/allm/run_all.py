import sys, os, time, pickle, numpy as np, pandas as pd
import grid
MK = {'NQ': ['NQ', 'MNQ'], 'ES': ['MES'], 'GC': ['MGC'], 'CL': ['MCL']}
SRC = sys.argv[1].split(',') if len(sys.argv) > 1 else ['misc']
OUT = sys.argv[2] if len(sys.argv) > 2 else 'acc_misc.pkl'

def load(src, m):
    p = f'sig_{src}_{m}.parquet'
    return pd.read_parquet(p) if os.path.exists(p) else None

frames = []
for mk, subs in MK.items():
    for m in subs:
        for src in SRC:
            S = load(src, m)
            if S is not None and len(S): frames.append(S.assign(market=mk, sub=m))
        for tf in ('1m', '5m', '15m', '1h', '4h') if 'misc' in SRC else ():
            try:
                R = grid.random_signals(m, tf)
            except Exception:
                continue
            frames.append(R.assign(strat='RANDOM ' + tf, tf=tf, market=mk, sub=m, nrr=np.nan, note='random'))
ALL = pd.concat(frames, ignore_index=True)
strats = sorted(ALL.strat.unique()); sid = {s: k for k, s in enumerate(strats)}
ALL['sgid'] = ALL.strat.map(sid)
res = {}
for mk in MK:
    acc = np.zeros((len(strats), 2, 2, grid.NE, grid.NS, grid.NT, grid.NX, 6))
    for (m, tf), S in ALL[ALL.market == mk].groupby(['sub', 'tf']):
        if tf == '1m' and m != 'NQ' and len(S) == 0: continue
        t = time.time(); grid.run(m, tf, S.reset_index(drop=True), acc)
        print(mk, m, tf, len(S), round(time.time() - t), 's', flush=True)
    res[mk] = acc
pickle.dump(dict(strats=strats, acc=res, counts=ALL.groupby(['market', 'strat', 'side']).size().to_dict()), open(OUT, 'wb'))
print('saved', OUT)
