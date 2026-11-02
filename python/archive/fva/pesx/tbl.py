import pandas as pd, numpy as np
h=pd.read_parquet('../grid_h/merged.parquet'); i=pd.read_parquet('../grid_i/merged.parquet')
i=i[i.entry.isin(['market at close'])|i.type.str.contains('RT')]
d=pd.concat([h.assign(src='h'),i.assign(src='i')],ignore_index=True)
EV={'PES/PEL+':'① PES+/PEL+ touch (limit at the zone)','Nest PES/PEL(+)':'② Nested PES/PEL(+) touch','FlipBC':'③ The flip BC itself (BC breaks the opposite BC)','Rej Zone':'④ Rejection: wick into the zone, close back out','G3 Zone':'⑤ Grey-phase rejection','Sig Zone':'⑥ Nested zone breakout','Fail+C RT':'⑦ Zone broken, limit back at the edge','Fail+C':'⑧ Zone FAIL: close through it, trade the break','RANDOM':'RANDOM (luck check)'}
d=d[d.type.isin(EV)]
def comb(r):
    n=r.n_o+r.n_n; s=r.s_o+r.s_n; s2=r.s2_o+r.s2_n; a=s/n
    sd=np.sqrt(np.maximum((s2-n*a*a)/(n-1),1e-12)); return n,(r.w_o+r.w_n)/n,a,(r.gw_o+r.gw_n)/np.maximum(r.gl_o+r.gl_n,1e-9),a/sd*np.sqrt(n)
d=d.copy(); d['N'],d['WR'],d['AV'],d['PF'],d['TS']=comb(d)
# fixed table
f=d[(d.side=='both')&(d.session=='All')&(d.stop=='S0 fixed 50')&(d.target=='1:2')&(d.exit=='X0 none')]
f=f.drop_duplicates(['tf','type'])
rows=[]
for tf in ['5m','15m','1h','4h']:
    for ty in EV:
        x=f[(f.tf==tf)&(f.type==ty)]
        if len(x)==0: continue
        r=x.iloc[0]
        rows.append(dict(tf=tf,ev=EV[ty],n=int(r.N),tpm=r.N/40.8,wr=r.WR,av=r.AV,pf=r.PF,t=r.TS,av_o=r.avgR_o,av_n=r.avgR_n))
F=pd.DataFrame(rows); F.to_csv('fixed.csv',index=False)
# pass rate & best per tf/type
rows=[]
for (tf,ty),g in d.groupby(['tf','type']):
    ok=g[(g.n_o>=100)&(g.n_n>=30)]
    pr=g.PASS.mean()*100
    b=ok[(ok.avgR_o>0)&(ok.avgR_n>0)].sort_values('TS',ascending=False).head(1)
    if len(b): b=b.iloc[0]; rows.append(dict(tf=tf,ev=EV[ty],combos=len(g),passpct=pr,npass=int(g.PASS.sum()),best=f"{b.side} · {b.session} · {b.stop[3:]} · {b.target} · {b.exit.split(' ',1)[1]}",n=int(b.N),wr=b.WR,av=b.AV,pf=b.PF,t=b.TS,t_o=b.t_o,t_n=b.t_n,av_o=b.avgR_o,av_n=b.avgR_n))
    else: rows.append(dict(tf=tf,ev=EV[ty],combos=len(g),passpct=pr,npass=int(g.PASS.sum())))
B=pd.DataFrame(rows); B['o']=B.tf.map({'5m':0,'15m':1,'1h':2,'4h':3}); B=B.sort_values(['o','ev']); B.to_csv('best.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_columns',30); pd.set_option('display.max_colwidth',70)
print(F.round(2).to_string()); print(B.drop(columns='o').round(2).to_string())
