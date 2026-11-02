import numpy as np, pandas as pd, json, bfgrid4 as G
def r(v,d=3):
    try:
        v=float(v); return None if not np.isfinite(v) else round(v,d)
    except: return None
BASE=['m','tf','kind','seq','slot','e','st','t','b','c','n1','wr1','r1','pf1','t1','n2','wr2','r2','pf2','t2']
D=pd.read_parquet('grid4_all.parquet',columns=BASE)
D['ok']=(D.n1>=30)&(D.n2>=20); D['pass']=D.ok&(D.t1>=2)&(D.t2>=2)
S={}
okD=D[D.ok]
L=okD.assign(p=(okD.r1>0)&(okD.r2>0)).groupby(['m','tf','kind'],observed=True).agg(c=('pass','size'),ps=('pass','sum'),pos=('p','mean')).reset_index()
S['bytf']=[[x.m,int(x.tf),x.kind,int(x.c),int(x.ps),r(x.pos)] for x in L.itertuples()]
cols=['m','tf','seq','slot','e','st','t','b','c','n1','wr1','r1','pf1','t1','n2','wr2','r2','pf2','t2']
def rows(df): return [[x.m,int(x.tf),int(x.seq),int(x.slot),int(x.e),int(x.st),int(x.t),int(x.b),int(x.c),int(x.n1),r(x.wr1),r(x.r1),r(x.pf1,2),r(x.t1,2),int(x.n2),r(x.wr2),r(x.r2),r(x.pf2,2),r(x.t2,2)] for x in df[cols].itertuples()]
S['passes']=rows(D[(D.kind=='cds')&D['pass']])
B=D[(D.seq==0)&(D.slot==0)]
S['bemean']=[[m,k,int(b),r(a),r(c)] for (m,k,b),(a,c) in B.groupby(['m','kind','b'],observed=True)[['r1','r2']].mean().iterrows()]
S['cxmean']=[[m,k,int(c),r(a),r(b)] for (m,k,c),(a,b) in B.groupby(['m','kind','c'],observed=True)[['r1','r2']].mean().iterrows()]
q=pd.read_parquet('grid4_all.parquet',filters=[('seq','==',0),('slot','==',0),('e','==',0),('c','==',0),('st','in',[0,3,8]),('t','in',[0,5])])
ends=[]
for x in q.itertuples():
    ends.append([x.m,int(x.tf),x.kind,int(x.st),int(x.t),int(x.b),r(x.r1),r(x.r2),r(x.wr1),int(x.n1),int(x.n2)]+[r(getattr(x,f'k{k}')) for k in range(G.NK)]+[r(getattr(x,f'kr{k}'),2) for k in range(G.NK)])
S['ends']=ends
bt=[]
C=D[D.ok&(D.kind=='cds')].assign(mt=lambda d:np.minimum(d.t1,d.t2))
R=D[(D.kind=='rnd')&(D.seq==0)&(D.slot==0)]
for (m,tf),g in C.groupby(['m','tf'],observed=True):
    x=g.sort_values('mt',ascending=False).iloc[0]
    rr=R[(R.m==m)&(R.tf==tf)&(R.e==x.e)&(R.st==(0 if x.st==1 else x.st))&(R.t==x.t)&(R.b==x.b)&(R.c==x.c)]
    bt.append(rows(pd.DataFrame([x]))[0]+([r(rr.r1.iloc[0]),r(rr.r2.iloc[0])] if len(rr) else [None,None]))
S['besttf']=bt
S['names']=dict(EN=G.EN,SN=G.SN,TN=G.TN,BN=G.BN,CN=G.CN,KN=G.KN,SEQ=G.SEQ,NE=G.NE,NST=G.NST,NV=G.NV,NB=G.NB,NC=G.NC)
json.dump(S,open('site4/summary.json','w'),separators=(',',':'))
print(len(json.dumps(S))//1024,'KB passes',len(S['passes']))
for p in S['passes'][:3]: print(p)
for b in bt:
    if b[0]=='NQ': print(b[:9],'RR',b[11],b[16],'t',b[13],b[18],'rand',b[19],b[20])
