"""Re-check every passing idea-grid combo per trade (one trade per candle per side) and rank."""
import sys, pickle, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import load, resample, simulate, map_replay, exit_events, EXIT_MO, TICK, atr
from rows import datr_prev_map
import fva_grid as G, replica4
XMO = np.r_[EXIT_MO, 0].astype(np.int64)
XI = {'X0': 0, 'XO': 1, 'XN2': 2, 'XN3': 3, 'XN4': 4, 'XN2A': 5, 'XN2W': 6, 'XN2R': 7, 'XSA': 8, 'XSB': 9, 'XSF': 10, 'XH': 11}
SK = {'S0 fixed 50': 'fix', 'S1 box': 'box', 'S2 swing': 'swing', 'S3 ATR x1': 'atr1', 'S4 ATR x1.5': 'atr15', 'S5 daily ATR x0.15': 'datr'}
MIN = {'5m': 5, '15m': 15, '1h': 60, '4h': 240}

def ctx(sig_full, rep, daily, dk, tf, t0, t1, setups):
    sig = sig_full[(sig_full.index >= t0) & (sig_full.index <= t1)]
    rep = rep[(rep.index >= t0) & (rep.index <= pd.Timestamp(t1) + pd.Timedelta(days=1))]
    ev = exit_events(sig); hn = G.next_true(G.hold_event(sig, MIN[tf]))
    return dict(sig=sig, rep=rep, ss=[s for s in setups if t0 <= s['t'] <= t1], datr=datr_prev_map(sig.index, daily, dk), a=atr(sig),
                se=G.sess_of(sig.index), evN=np.concatenate([ev, np.stack([hn, hn])[:, None, :]], axis=1), mr=map_replay(sig, rep),
                pos={t: k for k, t in enumerate(sig.index)})

def run_combo(C, r):
    sig = C['sig']; c = sig.close.values; n = len(c); a = C['a']; datr = C['datr']
    side, sess, stop = r.side, r.session, SK[r.stop]
    R = []
    for s in C['ss']:
        if s['etype'] != r.type: continue
        i = C['pos'].get(pd.Timestamp(s['t']))
        if i is None or i < 20 or i >= n - 1 or np.isnan(a[i]): continue
        sd = 1 if s['long'] else -1
        if side != 'both' and (sd == 1) != (side == 'long'): continue
        if sess != 'All' and G.SESS[C['se'][i]] != sess: continue
        if not s['mkt'] and not (sd * (c[i] - s['ep']) > 0): continue
        e0 = c[i] if s['mkt'] else s['ep']
        sp = {'fix': e0 - sd * 50, 'box': s['sl'], 'swing': s['swing'], 'atr1': e0 - sd * a[i], 'atr15': e0 - sd * 1.5 * a[i], 'datr': e0 - sd * 0.15 * datr[i]}[stop]
        if sp is None or np.isnan(sp): continue
        R.append([i, sd, np.nan if s['mkt'] else s['ep'], sp, s['tgt'] if s['tgt'] is not None else np.nan, 0])
    rows = np.array(R, float).reshape(-1, 6)
    if len(rows) == 0: return pd.DataFrame(columns=['t', 'j', 'side', 'R', 'd'])
    sF, sL, r2s = C['mr']; rep = C['rep']
    tg = r.target
    rkv = np.array([1.0 if tg == 'TGT' else float(tg.split(':')[1])])
    _, _, keep = simulate(rep.open.values, rep.high.values, rep.low.values, rep.close.values, sF, sL, r2s, c, n,
                          rows[:, 0].astype(np.int64), rows[:, 1].astype(np.int64), rows[:, 2], rows[:, 3], rows[:, 4],
                          rows[:, 5].astype(np.int64), 1, rkv, C['evN'], XMO, 5, 100, 1.0, 2.0, TICK, 1 if tg == 'TGT' else 0, XI[r.exit.split()[0]])
    e = np.where(np.isnan(rows[:, 2]), c[rows[:, 0].astype(int)], rows[:, 2])
    df = pd.DataFrame({'t': sig.index[rows[:, 0].astype(int)], 'j': rows[:, 0].astype(int), 'side': rows[:, 1], 'R': keep, 'd': np.abs(e - rows[:, 3])})
    return df.dropna(subset=['R'])

def st(R):
    R = np.asarray(R, float); n = len(R)
    if n < 2: return dict(n=n, avg=np.nan, t=np.nan, WR=np.nan)
    sd = R.std(ddof=1)
    return dict(n=n, avg=R.mean(), t=R.mean() / sd * np.sqrt(n) if sd > 0 else np.nan, WR=(R > 0).mean())

m = pd.read_parquet('grid_i/merged.parquet'); P = m[m.PASS & (m.type != 'RANDOM')].copy()
m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
m15 = load('MNQ', '15m'); m15 = m15[m15.index >= '2025-11-30 18:00']
mm1 = load('MNQ', '1m'); m5 = load('MNQ', '5m'); dd = load('MNQ', '1d')
k1 = mm1.index.floor('5min').unique()
rep = pd.concat([mm1, m5[~m5.index.isin(k1)]]).sort_index(); rep = rep[~rep.index.duplicated()]
OUT = []
for tf, g in P.groupby('tf'):
    so = bars[tf]; old = ctx(so, m1, bars['D'], True, tf, so.index[0], so.index[-1], replica4.run(so))
    s2 = m15 if tf == '15m' else (m5 if tf == '5m' else resample(m15, tf))
    segs = [('2026-09-01 00:00', '2026-10-16 16:59')] if tf == '5m' else [('2026-03-04 19:00', '2026-05-01 16:59'), ('2026-07-02 18:00', '2026-10-16 16:59')]
    su = replica4.run(s2)
    news = [ctx(s2, rep, dd, False, tf, pd.Timestamp(a), pd.Timestamp(b), su) for a, b in segs]
    months_o = (so.index[-1] - so.index[0]).days / 30.44
    months_n = sum((pd.Timestamp(b) - pd.Timestamp(a)).days for a, b in segs) / 30.44
    for _, r in g.iterrows():
        do = run_combo(old, r).assign(period='old')
        dn = pd.concat([run_combo(C, r) for C in news]).assign(period='new')
        d = pd.concat([do, dn]).drop_duplicates(['period', 'j', 'side'])
        so_, sn_, sb = st(d[d.period == 'old'].R), st(d[d.period == 'new'].R), st(d.R)
        usd = (d.R * d.d * 2.0).values
        cum = np.cumsum(usd); ddu = np.max(np.maximum.accumulate(np.r_[0, cum])[1:] - cum) if len(cum) else np.nan
        cr = np.cumsum(d.R.values); ddr = np.max(np.maximum.accumulate(np.r_[0, cr])[1:] - cr) if len(cr) else np.nan
        yr = d[d.period == 'old'].groupby(d[d.period == 'old'].t.dt.year).R.mean()
        yr = yr[d[d.period == 'old'].groupby(d[d.period == 'old'].t.dt.year).R.size() >= 10]
        OUT.append(dict(tf=tf, type=r.type, side=r.side, session=r.session, entry=r.entry, stop=r.stop, target=r.target, exit=r.exit,
                        n_o=so_['n'], WR_o=so_['WR'], avg_o=so_['avg'], t_o=so_['t'], n_n=sn_['n'], WR_n=sn_['WR'], avg_n=sn_['avg'], t_n=sn_['t'],
                        n=sb['n'], WR=sb['WR'], avg=sb['avg'], t=sb['t'], netR=d.R.sum(), ddR=ddr, net_usd=usd.sum(), dd_usd=ddu, stop_pts=d.d.mean(),
                        per_month=sb['n'] / (months_o + months_n), worst_year=yr.min() if len(yr) else np.nan))
    print(tf, 'done', flush=True)
R = pd.DataFrame(OUT)
R['PASS2'] = (R.n_o >= 100) & (R.avg_o > 0) & (R.t_o >= 2) & (R.n_n >= 30) & (R.avg_n > 0) & (R.t_n >= 2)
R['usd_month'] = R.net_usd / ((R.n / R.per_month))
R['ret_dd'] = R.net_usd / R.dd_usd
R.to_parquet('grid_i/rank_all.parquet')
print('still pass after one-trade-per-candle:', R.PASS2.sum(), 'of', len(R))
