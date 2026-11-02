import sys, numpy as np, pandas as pd
sys.path.insert(0,'/home/claude/cf3'); from sim3 import st
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',70); pd.set_option('display.max_rows',400)
def fam(t): return t.split(' |')[0].replace(' 20','').replace(' 80','')
def grid(T, keys, nmin=30):
    rows=[]
    for k,g in T.groupby(keys):
        a=g[g.per=='P1']; b=g[g.per=='P2']; A=st(a.r); B=st(b.r); ra=st(a.r_rand); rb=st(b.r_rand)
        rows.append(list(k)+[A['n'],A['wr'],A['avg'],A['pf'],A['t'],ra['avg'],B['n'],B['wr'],B['avg'],B['pf'],B['t'],rb['avg'],
                    A['n']>=nmin and B['n']>=nmin and A['t']>=2 and B['t']>=2, A['n']>=nmin and B['n']>=nmin and ra['t']>=2 and rb['t']>=2])
    return pd.DataFrame(rows,columns=list(keys)+['n1','wr1','avg1','pf1','t1','rnd1','n2','wr2','avg2','pf2','t2','rnd2','PASS','rPASS'])
