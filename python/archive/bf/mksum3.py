import numpy as np, pandas as pd, json, bfgrid3 as G
def r(v,d=3):
    try:
        v=float(v); return None if not np.isfinite(v) else round(v,d)
    except: return None
D=pd.read_parquet('grid3_all.parquet')
D['ok']=(D.n1>=30)&(D.n2>=20); D['pass']=D.ok&(D.t1>=2)&(D.t2>=2)
S={}
okD=D[D.ok]
L=okD.assign(p=(okD.r1>0)&(okD.r2>0)).groupby(['m','tf','kind'],observed=True).agg(c=('pass','size'),ps=('pass','sum'),pos=('p','mean')).reset_index()
S['bytf']=[[x.m,int(x.tf),x.kind,int(x.c),int(x.ps),r(x.pos)] for x in L.itertuples()]
cols=['m','tf','seq','slot','e','st','t','x','b','c','n1','wr1','r1','pf1','t1','n2','wr2','r2','pf2','t2']
def rows(df): return [[x.m,int(x.tf),int(x.seq),int(x.slot),int(x.e),int(x.st),int(x.t),int(x.x),int(x.b),int(x.c),int(x.n1),r(x.wr1),r(x.r1),r(x.pf1,2),r(x.t1,2),int(x.n2),r(x.wr2),r(x.r2),r(x.pf2,2),r(x.t2,2)] for x in df[cols].itertuples()]
S['passes']=rows(D[(D.kind=='cds')&D['pass']])
B=D[(D.seq==0)&(D.slot==0)]
S['bemean']=[[m,k,int(b),r(a),r(c)] for (m,k,b),(a,c) in B.groupby(['m','kind','b'],observed=True)[['r1','r2']].mean().iterrows()]
S['cxmean']=[[m,k,int(c),r(a),r(b)] for (m,k,c),(a,b) in B.groupby(['m','kind','c'],observed=True)[['r1','r2']].mean().iterrows()]
# step table
steps=[]
for m in ['NQ','ES','GC','CL']:
    O=pd.read_parquet(f'grid2_{m}.parquet'); O=O[(O.kind=='CDS/CDL')&(O.side=='both')&(O.slot=='all hours')&(O.w==0)&(O.e==0)&(O.t==0)&(O.x==0)]
    q=B[(B.m==m)&(B.e==0)&(B.t==0)&(B.x==0)]
    for st in (0,3,5,7,8):
        for tf in sorted(q.tf.unique()):
            o=O[(O.tf==tf)&(O.st==st)]
            row=[m,int(tf),st]+([r(o.r1.iloc[0]),r(o.r2.iloc[0]),r(o.wr1.iloc[0]),int(o.n1.iloc[0])] if len(o) else [None]*4)
            for k in ('cds','rnd'):
                for b,c in ((0,0),(1,0),(0,1),(1,1),(2,1)):
                    z=q[(q.kind==k)&(q.tf==tf)&(q.st==st)&(q.b==b)&(q.c==c)]
                    row+= [r(z.r1.iloc[0]),r(z.r2.iloc[0]),r(z.wr1.iloc[0]),int(z.n1.iloc[0])] if len(z) else [None]*4
            steps.append(row)
S['steps']=steps
bt=[]
C=D[D.ok&(D.kind=='cds')].assign(mt=lambda d:np.minimum(d.t1,d.t2))
R=D[(D.kind=='rnd')&(D.seq==0)&(D.slot==0)]
for (m,tf),g in C.groupby(['m','tf'],observed=True):
    x=g.sort_values('mt',ascending=False).iloc[0]
    rr=R[(R.m==m)&(R.tf==tf)&(R.e==x.e)&(R.st==(0 if x.st==1 else x.st))&(R.t==x.t)&(R.x==x.x)&(R.b==x.b)&(R.c==x.c)]
    bt.append(rows(pd.DataFrame([x]))[0]+([r(rr.r1.iloc[0]),r(rr.r2.iloc[0])] if len(rr) else [None,None]))
S['besttf']=bt
S['names']=dict(EN=G.EN,SN=G.SN,TN=G.TN,XN=G.XN,BN=G.BN,CN=G.CN,SEQ=G.SEQ,NE=G.NE,NST=G.NST,NV=G.NV)
json.dump(S,open('site3/summary.json','w'),separators=(',',':'))
print(len(json.dumps(S))//1024,'KB', len(S['passes']))
for b in bt: print(b[:10],'RR',b[12],b[17],'t',b[14],b[19],'rand',b[20],b[21])
