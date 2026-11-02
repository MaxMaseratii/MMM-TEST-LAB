"""Q5: open UPG gaps on the opposite side of the 10:00 candle target. Q6: runs from 10:00 to 11:30 until an 'opposite candle'."""
import numpy as np, pandas as pd, json
from common import raw, good_days, bars, lean, family, rs, pct, med, q, mean
OUT={}
def gaps_of(b):
    """UPG list on bars b: (formed_time_end, dir, lo, hi)"""
    H,L,C=b.high.values,b.low.values,b.close.values; idx=b.index; out=[]
    for i in range(2,len(b)):
        if C[i-1]>H[i-2] and L[i]>H[i-2]: out.append((idx[i],1,H[i-2],L[i]))
        if C[i-1]<L[i-2] and H[i]<L[i-2]: out.append((idx[i],-1,H[i],L[i-2]))
    return out
TFM={'5m':5,'15m':15,'1h':60,'4h':240}
for key in ('old','fresh'):
    d1=raw()[key]; days=good_days(d1); dset=set(days)
    one=d1
    B={tf:bars(key,tf) for tf in TFM}
    G={tf:gaps_of(rs(d1,tf)) for tf in ('5m','15m','1h','4h')}
    # index gaps per session day (18:00 start)
    res5={}
    for tf,mins in TFM.items():
        b=B[tf]; lab=pd.Timestamp('06:00').time() if tf=='4h' else (pd.Timestamp('10:00')-pd.Timedelta(minutes=mins)).time()
        rows=[]
        for day in days:
            t0=pd.Timestamp.combine(day.date(),lab)
            if t0 not in b.index: continue
            r=b.loc[t0]; ln=lean(r.type); d=1 if ln=='bull' else -1
            tgt=r.high if d==1 else r.low
            sess0=pd.Timestamp.combine(day.date(),pd.Timestamp('00:00').time())-pd.Timedelta(hours=6)
            end_t=pd.Timestamp.combine(day.date(),pd.Timestamp('11:29').time())
            path=one.loc[pd.Timestamp.combine(day.date(),pd.Timestamp('10:00').time()):end_t]
            if len(path)<30: continue
            ten=pd.Timestamp.combine(day.date(),pd.Timestamp('10:00').time())
            # open gaps on opposite side: from gaps of this TF and 5m, formed since 18:00, end before 10:00, untouched until 10:00, fully on the far side of the 10:00 close
            best=None
            for gtf in sorted({tf,'5m'}):
                for (gt,gd,lo,hi) in G[gtf]:
                    gend=gt+pd.Timedelta(minutes=TFM[gtf])
                    if gt<sess0 or gend>ten: continue
                    seg=one.loc[gend:ten-pd.Timedelta(minutes=1)]
                    if len(seg) and ((seg.low.min()<=hi) and (seg.high.max()>=lo)): continue   # touched already
                    if d==1 and hi<r.close: dist=r.close-hi
                    elif d==-1 and lo>r.close: dist=lo-r.close
                    else: continue
                    if best is None or dist<best[0]: best=(dist,gtf,gd,lo,hi)
            # outcomes until 11:30 on 1m path: target first vs gap touched first
            hitT=np.flatnonzero((path.high.values>=tgt) if d==1 else (path.low.values<=tgt))
            ti=hitT[0] if len(hitT) else None
            rec=dict(day=str(day.date()),type=r.type,fam=family(r.type),lean=ln,has=best is not None,tgt_hit=ti is not None)
            if best:
                dist,gtf,gd,lo,hi=best
                hitG=np.flatnonzero((path.low.values<=hi) if d==1 else (path.high.values>=lo))
                gi=hitG[0] if len(hitG) else None
                rec.update(gtf=gtf,gdist=round(dist,2),gap_hit=gi is not None,gap_first=(gi is not None and (ti is None or gi<ti)),
                           tgt_first=(ti is not None and (gi is None or ti<gi)),
                           tgt_after_gap=(gi is not None and ti is not None and ti>gi), same_dir=(gd==d))
            rows.append(rec)
        R=pd.DataFrame(rows); res5[tf]=R
    OUT[key]=dict(q5=res5)
    # Q6
    res6={}
    for tf in ('1m','5m','15m'):
        b=bars(key,tf) if tf!='1m' else None
        if tf=='1m':
            b=d1.copy(); b['pH']=b.high.shift(); b['pL']=b.low.shift(); b=b.dropna()
            from common import ctype
            b['bc']=np.where(b.close>b.pH,1,np.where(b.close<b.pL,-1,0))
        rows=[]
        mins={'1m':1,'5m':5,'15m':15}[tf]
        B10=B['5m'] if False else None
        for day in days:
            a=pd.Timestamp.combine(day.date(),pd.Timestamp('10:00').time()); z=pd.Timestamp.combine(day.date(),pd.Timestamp('11:30').time())-pd.Timedelta(minutes=mins)
            seg=b.loc[a:z]
            if len(seg)<3: continue
            O,H,L,C,BC=seg.open.values,seg.high.values,seg.low.values,seg.close.values,seg.bc.values
            # start = the first BC at or after 10:00 (bar opening 10:00 onward)
            st=np.flatnonzero(BC!=0)
            if not len(st): continue
            s=st[0]; d=BC[s]
            # 10:00-closing candle of this TF (context)
            prev=b.loc[:a-pd.Timedelta(minutes=1)].iloc[-1] if tf!='1m' else None
            for mode in ('opp BC','close past BC open','close past BC low'):
                tO,tL=O[s],L[s] if d==1 else H[s]; nbc=0; same=1; oppnoend=0; best=C[s]; endi=None
                for k in range(s+1,len(seg)):
                    if d==1: best=max(best,H[k])
                    else: best=min(best,L[k])
                    if mode=='opp BC': end = BC[k]==-d
                    elif mode=='close past BC open': end = (C[k]<tO) if d==1 else (C[k]>tO)
                    else: end = (C[k]<tL) if d==1 else (C[k]>tL)
                    if end: endi=k; break
                    if BC[k]==d: same+=1; tO=O[k]; tL=L[k] if d==1 else H[k]
                    elif BC[k]==0: nbc+=1
                    else: oppnoend+=1
                fin=endi if endi is not None else len(seg)-1
                rows.append(dict(day=str(day.date()),mode=mode,dir=d,start_min=int((seg.index[s]-a).total_seconds()//60),same=same,nbc=nbc,opp_inside=oppnoend,
                    mfe=round((best-C[s])*d,2),endpts=round((C[fin]-C[s])*d,2),alive=endi is None,mins=int((seg.index[fin]-seg.index[s]).total_seconds()//60)+mins,
                    prev_type=(prev.type if prev is not None else None)))
        res6[tf]=pd.DataFrame(rows)
    OUT[key]['q6']=res6
import pickle; pickle.dump(OUT,open('q56.pkl','wb'))
# ---- print summaries
pd.set_option('display.width',250); pd.set_option('display.max_rows',200)
for tf in TFM:
    print('Q5',tf)
    for key in ('old','fresh'):
        R=OUT[key]['q5'][tf]; Rb=R[R.fam.isin(['BC+','C2'])]
        def s(X):
            g=X[X.has]; ng=X[~X.has]
            return dict(n=len(X),has_gap=pct(len(g),len(X)),tgt_hit_with_gap=pct(g.tgt_hit.sum(),len(g)),tgt_hit_no_gap=pct(ng.tgt_hit.sum(),len(ng)),
                gap_first=pct(g.gap_first.sum(),len(g)) if len(g) else None,tgt_first=pct(g.tgt_first.sum(),len(g)) if len(g) else None,
                tgt_after_gap_of_gapfirst=pct(g.tgt_after_gap.sum(),g.gap_first.sum()) if len(g) and g.gap_first.sum() else None,med_gap_dist=med(list(g.gdist)) if len(g) else None)
        print(' ',key,'ALL',s(R)); print(' ',key,'BC+/C2',s(Rb)); print(' ',key,'other',s(R[~R.fam.isin(['BC+','C2'])]))
for tf in ('1m','5m','15m'):
    for key in ('old','fresh'):
        R=OUT[key]['q6'][tf]
        g=R.groupby('mode').agg(n=('same','size'),same_avg=('same','mean'),same_med=('same','median'),nbc_avg=('nbc','mean'),opp_in=('opp_inside','mean'),mfe_med=('mfe','median'),mfe75=('mfe',lambda x:x.quantile(.75)),end_med=('endpts','median'),alive=('alive','mean'),mins=('mins','median'))
        print('Q6',tf,key); print(g.round(2).to_string())
