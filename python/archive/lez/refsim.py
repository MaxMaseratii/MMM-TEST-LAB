import numpy as np, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim import STOPS,TPS,cfg_names,bc_arrays
from run import ltf_arrays, sid_of
def ref(O,H,L,C,bu,be,SID,e,px,d,EDGE,lim,cfg,cost=1.0):
    s,v,t,tr=cfg
    if s=='Sbox': dist=min(max(abs(px-EDGE)+0.25,20),50)
    else: dist=float(s[1:])
    R_=float(t[2:]) if t!='RUN' else 0
    stop=px-d*dist; tp=px+d*R_*dist; edge=EDGE; s0=SID[e]; sw=False; nfav=0; opp=False; sx=0
    n=len(C)
    for k in range(e,min(n,e+3000)):
        o,h,l,c=O[k],H[k],L[k],C[k]
        if k>e:
            if SID[k]>s0+1: return ((o-px)*d-cost)/dist
            if SID[k]>s0 and not sw:
                if (o-px)*d<=0: return ((o-px)*d-cost)/dist
                sw=True
        if (d==1 and l<=stop) or (d==-1 and h>=stop):
            x=min(o,stop) if d==1 else max(o,stop)
            if k==e and not lim: x=stop
            return ((x-px)*d-cost)/dist
        if R_>0 and (k>e or not lim) and ((d==1 and h>=tp) or (d==-1 and l<=tp)): return ((tp-px)*d-cost)/dist
        if d==1:
            if c<edge:
                if v: return ((c-px)*d-cost)/dist
            elif l<edge: edge=l
        else:
            if c>edge:
                if v: return ((c-px)*d-cost)/dist
            elif h>edge: edge=h
        fav=(bu[k] if d==1 else be[k]) and (c-px)*d>0
        if fav:
            nfav+=1
            if (tr=='BE1' and nfav>=1) or (tr=='BE2' and nfav>=2): stop=max(stop,px) if d==1 else min(stop,px)
            if tr=='trailBC' or sw: stop=max(stop,l) if d==1 else min(stop,h)
            if tr=='trailOpp' and opp: stop=max(stop,sx) if d==1 else min(stop,sx); opp=False
        if tr=='trailOpp':
            if (be[k] if d==1 else bu[k]) and not opp: opp=True; sx=l if d==1 else h
            if opp: sx=min(sx,l) if d==1 else max(sx,h)
        if k==n-1: return ((c-px)*d-cost)/dist
    return np.nan
if __name__=='__main__':
    R0=pickle.load(open('raw.pkl','rb'))
    CN=cfg_names(); rng=np.random.default_rng(1)
    for tf in ('1m','5m'):
        E,Rm=pickle.load(open(f'res_fresh_{tf}.pkl','rb'))
        d=ltf_arrays(R0['fresh'],tf); O,H,L,C=[d[k].values for k in ('open','high','low','close')]
        bu,be,nn=bc_arrays(H,L,C); sid=sid_of(d.index)
        bad=0;tot=0
        for q in rng.choice(len(E),300,replace=False):
            x=E.iloc[q]
            for c in rng.choice(len(CN),5,replace=False):
                r=ref(O,H,L,C,bu,be,sid,int(x.e),x.px,int(x.d),x.edge,bool(x.lim),CN[c])
                tot+=1
                if not (abs(r-Rm[q,c])<1e-3): bad+=1; print('MISMATCH',tf,q,CN[c],r,Rm[q,c]) if bad<5 else None
        print(tf,'checked',tot,'mismatches',bad)
