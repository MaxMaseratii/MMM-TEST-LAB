"""Q2: UPG gaps made 09:30-10:00 on 5m and 1m"""
import json
from common import *

TD = pd.Timedelta

def first(mask):
    w = np.flatnonzero(mask)
    return w[0] if len(w) else None

def run(key):
    d1 = raw()[key]
    days = good_days(d1)
    B5 = bars(key, '5m')
    H4 = bars(key, '4h')
    one = d1.copy()
    recs = []
    for tf in ['5m', '1m']:
        m = 5 if tf == '5m' else 1
        S = B5 if tf == '5m' else one
        for day in days:
            lab4 = day + TD(hours=6)
            lean4 = lean(H4.loc[lab4].type) if lab4 in H4.index else None
            dayseg = d1[(d1.index >= day + TD(hours=9)) & (d1.index < day + TD(hours=17))]
            b5d = B5[(B5.index >= day + TD(hours=9)) & (B5.index < day + TD(hours=16))]
            c3labs = pd.date_range(day + TD(hours=9, minutes=30), day + TD(hours=10) - TD(minutes=m), freq=f'{m}min')
            for c3t in c3labs:
                c2t = c3t - TD(minutes=m); c1t = c2t - TD(minutes=m)
                if not (c3t in S.index and c2t in S.index and c1t in S.index): continue
                c1 = S.loc[c1t]; c2 = S.loc[c2t]; c3 = S.loc[c3t]
                if c2.close > c1.high and c3.low > c1.high:
                    dr = 1; near = c3.low; far = c1.high
                elif c2.close < c1.low and c3.high < c1.low:
                    dr = -1; near = c3.high; far = c1.low
                else: continue
                T = c3t + TD(minutes=m)
                after = dayseg[(dayseg.index >= T) & (dayseg.index < day + TD(hours=16))]
                r = dict(day=str(day.date()), tf=tf, dir='bull' if dr == 1 else 'bear', c3=str(c3t.time()),
                         size=abs(near - far), lean4=lean4, agree4=(lean4 == ('bull' if dr == 1 else 'bear')))
                if dr == 1:
                    it = first(after.low.values <= near); ifl = first(after.low.values < far)
                else:
                    it = first(after.high.values >= near); ifl = first(after.high.values > far)
                r['touched'] = it is not None
                r['filled'] = ifl is not None
                r['min_to_touch'] = None if it is None else (after.index[it] - T).total_seconds() / 60
                r['min_to_fill'] = None if ifl is None else (after.index[ifl] - T).total_seconds() / 60
                r['outcome'] = 'untouched'
                if it is not None:
                    tt = after.index[it]
                    b5a = b5d[b5d.index >= tt.floor('5min')]
                    if dr == 1:
                        ir = first(b5a.close.values > near); ifa = first(b5a.close.values < far)
                    else:
                        ir = first(b5a.close.values < near); ifa = first(b5a.close.values > far)
                    if ir is None and ifa is None: r['outcome'] = 'neither'
                    else:
                        if ifa is None or (ir is not None and ir < ifa): r['outcome'] = 'react'; k = ir
                        else: r['outcome'] = 'fail'; k = ifa
                        cb = b5a.iloc[k]
                        r['out_type'] = cb.type; r['out_fam'] = family(cb.type); r['out_lean'] = lean(cb.type)
                        r['out_side'] = 'up' if cb.close > near and cb.close > far else 'down'
                        r['out_time'] = str(b5a.index[k].time())
                        side_bull = r['out_side'] == 'up'
                        r['with_gap'] = (side_bull == (dr == 1))
                        r['with_4h'] = None if lean4 is None else (side_bull == (lean4 == 'bull'))
                        r['candle_lean_matches_side'] = (r['out_lean'] == ('bull' if side_bull else 'bear'))
                if ifl is not None:
                    ft = after.index[ifl]
                    w = d1[(d1.index >= ft) & (d1.index < ft + TD(minutes=60))]
                    w_after = w.iloc[1:]
                    if dr == 1:
                        cont = far - w.low.min(); rev = (w_after.high.max() - far) if len(w_after) else 0.0
                        back = first(w_after.high.values > near)
                        c30 = first(w.low.values <= far - 30); c60 = first(w.low.values <= far - 60)
                        back16 = (dayseg[(dayseg.index > ft) & (dayseg.index < day + TD(hours=16))].high > near).any()
                        r30 = first(w_after.high.values >= far + 30)
                    else:
                        cont = w.high.max() - far; rev = (far - w_after.low.min()) if len(w_after) else 0.0
                        back = first(w_after.low.values < near)
                        c30 = first(w.high.values >= far + 30); c60 = first(w.high.values >= far + 60)
                        back16 = (dayseg[(dayseg.index > ft) & (dayseg.index < day + TD(hours=16))].low < near).any()
                        r30 = first(w_after.low.values <= far - 30)
                    r['fill_cont_mfe60'] = cont; r['fill_rev_mfe60'] = rev
                    r['fill_c30'] = c30 is not None; r['fill_c60'] = c60 is not None
                    r['fill_back60'] = back is not None; r['fill_back16'] = bool(back16)
                    bk = None if back is None else back + 1  # index in w
                    if c30 is None and bk is None: r['fill_race'] = 'neither'
                    elif bk is None or (c30 is not None and c30 < bk): r['fill_race'] = 'cont30 first'
                    elif c30 is None or bk < c30: r['fill_race'] = 'back first'
                    else: r['fill_race'] = 'same min'
                    r['fill_r30'] = r30 is not None
                    rk = None if r30 is None else r30 + 1
                    if c30 is None and rk is None: r['fill_race30'] = 'neither'
                    elif rk is None or (c30 is not None and c30 < rk): r['fill_race30'] = 'cont30 first'
                    else: r['fill_race30'] = 'rev30 first'
                recs.append(r)
    return pd.DataFrame(recs), len(days)

def summary(df, ndays):
    out = []
    for tf in ['5m', '1m']:
        for dr in ['bull', 'bear', 'all']:
            g = df[df.tf == tf] if dr == 'all' else df[(df.tf == tf) & (df.dir == dr)]
            n = len(g); t = g[g.touched]
            nt = len(t)
            out.append({'key': f'{tf} {dr}', 'n gaps': n, 'gaps/day': round(n / ndays, 2), 'med size pts': med(g['size'].tolist()),
                        'touched%': pct(nt, n), 'med min to touch': med(t.min_to_touch.tolist()), 'p75 min to touch': q(t.min_to_touch.tolist(), 75),
                        'touched <=5 min%': pct((t.min_to_touch <= 5).sum(), n), 'touched <=30 min%': pct((t.min_to_touch <= 30).sum(), n),
                        'full fill%': pct(g.filled.sum(), n), 'fill if touched%': pct(t.filled.sum(), nt),
                        'n touched': nt, 'REACT%': pct((t.outcome == 'react').sum(), nt), 'FAIL%': pct((t.outcome == 'fail').sum(), nt),
                        'neither%': pct((t.outcome == 'neither').sum(), nt)})
    return out

def by_agree(df):
    out = []
    for tf in ['5m', '1m']:
        for ag in [True, False]:
            g = df[(df.tf == tf) & (df.agree4 == ag)]; t = g[g.touched]; n = len(g); nt = len(t)
            out.append({'key': f'{tf} gap {"WITH" if ag else "AGAINST"} 4H 06-10 lean', 'n gaps': n, 'touched%': pct(nt, n),
                        'full fill%': pct(g.filled.sum(), n), 'n touched': nt,
                        'REACT%': pct((t.outcome == 'react').sum(), nt), 'FAIL%': pct((t.outcome == 'fail').sum(), nt)})
    return out

def after_fill(df):
    out = []
    for tf in ['5m', '1m']:
        for dr in ['bull', 'bear', 'all']:
            g = df[(df.tf == tf) & df.filled] if dr == 'all' else df[(df.tf == tf) & df.filled & (df.dir == dr)]
            n = len(g)
            out.append({'key': f'{tf} {dr}', 'n fills': n,
                        'cont 30 pts in 60m%': pct(g.fill_c30.sum(), n), 'cont 60 pts in 60m%': pct(g.fill_c60.sum(), n),
                        'back past gap in 60m%': pct(g.fill_back60.sum(), n), 'back past gap by 16:00%': pct(g.fill_back16.sum(), n),
                        'cont30 FIRST (vs back past gap)%': pct((g.fill_race == 'cont30 first').sum(), n), 'back past gap FIRST%': pct((g.fill_race == 'back first').sum(), n),
                        'rev 30 pts in 60m%': pct(g.fill_r30.sum(), n),
                        'cont30 FIRST (vs rev30)%': pct((g.fill_race30 == 'cont30 first').sum(), n), 'rev30 FIRST%': pct((g.fill_race30 == 'rev30 first').sum(), n),
                        'med pts same way (60m)': med(g.fill_cont_mfe60.tolist()), 'p75 pts same way': q(g.fill_cont_mfe60.tolist(), 75),
                        'med pts reverse (60m)': med(g.fill_rev_mfe60.tolist()), 'p75 pts reverse': q(g.fill_rev_mfe60.tolist(), 75)})
    return out

def out_candles(df):
    res = {}
    for tf in ['5m', '1m']:
        for side in ['react', 'fail', 'all', 'bull react', 'bull fail', 'bear react', 'bear fail']:
            g = df[(df.tf == tf) & (df.outcome.isin(['react', 'fail']))]
            if side in ('react', 'fail'): g = g[g.outcome == side]
            elif side != 'all': g = g[(g.dir == side.split()[0]) & (g.outcome == side.split()[1])]
            n = len(g)
            vc = g.out_type.value_counts().head(5)
            fc = g.out_fam.value_counts()
            res[f'{tf} {side}'] = {'n': n, 'top5 types': [[k, int(v), pct(v, n)] for k, v in vc.items()],
                                   'families': [[k, int(v), pct(v, n)] for k, v in fc.items()],
                                   'close WITH gap dir%': pct(g.with_gap.sum(), n),
                                   'close WITH 4H lean%': pct(g.with_4h.fillna(False).astype(bool).sum(), g.with_4h.notna().sum()),
                                   'candle lean = close side%': pct(g.candle_lean_matches_side.sum(), n)}
    return res

if __name__ == '__main__':
    res = {}
    for key, name in PERIODS.items():
        df, nd = run(key)
        df.to_csv(f'/home/claude/ten/q2_{key}_gaps.csv', index=False)
        res[name] = {'days': nd, 'summary': summary(df, nd), 'by_4h_lean': by_agree(df), 'after_full_fill': after_fill(df),
                     'first_5m_close_outside': out_candles(df)}
        print(name, len(df))
    json.dump(res, open('/home/claude/ten/q2.json', 'w'), indent=1, default=str)
