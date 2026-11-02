import numpy as np, numba as nb
TICK=0.25
@nb.njit(cache=True)
def bc_arrays(H,L,C):
    n=len(C); bu=np.zeros(n,np.bool_); be=np.zeros(n,np.bool_); nn=np.zeros(n,np.bool_)
    for i in range(1,n):
        bu[i]=C[i]>H[i-1]; be[i]=C[i]<L[i-1]; nn[i]=not bu[i] and not be[i]
    return bu,be,nn
@nb.njit(cache=True)
def turn_boxes(O,H,L,C,bu,be,nn):
    """the MMM PRO f turn box (BeBC → NBC(s) → BuBC = bull box, mirror for bear)"""
    n=len(C); J=np.empty(n,np.int64);P=np.empty(n,np.int8);T=np.empty(n);B=np.empty(n);k=0
    last=0; fnT=-1; fnTop=0.0; fnBot=0.0; sLo=0.0; sHi=0.0; have=False
    for i in range(1,n):
        o,h,l,c=O[i],H[i],L[i],C[i]
        if bu[i] and last==-1:
            lo=min(sLo,l) if have else l; tp=fnTop if fnT>=0 else o
            if tp<=lo: tp=max(o,c)
            J[k]=i;P[k]=1;T[k]=tp;B[k]=lo;k+=1
        elif be[i] and last==1:
            hi=max(sHi,h) if have else h; bt=fnBot if fnT>=0 else o
            if bt>=hi: bt=min(o,c)
            J[k]=i;P[k]=-1;T[k]=hi;B[k]=bt;k+=1
        if bu[i] or be[i]:
            last=1 if bu[i] else -1; fnT=-1; sLo=l; sHi=h; have=True
        elif nn[i]:
            if fnT<0: fnT=i; fnTop=max(o,c); fnBot=min(o,c)
            sLo=min(sLo,l); sHi=max(sHi,h)
    return J[:k],P[:k],T[:k],B[:k]

@nb.njit(cache=True)
def wr(out,r,a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13=0.0):
    out[r,0]=a0;out[r,1]=a1;out[r,2]=a2;out[r,3]=a3;out[r,4]=a4;out[r,5]=a5;out[r,6]=a6
    out[r,7]=a7;out[r,8]=a8;out[r,9]=a9;out[r,10]=a10;out[r,11]=a11;out[r,12]=a12;out[r,13]=a13
    return r+1
@nb.njit(cache=True)
def find_entries(O,H,L,C,bu,be,nn,EI,ED,ETOP,EBOT,BJ,BP,BT,BB,W1,W2):
    """per event: first reversal box after the touch whose extreme reached the level, then the entry models.
    out rows: ev, model, e(bar), px, d, edge(box invalidation edge), top, bot, limit, rt, ty, boxj, ft"""
    n=len(C); ne=len(EI); out=np.full((ne*5,14),-1.0); r=0
    nbx=len(BJ)
    for q in range(ne):
        i=EI[q]; d=ED[q]
        # first box with j>=i (searchsorted)
        lo_=0; hi_=nbx
        while lo_<hi_:
            m=(lo_+hi_)//2
            if BJ[m]<i: lo_=m+1
            else: hi_=m
        b=-1
        for z in range(lo_,nbx):
            if BJ[z]>i+W1: break
            if BP[z]!=d: continue
            if d==1 and BB[z]<=ETOP[q]: b=z;break
            if d==-1 and BT[z]>=EBOT[q]: b=z;break
        if b<0: continue
        j=BJ[b]; top=BT[b]; bot=BB[b]
        if j+1>=n: continue
        # did price CLOSE through the HTF level (far edge) between the touch and the box?
        lv=0.0
        for k in range(i,j+1):
            if (d==1 and C[k]<EBOT[q]) or (d==-1 and C[k]>ETOP[q]): lv=1.0
        # M4: break candle → next open
        edge=bot if d==1 else top
        r=wr(out,r,q,4,j+1,O[j+1],d,edge,top,bot,0,0,0,j,-1,lv)
        touched=False; ft=-1; nbc=0; opp=0; inside=False; ty=0; m2=False
        k=j+1
        e1=-1
        while k<=min(j+W2,n-2):
            if d==1:
                if C[k]<bot: break
                if L[k]<bot: bot=L[k]
                tch=L[k]<=top
            else:
                if C[k]>top: break
                if H[k]>top: top=H[k]
                tch=H[k]>=bot
            dirBC=bu[k] if d==1 else be[k]
            oppBC=be[k] if d==1 else bu[k]
            outside=C[k]>top if d==1 else C[k]<bot
            if not touched:
                if tch:
                    touched=True; ft=k; ty=3 if opp>0 else (2 if nbc>0 else 1)
                    # M3: limit at the box edge (top for a bull box)
                    lim=top if d==1 else bot
                    px=min(O[k],lim) if d==1 else max(O[k],lim)
                    edge=bot if d==1 else top
                    r=wr(out,r,q,3,k,px,d,edge,top,bot,1,0,ty,j,ft,lv)
                else:
                    if nn[k]: nbc+=1
                    if oppBC: opp+=1
                    if dirBC and outside and not m2:
                        m2=True; edge=bot if d==1 else top
                        r=wr(out,r,q,2,k+1,O[k+1],d,edge,top,bot,0,0,0,j,-1,lv)
            if touched:
                if (C[k]<=top and C[k]>=bot): inside=True
                if dirBC and outside:
                    rt=1 if k==ft else (3 if inside else 2)
                    edge=bot if d==1 else top
                    r=wr(out,r,q,1,k+1,O[k+1],d,edge,top,bot,0,rt,ty,j,ft,lv)
                    e1=k
                    break
            k+=1
        # M5: the entry BC made a GMC → limit at the gap
        if e1>0 and e1+1<n and e1-1>=0:
            k=e1
            gap=(L[k+1]>H[k-1]) if d==1 else (H[k+1]<L[k-1])
            if gap:
                lim=L[k+1] if d==1 else H[k+1]
                for m in range(k+2,min(k+2+W2,n)):
                    if d==1:
                        if L[m]<=lim:
                            r=wr(out,r,q,5,m,min(O[m],lim),d,bot,top,bot,1,rt,ty,j,ft,lv); break
                        if C[m]<bot: break
                        if L[m]<bot: bot=L[m]
                    else:
                        if H[m]>=lim:
                            r=wr(out,r,q,5,m,max(O[m],lim),d,top,top,bot,1,rt,ty,j,ft,lv); break
                        if C[m]>top: break
                        if H[m]>top: top=H[m]
    return out[:r]

STOPS=np.array([20.,30.,50.,-1.])      # -1 = box (clamped 20-50)
TPS=np.array([2.,3.,5.,10.,0.])        # 0 = runner (no target)
NTR=5                                  # 0 none · 1 BE after 1 BC · 2 BE after 2 BC · 3 under each BC · 4 after first opposite candle
@nb.njit(cache=True,parallel=True)
def simulate(O,H,L,C,bu,be,SID,E,PX,D,EDGE,LIM,cost):
    ne=len(E); ncf=len(STOPS)*2*len(TPS)*NTR
    R=np.full((ne,ncf),np.nan,np.float32); n=len(C)
    for q in nb.prange(ne):
        e=int(E[q]); px=PX[q]; d=D[q]
        if e>=n: continue
        cf=0
        for si in range(len(STOPS)):
            if STOPS[si]>0: dist=STOPS[si]
            else:
                dist=(px-(EDGE[q]-TICK)) if d==1 else ((EDGE[q]+TICK)-px)
                dist=min(max(dist,20.0),50.0)
            for vv in range(2):
                for ti in range(len(TPS)):
                    for tr in range(NTR):
                        stop=px-d*dist; tp=px+d*TPS[ti]*dist if TPS[ti]>0 else np.nan
                        edge=EDGE[q]; s0=SID[e]; sw=False; nfav=0; oppS=False; swX=0.0
                        ex=np.nan
                        for k in range(e,min(n,e+3000)):
                            o,h,l,c=O[k],H[k],L[k],C[k]
                            if k>e:
                                if SID[k]>s0+1: ex=o; break
                                if SID[k]>s0 and not sw:
                                    if (o-px)*d<=0: ex=o; break
                                    sw=True
                            # stop
                            if (d==1 and l<=stop) or (d==-1 and h>=stop):
                                ex=min(o,stop) if d==1 else max(o,stop)
                                if k==e and LIM[q]==0: ex=stop if (d==1 and o>stop) or (d==-1 and o<stop) else o
                                break
                            if TPS[ti]>0 and (k>e or LIM[q]==0):
                                if (d==1 and h>=tp) or (d==-1 and l<=tp): ex=tp; break
                            # box close exit / box extension
                            if d==1:
                                if c<edge:
                                    if vv==1: ex=c; break
                                elif l<edge: edge=l
                            else:
                                if c>edge:
                                    if vv==1: ex=c; break
                                elif h>edge: edge=h
                            # trails (at the close)
                            fav=(bu[k] if d==1 else be[k]) and (c-px)*d>0
                            if fav:
                                nfav+=1
                                if (tr==1 and nfav>=1) or (tr==2 and nfav>=2):
                                    stop=max(stop,px) if d==1 else min(stop,px)
                                if tr==3 or sw:
                                    stop=max(stop,l) if d==1 else min(stop,h)
                                if tr==4 and oppS:
                                    stop=max(stop,swX) if d==1 else min(stop,swX)
                                    oppS=False
                            if tr==4:
                                if (be[k] if d==1 else bu[k]):
                                    if not oppS: oppS=True; swX=l if d==1 else h
                                if oppS:
                                    swX=min(swX,l) if d==1 else max(swX,h)
                            if k==n-1: ex=c
                        if not np.isnan(ex):
                            R[q,cf]=((ex-px)*d-cost)/dist
                        cf+=1
    return R
def cfg_names():
    out=[]
    for s in ['S20','S30','S50','Sbox']:
        for v in ['','+box exit']:
            for t in ['TP2','TP3','TP5','TP10','RUN']:
                for tr in ['','BE1','BE2','trailBC','trailOpp']:
                    out.append((s,v,t,tr))
    return out
