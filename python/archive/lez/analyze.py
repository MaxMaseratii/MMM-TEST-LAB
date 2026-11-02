import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim import cfg_names, STOPS
CN=cfg_names(); NC=len(CN)
MV={'M1 all':('model',1,None),'M1 A · touch candle = BC':('model',1,('rt',1)),'M1 B · touch, then BC':('model',1,('rt',2)),
    'M1 C · close inside, then BC':('model',1,('rt',3)),'M1 type1 · immediate':('model',1,('ty',1)),'M1 type2 · after NBC':('model',1,('ty',2)),
    'M1 type3 · after opp BC':('model',1,('ty',3)),'M2 · no pullback, 2nd BC':('model',2,None),'M3 · limit at box edge':('model',3,None),
    'M4 · break candle':('model',4,None),'M5 · GMC gap limit':('model',5,None)}
GROUPS={'ALL PRO f boxes M15':lambda s:s.startswith('M15 ') and 'UPG' not in s,
        'ALL PRO f boxes H1':lambda s:s.startswith('H1 ') and 'UPG' not in s,
        'ALL PRO f boxes H4':lambda s:s.startswith('H4 ') and 'UPG' not in s and s not in('H4 high','H4 low','H4 open'),
        'ALL LEZ (any TF)':lambda s:'LEZ' in s,
        'ALL break boxes CDL/CDS/LD/SD':lambda s:s.split(' ')[-1] in ('CDL','CDS','LD','SD'),
        'ALL PO4 T# (any TF)':lambda s:s.split(' ')[-1] in ('T1','Tn'),
        'ALL UPG gaps':lambda s:'UPG' in s,
        'ALL session / range H-L':lambda s:any(s.startswith(x) for x in ('Asia','London','Pre-open','Globex','NY AM','NY PM')),
        'ALL opens':lambda s:'open' in s and 'gap' not in s,
        'ALL day / week / H4 H-L':lambda s:s in ('PDH','PDL','PWH','PWL','H4 high','H4 low','PD close'),
        'ALL opening gaps':lambda s:'opening gap' in s}
def load():
    out={}
    for per in ('old','fresh'):
        for tf in ('1m','5m'):
            E,R=pickle.load(open(f'res_{per}_{tf}.pkl','rb'))
            out[(per,tf)]=(E.reset_index(drop=True),R)
    return out
def dist_of(E):
    D=np.zeros((len(E),4),np.float32)
    for k,s in enumerate(STOPS):
        if s>0: D[:,k]=s
        else: D[:,k]=np.clip(np.abs(E.px.values-E.edge.values)+0.25,20,50)
    return D
def stats(R,tord):
    """R: n x NC (time ordered rows). returns dict of arrays per config"""
    n=np.sum(~np.isnan(R),0); Rz=np.nan_to_num(R)
    mu=Rz.sum(0)/np.maximum(n,1); sd=np.sqrt(np.maximum((Rz**2).sum(0)/np.maximum(n,1)-mu**2,0)*n/np.maximum(n-1,1))
    t=np.where(sd>0,mu/sd*np.sqrt(n),0); wr=(Rz>0).sum(0)/np.maximum(n,1)
    gp=np.where(Rz>0,Rz,0).sum(0); gl=-np.where(Rz<0,Rz,0).sum(0); pf=np.where(gl>0,gp/np.maximum(gl,1e-9),np.inf)
    cs=np.cumsum(Rz[tord],0); dd=(np.maximum.accumulate(np.vstack([np.zeros((1,R.shape[1])),cs]),0)[1:]-cs).max(0) if len(R) else np.zeros(R.shape[1])
    return dict(n=n,avg=mu,t=t,wr=wr,pf=pf,net=Rz.sum(0),dd=dd)
def maxcons(r):
    w=l=bw=bl=0
    for x in r:
        if x>0: w+=1;l=0
        else: l+=1;w=0
        bw=max(bw,w);bl=max(bl,l)
    return bw,bl
if __name__=='__main__':
    D=load(); rows=[]
    lvls=sorted(set(D[('old','1m')][0].lvl)|set(D[('old','5m')][0].lvl))
    keep={}
    for tf in ('1m','5m'):
        for held in ('held','any'):
            for name in lvls+list(GROUPS):
                for mv,(col,val,flt) in MV.items():
                    res={}
                    for per in ('old','fresh'):
                        E,R=D[(per,tf)]
                        m=(E.model.values==val)
                        if flt: m&=E[flt[0]].values==flt[1]
                        if held=='held': m&=E.lv.values==0
                        if name in GROUPS: m&=E.lvl.map(GROUPS[name]).values
                        else: m&=E.lvl.values==name
                        idx=np.flatnonzero(m)
                        if name in GROUPS and len(idx):   # one trade per entry bar + side
                            sub=E.iloc[idx]; idx=idx[~sub.duplicated(['e','d']).values]
                        idx=idx[np.argsort(E.e.values[idx],kind='stable')]
                        res[per]=(idx,stats(R[idx],np.arange(len(idx))))
                    so,sf=res['old'][1],res['fresh'][1]
                    if so['n'].max()<30: continue
                    # blended
                    Eo,Ro=D[('old',tf)];Ef,Rf=D[('fresh',tf)]
                    Rb=np.vstack([Ro[res['old'][0]],Rf[res['fresh'][0]]]); sb=stats(Rb,np.arange(len(Rb)))
                    for c in range(NC):
                        rows.append((tf,held,name,mv,c,*CN[c],
                            so['n'][c],so['wr'][c],so['avg'][c],so['pf'][c],so['t'][c],so['net'][c],so['dd'][c],
                            sf['n'][c],sf['wr'][c],sf['avg'][c],sf['pf'][c],sf['t'][c],sf['net'][c],sf['dd'][c],
                            sb['n'][c],sb['wr'][c],sb['avg'][c],sb['pf'][c],sb['t'][c],sb['net'][c],sb['dd'][c]))
                    keep[(tf,held,name,mv)]=(res['old'][0],res['fresh'][0])
        print(tf,len(rows),flush=True)
    cols=['ltf','held','level','entry','cfg','stop','boxexit','target','trail']
    for p in ('o','f','b'): cols+=[f'{p}_{k}' for k in ('n','wr','avg','pf','t','net','dd')]
    T=pd.DataFrame(rows,columns=cols)
    T.to_parquet('table.parquet'); pickle.dump(keep,open('keep.pkl','wb'))
    print(len(T))
