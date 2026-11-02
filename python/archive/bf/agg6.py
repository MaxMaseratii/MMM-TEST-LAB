import numpy as np, pandas as pd, glob, bfgrid3 as G
TFS=[1,2,3,5,10,15,60,240]
def frame(m,tf,kind):
    A=np.load(f'g3/{m}_{tf}.npz')[kind].astype(np.float64)   # seq, per, slot, e, st, v, 6
    n=A[...,0]; w=A[...,1]; sm=A[...,2]; sq=A[...,3]; pos=A[...,4]; neg=A[...,5]
    with np.errstate(all='ignore'):
        av=sm/n; sd=np.sqrt(np.maximum(sq/n-av*av,0)*n/np.maximum(n-1,1)); t=av/sd*np.sqrt(n); wr=w/n; pf=pos/neg
    idx=np.indices((3,2,G.NE,G.NST,G.NV)).reshape(5,-1)
    f=lambda a,p: a[:,p].reshape(-1)
    v=idx[4]; ci=v%5; bi=(v//5)%4; xi=(v//20)%2; ti=v//40
    df=pd.DataFrame(dict(m=m,tf=tf,kind=kind,seq=idx[0],slot=idx[1],e=idx[2],st=idx[3],t=ti,x=xi,b=bi,c=ci,
        n1=f(n,0),wr1=f(wr,0),r1=f(av,0),pf1=f(pf,0),t1=f(t,0),n2=f(n,1),wr2=f(wr,1),r2=f(av,1),pf2=f(pf,1),t2=f(t,1)))
    return df[(df.n1>0)|(df.n2>0)]
if __name__=='__main__':
    out=[]
    for fn in sorted(glob.glob('g3/*.npz')):
        m,tf=fn.split('/')[1][:-4].split('_'); tf=int(tf)
        for k in ('cds','rnd'):
            d=frame(m,tf,k)
            for c in d.columns[11:]: d[c]=d[c].astype(np.float32)
            out.append(d)
    D=pd.concat(out,ignore_index=True)
    for c in ('m','kind'): D[c]=D[c].astype('category')
    D.to_parquet('grid3_all.parquet'); print(len(D))
