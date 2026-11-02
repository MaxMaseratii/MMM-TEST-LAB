import numpy as np, pandas as pd
pd.set_option('display.width',250); pd.set_option('display.max_rows',500)
D=pd.read_parquet('ibtest.parquet')
def st(x):
    x=x.dropna(); n=len(x)
    if n<2: return pd.Series(dict(n=n))
    pos=x[x>0].sum(); neg=-x[x<=0].sum()
    return pd.Series(dict(n=n,wr=(x>0).mean(),avg=x.mean(),pf=pos/neg if neg>0 else np.nan,t=x.mean()/x.std(ddof=1)*np.sqrt(n)))
def tab(df,by):
    a=df.groupby(by+['per']).r.apply(st).unstack(); b=df.groupby(by+['per']).rr.apply(lambda x: x.mean()).rename('rand')
    a=a.unstack('per'); b=b.unstack('per')
    out=pd.DataFrame({'n1':a[('n','P1')],'wr1':a[('wr','P1')],'r1':a[('avg','P1')],'pf1':a[('pf','P1')],'t1':a[('t','P1')],'rand1':b['P1'],
                      'n2':a[('n','P2')],'wr2':a[('wr','P2')],'r2':a[('avg','P2')],'pf2':a[('pf','P2')],'t2':a[('t','P2')],'rand2':b['P2']})
    return out
# her exact rules: IB 15:00 cutoff wick, FA target mid, TC target IB edge, structure stop
D=D[~((D.variant=='IBc')&(D.kind=='TC'))]
T=tab(D,['m','tf','variant','kind','stop','target'])
print(T.round(2).to_string())
