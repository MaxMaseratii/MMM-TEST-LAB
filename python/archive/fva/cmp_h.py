import pandas as pd, numpy as np, glob, sys
sys.path.insert(0, '/home/claude/fva')
from grid_eval import met
KEY = ['tf', 'type', 'side', 'session', 'entry', 'stop', 'target', 'exit']
def load(d):
    o = met(pd.concat([pd.read_parquet(f) for f in glob.glob(f'{d}/old_*.parquet')]))
    n = met(pd.concat([pd.read_parquet(f) for f in glob.glob(f'{d}/new_*.parquet')]))
    return o.merge(n, on=KEY, suffixes=('_o', '_n'), how='left')
A = load('grid'); B = load('grid_h')
S = [('FVA.M1', 'PES/PEL+', '1:2', 'XN2 2 NBC'), ('FVA.M2', 'CDL/CDS+', '1:2', 'XN2 2 NBC'),
     ('FVA.M3', 'PES/PEL+', 'TGT', 'XO opp BC'), ('FVA.M4', 'PES/PEL+', '1:2', 'XO opp BC')]
rows = []
for nm, ty, tg, ex in S:
    for tf in ('15m', '5m', '1h'):
        for lab, M in (('before', A), ('honest', B)):
            r = M[(M.tf == tf) & (M.type == ty) & (M.side == 'both') & (M.session == 'All') & (M.entry == 'native') & (M.stop == 'S0 fixed 50') & (M.target == tg) & (M.exit == ex)]
            if len(r):
                r = r.iloc[0]
                rows.append((nm, tf, lab, int(r.n_o), round(r.WR_o*100,1), round(r.PF_o,2), round(r.avgR_o,3), round(r.t_o,1), int(r.n_n) if r.n_n==r.n_n else 0, round(r.WR_n*100,1), round(r.avgR_n,3), round(r.t_n,1)))
df = pd.DataFrame(rows, columns=['strat','tf','run','n_old','WR_old','PF_old','avg_old','t_old','n_new','WR_new','avg_new','t_new'])
pd.set_option('display.width', 200)
print(df.to_string(index=False))
