import pandas as pd, numpy as np, json
from core import stats
df = pd.read_parquet('gmu_trades.parquet')
MIR = {'XD':'XP','D':'P','MD':'MP','BAL':'BAL','MP':'MD','P':'D','XP':'XD'}
# depth name: bull level name; bear mirrored -> 'XD' always = deepest pullback
df['depth'] = np.where(df.side == 1, df.lvl, df.lvl.map(MIR).fillna(df.lvl))
DEP = ['XD','D','MD','BAL','MP','P','XP']
def s(x, rr=2.0):
    y = x[x.rr == rr]; st = stats(y.R[y.filled == 1].values); st['fill'] = round(100 * y.filled.mean(), 1) if len(y) else None
    y1 = x[(x.rr == 1.0) & (x.filled == 1)]; st['react'] = round(100 * (y1.R > 0).mean(), 1) if len(y1) else None
    return st
res = {}
for tf in ['5m','15m','1h','4h']:
    T = df[df.tf == tf]
    rows = []
    for ap in ['C3','GMU3','C1']:
        for dp in DEP:
            r = dict(app=ap, depth=dp)
            for stp in ['S50','ATR']:
                for per in ['old','fresh']:
                    x = T[(T.app==ap)&(T.depth==dp)&(T.stop==stp)&(T.period==per)]
                    r[f'{stp}_{per}'] = s(x)
            rows.append(r)
    r = dict(app='RANDOM', depth='-')
    for per in ['old','fresh']:
        r[f'S50_{per}'] = s(T[(T.app=='RANDOM')&(T.period==per)])
    rows.append(r)
    res[tf] = rows
# by c3 shape (family x lean), each approach at each depth, S50 1:2
shape = []
for tf in ['5m','15m','1h','4h']:
    T = df[(df.tf == tf) & (df.stop == 'S50') & (df.app != 'RANDOM')]
    for (ap, dp, fam, ln), g in T.groupby(['app','depth','fam','lean']):
        o = s(g[g.period=='old']); f = s(g[g.period=='fresh'])
        shape.append(dict(tf=tf, app=ap, depth=dp, fam=fam, lean=ln, old=o, fresh=f))
json.dump(dict(main=res, shape=shape), open('gmu_agg2.json','w'), default=str)
for tf, rows in res.items():
    print('==', tf)
    for r in rows:
        o, f = r['S50_old'], r['S50_fresh']
        a = r.get('ATR_old'); b = r.get('ATR_fresh')
        print(f"{r['app']:6} {r['depth']:4} fill {o['fill']}/{f['fill']} react {o['react']}/{f['react']} WR {o['wr']}/{f['wr']} avg {o['avg']}/{f['avg']} t {o['t']}/{f['t']}" + (f"  | ATR avg {a['avg']}/{b['avg']} t {a['t']}/{b['t']}" if a else ''))
print('\n== shapes passing: t>=2 old and avg>0.05 fresh and n fresh>=40')
for x in shape:
    o, f = x['old'], x['fresh']
    if o['t'] and o['t'] >= 2 and f['avg'] is not None and f['avg'] > 0.05 and f['n'] >= 40:
        print(x['tf'], x['app'], x['depth'], x['fam'], x['lean'], 'n', o['n'], f['n'], 'avg', o['avg'], f['avg'], 't', o['t'], f['t'], 'WR', o['wr'], f['wr'])
