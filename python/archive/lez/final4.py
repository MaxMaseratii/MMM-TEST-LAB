import numpy as np, pandas as pd, pickle, sys
sys.path.insert(0,'/home/claude/lez')
from sim2 import cfg_names2
from sim3 import cfg3
from final import st
CN=cfg_names2(); CN3=cfg3(); MONTHS={'old':36.5,'fresh':2.9}
T7=pd.read_parquet('table7.parquet'); T7m=pd.read_parquet('table7m.parquet')
S=[('FVA.M17','15m','ALL UPG gaps|all|wick touch only|all|A1 next open|held','s2',('Sbox','+box exit','TP3','')),
   ('FVA.M18','15m','M15 UPG|all|wick touch only|all|A4 limit at high/low the BC broke|held','s2',('S20','+box exit','TP10','')),
   ('FVA.M19','5m','ALL break boxes CDL/CDS/LD/SD|all|all|box with NBC|A1 next open|any','s2',('Sbox','+box exit','TP2','')),
   ('FVA.M20','15m','ALL UPG gaps|P0 break → touch (nothing between)|all|all|A1 next open|held','s2',('Sbox','+box exit','TP5','')),
   ('FVA.M21','5m','M15 UPG|P2 break → NBC → touch|all|all|A1 next open|any','s3',('S50','TP3','no BE','1 re-entry')),
   ('FVA.M22','1m','M15 I|P7 break → 2nd BC + NBC + opp → touch|closed inside|all|A1 next open|any','s2',('S50','','TP3','BE2'))]
rows=[]
for code,tf,key,kind,cfg in S:
    G=pickle.load(open(f'G7_{tf}.pkl','rb')); T={}
    tb=T7 if kind=='s2' else T7m; rob=float(tb[(tb.ltf==tf)&(tb.key==key)].both.iloc[0])
    for per in ('old','fresh'):
        E,Rm,R3,NT,PT,_=pickle.load(open(f'res4_{per}_{tf}.pkl','rb')); idx=G[per][key]
        px=E.px.values[idx]; edge=E.edge.values[idx]; raw=np.abs(px-edge)+0.25
        if kind=='s2':
            c=CN.index(cfg); r=Rm[idx,c].astype(float); s=cfg[0]
            dist=np.full(len(idx),float(s[1:])) if s[1:].isdigit() else (np.clip(raw,20,50) if s=='Sbox' else np.maximum(raw,10))
            T[per]=pd.DataFrame({'t':E.t.values[idx],'R':r,'pts':r*dist,'dist':dist,'nt':1})
        else:
            c=CN3.index(cfg); s=cfg[0]
            dist=np.full(len(idx),float(s[1:])) if s[1:].isdigit() else np.clip(raw,20,50)
            T[per]=pd.DataFrame({'t':E.t.values[idx],'R':R3[idx,c].astype(float),'pts':PT[idx,c].astype(float),'dist':dist,'nt':NT[idx,c]})
        T[per]=T[per].dropna(subset=['R']).sort_values('t')
    for per,df in (('2022–25',T['old']),('2026',T['fresh']),('Both',pd.concat([T['old'],T['fresh']]))):
        s=st(df,MONTHS['old'] if per=='2022–25' else MONTHS['fresh'] if per=='2026' else MONTHS['old']+MONTHS['fresh'])
        s['trades_per_setup']=df.nt.mean(); s['no_loss']=(df.R>=-0.001).mean(); s['full_loss']=(df.R<=-0.9).mean(); s['small']=((df.R>-0.9)&(df.R<0.5)).mean(); s['avg_win']=df.R[df.R>0].mean(); s['avg_loss']=df.R[df.R<0].mean()
        rows.append(dict(code=code,ltf=tf,key=key,kind=kind,cfg=' | '.join(cfg),rob=rob,period=per,**s))
D=pd.DataFrame(rows); D.to_parquet('strats4.parquet')
pd.set_option('display.width',300); pd.set_option('display.max_columns',40)
print(D.drop(columns=['key']).round(3).to_string())
