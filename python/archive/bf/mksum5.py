import numpy as np, pandas as pd, json, gzip, base64, bfgrid5 as G
def r(v,d=3):
    try:
        v=float(v); return None if not np.isfinite(v) else round(v,d)
    except: return None
MK=['NQ','ES','GC','CL']; TFS=[1,2,3,5,10,15,60,240]
KINDS=['FLIP (CDS / CDL)','TL touch-hold','TL break','ATR touch-hold','ATR break','PO4 touch-hold','PO4 break','old TL touch-hold','old ATR touch-hold','RANDOM side','RANDOM with trend']
SIDES=['both','long','short']
A=pd.concat([pd.read_parquet(f'grid5_{m}.parquet') for m in MK],ignore_index=True)
A['ok']=(A.n1>=30)&(A.n2>=20); A['pass']=A.ok&(A.t1>=2)&(A.t2>=2)
S={}
okA=A[A.ok]
L=okA.assign(p=(okA.r1>0)&(okA.r2>0)).groupby(['m','kind']).agg(c=('pass','size'),ps=('pass','sum'),pos=('p','mean')).reset_index()
S['luck']=[[x.m,x.kind,int(x.c),int(x.ps),r(x.pos)] for x in L.itertuples()]
key=['m','tf','side','slot','e','st','t','x']
RS=A[A.kind=='RANDOM side'][key+['r1','r2']].rename(columns={'r1':'rs1','r2':'rs2'})
RT=A[A.kind=='RANDOM with trend'][key+['r1','r2']].rename(columns={'r1':'rt1','r2':'rt2'})
P=A[A['pass']&~A.kind.str.startswith('RANDOM')].copy()
P['e0']=0
P=P.merge(RS.rename(columns={'e':'e0'}),on=['m','tf','side','slot','e0','st','t','x'],how='left').merge(RT.rename(columns={'e':'e0'}),on=['m','tf','side','slot','e0','st','t','x'],how='left')
P['mt']=np.minimum(P.t1,P.t2); P=P.sort_values('mt',ascending=False)
S['passes']=[[x.m,int(x.tf),x.kind,x.side,int(x.slot),int(x.e),int(x.st),int(x.t),int(x.x),int(x.n1),r(x.wr1),r(x.r1),r(x.pf1,2),r(x.t1,2),int(x.n2),r(x.wr2),r(x.r2),r(x.pf2,2),r(x.t2,2),r(x.rs1),r(x.rs2),r(x.rt1),r(x.rt2)] for x in P.itertuples()]
# reference trade: market entry, fixed 50 (st3), 1:2, out at next flip, all hours
q=A[(A.slot==0)&(A.e==0)&(A.st==3)&(A.t==1)&(A.x==1)]
S['ref']=[[x.m,int(x.tf),x.kind,x.side,int(x.n1),r(x.wr1),r(x.r1),r(x.t1,2),int(x.n2),r(x.wr2),r(x.r2),r(x.t2,2)] for x in q.itertuples()]
# foundation
F=pd.concat([pd.read_parquet(f'found5_{m}.parquet') for m in MK]); F=F[F.slot==0]
g=F.groupby(['m','tf','kind','per'])[['n','bc_before_opp','bc_before_nbc','p1','p5','p10','up5']].sum().reset_index()
S['found']=[[x.m,int(x.tf),x.kind,int(x.per),int(x.n),r(x.bc_before_opp/x.n if x.n else np.nan,2),r(x.bc_before_nbc/x.n if x.n else np.nan,2),r(x.p1/x.n if x.n else np.nan,2),r(x.p5/x.n if x.n else np.nan,2),r(x.p10/x.n if x.n else np.nan,2),r(x.up5/x.n if x.n else np.nan,3)] for x in g.itertuples()]
S['names']=dict(EN=G.EN,SN=G.SN,TN=G.TN,XN=G.XN,KINDS=KINDS,SIDES=SIDES,TFS=TFS)
json.dump(S,open('site5/summary.json','w'),separators=(',',':'))
print(len(json.dumps(S))//1024,'KB',len(S['passes']))
# explorer data: per market, cube [tf8, kind11, side3, slot2, e3, st8, t6, x4, per2] -> n uint32, wr/r/t int16
for m in MK:
    D=A[A.m==m]
    shape=(8,11,3,2,G.NE,G.NST,G.NT,G.NX)
    idx=np.ravel_multi_index((D.tf.map({t:i for i,t in enumerate(TFS)}).values,D.kind.map({k:i for i,k in enumerate(KINDS)}).values,D.side.map({s:i for i,s in enumerate(SIDES)}).values,D.slot.values,D.e.values,D.st.values,D.t.values,D.x.values),shape)
    N=int(np.prod(shape)); n=np.zeros((N,2),np.uint32); n[idx,0]=D.n1.values; n[idx,1]=D.n2.values
    def sc(a,f): return np.clip(np.round(np.nan_to_num(np.asarray(a,float)*f,nan=0,posinf=32767,neginf=-32767)),-32767,32767).astype(np.int16)
    qv=np.zeros((N,2,3),np.int16)
    for p,(w,rr,t) in enumerate((('wr1','r1','t1'),('wr2','r2','t2'))):
        qv[idx,p,0]=sc(D[w].values,1e4); qv[idx,p,1]=sc(D[rr].values,1e3); qv[idx,p,2]=sc(D[t].values,100)
    raw=n.tobytes()+qv.tobytes(); b=base64.b64encode(gzip.compress(raw,9)); open(f'site5/{m}.txt','wb').write(b); print(m,len(raw)//1e6,'MB raw',len(b)//1e6,'MB b64')
