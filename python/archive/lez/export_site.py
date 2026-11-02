import numpy as np, pandas as pd, pickle, json, sys
sys.path.insert(0,'/home/claude/lez')
import final, final2
from sim2 import cfg_names2
from sim3 import cfg3
from analyze import maxcons
CN2=cfg_names2(); CN3=cfg3()
T={}
for code,tf,lv,en,hd,fl,cfg in final.STRATS:
    T[code]=final.trades(tf,lv,en,hd,fl,cfg)
def full2(src,tf,key,cfg):
    G=pickle.load(open(final2.GF[src].format(tf),'rb')); c=CN2.index(cfg); out={}
    for per in ('old','fresh'):
        E,R=final2.load_res(src,per,tf); E=E.reset_index(drop=True); idx=G[per][key]
        r=R[idx,c].astype(float); px=E.px.values[idx]; ed=E.edge.values[idx]; s=cfg[0]
        dist=np.clip(np.abs(px-ed)+0.25,20,50) if s=='Sbox' else (np.maximum(np.abs(px-ed)+0.25,10) if s=='Szone' else np.full(len(idx),float(s[1:])))
        out[per]=pd.DataFrame({'t':E.t.values[idx],'R':r,'pts':r*dist,'dist':dist})
    return out
for code,src,tf,key,cfg,lvl,ent in final2.S2: T[code]=full2(src,tf,key,cfg)
# FVA.M16
G=pickle.load(open('G3_5m.pkl','rb')); c=CN3.index(('Sbox','RUN','BE+fees after 1 BC','3 re-entries')); out={}
for per in ('old','fresh'):
    E,_=pickle.load(open(f'res2_{per}_5m.pkl','rb')); R,NT,PT=pickle.load(open(f'res3_{per}_5m.pkl','rb'))
    idx=G[per]['H1 UPG|2 BCs (validated) then retest|all seq|A1 next open|held|all']
    out[per]=pd.DataFrame({'t':E.t.values[idx],'R':R[idx,c].astype(float),'pts':PT[idx,c].astype(float),'dist':np.clip(np.abs(E.px.values[idx]-np.where(E.d.values[idx]==1,E.bot.values[idx],E.top.values[idx]))+0.25,20,50)})
T['FVA.M16']=out
# FVA.M17-22 (same as final4)
src=open('final4.py').read(); S4=eval(src[src.index('S=[')+2:src.index(']\nrows=[]')+1])
for code,tf,key,kind,cfg in S4:
    G=pickle.load(open(f'G7_{tf}.pkl','rb')); out={}
    for per in ('old','fresh'):
        E,Rm,R3,NT,PT,_=pickle.load(open(f'res4_{per}_{tf}.pkl','rb')); idx=G[per][key]
        raw=np.abs(E.px.values[idx]-E.edge.values[idx])+0.25; s=cfg[0]
        if kind=='s2':
            r=Rm[idx,CN2.index(cfg)].astype(float)
            dist=np.full(len(idx),float(s[1:])) if s[1:].isdigit() else (np.clip(raw,20,50) if s=='Sbox' else np.maximum(raw,10))
            out[per]=pd.DataFrame({'t':E.t.values[idx],'R':r,'pts':r*dist,'dist':dist})
        else:
            cc=CN3.index(cfg); dist=np.full(len(idx),float(s[1:])) if s[1:].isdigit() else np.clip(raw,20,50)
            out[per]=pd.DataFrame({'t':E.t.values[idx],'R':R3[idx,cc].astype(float),'pts':PT[idx,cc].astype(float),'dist':dist})
    T[code]=out
def tstat(r): return float(r.mean()/r.std(ddof=1)*np.sqrt(len(r))) if len(r)>2 and r.std(ddof=1)>0 else 0.0
res={}
for code,d in T.items():
    o=d['old'].dropna(subset=['R']).sort_values('t'); f=d['fresh'].dropna(subset=['R']).sort_values('t')
    o['p']=0; f['p']=1; b=pd.concat([o,f]); r=b.R.values; usd=2*b.pts.values
    eq=np.cumsum(usd); dd=float((np.maximum.accumulate(np.r_[0,eq])[1:]-eq).max())
    gp=r[r>0].sum(); gl=-r[r<0].sum(); mw,ml=maxcons(r)
    cs=np.cumsum(r); n=len(r); idx=np.unique(np.linspace(0,n-1,min(220,n)).round().astype(int))
    # make sure the first period-2 point is included
    k=np.flatnonzero(b.p.values==1)
    if len(k): idx=np.unique(np.r_[idx,k[0]])
    curve=[[str(pd.Timestamp(b.t.values[i]).date()),round(float(cs[i]),2),int(b.p.values[i])] for i in idx]
    res[code]=dict(all=dict(n=int(n),tpm=round(n/39.4,1),wr=round(float((r>0).mean()),3),av=round(float(r.mean()),3),pf=round(float(gp/gl),2) if gl>0 else 99,t=round(tstat(r),2),
                   net=int(round(usd.sum())),dd=int(round(dd)),ml=int(ml),mw=int(mw),risk=round(float(b.dist.mean()),1),full_loss=round(float((r<=-0.9).mean()),3)),
        p1=dict(n=int(len(o)),av=round(float(o.R.mean()),3),t=round(tstat(o.R.values),2),wr=round(float((o.R>0).mean()),3)),
        p2=dict(n=int(len(f)),av=round(float(f.R.mean()),3),t=round(tstat(f.R.values),2),wr=round(float((f.R>0).mean()),3)),curve=curve)
    a=res[code]['all']; print(code,a['n'],a['wr'],a['av'],a['pf'],a['t'],a['net'],res[code]['p1']['av'],res[code]['p2']['av'],res[code]['p2']['n'])
json.dump(res,open('site_fm.json','w'))
