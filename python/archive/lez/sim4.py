import numpy as np, numba as nb
from sim2 import wr16, limit_fill
@nb.njit(cache=True)
def turn_boxes2(O,H,L,C,bu,be,nn):
    n=len(C); J=np.empty(n,np.int64);P=np.empty(n,np.int8);T=np.empty(n);B=np.empty(n);K=np.empty(n,np.int8);k=0
    last=0; fnT=-1; fnTop=0.0; fnBot=0.0; sLo=0.0; sHi=0.0; have=False
    for i in range(1,n):
        o,h,l,c=O[i],H[i],L[i],C[i]
        if bu[i] and last==-1:
            lo=min(sLo,l) if have else l; tp=fnTop if fnT>=0 else o
            if tp<=lo: tp=max(o,c)
            J[k]=i;P[k]=1;T[k]=tp;B[k]=lo;K[k]=2 if fnT>=0 else 1;k+=1
        elif be[i] and last==1:
            hi=max(sHi,h) if have else h; bt=fnBot if fnT>=0 else o
            if bt>=hi: bt=min(o,c)
            J[k]=i;P[k]=-1;T[k]=hi;B[k]=bt;K[k]=2 if fnT>=0 else 1;k+=1
        if bu[i] or be[i]:
            last=1 if bu[i] else -1; fnT=-1; sLo=l; sHi=h; have=True
        elif nn[i]:
            if fnT<0: fnT=i; fnTop=max(o,c); fnBot=min(o,c)
            sLo=min(sLo,l); sHi=max(sHi,h)
    return J[:k],P[:k],T[:k],B[:k],K[:k]
@nb.njit(cache=True)
def find_entries3(O,H,L,C,bu,be,nn,EI,ED,ETOP,EBOT,BJ,BP,BT,BB,BK,W1,W2,W3):
    """HTF touch → first LTF box → what happens BEFORE the retest (flags) → retest → 1st BC out → entry areas.
    entries cols: ev,area,e,px,d,edge,top,bot,lim,pre,touchtype,first,boxtype,lv,boxj,k
    boxes cols: ev,d,boxtype,first,second,retested,bars_to_retest,lv"""
    n=len(C); ne=len(EI); out=np.full((ne*6,18),-1.0); r=0; nbx=len(BJ)
    bx=np.full((ne,12),-1.0); rb=0
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
        j=BJ[b]; top=BT[b]; bot=BB[b]; btyp=BK[b]
        if j+2>=n: continue
        lv=0.0
        for k in range(i,j+1):
            if (d==1 and C[k]<EBOT[q]) or (d==-1 and C[k]>ETOP[q]): lv=1.0
        fD=False; fN=False; fO=False; touched=False; ft=-1; inside=False; kE=-1
        first=0; second=0; pN=False; pO=False; nxt=0; outc=3; broke=False
        for k in range(j+1,min(j+W2,n-2)):
            if d==1:
                if C[k]<bot:
                    broke=True; break
                if L[k]<bot: bot=L[k]
                tch=L[k]<=top; outside=C[k]>top
            else:
                if C[k]>top:
                    broke=True; break
                if H[k]>top: top=H[k]
                tch=H[k]>=bot; outside=C[k]<bot
            dirBC=bu[k] if d==1 else be[k]; oppBC=be[k] if d==1 else bu[k]
            ctype=1 if dirBC else (3 if oppBC else 2)
            if k==j+1: first=ctype
            if k==j+2: second=ctype
            if not touched:
                if tch:
                    touched=True; ft=k
                else:
                    if dirBC: fD=True
                    if nn[k]: fN=True
                    if oppBC: fO=True
                    continue
            if C[k]<=top and C[k]>=bot: inside=True
            if k==ft+1:
                nxt=(1 if outside else 4) if dirBC else (3 if oppBC else 2)
            if dirBC and outside:
                kE=k; break
            if k>ft:
                if nn[k]: pN=True
                if oppBC: pO=True
        # the box itself (retest or not)
        post=-1
        if kE>=0: post=4 if kE==ft else (2 if pN else 0)+(1 if pO else 0)
        if not touched: outc=0
        elif kE>=0: outc=1
        elif broke: outc=2
        bx[rb,0]=q;bx[rb,1]=d;bx[rb,2]=btyp;bx[rb,3]=first;bx[rb,4]=second;bx[rb,5]=1.0 if touched else 0.0;bx[rb,6]=(ft-j) if touched else -1.0;bx[rb,7]=lv
        bx[rb,8]=outc;bx[rb,9]=post;bx[rb,10]=nxt;bx[rb,11]=1.0 if inside else 0.0; rb+=1
        if kE<0: continue
        pre=(4 if fD else 0)+(2 if fN else 0)+(1 if fO else 0)
        edge=bot if d==1 else top
        k=kE
        v=np.empty(18)
        v[0]=q;v[2]=k+1;v[3]=O[k+1];v[4]=d;v[5]=edge;v[6]=top;v[7]=bot;v[8]=0;v[9]=pre;v[10]=1.0 if inside else 0.0;v[11]=first;v[12]=btyp;v[13]=lv;v[14]=j;v[15]=k;v[16]=post;v[17]=nxt
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
    return out[:r],bx[:rb]
