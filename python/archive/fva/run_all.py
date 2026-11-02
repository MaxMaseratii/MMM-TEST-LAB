import sys, time, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import load, resample
from replica import run, category
from sim import ind_sim, Fine, honest, stats

FEE = 1.50  # $ per micro contract, round trip (commission + exchange), used for the 'net' column


def fine_series(chart, tf_rule, parts):
    """parts = list of finer DataFrames in priority order; fills each chart bar with the finest data that covers it."""
    key_chart = chart.index
    used = pd.Series(False, index=key_chart)
    out = []
    for p in parts:
        p = p[(p.index >= key_chart[0]) & (p.index < key_chart[-1] + pd.Timedelta(tf_rule))]
        k = p.index.floor(tf_rule)
        ok = ~used.reindex(k).fillna(True).values
        sel = p[ok]
        out.append(sel)
        used.loc[used.index.intersection(sel.index.floor(tf_rule).unique())] = True
    rest = chart[~used.values]
    out.append(rest)
    f = pd.concat(out).sort_index()
    f = f[~f.index.duplicated(keep='first')]
    return f, used.mean()


def score(name, chart, fine, pv, fixed, years=True):
    t0 = time.time()
    tr = run(chart, pv=pv)
    h, l, c = chart.high.values, chart.low.values, chart.close.values
    F = Fine(fine, chart.index)
    rows = []
    for t in tr:
        cat = category(t['etype'])
        base = dict(ds=name, cat=cat, time=t['t'], long=t['long'])
        r, how, j = ind_sim(t, h, l, c)
        if r is not None:
            rows.append(dict(base, method='IND', R=r, how=how, fee=t['ps'] * FEE / t['arisk'], same=(j == t['i'])))
        for m, mode, fx in (('H', 'close', None), ('HL', 'limit', None), ('FX', 'close', fixed)):
            if m == 'HL' and cat not in ('BuX/BeX', 'LQG Brk'):
                continue  # same as H for touch entries
            res = honest(t, F, c, pv, mode=mode, fixed=fx)
            if res is not None:
                rr, how2, ps, ar = res
                rows.append(dict(base, method=m, R=rr, how=how2, fee=ps * FEE / ar, same=False))
    d = pd.DataFrame(rows)
    print(name, 'bars', len(chart), 'setups', len(tr), 'scored rows', len(d), round(time.time() - t0, 1), 's', flush=True)
    return d


if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'mnq':
        m15 = load('MNQ', '15m'); m15 = m15[m15.index >= '2025-11-30 18:00']
        m1 = load('MNQ', '1m'); m5 = load('MNQ', '5m')
        fine, cov = fine_series(m15, '15min', [m1, m5])
        print('MNQ fine coverage (1m or 5m) of 15m bars:', round(cov * 100, 1), '%')
        d = score('MNQ 15m 2026', m15, fine, 2.0, 50.0)
    elif which == 'mes':
        e15 = load('MES', '15m'); e15 = e15[e15.index >= '2025-11-30 18:00']
        e1 = load('MES', '1m'); e5 = load('MES', '5m')
        fine, cov = fine_series(e15, '15min', [e1, e5])
        print('MES fine coverage:', round(cov * 100, 1), '%')
        d = score('MES 15m 2026', e15, fine, 5.0, 20.0)
    else:  # nq tf
        tf = which.split('_')[1]
        m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
        chart = bars[tf] if tf in bars else resample(m1, tf)
        d = score(f'NQ {tf} 2023-25', chart, m1, 2.0, 50.0)
    d.to_parquet(f'/home/claude/fva/res_{which}.parquet')
