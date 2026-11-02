import numpy as np, pandas as pd, pickle
from sim2 import cfg_names2
from analyze import GROUPS
CN=cfg_names2(); C50=CN.index(('S50','','TP2','')); CBX=CN.index(('Sbox','+box exit','TP2',''))
FIRST={1:'2nd BC',2:'NBC',3:'opposite BC'}
NXT={0:'touch candle IS the BC out',1:'BC out (next candle)',2:'NBC',3:'opposite BC',4:'BC that stays inside'}
POST={4:'touch candle = BC',0:'touch → BC',2:'touch → NBC → BC',1:'touch → opp BC → BC',3:'touch → NBC + opp → BC'}
OUT={1:'entry (BC out)',2:'box broke',3:'nothing in time'}
rows=[]; wr=[]
for tf in ('1m','5m','15m'):
    for per in ('old','fresh'):
        E,Rm,R3,NT,PT,X=pickle.load(open(f'res4_{per}_{tf}.pkl','rb'))
        gm={l:['ALL levels']+[g for g,f in GROUPS.items() if f(l)] for l in X.lvl.unique()}
        X=X[X.retested==1].copy(); X['L']=X.lvl.map(gm); X=X.explode('L')
        for c in ('first','nxt','outc','post','boxtype'): X[c]=X[c].astype(int)
        for dim,mp in (('nxt',NXT),('outc',OUT)):
            g=X[X['first'].isin([1,2,3])].groupby(['L','first',dim]).size().rename('n').reset_index()
            g['share']=g.n/g.groupby(['L','first']).n.transform('sum'); g['dim']=dim; g['val']=g[dim].map(mp); g['tf']=tf; g['per']=per
            rows.append(g[['tf','per','L','first','dim','val','n','share']])
        A=E[E.area==1].reset_index(drop=True); r50=Rm[(E.area==1).values][:,C50]; rbx=Rm[(E.area==1).values][:,CBX]
        A=A.assign(r50=r50,rbx=rbx); gm2={l:['ALL levels']+[g for g,f in GROUPS.items() if f(l)] for l in A.lvl.unique()}
        A['L']=A.lvl.map(gm2); A=A.explode('L')
        for by in (['first'],['first','post'],['first','nxt'],['post'],['nxt'],['boxtype','post']):
            g=A.groupby(['L']+by).agg(n=('r50','size'),wr50=('r50',lambda r:(r>0).mean()),av50=('r50','mean'),wrbx=('rbx',lambda r:(r>0).mean()),avbx=('rbx','mean')).reset_index()
            g['by']='+'.join(by); g['tf']=tf; g['per']=per; wr.append(g)
P=pd.concat(rows); W=pd.concat(wr)
P.to_parquet('post_seq.parquet'); W.to_parquet('post_wr.parquet')
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
q=P[(P.L=='ALL levels')].pivot_table(index=['tf','dim','first','val'],columns='per',values='share').round(3)
print(q.to_string())
for by in ('first','first+post','first+nxt'):
    w=W[(W.L=='ALL levels')&(W.by==by)].pivot_table(index=['tf']+by.split('+'),columns='per',values=['n','wr50','av50','wrbx','avbx']).round(3)
    print(w.to_string())
