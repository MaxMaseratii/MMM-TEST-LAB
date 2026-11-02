import pandas as pd, numpy as np, glob, os
rows=[]
names=['base']+[os.path.basename(f)[9:].rsplit('_',1)[0] for f in sorted(glob.glob('grid_var_*_NQ.parquet'))+sorted(glob.glob('grid_var_*_ES.parquet'))]
names=list(dict.fromkeys(names))
for nm in names:
    for m in ['NQ','ES','GC','CL']:
        f=f'grid_base_{m}.parquet' if nm=='base' else f'grid_var_{nm}_{m}.parquet'
        if not os.path.exists(f): continue
        G=pd.read_parquet(f); G=G[(G.kind=='CDS/CDL')&G.slot.isin(['all hours','09:45-12:00'])]
        ok=(G.n1>=30)&(G.n2>=20)
        ps=ok&(G.t1>=2)&(G.t2>=2)&(G.r1>0)&(G.r2>0)
        pos=ok&(G.r1>0)&(G.r2>0)
        c=G[(G.e==0)&(G.st==0)&(G.t==2)&(G.x==0)&(G.h==0)&(G.side=='both')&(G.slot=='all hours')]
        rows.append(dict(variant=nm,m=m,cells=int(ok.sum()),passes=int(ps.sum()),pos_both=float(pos.sum()/max(1,ok.sum())),
                         best_min_t=float(np.minimum(G.t1,G.t2)[ok].max()),
                         classic_r1=float((c.r1*c.n1).sum()/c.n1.sum()), classic_r2=float((c.r2*c.n2).sum()/c.n2.sum()), signals=float(c.n1.sum()+c.n2.sum())))
V=pd.DataFrame(rows); V.to_parquet('variants.parquet')
pd.set_option('display.width',250); print(V.round(3).to_string())
