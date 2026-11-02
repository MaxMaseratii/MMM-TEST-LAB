import numpy as np, pandas as pd, bfgrid3 as G
pd.set_option('display.width',250); pd.set_option('display.max_rows',400)
D=pd.read_parquet('grid3_all.parquet', filters=[('seq','==',0),('slot','==',0)])
O=pd.read_parquet('grid2_NQ.parquet'); O=O[(O.kind=='CDS/CDL')&(O.side=='both')&(O.slot=='all hours')&(O.w==0)&(O.e==0)&(O.t==0)&(O.x==0)]
q=D[(D.m=='NQ')&(D.kind=='cds')&(D.e==0)&(D.t==0)&(D.x==0)]
rows=[]
for st in (0,3,5,7,8):
  for tf in [1,2,3,5,10,15,60,240]:
    o=O[(O.tf==tf)&(O.st==st)].iloc[0]
    def g(b,c):
        r=q[(q.tf==tf)&(q.st==st)&(q.b==b)&(q.c==c)].iloc[0]; return f"{r.r1:+.2f}/{r.r2:+.2f} ({r.wr1*100:.0f}%,n{r.n1:.0f})"
    rows.append([G.SN[st],tf,f"{o.r1:+.2f}/{o.r2:+.2f} (n{o.n1:.0f})",g(0,0),g(1,0),g(0,1),g(1,1),g(2,1)])
print(pd.DataFrame(rows,columns=['stop','tf','old no rules','1 at a time','+BE .25R','+close C2 open','ALL (BE.25+C2open)','ALL BE.5']).to_string(index=False))
