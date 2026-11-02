"""Per-trade check of grid picks (replica4 events), old NQ + new MNQ, one trade per candle per side."""
import sys, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import load, resample, simulate, map_replay, exit_events, EXIT_MO, TICK, atr
from rows import datr_prev_map
import fva_grid as G, replica4
XMO = np.r_[EXIT_MO, 0].astype(np.int64)
XI = {'X0': 0, 'XO': 1, 'XN2': 2, 'XN3': 3, 'XN4': 4, 'XN2A': 5, 'XN2W': 6, 'XN2R': 7, 'XSA': 8, 'XSB': 9, 'XSF': 10, 'XH': 11}
MIN = {'5m': 5, '15m': 15, '1h': 60, '4h': 240}
_cache = {}

def _setups(key, sig):
    if key not in _cache:
        _cache[key] = replica4.run(sig)
    return _cache[key]

def trades(sig, rep, daily, dk, tf, t0, t1, spec, ckey):
    et, side, sess, stop, rk, ex = spec
    full = sig
    sig = sig[(sig.index >= t0) & (sig.index <= t1)]
    rep = rep[(rep.index >= t0) & (rep.index <= pd.Timestamp(t1) + pd.Timedelta(days=1))]
    ss = [s for s in _setups(ckey, full) if s['etype'] == et and t0 <= s['t'] <= t1]
    datr = datr_prev_map(sig.index, daily, dk); a = atr(sig); se = G.sess_of(sig.index)
    ev = exit_events(sig); hn = G.next_true(G.hold_event(sig, MIN[tf]))
    evN = np.concatenate([ev, np.stack([hn, hn])[:, None, :]], axis=1)
    pos = {t: k for k, t in enumerate(sig.index)}
    c = sig.close.values; n = len(c); R = []; meta = []
    for s in ss:
        i = pos.get(pd.Timestamp(s['t']))
        if i is None or i < 20 or i >= n - 1 or np.isnan(a[i]): continue
        sd = 1 if s['long'] else -1
        if side != 'both' and (sd == 1) != (side == 'long'): continue
        if sess != 'All' and G.SESS[se[i]] != sess: continue
        e0 = c[i] if s['mkt'] else s['ep']
        if not s['mkt'] and not (sd * (c[i] - s['ep']) > 0): continue
        sp = {'fix': e0 - sd * 50, 'box': s['sl'], 'swing': s['swing'], 'atr1': e0 - sd * a[i], 'atr15': e0 - sd * 1.5 * a[i], 'datr': e0 - sd * 0.15 * datr[i]}[stop]
        if sp is None or np.isnan(sp): continue
        R.append([i, sd, np.nan if s['mkt'] else s['ep'], sp, s['tgt'] if s['tgt'] is not None else np.nan, 0]); meta.append(s['t'])
    rows = np.array(R, float).reshape(-1, 6)
    if len(rows) == 0: return pd.DataFrame(columns=['t', 'j', 'side', 'R', 'd'])
    sF, sL, r2s = map_replay(sig, rep)
    rkv = np.array([rk if rk != 'TGT' else 1.0])
    acc, cnt, keep = simulate(rep.open.values, rep.high.values, rep.low.values, rep.close.values, sF, sL, r2s, c, n,
                              rows[:, 0].astype(np.int64), rows[:, 1].astype(np.int64), rows[:, 2], rows[:, 3], rows[:, 4],
                              rows[:, 5].astype(np.int64), 1, rkv, evN, XMO, 5, 100, 1.0, 2.0, TICK, 1 if rk == 'TGT' else 0, XI[ex])
    e = np.where(np.isnan(rows[:, 2]), c[rows[:, 0].astype(int)], rows[:, 2])
    df = pd.DataFrame({'t': sig.index[rows[:, 0].astype(int)], 'j': rows[:, 0].astype(int), 'side': rows[:, 1], 'R': keep, 'd': np.abs(e - rows[:, 3])})
    return df.dropna(subset=['R'])

def all_trades(tf, spec):
    m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
    sig = bars[tf]
    old = trades(sig, m1, bars['D'], True, tf, sig.index[0], sig.index[-1], spec, ('old', tf)).assign(period='old')
    m15 = load('MNQ', '15m'); m15 = m15[m15.index >= '2025-11-30 18:00']
    mm1 = load('MNQ', '1m'); m5 = load('MNQ', '5m'); dd = load('MNQ', '1d')
    k1 = mm1.index.floor('5min').unique()
    rep = pd.concat([mm1, m5[~m5.index.isin(k1)]]).sort_index(); rep = rep[~rep.index.duplicated()]
    s2 = m15 if tf == '15m' else (m5 if tf == '5m' else resample(m15, tf))
    segs = [('2026-09-01 00:00', '2026-10-16 16:59')] if tf == '5m' else [('2026-03-04 19:00', '2026-05-01 16:59'), ('2026-07-02 18:00', '2026-10-16 16:59')]
    new = pd.concat([trades(s2, rep, dd, False, tf, pd.Timestamp(a), pd.Timestamp(b), spec, ('new', tf)) for a, b in segs]).assign(period='new')
    return pd.concat([old, new]).drop_duplicates(['period', 'j', 'side'])

def stats(R):
    R = np.asarray(R, float); n = len(R)
    if n < 2: return dict(n=n)
    w = R > 0; avg = R.mean(); sd = R.std(ddof=1)
    cum = np.cumsum(R); dd = np.max(np.maximum.accumulate(np.r_[0, cum])[1:] - cum)
    def streak(b):
        m = c = 0
        for x in b: c = c + 1 if x else 0; m = max(m, c)
        return m
    return dict(n=n, WR=w.mean(), PF=R[w].sum() / -R[~w].sum() if (~w).any() else np.nan, avgR=avg, t=avg / sd * np.sqrt(n), netR=R.sum(), DD=dd, maxW=streak(w), maxL=streak(~w))

def report(name, tf, spec, save=None):
    df = all_trades(tf, spec)
    if save: df.to_parquet(save)
    out = [name]
    for lab, g in [('old', df[df.period == 'old']), ('new', df[df.period == 'new']), ('both', df)]:
        s = stats(g.R.values)
        if s.get('n', 0) < 2: out.append(f'{lab}: n{s.get("n",0)}'); continue
        out.append(f"{lab}: n{s['n']} WR {s['WR']*100:.0f}% PF {s['PF']:.2f} avg {s['avgR']:+.2f} t {s['t']:.1f} | stop {g.d.mean():.0f}pt | W/L streak {s['maxW']}/{s['maxL']} DD {s['DD']:.1f}R")
    y = df[df.period == 'old'].copy(); y['y'] = y.t.dt.year
    out.append('years: ' + ' | '.join(f"{k}: n{len(g)} WR {(g.R>0).mean()*100:.0f}% {g.R.mean():+.2f}" for k, g in y.groupby('y') if len(g) > 3))
    print('\n  '.join(out), flush=True)
    return df

if __name__ == '__main__':
    P = [('A1 1h Fail+C both Asia box 1:1.5 X0', '1h', ('Fail+C', 'both', 'Asia 18-02', 'box', 1.5, 'X0')),
         ('A2 1h Fail+C both Asia fix50 1:1.5 XN2W', '1h', ('Fail+C', 'both', 'Asia 18-02', 'fix', 1.5, 'XN2W')),
         ('A3 1h Fail+C both Asia box 1:1 XN4', '1h', ('Fail+C', 'both', 'Asia 18-02', 'box', 1.0, 'XN4')),
         ('A4 1h Fail+C both Asia fix50 1:2 XN2W', '1h', ('Fail+C', 'both', 'Asia 18-02', 'fix', 2.0, 'XN2W')),
         ('B1 1h FailC both Asia fix50 1:1.5 XH', '1h', ('FailC', 'both', 'Asia 18-02', 'fix', 1.5, 'XH')),
         ('B2 1h FailC both Asia fix50 1:1 X0', '1h', ('FailC', 'both', 'Asia 18-02', 'fix', 1.0, 'X0')),
         ('C1 4h FailC long swing 1:1 X0', '4h', ('FailC', 'long', 'All', 'swing', 1.0, 'X0')),
         ('C2 4h FailC long atr1.5 1:6 X0', '4h', ('FailC', 'long', 'All', 'atr15', 6.0, 'X0')),
         ('D1 4h FailC both Asia datr 1:0.5 XH', '4h', ('FailC', 'both', 'Asia 18-02', 'datr', 0.5, 'XH')),
         ('E1 1h Fail+C long datr 1:4 XN2W (4.0 M1)', '1h', ('Fail+C', 'long', 'All', 'datr', 4.0, 'XN2W'))]
    for nm, tf, sp in P:
        report(nm, tf, sp, save=f'/home/claude/fva/pick_{nm.split()[0]}.parquet')
