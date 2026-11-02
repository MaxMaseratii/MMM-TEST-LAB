"""FVA final: 1 MNQ, one trade at a time, $ results, exact engine rules (market at close, stop first on 1m, 1 pt cost)."""
import sys, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import load, resample, map_replay, exit_events, EXIT_MO, atr
from rows import datr_prev_map
import fva_grid as G, replica4
XMO = np.r_[EXIT_MO, 0].astype(np.int64)
XI = {'X0': 0, 'XO': 1, 'XN2': 2, 'XN3': 3, 'XN4': 4, 'XN2A': 5, 'XN2W': 6, 'XN2R': 7, 'XSA': 8, 'XSB': 9, 'XSF': 10, 'XH': 11}
MIN = {'1h': 60, '4h': 240, '15m': 15}
PV, COST = 2.0, 1.0

def ctx(sig_full, rep, daily, dk, tf, t0, t1, setups):
    sig = sig_full[(sig_full.index >= t0) & (sig_full.index <= t1)]
    rep = rep[(rep.index >= t0) & (rep.index <= pd.Timestamp(t1) + pd.Timedelta(days=1))]
    ev = exit_events(sig); hn = G.next_true(G.hold_event(sig, MIN[tf]))
    sF, sL, r2s = map_replay(sig, rep)
    return dict(sig=sig, o=sig.open.values, c=sig.close.values, rO=rep.open.values, rH=rep.high.values, rL=rep.low.values, sF=sF, sL=sL, r2s=r2s,
                ss=[s for s in setups if t0 <= s['t'] <= t1], datr=datr_prev_map(sig.index, daily, dk), a=atr(sig), se=G.sess_of(sig.index),
                evN=np.concatenate([ev, np.stack([hn, hn])[:, None, :]], axis=1), pos={t: k for k, t in enumerate(sig.index)})

def trades(C, etypes, side='both', sess=None, stop='fix', rk=2.0, ex='X0'):
    c, n = C['c'], len(C['c']); out = []; seen = set()
    for s in C['ss']:
        if s['etype'] not in etypes: continue
        j = C['pos'].get(pd.Timestamp(s['t']))
        if j is None or j < 20 or j >= n - 1 or np.isnan(C['a'][j]): continue
        sd = 1 if s['long'] else -1
        if side != 'both' and (sd == 1) != (side == 'long'): continue
        if sess is not None and G.SESS[C['se'][j]] not in sess: continue
        if (j, sd) in seen: continue
        e = c[j]
        stp = {'fix': e - sd * 50, 'box': s['sl'], 'swing': s['swing'], 'atr1': e - sd * C['a'][j], 'atr15': e - sd * 1.5 * C['a'][j], 'datr': e - sd * 0.15 * C['datr'][j]}[stop]
        if stp is None or np.isnan(stp): continue
        d = sd * (e - stp)
        if d < 2: continue
        seen.add((j, sd))
        tp = e + sd * rk * d if rk else np.inf * sd
        xi = XI[ex]
        ej = C['evN'][0 if sd == 1 else 1, xi, min(j + 1 + XMO[xi], n)]
        ej = min(ej, j + 100, n - 1)
        px = None; xb = ej; how = 'exit'
        for i in range(C['sL'][j] + 1, C['sL'][ej] + 1):
            if (sd == 1 and C['rL'][i] <= stp) or (sd == -1 and C['rH'][i] >= stp):
                px = min(C['rO'][i], stp) if sd == 1 else max(C['rO'][i], stp); xb = C['r2s'][i]; how = 'stop'; break
            if (sd == 1 and C['rH'][i] >= tp) or (sd == -1 and C['rL'][i] <= tp):
                px = tp; xb = C['r2s'][i]; how = 'target'; break
        if px is None: px = c[ej]
        R = sd * (px - e) / d - COST / d
        out.append(dict(t=C['sig'].index[j], j=j, xb=xb, side=sd, e=e, d=d, R=R, usd=(sd * (px - e) - COST) * PV, how=how))
    return pd.DataFrame(out)

def one_at_a_time(df):
    if len(df) == 0: return df
    df = df.sort_values(['j', 'side']).reset_index(drop=True); keep = []; last = -1
    for k, r in df.iterrows():
        if r.j >= last:
            keep.append(k); last = r.xb
    return df.loc[keep]

def streak(b):
    m = c = 0
    for x in b: c = c + 1 if x else 0; m = max(m, c)
    return m

def stats(df, months):
    if len(df) < 2: return dict(Trades=len(df))
    u = df.usd.values; R = df.R.values; w = u > 0
    cum = np.cumsum(u); dd = np.max(np.maximum.accumulate(np.r_[0, cum])[1:] - cum)
    mo = df.groupby(df.t.dt.to_period('M')).usd.sum()
    return {'Trades': len(df), 'Trades/Month': len(df) / months, 'WR': w.mean(), 'AvgWin$': u[w].mean() if w.any() else 0, 'AvgLoss$': u[~w].mean() if (~w).any() else 0,
            'AvgRR': R.mean(), 'PF': u[w].sum() / -u[~w].sum() if (~w).any() else np.nan, 't-score': R.mean() / R.std(ddof=1) * np.sqrt(len(R)),
            'NetProfit$': u.sum(), '$/Month': u.sum() / months, 'MaxConsWins': streak(w), 'MaxConsLoss': streak(~w), 'MaxDD$': dd,
            'Net/DD': u.sum() / dd if dd > 0 else np.nan, 'MonthsUp': (mo > 0).mean(), 'AvgStop': df.d.mean()}

def load_all(tf):
    m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
    so = bars[tf]; old = ctx(so, m1, bars['D'], True, tf, so.index[0], so.index[-1], replica4.run(so))
    m15 = load('MNQ', '15m'); m15 = m15[m15.index >= '2025-11-30 18:00']
    mm1 = load('MNQ', '1m'); m5 = load('MNQ', '5m'); dd = load('MNQ', '1d')
    k1 = mm1.index.floor('5min').unique()
    rep = pd.concat([mm1, m5[~m5.index.isin(k1)]]).sort_index(); rep = rep[~rep.index.duplicated()]
    s2 = m15 if tf == '15m' else resample(m15, tf); su = replica4.run(s2)
    segs = [('2026-03-04 19:00', '2026-05-01 16:59'), ('2026-07-02 18:00', '2026-10-16 16:59')]
    news = [ctx(s2, rep, dd, False, tf, pd.Timestamp(a), pd.Timestamp(b), su) for a, b in segs]
    mo_o = (so.index[-1] - so.index[0]).days / 30.44
    mo_n = sum((pd.Timestamp(b) - pd.Timestamp(a)).days for a, b in segs) / 30.44
    return old, news, mo_o, mo_n

def run(L, **kw):
    old, news, mo_o, mo_n = L
    a = trades(old, **kw).assign(period='old'); b = pd.concat([trades(C, **kw) for C in news]).assign(period='new')
    a = one_at_a_time(a); b = pd.concat([one_at_a_time(trades(C, **kw)) for C in news]).assign(period='new') if len(b) else b
    return pd.concat([a, b]), mo_o, mo_n
