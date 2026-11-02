import numpy as np, numba as nb
from sim import bc_arrays, turn_boxes, wr, TICK
STOPS2=np.array([20.,30.,50.,-1.,-2.])   # -1 = zone edge clamped 20-50 · -2 = zone edge, no cap (min 10)
TPS2=np.array([2.,3.,5.,10.,0.]); NTR=5
@nb.njit(cache=True)
def wr16(out,r,v):
    for i in range(len(v)): out[r,i]=v[i]
    return r+1
@nb.njit(cache=True)
def limit_fill(O,H,L,C,d,lim,far,a,b):
    """first bar in [a,b) touching lim; cancel if a close goes past far edge first"""
    n=len(C)
    for m in range(a,min(b,n)):
        if d==1:
            if L[m]<=lim: return m,min(O[m],lim)
            if C[m]<far: return -1,0.0
        else:
            if H[m]>=lim: return m,max(O[m],lim)
            if C[m]>far: return -1,0.0
    return -1,0.0
@nb.njit(cache=True)
def find_entries2(O,H,L,C,bu,be,nn,EI,ED,ETOP,EBOT,BJ,BP,BT,BB,W1,W2,W3,needV):
    """HTF touch → first LTF reversal box → (optional: a 2nd BC in the trend first = box valid) → retest → entry BC.
    cols: ev,area,e,px,d,edge,top,bot,lim,seq,inside,ty,dirN,lv,boxj,k(entry BC)"""
    n=len(C); ne=len(EI); out=np.full((ne*6,16),-1.0); r=0; nbx=len(BJ)
    for q in range(ne):
        i=EI[q]; d=ED[q]
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
        if j+2>=n: continue
        lv=0.0
        for k in range(i,j+1):
            if (d==1 and C[k]<EBOT[q]) or (d==-1 and C[k]>ETOP[q]): lv=1.0
        valid=needV==0; touched=False; ft=-1; nbc=0; opp=0; dirN=0; ty=0
        hasN=False; hasO=False; inside=False; kE=-1
        for k in range(j+1,min(j+W2,n-2)):
            if d==1:
                if C[k]<bot: break
                if L[k]<bot: bot=L[k]
                tch=L[k]<=top; outside=C[k]>top
            else:
                if C[k]>top: break
                if H[k]>top: top=H[k]
                tch=H[k]>=bot; outside=C[k]<bot
            dirBC=bu[k] if d==1 else be[k]; oppBC=be[k] if d==1 else bu[k]
            if not valid:
                if dirBC and outside: valid=True; dirN+=1
                else:
                    if nn[k]: nbc+=1
                    if oppBC: opp+=1
                continue
            if not touched:
                if tch:
                    touched=True; ft=k; ty=3 if opp>0 else (2 if nbc>0 else 1)
                else:
                    if nn[k]: nbc+=1
                    if oppBC: opp+=1
                    if dirBC: dirN+=1
                    continue
            # from the touch on (the touch candle included)
            if C[k]<=top and C[k]>=bot: inside=True
            if dirBC and outside:
                kE=k; break
            if nn[k]: hasN=True
            if oppBC: hasO=True
        if kE<0: continue
        # sequence between the touch and the entry BC
        seq=1 if (not hasN and not hasO) else (2 if (hasN and not hasO) else (3 if (hasN and hasO) else 4))
        edge=bot if d==1 else top
        ins=1.0 if inside else 0.0
        k=kE
        # areas: 1 next open · 2 BC 50% · 3 BC open · 4 the high/low the BC broke · 5 box edge · 6 GMC gap
        v=np.empty(16)
        v[0]=q;v[2]=k+1;v[3]=O[k+1];v[4]=d;v[5]=edge;v[6]=top;v[7]=bot;v[8]=0;v[9]=seq;v[10]=ins;v[11]=ty;v[12]=dirN;v[13]=lv;v[14]=j;v[15]=k
        v[1]=1; r=wr16(out,r,v)
        for area in (2,3,4,5):
            if area==2: lim=(O[k]+C[k])/2
            elif area==3: lim=O[k]
            elif area==4: lim=H[k-1] if d==1 else L[k-1]
            else: lim=top if d==1 else bot
            m,px=limit_fill(O,H,L,C,d,lim,edge,k+1,k+1+W3)
            if m>=0:
                v[1]=area;v[2]=m;v[3]=px;v[8]=1; r=wr16(out,r,v)
        if k+1<n:
            gap=(L[k+1]>H[k-1]) if d==1 else (H[k+1]<L[k-1])
            if gap:
                lim=L[k+1] if d==1 else H[k+1]
                m,px=limit_fill(O,H,L,C,d,lim,edge,k+2,k+2+W3)
                if m>=0:
                    v[1]=6;v[2]=m;v[3]=px;v[8]=1; r=wr16(out,r,v)
    return out[:r]

@nb.njit(cache=True,parallel=True)
def simulate2(O,H,L,C,bu,be,SID,E,PX,D,EDGE,LIM,cost):
    ne=len(E); ncf=len(STOPS2)*2*len(TPS2)*NTR
    R=np.full((ne,ncf),np.nan,np.float32); n=len(C)
    for q in nb.prange(ne):
        e=int(E[q]); px=PX[q]; d=D[q]
        if e>=n or e<0: continue
        cf=0
        for si in range(len(STOPS2)):
            if STOPS2[si]>0: dist=STOPS2[si]
            else:
                dist=(px-(EDGE[q]-TICK)) if d==1 else ((EDGE[q]+TICK)-px)
                if STOPS2[si]==-1: dist=min(max(dist,20.0),50.0)
                else: dist=max(dist,10.0)
            for vv in range(2):
                for ti in range(len(TPS2)):
                    for tr in range(NTR):
                        stop=px-d*dist; tp=px+d*TPS2[ti]*dist if TPS2[ti]>0 else np.nan
                        edge=EDGE[q]; s0=SID[e]; sw=False; nfav=0; oppS=False; swX=0.0; ex=np.nan
                        for k in range(e,min(n,e+3000)):
                            o,h,l,c=O[k],H[k],L[k],C[k]
                            if k>e:
                                if SID[k]>s0+1: ex=o; break
                                if SID[k]>s0 and not sw:
                                    if (o-px)*d<=0: ex=o; break
                                    sw=True
                            if (d==1 and l<=stop) or (d==-1 and h>=stop):
                                ex=min(o,stop) if d==1 else max(o,stop)
                                if k==e and LIM[q]==0: ex=stop if (d==1 and o>stop) or (d==-1 and o<stop) else o
                                break
                            if TPS2[ti]>0 and (k>e or LIM[q]==0):
                                if (d==1 and h>=tp) or (d==-1 and l<=tp): ex=tp; break
                            if d==1:
                                if c<edge:
                                    if vv==1: ex=c; break
                                elif l<edge: edge=l
                            else:
                                if c>edge:
                                    if vv==1: ex=c; break
                                elif h>edge: edge=h
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
                        if not np.isnan(ex): R[q,cf]=((ex-px)*d-cost)/dist
                        cf+=1
    return R
def cfg_names2():
    out=[]
    for s in ['S20','S30','S50','Sbox','Szone']:
        for v in ['','+box exit']:
            for t in ['TP2','TP3','TP5','TP10','RUN']:
                for tr in ['','BE1','BE2','trailBC','trailOpp']:
                    out.append((s,v,t,tr))
    return out
