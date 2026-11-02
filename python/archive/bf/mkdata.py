import pandas as pd, numpy as np, json, bfgrid as B
G=pd.read_parquet('grid_base_all.parquet')
F=pd.read_parquet('found_base.parquet'); FS=pd.read_parquet('found_splits.parquet')
V=pd.read_parquet('variants.parquet'); P=pd.read_parquet('prop.parquet')
def r(v,d=3):
    try:
        v=float(v); return None if not np.isfinite(v) else round(v,d)
    except: return None
D={}
# luck table (slots all + 09:45-12:00)
g01=G[G.slot.isin(['all hours','09:45-12:00'])&(G.n1>=30)&(G.n2>=20)]
L=g01.groupby(['m','kind']).agg(cells=('pass','size'),passes=('pass','sum'),pos=('r1',lambda s: 0)).reset_index()
pos=g01.assign(p=(g01.r1>0)&(g01.r2>0)).groupby(['m','kind']).p.mean().reset_index()
L=L.merge(pos,on=['m','kind'])
D['luck']=[[x.m,x.kind,int(x.cells),int(x.passes),r(x.p)] for x in L.itertuples()]
# all passing rows (any slot)
PS=G[(G.kind=='CDS/CDL')&G['pass']]
cols=['m','tf','slot','side','e','st','t','x','h','n1','wr1','r1','pf1','t1','n2','wr2','r2','pf2','t2']
def rows(df): return [[x.m,int(x.tf),x.slot,x.side,int(x.e),int(x.st),int(x.t),int(x.x),int(x.h),int(x.n1),r(x.wr1),r(x.r1),r(x.pf1,2),r(x.t1,2),int(x.n2),r(x.wr2),r(x.r2),r(x.pf2,2),r(x.t2,2)] for x in df[cols].itertuples()]
D['passes']=rows(PS)
# top 150 per market by min t (slots all / 09:45-12:00), plus controls top for comparison
X=g01.assign(mt=np.minimum(g01.t1,g01.t2))
D['top']=rows(X[X.kind=='CDS/CDL'].sort_values('mt',ascending=False).groupby('m').head(150))
D['topR']=[[*rw[:9], k] + rw[9:] for k, df in (('RANDOM side',X[X.kind=='RANDOM side']),('RANDOM with trend',X[X.kind=='RANDOM with trend'])) for rw in rows(df.sort_values('mt',ascending=False).groupby('m').head(20))]
# classic fixed 1:2 market C2 close by tf / window, both sides, + all windows / filters
c=G[(G.kind=='CDS/CDL')&(G.e==0)&(G.st==0)&(G.t==2)&(G.x==0)&(G.h==0)&(G.side=='both')]
D['classic']=rows(c)
# dimension summaries: share of combos positive in both periods, CDS vs random
def dim(col,names):
    t=g01.assign(p=(g01.r1>0)&(g01.r2>0)).groupby([col,'kind']).p.mean().unstack(1)
    return [[names[i] if names else i]+[r(t.loc[i,k]) for k in ['CDS/CDL','RANDOM side','RANDOM with trend']] for i in t.index]
D['dims']={'Entry':dim('e',B.EN),'Stop':dim('st',B.SN),'Target':dim('t',B.TN),'Exit':dim('x',B.XN),'Half out':dim('h',B.HN)}
# exit comparison: market C2 close, ride, full, avg over fixed and C1 stops, all hours, both sides
xc=G[(G.kind=='CDS/CDL')&(G.e==0)&(G.t==6)&(G.h==0)&(G.side=='both')&(G.slot=='all hours')&(G.st==0)]
D['exits']=[[x.m,int(x.tf),int(x.x),int(x.n1),r(x.wr1),r(x.r1),r(x.t1,2),int(x.n2),r(x.wr2),r(x.r2),r(x.t2,2)] for x in xc.itertuples()]
# slot / filter summary for CDS: share positive both + passes (all combos)
gs=G[(G.kind=='CDS/CDL')]
D['slots']=[[x[0],x[1],r(x[2])] for x in gs.assign(p=(gs.r1>0)&(gs.r2>0)&(gs.n1>=30)&(gs.n2>=20)).groupby('slot').agg(passes=('pass','sum'),pos=('p','mean')).reset_index().itertuples(index=False)]
# foundation summary
s50=F.m.map({'NQ':50,'ES':20,'GC':12,'CL':0.5})
fo=F.groupby(['m','tf','kind','per']).agg(n=('p10R','size'),bc=('bc_opp','mean'),nbc=('bc_nbc','mean'),p1=('p1R','mean'),p3=('p3R','mean'),p5=('p5R','mean'),p10=('p10R','mean'),
    sd=('p10R','std'),r1=('r1','mean'),r2=('r2','mean'),r3=('r3','mean'),fx=('fix12','mean'),fsd=('fix12','std')).reset_index()
fo['t10']=fo.p10/fo.sd*np.sqrt(fo.n); fo['ft']=fo.fx/fo.fsd*np.sqrt(fo.n)
D['found']=[[x.m,int(x.tf),x.kind,x.per,int(x.n),r(x.bc,2),r(x.nbc,2),r(x.p1),r(x.p3),r(x.p10),r(x.t10,2),r(x.r1),r(x.r2),r(x.r3),r(x.fx),r(x.ft,2)] for x in fo.itertuples()]
D['fsplit']=[[x.m,int(x.tf),x.split,int(x.nP1),r(x.p10P1),r(x.tP1,2),r(x.fixP1),r(x.fixtP1,2),int(x.nP2),r(x.p10P2),r(x.tP2,2),r(x.fixP2),r(x.fixtP2,2)] for x in FS.itertuples()]
D['vars']=[[x.variant,x.m,int(x.cells),int(x.passes),r(x.pos_both),r(x.best_min_t,2),r(x.classic_r1),r(x.classic_r2),int(x.signals)] for x in V.itertuples()]
D['prop']=[[x.setup,x.rule,x.per,r(x.n,0),r(x.wr),r(x.avg),r(x.pf,2),r(x.t,2),r(x.dd,1),r(x.ml,0),r(x.usd_month_1micro,0)] for x in P.itertuples()]
D['names']={'E':B.EN,'S':B.SN,'T':B.TN,'X':B.XN,'H':B.HN}
json.dump(D,open('sheet_data.json','w'),separators=(',',':'))
print(len(json.dumps(D)), len(D['passes']), len(D['top']))
