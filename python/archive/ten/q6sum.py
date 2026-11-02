import pickle,pandas as pd,json,numpy as np
O=pickle.load(open('q56.pkl','rb'))
S={}
for key in ('old','fresh'):
  L4=O[key]['q5']['4h'].set_index('day')
  for tf in ('1m','5m','15m'):
    R=O[key]['q6'][tf].copy()
    R['l4']=R.day.map(L4.lean).map({'bull':1,'bear':-1})
    R['f4']=R.day.map(L4.fam)
    R['with4']=R.dir==R.l4
    for mode in ('opp BC','close past BC open','close past BC low'):
      for nm,X in (('all',R[R['mode']==mode]),('with 4H lean',R[(R['mode']==mode)&R.with4]),('against 4H lean',R[(R['mode']==mode)&~R.with4]),
                   ('with 4H BC+/C2',R[(R['mode']==mode)&R.with4&R.f4.isin(['BC+','C2'])])):
        S['|'.join((tf,key,mode,nm))]=dict(n=len(X),same_med=float(X.same.median()),same_avg=round(X.same.mean(),2),nbc_avg=round(X.nbc.mean(),2),nbc_med=float(X.nbc.median()),
          mfe_med=round(X.mfe.median(),1),mfe_avg=round(X.mfe.mean(),1),mfe75=round(X.mfe.quantile(.75),1),end_avg=round(X.endpts.mean(),1),end_med=round(X.endpts.median(),1),
          end_win=round(100*(X.endpts>0).mean(),1),alive=round(100*X.alive.mean(),1),mins=float(X.mins.median()),start=float(X.start_min.median()))
df=pd.DataFrame(S).T; pd.set_option('display.width',250); pd.set_option('display.max_rows',200); print(df.to_string())
json.dump(S,open('q6sum.json','w'))
