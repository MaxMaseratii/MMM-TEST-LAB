import numpy as np, pandas as pd, glob, bfgrid4 as G
def frame(m,tf,kind):
    A=np.load(f'g4/{m}_{tf}.npz')[kind].astype(np.float64)
    n=A[...,0]; w=A[...,1]; sm=A[...,2]; sq=A[...,3]; pos=A[...,4]; neg=A[...,5]
    with np.errstate(all='ignore'):
        av=sm/n; sd=np.sqrt(np.maximum(sq/n-av*av,0)*n/np.maximum(n-1,1)); t=av/sd*np.sqrt(n); wr=w/n; pf=pos/neg
        K=A[...,6:6+G.NK].sum(1)/np.maximum(n.sum(1),1)[...,None]       # exit-kind shares over both periods
        KR=A[...,6+G.NK:].sum(1)/np.maximum(A[...,6:6+G.NK].sum(1),1)    # avg R per exit kind
    idx=np.indices((3,2,G.NE,G.NST,G.NV)).reshape(5,-1)
    f=lambda a,p: a[:,p].reshape(-1)
    v=idx[4]; ci=v%G.NC; bi=(v//G.NC)%G.NB; ti=v//(G.NC*G.NB)
    d=dict(m=m,tf=tf,kind=kind,seq=idx[0],slot=idx[1],e=idx[2],st=idx[3],t=ti,b=bi,c=ci,
        n1=f(n,0),wr1=f(wr,0),r1=f(av,0),pf1=f(pf,0),t1=f(t,0),n2=f(n,1),wr2=f(wr,1),r2=f(av,1),pf2=f(pf,1),t2=f(t,1))
    for k in range(G.NK): d[f'k{k}']=K[...,k].reshape(-1); d[f'kr{k}']=KR[...,k].reshape(-1)
    df=pd.DataFrame(d); return df[(df.n1>0)|(df.n2>0)]
out=[]
for fn in sorted(glob.glob('g4/*.npz')):
    m,tf=fn.split('/')[1][:-4].split('_')
    for k in ('cds','rnd'):
        d=frame(m,int(tf),k)
        for c in d.columns[10:]: d[c]=d[c].astype(np.float32)
        out.append(d)
D=pd.concat(out,ignore_index=True)
for c in ('m','kind'): D[c]=D[c].astype('category')
D.to_parquet('grid4_all.parquet'); print(len(D))
