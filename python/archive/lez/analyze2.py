import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from sim import cfg_names
from analyze import GROUPS, stats
CN=cfg_names()
SUB=[i for i,c in enumerate(CN) if (c[1]=='+box exit' and c[2] in ('TP2','TP3','TP5','RUN') and c[3] in ('','BE1','trailBC','trailOpp'))
     or c in (('S50','','TP2',''),('S20','','TP2',''),('S30','','TP2',''),('Sbox','','TP2',''),('S50','','TP3',''),('Sbox','','TP3',''))]
TR=pickle.load(open('trend.pkl','rb'))
RTN={1:'M1 A · touch candle = BC',2:'M1 B · touch, then BC',3:'M1 C · close inside, then BC'}
TYN={1:'M1 type1 · immediate',2:'M1 type2 · after NBC',3:'M1 type3 · after opp BC'}
MN={2:'M2 · no pullback, 2nd BC',3:'M3 · limit at box edge',4:'M4 · break candle',5:'M5 · GMC gap limit'}
def sess(t):
    m=t.dt.hour*60+t.dt.minute
    return np.select([(m>=1080)|(m<120),m<480,m<570,m<720,m<960],['Asia 18-02','London 02-08','Pre-open 08-09:30','NY AM 09:30-12','NY PM 12-16'],'Close 16-18')
def explode(E,per):
    E=E.copy(); E['row']=np.arange(len(E))
    E['sess']=sess(E.t)
    for tf,nm in (('1h','H1'),('15m','M15')):
        ct,sd=TR[(per,tf)]; k=np.searchsorted(ct,E.t.values,'right')-1
        s=np.where(k>=0,sd[np.clip(k,0,None)],0)
        E[nm]=np.where(s==0,'none',np.where(s==E.d.values,'with','against'))
    lv_un=E.lvl.unique(); gmap={l:[l]+[g for g,f in GROUPS.items() if f(l)] for l in lv_un}
    E['L']=E.lvl.map(gmap)
    def var(r):
        if r.model==1: return ['M1 all',RTN[r.rt],TYN[r.ty]]
        return [MN[r.model]]
    E['V']=[ (['M1 all',RTN[a],TYN[b]] if m==1 else [MN[m]]) for m,a,b in zip(E.model.values,E.rt.values,E.ty.values)]
    E['Hd']=[['any','held'] if x==0 else ['any'] for x in E.lv.values]
    E['F']=[['all','sess: '+s,'H1 trend: '+h,'M15 trend: '+m] for s,h,m in zip(E.sess.values,E.H1.values,E.M15.values)]
    X=E[['row','e','d','L','V','Hd','F']]
    for c in ('L','V','Hd','F'): X=X.explode(c)
    X=X.drop_duplicates(['L','V','Hd','F','e','d'])
    return X
if __name__=='__main__':
    t0=time.time(); res={}
    for tf in ('1m','5m'):
        G={}
        for per in ('old','fresh'):
            E,R=pickle.load(open(f'res_{per}_{tf}.pkl','rb')); E=E.reset_index(drop=True)
            X=explode(E,per); print(tf,per,len(X),round(time.time()-t0),flush=True)
            for c in ('L','V','Hd','F'): X[c]=X[c].astype('category')
            X['g']=X.groupby(['L','V','Hd','F'],observed=True,sort=False).ngroup()
            names=X.drop_duplicates('g').set_index('g')[['L','V','Hd','F']]
            nmap={g:'|'.join(map(str,r)) for g,r in zip(names.index,names.values)}
            X=X.sort_values(['g','e'])
            gk=X.g.values; rows=X.row.values.astype(np.int64)
            b=np.r_[0,np.flatnonzero(gk[1:]!=gk[:-1])+1,len(gk)]
            keys=None
            del X
            Rs=R[:,SUB]
            for q in range(len(b)-1):
                u,v=b[q],b[q+1]
                if v-u<15: continue
                G.setdefault(nmap[gk[u]],{})[per]=rows[u:v]
            res[(tf,per)]=Rs
        K=[];M={f'{p}_{x}':[] for p in 'ofb' for x in ('n','wr','avg','pf','t','net','dd')}
        for k,dd in G.items():
            if 'old' not in dd or 'fresh' not in dd or len(dd['old'])<60: continue
            so=stats(res[(tf,'old')][dd['old']],np.arange(len(dd['old'])))
            sf=stats(res[(tf,'fresh')][dd['fresh']],np.arange(len(dd['fresh'])))
            Rb=np.vstack([res[(tf,'old')][dd['old']],res[(tf,'fresh')][dd['fresh']]]); sb=stats(Rb,np.arange(len(Rb)))
            K.append(k)
            for p,s_ in (('o',so),('f',sf),('b',sb)):
                for x in ('n','wr','avg','pf','t','net','dd'): M[f'{p}_{x}'].append(np.asarray(s_[x],np.float32))
        ng=len(K); nc=len(SUB)
        kk=np.array([k.split('|') for k in K]) if ng else np.zeros((0,4))
        D=pd.DataFrame({'ltf':tf,'level':np.repeat(kk[:,0],nc),'entry':np.repeat(kk[:,1],nc),'held':np.repeat(kk[:,2],nc),'filter':np.repeat(kk[:,3],nc),
                        'cfg':np.tile(np.array(SUB),ng)})
        cn=np.array(CN,dtype=object)[np.tile(np.array(SUB),ng)]
        for i,c in enumerate(('stop','boxexit','target','trail')): D[c]=[x[i] for x in cn]
        for c,v in M.items(): D[c]=np.concatenate(v) if ng else []
        for c in ('level','entry','held','filter','stop','boxexit','target','trail'): D[c]=D[c].astype('category')
        D.to_parquet(f'table2_{tf}.parquet'); out=D
        pickle.dump(G,open(f'G_{tf}.pkl','wb'))
        print(tf,'rows',len(out),round(time.time()-t0),flush=True); del out,D,G
