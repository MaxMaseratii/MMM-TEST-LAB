import numpy as np, pandas as pd, json, gzip, bfgrid2 as G
TFS=[1,2,3,5,10,15,60,240]; KINDS=['CDS/CDL','RANDOM side','RANDOM with trend']; SIDES=['both','long','short']; SLOTS=['all hours','09:45-12:00']
shape=(3,8,3,2,G.NW,G.NE,G.NST,G.NT,G.NX)
def r(v,d=3):
    try:
        v=float(v); return None if not np.isfinite(v) else round(v,d)
    except: return None
allD=[]; sizes={}
for m in ['NQ','ES','GC','CL']:
    D=pd.read_parquet(f'grid2_{m}.parquet'); allD.append(D)
    k=D.kind.map({k:i for i,k in enumerate(KINDS)}).values; tf=D.tf.map({t:i for i,t in enumerate(TFS)}).values
    sd=D.side.map({s:i for i,s in enumerate(SIDES)}).values; sl=D.slot.map({s:i for i,s in enumerate(SLOTS)}).values
    idx=np.ravel_multi_index((k,tf,sd,sl,D.w.values,D.e.values,D.st.values,D.t.values,D.x.values),shape)
    N=int(np.prod(shape))
    n=np.zeros((N,2),np.int32); n[idx,0]=D.n1.values; n[idx,1]=D.n2.values
    q=np.zeros((N,8),np.int16)
    def sc(a,f,lim=32767):
        a=np.nan_to_num(np.asarray(a,float)*f,nan=0,posinf=lim,neginf=-lim); return np.clip(np.round(a),-lim,lim).astype(np.int16)
    for j,(c,f) in enumerate([('wr1',1e4),('r1',1e3),('pf1',100),('t1',100),('wr2',1e4),('r2',1e3),('pf2',100),('t2',100)]): q[idx,j]=sc(D[c].values,f)
    raw=n.tobytes()+q.tobytes()
    open(f'site2/{m}.bin','wb').write(raw); sizes[m]=(len(raw),len(gzip.compress(raw)))
print(sizes)
A=pd.concat(allD,ignore_index=True)
A['pass']=(A.t1>=2)&(A.t2>=2)&(A.n1>=30)&(A.n2>=20)
S={}
B=A[(A.n1>=30)&(A.n2>=20)]
L=B.assign(p=(B.r1>0)&(B.r2>0)).groupby(['m','kind']).agg(cells=('pass','size'),passes=('pass','sum'),pos=('p','mean')).reset_index()
S['luck']=[[x.m,x.kind,int(x.cells),int(x.passes),r(x.pos)] for x in L.itertuples()]
cols=['m','tf','side','slot','w','e','st','t','x','n1','wr1','r1','pf1','t1','n2','wr2','r2','pf2','t2']
def rows(df): return [[x.m,int(x.tf),x.side,x.slot,int(x.w),int(x.e),int(x.st),int(x.t),int(x.x),int(x.n1),r(x.wr1),r(x.r1),r(x.pf1,2),r(x.t1,2),int(x.n2),r(x.wr2),r(x.r2),r(x.pf2,2),r(x.t2,2)] for x in df[cols].itertuples()]
S['passes']=rows(A[(A.kind=='CDS/CDL')&A['pass']])
S['passesR']=[[k]+rw for k in KINDS[1:] for rw in rows(A[(A.kind==k)&A['pass']].assign(mt=lambda d: np.minimum(d.t1,d.t2)).sort_values('mt',ascending=False).head(15))]
q=A[(A.side=='both')&(A.w==0)&(A.slot=='all hours')]
S['stops']=[[m,st]+[r(v) for v in vals] for (m,st),vals in q.groupby(['m','st']).apply(lambda g: [g[g.kind==k][c].mean() for k in KINDS for c in ('r1','r2')]).items()]
S['exits']=[[m,t,x]+[r(v) for v in vals] for (m,t,x),vals in q.groupby(['m','t','x']).apply(lambda g: [g[g.kind==k][c].mean() for k in KINDS for c in ('r1','r2')]).items()]
# entry family means per market (CDS only, PO4 last except 100% C1, any stop): mean avg RR by entry
q2=A[(A.kind=='CDS/CDL')&(A.side=='both')&(A.w==0)&(A.slot=='all hours')&(A.x==0)]
S['entries']=[[m,e]+[r(v) for v in vals] for (m,e),vals in q2.groupby(['m','e']).apply(lambda g: [g.r1.mean(),g.r2.mean(),g.n1.mean()/max(1,g[g.e==0].n1.mean() if False else 1)]).items()]
# fill rate: n of entry / n of market, NQ 15m, PO4? use ATR x1 (st3) 1:2 both all hours wait10 & wait30
fr=[]
for m in ['NQ','ES','GC','CL']:
    for w in (0,1):
        g=A[(A.m==m)&(A.kind=='CDS/CDL')&(A.side=='both')&(A.slot=='all hours')&(A.w==w)&(A.st==3)&(A.t==0)&(A.x==0)]
        base=g[g.e==0].groupby('tf').n1.sum()
        for e in range(G.NE):
            ge=g[g.e==e].groupby('tf').n1.sum()
            fr.append([m,w,e,r((ge/base).mean())])
S['fill']=fr
S['names']=dict(EN=G.EN,SN=G.SN,TN=G.TN,XN=G.XN,WN=G.WN,TFS=TFS,KINDS=KINDS,SIDES=SIDES,SLOTS=SLOTS,shape=list(shape))
json.dump(S,open('site2/summary.json','w'),separators=(',',':'))
print(len(json.dumps(S))//1024,'KB summary', len(S['passes']), len(S['passesR']))
# per chart
okA=A[(A.n1>=30)&(A.n2>=20)]
T=okA.assign(p=lambda d:(d.r1>0)&(d.r2>0)).groupby(['m','tf','kind']).agg(c=('pass','size'),ps=('pass','sum'),pos=('p','mean')).reset_index()
S['bytf']=[[x.m,int(x.tf),x.kind,int(x.c),int(x.ps),r(x.pos)] for x in T.itertuples()]
C=okA[okA.kind=='CDS/CDL'].assign(mt=lambda d:np.minimum(d.t1,d.t2))
bt=[]
for (m,tf),g in C.groupby(['m','tf']):
    for lab,gg in (('any stop',g),('fixed stop',g[g.st>=6])):
        if len(gg)==0: continue
        x=gg.sort_values('mt',ascending=False).iloc[0]
        rr=A[(A.m==m)&(A.tf==tf)&(A.kind=='RANDOM side')&(A.side==x.side)&(A.slot==x.slot)&(A.w==x.w)&(A.e==x.e)&(A.st==(0 if x.st==1 else x.st))&(A.t==x.t)&(A.x==x.x)]
        bt.append([lab]+rows(pd.DataFrame([x]))[0]+([r(rr.r1.iloc[0]),r(rr.r2.iloc[0])] if len(rr) else [None,None]))
S['besttf']=bt
json.dump(S,open('site2/summary.json','w'),separators=(',',':'))
print('besttf',len(bt), 'passes', len(S['passes']))
