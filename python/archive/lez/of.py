import numpy as np, pandas as pd, pickle, sys, time
sys.path.insert(0,'/home/claude/lez')
from data import rs
from eng4 import run
from sim import bc_arrays
from sim2 import simulate2, limit_fill
from run import sid_of
W={'1m':120,'5m':60,'15m':40,'1h':30}
def bars(m1,tf):
    if tf=='1m': return m1
    return rs(m1,tf)
R0=pickle.load(open('raw.pkl','rb'))
FOUND=[]; ALL={}
for per in ('old','fresh'):
    for tf in ('1m','5m','15m','1h'):
        t0=time.time(); d=bars(R0[per],tf)
        O,H,L,C=[d[k].values.astype(np.float64) for k in ('open','high','low','close')]; n=len(C)
        bu,be,nn=bc_arrays(H,L,C); sid=sid_of(d.index)
        _,_,ev,_=run(d,snap=False)
        rows=[]
        for q,e in enumerate(ev):
            t,nm,dd,pend,bi,bt,bb,nt,nb=e[:9]; lz=e[9:11] if len(e)>=11 else (None,None)
            nxt=ev[q+1][4] if q+1<len(ev) else n-1
            cont=None if q+1>=len(ev) else int(ev[q+1][2]==dd)
            typ=nm[:3] if nm[:3] in ('CDL','CDS') else nm[:2]
            # foundations
            a=bnb=0; hitN=False; mfe=0.0
            for k in range(bi+1,min(n,bi+500)):
                dirb=bu[k] if dd==1 else be[k]; opp=be[k] if dd==1 else bu[k]
                mfe=max(mfe,(H[k]-C[bi]) if dd==1 else (C[bi]-L[k]))
                if opp: break
                if dirb:
                    a+=1
                    if not hitN: bnb+=1
                if nn[k]: hitN=True
            near=bt if dd==1 else bb; far=bb if dd==1 else bt
            kin=-1
            for k in range(bi+1,min(nxt+1,n)):
                if (dd==1 and C[k]<=near) or (dd==-1 and C[k]>=near): kin=k-bi; break
            seg=slice(bi+1,min(nxt+1,n))
            mfeN=((H[seg].max()-C[bi]) if dd==1 else (C[bi]-L[seg].min())) if nxt>bi else 0.0
            maeN=((C[bi]-L[seg].min()) if dd==1 else (H[seg].max()-C[bi])) if nxt>bi else 0.0
            thru=any((C[bi+1:nxt+1]<far) if dd==1 else (C[bi+1:nxt+1]>far))
            FOUND.append((per,tf,typ,dd,a,bnb,mfe,kin,cont,mfeN,maeN,bt-bb,int(thru),nxt-bi))
            # entries
            ent=[]
            ent.append((1,bi+1,O[bi+1] if bi+1<n else np.nan,far,0,-1))
            zones=[(2,bt,bb)]
            if nt is not None and ((dd==1 and nt<C[bi]) or (dd==-1 and nb>C[bi])): zones.append((3,nt,nb))
            if lz[0] is not None and ((dd==1 and lz[0]<C[bi]) or (dd==-1 and lz[1]>C[bi])): zones.append((4,lz[0],lz[1]))
            # first extra BC in the break direction (validation)
            kv=-1
            for k in range(bi+1,min(nxt,bi+W[tf],n)):
                if (bu[k] if dd==1 else be[k]): kv=k; break
            for code,zt,zb in zones:
                lim=zt if dd==1 else zb; fr=zb if dd==1 else zt
                end=min(nxt+1,bi+1+W[tf],n)
                m,px=limit_fill(O,H,L,C,dd,lim,fr,bi+1,end)
                if m>=0: ent.append((code,m,px,fr,1,0))
                if kv>0:
                    m2,px2=limit_fill(O,H,L,C,dd,lim,fr,kv+1,end)
                    if m2>=0: ent.append((code+10,m2,px2,fr,1,0))
            for code,m,px,fr,lim_,_ in ent:
                if m>=n or np.isnan(px): continue
                bk=any((C[bi+1:m]<=near) if dd==1 else (C[bi+1:m]>=near)) if m>bi+1 else False
                rows.append((q,typ,dd,code,m,px,fr,lim_,int(bk),cont if cont is not None else -1))
        E=pd.DataFrame(rows,columns=['ev','typ','d','model','e','px','edge','lim','backin','cont'])
        E['t']=d.index[E.e.values]
        Rm=simulate2(O,H,L,C,bu,be,sid,E.e.values.astype(np.float64),E.px.values,E.d.values.astype(np.float64),E.edge.values,E.lim.values.astype(np.float64),1.0)
        ALL[(per,tf)]=(E,Rm)
        print(per,tf,'events',len(ev),'entries',len(E),round(time.time()-t0,1),flush=True)
F=pd.DataFrame(FOUND,columns=['per','tf','typ','d','bc_before_opp','bc_before_nbc','mfe_to_opp','backin_bars','cont','mfe_next','mae_next','box','closed_through','bars_to_next'])
F.to_parquet('of_found.parquet'); pickle.dump(ALL,open('of_res.pkl','wb'))
