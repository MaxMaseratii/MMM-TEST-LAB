"""Rebuild summary.csv + years.csv for the dashboard: IND from the original replica (matches the chart),
real-fill methods from the HONEST replica (touch limits live from the prior close)."""
import pandas as pd, numpy as np, sys
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import load
from sim import stats
CATS = ['PES/PEL', 'PES/PEL+', 'CDL/CDS', 'CDL/CDS+', 'Nest PES/PEL(+)', 'Nest CDL/CDS(+)', 'BuX/BeX', 'LQG Brk']
ML = {'IND': 'Indicator math', 'H': 'Real fills', 'HL': 'Real fills, limit at open', 'FX': 'Real fills, fixed stop'}
DN = {'nq_15m': 'NQ 15m 2023-25', 'nq_5m': 'NQ 5m 2023-25', 'nq_1h': 'NQ 1h 2023-25', 'mnq': 'MNQ 15m 2026', 'mes': 'MES 15m 2026'}
SYM = {'mnq': 'MNQ', 'mes': 'MES'}
def onem_mask(d, sym):
    k = set(load(sym, '1m').index.floor('15min'))
    return np.array([t in k for t in d.time])
S, Y = [], []
for key, name in DN.items():
    a = pd.read_parquet(f'res_{key}.parquet'); b = pd.read_parquet(f'res_h_{key}.parquet')
    d = pd.concat([a[a.method == 'IND'], b[b.method != 'IND']])
    if key in SYM:
        mk = onem_mask(d, SYM[key]); d = d[(d.method == 'IND') | mk]
    for m in ['IND', 'H', 'HL', 'FX']:
        x = d[d.method == m]
        for cat in ['ALL'] + CATS:
            y = x if cat == 'ALL' else x[x.cat == cat]
            if len(y) == 0: continue
            s = stats(y.R.values, y.fee.values)
            S.append(dict(key=f"{name}|{ML[m]}|{cat}", data=name, method=ML[m], entry='All entries' if cat == 'ALL' else cat, trades=s['N'],
                          wr=round(s['WR'] / 100 if s['WR'] > 1 else s['WR'], 4), pf=round(s['PF'], 3), avg_rr=round(s['avgRR'], 3), t=round(s['t'], 2), avg_rr_net=round(s['avgRR_net'], 3)))
    if key == 'nq_15m':
        d['year'] = pd.to_datetime(d.time).dt.year
        for m in ['H', 'FX']:
            for yr, g in d[d.method == m].groupby('year'):
                for cat in ['ALL'] + CATS:
                    z = g if cat == 'ALL' else g[g.cat == cat]
                    if len(z) < 20: continue
                    s = stats(z.R.values, z.fee.values)
                    Y.append(dict(key=f"{ML[m]}|{cat}|{yr}", method=ML[m], entry='All entries' if cat == 'ALL' else cat, year=yr, trades=s['N'],
                                  wr=round(s['WR'] / 100 if s['WR'] > 1 else s['WR'], 4), pf=round(s['PF'], 3), avg_rr=round(s['avgRR'], 3), t=round(s['t'], 2), avg_rr_net=round(s['avgRR_net'], 3)))
S = pd.DataFrame(S); Y = pd.DataFrame(Y)
old = pd.read_csv('dash/summary.csv')
print('old wr sample', old.wr.head(3).tolist(), 'new', S.wr.head(3).tolist())
S.to_csv('dash/summary_h.csv', index=False); Y.to_csv('dash/years_h.csv', index=False)
o = old.set_index('key'); n = S.set_index('key')
for k in ['NQ 15m 2023-25|Real fills|ALL', 'NQ 15m 2023-25|Real fills|PES/PEL+', 'NQ 15m 2023-25|Real fills|CDL/CDS+', 'NQ 15m 2023-25|Real fills, fixed stop|PES/PEL+', 'NQ 15m 2023-25|Real fills, fixed stop|CDL/CDS+', 'MNQ 15m 2026|Real fills|CDL/CDS+', 'NQ 1h 2023-25|Real fills|CDL/CDS+']:
    print(k, '| before', o.loc[k, ['trades', 'wr', 'avg_rr', 't', 'avg_rr_net']].tolist(), '| honest', n.loc[k, ['trades', 'wr', 'avg_rr', 't', 'avg_rr_net']].tolist())
print(len(S), len(old), len(Y))
