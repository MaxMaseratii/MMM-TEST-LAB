import pandas as pd, numpy as np, json
from core import stats
df = pd.read_parquet('gmu_trades.parquet')
LV = ['XD','D','MD','BAL','MP','P','XP']
def s(x):
    st = stats(x.R[x.filled == 1].values); st['fill'] = round(100 * x.filled.mean(), 1); return st
out = {}
base = df[(df.stop == 'S50')]
# 1) by approach x level, both sides, 1:2
for tf in ['5m','15m','1h','4h']:
    rows = []
    for ap in ['C3','GMU3','C1']:
        for lv in LV:
            r = {'app': ap, 'lvl': lv}
            for per in ['old','fresh']:
                x = base[(base.tf==tf)&(base.period==per)&(base.app==ap)&(base.lvl==lv)&(base.rr==2.0)]
                r[per] = s(x)
                x1 = base[(base.tf==tf)&(base.period==per)&(base.app==ap)&(base.lvl==lv)&(base.rr==1.0)&(base.filled==1)]
                r[per]['react'] = round(100*(x1.R>0).mean(),1) if len(x1) else None
            rows.append(r)
    for per in ['old','fresh']:
        x = base[(base.tf==tf)&(base.period==per)&(base.app=='RANDOM')&(base.rr==2.0)]
        x1 = base[(base.tf==tf)&(base.period==per)&(base.app=='RANDOM')&(base.rr==1.0)]
        st = s(x); st['react'] = round(100*(x1.R>0).mean(),1)
        rows.append({'app':'RANDOM','lvl':'-', per: st} if per=='old' else None) if False else None
    rnd = {}
    for per in ['old','fresh']:
        x = base[(base.tf==tf)&(base.period==per)&(base.app=='RANDOM')&(base.rr==2.0)]
        x1 = base[(base.tf==tf)&(base.period==per)&(base.app=='RANDOM')&(base.rr==1.0)]
        st = s(x); st['react'] = round(100*(x1.R>0).mean(),1); rnd[per] = st
    rows.append({'app':'RANDOM','lvl':'-', **rnd})
    out[tf] = rows
json.dump(out, open('gmu_agg.json','w'), default=str)
for tf, rows in out.items():
    print('==', tf)
    for r in rows:
        o, f = r['old'], r['fresh']
        print(f"{r['app']:6} {r['lvl']:4} fill {o['fill']}/{f['fill']}  n {o['n']}/{f['n']}  react {o['react']}/{f['react']}  WR {o['wr']}/{f['wr']}  avg {o['avg']}/{f['avg']}  t {o['t']}/{f['t']}")
