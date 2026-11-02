"""Q1: candles that close at 10:00 NY (4H 06-10, 1h 09-10, 15m 09:45, 5m 09:55)"""
import json
from common import *

TD = pd.Timedelta

def first_idx(mask):
    w = np.flatnonzero(mask)
    return w[0] if len(w) else None

def run(key):
    d1 = raw()[key]
    days = good_days(d1)
    out = {}
    recs_all = {}
    for tf in ['4h', '1h', '15m', '5m']:
        m = TFMIN[tf]
        B = bars(key, tf)
        recs = []
        for day in days:
            lab = day + TD(hours=10) - TD(minutes=m)
            nxt = day + TD(hours=10)
            if lab not in B.index or nxt not in B.index: continue
            b = B.loc[lab]
            if b.plab != lab - TD(minutes=m): continue  # previous bar must be the real previous slot
            nb = B.loc[nxt]
            seg = d1[(d1.index >= nxt) & (d1.index < nxt + TD(minutes=m))]
            if len(seg) == 0: continue
            ih = first_idx(seg.high.values > b.high); il = first_idx(seg.low.values < b.low)
            if ih is None and il is None: first = 'none'
            elif il is None or (ih is not None and ih < il): first = 'high'
            elif ih is None or il < ih: first = 'low'
            else: first = 'same'
            took_h = ih is not None; took_l = il is not None
            day1 = d1[(d1.index >= nxt) & (d1.index <= day + TD(hours=15, minutes=59))]
            c16 = day1.close.iloc[-1] if len(day1) and day1.index[-1] >= day + TD(hours=15, minutes=50) else np.nan
            t = b.type; ln = lean(t)
            r = dict(day=str(day.date()), type=t, lean=ln, fam=family(t), first=first, took_h=took_h, took_l=took_l,
                     took_lean=(took_h if ln == 'bull' else took_l), first_lean=(first == ('high' if ln == 'bull' else 'low')),
                     nfam=family(nb.type), nlean=lean(nb.type), ntype=nb.type,
                     c10=b.close, c16=c16, d16=(c16 - b.close) if not np.isnan(c16) else np.nan,
                     rng=b.high - b.low, nclose_pos=('above high' if nb.close > b.high else 'below low' if nb.close < b.low else 'inside'))
            recs.append(r)
        df = pd.DataFrame(recs)
        recs_all[tf] = df
        out[tf] = summarize(df)
    return out, recs_all

def row(g, n_total):
    n = len(g)
    r = {'n': n, 'share%': pct(n, n_total)}
    for k in ['high', 'low', 'same', 'none']:
        r['1st ' + k + '%'] = pct((g['first'] == k).sum(), n)
    r['took HI%'] = pct(g.took_h.sum(), n); r['took LO%'] = pct(g.took_l.sum(), n)
    r['took LEAN ext%'] = pct(g.took_lean.sum(), n)
    r['LEAN ext 1st%'] = pct(g.first_lean.sum(), n)
    for f in FAMS: r['next ' + f + '%'] = pct((g.nfam == f).sum(), n)
    r['next same lean%'] = pct((g.nlean == g.lean).sum(), n)
    dd = g.d16.dropna()
    r['16:00 UP%'] = pct((dd > 0).sum(), len(dd)); r['16:00 DOWN%'] = pct((dd < 0).sum(), len(dd))
    r['16:00 med pts'] = med(dd.tolist()); r['16:00 avg pts'] = mean(dd.tolist())
    # in lean direction
    sgn = np.where(g.lean == 'bull', 1, -1)
    ld = (g.d16 * sgn).dropna()
    r['16:00 WITH lean%'] = pct((ld > 0).sum(), len(ld)); r['16:00 med pts WITH lean'] = med(ld.tolist())
    return r

def summarize(df):
    N = len(df)
    res = {'by_type': [], 'by_lean': [], 'by_family': []}
    for t in TYPES:
        g = df[df.type == t]
        res['by_type'].append({'key': t, **row(g, N)})
    for ln in ['bull', 'bear']:
        res['by_lean'].append({'key': ln, **row(df[df.lean == ln], N)})
    for f in FAMS:
        for ln in ['bull', 'bear']:
            g = df[(df.fam == f) & (df.lean == ln)]
            res['by_family'].append({'key': f + ' ' + ln, **row(g, N)})
    res['all'] = {'key': 'ALL', **row(df, N)}
    return res

def extra4h(df):
    """4H 06-10 then 10-14 candle: high/low first and where it closes"""
    out = []
    def r(g, k):
        n = len(g)
        return {'key': k, 'n': n,
                '1st high%': pct((g['first'] == 'high').sum(), n), '1st low%': pct((g['first'] == 'low').sum(), n),
                '1st same%': pct((g['first'] == 'same').sum(), n), 'none%': pct((g['first'] == 'none').sum(), n),
                'took LEAN ext%': pct(g.took_lean.sum(), n),
                'close ABOVE high%': pct((g.nclose_pos == 'above high').sum(), n),
                'close BELOW low%': pct((g.nclose_pos == 'below low').sum(), n),
                'close INSIDE%': pct((g.nclose_pos == 'inside').sum(), n)}
    out.append(r(df, 'ALL'))
    for ln in ['bull', 'bear']: out.append(r(df[df.lean == ln], ln + ' lean'))
    for t in TYPES: out.append(r(df[df.type == t], t))
    return out

if __name__ == '__main__':
    res = {}
    for key, name in PERIODS.items():
        o, recs = run(key)
        o['4h_next_10_14'] = extra4h(recs['4h'])
        res[name] = o
        for tf, df in recs.items(): df.to_csv(f'/home/claude/ten/q1_{key}_{tf}.csv', index=False)
        print(name, {tf: len(df) for tf, df in recs.items()})
    json.dump(res, open('/home/claude/ten/q1.json', 'w'), indent=1, default=str)
