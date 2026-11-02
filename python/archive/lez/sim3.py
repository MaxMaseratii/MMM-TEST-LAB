import numpy as np, numba as nb
TICK=0.25
ST3=np.array([20.,30.,50.,-1.]); TP3=np.array([2.,3.,5.,0.]); MG3=4; RE3=np.array([0,1,3])
@nb.njit(cache=True)
def one_trade(O,H,L,C,bu,be,SID,e,px,d,top,bot,dist,tpm,mg,cost,n):
    """returns exit bar, R, reason (0 stop/BE · 1 target · 2 box violated · 3 time · 4 end)"""
    stop=px-d*dist; tp=px+d*tpm*dist if tpm>0 else np.nan
    s0=SID[e]; sw=False; nfav=0; oppS=False; be_px=px+d*cost
    for k in range(e,min(n,e+3000)):
        o,h,l,c=O[k],H[k],L[k],C[k]
        if k>e:
            if SID[k]>s0+1: return k,((o-px)*d-cost)/dist,3
            if SID[k]>s0 and not sw:
                if (o-px)*d<=0: return k,((o-px)*d-cost)/dist,3
                sw=True
        if (d==1 and l<=stop) or (d==-1 and h>=stop):
            x=min(o,stop) if d==1 else max(o,stop)
            if k==e: x=stop
            return k,((x-px)*d-cost)/dist,0
        if tpm>0 and ((d==1 and h>=tp) or (d==-1 and l<=tp)): return k,((tp-px)*d-cost)/dist,1
        if d==1:
            if c<bot: return k,((c-px)*d-cost)/dist,2
            if l<bot: bot=l
        else:
            if c>top: return k,((c-px)*d-cost)/dist,2
            if h>top: top=h
        fav=(bu[k] if d==1 else be[k]) and (c-px)*d>cost
        if fav:
            nfav+=1
            if (mg==1 and nfav>=1) or (mg==2 and nfav>=2) or (mg==3 and oppS):
                stop=max(stop,be_px) if d==1 else min(stop,be_px)
            if sw: stop=max(stop,l) if d==1 else min(stop,h)
        if mg==3 and (be[k] if d==1 else bu[k]): oppS=True
        if k==n-1: return k,((c-px)*d-cost)/dist,4
    return min(n-1,e+2999),0.0,4
@nb.njit(cache=True,parallel=True)
def simulate3(O,H,L,C,bu,be,SID,E,PX,D,TOP,BOT,cost,W):
    ne=len(E); nc=len(ST3)*len(TP3)*MG3*len(RE3); n=len(C)
    R=np.full((ne,nc),np.nan,np.float32); NT=np.zeros((ne,nc),np.int8); PT=np.full((ne,nc),np.nan,np.float32)
    for q in nb.prange(ne):
        e0=int(E[q])
        if e0<0 or e0>=n: continue
        d=int(D[q]); cf=0
        for si in range(len(ST3)):
            for ti in range(len(TP3)):
                for mg in range(MG3):
                    for ri in range(len(RE3)):
                        tot=0.0; pts=0.0; nt=0; e=e0; px=PX[q]; top=TOP[q]; bot=BOT[q]; left=RE3[ri]
                        while True:
                            if ST3[si]>0: dist=ST3[si]
                            else:
                                dist=(px-(bot-TICK)) if d==1 else ((top+TICK)-px)
                                dist=min(max(dist,20.0),50.0)
                            k,r,why=one_trade(O,H,L,C,bu,be,SID,e,px,d,top,bot,dist,TP3[ti],mg,cost,n)
                            tot+=r; pts+=r*dist; nt+=1
                            if why!=0 or left==0: break
                            # re-entry: box still valid → touch → BC out of the box → next open
                            sx=SID[k]; touched=False; ne_=-1
                            for m in range(k+1,min(n-1,k+W)):
                                if SID[m]>sx+1: break
                                if d==1:
                                    if C[m]<bot: break
                                    if L[m]<=top: touched=True
                                    if touched and bu[m] and C[m]>top: ne_=m+1; break
                                else:
                                    if C[m]>top: break
                                    if H[m]>=bot: touched=True
                                    if touched and be[m] and C[m]<bot: ne_=m+1; break
                            if ne_<0: break
                            e=ne_; px=O[e]; left-=1
                        R[q,cf]=tot; NT[q,cf]=nt; PT[q,cf]=pts; cf+=1
    return R,NT,PT
def cfg3():
    out=[]
    for s in ['S20','S30','S50','Sbox']:
        for t in ['TP2','TP3','TP5','RUN']:
            for m in ['no BE','BE+fees after 1 BC','BE+fees after 2 BC','BE+fees after opp candle → BC']:
                for r in ['no re-entry','1 re-entry','3 re-entries']:
                    out.append((s,t,m,r))
    return out
