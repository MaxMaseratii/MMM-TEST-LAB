import pandas as pd, numpy as np
A=pd.read_parquet('found_base.parquet')
SL=['all','0945-1200','C','A','Asia','London','NYAM','PM','C2 50-75','C2 75-100','C2 100-150','C2 150+','dWith','dAgainst','d50With','res0','res1+','BIG','HTFwith','HTFagainst']
E=A[A.kind=='CDS/CDL']
rows=[]
for (m,tf),g in E.groupby(['m','tf']):
    mk=g['mask'].values.astype(np.int64)
    for k,nm in enumerate(SL):
        x=g[(np.right_shift(mk,k)&1)==1]
        r={'m':m,'tf':tf,'split':nm}
        for p in ('P1','P2'):
            y=x[x.per==p]
            r[f'n{p}']=len(y); r[f'p10{p}']=y.p10R.mean(); r[f't{p}']=y.p10R.mean()/y.p10R.std()*np.sqrt(len(y)) if len(y)>2 else np.nan
            r[f'fix{p}']=y.fix12.mean(); r[f'fixt{p}']=y.fix12.mean()/y.fix12.std()*np.sqrt(len(y)) if len(y)>2 else np.nan
            r[f'R1{p}']=y.r1.mean(); r[f'bc{p}']=y.bc_opp.mean()
        rows.append(r)
F=pd.DataFrame(rows)
F.to_parquet('found_splits.parquet')
pd.set_option('display.width',250)
ok=F[(F.nP1>=30)&(F.nP2>=20)&(F.tP1>=2)&(F.tP2>=2)]
print('splits with move after 10 candles t>=2 both periods:'); print(ok.round(3).to_string())
ok2=F[(F.nP1>=30)&(F.nP2>=20)&(F.fixtP1>=2)&(F.fixtP2>=2)]
print('fixed 1:2 t>=2 both:'); print(ok2.round(3).to_string())
ok3=F[(F.nP1>=30)&(F.nP2>=20)&(F.fixP1>0)&(F.fixP2>0)]
print('fixed 1:2 positive both (count by market):'); print(ok3.groupby('m').size())
print(ok3.sort_values('fixP1',ascending=False).round(3).head(25).to_string())
