import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim3 import cfg3
from final import st
CN=cfg3(); MONTHS={'old':36.5,'fresh':2.9}
S3=[('F.M16','5m','H1 UPG|2 BCs (validated) then retest|all seq|A1 next open|held|all',('Sbox','RUN','BE+fees after 1 BC','3 re-entries'),
     'H1 UPG gap touched, level held → 5m reversal box','box → a 2nd BC first (valid) → retest → BC out → next open · re-enter up to 3 times on touch → BC out while the box holds'),
    ('F.M17','5m','M15 UPG|1 BC (break only)|all seq|A1 next open|any|NY PM 12-16',('Sbox','RUN','BE+fees after 1 BC','3 re-entries'),
     'M15 UPG gap touched → 5m reversal box (12:00–16:00)','retest → BC out → next open · re-enter up to 3 times on touch → BC out while the box holds')]
rows=[]
for code,tf,key,cfg,lvl,ent in S3:
    G=pickle.load(open(f'G3_{tf}.pkl','rb')); c=CN.index(cfg); T={}
    for per in ('old','fresh'):
        E,_=pickle.load(open(f'res2_{per}_{tf}.pkl','rb')); R,NT,PT=pickle.load(open(f'res3_{per}_{tf}.pkl','rb'))
        idx=G[per][key]
        T[per]=pd.DataFrame({'t':E.t.values[idx],'R':R[idx,c].astype(float),'pts':PT[idx,c].astype(float),'dist':np.clip(np.abs(E.px.values[idx]-np.where(E.d.values[idx]==1,E.bot.values[idx],E.top.values[idx]))+0.25,20,50),'nt':NT[idx,c]})
    for per,df in (('2022–25',T['old']),('2026',T['fresh']),('Both',pd.concat([T['old'],T['fresh']]))):
        s=st(df,MONTHS['old'] if per=='2022–25' else MONTHS['fresh'] if per=='2026' else MONTHS['old']+MONTHS['fresh'])
        s['trades_per_setup']=df.nt.mean(); s['no_loss']=(df.R>=-0.001).mean()
        rows.append(dict(code=code,ltf=tf,level=lvl,entry=ent,stop=cfg[0],boxexit='+box exit',target=cfg[1],trail=cfg[2]+' · '+cfg[3],period=per,**s))
S=pd.DataFrame(rows); S.to_parquet('strats3.parquet')
pd.set_option('display.width',300); pd.set_option('display.max_columns',40)
print(S.drop(columns=['level','entry']).round(2).to_string())
