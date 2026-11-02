import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from sim2 import cfg_names2
from sim3 import cfg3
from analyze import GROUPS
from summ import groups_from, summarize
CN=cfg_names2(); CN3=cfg3()
STD={'max':CN.index(('Sbox','+box exit','RUN','BE2')),'tp2':CN.index(('Sbox','+box exit','TP2','')),'fix50':CN.index(('S50','','TP2','')),'tp3o':CN.index(('Sbox','+box exit','TP3','trailOpp'))}
STD3={'mg1':CN3.index(('Sbox','RUN','BE+fees after 1 BC','no re-entry')),'mg2':CN3.index(('Sbox','RUN','BE+fees after 2 BC','no re-entry')),'mg1r':CN3.index(('Sbox','RUN','BE+fees after 1 BC','3 re-entries'))}
PRE={0:'P0 break → touch (nothing between)',4:'P1 break → 2nd BC → touch',2:'P2 break → NBC → touch',1:'P3 break → opp BC → touch',
     6:'P4 break → 2nd BC + NBC → touch',5:'P5 break → 2nd BC + opp BC → touch',3:'P6 break → NBC + opp BC → touch',7:'P7 break → 2nd BC + NBC + opp → touch'}
TCH={0:'wick touch only',1:'closed inside'}
BOX={1:'BC on BC (no NBC)',2:'box with NBC'}
AREA={1:'A1 next open',2:'A2 limit 50% of entry BC',3:'A3 limit at entry BC open',4:'A4 limit at high/low the BC broke',5:'A5 limit at box edge',6:'A6 GMC gap limit'}
def gmap(lv): return {l:['ALL levels',l]+[g for g,f in GROUPS.items() if f(l)] for l in lv}
def explode(E):
    E=E.reset_index(drop=True).copy(); E['row']=np.arange(len(E)); gm=gmap(E.lvl.unique())
    X=pd.DataFrame({'row':E.row,'e':E.e,'d':E.d})
    X['L']=E.lvl.map(gm).values
    X['P']=[['all',PRE[p]] for p in E.pre.values]
    X['T']=[['all',TCH[t]] for t in E.touch.values]
    X['B']=[['all',BOX[b]] for b in E.boxtype.values]
    X['H']=[['any','held'] if x==0 else ['any'] for x in E.lv.values]
    X['A']=E.area.map(AREA).values
    for c in ('L','P','T','B','H'): X=X.explode(c)
    X['key']=(X['L']+'|'+X['P']+'|'+X['T']+'|'+X['B']+'|'+X['A']+'|'+X['H']).astype('category')
    return X[['key','row','e','d']]
if __name__=='__main__':
    t0=time.time(); out=[]; out3=[]; rt=[]
    for tf in ('1m','5m','15m'):
        G={};RR={};G3={};R3={}
        for per in ('old','fresh'):
            E,Rm,R,NT,PT,Xb=pickle.load(open(f'res4_{per}_{tf}.pkl','rb'))
            X=explode(E); G[per]=groups_from(X); RR[per]=Rm
            a1=E.area.values==1
            G3[per]=G[per]; R3[per]=R
            # retest probability
            Xb=Xb.copy(); Xb['entry']=Xb.ev.isin(E.ev[a1]).astype(int); gm=gmap(Xb.lvl.unique())
            Xb['L']=Xb.lvl.map(gm); Xb=Xb.explode('L')
            Xb['first2']=Xb['first'].astype(int).astype(str)+Xb['second'].astype(int).astype(str)
            for dim in ('all','first','first2','boxtype'):
                g=Xb.groupby(['L']+([] if dim=='all' else [dim]))
                s=g.agg(n=('retested','size'),retest=('retested','mean'),entry=('entry','mean'),bars=('bars',lambda b:np.median(b[b>=0]) if (b>=0).any() else np.nan)).reset_index()
                s['dim']=dim; s['val']=s[dim].astype(str) if dim!='all' else 'all'; s['per']=per; s['ltf']=tf
                rt.append(s[['ltf','per','L','dim','val','n','retest','entry','bars']])
            del X
            print(tf,per,len(G[per]),round(time.time()-t0),flush=True)
        S=summarize(G['old'],G['fresh'],RR['old'],RR['fresh'],CN,STD,min_o=60,min_f=10); S['ltf']=tf; out.append(S)
        k1={k:v for k,v in G['old'].items() if 'A1 next open' in k}; k1f={k:v for k,v in G['fresh'].items() if 'A1 next open' in k}
        S3=summarize(k1,k1f,R3['old'],R3['fresh'],CN3,STD3,min_o=60,min_f=10); S3['ltf']=tf; out3.append(S3)
        pickle.dump(G,open(f'G7_{tf}.pkl','wb'))
        print(tf,'groups',len(S),len(S3),round(time.time()-t0),flush=True)
    for nm,L in (('table7',out),('table7m',out3)):
        S=pd.concat(L,ignore_index=True); k=S.key.str.split('|',expand=True); k.columns=['level','pre','touch','box','area','held']
        pd.concat([S,k],axis=1).to_parquet(nm+'.parquet')
    pd.concat(rt,ignore_index=True).to_parquet('retest7.parquet'); print('done',round(time.time()-t0))
