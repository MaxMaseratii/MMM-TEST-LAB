import sys;sys.path.insert(0,'/home/claude/rt/eng')
from core import load
import numpy as np, matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
from collections import Counter
from eng2 import run
d=load('MNQ','1m',['2026-10'])
full=d[d.index>='2026-10-01']
BX,S,ev=run(full)
print('bars',len(full),Counter(e[1][:2] for e in ev),'pending events',sum(1 for e in ev if e[3]))
# duplicate T at same level
Ts=[b for b in BX if b.kind==3]
dup=sum(1 for i,a in enumerate(Ts) for b in Ts[i+1:] if a.pol==b.pol and abs((a.top if a.pol==-1 else a.bot)-(b.top if b.pol==-1 else b.bot))<.1)
print('live T',len(Ts),'dupes',dup,'total boxes',len(BX))
# replay window plot
w0='2026-10-14 08:00';d=d[d.index>=w0][:400]
BX,S,ev=run(d)
fig,ax=plt.subplots(figsize=(22,10));x={t:i for i,t in enumerate(d.index)};w=d.iloc[-150:];x0=x[w.index[0]];R=len(d)+5
for i,(t,r) in enumerate(d.iterrows()):
    if i<x0: continue
    col='#2bd4a4' if r.close>r.open else '#9c27b0'
    ax.plot([i,i],[r.low,r.high],color='k',lw=.6);ax.add_patch(plt.Rectangle((i-.35,min(r.open,r.close)),.7,max(abs(r.close-r.open),.1),color=col))
lo,hi=w.low.min()-5,w.high.max()+5
def nm(b):
    p='Bu' if b.pol==1 else 'Be'
    return {3:('BuPO4' if b.pol==1 else 'BePO4')+' T'+str(b.tier),1:p+'P'+str(b.tier),2:p+'R'+str(b.tier),0:p.lower()+(b.il or 'r')+str(b.tier)}.get(b.kind,b.brk+b.bn)
def dr(b,col,a,right,ctr=False):
    l=max(x.get(b.tL,0),x0-1)
    if right<x0 or b.bot>hi or b.top<lo: return
    ax.add_patch(plt.Rectangle((l-.4,b.bot),right-l,max(b.top-b.bot,.2),color=col,alpha=a,lw=0))
    ax.text((l+right)/2 if ctr else right-1,(b.top+b.bot)/2,nm(b),ha='center' if ctr else 'right',va='center',fontsize=8)
for b in BX:
    if b.kind==0: dr(b,'#EE72E8',.2,R)
for b in BX:
    if b.kind==3:
        ww=[q for q in BX if q.id==b.wife]
        if ww: dr(ww[0],{'CDL':'#01d401','CDS':'#c2185b'}.get(ww[0].brk,'#EE72E8'),.4,x[ww[0].tB],True)
        dr(b,'#E254FF',.8,R)
for k,c in (('idP','#EE72E8'),('idR','#C77DFF')):
    b=[q for q in BX if q.id==S[k]]
    if b: dr(b[0],c,.8,R)
ax.set_xlim(x0-1,R+1);ax.set_ylim(lo,hi)
plt.savefig('look2.png',dpi=80,bbox_inches='tight')
print(ev[-12:])
