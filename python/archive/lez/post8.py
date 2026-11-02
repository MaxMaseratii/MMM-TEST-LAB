import numpy as np, pandas as pd, pickle
from sim2 import cfg_names2
from analyze import GROUPS
CN=cfg_names2(); C50=CN.index(('S50','','TP2','')); CBX=CN.index(('Sbox','+box exit','TP2',''))
FIRST={1:'2nd BC',2:'NBC',3:'opposite BC'}
NX={0:'touch candle is the BC out',1:'BC out',2:'NBC',3:'opposite BC',4:'BC that stays inside',5:'closes through the box'}
out=[]
for tf in ('1m','5m','15m'):
    for per in ('old','fresh'):
        E,Rm,R3,NT,PT,X=pickle.load(open(f'res4_{per}_{tf}.pkl','rb'))
        X=X[(X.retested==1)&X['first'].isin([1,2,3])].copy()
        for c in ('first','nxt','outc','post'): X[c]=X[c].astype(int)
        X['nx']=np.where(X.post==4,0,np.where(X.nxt==0,5,X.nxt))
        m=(E.area==1).values; A=E[m].copy(); A['r50']=Rm[m][:,C50]; A['rbx']=Rm[m][:,CBX]
        A['nx']=np.where(A.post==4,0,A.nxt)
        A=A.set_index('ev')[['r50','rbx']]
        X=X.join(A,on='ev')
        gm={l:['ALL levels']+[g for g,f in GROUPS.items() if f(l)] for l in X.lvl.unique()}
        X['L']=X.lvl.map(gm); X=X.explode('L')
        g=X.groupby(['L','first','nx']).agg(n=('ev','size'),entry=('outc',lambda o:(o==1).mean()),broke=('outc',lambda o:(o==2).mean()),
            ne=('r50',lambda r:r.notna().sum()),wr50=('r50',lambda r:(r>0).sum()/max(r.notna().sum(),1)),av50=('r50','mean'),wrbx=('rbx',lambda r:(r>0).sum()/max(r.notna().sum(),1)),avbx=('rbx','mean')).reset_index()
        g['share']=g.n/g.groupby(['L','first']).n.transform('sum')
        t=X.groupby(['L','first']).agg(n=('ev','size'),entry=('outc',lambda o:(o==1).mean()),broke=('outc',lambda o:(o==2).mean()),ne=('r50',lambda r:r.notna().sum()),
            wr50=('r50',lambda r:(r>0).sum()/max(r.notna().sum(),1)),av50=('r50','mean'),wrbx=('rbx',lambda r:(r>0).sum()/max(r.notna().sum(),1)),avbx=('rbx','mean')).reset_index()
        t['nx']=-1; t['share']=1.0
        g=pd.concat([t,g]); g['tf']=tf; g['per']=per; out.append(g)
P=pd.concat(out); P['firstN']=P['first'].map(FIRST); P['nxN']=P.nx.map(NX).fillna('all next candles')
W=P.pivot_table(index=['tf','L','firstN','nxN','nx'],columns='per',values=['n','share','entry','broke','ne','wr50','av50','wrbx','avbx']).reset_index()
W.columns=['_'.join([c for c in col if c]) for col in W.columns]
W.to_parquet('post8.parquet')
pd.set_option('display.width',260); pd.set_option('display.max_rows',300)
for L in ('ALL levels','ALL UPG gaps'):
    q=W[W.L==L].sort_values(['tf','firstN','nx'])
    print(L); print(q[['tf','firstN','nxN','n_old','n_fresh','share_old','share_fresh','entry_old','entry_fresh','broke_old','wr50_old','wr50_fresh','av50_old','av50_fresh','wrbx_old','wrbx_fresh','avbx_old','avbx_fresh']].round(2).to_string(index=False))
