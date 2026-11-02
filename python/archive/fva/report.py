import pandas as pd, numpy as np, sys, json
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import load
from sim import stats

CATS = ['PES/PEL', 'PES/PEL+', 'CDL/CDS', 'CDL/CDS+', 'Nest PES/PEL(+)', 'Nest CDL/CDS(+)', 'BuX/BeX', 'LQG Brk']
MLAB = {'IND': 'Indicator math (same-bar, target first)', 'H': 'Real fills (⑤⑥ market at close)',
        'HL': 'Real fills (⑤⑥ limit at the open, next bars)', 'FX': 'Real fills + fixed stop 1:2'}


def tab(d):
    out = []
    for m in ['IND', 'H', 'HL', 'FX']:
        x = d[d.method == m]
        if len(x) == 0:
            continue
        for cat in ['ALL'] + CATS:
            y = x if cat == 'ALL' else x[x.cat == cat]
            if len(y) == 0:
                continue
            s = stats(y.R.values, y.fee.values)
            out.append(dict(method=m, entry=cat, N=s['N'], WR=s['WR'], PF=s['PF'], avgRR=s['avgRR'], t=s['t'],
                            avgRR_net=s['avgRR_net'], t_net=s['t_net']))
    return pd.DataFrame(out)


def onem_mask(d, sym):
    m1 = load(sym, '1m')
    k = set(m1.index.floor('15min'))
    return np.array([t in k for t in d.time])


res = {}
for key, name, sym in [('nq_15m', 'NQ 15m · Dec 2022 – Dec 2025', None), ('nq_5m', 'NQ 5m · Dec 2022 – Dec 2025', None),
                       ('nq_1h', 'NQ 1h · Dec 2022 – Dec 2025', None), ('mnq', 'MNQ 15m · Dec 2025 – Oct 2026', 'MNQ'),
                       ('mes', 'MES 15m · Dec 2025 – Oct 2026', 'MES')]:
    try:
        d = pd.read_parquet(f'/home/claude/fva/res_{key}.parquet')
    except Exception as e:
        print('missing', key); continue
    if sym:
        mk = onem_mask(d, sym)
        d = d[(d.method == 'IND') | mk]   # real-fill methods only where 1m data exists
    t = tab(d)
    t.insert(0, 'data', name)
    res[key] = t
    if key.startswith('nq'):
        d['year'] = pd.to_datetime(d.time).dt.year
        y = []
        for m in ['IND', 'H', 'FX']:
            for yr, g in d[d.method == m].groupby('year'):
                for cat in ['ALL'] + CATS:
                    z = g if cat == 'ALL' else g[g.cat == cat]
                    if len(z) < 20: continue
                    s = stats(z.R.values, z.fee.values)
                    y.append(dict(data=name, method=m, year=yr, entry=cat, N=s['N'], WR=s['WR'], PF=s['PF'], avgRR=s['avgRR'], t=s['t'], avgRR_net=s['avgRR_net']))
        res[key + '_year'] = pd.DataFrame(y)
    # how many indicator wins were decided on the creation bar
    x = d[d.method == 'IND']
    res[key + '_same'] = pd.DataFrame([dict(data=name, entry=c, same_bar_pct=(x[x.cat == c].same.mean() * 100)) for c in CATS])
pd.to_pickle(res, '/home/claude/fva/report.pkl')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500)
for k, v in res.items():
    print('\n==', k); print(v.round(3).to_string(index=False))
