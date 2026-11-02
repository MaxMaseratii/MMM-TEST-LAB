"""09:30-11:30 window profile: when the high/low is made, range, the 09:30 candle (5m/15m), the 09:30-10:00 opening range break."""
import numpy as np, pandas as pd, json
from common import raw, good_days, ctype, lean, family, pct, med, q
OUT={}
for key in ('old','fresh'):
    d1=raw()[key]; days=good_days(d1); rows=[]; oc={'5m':[], '15m':[]}; orr=[]
    for day in days:
        a=day+pd.Timedelta(hours=9,minutes=30); z=day+pd.Timedelta(hours=11,minutes=29)
        w=d1.loc[a:z]
        if len(w)<110: continue
        H=w.high.values; L=w.low.values; C=w.close.values; O=w.open.values; t=((w.index-a).total_seconds()//60).astype(int)
        ih=int(np.argmax(H)); il=int(np.argmin(L))
        rows.append(dict(rng=H.max()-L.min(), hb=t[ih]//15, lb=t[il]//15, up=C[-1]>O[0], move=C[-1]-O[0], first_hi=ih<il))
        # 09:30 candles (prev = the candle before 09:30 of same TF)
        for tf,m in (('5m',5),('15m',15)):
            pv=d1.loc[a-pd.Timedelta(minutes=m):a-pd.Timedelta(minutes=1)]
            if len(pv)<m: continue
            cd=w.iloc[:m]; nx=w.iloc[m:2*m]
            o,h,l,c=cd.open.iloc[0],cd.high.max(),cd.low.min(),cd.close.iloc[-1]
            T=ctype(o,h,l,c,pv.high.max(),pv.low.min()); dl=1 if lean(T)=='bull' else -1
            tg=h if dl==1 else l; pr=l if dl==1 else h
            rest=w.iloc[m:]
            it=np.flatnonzero(rest.high.values>=tg) if dl==1 else np.flatnonzero(rest.low.values<=tg)
            ip=np.flatnonzero(rest.low.values<=pr) if dl==1 else np.flatnonzero(rest.high.values>=pr)
            nt=np.flatnonzero(nx.high.values>=tg) if dl==1 else np.flatnonzero(nx.low.values<=tg)
            npr=np.flatnonzero(nx.low.values<=pr) if dl==1 else np.flatnonzero(nx.high.values>=pr)
            oc[tf].append(dict(T=T,fam=family(T),lean=dl,
                next_tgt_first=len(nt)>0 and (len(npr)==0 or nt[0]<npr[0]),
                tgt_by1130=len(it)>0, prot_by1130=len(ip)>0, tgt_before_prot=len(it)>0 and (len(ip)==0 or it[0]<ip[0]),
                close1130_lean=(C[-1]-c)*dl>0, pts1130=(C[-1]-c)*dl,
                mfe=((rest.high.max()-c) if dl==1 else (c-rest.low.min())), mae=((c-rest.low.min()) if dl==1 else (rest.high.max()-c))))
        # opening range 09:30-09:59
        orh=H[:30].max(); orl=L[:30].min(); r2=w.iloc[30:]
        bu=np.flatnonzero(r2.close.values>orh); be=np.flatnonzero(r2.close.values<orl)
        first=None
        if len(bu) and (not len(be) or bu[0]<be[0]): first=1
        elif len(be): first=-1
        cont=None
        if first is not None:
            k=(bu if first==1 else be)[0]; lvl=orh if first==1 else orl; seg=r2.iloc[k:]
            ext=(seg.high.max()-lvl) if first==1 else (lvl-seg.low.min())
            back=np.flatnonzero(seg.close.values<orl) if first==1 else np.flatnonzero(seg.close.values>orh)
            cont=dict(ext=ext, other_side=len(back)>0, end_with=((C[-1]-lvl)*first)>0)
        orr.append(dict(rng=orh-orl, first=first, both=len(bu)>0 and len(be)>0, none=first is None, **({} if cont is None else cont)))
    R=pd.DataFrame(rows); res={}
    res['days']=len(R); res['range']=dict(med=med(list(R.rng)),p25=q(list(R.rng),25),p75=q(list(R.rng),75))
    res['up%']=pct(R.up.sum(),len(R)); res['high_first%']=pct(R.first_hi.sum(),len(R))
    lab=['09:30','09:45','10:00','10:15','10:30','10:45','11:00','11:15']
    res['high_when']=[pct((R.hb==i).sum(),len(R)) for i in range(8)]; res['low_when']=[pct((R.lb==i).sum(),len(R)) for i in range(8)]
    res['either_by_1000%']=pct(((R.hb<2)|(R.lb<2)).sum(),len(R)); res['both_after_1000%']=pct(((R.hb>=2)&(R.lb>=2)).sum(),len(R))
    for tf in oc:
        X=pd.DataFrame(oc[tf]); tab=[]
        for nm,Y in [('ALL',X)]+[(f,X[X.fam==f]) for f in ['BC+','BC-','C2','AFs','CI','S&D']]:
            if not len(Y): continue
            tab.append(dict(key=nm,n=len(Y),share=pct(len(Y),len(X)),next_tgt_first=pct(Y.next_tgt_first.sum(),len(Y)),tgt_by1130=pct(Y.tgt_by1130.sum(),len(Y)),
                prot_by1130=pct(Y.prot_by1130.sum(),len(Y)),tgt_before_prot=pct(Y.tgt_before_prot.sum(),len(Y)),close_lean=pct(Y.close1130_lean.sum(),len(Y)),
                pts_med=med(list(Y.pts1130)),mfe_med=med(list(Y.mfe)),mae_med=med(list(Y.mae))))
        res['open_'+tf]=tab
    O_=pd.DataFrame(orr)
    br=O_[~O_.none].copy()
    for c_ in ('other_side','end_with'): br[c_]=br[c_].astype(float).fillna(0).astype(bool)
    res['or']=dict(n=len(O_),rng_med=med(list(O_.rng)),broke=pct(len(br),len(O_)),first_up=pct((br['first']==1).sum(),len(O_)),first_dn=pct((br['first']==-1).sum(),len(O_)),
        both=pct(O_.both.sum(),len(O_)),none=pct(O_.none.sum(),len(O_)),ext_med=med(list(br.ext)),ext_p75=q(list(br.ext),75),
        other_side=pct(br.other_side.sum(),len(br)),end_with=pct(br.end_with.sum(),len(br)))
    OUT[key]=res
json.dump(OUT,open('q8.json','w'),indent=1); print(json.dumps({k:v['or'] for k,v in OUT.items()},indent=1))
