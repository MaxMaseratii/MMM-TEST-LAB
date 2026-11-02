import pandas as pd, numpy as np, pickle, grade1
RULES={'C.M4':(1,1,5,2,1),'XCS.M1':(6,1,2,0,1),'X.M3':(1,0,2,0,1),'X.M4':(1,1,2,2,1)}
R={}
for s,(e,st,t,x,side) in RULES.items():
    out=[]
    for m in ('NQ','MNQ'):
        S=pd.read_parquet(f'sig_edge_{m}.parquet'); S=S[(S.strat==s)&(S.side==side)]
        tf=S.tf.iloc[0]
        T=grade1.trades(m,tf,S,e,st,t,x); out.append(T)
        r=T.R; print(s,m,len(r),round(r.mean(),3),round(r.mean()/r.std()*np.sqrt(len(r)),2),round((r>0).mean(),3))
    R[s]=pd.concat(out)
pickle.dump(R,open('new_trades.pkl','wb'))
