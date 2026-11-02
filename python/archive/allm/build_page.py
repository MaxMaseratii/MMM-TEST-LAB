import json, numpy as np, pandas as pd, os, glob, shutil
import grid
R = pd.read_parquet('rank_all.parquet'); D = pd.read_parquet('grid_all.parquet')
R = R[~R.strat.str.startswith('RANDOM')].copy()
MKN = {'NQ': 'NQ / MNQ', 'ES': 'ES / MES', 'GC': 'Gold / MGC', 'CL': 'Crude / MCL'}
strats = sorted(R.strat.unique()); sid = {s: k for k, s in enumerate(strats)}
shutil.rmtree('site/data', ignore_errors=True); os.makedirs('site/data')
def r3(x, k=3):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), k)
for (mk, s), g in D[~D.strat.str.startswith('RANDOM')].groupby(['market', 'strat']):
    g = g[(g.n1 >= 10) | (g.n2 >= 10)]
    cols = {c: g[c].astype(int).tolist() for c in ['side', 'e', 'st', 't', 'x']}
    for c, k in [('n1', 0), ('wr1', 1), ('pf1', 2), ('avg1', 3), ('t1', 2), ('n2', 0), ('wr2', 1), ('pf2', 2), ('avg2', 3), ('t2', 2)]:
        v = g[c].astype(float).values
        cols[c] = [None if not np.isfinite(x) else (int(x) if k == 0 else round(x, k)) for x in v]
    json.dump(cols, open(f'site/data/{mk}_{sid[s]}.json', 'w'), separators=(',', ':'))
rows = []
for _, r in R.iterrows():
    rows.append({k: (r3(v) if isinstance(v, (float, np.floating)) else (int(v) if isinstance(v, (np.integer,)) else v)) for k, v in r.items()})
rnd = pd.read_parquet('rank_all.parquet'); rnd = rnd[rnd.strat.str.startswith('RANDOM')]
rr = {f'{a}|{b}|{c}': [r3(x) for x in (d1, d2)] for a, b, c, d1, d2 in zip(rnd.market, rnd.tf, rnd.side, rnd.fx_avg1, rnd.fx_avg2)}
meta = dict(rows=rows, sid=sid, entry=grid.ENAME, stop=grid.SNAME, target=[f'1:{t:g}' for t in grid.TGT], exit=grid.XNAME, mk=MKN, random=rr)
json.dump(meta, open('site/meta.json', 'w'), separators=(',', ':'))
print(len(rows), len(glob.glob('site/data/*.json')), sum(os.path.getsize(f) for f in glob.glob('site/data/*.json')) / 1e6, 'MB')
