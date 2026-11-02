"""FVA Break 3.1 edge grid, run through the established MMM test engine (rt/eng/core.simulate).
Every entry type x side x session x entry mode x 6 stops x 7 targets x 12 exits, old (NQ 2022-25, 1m replay)
and new (MNQ 2026, 1m replay, 5m where 1m is missing). Engine rules: limits fill 1 tick through, stop wins ties,
stop >= 2 pts, 1 pt cost, 100-candle max. RANDOM rows = luck baseline."""
import sys, numpy as np, pandas as pd, time, pickle
sys.path.insert(0, '/home/claude/rt/eng'); sys.path.insert(0, '/home/claude/fva')
from core import load, resample, atr, simulate, map_replay, exit_events, EXITS, EXIT_MO, TICK
from rows import datr_prev_map
from replica2 import run as replica_run

OUT = '/home/claude/fva/grid'
TYPES = ['PES/PEL', 'PES/PEL+', 'CDL/CDS', 'CDL/CDS+', 'Nest PES/PEL(+)', 'Nest CDL/CDS(+)', 'BuX/BeX', 'LQG', 'Fail', 'Fail+', 'RANDOM']
SIDES = ['long', 'short']
SESS = ['Asia 18-02', 'London 02-08', 'NY 08-13:30', 'PM 13:30-18']
ENTS = ['native', 'limit at open']
STOPS = ['S0 fixed 50', 'S1 box', 'S2 swing', 'S3 ATR x1', 'S4 ATR x1.5', 'S5 daily ATR x0.15']
RK = np.array([1., 1.5, 2., 3., 4., 6.])
TN = ['1:1', '1:1.5', '1:2', '1:3', '1:4', '1:6', 'TGT']
XN = EXITS + ['XH hold to next session open']
XMO = np.r_[EXIT_MO, 0].astype(np.int64)
TOUCH = {'PES/PEL', 'PES/PEL+', 'CDL/CDS', 'CDL/CDS+', 'Nest PES/PEL(+)', 'Nest CDL/CDS(+)'}


def tcat(et):
    if 'Nested' in et and 'PES/PEL' in et: return 'Nest PES/PEL(+)'
    if 'Nested' in et and 'CDL/CDS' in et: return 'Nest CDL/CDS(+)'
    for k, n in (('①', 'PES/PEL'), ('②', 'PES/PEL+'), ('③', 'CDL/CDS'), ('④', 'CDL/CDS+'), ('⑤', 'BuX/BeX'), ('⑥', 'LQG'), ('⑦ Fail+', 'Fail+'), ('⑦ Fail', 'Fail')):
        if k in et: return n
    raise ValueError(et)


def sess_of(idx):
    m = idx.hour * 60 + idx.minute
    return np.select([(m >= 1080) | (m < 120), (m >= 120) & (m < 480), (m >= 480) & (m < 810)], [0, 1, 2], 3)


def hold_event(sig, tf_min):
    """bar whose CLOSE is a session open (18:00, 02:00, 08:00, 09:30)."""
    end = sig.index + pd.Timedelta(minutes=tf_min)
    m = end.hour * 60 + end.minute
    return np.isin(m, [1080, 120, 480, 570])


def next_true(ev):
    n = len(ev); nxt = np.full(n + 1, n, np.int64)
    for j in range(n - 1, -1, -1):
        nxt[j] = j if ev[j] else nxt[j + 1]
    return nxt


def swings(h, l):
    n = len(h); rsl = np.full(n, np.nan); rsh = np.full(n, np.nan)
    a = b = np.nan
    for i in range(2, n):
        if l[i - 1] < l[i - 2] and l[i - 1] < l[i]: a = l[i - 1]
        if h[i - 1] > h[i - 2] and h[i - 1] > h[i]: b = h[i - 1]
        rsl[i] = a; rsh[i] = b
    return rsl, rsh


def gidx(ti, si_, se, en, st):
    return ((((ti * 2 + si_) * 4 + se) * 2 + en) * 6) + st


NG = len(TYPES) * 2 * 4 * 2 * 6


def make_rows(sig, setups, datr, seed):
    """returns (touch_rows, other_rows): [j, side, L, stp, tgt, grp]"""
    o, h, l, c = sig.open.values, sig.high.values, sig.low.values, sig.close.values
    n = len(c); a = atr(sig); sess = sess_of(sig.index)
    T, O = [], []
    pos = {t: k for k, t in enumerate(sig.index)}
    for s in setups:
        i = pos.get(pd.Timestamp(s['t']))
        if i is None:
            continue
        ty = tcat(s['etype']); ti = TYPES.index(ty); sd = 1.0 if s['long'] else -1.0; si_ = 0 if s['long'] else 1
        if ty in TOUCH:
            j = i - 1
            if j < 20 or j >= n - 1 or np.isnan(a[j]) or not (sd * (c[j] - s['ep']) > 0):
                continue
            modes = [(0, s['ep'], j, s['sl'])]
            se = sess[i]
        else:
            j = i
            if j < 20 or j >= n - 1 or np.isnan(a[j]):
                continue
            modes = [(0, np.nan, j, s['sl'])]
            if ty in ('BuX/BeX', 'LQG'):
                modes.append((1, s['ep'], j, s['sl']))   # the candle open as a limit from the next candle
            se = sess[j]
        for en, L, jj, slbox in modes:
            e0 = c[jj] if np.isnan(L) else L
            stops = [e0 - sd * 50.0, slbox, s['swing'], e0 - sd * a[jj], e0 - sd * 1.5 * a[jj], e0 - sd * 0.15 * datr[jj]]
            for st, sp in enumerate(stops):
                if sp is None or np.isnan(sp):
                    continue
                row = [jj, sd, L, sp, s['tgt'] if s['tgt'] is not None else np.nan, gidx(ti, si_, se, en, st)]
                (T if ty in TOUCH else O).append(row)
    # RANDOM: market at a random close, random side, candle stop / swing stop like the others
    rng = np.random.default_rng(seed)
    rsl, rsh = swings(h, l)
    J = rng.choice(np.arange(20, n - 1), size=min(n // 4, 20000), replace=False)
    ti = TYPES.index('RANDOM')
    for j in J:
        if np.isnan(a[j]): continue
        sd = 1.0 if rng.random() < .5 else -1.0; si_ = 0 if sd > 0 else 1
        e0 = c[j]
        stops = [e0 - sd * 50.0, (l[j] - 4 * TICK) if sd > 0 else (h[j] + 4 * TICK), (rsl[j] - 4 * TICK) if sd > 0 else (rsh[j] + 4 * TICK),
                 e0 - sd * a[j], e0 - sd * 1.5 * a[j], e0 - sd * 0.15 * datr[j]]
        for st, sp in enumerate(stops):
            if np.isnan(sp): continue
            O.append([j, sd, np.nan, sp, np.nan, gidx(ti, si_, sess[j], 0, st)])
    return np.array(T, float).reshape(-1, 6), np.array(O, float).reshape(-1, 6)


def sim(sig, rep, rows, evN, W):
    if len(rows) == 0:
        return np.zeros((NG, len(RK) + 1, len(XN), 6)), np.zeros((NG, 3))
    sF, sL, r2s = map_replay(sig, rep)
    acc, cnt, _ = simulate(rep.open.values, rep.high.values, rep.low.values, rep.close.values, sF, sL, r2s,
                           sig.close.values, len(sig), rows[:, 0].astype(np.int64), rows[:, 1].astype(np.int64),
                           rows[:, 2], rows[:, 3], rows[:, 4], rows[:, 5].astype(np.int64), NG, RK, evN, XMO,
                           W, 100, 1.0, 2.0, TICK, -1, -1)
    return acc, cnt


def segment(sig_full, setups, rep, daily, dk, tf_min, seed, t0, t1):
    sig = sig_full[(sig_full.index >= t0) & (sig_full.index <= t1)]
    rep = rep[(rep.index >= t0) & (rep.index <= pd.Timestamp(t1) + pd.Timedelta(days=1))]
    ss = [s for s in setups if t0 <= s['t'] <= t1]
    datr = datr_prev_map(sig.index, daily, dk)
    ev = exit_events(sig)
    hn = next_true(hold_event(sig, tf_min))
    evN = np.concatenate([ev, np.stack([hn, hn])[:, None, :]], axis=1)
    Tr, Or = make_rows(sig, ss, datr, seed)
    a1, c1 = sim(sig, rep, Tr, evN, 1)
    a2, c2 = sim(sig, rep, Or, evN, 5)
    return a1 + a2, c1 + c2


def flatten(acc, cnt, meta):
    A = acc.reshape(len(TYPES), 2, 4, 2, 6, len(TN), len(XN), 6)
    C = cnt.reshape(len(TYPES), 2, 4, 2, 6, 3)
    recs = []
    sides = {'long': [0], 'short': [1], 'both': [0, 1]}
    sessn = {SESS[k]: [k] for k in range(4)}; sessn['All'] = [0, 1, 2, 3]
    for ti, ty in enumerate(TYPES):
        for sn, sl in sides.items():
            for se, sv in sessn.items():
                for en in range(2):
                    for st in range(6):
                        sub = A[ti][np.ix_(sl, sv)][:, :, en, st].sum(axis=(0, 1))   # (K, X, 6)
                        sig_n = C[ti][np.ix_(sl, sv)][:, :, en, st, 0].sum()
                        fills = C[ti][np.ix_(sl, sv)][:, :, en, st, 1].sum()
                        if sub[:, :, 0].max() < 1:
                            continue
                        for k in range(len(TN)):
                            for x in range(len(XN)):
                                nn, w, s1, s2, gw, gl = sub[k, x]
                                if nn < 1: continue
                                recs.append((*meta, ty, sn, se, ENTS[en], STOPS[st], TN[k], XN[x], int(nn), w, s1, s2, gw, gl, sig_n, fills))
    cols = ['period', 'tf', 'type', 'side', 'session', 'entry', 'stop', 'target', 'exit', 'n', 'w', 's', 's2', 'gw', 'gl', 'signals', 'fills']
    return pd.DataFrame(recs, columns=cols)


def run(which):
    t0 = time.time()
    if which == 'old':
        m1, bars = pickle.load(open('/home/claude/rt/cache/old.pkl', 'rb'))
        out = []
        for tf, mins in (('15m', 15), ('1h', 60), ('5m', 5)):
            sig = bars[tf]
            setups = replica_run(sig)
            acc, cnt = segment(sig, setups, m1, bars['D'], True, mins, 7, sig.index[0], sig.index[-1])
            df = flatten(acc, cnt, ('old', tf)); df.to_parquet(f'{OUT}/old_{tf}.parquet')
            print(which, tf, 'setups', len(setups), 'cells', len(df), f'{time.time() - t0:.0f}s', flush=True)
    else:
        m15 = load('MNQ', '15m'); m15 = m15[m15.index >= '2025-11-30 18:00']
        m1 = load('MNQ', '1m'); m5 = load('MNQ', '5m'); dd = load('MNQ', '1d')
        k1 = m1.index.floor('5min').unique()
        rep = pd.concat([m1, m5[~m5.index.isin(k1)]]).sort_index()
        rep = rep[~rep.index.duplicated()]
        segs = [('2026-03-04 19:00', '2026-05-01 16:59'), ('2026-07-02 18:00', '2026-10-16 16:59')]
        for tf, mins in (('15m', 15), ('1h', 60), ('5m', 5)):
            if tf == '5m':
                sig = m5; segs_tf = [('2026-09-01 00:00', '2026-10-16 16:59')]
            else:
                sig = m15 if tf == '15m' else resample(m15, '1h'); segs_tf = segs
            setups = replica_run(sig)
            acc = cnt = 0
            for a_, b_ in segs_tf:
                A_, C_ = segment(sig, setups, rep, dd, False, mins, 11, pd.Timestamp(a_), pd.Timestamp(b_))
                acc = acc + A_; cnt = cnt + C_
            df = flatten(acc, cnt, ('new', tf)); df.to_parquet(f'{OUT}/new_{tf}.parquet')
            print(which, tf, 'setups', len(setups), 'cells', len(df), f'{time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    import os; os.makedirs(OUT, exist_ok=True)
    run(sys.argv[1])
