"""MMCB odds per candle type: what the NEXT candle does (all sessions)."""
import numpy as np, pandas as pd, json
from common import raw, bars, lean, TYPES
OUT={}
for key in ('old','fresh'):
    m1=raw()[key]; t1=m1.index.values; H1=m1.high.values; L1=m1.low.values
    for tf,mins in (('5m',5),('15m',15),('1h',60),('4h',240)):
        b=bars(key,tf)
        ty=b.type.values; H=b.high.values; L=b.low.values; C=b.close.values; O=b.open.values; idx=b.index.values
        nxtH=np.r_[H[1:],np.nan]; nxtL=np.r_[L[1:],np.nan]; nxtC=np.r_[C[1:],np.nan]
        # contiguous: next bar starts within 1 bar length (skip weekend/holiday gaps)
        gap=np.r_[(idx[1:]-idx[:-1]).astype('timedelta64[m]').astype(int),9999]
        ok=gap<=mins
        # 1m positions for first-touch order
        st=np.searchsorted(t1,np.r_[idx[1:],idx[-1]]); en=np.searchsorted(t1,np.r_[idx[1:],idx[-1]]+np.timedelta64(mins,'m'))
        rows={}
        for T in TYPES:
            d=1 if lean(T)=='bull' else -1
            sel=np.flatnonzero((ty==T)&ok)
            if not len(sel): continue
            tg=np.where(d==1,H[sel],L[sel]); pr=np.where(d==1,L[sel],H[sel])
            hitT=(nxtH[sel]>=tg) if d==1 else (nxtL[sel]<=tg)
            hitP=(nxtL[sel]<=pr) if d==1 else (nxtH[sel]>=pr)
            # next close side vs this candle
            bcw=(nxtC[sel]>H[sel]) if d==1 else (nxtC[sel]<L[sel]); bca=(nxtC[sel]<L[sel]) if d==1 else (nxtC[sel]>H[sel])
            # open/50% retest before TGT? use 1m: first TGT touch vs first touch of 50%
            mid=(H[sel]+L[sel])/2
            tfirst=0; both=0; midb=0; openb=0
            for k,i in enumerate(sel):
                a,z=st[i],en[i]
                if z<=a: continue
                hh=H1[a:z]; ll=L1[a:z]
                if d==1:
                    it=np.flatnonzero(hh>=tg[k]); ip=np.flatnonzero(ll<=pr[k]); im=np.flatnonzero(ll<=mid[k]); io=np.flatnonzero(ll<=O[i])
                else:
                    it=np.flatnonzero(ll<=tg[k]); ip=np.flatnonzero(hh>=pr[k]); im=np.flatnonzero(hh>=mid[k]); io=np.flatnonzero(hh>=O[i])
                if len(it) and len(ip): both+=1
                if len(it) and (not len(ip) or it[0]<ip[0]): tfirst+=1
                if len(im) and (not len(it) or im[0]<it[0]): midb+=1
                if len(io) and (not len(it) or io[0]<it[0]): openb+=1
            n=len(sel); r=lambda x: round(100*x/n,1)
            rows[T]=dict(n=n,tgt=r(hitT.sum()),prot=r(hitP.sum()),tgt_first=r(tfirst),both=r(both),neither=r((~hitT&~hitP).sum()),
                bc_with=r(bcw.sum()),bc_against=r(bca.sum()),nbc=r(n-bcw.sum()-bca.sum()),mid_before=r(midb),open_before=r(openb))
        OUT[f'{key}|{tf}']=rows
        print(key,tf,{k:(v['n'],v['tgt'],v['prot'],v['tgt_first'],v['bc_with']) for k,v in rows.items()})
json.dump(OUT,open('odds.json','w'))
