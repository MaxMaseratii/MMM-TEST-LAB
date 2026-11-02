"""Combine every Chart Fanatics strategy test -> site/data.json for the claims-vs-results website.
For each strategy: full grid pass counts (real vs random), the trader's own headline rule(s) + Max's fixed 1:2, year-by-year, dollars,
and the multi-account burn simulation on the headline rule."""
import sys, json, glob, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, '/home/claude/mmmlab'); sys.path.insert(0, '/home/claude/cf'); sys.path.insert(0, '/home/claude/cf2')
from mmmlab import money as MO, propsim as PS
from headlines import HEAD, CLAIMS
import inspect, cfstrat as CS1, cfstrat2 as CS2, cfstrat3 as CS3, cfstrat4 as CS4
FN = {'Fabio Valentini': CS1.fabio, 'JJ Simon': CS1.jj_simon, 'Okala': CS1.okala, 'Candace Lau': CS1.candace, 'Dhesi': CS1.dhesi, 'Marci Silfrain': CS1.marci,
      'TG Capital': CS2.tg_capital, 'Tori Trades': CS2.tori, 'Jade Cap': CS2.jadecap, 'Trader Kane': CS2.kane, 'Tanja Trades': CS2.tanja,
      'Andrea Cimitan': CS3.cimitan, 'Carmine Rosato': CS3.rosato, 'Forrest Knight': CS3.knight, 'Rajan Dhall': CS3.dhall, 'Anthony Crudele': CS3.crudele,
      'Trader Mayne': CS4.mayne, 'Marco Trades': CS4.marco, 'Vincent Desiano': CS4.desiano, 'Abraham Perez': CS4.perez, 'Trader Yush': CS4.yush}
METHOD = {k: ' '.join((inspect.getdoc(f) or '').split()) for k, f in FN.items()}

T = pd.concat([pd.read_parquet('/home/claude/cf/cf_all.parquet')] + [pd.read_parquet(f) for f in sorted(glob.glob('/home/claude/cf2/trades_*.parquet'))], ignore_index=True)
T['tf'] = T.tf.astype(int)


def r(v, d=3):
    try:
        v = float(v); return None if not np.isfinite(v) else round(v, d)
    except Exception: return None


def st(x):
    x = pd.Series(x).dropna(); n = len(x)
    if n < 2: return [n, None, None, None, None]
    pos = x[x > 0].sum(); neg = -x[x <= 0].sum()
    return [n, r((x > 0).mean()), r(x.mean()), r(pos / neg if neg > 0 else np.nan, 2), r(x.mean() / x.std(ddof=1) * np.sqrt(n), 2) if x.std() > 0 else None]


def tval(x):
    x = pd.Series(x).dropna(); return x.mean() / x.std(ddof=1) * np.sqrt(len(x)) if len(x) > 2 and x.std() > 0 else np.nan


def pick(strat, m, tf, f):
    z = T[(T.strat == strat) & (T.m == m) & (T.tf == tf)]
    for k, v in f.items():
        if k == 'tagstart': z = z[z.tag.str.startswith(v)]
        elif k == 'tagnot': z = z[~z.tag.str.contains(v)]
        else: z = z[z[k].isin(v if isinstance(v, list) else [v])]
    return z


OUT = {'strategies': []}
KEYS = ['m', 'tf', 'entry', 'stop', 'target', 'exit']
for strat in HEAD:
    Z = T[T.strat == strat]
    if not len(Z): print('no trades', strat); continue
    # grid pass counts
    tested = passed = rp = 0; grid = []
    for k, g in Z.groupby(KEYS):
        a = g[g.per == 'P1']; b = g[g.per == 'P2']
        ok = len(a) >= 30 and len(b) >= 30
        t1, t2 = tval(a.r), tval(b.r); q1, q2 = tval(a.r_rand), tval(b.r_rand)
        tested += ok; passed += ok and t1 >= 2 and t2 >= 2; rp += ok and q1 >= 2 and q2 >= 2
        grid.append(list(k[:2]) + [str(x) for x in k[2:]] + st(a.r) + [r(a.r_rand.mean())] + st(b.r) + [r(b.r_rand.mean())])
    best = max(grid, key=lambda g: min(g[10] if g[10] is not None else -99, g[16] if g[16] is not None else -99) if (g[6] or 0) >= 30 and (g[12] or 0) >= 30 else -999)
    rows = []; years = []; burn = []; money = []
    for lab, m, tf, f, risk, ml in HEAD[strat]:
        z = pick(strat, m, tf, f)
        if not len(z): print('EMPTY', strat, lab); continue
        a = z[z.per == 'P1']; b = z[z.per == 'P2']
        rows.append([lab, m, tf] + st(a.r) + [r(a.r_rand.mean())] + st(b.r) + [r(b.r_rand.mean())])
        y = z.assign(yr=pd.to_datetime(z.te).dt.year)
        years.append([lab, m, tf, [[int(yy), len(x), r((x.r > 0).mean()), r(x.r.mean()), r(x.r_rand.mean())] for yy, x in y.groupby('yr') if len(x) >= 3]])
        if risk:
            for p, x in (('P1', a), ('P2', b)):
                x = x[['te', 'tx', 'r', 'r_rand']].dropna()
                if len(x) < 10: continue
                A = MO.account(x, risk_usd=risk, max_losses=ml)
                mm = MO.monthly(A); pr = MO.prop(A)
                money.append([lab, m, tf, p, len(A), r(mm['per_month'], 0), r(mm['best'], 0), r(mm['worst'], 0), r(mm['green']), len(pr), r(pr.count('pass') / max(1, len(pr)), 2), risk])
                for n, cost, kind in ((1, 100, 'generic'), (5, 100, 'generic'), (20, 100, 'generic'), (45, 100, 'generic'), (20, 50, 'generic'), (20, 300, 'generic'), (1, 25, 'Apex-like'), (20, 25, 'Apex-like'), (45, 25, 'Apex-like')):
                    kw = dict(eval_cost=cost) if kind == 'generic' else dict(eval_cost=cost, activation=79.0, cap=2000.0, max_pays=6)
                    ra = PS.slots(A, risk_usd=risk, n=n, col='r', stagger=5, **kw)
                    rb = PS.slots(A, risk_usd=risk, n=n, col='r_rand', stagger=5, **kw)
                    burn.append([lab, m, tf, p, n, cost if kind == 'generic' else '25 + $79 activation', len(A), r(A.r.mean()), r(A.r_rand.mean()), int(ra['evals']), r(ra['spent'], 0), int(ra['payouts']), r(ra['paid'], 0), r(ra['best_month'], 0), r(ra['net'], 0),
                                 int(rb['evals']), r(rb['paid'], 0), r(rb['best_month'], 0), r(rb['net'], 0), kind])
    OUT['strategies'].append(dict(name=strat, claims=CLAIMS.get(strat, {}), method=METHOD.get(strat, ''), tested=int(tested), passed=int(passed), rpassed=int(rp), combos=len(grid),
                                  best=best, rules=rows, years=years, money=money, burn=burn, grid=grid))
    print(f'{strat}: combos {len(grid)} tested {tested} passed {passed} random {rp}', flush=True)
json.dump(OUT, open('/home/claude/cf2/site/data.json', 'w'), separators=(',', ':'))
print('saved', len(json.dumps(OUT)) // 1024, 'KB')
