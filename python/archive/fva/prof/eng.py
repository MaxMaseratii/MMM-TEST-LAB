import pandas as pd, numpy as np
class Bx:
    def __init__(s,id,pol,kind,tier,top,bot,tL,mk,ts):
        s.id,s.pol,s.kind,s.tier,s.top,s.bot,s.tL,s.mk,s.ts=id,pol,kind,tier,top,bot,tL,mk,ts
        s.tB=None;s.brk='';s.bn='';s.wife=-1;s.born=0;s.il=''
def run(d,purge=True,showIntB=False,cap=120,tick=0.25):
    BX=[];nid=[0];S=dict(side=0,tier=0,idT=-1,idP=-1,idR=-1)
    pH=pL=None;lastBc=0;fnTop=fnBot=fnT=None;seqLo=seqHi=None
    legX=legXO=legXC=legXT=None;pbX=pbXO=pbXC=pbXT=None;ev=[]
    def get(i):
        for b in BX:
            if b.id==i: return b
    def new(*a):
        i=nid[0];nid[0]+=1;BX.append(Bx(i,*a));return i
    def kill(i):
        g=0
        while i>=0 and g<6:
            b=get(i)
            if b is None: break
            BX.remove(b);i=b.wife;g+=1
    O,H,L,C=d.open.values,d.high.values,d.low.values,d.close.values;T=d.index
    for bi in range(len(d)):
        o,h,l,c,t=O[bi],H[bi],L[bi],C[bi],T[bi]
        isBu=pH is not None and c>pH; isBe=pL is not None and c<pL; isN=pH is not None and not isBu and not isBe
        side,tier=S['side'],S['tier']
        newId=-1
        if isBu and lastBc==-1:
            lo=min(seqLo if seqLo is not None else l,l); tp=o if fnTop is None else fnTop
            if tp<=lo: tp=max(o,c)
            newId=new(1,0,tier,tp,lo,t if fnT is None else fnT,bi,side)
        elif isBe and lastBc==1:
            hi=max(seqHi if seqHi is not None else h,h); bt=o if fnBot is None else fnBot
            if bt>=hi: bt=min(o,c)
            newId=new(-1,0,tier,hi,bt,t if fnT is None else fnT,bi,side)
        if newId>=0:
            nb=get(newId)
            if side==0:
                S['side']=side=nb.pol;S['tier']=tier=1;nb.kind=3;nb.tier=1;nb.ts=side;S['idT']=newId;legX=None
            elif nb.pol==-side:
                if S['idP']<0: nb.kind=1;S['idP']=newId;pbX=None
                else: nb.il='p'
            else:
                if S['idP']>=0:
                    oR=get(S['idR'])
                    if oR: oR.kind=0;oR.il='r'
                    nb.kind=2;S['idR']=newId
                else: nb.il='r'
        if side!=0:
            if legX is None or (l<legX if side==-1 else h>legX): legX=l if side==-1 else h;legXO,legXC,legXT=o,c,t
            if S['idP']>=0 and (pbX is None or (h>pbX if side==-1 else l<pbX)): pbX=h if side==-1 else l;pbXO,pbXC,pbXT=o,c,t
        official=False
        cT=get(S['idT'])
        if cT and side!=0:
            if (c>cT.top if side==-1 else c<cT.bot):
                ns=-side;nT=S['idP']
                if nT<0:
                    eb,et=min(legXO,legXC),max(legXO,legXC)
                    if ns==1: nT=new(1,3,1,eb if eb>legX else et if et>legX else legX+tick,legX,legXT,bi,ns)
                    else: nT=new(-1,3,1,legX,et if et<legX else eb if eb<legX else legX-tick,legXT,bi,ns)
                nTb=get(nT);kill(cT.wife);cT.wife=-1;cT.born=3;cT.kind=4;cT.tB=t;cT.brk='CDL' if ns==1 else 'CDS';cT.bn=''
                nTb.kind=3;nTb.tier=1;nTb.ts=ns;nTb.wife=cT.id
                oR=get(S['idR'])
                if oR: oR.kind=0;oR.il='r'
                ev.append((t,cT.brk,ns))
                S.update(side=ns,tier=1,idT=nT,idP=-1,idR=-1);legX=l if ns==-1 else h;legXO,legXC,legXT=o,c,t;pbX=None;official=True
            else:
                cP=get(S['idP'])
                if cP and (c<cP.bot if side==-1 else c>cP.top):
                    nT=S['idR']
                    if nT<0:
                        eb,et=min(pbXO,pbXC),max(pbXO,pbXC)
                        if side==-1: nT=new(-1,3,tier+1,pbX,et if et<pbX else eb if eb<pbX else pbX-tick,pbXT,bi,side)
                        else: nT=new(1,3,tier+1,eb if eb>pbX else et if et>pbX else pbX+tick,pbX,pbXT,bi,side)
                    nTb=get(nT);cP.born=1;cP.kind=4;cP.tB=t;cP.brk='LD' if side==1 else 'SD';cP.bn=str(tier)
                    nTb.kind=3;nTb.tier=tier+1;nTb.ts=side;nTb.wife=cP.id
                    ev.append((t,cP.brk+cP.bn,side))
                    S.update(tier=tier+1,idT=nT,idP=-1,idR=-1);legX=l if side==-1 else h;legXO,legXC,legXT=o,c,t;pbX=None;official=True
        if official and purge:
            for i in [b.id for b in BX if b.kind in (0,5)]: kill(i)
        kl=[]
        for b in BX:
            if b.kind in (4,5) or b.mk==bi: continue
            if (c<b.bot if b.pol==1 else c>b.top):
                if b.kind==3:
                    if b.id!=S['idT']: kl.append(b.id)
                elif b.kind in (2,0):
                    if b.id==S['idR']: S['idR']=-1
                    if showIntB: b.born=b.kind;b.kind=5;b.tB=t;b.brk='cdl' if b.pol==-1 else 'cds'
                    else: kl.append(b.id)
        for i in kl: kill(i)
        for b in BX:
            if b.kind in (4,5) or b.mk==bi: continue
            if b.pol==-1 and h>b.top and c<=b.top:
                b.top=h;n=max(o,c)
                if b.bot<n<b.top: b.bot=n
            elif b.pol==1 and l<b.bot and c>=b.bot:
                b.bot=l;n=min(o,c)
                if b.bot<n<b.top: b.top=n
        g=0
        while len(BX)>cap and g<20:
            g+=1;cT=get(S['idT']);kw=cT.wife if cT else -1
            for b in BX:
                if b.id not in (S['idT'],S['idP'],S['idR'],kw): kill(b.id);break
        if isBu or isBe: lastBc=1 if isBu else -1;fnTop=fnBot=fnT=None;seqLo,seqHi=l,h
        elif isN:
            if fnT is None: fnTop,fnBot,fnT=max(o,c),min(o,c),t
            seqLo=min(seqLo if seqLo is not None else l,l);seqHi=max(seqHi if seqHi is not None else h,h)
        pH,pL=h,l
    return BX,S,ev
