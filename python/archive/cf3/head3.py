import sys, json, numpy as np, pandas as pd
sys.path.insert(0,'/home/claude/cf3'); from sim3 import st
from ana3 import fam
L = {}
def load(nm):
    if nm not in L: L[nm] = pd.read_parquet(f'T_{nm}.parquet'); L[nm]['te'] = pd.to_datetime(L[nm].te)
    return L[nm]
def row(label, nm, q, note=''):
    T = load(nm); z = T[q(T)]
    a = z[z.per == 'P1']; b = z[z.per == 'P2']; A, B = st(a.r), st(b.r)
    yrs = [[int(y), len(g), round((g.r > 0).mean(), 2), round(g.r.mean(), 2), round(g.r_rand.mean(), 2)] for y, g in z.groupby(z.te.dt.year) if len(g) >= 3]
    r = lambda v, d=2: None if v != v else round(float(v), d)
    return dict(label=label, note=note, n1=A['n'], wr1=r(A['wr']), avg1=r(A['avg']), pf1=r(A['pf']), t1=r(A['t'], 1), rnd1=r(a.r_rand.mean()),
                n2=B['n'], wr2=r(B['wr']), avg2=r(B['avg']), pf2=r(B['pf']), t2=r(B['t'], 1), rnd2=r(b.r_rand.mean()), years=yrs)
OKE = lambda T: ((T.entry == 'limit lim') & ~T.tag.str.startswith('Fork')) | ((T.entry == 'market') & T.tag.str.startswith('Fork'))
ok = lambda tf, ex='Okala: 2 of 3 off at +15, break-even, runner', tgt='col tp', extra=None: (lambda T: (T.tf == tf) & (T.stop == 'pts 10.0') & (T.target == tgt) & (T.exit == ex) & OKE(T) & (extra(T) if extra else True))
OUT = {}
OUT['Okala'] = [
 row('His full model (200 s proxy): all setups, 10 pt stop, 2 of 3 off at +15, break-even, runner to the nearest magnet', 'okala', ok('200s')),
 row('Same, 1-minute chart', 'okala', ok('1m')),
 row('Same, 3-minute chart', 'okala', ok('3m')),
 row('200 s: level taps only (limit at the 20 / 80)', 'okala', ok('200s', extra=lambda T: T.tag.str.startswith('Level tap'))),
 row('200 s: fork setups only', 'okala', ok('200s', extra=lambda T: T.tag.str.startswith('Fork'))),
 row('200 s: H setups only (limit at the level retest)', 'okala', ok('200s', extra=lambda T: T.tag.str.startswith('H '))),
 row('200 s: cross-section entries only', 'okala', ok('200s', extra=lambda T: T.tag.str.startswith('Cross'))),
 row('200 s: "best entries" only (structure + a 20/80 level stacked)', 'okala', ok('200s', extra=lambda T: T.tag.str.startswith('H ') | T.tag.str.contains('\\| level'))),
 row('200 s: all setups, everything off at +15 (base hit, 1.5 : 1)', 'okala', ok('200s', ex='all off at +15 (base hit)', tgt='none')),
 row('200 s: 4 contracts: 1/2 at +15, 1/4 at +30, 1/4 at +60', 'okala', ok('200s', ex='Okala: 1/2 at +15, 1/4 at +30, 1/4 at +60', tgt='none')),
 row('1 m: H short only, half at +15, runner (the "worth watching" rule from the first test)', 'okala', lambda T: (T.tf == '1m') & (T.tag.str.startswith('H short')) & (T.entry == 'limit lim') & (T.stop == 'pts 10.0') & (T.target == 'none') & (T.exit == 'half at +15, break-even, runner')),
 row('1 m: H short at an 80 only, half at +15, runner to 16:00 (the exact rule from the first test)', 'okala', lambda T: (T.tf == '1m, runner to 16:00') & (T.tag == 'H short 80') & (T.entry == 'limit lim') & (T.stop == 'pts 10.0') & (T.target == 'none') & (T.exit == 'half at +15, break-even, runner')),
 row('Max fixed 1:2 (50 pt stop), market entry, 200 s, all setups', 'okala', lambda T: (T.tf == '200s') & (T.exit.str.startswith('Max'))),
]
kn = lambda grp, tf, entry='market', ex='Kane: break-even when the next hour flips his way', stop='col wk', tgt='col tp', extra=None: (lambda T: (T.src.str.contains('no ES') == (grp == 'noES')) & (T.tf == tf) & (T.entry == entry) & (T.stop == stop) & (T.target == tgt) & (T.exit == ex) & (extra(T) if extra else True))
good = lambda T: T.tag.str.contains('premium') & T.tag.str.contains('Tue-Thu')
OUT['Trader Kane'] = [
 row('His model WITH SMT (NQ + ES, 2026 only, 5m): sell stop at the inversion, stop at the divergence high, TP 50%, break-even on the hour flip', 'kane', kn('SMT', '5m'), 'P1 / P2 = first / second half of the NQ+ES overlap'),
 row('Same with SMT, 3m', 'kane', kn('SMT', '3m'), 'P1 / P2 = halves of 2026'),
 row('Without SMT (NQ only, 2022–26), 5m: H1 + H4 PO3 sweep, inversion entry, stop at the high, TP 50%, break-even on the hour flip', 'kane', kn('noES', '5m')),
 row('Without SMT, 3m', 'kane', kn('noES', '3m')),
 row('Without SMT, 5m, only his best conditions: premium / discount + Tue–Thu', 'kane', kn('noES', '5m', extra=good)),
 row('Without SMT, 5m, limit on the retap of the inversion', 'kane', kn('noES', '5m', entry='limit lim')),
 row('Without SMT, 5m, no break-even', 'kane', kn('noES', '5m', ex='no break-even')),
 row('Max fixed 1:2 (50 pt stop), without SMT, 5m', 'kane', lambda T: T.src.str.contains('no ES') & (T.tf == '5m') & T.exit.str.startswith('Max')),
]
fm = lambda tf, entry='limit lim', tgt='R 1', extra=None: (lambda T: (T.tf == tf) & (T.entry == entry) & (T.stop == 'col wk') & (T.target == tgt) & (T.exit.str.startswith('stop')) & (extra(T) if extra else True))
full = lambda T: T.tag.str.contains('with VWAP') & T.tag.str.contains('effort yes')
OUT['Fabio (machine gun)'] = [
 row('Machine gun 1:1, 5m: value moves up + green candle + buyers win (delta) -> limit at the candle POC, stop under its value area, 1:1', 'fabio_mg', fm('5m')),
 row('Same, 3m', 'fabio_mg', fm('3m')),
 row('5m, with the day only (VWAP side)', 'fabio_mg', fm('5m', extra=lambda T: T.tag.str.contains('with VWAP'))),
 row('5m, all his confirmations (with VWAP + effort)', 'fabio_mg', fm('5m', extra=full)),
 row('5m, value SWITCH candles only', 'fabio_mg', fm('5m', extra=lambda T: T.tag.str.startswith('switch'))),
 row('5m, all confirmations, "squeeze a 1:2"', 'fabio_mg', fm('5m', tgt='R 2', extra=full)),
 row('5m, all confirmations, market entry at the candle close, 1:1', 'fabio_mg', fm('5m', entry='market', extra=full)),
 row('Max fixed 1:2 (50 pts), 5m, with VWAP', 'fabio_mg', lambda T: (T.tf == '5m') & T.exit.str.startswith('Max') & T.tag.str.contains('with VWAP')),
]
ft = lambda ex, tgt: (lambda T: (T.exit == ex) & (T.target == tgt))
OUT['Fabio (NY trend model)'] = [
 row('Trend model, NO partials (his rule now), full exit at the previous day high / low', 'fabio_trend', ft('no partials, full exit at stop / target', 'col tp')),
 row('Trend model, no partials, trail under the last aggression candle', 'fabio_trend', ft('no partials, trail under the last aggression candle', 'none')),
 row('Trend model, no partials, 1:2.5', 'fabio_trend', ft('no partials, full exit at stop / target', 'R 2.5')),
 row('Trend model, no partials, 1:5 ("1 to five is common")', 'fabio_trend', ft('no partials, full exit at stop / target', 'R 5')),
 row('Old test: half at 1:2 + runner to the previous day high / low', 'fabio_trend', ft('half at 1:2 + runner (old test)', 'col tp')),
 row('Max fixed 1:2 (50 pts)', 'fabio_trend', lambda T: T.exit.str.startswith('Max')),
]
json.dump(OUT, open('head3.json', 'w'))
for k, v in OUT.items():
    print('\n####', k)
    for x in v: print(f"{x['label'][:95]:95s} | P1 n{x['n1']} WR {x['wr1']} avg {x['avg1']} PF {x['pf1']} t {x['t1']} rnd {x['rnd1']} | P2 n{x['n2']} WR {x['wr2']} avg {x['avg2']} t {x['t2']} rnd {x['rnd2']}\n      years {x['years']}")
