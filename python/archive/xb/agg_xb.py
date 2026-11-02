import pandas as pd, numpy as np, json
from core import stats
Z = pd.read_parquet('xb_zone.parquet'); Fd = pd.read_parquet('xb_fva.parquet'); Bd = pd.read_parquet('xb_brk.parquet')
TF = ['5m','15m','1h','4h']
def pr(lbl, x):
    o = stats(x[x.period=='old'].R.values); f = stats(x[x.period=='fresh'].R.values)
    print(f"{lbl:48} n {o['n']}/{f['n']} WR {o['wr']}/{f['wr']} PF {o['pf']}/{f['pf']} avg {o['avg']}/{f['avg']} t {o['t']}/{f['t']}")
    return dict(old=o, fresh=f)
out = {'zone':{}, 'fva':{}, 'desc':{}, 'gmu':{}}
nblk = Bd.groupby(['tf','period']).size()
for tf in TF:
    print('\n######', tf, 'blocks', nblk[tf].to_dict())
    print('-- A. inside the block (before the break), 1:2')
    for (zn, st), g in Z[Z.tf==tf].groupby(['zone','stop']):
        r = pr(f'{zn} [{st}]', g); r['fill_old'] = round(100*len(g[g.period=="old"])/nblk[tf]['old'],1); r['fill_fresh']=round(100*len(g[g.period=="fresh"])/nblk[tf]['fresh'],1)
        out['zone'][f'{tf}|{zn}|{st}'] = r
    print('-- B. after the break, 1:2')
    for (en, st), g in Fd[Fd.tf==tf].groupby(['entry','stop']):
        r = pr(f'{en} [{st}]', g); out['fva'][f'{tf}|{en}|{st}|all'] = r
    for (en, rel), g in Fd[(Fd.tf==tf)&(Fd.stop=='S50')].groupby(['entry','rel']):
        out['fva'][f'{tf}|{en}|S50|{rel}'] = pr(f'  {en} {rel}', g)
    # descriptive
    B = Bd[Bd.tf==tf]
    d = {}
    for per in ['old','fresh']:
        b = B[B.period==per]; n = len(b)
        t = b[b.touchAfter>=0]
        d[per] = dict(n=n, cont=round(100*(b.rel=='cont').mean(),1),
            touch=round(100*len(t)/n,1), touch5=round(100*(t.touchAfter<=5).sum()/n,1),
            tcl={k: round(100*v/len(t),1) for k,v in t.touchClose.value_counts().items()},
            broke20_by_tcl={k: round(100*g.broke20.mean(),1) for k,g in t.groupby('touchClose')},
            mfe_by_tcl={k: round(g.mfe.median(),1) for k,g in t.groupby('touchClose')},
            mae_by_tcl={k: round(g.mae.median(),1) for k,g in t.groupby('touchClose')},
            fvaH=round(b.fvaH.median(),1), brkGMU=round(100*b.brkGMU.mean(),1),
            opp={k: round(100*v/n,1) for k,v in b.oppGMU.value_counts().items()})
    out['desc'][tf] = d
    print(json.dumps(d))
    print('-- GMU relation (S50, 1:2)')
    for key in ['brkGMU','oppGMU','touchClose']:
        for (en, v), g in Fd[(Fd.tf==tf)&(Fd.stop=='S50')&(Fd.entry.isin(['E0 market at break close','E1 limit FVA near edge','E4 touch then BC (close)']))].groupby(['entry', key]):
            out['gmu'][f'{tf}|{en}|{key}={v}'] = pr(f'  {en[:22]} {key}={v}', g)
json.dump(out, open('xb_agg.json','w'), default=str)
