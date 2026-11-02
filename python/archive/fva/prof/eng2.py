class Bx:
    def __init__(s,id,pol,kind,tier,top,bot,tL,mk,ts):
        s.id,s.pol,s.kind,s.tier,s.top,s.bot,s.tL,s.mk,s.ts=id,pol,kind,tier,top,bot,tL,mk,ts
        s.tB=None;s.brk='';s.bn='';s.wife=-1;s.born=0;s.il='';s.leg=0
def run(d,purge=True,showIntB=False,cap=120,tick=0.25):
    HT=tick/2;BX=[];nid=[0];S=dict(side=0,tier=0,idT=-1,idP=-1,idR=-1,pend=0,pendW=-1,legN=0,legBu=-1,legBe=-1)
    pbX=pbXO=pbXC=pbXT=None
    pH=pL=None;lastBc=0;fnTop=fnBot=fnT=None;seqLo=seqHi=None;ev=[]
    def get(i):
        if i is None or i<0: return None
        for b in BX:
            if b.id==i: return b
    def new(*a):
        i=nid[0];nid[0]+=1;BX.append(Bx(i,*a));return i
    def same(pol,px):
        for b in reversed(BX):
            if (b.kind<=2 or b.id==S['idT']) and b.pol==pol and abs((b.bot if pol==1 else b.top)-px)<HT: return b.id
        return -1
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
        for b in BX:
            if b.kind in (4,5) or (b.kind==3 and b.id!=S['idT']): continue
            if b.pol==-1 and h>b.top+HT and c<=b.top:
                b.top=h;n=max(o,c)
                if b.bot+HT<n<b.top: b.bot=n;b.tL=t
            elif b.pol==1 and l<b.bot-HT and c>=b.bot:
                b.bot=l;n=min(o,c)
                if b.bot<n<b.top-HT: b.top=n;b.tL=t
        for pol in (-1,1):
            px=h if pol==-1 else l
            win=None;wp=-1
            for b in BX:
                if (b.kind<=2 or b.id==S['idT']) and b.pol==pol and abs((b.top if pol==-1 else b.bot)-px)<HT:
                    pr=5 if b.id==S['idT'] else 4 if b.kind==2 else 3 if b.kind==1 else 2 if b.kind==3 else 1
                    if pr>=wp: win=b;wp=pr
            if win:
                kl=[]
                for b in BX:
                    if b is not win and (b.kind<=2 or b.id==S['idT']) and b.pol==pol and abs((b.top if pol==-1 else b.bot)-px)<HT:
                        if (b.bot>win.bot+HT) if pol==-1 else (b.top<win.top-HT):
                            if pol==-1: win.bot=b.bot
                            else: win.top=b.top
                            win.tL=b.tL
                        if b.id==S['idR']: S['idR']=-1
                        if b.id==S['idP']: S['idP']=-1
                        kl.append(b.id)
                for i in kl: kill(i)
        side=S['side']
        if side!=0 and (S['idP']>=0 or S['pend']==1):
            if pbX is None or (h>pbX if side==-1 else l<pbX): pbX=h if side==-1 else l;pbXO,pbXC,pbXT=o,c,t
        newId=-1
        if isBu and lastBc==-1:
            lo=min(seqLo if seqLo is not None else l,l); tp=o if fnTop is None else fnTop; tl=t if fnT is None else fnT
            if tp<=lo: tp=max(o,c);tl=t
            mi=same(1,lo)
            if mi>=0:
                m=get(mi)
                if tp<m.top-HT: m.top=tp;m.tL=tl
                newId=mi
            else: newId=new(1,0,S['tier'],tp,lo,tl,bi,S['side'])
        elif isBe and lastBc==1:
            hi=max(seqHi if seqHi is not None else h,h); bt=o if fnBot is None else fnBot; tl=t if fnT is None else fnT
            if bt>=hi: bt=min(o,c);tl=t
            mi=same(-1,hi)
            if mi>=0:
                m=get(mi)
                if bt>m.bot+HT: m.bot=bt;m.tL=tl
                newId=mi
            else: newId=new(-1,0,S['tier'],hi,bt,tl,bi,S['side'])
        side=S['side']
        if newId>=0:
            nb=get(newId)
            if nb.kind==0:
                cand=nb;resum=nb.pol==side and side!=0 and ((S['pend']==0 and S['idP']>=0) or S['pend']==1)
                if resum and pbX is not None and (pbX>nb.top+HT if side==-1 else pbX<nb.bot-HT):
                    rid=same(side,pbX)
                    if rid<0:
                        eb,et=min(pbXO,pbXC),max(pbXO,pbXC)
                        if side==-1: rid=new(-1,0,S['tier'],pbX,eb if eb<pbX-HT else pbX-tick,pbXT,bi,side)
                        else: rid=new(1,0,S['tier'],et if et>pbX+HT else pbX+tick,pbX,pbXT,bi,side)
                    if rid!=S['idT']: nb.il='r';cand=get(rid)
                oR0=get(S['idR'])
                moreR=True if oR0 is None else (False if cand is oR0 else (cand.top>oR0.top+HT if side==-1 else cand.bot<oR0.bot-HT))
                if S['pend']==1 and resum:
                    cand.kind=3;cand.tier=S['tier'];cand.leg=S['legN'];cand.wife=S['pendW'];S.update(idT=cand.id,pend=0,pendW=-1);pbX=None
                elif S['pend']==2 and nb.pol==side:
                    nb.kind=3;nb.tier=S['tier'];nb.leg=S['legN'];nb.wife=S['pendW'];S.update(idT=nb.id,pend=0,pendW=-1)
                elif side==0:
                    S['side']=side=nb.pol;S['tier']=1;S['legN']+=1;nb.kind=3;nb.tier=1;nb.leg=S['legN'];S['idT']=nb.id
                    S['legBu' if side==1 else 'legBe']=S['legN']
                elif S['pend']==0 and nb.pol==-side:
                    if S['idP']<0: nb.kind=1;nb.tier=S['tier'];S['idP']=nb.id;pbX=h if side==-1 else l;pbXO,pbXC,pbXT=o,c,t
                    else: nb.il='p'
                elif resum and cand.kind==0:
                    if moreR:
                        if oR0: oR0.kind=0;oR0.il='r'
                        cand.kind=2;cand.tier=S['tier'];S['idR']=cand.id
                    else: cand.il='r';nb.il='r'
                else: nb.il='p' if nb.pol==-side else 'r'
        official=False;cT=get(S['idT'])
        if side!=0 and cT:
            if (c>cT.top if side==-1 else c<cT.bot):
                ns=-side;kill(cT.wife);cT.wife=-1;cT.born=3;cT.kind=4;cT.tB=t;cT.brk='CDL' if ns==1 else 'CDS';cT.bn=''
                if S['pend']==1: kill(S['pendW'])
                S['pend']=0;S['pendW']=-1
                oR=get(S['idR'])
                if oR: oR.kind=0;oR.il='r'
                S['legN']+=1;S['legBu' if ns==1 else 'legBe']=S['legN']
                bP=get(S['idP'])
                if bP: bP.kind=3;bP.tier=1;bP.leg=S['legN'];bP.wife=cT.id;S['idT']=bP.id
                else: S.update(idT=-1,pend=2,pendW=cT.id)
                pbX=None;ev.append((t,cT.brk,ns,S['pend']));S.update(side=ns,tier=1,idP=-1,idR=-1);official=True
            elif S['pend']==0:
                cP=get(S['idP'])
                if cP and (c<cP.bot if side==-1 else c>cP.top):
                    cP.born=1;cP.kind=4;cP.tB=t;cP.brk='LD' if side==1 else 'SD';cP.bn=str(S['tier']);S['tier']+=1
                    bR=get(S['idR'])
                    if bR: bR.kind=3;bR.tier=S['tier'];bR.leg=S['legN'];bR.wife=cP.id;S['idT']=bR.id
                    else: S.update(pend=1,pendW=cP.id)
                    if S['pend']==0: pbX=None
                    ev.append((t,cP.brk+cP.bn,side,S['pend']));S.update(idP=-1,idR=-1);official=True
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
        gg=0
        while len(BX)>cap and gg<20:
            gg+=1;cT=get(S['idT']);kw=cT.wife if cT else -1
            for b in BX:
                if b.id not in (S['idT'],S['idP'],S['idR'],kw,S['pendW']): kill(b.id);break
        if isBu or isBe: lastBc=1 if isBu else -1;fnTop=fnBot=fnT=None;seqLo,seqHi=l,h
        elif isN:
            if fnT is None: fnTop,fnBot,fnT=max(o,c),min(o,c),t
            seqLo=min(seqLo if seqLo is not None else l,l);seqHi=max(seqHi if seqHi is not None else h,h)
        pH,pL=h,l
    return BX,S,ev
