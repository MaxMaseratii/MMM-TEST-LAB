import sys;sys.path.insert(0,'/home/claude/rt/eng')
from core import load
import pandas as pd, numpy as np, matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
from eng import run
d=load('MNQ','1m',['2026-10'])
d=d[d.index>='2026-10-14 08:00'][:400]
BX,S,ev=run(d)
from collections import Counter
print(len(d),'bars',Counter(e[1][:2] for e in ev),S)
print(ev[:20])
end=d.index[-1]
fig,ax=plt.subplots(figsize=(22,10));x={t:i for i,t in enumerate(d.index)}
w=d.iloc[-140:];xs=np.arange(len(d))
for i,(t,r) in enumerate(d.iterrows()):
    if t<w.index[0]: continue
    col='#2bd4a4' if r.close>r.open else '#9c27b0'
    ax.plot([i,i],[r.low,r.high],color='k',lw=.6);ax.add_patch(plt.Rectangle((i-.35,min(r.open,r.close)),.7,max(abs(r.close-r.open),.1),color=col))
def nm(b):
    pfx=lambda: 'Bu' if b.pol==1 else 'Be'
    if b.kind==3: return ('BuPO4' if b.pol==1 else 'BePO4')+' T'+str(b.tier)
    if b.kind==1: return pfx()+'P'+str(b.tier)
    if b.kind==2: return pfx()+'R'+str(b.tier)
    if b.kind==0: return pfx().lower()+(b.il or 'r')+str(b.tier)
    return b.brk+b.bn
x0=x[w.index[0]]
def dr(b,col,a,right):
    l=max(x.get(b.tL,0),x0-1);r=right
    if r<x0: return
    ax.add_patch(plt.Rectangle((l,b.bot),r-l,b.top-b.bot,color=col,alpha=a,lw=0))
    ax.text(r-1 if b.kind!=4 else (l+r)/2,(b.top+b.bot)/2,nm(b),ha='right' if b.kind!=4 else 'center',va='center',fontsize=8)
R=len(d)+5
for b in BX:
    if b.kind==0: dr(b,'#EE72E8',.2,R)
for b in BX:
    if b.kind==3:
        w_=[q for q in BX if q.id==b.wife]
        if w_: dr(w_[0],'#999999',.35,x[w_[0].tB])
        dr(b,'#E254FF',.8,R)
for k,c in (('idP','#EE72E8'),('idR','#C77DFF')):
    b=[q for q in BX if q.id==S[k]]
    if b: dr(b[0],c,.8,R)
ax.set_xlim(x0-1,R+1);lo,hi=w.low.min(),w.high.max();ax.set_ylim(lo-10,hi+10)
plt.savefig('look.png',dpi=80,bbox_inches='tight')
