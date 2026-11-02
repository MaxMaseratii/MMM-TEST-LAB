import pandas as pd, numpy as np
OUT='/home/claude/rt/out'
KEY=['period','tf','family','signal','side','entry','stop','target','exit']
def finish(g):
    n=g.trades; avg=g._s/n
    var=(g._s2-n*avg**2)/(n-1).clip(lower=1)
    sd=np.sqrt(var.clip(lower=0))
    g['WR']=g._w/n; g['avgR']=avg; g['PF']=g._gw/g._gl.replace(0,np.nan); g['t']=avg/sd*np.sqrt(n)
    g['fill']=g._fill/g._sig.replace(0,np.nan)
    return g
def combos(d):
    num=['trades','_w','_s','_s2','_gw','_gl','_sig','_fill']
    a=d[d.session.isin(['Asia','NY AM'])].groupby(KEY)[num].sum().reset_index(); a['session']='Asia+NY AM'
    b=d.groupby(KEY)[num].sum().reset_index(); b['session']='All sessions'
    return finish(pd.concat([a,b],ignore_index=True))
if __name__=='__main__':
    d=pd.read_parquet(f'{OUT}/ALL_grid.parquet')
    c=combos(d); c.to_parquet(f'{OUT}/ALL_sess.parquet'); print(len(c))
