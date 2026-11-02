"""Summaries for the Chart Fanatics strategy check -> site7/summary.json"""
import sys, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..'))
from mmmlab import money as MO

T = pd.concat([pd.read_parquet('cf_trades_JJ_Candace_Dhesi.parquet'), pd.read_parquet('cf_trades_Okala_Fabio_Marci.parquet').query("strat != 'Fabio Valentini'"), pd.read_parquet('cf_trades_Fabio.parquet')], ignore_index=True)
T['grp'] = T.tag.str.split(' ').str[0]
T.loc[T.strat == 'Fabio Valentini', 'grp'] = T.tag.str.replace(r' \|.*', '', regex=True)
T.loc[T.strat == 'Candace Lau', 'grp'] = T.tag.str.split(' ').str[0]
T.loc[T.strat == 'Marci Silfrain', 'grp'] = T.tag
T.loc[T.strat == 'Okala', 'grp'] = T.tag
T.loc[T.strat == 'Dhesi', 'grp'] = T.tag
FIX = {'NQ': 'fixed', 'ES': 'fixed', 'GC': 'fixed'}


def r(v, d=3):
    try:
        v = float(v); return None if not np.isfinite(v) else round(v, d)
    except Exception: return None


def st(x):
    x = x.dropna(); n = len(x)
    if n < 2: return [n, None, None, None, None]
    pos = x[x > 0].sum(); neg = -x[x <= 0].sum()
    return [n, r((x > 0).mean()), r(x.mean()), r(pos / neg if neg > 0 else np.nan, 2), r(x.mean() / x.std(ddof=1) * np.sqrt(n), 2)]


def stt(x):
    x = x.dropna(); n = len(x)
    return x.mean() / x.std(ddof=1) * np.sqrt(n) if n > 2 and x.std() > 0 else np.nan


def row(z):
    a = z[z.per == 'P1']; b = z[z.per == 'P2']
    return st(a.r) + [r(a.r_rand.mean())] + st(b.r) + [r(b.r_rand.mean())]


KEYS = ['strat', 'm', 'tf', 'entry', 'stop', 'target', 'exit']
S = {}
# ---- every combo, all signals pooled
rows = []; passes = []
for k, g in T.groupby(KEYS):
    z = row(g)
    a = g[g.per == 'P1']; b = g[g.per == 'P2']
    ok = len(a) >= 30 and len(b) >= 30
    ps = ok and (z[4] or -9) >= 2 and (z[10] or -9) >= 2
    rp = ok and stt(a.r_rand) >= 2 and stt(b.r_rand) >= 2
    rows.append(list(k[:2]) + [int(k[2])] + list(k[3:]) + ['all'] + z + [int(ps), int(rp)])
    passes.append((k[0], ok, ps, rp))
# ---- sub-setups (tags)
for k, g in T.groupby(KEYS + ['grp']):
    if T[(T.strat == k[0])].grp.nunique() < 2: continue
    z = row(g); a = g[g.per == 'P1']; b = g[g.per == 'P2']
    ok = len(a) >= 30 and len(b) >= 30
    ps = ok and (z[4] or -9) >= 2 and (z[10] or -9) >= 2
    rp = ok and stt(a.r_rand) >= 2 and stt(b.r_rand) >= 2
    rows.append(list(k[:2]) + [int(k[2])] + list(k[3:7]) + [k[7]] + z + [int(ps), int(rp)])
    passes.append((k[0] + ' (sub-setups)', ok, ps, rp))
S['all'] = rows
P = pd.DataFrame(passes, columns=['strat', 'ok', 'ps', 'rp']).groupby('strat').agg(combos=('ok', 'size'), tested=('ok', 'sum'), passed=('ps', 'sum'), rand=('rp', 'sum'))
S['passes'] = [[k, int(v.combos), int(v.tested), int(v.passed), int(v.rand)] for k, v in P.iterrows()]
print(P)

# ---- their own rules (headline rows) + Max's fixed 1:2
def pick(strat, m, tf, entry, stop, target, exit_, grp=None):
    z = T[(T.strat == strat) & (T.m == m) & (T.tf == tf) & (T.entry == entry) & (T.stop == stop) & (T.target == target) & (T.exit == exit_)]
    if grp is not None: z = z[z.grp.isin(grp if isinstance(grp, list) else [grp])]
    return z


def ptsname(x): return f'pts {round(x, 2)}'


H = []
def add(label, z, strat, m, tf):
    H.append([strat, label, m, tf] + row(z))
    return z


RULES = {}
for m in ('NQ', 'ES'):
    k = 1.0 if m == 'NQ' else 0.4
    RULES[('JJ Simon', m)] = [
        ('Eval rule: 25 pt stop, 1:1.5 target (all entries)', pick('JJ Simon', m, 1, 'market', ptsname(25 * k), '1.52', 'stop/target')),
        ('Reversion to fair price (25 pt stop, target = fair price)', pick('JJ Simon', m, 1, 'market', ptsname(25 * k), 'col tp', 'stop/target', 'REV')),
        ('Continuation, 25 pt stop, 1:4 (his "20% win rate at 1:4")', pick('JJ Simon', m, 1, 'market', ptsname(25 * k), '4', 'stop/target', 'CONT')),
        ('Max fixed 1:2 (50 pts NQ / 20 ES)', pick('JJ Simon', m, 1, 'market', 'fixed', '2', 'stop/target'))]
    RULES[('Candace Lau', m)] = [
        ('Limit in the IFVG, stop beyond the sweep, 1:2', pick('Candace Lau', m, 1, 'limit lim', 'col wk', '2', 'stop/target')),
        ('Limit in the IFVG, stop beyond the sweep, opposing liquidity', pick('Candace Lau', m, 1, 'limit lim', 'col wk', 'col tp', 'stop/target')),
        ('London only (02-05), limit, sweep stop, 1:2', pick('Candace Lau', m, 1, 'limit lim', 'col wk', '2', 'stop/target', 'London')),
        ('Max fixed 1:2', pick('Candace Lau', m, 1, 'market', 'fixed', '2', 'stop/target'))]
    RULES[('Dhesi', m)] = [
        ('Structure stop, half at first target (1:1.5), runner to the opposing level', pick('Dhesi', m, 1, 'market', 'col wk', 'col tp', 'half 1.5')),
        ('Structure stop, 1:2', pick('Dhesi', m, 1, 'market', 'col wk', '2', 'stop/target')),
        ('Max fixed 1:2', pick('Dhesi', m, 1, 'market', 'fixed', '2', 'stop/target'))]
    for tf in (1, 5):
        RULES[('Fabio Valentini', m, tf)] = [
            ('TREND: stop beyond the aggression candle, 1:2.5 (his minimum)', pick('Fabio Valentini', m, tf, 'market', 'col wk', '2.5', 'stop/target', 'TREND NY')),
            ('TREND: stop beyond aggression, 1:5 ("common")', pick('Fabio Valentini', m, tf, 'market', 'col wk', '5', 'stop/target', 'TREND NY')),
            ('TREND: half at 1:2, runner to previous day high / low', pick('Fabio Valentini', m, tf, 'market', 'col wk', 'col tp', 'half 2', 'TREND NY')),
            ('MEAN REV London: target = previous POC', pick('Fabio Valentini', m, tf, 'market', 'col wk', 'col tp', 'stop/target', 'MEAN REV London')),
            ('MEAN REV NY: target = previous POC', pick('Fabio Valentini', m, tf, 'market', 'col wk', 'col tp', 'stop/target', 'MEAN REV NY')),
            ('Max fixed 1:2', pick('Fabio Valentini', m, tf, 'market', 'fixed', '2', 'stop/target'))]
for tf in (1, 3, 5):
    RULES[('Okala', 'NQ', tf)] = [
        ('10 pt stop, scale half at +15, break-even, runner', pick('Okala', 'NQ', tf, 'market', 'pts 10.0', 'none', 'half 1.5')),
        ('10 pt stop, all out at +15', pick('Okala', 'NQ', tf, 'market', 'pts 10.0', '1.5', 'stop/target')),
        ('Fork long only, 10 pt stop, half at +15', pick('Okala', 'NQ', tf, 'market', 'pts 10.0', 'none', 'half 1.5', 'Fork long')),
        ('H short, limit at the 80 level, 10 pt stop, half at +15', pick('Okala', 'NQ', tf, 'limit lim', 'pts 10.0', 'none', 'half 1.5', 'H short')),
        ('Max fixed 1:2', pick('Okala', 'NQ', tf, 'market', 'fixed', '2', 'stop/target'))]
for m in ('NQ', 'ES', 'GC'):
    for tf in (5, 15, 60):
        RULES[('Marci Silfrain', m, tf)] = [
            ('Measured-move target, stop past the trendline (all structures)', pick('Marci Silfrain', m, tf, 'market', 'col wk', 'col tp', 'stop/target')),
            ('1st and 2nd structure only (her best)', pick('Marci Silfrain', m, tf, 'market', 'col wk', 'col tp', 'stop/target', ['structure 1', 'structure 2'])),
            ('Max fixed 1:2', pick('Marci Silfrain', m, tf, 'market', 'fixed', '2', 'stop/target'))]
for key, lst in RULES.items():
    strat, m = key[0], key[1]; tf = key[2] if len(key) > 2 else 1
    for lab, z in lst: add(lab, z, strat, m, tf)
S['rules'] = H

# ---- money: one trade at a time, $ risk, daily loss rule, annual return at the trader's own risk %
RISK = {'JJ Simon': (500, 3, None), 'Candace Lau': (200, 3, None), 'Dhesi': (500, 2, None), 'Okala': (200, 3, None), 'Fabio Valentini': (500, 4, 0.5), 'Marci Silfrain': (200, None, 1.0)}
M = []
for key, lst in RULES.items():
    strat, m = key[0], key[1]; tf = key[2] if len(key) > 2 else 1
    risk, ml, pct = RISK[strat]
    for lab, z in (lst[:3] + [lst[3]] if strat == 'Fabio Valentini' else lst[:2]):
        if not len(z): continue
        for p in ('P1', 'P2'):
            x = z[z.per == p][['te', 'tx', 'r']].dropna()
            if len(x) < 5: continue
            A = MO.account(x, risk_usd=risk, max_losses=ml)
            mm = MO.monthly(A); pr = MO.prop(A)
            yrs = max((pd.to_datetime(A.te).max() - pd.to_datetime(A.te).min()).days / 365.25, 1 / 12)
            Ryr = A.r.sum() / yrs
            ann = (np.prod(1 + A.r.values * (pct or 0.5) / 100) ** (1 / yrs) - 1) * 100
            M.append([strat, lab, m, tf, p, len(A), r(len(A) / max(mm['months'], 1), 1), r((A.r > 0).mean()), r(A.r.mean()), r(mm['per_month'], 0), r(mm['best'], 0), r(mm['worst'], 0), r(mm['green']), len(pr), r(pr.count('pass') / max(len(pr), 1), 2), r(Ryr, 1), r(ann, 1), risk, pct or 0.5])
S['money'] = M
json.dump(S, open('site7/summary.json', 'w'), separators=(',', ':'))
print(len(json.dumps(S)) // 1024, 'KB')
pd.set_option('display.width', 260); pd.set_option('display.max_rows', 300)
print(pd.DataFrame(H, columns=['strat', 'rule', 'm', 'tf', 'n1', 'wr1', 'r1', 'pf1', 't1', 'rd1', 'n2', 'wr2', 'r2', 'pf2', 't2', 'rd2']).to_string())
print(pd.DataFrame(M, columns=['strat', 'rule', 'm', 'tf', 'per', 'n', 'pm', 'wr', 'avg', 'usd_m', 'best', 'worst', 'green', 'evals', 'pass', 'R_yr', 'ann%', 'risk', 'pct']).to_string())
