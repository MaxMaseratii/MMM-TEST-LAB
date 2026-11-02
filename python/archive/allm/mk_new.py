import pandas as pd, numpy as np, json, pickle, grade1
RULES={'C.M4':(1,1,5,2,'market at c3 close · fixed stop · 1:6 · next session open'),
       'XCS.M1':(6,1,2,0,'limit at MP of the break candle · fixed stop · 1:2'),
       'X.M3':(1,0,2,0,'market at block birth close · stop block top − fixed · 1:2'),
       'X.M4':(1,1,2,2,'market at break close · fixed stop · 1:2 · next session open')}
SITE=json.load(open('/home/claude/mmmpro-journal/backtests/d_book_assets.json'))
MK={'ES':'MES','GC':'MGC','CL':'MCL'}
def tst(r): return float(r.mean()/r.std(ddof=1)*np.sqrt(len(r))) if len(r)>2 and r.std(ddof=1)>0 else None
def mx(r):
    ml=mw=cl=cw=0
    for v in r:
        if v>0: cw+=1; cl=0
        else: cl+=1; cw=0
        ml=max(ml,cl); mw=max(mw,cw)
    return ml,mw
def st(b,months):
    if len(b)==0: return None
    r=b.R.values; pts=r*b.risk.values; w=pts[pts>0]; l=-pts[pts<=0]
    eq=np.cumsum(r); ddR=float((np.maximum.accumulate(np.r_[0,eq])[1:]-eq).max())
    ep=np.cumsum(pts); ddP=float((np.maximum.accumulate(np.r_[0,ep])[1:]-ep).max())
    ml,mw=mx(r); gw=r[r>0].sum(); gl=-r[r<=0].sum()
    return dict(n=int(len(r)),wr=float((r>0).mean()),av=float(r.mean()),pf=float(gw/gl) if gl>0 else None,t=tst(r),netR=float(r.sum()),netPts=float(pts.sum()),
        winPts=float(w.sum()),lossPts=float(l.sum()),avgWinPts=float(w.mean()) if len(w) else 0.0,avgLossPts=float(l.mean()) if len(l) else 0.0,
        bigWinPts=float(w.max()) if len(w) else 0.0,bigLossPts=float(l.max()) if len(l) else 0.0,maxLoss=ml,maxWin=mw,ddPts=ddP,ddR=ddR,perMonth=float(len(r)/months),risk=float(b.risk.mean()))
def verdict(a,p1,p2):
    if a is None or p1 is None or p2 is None or p1['n']<20 or p2['n']<20: return 'too few trades'
    if a['av']<=0: return 'no edge'
    if p1['av']>0.05 and p2['av']>0.05: return 'PASS · edge' if (a['t'] or 0)>=2 else 'PASS · watch'
    return 'weak'
out={}
for site,m in MK.items():
    S=pd.read_parquet(f'sig_edge_{m}.parquet')
    for code,(e,stp,t,x,pair) in RULES.items():
        old=SITE[site]['sheets'][code]
        cut=pd.Timestamp(old['p2lab'][:10])
        g=S[(S.strat==code)&(S.side==1)]
        if not len(g): print(site,code,'no signals'); continue
        T=grade1.trades(m,g.tf.iloc[0],g,e,stp,t,x).sort_values('t')
        T['t']=pd.to_datetime(T.t)
        T=T[T.t>=pd.Timestamp(old['p1lab'][:10])]
        mo=T.t.dt.to_period('M'); months=max(1.0,(T.t.max()-T.t.min()).days/30.44)
        a=st(T,months); p1=st(T[T.t<cut],max(1,(cut-T.t.min()).days/30.44)); p2=st(T[T.t>=cut],max(1,(T.t.max()-cut).days/30.44))
        v=verdict(a,p1,p2)
        mr=T.groupby(mo).R.sum()
        cs=np.cumsum(T.R.values)
        sh=dict(per=[a],verdict=v,ok=v.startswith('PASS'),p1=p1,p2=p2,p1lab=old['p1lab'],p2lab=old['p2lab'],
            why=f"{v} · P1 {p1['av']:+.2f} → P2 {p2['av']:+.2f} avg RR · t {(a['t'] or 0):.1f}" if p1 and p2 else v,
            pairing=pair+' · NEW RULES (Oct 30 2026) · longs',sides=[['LONG',a]],
            months=dict(n=int(len(mr)),up=int((mr>0).sum()),worst=[str(mr.idxmin()),float(mr.min())],best=[str(mr.idxmax()),float(mr.max())]),
            curve=[[str(d.date()),round(float(c),2),'fresh'] for d,c in zip(T.t,cs)],range=[str(T.t.min().date()),str(T.t.max().date())],
            old=dict(verdict=old['verdict'],n=old['per'][-1]['n'] if old['per'][-1] else None,av=old['per'][-1]['av'] if old['per'][-1] else None,pairing=old.get('pairing')))
        out.setdefault(site,{})[code]=sh
        print(site,code,v,'| new n',a['n'],'av %.3f'%a['av'],'t',round(a['t'] or 0,2),'p1 %.3f p2 %.3f'%(p1['av'],p2['av']),'| old',old['verdict'],old['per'][-1]['n'] if old['per'][-1] else '',round(old['per'][-1]['av'],3) if old['per'][-1] else '')
json.dump(out,open('new_mk.json','w'))
