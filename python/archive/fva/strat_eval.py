"""Per-trade results of the honest box-failure strategies (1h), old NQ 2023-25 and new MNQ 2026."""
import sys, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import load, resample, simulate, map_replay, exit_events, EXIT_MO, TICK
from rows import datr_prev_map
import fva_grid as G, replica2

XMO = np.r_[EXIT_MO, 0].astype(np.int64)
STRATS = {  # name: (etype, stop kind, stop mult, RK, exit index)
    'M1 Fail+ L dATR 1:4 XN2W': ('⑦ Fail+', 'datr', 0.15, 4.0, 6),
    'M1b Fail+ L fix50 1:4 XN2W': ('⑦ Fail+', 'fix', 50.0, 4.0, 6),
    'M1c Fail+ L fix50 1:2 XN2W': ('⑦ Fail+', 'fix', 50.0, 2.0, 6),
    'M2 Fail L dATR 1:6 XH': ('⑦ Fail', 'datr', 0.15, 6.0, 11),
    'M2b Fail L fix50 1:2 XH': ('⑦ Fail', 'fix', 50.0, 2.0, 11),
}

def trades(sig, rep, daily, dk, tf_min, t0, t1, name):
    et, sk, sm, rk, xi = STRATS[name]
    sig = sig[(sig.index >= t0) & (sig.index <= t1)]
    rep = rep[(rep.index >= t0) & (rep.index <= pd.Timestamp(t1) + pd.Timedelta(days=1))]
    ss = [s for s in replica2.run(sig) if s['etype'] == et and s['long']]
    datr = datr_prev_map(sig.index, daily, dk)
    ev = exit_events(sig); hn = G.next_true(G.hold_event(sig, tf_min))
    evN = np.concatenate([ev, np.stack([hn, hn])[:, None, :]], axis=1)
    pos = {t: k for k, t in enumerate(sig.index)}
    c = sig.close.values; n = len(c)
    R = []
    for s in ss:
        i = pos.get(pd.Timestamp(s['t']))
        if i is None or i < 20 or i >= n - 1: continue
        stp = c[i] - (sm * datr[i] if sk == 'datr' else sm)
        if np.isnan(stp): continue
        R.append([i, 1, np.nan, stp, np.nan, 0])
    rows = np.array(R, float).reshape(-1, 6)
    sF, sL, r2s = map_replay(sig, rep)
    acc, cnt, keep = simulate(rep.open.values, rep.high.values, rep.low.values, rep.close.values, sF, sL, r2s,
                              c, n, rows[:, 0].astype(np.int64), rows[:, 1].astype(np.int64), rows[:, 2], rows[:, 3], rows[:, 4],
                              rows[:, 5].astype(np.int64), 1, np.array([rk]), evN, XMO, 1, 100, 1.0, 2.0, TICK, 0, xi)
    df = pd.DataFrame({'t': sig.index[rows[:, 0].astype(int)], 'j': rows[:, 0].astype(int), 'R': keep, 'd': c[rows[:, 0].astype(int)] - rows[:, 3]})
    return df.dropna(subset=['R'])

def all_trades(name):
    m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
    sig = bars['1h']
    old = trades(sig, m1, bars['D'], True, 60, sig.index[0], sig.index[-1], name).assign(period='old')
    m15 = load('MNQ', '15m'); m15 = m15[m15.index >= '2025-11-30 18:00']
    mm1 = load('MNQ', '1m'); m5 = load('MNQ', '5m'); dd = load('MNQ', '1d')
    k1 = mm1.index.floor('5min').unique()
    rep = pd.concat([mm1, m5[~m5.index.isin(k1)]]).sort_index(); rep = rep[~rep.index.duplicated()]
    s1h = resample(m15, '1h')
    new = pd.concat([trades(s1h, rep, dd, False, 60, pd.Timestamp(a), pd.Timestamp(b), name) for a, b in
                     [('2026-03-04 19:00', '2026-05-01 16:59'), ('2026-07-02 18:00', '2026-10-16 16:59')]]).assign(period='new')
    return pd.concat([old, new])

def stats(R, pv=None, d=None):
    R = np.asarray(R); n = len(R)
    if n == 0: return {}
    w = R > 0; avg = R.mean(); sd = R.std(ddof=1) if n > 1 else np.nan
    cum = np.cumsum(R); dd = np.max(np.maximum.accumulate(np.r_[0, cum])[1:] - cum)
    def streak(b):
        m = c = 0
        for x in b:
            c = c + 1 if x else 0; m = max(m, c)
        return m
    return dict(n=n, WR=w.mean(), PF=R[w].sum() / -R[~w].sum() if (~w).any() else np.nan, avgR=avg, t=avg / sd * np.sqrt(n) if sd > 0 else np.nan,
                netR=R.sum(), maxDD_R=dd, maxW=streak(w), maxL=streak(~w))

if __name__ == '__main__':
    out = {}
    for name in STRATS:
        df = all_trades(name)
        df.to_parquet(f'/home/claude/fva/trades_{name.split()[0]}.parquet')
        for lab, g in [('old', df[df.period == 'old']), ('new', df[df.period == 'new']), ('blend', df)]:
            st = stats(g.R.values); dedup = stats(g.drop_duplicates(['period', 'j']).R.values)
            print(f"{name:30s} {lab:5s} n{st['n']:5d} WR {st['WR']*100:4.1f}% PF {st['PF']:.2f} avg {st['avgR']:+.3f} t {st['t']:.2f} | dedup n{dedup['n']} avg {dedup['avgR']:+.3f} t {dedup['t']:.2f} | maxW {st['maxW']} maxL {st['maxL']} DD {st['maxDD_R']:.1f}R")
        y = df[df.period == 'old'].copy(); y['y'] = y.t.dt.year
        print('   years:', ' | '.join(f"{k}: n{len(g)} {g.R.mean():+.2f} t{g.R.mean()/g.R.std()*np.sqrt(len(g)):.1f}" for k, g in y.groupby('y')))
        print('   avg stop pts old/new:', round(df[df.period=='old'].d.mean(),1), round(df[df.period=='new'].d.mean(),1))
