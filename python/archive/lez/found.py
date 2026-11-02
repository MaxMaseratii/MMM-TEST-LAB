import numpy as np,pandas as pd,pickle,sys
sys.path.insert(0,'/home/claude/lez')
from run import ltf_arrays
from sim import bc_arrays
from analyze import GROUPS
R0=pickle.load(open('raw.pkl','rb')); rows=[]
for per in ('old','fresh'):
    for tf in ('1m','5m'):
        E,_=pickle.load(open(f'res_{per}_{tf}.pkl','rb'))
        d=ltf_arrays(R0[per],tf); O,H,L,C=[d[k].values for k in ('open','high','low','close')]
        bu,be,nn=bc_arrays(H,L,C); n=len(C)
        B=E[E.model==4].drop_duplicates(['boxj','d','lvl'])
        for _,x in B.iterrows():
            j=int(x.boxj); dd=int(x.d); a=b=0; nbcHit=False; mfe=0.0; pts_opp=np.nan
            for k in range(j+1,min(n,j+500)):
                dirb=bu[k] if dd==1 else be[k]; opp=be[k] if dd==1 else bu[k]
                mfe=max(mfe,(H[k]-C[j]) if dd==1 else (C[j]-L[k]))
                if opp: pts_opp=(C[k]-C[j])*dd; break
                if dirb:
                    a+=1
                    if not nbcHit: b+=1
                if nn[k]: nbcHit=True
            rows.append((per,tf,x.lvl,dd,a,b,mfe,pts_opp))
F=pd.DataFrame(rows,columns=['per','ltf','lvl','d','bc_before_opp','bc_before_nbc','mfe_pts','pts_at_opp'])
out=[]
for nm,f in [('ALL levels',lambda s:True)]+list(GROUPS.items()):
    g=F[F.lvl.map(f)]
    for (per,tf),h in g.groupby(['per','ltf']):
        out.append((nm,tf,per,len(h),h.bc_before_opp.mean(),h.bc_before_nbc.mean(),(h.bc_before_opp==0).mean(),h.mfe_pts.mean(),h.mfe_pts.median(),h.pts_at_opp.mean()))
O=pd.DataFrame(out,columns=['group','ltf','period','breaks','avg BCs before opp BC','avg BCs before 1st NBC','% opp BC next (0 BCs)','avg pts max move before opp BC','median pts','avg pts at the opp BC close'])
O.to_parquet('found.parquet'); print(O.round(2).to_string())
