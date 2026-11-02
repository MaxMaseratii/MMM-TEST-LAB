import numpy as np, pandas as pd, json, sys, warnings; warnings.filterwarnings('ignore')
sys.path.insert(0,'.'); import bfprop
from lvagg import D, grid
def r(v,d=3):
    try:
        v=float(v); return None if not np.isfinite(v) else round(v,d)
    except: return None
def st(x):
    x=x.dropna(); n=len(x)
    if n<2: return [n,None,None,None,None]
    pos=x[x>0].sum(); neg=-x[x<=0].sum()
    return [n,r((x>0).mean()),r(x.mean()),r(pos/neg if neg>0 else np.nan,2),r(x.mean()/x.std(ddof=1)*np.sqrt(n),2)]
def row(x): return st(x[x.per=='P1'].r)+[r(x[x.per=='P1'].rr.mean())]+st(x[x.per=='P2'].r)+[r(x[x.per=='P2'].rr.mean())]
S=json.load(open('site6/summary.json'))
SS='structure (swing)'; F='fixed 1:2 (NQ 50 / ES 20 / GC 12)'
LV=[]
for m in ['NQ','ES','GC']:
  for tf in sorted(D[D.m==m].tf.unique()):
    b=D[(D.m==m)&(D.tf==tf)]; L=b[b.variant=='LEVELS']
    x=L[(L.kind=='LV')&(L.trig=='aggr')&(L.stop==SS)&(L.target=='her target')]
    x3=L[(L.kind=='LV')&(L.trig=='aggr')&(L.stop==SS)&(L.target=='3R')]
    xf=L[(L.kind=='LV')&(L.trig=='aggr')&(L.stop==F)]
    y=L[(L.kind=='LVA')&(L.trig=='aggr')&(L.stop==SS)&(L.target=='her target')]
    a=L[(L.kind=='AV')&(L.stop==SS)]
    I=b[(b.variant=='IB')&(b.stop==SS)&(b.target=='her target')]; fa=I[I.kind=='FA']; tc=I[I.kind=='TC']
    A=b[(b.variant=='ASIA')&(b.stop==SS)&(b.target=='3R')]
    hd=x[(x.lvt.isin(['pVAH','wVAH','pdH'])&(x.s==-1))|(x.lvt.isin(['pVAL','wVAL','pdL'])&(x.s==1))]
    items=[('NY levels','All her levels, aggressive reaction, next-level target',x),
      ('NY levels','A+ (2+ levels stacked), next-level target',x[x.conf>=1]),
      ('NY levels','3+ levels stacked, next-level target',x[x.conf>=2]),
      ('NY levels','A+ (2+ levels stacked), 3R target',x3[x3.conf>=1]),
      ('NY levels','A+ (2+ levels stacked), fixed 1:2',xf[xf.conf>=1]),
      ('NY levels','Her directions only (VAH / PDH short, VAL / PDL long)',hd),
      ('NY levels','Previous day high / low only',x[x.grp=='PD']),
      ('NY levels','London high / low only',x[x.grp=='LON']),
      ('NY levels','Previous session volume profile only',x[x.grp=='NYVP']),
      ('NY levels','Previous week volume profile only',x[x.grp=='WKVP']),
      ('NY levels','30m supply / demand zones only',x[x.grp=='Z30']),
      ('NY levels','60m supply / demand zones only',x[x.grp=='Z60']),
      ('NY levels','Strict zones, first touch only',x[x.grp.isin(['Z30','Z60'])&x.lvt.str.endswith('s')&x.fresh.astype(bool)]),
      ('IB + levels','Failed auction (no levels)',fa),
      ('IB + levels','Failed auction, swing into a level (her A+)',fa[fa.conf>=1]),
      ('IB + levels','Failed auction, swing into 2+ levels',fa[fa.conf>=2]),
      ('IB + levels','Trend continuation (no levels)',tc),
      ('IB + levels','Trend continuation + VWAP at IB mid',tc[tc.vwOK]),
      ('IB + levels','Trend continuation + level at IB mid',tc[tc.conf>=1]),
      ('IB + levels','Trend continuation + VWAP + level',tc[tc.vwOK&(tc.conf>=1)]),
      ('Asia + levels','All levels in Asia, aggressive, next level',y),
      ('Asia + levels','Her VP rule: opens inside value, VAH short / VAL long',y[y.inVA.astype(bool)&(((y.lvt=='pVAH')&(y.s==-1))|((y.lvt=='pVAL')&(y.s==1)))]),
      ('Asia + levels','VWAP retest after a range break, 3R',a[a.target=='3R']),
      ('Asia + levels','VWAP retest after a range break, next level',a[a.target=='her target']),
      ('Asia + levels','Tokyo sweep-fade 3R (no levels)',A[A.kind=='AF']),
      ('Asia + levels','Tokyo sweep-fade 3R + level at the sweep',A[(A.kind=='AF')&(A.conf>=1)]),
      ('Asia + levels','Tokyo breakout-retest 3R + VWAP',A[(A.kind=='AB')&A.vwOK.astype(bool)])]
    for g,lab,z in items: LV.append([m,int(tf),g,lab]+row(z))
S['levels']=LV
G=grid(D[D.variant=='LEVELS'],['m','tf','kind','grp','trig','cb','stop','target'])
G=G[(G.n1>=10)|(G.n2>=10)]
S['lvall']=[[a.m,int(a.tf),a.kind,a.grp,a.trig,a.cb,a.stop,a.target,int(a.n1),r(a.wr1),r(a.avg1),r(a.pf1,2),r(a.t1,2),r(a.rand1),int(a.n2),r(a.wr2),r(a.avg2),r(a.pf2,2),r(a.t2,2),r(a.rand2)] for a in G.itertuples()]
ok=(G.n1>=30)&(G.n2>=30); S['lvpass']=[int(ok.sum()),int((ok&(G.t1>=2)&(G.t2>=2)).sum()),int((ok&(G.rt1>=2)&(G.rt2>=2)).sum())]
# money: one trade at a time, $200 risk, stop for the day after 2 losses (counted when they close)
def money(p, m, tf, lab):
    out=[]
    p=p.copy(); p['t']=pd.to_datetime(p.te)
    p=p.sort_values(['te','tx']); keep=[]; los={}; busy=pd.Timestamp(0)
    for k,(te,tx,rr) in enumerate(zip(p.te,p.tx,p.r)):
        sd=(te+pd.Timedelta(hours=6)).normalize()
        if te < busy or los.get(sd,0)>=2: continue
        keep.append(k); busy=tx
        if rr<=0: los[sd]=los.get(sd,0)+1
    p=p.iloc[keep]
    for pp in ('P1','P2'):
        x=p[p.per==pp]
        if len(x)<5: continue
        mo=x.t.dt.to_period('M'); months=mo.nunique(); usd=x.r*200; pm=usd.groupby(mo).sum()
        T=pd.DataFrame({'t':x.t,'r':x.r,'risk':200.0}).reset_index(drop=True)
        pr=bfprop.prop(T,pv=1.0,risk_usd=200.0)
        out.append([m,int(tf),pp,len(x),r(len(x)/months,1),r((x.r>0).mean()),r(x.r.mean()),r(usd.sum()/months,0),r(pm.max(),0),r(pm.min(),0),r((pm>0).mean()),len(pr),r(pr.count('pass')/len(pr),2),lab])
    return out
M=[]
for m in ['NQ','ES','GC']:
  for tf in sorted(D[D.m==m].tf.unique()):
    b=D[(D.m==m)&(D.tf==tf)&(D.stop==SS)]
    ib=b[(b.variant=='IB')&b.kind.isin(['FA','TC'])&(b.target=='her target')]
    full=pd.concat([ib,b[(b.variant=='LEVELS')&(b.kind=='LV')&(b.trig=='aggr')&(b.conf>=1)&(b.target=='her target')],b[(b.variant=='ASIA')&(b.kind=='AF')&(b.target=='3R')]])
    M+=money(ib,m,tf,'IB setups only')+money(full,m,tf,'Full playbook')
S['money']=[z for z in M if z[-1]=='IB setups only']; S['money2']=[z for z in M if z[-1]=='Full playbook']
json.dump(S,open('site6/summary.json','w'),separators=(',',':'))
print(len(json.dumps(S))//1024,'KB', S['lvpass']); [print(z) for z in M]
