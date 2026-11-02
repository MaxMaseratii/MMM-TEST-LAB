import numpy as np, gzip, base64, json, bfgrid3 as G
TFS=[1,2,3,5,10,15,60,240]
def stats(A):
    n=A[...,0]; w=A[...,1]; sm=A[...,2]; sq=A[...,3]
    with np.errstate(all='ignore'):
        av=sm/n; sd=np.sqrt(np.maximum(sq/n-av*av,0)*n/np.maximum(n-1,1)); t=av/sd*np.sqrt(n); wr=w/n
        pf=A[...,4]/A[...,5]
    return n,wr,av,t,pf
def sc(a,f,lim=32767):
    return np.clip(np.round(np.nan_to_num(a*f,nan=0,posinf=lim,neginf=-lim)),-lim,lim).astype(np.int16)
tot=0
for m in ['NQ','ES','GC','CL']:
    for tf in TFS:
        try: Z=np.load(f'g3/{m}_{tf}.npz')
        except FileNotFoundError: continue
        nb=b''; qb=b''
        for kind in ('cds','rnd'):
            A=Z[kind].astype(np.float64)
            if kind=='rnd': A=A[:1,:,:1]
            A=np.moveaxis(A,1,-2)
            n,wr,av,t,pf=stats(A)
            nb+=n.astype(np.uint32).tobytes(); qb+=np.stack([sc(wr,1e4),sc(av,1e3),sc(t,100)],-1).tobytes()
        gz=gzip.compress(nb+qb,9); b=base64.b64encode(gz); open(f'site3/{m}_{tf}.txt','wb').write(b); tot+=len(b)
print(tot/1e6,'MB total')
