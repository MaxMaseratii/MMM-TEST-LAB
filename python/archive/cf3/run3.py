"""python run3.py okala|kane|fabio_mg|fabio_trend  -> T_<name>.parquet"""
import sys, time, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/cf3'); sys.path.insert(0, '/home/claude/cf'); sys.path.insert(0, '/home/claude/mmmlab')
from mmmlab import data as D
import strat3 as S3, sim3 as G, cfstrat as CS

def halves(idx):
    sd = D.sday(idx); days = np.sort(sd.unique()); cut = days[len(days) // 2]
    return np.where(sd < cut, 'P1', 'P2')

def run(d, S, m, grids, fill=10, label=''):
    if not len(S): return None
    S = S[S.endb > S.i].reset_index(drop=True)
    out = []
    for g in grids:
        T = G.trades(d, S, m, g['entries'], g['stops'], g['targets'], g['exits'], end=S.endb.values, window=(S.w0.values, S.w1.values), fill=g.get('fill', fill))
        if len(T): out.append(T)
    return pd.concat(out, ignore_index=True) if out else None

name = sys.argv[1]; ALL = []
MAX = dict(entries=['market'], stops=['fixed'], targets=[('R', 2)], exits=[dict(name='Max fixed 1:2 (50 pts)', legs=[])])
if name == 'okala':
    EX = [dict(name='Okala: 2 of 3 off at +15, break-even, runner', legs=[('pts', 15, 2 / 3)]),
          dict(name='Okala: 1/2 at +15, 1/4 at +30, 1/4 at +60', legs=[('pts', 15, .5), ('pts', 30, .25), ('pts', 60, .25)]),
          dict(name='half at +15, break-even, runner', legs=[('pts', 15, .5)]),
          dict(name='all off at +15 (base hit)', legs=[('pts', 15, 1.0)])]
    GR = [dict(entries=['market', ('limit', 'lim')], stops=[('pts', 10.0), ('col', 'wk')], targets=[('col', 'tp'), ('col', 'tp2'), None], exits=EX, fill=3), MAX]
    for d1 in D.series('NQ', 1):
        for tfn, d, tend in (('200s', S3.bars200(d1), 720), ('1m', d1, 720), ('3m', S3.resample(d1, 3), 720), ('1m, runner to 16:00', d1, 960)):
            t0 = time.time(); S = S3.okala2(d, tend=tend)
            if tfn in ('200s', '3m'): S = S3.to_1m(d, S, d1)
            T = run(d1, S, 'NQ', [dict(g, fill=10) for g in GR], label=tfn)
            if T is None: continue
            T['tf'] = tfn; T['src'] = d1.src.iloc[0]; ALL.append(T); print('okala', tfn, d1.src.iloc[0], len(S), 'signals', len(T), 'trades', f'{time.time()-t0:.0f}s', flush=True)
if name == 'kane':
    EX = [dict(name='Kane: break-even when the next hour flips his way', legs=[], bemode=1), dict(name='no break-even', legs=[]),
          dict(name='half at 1:1, break-even, runner', legs=[('R', 1, .5)])]
    GR = [dict(entries=['market', ('limit', 'lim')], stops=[('col', 'wk'), ('pts', 25.0)], targets=[('col', 'tp'), ('R', 1), ('R', 2)], exits=EX), MAX]
    for tf in (3, 5):
        dn = D.bars('MNQ', tf); de = D.bars('MES', tf)
        J = dn.join(de[['high', 'low']].rename(columns={'high': 'high_e', 'low': 'low_e'}), how='inner'); J['per'] = halves(J.index)
        S = S3.kane2(J, True); T = run(J, S, 'NQ', GR)
        if T is not None: T['tf'] = f'{tf}m'; T['src'] = 'MNQ+MES 2026 (halves)'; ALL.append(T); print('kane SMT', tf, len(S), len(T), flush=True)
        for d in D.series('NQ', tf):
            J = d.copy(); S = S3.kane2(J, False); T = run(J, S, 'NQ', GR)
            if T is not None: T['tf'] = f'{tf}m'; T['src'] = d.src.iloc[0] + ' (no ES: SMT skipped)'; ALL.append(T); print('kane noES', tf, d.src.iloc[0], len(S), len(T), flush=True)
if name == 'fabio_mg':
    GR = [dict(entries=[('limit', 'lim'), 'market'], stops=[('col', 'wk')], targets=[('R', 1), ('R', 2)], exits=[dict(name='stop / target (no partials)', legs=[])], fill=3), MAX]
    for d1 in D.series('NQ', 1):
        for tf in (5, 3):
            t0 = time.time(); B = S3.candles_with_value(d1, tf); S = S3.to_1m(B, S3.fabio_mg(B), d1); T = run(d1, S, 'NQ', [dict(g, fill=3 * tf) for g in GR])
            if T is not None: T['tf'] = f'{tf}m'; T['src'] = d1.src.iloc[0]; ALL.append(T); print('fabio mg', tf, d1.src.iloc[0], len(S), len(T), f'{time.time()-t0:.0f}s', flush=True)
if name == 'fabio_trend':
    for d1 in D.series('NQ', 1):
        src = d1.src.iloc[0]; DL = CS.extra_levels(src, 'NQ'); S = CS.fabio(d1, 'NQ', DL); S = S[S.tag.str.startswith('TREND')]
        S = S.assign(tp2=np.nan)
        TR = S3.aggression_trail(d1)
        EX = [dict(name='no partials, full exit at stop / target', legs=[]), dict(name='no partials, trail under the last aggression candle', legs=[], flip=TR),
              dict(name='half at 1:2 + runner (old test)', legs=[('R', 2, .5)])]
        GR = [dict(entries=['market'], stops=[('col', 'wk')], targets=[('col', 'tp'), ('R', 2.5), ('R', 5), None], exits=EX), MAX]
        T = run(d1, S, 'NQ', GR)
        if T is not None: T['tf'] = '1m'; T['src'] = src; ALL.append(T); print('fabio trend', src, len(S), len(T), flush=True)
A = pd.concat(ALL, ignore_index=True)
for col in ('entry', 'stop', 'target', 'exit', 'tag', 'per', 'tf', 'src'): A[col] = A[col].astype(str)
A.to_parquet(f'/home/claude/cf3/T_{name}.parquet'); print('saved', name, len(A))
