import pandas as pd, numpy as np, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim import cfg_names
from analyze import maxcons
CN=cfg_names()
G={tf:pickle.load(open(f'G_{tf}.pkl','rb')) for tf in ('1m','5m')}
RES={(per,tf):pickle.load(open(f'res_{per}_{tf}.pkl','rb')) for per in ('old','fresh') for tf in ('1m','5m')}
MONTHS={'old':36.5,'fresh':2.9}
def trades(tf,level,entry,held,filt,cfg):
    k='|'.join([level,entry,held,filt]); out={}
    c=CN.index(cfg)
    for per in ('old','fresh'):
        E,R=RES[(per,tf)]; E=E.reset_index(drop=True); idx=G[tf][k][per]
        r=R[idx,c].astype(float)
        s=cfg[0]
        dist=np.clip(np.abs(E.px.values[idx]-E.edge.values[idx])+0.25,20,50) if s=='Sbox' else np.full(len(idx),float(s[1:]))
        out[per]=pd.DataFrame({'t':E.t.values[idx],'R':r,'pts':r*dist,'dist':dist,'lvl':E.lvl.values[idx]})
    return out
def st(df,months):
    r=df.R.values; n=len(r)
    if n==0: return {}
    w=(r>0).mean(); gp=r[r>0].sum(); gl=-r[r<0].sum()
    cs=np.cumsum(r); dd=(np.maximum.accumulate(np.r_[0,cs])[1:]-cs).max()
    bw,bl=maxcons(r)
    sd=r.std(ddof=1)
    return dict(trades=n,per_month=n/months,WR=w,PF=gp/gl if gl>0 else np.inf,avgRR=r.mean(),t=r.mean()/sd*np.sqrt(n),netRR=r.sum(),
                won_usd=2*df.pts[df.pts>0].sum(),lost_usd=2*df.pts[df.pts<0].sum(),net_usd=2*df.pts.sum(),maxDD_RR=dd,max_wins=bw,max_losses=bl,avg_stop=df.dist.mean())
def full(tf,level,entry,held,filt,cfg):
    T=trades(tf,level,entry,held,filt,cfg)
    o=st(T['old'],MONTHS['old']); f=st(T['fresh'],MONTHS['fresh'])
    b=st(pd.concat([T['old'],T['fresh']]),MONTHS['old']+MONTHS['fresh'])
    return o,f,b,T
STRATS=[
 ('F.M1','5m','H1 UPG','M3 · limit at box edge','held','all',('Sbox','+box exit','TP2','trailOpp')),
 ('F.M2','5m','ALL UPG gaps','M3 · limit at box edge','any','sess: NY PM 12-16',('S50','+box exit','TP3','trailBC')),
 ('F.M3','5m','M15 UPG','M3 · limit at box edge','any','sess: NY AM 09:30-12',('Sbox','+box exit','TP2','trailBC')),
 ('F.M4','5m','NY PM OR L','M3 · limit at box edge','any','all',('S50','+box exit','TP3','trailBC')),
 ('F.M5','5m','ALL session / range H-L','M3 · limit at box edge','any','H1 trend: with',('Sbox','+box exit','TP3','trailBC')),
 ('F.M6','1m','M15 I','M3 · limit at box edge','any','sess: NY AM 09:30-12',('S20','+box exit','RUN','trailOpp')),
 ('F.M7','1m','ALL LEZ (any TF)','M3 · limit at box edge','held','sess: London 02-08',('S20','+box exit','TP2','trailOpp')),
 ('F.M8','5m','ALL UPG gaps','M3 · limit at box edge','held','all',('Sbox','+box exit','TP2','trailOpp')),
 ('F.M9','5m','ALL PRO f boxes H1','M1 B · touch, then BC','held','H1 trend: with',('Sbox','+box exit','TP5','BE1')),
]
if __name__=='__main__':
    rows=[]
    for code,tf,lv,en,hd,fl,cfg in STRATS:
        o,f,b,T=full(tf,lv,en,hd,fl,cfg)
        for per,s in (('2022–25',o),('2026',f),('Both',b)):
            rows.append(dict(code=code,ltf=tf,level=lv,entry=en,held=hd,filter=fl,stop=cfg[0],boxexit=cfg[1],target=cfg[2],trail=cfg[3],period=per,**s))
    S=pd.DataFrame(rows); S.to_parquet('strats.parquet')
    pd.set_option('display.width',300); pd.set_option('display.max_columns',40)
    print(S.drop(columns=['level','entry','held','filter','stop','boxexit','target','trail']).round(2).to_string())
