"""E2 / F: daily rules and prop checks on the best Body Flip candidates (single trades exported from the grid engine)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/pp')
import ppdata, bfeng, bfgrid, bfrun

CANDS = [  # m, tf, window slot (0 all, 1 09:45-12:00), side ('long'/'short'/'both'), e, st, t, x, h, name
    ('NQ', 10, 0, 'long', 0, 7, 6, 0, 0, 'NQ 10m long · market C2 close · ATR x2 trailing · ride'),
    ('NQ', 30, 0, 'long', 2, 3, 6, 0, 0, 'NQ 30m long · limit C2 50% · ATR x0.5 trailing · ride'),
    ('NQ', 15, 0, 'both', 0, 0, 2, 0, 0, 'NQ 15m both · market C2 close · fixed 50 · 1:2'),
    ('NQ', 5, 1, 'both', 0, 0, 2, 0, 0, 'NQ 5m both 09:45-12:00 · market C2 close · fixed 50 · 1:2'),
    ('NQ', 2, 1, 'both', 0, 0, 2, 0, 0, 'NQ 2m both 09:45-12:00 · market C2 close · fixed 50 · 1:2'),
    ('ES', 3, 1, 'both', 4, 0, 0, 1, 1, 'ES 3m both 09:45-12:00 · limit CDS/CDL line · fixed 20 · 1:1 · half'),
]


def trades_for(m, tf, e, st, t, x, h, kw=None):
    kw = kw or {}
    sp = ppdata.SPEC[m]; out = []
    for d in ppdata.series(m, tf):
        S = bfeng.signals(d, **kw)
        flipUp, flipDn, buX, beX, sess, mn = bfrun.bar_arrays(d, S)
        per = (d.per.values == 'P2').astype(np.int64)
        fI = S['fI']
        acc = np.zeros((2, 2, 1, 6, 8, 7, 9, 2, 6))
        keep = np.array([[e, st, t, x, h]], np.int64); outK = np.zeros((len(fI) * 6 + 10, 5))
        mk = np.ones(len(fI), np.int64)
        nout = bfgrid.grade(S['o'], S['h'], S['l'], S['c'], S['trend'], S['lnW'], S['atr'], flipUp, flipDn, buX, beX, sess,
                            fI, S['fS'].astype(np.int64), S['fW1'], S['fL1'], S['fLine'], mk, per[fI], 1,
                            sp['stop'], sp['cost'], sp['tick'], 100, 10, bfgrid.KST, bfgrid.KEX, bfgrid.TGT, acc, keep, outK)
        K = outK[:nout]
        q = K[:, 1].astype(int); i = K[:, 4].astype(int)
        T = pd.DataFrame({'t': d.index.values[i], 'side': S['fS'][q], 'r': K[:, 2], 'risk': K[:, 3], 'per': np.where(per[i] == 1, 'P2', 'P1'),
                          'min': mn[i]})
        out.append(T)
    return pd.concat(out, ignore_index=True).sort_values('t').reset_index(drop=True)


def stats(r):
    n = len(r)
    if n < 2: return dict(n=n)
    pos = r[r > 0].sum(); neg = -r[r <= 0].sum()
    eq = np.cumsum(r); dd = (np.maximum.accumulate(np.r_[0, eq])[1:] - eq).max()
    mx = cur = 0
    for v in r:
        cur = cur + 1 if v <= 0 else 0; mx = max(mx, cur)
    return dict(n=n, wr=(r > 0).mean(), avg=r.mean(), pf=pos / neg if neg > 0 else np.nan, t=r.mean() / r.std(ddof=1) * np.sqrt(n), dd=dd, ml=mx)


def daily(T, mx=3, ml=2):
    day = (pd.to_datetime(T.t)).dt.date.values
    keep = []; cnt = {}; los = {}
    for k, (dd, r) in enumerate(zip(day, T.r.values)):
        if cnt.get(dd, 0) >= mx or los.get(dd, 0) >= ml: continue
        keep.append(k); cnt[dd] = cnt.get(dd, 0) + 1
        if r <= 0: los[dd] = los.get(dd, 0) + 1
    return T.iloc[keep]


def prop(T, pv, risk_usd=150.0, target=3000.0, trail=2000.0, dloss=1000.0):
    """start a 50k evaluation on the first trade of every month; pass = +$3,000 before the trailing EOD drawdown or rules break."""
    T = T.copy(); T['usd'] = T.r * np.maximum(1, np.floor(risk_usd / (T.risk * pv))) * T.risk * pv
    T['day'] = pd.to_datetime(T.t).dt.date; T['mon'] = pd.to_datetime(T.t).dt.to_period('M')
    res = []
    for mo in T.mon.unique():
        S = T[T.t >= T[T.mon == mo].t.min()]
        bal = 0.0; peak = 0.0; out = 'open'
        for dd, g in S.groupby('day', sort=True):
            dsum = 0.0
            for u in g.usd.values:
                if dsum <= -dloss: break
                dsum += u; bal += u
                if bal >= target: out = 'pass'; break
            if out == 'pass': break
            peak = max(peak, bal)
            if bal <= peak - trail: out = 'fail'; break
        res.append(out)
    return res


if __name__ == '__main__':
    rows = []
    for (m, tf, slot, side, e, st, t, x, h, name) in CANDS:
        T = trades_for(m, tf, e, st, t, x, h)
        if slot == 1: T = T[(T['min'] >= 585) & (T['min'] < 720)]
        if side != 'both': T = T[T.side == (1 if side == 'long' else -1)]
        pv = ppdata.SPEC[m]['pv']
        for rule, TT in (('no daily rules', T), ('max 3 a day, stop after 2 losses', daily(T))):
            for p in ('P1', 'P2'):
                s = stats(TT[TT.per == p].r.values)
                months = max(1, (pd.to_datetime(TT[TT.per == p].t).dt.to_period('M').nunique()))
                usd = (TT[TT.per == p].r * TT[TT.per == p].risk * pv).sum() / months
                rows.append(dict(setup=name, rule=rule, per=p, usd_month_1micro=usd, **s))
            pr = prop(TT, pv)
            rows.append(dict(setup=name, rule=rule, per='prop 50k', n=len(pr), wr=pr.count('pass') / max(1, len(pr)), avg=pr.count('fail') / max(1, len(pr))))
        print(name, flush=True)
    R = pd.DataFrame(rows)
    R.to_parquet('prop.parquet')
    pd.set_option('display.width', 250)
    print(R.round(3).to_string())
