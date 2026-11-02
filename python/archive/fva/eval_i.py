import pandas as pd, numpy as np, glob, sys
sys.path.insert(0, '/home/claude/fva')
from grid_eval import met
KEY = ['tf', 'type', 'side', 'session', 'entry', 'stop', 'target', 'exit']
o = met(pd.concat([pd.read_parquet(f) for f in glob.glob('grid_i/old_*.parquet')]))
n = met(pd.concat([pd.read_parquet(f) for f in glob.glob('grid_i/new_*.parquet')]))
m = o.merge(n, on=KEY, suffixes=('_o', '_n'), how='left')
m['PASS'] = (m.n_o >= 100) & (m.avgR_o > 0) & (m.t_o >= 2) & (m.n_n >= 30) & (m.avgR_n > 0) & (m.t_n >= 2)
m['W50'] = m.PASS & (m.WR_o >= .5) & (m.WR_n >= .5)
m.to_parquet('grid_i/merged.parquet')
el = (m.n_o >= 100) & (m.n_n >= 30)
pr = m[el].groupby(['tf', 'type']).agg(cells=('PASS', 'size'), passed=('PASS', 'sum'), wr50=('W50', 'sum'))
pr['pass %'] = (pr.passed / pr.cells * 100).round(2)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 400)
print(pr.to_string())
cols = KEY + ['n_o', 'WR_o', 'PF_o', 'avgR_o', 't_o', 'n_n', 'WR_n', 'PF_n', 'avgR_n', 't_n']
w = m[m.W50 & (m.type != 'RANDOM')].copy()
w['minR'] = np.minimum(w.avgR_o, w.avgR_n)
print('\nWR>=50% both periods, passing:', len(w))
print(w.sort_values('minR', ascending=False)[cols].head(60).round(3).to_string(index=False))
p = m[m.PASS & (m.type != 'RANDOM')].copy(); p['minR'] = np.minimum(p.avgR_o, p.avgR_n)
print('\nAll passing by minR (top 30):')
print(p.sort_values('minR', ascending=False)[cols].head(30).round(3).to_string(index=False))
