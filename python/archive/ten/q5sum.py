import pickle,pandas as pd,json
from common import pct,med
O=pickle.load(open('q56.pkl','rb'))
S={}
for tf in ('5m','15m','1h','4h'):
  for key in ('old','fresh'):
    R=O[key]['q5'][tf].copy()
    for c in ('gap_hit','gap_first','tgt_first','tgt_after_gap','same_dir'): R[c]=R[c].fillna(False).astype(bool)
    def s(X):
        g=X[X.has]; ng=X[~X.has]; gf=g[g.gap_first]
        return dict(n=len(X),has=pct(len(g),len(X)),tgt_with=pct(g.tgt_hit.sum(),len(g)),tgt_without=pct(ng.tgt_hit.sum(),len(ng)),
            gap_touch=pct(g.gap_hit.sum(),len(g)),gap_first=pct(len(gf),len(g)),tgt_after_gap=pct(gf.tgt_after_gap.sum(),len(gf)),
            dist=med(list(g.gdist)),n_gap=len(g),n_gf=len(gf))
    for nm,X in (('ALL',R),('BC+/C2',R[R.fam.isin(['BC+','C2'])]),('other',R[~R.fam.isin(['BC+','C2'])])):
        S[(tf,key,nm)]=s(X)
    g=R[R.has]
    S[(tf,key,'gap with lean')]=s(R[~R.has | R.same_dir]) ; S[(tf,key,'gap against lean')]=s(R[~R.has | ~R.same_dir])
df=pd.DataFrame(S).T; pd.set_option('display.width',250); print(df.to_string())
json.dump({'|'.join(k):v for k,v in S.items()},open('q5sum.json','w'))
