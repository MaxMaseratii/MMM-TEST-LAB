import numpy as np, pandas as pd
from analyze import stats
def groups_from(X):
    """X: exploded frame with columns key (str/cat), row, e, d → {key: rows sorted by e}"""
    X=X.drop_duplicates(['key','e','d'])
    X['g']=X.groupby('key',observed=True,sort=False).ngroup()
    names=X.drop_duplicates('g').set_index('g')['key']
    X=X.sort_values(['g','e']); gk=X.g.values; rows=X.row.values.astype(np.int64)
    b=np.r_[0,np.flatnonzero(gk[1:]!=gk[:-1])+1,len(gk)]
    return {str(names[gk[b[q]]]):rows[b[q]:b[q+1]] for q in range(len(b)-1)}
def summarize(Go,Gf,Ro,Rf,CN,std,min_o=60,min_f=10):
    out=[]
    for k,io in Go.items():
        if k not in Gf or len(io)<min_o or len(Gf[k])<min_f: continue
        jf=Gf[k]
        so=stats(Ro[io],np.arange(len(io))); sf=stats(Rf[jf],np.arange(len(jf)))
        Rb=np.vstack([Ro[io],Rf[jf]]); sb=stats(Rb,np.arange(len(Rb)))
        both=(so['avg']>0)&(sf['avg']>0)
        cand=np.flatnonzero(both&(so['n']>=min_o))
        bi=cand[np.argmax(sb['t'][cand])] if len(cand) else int(np.argmax(sb['t']))
        rec=dict(key=k,n_o=int(so['n'].max()),n_f=int(sf['n'].max()),both=both.mean(),o_med=float(np.median(so['avg'])),f_med=float(np.median(sf['avg'])))
        def put(pfx,c):
            rec[pfx+'cfg']=' | '.join(CN[c])
            for p,s in (('o',so),('f',sf),('b',sb)):
                for x in ('n','wr','avg','pf','t','net','dd'): rec[f'{pfx}{p}_{x}']=float(s[x][c])
        put('best_',bi)
        for nm,c in std.items(): put(nm+'_',c)
        out.append(rec)
    return pd.DataFrame(out)
