import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from data import rs
from eng4 import run
TICK=0.25
def sess_min(idx):
    m=idx.hour*60+idx.minute
    return (m-1080)%1440            # minutes since 18:00
def day_key(idx):
    return ((idx+pd.Timedelta(hours=6)).normalize())   # trading date (18:00 belongs to next date)

def first_touch_zone(L,H,C,s,e,top,bot,d):
    """first bar in [s,e) touching a zone from the right side. d=1 support (low<=top), d=-1 resistance (high>=bot)"""
    if s>=e: return -1
    if d==1:
        w=np.flatnonzero(L[s:e]<=top)
    else:
        w=np.flatnonzero(H[s:e]>=bot)
    return s+w[0] if len(w) else -1

def first_touch_line(L,H,C,s,e,p):
    if s<1 or s>=e: return -1,0
    pc=C[s-1]
    if pc>p: d=1; w=np.flatnonzero(L[s:e]<=p)
    elif pc<p: d=-1; w=np.flatnonzero(H[s:e]>=p)
    else: return -1,0
    return (s+w[0],d) if len(w) else (-1,0)

def build(m1, name):
    idx=m1.index; O,H,L,C=[m1[k].values for k in ('open','high','low','close')]
    n=len(m1); EV=[]
    sm=sess_min(idx); dk=day_key(idx)
    ts=idx.values
    def add(i,d,nm,top,bot,t0):
        if i>=0: EV.append((i,d,nm,top,bot,t0))
    # ── 1. MMM PRO f boxes on M15 / H1 / H4 ──
    for tf,tag in (('15m','M15'),('1h','H1'),('4h','H4')):
        d=rs(m1,tf)
        if tf=='4h': key=(idx-pd.Timedelta(hours=18)).floor('4h')+pd.Timedelta(hours=18)
        else: key=idx.floor({'15m':'15min','1h':'60min'}[tf])
        hidx=np.searchsorted(d.index.values,key.values)        # htf candle of each 1m bar
        seg=np.r_[0,np.flatnonzero(np.diff(hidx))+1,n]           # 1m segments per htf candle
        segs={hidx[seg[k]]:(seg[k],seg[k+1]) for k in range(len(seg)-1)}
        BX,S,ev,SN=run(d)
        sn=pd.DataFrame(SN,columns=['bi','id','d','cat','top','bot'])
        cats=sorted(sn['cat'].unique()); cmap={c:i for i,c in enumerate(cats)}
        A_bi=sn.bi.values; A_key=sn.id.values.astype(np.int64)*100+sn['cat'].map(cmap).values
        A_d=sn.d.values; A_tp=sn.top.values; A_bt=sn.bot.values; A_cat=sn['cat'].values
        bnd=np.r_[0,np.flatnonzero(np.diff(A_bi))+1,len(A_bi)]
        done=set()
        for q in range(len(bnd)-1):
            u,v=bnd[q],bnd[q+1]; bi=A_bi[u]
            if bi+1 not in segs: continue
            s,e=segs[bi+1]
            keys=A_key[u:v]
            m=np.array([k not in done for k in keys])
            if not m.any(): continue
            idxs=np.arange(u,v)[m]
            dd=A_d[idxs];tp=A_tp[idxs];bt=A_bt[idxs]
            lo=L[s:e][:,None];hi=H[s:e][:,None]
            hit=np.where(dd[None,:]==1,lo<=tp[None,:],hi>=bt[None,:])
            any_=hit.any(0)
            if any_.any():
                fi=hit.argmax(0)
                for jj in np.flatnonzero(any_):
                    r=idxs[jj]; done.add(A_key[r])
                    add(s+fi[jj],int(A_d[r]),tag+' '+A_cat[r],A_tp[r],A_bt[r],0)
        print(name,tag,'events so far',len(EV),flush=True)
    # ── 2. UPG / UDG gaps (3-candle) ──
    age={'15m':2,'1h':5,'4h':10,'D':30,'W':90}
    for tf,tag in (('15m','M15'),('1h','H1'),('4h','H4'),('D','D'),('W','W')):
        d=rs(m1,tf); ho,hh,hl,hc=d.open.values,d.high.values,d.low.values,d.close.values
        st=d.index.values
        # first 1m bar after the candle close = start of the next candle
        nxt=np.r_[st[1:],np.datetime64('2100-01-01')]
        for k in range(2,len(d)):
            if k+1>=len(d): break
            s=np.searchsorted(ts,nxt[k]); e=np.searchsorted(ts,nxt[k]+np.timedelta64(age[tf],'D'))
            if hl[k]-hh[k-2]>=2*TICK and hc[k-1]>hh[k-2]:
                add(first_touch_zone(L,H,C,s,e,hl[k],hh[k-2],1),1,tag+' UPG',hl[k],hh[k-2],0)
            if hl[k-2]-hh[k]>=2*TICK and hc[k-1]<hl[k-2]:
                add(first_touch_zone(L,H,C,s,e,hl[k-2],hh[k],-1),-1,tag+' UPG',hl[k-2],hh[k],0)
    print(name,'gaps',len(EV),flush=True)
    # ── 3. session ranges / day levels / opens ──
    df=pd.DataFrame({'i':np.arange(n),'sm':sm,'dk':dk,'h':H,'l':L,'o':O,'c':C})
    days=df.groupby('dk')
    win={'Asia':(0,480,480,1320),'London':(480,840,840,1320),'London OR':(480,510,510,840),'Pre-open':(840,930,930,1320),
         'Globex/ON':(0,930,930,1320),'NY AM OR15':(930,945,945,1320),'NY AM OR30':(930,960,960,1320),
         'NY AM session':(930,1080,1080,1320),'NY PM OR':(1170,1185,1185,1320)}
    dlist=list(days.groups.keys())
    for nm,(a,b,va,vb) in win.items():
        for k_,g in days:
            f=g[(g.sm>=a)&(g.sm<b)]; v=g[(g.sm>=va)&(g.sm<vb)]
            if len(f)<max(3,(b-a)//3) or not len(v): continue
            s,e=v.i.iloc[0],v.i.iloc[-1]+1
            for p,lab in ((f.h.max(),'H'),(f.l.min(),'L')):
                i,dd=first_touch_line(L,H,C,s,e,p); add(i,dd,f'{nm} {lab}',p,p,0)
    print(name,'ranges',len(EV),flush=True)
    # PDH/PDL/PDC, opens
    prev=None
    for k_,g in days:
        if prev is not None and len(g)>30:
            s,e=g.i.iloc[0],g.i.iloc[-1]+1
            for p,lab in ((prev.h.max(),'PDH'),(prev.l.min(),'PDL'),(prev.c.iloc[-1],'PD close')):
                i,dd=first_touch_line(L,H,C,s+1,e,p); add(i,dd,lab,p,p,0)
            # futures daily opening gap (17:00 close → 18:00 open)
            go,gc=g.o.iloc[0],prev.c.iloc[-1]
            if abs(go-gc)>=2*TICK:
                dd=1 if go>gc else -1; top,bot=max(go,gc),min(go,gc)
                add(first_touch_zone(L,H,C,s+1,e,top,bot,dd),dd,'Daily opening gap',top,bot,0)
            # RTH opening gap (prior 16:00 close → 9:30 open)
            pr=prev[prev.sm<1320]; r=g[g.sm>=930]
            if len(pr) and len(r) and r.sm.iloc[0]==930:
                go,gc=r.o.iloc[0],pr.c.iloc[-1]; ri=r.i.iloc[0]; re_=g[g.sm<1320].i.iloc[-1]+1
                if abs(go-gc)>=2*TICK:
                    dd=1 if go>gc else -1; top,bot=max(go,gc),min(go,gc)
                    add(first_touch_zone(L,H,C,ri+1,re_,top,bot,dd),dd,'RTH opening gap',top,bot,0)
        # opens (touch after the open candle)
        if len(g)>30:
            s,e=g.i.iloc[0],g.i.iloc[-1]+1
            i,dd=first_touch_line(L,H,C,s+1,e,g.o.iloc[0]); add(i,dd,'Daily open 18:00',g.o.iloc[0],g.o.iloc[0],0)
            mo=g[g.sm==360]
            if len(mo):
                j=mo.i.iloc[0]; e2=g[g.sm<1320].i.iloc[-1]+1
                i,dd=first_touch_line(L,H,C,j+1,e2,O[j]); add(i,dd,'Midnight open',O[j],O[j],0)
            no=g[g.sm==930]
            if len(no):
                j=no.i.iloc[0]; e2=g[g.sm<1320].i.iloc[-1]+1
                i,dd=first_touch_line(L,H,C,j+1,e2,O[j]); add(i,dd,'NY 9:30 open',O[j],O[j],0)
        prev=g
    print(name,'day',len(EV),flush=True)
    # weekly: PWH/PWL/weekly open, NWOG
    wk=(pd.to_datetime(df.dk)-pd.to_timedelta(pd.to_datetime(df.dk).dt.weekday,unit='D'))
    df['wk']=wk.values; prevw=None
    for k_,g in df.groupby('wk'):
        s,e=g.i.iloc[0],g.i.iloc[-1]+1
        if prevw is not None:
            for p,lab in ((prevw.h.max(),'PWH'),(prevw.l.min(),'PWL')):
                i,dd=first_touch_line(L,H,C,s+1,e,p); add(i,dd,lab,p,p,0)
            go,gc=g.o.iloc[0],prevw.c.iloc[-1]
            if abs(go-gc)>=2*TICK:
                dd=1 if go>gc else -1; top,bot=max(go,gc),min(go,gc)
                add(first_touch_zone(L,H,C,s+1,e,top,bot,dd),dd,'Weekly opening gap',top,bot,0)
        i,dd=first_touch_line(L,H,C,s+1,e,g.o.iloc[0]); add(i,dd,'Weekly open',g.o.iloc[0],g.o.iloc[0],0)
        prevw=g
    # H4: prior H4 high/low + H4 open
    key=(idx-pd.Timedelta(hours=18)).floor('4h')+pd.Timedelta(hours=18)
    hk=np.searchsorted(np.unique(key.values),key.values)
    seg=np.r_[0,np.flatnonzero(np.diff(hk))+1,n]
    for k in range(len(seg)-1):
        s,e=seg[k],seg[k+1]
        if k>0:
            ps,pe=seg[k-1],seg[k]
            for p,lab in ((H[ps:pe].max(),'H4 high'),(L[ps:pe].min(),'H4 low')):
                i,dd=first_touch_line(L,H,C,s,e,p); add(i,dd,lab,p,p,0)
        i,dd=first_touch_line(L,H,C,s+1,e,O[s]); add(i,dd,'H4 open',O[s],O[s],0)
    print(name,'all',len(EV),flush=True)
    ev=pd.DataFrame(EV,columns=['i','d','lvl','top','bot','x']).drop(columns='x')
    ev['t']=idx[ev.i.values]
    return ev
if __name__=='__main__':
    R=pickle.load(open('/home/claude/lez/raw.pkl','rb'))
    out={}
    for nm in ('fresh','old'):
        out[nm]=build(R[nm],nm)
        print(out[nm].groupby('lvl').size().to_string())
    pickle.dump(out,open('/home/claude/lez/events.pkl','wb'))
