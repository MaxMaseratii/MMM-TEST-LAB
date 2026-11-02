"""Q3: pullback inside the 10:00-14:00 4H candle"""
import json
from common import *

TD = pd.Timedelta

def run(key):
    d1 = raw()[key]; H4 = bars(key, '4h'); recs = []
    for day in good_days(d1):
        a = day + TD(hours=6); b = day + TD(hours=10)
        if a not in H4.index: continue
        A = H4.loc[a]
        if A.plab != day + TD(hours=2): continue
        w = d1[(d1.index >= b) & (d1.index < b + TD(hours=4))]
        if len(w) < 200: continue
        o = w.open.iloc[0]; c = w.close.iloc[-1]; hi = w.high.max(); lo = w.low.min()
        ln = lean(A.type); rngA = A.high - A.low; rngB = hi - lo
        t_lo = w.low.idxmin(); t_hi = w.high.idxmax()
        if ln == 'bull':
            adv = max(0.0, o - lo); t_adv = t_lo
            fav = max(0.0, hi - o)
        else:
            adv = max(0.0, hi - o); t_adv = t_hi
            fav = max(0.0, o - lo)
        # (b) 10-14 candle itself
        up = c > o
        if up:
            dd = o - lo; dd_before = o - w.loc[:t_hi].low.min(); low_first = t_lo <= t_hi
        else:
            dd = hi - o; dd_before = w.loc[:t_lo].high.max() - o; low_first = t_hi <= t_lo
        recs.append(dict(day=str(day.date()), type=A.type, lean=ln, fam=family(A.type), rngA=rngA, adv=adv,
                         adv_pctA=100 * adv / rngA if rngA else np.nan, adv_min=(t_adv - b).total_seconds() / 60,
                         fav=fav, up=up, dd=dd, dd_before=max(0.0, dd_before), dd_pctB=100 * dd / rngB if rngB else np.nan,
                         opp_first=low_first, rngB=rngB, closes_with_lean=(up == (ln == 'bull'))))
    return pd.DataFrame(recs)

def tbl_a(df):
    out = []
    groups = [('ALL', df), ('bull lean', df[df.lean == 'bull']), ('bear lean', df[df.lean == 'bear'])]
    groups += [('lean RIGHT (10-14 closes with lean)', df[df.closes_with_lean]), ('lean WRONG', df[~df.closes_with_lean])]
    groups += [('bull lean RIGHT', df[(df.lean == 'bull') & df.closes_with_lean]), ('bear lean RIGHT', df[(df.lean == 'bear') & df.closes_with_lean])]
    groups += [(f, df[df.fam == f]) for f in FAMS]
    for k, g in groups:
        n = len(g); t = g.adv_min
        out.append({'key': k, 'n': n, 'med adverse pts': med(g.adv.tolist()), 'p75 adverse pts': q(g.adv.tolist(), 75),
                    'p90 adverse pts': q(g.adv.tolist(), 90),
                    'med adverse % of 06-10 range': med(g.adv_pctA.tolist()), 'p75 adverse %': q(g.adv_pctA.tolist(), 75),
                    'adverse <=10 pts%': pct((g.adv <= 10).sum(), n), 'adverse >=50 pts%': pct((g.adv >= 50).sum(), n),
                    'med 06-10 range pts': med(g.rngA.tolist()), 'med min to worst pt': med(t.tolist()),
                    'worst by 10:30%': pct((t < 30).sum(), n), 'worst 10:30-11%': pct(((t >= 30) & (t < 60)).sum(), n),
                    'worst 11-12%': pct(((t >= 60) & (t < 120)).sum(), n), 'worst 12-13%': pct(((t >= 120) & (t < 180)).sum(), n),
                    'worst 13-14%': pct((t >= 180).sum(), n),
                    'med favour pts': med(g.fav.tolist()), '10-14 closes WITH lean%': pct(g.closes_with_lean.sum(), n)})
    return out

def tbl_b(df):
    out = []
    for ln in ['ALL', 'bull', 'bear']:
        g0 = df if ln == 'ALL' else df[df.lean == ln]
        for up in [True, False]:
            g = g0[g0.up == up]; n = len(g)
            out.append({'key': f'{ln} lean / 10-14 closes {"UP" if up else "DOWN"}', 'n': n, 'share%': pct(n, len(g0)),
                        'med pts against open first': med(g.dd_before.tolist()), 'p75 pts against first': q(g.dd_before.tolist(), 75),
                        'med wick vs open pts (any time)': med(g.dd.tolist()), 'p75 wick pts': q(g.dd.tolist(), 75),
                        'med wick % of 10-14 range': med(g.dd_pctB.tolist()), 'p75 wick %': q(g.dd_pctB.tolist(), 75),
                        'opposite extreme made FIRST%': pct(g.opp_first.sum(), n), 'med 10-14 range pts': med(g.rngB.tolist())})
    return out

if __name__ == '__main__':
    res = {}
    for key, name in PERIODS.items():
        df = run(key); df.to_csv(f'/home/claude/ten/q3_{key}.csv', index=False)
        res[name] = {'a_adverse_vs_0610_lean': tbl_a(df), 'b_1014_candle': tbl_b(df)}
        print(name, len(df))
    json.dump(res, open('/home/claude/ten/q3.json', 'w'), indent=1, default=str)
