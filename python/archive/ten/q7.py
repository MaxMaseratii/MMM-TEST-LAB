"""Fixed 50 pt stop, 1:2 (100 pt target), entry at the close of the first 5m/15m BC at or after 10:00, out at 11:30. Cost 1 pt."""
import numpy as np, pandas as pd, pickle, json
from common import raw, bars, good_days, lean, family
O=pickle.load(open('q56.pkl','rb'))
res={}
for key in ('old','fresh'):
    m1=raw()[key]; L4=O[key]['q5']['4h'].set_index('day')
    for tf,mins in (('5m',5),('15m',15)):
        R=O[key]['q6'][tf]; R=R[R['mode']=='opp BC']
        b=bars(key,tf); rows=[]
        for _,r in R.iterrows():
            day=pd.Timestamp(r.day); a=day+pd.Timedelta(hours=10)
            et=a+pd.Timedelta(minutes=int(r.start_min)+mins)  # entry after the BC closes
            st=b.loc[a+pd.Timedelta(minutes=int(r.start_min))]
            e=st.close; d=r.dir
            path=m1.loc[et:day+pd.Timedelta(hours=11,minutes=29)]
            if not len(path): continue
            sl=e-50*d; tp=e+100*d; out=None
            for h,l,c in zip(path.high.values,path.low.values,path.close.values):
                hs=(l<=sl) if d==1 else (h>=sl); ht=(h>=tp) if d==1 else (l<=tp)
                if hs: out=-50; break
                if ht: out=100; break
            if out is None: out=(path.close.values[-1]-e)*d
            l4=L4.lean.get(r.day); f4=L4.fam.get(r.day)
            rows.append(dict(R=(out-1)/50, with4=(l4=='bull')==(d==1), f4=f4, typ=st.type))
        X=pd.DataFrame(rows)
        for nm,Y in (('all',X),('with 4H lean',X[X.with4]),('against 4H lean',X[~X.with4]),('first BC is BC+',X[X.typ.str.contains(r'BC\+')]),('with 4H BC+/C2',X[X.with4&X.f4.isin(['BC+','C2'])])):
            r_=Y.R.values; n=len(r_)
            if n<5: continue
            w=r_[r_>0].sum(); l=-r_[r_<0].sum()
            res[f'{tf}|{key}|{nm}']=dict(n=n,WR=round(100*(r_>0).mean(),1),avgRR=round(r_.mean(),3),PF=round(w/l,2) if l else None,t=round(r_.mean()/r_.std(ddof=1)*np.sqrt(n),2))
df=pd.DataFrame(res).T; print(df.to_string()); json.dump(res,open('q7.json','w'))
