import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim2 import cfg_names2
from final import st
CN=cfg_names2(); MONTHS={'old':36.5,'fresh':2.9}
def load_res(src,per,tf):
    if src=='B': return pickle.load(open(f'res2_{per}_{tf}.pkl','rb'))
    if src=='O': return pickle.load(open('of_res.pkl','rb'))[(per,tf)]
    if src=='K': return pickle.load(open('ofk_res.pkl','rb'))[(per,tf)]
GF={'B':'G3_{}.pkl','O':'G4_{}.pkl','K':'G5_{}.pkl'}
def full(src,tf,key,cfg):
    G=pickle.load(open(GF[src].format(tf),'rb')); c=CN.index(cfg); T={}
    for per in ('old','fresh'):
        E,R=load_res(src,per,tf); E=E.reset_index(drop=True); idx=G[per][key]
        r=R[idx,c].astype(float); px=E.px.values[idx]; ed=E.edge.values[idx]
        s=cfg[0]
        dist=np.clip(np.abs(px-ed)+0.25,20,50) if s=='Sbox' else (np.maximum(np.abs(px-ed)+0.25,10) if s=='Szone' else np.full(len(idx),float(s[1:])))
        T[per]=pd.DataFrame({'t':E.t.values[idx],'R':r,'pts':r*dist,'dist':dist})
    o=st(T['old'],MONTHS['old']); f=st(T['fresh'],MONTHS['fresh']); b=st(pd.concat([T['old'],T['fresh']]),MONTHS['old']+MONTHS['fresh'])
    return o,f,b
S2=[
 ('F.M10','K','5m','LD|O5 no close back inside for 3 candles → enter|all|all',('Sbox','+box exit','TP10',''),
   '5m MMM PRO f LD (long only)','after the LD, wait 3 candles; if none closed back inside the broken box → enter long at the next open'),
 ('F.M11','K','15m','continuations LD/SD|O5 no close back inside for 3 candles → enter|all|all',('S50','+box exit','TP10','trailOpp'),
   '15m MMM PRO f LD / SD','after the LD/SD, wait 3 candles; if none closed back inside the broken box → enter at the next open'),
 ('F.M12','O','1h','LD|O1 break close → next open|all|all',('Sbox','+box exit','TP5','trailBC'),
   '1h MMM PRO f LD (long only)','enter long at the open after the LD candle'),
 ('F.M13','B','15m','ALL UPG gaps|1 BC (break only)|touch only|A1 next open|held|Asia 18-02',('Sbox','+box exit','TP2',''),
   'any UPG gap touched, level held → 15m reversal box','retest that only touches the box (no close inside) → BC out of the box → next open · Asia 18:00–02:00'),
 ('F.M14','B','5m','H1 UPG|2 BCs (validated) then retest|all seq|A2 limit 50% of entry BC|held|all',('Szone','','TP10',''),
   'H1 UPG gap touched, level held → 5m reversal box','2nd BC first (box valid) → retest → BC out → limit at 50% of that BC'),
 ('F.M15','B','15m','ALL UPG gaps|2 BCs (validated) then retest|touch only|A2 limit 50% of entry BC|any|London 02-08',('S50','+box exit','TP3','trailBC'),
   'any UPG gap touched → 15m reversal box','2nd BC first → retest that only touches → BC out → limit at 50% of that BC · London 02:00–08:00'),
]
if __name__=='__main__':
    rows=[]
    for code,src,tf,key,cfg,lvl,ent in S2:
        o,f,b=full(src,tf,key,cfg)
        for per,s in (('2022–25',o),('2026',f),('Both',b)):
            rows.append(dict(code=code,ltf=tf,level=lvl,entry=ent,stop=cfg[0],boxexit=cfg[1],target=cfg[2],trail=cfg[3],period=per,**s))
    S=pd.DataFrame(rows); S.to_parquet('strats2.parquet')
    pd.set_option('display.width',300); pd.set_option('display.max_columns',40)
    print(S.drop(columns=['level','entry']).round(2).to_string())
